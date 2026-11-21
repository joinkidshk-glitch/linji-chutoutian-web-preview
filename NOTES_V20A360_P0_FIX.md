# v20a360 NOTES — 多工人實玩評估 P0 三修

對象：live v359（main `8d7df2e`）→ v360。評估報告：`~/workspace/linji-playtest-eval-2026-11-21/REPORT.md`（P0 第一批三項）。只修三項，冇順手改其他平衡（P1/P2 等用戶拍板）。冇改 SAVE key／softRev／產品 `?v=`；年份 source 冇手改。

## ① 試鏡 reveal 派送修復（strand 自癒）

**Strand 路徑（已確認）**：`aud91PresentDue`（index.html，晨鏈試鏡消息環）用 session 旗 `_aud91Presenting` 串行呈現，旗只喺 `done()`（到期清單空）先清。死亡路徑有二：
- `aud91PresentOne` 同步拋錯（modal 未接線前）→ `step()` 永遠唔再行 → 旗 strand；
- reveal modal 被其他 `modal()` 取代（`_modalDismiss`＋內容被覆寫）→ continuation 永遠唔行 → 旗 strand。

旗 strand 後，之後每次晨鏈 `aud91PresentDue` 都回 false，所有 reveal 唔呈現，pending 滿 3 張連新試鏡都 block（W1/W5 兩 driver 同證：revealDay 過咗 15–23 日未呈現）。reload 先重置（旗係 session 變量）。

**修法**（`aud91PresentDue` 內，唔改呈現內容／次序）：
1. **自癒**：旗真但 `#mask` 冇開緊＝上次呈現已死 → 清旗照呈現；旗真且有 modal 開緊＝真呈現中，照舊回 false。呈現鏈全程同步（掣 on→cont→step→PresentOne→modal），冇合法嘅「旗真＋mask 關」空窗。
2. **拋錯隔離**：`step()` 包 try/catch，PresentOne 拋錯 → 剔走壞單，續呈現其餘到期單，旗唔 strand。
3. **done 冪等**：`done()` 加一次性守衛，continueFn 只行一次。

**舊檔補掃**：load 路徑本身已覆蓋——旗係 session 變量（reload 即重置），`enterHome` 已有到期補呈現（v20a91），晨鏈每日行；自癒之後任何 strand 都會喺下一次晨鏈／入屋自動恢復，唔使另加掃描。

**驗證**：函數級 harness 7 項（strand 自癒／modal 開緊唔搶／閂後補呈現／拋錯剔單／正常路徑／未到期唔呈現／continueFn 一次）＋真駕逾期 pending 晨鏈呈現（aud91Log +1、pending 清）。

## ② N9／N12 標籤授予來源＋舊檔回填

**問題**：STORY_GATE_3Y N9 tagAny 含 tag_comedy／喜劇細胞／tag_action／身手好，N12 含 tag_action／身手好；但 `S.castingTags` 全 code 冇授予路——`applyGigTagOnComplete` 只讀 `gig.tagOnComplete`，而全庫 323 張通告冇一張有 tagOnComplete，標籤只嚟自主線 choice effects.tags（14 種冇一隻中）。E1 結構上不可達（W5 真玩：602 日 59 部作品零授予）。

**修法**（`applyGigTagOnComplete` 擴充＋新函數，殺青呼叫點不變）：
- 按完成作品 genre 授予：喜劇→`tag_comedy`「喜劇細胞」；動作／武俠→`tag_action`「動作好手」；roleLabel「動作替身」同樣授予 tag_action（含 2 張靈異驚慄替身工）。映射表 `GIG_GENRE_TAG360`。
- **任何級別完成即授予**（包括臨記級）：標籤係業內印象，唔係成就——臨記做過喜劇組都留低印象。庫存量：喜劇 48 張（臨記＋初級 32 張，早期可達）、動作 22＋武俠 14 張。
- 授予經既有 `applyCastingTags` sink（去重、弱印章、雙軌 delta 跟 registry：tag_comedy 聲望 +1 遞減帶、tag_action 聲望 +1＋信用 delta +1，一次性）。
- gig 查找改用 `work59GigLookup`（全歷年庫，跨年殺青都搵到）。

