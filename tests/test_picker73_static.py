# -*- coding: utf-8 -*-
# v20a73 PICKER73 靜態測試：排程課程選擇器瘦身（用戶 2026-11-10 15:16 拍板）。
# 原則：選擇器只方便排訓練行程——未開放成課隱藏、未報名只出一句純文字、
# 任何「前往」跳轉掣／handler 都唔准喺 picker 入面出現。
# 反證：喺 v20a72 index 上行會 FAIL（冇 train73 分流、picker 仲有三種前往掣＋gloc handler）。
# 用法：python3 tests/test_picker73_static.py [path-to-index.html]
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
ok('PICKER73 標記在檔', 'PICKER73' in src)

# --- 三分流部件 ---
ok('三分流函數齊（train73CourseKind／train73EnrollNote）',
   'function train73CourseKind' in src and 'function train73EnrollNote' in src
   and '"unenrolled"' in src and '"locked"' in src)
ok('未報名純文字句格式（「課名」未報名——去 地點 報名。）',
   '未報名——去 ' in src and ' 報名。</p>' in src and 'train73-note' in src)
ok('零報名總說明＋樣式（train73-zero）', '你仲未報名任何課程' in src and 'train73-zero' in src)
ok('成組未開放通用一句（唔出課名唔出條件）', '暫時未開放報名' in src)

# --- picker 本體零跳轉 ---
_i = src.find('function train71CourseCard')
_j = src.find('function train71RenderPanel')
picker_block = src[_i:_j] if 0 <= _i < _j else ''
ok('picker 本體抽取到（train71CourseCard → train71RenderPanel）', bool(picker_block))
ok('picker 本體冇 data-gloc 屬性', 'data-gloc' not in picker_block)
ok('picker 本體冇「前往」字眼（冇跳轉掣文案）', '前往' not in picker_block)
ok('picker 本體冇 guide68-go 跳轉掣樣式', 'guide68-go' not in picker_block)
ok('picker 本體保留排入掣（已報名可排）', 'data-t71pick' in picker_block)
# v20a74 改版：主攻目標成個移除（用戶 2026-11-10 16:06 拍板）——
# 舊斷言「保留目標設定入口」改為驗全清；喺 v73 index 上行會 FAIL（反證）。
ok('v74：picker 本體冇目標設定入口（冇 data-gtgt／冇「主攻」）', 'data-gtgt' not in picker_block and '主攻' not in picker_block)

# --- handler 冇跳轉分支 ---
_h = src.find('function train71HandleClick')
_w = src.find('(function train71WirePicker', _h)
handler_block = src[_h:_w] if 0 <= _h < _w else ''
ok('handler 抽取到（train71HandleClick → wirePicker）', bool(handler_block))
ok('handler 冇 data-gloc 分支', 'data-gloc' not in handler_block)
ok('handler 冇呼叫 ux68GoLoc', 'ux68GoLoc(' not in handler_block)
ok('handler 保留排入處理（applyActToUnlocked／planDraft 寫入）',
   'applyActToUnlocked(cid' in handler_block and 'planDraft[planSelDay] = cid' in handler_block)

# --- 唔好誤傷其他系統 ---
ok('ux68GoLoc 本體保留（picker 以外唔受影響）', 'function ux68GoLoc' in src)
ok('課程狀態衍生保留（ux68CourseStatus／ux68UnlockRule 冇郁）',
   'function ux68CourseStatus' in src and 'function ux68UnlockRule' in src)
ok('全日訓練入口保留（quickFillTrain 開選擇器）',
   'function quickFillTrain' in src and 'train71TogglePanel()' in src)

print('FAILURES: ' + ' | '.join(fails) if fails else 'ALL PASS')
sys.exit(1 if fails else 0)
