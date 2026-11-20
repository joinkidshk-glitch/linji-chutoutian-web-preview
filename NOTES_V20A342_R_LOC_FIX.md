# v20a342 R_ 節點 locId 修復 — NOTES

## Bug（v299 實駕發現）

全部 31 個 R_ 感情節點（`content/story_detail_romance_lan_xu.json` 11 個＋
`story_detail_romance_vera_hiu_choi.json` 10 個＋`story_detail_romance_yip_so.json` 10 個）
JSON 無 `locId`，`STORY_LOC_SOFT`（index.html L6736）只有 N 節點 →
`storyNodeLocId()`（L7587）回 `null` → `enterLoc`／`doTalk` 永遠唔寫 offer →
入唔到 `listOpen` → `StoryPlay.start` 拒播（「這幕尚未在地圖出現」）。
六條感情線嘅 pack 節點喺真實玩法下全部播唔到；感情推進之前只靠送禮／約會／COMMIT48
code-side 節點。v299 drive 證明節點內容本身無問題（手動 `openMeetOffer` 後三版對白
驗證正確），純粹缺觸發路徑（證據：`~/workspace/linji-drive-299/`）。

## 改動（完美做法：畀 R_ 節點派 locId，行返現成 offer 機制）

### 1. index.html `STORY_LOC_SOFT`（N17 行之後加 31 條，淨 +20 行）

| 線 | 節點 | locId | 理由（setting／女角主場） |
|---|---|---|---|
| 藍若曦 | meet／push1／push2／crisis／ending | `tvb_longmen` | 全線電視台場景（廠景／人事部走廊／廠景門口），ROM176 primary 亦係星河電視台 |
| 徐寶珊 | meet | `tvb_longmen` | setting「星河電視台春茗酒會」 |
| 徐寶珊 | push1／push2／crisis／ending | `ad_central` | 商場廣告活動／私人會所飯局／商界包廂／商界晚宴後台，全部商界場；寶珊主場係中環廣告 |
| （stub） | R_tang_meet_stub | `ad_central` | 公關公司會議室；`isStubNode` 命中 `/_stub$/` 永不播，locId 只為齊全 |
| 林曉晴 | meet／push2／crisis／ending | `tvb_longmen` | 廠景休息角／夜班殺青後／試鏡廊／廠景天台 |
| 林曉晴 | push1 | `cafe_cha` | setting「茶餐廳／廠景後門」，取茶餐廳 |
| 周采兒 | meet | `tvb_longmen` | runtime setting 經 WF5 override 係「電視台走廊一角」（同 N5 同地） |
| 周采兒 | push1／push2 | `cafe_cha` | 茶記／報館附近、私下晚餐 |
| 周采兒 | crisis／ending | `ad_adm` | 週刊會議室／報館後巷，歸金鐘創意（辦公室地點） |
| 葉敏芝 | 全五節 | `tvb_longmen` | 跟 N8 選美後台（星河綜藝廠）——見下方出入註記 |
| 蘇芷茵 | meet／push1／crisis／ending | `rec_wanchai` | 灣仔唱片大堂／錄音室走廊／會議室／錄音室 |
| 蘇芷茵 | push2 | `ad_central` | setting「中環廣告公司樓下」 |

**出入註記（葉線）**：R_yip_meet setting 寫「九龍電視台選美後台」，但節點
`linksMain` 係 N8，而 N8 JSON `locId`＝`tvb_longmen`（星河電視台綜藝廠後台；
選美綵排）。跟設計「葉 meet 掛 N8 選美後台」派 `tvb_longmen`；setting 文字嘅
「九龍電視台」係舊稿地名，同 N8 實際場地唔同，今票唔改對白／setting 文字。

### 2. JSON 三個 pack：移除 19 個節點嘅 `"playerOffer": false`

只派 locId 修唔到呢 19 個節點：`openMeetOffer`／`enterLoc`／`doTalk`／`listOpen`
（playerStrict）全部擋 `playerOffer===false`，有 locId 都寫唔到 offer。
設計意圖（STORY_MEET_SOFT 註解「首次入 loc／傾談先開 offer」）從來冇接上 code；
NOTES_V20A159 L96 亦明文「R_yip／R_so meet-offer 接線未做」係已知留低。
改做 omit（同其餘 12 個節點一致）後，現成 offer 機制即行得通。

