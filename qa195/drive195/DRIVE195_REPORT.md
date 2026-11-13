# v195 實駕報告 — 阿偉造型最高紀錄（B 方案）跨年驗證

- 工作副本：`~/workspace/linji-work195/`（分支 `v20a195`，rebase 上 main `b104f85`；index.html sha `369e4c96fccb`）
- 對照 pristine：`~/workspace/pristine195-b104f85`（detached HEAD `b104f85`，index.html sha `df05fdd3740c`，`playerTierMax`／`enc195` 出現 0 次，`awi_s2_angry`／`awi_s3_angry` 欠奉；跑完留低，冇刪除）
- 實駕：Playwright venv `/home/hatch/pwenv49/bin/python`＋`chrome-headless-shell`；工作版 port 8985、pristine 版 port 8986；LIVE 模式（唔加 `?softPreview=1`）
- 頭像證據以 DOM 層為準（`.dlg106-char` img src、`#home-awi` src）；headless_shell 截圖有 stale frame 殘影，只做輔助
- **結果：23 個 run 全部 PASS；0 pageerror、0 http fail**
- 腳本：`drive195.py`（probe／模板攞取：`probe195.py`）；逐 run 詳細數據：`drive195_report.json`；截圖：`shots/`（共 39 張，含 probe 1 張）

## 播種方法（逐 case 相同，真載入路徑）

1. 先經 UI 開新局＋`saveQ()` 攞一個真存檔做模板（`save_template.json`，day 0、fame 5；模板本身已有 `flags.playerTierMax: 0`）。
2. 每 case 將模板改寫（`dayIndex`／`fame`／`done_*` 完成旗／`playerTierMax`／`story.done={C1..C5:true}`／`lastMainDoneDay=day-8`），寫入 localStorage slot 1（key `starVolunteer_map_v19w`），reload 後撳 `#btn-cont`「繼續」讀檔——即係行真載入路徑（`normalizeSaveObj` → backfill），唔係 in-page 改 `S`。
3. 對話觸發：沿用調查員方法（開金龍茶餐廳 sheet 再閂 → 強制主線播出）；播唔出嗰陣 fallback `StoryPlay.start('C6', {force:true})`，下表有註明邊個 case 用咗 fallback。播出嘅係 C6（何生事務所／茶餐廳場口），逐句讀 DOM `src`，每 case 播最多 12 句。

**注意（量度如實記錄）：**
- 載入後 `dayIndex` 會＋1（seed 300 → 301；seed 400 → 401；應係 Continue 嗰陣晨早推進一日）。年份唔變（A／D300 的 `gigsYear` 仍係 1990；B／C／D400／E 係 1991），不影響跨年判斷。
- `enc79PlayerTier()` 唔係 global（IIFE 內部函數），in-page 讀唔到 live tier（報告 JSON 記為 `liveTier: null`）。判斷用 `DLG106.aweiStem()`＋對話逐句 `src`＋`gigsYear`，已經足夠；live tier 跌唔跌本身係邏輯測試已覆蓋嘅範圍。
- 1990 真男主角：`gig_1988_film_05`（另 D 用首 3 部：`film_05`／`film_06`／`film_07`）；1991 真男主角：`gig_1989_tv_10`（1991 年庫得 2 部，另一部係 `gig_1989_film_09`）。`gig_1988_tv_06` 等假男主角冇用過。

## 逐 case 結果

