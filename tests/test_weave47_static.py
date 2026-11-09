# Weave Phase 4-7（v20a30）靜態測試：1990 抉擇三連——模組／掛點／時間閘／旗名與 NOTES 清單對照／慣例不變
# 用法：python3 tests/test_weave47_static.py [path-to-index.html]
import sys, pathlib, re
root = pathlib.Path(__file__).resolve().parent.parent
p = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else root / 'index.html'
notes_p = root / 'NOTES_V20A30_WEAVE_PHASE4_7_CHOICES_1990.md'
html = p.read_text(encoding='utf-8')
notes = notes_p.read_text(encoding='utf-8') if notes_p.exists() else ''
fails = []
def ok(name, cond):
    print(('PASS' if cond else 'FAIL') + ' ' + name)
    if not cond:
        fails.append(name)

# ---- 模組本體 ----
ok('phase marker v20a30', 'Weave Phase 4-7（v20a30）' in html)
for sym in ['const CHOICE47_SEASON_IDX', 'const CHOICE47_NODES', 'const CHOICE47_DEFS',
            'function choice47SeasonReached(', 'function choice47Answered(',
            'function choice47Available(', 'function choice47ActionsAt(',
            'function choice47Play(', 'function choice47FamilyCardHtml(',
            'const EXODUS_GIGS', 'function mergeExodusGigs(']:
    ok('symbol present: ' + sym, sym in html)

m = re.search(r'const CHOICE47_NODES = \{(.*?)\n\};', html, re.S)
nodes = m.group(1) if m else ''
ok('CHOICE47_NODES block extractable', bool(nodes))
ok('node F4_stay_mind present', re.search(r'^\s*F4_stay_mind: \{', nodes, re.M) is not None)
ok('node G4_family_job present', re.search(r'^\s*G4_family_job: \{', nodes, re.M) is not None)
ok('F4 title 何生問：走定留', 'title:"何生問：走定留"' in nodes)
ok('G4 title 屋企有話同你講', 'title:"屋企有話同你講"' in nodes)
ok('F4 asks 有冇諗過走', '有冇諗過走' in nodes)
ok('G4 copy: 表叔／銀行／文職', '表叔' in nodes and '銀行' in nodes and '文職' in nodes)
ok('G4 copy: 阿媽語氣（唔好餓親）', '唔好餓親' in nodes)
# 五個抉擇一律零 stats（只寫旗＋notes）
ok('nodes have exactly 5 flag-writing choices', nodes.count('effects:{ flags:[') == 5)
ok('nodes choices carry NO stats (餌唔改數值)', 'stats:' not in nodes and 'statsApplied' not in nodes)

# ---- 旗名清單：index 同 NOTES 交叉對照 ----
FLAGS = ['flag_stay_mind', 'flag_leave_mind', 'flag_undecided_mind',
         'flag_family_job_accept', 'flag_family_job_decline']
for f in FLAGS:
    ok('flag in nodes: ' + f, ('"' + f + '"') in nodes)
    ok('flag in NOTES list: ' + f, f in notes)
ok('undecided handling documented in NOTES', 'flag_undecided_mind' in notes and '中性' in notes)

# ---- 時間閘（DEFS）----
d = re.search(r'const CHOICE47_DEFS = \{(.*?)\n\};', html, re.S)
defs = d.group(1) if d else ''
ok('CHOICE47_DEFS block extractable', bool(defs))
f4line = next((ln for ln in defs.splitlines() if 'F4_stay_mind:' in ln), '')
g4line = next((ln for ln in defs.splitlines() if 'G4_family_job:' in ln), '')
ok('F4 gate: 1990 夏 @ agency_ho', 'year:1990' in f4line and 'season:"夏"' in f4line and 'loc:"agency_ho"' in f4line)
ok('G4 gate: 1990 冬', 'year:1990' in g4line and 'season:"冬"' in g4line)
ok('exodus gigs gate: 1990 秋', 'choice47SeasonReached(1990, "秋")' in html)
ok('season gate via yearSeasonNow', 'yearSeasonNow()' in html[html.index('function choice47SeasonReached('):html.index('function choice47SeasonReached(') + 700])