**舊檔回填**（`castingTagGenreBackfill360`，掛 `normalizeSaveObj`＋`enterHome` 懶掃）：
- 由 `wrapHistory`＋`done_*` 旗反推已完成作品，按 genre 補授予；冪等（已有 id／label 唔重複，舊字串格式都認）。
- **唔套雙軌 delta**（唔追溯改數值），`from:"backfill360"`（標籤頁唔假裝有來源）。
- normalize 嗰陣年庫未載入 lookup miss 咗嘅，enterHome 再掃一次。

**驗證**：harness 13 項（授予／去重／label 跟 registry／文藝唔授予／替身／武俠／回填／唔改數值／冪等／N9·N12 tagAny 命中）＋真駕兩項（舊檔 reload 回填兩標籤、播種 shoot 殺青即時授予 tag_comedy）。

## ③ auto-plan 歌藝保底（訓練位輪替）

**問題**：`defaultWeekPlan` 訓練位（星期二）舊次序：演技未夠 2 堂→演技；已報歌藝且未夠 2 堂→歌藝；外貌未練→外貌；否則 scout_all（唔訓練）。跟預設計劃嘅玩家演技以外全部凍結（W1/W6 實測歌藝凍結 370 日）。

**修法**（`defaultWeekPlan` 內，第 1 週 base 同演技 bootstrap 不變）：
- 訓練位改輪替：候選＝已報名課程＋演技＋歌藝，揀**主屬性最低**嗰課（同分揀堂數少、再按固定次序 acting→vocal→stage→looks→charm→iq→stamina）。
- **歌藝未報名都排**：排程上堂（`resolvePlannedDay`→`train75ApplyLesson`）唔經報名閘，同演技 bootstrap 同一口徑（舊制演技未報名都照排）；舊註解「排咗都上唔到堂」與實作不符，今次跟實作。保證跟預設計劃玩一年歌藝有可見成長。
- 原則：每科都有可見成長，唔再有「夠 2 堂就停」嘅凍結點。

**驗證**：harness 8 項（bootstrap 保留／未報名歌藝最低→排歌藝／已報名最低屬性輪替×2／第 1 週不變／一年模擬：只報演技＋歌藝 → 歌藝 14→89、演技 18→85；全報名 → 六科全成長）。

## Suite

- 基線 v359：398 PASS／9 FAIL（九項 pre-existing：flash51／slot50／soft_tip_111_restore／start53／weave43_static／weave44_static／weave49_static／wf5_87／wrap38）。
- v360 首跑 389/18：9 項新 FAIL 全部係行號釘漂移（index.html 淨 +69 行）＋calib60 行為釘。
  - 行號釘 7 檔（text125／rom159／rom176／travel114／tang171／tang173／gift185）按 difflib 映射 resync，逐釘驗證內容逐字相同（`qa360/qa360_resync.py`），各檔加 v20a360 resync 頭註解。
  - calib60 兩檔行為釘按新行為更新（未報歌藝 → 照排 train_vocal，係 P0-3 有意改行為；static 改驗輪替機制標記）。
- 新增測試 `tests/test_p360_static.py`（13 項內容錨點，唔釘行號）→ suite 總數 399 PASS／9 FAIL（新測 +1 PASS，其餘同基線）。
- 跑完已還原 `qa296/derive296.json`。

## 驗證產物

- `qa360/qa360_harness.js`：函數級抽取 harness，28/28 PASS。
- `qa360/qa360_drive3.py`：真駕——舊檔回填（reload）＋逾期 pending 呈現。
- `qa360/qa360_drive5.py`：真駕——播種 shoot 殺青授予（N1–N5 標已做跳過強制播）。
- `qa360/qa360_resync.py`：行號釘 difflib resync（一次性，留檔備查）。
