# NOTES_V20A153 — v136 設計 review A1＋B2＋B3 修復

- 分支：`v20a153`（基底 main `e08a070`，即 v148；工作副本 `~/workspace/linji-work153/`）
- 範圍：A1 C17 入口分裂、B2 C17 開場空走廊、B3 進度頁幕次序亂。B1 推辭報紙唔講賽果唔郁（v149 範圍）。
- 狀態：已 commit，未 push、未落地（落地由統籌做）。

## A1 — C17 入口分裂（最重要）

**根源**：C17 嘅 `locIdAny: ["agency_ho","cafe_cha"]` 同 `locId: "agency_ho"` 嚟自 content pack `STUB_STORY_BEATS_FREEPLAY_SLOTS_v1.json` 嘅 C17 slot，經 `BehaviorGate.applyFreeplaySlots` 接入軟閘。故事節點本身（410 override `STORY_SPINE_NODE_C17_410`，locId `tvb_longmen`）同 `STORY_LOC_SOFT` C17（`tvb_longmen`）一早已經啱——**只有軟預覽路徑分裂，live（flag-off）路徑本身冇錯**。實駕行 `?softPreview=1`，所以測嘅係軟路徑。

**修法（跟文案＋STORY_LOC_SOFT＋410 locId，改返 `tvb_longmen`；一個 canonical 門＋進度頁「播呢幕」做後備，事務所／茶餐廳兩度門唔留）**：

1. `BehaviorGate.healC17Loc(node)`（`index.html` L25097，貼住舊嘅 `healC1Loc`）：id 係 C17 就將 `byId.C17.locId` 設 `tvb_longmen`、`trigger.locIdAny` 設 `["tvb_longmen"]`、slot beats 入面嘅 `locId` agency_ho／cafe_cha 正規化做 tvb_longmen。5 個 call 位，同 C1 鏡像：`loadStub_nodes_trigger`（L25073，stub 得 C1–C5 嗰陣 no-op）、`applyFreeplaySlots`（L25173，真正 choke point）、`evalTrigger_AND_softRumor`（L25525）、`softLockPlayerLine`（L25756）、`progressToward`（L25869）。
2. 全局 `softCanonC17Loc(node)`（L44479，貼住 `softCanonC1Face`）：強制 `locId = "tvb_longmen"`；只喺 trigger object 存在嗰陣先郁 `trigger.locIdAny`（410 node 冇 trigger，唔可以無端端生一個出嚟）；正規化 beat locIds。由 `applyFreeplaySlotsToSoftGate` 嘅 overlay loop 入面新加嘅 `if(id==="C17")` 分支叫（L44594，唔似 C1 分支咁抄 `slot.locId`）。
3. 進度頁 C17 行「你而家喺何生事務所，可以即刻播呢幕」唔使人手改——`prog71LocName` 讀 `storyNodeLocId`，路由修好之後自動變電視台（實駕證實行文係「你而家喺星河電視台，可以即刻播呢幕。」）。

**巧遇排隊——唔使新寫排隊機制**：`enc79TryIntercept` 本來已經有 `if(enc79StoryPendingAt(loc)) return false;`（「主線待播優先」，L52373）。之前喺電視台失效，係因為 `storyNodeLocId(C17)` 返 `agency_ho`；路由修好之後，C17 待播嗰陣電視台入場唔會彈巧遇，C17 卡排第一，唔使開進度頁。實駕 12-05 當日：工作版入電視台零 overlay、C17 第一張卡；pristine 同日同 seed 入電視台即彈「巧遇 · 齊鎮海」overlay（見下面實駕 A/B）。

**WF4 守門（範圍判斷，請統籌覆核）**：`wf4TryLocEvent` 本來完全冇主線待播守門——reviewer 第三次入電視台就係俾 WF4 食咗。呢度加返同一條規則（L40740，一行，`typeof` guard，`locTries` 遞增之前 return，唔會嘥咗當日入場額度）：

```js
try{ if(typeof enc79StoryPendingAt==="function" && enc79StoryPendingAt(locId)) return false; }catch(_w4sp){}
```

