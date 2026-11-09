# NOTES V20A43 — 大地圖：刪底部快捷列＋地圖放大＋釘改隱形熱區

性質：soft 預覽版面改動。**純 CSS 改動**：主 `<style>` 段尾新增一段「v20a43 皮膚層」（喺 v20a41/42 層之後），冇刪任何 DOM、冇改模板、冇改 JS／drawMap 邏輯、冇新素材。唔改 SAVE key（starVolunteer_map_v19w）、softRev（s107）、產品 ?v=（v20a10）；唔改 content pack；唔改 LOCS 座標。回滾方法：成段 v20a43 皮膚層刪走即還原。

用戶指示（2026-11-09 20:22–20:23）：(1) 地圖下面嗰行地點快捷鍵成行刪走；(2) 大地圖頁面再大啲；(3) 地圖上嘅釘都唔要（太醜）——改隱形熱區，篤建築本身入地點。

## (1) 底部地點快捷列——元素出處同刪法

- **元素**：`#map-area-list`（class `map-area-list`）。唔喺靜態模板入面——係 `drawMap()` 尾段（「底欄快捷：預設只列『有事做』」嗰段，成段包喺 try/catch）**每次畫地圖時動態生成**：`document.createElement("div")` → `host.parentNode.insertBefore(list, host.nextSibling)` 插喺 `#map-hint` 之後（即 `.map-wrap` 入面、hint 下面），再填入各地點 `<button data-loc>` 並逐個綁 `onclick → openLoc(...)`。CSS 本體喺行 3105–3106。
- **刪法**：v20a43 段加 `#app #map-area-list{ display:none !important; }`。DOM 同 JS 完全保留：drawMap 照生成、照填、照綁掣，只係唔渲染、唔佔版面（display:none 喺 .map-wrap 嘅 flex column 入面等於零高度），零報錯風險（嗰段本身仲有 try/catch 兜底）。冇直刪模板／JS——因為佢係 JS 動態產物，刪生成邏輯先係高風險，CSS 隱藏係正路。
- **連帶效果**：v20a41/42 修嘅對話舞台底部漏光，透出嘅正係呢條列；而家列本身唔渲染，漏光源頭消失（story-play-on 嗰段 CSS 一行冇郁，v20a42 嘅不透明承托保留）。
- **連帶決定（圖例）**：`#map-legend`（有通告／情報／劇／熟人／星 五個圖例）一併用同一手法隱藏。理由：圖例淨係解釋釘上面嘅徽章，釘同徽章冇咗（見 (3)）之後圖例變成誤導資訊兼食位；JS 對佢只係 set 入面幾張 icon 嘅 src（`lg-board` 等），隱藏零影響。呢項係實作判斷，已喺度申報，如要保留圖例刪 v20a43 段嗰一條規則即可。

## (2) 地圖放大——點解之前未用盡＋改前改後尺寸推算

查明嘅版面帳（`#v-map` 係 flex column；`.map-wrap` 係 flex column、flex:1）：
- 由上而下食位：`#map-bar`（HUD，冇郁，約 74px）→ `.map-wrap` 入面：`#map-legend`（約 26px 連邊距）→ `.map-polaroid`（flex:1）→ `#map-hint`（約 40px，保留——佢係玩法提示唔係地點快捷）→ `#map-area-list`（掣高約 26px/行＋gap 4＋margin-top 6；預設淨列「有事做」地點，常見 2 行約 62px，多則 3 行約 92px）。
- 舞台尺寸舊制：`.map-polaroid` 左右 margin 6px＋border 1px×2 → 舞台闊 = 框闊 − 14；高度 = flex 食剩。`.map-img` 舊制係行 1510 嘅 `width/height:100% + object-fit:cover + object-position:center 42%`（全部 !important）——舞台闊高比同圖（MAP_IMG 1080×1432，比例 0.7542）唔同嗰陣，**cover 會裁走圖邊**；釘（熱區）係 `.map-pins` inset:0 跟舞台百分比定位，裁圖嗰陣對位純靠彩數（v20a39 標定嗰陣瀏覽器框高啱啱令舞台比例 ≈ 圖比例先至冇出事）。

改法（v20a43 段）：
- `#map-area-list`、`#map-legend` display:none → 騰出約 26＋62 ≈ **88px** 高（area-list 行數浮動，範圍約 62–118px）。
- `.map-polaroid` 左右 margin 6px→2px → 舞台闊 **+8px**；`justify-content:center` 令舞台喺騰出嘅空間垂直置中。
- `.map-well` 改 `flex:0 1 auto; height:auto`、`.map-stage` 改 `height:auto`（蓋過行 1473/1505 嘅 height:100% !important，特異度 #app 前綴勝出）、`.map-img` 改 `height:auto + object-fit:contain`：**舞台高度跟圖自然比例行（闊 ÷ 0.7542），成張圖完整顯示、任何框尺寸都永不裁圖**；`.map-pins` 本來就 inset:0 貼舞台（行 1474），舞台＝圖框，熱區百分比同建築天然對齊，唔再靠彩數。drawMap 寫 pins 盒高度嗰句用 `.map-well` clientHeight，新制下 well 高＝舞台高＝圖高，數值一致。

尺寸推算（假設手機框 390×844、#app 闊 390、bar 約 74px；數字係 CSS 幾何推算，非實測）：

| | 改前 | 改後 |
|---|---|---|
| 舞台闊 | 390−14 = **376px** | 390−6 = **384px**（+8） |
| 舞台高 | flex 食剩 ≈ **634px** | 384 ÷ 0.7542 ≈ **509px**（跟圖比例） |
| 圖渲染 | cover：scale = max(376/1080, 634/1432) = 0.443 → 478×634，**左右共裁走 ≈102/478 ≈ 21% 圖闊睇唔到** | contain 自然比例：scale 0.356，**全圖 100% 可見，裁圖 0%** |
| 可見地圖內容 | 約 79%（闊度計） | **100%** |

