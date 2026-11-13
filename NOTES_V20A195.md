# NOTES_V20A195 — 阿偉造型最高紀錄（B 方案）＋ s2／s3 angry 表情

## 0. 接手說明（takeover）
- 上一手統籌（`3ec8022e`）完結嗰陣冇交最終報告，工人（`08673cf8`）中斷咗，半成品留喺工作副本，零 commit。**冇 resume 嗰個工人**——接手統籌直接接手半成品：逐樣對 code 核實、rebase 上最新 main、補完、驗證、落地。
- 接手嗰陣半成品狀態：`index.html` 已改（淨 +93／−6）；16 檔靜態測試已 resync；兩張 angry 圖已入庫；`tests/test_awei195_logic.js`、`tests/test_awei195_static.py` 已寫好；`qa195/`（resync 腳本＋舊全套記錄）、`qa195_bake195.py`、`samples195/` 已有；**NOTES 未有**（呢份由零寫）。
- 接手核實結論：半成品**真係行 B 方案**（唔係 A，亦冇撈埋）——寫入／讀取／backfill 三件齊，兩張圖係真新圖（見 §2），兩檔新測試全 PASS。接手後唯一改動係 rebase 上 v192 main（見 §5）＋補 NOTES。

## 1. 根因（調查報告 `~/workspace/linji-work-awei-look/INVESTIGATION.md`）
- `enc79PlayerTier()`（L52503 附近）只數**當年** `GIGS` 入面 `done_*` 旗＋`roleScale` 含 lead 嘅通告（tier 2 要 lead≥1；tier 3 要 lead≥3＋fame≥70）。
- `syncGigsForCalendarYear()` 每年 1 月 1 日成張換走年庫（1990＝`gigs_1988.json` 155 張、1991＝`gigs_1989.json` 52 張）。1990 年做完男主角升到 s2，踏入 1991 年嗰部 1990 男主角唔再喺清單入面，tier 即時由 2 跌返 1。
- `dlg106AweiStem()`（L26796）：tier 0–1→`awi`、2→`awi_s2`、3→`awi_s3`。對話全身圖、屋企 `#home-awi`（`bust109HeroSrc()`）、頁頭 bust 共用同一規則，一齊變返 s1。
- 實駕重現（同一 save）：day 300（1990 男主角後）出 `awi_s2_base.webp`（淺灰西裝），day 400（1991）跌返 `awi_base.webp`（深藍 bomber 褸臨記樣）。
- 次要發現：① s2/s3 欠 `angry` 表情（各 7 張欠 angry；s1 有）——tier 2 憤怒句停喺 `awi_s2_base.webp`，外形保得住但嬲變中性。② 5 張「假男主角」：`NAME93_FIX` 將 `gig_1988_tv_06`／`07`／`08` 等由 lead 降級做配角；1990 pack 話 20 部男主角戲，實際得 15 部——修 tier 計數一定要跟 normalize 後嘅 `roleScale`，唔可以直接數 pack 檔。

## 2. 修法：B 方案（用戶 2026-11-13 20:57 撳 A、20:58 改做 B——行 B，唔係 A）
- **寫入**：殺青嗰陣（`resolvePlannedDay` 寫 `done_*` 旗之後）＋逾期掉單（`failShootOverdue` 同樣寫 `done_*` 旗嗰陣）call `enc195RecordTierMax()`，記 `max(現值, 即時 tier)`。即時 tier 計數本身唔郁。
- **讀取**：`dlg106AweiStem()` 讀 `max(即時 tier, S.flags.playerTierMax)`（讀之前先 `enc195EnsureTierMax()` 懶回填）。
- **Backfill**：舊檔載入嗰陣 `normalizeSaveObj` → `enc195BackfillTierMax(o)`，由現有 `done_*` 旗反推一次最高 tier 寫入。口徑跟 `enc79PlayerTier`（`normalizeGigRecord` 後嘅 `roleScale`，NAME93／OVR110 降級一致；掃 `STORY_WIRE.gigsByYear` 全部年庫 1990–1994）。**冪等**：已有數字就唔郁；年庫未載入就留空唔寫 0，等第一次讀造型嗰陣懶回填。
- **已知取捨（寫明，唔係漏咗）**：backfill 係一次性、唔覆寫已有值；殺青寫入點用即時 tier（當年計數）。所以一個新檔玩家如果將 3 部 lead 分散喺唔同年份做（每年都唔夠 3 部），即時 tier 永遠唔到 3，最高紀錄會停喺 2——而同樣歷史嘅舊檔經 backfill（全歷年掃）會回填到 3。呢個係「最高紀錄」定義嘅邊界：紀錄＝`enc79PlayerTier` 曾經達到過嘅最高值，唔係全歷年累計重計。升 tier 唯一路徑係殺青寫入點（logic test (d) 釘死咗呢點）。如果日後用戶覺得跨年累計都應該升 tier 3，先至再改寫入點用全歷年計數——嗰陣要改埋 (d) 嗰組斷言。
- **附帶同票**：補 `awi_s2_angry.webp`／`awi_s3_angry.webp` 各一張（跟官方風格錨 `~/workspace/linji-native-design/style-anchor-awei-anime.jpg`：乾淨平塗賽璐璐、清線條、大眼少年感、米白光邊）。接手目視核實：兩張都係真新圖（唔係 s1 改名）、嬲樣清晰（眉頭緊鎖、嘴角向下）；s2 淺灰西裝＋白恤衫、s3 深藍西裝＋白恤衫開領＋單手插袋，同 s1 深藍 bomber 褸分得清。s2／s3 表情而家各齊 8 張（含 angry）。
- **唔郁**：`enc79PlayerTier()` 本身（仲係數當年 GIGS，好感上限等判定唔受影響）；SAVE key（`starVolunteer_map_v19w`）、softRev（`s107`）、`?v=`（`v20a10`）；唔直改 content pack JSON；開局 `#start-standee`／UI40_STAND 舊圖（已知殘留，另開一票）。