# ---- 掛點 ----
ok('openLoc hook: choice47ActionsAt iterated',
   'choice47ActionsAt(L.id).forEach' in html)
ok('openLoc hook AFTER DualMeet block',
   html.index('DualMeet.actionsAt(L.id).forEach') < html.index('choice47ActionsAt(L.id).forEach'))
ok('openLoc hook plays via choice47Play', 'choice47Play(act.id)' in html)
ok('debt pane: choice47Html composed after family cards',
   'banner+famCardsHtml+choice47Html+cardHtml' in html)
seg_start = html.index('function renderDebtPane(')
seg = html[seg_start:html.index('\nfunction ', seg_start + 10)]
onclick_seg = seg[seg.index('box.onclick=(ev)=>{'):] if 'box.onclick=(ev)=>{' in seg else ''
ok('debt pane onclick: data-choice47 branch present', '[data-choice47]' in onclick_seg)
ok('debt pane onclick: choice47 branch BEFORE repay lookup',
   bool(onclick_seg) and onclick_seg.index('[data-choice47]') < onclick_seg.index('closest(".debt-repay-btn")'))
ok('debt pane onclick: plays via choice47Play', 'choice47Play(nid)' in onclick_seg)
ok('family card html: data-choice47 button for G4',
   'data-choice47="G4_family_job"' in html and 'data-choice47-card="G4_family_job"' in html)
ok('gigs hook: mergeExodusGigs called in board fn', 'mergeExodusGigs(); }catch(_xg){}' in html)
ok('gigs hook AFTER mergeRivalGigs call',
   html.index('mergeRivalGigs(); }catch(_rg){}') < html.index('mergeExodusGigs(); }catch(_xg){}'))

# ---- 空位通告 ----
g = re.search(r'const EXODUS_GIGS = \[(.*?)\n\];', html, re.S)
gigs = g.group(1) if g else ''
ok('EXODUS_GIGS block extractable', bool(gigs))
for gid, loc, pay in [('gig_exodus_tv_senior', 'tvb_longmen', 'payExact:3300'),
                      ('gig_exodus_film_hand', 'film_harbour', 'payExact:2900')]:
    ok('gig present: ' + gid, ('id:"' + gid + '"') in gigs)
    ok('gig ' + gid + ' loc ' + loc, ('loc:"' + loc + '"') in gigs)
    ok('gig ' + gid + ' ' + pay, pay in gigs)
    ok('gig id in NOTES list: ' + gid, gid in notes)
ok('all five gigs tier 中 (v20a36 F7: exodus 2->5)', gigs.count('tier:"中"') == 5)
ok('gig copy: 移民空位 framing', '移民' in gigs and '移民空位' in gigs)
ok('gig tv copy: 原班兩個移民', '原班兩個資深臨記一齊移民' in gigs)
ok('gig film copy: 武師移民加拿大', '移民去咗加拿大' in gigs)

# ---- 玩家面真名／禁用詞掃描（新模組區塊，去註解） ----
mod_start = html.index('/* ===== Weave Phase 4-7（v20a30）')
mod_end = html.index('const MERGE_FRAGS = [')
mod = re.sub(r'/\*.*?\*/', '', html[mod_start:mod_end], flags=re.S)
for w in ['張國榮', '陳百強', '梅艷芳', '周潤發', '劉德華', '關海媚', 'Ho哥', 'Ho 哥']:
    ok('module player text free of banned: ' + w, w not in mod)

# ---- 慣例不變 ----
ok('SAVE key unchanged', 'starVolunteer_map_v19w' in html)
ok('softRev unchanged', 'softRev=s108' in html)
ok('version marker v20a30', 'v20a30' in html)
ok('NOTES file present', bool(notes))

print('FAILURES: ' + ' | '.join(fails) if fails else 'ALL PASS')
sys.exit(1 if fails else 0)
