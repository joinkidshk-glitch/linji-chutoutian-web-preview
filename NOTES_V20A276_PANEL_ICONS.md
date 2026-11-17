# NOTES_V20A276 — 面板標題圖示放大加亮

## 1. 背景
- v275 將 4 個約會地點 emoji 換做手繪圖標（`EMOJI_ICON112` 對照，經 `iconHtml112()`）。
- 瀏覽器 2026-11-17 21:02 實機驗證：emoji 全清，4 個地點面板標題出晒手繪圖，但**圖示偏細偏暗——深啡墨線（#3a2e22）配深灰色標題底色，乍看較暗淡，要放大先易辨認**；山頂嗰隻喺細尺寸下只見山形，發射塔睇唔到。
- 用戶 2026-11-17 21:10 拍板：開票放大加亮面板圖示。
- 地圖本身從來冇圖示釘（早已移除改隱形熱區），呢票唔郁地圖。

## 2. 改前量度（現況）
| 位置 | 改前尺寸 | 背景 | 問題 |
|---|---|---|---|
| 地點面板標題 `#loc-title img.ic112` | 1.1em ≈ 20px（標題字 1.15rem） | 場景相（深淺不定；素底態米紙 #F2EBD8） | 深啡線落深色相上面對比度低 |
| 地圖列掣 `.map-area-list button img.ic112` | base 1.15em ≈ 13px（掣字 .72rem） | 深藍 rgba(20,36,56,.85)／深啡 rgba(40,28,12,.92) | 幾乎隱形 |
| 其餘 `.ic112` 用法（day-row／cat-tab／act-item／禮物等） | 1.15–1.4em | 淺底 | 無問題，唔郁 |

## 3. 改法
- **米紙圓底 chip（唔改圖標線稿本身）**：跟 v20a174 A1／v20a207 C2 同一解法——嗰陣深啡獎盃線稿喺深底隱形，加金底 chip 解決。呢次用米紙 `#f8f1de`（同 `.btnrow`／標題字同一暖紙色，夾遊戲暖紙質感；金色留返頒獎用）。
- `#loc-title img.ic112`：36px chip（`box-sizing:border-box`＋`padding:3px`，畫芯 30px，`border-radius:50%`，`vertical-align:-0.6em`）。改前 20px → 改後畫芯 30px（＋50%），加米紙底托。
- `.map-area-list button img.ic112`（新增規則，共用同一渲染位一併處理）：22px chip（`padding:2px`，畫芯 18px，`border-radius:50%`，`vertical-align:-0.6em`）。改前 13px → 改後畫芯 18px（＋38%），加米紙底托。
- 素底態（`locpanel118-nobg`，米紙實底）：chip 同底色接近，邊緣唔明顯，但圖標本身深線落米紙本來就睇得清，chip 無害，唔使例外。
- 其餘 `.ic112` 用法零改動。

## 4. 山頂圖處理（`assets/icons/icon_peak.png`）
- 問題：格仔塔線條喺 256px 得 2–3px 闊，縮到 20–30px 顯示嗰陣低過 1px，靠抗鋸齒先勉強見到；直接 3×3 膨脹會塞死格仔間隙，成座塔變實心黑 blob（試過，廢棄）；十字形膨脹一樣塞死。
- 最終做法（機械處理，唔係重畫）：逐行取塔區（x112–144，y48–142）深色像素嘅左右邊界，中間填實——外輪廓（塔腳＋天線＋橫桿）原封不動，只係格仔內籠填實，變實色剪影塔。月亮、兩粒星、山形、山上紋理全部唔郁。
- 塔區深色像素：910（v275 格仔）→ 1138（v276 實色）。
- 其餘 3 隻圖（wave／beach／plane）sha256 同 v275 一致，唔郁。
- **Cache-buster**：`iconHtml112()` 出嘅 `<img>` 由 `icon_<stem>.png` 改做 `icon_<stem>.png?v=20a276`——icon_peak.png 內容改咗，之前 icon URL 無 per-asset `?v=`（v275 已確認），舊玩家會繼續用緩存舊圖；跟 fullbody `?v=20a106` 同一做法。`tests/test_icons112_logic.js`＋`tests/test_icons275_logic.js` 期望字串同步改咗。

## 5. QC（Playwright 實渲染，390px 闊）
- 標題列（場景深底）：4 隻 chip 上面圖標全部一眼認得出——山頂見到山＋塔、波浪、沙灘傘、飛機；chip 同文字垂直置中。
- 素底態（米紙底）：chip 邊緣融入底色，圖標本身清晰。
- 地圖列掣（深藍掣＋深啡掣）：4 隻 chip 全部清晰可辨。
- 截圖：`/tmp/qc276_shot.png`（工作副本 QC 用，唔入 repo）。

## 6. 測試
- 新檔 `tests/test_icons276_logic.js`：**23 項 ALL PASS**（標題 chip 36px／米紙／圓底／border-box、列掣 chip 22px 同款、輸出帶 `?v=20a276`、peak 256×256 RGBA＋塔區 >1000 深色像素＋sha 釘死、其餘 3 隻 sha256 唔郁、base 1.15em＋day-row／cat-tab／act-item 規則唔郁）。
- `tests/test_icons112_logic.js`、`tests/test_icons275_logic.js`、`tests/test_icons112_static.py` 全部 ALL PASS（期望字串已同步 `?v=20a276`）。
- 兩個 script block `node --check` 通過。

## 7. 全套 suite
- **TOTAL PASS 341 FAIL 9**（v275 基線 340／9＋新檔 1 項），FAIL 九項同基線逐項一致（flash51／slot50／soft_tip_111_restore／start53／weave43_static／weave44_static／weave49_static／wf5_87／wrap38），零回歸。
- 中途第一跑 332／18：9 檔額外 FAIL 全部係 CSS 新規則嗰行（＋1 行）令釘行漂移，唔係內容錯——逐檔 resync（見 §7.1）後逐個重跑全過，第二跑即刻 341／9。
- `tests/test_icons276_logic.js` 23 項、`tests/test_icons112_logic.js`、`tests/test_icons275_logic.js`、`tests/test_icons112_static.py` 全部 ALL PASS；兩個 script block `node --check` 通過。

### 7.1 Resync（v276 ＋1 行漂移）
- 根源：新 `.map-area-list button img.ic112` 規則係多咗一行（舊 L4010 變兩行），index.html 總行數 45502→45503，之後所有釘行 ＋1。
- 用 `/tmp/resync276.py` 單次掃描 dict 查表（唔逐對 re.sub——kwan151 有 9472→9473→9474→9475／14425→14426→14427 兩條鏈，逐對會撞值）；註解入面嘅歷史映射一律唔郁（tokenize 攞 COMMENT span，只改 code 區）；每檔檔頭加 v276 resync 註解。
- 9 檔共 133 粒釘＋鏈尾：kwan151 25（line()）、rom159 7（line_has＋全佳行）、rom176 7（line()）、tang152 3（lines()[]）、text125 9（ls[]＋guard＋報錯字串行號）、gift185 3（總行數鏈尾＋斷言）、tang171 7（總行數鏈＋DEF 鏈）、tang173 18（總行數鏈＋DEF 鏈＋L4862→L4863＋註解平衡）、travel114 54（COUNT 12＋FREE 40＋DEF 40752→40753＋WRAPPER 28576→28577）。歷史標籤（ok() 名入面嘅 L25608 等）一律唔郁。
- 逐檔重跑全部 PASS 後，全套第二跑 341／9。resync 腳本本身係 /tmp 臨時檔，唔入 repo。

## 8. 落地記錄（統籌補）
- （待填）
