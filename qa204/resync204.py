# v20a204 resync：index.html 淨 +32 行（POSTER59_STAR_IDS +1 @~32521／build pack gender +1／
# fellows 逐類別 +2／AWARDS63 註解 +1／POOL 註解 +2／TIER_WEIGHT＋AWARDS204_FEMALE_STARS＋
# awards204StarGender +10／其餘註解 0 淨；git diff hunk 對位，見下面 HUNKS）。
# 6 個靜態測試嘅釘行按段重算，每粒先核實 pristine 行內容 == 工作版行內容（逐字相同，純漂移）
# 先改；內容唔啱就報錯停手，唔硬改。單次掃描 dict 查表一次過換，唔逐對 re.sub。
# 用法：python3 qa204/resync204.py [--write]
import re, subprocess, sys

WORK = '/home/hatch/workspace/linji-work204'
BASE = 'main'

def show(rev, path):
    out = subprocess.run(['git', '-C', WORK, 'show', f'{rev}:{path}'],
                         capture_output=True, text=True)
    assert out.returncode == 0, (rev, path, out.stderr[:200])
    return out.stdout.split('\n')

def diff_hunks():
    out = subprocess.run(['git', '-C', WORK, 'diff', '-U0', BASE, '--', 'index.html'],
                         capture_output=True, text=True)
    assert out.returncode == 0
    hunks = []
    for ln in out.stdout.split('\n'):
        m = re.match(r'@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@', ln)
        if m:
            a = int(m.group(1)); b = int(m.group(2) or 1)
            c = int(m.group(3)); d = int(m.group(4) or 1)
            hunks.append((a, b, c, d))
    return hunks

HUNKS = diff_hunks()
print('hunks:', HUNKS)
# 由 hunk 計累積偏移：舊行 L 嘅新行 = L + sum(新-舊 for hunk.old_start <= L)
def mapping(old):
    delta = 0
    for (a, b, c, d) in HUNKS:
        if a <= old:
            delta += (d - b)
    return old + delta

base_lines = show(BASE, 'index.html')
work_lines = open(WORK + '/index.html', encoding='utf-8').read().split('\n')
print('base lines:', len(base_lines) - 1, '-> work lines:', len(work_lines) - 1,
      'delta', (len(work_lines) - 1) - (len(base_lines) - 1))
NEW_TOTAL = len(work_lines) - 1

def verify(old, new=None):
    new = new if new is not None else mapping(old)
    b = base_lines[old - 1] if 1 <= old <= len(base_lines) else None
    w = work_lines[new - 1] if 1 <= new <= len(work_lines) else None
    ok = (b is not None and b == w)
    print(('OK  ' if ok else 'BAD ') + f'L{old} -> L{new}: ' + (b or '')[:80])
    return ok

def parse_set(txt, name):
    # 逐行抽：只取「獨立數字行」（數字＋可選逗號＋可選註解）；註解入面嘅 {travelFree} 有 }，唔可以用 [^}]* 截 block。
    lines = txt.split('\n')
    start = next(i for i, l in enumerate(lines) if l.startswith(name + ' = {'))
    out = []
    for l in lines[start + 1:]:
        if l.strip() == '}':
            break
        m = re.match(r'\s*(\d+),?\s*(?:#.*)?$', l)
        if m:
            out.append(int(m.group(1)))
    assert out, name
    return out

travel_txt = open(WORK + '/tests/test_travel114_static.py', encoding='utf-8').read()
COUNT = parse_set(travel_txt, 'COUNT_LINES')
FREE = parse_set(travel_txt, 'FREE_LINES')
print('travel114 COUNT:', len(COUNT), 'FREE:', len(FREE))

PINS = {
    'rom176': [54069, 54437, 55576, 55670],
    'tang171_def': [55639],
    'tang173_def': [55639],
    'text125': [27847, 27976, 33683],   # 1-based 行；code 用 ls[row-1]
    'travel114_count': COUNT,
    'travel114_free': FREE,
    'travel114_def': [55639],
    'travel114_wrapper': [44902],
}
allok = True
for group, olds in PINS.items():
    print(f'-- {group}')
    for old in olds:
        allok = verify(old) and allok

assert allok, '有釘行內容唔啱，唔寫'
print('ALL PINS VERIFIED (pure drift)')

if '--write' not in sys.argv:
    print('dry run only (加 --write 先改測試檔)')
    sys.exit(0)

def sub_count(path, pairs):
    txt = open(path, encoding='utf-8').read()
    for old_s, new_s in pairs:
        n = txt.count(old_s)
        if n == 0 and new_s in txt:
            print(f'{path}: skip (already resynced): {old_s!r}')
            continue
        assert n >= 1, (path, old_s, 'not found')
        txt = txt.replace(old_s, new_s)
        print(f'{path}: {old_s!r} x{n} -> {new_s!r}')
    open(path, 'w', encoding='utf-8').write(txt)