判斷：呢個唔係新功能，係將 A1「唔好食咗個入場」嘅要求補埋最後一隻漏網入口；規則同 enc79 嗰條逐字一樣，唔會改 WF4 其他行為。如果統籌認為要另開票，先拎走呢 1 行都唔影響其餘 A1 修復（新測試有獨立斷言，拎走會令該項 FAIL，唔會靜默通過）。

**冇郁**：content pack JSON 零改動（slots JSON 源頭 C17 仲係 agency_ho／`["agency_ho","cafe_cha"]`，修復喺 code 層；新測試有斷言釘死呢點，防日後有人「順手」改 pack 又改 code 兩頭唔對）。SAVE key／softRev／產品 `?v=` 零郁。

## B2 — C17 開場兩句係空走廊（何生由第一句就企台）

**做法**：`StoryPlay.spDlgPairIds(cur)`（L27864）加開場旁白 look-ahead——pair 係空（開場旁白 beats，之前非系統講者一個都未出現）嗰陣，向前望搵第一個非系統 beat 嘅講者，經 `dlg119DedupePair([nid])` 返**單人**（唔 preview 後面其他講者）。C17 beat 0／1 係系統旁白，beat 2 先係何生對白，所以開場兩句舞台得何生一個，暗態 0.6（`render()` 旁白模式 `activeId` 係 null，人物行聽者暗態——同 v20a128 D-1 規則一致，唔使特別處理）。

**點解揀呢個做法，唔係其他**：
- 唔改文案、唔補新場景圖（已拍板）。
- 唔喺節點數據加一個「開場何生」beat——會改數據語義，之後任何系統開場都要人手補。
- 唔用 v20a128 D-1 嘅阿偉補位規則：D-1 只適用非系統 beats；C17 呢度係系統開場，而且 410 尾段已經有阿偉 player beats，補阿偉會令開場變雙人，唔係想要嘅「何生企台」。
- 只 look-ahead 一個講者：開場畫面唔會劇透後面出場人物（例如老場務、張子駿）。

**410 真結構**（實測＋源碼雙重確認）：beat 0 系統×2 句（L0「1992 年冬末，星河電視台頒獎禮後台。化妝鏡一排燈泡熱到出煙……」）、beat 1 系統×2 句、beat 2 何生對白（「阿偉，坐陣。今晚之後……」）、beat 3 何生、beat 4 老場務、beat 5 張子駿、beat 6 系統、beat 7–8 阿偉、beat 9 系統。實駕逐行行到 beat 2：何生光態 `brightness(1)`，阿偉聽者暗態 0.6，兩人同台。

## B3 — 進度頁幕次序亂

- `order71`（L44076）排返 1–20：`[["C1",1]…["C17",17],["C18",18],["C19",19],["C6F",20]]`。
- detail 資格由行號改做幕號（L44115–44118，`lastDetailN71`，`lastDetailN71 >= (r.n|0) - 1`）：保留 v20a80 原意（inserts C18／C19／C6F 喺上一幕 detailed 嗰陣逐項出），唔係嘅話搬去尾三個之後永遠唔會入 detail 範圍。
- 遠幕合併行守門（L44177，`if(!farNs.length) return;`）：主線 1–17 全部 done／open、淨低鎖住嘅 inserts 嗰陣，唔再印倒轉區間（舊碼會印「第 18–17 幕」／「第 20–17 幕」）。
- 實駕 seed 態（C1–C16 done、C17＋C18 open、C19／C6F 鎖住唔出 row）：進度頁見第 1–18 幕，C17 行喺 C18 之前，有「播呢幕」掣。

## 1990 年份陷阱：冇郁

`STORY_SPINE_NODE_C17_410` 源字串（`when: "1990冬"`、setting／synopsis／lockedHint 入面嘅 1990）**一個字都冇改**。新測試逐項斷言源頭仲係 1990；實駕首句顯示「1992 年冬末，星河電視台頒獎禮後台。」——year-walk 正常運作。郁源頭會令畫面變 1994，呢個陷阱冇踩。

## 測試

### 新測試 `tests/test_c17route153_static.py`（23 項，內容匹配、唔寫死行號）

