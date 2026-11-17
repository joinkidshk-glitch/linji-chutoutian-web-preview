# v20a280 resync：index.html 淨 +38 行（helper block ＋37 @舊 L38870 之後＋ngai fx 行 ＋1 @舊 L39065；
# 另 15 處 grants() 單行 replace 行數不變）；difflib 對位核實純漂移——5 檔釘行按映射重算，
# 內容逐行核實（見下）。用法：python3 qa280/resync280.py（由工作副本根目錄跑）。
import difflib, re, sys

OLD = '/home/hatch/workspace/linji-repo/index.html'  # main 451cb8a（v279）
NEW = 'index.html'
old = open(OLD, encoding='utf-8').read().splitlines()
new = open(NEW, encoding='utf-8').read().splitlines()
assert len(new) - len(old) == 38, (len(old), len(new))

# 單次掃描建舊→新行號映射（dict 查表）
mapping = {}
sm = difflib.SequenceMatcher(a=old, b=new, autojunk=False)
for tag, i1, i2, j1, j2 in sm.get_opcodes():
    if tag in ('equal', 'replace'):
        assert (i2 - i1) == (j2 - j1), (tag, i1, i2, j1, j2)
        for k in range(i2 - i1):
            mapping[i1 + 1 + k] = j1 + 1 + k
    elif tag == 'insert':
        pass  # 插入行無舊行號
    elif tag == 'delete':
        raise AssertionError('unexpected delete %d-%d' % (i1 + 1, i2))

def check_anchor(old_ln, label):
    nl = mapping[old_ln]
    ok = old[old_ln - 1] == new[nl - 1]
    print('%s 舊 L%d → 新 L%d 內容%s：%s' % (label, old_ln, nl, '一致' if ok else '！！不一致', old[old_ln - 1].strip()[:80]))
    return ok

all_ok = True
# travel114：COUNT 12／FREE 40／DEF／WRAPPER
for ln in (15395, 18794, 20995, 22197, 22637, 22640, 22671, 28124, 44616, 44828, 44986, 45007):
    all_ok &= check_anchor(ln, 'travel114 COUNT')
for ln in (6531, 6532, 8223, 14250, 14251, 14263, 14264, 14275, 14276, 14376, 24458, 25801, 25802,
           25878, 27933, 27966, 39530, 39649, 39724, 39932, 39976, 39982, 40049, 40051, 40054, 40081,
           41225, 41272, 41642, 41664, 41816, 41821, 42745, 44223, 44493, 44494, 44538, 44539, 44564, 45457):
    all_ok &= check_anchor(ln, 'travel114 FREE')
all_ok &= check_anchor(41377, 'travel114 DEF')
all_ok &= check_anchor(28693, 'travel114 WRAPPER')
# rom176：2 釘喺插入點之前唔郁＋4 釘之後 ＋38
for ln in (6325, 14813, 39732, 40090, 41262, 41418):
    all_ok &= check_anchor(ln, 'rom176')
# tang171／173 DEF 行
all_ok &= check_anchor(41377, 'tang DEF')
if not all_ok:
    print('ANCHOR MISMATCH — 停，唔改檔')
    sys.exit(1)

HDR = '# v20a280 resync：index.html 淨 +38 行（sideline280GrantCompletion helper ＋37 @舊 L38870 之後＋ngai_vouch fx 行 ＋1 @舊 L39065；15 處 grants() 單行原地改，行數不變）；釘行按 difflib 映射重算（插入點之前唔郁、38870–39064 者 ＋37、其後者 ＋38；本批全部受影響釘行喺 ＋38 區），內容逐行核實純漂移（見 qa280/resync280.py）。\n'

def insert_hdr(lines, fname):
    for i, l in enumerate(lines):
        if '# v20a279 resync' in l:
            lines.insert(i, HDR)
            print(fname, '：header 插喺第 %d 行之前' % (i + 1))
            return
    raise AssertionError(fname + ' 搵唔到 v279 header 行')

def rewrite(path, fn):
    lines = open(path, encoding='utf-8').read().splitlines(keepends=True)
    fn(lines)
    insert_hdr(lines, path)
    open(path, 'w', encoding='utf-8').write(''.join(lines))
    print(path, '已寫')

# ---- travel114：COUNT_LINES／FREE_LINES 集合內整數＋DEF_LINE 用 dict 查表（單次掃描） ----
def fix_travel114(lines):
    in_set = None
    for i, l in enumerate(lines):
        if l.startswith('COUNT_LINES = {'):
            in_set = 'count'
        elif l.startswith('FREE_LINES = {'):
            in_set = 'free'
        elif in_set and l.startswith('}'):
            in_set = None
        elif in_set:
            m = re.match(r'^(\s*)(\d+)(,.*)$', l)
            if m:
                lines[i] = m.group(1) + str(mapping[int(m.group(2))]) + m.group(3) + '\n'
        m2 = re.match(r'^DEF_LINE = (\d+)(\s+#.*)$', l)
        if m2:
            lines[i] = 'DEF_LINE = %d%s\n' % (mapping[int(m2.group(1))], m2.group(2))
rewrite('tests/test_travel114_static.py', fix_travel114)

# ---- rom176：4 個 line(N) 釘（6325／14813 喺插入點之前，唔郁） ----
def fix_rom176(lines):
    for i, l in enumerate(lines):
        m = re.search(r'line\((\d+)\)', l)
        if m and '釘：' in l:
            old_n = int(m.group(1))
            if old_n in mapping and mapping[old_n] != old_n:
                lines[i] = l.replace('line(%d)' % old_n, 'line(%d)' % mapping[old_n], 1)
rewrite('tests/test_rom176_static.py', fix_rom176)

# ---- gift185／tang171／tang173：總行數＋DEF 行（只改 ok( 斷言行，唔掂註解） ----
def fix_chain(lines, with_def):
    for i, l in enumerate(lines):
        if l.lstrip().startswith("ok('") and '總行數 46129' in l:
            assert '＋v279 +99）' in l and '== 46129' in l
            lines[i] = l.replace('總行數 46129', '總行數 46167', 1) \
                        .replace('＋v279 +99）', '＋v279 +99＋v280 +38）', 1) \
                        .replace('== 46129', '== 46167', 1)
        if with_def and l.lstrip().startswith("ok('") and 'openLoc DEF 行 41377' in l:
            assert '＋v279 +97，travel114' in l
            lines[i] = l.replace('openLoc DEF 行 41377', 'openLoc DEF 行 41415', 1) \
                        .replace('＋v279 +97，travel114', '＋v279 +97＋v280 +38，travel114', 1)
rewrite('tests/test_gift185_static.py', lambda ls: fix_chain(ls, False))
rewrite('tests/test_tang171_static.py', lambda ls: fix_chain(ls, True))
rewrite('tests/test_tang173_static.py', lambda ls: fix_chain(ls, True))
print('RESYNC280 OK')
