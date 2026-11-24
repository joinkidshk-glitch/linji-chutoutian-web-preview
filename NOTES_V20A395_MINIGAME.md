# NOTES_V20A395 — 殺青「最後一 take」小遊戲 prototype（v395）

## 1. 做咗咩（已做完）

殺青「最後一 take」場景兩個機制，prototype 範圍，唔係正式實裝。設計依據
`~/workspace/linji-minigame-ui-design-2026-11-24/gpt/plan_round2_part1.md`＋
`cue/gemini/design_cue.png`、`rhythm/gemini/design_rhythm.png`（場記板黑底軌道、
粉筆 X 走位圖、劇本紙、五線譜軌道、四級判定金星／藍圈／灰半圓／紅叉）。

### 機制 1：Cue 點走位（`?minigame=cue`）
- 走位圖（俯視片場）：拖「偉」圓圈（60px）去 2 個紅粉筆 X 記號（36px 吸附半徑），到位變金＋「到位」。
- 4 條場記板軌，Cue 點逐個出：外圈 100px→40px 縮 1000ms，目標時刻分別係開局後 1500／2900／4300／5700ms。
- 判定窗：完美 ±80ms／良好 ±80–250ms／普通 ±250–500ms／失手（>500ms 或無撳）。
  註：「普通」±250–500ms 係本票補充（設計稿只寫完美／良好窗；四級都要掂得到，先有普通格）。

### 機制 2：對白節奏拍點（`?minigame=rhythm`）
- 殺青場戲 5 句對白（廣東話對白；其餘 UI 字書面語）變節奏軌，音符由右滑入 28% 處拍點線，
  提前 1800ms 入場；拍點分別係 1600／3100／4600／6100ms，第 5 句係長音 7700ms、時長 1600ms。
- 撳「撳」掣（64px 高）或撳軌道判分，同一判定窗；長音要按住 ≥80%（1280ms）先算完成，
  夠 80% 即判（按按下時機分級），早放手＝失手＋「再長點」。
- 劇本紙逐句標色（已說灰／當前黑粗／待說淡灰），長音填充條有 80% 紅線。

### 共通
- 結果畫面只顯示四級計數＋走位／長音行，寫明「試玩版：結果只作顯示，唔會寫入聲望、信用、片酬或好感。失手唔扣分，跳過照原獎勵。」
- 跳過掣左下 60×44px，一撳即離開，殺青獎勵照常結算。
- 方向二「紙本手帳 · 實物劇組」：米紙底、場記板、試玩版紅印；直向手機、單手操作。
- `window.__mg395` 係實駕用 debug handle（kind／時間軸／已判數），唔係遊戲邏輯。

## 2. 點入（用戶試玩指南）

### 直接試玩入口（唔使打通成局）
- Cue：`https://joinkidshk-glitch.github.io/linji-chutoutian-web-preview/?v=20a10&softBehaviorGate=1&softRev=s107&minigame=cue`
- Rhythm：同上，`&minigame=rhythm`
- 開頁 load 後即彈小遊戲；玩完撳「完成」返標題畫面，跳過掣左下角。

### 殺青觸發（邊度觸發、邊幾張通告）
- 殺青完成嗰陣，日結板撳「繼續」（開始今日行程）之後彈出，玩完／跳過先出殺青獎勵頁（傳媒・街外・成績），再返地圖／下一日。
- Allowlist 只得 3 張（全部 1990 年臨記級電影通告，開局數值接得到，唔係主線強制通告）：
  - `gig_1990_film_204` 戲院散場路人（春，1 日，req {}）
  - `gig_1990_film_205` 大排檔夜市群演（夏，2 日，req {}）
  - `gig_1990_film_206` 碼頭貨櫃場搬運工人（秋，3 日，req stamina 55；開局體能 75）
- 殺青輪換：同一頁 load 入面，第一單彈 cue、第二單彈 rhythm、如此類推（`minigame395PickKind`；
  每局 reload 計數器重置，首單一律 cue）。週加速嗰陣唔彈（加速路徑唔經鉤子）。
  同一單同一日只彈一次（`window.mg395DoneKey395` 去重）。

### 點玩／點跳過
- Cue：拖「偉」去紅 X；圓圈縮到最細嗰陣撳嗰條軌。
- Rhythm：音符到白線嗰陣撳「撳」；長句 ♫ 按住唔放，到紅線（80%）先放手。
- 跳過：左下角「跳過」掣，獎勵照常。

## 3. 實裝方式（點解咁做）