- 工作版：**23/23 PASS**。
- 對 pristine main `e08a070`：**15 項新斷言乾淨 FAIL（exit 1，唔 crash）**，8 項基線 PASS。反證成立。
- 覆蓋：基線（SAVE／softRev／`?v=` 不變；410 陷阱未郁；410 locId＋`STORY_LOC_SOFT` C17 仲係 tvb_longmen；slots JSON 源頭仲係 agency_ho／cafe_cha）／A1（`healC17Loc` 定義＋寫 tvb_longmen＋喺 `applyFreeplaySlots`／`evalTrigger_AND_softRumor` 有 call；`softCanonC17Loc` 定義＋強制 tvb_longmen；overlay C17 分支唔抄 `slot.locId`；index.html 再冇 `"agency_ho", "cafe_cha"` 字面；WF4 守門在位）／B2（look-ahead 三要素＋單人＋舊註解已換）／B3（order71 解析出 n＝1–20 順序＋`lastDetailN71` 規則＋`lastDetailIdx71` 已刪＋遠幕守門）。
- 寫死行號問題：呢個測試刻意唔寫死行號（跟 taxi148 先例）。但今次修復令其他三個寫死行號嘅測試要 resync（見下）——行號漂移係真實成本，記錄喺度。

### 全套 A/B（`qa131/run_suite.sh`）

- Pristine `e08a070`：**211 PASS／12 FAIL**（`qa153_suite_pristine.txt`）。
- 工作版：**212 PASS／12 FAIL**（`qa153_suite_work.txt`）。12 個 FAIL 同 pristine 逐個相同（flash51／giglib36／pacing35／poster59／rumor49／slot50／soft_tip_111_restore／start53／weave43／weave44／weave49／wrap38，全部 pre-existing）。+1 係新測試。**零回歸**。
- **套件數字會波動**：同一 repo 連續跑出過 212/12、153/71、201/23，額外 FAIL 每次唔同、逐個直接跑全部 PASS——同 AGENTS.md 記低嘅 v151 教訓一樣，係環境負載問題，唔係回歸。判斷方法：睇「12 項穩定 FAIL＋相關測試逐個直接覆驗」，唔好齋信一次總數。最後一次用逐 test 留 log 嘅 runner（`qa153/run_suite_logged.sh`，失敗 log 存 `qa153/suite_fail_logs/`）跑出 212/12，以呢次為準。
- `node --check`：兩個 inline script 段都 OK（block 0：1,141 字元；block 1：4,308,091 字元）。

### 四個被修復牽連嘅舊測試（全部唔係遊戲回歸）

1. **`tests/test_verify37_logic.js`**——B2 令 C1 開場系統 beat 嘅 pair 由空變非空，`spDlgCharsHtml` 第一次 call 到 `dlg106HasFullbody`，harness 未抽 DLG106 鏈就 `ReferenceError`。修 harness：加 `extractSlice()`，成段抽 DLG106/119 運行段（`const DLG106_CATEGORIES` 起，`haloUrl:dlg119HaloUrl }; }catch(_e){}` 止，L26505–L27030 左右），7 個頂層 `const` 轉 `var`。真頁面唔受影響（函數本身存在）。修後 `VERIFY37 LOGIC: ALL PASS`。
2. **`tests/test_text125_static.py`**——三個寫死行號漂移：currentLine 27800→**27820**、advance 27913→**27949**、applyFamilySafeToNode 33516→**33552**（實量，唔係計出嚟：＋20 係 BehaviorGate healC17Loc 定義＋13／call 位＋7，＋16 係 spDlgPairIds B2 look-ahead）。已更新＋留 shift 記錄。修後 `RESULT PASS`。
3. **`tests/test_travel114_static.py`**——硬計 DEF／WRAPPER 行號漂移。按先例 resync（`qa153/resync_travel114.py`，OLD＝`e08a070`，NEW＝工作版）：44 個 `openLoc(` 呼叫點序列逐字相同，純漂移，先至重寫。DEF 53562→**53633**、WRAPPER 44171→**44221**。修後 `RESULT PASS`。
4. **`tests/test_wf1_80_static.py`**——斷言本身就係舊（錯）次序（v89 BR89 將 C6F／C18／C19 插喺 C6 後）。B3 刻意推翻呢個排法，更新斷言做新 1–20 順序＋註明 v20a153 B3 supersedes v89。修後 `ALL PASS`。

## 實駕（本地鏡像＋Playwright，唔直連 github.io）

