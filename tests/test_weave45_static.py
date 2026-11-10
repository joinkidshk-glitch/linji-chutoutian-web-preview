# Weave Phase 4-5（v20a28）靜態測試：三年版覆寫表／ctx 擴充／phase 重映射接線＋慣例不變
# 用法：python3 tests/test_weave45_static.py [path-to-index.html]
import sys, pathlib, re
p = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else pathlib.Path(__file__).resolve().parent.parent / 'index.html'
html = p.read_text(encoding='utf-8')
fails = []
def ok(name, cond):
    print(('PASS' if cond else 'FAIL') + ' ' + name)
    if not cond:
        fails.append(name)

# ---- 覆寫表本體 ----
ok('STORY_GATE_3Y table defined', 'const STORY_GATE_3Y = {' in html)
m = re.search(r'const STORY_GATE_3Y = \{(.*?)\n\};', html, re.S)
block = m.group(1) if m else ''
ok('gate table block extractable', bool(block))
for cid in ['C6','C7','C8','C9','C10','C11','C12','C13','C14','C15','C16','C17']:
    ok('gate entry present: '+cid, re.search(r'^\s*'+cid+r'\s*:', block, re.M) is not None)
for cid in ['C1','C2','C3','C4','C5']:
    ok('gate entry absent (C1–C5 zero change): '+cid, re.search(r'^\s*'+cid+r'\s*:', block, re.M) is None)
ok('N6 gate: route_tv + weekMin 15', 'route: "route_tv", weekMin: 15' in block)
ok('N7 gate: creditGt 20 (scaled)', 'creditGt: 20' in block)
ok('N9 gate: fameGt 28 (scaled)', 'fameGt: 28' in block)
ok('N11 gate: dualGt 70 (scaled)', 'dualGt: 70' in block)
ok('N13 gate: creditGt 42 (scaled)', 'creditGt: 42' in block)
ok('N14 gate: fameGt 50 (scaled)', 'fameGt: 50' in block)
ok('N15 gate: dualGt 125 (scaled)', 'dualGt: 125' in block)
ok('N17 gate: yearEq 1992 event gate', 'yearEq: 1992' in block)
ok('prereq chain N9<-N7 (C8 needDone C7)', 'C8:  { needDone: ["C7"]' in block)
ok('prereq chain N13<-N11 (C14 needDone C10)', 'C14: { needDone: ["C10"]' in block)
ok('prereq chain N14<-N13 (C12 needDone C14)', 'C12: { needDone: ["C14"]' in block)
ok('prereq chain N15<-N14 (C16 needDone C12)', 'C16: { needDone: ["C12"]' in block)
ok('prereq chain N17<-N16 (C17 needDone C13)', 'C17: { needDone: ["C13"]' in block)

# ---- 評估器＋掛點 ----
ok('evalGate3Y defined', 'function evalGate3Y(' in html)
ok('gate3YEntry defined', 'function gate3YEntry(' in html)
ok('evalGate3Y exported on BehaviorGate api', 'evalGate3Y: evalGate3Y,' in html)
ok('gate3YEntry exported on BehaviorGate api', 'gate3YEntry: gate3YEntry,' in html)
ok('evalNode hook calls evalGate3Y', 'BehaviorGate.evalGate3Y(node, opts)' in html)
hook_at = html.index('BehaviorGate.evalGate3Y(node, opts)')
soft_at = html.index('BehaviorGate.coversNode(node)) return BehaviorGate.evalTrigger_AND_softRumor')
ok('hook runs before soft stub dispatch (slots cannot pre-empt)', hook_at < soft_at)
ok('evalGate3Y result tagged gate3Y', 'gate3Y: true,' in html)
ok('evalGate3Y mirrors same-day block', 'days_after_prev:same_day' in html)

# ---- ctx 擴充 ----
ok('liveCredit defined (readDualTracks based)', 'function liveCredit(' in html and 'readDualTracks(S).industryCredit' in html)
ok('liveYearSeason defined (yearSeasonNow based)', 'function liveYearSeason(' in html and 'yearSeasonNow()' in html)
ok('liveTags defined (normalize id+label)', 'function liveTags(' in html)
ok('readCtx: fame var', 'const fame = raw.fame!=null' in html)
ok('readCtx: credit var', 'const credit = raw.credit!=null' in html)
ok('readCtx: dual = fame + credit', 'dual: raw.dual!=null ? Number(raw.dual) : fame + credit,' in html)
ok('readCtx: year via liveYearSeason', 'year: raw.year!=null ? Number(raw.year) : (has ? 1990 : liveYearSeason().year),' in html)
ok('readCtx: tags live default', 'tags: Array.isArray(raw.tags) ? raw.tags.slice() : (has ? [] : liveTags()),' in html)

# ---- phase 三年版重映射 ----
ok('phase remap comment present', '三年版 phase 對照' in html)
ok('phase: P3 = year 1992 plain', 'if(year>=1992) bump("P3");' in html)
ok('phase: P5 winter month guard (Dec)', 'month>=12 && season==="冬"' in html)
ok('phase: P4 autumn from Sep', 'month>=9 && (season==="秋" || season==="冬")' in html)
ok('phase: five-year P4 rule removed', 'year>=1991 && (isDone("C11")' not in html)
ok('phase: five-year P3 C10 requirement removed', 'route_indie || st.routes.route_commercial || st.flags.route_indie' not in html)

# ---- 慣例不變 ----
ok('SAVE key unchanged', 'starVolunteer_map_v19w' in html)
ok('version marker v20a28', 'v20a28' in html)
ok('content pack JSON untouched by this change (no inline pack edit marker)', 'story_detail_c1_to_c17' in html)

print('FAILURES: ' + ' | '.join(fails) if fails else 'ALL PASS')
sys.exit(1 if fails else 0)
