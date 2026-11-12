# v20a114 合併後冒煙實駕報告（zh-HK）

- **驗收對象**：main HEAD `cf66865`（v20a114 已合併），`index.html` 已含 TRAVEL114。工作樹 `index.html`／`assets`／`content` 經 `git diff --stat HEAD` 核實零改動（工作樹唯一 dirty 檔係 `NOTES_V20A113.md`，同驗收無關）。
- **驗收方法**：本地鏡像（main 工作樹直開 `python3 -m http.server`，port 8977；全個 repo 873M、`/tmp` 跨裝置唔支援 hardlink，所以唔另行複製成鏡像目錄，改為直接駕駛 HEAD 檔案——檔案內容即係 HEAD），Playwright headless shell（`pwenv49`），viewport 390×844，gate-on `?softPreview=1`。**只用存檔槽 3**（`activeSlot: 3` 已核實）。**只驗收，冇改 code、冇合併、冇推 main。**
- **結果總覽：6 項全部 PASS。pageerror：0。**

## 逐項結果

| 項 | 結論 | 證據 |
|---|---|---|
| 1. 地圖顯示 | **PASS** | 新開局（1990-01-01，第 1 週，day 0），地圖底部卡：`今日出行：仲可以去 2 個地方`（`S.travel114={day:0,used:0}`）。截圖：`shots/merged114/drive_merged_A_fresh_map.png` |
| 2. 計數（入 2 個唔同地點） | **PASS** | 入 `cafe_cha`（金龍茶餐廳）：廖炳星巧遇對話先播，撳完「下一句」開 sheet；`used 0→1`，返地圖顯示`今日出行：仲可以去 1 個地方`。再入 `gift_shop`（廟街禮品檔）：直接開 sheet；`used 1→2`，顯示`今日出行額度已用完，聽日再去`；鎖定視覺：`travel-locked` 釘 15 個、底欄掣 13 個。截圖：`drive_merged_A1_cafe_afterdlg_sheet.png`、`drive_merged_A_after1_map.png`、`drive_merged_A2_gift_sheet.png`、`drive_merged_A_after2_map.png` |
| 3. 額度用完再撳第 3 個地點 | **PASS** | 額度用完後撳 `hospital`（仁康醫院）：toast 逐字核對無誤——`今日出行額度用完——今日已經去咗 2 個地方，聽日再去。`；sheet 唔開；玩家留喺 `v-map`；`used` 維持 2。截圖：`drive_merged_A3_hosp_blocked.png`（toast 實影見圖） |
| 4. 重入同一地點都計 | **PASS** | 新開局：入 `cafe_cha`（`used=1`，廖炳星巧遇先播）→ 返地圖 → **再入同一個 `cafe_cha` → 開 sheet，`used=2`**，顯示額度已用完；再入 `gift_shop` → 被擋（同款 toast）。截圖：`drive_merged_B2_cafe_again_sheet.png`、`drive_merged_B3_gift_blocked.png` |
| 5. 過一日後額度重置 | **PASS** | 接第 4 項（`used=2` 用晒嗰局）撳「過一日」→ day 0→1，`travel={day:1,used:0}`，地圖顯示返`今日出行：仲可以去 2 個地方`。截圖：`drive_merged_B_advance_nextday.png` |
| 6. 巧遇仍然觸發到 | **PASS** | 新開局 day 0 當日出沒盤（由 `S.starDay.presence` 讀）：`rec_star:[陸柏言]、cafe_cha:[廖炳星]、rec_hk:[葉敏芝]、ad_adm:[鍾楚凝]、tvb_harbour:[顧明輝]`。先入 `hospital` 探盤（唔觸發，用 1 次額度），再入 `rec_star`（天星音樂）：**陸柏言巧遇對話正常觸發**（`starDay.triggered 0→1`，雙全身舞台＋「下一句」），播完開 sheet；呢次入場照計（`used=2`）。截圖：`drive_merged_C0_star_rec_star_afterdlg_sheet.png`、`drive_merged_C0_probe_hosp_sheet.png` |

## 錯誤統計

- **pageerror：0**。
- **Console error：4 個**，全部係同一類缺圖 404（`Failed to load resource: the server responded with a status of 404`）。今次跑嘅 log 冇記 URL（`requestfailed` 亦係 0，headless shell 圖片 404 唔經嗰個事件），但已即場核實：`assets/story/fullbody/` 入面廖炳星只有 `base`／`serious`／`smile` 三張，**`liu_bingxing_shy.*` 唔存在**——同分支實駕報告（`drive_114_report.md`）記錄嘅已知缺口完全一致。
- **性質：唔係 v114 合併問題**——v114 冇掂美術／表情庫；係 v106／v107 表情庫缺口類（廖炳星欠 `shy` 表情圖）。對話本身靠 fallback 正常行完，無斷、無 pageerror。建議另開一票補圖，唔阻 v114。

## 產出檔案（`~/workspace/linji-repo/qa114/`）

- `drive_merged_114.py` —— 冒煙驗收腳本（6 項，由分支版 `drive_114.py` 改編：ROOT 指 main、port 8977、shot 前綴 `drive_merged_`，刪走分支版第 7／8a／8b 項）
- `drive_merged_114.json` —— 逐項 JSON 紀錄
- `drive_merged_report.md` —— 本報告
- `shots/merged114/drive_merged_*.png` —— 逐項截圖（14 張）
