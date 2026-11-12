# v20a110：通告級別與要求脫節（OVR110）——完成交代

- **合併**：squash merge 入 main，commit **`b218966`**（「v20a110：通告級別 vs 要求對齊（normalize 層 id 對照表，273 張觸及；test_travel114 行號再實量）（squash）」）。分支 `v110-gigreq`（由 main `8e9e773` 開，rebase 後最終 `0d054fd`，已 push origin）。
- **線上核實**：GitHub Pages 已部署，線上 `index.html` 同本地逐 byte 一致——**5,121,987 bytes，sha256 `d1c8fceae5a86729d06c12c13beafb90e47a6e9c8b50993b615ac09605734201`**（curl 核實；第一次 curl 攞到舊版 5,099,919 bytes，約 90 秒後部署追上再 curl 即對上，唔使重觸發）。

## 改動（index.html，+16 行，零刪改原有行）

- `normalizeGigRecord` 之前貼入 `ovr110_snippet.js` 全文（`TIER110` 96 id、`REQ110` 246 id、`ovr110Apply(o)`；`null`＝剔走該要求項；冪等），`normalizeGigRecord` 內 NAME93 呼叫之後加一行呼叫。唔改 content pack JSON、唔改 SAVE key／softRev／`?v=`。
- 觸及去重 **273 張**（96＋246−重疊 69）。審計 §1「281 張」係筆誤，唔好抄。
- 要求帶（六主屬性最高要求）：初 0–40／中 41–110／高 111–200。升 tier 27 張（初→中 23、初→高 1、中→高 3）、降 tier 69 張。清單見 `NOTES_V20A110_IMPLEMENT.md` §6。
- 和音家族：夜更和音 {vocal:10}、新春大合唱 {vocal:15,stage:15}、鬼馬夜更和音 中→初 {vocal:10}、賀年大碟和唱 中→初 {vocal:20,stage:20}（理據見 IMPLEMENT §4）。
- 重要更正：見報分類器跟角色文字，唔跟 tier——升 tier 唔會自動除「臨」印；只有《櫥窗》過場模特 `gig_1990_film_01`（初→中）例外，標題有「過場」二字，升中後「臨」印不變，唔係 bug（IMPLEMENT §5）。
- 審計＋改動表＋實作細節：工作目錄 `~/workspace/linji-work110/`（`audit110.md`、`req_overrides110.json`、`tier_overrides110.json`、`ovr110_snippet.js`、`sim110.js`）；實作紀錄 `NOTES_V20A110_IMPLEMENT.md`（121 行，喺 main）。

## Rebase 紀錄（三輪，全部喺 `~/workspace/linji-work110-repo` worktree 做；主 clone 當時 checkout 緊其他分支，冇掂過）

1. `8e9e773` → `41e4be8`（v111 入 main）：**零衝突**，commit `67ac16f`。
2. `41e4be8` → `2d71588`（v112 圖標／v113 閘／v114 出行額度／v115 卡文入 main）：**零衝突**，commit `4dda5bb`。
3. `2d71588` → `aeec7a5`（v117 詳情區刪除／v116 老闆立繪換入）：**1 個衝突**，喺 `tests/test_travel114_static.py`——v117 刪詳細區（淨 −93 行）之後已再實量過嗰檔嘅釘行號，同我嘅 +16 再實量撞車。解法：取 main 版（v117 實量）做底，再將 OVR110 嘅 +16 套上去（行號 ≥32183 者 +16，<32183 不變；最近釘行 30269／34824，中間冇釘行）；順手修埋 v117 版 WRAPPER 註釋手民之誤（`__phase43233`→`__phase2`）。解完即跑該測試 PASS（免費 27＋計數 13＋定義 4，全部對上）。commit `ca095d5`＋`0d054fd`。
- Squash 方式：main 喺主 clone 被佔用，worktree 唔可以 checkout main，改用 plumbing——`git merge-tree --write-tree origin/main v110-gigreq` 得出嘅 tree 同分支頭 tree 完全一致（`199eab8…`），再 `git commit-tree`＋push `HEAD:main`。內容同分支逐 byte 相同。

