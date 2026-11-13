# v20a189 日結板三粒掣・靜態測試：返回地圖真返地圖／加速降級做細連結／版面唔裁字。
# 用法：python3 tests/test_dayend189_static.py [path-to-index.html]
import os, sys

path = sys.argv[1] if len(sys.argv) > 1 else 'index.html'
html = open(path, encoding='utf-8').read()
fails = []
def ok(name, cond):
    print(('PASS ' if cond else 'FAIL ') + name)
    if not cond:
        fails.append(name)

def seg(start, end):
    # 搵唔到起點就返空字串：檢查項會乾淨 FAIL，唔會 crash（反證嗰陣要呢個行為）
    if start not in html:
        return ''
    i = html.index(start)
    try:
        j = html.index(end, i) if end else len(html)
    except ValueError:
        j = min(len(html), i + 30000)
    return html[i:j]

def idx(hay, needle):
    return hay.index(needle) if needle in hay else -1

fn = seg('function dayEndContinueButtons(', 'function flushWeekAccelSummary(')

# ---- 1：soft 分支「返回地圖」真係返地圖 ----
ok('soft map button goes to goToMapForBrowse',
   'label:"返回地圖", role:"p", on:(()=>{ try{ goToMapForBrowse(); }catch(_e){} })}' in fn)
ok('soft map button does NOT run goRunSchedule',
   fn.count('label:"返回地圖"') == 2
   and 'label:"返回地圖", role:"p", on: (typeof goRunSchedule' in fn  # 只剩 nextIsMap 嗰粒
   and 'label:"返回地圖", role:"p", on:goRunSchedule' not in fn)
ok('soft schedule button still runs goRunSchedule',
   'label:"開始今日行程", role:"g", on:goRunSchedule' in fn)

# ---- 2：forced／map 分支唔郁 ----
ok('forced branch unchanged (only 開始今日行程 on goRunSchedule)',
   'btns.push({label:"開始今日行程", role:"p", on:goRunSchedule});' in fn)
ok('map branch unchanged (v20a4 comment + 返回地圖 on goRunSchedule)',
   'v20a4' in fn and 'label:"返回地圖", role:"p", on: (typeof goRunSchedule==="function") ? goRunSchedule' in fn)
ok('ended branch unchanged (回家結算 on goRunSchedule)',
   'btns.push({label:"回家結算", role:"p", on:goRunSchedule});' in fn)

# ---- 3：加速降級做細連結 ----
ok('no big accel button any more', 'label:"加速本週剩餘"' not in fn)
ok('accel is a link entry (role link, label names accel)',
   'role:"link"' in fn and '想跳過本週剩餘日子？加速' in fn)
ok('accel link still wires confirmWeekAccel + goRunSchedule',
   'confirmWeekAccel(()=>{ if(typeof goRunSchedule==="function") goRunSchedule(); })' in fn)
ok('accel link pushed after main buttons (renders below the row)',
   idx(fn, '想跳過本週剩餘日子？加速') > 0
   and idx(fn, '想跳過本週剩餘日子？加速') > idx(fn, 'label:"開始今日行程", role:"g", on:goRunSchedule'))

# ---- 4：modal() 識得 render link ----
modal_seg = seg('function modal(', 'function closeModal()')
ok('modal renders role link as day-end-accel-link',
   'role==="link"' in modal_seg and 'day-end-accel-link' in modal_seg)

# ---- 5：細連結 CSS（夠顯眼撳得到）----
_css_i = html.index('#modal-btns button.day-end-accel-link{') if '#modal-btns button.day-end-accel-link{' in html else -1
css_seg = html[_css_i:html.index('}', _css_i)] if _css_i >= 0 else ''
ok('accel link css exists', '#modal-btns button.day-end-accel-link{' in html)
ok('accel link is full-width row below buttons', 'flex: 1 1 100%;' in css_seg)
ok('accel link tappable (44px min-height)', 'min-height: 44px;' in css_seg)
ok('accel link readable (underlined, .85rem)', 'text-decoration: underline;' in css_seg and 'font-size: .85rem;' in css_seg)

# ---- 6：版面——hint 行拎走＋矮屏放寬 ----
ok('week-accel-hint no longer emitted in day-end bodies (css rule only)',
   html.count('week-accel-hint') == 1)
ok('day-end modal gets day-res class (wrap path, for short-screen relief)',
   seg('function resolvePlannedDay(', 'function autoPushC1IfNeeded(').count('classList.add("day-res")') >= 3)
# v20a197 B4：92dvh 矮屏放寬唔再排除 tut-on——舊版 :not(.tut-on) 令成條規則喺
# 教學態下完全唔生效（兩板日結都係 tut-on，實駕量度掣 y 差 70px 同 review 逐 px
# 相同）；宜家 day-res modal 一律固定高度＋底錨，矮屏放寬跟同一條。
ok('short-screen relief scoped to day-res modals (92dvh)',
   '#mask.day-res .modal{' in html and '#mask.day-res:not(.tut-on) .modal{' not in html
   and 'min(92dvh,92svh,720px)' in html)

# ---- 7：confirmWeekAccel 確認流程唔郁 ----
ok('confirmWeekAccel still exists with 取消／確認加速',
   'function confirmWeekAccel(' in html and 'label:"取消"' in html and 'label:"確認加速"' in html)

# ---- 紅線 ----
ok('redline SAVE key untouched', 'starVolunteer_map_v19w' in html)
ok('redline softRev s107 present', 's107' in html)
ok('redline ?v= v20a10 present', '?v=20a10' in html)
ok('notes file exists', os.path.exists(os.path.join(os.path.dirname(os.path.abspath(path)), 'NOTES_V20A189_DAYEND_BUTTONS.md')))

print('')
if fails:
    print('FAILED: ' + ' | '.join(fails))
    sys.exit(1)
print('DAYEND189 STATIC: ALL PASS')
