# v20a114 實駕驗收報告（zh-HK）

- **驗收對象**：分支 `v20a114`，工作目錄 `~/workspace/linji-work114`，HEAD `4565fd2`（rebase 到 main `8e9e773`，開工時核實）。
- **驗收方法**：本地鏡像（工作副本直開 `python3 -m http.server`，port 8973／8974），Playwright headless shell（`pwenv49`），viewport 390×844，gate-on `?softPreview=1`。**只用存檔槽 3**（新開局前只寫槽 3 種子檔迫出選槽 modal；實測 `activeSlot: 3`）。**只驗收，冇改 code、冇合併、冇推 main。**
- **結果總覽：8 項全部 PASS。**主跑 `drive_114.py`（run 3）1–7 項 PASS；8a／8b 初版 FAIL 係實駕腳本問題（見「實駕環境問題」），修好腳本後補跑 `drive_114b.py` 全部 PASS。
- **pageerror 總數：0**（兩跑合計）。Console error：主跑 8 個、補跑 2 個，全部係同一個缺圖 404（見觀察項）。

## 逐項結果

| 項 | 結論 | 證據 |
|---|---|---|
| 1. 地圖顯示 | **PASS** | 新開局（1990-01-01，第 1 週，day 0），地圖底部卡：`今日出行：仲可以去 2 個地方`（`S.travel114={day:0,used:0}`）。截圖：`shots/drive_114_A_fresh_map.png` |
| 2. 計數 | **PASS** | 入 `cafe_cha`（金龍茶餐廳）：先彈廖炳星巧遇對話，撳完「下一句」開 sheet；`used 0→1`，返地圖顯示`今日出行：仲可以去 1 個地方`。再入 `gift_shop`（廟街禮品檔）：直接開 sheet；`used 1→2`，顯示`今日出行額度已用完，聽日再去`；鎖定視覺：`travel-locked` 釘 15 個、底欄掣 13 個。截圖：`drive_114_A1_cafe_sheet.png`、`drive_114_A_after1_map.png`、`drive_114_A2_gift_sheet.png`、`drive_114_A_after2_map.png` |
| 3. 鎖住 | **PASS** | 額度用完後撳第 3 個地點 `hospital`（仁康醫院）：toast 逐字核對無誤——`今日出行額度用完——今日已經去咗 2 個地方，聽日再去。`；sheet 唔開；玩家留喺 `v-map`，冇 kick 返其他畫面；`used` 維持 2。截圖：`drive_114_A3_hosp_blocked.png`（toast 實影見圖） |
| 4. 重入都計（重點） | **PASS** | 新開局：入 `cafe_cha`（`used=1`，廖炳星巧遇先播）→ 返地圖 → **再入同一個 `cafe_cha` → 開 sheet，`used=2`**，顯示額度已用完；再入 `gift_shop` → 被擋（同款 toast）。截圖：`drive_114_B2_cafe_again_sheet.png`、`drive_114_B3_gift_blocked.png` |
| 5. 聽日重置 | **PASS** | 接第 4 項（`used=2` 用晒嗰局）撳「過一日」→ day 0→1，`travel={day:1,used:0}`，地圖顯示返`今日出行：仲可以去 2 個地方`。截圖：`drive_114_B_advance_nextday.png`（影嗰陣 toast 啱啱彈起，遮咗底部卡一瞬；數值以同期 DOM 讀數為準） |
| 6. 巧遇系統未整死 | **PASS** | 新開局 day 0 當日出沒盤（由 `S.starDay.presence` 讀）：`rec_star:[陸柏言]、cafe_cha:[廖炳星]、rec_hk:[葉敏芝]、ad_adm:[鍾楚凝]、tvb_harbour:[顧明輝]`。先入 `hospital` 探盤（唔觸發），再入 `rec_star`（天星音樂）：**陸柏言巧遇對話正常觸發**（`starDay.triggered 0→1`，雙全身舞台＋「下一句」），播完開 sheet；呢次入場照計（`used=2`）。截圖：`drive_114_C0_star_rec_star_unknown.png`（檔名「unknown」係舊版腳本分類殘留，內容係陸柏言巧遇舞台）、`drive_114_C0_probe_hosp_sheet.png`。註：`enc79PresenceAt`／`enc79TryIntercept` 唔係全域函數（主 script 作用域內），改由 `S.starDay` 讀出沒盤＋`triggered` 計數驗證，效果等價。 |
| 7. 舊檔相容 | **PASS** | 攞槽 3 舊 save（`travel114.used=2`，day 0），手動刪走 `travel114` 欄寫返，reload → 讀檔槽 3：載入後 `remain=2`，顯示`今日出行：仲可以去 2 個地方`，`travel={day:0,used:0}`（lazy init 滿額，冇一載入就鎖死）；入 `cafe_cha` 計數正常（`used=1`，廖炳星巧遇先播）。截圖：`drive_114_D_old_save_map.png`、`drive_114_D_old_cafe_sheet.png` |
| 8a. 地點 sheet 各掣 | **PASS**（補跑） | 獅子山製片（`film_lion`）sheet：掣列有「只查看通告欄」「同張子駿傾談」「報名：鏡頭練習」等。撳「傾談」→ 傾談 modal 彈出（掣 `['關閉']`），撳完返 sheet；重入一次撳「通告欄」→ modal `通告欄 · 獅子山製片`（掣 `['返地點選單']`）。截圖：`shots/drive_114_G_talk_open.png`、`shots/drive_114_G_board_open.png` |
| 8b. 行程執行唔受額度影響 | **PASS**（補跑） | 新開局 Mon→Fri 四次過日全部成功（Tue 休息日／Wed／Thu 逛逛日／Fri）。Fri（day 4）先用 1 次額度入 `cafe_cha`（`used=1`，巧遇先播），返地圖撳「開始今日行程」執行街頭表演：**day 5 快照 `$12,000→$12,958`（Fri 收入 +$958），`travel={day:5,used:0}`**，即行程照常執行＋額度照常重置。之後返地圖自動連跑 Sat 強制日＋Sun 休息日（`goToMapForBrowse` kickSchedule 既定行為），終點 day 7、`$12,992`、顯示返 2 次。截圖：`shots/drive_114_H_sat_map.png` |

