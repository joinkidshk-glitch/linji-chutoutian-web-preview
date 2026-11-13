# v20a190：修 v187 設計 review 新 C1（glamour panel 上半留空）

- **分支**：`v20a190`；**基底**：main `dcf1b72`（v187 NOTES；遊戲 `fe09b67`）。開工核實 main HEAD 仍係 `dcf1b72`，v188／v189 未落地，唔使 rebase。
- **任務書**：v187 review §4 新 C1；用戶 2026-11-13 19:40 拍板「修：海報置中返少少／panel 縮短」。
- **範圍**：只郁頒獎禮 glamour 兩行 CSS＋測試；唔落地（唔做 squash merge、唔 push main、唔做設計 review）。

## §1 改咗咩（index.html，2 行）

| 行 | 舊 | 新 |
|---|---|---|
| 808 `.awd63-glamour` | `align-items:stretch` | `align-items:flex-end;container-type:size` |
| 810 `.awd63-glamour-panel>img` | `max-height:40%` | `max-height:calc(40cqh - 8px)` |

- **效果**：panel 高由全高 570／504px 改做內容高（932：306.9px；700：280.5px），貼住 overlay 底；海報＋caption 位置完全唔郁。Panel 本身全高暗底係 v166 設計，今次先至縮短（review 建議兩個方向一齊做：置中返少少＋panel 縮短——縮短之後海報已經貼住 panel 頂（只剩 10px padding），唔使再加置中）。
- **其餘唔郁**：panel 闊 44%、0.93 暗底、column、flex-end、gap 8、padding 10/12；img max-width 88%、金框、光暈；overlay absolute／aspect 480/360／pointer-events:none；cap 19px／1.55。

### 點解唔係淨改 flex-end／唔係 40cqh——探針證實嘅機制

開工先用隔離 CSS 探針（`qa190/probe190_css.py`，760／672px overlay＋真海報 data URI，decode 後量度）搞清舊 cap 點計，唔係估：

1. **舊 cap 實際值**：全域 `*{box-sizing:border-box}`（L57）之下，`max-height:40%` 對住 panel **內容高**（570−20 padding＝550）解，border-box cap＝220（932）／193.6（700），唔係 40%×570＝228。探針 A 組重現 live 幾何逐 px（img 220 高、空 273.1）。
2. **淨改 flex-end 會出事**：panel 一縮做內容高，`40%` 對住不定高失效，海報脹到 **284.8 高、闊 273.1**（探針 B 組），頂會撞返白牌——v187 C1 fix 倒退。所以唔可以直接留 40%。
3. **裸 40cqh 亦唔啱**：40cqh＝40%×overlay 高＝228，高咗 8px，932 clearance 會由 36 跌到 28（探針 C 組）。
4. **正確式係 `calc(40cqh - 8px)`**：40cqh＝舊 40%×overlay 高；−8px＝扣返 panel 上下 padding 各 10px 嘅 40%（0.4×20）。overlay 加 `container-type:size` 令 cqh 以 overlay 高計（唔係 viewport）。探針 G 組：932 img 220.0／700 img 193.6，同舊 cap 逐 px 等價；panel 306.9／280.5；空 10px。

## §2 新舊數字對照（實駕量度，glamour beat）

| 項目 | v187（舊） | v190（新） |
|---|---|---|
| 932 panel | 123–693（高 570） | **386–693（高 307）** |
| 932 海報 img | 396–616（220 高） | **396–616（唔郁）** |
| 932 panel 頂→海報頂空位 | 273px＝**47.9%** | **10px＝3.3%** |
| 932 海報頂離牌底 | 36px | **36px（唔跌，下限）** |
| 932 海報底→panel 底 | 77px | **77px（唔郁）** |
| 700 panel | 156–660（高 504） | **380–660（高 280）** |
| 700 海報 img | 390–583（193.6 高） | **390–583（唔郁）** |
| 700 panel 頂→海報頂空位 | 234px＝**46.3%** | **10px＝3.6%** |
| 700 海報頂離牌底 | 24px | **24px（唔跌，下限）** |
| 700 海報底→panel 底 | 77px | **77px（唔郁）** |
| 海報 vs 白牌重疊 | False（overlapY 0） | **False（overlapY 0；overlapX 121／107 唔郁，縱向完全避開）** |
| img computed max-height | `40%` | **`220px`（932）／`193.6px`（700）** |
| overlay align-items | stretch | **flex-end** |

