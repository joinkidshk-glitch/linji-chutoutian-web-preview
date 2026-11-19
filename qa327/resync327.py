# qa327/resync327.py — v20a327 resync：index.html 淨 −36 行
# （刪死鎖：函數舊 L17426–17450（25 行）＋canAudition try block
#  舊 L17510–17513（4 行）＋gateShortReason try block 舊 L17559–17562（4 行）＋
#  __freeplay export 舊 L35370（1 行）＋自檢舊 L35450（1 行）＋回傳欄位舊 L35484（1 行）；
#  註解三處改寫（舊 L22737／22931／23380–23381，replace 淨 0）；
#  漂移分區：＜17426 唔郁、17563–35369 −33、35371–35449 −34、35451–35483 −35、≥35485 −36；
#  difflib 對位核實純漂移）。
# 用法：python3 qa327/resync327.py  （喺工作副本根目錄行；只改 5 檔測試，唔郁 index.html）
# 原則：逐對 re.sub 會撞值丟失／重複——全部用單次掃描 dict 查表＋精確錨點＋次數斷言。
import difflib
import re
import subprocess

BS = chr(92)  # backslash（測試檔入面 count('BSn') 嘅字面反斜線）
ROOT = '.'
NEW = open('index.html', encoding='utf-8').read().splitlines()
OLD = subprocess.check_output(['git', 'show', 'HEAD:index.html'], text=True).splitlines()

# ---- 1. difflib 核實純漂移：淨 −36，只得 9 處非 equal hunk ----
assert len(OLD) == 47280 and len(NEW) == 47244, (len(OLD), len(NEW))
assert 'softOverdueFavorDebtLock' not in '\n'.join(NEW), 'lock still present in new index.html'
sm = difflib.SequenceMatcher(a=OLD, b=NEW, autojunk=False)
non_eq = [(tag, i1, i2, j1, j2) for tag, i1, i2, j1, j2 in sm.get_opcodes() if tag != 'equal']
expected = [
    ('delete', 17425, 17450, 17425, 17425),   # 舊 L17426–17450 函數
    ('delete', 17509, 17513, 17484, 17484),   # 舊 L17510–17513 canAudition try
    ('delete', 17558, 17562, 17529, 17529),   # 舊 L17559–17562 gateShortReason try
    ('replace', 22736, 22737, 22703, 22704),  # 舊 L22737 FAVOR_DUE 註解
    ('replace', 22930, 22931, 22897, 22898),  # 舊 L22931 RIPPLE 註解
    ('replace', 23379, 23381, 23346, 23348),  # 舊 L23380–23381 屋企債註解
    ('delete', 35369, 35370, 35336, 35336),   # 舊 L35370 __freeplay export
    ('delete', 35449, 35450, 35415, 35415),   # 舊 L35450 自檢 debt_lock
    ('delete', 35483, 35484, 35448, 35448),   # 舊 L35484 回傳欄位 debtLock
]
assert non_eq == expected, non_eq
assert NEW[17425] == 'function softCastingTagGate(gig){', NEW[17425]
assert NEW[22703] == '   到期＝作廢（唔設逾期狀態）。', NEW[22703]
assert NEW[22897] == '   永不設「已逾期」status（跟 F1，到期＝作廢）。 ===== */', NEW[22897]
assert NEW[23346] == '   - 永不逾期：status 恆「未到期」、無 dueDay（唔入 favorDue 流程）；favorPressure 計算明確排除', NEW[23346]
assert NEW[42452] == 'function openLoc(id, opts){', NEW[42452]
assert 'openLoc: function(id, opts){ openLoc(id, opts); }' in NEW[29064], NEW[29064]
print('drift check OK: 9 hunks only (3 deletes zone A + 3 comment replaces + 3 deletes __freeplay), net -36')

def shift(n):
    """舊行號 -> 新行號（v327 分區漂移）。刪除區內錨點唔應該存在，直接 raise。"""
    if n < 17426:
        return n
    if n <= 17562:
        raise AssertionError('anchor inside deleted zone A: %d' % n)
    if n <= 35369:
        return n - 33
    if n == 35370:
        raise AssertionError('anchor is deleted export line 35370')
    if n <= 35449:
        return n - 34
    if n == 35450:
        raise AssertionError('anchor is deleted self-check line 35450')
    if n <= 35483:
        return n - 35
    if n == 35484:
        raise AssertionError('anchor is deleted return-field line 35484')
    return n - 36

def anchor(n_new, frag):
    assert frag in NEW[n_new - 1], (n_new, frag, NEW[n_new - 1][:90])
    return True

def replace_once(path, old, new, expect=1):
    s = open(path, encoding='utf-8').read()
    n = s.count(old)
    assert n == expect, (path, old[:70], n, expect)
    open(path, 'w', encoding='utf-8').write(s.replace(old, new))
    print('  %s: replaced %r (x%d)' % (path, old[:60], n))

def prepend_header(path, line):
    s = open(path, encoding='utf-8').read()
    assert not s.startswith(line), path
    open(path, 'w', encoding='utf-8').write(line + '\n' + s)
    print('  %s: header added' % path)

