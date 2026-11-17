# NOTES_V20A277 — 山頂圖標重畫（支塔畫大）＋清走死 CSS

## 背景

- v276 標題圓片得咗（36px 米紙 chip，瀏覽器 21:32 驗過），但山頂圖喺面板尺寸下
  依然讀做「座山多過發射塔」。v276 填實本身做咗（parent 像素核實：塔區 1138
  深色像素、每行連續實心），問題係成隻圖入面支塔太細——256px 圖入面塔闊得
  32px，喺 30px 畫芯下得 ~2px 闊，睇落似天線。
- v276 同時做咗地圖列掣 22px chip，但嗰行掣自 v20a43 起已經
  `#app #map-area-list{ display:none !important; }`（用戶 2026-11-09 拍板刪走
  底部快捷列），係死 CSS——v276 統籌嘅 Playwright QC 係隔離渲染，唔係 live 狀態。
  今次 QC 一定要喺真實可見嘅 UI 處境做（36px 標題 chip、場景色底）。

## 1. 新塔幾何（`assets/icons/icon_peak.png`，PIL 機械繪製）

風格照舊：深啡墨線 #3a2e22、256×256 RGBA 透明底、塔身實色剪影。
幾何（PIL ImageDraw，見已刪嘅 `draw_peak277.py` 備份邏輯）：

| 部分 | 座標 | 尺寸 |
|---|---|---|
| 天線 | x124–132，y16–58 ＋兩條橫桿 x116–140（y26–30、y38–42） | 8px 闊 |
| 橫臂 | x40–216，y58–74 | 176px 闊（69% 畫面） |
| 主塔 | 梯形 (112,74)(144,74)(198,222)(58,222) | 底闊 140（55%）、高 148 |
| 塔總高 | y16–222 | 207px（81% 畫面） |
| 山丘 | 低丘輪廓線 [(14,234)(64,208)(128,198)(192,208)(242,234)]，3px 線 | 塔基裝飾 |
| 月亮 | 彎月，中心 (40,38) r17（橫臂 y58 之上，唔撞） | 點綴 |
| 星 | 兩個十字星 (220,30)、(238,64)（橫臂 x≤216 之外，唔撞） | 點綴 |

舊圖對比：v276 塔闊 32px／塔高 ~94px／塔區 1138 深色像素；
v277 塔闊 177px／塔高 207px／塔區（x40–216，y16–222）16,797 深色像素；
全圖不透明像素 5,211 → 17,538。

## 2. 縮放 QC（PIL，米紙 #f8f1de 底）

| 尺寸 | 深色像素 | 橫臂帶最闊連續段 | 塔底帶最闊連續段 | 目測 |
|---|---|---|---|---|
| 256px | 17,538／65,536（26.8%） | 177px | — | 發射塔清晰：橫臂＋天線＋實色梯形塔身、彎月、兩星 |
| 30px（標題 chip 畫芯） | 228／900（25.3%） | 20px | 16px | 一眼認得出係發射塔 |
| 24px | 138／576（24.0%） | 16px | 14px | 一眼認得出係發射塔 |

A/B 對照（36px 米紙圓 chip、場景色底）：左＝v276 舊圖（細天線＋空心山形，
讀做座山）；右＝v277 新圖（深色發射塔剪影，橫臂＋天線＋實色塔身）。
證據圖為臨時 QC 圖，未入 repo。

## 3. 死 CSS 刪除

- 刪 `index.html` L4011（刪前行號）`.map-area-list button img.ic112` 22px chip
  規則成行＋註解，改做一行 v277 註解說明刪除原因。
- 核實：全檔只得 L4011 一處用 `.map-area-list button img.ic112` 選擇器；
  其餘 `.map-area-list button` 規則（掣本身樣式）唔郁；`#app #map-area-list{
  display:none !important; }`（L4426）唔郁——刪規則唔等於恢復嗰行掣。
- `tests/test_icons276_logic.js` §2 同步改：由「釘死 22px chip 存在」改做
  「釘死規則已刪＋display:none 留喺度」。

## 4. Cache-buster

- `iconHtml112()` 出嘅 `<img>` 由 `?v=20a276` 升去 `?v=20a277`（L17790）。
- 三檔舊測試期望字串同步改：`test_icons112_logic.js`、
  `test_icons275_logic.js`、`test_icons276_logic.js`。

## 5. 測試

- 新檔 `tests/test_icons277_logic.js`（19 項，純 Node 解 PNG＋box-downsample，
  唔靠 PIL）：新塔幾何（塔闊 ≥128、塔高 ≥154、塔區深色像素 >12000）、
  30px／24px 縮放可讀（深色格數、橫臂帶／塔底帶最闊連續段）、死 CSS 已刪、
  display:none 留喺度、?v=20a277、其餘 3 隻圖 sha256 唔郁。
- `test_icons276_logic.js` §4 同步：peak sha 改 v277（`945fe0c9…13cc84`）、
  塔區閾值 >2000（實測 2895）。
- 其餘 3 隻圖 sha256 同 v275 一致，唔郁（wave／beach／plane）。
- 兩個 script block `node --check` 通過。

## 6. Suite／落地

- 全套 suite：見 §8 落地記錄。
- SAVE key／softRev／`?v=20a10` 無改動。無改 `~/MEMORY.md`。

## 7. 檔

- 改：`assets/icons/icon_peak.png`（重畫）、`index.html`（刪 1 行死 CSS、
  cache-buster 升）、`tests/test_icons112_logic.js`、`tests/test_icons275_logic.js`、
  `tests/test_icons276_logic.js`（期望同步）。
- 新：`tests/test_icons277_logic.js`、`NOTES_V20A277_PEAK_ICON.md`。
- 刪：`draw_peak277.py`（繪圖腳本，用完即刪，幾何已記喺 §1）。

## 8. 落地記錄（統籌補）

- 新 main HEAD `3adf5cf`（squash merge v277，base `9772022`，合併期間 main 無郁過，
  無 rebase）；GitHub `ls-remote` 一致，已推 main；工作副本 `linji-work277` 已刪；
  分支 `v20a277` 留喺常駐 clone 做紀錄。
- 全套 suite（工作副本獨立重跑）：**TOTAL PASS 342 FAIL 9**（基線 341／9＋新檔 1 項），
  FAIL 九項同基線逐項一致（flash51／slot50／soft_tip_111_restore／start53／
  weave43_static／weave44_static／weave49_static／wf5_87／wrap38），零回歸。
- Pages：推 main 後等傳播約 4 分鐘，curl 核實主頁 HTTP 200、字節數／sha256 同本地
  逐字節一致；`assets/icons/icon_peak.png?v=20a277` HTTP 200、sha256 同本地一致
  （v277 重畫版）。
- QC 教訓：v276 統籌隔離渲染隱藏元素話得；今次 A/B 對照喺 36px 米紙圓 chip＋
  場景色底做（真實可見嘅標題處境），舊圖讀做座山、新圖一眼認得出係發射塔。