## 錯誤統計

- **pageerror：0**（主跑＋補跑合計）。
- **Console error**：主跑 8 個、補跑 2 個；補跑已實名，全部指向同一個缺圖：`assets/story/fullbody/liu_bingxing_shy.webp` → fallback `.png` 同樣 404（HTTP 404 ×2）。主跑嗰 8 個未記 URL，但同一流程（廖炳星巧遇）重現時只得呢兩個 URL，極可能係同一檔案喺多句 shy 表情對白重複請求所致。
- **性質**：**唔係 v114 問題**——v114 冇掂美術／表情庫；係 v106／v107 表情庫缺口類（廖炳星欠 `shy` 表情圖）。對話本身靠 fallback 正常行完，無斷、無 pageerror、截圖入面人物正常顯示。建議另開一票補圖，唔阻 v114。

## 實駕環境問題（腳本問題，唔係產品問題；已修好再驗）

1. **底欄地點掣撳唔到**：`#map-area-list` 自 v20a43 起係 `display:none`（地圖放大改版既定設計），Playwright 實體撳掣會 timeout。改行**真地圖釘**（`#map-pins button.pin`）入場，全部項目先至行得通。
2. **巧遇舞台探測唔到**：巧遇用獨立 `.e79-stage` 覆蓋，唔係 `.story-play`／`#modal-btns`；初版探測器認唔到，誤判 `unknown`。修好探測器（認埋 `.e79-stage`／`.e79-row` 掣）後，2a／4／6 全部判返啱。
3. **Toast 遮住「過一日」掣**：toast 顯示嗰 1.8 秒，`#app.toast-up` 會隱藏成個 `#map-hint`（入面有「過一日」掣）。腳本改為等 toast 散先撳。
4. **休息日／soft 日冇「過一日」掣**：Tue 休息日等日子，地圖只出「開始今日行程」掣（執行嗰日行程過日），冇 `#map-end-day`。`advance_day` 加咗 fallback（撳「開始今日行程」），Mon→Fri 先行得通。
5. **8a 初版揀錯地點**：`gift_shop` 係舖頭，本身冇通告欄／傾談掣（只得「買禮物」）。改用獅子山製片，兩隻掣齊。
6. **8b 終點唔係 day 5**：Fri 執行完返地圖，遊戲既定行為會自動連跑 Sat 強制日＋Sun 休息日，所以終點係 day 7。Fri 執行本身嘅證據用 day-5 快照（收入＋$958、額度重置）。

## 產出檔案（`~/workspace/linji-work114/qa114/`）

- `drive_114.py` —— 主驗收腳本（8 項，run 3 全數通過 1–7 項）
- `drive_114.json` —— 主跑逐項 JSON 紀錄
- `drive_114b.py` —— 8a／8b 補驗＋404 實名腳本
- `drive_114b.json` —— 補跑逐項 JSON 紀錄
- `drive_114_report.md` —— 本報告
- `shots/drive_114_*.png` —— 逐項截圖（主跑＋補跑）
- `probe114.py`、`probe2.py`、`diag114.py` —— 探路／診斷腳本（過程檔，留底）
