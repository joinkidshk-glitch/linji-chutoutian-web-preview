# NOTES — v20a147 頒獎禮整改（D2 安慰場面＋gallery 做長做實／對手加權／D4 贏線校準）

- 分支：`v20a147`（工作副本 `~/workspace/linji-work147/`，基底 main `79defe3`）
- 狀態：code＋單元測試＋實駕已完成並驗證（drive147 5/5 PASS，見 §8）
- 唔開 PR、唔推 main（落地由統籌做）。SAVE key／softRev／`?v=` 一律無郁；無直改 content pack JSON。
- index.html：58744 → **58820 行（＋76 行）**（上一手 ＋67；D4 重做 ＋9）

## 1. 改動一覽（index.html）

### 任務 2 — D2 安慰場面＋gallery 宣佈弧
- `awards62CeremonyBeats`（約 L45990）：gallery 分支改行完整宣佈弧——open 1200＋pan 2000＋**names 2400＋suspense 1400＋reveal 2100**＋out 500 ＝ **9600ms ≈ 9.6 秒**（舊 3.7 秒）。唱名只列 fellows（唔列阿偉）；無 fellows 用通用行「入圍名單逐個唱出……」；reveal 得主＝fellows[0]（有星名＋作品），無 fellows 用通用 fallback「今晚嘅得獎者誕生——掌聲屬於台上嗰位。」；out caption 加「掌聲響起——今晚完滿落幕。」。
- nominated 加 **comfort beat**（reveal 之後、out 之前，2600ms）：caption「何生拍拍你膊頭：「差少少啫，唔緊要，下年再嚟過。」\n阿偉：「……嗯。下年，我要自己行上台。」」；唔加新 sprite；won／gallery 唔行呢段。nominated 總長 9350＋2600＝11950ms；won 唔變（9350ms，無海報；有海報＋glamour 1800ms）。
- `awards62PlayCeremony`（約 L46028）：`winFellow` 改做 `focus.winner63 || focus.fellows63[0]`（gallery 類別 winner63 係 null——`buildAwardResultPack` 只喺 nominated 嗰陣設 winner63——得主照 fellows[0] 規則取 fellows63[0]，等揭曉嗰陣得主行前；nominated／won 行為不變）。`draw()` 加 `comfort` case（企定人仔，玩家 alpha 1、得主 0.85、其餘 0.7）。`syncCards` 加 comfort（卡片維持 reveal 狀態可見）。跳過掣／try/catch 兜底無郁。
- 結果卡：`renderAwardResultHtml`（約 L45490）nominated 類別喺 weakHint 之後加一行 `<p class="psr-comfort147">何生：「差少少啫，唔緊要，下年再嚟過。」</p>`（鼓勵，唔重複 weakHint 診斷，唔話佢贏咗）。

### 任務 3 — 對手加權（加權隨機，唔係固定）
- `AWARDS63_POOL` 之後加 `AWARDS63_TIER_WEIGHT`（starId→權重 3／2／1，註解寫明來源係名冊巔峰年）：頂級 ×3＝陸柏言 `luk_baakyin`、蘇芷茵 `so_jiyan`、廖炳星 `liu_bingxing`、駱家聲 `lok_gasing`、葉敏芝 `yip_manji`（巔峰 1990–92）；上一代當紅 ×2＝麥震東 `mak_zhendong`、齊鎮海 `chai_zanhoi`、鍾楚凝 `chung_choning`（巔峰 1988–89）；過氣 ×1＝魏詠男 `ngai_wingnaam`、顧明輝 `gu_mingfai`（巔峰 1984–85）。池外星（程天諾等）唔入池。來源：`~/workspace/user/files/PLAN_ERA_STAR_TARGETS_v1.md` 紅星名冊巔峰年；巧遇設計檔無星級 tier 表（只有玩家級數鎖），所以用名冊巔峰年做 proxy。
- 加 `awards63KeySeed`（FNV-1a 32-bit）＋`awards63SeededRng`（mulberry32 類）＋`awards63WeightedPick(pool, used, rng)`（未用過嘅池星按權重抽一粒，缺值當 1，池抽乾返 ""）。
- `awards63Fellows`（約 L46447）第二輪改用加權抽：seed key＝`[year, ceremony.id, medium].join("/")`，逐個無主演 candidate 抽一粒；第一輪（片酬序）唔郁；得主＝fellows[0] 唔郁；唔用裸 `Math.random()`。

