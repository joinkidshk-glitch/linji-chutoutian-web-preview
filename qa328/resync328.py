# qa328/resync328.py — v20a328 resync：index.html 淨 ＋18 行
# （A1：choi299PrepareNode 加 push2 回call分支——舊 L27705 註解行 1→2（＋1）、
#  舊 L27708 if 行同行改寫（0）、舊 L27710 之後插入 push2 分支 17 行（＋17）；
#  A4：暖版 heart 閘舊 L40219 同行改寫（0）；其後錨點一律 ＋18，之前唔郁；
#  difflib 對位核實純漂移；單次掃描 dict 查表＋精確錨點＋次數斷言）。
# 用法：python3 qa328/resync328.py  （喺工作副本根目錄行；只改 5 檔測試，唔郁 index.html）
import difflib
import re
import subprocess

BS = chr(92)  # backslash（測試檔入面 count('BSn') 嘅字面反斜線；寫檔嗰陣唔好直接打 BS+n）
NL = chr(10)
ROOT = '.'
NEW = open('index.html', encoding='utf-8').read().splitlines()
OLD = subprocess.check_output(['git', 'show', 'HEAD:index.html'], text=True).splitlines()

# ---- 1. difflib 核實純漂移：淨 ＋18，只得 4 處非 equal hunk ----
assert len(OLD) == 47244 and len(NEW) == 47262, (len(OLD), len(NEW))
sm = difflib.SequenceMatcher(a=OLD, b=NEW, autojunk=False)
non_eq = [(tag, i1, i2, j1, j2) for tag, i1, i2, j1, j2 in sm.get_opcodes() if tag != 'equal']
expected = [
    ('replace', 27704, 27705, 27704, 27706),  # 舊 L27705 註解行 1→2（＋1）
    ('replace', 27707, 27708, 27708, 27709),  # 舊 L27708 if(!node || ...) → if(!node)（0）
    ('insert', 27709, 27709, 27710, 27727),   # 舊 L27710 之後插入 push2 分支 17 行（＋17）
    ('replace', 40218, 40219, 40236, 40237),  # 舊 L40219 暖版閘同行改寫（0）
]
assert non_eq == expected, non_eq
assert NEW[27704].startswith('   v20a328 A1'), NEW[27704]
assert NEW[27710].startswith('    /* v20a328 A1'), NEW[27710]
assert 'flag_choi_spin_repaid' in NEW[27712], NEW[27712]
assert 'lok_first_mock && !(st.beatsDone||{}).lok_help' in NEW[40236], NEW[40236]
assert 'chai_first_bluff && !(st.beatsDone||{}).chai_choice' in NEW[40236], NEW[40236]
assert NEW[42470] == 'function openLoc(id, opts){', NEW[42470]
assert 'openLoc: function(id, opts){ openLoc(id, opts); }' in NEW[29082], NEW[29082]
assert NEW[40702].startswith('/* ===== v20a176 ROM176'), NEW[40702]
assert NEW[41052].startswith('function rom176ApplyGiftOverrides()'), NEW[41052]
assert NEW[42355].startswith('function addLocTalkGiftActs(add, L, npcId)'), NEW[42355]
assert 'rom176TryIntercept(id)' in NEW[42511], NEW[42511]
assert OLD[42452] == 'function openLoc(id, opts){', OLD[42452]
assert OLD[29064].find('openLoc: function(id, opts){ openLoc(id, opts); }') >= 0, OLD[29064]
print('drift check OK: 4 hunks only (comment 1->2 + if rewrite + insert 17 + heart gate rewrite), net +18')

def shift(n):
    """舊行號 -> 新行號（v328：＜27705 唔郁、≥27710 ＋18；27705–27709 係改寫區內，錨點唔應該喺度）。"""
    if n < 27705:
        return n
    if n <= 27709:
        raise AssertionError('anchor inside rewritten zone 27705-27709: %d' % n)
    return n + 18

# ---- 2. 單次掃描 dict 查表改寫 ----
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

HDR = '# v20a328 resync：index.html 淨 ＋18 行（A1 choi299PrepareNode 加 push2 回call分支＋18＠舊 L27705 之後／A4 暖版閘同行改寫，行數不變；其後錨點一律 ＋18，之前唔郁，difflib 對位核實純漂移，見 qa328/resync328.py）。'

# gift185：總行數 1 處（名＋值）
resync_pairs('tests/test_gift185_static.py', [
    ('總行數 47244（', '總行數 47262（', 1),
    ('＋v327 −36）', '＋v327 −36＋v328 ＋18）', 1),
    ('== 47244', '== 47262', 1),
], HDR)

# tang171／tang173：總行數＋openLoc DEF（名＋值＋guard＋index）
for f in ('tests/test_tang171_static.py', 'tests/test_tang173_static.py'):
    resync_pairs(f, [
        ('總行數 47244（', '總行數 47262（', 1),
        ('＋v327 −36）', '＋v327 −36＋v328 ＋18）', 1),
        ('== 47244', '== 47262', 1),
        ('openLoc DEF 行 42453（', 'openLoc DEF 行 42471（', 1),
        ('＋v327 −36，travel114 釘行）', '＋v327 −36＋v328 ＋18，travel114 釘行）', 1),
        ('len(lines) >= 42459', 'len(lines) >= 42477', 1),
        ('lines[42452]', 'lines[42470]', 1),
    ], HDR)

# rom176：4 個釘行各 ＋18（ok() 名 L55647 等係歷史名，唔郁）
resync_pairs('tests/test_rom176_static.py', [
    ('line(40685)', 'line(40703)', 1),
    ('line(41035)', 'line(41053)', 1),
    ('line(42338)', 'line(42356)', 1),
    ('line(42494)', 'line(42512)', 1),
], '# v20a328 resync：index.html 淨 ＋18 行（A1＋18＠舊 L27705 之後；4 個釘行各 ＋18（40685→40703、41035→41053、42338→42356、42494→42512；6321／14772 喺插入點之前唔郁），內容逐字核實純漂移；L55647 等名唔郁，見 qa328/resync328.py）。')

# travel114：COUNT／FREE 集合＋DEF／WRAPPER（＜27705 唔郁、≥27710 ＋18）
def resync_travel114():
    path = 'tests/test_travel114_static.py'
    lines = open(path, encoding='utf-8').read().splitlines()
    # 集合區：COUNT_LINES = { ... } 同 FREE_LINES = { ... } 入面行首數字先 shift
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
    # DEF／WRAPPER 行（精確全行）
    for i, ln in enumerate(lines):
        if ln.startswith('DEF_LINE = 42453'):
            lines[i] = 'DEF_LINE = 42471      # function openLoc(id, opts){'
            changed += 1
        if ln.startswith('WRAPPER_LINE = 29065'):
            lines[i] = 'WRAPPER_LINE = 29083  # window.__phase2.openLoc：轉發 opts'
            changed += 1
    # 預期：COUNT 5 處（28496／45729／45937／46095／46116）＋FREE 26 處＋DEF＋WRAPPER ＝ 33 處
    assert changed == 33, changed
    open(path, 'w', encoding='utf-8').write(
        '# v20a328 resync：index.html 淨 ＋18 行（A1＋18＠舊 L27705 之後；COUNT 5 處＋FREE 26 處＋DEF 42453→42471＋WRAPPER 29065→29083，＜27705 者唔郁，內容逐行核實純漂移，見 qa328/resync328.py）。' + NL + NL.join(lines) + NL)
    print('resynced tests/test_travel114_static.py (33 anchors)')

resync_travel114()
print('ALL RESYNC DONE')