- Seed：1992-12-05（day 1069，第 153 週，冬），C1–C16 done，冬台慶有結果（`awardsFlags 1992/award_singho_tv: done`），C10 done。`?softPreview=1`。
- 腳本：`qa153/drive153.py`（`route`＋`route_after_play`，每 case 新 context；`tv_entry` 做 pristine 對照）。結果 JSON：`qa153/drive153_work_932.json`、`qa153/drive153_work_700.json`、`qa153/drive153_pristine_932.json`。截圖：`qa153/shots/`（19 張）。
- **工作版 932：46 PASS／0 FAIL／0 pageerror。工作版 700：46 PASS／0 FAIL／0 pageerror。**

逐項（✓＝兩尺寸都 PASS）：

| 項 | 證據 |
|---|---|
| ① 電視台入場見 C17 掣第一張卡 | TV sheet「要事」第一張就係「播劇情：三年收科」（「台慶之後，何生喺後台等你——三年，係時候收科。」），截圖 `tv_sheet_932.png`／`tv_sheet_700.png` |
| ② 撞巧遇之後 C17 自動接上 | 機制係「主線待播優先」壓制＋C17 卡排第一，唔係播完巧遇再 autoplay。12-05 當日工作版入電視台零巧遇 overlay（pristine 同日同 seed 即彈「巧遇 · 齊鎮海」）；C17 卡即場可播，唔使開進度頁 |
| ③ 事務所／茶餐廳唔再有 C17 掣 | 兩地 sheet 實讀零「三年收科」卡；tips 亦證實（入場刷新後 tvb_longmen＝story:C17，agency／cafe 冇 C17） |
| ④ 進度頁幕次序 1–20（C17 掣喺 C18 之前） | Seed 態實見第 1–18 幕順序（C19／C6F 鎖住唔出 row 係設計），C17 行 index 16、 C18 行 index 17，C17 有「播呢幕」掣，提示行「你而家喺星河電視台，可以即刻播呢幕。」；截圖 `progress_932.png`／`progress_700.png` |
| ⑤ C17 開場第一句何生企台 | 首句「1992 年冬末，星河電視台頒獎禮後台。化妝鏡一排燈泡熱到出煙……」舞台得何生一人，`brightness(0.6)`；截圖 `c17_beat1_932.png`。逐行行到 beat 2 何生對白「阿偉，坐陣。今晚之後……」：何生 `brightness(1)`、阿偉聽者 0.6，截圖 `c17_ho_dialogue_932.png` |
| ⑥ 0 pageerror | 兩尺寸 0 pageerror（`ERR_EMPTY_RESPONSE` 假 error 已過濾，今次一個都冇出） |

路由事實（實駕讀數）：`evalGate3Y('C17').ok=true`、`listOpen=[C17,C18]`、`locIdAny=["tvb_longmen"]`、`softLocId=storyNodeLocId=tvb_longmen`。

**Pristine 對照**（`tv_entry`，932）：`locIdAny=["agency_ho","cafe_cha"]`、`softLocId=storyNodeLocId=agency_ho`（節點本身 `locId` 已經係 tvb_longmen——再次證實只有軟路徑分裂）；入電視台即彈「巧遇 · 齊鎮海」overlay，sheet 第一卡唔係 C17。截圖 `tv_entry_pristine_932.png`。同 review 所述逐字吻合，修復前後對比決定性。

### 實駕 harness 教訓（寫低，免下一手再中）