# ---- 2. gift185 / tang171 / tang173：總行數算術鏈 ----
for path, counter in [('tests/test_gift185_static.py', "html.count('" + BS + "n')"),
                      ('tests/test_tang171_static.py', "src.count('" + BS + "n')"),
                      ('tests/test_tang173_static.py', "src.count('" + BS + "n')")]:
    replace_once(path, '總行數 47280（', '總行數 47244（')
    replace_once(path, '＋v323 −9＋v326 −1）', '＋v323 −9＋v326 −1＋v327 −36）')
    replace_once(path, '%s == 47280' % counter, '%s == 47244' % counter)
    prepend_header(path,
        '# v20a327 resync：index.html 淨 −36 行（刪死鎖：函數舊 L17426–17450＋兩 try block 舊 L17510–17513／17559–17562＋__freeplay 三行舊 L35370／35450／35484；總行數 47280→47244；其後錨點按段 −33／−34／−35／−36，difflib 對位核實純漂移，見 qa327/resync327.py）。')
# tang171 / tang173：openLoc DEF 釘行（舊 42489，≥35485 區 → −36 → 42453）
for path in ['tests/test_tang171_static.py', 'tests/test_tang173_static.py']:
    replace_once(path, 'openLoc DEF 行 42489（', 'openLoc DEF 行 42453（')
    replace_once(path, '＋v323 −9＋v326 −1，travel114 釘行）', '＋v323 −9＋v326 −1＋v327 −36，travel114 釘行）')
    replace_once(path, "len(lines) >= 42495 and 'function openLoc(id, opts){' in lines[42488]",
                 "len(lines) >= 42459 and 'function openLoc(id, opts){' in lines[42452]")
anchor(42453, 'function openLoc(id, opts){')

# ---- 3. rom176：line() 釘行（ok() 名入面嘅 L 號係歷史標籤，一律唔郁） ----
for old_n, frag in [(40721, '/* ===== v20a176 ROM176'),
                    (41071, 'function rom176ApplyGiftOverrides()'),
                    (42374, 'function addLocTalkGiftActs(add, L, npcId)'),
                    (42530, 'rom176TryIntercept(id)')]:
    new_n = shift(old_n)
    replace_once('tests/test_rom176_static.py', 'line(%d)' % old_n, 'line(%d)' % new_n)
    anchor(new_n, frag)
prepend_header('tests/test_rom176_static.py',
    '# v20a327 resync：index.html 淨 −36 行（刪死鎖；4 個釘行各 −36（40721→40685、41071→41035、42374→42338、42530→42494；6321／14772 喺刪除點之前唔郁），內容逐字核實純漂移；L55647 等名唔郁，見 qa327/resync327.py）。')

# ---- 4. travel114：FREE／COUNT 區塊逐行行首數字按分區 shift＋DEF／WRAPPER ----
p = 'tests/test_travel114_static.py'
s = open(p, encoding='utf-8').read()
for block in ['FREE_LINES = {', 'COUNT_LINES = {']:
    a = s.index(block)
    b = s.index('}', a)
    seg_lines = s[a:b].split('\n')
    out = []
    for ln in seg_lines:
        m = re.match(r'^( *)([0-9]+),', ln)
        if m:
            old_n = int(m.group(2))
            out.append(ln[:m.start(2)] + str(shift(old_n)) + ln[m.end(2):])
        else:
            out.append(ln)
    seg2 = '\n'.join(out)
    assert seg2 != s[a:b], block
    s = s[:a] + seg2 + s[b:]
    print('  %s: %s block shifted' % (p, block))
s = s.replace('DEF_LINE = 42489', 'DEF_LINE = 42453', 1)
s = s.replace('WRAPPER_LINE = 29098', 'WRAPPER_LINE = 29065', 1)
open(p, 'w', encoding='utf-8').write(s)
anchor(42453, 'function openLoc(id, opts){')
anchor(29065, 'openLoc: function(id, opts){ openLoc(id, opts); }')
# 逐個 FREE／COUNT 錨點內容核實：FREE 行帶免費旗，COUNT 行唔帶
FREE_FLAGS = ('travelFree:true', 'encDone:true', 'forceRestore:true', 'wf4Done:true')
ns = {}
for block in ['FREE_LINES = {', 'COUNT_LINES = {']:
    a = s.index(block)
    b = s.index('}', a)
    exec(s[a:b + 1], ns)
for ln in sorted(ns['FREE_LINES']):
    assert any(f in NEW[ln - 1] for f in FREE_FLAGS), ('FREE', ln, NEW[ln - 1][:80])
for ln in sorted(ns['COUNT_LINES']):
    assert not any(f in NEW[ln - 1] for f in FREE_FLAGS), ('COUNT', ln, NEW[ln - 1][:80])
print('  %s: FREE %d + COUNT %d anchors content-verified' % (p, len(ns['FREE_LINES']), len(ns['COUNT_LINES'])))
prepend_header(p,
    '# v20a327 resync：index.html 淨 −36 行（刪死鎖；FREE／COUNT 錨點按分區 shift（＜17426 唔郁、17563–35369 −33、≥35485 −36；28337 等舊釘行已重算，內容逐行核實純漂移）＋DEF 42489→42453＋WRAPPER 29098→29065，見 qa327/resync327.py）。')

print('resync327 done')
