# -*- coding: utf-8 -*-
# v20a144 ENC144 靜態測試：紅星巧遇頻率收緊（用戶 2026-11-12 拍板：每日上限 2→1＋新增每週硬上限 2）——
# 一、常數：DAILY_CAP=1、WEEKLY_CAP=2
# 二、S.starWeek 計數器 lazy-init（enc79EnsureStars，跟 S.starFavWeek 先例）
# 三、檢查＋入帳位置：enc79TryIntercept 入面，每週檢查喺每日檢查隔籬、每週遞增喺 sd.triggered 遞增隔籬
# 四、週定義：用 weekNumNow()（星期一界），唔發明第二套週
# 五、不變項：冷卻 3 日、出沒率 base 0.5、級數上限 [30,55,80,100]、每週好感軟頂 10
# 六、紅線：SAVE key／softRev／?v= 不變
# 反證：喺 pristine main（v20a141）index 上行會 FAIL（冇 WEEKLY_CAP／starWeek）。
# 用法：python3 tests/test_enc144_static.py [path-to-index.html]
import re
import sys
from pathlib import Path
p = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent.parent / 'index.html'
src = p.read_text(encoding='utf-8')
fails = []
def ok(name, cond):
    print(('PASS ' if cond else 'FAIL ') + name)
    if not cond: fails.append(name)

def seg(a, b, span=8000):
    i = src.find(a)
    if i < 0: return ''
    j = src.find(b, i + len(a)) if b else -1
    return src[i:j] if j > i else src[i:i + span]

# --- 基線不變 ---
ok('SAVE key／softRev／?v= 不變', 'starVolunteer_map_v19w' in src and 's107' in src and 'v20a10' in src)
ok('NOTES_V20A144 在位', (p.parent / 'NOTES_V20A144.md').exists())

# --- 一、常數 ---
ok('每日上限收緊到 1', 'const ENC79_DAILY_CAP = 1;' in src)
ok('每週硬上限 2', 'const ENC79_WEEKLY_CAP = 2;' in src)

# --- 二、計數器 lazy-init ---
ok('S.starWeek lazy-init（enc79EnsureStars）', 'S.starWeek = { week:-1, triggered:0 }' in seg('function enc79EnsureStars()', 'function enc79StarState(', 3000))

# --- 三、檢查＋入帳位置（enc79TryIntercept） ---
itc = seg('function enc79TryIntercept(', '/* ---------- sheet 降格描寫', 6000)
ok('每週上限檢查喺每日檢查隔籬', '(sd.triggered||0) >= ENC79_DAILY_CAP' in itc and '(S.starWeek.triggered||0) >= ENC79_WEEKLY_CAP' in itc
   and itc.index('(S.starWeek.triggered||0) >= ENC79_WEEKLY_CAP') - itc.index('(sd.triggered||0) >= ENC79_DAILY_CAP') < 200)
ok('每週計數遞增喺 sd.triggered 遞增隔籬（跳過都計）', 'sd.triggered = (sd.triggered||0) + 1;' in itc and 'S.starWeek.triggered = (S.starWeek.triggered||0) + 1;' in itc
   and itc.index('S.starWeek.triggered = (S.starWeek.triggered||0) + 1;') - itc.index('sd.triggered = (sd.triggered||0) + 1;') < 200)

# --- 四、週定義跟現成 weekNumNow ---
ok('跨週重置用 weekNumNow()', 'weekNumNow()' in itc and 'S.starWeek.week!==wk144' in itc)
ok('weekNumNow 本身係星期一界（dayIndex/7）', 'Math.floor(((S&&S.dayIndex)||0)/7)+1' in src)

# --- 五、不變項 ---
ok('冷卻 3 日不變', 'const ENC79_COOLDOWN = 3;' in src)
ok('級數上限 [30,55,80,100] 不變', 'const ENC79_FAV_CAPS = [30,55,80,100];' in src)
ok('每週好感軟頂 10 不變', 'const ENC79_WEEK_SOFT_CAP = 10;' in src)
ok('出沒率 base 0.5 不變', re.search(r'let p = 0\.5', seg('function enc79PresenceP(', 'function enc79EnsureDay(', 3000)) is not None)

print('\n' + ('FAILURES: ' + ' | '.join(fails) if fails else 'ALL PASS'))
sys.exit(1 if fails else 0)