- 小遊戲本體獨立檔 `minigame395.js`（自帶 CSS 注入＋load 自啟），`index.html` 只加兩處：
  1. 檔尾 `<script src="minigame395.js"></script>` 一行；
  2. `resolvePlannedDay` 鉤子三行（等行數寫法）：記低殺青 `gigId／title`，`afterDayRes`
     攔截——合 allowlist 先開 game，`onDone` 行原獎勵鏈（`presentPendingPostShootReward → cont`）。
- 咁做令 `index.html` 淨 +1 行，釘行零漂移；resync 只係總行數鏈（見 §5）。
- 鉤子揀 `afterDayRes` 嘅原因：佢係日結板所有繼續路徑（掣／撳外面 dismiss／休息卡）嘅唯一匯合點；
  週加速有自己嘅 `cont`，唔經 `afterDayRes`，所以加速唔會彈 game。
  檔案載入失敗嗰陣 `typeof` 守衛令遊戲靜默跳過，原流程照行。
- 冇改主線／結局／頒獎／排他鎖；冇改 SAVE key（`starVolunteer_map_v19w`）／softRev（s107）／
  產品 `?v=`（20a10）；冇改頒獎贏線 0.875；冇手改 source 年份；冇刪舊 code（新檔，無死 code）。

## 4. 驗證（實測數字）

### 新增測試
- `tests/test_v395_logic.js`：38 項全過（判定窗邊界 80／250／500、長音 799／800、allowlist、
  參數解析、輪換 cue→rhythm→cue）。
- `tests/test_v395_static.py`：62 項全過（鉤子接線、allowlist 庫內核實、觸控目標、
  獎勵零寫入守門——全檔掃描 21 個禁詞：applyGain60／bumpNpc／enc79OnWrap／
  end95AddWrap／contractCredit361OnWrap／S.fame／S.money／saveQ／localStorage 等全部無；
  另釘獎勵包喺 game 開之前已經建好兼派好）。

### 全套 suite
- `bash qa131/run_suite.sh`：**415 PASS／9 FAIL**；9 項全部係 v394 基線已知 pre-existing
  （flash51／slot50／soft_tip_111_restore／start53／weave43／44／49／wf5_87／wrap38），
  新 FAIL 係 0。跑完已還原 `qa296/derive296.json`。

### 實駕（Playwright，`qa395/drive395.py`，`qa395/shots/`，exit 0，零 page error）
- A cue 直接入口：4 完美、走位 2/2、撳完成返標題。
- B rhythm 直接入口：5 完美、長音完成（按住 1400ms ≥80%）。
- C 跳過掣：即刻消失。
- D 失手：唔撳 → 4 失手。
- E 殺青鉤子（播種 1 日 204 通告，N1 故事→抉擇→拍攝日結「殺青：戲院散場路人」→
  撳繼續→彈 cue→玩完（3 完美 1 良好，實時撳點抖動）→殺青獎勵頁→下一日）：
  玩 vs 跳過兩局，錢 $1200→$1242（+42 片酬）、人氣 3→8（+5）、weekGigsDone 1、
  gigCount 1、shootsLeft 0、done204 1——決定性數值全部一致。
- 聲望／壓力兩局有 ±1 差，係原系統隨機，唔係小遊戲造成（見 §6）。

## 5. Resync
- `qa395/resync395.py`：index.html 淨 +1 行（檔尾 script 標籤）。
  `test_tang171／test_tang173／test_gift185` 總行數鏈 ＋v395 +1（50511→50512）；
  `test_tail270` script 由 2 個變 3 個、檔尾加 src 行。其餘釘行一律唔郁（插入點喺檔尾）。

## 6. 新發現（已查明，唔係 bug，唔使修）
- **殺青獎勵聲望有 ±1 隨機**：`applyPostShootRewardDual` 派聲望＝
  `calib60FameGain(1＋Σ隨機抽卡 stageVolumeDelta)`，pack 喺殺青嗰刻
  （`queuePostShootRewardOnWrap`，日結板之前）已經建好兼即派；小遊戲喺撳繼續先至開，
  掂唔到。實駕 E1／E2 首輪聲望 14 vs 15、次輪 14 vs 14，就係抽卡唔同。
  壓力／演技兩局差 1–2 亦係原系統 `shootDailyDelta` 用 `R()` 抖動。
  對照斷言已改為只比決定性字段（錢／人氣／次數），靜態測試另釘 pack 行先次序。

## 7. 等拍板／未做（prototype 之外）
- 正式實裝嗰陣先決定：獎勵掛鈎（完美加咩）、鋪開去全部通告定維持 allowlist、
  難度（Cue 間距／音符速度）、用唔用真立繪／場景圖（而家「偉」字圓圈係佔位，
  設計稿阿偉立繪未接入）、音效／BPM 同步（而家無音樂，純視覺節奏）。
- Cue 局中段下方有空白（stage flex 撐高），prototype 可接受；正式版先排版執齊。
