# v20a51 入何生事務所深色長方形閃爍：根因＝.push-door 推門動畫三處缺陷。
# 靜態測試守住三項修復＋紅線。用 法：python3 tests/test_flash51_static.py [path-to-index.html]
import sys

path = sys.argv[1] if len(sys.argv) > 1 else 'index.html'
html = open(path, encoding='utf-8').read()
fails = []
def ok(name, cond):
    print(('PASS ' if cond else 'FAIL ') + name)
    if not cond:
        fails.append(name)

def seg(start, end=None, span=30000):
    try:
        i = html.index(start)
    except ValueError:
        return ''
    try:
        j = html.index(end, i) if end else len(html)
    except ValueError:
        j = min(len(html), i + span)
    return html[i:j]

# ---- 根因元素本體（修復前後都應存在） ----
door = seg('.push-door{', '}')
ok('push-door base rule present', bool(door))
ok('push-door slab gradient (the reported dark rectangle)',
   'linear-gradient(90deg,#2a2118,#6b4e2e 55%,#1a1410)' in html)
ok('pushDoor keyframes 700ms-class animation present', '@keyframes pushDoor' in html
   and 'animation:pushDoor .7s ease forwards' in html)
ok('playPushDoor called only for agency_ho',
   html.count('playPushDoor()') >= 1 and 'if(id==="agency_ho") playPushDoor();' in html)

# ---- 修復 1：z-index 低過地點 sheet（.sheet z-20），唔再蓋住場景相 ----
ok('push-door z-index lowered below sheet', 'z-index:15; pointer-events:none' in door)
ok('push-door no longer z-index 45', 'z-index:45' not in door)

# ---- 修復 2：門鈴改黐左側，全程留喺畫面 ----
bell = seg('.push-door-bell{', '}')
ok('bell repositioned to left side of slab', 'left:6%' in bell)
ok('bell no longer right:8% declaration', 'right:8%;' not in bell and 'position:absolute; left:6%' in bell)

# ---- 修復 3：560ms 只藏鈴；700ms 先落 done（等動畫自己淡出完） ----
fn = seg('function playPushDoor(){', 'function setHomeTab')
ok('playPushDoor present', bool(fn))
bell_timer = seg('playPushDoor._t=setTimeout', '}, 560);') if 'playPushDoor._t=setTimeout' in fn else ''
ok('560ms timer only hides bell (no done/opacity cut)',
   bool(bell_timer) and 'bell.textContent = ""' in bell_timer
   and 'classList.add("done")' not in bell_timer and 'door.style.opacity' not in bell_timer)
done_timer = seg('playPushDoor._tDone=setTimeout', '}, 700);') if 'playPushDoor._tDone=setTimeout' in fn else ''
ok('700ms timer applies done after animation fade completes',
   bool(done_timer) and 'classList.add("done")' in done_timer)
ok('new timer handle cleared on replay', 'clearTimeout(playPushDoor._tDone);' in fn)
ok('node removal timer kept at 820ms', '}, 820);' in fn)

# ---- 紅線 ----
ok('SAVE key untouched', 'starVolunteer_map_v19w' in html)
ok('softRev marker present', 's108' in html)
ok('product version marker present', 'v20a10' in html)

print('---')
print('FAILURES:', len(fails))
sys.exit(1 if fails else 0)