- **對白有打字機**：每句 ~25–30ms／字打出來，轉句有 ~600ms 延遲，延遲期間撳「下一句」會食咗。700ms 定時採樣會撞正打緊字中途（試過得「三」字）。Drive 改咗做等行文連續 1200ms 唔變先撳（`wait_stable_line`），再按行斷言內容（beat0 L0／L1、beat1 L0／L1、beat2 L0 逐句對）。
- **`refreshStoryMapTips`／`enc79StoryPendingAt` 唔係 global**（主 script 係 IIFE）：harness 直接 call 會 `ReferenceError` 成個 evaluate 報廢；mapTips 喺 seed 後、入場前讀到嘅係開局殘留（C1@agency）。正確做法係入場後先讀（`openLoc` 入場嗰陣先會 `refreshStoryMapTips()`），入場後 tips 實測 tvb_longmen＝story:C17。
- **巧遇對白唔行 `#modal`**：enc79 overlay 自己有 `e79-btn`「下一句」，每撳行一句，冇打字機；唔好用主線舞台嘅 `wait_stable_line` 去等佢（容器唔存在，會每次燒足 timeout）。
- **茶餐廳廖炳星初遇**：12-05 入茶餐廳會撞廖炳星主場巧遇（pre-existing，v138 review 已記低「seed 晒冷卻都唔受壓制，待核實係咪真 bug」）。呢次 drive 證實：① 佢唔係我改嘢引起（我嘅守門只壓「有待播主線」嘅地點，茶餐廳冇 C17 待播）；② 佢係陽性對照——守門冇過壓，唔係全地圖禁巧遇。Drive 會撳散場對白再讀真 sheet（`dismiss_encounter_dialogue`），唔再用 overlay 蓋住嗰陣嘅空 acts 當證據。
- **環境 flake**：`new_game_to_map` 嘅 locator click 同 http.server 起動喺重負載下會 timeout／撞殘留 port。Drive 已改：開局用 JS click＋重試；`serve()` 先 pkill 殘留＋重試等齊 20s；`stop()` 兜底 SIGKILL。

## 檔案

Commit 入分支 `v20a153`（未 push）：
- `index.html`（diff ＋80／－9，89 行異動）
- `tests/test_c17route153_static.py`（新，23 項）
- `tests/test_text125_static.py`、`tests/test_travel114_static.py`、`tests/test_verify37_logic.js`、`tests/test_wf1_80_static.js`（測試維護，見上）
- `NOTES_V20A153.md`（呢份）

工作副本留低、唔入 commit：`qa153/`（drive／探針／resync 腳本、結果 JSON、19 張截圖、suite fail logs）、`qa153_suite_pristine.txt`、`qa153_suite_work.txt`。

## 待統籌決定

1. **WF4 守門嗰 1 行**（L40740）：留定另開票？留低係 A1 完整修復（reviewer 第三次入場就係俾 WF4 食咗）；拎走唔影響其餘 A1。
2. **茶餐廳廖炳星初遇唔受冷卻壓制**：pre-existing，v138 已記低，呢票只係再證實一次，唔喺呢票修。

## Rebase 上 main 29d4821（v171）＋落地前重驗（落地統籌，2026-11-13）

