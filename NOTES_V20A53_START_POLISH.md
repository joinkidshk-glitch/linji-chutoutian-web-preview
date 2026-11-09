# NOTES v20a53 — 開始畫面打磨（企立裁口／簡介對比／揀槽詳情）＋片場圖換 v5 定版

基線：v20a52 合併版（linji-work52m，4,219,135 bytes）→ 本版 **4,256,978 bytes**（+37,843：片場圖換版 +33,940 字節字串差＋v53 CSS 段約 +1.9KB＋其餘為編碼浮動；全檔低過 ~4.35MB 線）。全部改動只限呈現層＋一張內嵌圖數據；冇掂 SAVE key／softRev／?v=／任何邏輯／三掣 id・綁定・停用態。

## 1. 阿偉企立裁口：腰位 → 髖位

根因：企立原圖 `UI40_STAND.awi` 本身係腰上圖（325×500，圖底邊＝髖／褸尾，插袋手喺圖高 88–97%）。舊 CSS 高 `min(44%,372px)`＋`bottom:148px`，通告紙（#btn-new）頂邊喺圖高 **87.2%** 處斬斷（harness 探針實測，390×844 同 468×960 一致）——正好遮晒插袋手同褸尾，淨返頭＋軀幹，睇落似半身像。

修法（v53 CSS 段同選擇器覆寫）：`height:min(52%,430px)`、`bottom:170px`。
實測：紙邊裁口落到圖高 **94.1%（390×844）／93.9%（468×960）**，即髖位——插袋手、褸尾入鏡，圖底邊（674／790）藏喺通告紙垂直範圍（648–715／764–831）入面，唔會露出圖邊。頭頂（y244／y360）仍低過標題（底 173／204）同副題（底 208／239），冇遮標題／副題；390 版髮頂輕掠簡介第二行右端下方（文字喺 z-3 上層＋柔霧托底，可讀性無損，截圖可見）；冇出界；`.start-inner` 兩尺寸都唔使捲（scrollH=clientH）。

## 2. 簡介句對比

根因：`.start-intro` 米色字（rgba(248,239,219,.94)）直接疊喺繁忙街景上，只靠兩層文字陰影；scrim 漸變喺簡介所在高度（約 26–31%）已跌到 .22→0，部分字同窗框／空白招牌重疊難讀。

修法（作用域限 `#app #v-start .start52`）：
- `.start-intro` 加放射漸變柔霧托底 `radial-gradient(115% 135% at 50% 45%, rgba(24,12,2,.55) → .40 55% → 0 78%)`——邊緣淡出嘅霧，唔係硬黑 band；`border-radius:18px`。
- 文字陰影加強：`0 1px 2px rgba(0,0,0,.92), 0 2px 7px rgba(0,0,0,.85), 0 4px 20px rgba(0,0,0,.6)`。
- 版面補償：`margin:12px→2px`＋`padding:10px 16px`、`max-width:300→332px`（border-box 下保內容闊 300），文字位置同折行不變（探針：仍 2 行，盒高 45→65 只係托底範圍）。
- `.start-scrim` 中段同步輕微加深（24% .22→.30、34% 新增 .17、46% 0→.05），頭尾原 stops 不變。

## 3. 揀槽 modal 詳情行睇唔到

根因（computed-style 探針實測，同實機症狀逐項吻合）：modal 本體係米紙底（#F2EBD8），但槽行 `.slot-row` 係舊深色主題組件——底 `var(--panel2)` #4A433C；詳情行 `.slot-meta` 色 `var(--muted)` #6B5340，**對比 1.36:1**，深啡字疊深啡底幾乎消失。而 `.slot-title` 繼承按鈕色 `var(--text)` #F2EBD8（對比 8.17:1）、`.slot-tag` 金色，所以實機「只見槽號同黃色標籤」。

修法：`.slot-list .slot-row .slot-meta{ color:#dccba6 }`——`.slot-list`/`.slot-*` 只由 `openSaveSlotsModal` 產生，作用域天然限嗰個 modal，其他 modal 排版零影響；base 規則原封不動。修復後 computed 對比 **6.08:1**，三行詳情（第×週・存款・幕前聲望／空白槽）全部清晰（harness 截圖實證）。

