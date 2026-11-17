# qa284 resync: 5 檔靜態測試＋nat92 邏輯計數重算（v284，index.html 淨 +58 行）。
# 插入點（舊行號，見 git diff -U0 index.html hunk 頭）：
#   F 註解 ＋1＠舊 L26424 之後（舊 26424 行本身改寫，＋1 由 26425 起）；
#   BR89 film_114 行 ＋1＠舊 L26433 之後；C2 註解 ＋1＠舊 L26534 之後；
#   mockAskDefs hint ＋10＠舊 L27679 之後；E helpers ＋20＠舊 L40570 之後；
#   TeaListen cap ＋6＠舊 L40573（原地 1→7 行）；強制風聲 ＋11＠舊 L40577 之後；
#   消耗 ＋5＠舊 L40613 之後；G tick ＋3＠舊 L40745（原地 1→4 行）。
# 段規則（舊行 → shift）：＜26425 ＋0；26425–26433 ＋1；26434–26534 ＋2；
#   26535–27679 ＋3；27680–40570 ＋13；40571–40573 ＋33；40574–40577 ＋39；
#   40578–40613 ＋50；40614–40745 ＋55；≥40746 ＋58。
# 單次掃描 dict 查表（只換 dict／set 區行首 key 數字，唔逐對 re.sub，免撞值）；
# 其餘檔案用長錨點精確替換；改完逐行對內容核實（唔信算術，信內容）。
# 冪等：每節先檢查舊值係咪仲喺度，已經 resync 過就跳過重寫、淨係核實。
import re

ROOT = '/home/hatch/workspace/linji-work284'
html_lines = open(ROOT + '/index.html', encoding='utf-8').read().split('\n')
bad = []
BS = chr(92)  # 測試檔 count('X') 入面 X 係一個反斜線＋n；用 chr(92) 拼字串，避開原始碼轉義混亂


def shift(n):
    if n < 26425:
        return 0
    if n <= 26433:
        return 1
    if n <= 26534:
        return 2
    if n <= 27679:
        return 3
    if n <= 40570:
        return 13
    if n <= 40573:
        return 33
    if n <= 40577:
        return 39
    if n <= 40613:
        return 50
    if n <= 40745:
        return 55
    return 58


def new(n):
    return n + shift(n)


def check(cond, label, detail=''):
    if not cond:
        bad.append((label, detail[:90]))


def resync_set(text, start_marker, mapping):
    i = text.index(start_marker)
    j = text.index('\n}', i)
    region = text[i:j]

    def repl(m):
        n = int(m.group(2))
        return m.group(1) + str(mapping.get(n, n)) + m.group(3)

    return text[:i] + re.sub(r'^(\s*)(\d+)(,)', repl, region, flags=re.M) + text[j:]


# ---------- 1. travel114：FREE／COUNT set＋DEF＋WRAPPER ----------
p = ROOT + '/tests/test_travel114_static.py'
src = open(p, encoding='utf-8').read()
free_cur = sorted(int(x) for x in re.findall(r'^    (\d+),', src[src.index('FREE_LINES = {'):src.index('\n}', src.index('FREE_LINES = {'))], flags=re.M))
count_cur = sorted(int(x) for x in re.findall(r'^    (\d+),', src[src.index('COUNT_LINES = {'):src.index('\n}', src.index('COUNT_LINES = {'))], flags=re.M))
if 'DEF_LINE = 41491' in src:
    free_map = {n: new(n) for n in free_cur}
    count_map = {n: new(n) for n in count_cur}
    src = resync_set(src, 'FREE_LINES = {', free_map)
    src = resync_set(src, 'COUNT_LINES = {', count_map)
    src = src.replace('DEF_LINE = 41491', 'DEF_LINE = %d' % new(41491), 1)
    src = src.replace('WRAPPER_LINE = 28769', 'WRAPPER_LINE = %d' % new(28769), 1)
    comment = ("# v20a284 resync：index.html 淨 +58 行（F 註解＋1／BR89 film_114＋1／C2 註解＋1／"
               "mockAskDefs hint＋10／E helpers＋20／TeaListen cap＋6／強制風聲＋11／消耗＋5／G tick＋3；"
               "COUNT／FREE／DEF／WRAPPER 按段重算：＜26425 唔郁、26425–26433 ＋1、26434–26534 ＋2、"
               "26535–27679 ＋3、27680–40570 ＋13、40571–40573 ＋33、40574–40577 ＋39、40578–40613 ＋50、"
               "40614–40745 ＋55、≥40746 ＋58；DEF 41491→41549、WRAPPER 28769→28782），"
               "內容逐行核實純漂移。\n")
    if 'v20a284 resync' not in src:
        src = comment + src
    open(p, 'w', encoding='utf-8').write(src)
    free_cur = [new(n) for n in free_cur]
    count_cur = [new(n) for n in count_cur]

FLAGS = ("travelFree:true", "encDone:true", "forceRestore:true", "wf4Done:true")
for n in free_cur + count_cur:
    check('openLoc(' in html_lines[n - 1], 'travel114 %d openLoc' % n, html_lines[n - 1])
for n in free_cur:
    check(any(f in html_lines[n - 1] for f in FLAGS), 'travel114 FREE %d flag' % n, html_lines[n - 1])
for n in count_cur:
    check(not any(f in html_lines[n - 1] for f in FLAGS), 'travel114 COUNT %d noflag' % n, html_lines[n - 1])
for n in (6531, 6532, 8223, 14250, 14251, 14263, 14264, 14275, 14276, 14376):
    check(any(f in html_lines[n - 1] for f in FLAGS), 'travel114 FREE untouched %d' % n, html_lines[n - 1])
