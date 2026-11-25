# NOTES_V20A400_SCHEDULE_PRESETS

行程預設三項細改（用戶 2026-11-25 07:55 拍板；諮詢報告
`~/workspace/linji-schedule-consult-2026-11-23/REPORT.md` §③，GPT＋Claude 共識）。
基線 v399（main `137036e`，第七輪 UI 檢視頭五項）。

## 改動一覽（只做三項）

### 1. 預設唔再自動揀最低屬性課
- `defaultWeekPlan()`：第 2 週起訓練位（index 1）預填自由日 `scout_all`；第 1 週
  引導照舊（返 base）。刪走 v360 最低屬性輪替同演技堂數 <2 自動揀課兩個分支。
- 新 helper `lowestStatTrain400()`（沿用舊候選邏輯）只畀建議掣用；**候選只限已報名課**
  （開局 `S.enrolled` 係 `{}`，無自動報名；同 v73 揀課器口徑一致）。
- 訓練位附近兩個建議掣（可編輯態、第 2 週起、訓練位係自由日先顯示）：
  「沿用上次手動排嘅課」＋「補最低屬性」，撳先套用到 index 1（拍攝鎖位唔郁）。
- 「上次」經兩個改格位記錄入 `S.lastTrain400`（跟 save 走，全量序列化；舊檔
  undefined 嗰陣掣隱藏）。通用改格 onclick 同 `train71HandleClick()` 都有記。
- **v360 遺留問題一併解決**：舊預設將未報名歌藝排入訓練位——新做法根本唔再自動
  揀課，嗰個取捨唔使再等表態。
- 人情債留位（plan[4]=scout_all）維持不變。

### 2. 壓力加休息改做建議唔靜靜換
- 刪走 `defaultWeekPlan` 入面壓力 ≥60／≥80 靜靜換 plan[1]／plan[3] 做 rest 嗰兩行。
  壓力計法（現壓力 vs 預覽峰值取高，計埋已 lock 拍攝）保留，用嚟出建議。
- 手帳建議列 `#nb-suggest400`（可編輯態先顯示，近 `#nb-days`／`#nb-live-stress`）：
  峰值 ≥60 出「建議：壓力偏高，用週X自由日換休息」掣，≥80 再多一粒
  「再加一日休息」掣；目標日＝第一個未鎖定嘅自由日（scout_*），標明實際星期幾；
  玩家撳先換，唔撳唔換；唔准掂拍攝鎖位。掣換完／峰值跌返 <60 建議列自然消失，
  render 唔重複自動換。
- 非編輯呼叫方已逐個檢查，冇嘢依賴舊行為（fresh／preview 函數／`lockShootsIntoDraft`
  fallback 全部只係底稿）。

### 3. 改格顯示機會成本
- 訓練格 hint 加「再 N 堂升 X 級」（`levels75Next`；到頂「已到三級」）；`train71CourseMini`
  補同一口徑進度行 `.t70-mprog`。外出日 hint「本週外出機會剩 X 日」（X＝planDraft 入面
  scout_* 格數）。
- 改格嗰刻（通用改格、訓練揀課、建議掣套用）喺日格下方常駐 div `#nb-cost400`
  （近 `#nb-live-stress`）寫明失去／得到，例如「週二：街演 → 休息：失去約 $35–60
  收入；得到壓力 −7」。數字來源：`stressDeltaForAct`、街演 $35–60／咖啡 $45–75／
  補班 $185、學費 $20、`levels75Next`。成本行改完一直留喺度，直到下一次改格，
  render 唔清走；新一週新底稿嗰陣清（`enterHome()` 可編輯分支）。
- 用香港式書面語，唔用術語。

## 邊界
- 唔改任何規則數字（壓力公式、病倒懲罰、學費、收入全部唔郁）。唔改主線／結局／
  頒獎／排他鎖。唔改 SAVE key（`starVolunteer_map_v19w`）／softRev／產品 `?v=`。
  唔改頒獎贏線 0.875。唔手改 source 年份。

## 實裝
- `index.html` 淨 +186 行（51183→51369）。新 helpers（全部喺 `defaultWeekPlan` 之前）：
  `lowestStatTrain400()`、`weekStressPeak400()`（舊 v379／v384／v386 峰值計法原封抽出，
  含 lock 拍攝 snapshot／restore）、`freeDays400()`、`nbDayHint400()`、`costLose400()`、
  `costGain400()`、`costLine400()`、`showCost400()`、`renderSuggest400()`。
