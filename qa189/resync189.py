# v20a189 resync：index.html 淨 +34 行（accel-link CSS +15 @~1831／day-res 92dvh media +10 @~3235／
#   hint 刪除 -10 @37990／soft map 掣 +3 @38006／accel link push +12 @38009／day-res class +4 @38399），
#   8 檔靜態測試行號釘純漂移。用 difflib 對位 pristine main (dcf1b72) vs 現行 index.html，
#   逐個錨點核實內容逐字相同，先至更新測試檔釘行（唔靠心算 shift）。
# 用法：python3 qa189/resync189.py
import difflib, subprocess, sys

old = subprocess.check_output(['git', 'show', 'main:index.html'], text=True).split('\n')
new = open('index.html', encoding='utf-8').read().split('\n')
print('old newlines %d / new newlines %d (net %+d)' % (len(old) - 1, len(new) - 1, len(new) - len(old)))

# old(1-based) -> new(1-based)，只限 equal block 內嘅行
mapping = {}
sm = difflib.SequenceMatcher(a=old, b=new, autojunk=False)
for tag, i1, i2, j1, j2 in sm.get_opcodes():
    if tag == 'equal':
        for k in range(i2 - i1):
            mapping[i1 + k + 1] = j1 + k + 1
print('mapped lines: %d / %d' % (len(mapping), len(old)))

# (test, old_line_1based, needle) —— needle 係測試期望喺該行搵到嘅獨特內容
pins = [
    # kwan151 (14)
    ('kwan151', 25632, '/Ho\\s*哥|陳淑芬|施南生/'),
    ('kwan151', 25973, '["陳淑芬","施南生","Ho哥"]'),
    ('kwan151', 26021, '["陳淑芬","施南生","Ho哥","Ho 哥","nextHint"]'),
    ('kwan151', 26240, '["陳淑芬","施南生","Ho哥","Ho 哥"]'),
    ('kwan151', 25978, 'v151 退役'),
    ('kwan151', 25976, '雙女主改讀 devAppendix'),
    ('kwan151', 25977, 'bad("dual_note")'),
    ('kwan151', 30995, '["星河電視城", "星河電視台"]'),
    ('kwan151', 30986, '關海媚提醒頭條係雙刃'),
    ('kwan151', 27219, 'kwan_hoimei: { artId:"char_kwan", portraitsKey:null, display:"關海媚" }'),
    ('kwan151', 31037, '["rel_mei","關海媚"]'),
    ('kwan151', 30994, '采兒同關海媚嗰邊都近咗啲'),
    ('kwan151', 27186, '"關海媚":"kwan_hoimei"'),
    # rom176 (6)
    ('rom176', 6045, 'lan:{ id:"lan", name:"藍若曦"'),
    ('rom176', 31549, 'GIFT_REACT = giftReact'),
    ('rom176', 53081, '/* ===== v20a176 ROM176'),
    ('rom176', 53449, 'function rom176ApplyGiftOverrides()'),
    ('rom176', 54588, 'function addLocTalkGiftActs(add, L, npcId)'),
    ('rom176', 54682, 'rom176TryIntercept(id)'),
    # tang152 (3；測試用 0-based index，呢度寫 1-based 行號)
    ('tang152', 25792, 'const HELD = ["R_tang_push1","R_tang_push2","R_tang_crisis"];'),
    ('tang152', 31476, 'function normaliseTangStub152(pack){'),
    ('tang152', 31620, 'try{ normaliseTangStub152(rom2);'),
    # tang171 / tang173
    ('tang171', 54651, 'function openLoc(id, opts){'),
    ('tang173', 54651, 'function openLoc(id, opts){'),
    ('tang173', 4862, 'loc-acts-more171::after'),
    # text125 (3)
    ('text125', 27711, '(typeof b.text === "string" && b.text ? [b.text] : [])'),
    ('text125', 27840, '(typeof b.text === "string" && b.text ? [b.text] : [])'),
    ('text125', 33534, 'if(typeof b.text === "string" && b.text){'),
]
bad = 0
for test, o, needle in pins:
    n = mapping.get(o)
    if n is None:
        print('FAIL %-8s old %6d -> (changed/deleted)' % (test, o)); bad += 1; continue
    hit = needle in new[n - 1]
    print('%s %-8s old %6d -> new %6d (delta %+d) needle %s :: %s' % (
        'PASS' if hit else 'FAIL', test, o, n, n - o, 'found' if hit else 'NOT FOUND', new[n - 1].strip()[:70]))
    if not hit:
        bad += 1

# travel114：成個 COUNT／FREE／DEF／WRAPPER 逐行對位
travel = {
    'COUNT': [32150, 35646, 37773, 38844, 39278, 39281, 39312, 43866, 58711, 58889, 59032, 59053],
    'FREE': [24659, 28194, 30817, 30818, 30830, 30831, 30842, 30843, 30946, 40821, 43523, 43546,
             52904, 53023, 53073, 53296, 53335, 53341, 53408, 53410, 53413, 53440, 54551, 54925,
             54947, 55098, 56735, 58479, 58597, 58598, 58633, 58634, 58659, 59503],
    'DEF': [54651], 'WRAPPER': [44353],
}
for kind, lst in travel.items():
    mapped = []
    for o in lst:
        n = mapping.get(o)
        if n is None:
            print('FAIL travel114 %s old %d -> (changed)' % (kind, o)); bad += 1; continue
        # 內容核實：該行要有 openLoc(（DEF 係定義行，WRAPPER 係轉發行）
        okc = 'openLoc(' in new[n - 1]
        if not okc:
            print('FAIL travel114 %s old %d -> new %d :: no openLoc(: %s' % (kind, o, n, new[n - 1].strip()[:70])); bad += 1
        mapped.append(n)
    print('travel114 %s: %s' % (kind, mapped))
print('---')
print('FAILURES: %d' % bad if bad else 'ALL PINS VERIFIED (pure drift)')
sys.exit(1 if bad else 0)