| case | viewport | seed（day／fame／flags） | 載入後 `playerTierMax`／stem | 對話阿偉 `src`（逐句 tier） |  verdict |
|---|---|---|---|---|---|
| A（基線） | 932 | 300／30／`done_gig_1988_film_05`＋ptm 2 | ptm 2／`awi_s2`（gigsYear 1990） | 2 句，tier [2, 2]，`awi_s2_base.webp` | **PASS** |
| A（基線） | 700 | 同上 | ptm 2／`awi_s2` | 2 句，tier [2, 2] | **PASS** |
| **B（核心修復）** | 932 | 400／30／`done_gig_1988_film_05`＋ptm 2 | ptm 2／`awi_s2`（gigsYear 1991） | 3 句，tier [2, 2, 2]，`awi_s2_base.webp`，零 `awi_base.webp` | **PASS** |
| **B（核心修復）** | 700 | 同上 | ptm 2／`awi_s2` | 3 句，tier [2, 2, 2] | **PASS** |
| B 附加：懶回填 | 932＋700 | 同 B 頁內：`delete S.flags.playerTierMax` 後再讀 stem | stem 照係 `awi_s2`，`playerTierMax` 讀完寫返 2 | — | **PASS** |
| C（對照） | 932 | 400／30／`done_gig_1989_tv_10`＋ptm 2 | ptm 2／`awi_s2`（gigsYear 1991） | 3 句，tier [2, 2, 2] | **PASS** |
| C（對照） | 700 | 同上 | ptm 2／`awi_s2` | 3 句，tier [2, 2, 2] | **PASS** |
| D（tier 3 跨年）day 300 | 932 | 300／70／3 部 1990 lead＋ptm 3 | ptm 3／`awi_s3`（gigsYear 1990） | 2 句，tier [3, 3]，`awi_s3_base.webp` | **PASS** |
| D（tier 3 跨年）day 300 | 700 | 同上 | ptm 3／`awi_s3` | 2 句，tier [3, 3] | **PASS** |
| D（tier 3 跨年）day 400 | 932 | 400／70／3 部 1990 lead＋ptm 3 | ptm 3／`awi_s3`（gigsYear 1991） | 3 句，tier [3, 3, 3] | **PASS** |
| D（tier 3 跨年）day 400 | 700 | 同上 | ptm 3／`awi_s3` | 3 句，tier [3, 3, 3] | **PASS** |
| **E（舊檔 backfill）** | 932 | 400／30／`done_gig_1988_film_05`、**冇 `playerTierMax` 呢支旗** | 載入後 ptm **2**（backfill 寫入咗，`ptmPresent` 載入前 false → 之後 true）／`awi_s2` | 3 句，tier [2, 2, 2] | **PASS** |
| **E（舊檔 backfill）** | 700 | 同上 | 載入後 ptm **2**／`awi_s2` | 3 句，tier [2, 2, 2] | **PASS** |
| F2（angry 新圖，tier 2） | 932 | B 頁（day 401、ptm 2） | `candidates('awi','angry')[0]`＝`awi_s2_angry.webp` | 見 F 節 | **PASS** |
| F2（angry 新圖，tier 2） | 700 | B 頁 | 同上 | 見 F 節 | **PASS** |
| F3（angry 新圖，tier 3） | 932 | D400 頁（day 401、ptm 3） | `candidates('awi','angry')[0]`＝`awi_s3_angry.webp` | 見 F 節 | **PASS** |
| F3（angry 新圖，tier 3） | 700 | D400 頁 | 同上 | 見 F 節 | **PASS** |
| G2（屋企 bust，tier 2） | 932 | B 頁 | `#home-awi` src 完全等於 `BUST109_EXTRA.awi_s2` 首 140 字元（見 G 節） | 目視淺灰西裝（`G2_932_home.png`） | **PASS** |
| G2（屋企 bust，tier 2） | 700 | B 頁 | 同上（`awi_s2`） | 目視淺灰西裝 | **PASS** |
| G3（屋企 bust，tier 3） | 932 | D400 頁 | `#home-awi` src 完全等於 `BUST109_EXTRA.awi_s3` 首 140 字元 | 目視深藍西裝（`G3_932_home.png`） | **PASS** |
| G3（屋企 bust，tier 3） | 700 | D400 頁 | 同上（`awi_s3`） | 目視深藍西裝 | **PASS** |
| H-B（pristine 對照） | 932 | 400／30／`done_gig_1988_film_05`（pristine 冇 ptm） | ptm 不存在／`awi`（gigsYear 1991） | 3 句，tier [1, 1, 1]，`awi_base.webp`（深藍 bomber 臨記樣） | **PASS**（bug 重現） |
| H-B（pristine 對照） | 700 | 同上 | ptm 不存在／`awi` | 3 句，tier [1, 1, 1] | **PASS**（bug 重現） |
| H-D（pristine 對照） | 932 | 400／70／3 部 1990 lead（pristine 冇 ptm） | ptm 不存在／`awi`（gigsYear 1991） | 3 句，tier [1, 1, 1]，`awi_base.webp` | **PASS**（bug 重現） |

觸發方式：B／C／D400／E／H 全部用茶餐廳 trigger；A／D300 兩頁茶餐廳 trigger 播唔出故事，行咗 fallback `StoryPlay.start('C6', {force:true})`（播出嘅同樣係 C6 實體內容，證據效力相同；點解嗰兩頁 trigger 唔到未深究，估計同 Continue 後已有其他待播事件有關——唔影響 verdict）。

## F — angry 新圖實駕（方法講明）

**搵唔到現成阿偉 angry 對白。** 試過嘅路徑：全庫 grep `index.html` 入面 25 句 `speakerId:"player"` 阿偉對白＋3 句 `"speaker": "阿偉"` beats，對照 `DLG106_KW.angry` 關鍵字（夠啦／黐線／唔准／滾／廢話…）——0 句命中。所以 F 唔係播現成對白，而係**經對話引擎指定表情**（任務容許嘅第二種方法）：

`StoryPlay.start({id:'T195_ANGRY', beats:[{何生一句}, {speaker:'阿偉', speakerId:'player', emotion:'angry', lines:['夠啦！呢場戲唔係咁拍㗎！']}]}, {force:true})`

