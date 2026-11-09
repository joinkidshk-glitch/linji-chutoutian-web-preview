# Weave Phase 4-2（v20a25）靜態測試：favorLedger 接線＋鏈 F 第 2 拍＋慣例不變
# 用法：python3 tests/test_weave42_static.py [path-to-index.html]
import sys, pathlib
p = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else pathlib.Path(__file__).resolve().parent.parent / 'index.html'
html = p.read_text(encoding='utf-8')
fails = []
def ok(name, cond):
    print(('PASS' if cond else 'FAIL') + ' ' + name)
    if not cond:
        fails.append(name)

# 帳本本體
ok('favorLedger field in fresh state', 'favorLedger:{ settled:0, credits:0, exodus:[], counted:{} }' in html)
ok('mockCredits field in fresh state', 'mockCredits:[]' in html)
ok('ensureFavorLedger defined', 'function ensureFavorLedger(' in html)
ok('backfill marker __bf', '__bf' in html)
ok('backfill skips void_expired (only repaid_help/closed_other)', 'r==="repaid_help" || r==="closed_other"' in html)
ok('note settled defined', 'function favorLedgerNoteSettled(' in html)
ok('note credit defined', 'function favorLedgerNoteCredit(' in html)
ok('counts helper defined', 'function favorLedgerCounts(' in html)
ok('backfill source upgrade in note', 'indexOf("backfill_")===0' in html)

# 結清路徑掛點
ok('hook: applyMockAsk ledger note', 'favorLedgerNoteSettled(debt.id, isTutorial ? "closed_other"' in html)
ok('hook: repaid_help note', 'favorLedgerNoteSettled(d.id, "repaid_help")' in html)
ok('hook: closed_other fallback note', 'favorLedgerNoteSettled(FAVOR_DUE_CFG.debtId, "closed_other")' in html)
ok('hook: void has no note (comment documents decision)', '作廢唔計入帳本 settled' in html)
ok('hook: advanceDay exodus tick', 'exodusFenTick()' in html)
ok('hook: ensureMockJournal ledger ensure', 'ensureFavorLedger(); }catch' in html)
ok('hook: ensureMockJournal fen seed', 'seedExodusFenPair(); }catch' in html)

# 鏈 F 第 2 拍
ok('fen debt seed id', 'id:"debt_fen_standin"' in html)
ok('fen credit seed id', 'id:"credit_fen_rescue"' in html)
ok('fen creditor uses LIVE display name', 'creditor:"副導演芬姐"' in html and 'debtor:"副導演芬姐"' in html)
ok('fen intel frag id', 'id:"rumor_fen_exodus_tip"' in html)
ok('intel frag NOT in MERGE_PAIRS', 'rumor_fen_exodus_tip' not in html.split('const MERGE_PAIRS')[1].split('];')[0] if 'const MERGE_PAIRS' in html else False)
ok('exodus tick defined', 'function exodusFenTick(' in html)
ok('exodus gate: 1989 summer or catch-up', 'ys.year===1989 && ys.season==="夏") || ys.year>=1990' in html)
ok('seed gate: year>=1989', 'yearSeasonNow().year < 1989' in html)
ok('write-off source tag', '"exodus_writeoff"' in html)
ok('exodus list push', 'L.exodus.indexOf(c.id)<0' in html)

# 絕響渲染／排除
ok('CSS exodus grey', '.debt-row.debt-exodus{ opacity:.55; filter:grayscale(1) }' in html)
ok('CSS tone 絕響', '.debt-status[data-tone="絕響"]' in html)
ok('render: credit row class', 'credit-row' in html and 'data-credit-id' in html)
ok('render: 人已不在香港 copy', '人已不在香港' in html)
ok('debtStatusLabel passes 絕響', '"絕響":1' in html)
ok('DEBT_FUZZY has 絕響', '"絕響":"人已不在香港' in html)
ok('favorPressure excludes 絕響', 'd.status!=="絕響" && debtStatusLabel' in html)
ok('allDebtsForRepay excludes 絕響', 'if(d.status==="絕響") return;' in html)

# 慣例不變
ok('SAVE key unchanged', 'starVolunteer_map_v19w' in html)
ok('softRev unchanged', 's110' in html)
ok('no real artist names in new copy', all(x not in html.split('EXODUS_FEN_INTEL')[1].split('};')[0] for x in ['張國榮','陳百強','梅艷芳','周潤發']))

print('\nFAILED: ' + ' | '.join(fails) if fails else '\nALL PASS')
sys.exit(1 if fails else 0)
