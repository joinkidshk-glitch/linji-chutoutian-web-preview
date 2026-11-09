# Weave Phase 4-3（v20a26）靜態測試：鏈 G 屋企債接線＋排除點＋慣例不變
# 用法：python3 tests/test_weave43_static.py [path-to-index.html]
import sys, pathlib
p = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else pathlib.Path(__file__).resolve().parent.parent / 'index.html'
html = p.read_text(encoding='utf-8')
fails = []
def ok(name, cond):
    print(('PASS' if cond else 'FAIL') + ' ' + name)
    if not cond:
        fails.append(name)

# 屋企債本體
ok('family debt id const', 'const FAMILY_HOME_DEBT_ID = "debt_family_home"' in html)
ok('family cycles defined (4 rotating bills)', html.count('title:"今個月家用"') == 1 and 'title:"今期幫補交租"' in html and 'title:"阿媽覆診藥費"' in html and 'title:"屋企換雪櫃嗰份"' in html)
ok('family creditor is 屋企／阿媽', 'creditor:"屋企／阿媽"' in html)
ok('family state helper defined', 'function ensureFamilyHomeState(' in html)
ok('family seed fn defined', 'function ensureFamilyHomeDebt(' in html)
ok('family paid note fn defined', 'function noteFamilyHomePaid(' in html)
ok('family settle lines fn defined', 'function familyHomeSettleLines(' in html)
ok('family attitude fn defined', 'function familyAttitudeLine(' in html)
ok('seed pushes status 未到期, no dueDay in seed', 'status:"未到期", familyHome:true' in html)

# 掛點
ok('hook: ensureMockJournal seeds family debt', 'ensureFamilyHomeDebt(); }catch(_e){}' in html)
ok('hook: advanceDay reseeds on month rollover', 'ensureFamilyHomeDebt(); }catch(_fh){}' in html)
ok('hook: settleWeek consumes family flavor', 'familyHomeSettleLines()' in html)
ok('hook: applyMockAsk family branch before ledger note', 'debt.id==="debt_family_home")' in html and 'noteFamilyHomePaid(); }catch(_fh){}' in html)
ok('hook: renderDebtPane family-attitude note in card', 'family-attitude' in html and 'familyAttitudeLine()' in html)

# 排除清單（明確排除，唔靠 status 巧合）
ok('exclude: favorPressure skips family debt', 'd.id!=="debt_family_home" && d.status!=="絕響"' in html)
ok('exclude: overdue lock skips family debt', 'if(d.id==="debt_family_home") return false;' in html)
ok('exclude: favorLedgerCounts openDebts skips family debt', 'd.id!=="debt_family_home" && d.status!=="絕響"' in html)

# 家人態度三段原文齊全
ok('attitude anon copy', '做臨記唔係辦法' in html)
ok('attitude named copy', '報紙有寫你個名' in html and '唔好俾人呃先好' in html)
ok('attitude titled copy', '我個仔上報紙' in html)
ok('attitude borrows newspaperNameTier', 'newspaperNameTier()' in html.split('function familyAttitudeLine(')[1].split('}')[0] if 'function familyAttitudeLine(' in html else False)

# flavor 兩條
ok('seed flavor copy', '屋企人催數，從來唔出聲' in html)
ok('paid flavor copy', '煲多咗個湯' in html)

# 慣例不變＋玩家面守則
ok('SAVE key unchanged', 'starVolunteer_map_v19w' in html)
ok('softRev unchanged', 's108' in html)
fam_block = html.split('const FAMILY_HOME_CYCLES')[1].split('];')[0] if 'const FAMILY_HOME_CYCLES' in html else ''
ok('no real artist names in family copy', all(x not in fam_block for x in ['張國榮','陳百強','梅艷芳','周潤發','劉德華']))

print('\nFAILED: ' + ' | '.join(fails) if fails else '\nALL PASS')
sys.exit(1 if fails else 0)
