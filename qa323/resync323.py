# qa323/resync323.py — v20a323 resync：index.html 淨 −9 行
# （刪 TEXTFIX57 死映射 5 條＋KEY_RENAME＋walk hook 簡化，刪除區間舊 L14401–14487；
#  其後錨點一律 −9，之前唔郁；difflib 對位核實純漂移）。
# 用法：python3 qa323/resync323.py  （喺工作副本根目錄行；只改 8 檔測試，唔郁 index.html）
# 原則：逐對 re.sub 會撞值丟失／重複——全部用單次掃描 dict 查表＋精確錨點＋次數斷言。
import difflib
import re
import subprocess
import sys

ROOT = '.'
NEW = open('index.html', encoding='utf-8').read().splitlines()
OLD = subprocess.check_output(['git', 'show', 'HEAD:index.html'], text=True).splitlines()

# ---- 1. difflib 核實純漂移：所有非 equal hunk 必須喺舊 L14398–14487 之內，淨 −9 ----
assert len(OLD) == 47290 and len(NEW) == 47281, (len(OLD), len(NEW))
sm = difflib.SequenceMatcher(a=OLD, b=NEW, autojunk=False)
for tag, i1, i2, j1, j2 in sm.get_opcodes():
    if tag != 'equal':
        assert 14397 <= i1 and i2 <= 14487, (tag, i1, i2, j1, j2)
print('drift check OK: only old lines 14398-14487 changed, net -9')

def new_line(n_old):
    """舊行號（1-based）→ 新行號；刪除區間之前唔郁，之後 −9。"""
    assert n_old > 14487 or n_old < 14401, n_old
    return n_old if n_old < 14401 else n_old - 9

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

# ---- 2. 各檔釘行（ok() 名入面嘅 L 號係歷史標籤，一律唔郁） ----
# tang152：lines() 0-based 索引
replace_once('tests/test_tang152_static.py', 'lines()[14708]', 'lines()[14699]')
replace_once('tests/test_tang152_static.py', 'lines()[14835]', 'lines()[14826]')
anchor(14700, 'function normaliseTangStub152(pack){')
anchor(14827, 'try{ normaliseTangStub152(rom2);')
prepend_header('tests/test_tang152_static.py',
    '# v20a323 resync：index.html 淨 −9 行（刪 TEXTFIX57 死映射，刪除區間舊 L14401–14487）；2 個釘索引各 −9（14708→14699、14835→14826），內容逐字核實純漂移；ok() 名入面嘅 L 號係歷史標籤，唔郁。')

# text125：b.text 釘行（0-based ls 索引）
replace_once('tests/test_text125_static.py', 'if len(ls) < 16350', 'if len(ls) < 16341')
replace_once('tests/test_text125_static.py', "not in ls[16349]", "not in ls[16340]")
replace_once('tests/test_text125_static.py', 'applyFamilySafeToNode 第 16350 行冇 b.text 分支', 'applyFamilySafeToNode 第 16341 行冇 b.text 分支')
anchor(16341, 'if(typeof b.text === "string" && b.text){')
prepend_header('tests/test_text125_static.py',
    '# v20a323 resync：index.html 淨 −9 行（刪 TEXTFIX57 死映射，刪除區間舊 L14401–14487）；applyFamilySafeToNode b.text 釘行 −9（16350→16341），內容逐字核實純漂移；currentLine／advance 釘行喺刪除區間之前唔郁。')

# rom159：line_has 1-based 行號
for old_n, frag in [(25466, 'v20a159 ROM159 Phase 1'), (26314, 'COMMIT48_NODES.CMT_lan_commit'),
                    (14783, 'rom159ApplyGiftOverrides()'), (26215, 'function rom159SoMeetGate')]:
    replace_once('tests/test_rom159_static.py', 'line_has(%d,' % old_n, 'line_has(%d,' % new_line(old_n))
    anchor(new_line(old_n), frag)
replace_once('tests/test_rom159_static.py', 'idx_lines[25494 - 1]', 'idx_lines[25485 - 1]')
anchor(25485, '全佳')
prepend_header('tests/test_rom159_static.py',
    '# v20a323 resync：index.html 淨 −9 行（刪 TEXTFIX57 死映射，刪除區間舊 L14401–14487）；5 個釘行各 −9（25466→25457、26314→26305、14783→14774、26215→26206、全佳 25494→25485；8241／10699 喺刪除區間之前唔郁），內容逐字核實純漂移；ok() 名入面嘅 L 號係歷史標籤，唔郁。')