- **決定**：WF4 守門嗰 1 行**留低**（A1 完整修復一部分；新測試有獨立斷言釘死）。茶餐廳初遇唔修（pre-existing；rebase 實駕再證實係隨機掣——932 兩輪一輪出、一輪唔出）。
- Rebase：`442bce2`（基底 `9346a8e`）→ `36d4407`，再 amend 三檔 resync → **`bc1fb82`**（11 檔 ＋398／−83）。`index.html` 自動合併，diff 對 main ＋80／−9 同原分支一字不差；三個測試檔衝突（kwan151／text125／travel114，全部行號漂移），用 `qa153/resync_rebase153.py`（difflib 對位 main→rebased，equal 段先至映射；37 opcodes 全部係 v153 自身 hunks）解，逐行核實內容相同先改。
- **410 斷言要跟 v157 措辭**：v157 重寫改咗 410 setting／synopsis／lockedHint（後台化妝間→會議室、「台慶頒獎禮之後」→「頒獎禮之後嗰晚」）同 beats 結構（開場兩句系統→一句；老場務已無；beat1 何生「阿偉，呢三年…」、beat2 何生兩句、beat3 張子駿）。`test_c17route153_static.py` 兩項斷言改跟 v157 版措辭（`when: "1990冬"` 仲係舊版，唔郁）；反證改為 e08a070 嗰陣 17 FAIL（15 新斷言＋2 句措辭）。
- **Rebase 後多三檔要 resync**（舊 base 嗰陣唔 fail，主因係 main 期間嘅 resync 將釘行移去 v153 插入點之後）：tang152（HELD 25725→25745、normaliser 31387→31423、loader 31531→31567）、tang171（總行數 59171→59242、DEF 53690→53761＝travel114 resync 後數值）、v155（order71 斷言改跟新 1–20 順序，同 wf1_80 一樣註明 v153 B3 supersedes v89）。三檔反證對 pristine 29d4821 乾淨 FAIL（淨係 resync 嗰幾項）。
- **全套 A/B**：pristine `29d4821` **230／12**；工作版 **231／12**（＋1 係新測試；12 FAIL 同 pristine 逐個相同，pre-existing）。第一次工作版跑出 228／15 係上述三檔未 resync，唔係回歸。
- `node --check`：兩個 inline script 段都 OK。
- **實駕抽查（rebase 後，`qa153/drive153_rebase.py`，因 v157 改咗 beats 結構＋v165 拎走咗進度頁「播呢幕」掣，舊 drive153.py 斷言要相應更新）**：
  - **932：49／49 PASS；700：49／49 PASS；0 pageerror**。結果 JSON `qa153/drive153_rebase_932.json`／`_700.json`，截圖 `qa153/shots/*_rb_*.png`。
  - A1：電視台入場 C17 卡第一張（「播劇情：三年收科｜台慶之後，何生喺星河電視台會議室等你」）、零巧遇 overlay；事務所／茶餐廳無 C17 卡；tips 入場後 tvb_longmen＝story:C17。
  - B2：首句「1992 年冬末，星河電視台會議室。冬台慶啱啱完，彩紙仲喺走廊掃唔切…」（year-walk 顯示 1992），舞台得何生一人暗態 0.6；下一句何生對白光態 1；再下一句 beat2 何生；再下一句 beat3 張子駿光態、何生暗態。
  - B3：進度頁第 1–18 幕順序（seed 態），C17 行喺 C18 之前；C17 行文案「已經開放——返地圖嗰陣就會播出。（場景：星河電視台）」，「播呢幕」掣已無（v165 改咗，唔係回歸）。
  - v165 強制播副作用已證實：由事務所返地圖會即播 C18（h3「上岸路」），drive 要先撳「先返回」退出先入到茶餐廳——係 v165 設計，唔係 v153 問題。
  - 兩輪 932 都有 **2 個 console 404（`ho_sang_shy.webp`／`.png`）**，0 pageerror：loader  graceful fallback，舞台照常渲染。查明係 pre-existing 缺圖——410 節點同 main 29d4821 逐字相同（diff 零差異），`ho_sang_shy` 兩邊都冇檔（何生得 7 張表情），v153 冇掂過 beats／expression loader。留返表情修復票，唔喺呢票修。
  - 茶餐廳廖炳星初遇：兩輪 932 一輪出、一輪唔出——隨機掣（p≈0.5），唔係 v153 守門問題（守門只壓有待播主線嘅地點）。

## 第二輪 rebase 上 main e8c3a73（v170）（落地統籌，2026-11-13）

- 第一輪驗證期間 main 郁咗：29d4821 → **e8c3a73**（v170 落地：遊戲 `59fdf54`、NOTES `e8c3a73`、線上 5,254,542 bytes sha `651c26e7…`）。按 v160 教訓，落地前再 rebase 一次。
- `git rebase origin/main` 第一次停咗（todo 重複咗同一個 pick；`git rebase --continue` 先至真正套用），衝突只得 tang171／travel114 兩檔（v170 都 resync 過呢兩檔）；index.html 自動合併，diff 對 e8c3a73 係 ＋80／−9，同 v153 原 diff 一字不差；其餘測試檔（kwan151／text125／tang152／v155／c17route153）乾淨合併——v170 淨係喺 L46098 插 2 行，喺呢啲檔釘行之後，唔影響。
- Resync 第二輪：`qa153/resync_rebase153b.py`（difflib old=e8c3a73 → new rebased；37 opcodes 全部係 v153 自身 hunks）。tang171 總行數 59173→**59244**、openLoc DEF 53692→**53763**；travel114 42 個數字映射（DEF 53763、WRAPPER 44222）。**教訓**：腳本用咗 blanket `txt.replace('總行數 59173'...)`，誤改咗 v170 歷史註解行嘅數字（話 v170 做到 59244／53763，其實係 59173／53692）——已人手改返，tang171 重驗 22/22。Resync 腳本唔應該用 blanket replace 改 prose 數字。
- 新 HEAD **`eebd2f7`**（11 檔 ＋416／−83），index.html 對 e8c3a73 係 ＋80／−9，`healC17Loc` 只定義一次（冇重複套用）。
- **全套 A/B（今次用正確參數跑，有逐檔清單）**：pristine e8c3a73 **231／12**（同 v170 落地數字一致）；工作版 **232／12**（＋1 係新測試）；**FAIL 清單逐項相同**（12 項 pre-existing）。註：第一輪用咗 `bash run_suite.sh` 唔帶參數（`$OUT` 空，逐檔行寫唔到檔），總數本身可信但冇清單，已經用正確參數重跑。
- 相關測試全 PASS：c17route153 23/23、kwan151、text125、tang152、tang171 22/22、travel114、v155、wf1_80、verify37；`node --check` 兩段 inline script 都 OK。
- **實駕抽查（最終樹 eebd2f7，`qa153/drive153_rebase.py`）**：**932：49／49 PASS；700：49／49 PASS；0 pageerror**；兩輪各 2 個 console 404（同一 pre-existing `ho_sang_shy` 缺圖）。

