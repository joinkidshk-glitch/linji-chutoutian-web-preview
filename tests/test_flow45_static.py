# v20a45 流程確認（A 方案）靜態測試：接線標記／入口區分／紅線／結算公式冇郁。
# 用法：python3 tests/test_flow45_static.py [path-to-index.html]
import os, re, sys

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

# ---- 確認函數本體 ----
ok('confirm fn defined', 'function presentStartScheduleConfirm45(' in html)
cf = seg('function presentStartScheduleConfirm45(', 'function presentRestSleepDayEnd(')
ok('confirm copy: title asks', '開始今日行程？' in cf)
ok('confirm copy: starts date line', '將會開始' in cf and 'fmtDate()' in cf)
ok('confirm copy: instant-settle warning', '即時結算埋今日' in cf)
ok('confirm buttons: start + back to map', '"開始今日行程"' in cf.replace('label:"', '"') or 'label:"開始今日行程"' in cf)
ok('confirm dismiss goes to map', 'onDismiss' in cf)
ok('confirm fn never touches dayIndex', 'dayIndex' not in cf)

# ---- 閘門接線（presentRestSleepDayEnd 內） ----
ps = seg('function presentRestSleepDayEnd(', 'function playRestSleepFx(')
ok('gate fn goScheduleAsk defined in card', 'goScheduleAsk' in ps)
ok('gate wired to start button only', 'indexOf("開始今日")>=0) return Object.assign({}, b, { on: goScheduleAsk })' in ps)
ok('home-settle button stays ungated', 'indexOf("回家結算")>=0) return Object.assign({}, b, { on: goSchedule })' in ps)
ok('gate checks flag', 'opts.confirmStartSchedule' in ps)

# ---- 旗標呼叫點：三處日結卡，冇多冇少 ----
n_flag = len(re.findall(r'confirmStartSchedule:\s*true', html))
ok('flag passed at exactly 3 day-end call sites', n_flag == 3)
eb = seg('function endBrowseDayGoHome(', 'function confirmEarlyRestFromMenu(')
ok('flag at early-rest card (endBrowseDayGoHome)', 'confirmStartSchedule: true' in eb)
rp = seg('function resolvePlannedDay(', 'function autoPushC1IfNeeded(')
ok('flag at planned-rest card (resolvePlannedDay)', 'confirmStartSchedule: true' in rp)
dr = seg('function doRest(', 'function tipGig(')
ok('flag at location-rest card (doRest)', 'confirmStartSchedule: true' in dr)

# ---- 唔加確認嘅路徑保持原狀 ----
pl = seg('function playRestSleepFx(', 'function restSleepFxCheck(')
ok('legacy playRestSleepFx has no flag', 'confirmStartSchedule' not in pl)
am = seg('function afterDayModal(', 'function shootPendingLine38(')
ok('generic afterDayModal untouched by gate', 'confirmStartSchedule' not in am and 'goScheduleAsk' not in am)
ok('map proactive start untouched', 'function startTodayScheduleFromMap(' in html and 'confirmStartSchedule' not in seg('function startTodayScheduleFromMap(', 'function endBrowseDayGoHome('))

# ---- 紅線＋公式 ----
ok('redline SAVE key', 'starVolunteer_map_v19w' in html)
ok('redline softRev', 'softRev=s111' in html or 'softRev = "s111"' in html or '"s111"' in html)
ok('redline version tag', '"v20a10"' in html)
# v20a58：休息唔再加體能係刻意修復（用戶實玩報告），公式鎖同步更新——鎖嘅係「唔好靜靜漂移」，唔係鎖死舊 bug
ok('early-rest formula unchanged', 'apply({stress:-(4+R(0,4))})' in html and 'stamina:6+R(0,4)' not in html)
ok('planned-rest formula unchanged', 'apply({stress:-(18+R(0,8))})' in html and 'stamina:20+R(0,8)' not in html)
ok('advanceDay single increment unchanged', 'S.dayIndex += 1' in html)

print('')
if fails:
    print('FAILED: ' + ' | '.join(fails))
    sys.exit(1)
print('FLOW45 STATIC: ALL PASS')
