# v20a202 resync：index.html 淨 +88 行（CSS +7 @~1856／showResult 註解 +1／
# render C2 +4／afterDayModal +3／v202 helpers +50／resolve note +2／
# modal note +9／confirm45 簽名 +1／取消掣 +5／goScheduleAsk +4／休息卡 +2；
# git diff hunk 對位，見下面 HUNKS）。8 個靜態測試嘅釘行按段重算，
# 每粒先核實 pristine 行內容 == 工作版行內容（逐字相同，純漂移）先改；
# 內容唔啱就報錯停手，唔硬改。
# 用法：python3 qa202/resync202.py [--write]
import subprocess, sys

WORK = '/home/hatch/workspace/linji-work202'
BASE = '860e790'

def show(rev, path):
    out = subprocess.run(['git', '-C', WORK, 'show', f'{rev}:{path}'],
                         capture_output=True, text=True)
    assert out.returncode == 0, (rev, path, out.stderr[:200])
    return out.stdout.split('\n')

def diff_hunks():
    out = subprocess.run(['git', '-C', WORK, 'diff', '-U0', '--', 'index.html'],
                         capture_output=True, text=True)
    assert out.returncode == 0
    hunks = []  # (old_start, old_count, new_start, new_count)
    import re
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
# （釘行唔可以落喺被刪／被改嘅行上面，內容核實會捉到。）
def mapping(old):
    delta = 0
    for (a, b, c, d) in HUNKS:
        if a <= old:
            delta += (d - b)
    return old + delta

base_lines = show(BASE, 'index.html')
work_lines = open(WORK + '/index.html', encoding='utf-8').read().split('\n')
print('base lines:', len(base_lines) - 1, 'work lines:', len(work_lines) - 1)

def verify(old, new=None):
    new = new if new is not None else mapping(old)
    b = base_lines[old - 1] if 1 <= old <= len(base_lines) else None
    w = work_lines[new - 1] if 1 <= new <= len(work_lines) else None
    ok = (b is not None and b == w)
    print(('OK  ' if ok else 'BAD ') + f'L{old} -> L{new}: ' + (b or '')[:80])
    return ok

# ---- 釘行清單（舊行號；新行號由 mapping 計） ----
PINS = {
    'kwan151': [25714, 26055, 26103, 26322, 26060, 26058, 26059, 31129, 31120, 31128, 27348, 31171, 27315],
    'tang152_0based': [25873, 31609, 31753],  # lines()[N]：1-based 行 = N+1
    'rom176': [6127, 31683, 53814, 54182, 55321, 55415],
    'tang171': [55384], 'tang173': [55384, 4935],
    'text125': [27840, 27969, 33671],
    'travel114_count': [32284, 35783, 37931, 39033, 39465, 39468, 39499, 44078, 59453, 59631, 59777, 59798],
    'travel114_free': [24741, 30951, 30952, 30964, 30965, 30976, 30977, 31080, 41022, 43735, 43758, 53637, 53756, 53806, 54029, 54068, 54074, 54141, 54143, 54146, 54173, 55284, 55658, 55680, 55831, 57468, 59221, 59339, 59340, 59375, 59376, 59401, 60248],
    'travel114_def': [55384], 'travel114_wrapper': [44647],
}
allok = True
for group, olds in PINS.items():
    print(f'-- {group}')
    for old in olds:
        if group == 'tang152_0based':
            # 0-based index N 對應 1-based 行 N+1
            new1 = mapping(old + 1)
            b = base_lines[old] if 0 <= old < len(base_lines) else None
            w = work_lines[new1 - 1] if 1 <= new1 <= len(work_lines) else None
            ok = (b is not None and b == w)
            print(('OK  ' if ok else 'BAD ') + f'idx{old} (L{old+1}) -> idx{new1-1} (L{new1}): ' + (b or '')[:80])
            allok = allok and ok
        else:
            allok = verify(old) and allok
# 總行數
print('total: base', len(base_lines) - 1, '-> work', len(work_lines) - 1,
      'delta', (len(work_lines) - 1) - (len(base_lines) - 1))
assert allok, '有釘行內容唔啱，唔寫'
print('ALL PINS VERIFIED (pure drift)')

if '--write' not in sys.argv:
    print('dry run only (加 --write 先改測試檔)')
    sys.exit(0)

import re
def sub_count(path, pairs):
    txt = open(path, encoding='utf-8').read()
    for old_s, new_s in pairs:
        n = txt.count(old_s)
        assert n >= 1, (path, old_s, 'not found')
        txt = txt.replace(old_s, new_s)
        print(f'{path}: {old_s!r} x{n} -> {new_s!r}')
    open(path, 'w', encoding='utf-8').write(txt)

T = WORK + '/tests/'
# gift185：總行數（名＋值＋頭註解）
sub_count(T + 'test_gift185_static.py', [
    ("# v20a196 落地合併上 main 2de5026：總行數 60817→60900（v197 ＋94 之上再 ＋83）。",
     "# v20a196 落地合併上 main 2de5026：總行數 60817→60900（v197 ＋94 之上再 ＋83）。\n# v20a202 resync：index.html 淨 +88 行（見 qa202/resync202.py），總行數 60900→60988。"),
    ("ok('總行數 60900（v196 落地合併上 main 2de5026：v197 60817＋83）', html.count('\\n') == 60900)",
     "ok('總行數 60988（v202 淨 +88：CSS +7／showResult +1／render +4／afterDayModal +3／helpers +50／resolve +2／modal +9／confirm45 +1+5+4／休息卡 +2）', html.count('\\n') == 60988)"),
])
# kwan151：只改 line() 參數（名入面嘅 L25608 等係歷史標籤，舊 resync 一律留返，唔郁）
pairs = [(f'line({o})', f'line({mapping(o)})') for o in PINS['kwan151']]
sub_count(T + 'test_kwan151_static.py', pairs)
# tang152：0-based index（名留返）
pairs = [(f'lines()[{o}]', f'lines()[{mapping(o + 1) - 1}]') for o in PINS['tang152_0based']]
sub_count(T + 'test_tang152_static.py', pairs)
# rom176：line() 參數＋名一併改（呢檔名同參數一向同步）
pairs = []
for o in PINS['rom176']:
    pairs.append((f'line({o})', f'line({mapping(o)})'))
    pairs.append((f'L{o}', f'L{mapping(o)}'))
