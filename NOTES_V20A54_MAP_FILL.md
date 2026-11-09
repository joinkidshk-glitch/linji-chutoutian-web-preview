# v20a54 — 大地圖紙面填充 ＋ 入地圖空白（預解碼）

基線：v20a53 合併版 4,244,158 bytes → **4,247,738 bytes**（+3,580：CSS 段＋SVG data URI＋boot 接線）。
全部改動只限呈現層：SAVE key／softRev／?v=／任何邏輯／drawMap／熱區綁定零改動。

## 症狀（用戶 iPhone 實機，430×932pt 機）
1. 入地圖畫面，大地圖下方空咗一大片深色（約畫面 28%），似壞咗／未載完。
2. 入地圖嗰陣「有幾秒會空白」：頂部「今日：…」banner（toast，純 HTML）即刻出現，
   但佢下面幅地圖圖要幾秒先畫得出，期間下面空白。

## 診斷一：下方深色虛空係邊個元素
版面鏈（cascade 全查，行號以 v20a53 檔計）：
- `#app`（flex column，height:100dvh）→ `#v-map.view.on`（flex:1）→ `.bar` HUD →
  **`.map-wrap`（flex:1、flex column、overflow:hidden）** → `.map-polaroid`（flex:1 伸展、
  透明底、金幼邊）→ `.map-well` → `.map-stage` → `#map-img`。
- v20a43 定案：`.map-img` 自然比例 contain（圖 1080×1432），舞台高＝闊÷0.7542，
  係**闊度-bound**——高身屏永遠填唔滿高度，剩餘高度必然存在。
- 剩餘面積冇任何嘢油漆：`.map-polaroid` 背景透明；`.map-well` 尺寸啱啱＝舞台
  （harness 實測 well rect ≡ stage rect）；結果全部透出 `.map-wrap` 嘅底色——
  v19z20 規則 `.map-wrap{background:#2a2622 !important}`（深啡黑）。
- Harness 實測（真 CSS＋真 DOM，390×844）：polaroid 內舞台上下各有 115.3px
  透出深色；393×852 各 117.3px；468×960 各 121.6px；框下另有 39.2px（提示行區）。
- 用戶截圖像素掃描（1290×2796 原圖逐列取樣）：幅圖內容 19.9%→74.0%；
  74.2% 起連續 #2a2622 深色直到瀏覽器底欄（~91.8%），即約 165pt 以上純虛空，
  連同圖上下嘅深色帶，成個地圖區約四分之一係「唔屬於張地圖嘅深色」。
  （注：Blink harness 入面舞台係垂直置中、深色上下分；用戶 WebKit 實機幅圖
  貼近頂部、深色集中喺下方——引擎差異唔影響結論：虛空＝冇油漆嘅 wrap 底色。）

## 診斷二：banner 先出、圖後出嗰個 gap
- 「今日：…」banner ＝ `goToMapForBrowse` 嘅 `toast()`（行 27842），純 DOM，
  切 view 嗰刻即刻 paint。
- 幅圖：`#map-img` 喺 markup 冇 src；boot 接線（行 39001）先至 assign
  `MAP_IMG`（data URI JPEG，509,299 字元／382KB 二進制／1080×1432）。
  但嗰陣 `#v-map` 係 `display:none`——WebKit 唔會為隱藏圖解碼，
  decode＋raster 全部留到切入地圖嗰刻先發生，就係嗰幾秒空白；
  而未 paint 嗰陣舞台背後係 `.map-well` 嘅深藍黑 #1A1A2E（行 770），
  所以「空白」係深色一塊，唔係紙。
- Harness 量度（真 index.html、Chromium headless、CPU 節流 4×、393×852，
  截圖輪詢舞台中心像素，script `harness/time54.py`）：
  - 冷 decode 組件成本（新 Image 對 MAP_IMG 解碼）：修前 **17.6／17.5ms**（兩跑）；
    Chromium 對隱藏圖都會預解碼，所以呢個數只係下限——WebKit 延遲到可見先解碼，
    嗰份成本成份落喺切 view 嗰刻，喺真機（仲要計埋 raster 同記憶體壓力）就係以秒計。
  - 切 view → 圖 paint 完成：修前 **721／801ms**（兩跑；含截圖輪詢粒度 ~±100ms）。
    Chromium 入面呢個 gap 主要係首次 raster，唔係 decode——平台差異如實記低，
    唔將真機幾秒直接等同呢個數。
  - 參考：成個 app 冷載入去到 boot 接線執行（4.24MB 單檔 parse）約 2.2–2.3s
    （4× 節流下）——係「開 app」嘅等待，唔係用戶講嗰個入地圖 gap，範圍分清。

