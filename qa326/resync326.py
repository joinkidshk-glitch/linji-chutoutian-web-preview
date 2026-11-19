# qa326/resync326.py — v20a326 resync：index.html 淨 −1 行
# （刪 WEAK_MARKS 死常數舊 L27959 一行＋L12541 註解刪括號一句；
#  其後錨點一律 −1，之前唔郁；difflib 對位核實純漂移）。
# 用法：python3 qa326/resync326.py  （喺工作副本根目錄行；只改 3 檔測試，唔郁 index.html）
# 原則：逐對 re.sub 會撞值丟失／重複——全部用單次掃描 dict 查表＋精確錨點＋次數斷言。
import difflib
import subprocess

ROOT = '.'
NEW = open('index.html', encoding='utf-8').read().splitlines()
OLD = subprocess.check_output(['git', 'show', 'HEAD:index.html'], text=True).splitlines()

# ---- 1. difflib 核實純漂移：淨 −1，只得兩處非 equal hunk ----
#   (a) 舊 L12541 註解 replace（0-based 12540，1 行換 1 行）；
#   (b) 舊 L27959 WEAK_MARKS 定義 delete（0-based 27958，刪 1 行）。
assert len(OLD) == 47281 and len(NEW) == 47280, (len(OLD), len(NEW))
assert 'WEAK_MARKS' not in '\n'.join(NEW), 'WEAK_MARKS still present in new index.html'
sm = difflib.SequenceMatcher(a=OLD, b=NEW, autojunk=False)
non_eq = [(tag, i1, i2, j1, j2) for tag, i1, i2, j1, j2 in sm.get_opcodes() if tag != 'equal']
assert len(non_eq) == 2, non_eq
assert non_eq[0] == ('replace', 12540, 12541, 12540, 12541), non_eq[0]
assert non_eq[1] == ('delete', 27958, 27959, 27958, 27958), non_eq[1]
assert NEW[12540] == '   -「大牌」「爛片」：專檔原詞，現行內容未有同名標籤，先入清單，', NEW[12540]
assert NEW[27958] == 'function debtStatusLabel(status){', NEW[27958]
print('drift check OK: only old L12541 (comment) + old L27959 (WEAK_MARKS) changed, net -1')

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
# gift185 / tang171 / tang173：算術鏈（名＋斷言一併改）
for path, counter in [('tests/test_gift185_static.py', "html.count('\\n')"),
                      ('tests/test_tang171_static.py', "src.count('\\n')"),
                      ('tests/test_tang173_static.py', "src.count('\\n')")]:
    replace_once(path, '總行數 47281（', '總行數 47280（')
    replace_once(path, '＋v323 −9）', '＋v323 −9＋v326 −1）')
    replace_once(path, '%s == 47281' % counter, '%s == 47280' % counter)
    prepend_header(path,
        '# v20a326 resync：index.html 淨 −1 行（刪 WEAK_MARKS 死常數舊 L27959；總行數 47281→47280；其後錨點一律 −1，difflib 對位核實純漂移，見 qa326/resync326.py）。')
# tang171 / tang173：openLoc DEF 釘行
for path in ['tests/test_tang171_static.py', 'tests/test_tang173_static.py']:
    replace_once(path, 'openLoc DEF 行 42490（', 'openLoc DEF 行 42489（')
    replace_once(path, '＋v323 −9，travel114 釘行）', '＋v323 −9＋v326 −1，travel114 釘行）')
    replace_once(path, "len(lines) >= 42496 and 'function openLoc(id, opts){' in lines[42489]",
                 "len(lines) >= 42495 and 'function openLoc(id, opts){' in lines[42488]")
anchor(42489, 'function openLoc(id, opts){')

print('resync326 done')