### 任務 4 — D4 贏線校準（重做；上一手 0.90 作廢）
- 上一手 0.82→0.90 只對理論檔校準，觀測分佈期望贏場數仍然 0.00，唔符合「正常實玩贏得到先至算驗到」，作廢。重做：`AWARDS62_WIN_LINE` 0.90→**0.875**（約 L45675，連註解）；wrapHistory 上限 30→**90**（約 L38055）；`awards62YearOf` 改 `wrappedDay` 日曆年優先（約 L45711）；`awardsScoreCategory` 註解同步 0.875。除數 1.6 唔郁。理據＋掃描詳見 `qa147/CALIBRATION_D4.md` §5（摘要見 §4）。新數字：觀測 E=0.54／9 場、頂級檔 57%、Y1 強 0%。

## 2. D1 核實——未完成（實駕被環境攔截）
- v136 已做旁聽報紙（`NEWSPAPER_AWARD_GALLERY_TEMPLATES_136`＋`award_gallery` 桶＋inline 測試，`NOTES_V20A136_GATE.md`）。v147 嘅工作係實駕證實。
- inline 測試本身已驗：gallery 桶 `fameDelta===1`、`templateEventKey==="award_gallery.film"`、headline+dek 唔含 入圍／提名／得獎／奪獎（`index.html` 約 L47974–47976）。
- 實駕腳本已寫好（`qa147/drive147.py`，case `gallery_932`／`gallery_700`／`nominated_932`／`skip_932`／`declined_932`；port 8971；browser launch 失敗會重試最多 6 次、每隔 15 秒，捱過寫入壞窗口；截圖／JSON 寫檔失敗唔中斷 case，結果照印 stdout）。
- **實駕跑唔到（環境，2026-11-13 01:25–01:33，兩輪共 12 次 launch 全部失敗）**：Chromium launch 即死（`TargetClosedError`，browser process SIGTRAP）。隔離測試：binary 獨跑 `--version` 正常（156.0.8078.4）；最簡 Playwright launch 一樣死；`--single-process --no-zygote` 過到 launch 但 `new_page` 嗰陣 renderer 撞死（trap #UD，stack trace 見 crash dump）；`--dump-dom about:blank` 零輸出（zygote `write: Broken pipe`）。同期可用記憶體只剩 **~430–480MB 且持續下跌**（free 135–180MB；hatch daemon 353MB RSS；另一 agent 跑緊 `/tmp/dl.py`），renderer 極可能因分配失敗 CHECK 而 trap——同 v136 當日 drive136 跑得順比較，係環境變咗，唔係 game code 問題。
- **已完成（2026-11-13，見 §8）**：環境恢復後 drive147 跑到，**5/5 PASS**——旁聽報紙＋推辭報紙＋安慰場面全部實駕證實。第一輪 1/5 係三個 harness bug（已修，只郁 drive147.py），唔係 game code。

## 3. 對手加權分佈（`tests/test_awards63_logic.js` §147，枚舉 2000 粒 seed，首抽頂級星佔比）
| 媒介 | 頂級星佔比（實測） | 理論值 | 均勻分佈 |
|---|---|---|---|
| film | **63.6%** | 64% | 50% |
| tv | **60.1%** | 60% | 50% |
| music | **84.9%** | 86% | 67% |
| ad | **59.8%** | 60% | 40% |
理論值：film 頂級 (3+3+3)/14、tv (3+3)/10、music (3+3)/7、ad (3+3)/10。