T = WORK + '/tests/'
RESYNC_NOTE = '# v20a204 resync：index.html 淨 +32 行（見 qa204/resync204.py difflib 對位核實純漂移）。'
# gift185：總行數
sub_count(T + 'test_gift185_static.py', [
    ("ok('總行數 61167（v202 60988＋v193 淨 +179）', html.count('\\n') == 61167)",
     f"ok('總行數 {NEW_TOTAL}（v193 61167＋v204 淨 +32）', html.count('\\n') == {NEW_TOTAL})"),
])
# rom176：line() 參數＋名一併改
pairs = []
for o in PINS['rom176']:
    pairs.append((f'line({o})', f'line({mapping(o)})'))
    pairs.append((f'L{o}', f'L{mapping(o)}'))
sub_count(T + 'test_rom176_static.py', pairs)
# tang171：總行數＋DEF
sub_count(T + 'test_tang171_static.py', [
    ("ok('零行數漂移：總行數 61167（v202 60988＋v193 淨 +179）', src.count('\\n') == 61167)",
     f"ok('零行數漂移：總行數 {NEW_TOTAL}（v193 61167＋v204 淨 +32）', src.count('\\n') == {NEW_TOTAL})"),
    ("ok('零行數漂移：openLoc DEF 行 55639（v202 55460＋v193 +179，travel114 釘行）',\n   len(lines) >= 55639 and 'function openLoc(id, opts){' in lines[55638])",
     f"ok('零行數漂移：openLoc DEF 行 {mapping(55639)}（v193 55639＋v204 淨 +32，travel114 釘行）',\n   len(lines) >= {mapping(55639)} and 'function openLoc(id, opts){{' in lines[{mapping(55639) - 1}])"),
])
# tang173：總行數＋DEF（同 tang171 一樣寫法）
sub_count(T + 'test_tang173_static.py', [
    ("ok('零行數漂移：總行數 61167（v202 60988＋v193 淨 +179）', src.count('\\n') == 61167)",
     f"ok('零行數漂移：總行數 {NEW_TOTAL}（v193 61167＋v204 淨 +32）', src.count('\\n') == {NEW_TOTAL})"),
    ("ok('零行數漂移：openLoc DEF 行 55639（v202 55460＋v193 +179，travel114 釘行）',\n   len(lines) >= 55639 and 'function openLoc(id, opts){' in lines[55638])",
     f"ok('零行數漂移：openLoc DEF 行 {mapping(55639)}（v193 55639＋v204 淨 +32，travel114 釘行）',\n   len(lines) >= {mapping(55639)} and 'function openLoc(id, opts){{' in lines[{mapping(55639) - 1}])"),
])
# text125：ls[] index＋訊息入面嘅行號（只有 33683 郁，27847／27976 喺插入點之前唔郁）
for o in PINS['text125']:
    n = mapping(o)
    if n != o:
        sub_count(T + 'test_text125_static.py', [(f'ls[{o - 1}]', f'ls[{n - 1}]')])
        sub_count(T + 'test_text125_static.py', [(f'第 {o} 行', f'第 {n} 行')])
# travel114：COUNT／FREE／DEF／WRAPPER（獨立行號；單次 regex 掃描一併替換）
def sub_lines(path, olds):
    txt = open(path, encoding='utf-8').read()
    want = {o: mapping(o) for o in olds}
    def repl(m):
        old = int(m.group(2))
        assert old in want, (path, old)
        return m.group(1) + str(want[old]) + m.group(3)
    pat = re.compile(r'^(\s*)(\d+)(,?\s*(?:#.*)?)$', re.M)
    for o in olds:
        hits = [m for m in pat.finditer(txt) if int(m.group(2)) == o]
        assert len(hits) == 1, (path, o, len(hits))
    txt = pat.sub(repl, txt)
    for o in olds:
        print(f'{path}: list {o} -> {want[o]}')
    open(path, 'w', encoding='utf-8').write(txt)
sub_lines(T + 'test_travel114_static.py', PINS['travel114_count'] + PINS['travel114_free'])
sub_count(T + 'test_travel114_static.py', [
    ("DEF_LINE = 55639      # function openLoc(id, opts){",
     f"DEF_LINE = {mapping(55639)}      # function openLoc(id, opts){{"),
    ("WRAPPER_LINE = 44902  # window.__phase2.openLoc：轉發 opts",
     f"WRAPPER_LINE = {mapping(44902)}  # window.__phase2.openLoc：轉發 opts"),
])
print('RESYNC WRITTEN')
