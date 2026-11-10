# -*- coding: utf-8 -*-
# v20a71 PROGRESS71＋PART3 靜態測試：
#   一、storyMainProgressLine 組句改版（完整句子、冇拼裝碎片）＋地圖 hint 行可撳
#   二、手帳「進度」子頁（行程組）接線＋防劇透＋年份紅線
#   三、PART3A 返回地圖去重／PART3B 訓練選擇器接線／PART3C 結算卡移除
# 反證：喺 v20a70 index 上行會 FAIL（冇 PROGRESS71／train71、仲有拼裝句同結算卡）。
# 用法：python3 tests/test_progress71_static.py [path-to-index.html]
import sys
from pathlib import Path
p = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent.parent / 'index.html'
src = p.read_text(encoding='utf-8')
fails = []
def ok(name, cond):
    print(('PASS ' if cond else 'FAIL ') + name)
    if not cond: fails.append(name)
def seg(a, b):
    i = src.find(a)
    j = src.find(b, i) if i >= 0 else -1
    return src[i:j] if 0 <= i < j else ''
def segN(a, n):
    i = src.find(a)
    return src[i:i + n] if i >= 0 else ''

# --- 基線不變 ---
ok('SAVE key／softRev／?v= 不變', 'starVolunteer_map_v19w' in src and 's107' in src and 'v20a10' in src)

# --- 一、組句改版 ---
prog = seg('function storyMainProgressLine(){', 'function storyMapHintHtml(){')
ok('PROGRESS71 標記存在', 'PROGRESS71' in src and 'PROGRESS71：組句全面改版' in prog)
ok('進度行冇「開咗去」拼裝碎片', '開咗去' not in prog)
ok('進度行冇「即將」碎片頭', '即將' not in prog)
ok('進度行冇 locBit37 舊拼裝', 'locBit37' not in prog)
ok('進度行用完整句部件（未開——／仲差／就會觸發）',
   all(s in prog for s in ['未開——', '通告仲差 ', '就會觸發。', '已經開咗']))
ok('進度行有「條件已經夠晒」守衛句（只喺閘數據在手嗰陣先講）', '條件已經夠晒' in prog)
picker = segN('function playOpenPicker(){', 30000)
ok('劇情列表兄弟句改完整子句（開咗之後…就會觸發）', '開咗之後' in picker and '開咗去' not in picker)

# --- 一（續）、地圖 hint 行可撳 ---
hint = seg('function storyMapHintHtml(){', 'function refreshMapHintStory(){')
ok('hint 內容態出掣（data-prog71 恰好兩處：有劇情行＋進度行）', src.count('data-prog71="1"') == 2)
ok('hint 錯誤／載入態保留普通 span（唔撳得）',
   'map-hint-story-err' in hint[:600] and 'data-prog71' not in hint[:600]
   and '劇情內容載入中，請稍候。' in hint and hint.count('data-prog71') == 2)
ok('hint 撳入開進度頁（委派＋enterHome progress）',
   'enterHome(null, false, "progress")' in src and 'closest("[data-prog71]")' in src)
ok('hint 進度句改副行承載（map-hint-story-remain）', '<span class="map-hint-story-remain">' in hint)

# --- 二、進度子頁 ---
ok('行程組分段掣＝行程＋進度（冇訓練掣——3B 後訓練入選擇器）',
   'id="htab-plan"' in src and 'id="htab-progress"' in src and 'id="htab-train"' not in src)
ok('進度 pane 存在', 'id="home-pane-progress"' in src and 'id="progress-list"' in src)
ok('分組映射加 progress（BOOK70_TAB_GROUP）', 'progress:"plan"' in src and 'plan:"plan"' in seg('const book70GroupSub', 'function book70SyncTabGroups'))
ok('渲染函數齊（renderProgressPane71／prog71Rows／prog71GateItems／prog71StubItems）',
   all(s in src for s in ['function renderProgressPane71', 'function prog71Rows', 'function prog71GateItems', 'function prog71StubItems']))
ok('條件衍生用結構化數據（evalGate3Y／progressToward／CALIB60_NODE_WINDOWS）',
   'BehaviorGate.evalGate3Y(id)' in src and 'BehaviorGate.progressToward({ id:id })' in src and 'CALIB60_NODE_WINDOWS' in seg('function prog71GateItems', 'function prog71StubItems'))
ok('防劇透文案＋最近兩幕規則（fullLeft = 2）',
   '完成前面嘅幕之後，呢幕嘅標題同條件會逐項列出' in src and 'let fullLeft = 2' in src)
i71 = src.find('function prog71Esc')
j71 = src.find('function renderProgressPane71')
seg71 = src[i71:j71 + 6000] if 0 <= i71 < j71 else ''
ok('進度頁代碼冇舊年份／冇關海媚個名', 'prog71-row far' in seg71 and '1988' not in seg71 and '1989' not in seg71 and '關海媚' not in seg71)

# --- 三 A、返回地圖去重 ---
nb = seg('function renderNotebook(){', 'function enterHome(')
ok('PART3A 標記＋日子掣只喺強制／soft 先出', 'PART3A' in nb and 'if(forced || soft){' in nb)
ok('日子掣冇日子工作嗰陣隱藏（唔再同恆常出口撞名）',
   'hbm.style.display = "none"' in nb and 'soft ? "開始今日行程" : "返回地圖"' not in nb)

# --- 三 B、訓練選擇器接線 ---
qf = seg('function quickFillTrain(){', 'function quickClearWeek(){')
ok('全日訓練改開選擇器（唔再自動用第一課）',
   'train71TogglePanel()' in qf and 'items[0]' not in qf and 'first.name' not in qf)
ok('冇已報名課程嗰陣有 toast 引導（唔靜默失敗）', '未報名任何課程' in qf and 'toast(' in qf)
ok('選擇器共用接線（面板＋逐日清單同一 handler）',
   'function train71HandleClick' in src and 'data-t71pick' in src and 'applyActToUnlocked(cid' in src)

# --- 三 C、結算卡移除 ---
ok('結算卡 UI 已移除（冇 home-summary-card／settle-toggle 元素）',
   'id="home-summary-card"' not in src and 'id="settle-toggle"' not in src and 'id="home-summary"' not in src)
ok('enterHome 唔再填充結算卡（冇攞卡元素）',
   'getElementById("home-summary-card")' not in src and 'getElementById("settle-chev")' not in src)
ok('PART3C 標記存在（移除原因有記錄）', 'PART3C' in src)

print('FAILURES: ' + ' | '.join(fails) if fails else 'ALL PASS')
sys.exit(1 if fails else 0)
