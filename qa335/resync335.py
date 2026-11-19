# qa335/resync335.py — v20a335 resync：index.html 淨 +7 行
# （板短卡 gigBoardTeaserHtml 補人情免試鏡金提示：CSS .gig-teaser .gold ＋2＠舊 L2937 之後
#  ＋teaser 函數內 favor158Html 計算 ＋4＠舊 L18031 之後＋template 內插 ＋1＠舊 L18050 之後；
#  總行數 47256→47263；錨點按段 shift（≤2937 唔郁、2938–18031 ＋2、≥18032 ＋7），
#  difflib 對位核實純漂移；單次掃描 dict 查表＋精確錨點＋次數斷言）。
# 用法：python3 qa335/resync335.py  （喺工作副本根目錄行；只改 5 檔測試，唔郁 index.html）
import difflib
import re
import subprocess

NL = chr(10)
NEW = open('index.html', encoding='utf-8').read().splitlines()
OLD = subprocess.check_output(['git', 'show', 'HEAD:index.html'], text=True).splitlines()

# ---- 1. difflib 核實純漂移：淨 +7，只得 3 處非 equal hunk ----
assert len(OLD) == 47256 and len(NEW) == 47263, (len(OLD), len(NEW))
sm = difflib.SequenceMatcher(a=OLD, b=NEW, autojunk=False)
non_eq = [(tag, i1, i2, j1, j2) for tag, i1, i2, j1, j2 in sm.get_opcodes() if tag != 'equal']
expected = [
    ('insert', 2937, 2937, 2937, 2939),    # CSS .gig-teaser .gold ＋2＠舊 L2937（.gt-hint）之後
    ('insert', 18031, 18031, 18033, 18037),  # teaser 內 favor158Html 計算 ＋4＠舊 L18031（let intelMark）之後
    ('insert', 18050, 18050, 18056, 18057),  # template 內插 ${favor158Html} ＋1＠舊 L18050（${intelMark}）之後
]
assert non_eq == expected, non_eq
assert OLD[2936].strip().startswith('.gig-teaser .gt-hint'), OLD[2936]
assert NEW[2937].startswith('/* v20a335'), NEW[2937]
assert NEW[2938] == '.gig-teaser .gold{ font-size:.72rem; line-height:1.45; margin:6px 0 0; }', NEW[2938]
assert OLD[18030].strip() == 'let intelMark = "";', OLD[18030]
assert NEW[18033].strip().startswith('/* v20a335'), NEW[18033]
assert NEW[18035].strip() == 'let favor158Html = "";', NEW[18035]
assert 'favor158ChannelHintHtml(g)' in NEW[18036], NEW[18036]
assert OLD[18049].strip() == '${intelMark}', OLD[18049]
assert NEW[18056].strip() == '${favor158Html}', NEW[18056]
assert NEW[18055].strip() == '${intelMark}', NEW[18055]
print('drift check OK: 3 hunks only (CSS +2, teaser calc +4, template +1), net +7')


def shift(n):
    """舊行號 -> 新行號（v335：≤2937 唔郁、2938–18031 ＋2、≥18032 ＋7）。"""
    if n <= 2937:
        return n
    if n <= 18031:
        return n + 2
    return n + 7


def resync_pairs(path, pairs, header):
    """pairs：(old, new, expected_count)；一次過用 combined regex 掃描，逐對斷言次數。"""
    text = open(path, encoding='utf-8').read()
    pats = sorted(((o, n, c) for o, n, c in pairs), key=lambda t: -len(t[0]))
    rx = re.compile('|'.join(re.escape(o) for o, _, _ in pats))
    counts = {o: 0 for o, _, _ in pats}
    mapping = {o: n for o, n, _ in pats}

    def repl(m):
        counts[m.group(0)] += 1
        return mapping[m.group(0)]
    out = rx.sub(repl, text)
    for o, n, c in pats:
        assert counts[o] == c, (path, o, counts[o], c)
    open(path, 'w', encoding='utf-8').write(header + NL + out)
    print('resynced %s (%d pairs)' % (path, len(pats)))


HDR = '# v20a335 resync：index.html 淨 +7 行（板短卡金提示：CSS ＋2＠舊 L2937 後＋teaser 計算 ＋4＠舊 L18031 後＋template ＋1＠舊 L18050 後；總行數 47256→47263；錨點按段 shift（≤2937 唔郁、2938–18031 ＋2、≥18032 ＋7），內容逐行核實純漂移，見 qa335/resync335.py）。'

# gift185：總行數 1 處（名＋值）
resync_pairs('tests/test_gift185_static.py', [
    ('總行數 47256（', '總行數 47263（', 1),
    ('＋v333 +7）', '＋v333 +7＋v335 +7）', 1),
    ('== 47256', '== 47263', 1),
], HDR)

# tang171／tang173：總行數（名＋值）；openLoc DEF 42478→42485
for f in ('tests/test_tang171_static.py', 'tests/test_tang173_static.py'):
    resync_pairs(f, [
        ('總行數 47256（', '總行數 47263（', 1),
        ('＋v333 +7）', '＋v333 +7＋v335 +7）', 1),
        ('== 47256', '== 47263', 1),
        ('openLoc DEF 行 42478（', 'openLoc DEF 行 42485（', 1),
        ('＋v333 +7，travel114 釘行）', '＋v333 +7＋v335 +7，travel114 釘行）', 1),
        ('len(lines) >= 42478', 'len(lines) >= 42485', 1),
        ('lines[42477]', 'lines[42484]', 1),
    ], HDR)

