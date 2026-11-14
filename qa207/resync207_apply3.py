# v20a207 resync：按 qa207/resync207.py 對位（72 錨點零 mismatch，純漂移）更新 11 檔測試。
# 另 ui142／ux68（C5 刻意 60%→51%）、buttons197（B3 刻意 top:8→bottom:8）係意圖改動，同步更新期望值。
import io, re, sys

W = '/home/hatch/workspace/linji-work207/tests/'
def load(n):
    return io.open(W + n, encoding='utf-8').read()
def save(n, s):
    io.open(W + n, 'w', encoding='utf-8').write(s)
def rep(s, old, new, cnt=1, fname='?'):
    n = s.count(old)
    assert n == cnt, f'{fname}: {old!r} 出現 {n} 次，預期 {cnt} 次'
    return s.replace(old, new)

HDR = '# v20a207 resync (part 2).\n'
# ---- travel114：COUNT/FREE/DEF/WRAPPER（只改 set 內數字行＋兩個常數） ----
s = load('test_travel114_static.py')
count_map = {32296: 32313, 35796: 35813, 37947: 37964, 39117: 39134, 39549: 39566,
             39552: 39569, 39583: 39600, 44567: 44586, 59985: 60019, 60163: 60197,
             60309: 60343, 60330: 60364}
free_map = {24748: 24765, 30963: 30980, 30964: 30981, 30976: 30993, 30977: 30994,
            30988: 31005, 30989: 31006, 31092: 31109, 41510: 41529, 44224: 44243,
            44247: 44266, 54157: 54191, 54276: 54310, 54326: 54360, 54549: 54583,
            54588: 54622, 54594: 54628, 54661: 54695, 54663: 54697, 54666: 54700,
            54693: 54727, 55804: 55838, 56178: 56212, 56200: 56234, 56351: 56385,
            57988: 58022, 59753: 59787, 59871: 59905, 59872: 59906, 59907: 59941,
            59908: 59942, 59933: 59967, 60780: 60814}
def remap_set(text, start_marker, mapping, fname):
    a = text.index(start_marker)
    m = re.search(r'(?m)^}$', text[a:])
    assert m, fname + ': set 結尾搵唔到'
    b = a + m.start()
    seg = text[a:b]
    for old, new in mapping.items():
        pat = re.compile(r'(?m)^(\s+)%d,(.*)$' % old)
        seg2, n = pat.subn(r'\g<1>%d,\g<2>' % new, seg)
        assert n == 1, f'{fname}: set 內 {old} 出現 {n} 次'
        seg = seg2
    return text[:a] + seg + text[b:]
s = remap_set(s, 'COUNT_LINES = {', count_map, 'travel114-COUNT')
s = remap_set(s, 'FREE_LINES = {', free_map, 'travel114-FREE')
s = rep(s, 'DEF_LINE = 55904', 'DEF_LINE = 55938', 1, 'travel114')
s = rep(s, 'WRAPPER_LINE = 45136', 'WRAPPER_LINE = 45155', 1, 'travel114')
s = HDR + s
save('test_travel114_static.py', s)

# ---- tang171 / tang173 / gift185：總行數 61432→61466、DEF 55904→55938 ----
for fname in ['test_tang171_static.py', 'test_tang173_static.py']:
    s = load(fname)
    s = rep(s, '總行數 61432（v193 61167＋v203 +233＋v204 +32）',
            '總行數 61466（v193 61167＋v203 +233＋v204 +32＋v207 +34）', 1, fname)
    s = rep(s, "src.count('\\n') == 61432", "src.count('\\n') == 61466", 1, fname)
    s = rep(s, 'openLoc DEF 行 55904（v193 55639＋v203 +233＋v204 +32，travel114 釘行）',
            'openLoc DEF 行 55938（v193 55639＋v203 +233＋v204 +32＋v207 +34，travel114 釘行）', 1, fname)
    s = rep(s, 'len(lines) >= 55904', 'len(lines) >= 55938', 1, fname)
    s = rep(s, 'lines[55903]', 'lines[55937]', 1, fname)
    s = HDR + s
    save(fname, s)
s = load('test_tang173_static.py')
s = rep(s, 'len(lines) >= 4942', 'len(lines) >= 4954', 1, 'tang173')
s = rep(s, 'lines[4941]', 'lines[4953]', 3, 'tang173')
save('test_tang173_static.py', s)

s = load('test_gift185_static.py')
s = rep(s, '總行數 61432（v193 61167＋v203 +233＋v204 +32）',
        '總行數 61466（v193 61167＋v203 +233＋v204 +32＋v207 +34）', 1, 'gift185')
s = rep(s, "html.count('\\n') == 61432", "html.count('\\n') == 61466", 1, 'gift185')
s = HDR + s
save('test_gift185_static.py', s)

# ---- ui142：中環廣告由 UNCHANGED 移去錨檢查（C5 刻意 60%→51%） ----
s = load('test_ui142_static.py')
s = rep(s, "    '中環廣告': 'left:60%;top:calc(57% + 30px)',\n", '', 1, 'ui142')
s = rep(s, "# --- B1：4 張錨新值；其餘 11 張唔郁；LOCS 熱區座標唔郁 ---",
        "# --- B1：5 張錨新值；其餘 10 張唔郁；LOCS 熱區座標唔郁（v20a207 C5：中環廣告 60%→51%，避開藍塔） ---", 1, 'ui142')
s = rep(s, "ok('B1 金龍茶餐廳錨＝16%／16% -56px', mn('金龍茶餐廳') == 'left:16%;top:calc(16% - 56px)')",
        "ok('B1 金龍茶餐廳錨＝16%／16% -56px', mn('金龍茶餐廳') == 'left:16%;top:calc(16% - 56px)')\n"
        "ok('B1 中環廣告錨＝51%／57% +30px（v20a207 C5：60%→51%，避開藍塔，「廣」字唔再俾遮）', mn('中環廣告') == 'left:51%;top:calc(57% + 30px)')", 1, 'ui142')
s = HDR + s
save('test_ui142_static.py', s)

# ---- ux68：spec 中環廣告 60→51 ----
s = load('test_ux68_static.py')
s = rep(s, "'維港電影': ('80', '18', '+', '38'), '中環廣告': ('60', '57', '+', '30'),",
        "'維港電影': ('80', '18', '+', '38'), '中環廣告': ('51', '57', '+', '30'),  # v20a207 C5：60%→51%，避開藍塔", 1, 'ux68')
s = HDR + s
save('test_ux68_static.py', s)

# ---- buttons197：B3 刻意 top:8→bottom:8；B3 label 480×360→480×432（B2） ----
s = load('test_buttons197_static.py')
s = rep(s, "'B3：跳過掣 CSS 唔郁（absolute top:8 right:8，宜家相對 canvaswrap）',",
        "'B3：跳過掣 CSS 搬去底邊（v20a207 B3：absolute bottom:8 right:8，唔再壓框角「角度」pill）',", 1, 'buttons197')
s = rep(s, "'.awd62-skip{position:absolute;top:8px;right:8px' in src",
        "'.awd62-skip{position:absolute;bottom:8px;right:8px' in src", 1, 'buttons197')
s = rep(s, '（480×360 固定比例，唔跟 beat 高度走）', '（480×432 固定比例，v20a207 B2，唔跟 beat 高度走）', 1, 'buttons197')
s = HDR + s
save('test_buttons197_static.py', s)

print('resync edits applied OK')