## 4. D4 模擬＋校準（重做；詳見 `qa147/CALIBRATION_D4.md` §5、模擬 `qa147/sim147b.js`＋`qa147/sim147b_out.txt`）
- **上一手 0.90 作廢**：只對理論檔校準（0.882 檔 P=32%），觀測分佈期望贏場數仍然 0.00。重做以觀測到嘅真實全弧分佈做校準對象。舊 0.90 表留低做對照（見 CALIBRATION_D4.md §3）。
- 樽頸（已量化）：① wrapHistory 上限 30 擠走三部 0.74 代表作（day 609 桶 2 部、base 0.694；窗口 30→60 升到 0.879）；② 計數 vs 計分年份口徑唔同（35 部 pack≠cal，全係橋接工；計數用日曆年，計分用 pack 年；對齊獨立效應：WIN 30 下 day 609 0.694→0.778）。postShootRewards 唔係逃生口（同樣截 30，entries 係獎勵 packs，冇質量數據）。窗口讀取審計逐項見 CALIBRATION_D4.md §5.1——上限 90 只會加長個 list，所有讀取只會更準。
- 掃描：WIN（30／60／90／999）× DIV（1.6–1.2）× YEAR（pack／cal）× L（0.82–0.90）。通過驗收得兩族（31 個組合）：A 族 DIV 1.6／1.5／1.4、WIN≥60、L=0.875（E=0.54）；B 族 DIV 1.2、L=0.885／0.89（E=0.74／0.59）。揀 A 族 DIV 1.6：DIV≤1.4 會抬 Y1 強（26%）／Y2 中（39%），DIV 1.2 仲會殺死桶深度設計（wsum 喺 1.2 已封頂）。贏線 0.875 係唯一可行中點（可行窗 [0.872, 0.879]）；上一手 §2「改權重只會成體下移」已修正——除數 1.6→更細係薄桶升近封頂，唔係成體下移。
- 觀測分佈新舊對照（入圍 6 場 base）：舊 [0.435, 0.748, 0.748, 0.655, 0.739, 0.694] E=0.00 → 新 [0.435, 0.748, 0.748, 0.655, 0.739, 0.879] **E=0.54**。
- Synthetic 新舊對照（P(win)，舊 L=0.90 → 新 L=0.875）：Y1 強 0.800：0%→**0%**；Y2 中 0.821：0%→**0%**；Y2 thin 0.741：0%→**0%**；Y2／Y3 擔正 0.882：32%→**57%**；Y3 擔正但專攻 0.820：0%→**0%**；理論完美檔 0.900：50%→**75%**。
- 脆弱性：E=0.54 全靠 day 609 單一場次（P=0.54）；margin 得 0.04；下次全弧最佳場次低過 0.879 會再跌穿 0.5——嗰陣要第二個強場次，唔係再調條線。門檻行／standing／weakHint 唔使改（gapWin 動態計）。

