# NOTES — v20a266 林曉晴《留低》覆寫層跟進票（ROMANCE_V158_OVERRIDES 移植落地）

- 工作副本：`~/workspace/linji-work266/`，分支 `v20a266`，base main `60f0d12`（v265）。
- 來源：舊工作副本 `~/workspace/linji-work158/` 未落地 WIP（base v148，分支 v20a158）入面嘅
  林曉晴《留低》覆寫層。舊副本本身冇郁過（只讀；`git status` 維持原有未提交狀態）。
- 任務：先調查再決定落地／唔落地／部分落地。結論：**(a) 移植落地**（見 §1 證據）。

## 1. 調查結論：點解值得落地，點解唔係已被取代

- **v159 冇取代佢**：v159（`9b1e6f0`）只做換人＋約會層，`git show 9b1e6f0` 7 處 R_hiu_ 提及
  全部係接線／註解，其中一句寫明「R_hiu_* 故事節點本身唔郁（v158 支線票嗰邊）」；pack
  `content/story_detail_romance_vera_hiu_choi.json` 入面 R_hiu_* 仍係原裝五節點
  （meet P1／push1 P1.5／push2 P2／crisis P4／ending P5，舊 choice ids）。
- **設計唯一實現**：`romance-revamp-draft.md` §1 林曉晴《留低》弧線（兩封信→同場搶通告→
  夜班殺青後交心→廠景天台收尾；HE「留低」／BE「機場送別」）喺 live 唯一實現就係呢層；
  現行 live R_hiu_* 係 Vera 時代舊稿（茶餐廳試鏡情報／屋企唔支持心事／通用天台表白），
  「兩封信」／玉女約／移民抉擇完全唔存在。
- **機制兼容**：WF2 表現行得返 10 keys（vera／lan 各 5），唔掂 hiu；`enc87StoryFlag`、
  `contra98PrepareNode` 呼叫點、`refreshCopyPacksFromDisk` WF2 呼叫點、`STORY_WIRE.romance`
  全部喺現行 main 存在；openConditions 引擎（WIRING_OC_ENGINE）支援節點號＋phase token
  （主線 N2 `['N1', ...]`、A_ko_ending `['phase_P4']` 係現成先例）。
- **phase 對得上現行計算**：push1 P1＋N4（N4 後開）、crisis P2＋N9（1991 秋）、push2 P2＋N10
  （1991 冬）、ending P4＋phase_P4＋N14（1992 秋），同 when 值（crisis 1991秋／push2 1991冬／
  ending 1992秋）一致。phase 觸發已改 N 號（P1.5＝N5 done、P2＝1991 或 N7 done、
  P4＝1992秋 或 N13 done、P5＝1992冬 或 N16 done），層內 phase 值唔使改。
- **舊旗唔撞**：`flag_hiu_push1_help/self`、`flag_hiu_push2_date/friend`、
  `flag_hiu_crisis_yield/fight` 喺現行 main 除咗 pack 自身鏈（openConditionsAny）之外
  冇任何讀取點；新 choices 寫新旗，舊旗留喺 openConditionsAny 做舊檔 fallback。
- **rel 尺度唔郁**：新旗 rel 增減（push1 ＋2／0／−1、crisis ＋2／−2、push2 ＋2／0）同
  原裝一致，commit 閘 rel 6／排他鎖 rel 5 唔受影響；ending choices／flags_written 一字唔郁。

## 2. 移植適配（相對舊 WIP，全部有意圖改動）

1. **openConditions C→N**：`["C4"]`→`["N4"]`、`["C8"]`→`["N9"]`、`["C9"]`→`["N10"]`、
   `["phase_P4","C12"]`→`["phase_P4","N14"]`（C 節點號已死：現行 main 零 `"C4"`／`"C8"`／
   `"C9"`／`"C12"`；對照 v210：N4=C4、N9=C8、N10=C9、N14=C12）。
2. **5 段 synopsis 改寫做香港式書面語**（用戶 2026-11-15 語言規則：synopsis 係敘述，唔係對白）：
   舊版用 喺／佢／咗／搵 等口語；新版對照現行 pack synopsis 寫法（她／在）。beats 對白維持廣東話。
   crisis synopsis 直接用返 pack 現文（內容相同，已經係書面語）。
3. **packs 刪 rom.tang**：`[rom.veraHiuChoi, rom.lanXu, rom.tang]`→`[rom.veraHiuChoi, rom.lanXu]`
   （v152 已刪鄧麗萍感情線；`STORY_WIRE.romance` 現行得返 veraHiuChoi／lanXu／yipSo）。
4. **CONTRA98_WHEN_FIX 唔郁**：層內兩項（crisis `["1989秋"]`／ending `["1990秋"]`）已由
   v223（`91e6365`，when 顯示值修復）獨立落地，數值完全相同；key 數維持 23。
5. 標識符保留原名（`ROMANCE_V158_OVERRIDES`／`applyRomanceV158Overrides158`／
   `enc158PrepareNode`／`V158_APPLIED158`），加 v266 移植註解，方便對照舊副本核實。

