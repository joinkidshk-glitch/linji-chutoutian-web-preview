# v20a38 收尾修復包・靜態測試：接線標記／紅線／NOTES。
# 用法：python3 tests/test_wrap38_static.py [path-to-index.html]
import os, sys

path = sys.argv[1] if len(sys.argv) > 1 else 'index.html'
html = open(path, encoding='utf-8').read()
fails = []
def ok(name, cond):
    print(('PASS ' if cond else 'FAIL ') + name)
    if not cond:
        fails.append(name)

def seg(start, end):
    i = html.index(start)
    try:
        j = html.index(end, i) if end else len(html)
    except ValueError:
        j = min(len(html), i + 30000)
    return html[i:j]

# ---- 修復 1：跨次記憶 ----
ok('fix1 recent helper defined', 'function psrRecent38(' in html)
ok('fix1 memory stored on save object S.psrRecent38', 'S.psrRecent38' in html)
pick_seg = seg('function psrPickNoRepeat35(', 'function psrSceneForShoot38(')
ok('fix1 pick reads memory + relaxes (no deadlock loop)', 'psrRecent38(channel)' in pick_seg and 'exclN--' in pick_seg)
ok('fix1 memory capped at 3', 'recent.length = 3' in pick_seg or 'recent.length>3' in pick_seg)
bps_seg = seg('function buildPostShootRewardPack(', 'function applyPostShootRewardDual')
ok('fix1 build uses chosen-first draws (extraChosen)', 'extraChosen' in bps_seg and '入選先抽' in bps_seg)

# ---- 修復 2：場景適配 ----
ok('fix2 scene tag table present', 'const PSR_SCENE_TAGS38' in html)
for tid, tags in [('psr35_press_tv_02', '"night", "studio"'), ('psr35_press_film_02', '"outdoor", "day"'), ('psr35_news_film_02', '"outdoor"')]:
    ok('fix2 tag ' + tid, tid in html and tags in html)
ok('fix2 scene derivation + filter defined', 'function psrSceneForShoot38(' in html and 'function psrSceneFilter38(' in html)
ok('fix2 pick template accepts scene38', 'function postShootPickTemplate(channel, gigType, scene38)' in html)
ok('fix2 build passes scene38 to all channels',
   'postShootPickTemplate("press", gigType, scene38)' in bps_seg
   and 'postShootPickTemplate("news", gigType, scene38)' in bps_seg
   and 'postShootPickTemplate("streetFans", gigType, scene38)' in bps_seg
   and 'postShootPickTemplate("metrics", gigType, scene38)' in bps_seg)

# ---- 修復 3：手帳拍攝中卡待入帳標示 ----
ok('fix3 pending line helper defined', 'function shootPendingLine38(' in html)
wi_seg = seg('function workItems(){', 'function dayPlanLocked(')
ok('fix3 workItems card carries pending line', 'shootPendingLine38(sh)' in wi_seg and '(pend?' in wi_seg)
ok('fix3 pending line format (約酬/聲望/人氣)', '殺青後入帳：' in html and '約酬 $' in seg('function shootPendingLine38(', 'function workItems(){'))

# ---- 紅線 ----
ok('redline SAVE key untouched', 'starVolunteer_map_v19w' in html)
ok('redline softRev s111 present', 's111' in html)
ok('notes file exists', os.path.exists(os.path.join(os.path.dirname(os.path.abspath(path)), 'NOTES_V20A38_WRAP_FIXES.md')))

print('')
if fails:
    print('FAILED: ' + ' | '.join(fails))
    sys.exit(1)
print('WRAP38 STATIC: ALL PASS')
