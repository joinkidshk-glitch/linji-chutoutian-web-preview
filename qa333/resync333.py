# qa333/resync333.py — v20a333 resync：index.html 淨 +7 行
# （enc79HasDoneStuntDouble helper 7 行＠舊 L39872 之後＋暖版 heart 閘加 ngai_walk_past 軟條件 1 行改寫；
#  總行數 47249→47256；其後錨點一律 +7，difflib 對位核實純漂移；單次掃描 dict 查表＋精確錨點＋次數斷言）。
# 用法：python3 qa333/resync333.py  （喺工作副本根目錄行；只改 5 檔測試，唔郁 index.html）
import difflib
import re
import subprocess

NL = chr(10)
NEW = open('index.html', encoding='utf-8').read().splitlines()
OLD = subprocess.check_output(['git', 'show', 'HEAD:index.html'], text=True).splitlines()

# ---- 1. difflib 核實純漂移：淨 +7，只得 2 處非 equal hunk ----
assert len(OLD) == 47249 and len(NEW) == 47256, (len(OLD), len(NEW))
sm = difflib.SequenceMatcher(a=OLD, b=NEW, autojunk=False)
non_eq = [(tag, i1, i2, j1, j2) for tag, i1, i2, j1, j2 in sm.get_opcodes() if tag != 'equal']
expected = [
    ('insert', 39871, 39871, 39871, 39878),   # 舊 L39872（enc79AnyBeatOpen）之前插入 helper 7 行
    ('replace', 40236, 40237, 40243, 40244),  # 舊 L40237 暖版 heart 閘行：加 ngai_walk_past 軟條件＋註解
]
assert non_eq == expected, non_eq
assert OLD[39870].strip() == '}', OLD[39870]
assert OLD[39871] == 'function enc79AnyBeatOpen(starId){', OLD[39871]
assert NEW[39871].startswith('function enc79HasDoneStuntDouble(){'), NEW[39871]
assert 'v20a333 B2' in NEW[39871], NEW[39871]
assert NEW[39872].strip() == 'try{', NEW[39872]
assert 'roleLabel==="動作替身"' in NEW[39875], NEW[39875]
assert NEW[39877].strip() == '}', NEW[39877]
assert NEW[39878] == 'function enc79AnyBeatOpen(starId){', NEW[39878]
assert 'enc79HasDoneStuntDouble' not in OLD[40236] and 'chai_first_bluff' in OLD[40236], OLD[40236]
assert 'ngai_walk_past && !enc79HasDoneStuntDouble()' in NEW[40243], NEW[40243]
assert 'v20a333 B2' in NEW[40243], NEW[40243]
assert 'chai_first_bluff' in NEW[40243] and 'lok_first_mock' in NEW[40243], NEW[40243]
print('drift check OK: 2 hunks only (insert helper 7 + gate replace 1), net +7')


def shift(n):
    """舊行號 -> 新行號（v333：≤39871 唔郁、＞39871 一律 +7）。"""
    return n + 7 if n > 39871 else n


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


HDR = '# v20a333 resync：index.html 淨 +7 行（enc79HasDoneStuntDouble helper＋7＠舊 L39872 之後＋暖版 heart 閘加 ngai_walk_past 軟條件；總行數 47249→47256；其後錨點一律 +7，內容逐行核實純漂移，見 qa333/resync333.py）。'

# gift185：總行數 1 處（名＋值）
resync_pairs('tests/test_gift185_static.py', [
    ('總行數 47249（', '總行數 47256（', 1),
    ('＋v329 −13）', '＋v329 −13＋v333 +7）', 1),
    ('== 47249', '== 47256', 1),
], HDR)