## 全套測試 A/B（最終輪，基線＝最新 main `aeec7a5` pristine）

| | PASS | FAIL |
|---|---|---|
| 基線 `aeec7a5` | 155 | 12 |
| 分支 `0d054fd` | **157** | **12** |

- ＋2＝兩隻新 v110 測試（`test_gigreq110_logic.js` 45 項、`test_gigreq110_static.py` 22 項）；FAIL 清單逐字相同（12 個全屬已知環境性 static FAIL：`test_flash51_static.py`、`test_giglib36_static.py`、`test_pacing35_static.py`、`test_poster59_static.py`、`test_rumor49_static.py`、`test_slot50_static.py`、`test_soft_tip_111_restore.py`、`test_start53_static.py`、`test_weave43_static.py`、`test_weave44_static.py`、`test_weave49_static.py`、`test_wrap38_static.py`），**零新增回歸**。Log：`~/workspace/linji-work110/qa110/baseline3/`、`branch3/`（中間輪 2d71588：154／12→156／12，同樣零回歸，log 喺 `baseline2/`／`branch2/`）。
- 中途插曲：第二輪 rebase 後分支一度 155 PASS／13 FAIL——多出嚟嘅 `test_travel114_static.py` 唔係 v110 邏輯回歸，係嗰隻測試釘死絕對行號，OVR110 加 16 行令釘行號移位（內容本身 27＋13＋4 全部啱）。修法係將釘行號再實量 +16（見上面 rebase 第 3 輪），修完 156／12。教訓：行號釘死嘅 static 測試，任何上游插入都會打爆佢——將來改 index.html 要預咗再實量。

## 實駕（Playwright，`~/workspace/linji-work110/qa110/drive110.py`，最終 run 12，對住分支 `0d054fd`）