## 4. 片場場景圖換定版 v5（追加項，取代中途 v2／v3／v4）

- 對象：`UI40_SCENE.studio` 內嵌數據。舊圖問題：唐樓招牌上下疊兩三塊、中景有糊咗嘅物件、折凳變形。
- 定版來源：`~/workspace/linji-native-design/p1/scenes/media-generation-scene-clearwaterbay-studio-v5-0-99d3bc7d-ff19-4737-8da8-464cbba2cbb5.webp`（每鋪一塊招牌、上層百葉窗＋露台欄杆、折凳左三＋中二＋木箱電線圈、中景改疊好嘅器材帆布袋＋摺埋靠牆折凳、構圖／吊臂／反光板原封、零文字；換前已逐項開圖核實）。
- 編碼規格跟返既有做法：唔原圖直塞——原圖 1376×1824 WebP 先縮到 **800×1060、JPEG q70**（同 UI40_SCENE 其他場景一致：全套 800 闊 JPEG）。
- Byte 帳：內嵌二進制 140,659（舊）→ 167,614（v5），base64 字串 187,571 → 223,511（+35,940）；全檔 4,219,135 → 4,256,978（連 v53 CSS）。
- **影響範圍**：`UI40_SCENE.studio` 同時係 (a) 開始畫面背景（boot 接線 `#start-bg`）同 (b) StoryPlay 片場場景背景（`UI40_BG_BY_KEY` 經 `spBgImageCandidates`）——兩處一齊換新圖，係一致性正確，唔係副作用。LOC_SHEET_BG 冇用到 studio，無影響。

## 改動清單（方便移植）

1. `</style>` 前（v20a52 段之後）新增「v20a53」CSS 段 4 條規則：`.start-standee` 覆寫、`.start-scrim` 覆寫、`.start-intro` 覆寫、`.slot-list .slot-row .slot-meta` 新規。v52 原規則全部原封（靠同特異度＋後置勝出）。
2. `UI40_SCENE.studio` data URI 一處換成 v5 重編碼版。
3. 新增測試 `tests/test_start53_static.py`（30 斷言）＋ harness `build_harness53.js`／`shot53.py`。

## 驗證

- `node --check`：兩段 script 全 OK。
- **repo tests 全套 39/39 檔案 PASS**（基線 38 個可跑測試檔＋新增 1；tests 目錄 39 條目含 fixtures 資料夾）。新測試行落 v20a52 基線有 14 項 FAIL（反證成立）。
- 紅線 grep：SAVE key `starVolunteer_map_v19w`、softRev s107、產品 `?v=` v20a10 全部原樣；style 大括號平衡。
- 推門修復（v20a51）原封：靜態測試守住 `.push-door` z-index:15＋`.push-door-bell` left:6%（PASS）。
- Harness 截圖（`harness/`，抽真 style＋真 DOM，Playwright）：
  - `start53_before_390.png`／`start53_before_468.png`：修復前（裁口 87.2%／87.1%、簡介無托底；背景仍舊圖）
  - `start53_after_390.png`／`start53_after_468.png`：修復後＋v5 背景（裁口 94.1%／93.9%、簡介柔霧托底、招牌單塊、折凳正常）
  - `slots53_before.png`／`slots53_after.png`：揀槽 modal 前後（詳情行對比 1.36:1 → 6.08:1）
  - 探針數值全部喺 shot53.py 輸出留底（standee/intro/btnNew 盒、visibleFrac、computed 色值同對比）。

## 補記（主代理，出貨前）
- 片場圖定版最終改用 **v6**（`media-generation-scene-clearwaterbay-studio-v6-0-…webp`）：用戶放大覆核 v5 後指出反光板右邊嗰堆器材（椅背＋木箱＋帆布袋）仍然糊成一團，v6 將嗰堆成嚿移除、補返鋪前石級同空地，同位放大截圖驗證乾淨。編碼同樣 800×1060 JPEG q70，主代理喺 work53 直接替換 data URI（一處），其餘 v53 改動不變。