## 3. 唔郁嘅嘢（有意圖保留）

- 舊 WIP 其餘四條支線（陸／廖／顧／麥：flags 欄位引擎、冷版 beats、absent tick 等）**唔喺呢票
  範圍**，留返支線補完 WORKORDER ①組跟進。呢票只抽曉晴層（表＋apply 函數＋hook＋兩處呼叫）。
- WF2 表（10 keys）＋merge 函數一字唔郁；V158 層喺 WF2 之後跑，覆寫同一 5 節點。
- `COMMIT48_REL_MIN=6`、commit 機制、`CMT_hiu_commit`、SAVE key／softRev／`?v=` 唔郁。
- content pack JSON 唔郁（全部經 inline 覆寫層注入）。

## 4. 已知留低（唔阻塞落地）

- **感情線未解決項第 10 項（舊 WIP 已寫明）**：揀咗 `hiu_family_go`（勸跟屋企走）嗰陣，
  ending hook 換成啟德送機 beats（BE「機場送別」），但 HE choice 仍然可以揀——同原裝 pack
  一樣（crisis 硬搶之後 HE 照樣可以揀），係 beat 變體層唔做閘嘅既有設計，唔係呢層新引入
  嘅不一致。留待感情線跟進票決定係咪要喺「走」路徑閘住 HE。
- **實機驗證押後**（瀏覽器死）：R_hiu_push1 兩封信三揀一、crisis 三版開場、ending 三版收尾、
  鏈重排後各節點開閘時序（N4／N9／N10／N14），等瀏覽器恢復再實駕。

## 5. 實作改動對照（work266，base 60f0d12）

- `index.html` 淨 +328 行（0 刪）：
  - V158 block ＋284 行（WF2 apply 函數之後）：表＋`V158_APPLIED158`＋apply 函數。
  - `enc158PrepareNode` ＋42 行（`wf3PrepareNode82` 之前）。
  - 載入鏈呼叫 ＋1 行（`applyRomanceWf2Overrides81();` 之後，textfix55 之前）。
  - StoryPlay 預備鉤 ＋1 行（`contra98PrepareNode` 呼叫之後、`rom159PrepareNode` 之前）。
- 移植方法：`/tmp/port266.py` 逐字抽舊副本三段（表／apply／hook），全部編輯 assert exact-match；
  其後兩處手動修補（apply 註解入面 `rom.tang` 字串會令靜態斷言誤判，已改寫做「tang 槽」；
  詳見 §6）。
- 新測試 `tests/test_hiu266_logic.js`：**36 項 ALL PASS**（靜態 6／apply 8／語體 10／hook 9／載入鏈 4；
  beats 廣東話標記 109–152／節點，書面語 0；synopsis 廣東話標記 0）。
- 主 script 抽出 `node --check` 通過（SYNTAX_OK）。

## 6. 全套 suite＋resync

- 第一輪：**322／19**——多出 9 項釘行漂移（gift185／kwan151／rom159／rom176／tang152／
  tang171／tang173／text125／travel114），全部係插入點之後嘅行號／總行數帳本，內容零郁。
- Resync（`qa266/resync266.py`＋`qa266/resync266b.py`，difflib 對位核實內容逐字相同，純漂移）：
  9 檔釘行按映射重寫（text125 3 處／kwan151 14 處／tang152 3 處／rom159 6＋全佳 1 處／
  rom176 5 處／travel114 COUNT 12＋FREE 40＋DEF／WRAPPER／gift185＋tang171＋tang173 總行數
  帳本＋DEF 帳本，鏈尾加 ＋v266 +328）。
  - resync 腳本教訓：`line(N)` 同一錨點喺同一 `ok()` 行可以出現多次（kwan151 A1 兩次、
    `line(14697)` B3／B4／B5 共 5 次），replace 唔可以 assert count==1；另外
    `＋v265 +378）` 喺 tang171 檔頭註解同 ok() 標籤各出現一次，錨點要連埋後續字元先唯一。
- 重跑：**331／10**（基線 330＋新檔 1；十項全部係已知 pre-existing FAIL：flash51／rumor49／
  slot50／soft_tip_111_restore／start53／weave43／weave44／weave49／wf5_87／wrap38），零回歸。
  逐檔覆驗：9 檔 resync 後個別全部 PASS＋新檔 ALL PASS（`qa266/suite266b.txt`）。

## 7. 落地

- 方式：常駐 clone `git merge --squash v20a266` → commit → push main（deploy key，唔開 PR）；
  合併後 main HEAD 見 `git log`（本票 commit 訊息有 v20a266 字樣）；Pages 核實：等傳播約 4 分鐘後
  curl 主頁 200 且同本地一致，`ROMANCE_V158_OVERRIDES` 在位。
- 落地後即刪工作副本 linji-work266；舊 linji-work158 保持原樣唔郁（入面仲有四條支線 WIP 等跟進票）。