## 5. 測試
- 上一手更新檔：`tests/test_awards62_logic.js`（§2 邊界改寫：新邊界檔 base **0.92**；§6 beats：gallery 約 9.6 秒＋6 beats＋唱名唔列阿偉＋揭曉唔寫阿偉＋無 comfort；nominated 有 comfort beat 2600ms、reveal 之後 out 之前、文案有何生＋阿偉、唔話贏咗、全長 9350＋2600；得獎無 comfort）、`tests/test_awards63_logic.js`（§147 加權分佈＋同一 key 同一 pick＋唔抽已用星＋池抽乾返 ""＋權重表齊晒池內 10 星；§3 兜底改加權隨機，確定性斷言保留）、`tests/test_awards62_static.py:29` 同 `tests/test_awards63_static.py:107` 硬編 0.82 → 0.90、63_static 加 beats 靜態檢查（gallery 宣佈弧、comfort beat、加權三件套）。
- **D4 重做更新檔**：`tests/test_awards62_logic.js`（§2 文案 0.90→0.875；**新增 §9**：WIN_LINE 0.875 pin；§9a 窗口——33 部歷史舊 30 模擬 base ≈0.499、代表作跌返「臨記工」，全量 base ≈0.82、代表作「大製作」；§9b 年份口徑——pack 1990＋1991 殺青 → YearOf 1991、入 1991 桶 base 0.6625、唔入 1990 桶 base 0.40，反向同 fallback 兩級都 pin）、`tests/test_fix65_logic.js`（fixture `wrappedDay` 改 `(year-1990)*365+100`；加 eval 真 `awardsCalendarYear`＋`awardsYearFromDay`；**新增 §6**：WIN_LINE 0.875、YearOf 橋接個案、橋接工入殺青年份桶／唔入 pack 年份桶）、`tests/test_awards62_static.py:29`／`tests/test_awards63_static.py:111`／`tests/test_fix65_static.py:81–82`（贏線 pin 0.90→0.875；fix65 註解誠實改寫——「唔係放水，係修樽頸＋重設線」，上限 pin `length>30`→`length>90`）。
- 受影響 11 檔全部 PASS：62_logic、62_static、63_logic、63_static、64_chibi_static、64_static、78_edition、fix65_logic（38 pass, 0 fail）、fix65_static、ladder95_logic（39 passed）、ladder95_static。
- Pristine 反證（工作副本真測試檔對 `~/workspace/pristine147real/`）：62_logic **FAILED 13 項**；fix65_logic 34 pass, 4 fail（WIN_LINE＋§6 三項）；62_static 1 FAIL；63_static 5 FAIL；fix65_static 2 FAIL（贏線＋上限 90）——全部乾淨。註：62_logic §9a 窗口測試喺 pristine 都 PASS（計分本身唔截斷，cap 係由 fix65_static pin 嘅），檔案整體喺 pristine 照樣 FAIL。
- 回歸修復：上一手（v147 ＋67 行漂移）`tests/test_venue99_logic.js`（gallery beats 斷言改 6 beats 新結構）、`tests/test_fix65_static.py`（贏線 pin 0.82→0.90，附 D4 校準註解——重做已改寫做 0.875＋誠實註解）。**D4 重做（＋9 行漂移）**：`tests/test_travel114_static.py`——寫咗 `qa147/resync_travel114.py`（difflib 對位；第一版有 bug——EDITS 入面 YearOf 新字串截斷咗，令重建檔案短咗一行、映射成 +10；已修正為完整字串，重跑核實淨 +9、44 個 openLoc 呼叫點逐字一致）。更新 pin：DEF 53469→**53478**、WRAPPER 44087 不變；COUNT 13 處中 5 處＋9（57499→57508、57666→57675、57809→57818、57830→57839、58280→58289），其餘不變；FREE 27 處中 15 處＋9，其餘不變；加咗 resync 註解行。travel114 而家 **PASS**。

## 6. 全套對照——零回歸（FAIL 清單同真正 baseline 一致）
- 真正 baseline（`qa147/suite_baseline147real.txt`，`~/workspace/pristine147real/` 584M，232 測試檔齊）：**207 PASS / 12 FAIL**（12 個 pre-existing FAILs，同 v147 無關）。注意：舊 `qa147/suite_baseline147.txt`（219/0）係假——`/tmp/pristine147` 入面測試檔全空（/tmp 爆滿致 tar 失敗），唔好再引用；`/tmp/pristine147` 已刪。
- 工作副本全套（pipe-based，`qa147/run_suite_pipe.sh`——stdout 經 pipe 唔寫 `/tmp/suite_one.log`，免受寫入攔截影響；結果 `qa147/suite_work147_pipe.txt`）：**207 PASS / 12 FAIL**，FAIL 清單同 baseline 逐項相同（`test_flash51_static.py`、`test_giglib36_static.py`、`test_pacing35_static.py`、`test_poster59_static.py`、`test_rumor49_static.py`、`test_slot50_static.py`、`test_soft_tip_111_restore.py`、`test_start53_static.py`、`test_weave43_static.py`、`test_weave44_static.py`、`test_weave49_static.py`、`test_wrap38_static.py`）——**零回歸**。
- 上一手 200/19 嗰 7 檔 tempfile FAIL（`test_bust109_static.py`、`test_dlg107_static.py`、`test_dlg119_static.py`、`test_dlg123_static.py`、`test_dlg126_static.py`、`test_dlg127_static.py`、`test_dlg138_static.py`）而家喺工作版同 baseline 都 PASS——環境寫入攔截已緩和（見 §7），唔係回歸修復。
- 作廢記錄：`qa147/suite_work147.txt` 曾經有兩個 file-based 跑數——204/15（修復 3 個回歸之前）同 98/121（跑途中撞正壞窗口，成批 Python 測試 stdout 寫檔失敗 exit 120）。上一手 pipe-run 200/19 亦已由今次 207/12 取代。

