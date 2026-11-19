# qa336/resync336.py — v20a336 漂移 resync（跨年即派修復）
# 背景：grant229GigById 加三年全庫 fallback（註解 ＋5＠舊 L27148 後、查表體 1→13 行
# ＠舊 L27151）＋grant229Record 註解改字（1→1＠舊 L27171）＋grant229DeliverOne 派發後
# 補入 GIGS（＋7＠舊 L27282 後）。淨 +24，47272→47296；difflib 對位核實 4 處 hunk。
# 錨點 shift（舊＝v335 HEAD 行號，1-based）：
#   ≤27148 唔郁、27149–27151 ＋5、27152–27282 ＋17、≥27283 ＋24。
#   （travel114 集合 52 個錨：21 個 ≤27148、31 個 ≥27283，邊界段冇錨。）
# 用法：python3 qa336/resync336.py（喺工作副本根目錄行；只改 5 檔測試，唔郁 index.html）
import difflib
import re
import subprocess

NL = chr(10)
NEW = open('index.html', encoding='utf-8').read().splitlines()
OLD = subprocess.check_output(['git', 'show', 'HEAD:index.html'], text=True).splitlines()

# ---- 1. difflib 核實漂移：淨 +24，只得 4 處非 equal hunk ----
assert len(OLD) == 47272 and len(NEW) == 47296, (len(OLD), len(NEW))
sm = difflib.SequenceMatcher(a=OLD, b=NEW, autojunk=False)
non_eq = [(tag, i1, i2, j1, j2) for tag, i1, i2, j1, j2 in sm.get_opcodes() if tag != 'equal']
expected = [
    ('insert', 27148, 27148, 27148, 27153),    # grant229GigById 註解 ＋5＠舊 L27148（函數行）之後
    ('replace', 27150, 27151, 27155, 27168),   # 查表體 1→13 行（全庫 fallback，淨 ＋12）＠舊 L27151
    ('replace', 27170, 27171, 27187, 27188),   # grant229Record 註解改字（1→1）＠舊 L27171
    ('insert', 27282, 27282, 27299, 27306),    # DeliverOne 補入 GIGS ＋7＠舊 L27282（scheduleShoot 行）之後
]
assert non_eq == expected, non_eq
assert OLD[27147] == 'function grant229GigById(gigId){', OLD[27147]
assert NEW[27147] == 'function grant229GigById(gigId){', NEW[27147]
assert NEW[27148].strip().startswith('/* v20a336'), NEW[27148]
assert 'STORY_WIRE.gigsByYear' in NEW[27158], NEW[27158]
assert 'normalizeGigRecord(f)' in NEW[27163], NEW[27163]
assert '全庫都無呢張' in NEW[27187], NEW[27187]
assert NEW[27298].strip().startswith('const shoot = scheduleShoot(gig'), NEW[27298]
assert NEW[27299].strip().startswith('/* v20a336'), NEW[27299]
assert 'GIGS.push(gig)' in NEW[27304], NEW[27304]
print('drift check OK: 4 hunks only, net +24')


def shift(n):
    """舊行號（v335 HEAD，1-based）-> 最終行號。"""
    if n <= 27148:
        return n
    if n <= 27151:
        return n + 5
    if n <= 27282:
        return n + 17
    return n + 24


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


HDR = '# v20a336 resync：跨年即派修復 drift（grant229GigById 全庫 fallback ＋17＠舊 L27148–27151＋DeliverOne 補入 GIGS ＋7＠舊 L27282 後；總計淨 +24，47272→47296；錨點按段 shift：≤27148 唔郁、27149–27151 ＋5、27152–27282 ＋17、≥27283 ＋24；內容逐行核實，見 qa336/resync336.py）。'

# ---- gift185：總行數 47272→47296（名＋值＋鏈尾）----
resync_pairs('tests/test_gift185_static.py', [
    ('總行數 47272（', '總行數 47296（', 1),
    ('＋v335b +9）', '＋v335b +9＋v336 +24）', 1),
    ('== 47272', '== 47296', 1),
], HDR)

