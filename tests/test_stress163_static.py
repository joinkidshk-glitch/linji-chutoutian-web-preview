# -*- coding: utf-8 -*-
# v20a163 靜態測試：成條地圖底部壓力提示刪走（用戶 2026-11-13 08:23 拍板，
# 舊 brief「淨刪 60–69 漸升段」作廢）。
# 刪走：#map-stress-tip 元素＋updateMapStressTip() 函數＋相關 CSS
# （#map-stress-tip／.on／.warn）＋drawMap() 呼叫點＋story-play-lock 死規則。
# ≥70「壓力偏高」／≥80「身體警號」兩段一齊消失——係用戶明確要嘅結果。
# 反證：喺 v261 main（6e051e7）index 上行會 FAIL
# （元素＋函數＋CSS＋呼叫點全部仲喺度）。
# 註：本檔係 2026-11-13 舊版 test_stress163_static.py 嘅重做版——舊版從未落地，
# 保留斷言已按現行 live 文案更新（RW 重寫後）：訓練 modal「現在壓力」、
# 週結旁白「身體警號：近來睡得差、胃口又沒有，整個人燶透」。
# 用法：python3 tests/test_stress163_static.py [path-to-index.html]
import sys
from pathlib import Path
p = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent.parent / 'index.html'
src = p.read_text(encoding='utf-8')
fails = []
def ok(name, cond):
    print(('PASS ' if cond else 'FAIL ') + name)
    if not cond: fails.append(name)

# --- 基線不變 ---
ok('SAVE key／softRev／?v= 不變', 'starVolunteer_map_v19w' in src and 's107' in src and 'v20a10' in src)

# --- v163 主改動：成條 bar 拎走 ---
ok('v163：#map-stress-tip 元素消失', 'id="map-stress-tip"' not in src)
ok('v163：updateMapStressTip 函數消失', 'function updateMapStressTip' not in src)
ok('v163：updateMapStressTip 呼叫點消失', 'updateMapStressTip' not in src)
ok('v163：map-stress-tip 字串全檔清零', 'map-stress-tip' not in src)
ok('v163：#map-stress-tip CSS 規則消失', '#map-stress-tip{' not in src)
ok('v163：#map-stress-tip.on 規則消失', '#map-stress-tip.on' not in src)
ok('v163：#map-stress-tip.warn 規則消失', '#map-stress-tip.warn' not in src)
ok('v163：story-play-lock 死規則清走', '#app.story-play-lock #map-stress-tip' not in src)
ok('v163：「壓力漸升」文案消失', '壓力漸升' not in src)
ok('v163：地圖版「身體警號」文案消失（連續多日高壓嗰句）',
   '身體警號：連續多日高壓' not in src)

# --- 保留：story-play-lock 其餘規則唔郁（淨係拎走 map-stress-tip 嗰行） ---
ok('保留：story-play-lock 其餘選擇器仲喺度',
   '#app.story-play-lock #map-focus-bar' in src
   and '#app.story-play-lock #map-hint,' in src
   and '#app.story-play-lock .map-hint,' in src)

# --- 保留：地圖其餘元素唔郁 ---
ok('保留：#map-hint／#map-money-tip 仲喺度',
   'id="map-hint"' in src and 'id="map-money-tip"' in src)
ok('保留：drawMap() 函數仲喺度', 'function drawMap(){' in src)

# --- 保留：壓力系統其餘出面位置唔郁 ---
ok('保留：全日訓練確認 modal（壓力偏高 h3）唔郁',
   'modal(`<h3>壓力偏高</h3><p>現在壓力 ${Number(S.stress)||0}。全日訓練會再推高壓力，確定要練？</p>`' in src)
ok('保留：週結 ≥80 身體警號旁白唔郁',
   '身體警號：近來睡得差、胃口又沒有，整個人燶透' in src)
ok('保留：病倒休養流程唔郁', '病倒休養（第 ${dayNo} 日）' in src)
ok('保留：conseq61 病倒判定唔郁', 'conseq61DailyTick' in src and 'sickStreak: 2' in src)
ok('保留：日期卡壓力提示（map-hint stressHint）唔郁',
   "else if(stVal>=52) stressHint=\" · <span class='bad'>壓力偏高</span>\"" in src)

# --- 回歸守衛：其他 .warn 規則唔受影響 ---
ok('回歸：.chip-stress.warn／.map-money-tip.warn 等其他 .warn 規則仲喺度',
   '.chip-stress.warn' in src and '.map-money-tip.warn' in src)

print('FAILURES: ' + ' | '.join(fails) if fails else 'ALL PASS')
sys.exit(1 if fails else 0)