# tang173：L4863 釘（實查 lines[5087]，舊 L5088 → 新 L5090，＋2）
resync_pairs('tests/test_tang173_static.py', [
    ('lines[5087]', 'lines[5089]', 8),
    ('len(lines) >= 5088', 'len(lines) >= 5090', 1),
], HDR)

# rom176：6 個釘行按段 shift（6321／14772 ＋2；40710／41060／42363／42519 ＋7）
resync_pairs('tests/test_rom176_static.py', [
    ('line(6321)', 'line(6323)', 1),
    ('line(14772)', 'line(14774)', 2),
    ('line(40710)', 'line(40717)', 1),
    ('line(41060)', 'line(41067)', 1),
    ('line(42363)', 'line(42370)', 1),
    ('line(42519)', 'line(42526)', 1),
], HDR)

# 內容核實：6 個新釘行逐字相同
assert NEW[6322].startswith('  lan:{ id:"lan", name:"藍若曦"'), NEW[6322]
assert 'GIFT_REACT = giftReact' in NEW[14773] and 'rom176ApplyGiftOverrides()' in NEW[14773], NEW[14773]
assert NEW[40716].startswith('/* ===== v20a176 ROM176'), NEW[40716]
assert NEW[41066].startswith('function rom176ApplyGiftOverrides()'), NEW[41066]
assert NEW[42369].startswith('function addLocTalkGiftActs(add, L, npcId)'), NEW[42369]
assert 'rom176TryIntercept(id)' in NEW[42525], NEW[42525]
print('rom176 content check OK: 6 anchors')


# travel114：COUNT／FREE 集合按段 shift＋DEF_LINE 42478→42485＋WRAPPER_LINE 29083→29085
def resync_travel114():
    path = 'tests/test_travel114_static.py'
    lines = open(path, encoding='utf-8').read().splitlines()
    in_set = None
    changed = 0
    count_n = 0
    free_n = 0
    new_count = []
    new_free = []
    for i, ln in enumerate(lines):
        if ln.startswith('COUNT_LINES = {'):
            in_set = 'COUNT'
            continue
        if ln.startswith('FREE_LINES = {'):
            in_set = 'FREE'
            continue
        if in_set and ln == '}':
            in_set = None
            continue
        if in_set:
            m = re.match(r'^(    )([0-9]+)(,.*)$', ln)
            if m:
                old_n = int(m.group(2))
                new_n = shift(old_n)
                if new_n != old_n:
                    lines[i] = m.group(1) + str(new_n) + m.group(3)
                    changed += 1
                    if in_set == 'COUNT':
                        count_n += 1
                    else:
                        free_n += 1
                if in_set == 'COUNT':
                    new_count.append(new_n)
                else:
                    new_free.append(new_n)
    # DEF_LINE 42478→42485（＋7）；WRAPPER 29083→29090（＋7：CSS ＋2＋teaser ＋5，兩個插入點都在之前）
    def_hit = [i for i, ln in enumerate(lines) if ln.startswith('DEF_LINE = 42478')]
    assert len(def_hit) == 1, def_hit
    lines[def_hit[0]] = 'DEF_LINE = 42485      # function openLoc(id, opts){'
    wr_hit = [i for i, ln in enumerate(lines) if ln.startswith('WRAPPER_LINE = 29083')]
    assert len(wr_hit) == 1, wr_hit
    lines[wr_hit[0]] = 'WRAPPER_LINE = 29090  # window.__phase2.openLoc：轉發 opts'
    # 預期：52 處 shift（COUNT 12＋FREE 40；其餘錨點 ≤2937 唔郁）
    assert changed == 52 and count_n == 12 and free_n == 40, (changed, count_n, free_n)
    # 內容核實：每個新錨點行實際係 openLoc( 呼叫點；FREE 錨帶旗、COUNT 錨唔帶旗
    FREE_FLAGS = ('travelFree:true', 'encDone:true', 'forceRestore:true', 'wf4Done:true')
    for n in new_count:
        assert 'openLoc(' in NEW[n - 1], (n, NEW[n - 1])
        assert not any(f in NEW[n - 1] for f in FREE_FLAGS), (n, NEW[n - 1])
    for n in new_free:
        assert 'openLoc(' in NEW[n - 1], (n, NEW[n - 1])
        assert any(f in NEW[n - 1] for f in FREE_FLAGS), (n, NEW[n - 1])
    assert NEW[42484] == 'function openLoc(id, opts){', NEW[42484]
    assert 'openLoc: function(id, opts){ openLoc(id, opts); }' in NEW[29089], NEW[29089]
    open(path, 'w', encoding='utf-8').write(
        '# v20a335 resync：index.html 淨 +7 行（板短卡金提示：CSS ＋2＠舊 L2937 後＋teaser 計算 ＋4＠舊 L18031 後＋template ＋1＠舊 L18050 後；COUNT 12 處＋FREE 40 處按段 shift＋DEF 42478→42485＋WRAPPER 29083→29090，≤2937 者唔郁，內容逐行核實純漂移，見 qa335/resync335.py）。' + NL + NL.join(lines) + NL)
    print('resynced tests/test_travel114_static.py (52 set shifts + DEF + WRAPPER)')


resync_travel114()
print('ALL RESYNC DONE')