## 7. 環境寫入攔截（2026-11-13 01:09 HKT 起，間歇性，現已緩和）
- 現象：exec 進程寫入檔案內容被拒——`os.open(O_CREAT)` 成功（檔案建立到，0 bytes），`os.write()` 擲 `PermissionError [Errno 1] Operation not permitted`。影響全部路徑（/tmp、/var/tmp、/home/hatch、/dev/shm）；metadata 操作（touch／rm／mkdir）正常；`muse.write`／`muse.edit` 工具路徑正常。
- 證據：`python3 -c "open('/tmp/x','w').write('hi')"` 表面成功但檔案 0 bytes（緩衝 IO 喺 shutdown 靜默吞咗失敗）；unbuffered `os.write` 直接擲 EPERM；`tempfile.gettempdir()` 全部候選目錄都失敗；另一 agent 同期跑嘅 7 個 `one_test_*.log`（/tmp，17:18）全部 0 bytes。
- 後果（上一手）：① 全套 7 個 tempfile 測試 FAIL（pristine 同樣 FAIL，見 §6）② Playwright 實駕跑唔到——Chromium launch 即死（見 §2；`--user-data-dir=/tmp/playwright_chromiumdev_profile-*` 寫唔到係其中一個因素，但最簡 launch 喺好窗口下一樣死，同期記憶體壓力（可用 ~430MB）先係主因）。**攔截係間歇性**（strace 證實 `write(2)` 直接返 EPERM；好窗口可以維持幾十秒，壞窗口又可以維持幾分鐘；pipe（stdout）唔受影響，所以 pipe-based 全套跑到 200/19）。drive147.py 已加 launch 重試（6 次 × 15 秒），兩輪 12 次全部失敗。
- 已做嘅緩解：刪咗壞嘅 `/tmp/pristine147`（247M，/tmp 由 64% 用量清到 16%，434M 空位）——唔係容量問題，攔截依舊。/tmp 其餘舊檔（live*.html 等）屬其他 session，唔郁。
- **更新（2026-11-13 D4 重做時段）**：攔截仍然間歇性出現——sim147b 首次 exec 寫檔撞 EPERM（`qa147/sim147b_out.txt` 建咗但 0 bytes），之後重跑寫檔成功（檔案而家完整）；同一時段 node 寫 `/tmp/wp147.txt` 成功。7 檔 tempfile 測試全部回復 PASS（見 §6）。記憶體仍然緊（free 124MB、available 660MB），但 Playwright 最簡 launch 而家 PASS（見 §8）——上一手 12 次 launch 全死嘅 SIGTRAP 狀態已恢復，至少喺今次窗口。

## 8. 實駕——5/5 PASS（2026-11-13，環境恢復後跑到）
- 腳本：`qa147/drive147.py`（沿用 `qa136/drive136.py` 模式；port 8971；cases：`gallery_932`／`gallery_700`／`nominated_932`／`skip_932`／`declined_932`）。每 case 量度每 beat 時長＋總長、結果卡、翌日報紙、邀請出席／推辭、0 pageerror／0 failed request、截圖放 `qa147/shots/`。
- 環境恢復：最簡 Playwright launch PASS（上一手 12 次 launch 全死嘅 SIGTRAP 狀態已過；可用記憶體仍緊，660MB）。第一輪 `all 932` 跑到（~570 秒，6 attempts）：**OVERALL 1/5 PASS**——只得 skip_932 過；其餘 4 個 case 全部係 **harness bug，唔係 game code**（遊戲行為本身喺輸出證據入面全部啱）：
  1. `nominated_932` 用錯 forceTier 字串：driver 傳 `"nominated"`，遊戲 `awardsEvalTier` 只認 `"gallery"`／`"nominee"`（index.html L45103；inline test 都係用 `"nominee"`）——pack 跌返 gallery，comfort 路徑完全冇行到。
  2. `paper_queued_next_day`：字串 `in` dict list，永遠 False（queue 入面係物件，唔係字串）——declined 報喺 after_decline queue 入面明明有齊 template／fameDelta。
  3. `paper_for_ceremony` 嘅 clipped 來源：`clipItems` 嚟自 `S.newspaperClippings[].items`，但遊戲剪報物件根本無 `.items`（得 `eventKeys` 字串陣列）——clipped 永遠空；next-day queue 已經排走，presence check 無路可 pass。
