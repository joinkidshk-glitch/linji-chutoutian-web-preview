# v404 意圖更新：用戶 2026-11-25 拍板刪「開始今日行程？」確認閘——presentStartScheduleConfirm45＋goScheduleAsk＋confirmStartSchedule 旗標全刪，掣名改講明後果（休息並過日／執行今日行程／開始拍攝／開始工作）；斷言同步改做「已刪＋新掣名在位」。
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

# ---- 確認閘已刪（v404 用戶拍板：已安排行程撳掣即執行，掣名講明後果） ----
ok('confirm fn deleted (v404)', 'function presentStartScheduleConfirm45(' not in html)
ok('confirm copy gone (v404)', 'label:"開始並結算當日"' not in html and 'label:"返回休息卡"' not in html and '<h3>開始今日行程？</h3>' not in html)
ok('consequence labels present (v404)', '休息並過日' in html and '執行今日行程' in html and '開始拍攝' in html and '開始工作' in html)

# ---- 閘門接線已拆（v404）：執行掣直行 goSchedule ----
ps = seg('function presentRestSleepDayEnd(', 'function playRestSleepFx(')
ok('gate fn goScheduleAsk deleted (v404)', 'goScheduleAsk' not in ps)
ok('execute buttons wired straight to goSchedule (v404)', 'on: goSchedule' in ps)
ok('gate flag check deleted (v404)', 'opts.confirmStartSchedule' not in ps)

# ---- 旗標呼叫點已全刪（v404） ----
n_flag = len(re.findall(r'confirmStartSchedule:\s*true', html))
ok('flag passed nowhere (v404)', n_flag == 0)

# ---- 唔加確認嘅路徑保持原狀 ----
pl = seg('function playRestSleepFx(', 'function restSleepFxCheck(')
ok('legacy playRestSleepFx has no flag', 'confirmStartSchedule' not in pl)
am = seg('function afterDayModal(', 'function shootPendingLine38(')
ok('generic afterDayModal untouched by gate', 'confirmStartSchedule' not in am and 'goScheduleAsk' not in am)
ok('map proactive start untouched', 'function startTodayScheduleFromMap(' in html and 'confirmStartSchedule' not in seg('function startTodayScheduleFromMap(', 'function endBrowseDayGoHome('))

# ---- 紅線＋公式 ----
ok('redline SAVE key', 'starVolunteer_map_v19w' in html)
ok('redline softRev', 'softRev=s107' in html or 'softRev = "s107"' in html or '"s107"' in html)
ok('redline version tag', '"v20a10"' in html)
# v20a58：休息唔再加體能係刻意修復（用戶實玩報告），公式鎖同步更新——鎖嘅係「唔好靜靜漂移」，唔係鎖死舊 bug
ok('early-rest formula unchanged', 'apply({stress:-(4+R(0,4))})' in html and 'stamina:6+R(0,4)' not in html)
ok('planned-rest = stress clear (v20a65 FIX65-1, user rule 2026-11-10: full-day rest zeroes stress)', 'apply({stress:-S.stress})' in html and 'stamina:20+R(0,8)' not in html and 'apply({stress:-(18+R(0,8))})' not in html)
ok('advanceDay single increment unchanged', 'S.dayIndex += 1' in html)

print('')
if fails:
    print('FAILED: ' + ' | '.join(fails))
    sys.exit(1)
print('FLOW45 STATIC: ALL PASS')