sub_count(T + 'test_rom176_static.py', pairs)
# tang171：總行數＋DEF（名＋值）
sub_count(T + 'test_tang171_static.py', [
    ("# v20a196 落地合併上 main 2de5026：總行數 60817→60900、DEF 55310→55384（v197 ＋94 之上再 ＋83）。",
     "# v20a196 落地合併上 main 2de5026：總行數 60817→60900、DEF 55310→55384（v197 ＋94 之上再 ＋83）。\n# v20a202 resync：index.html 淨 +88 行（見 qa202/resync202.py），總行數 60900→60988、DEF 55384→55460。"),
    ("ok('零行數漂移：總行數 60900（v196 落地合併上 main 2de5026：v197 60817＋83）', src.count('\\n') == 60900)",
     "ok('零行數漂移：總行數 60988（v202 淨 +88）', src.count('\\n') == 60988)"),
    ("ok('零行數漂移：openLoc DEF 行 55384（v196 落地合併上 main 2de5026：v197 55310＋74，travel114 釘行）',\n   len(lines) >= 55384 and 'function openLoc(id, opts){' in lines[55383])",
     "ok('零行數漂移：openLoc DEF 行 55460（v202 淨 +88，travel114 釘行）',\n   len(lines) >= 55460 and 'function openLoc(id, opts){' in lines[55459])"),
])
# tang173：總行數＋DEF＋L4862 錨點（lines[4934] 三處）
sub_count(T + 'test_tang173_static.py', [
    ("ok('零行數漂移：總行數 60900（v196 落地合併上 main 2de5026：v197 60817＋83）', src.count('\\n') == 60900)",
     "ok('零行數漂移：總行數 60988（v202 淨 +88）', src.count('\\n') == 60988)"),
    ("ok('零行數漂移：openLoc DEF 行 55384（v196 落地合併上 main 2de5026：v197 55310＋74，travel114 釘行）',\n   len(lines) >= 55384 and 'function openLoc(id, opts){' in lines[55383])",
     "ok('零行數漂移：openLoc DEF 行 55460（v202 淨 +88，travel114 釘行）',\n   len(lines) >= 55460 and 'function openLoc(id, opts){' in lines[55459])"),
    ("len(lines) >= 4935 and 'loc-acts-more171::after' in lines[4934] and 'act-locked171' in lines[4934])",
     "len(lines) >= 4942 and 'loc-acts-more171::after' in lines[4941] and 'act-locked171' in lines[4941])"),
    ("   lines[4934].count('/*') == lines[4934].count('*/')\n   and lines[4934].rfind('/*', 0, lines[4934].find('#app #loc-sheet.sheet .act.act-locked171{ background'))\n   < lines[4934].rfind('*/', 0, lines[4934].find('#app #loc-sheet.sheet .act.act-locked171{ background')))",
     "   lines[4941].count('/*') == lines[4941].count('*/')\n   and lines[4941].rfind('/*', 0, lines[4941].find('#app #loc-sheet.sheet .act.act-locked171{ background'))\n   < lines[4941].rfind('*/', 0, lines[4941].find('#app #loc-sheet.sheet .act.act-locked171{ background')))"),
])
# text125：ls[] index＋訊息入面嘅行號
for o in PINS['text125']:
    n = mapping(o)
    sub_count(T + 'test_text125_static.py', [(f'ls[{o - 1}]', f'ls[{n - 1}]')])
    sub_count(T + 'test_text125_static.py', [(f'第 {o} 行', f'第 {n} 行')])
# travel114：COUNT／FREE／DEF／WRAPPER（獨立行號；單次 regex 掃描一併替換，
# 唔逐個順序改——新值可能撞舊值，例如 30952→30964 之後再搵 30964 會搵到兩行）
def sub_lines(path, olds):
    txt = open(path, encoding='utf-8').read()
    want = {o: mapping(o) for o in olds}
    def repl(m):
        old = int(m.group(2))
        assert old in want, (path, old)
        return m.group(1) + str(want[old]) + m.group(3)
    pat = re.compile(r'^(\s*)(\d+)(,?\s*(?:#.*)?)$', re.M)
    # 先數：每個舊值喺 list 區只出現一次
    for o in olds:
        hits = [m for m in pat.finditer(txt) if int(m.group(2)) == o]
        assert len(hits) == 1, (path, o, len(hits))
    txt = pat.sub(repl, txt)
    for o in olds:
        print(f'{path}: list {o} -> {want[o]}')
    open(path, 'w', encoding='utf-8').write(txt)
sub_lines(T + 'test_travel114_static.py', PINS['travel114_count'] + PINS['travel114_free'])
sub_count(T + 'test_travel114_static.py', [
    ("DEF_LINE = 55384      # function openLoc(id, opts){",
     "DEF_LINE = 55460      # function openLoc(id, opts){"),
    ("WRAPPER_LINE = 44647  # window.__phase2.openLoc：轉發 opts",
     "WRAPPER_LINE = 44723  # window.__phase2.openLoc：轉發 opts"),
])
print('RESYNC WRITTEN')
