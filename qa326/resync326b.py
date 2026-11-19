# qa326/resync326b.py — v20a326 resync 續：rom176＋travel114（suite 兜底）
# （刪 WEAK_MARKS 死常數舊 L27959 淨 −1 行之後，suite 多出 2 個 FAIL；
#  difflib 已核實 index.html 只有 L12541＋L27959 兩處改動，兩檔皆純 −1 漂移）。
# 用法：python3 qa326/resync326b.py  （喺工作副本根目錄行；只改 2 檔測試，唔郁 index.html）
# 原則：逐對 re.sub 會撞值丟失／重複——全部用單次掃描 dict 查表＋精確錨點＋次數斷言。
import re
import subprocess

NEW = open('index.html', encoding='utf-8').read().splitlines()
OLD = subprocess.check_output(['git', 'show', 'HEAD:index.html'], text=True).splitlines()
assert len(OLD) == 47281 and len(NEW) == 47280, (len(OLD), len(NEW))

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

# ---- rom176：line() 1-based 釘行，＞27959 者 −1；ok() 名入面嘅 L 號係歷史標籤，唔郁 ----
for old_n, frag in [(40722, '/* ===== v20a176 ROM176'),
                    (41072, 'function rom176ApplyGiftOverrides()'),
                    (42375, 'function addLocTalkGiftActs(add, L, npcId)'),
                    (42531, 'rom176TryIntercept(id)')]:
    replace_once('tests/test_rom176_static.py', 'line(%d)' % old_n, 'line(%d)' % (old_n - 1))
    anchor(old_n - 1, frag)
prepend_header('tests/test_rom176_static.py',
    '# v20a326 resync：index.html 淨 −1 行（刪 WEAK_MARKS 死常數舊 L27959；4 個釘行各 −1（40722→40721、41072→41071、42375→42374、42531→42530；6321／14772 喺刪除點之前唔郁），內容逐字核實純漂移；L55647 等名唔郁，見 qa326/resync326b.py）。')

# ---- travel114：FREE／COUNT 區塊內數字單次掃描 dict 查表（＞27959 者 −1，之前唔郁）＋DEF／WRAPPER ----
p = 'tests/test_travel114_static.py'
s = open(p, encoding='utf-8').read()
for block, bname in [('FREE_LINES = {', 'FREE'), ('COUNT_LINES = {', 'COUNT')]:
    a = s.index(block)
    b = s.index('}', a)
    seg = s[a:b]
    def shift(m):
        n = int(m.group(0))
        return str(n - 1 if n > 27959 else n)
    seg2 = re.sub(r'\b\d+\b', shift, seg)
    assert seg2 != seg, bname
    s = s[:a] + seg2 + s[b:]
    print('  %s: %s block shifted' % (p, bname))
s = s.replace('DEF_LINE = 42490', 'DEF_LINE = 42489', 1)
s = s.replace('WRAPPER_LINE = 29099', 'WRAPPER_LINE = 29098', 1)
open(p, 'w', encoding='utf-8').write(s)
anchor(42489, 'function openLoc(id, opts){')
anchor(29098, 'openLoc: function(id, opts){ openLoc(id, opts); }')
# 逐個 FREE／COUNT 錨點內容核實：FREE 行帶免費旗，COUNT 行唔帶
FREE_FLAGS = ('travelFree:true', 'encDone:true', 'forceRestore:true', 'wf4Done:true')
ns = {}
exec(re.search(r'(FREE_LINES = \{[^}]*\})', s).group(1), ns)
exec(re.search(r'(COUNT_LINES = \{[^}]*\})', s).group(1), ns)
for ln in sorted(ns['FREE_LINES']):
    assert any(f in NEW[ln - 1] for f in FREE_FLAGS), ('FREE', ln, NEW[ln - 1][:80])
for ln in sorted(ns['COUNT_LINES']):
    assert not any(f in NEW[ln - 1] for f in FREE_FLAGS), ('COUNT', ln, NEW[ln - 1][:80])
print('  %s: FREE %d + COUNT %d anchors content-verified' % (p, len(ns['FREE_LINES']), len(ns['COUNT_LINES'])))
prepend_header(p,
    '# v20a326 resync：index.html 淨 −1 行（刪 WEAK_MARKS 死常數舊 L27959；COUNT 5 處＋FREE 26 處＋DEF 42490→42489＋WRAPPER 29099→29098 各 −1，之前唔郁；difflib 對位核實純漂移，見 qa326/resync326b.py）。')

print('resync326b done')
