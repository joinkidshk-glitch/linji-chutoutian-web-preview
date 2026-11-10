# v20a48 打磨靜態測試：斜度／掣位／補償／傳聞對比標記＋作用域＋紅線。
# 用法：python3 tests/test_polish48_static.py [path-to-index.html]
import re, sys

path = sys.argv[1] if len(sys.argv) > 1 else 'index.html'
html = open(path, encoding='utf-8').read()
fails = []
def ok(name, cond):
    print(('PASS ' if cond else 'FAIL ') + name)
    if not cond:
        fails.append(name)

def seg(start, end=None):
    i = html.index(start)
    try:
        j = html.index(end, i) if end else len(html)
    except ValueError:
        j = min(len(html), i + 30000)
    return html[i:j]

# ---- (1) 斜度 ----
paper = seg('#mask.paper-on .paper-sheet{', '/* --- (3)')
ok('paper tilt -2.2deg', 'rotate(-2.2deg)' in paper)
ok('old -1.1deg paper tilt gone', 'rotate(-1.1deg)' not in paper)
clip_css = seg('#app #clippings-list .clip-card:nth-child(odd)')
ok('clip odd tilt -1.1deg', 'rotate(-1.1deg)' in clip_css)
ok('clip even tilt 1deg', 'rotate(1deg)' in seg('#app #clippings-list .clip-card:nth-child(even)', '#app .clip-card::before'))
v48 = seg('/* === v20a48 打磨', '/* === v20a48 打磨完 === */')
ok('inner sweep padding compensation', '#mask.paper-on #modal-inner' in v48 and 'padding:10px 16px 14px' in v48)
ok('clip card side margins', '#app #clippings-list .clip-card' in v48 and 'margin-left:5px' in v48)

# ---- (2) 收紙掣黐紙（作用域只限 paper-on） ----
_bi = v48.index('#mask.paper-on #modal-btns{') if '#mask.paper-on #modal-btns{' in v48 else -1
btns = v48[_bi:v48.index('/* (1b)', _bi)] if _bi >= 0 else ''
ok('btns tilt with paper', 'rotate(-2.2deg)' in btns)
ok('btns pulled up overlapping', 'margin-top:-7px !important' in btns)
ok('btns above paper stacking', 'z-index:7' in btns)
# 其他 modal 掣欄唔受影響：全域 #modal-btns base 規則 margin-top 仍係 +8px !important
base_btns = seg('\n#modal-btns{\n', '#modal-btns button')
ok('base btns margin untouched', 'margin-top: 8px !important' in base_btns)
ok('btns tilt scoped to paper-on only', html.count('rotate(-2.2deg)') == 2)

# ---- (3) 眉題去重接線 ----
fn = seg('function renderMorningPaperHtml(', 'function pushNewspaperRumor(')
ok('dedupe: kickNorm computed', 'kickNorm' in fn and 'replace(/\\s+/g, "")' in fn)
ok('dedupe: prefix checks', 'headRaw.startsWith(kickTrim)' in fn and 'headNorm.startsWith(kickNorm)' in fn)
ok('dedupe: clip gated by kickDup', '!kickDup' in fn)
ok('presentDueMorningPaper untouched (paperSheet opt kept)', 'paperSheet: true' in html)

# ---- (4) 傳聞頁說明對比（作用域只限傳聞頁） ----
ok('rumor intro solid bg fix', '#home-pane-rumor .pane-intro' in v48 and 'background:#fff8e8' in v48 and 'color:#3a2a18' in v48)
# v20a76 CONTRAST76 supersede：v48 當時明文留低人情債頁唔郁；v76 全手帳普查
# 量到該引言 1.24:1 讀唔到，用戶拍板一次修清——已加深底亮字規則，斷言跟住改。
ok('debt pane intro restyled by v76 CONTRAST76', '#home-pane-debt .pane-intro{ color:#e6d7ae; }' in html)

# ---- 紅線 ----
ok('SAVE key intact', html.count('starVolunteer_map_v19w') == 10)
ok('product ?v= intact', html.count('"v20a10"') == 7)
ok('softRev marker intact', 's107' in html)
# CSS 大括號平衡（主 style 段）
style = html.split('<style', 1)[1].split('</style>', 1)[0]
ok('style braces balanced', style.count('{') == style.count('}'))

print('FAILURES: ' + ' | '.join(fails) if fails else 'ALL PASS')
sys.exit(1 if fails else 0)