- Harness 修正（只郁 `qa147/drive147.py`，game code 一字唔郁）：① forceTier `"nominated"`→`"nominee"` ② paper_queued_next_day 改 `any(q.eventKey == key)` ③ `paper_for_ceremony` 加 `key in clippings` 當已剪存 ④ gallery／declined 加 advance 前 snapshot（報喺典禮完結嗰刻入 queue，publishDay=翌日，advance 之後先攞唔到原物件）——`gal`／`dec` 優先用 pre-advance queued 原物件，next-day clippings 做送達證明。
- 第二輪 `all 932`：**OVERALL 5/5 PASS**（一次過，~97 秒，0 retries，全部 0 pageerror）：
  - gallery_932：19/19——宣佈弧總長 9278ms（約 9.6 秒）、6 beats 唱名唔列阿偉、揭曉廖炳星、結果卡無贏 claim；翌日報紙 template `award_gallery.film`、fameDelta 1、headline／dek 無入圍／提名／得獎／奪獎（「維港影藝獎之夜 阿偉台下見證新面孔誕生」）。
  - gallery_700：19/19（總長 9298ms）。
  - nominated_932：12/12——**comfort beat 首次實駕驗證**：reveal（t=6398）之後 comfort（t=8566，長 2626ms ≈ 2600ms），文案有何生＋阿偉、唔話贏咗；總長 11665ms（約 12 秒）；結果卡 comfort 行逐字啱。
  - skip_932：5/5（skip 後 829ms 舞台消失，結果卡照出）。
  - declined_932：9/9——推辭後 flag skipped、pending 清空、報即時入 queue（template `award_declined.film`、fameDelta 0、唔寫阿偉），翌日見報＋入 clippings。
- 附帶觀察（debug 強制路徑 only，唔係本票範圍）：nominated 強制包嘅請柬 body 仍然顯示「仲差 2 部電影作品先夠入圍（而家 0/2）」——body 文案由計數門行，唔跟 forceTier；「席位：入圍／提名」嗰行啱。真實路徑（夠 wraps 先入圍）唔受影響。
- D1 核實完成：旁聽報紙（gallery）＋推辭報紙（declined）實駕證實。D2 安慰場面實駕證實。

## 9. 檔案
- 改動：`index.html`（＋76 行）；測試檔——上一手：`tests/test_awards62_logic.js`、`tests/test_awards62_static.py`、`tests/test_awards63_logic.js`、`tests/test_awards63_static.py`、`tests/test_fix65_static.py`、`tests/test_travel114_static.py`、`tests/test_venue99_logic.js`；D4 重做再改：`tests/test_awards62_logic.js`、`tests/test_awards62_static.py`、`tests/test_awards63_static.py`、`tests/test_fix65_logic.js`、`tests/test_fix65_static.py`、`tests/test_travel114_static.py`
- 新增：`qa147/drive147.py`、`qa147/CALIBRATION_D4.md`、`qa147/sim147.js`、`qa147/sim147_out2.txt`、`qa147/sim147b.js`、`qa147/sim147b_out.txt`、`qa147/resync_travel114.py`、`qa147/suite_baseline147real.txt`、`qa147/suite_work147.txt`、`qa147/suite_work147_pipe.txt`、`NOTES_V20A147_AWARDS.md`（本檔）
- 已廢棄：`qa147/sim147.py`／`qa147/sim147_out.txt`（舊模擬，數字錯）／`qa147/suite_baseline147.txt`（假 baseline）
- `git status`：M index.html＋8 個測試檔；未追蹤 `NOTES_V20A147_AWARDS.md`、`qa147/`、`samples147/`（後者非本票產物——另一 agent 嘅頒獎場景樣本，16:39–16:47）
