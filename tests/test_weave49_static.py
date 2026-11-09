# Weave Phase 4-9 靜態測試（v20a32）：預兆系統——軌跡分類＋三渠道呈現接駁點
import sys, re
html = open(sys.argv[1] if len(sys.argv)>1 else 'index.html', encoding='utf-8').read()
fails = []
def ok(name, cond):
    if not cond: fails.append(name)
    print(('PASS' if cond else 'FAIL')+' '+name)

ok('trajectoryOf49 exists', 'function trajectoryOf49(' in html)
ok('trajTagCounts49 exists', 'function trajTagCounts49(' in html)
ok('newspaperTrajRef49 exists', 'function newspaperTrajRef49(' in html)
ok('hoIntroLine49 exists', 'function hoIntroLine49(' in html)
ok('wrapTrajNotePool49 exists', 'function wrapTrajNotePool49(' in html)
ok('tag sets const exists', 'const TRAJ49_TAG_SETS' in html)
ok('paper ref table exists', 'const TRAJ_PAPER_REF49' in html)
ok('ho intro lines exist', 'const HO_INTRO_LINES49' in html)
ok('wrap notes exist', 'const TRAJ_WRAP_NOTES49' in html)

# 報紙接駁：FaceLines 單點替換＋評語附加
ok('FaceLines hooks traj ref', 'newspaperTrajRef49(trajectoryOf49(), nameTier)' in html)
ok('FaceLines appends wrap note from pool', 'notePool49' in html and 'wrapTrajNotePool49()' in html)
ok('wrap note gated on named+', 'nameTier!=="anon" && typeof wrapTrajNotePool49==="function"' in html)

# 何生接駁：tier 池 traj 桶＋pickNpcLine 入池
ok('npcTierPool has traj bucket', 'insider:[], traj:[]' in html)
ok('npcTierPool pushes intro conditionally', 'out.traj.push(hl)' in html and 'npcId==="agent"' in html)
ok('pickNpcLine adds tp.traj', 'tp.traj && tp.traj.length' in html)

# 文案齊全（五軌 × 三渠道關鍵字眼）
for w in ['人氣偶像阿偉', '當紅小生阿偉', '金牌甘草阿偉', '幕後能手阿偉', '江湖味阿偉',
          '穩陣綠葉阿偉', '幕後幫手阿偉']:
    ok('paper ref wording: '+w, w in html)
for w in ['第時唔得了', '實冇死', '小心啲用', '人脈，而家貴過我']:
    ok('ho intro wording: '+w, w in html)
for w in ['主角相', '唔使睇住', '有火', '邊度都食得開']:
    ok('wrap note keyword: '+w, w in html)

# 邊界：今步（4-9）唔寫結局判定函數——判定留畀 4-10。
# v20a33 申報：4-10 已按規劃落地 resolveEnding410（喺 4-10 區塊，唔喺 4-9 區塊），
# 原斷言「全檔冇 resolver」按新現實收窄到「4-9 區塊內冇 resolver」，邊界語義（預兆≠判定）保留不變。
_m49 = re.search(r'Weave Phase 4-9.*?Weave Phase 4-10', html, re.S)
ok('no ending resolver in this step', 'function resolveEnding' not in (_m49.group(0) if _m49 else ''))

# 4-9 區塊內唔准真藝名（玩家面永禁；靈感對照只限 DEV 內部）
m = re.search(r'Weave Phase 4-9.*?function pickNpcLine', html, re.S)
block = m.group(0) if m else ''
ok('4-9 block found', len(block) > 1000)
for banned in ['張國榮', '陳百強', '梅艷芳', '周潤發', '劉德華', '林青霞']:
    ok('no real star name in 4-9 block: '+banned, banned not in block)

# 慣例不變
ok('name tier thresholds unchanged', 'PAPER_NAME_TIER_NAMED = 15' in html and 'PAPER_NAME_TIER_TITLED = 40' in html)
ok('SAVE key unchanged', 'starVolunteer_map_v19w' in html)
ok('softRev unchanged', 's108' in html)

print('\nFAILED: '+' | '.join(fails) if fails else '\nALL PASS')
sys.exit(1 if fails else 0)