- **20／20 checks PASS，零 pageerror**。Log `qa110/drive_log110.json`、`qa110/drive110_stdout.txt`。
- 兼容：基線 main `aeec7a5` 新遊戲→槽 3 存檔（money 110110／dayIndex 3／flags.qa110mark）→分支繼續→標記原樣還原 PASS；指紋 `OVR110` 基線 False／分支 True。
- Day-0 全板可接 **20／20**，逐地點全部啱 sim：rec_hk 2/8、tvb_longmen 3/12、film_lion 1/10、film_cotton 1/8、film_harbour 1/8、tvb_harbour 2/8、tvb_kowloon 1/8、ad_central 2/9、ad_adm 2/8、rec_wanchai 1/8、rec_star 4/7。
- 第 2 週 rec_hk 梯子（真 UI 讀板）：S0 零訓練 **2/8**（夜更和音＋錄音室拍板）；S1 真實歌藝上堂一堂後 **3/8**（＋新春大合唱；上堂實測 vocal 14→20（+6）、trainCount 1）；S2 **3/8**；S3 **4/8**（＋賀年大碟和唱，三張和音全開）。
- 升 tier 抽查：`window.GIGS` 核實 `gig_1988_ad_02`／`gig_1988_var_01` tier 均為「中」；day-0 fame 5 時兩張都鎖住、印 `seal_mid.png` alt「中」；ad_02 gap 行明寫「聲望 5／需 16（差 11）；外貌 22／需 45…」；設 fame 20／looks 50／charm 40／acting 35 後 ad_02 入可接區、印「中」。詳情頁見 S-30 老闆「方樂怡／金鐘創意 · 老闆」、要求格全部 ✓、期間／完成期限／報名截止拆行、簽約金「（獲聘後即收）」（v115 行字）。
- 《櫥窗》`gig_1990_film_01`：tier 中、roleClass base、badge {key:'extra', label:'臨'}，PASS（見報印跟內容，唔跟 tier，唔係 bug）。
- 截圖：`qa110/shots/`——`board_day0_<11 地點>.png`、`map_day0.png`、`compat_before_saved.png`、`compat_after_restored.png`、`ad02_locked.png`、`ad02_ready.png`、`ad02_detail.png`、`var01_locked.png`、`rec_hk_S0.png`、`rec_hk_S1.png`、`rec_hk_S2.png`、`rec_hk_S3.png`。
- 實駕教訓（已入 `drive110.py` 註釋，後人實駕留意）：
  - 歌藝 L1 一堂主加成 **+4~6 隨機**，唔係固定 +5（run 8 係 18、run 5/6 係 19、run 10/12 係 20）；S1 驗收要收 18–20，唔可以死咬 19。S1 板面亦唔可以死咬 3/8——頂 roll（vocal +6）＋附帶增益撞正，第 3 張和音會提早開，3/8 同 4/8 都合法；驗收改做 ready 3–4／8＋新春大合唱在內。
  - 上堂後嘅日結 modal 掣全部會行下一日：settle 通用 fallback 絕對唔撳「開始今日行程」／「加速本週剩餘」／「回家結算」；上堂後只撳純 dismiss 掣（好／我知道了／知道了／確定／確認），剩低嘅交畀 settle（識撳 `.sp-next` 播完故事 modal）。
  - 清 `S.weekPlan` 做自由日嗰陣，要連 `S.weekPlanWeek37` 一齊設做當週（`Math.floor(S.dayIndex/7)+1`），否則遊戲見到舊戳會用 `defaultWeekPlan()` 蓋返預設 plan，日程連鎖反應（報紙反響／剪報／週末回家結算）會阻住開板。
  - v114 出行額度已入 base：實駕每次開地點前重置 `S.travel114.used = 0`（逐地點獨立量度；額度機制本身由 v114 實駕驗過）。
  - HTTP cache 304 陷阱：換 server 後重用舊 query 會攞返舊 index——每次 goto 用全新 query＋`OVR110` 指紋驗證。
  - `#loc-sheet` 關閉時 base CSS 仍係 `display:flex`，可見性唔可以用 offsetParent 判，要睇 classList 有冇 `on`；modal 開合判據係 `#mask.on`。

## 殘留缺口（今包唔包，另票；詳見 IMPLEMENT §8）

1. 審計數字筆誤：audit §1「281 張」錯，實數 273 張。
2. 內嵌 fallback 11 張 req 差異未處理（`index.html` 內嵌 GIGS 137 張有 11 張 req 同 pack 唔同）。
3. 片酬／工期異常 9 項另票（例：`rec_hk_autumn` 雨夜街頭主唱 $3,900／13 日高級主唱太低；`film_harbour_summer_high` 動作特約 $41,900／25 日落咗中級）。
4. 文案殘留：「特約男主」`film_harbour_high` 名不副實；`tv_06`／`tv_07` synopsis 入面「臨記」字眼同中級定位有輕微出入。
5. 死內容 103 張（`gigs_1991.json`／`gigs_1992.json` 永不載入；改動表有佢哋 37 張，等加年先生效）。
6. 聲望第二閘：中要聲望 ≥16（約第 10–13 週）、高要 ≥32（約第 20–24 週）——設計原意，唔係 bug。
7. Day-0 20 vs 目標約 14：+6 全部入門初工，可接受；唔建議壓返 14。
8. B-raise 判斷：1991／92 pack 中／高通告原 req 全部細碼（20–36），成批升去中帶／高帶——跟驗收標準做嘅判斷，唔係逐張內容判斷。
9. 1990 高級後移：1990 年 29 張高級工最平都要 106 堂，實質第二年先開到。
10. C 類原先係 0；B-raise 後有 5 張變咗 C，生成器已用副項預算夾返落去，覆核清零。