- `emotion:"angry"` 欄＋對白含「夠啦」：`DLG106.resolveCategory()` 實測回 `angry`（兩條路徑一致，唔係淨靠 emotion 欄）。
- 講者句（阿偉）：DOM `.dlg106-char[data-dlg-id="awi"]` src＝`assets/story/fullbody/awi_s2_angry.webp?v=20a106`（F2）／`awi_s3_angry.webp?v=20a106`（F3），`complete: true`，`naturalWidth: 880`；HTTP 200 四次齊晒（932＋700 各一；見 `drive195_report.json` 的 `angry_http`）。
- 目視：`F2_932_angry.png` 阿偉企左、淺灰西裝、眉頭皺起嬲樣，對白框「阿偉：夠啦！呢場戲唔係咁拍㗎！」，何生右邊聽者變暗；兩張新圖開首已目視核對（s2 淺灰西裝嬲樣、s3 深藍西裝嬲樣）。
- 附帶對比：pristine 的 `candidates('awi','angry')[0]` 係 `awi_angry.webp`（s1 鏈），工作版係 `awi_s2/s3_angry.webp`——證明新圖真係接入咗候補鏈首選，唔係跌返 s1。

## G — 屋企 bust 補驗（UI 路徑行唔通，如實記錄）

**試過嘅 UI 路徑（全部記錄喺 `drive195_report.json` 各 G run 的 `attempts`）：**
1. 地圖畫面 dump 全部可見掣：15 個地點＋「過一日」＋「進度」＋「☰」，**冇「屋企」／「返屋企」／「回家」掣**（同調查報告「返屋企掣撳唔到」一致）。
2. 撳「進度」掣 → 開咗手帳（tabs：行程／事業／近況／消息／人情／進度），入面**冇「回顧手帳」／「屋企」掣**。
3. 最後用 fallback：直接 call `enterHome(null, false)`——同 UI 掣 call 嘅同一個函數（例如 L28052 的「進度」掣就係咁 call 法），`#v-home` 顯示、`#home-awi` 渲染。

**判定方法（ drive 當刻判錯，事後覆核修正——原因講明）：** `bust109HeroSrc()` 回嘅唔係檔路徑，而係內嵌 data URI（`BUST109_EXTRA[stem]`／`PORTRAITS.hero_awi`），所以 drive 腳本原先「src 入面有冇 `s2`」嘅判準必然 FAIL。事後覆核：將所存 `#home-awi` src 首 140 字元逐字對 `index.html` 內三個候選——G2 完全等於 `BUST109_EXTRA.awi_s2`、G3 完全等於 `BUST109_EXTRA.awi_s3`、兩者都唔等於 s1 的 `PORTRAITS.hero_awi`；`complete: true`、`naturalWidth: 240`、`homeVisible: true`；截圖目視 G2 頭像淺灰西裝、G3 頭像深藍西裝。**G2／G3 四個 run 改判 PASS**（`drive195_report.json` 已更新，附 `verificationNote`＋`dataUriMatch`）。

## pageerror／http fail

- **pageerror：0**（23 個 run，兩個 viewport，工作版＋pristine）
- **HTTP ≥400：0**
- 另有記錄：`awi_s2_angry.webp`／`awi_s3_angry.webp` 各兩次 HTTP 200（932＋700）

## 存檔種子（逐 case，見上表；完整版喺 JSON 每 run 的 `seed`＋`postLoad`）

- A：day 300、fame 30、`done_gig_1988_film_05: 1`、`playerTierMax: 2`
- B：day 400、fame 30、`done_gig_1988_film_05: 1`、`playerTierMax: 2`
- C：day 400、fame 30、`done_gig_1989_tv_10: 1`、`playerTierMax: 2`
- D：day 300／400、fame 70、`done_gig_1988_film_05／film_06／film_07: 1`、`playerTierMax: 3`
- E：day 400、fame 30、`done_gig_1988_film_05: 1`、**冇 `playerTierMax`**
- F2／G2：沿用 B 頁存檔；F3／G3：沿用 D400 頁存檔
- H（pristine）：B／D 嗰兩個 seed，唔寫 `playerTierMax`（pristine 根本冇呢個機制）

## 殘留／跟進建議（唔影響 verdict）

1. 地圖入屋企冇正常 UI 路徑（G 節）：玩家層面「返屋企」係咪應該有掣，係產品問題，唔係 v195 回歸——但值得另開一票（調查報告已提過同一點）。
2. A／D300 嗰兩頁茶餐廳 trigger 播唔出故事，要 fallback `StoryPlay.start('C6')`——原因未查，可能同 Continue 後待播事件疊加有關；唔影響今次證據，但 trigger 穩定性值得留意。
3. 現成內容入面冇一句阿偉 angry 對白（F 節）：`awi_s2/s3_angry.webp` 兩張圖已接入候補鏈，但要等將來有阿偉嬲嘅劇情先會喺自然遊玩入面出現。
4. 載入後 `dayIndex`＋1（300→301、400→401）：年份唔變，今次無影響；如果將來有測試要逐日對齊，要留意 Continue 會推進一日。