## 3. 改動清單
- `index.html`：淨 +87 行（93 增 −6 刪），5 處：(1) `dlg106AweiStem` 改讀最高紀錄（淨 +4）；(2) `normalizeSaveObj` 加 backfill 呼叫（淨 +3）；(3) `resolvePlannedDay` 殺青寫入點加 record 呼叫（淨 +2）；(4) `enc79PlayerTier` 之後加 enc195 四函數（`enc195TierFromAllYears`／`enc195BackfillTierMax`／`enc195EnsureTierMax`／`enc195RecordTierMax`，淨 +75）；(5) `failShootOverdue` 寫入點加 record 呼叫（淨 +3）。
- 新圖：`assets/story/fullbody/awi_s2_angry.webp`（194,726 bytes，880×3056）、`assets/story/fullbody/awi_s3_angry.webp`（188,116 bytes，880×3056）。fullbody 總數 207→209、真檔 182→184。
- 新測試：`tests/test_awei195_logic.js`（31 項斷言，7 組：(a) 跨年唔跌 (b) 殺青寫入 (c) tier 3 跨年 (d) 舊檔 backfill (e) 假男主角 (f) 年庫未齊＋懶回填 (g) 全池口徑 15 部真男主角）、`tests/test_awei195_static.py`（S1–S8）。
- Resync：16 檔靜態測試（dlg107／108／109／119／123／126／127／138、gift185、kwan151、rom176、tang152／171／173、text125、travel114）——行號釘按段重算＋fullbody 數 207→209／182→184。核實方法見 §5。