## 第三輪 rebase 上 main a500536（v149）（落地統籌，2026-11-13）

- 第二輪驗證期間 main 又郁咗：e8c3a73 → **a500536**（v149 落地：遊戲 `461dc87`、NOTES `a500536`、線上 5,262,537 bytes sha `b299ce9f…`）。
- 今輪 `git rebase origin/main` 開頭報「local changes would be overwritten」（8 檔測試），但 `git diff` 係空——同第二輪一樣係 todo 重複 pick 嘅環境怪象，`git rebase --continue` 正常套用。衝突五檔（kwan151／tang152／tang171／text125／travel114——v149 都 resync 過呢五檔）；index.html 自動合併，diff 對 a500536 係 ＋80／−9。
- Resync 第三輪：`qa153/resync_rebase153c.py`（difflib old=a500536 → new rebased；37 opcodes 全部係 v153 自身 hunks；今次全部只改 code 行，註解行原封不動）。tang171 總行數 59270→**59341**、openLoc DEF 53789→**53860**（淨 ＋71 吻合）；travel114 42 個數字映射；kwan151／text125／tang152 按 round-1 pattern 映射。
- 新 HEAD **`e8908b7`**（14 檔 ＋927／−82——連同 qa153 兩份 resync 腳本＋一份 suite log 一齊入咗 commit，NOTES 引用佢哋做 resync 證據）。
- **全套 A/B（正確參數，逐檔清單）**：pristine a500536 **231／12**；工作版 **232／12**（＋1 係新測試）；**FAIL 清單逐項相同**（12 項 pre-existing）。
- 相關測試全 PASS：c17route153 23/23、kwan151、text125、tang152、tang171 22/22、travel114、v155、wf1_80、verify37。
- **實駕抽查（最終樹 e8908b7）**：**932：49／49 PASS；700：49／49 PASS；0 pageerror**；兩輪各 2 個 console 404（同一 pre-existing `ho_sang_shy` 缺圖）。

## 落地紀錄

- **遊戲 commit `bbd318e`**（squash merge `v20a153`，基底 a500536／v149；14 檔 ＋937／−82；index.html ＋80／−9），**2026-11-13 已 push main**（`a500536..bbd318e`），`git fsck` 乾淨（淨 dangling 殘留）。
- **線上核實**：https://joinkidshk-glitch.github.io/linji-chutoutian-web-preview/ —— **5,266,916 bytes、sha256 `094072a4…`**，同 repo `HEAD:index.html` 完全一致。第一次 curl 仲係舊版（Pages 部署滯後，5,262,537 bytes sha `b299ce9f…`）；第二次 curl 撞到 egress 傳輸中斷（2,756 bytes、exit 23）；重試後攞到完整新版。
- 驗收總數（最終樹 e8908b7／分支 HEAD `0135b21`）：新測試 23/23；全套 pristine a500536 231／12 vs 工作版 232／12，FAIL 清單逐項相同，零回歸；實駕 932＋700 各 49／49 PASS、0 pageerror（2 個 console 404 係 pre-existing `ho_sang_shy` 缺圖）。
- 殘留：`ho_sang_shy` 缺檔（表情修復票跟進）；茶餐廳廖炳星初遇唔受冷卻壓制（pre-existing，v138 已記低）。
