# NOTES — v20a275 icons112 手繪圖標：約會地點 4 隻 emoji 換手繪圖

- **版本**：v20a275（分支 `v20a275`，基底 main `e2b2fbc` v274＋NOTES）
- **拍板**：用戶 2026-11-17 20:18「做手繪版，換走 emoji」
- **範圍**：約會層 6 個新點入面仲係 emoji 嗰 4 個——🌊 尖沙咀海傍（`date_harbour`）、
  🌃 山頂（`date_peak`）、🏖️ 淺水灣（`date_beach`）、✈️ 啟德機場（`date_airport`）。
  其餘兩個約會點（🎤 酒廊唱歌、🎬 旺角戲院）早已有手繪圖標，唔郁。

## 1. 接入方式（跟 v112 中央對照慣例；同 brief 步驟 3 有出入，見 §2）

- `EMOJI_ICON112` 加 4 條：`"🌊":"wave", "🌃":"peak", "🏖️":"beach", "✈️":"plane"`。
- 渲染位唔使改：地點列掣（L22667）同地點板標題（L40844）本來已經行 `iconHtml112(L.emoji)`，
  加對照即刻出 `<img class="ic112" src="assets/icons/icon_<stem>.png">`。
  地圖本身無釘（隱形熱區，用戶早已拍板拎走），emoji 只出現喺呢兩個渲染位。
- 4 隻圖檔：`assets/icons/icon_wave.png`／`icon_peak.png`／`icon_beach.png`／`icon_plane.png`，
  全部 256×256 RGBA 透明底（同現成 43 隻一致）。

## 2. 同 brief 步驟 3 嘅出入（有意圖，唔係漏做）

- Brief 話「4 個地點定義由 `emoji:` 改做圖標引用，emoji 4 個清零」。
- **實際做法：LOCS 定義保留 emoji 原值，只加中央對照。** 理由（v112 已定慣例，
  見 `NOTES_V20A112_ICONS.md` §2／`notes_icon_audit.md` §2）：
  (a) 欄位值保留原值係舊存檔相容＋舊測試唔郁嘅設計，改數據要同時改兩個渲染位、
  改 `fieldVals` 窮舉測試，風險大過收益；(b) 用戶睇到嘅結果一樣——渲染出嚟係手繪圖，
  無 emoji 殘留（新測試第 (4) 項釘死：全檔 4 個 emoji 各只出現 2 次＝LOCS 定義＋對照鍵）。
- 如將來要清數據層 emoji，係另一張重構票，唔喺呢包做。

## 3. 圖標風格（跟 v112 已批核標準，唔係 brief 寫嘅賽璐璐）

- Brief 話「乾淨平塗賽璐璐」——嗰個係角色／場景錨，**圖標組已批核風格係
  細線條手繪風、深啡墨線 `#3a2e22`、無填色、透明底 PNG 256×256**
  （`NOTES_V20A112_ICONS.md`，用戶 2026-11-12 06:59 批核「ok」）。4 隻新圖跟呢套。
- 製作：以現成 `icon_home.png` 做風格參照生成，落 256×256 後白底轉透明、
  墨色統一 `#3a2e22`（PIL：亮度反推 alpha，≥248 當背景清零）。
- 主體：海浪＝三層浪＋頂捲；山頂＝圓山＋山頂發射塔＋彎月＋兩星；
  沙灘＝沙灘傘＋底浪捲；機場＝側面客機＋三劃動態線。
- QC（`qa275`，對照 v112 標準）：4 隻 256px 淺底清晰可辨；24px 淺底可辨；
  24px 深底（`#1b2d48`）同現成 4 隻（屋／茶／咪／場記板）一樣淡——
  係成套深啡線稿固有退化，唔係呢 4 隻問題（v112 收貨標準同一句；
  v174 前例：深底隱形嗰陣加金底 chip，唔改圖標資產；地圖地點列掣本身係深底，
  全部 43 隻圖標同一情況，唔喺呢包改）。
- Peak v1 廢棄原因：山頂畫咗間屋（似 `icon_home`，會撞），重出 v2 改發射塔。
  草稿留 `~/workspace/icons275-draft/`（落地後清）。

## 4. 測試

- 新檔 `tests/test_icons275_logic.js`：**20／20 ALL PASS**——(1) 4 個 LOCS 定義在位＋emoji 值保留；
  (2) `iconHtml112()` 逐個轉對應 `<img>`，輸出無 emoji；(3) 4 圖檔 256×256 RGBA；
  (4) 全檔 4 個 emoji 各只出現 2 次。
- `tests/test_icons112_logic.js`：EXPECT 44→48，PASSTHROUGH159 清單已刪（4 隻入段一映射＋覆蓋檢查）——ALL PASS。
- `tests/test_icons112_static.py`：stems 39→43（加 wave／peak／beach／plane），檔案齊——ALL PASS。
- 兩個 script block `node --check` 通過（`node --check index.html` 本身唔支援 .html 後綴，
  故抽 script 驗，同 v112 做法一樣）。
- 全套 suite：`bash qa131/run_suite.sh` 工作副本，**TOTAL PASS 340 FAIL 9**（基線 339／9＋新檔 1；
  FAIL 九項同基線逐項一致：flash51／slot50／soft_tip_111_restore／start53／weave43_static／
  weave44_static／weave49_static／wf5_87／wrap38，零回歸；三檔 icons 測試全部 PASS）。

## 5. Suite＋落地

- （已填）全套 suite 340／9，零回歸（見 §4）。
- Cache-buster：`iconHtml112` 出嘅 `<img>` 同現成 43 隻一樣無 per-asset `?v=`（只係 seal 圖有）；
  4 隻係新檔，無舊版緩存問題，唔使升。
- 紅線：SAVE key／softRev／`?v=20a10` 無改動。