補充：框冇咁高嗰陣（例如 Safari 可視高約 700px）改前舞台約 376×490、比例 0.767 ≈ 圖比例，cover 裁圖得約 1%（近乎冇裁）、scale 0.348；改後 384×509、scale 0.356（線性 +2.3%）兼全圖可見。即係：**放大嘅實質係「成張圖入晒畫面＋闊 +8px」，唔再係靠裁邊填高**。舞台高度而家由圖比例決定，唔會再拉高嚟裁圖——呢個係「完整可見、保百分比對位」要求下嘅幾何必然，喺度講明。

## (3) 釘改隱形熱區＋NPC 徽章處理

釘嘅結構（drawMap 生成）：每地點一個 `<button class="pin …" data-loc>`，`style.left/top = LOCS %`，入面係 `<span class="pin-head"><span class="marks">徽章…</span><img class="pin-img" 釘圖></span><span class="plab">地點名</span>`；綁定有兩層：`btn.onclick = goPin`（入面有最近釘解析：篤中位置 10% 內有多支釘嗰陣揀最近、優先有事做嗰支）＋ `.plab/.pin-img` 各自嘅 click listener（同一個 goPin）。

改法（v20a43 段，純 CSS，drawMap 一行冇改）：
- **熄視覺**：`.pin .pin-head`、`.pin .pin-img`、`.pin .plab`、`.pin .marks`、`.pin .dot` 全部 `display:none !important`；`.pin` 本體 `filter:none`（去埋 drop-shadow）、`background:transparent`、`-webkit-tap-highlight-color:transparent`。畫面淨返地圖本身——地標建築就係介面。
- **保熱區**：`.pin` 本體保留喺 DOM 同佈局，改做 **64×64px** 正方熱區（≥ 44px 易篤標準；約等於舊釘連名牌佔位 ~78×75px 嘅核心範圍），`transform:translate(-50%,-50%)` 以 LOCS 座標為正中心（舊 -50%,-92% 係遷就釘尖位置，冇釘之後改置中先至係「篤建築」）。掣本體 pointer-events 本來就係 auto（行 1475 !important）；`btn.onclick` 照收 click（子元素 display:none 只係令佢哋自己唔再收事件，唔影響掣本體）；`dataset.loc`、`aria-label`（地點名＋通告/事態/熟人狀態）原封不動，無障礙讀名不受影響。
- **重疊安全**：最密一對熱區（灣仔唱片↔天星音樂，座標距約 10.3%）64px 熱區會有重疊；邊個掣喺面上由 drawOrder 決定（有事做後畫＝喺面），而 goPin 本身有最近釘解析，會按篤中位置揀返最近嗰個地點，唔會因為重疊亂開。v20a39 標定時刻意令點距 ≥10.3% > CLUSTER 7.5%，所以冇扇形錯開，熱區中心 = LOCS 座標 = 建築位置。
- **NPC「熟人」徽章**：出處係 drawMap 嘅 marks 組裝——`hasNpc`（`S.locNpc[L.id]` 有派位）嗰陣 push 一張 `legend_acquaintance` 圖（冇圖就 👤）入 `markImgs`，渲染喺 `.pin .marks` 入面（釘右上角嗰列徽章之一，同通告📋／情報／劇／星 並排）。所以隱藏 `.marks` 即同時收起 NPC 徽章，唔會浮空留喺圖上。**功能零影響**：`S.locNpc` 派位邏輯（refreshNpc）、地點 sheet 嘅在場 NPC 顯示（loc-who／傾談掣行 locNpc＋residentNpc 兜底）全部冇掂——入到地點照樣見到邊個喺度、照樣傾到談。
- **冇郁嘅相關物**：`.pin.hidden`（display:none 語義）冇被新規則覆蓋；`#map-show-all-locs`（HUD「全部地點」掣）保留——佢而家淨係影響熱區嘅 drawOrder/aria 同 wrap class，視覺淡化對隱形熱區冇意義但冇害，HUD 按用戶要求冇郁。

## 驗證

- 逐行 diff（vs v20a42 線上版）：**全檔只有一處新增**——行 4033 起插入 v20a43 皮膚層共 68 行，零刪除、零改動其他行；模板／JS／素材／LOCS 全部冇掂。
- `node --check`：2 段 script 全部 OK。
- **repo tests 全套 30/30 PASS**（16 node 邏輯＋14 python 靜態，副本根目錄傳 index.html 路徑）。
- CSS 大括號平衡：v20a43 段 8/8、全 style 段 1296/1296。
- 特異度核實：新段規則全用 `#app` 前綴＋!important，逐條壓過要覆蓋嘅舊規則（行 1473 .map-stage height、行 1505 .map-well flex/height、行 1510 .map-img cover、行 2641 .map-polaroid margin、行 3105 .map-area-list display）——已逐條對照行號確認。
- 紅線 grep：`starVolunteer_map_v19w` 在位（10 處引用）、`softRev=s107` 在位、`"v20a10"` 在位（7 處）。
- Byte 數：4,191,715 → **4,195,286**（+3,571，純 CSS＋註解，仍喺推送通道上限內）。

留待主代理：推分支＋PR＋部署核實＋實機驗（重點望：地圖頁冇咗底部列同圖例、地圖全圖可見冇裁邊、篤建築入到對應地點 sheet、釘/名牌/熟人徽章全部唔見、對話舞台冇漏光回歸）。