- lan_xu（7）：R_lan_meet／push1／push2／crisis／ending、R_xu_meet、R_tang_meet_stub
- vera_hiu_choi（2）：R_hiu_meet、R_choi_meet
- yip_so（10）：全部

### 3. JSON crisis when 修復（source 1991→1990，顯示 1992）

`when` 只影響頁首顯示（`evalNode` 閘唔讀 when）；YEARS66 walk 將 source 年份 +2。
四個 crisis＋R_xu_push2 source 寫 1991 → 顯示 1993，超出遊戲終點 1992，逐個改 source 做 1990：

- R_lan_crisis `"1991春"`→`"1990春"`（顯示 1992春）
- R_xu_push2 `"1991"`→`"1990"`（顯示 1992秋）
- R_xu_crisis `"1991"`→`"1990"`（顯示 1992秋）
- R_hiu_crisis `"1991"`→`"1990"`（顯示 1992夏）
- R_choi_crisis `"1991冬"`→`"1990冬"`（顯示 1992冬，parent 點名嗰個）

唔郁：五個 ending `when: "1992"`（walked "1994" 但冇季字，頁首跌返 fallback
「1990春」，屬既有顯示怪癖，唔喺今票範圍）；R_tang_meet_stub `when: "1991"`
（stub 永不播、唔顯示）；`eraTag`（喺 SKIP_KEYS，唔 walk）。

### 4. 唔郁

節點對白內容、`choi299PrepareNode`、`rom159PrepareNode`、COMMIT48、送禮／約會路徑、
STORY_MEET_SOFT（死數據，唔掂）。

## 測試

- **新測試 `tests/test_r342_r_loc_fix.js`（54 項 ALL PASS）**：抽真函數沙盒——
  (a) 31 節點 `storyNodeLocId` 全部命中派位＋`playerOffer` 無 false；
  (b) 六線逐線真跑觸發鏈（播種存檔→複製 enterLoc offer loop 真寫 offer→
  `listOpen` 真入列→`hasPlayerOffer`＋`evalNode` 兩閘通過，即 `StoryPlay.start`
  唔會拒播；start 本體要 DOM，drive-299 已實駕證明有 offer 即播到）；
  (c) push1 鏈兩線（lan meet 旗／choi N5 spin 旗）；
  (d) 五個 crisis/push2 頁首經 `years66Walk`＋`spPlayerMeta_softSeasonFrom`
  真顯示 1992（R_choi_crisis＝「主線 · 1992冬」）。
- **既有斷言同步**：`test_rom159_yipso_static.py`、`test_weave48_static.py`、
  `test_weave48_logic.js` 嘅 playerOffer 斷言改做「非 false」；
  `test_aud91fix122_static.py`／`test_aud91fix124_static.py`／
  `test_newspaper214_award_static.py` 加 v342 content 豁免集（三個 romance pack）。
- **釘行 resync**（index.html 淨 +20 行，插入點舊 L6758 後）：`qa342/resync342.py`
  逐檔精確替換（count 斷言）——rom159_static 7 釘、rom176_static 5 釘、
  tang152_static 3 釘、tang171／tang173／gift185 總行數 47296→47316＋openLoc DEF
  42516→42536、travel114 COUNT／FREE 50 錨點＋DEF／WRAPPER、text125 3 釘。
  `qa342/fix342.py` 係 JSON 改動腳本，一併留檔。
- **全套 suite：395 PASS／9 FAIL**（v341 基線 394／9＋新測試 1 項；九項 FAIL 同基線
  逐項一致：flash51／slot50／soft_tip_111_restore／start53／weave43_static／
  weave44_static／weave49_static／wf5_87／wrap38）。跑完已還原 `qa296/derive296.json`。

## 出貨

- 工作副本 `linji-work342`（clone 式），分支 `v342`（commit `85f4c39`）。
- main HEAD `977bfe9`（squash 內容 commit，suite 395／9）；Pages 核實 byte-identical：
  index.html md5 `e72e24c27234c85d92d6d69a95fd12f7`／4,706,558 bytes／47,316 行；
  三個 romance pack md5 亦逐一對版（lan_xu `5748debc…`／vera_hiu_choi `e223e395…`／
  yip_so `93f37dea…`）。
- 通告庫 323 張不變；index.html 47,296→47,316 行（+20，STORY_LOC_SOFT R_ 條目）。
- 證據：`~/workspace/suite342_base.txt`（基線 394／9）、`~/workspace/suite342_r2.txt`
  （落地前 395／9）。