# tang171／tang173：總行數（名＋值）；openLoc DEF 42471→42478
for f in ('tests/test_tang171_static.py', 'tests/test_tang173_static.py'):
    resync_pairs(f, [
        ('總行數 47249（', '總行數 47256（', 1),
        ('＋v329 −13）', '＋v329 −13＋v333 +7）', 1),
        ('== 47249', '== 47256', 1),
        ('openLoc DEF 行 42471（', 'openLoc DEF 行 42478（', 1),
        ('＋v328 ＋18，travel114 釘行）', '＋v328 ＋18＋v333 +7，travel114 釘行）', 1),
        ('len(lines) >= 42477', 'len(lines) >= 42478', 1),
        ('lines[42470]', 'lines[42477]', 1),
    ], HDR)

# rom176：4 個釘行各 +7（6321／14772 喺插入點之前唔郁；L55647 等名唔郁）
resync_pairs('tests/test_rom176_static.py', [
    ('line(40703)', 'line(40710)', 1),
    ('line(41053)', 'line(41060)', 1),
    ('line(42356)', 'line(42363)', 1),
    ('line(42512)', 'line(42519)', 1),
], HDR)

# 內容核實：4 個新釘行逐字相同
assert NEW[40709].startswith('/* ===== v20a176 ROM176'), NEW[40709]
assert NEW[41059].startswith('function rom176ApplyGiftOverrides()'), NEW[41059]
assert NEW[42362].startswith('function addLocTalkGiftActs(add, L, npcId)'), NEW[42362]
assert 'rom176TryIntercept(id)' in NEW[42518], NEW[42518]
print('rom176 content check OK: 4 anchors')


# travel114：COUNT／FREE 集合（≤39871 唔郁、＞39871 一律 +7）＋DEF_LINE 42471→42478
def resync_travel114():
    path = 'tests/test_travel114_static.py'
    lines = open(path, encoding='utf-8').read().splitlines()
    in_set = None
    changed = 0
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
    # DEF_LINE 42471→42478；WRAPPER 29083 喺插入點之前，唔郁（只核實在位）
    def_hit = [i for i, ln in enumerate(lines) if ln.startswith('DEF_LINE = 42471')]
    assert len(def_hit) == 1, def_hit
    lines[def_hit[0]] = 'DEF_LINE = 42478      # function openLoc(id, opts){'
    assert any(ln.startswith('WRAPPER_LINE = 29083') for ln in lines), 'WRAPPER_LINE moved?!'
    # 預期：COUNT 4 處（45734／45942／46100／46121）＋FREE 24 處（40501 起）shift，DEF 1 處
    assert changed == 28, changed
    # 內容核實：每個新錨點行實際係 openLoc( 呼叫點；FREE 錨帶旗、COUNT 錨唔帶旗
    FREE_FLAGS = ('travelFree:true', 'encDone:true', 'forceRestore:true', 'wf4Done:true')
    for n in (45741, 45949, 46107, 46128):
        assert 'openLoc(' in NEW[n - 1], (n, NEW[n - 1])
        assert not any(f in NEW[n - 1] for f in FREE_FLAGS), (n, NEW[n - 1])
    for n in (40508, 40627, 40702, 40902, 40946, 40952, 41019, 41021, 41024, 41051,
              42326, 42373, 42743, 42765, 42917, 42922, 43847, 45521, 45618, 45619,
              45663, 45664, 45689, 46578):
        assert 'openLoc(' in NEW[n - 1], (n, NEW[n - 1])
        assert any(f in NEW[n - 1] for f in FREE_FLAGS), (n, NEW[n - 1])
    assert NEW[42477] == 'function openLoc(id, opts){', NEW[42477]
    open(path, 'w', encoding='utf-8').write(
        '# v20a333 resync：index.html 淨 +7 行（enc79HasDoneStuntDouble helper＋7＠舊 L39872 之後；COUNT 4 處＋FREE 24 處＋DEF 42471→42478 各 +7，≤39871 者唔郁，內容逐行核實純漂移，見 qa333/resync333.py）。' + NL + NL.join(lines) + NL)
    print('resynced tests/test_travel114_static.py (28 set shifts + DEF)')


resync_travel114()
print('ALL RESYNC DONE')