- CSS：`.nb-suggest400`／`.nb-suggest400-btn`／`.nb-cost400`（米紙卡，同
  `.nb-live-stress` 一套）、`.t70-mprog`。HTML：`#nb-stress-detail105` 之後加
  `<div id="nb-suggest400" hidden>`＋`<div id="nb-cost400" hidden>`。

## 測試
- 新：`tests/test_v400_logic.js`（38 項）＋`tests/test_v400_static.py`（內容錨點，
  唔釘行號）——兩份 exit 0。修過一個測試本身嘅 bug：結尾 `fails? 1: 0`——`fails`
  係 array，`[]` 喺 JS 係 truthy，永遠 exit 1；已改 `fails.length? 1: 0`。
- 意圖性行為改變而更新嘅舊測試：`test_calib60_logic.js`（§5 改 v400 斷言＋抽
  `TRAIN75_SPEC`＋`lowestStatTrain400`）、`test_calib60_static.py`、
  `test_p360_static.py`（§③）、`test_eval6_384_logic.js`（D：高壓預設得 plan[6]
  一日休息）、`test_eval7_386_logic.js`（B：重拍攝週預設一日休息）。
- 全套 suite：**424 PASS／9 FAIL**（`~/workspace/suite400.txt`）。9 項同 v398 已知
  pre-existing 清單完全一致（flash51、slot50、soft_tip_111_restore、start53、
  weave43、weave44、weave49、wf5_87、wrap38）。跑完已還原 `qa296/derive296.json`。
- Resync（`qa400/resync400.py`，跟 qa399 模式，difflib 映射 `/tmp/linemap400.json`）：
  8 檔已 resync 並逐檔重跑通過——gift185、rom159、rom176、tang152、tang171／tang173、
  text125、travel114。途中捉到一個坑：抽 FREE／COUNT set 嗰陣 `\b(\d+)\b` 會食註解
  入面嘅裸數字 `7`；已改做只抽行首釘數字（`^\s*(\d+),`）。

## 實駕（Playwright，`qa400/drive400.py`，結果 `qa400/verify/drive400.json`）
- v400 五項**全部通過**：
  ① 第 1 週引導照舊（base 計劃不變）。
  ② 第 2 週訓練位係自由日，兩個建議掣「沿用上次：歌藝訓練」「補最低屬性：歌藝訓練」
  撳落去都將 plan[1] 變歌藝訓練，成本行「週二：到處逛逛 → 歌藝訓練：失去一日外出
  機會；得到歌藝 +1 堂（再 5 堂升二級）· 學費 $20 · 壓力 +10」；舊檔（無 lastTrain、
  未報名）建議掣隱藏。
  ③ 壓力 85 嗰陣建議列出「建議：壓力偏高，用週一自由日換休息」「再加一日休息：週二」，
  唔撳唔換；撳先換 plan[0]=rest，成本行「週一：到處逛逛 → 休息瞓覺：失去一日外出
  機會；得到壓力清零」。
  ④ 改格成本行有顯示：街演「週三：到處逛逛 → 街頭表演：失去一日外出機會；得到約
  $35–60 收入 · 壓力 +7」；歌藝「再 2 堂升二級」日格 hint＋卡 meta「已練 3 次 · 再 2 堂
  升二級」＋訓練成本行；外出機會 5 日→4 日→3 日逐格扣。
  ⑤ 新手跟預設玩 6 週（2 run）：第 42 日金錢 $1038／$1031，壓力 0，**病倒 0 日**。
- v398 基線對照（同一劇本，副本 `070eae7`，結果
  `~/workspace/linji-work398base/qa400/verify/drive400.json`）：① 通過；②–④ 失敗
  （舊行為：第 2 週訓練位自動排演技訓練、無建議掣、無建議列、無成本行、無日格 hint）；
  ⑤ 新手第 42 日 $936／$956，病倒 0 日。**v400 新手無惡化**，反而第 42 日多
  $75–$102（唔再自動排課，慳返約 $20／週學費；兩邊病倒率同壓力都係 0）。
- 實駕工具教訓（寫入 `qa400/drive400.py`，唔好重蹈）：主 script 頂層 binding 唔係全域
  可見，evaluate 叫唔到內部函數——播種只經 `window.S`＋localStorage，入屋／重繪一律
  經真實 DOM 撳掣；N1「通告板」故事 modal 要逐句撳「下一句」再揀選項（第一個選項）
  再「確定」再「關閉」；瞓覺掣會彈確認 modal，確認掣係「瞓覺」（role p），唔係「確定」；
  訓練頁籤要先撳屬性 chip（預設演技）先出課程卡；`fullarc/driver.py` import 嗰陣會讀
  sys.argv，parse 完自己嘅 args 要先清 argv 再 import。
