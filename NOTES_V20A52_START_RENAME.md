# NOTES v20a52 — 開始畫面重設計＋改名《臨記埋位》

基線：v20a49（線上 4,210,205 bytes）→ 本版 **4,218,447 bytes**（+8,242，全部係 CSS／標記／接線文字，**新增內嵌圖像 0**；素材全部用檔內已內嵌嘅 UI40 資產）。

## 改名落地（玩家面舊名清零）

全檔 grep「臨記出頭天」＝ **0 處**（舊版 5 處，全屬玩家面，已全改）：

1. `<title>` →《臨記埋位 · 阿偉》
2. 開始畫面品牌圖卡（`start_title_card.png`，圖入面燒死舊名）→ 成個元素移除，由 HTML 標題取代（見下）
3. sr-only h1 → 併入新版可見 h1「臨記埋位」
4. 開始畫面簡介句 →「港產新人陳偉翔（阿偉），自己跑通告——臨記埋位，一步一步上。」
5. E6「遠走」結局金句 →「臨記埋位——你嗰本帳，唔喺香港收科。」（title-drop 保留）

code 註解／dev 字串冇掂；SAVE key／softRev／?v= 冇掂。殘留 `.start-brand` CSS 規則同 `--phys-start-card` 變數係無引用嘅死規則／dev 資產變數，按守則唔郁（冇 JS 引用已移除嘅 img 元素，grep 實證）。

## 開始畫面重設計（跟已拍板視覺語言）

舊版：米紙底＋置中品牌圖卡＋膠囊掣，成版「網頁卡片」語言，下半版大量空白。新版：

- **全幅場景底**：`UI40_SCENE.studio`（片場街景：吊臂、反光板、導演椅，「開工」氣氛最濃）全屏 cover；上／下暖啡深漸變 scrim 托起標題區同選單區。
- **阿偉企立做主角**：`UI40_STAND.awi`（同對話分層同一套去背企立）企右下，高約 44% 畫面，下半身俾選單紙疊住，遮住企立圖本身腰部裁口，唔再係細頭像困喺卡入面。
- **標題係主角**：`臨記／埋位` 兩行 HTML 大字（clamp 56–78px），金箔漸變文字（background-clip）＋drop-shadow 描深邊；右上斜釘紅色印章「一九八八」（直書、雙圈印泥感）；副題「1988 · 片場星途」金字置中、兩側金線。
- **選單實物化**：「新遊戲」＝最大嗰張通告紙——米紙纖維紋（沿用 v20a47 紙紋配方）、頂部膠紙貼、右側紅色「開工」印、副字「1988 年春 · 由零開始」、輕斜 −0.7°；「繼續／讀檔」＝下方兩張細紙條（交錯輕斜）。試玩規則小字改坐喺深漸變上嘅米字 caption。
- **功能原封**：三掣 id／綁定零改動；`paintTitleSaveBtns` 嘅 display／disabled／title／文字改寫（含「繼續（尚無存檔）」）照常運作，停用紙條另加脫色＋減陰影呈現（harness 冇存檔態截圖實證文字一行放得落、狀態可辨）。`#start-soft-tip`（含 soft 模式追加「本頁修訂 s107」嘅 JS 落點）保留原位原 id。隱藏嘅 `#start-guide`／`#start-hero` 元素保留（wireUiAssets／PORTRAITS 接線唔受影響）。

## 改動範圍（diff vs v20a49 共 185 行、5 處，方便移植）

1. 行 8：`<title>` 一字串。
2. `</style>` 前新增「v20a52」CSS 段（約 148 行）：全部選擇器作用域 `#app #v-start .start52 …`，其他畫面零影響。`.start` 加咗修飾 class `start52` 疊高特異度，蓋過 v20a47 嗰段 `#app #v-start .start` 米紙底（同為 !important 時靠 (2,2,0) 勝出）。
   - **移植注意**：`#btn-new` 嘅 background／border／radius／shadow／color 必須保留 !important——主 style 段有一條全域「Physical primary buttons」規則（`button.p`，行首段約 825）用 !important 鎖死金色漸變，唔加權重張通告紙會變返金掣（第一輪 harness computed-style 探針實證：background 被食成 `linear-gradient(#E6D2A8,#C9A227)`，加權後修正）。
3. `#v-start` section 標記（約 20 行）：換成 start-bg／start-standee／start-scrim／start-inner（head＋menu＋tip）結構；移除品牌 img 同 sr-only h1。
4. E6 結局字串一處（「臨記埋位——」）。
5. boot 接線 3 行（緊貼既有 `_sh` start-hero 接線之後）：將 `UI40_SCENE.studio`／`UI40_STAND.awi` 分派去 `#start-bg`／`#start-standee`——同 wireUiAssets 既有模式一致嘅呈現接線，冇改任何遊戲邏輯。

## 驗證

- `node --check`：兩段 script 全 OK。
- **repo tests 全套 35/35 PASS**（此工作副本含 35 套；冇任何測試鎖死舊名／品牌卡，唔使改測試。基線未改前同為 35/35。）
- 紅線：SAVE key `starVolunteer_map_v19w`、softRev s107、產品 `?v=` 全部原樣（grep 實證）。
- Harness 截圖（`harness/`，抽真 style＋真 DOM，Playwright，390×844 為主）：
  - `start52_before.png`：舊版（品牌圖係外部 assets PNG，harness 以同 class 漸變色塊＋字代替，已註明）
  - `start52_after.png`：新版有存檔態——標題金箔＋紅印、阿偉企右下腰口俾通告紙遮住、新遊戲紙＋膠紙＋開工印、兩張細紙條，版面零走位（探針：title box 138×136、standee 241×371、btn-new y648 h66、inner scrollH=clientH=844 唔使捲）
  - `start52_after_nosave.png`：冇存檔停用態——兩紙條脫色可辨、「（尚無存檔）」一行放得落
  - `start52_after_desktop.png`：468×960 幾何同樣成立
  - builder／截圖腳本：`harness/build_harness52.js`、`harness/shot52.py`

## 已知取捨

- 企立圖得 stage1 一張（同對話層現況一致）；開始畫面唔跟存檔階段換造型——屬日後美術輪次，唔喺今期範圍。
- 場景圖 object-position 50% 20% 保住吊臂同街景；極短屏（高度 < 約 640）時 start-inner 可捲動（scrollbar 隱藏），選單唔會被裁死。
