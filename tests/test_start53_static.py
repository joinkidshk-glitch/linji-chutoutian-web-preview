# v20a53 開始畫面打磨＋揀槽詳情對比＋片場圖 v3 靜態測試。
# 用法：python3 tests/test_start53_static.py [path-to-index.html]
import base64, io, sys
from PIL import Image

path = sys.argv[1] if len(sys.argv) > 1 else 'index.html'
html = open(path, encoding='utf-8').read()
fails = []
def ok(name, cond):
    print(('PASS ' if cond else 'FAIL ') + name)
    if not cond:
        fails.append(name)

def seg(start, end=None, src=None):
    src = html if src is None else src
    try:
        i = src.index(start)
    except ValueError:
        return ''
    try:
        j = src.index(end, i) if end else len(src)
    except ValueError:
        j = len(src)
    return src[i:j]

v53 = seg('/* === v20a53 開始畫面打磨', '/* === v20a53 完 === */')
ok('v53 segment present', bool(v53))

# ---- 1. 阿偉企立：v53 覆寫值（紙邊裁口 圖高 ~87% → ~94%） ----
stand = seg('#app #v-start .start52 .start-standee{', '}', v53)
ok('standee override inside v53 segment', bool(stand))
ok('standee height raised to min(52%,430px)', 'height:min(52%,430px)' in stand)
ok('standee bottom lowered to 170px', 'bottom:170px' in stand)
old_stand = seg('#app #v-start .start52 .start-standee{\n  position:absolute;', '}')
ok('v52 standee rule still present (bottom:148px / 44%)', 'bottom:148px' in old_stand and 'min(44%,372px)' in old_stand)

# ---- 2. 簡介句托底 ----
intro = seg('#app #v-start .start52 .start-intro{', '}', v53)
ok('intro override inside v53 segment', bool(intro))
ok('intro has soft radial veil (not a hard band)', 'radial-gradient(' in intro and 'rgba(24,12,2,.55)' in intro and 'rgba(24,12,2,0) 78%' in intro)
ok('intro text-shadow strengthened', '0 1px 2px rgba(0,0,0,.92)' in intro)
ok('intro layout compensated (margin 2 + padding 10)', 'margin:2px auto 0' in intro and 'padding:10px 16px' in intro and 'max-width:332px' in intro)
scrim = seg('#app #v-start .start52 .start-scrim{', '}', v53)
ok('scrim mid stops raised in v53 segment', 'rgba(22,12,3,.30) 24%' in scrim and 'rgba(22,12,3,.17) 34%' in scrim)
ok('intro copy intact', '港產新人<strong>陳偉翔（阿偉）</strong>，自己跑通告——臨記埋位，一步一步上。' in html)

# ---- 3. 揀槽詳情對比 ----
meta = seg('.slot-list .slot-row .slot-meta{', '}', v53)
ok('slot-meta scoped fix inside v53 segment', bool(meta))
ok('slot-meta light readable color', 'color:#dccba6' in meta)
ok('slot-meta fix appears exactly once', html.count('.slot-list .slot-row .slot-meta') == 1)
base_meta = seg('.slot-row .slot-meta{', '}')
ok('base slot-meta rule untouched (var(--muted))', 'color:var(--muted)' in base_meta)
ok('base slot-row bg untouched (var(--panel2))', 'background:var(--panel2)' in seg('.slot-row{', '}'))
ok('slot modal markup intact', 'class="slot-meta"' in html and '幕前聲望' in html)

# ---- 推門修復（v20a51）原封保留 ----
door = seg('.push-door{', '}')
ok('push-door z-index still 15', 'z-index:15' in door)
ok('push-door bell still left:6%', 'left:6%' in seg('.push-door-bell{', '}'))

# ---- 片場圖換 v3：內嵌規格（800 闊 JPEG）＋唔係原圖直塞 ----
i = html.index('const UI40_SCENE')
m = None
import re
mm = re.search(r'studio:"data:image/jpeg;base64,([^"]+)"', html[i:i + 2500000])
ok('studio embed is jpeg data uri', bool(mm))
if mm:
    raw = base64.b64decode(mm.group(1))
    im = Image.open(io.BytesIO(raw))
    ok('studio embed is 800x1060', im.size == (800, 1060))
    ok('studio embed recompressed (<200KB, not original webp)', len(raw) < 200000)
    ok('studio embed differs from v2-era size 140659', len(raw) != 140659)

# ---- 開始畫面功能紅線 ----
ok('btn ids intact', all(x in html for x in ('id="btn-new"', 'id="btn-cont"', 'id="btn-load"', 'id="start-soft-tip"')))
ok('paintTitleSaveBtns intact', 'paintTitleSaveBtns' in html)

# ---- 紅線 ----
ok('SAVE key intact', html.count('starVolunteer_map_v19w') == 10)
ok('product ?v= intact', html.count('"v20a10"') == 7)
ok('softRev marker intact', 's110' in html)
style = html.split('<style', 1)[1].split('</style>', 1)[0]
ok('style braces balanced', style.count('{') == style.count('}'))

print('FAILURES: ' + ' | '.join(fails) if fails else 'ALL PASS')
sys.exit(1 if fails else 0)