for n in (15395, 18794, 20995):
    check('openLoc(' in html_lines[n - 1] and not any(f in html_lines[n - 1] for f in FLAGS),
          'travel114 COUNT untouched %d' % n, html_lines[n - 1])
check('function openLoc(id, opts){' in html_lines[new(41491) - 1], 'travel114 DEF', html_lines[new(41491) - 1])
check('openLoc: function(id, opts){ openLoc(id, opts); }' in html_lines[new(28769) - 1],
      'travel114 WRAPPER', html_lines[new(28769) - 1])
print('travel114: FREE %d + COUNT %d + DEF %d + WRAPPER %d' % (len(free_cur), len(count_cur), new(41491), new(28769)))

# ---------- 2. rom176：4 個釘行（其餘 2 釘 6325／14813 喺改動點之前唔郁） ----------
p = ROOT + '/tests/test_rom176_static.py'
src = open(p, encoding='utf-8').read()
pins = {39846: '/* ===== v20a176 ROM176', 40204: 'function rom176ApplyGiftOverrides()',
        41376: 'function addLocTalkGiftActs(add, L, npcId)', 41532: 'rom176TryIntercept(id)'}
if 'line(39846)' in src:
    for old in pins:
        src = src.replace('line(%d)' % old, 'line(%d)' % new(old), 1)
    comment = ("# v20a284 resync：index.html 淨 +58 行；4 個釘行按段重算（39846→39859、40204→40217 各 ＋13，"
               "41376→41434、41532→41590 各 ＋58；6325／14813 喺改動點之前唔郁），內容逐字核實純漂移；"
               "L55647 等名唔郁。\n")
    if 'v20a284 resync' not in src:
        src = comment + src
    open(p, 'w', encoding='utf-8').write(src)
for old, frag in pins.items():
    check(frag in html_lines[new(old) - 1], 'rom176 %d->%d' % (old, new(old)), html_lines[new(old) - 1])
print('rom176: pins %s' % {k: new(k) for k in pins})

# ---------- 3. tang171／tang173：總行數＋openLoc DEF＋guard ----------
for fname in ('test_tang171_static.py', 'test_tang173_static.py'):
    p = ROOT + '/tests/' + fname
    src = open(p, encoding='utf-8').read()
    if '總行數 46243' in src:
        count_lit_old = "src.count('" + BS + "n') == 46243"
        count_lit_new = "src.count('" + BS + "n') == 46301"
        assert count_lit_old in src, fname
        assert 'openLoc DEF 行 41491' in src and 'len(lines) >= 41497' in src and 'lines[41490]' in src
        src = src.replace('總行數 46243（v193', '總行數 46301（v193', 1)
        src = src.replace('＋v283 +76）\', ' + count_lit_old, '＋v283 +76＋v284 +58）\', ' + count_lit_new, 1)
        src = src.replace('openLoc DEF 行 41491', 'openLoc DEF 行 41549', 1)
        src = src.replace('＋v283 +76，travel114 釘行', '＋v283 +76＋v284 +58，travel114 釘行', 1)
        src = src.replace('len(lines) >= 41497', 'len(lines) >= 41555', 1)
        src = src.replace('lines[41490]', 'lines[41548]', 1)
        comment = ("# v20a284 resync：index.html 淨 +58 行（插入點全部喺釘行之前：F／C2 註解＋3／mockAskDefs＋10／"
                   "E＋42／G＋3；總行數 46243→46301、openLoc DEF 41491→41549；鏈尾加 ＋v284 +58；"
                   "標籤＋lines[] guard 一併更新），內容逐字核實純漂移。\n")
        if 'v20a284 resync' not in src:
            src = comment + src
        open(p, 'w', encoding='utf-8').write(src)
    check(len(html_lines) - 1 == 46301, fname + ' total', 'lines=%d' % (len(html_lines) - 1))
    check('function openLoc(id, opts){' in html_lines[41549 - 1], fname + ' DEF', html_lines[41549 - 1])
    print(fname + ': total 46301, DEF 41549')

# ---------- 4. gift185：總行數 ----------
p = ROOT + '/tests/test_gift185_static.py'
src = open(p, encoding='utf-8').read()
if '總行數 46243' in src:
    count_lit_old = "html.count('" + BS + "n') == 46243"
    count_lit_new = "html.count('" + BS + "n') == 46301"
    assert count_lit_old in src
    src = src.replace('總行數 46243（v193', '總行數 46301（v193', 1)
    src = src.replace('＋v283 +76）\', ' + count_lit_old, '＋v283 +76＋v284 +58）\', ' + count_lit_new, 1)
    comment = ("# v20a284 resync：index.html 淨 +58 行（F／C2 註解＋3／mockAskDefs＋10／E＋42／G＋3；"
               "總行數 46243→46301，鏈尾加 ＋v284 +58）。\n")
    if 'v20a284 resync' not in src:
        src = comment + src
    open(p, 'w', encoding='utf-8').write(src)
check(len(html_lines) - 1 == 46301, 'gift185 total', 'lines=%d' % (len(html_lines) - 1))
print('gift185: total 46301')

# ---------- 5. nat92 F2：庫 288→289，錯峰合資格 276→277（289－12 入門） ----------
p = ROOT + '/tests/test_nat92_logic.js'
src = open(p, encoding='utf-8').read()
if 'stagN === 276' in src:
    assert "ok('F2 錯峰合資格 276 張（288－12 入門）', stagN === 276" in src
    src = src.replace("ok('F2 錯峰合資格 276 張（288－12 入門）', stagN === 276",
                      "ok('F2 錯峰合資格 277 張（289－12 入門）', stagN === 277", 1)
    open(p, 'w', encoding='utf-8').write(src)
print('nat92: F2 276->277')

print('MISMATCHES:', bad if bad else 'none')