## 4. 驗證（接手後重跑）
- 新測試（rebase 後最終樹）：`test_awei195_logic.js` ALL PASS、`test_awei195_static.py` ALL PASS。
- 反證（pristine main b104f85，`/tmp/awei195-pristine/` 淨抽 index.html＋兩檔測試）：logic 7 FAIL（逐組印 FAIL，exit 1，唔 crash）、static 5 FAIL（S1–S5，exit 1，唔 crash）。
- 全套 A/B（`qa131/run_suite.sh`，接手後 rebase 樹重跑）：pristine b104f85 `qa195/suite_pristine195.txt` **265 PASS／12 FAIL** vs 工作版 `qa195/suite_work195.txt` **267 PASS／12 FAIL**——FAIL 清單逐行相同（12 項穩定 pre-existing FAIL：flash51／giglib36／pacing35／poster59／rumor49／slot50／soft_tip_111_restore／start53／weave43／weave44／weave49／wrap38），**零回歸**；+2 PASS 啱啱係兩檔新測試（awei195 logic＋static）。注意：第一次鏈式跑嗰陣 OUT 用咗相對路徑，pristine 嗰份寫唔到（run_suite.sh 會 `cd $ROOT` 先），只得 stdout 總數；已用絕對路徑重跑 pristine 一次，兩份 OUT 齊晒。舊工人嗰兩份 `suite_workA.txt`／`suite_workB.txt` 係舊基底＋B 份中斷咗（得 76 行），作廢，唔好引用。
- 實駕（`qa195/drive195/DRIVE195_REPORT.md`＋`drive195_report.json`，39 張截圖）：**23/23 PASS，0 pageerror、0 http fail**（932＋700，LIVE 模式，真載入路徑 `#btn-cont` 繼續讀檔）。A 基線 day 300 出 `awi_s2`；**B 核心修復 day 400（1991）仲係 `awi_s2`，零 s1 圖**；C 對照 1991 真男主角出 s2；**D tier 3 跨年 day 400 仲係 `awi_s3`**；**E 舊檔 backfill**（冇 `playerTierMax` 旗）載入後 `playerTierMax === 2`、對話出 s2；F angry 新圖：`candidates('awi','angry')[0]` 係 `awi_s2_angry.webp`／`awi_s3_angry.webp`（`complete`＋`naturalWidth 880`＋HTTP 200，目視嬲樣＋對應西裝色）；G 屋企 bust：`#home-awi` src 首 140 字元逐字等於 `BUST109_EXTRA.awi_s2`／`awi_s3`（唔等於 s1），截圖目視淺灰／深藍西裝；H pristine 對照（b104f85）同一批 seed 1991 年跌返 `awi_base.webp`（tier [1,1,1]），bug 重現。B 附加：`delete playerTierMax` 後再讀 stem 照係 s2、紀錄寫返 2（懶回填）。
  - 如實記錄嘅限制：① F 用咗合成 beat（`StoryPlay.start`＋`emotion:"angry"`＋對白「夠啦！呢場戲唔係咁拍㗎！」），因為全庫 25 句 player 阿偉對白＋3 句阿偉 beats，0 句含嬲關鍵字——**兩張新圖已接入候補鏈首選，但自然遊玩要等將來有阿偉嬲嘅劇情先會出現**。② G 無正常 UI 路徑入屋企（地圖冇屋企掣、手帳冇回顧手帳掣，同調查報告一致），最後直接 call `enterHome(null,false)`（同 UI 掣同一個函數）；「返屋企」應唔應該有掣係產品問題，值得另開一票，唔喺 v195 入面。③ A／D300 茶餐廳 trigger 播唔出故事，要 fallback `StoryPlay.start('C6')`（播出嘅同樣係 C6 實體內容；原因未查，估計同 Continue 後待播事件疊加有關）。④ 載入後 `dayIndex`＋1（300→301、400→401，年份唔變），唔影響跨年判斷。

## 5. Rebase（接手做）
- 基底由 f2a6b0c（v191）rebase 上 b104f85（v192 NOTES，main 6cfcfbf）。`index.html` 自動合併乾淨（v192 改動喺 L45343–46569 頒獎禮區，同 v195 5 處插入點無重疊）。
- 5 檔測試衝突（gift185／rom176／tang171／tang173／travel114——兩邊都只係行號 resync）：以 HEAD（v192 版）做底，按 `qa195/resync195_rebase.py` difflib 映射（b104f85→工作版，淨 +87、6 個 hunks 全部係 v195 插入、全部釘內容逐字核實，BAD: 0）重算釘行；解法腳本 `qa195/resolve_rebase195.py`（數字單次掃描 dict 查表，唔逐對 re.sub）。解完 5 檔測試全 PASS＋兩檔新測試全 PASS，`GIT_EDITOR=true git rebase --continue` 成功。
- Rebase 後總行數 60522→60609（v192 基底 60522＋v195 淨 +87）。
- 注意：半成品嗰陣 `qa195/resync195.py`／`apply_resync195.py` 係對 f2a6b0c 基底寫嘅，留返做審計紀錄；rebase 後嘅正確映射係 `resync195_rebase.py`＋`resolve_rebase195.py`。

## 6. 落地
- Squash merge：常駐 clone main `b104f85`（v192）→ `git merge --squash v20a195` → commit `4f47077`（「v20a195: 阿偉造型最高紀錄（B 方案）＋ s2/s3 angry 表情（新測試 32+18 項＋實駕 23/23 PASS；全套 267/12 零回歸）」），75 檔、5197+/93-。`git fsck --strict` 乾淨。
- Push main 一次成功（`b104f85..4f47077 main -> main`）；curl 核實線上 **5,343,979 bytes、sha `369e4c96fccb…`** 同 repo HEAD:index.html 一致（第一次 curl 嗰陣 Pages 仲係舊版 v192，75 秒後再核先追上）。
- `samples195/`（raw 生成 PNG）跟 v147 前例唔入 repo，留喺工作副本 `~/workspace/linji-work195/samples195/`。

## 7. 設計 review
- （待填）
