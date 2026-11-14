# v20a207 resync part 4：tang173 尾段＋gift185＋ui142＋ux68＋buttons197（其餘 6 檔已喺 apply/apply2/apply3 完成）。
import io

W = '/home/hatch/workspace/linji-work207/tests/'
def load(n):
    return io.open(W + n, encoding='utf-8').read()
def save(n, s):
    io.open(W + n, 'w', encoding='utf-8').write(s)
def rep(s, old, new, cnt=1, fname='?'):
    n = s.count(old)
    assert n == cnt, f'{fname}: {old!r} 出現 {n} 次，預期 {cnt} 次'
    return s.replace(old, new)

HDR = '# v20a207 resync：index.html 淨 +34 行（見 qa207/resync207.py，73 錨點對位零 mismatch，純漂移）。\n'

s = load('test_tang173_static.py')
s = rep(s, 'len(lines) >= 4942', 'len(lines) >= 4954', 1, 'tang173')
s = rep(s, 'lines[4941]', 'lines[4953]', 8, 'tang173')
save('test_tang173_static.py', s)

s = load('test_gift185_static.py')
s = rep(s, '總行數 61432（v193 61167＋v203 +233＋v204 +32）',
        '總行數 61466（v193 61167＋v203 +233＋v204 +32＋v207 +34）', 1, 'gift185')
s = rep(s, "html.count('\\n') == 61432", "html.count('\\n') == 61466", 1, 'gift185')
s = HDR + s
save('test_gift185_static.py', s)

s = load('test_ui142_static.py')
s = rep(s, "    '中環廣告': 'left:60%;top:calc(57% + 30px)',\n", '', 1, 'ui142')
s = rep(s, "# --- B1：4 張錨新值；其餘 11 張唔郁；LOCS 熱區座標唔郁 ---",
        "# --- B1：5 張錨新值；其餘 10 張唔郁；LOCS 熱區座標唔郁（v20a207 C5：中環廣告 60%→51%，避開藍塔） ---", 1, 'ui142')
s = rep(s, "ok('B1 金龍茶餐廳錨＝16%／16% -56px', mn('金龍茶餐廳') == 'left:16%;top:calc(16% - 56px)')",
        "ok('B1 金龍茶餐廳錨＝16%／16% -56px', mn('金龍茶餐廳') == 'left:16%;top:calc(16% - 56px)')\n"
        "ok('B1 中環廣告錨＝51%／57% +30px（v20a207 C5：60%→51%，避開藍塔，「廣」字唔再俾遮）', mn('中環廣告') == 'left:51%;top:calc(57% + 30px)')", 1, 'ui142')
s = HDR + s
save('test_ui142_static.py', s)

s = load('test_ux68_static.py')
s = rep(s, "'維港電影': ('80', '18', '+', '38'), '中環廣告': ('60', '57', '+', '30'),",
        "'維港電影': ('80', '18', '+', '38'), '中環廣告': ('51', '57', '+', '30'),  # v20a207 C5：60%→51%，避開藍塔", 1, 'ux68')
s = HDR + s
save('test_ux68_static.py', s)

s = load('test_buttons197_static.py')
s = rep(s, "'B3：跳過掣 CSS 唔郁（absolute top:8 right:8，宜家相對 canvaswrap）',",
        "'B3：跳過掣 CSS 搬去底邊（v20a207 B3：absolute bottom:8 right:8，唔再壓框角「角度」pill）',", 1, 'buttons197')
s = rep(s, "'.awd62-skip{position:absolute;top:8px;right:8px' in src",
        "'.awd62-skip{position:absolute;bottom:8px;right:8px' in src", 1, 'buttons197')
s = rep(s, '（480×360 固定比例，唔跟 beat 高度走）', '（480×432 固定比例，v20a207 B2，唔跟 beat 高度走）', 1, 'buttons197')
s = HDR + s
save('test_buttons197_static.py', s)

print('resync part 4 applied OK')