- 目測（`qa190/shots190/932_won_glamour.png`、`700_won_glamour.png`）：白牌完整、海報女人面完整、兩者分開；panel 而家係右下角貼住海報＋caption 嘅暗卡，上面係舞台幕布＋燕尾服阿偉，構圖平衡。字安全（caption 兩行齊全）。
- 其餘 beats 唔變：names／walkup／reveal／comfort／out 幾何同 v187 一致（見 §4）。

## §3 測試

### 新測試（65 項斷言）

- `tests/test_awards190_logic.js`（32 項）＋`tests/test_awards190_static.py`（33 項）：新 C1 機制三項（flex-end／container-type:size／calc(40cqh - 8px)，舊 40%／裸 40cqh 唔准出現）＋逐 px 計數（932／700 cap、img 頂、clearance、空佔比、底罅、海報盒、高身海報 guard）＋六項守衛＋流程／版本守衛。工作副本行：**全部 PASS**。
- **反證**：兩檔對 pristine main `dcf1b72`（`~/workspace/linji-repo/index.html`）行 → **新 C1 機制 3 項乾淨 FAIL，守衛全 PASS，exit 1，唔 crash**。（計數斷言係純算術，pristine 都 PASS——同 v187 寫法一樣；機制斷言先係判別項。）
- **舊測試更新**（v187 改 v181 嗰陣同一慣例：修法令舊斷言過時就一併更新，唔係靜靜刪）：`test_awards166_static.py`、`test_awards168_static.py`、`test_awards187_logic.js`、`test_awards187_static.py` 四檔釘住 `max-height:40%` 嗰句改做 `calc(40cqh - 8px)`；v187「panel 全高暗底」嗰句改名（條件不變：44%＋暗底）。四檔工作副本行全部 PASS。

### 全套 A/B（`qa131/run_suite.sh`）

- 乾淨基線（linji-repo `dcf1b72`，未改）：**255 PASS／12 FAIL**。
- 工作副本（v190）：**257 PASS／12 FAIL**——多 2 PASS 係新測兩檔，12 FAIL 清單同基線逐檔相同（`test_flash51／test_giglib36／test_pacing35／test_poster59／test_rumor49／test_slot50／test_soft_tip_111_restore／test_start53／test_weave43／test_weave44／test_weave49／test_wrap38`，全部 pre-existing）。**零回歸**。
- 註：suite 數字會波動（見 AGENTS.md v151 教訓），今次以 FAIL 清單相同＋相關測試逐個覆驗為準，唔係齋信總數。

### 實駕（`qa190/drive190.py`，port 8977，本地鏡像＋http.server；LIVE 模式）

- **6/6 播完，0 pageerror、0 http fail**（932／700 × won／nominated／gallery；真實 UI 路徑：新局→C1→morning chain→請柬→出席／推辭→典禮全程）。
- 黃字 fix 三項 36/36 全 True（sub 喺牌內／sub 底高過人頭頂／牌底唔過 glyph 頂）。
- 報告：`qa190/drive190_report.json`；截圖 22 張 `qa190/shots190/`；基線單場（改 code 前 932_won）`qa190/drive190_report_932_won.json`——基線同 v187 review 數字逐項吻合（panel 123–693、img 396–616、空 273、clearance 36）。

## §4 六項守衛覆核（實駕＋測試）

