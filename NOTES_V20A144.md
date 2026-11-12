# NOTES_V20A144 — 紅星巧遇頻率收緊（每日 1 次＋每週 2 次）

- 用戶 2026-11-12 22:56 拍板：巧遇由「每日上限 2 次」收緊到「每週上限 2 次＋每日上限 1 次」。原因：實玩覺得太易刷到——每粒星主場固定，摸熟之後每日去兩個有星嘅地方就穩攞 2 次，一星期最多 14 次。
- 設計依據：`~/workspace/linji-encounter-design.md` §1.2（每日上限 2、冷卻 3 日、出沒率 50%）；本次只改頻率，唔郁其他參數。

## 改動（index.html，9 行新增／1 行改值）
1. `ENC79_DAILY_CAP`：2 → **1**（L51232，註解一併改）。
2. 新增 `ENC79_WEEKLY_CAP = 2`（L51233）。
3. 新增 `S.starWeek = { week, triggered }`，lazy-init 喺 `enc79EnsureStars()`（跟 `S.starFavWeek` 先例）；舊存檔唔使遷移（由當前週起計）。
4. `enc79TryIntercept()`：每週上限檢查放喺每日上限檢查隔籬；跨週重置用現成 `weekNumNow()`（星期一界，1990-01-01 星期一起步，跟 `S.starFavWeek` 同一套週，唔發明第二套）；每週計數遞增放喺 `sd.triggered` 遞增隔籬——跳過都計，同每日上限邏輯一致。
5. 唔郁：3 日同星冷卻、出沒率 50%、好感級數上限 `[30,55,80,100]`、每週好感軟頂 10。唔加新 UI（每日上限本身都冇 UI 提示，撞上限靜靜唔觸發，維持一致）。

## 紅線
- SAVE key（`starVolunteer_map_v19w`）、softRev s107、產品 `?v=` v20a10 不變；唔直改 content pack JSON；註解冇寫其他測試硬計嘅版本字串。

## 測試
- 新：`tests/test_enc144_logic.js`（常數／同日第二次擋／同週第三次擋／跳過照計／跨週重置／冷卻不變／軟頂不變／出沒率 base 不變／starWeek lazy-init＋冪等）、`tests/test_enc144_static.py`（常數／lazy-init／檢查＋入帳位置／weekNumNow／不變項／紅線）。
- 反證：兩新測試喺 pristine main（v20a141，`git show HEAD:index.html`）乾淨 FAIL；工作副本 ALL PASS。
- 舊測試跟進（規格改動，唔係回歸）：`tests/test_enc79_static.py` 嘅 `ENC79_DAILY_CAP = 2` 斷言改做 `= 1` 並加 `WEEKLY_CAP = 2`；`tests/test_enc79_logic.js` 相關註解／名改做每日上限 1（斷言本身 `triggered=2` 仍擋，邏輯不變）。
- 全套：`qa144/suite_baseline144.txt`（pristine baseline：PASS 196／FAIL 12，12 個全部係舊 static）vs 工作副本 `qa144/suite_work144.txt`（**PASS 198／FAIL 12，FAIL 清單完全一致，零回歸**；PASS +2 係兩個新測試）。

## 實駕
- `qa144/drive144.py` → `qa144/drive144.json`＋截圖 `qa144/shots/`，**OVERALL PASS（16/16 checks，零 page error）**，430×932，`?softPreview=1`，本地 server（起 server 時核 sha＋驗 `ENC79_WEEKLY_CAP` 在位，防撞 port 食錯 code）：
  - ① 日 0：茶餐廳初遇廖炳星（14 句＋選項「大膽講邊句橋好笑啲」，好感 0→+3），`S.starWeek={week:1,triggered:1}`、`S.starDay.triggered=1`；同日第二個有星地點（天星音樂，陸柏言在場）直接開 sheet 唔觸發，計數不變。
  - ② 日 1：茶餐廳再遇廖炳星（11 句，冇選項，好感不變），`S.starWeek={week:1,triggered:2}`；日 2：茶餐廳廖炳星在場但唔觸發，`S.starWeek={week:1,triggered:2}`、`S.starDay.triggered=0`。
  - ③ 推到日 7（星期一）：先經週計劃畫面確定行程返地圖；獅子山製片初遇陸柏言（11 句＋選項「雙手遞返，唔多口」），`S.starWeek={week:2,triggered:1}`——跨週重置證實。
  - ④ 正常流程：三段巧遇對白／選項／好感（廖 +3、陸 +3）零回歸；最終 `stars：luk fav 3 seen 1、liu fav 3 seen 2`。
  - Drive 教訓（已修入 drive，未改遊戲）：有 soft 行程嘅日子地圖出「開始今日行程」唔係「過一日」（end_day 兩條路都支援）；schedule 執行有機會一日跳兩日（日 5→7，drive 以實際 dayIndex 為準，唔假設每日只進一日）；星期一朝早開週計劃要確定先返到地圖；出沒盤 Python 重算（FNV-1a 日種子）同 live `S.starDay.presence` 每次都對得上。
  - 殘留觀察（唔係 bug）：`enc1_sheet.png` 同 `enc2_sheet.png` byte-identical——同一個地點全屏 sheet、內容完全一樣，合理。

## 合併紀錄
- Squash merge 入 main：`a9c66cd`（分支 `v20a144`，工作 commit `02ef4cb`），已推上 GitHub。
- 線上核實（push 後約 3 分鐘）：index.html **5,194,707 bytes、sha256 `9d0ad918f4b009abd1210e77a6118c2b587335f958df9b63cd45f1faaa60aff1`**，同 repo HEAD 完全一致；`ENC79_WEEKLY_CAP` 線上在位。
- 獨立核實（統籌親自重跑）：新測試喺 pristine main 乾淨 FAIL（logic 抽唔到 `ENC79_WEEKLY_CAP` 即 throw；static 8 FAIL）；全套親自重跑 **PASS 198／FAIL 12**，FAIL 清單同 baseline 完全一致，零回歸。