# rom176：line() 1-based 行號（14781 同行出現兩次，兩處一併改）
for old_n, frag, cnt in [(14781, 'GIFT_REACT = giftReact', 2), (40731, '/* ===== v20a176 ROM176', 1),
                    (41081, 'function rom176ApplyGiftOverrides()', 1), (42384, 'function addLocTalkGiftActs(add, L, npcId)', 1),
                    (42540, 'rom176TryIntercept(id)', 1)]:
    replace_once('tests/test_rom176_static.py', 'line(%d)' % old_n, 'line(%d)' % new_line(old_n), expect=cnt)
    anchor(new_line(old_n), frag)
prepend_header('tests/test_rom176_static.py',
    '# v20a323 resync：index.html 淨 −9 行（刪 TEXTFIX57 死映射，刪除區間舊 L14401–14487）；5 個釘行各 −9（14781→14772、40731→40722、41081→41072、42384→42375、42540→42531；6321 喺刪除區間之前唔郁），內容逐字核實純漂移；L55647 等名唔郁。')

# gift185 / tang171 / tang173：算術鏈（名＋斷言一併改）
for path, counter in [('tests/test_gift185_static.py', "html.count('\\n')"),
                      ('tests/test_tang171_static.py', "src.count('\\n')"),
                      ('tests/test_tang173_static.py', "src.count('\\n')")]:
    replace_once(path, '總行數 47290（', '總行數 47281（')
    replace_once(path, '＋v322 +4）', '＋v322 +4＋v323 −9）')
    replace_once(path, '%s == 47290' % counter, '%s == 47281' % counter)
    prepend_header(path,
        '# v20a323 resync：index.html 淨 −9 行（刪 TEXTFIX57 死映射 5 條＋KEY_RENAME＋walk hook 簡化，刪除區間舊 L14401–14487；總行數 47290→47281；其後錨點一律 −9，difflib 對位核實純漂移，見 qa323/resync323.py）。')
# tang171 / tang173：openLoc DEF 釘行
for path in ['tests/test_tang171_static.py', 'tests/test_tang173_static.py']:
    replace_once(path, 'openLoc DEF 行 42499（', 'openLoc DEF 行 42490（')
    replace_once(path, '＋v322 +4，travel114 釘行）', '＋v322 +4＋v323 −9，travel114 釘行）')
    replace_once(path, "len(lines) >= 42505 and 'function openLoc(id, opts){' in lines[42498]",
                 "len(lines) >= 42496 and 'function openLoc(id, opts){' in lines[42489]")
anchor(42490, 'function openLoc(id, opts){')

# travel114：FREE／COUNT 區塊內數字單次掃描 dict 查表（＞14487 者 −9，之前唔郁）＋DEF／WRAPPER
p = 'tests/test_travel114_static.py'
s = open(p, encoding='utf-8').read()
for block, bname in [('FREE_LINES = {', 'FREE'), ('COUNT_LINES = {', 'COUNT')]:
    a = s.index(block)
    b = s.index('}', a)
    seg = s[a:b]
    def shift(m):
        n = int(m.group(0))
        return str(n - 9 if n > 14487 else n)
    seg2 = re.sub(r'\b\d+\b', shift, seg)
    assert seg2 != seg, bname
    s = s[:a] + seg2 + s[b:]
    print('  %s: %s block shifted' % (p, bname))
s = s.replace('DEF_LINE = 42499', 'DEF_LINE = 42490', 1)
s = s.replace('WRAPPER_LINE = 29108', 'WRAPPER_LINE = 29099', 1)
open(p, 'w', encoding='utf-8').write(s)
anchor(42490, 'function openLoc(id, opts){')
anchor(29099, 'openLoc: function(id, opts){ openLoc(id, opts); }')
# 逐個 FREE／COUNT 錨點內容核實：FREE 行帶免費旗，COUNT 行唔帶
FREE_FLAGS = ('travelFree:true', 'encDone:true', 'forceRestore:true', 'wf4Done:true')
# 直接由檔案讀返兩個集合再核實
ns = {}
exec(re.search(r'(FREE_LINES = \{[^}]*\})', s).group(1), ns)
exec(re.search(r'(COUNT_LINES = \{[^}]*\})', s).group(1), ns)
for ln in sorted(ns['FREE_LINES']):
    assert any(f in NEW[ln - 1] for f in FREE_FLAGS), ('FREE', ln, NEW[ln - 1][:80])
for ln in sorted(ns['COUNT_LINES']):
    assert not any(f in NEW[ln - 1] for f in FREE_FLAGS), ('COUNT', ln, NEW[ln - 1][:80])
print('  %s: FREE %d + COUNT %d anchors content-verified' % (p, len(ns['FREE_LINES']), len(ns['COUNT_LINES'])))
prepend_header(p,
    '# v20a323 resync：index.html 淨 −9 行（刪 TEXTFIX57 死映射，刪除區間舊 L14401–14487）；其後錨點一律 −9（COUNT 12／FREE 30／DEF 42499→42490／WRAPPER 29108→29099），之前唔郁；difflib 對位核實純漂移，見 qa323/resync323.py。')

print('resync323 done')