## 修法（兩部分，同一脈絡：紙即時喺度＋圖預先 ready）
### (1) 紙面填充——新增 `v20a54` CSS 段（`</style>` 前最後一段）
全部只改 `background`／`box-shadow` 油漆屬性，**零 layout 屬性**：
- `#app .map-wrap`：底改多層紙面——羅盤玫瑰＋「香江 · 一九八八」SVG data URI
  （背景層，置於 wrap 高度 88% 處，淡淡啡墨，幅圖會遮住佢上半，淨係下半
  喺圖下方餘白露出）＋ v47 同款纖維紋漸變 ＋ 米紙放射漸變，基色對齊幅圖
  本身紙色（實測 JPEG 角位 #F8EAD0）。所有原本透出深色嘅面積即刻變成
  同一張紙；成個地圖區讀起嚟係一張大紙本地圖。
- `#app .map-polaroid`：加 inset 內框（6px 紙邊＋1px 啡線），張紙有印刷邊界；
  inset shadow 畫喺子元素（舞台）之下，唔會覆蓋幅圖。
- `#app .map-well`／`.map-stage`／`.map-img`：底改紙色 #f3e7c9——圖未 paint
  嗰陣舞台係紙面，唔再係深藍黑（同 (2) 雙保險）。
- 冇加返任何功能元素：地圖下快捷列（`#map-area-list`）同圖例維持
  v20a43 嘅 `display:none`，冇翻生（靜態測試守住）。
### (2) 預解碼——boot 接線加一行（主 script，緊貼既有 `_mi` 接線之後）
```js
try{ if(_mi && _mi.decode) _mi.decode().catch(()=>{});
     if(_mi && _mi.src){ const _pm=new Image(); _pm.src=_mi.src;
     if(_pm.decode) _pm.decode().catch(()=>{}); } }catch(_e){}
```
對真身 `#map-img` 同一個 detached Image 各呼叫 `decode()`：玩家仲喺開始
畫面嗰陣 bitmap 已經解好，切 view 直接 paint。detached 嗰張唔喺
display:none 子樹入面，係畀 WebKit 嘅保險；兩張同 URL 共用解碼快取。
純呈現接線，try/catch 包好，MAP_IMG 缺席（fallback 圖）都唔會報錯。

## 驗證
- **幾何零偏移（紅線）**：harness（`build_harness54.js`／`shot54.py`）三個
  長寬比 390×844、468×960、393×852，修前修後 bar／wrap／polaroid／well／
  stage／img／hint 嘅 rect **逐項一致到 0.1px**；13 個 LOCS 探針釘中心
  對預期座標誤差 0–0.1px（修前修後同值）。截圖：
  `harness/map54_{before,after}_{390x844,468x960,393x852}.png`
  （after 圖：成屏一張紙、釘圈逐粒對正建築、下方羅盤＋「香江 · 一九八八」、
  提示行深色牌喺紙面上面照樣可讀）。
- **Timing（after，同條件重跑）**：冷 decode 組件成本 **17.5ms → 0.9ms**
  （boot 接線已經解好，共用快取即時命中——預解碼生效嘅直接證據）；
  切 view → paint 744ms（同修前 721/801ms 同級——Chromium 個 gap 本來
  就唔係 decode-bound，已喺診斷二講明；修嘅係 WebKit 嗰份延遲解碼成本
  同「空白係深色」嘅觀感，後者由紙面兜底）。
- `node --check` 兩段 script OK；repo tests **40/40 檔案 PASS**（含新增
  `tests/test_map54_static.py` 27 斷言；新測試行落 v20a53 基線 12 項 FAIL，
  反證成立——守住：紙面規則齊全、wrap 規則不含 layout 屬性、v43 舞台
  幾何原文不變、快捷列冇翻生、預解碼接線齊全、SAVE／推門／片場圖紅線）。

## 影響範圍與遺留
- `.map-wrap` 紙面喺 sheet 開啟／事態金框／toast 期間同樣係紙底（sheet 係
  `#v-map` 嘅 absolute 子元素，照常覆蓋下半屏，冇郁佢）。
- 原生移植備註：iOS 版起手就應該（a）地圖畫面用紙面填滿、圖按自然比例置中；
  (b) 喺開始畫面階段預解碼地圖圖（SwiftUI/UIImage 預載），唔好等入地圖先解。
