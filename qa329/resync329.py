# qa329/resync329.py — v20a329 resync：index.html 淨 −13 行
# （刪死函數舊 L45312–45330＝19 行＋doAudition fail branch 搬入教學 toast 6 行＠舊 L45531 之後
#  ＋L17682 註解改寫；總行數 47262→47249；其後錨點按段 shift（45331–45531 −19、≥45532 −13），
#  difflib 對位核實純漂移；單次掃描 dict 查表＋精確錨點＋次數斷言）。
# 用法：python3 qa329/resync329.py  （喺工作副本根目錄行；只改 5 檔測試，唔郁 index.html）
# 註：brief 寫「淨 −18 行／總行數 47244」係算錯數——死函數實為 19 行（舊 L45312–45330，連埋
#  閉括號行），搬入 doAudition 嘅教學 toast 係 6 行，淨 −19＋6＝−13，總行數 47249。按實測處理。
import difflib
import re
import subprocess

NL = chr(10)
NEW = open('index.html', encoding='utf-8').read().splitlines()
OLD = subprocess.check_output(['git', 'show', 'HEAD:index.html'], text=True).splitlines()

# ---- 1. difflib 核實純漂移：淨 −13，只得 3 處非 equal hunk ----
assert len(OLD) == 47262 and len(NEW) == 47249, (len(OLD), len(NEW))
sm = difflib.SequenceMatcher(a=OLD, b=NEW, autojunk=False)
non_eq = [(tag, i1, i2, j1, j2) for tag, i1, i2, j1, j2 in sm.get_opcodes() if tag != 'equal']
expected = [
    ('replace', 17681, 17682, 17681, 17682),  # 舊 L17682 註解：promptAudition → doAudition
    ('delete', 45311, 45330, 45311, 45311),   # 舊 L45312–45330 死函數 19 行全刪
    ('insert', 45531, 45531, 45512, 45518),   # 舊 L45531 之後插入教學 toast 6 行
]
assert non_eq == expected, non_eq
assert 'promptAudition' in OLD[17681] and 'promptAudition' not in NEW[17681], NEW[17681]
assert 'doAudition' in NEW[17681], NEW[17681]
assert OLD[45311].startswith('function promptAudition'), OLD[45311]
assert OLD[45329].strip() == '}', OLD[45329]
assert OLD[45330] == '', OLD[45330]
assert NEW[45311] == '', NEW[45311]
assert NEW[45511] == '  if(!gate.ok){', NEW[45511]
assert NEW[45512].strip() == 'S.flags=S.flags||{};', NEW[45512]
assert 'const back=' in NEW[45513] and 'openLoc(L.id, {travelFree:true})' in NEW[45513], NEW[45513]
assert 'sawTutAudLock' in NEW[45514], NEW[45514]
assert 'maybeShowTutToast("sawTutAudLock","TUT_AUD_LOCK", back);' in NEW[45515], NEW[45515]
assert NEW[45516].strip() == 'return;', NEW[45516]
assert NEW[45517].strip() == '}', NEW[45517]
assert 'toast(gate.reason' in NEW[45518], NEW[45518]
assert NEW[42470] == 'function openLoc(id, opts){', NEW[42470]
print('drift check OK: 3 hunks only (comment rewrite + delete 19 + insert 6), net -13')


def shift(n):
    """舊行號 -> 新行號（v329：＜45312 唔郁、45312–45330 刪除區、45331–45531 −19、≥45532 −13）。"""
    if n < 45312:
        return n
    if n <= 45531:
        return n - 19
    return n - 13


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


HDR = '# v20a329 resync：index.html 淨 −13 行（刪死函數 19 行＠舊 L45312–45330＋doAudition fail branch 搬入教學 toast 6 行＠舊 L45531 之後；總行數 47262→47249；其後錨點按段 shift（45331–45531 −19、≥45532 −13），difflib 對位核實純漂移，見 qa329/resync329.py）。'

# gift185：總行數 1 處（名＋值）
resync_pairs('tests/test_gift185_static.py', [
    ('總行數 47262（', '總行數 47249（', 1),
    ('＋v328 ＋18）', '＋v328 ＋18＋v329 −13）', 1),
    ('== 47262', '== 47249', 1),
], HDR)

# tang171／tang173：總行數（名＋值）；openLoc DEF 42471／guard 42477／index 42470 喺刪除點之前，唔郁
for f in ('tests/test_tang171_static.py', 'tests/test_tang173_static.py'):
    resync_pairs(f, [
        ('總行數 47262（', '總行數 47249（', 1),
        ('＋v328 ＋18）', '＋v328 ＋18＋v329 −13）', 1),
        ('== 47262', '== 47249', 1),
    ], HDR)


# travel114：COUNT／FREE 集合（＜45312 唔郁、45317 刪、≥45532 −13）＋新 FREE 錨 45514
def resync_travel114():
    path = 'tests/test_travel114_static.py'
    lines = open(path, encoding='utf-8').read().splitlines()
    in_set = None
    changed = 0
    replaced = 0
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
                if in_set == 'FREE' and old_n == 45317:
                    # 刪舊錨，原位換做搬入咗嘅 back 行（新 45514，排序 43840＜45514＜45611）
                    lines[i] = '    45514,  # doAudition fail branch：首次教學 toast back（v329 由死函數搬入，travelFree）'
                    replaced += 1
                    continue
                new_n = shift(old_n)
                if new_n != old_n:
                    lines[i] = m.group(1) + str(new_n) + m.group(3)
                    changed += 1
    # DEF／WRAPPER 喺刪除點之前，唔郁（只核實在位）
    assert any(ln.startswith('DEF_LINE = 42471') for ln in lines), 'DEF_LINE moved?!'
    assert any(ln.startswith('WRAPPER_LINE = 29083') for ln in lines), 'WRAPPER_LINE moved?!'
    # 預期：COUNT 4 處（45747／45955／46113／46134）＋FREE 6 處（45624／45625／45669／45670／45695／46584）shift，舊 45317 換做新 45514
    assert changed == 10, changed
    assert replaced == 1, replaced
    # 內容核實：每個新錨點行實際係 openLoc( 呼叫點；FREE 錨帶旗、COUNT 錨唔帶旗
    for n in (45734, 45942, 46100, 46121):
        assert 'openLoc(' in NEW[n - 1], (n, NEW[n - 1])
        assert 'travelFree:true' not in NEW[n - 1] and 'encDone:true' not in NEW[n - 1], (n, NEW[n - 1])
    for n in (45514, 45611, 45612, 45656, 45657, 45682, 46571):
        assert 'openLoc(' in NEW[n - 1], (n, NEW[n - 1])
        assert ('travelFree:true' in NEW[n - 1] or 'encDone:true' in NEW[n - 1]), (n, NEW[n - 1])
    open(path, 'w', encoding='utf-8').write(
        '# v20a329 resync：index.html 淨 −13 行（刪死函數 19 行＠舊 L45312–45330＋doAudition 搬入教學 toast 6 行；FREE 刪舊 45317、加新 45514（搬入嘅 back 行）、其後 6 處 −13，COUNT 4 處 −13；DEF 42471／WRAPPER 29083 唔郁，內容逐行核實純漂移，見 qa329/resync329.py）。' + NL + NL.join(lines) + NL)
    print('resynced tests/test_travel114_static.py (10 shifts + 1 replaced anchor)')


resync_travel114()
print('ALL RESYNC DONE')