| 項 | v190 實測 | 結果 |
|---|---|---|
| B1 地板帶 | 228.0–310.0、深 82.0；人物高 89.0–89.8；地板／人物 0.91–0.92；腳底以下／人物 0.53–0.54（6 場一致） | ✓ 唔郁 |
| C2 卡罅 | [24, 24, 24]、角標 clearance 10、卡列總闊 424（兩個 viewport 一致） | ✓ 唔郁 |
| C3 out 留人 | out 對比 won 224.5／129.4（兩 viewport 取樣瞬間唔同）、nominated 221.9、gallery 214.2–216.0，對照空台 17.7——全部 >> 空台 | ✓ 唔郁 |
| C4 walkup 前層 | 700 最暗腳區 x0＝60、delta 32.0；932 x0＝50、delta 32.0（見 §5 註） | ✓ 唔郁 |
| C5 下移 124px | glamour frameTop 123 vs −1（932）、156 vs 32（700），shift 124px；glamour-hide display:none 唔郁 | ✓ keep |
| C6 glyph 罅 | glyphGap 5px（932）／4px（700） | ✓ 唔郁 |

- 唔郁：fellows 池／對手加權／贏線 0.875／報紙流程／6 beats 順序（得獎全長 13350ms；walkup 2200／glamour 1800／comfort 2600ms）；SAVE key／softRev `s107`／`?v=20a10` 唔郁；唔直改 content pack JSON。

## §5 殘留／觀察

1. **C4 932 最暗腳區 x0＝50（v187 係 60）**：取樣抖動，唔係回歸——walkup_mid 係 caption 錨定＋100ms poll 捉中段，幀位差少少，最暗 30px 區由 60–90 移到 50–80；delta 32.0 同 v187 嘅 32.5 基本一致，700 嗰場仍係 x0＝60。walkup code 零改動。
2. **700 clearance 剛好 24.0**：貼住 v187 實測下限，唔係新風險——海報盒同 v187 逐 px 相同（390–583），24 本來就係 v187 量到嘅數。將來換海報／改 cap 高先要重驗。
3. **高身海報（0.5 比例，4 張 POSTER59）只做計數 guard，未實駕**：新 cap 下闊＝(220−8)×0.5＝106px，細過 max-width，唔會脹；但未有以高身海報做 repGig 嘅實駕場次。將來有需要可加一場。
4. **`container-type:size` 係新引入嘅 CSS 機制**：Chrome 105+／Safari 16+ 先支援 cqh；overlay 尺寸嚟自 width＋aspect-ratio（唔靠內容），size containment 唔影響佢（探針＋實駕核實）。若將來 panel padding 上下唔再係 10px，`calc(40cqh - 8px)` 嘅 −8px（＝0.4×20）要跟住改——註解已寫明。
5. **panel 縮短後，panel 頂上面嗰截露出舞台幕布**（深色，唔係空暗底）：目測自然，係預期效果——左邊本來已經透明，依家右上都見到舞台，唔再係一大幅實色暗 panel。
6. **主畫面未抽查**：今次只郁頒獎禮兩行 CSS，主畫面無損；v187 review 已抽查過，今票唔重做。

## §6 檔案

- 改動：`index.html`（2 行）、`tests/test_awards190_logic.js`（新）、`tests/test_awards190_static.py`（新）、`tests/test_awards166_static.py`、`tests/test_awards168_static.py`、`tests/test_awards187_logic.js`、`tests/test_awards187_static.py`（四檔跟住更新）。
- 實駕：`qa190/drive190.py`、`qa190/drive190_report.json`、`qa190/drive190_report_932_won.json`（改前基線）、`qa190/probe190_css.py`（機制探針）、`qa190/shots190/`（22 張）、`qa190/suite190_pristine.txt`（混合時段跑，見註）、`qa190/suite190_work.txt`。
- 註：`suite190_pristine.txt` 係工作副本跑嗰陣同我改 code 撞咗時段（89 秒內），嚴格講唔係乾淨基線；乾淨基線已喺 linji-repo `dcf1b72` 重跑（`/tmp/suite190_pristine_repo.txt`，255／12，FAIL 清單同 work 版逐檔相同）。`suite190_pristine.txt` 留檔只作參考。