# ---- tang171／tang173：總行數＋openLoc DEF 42492→42516（≥27283，＋24）----
for f in ('tests/test_tang171_static.py', 'tests/test_tang173_static.py'):
    resync_pairs(f, [
        ('總行數 47272（', '總行數 47296（', 1),
        ('＋v335b +9）', '＋v335b +9＋v336 +24）', 1),
        ('== 47272', '== 47296', 1),
        ('openLoc DEF 行 42492（', 'openLoc DEF 行 42516（', 1),
        ('＋v335b +9，travel114 釘行）', '＋v335b +9＋v336 +24，travel114 釘行）', 1),
        ('len(lines) >= 42492', 'len(lines) >= 42516', 1),
        ('lines[42491]', 'lines[42515]', 1),
    ], HDR)
assert NEW[42515] == 'function openLoc(id, opts){', NEW[42515]
print('tang171/173 content check OK: openLoc DEF at 42516')

# ---- rom176：4 個釘行各 ＋24（40719／41069／42372／42533；6325／14776 喺插入點之前唔郁；ok() 名入面 L55647 等歷史標籤唔郁）----
resync_pairs('tests/test_rom176_static.py', [
    ('line(40719)', 'line(40743)', 1),
    ('line(41069)', 'line(41093)', 1),
    ('line(42372)', 'line(42396)', 1),
    ('line(42533)', 'line(42557)', 1),
], HDR)
assert NEW[40742].startswith('/* ===== v20a176 ROM176'), NEW[40742]
assert NEW[41092].startswith('function rom176ApplyGiftOverrides()'), NEW[41092]
assert NEW[42395].startswith('function addLocTalkGiftActs(add, L, npcId)'), NEW[42395]
assert 'rom176TryIntercept(id)' in NEW[42556], NEW[42556]
print('rom176 content check OK: 4 anchors')


# ---- travel114：COUNT／FREE 集合按段 shift＋DEF_LINE 42492→42516＋WRAPPER_LINE 29092→29116 ----
def resync_travel114():
    path = 'tests/test_travel114_static.py'
    lines = open(path, encoding='utf-8').read().splitlines()
    in_set = None
    changed = 0
    new_count = []
    new_free = []
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
                if in_set == 'COUNT':
                    new_count.append(new_n)
                else:
                    new_free.append(new_n)
    def_hit = [i for i, ln in enumerate(lines) if ln.startswith('DEF_LINE = 42492')]
    assert len(def_hit) == 1, def_hit
    lines[def_hit[0]] = 'DEF_LINE = 42516      # function openLoc(id, opts){'
    wr_hit = [i for i, ln in enumerate(lines) if ln.startswith('WRAPPER_LINE = 29092')]
    assert len(wr_hit) == 1, wr_hit
    lines[wr_hit[0]] = 'WRAPPER_LINE = 29116  # window.__phase2.openLoc：轉發 opts'
    assert changed == 31, changed  # 52 錨入面 31 個 ≥27283（＋24），21 個 ≤27148 唔郁
    for n in new_count:
        assert 'openLoc(' in NEW[n - 1], (n, NEW[n - 1])
        assert not any(f in NEW[n - 1] for f in ('travelFree:true', 'encDone:true', 'forceRestore:true', 'wf4Done:true')), (n, NEW[n - 1])
    for n in new_free:
        assert 'openLoc(' in NEW[n - 1], (n, NEW[n - 1])
        assert any(f in NEW[n - 1] for f in ('travelFree:true', 'encDone:true', 'forceRestore:true', 'wf4Done:true')), (n, NEW[n - 1])
    assert NEW[42515] == 'function openLoc(id, opts){', NEW[42515]
    assert 'openLoc: function(id, opts){ openLoc(id, opts); }' in NEW[29115], NEW[29115]
    open(path, 'w', encoding='utf-8').write(HDR + NL + NL.join(lines) + NL)
    print('resynced tests/test_travel114_static.py (%d set shifts)' % changed)


resync_travel114()
print('ALL RESYNC DONE')
