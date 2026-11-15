# NOTES_V20A228 — 拎走全部四個存檔遷移函數

## 拍板
用戶 2026-11-15 20:35 拍板：而家嘅舊存檔冇意義，唔使保留，code 保持乾淨——
四個存檔遷移函數一併拎走，連測試一併清。

## 刪咗咩（index.html 淨 −170 行：63175→63005 split／63174→63004 wc -l）
- `c2n210MigrateSave`（v210 新加，C→N 舊存檔 remap）36 行
- `levels75MigrateSave`（舊進階課點遷移）27 行
- `years66MigrateSave`（舊存檔年份鍵 remap）40 行
- `jan67MigrateSave` 機械部分（舊存檔 +65 日遷移＋日戳 walker）54 行
- 四函數喺 `normalizeSaveObj` 入面嘅 try/catch 呼叫點 11 行
- 單行兩處：YEARS66 頭行註解刪一行、常數 `LEVELS75_MID_OF` 一行
- 淨係講呢四個遷移嘅註解一併改／刪（YEARS66 頭行、JAN67 頭行「兩件事→一件事」、
  COURSE_DEFS 註解、LEVELS75 註解、fresh() 兩印註解）

實際刪除區間（1-based，difflib 對位核實，見 qa228/resync228.py）：
L31647／L31696–31735／L31744–31797／L32142／L33783–33793／L36706–36768。
注意：qa228/delete228.py 印出嚟嘅行號係 0-based 切片口徑，比實際 1-based
區間各偏 −1（例如佢話 years66 係 L31695–31734，實際係 L31696–31735）；
內容一樣，只係邊界 `}`／空行撞款令 difflib 將邊界認做另一邊嘅相同行，
結果檔案內容無分別。以 resync228.py 嘅 1-based 區間為準。

## 唔准郁、冇郁
- YEARS66 運行時推移層（SHIFT=2）原封不動；`years66Walk`／`years66ShiftYear`
  （載入 pack 用）保留；`LEVELS75_STEP` 保留。
- `jan67OpeningTextFix`＋`JAN67_OPENING_TEXT_MAP`（開局季節文字定點修正，
  載入 pack 文字用）保留。
- `normalizeSaveObj` 其他步驟（storyGate113Scrub、calib60MissedScan、
  conseq61LegacyMark、enc195BackfillTierMax）原封不動。
- `fresh()` 出生印 `years66Shifted:1`／`startEpoch67:1` 保留（存檔格式相容，
  註解已改做 v228 說明）；三個測試斷言佢哋存在。
- 歷史 NOTES 檔唔改。

## 安全核實（刪之前做）
- 四函數只由 `normalizeSaveObj` 呼叫（舊 L33784／33787／33789／33793），
  全部舊存檔專用、有 epoch guard／冪等；`fresh()` 出生已有兩印，
  新檔永遠唔行遷移。
- `storyGate113Scrub` 只讀 `o.story.done`（N id）、`o.dayIndex`、`o.ending410`，
  唔依賴遷移輸出；`calib60MissedScan` 讀新 epoch dayIndex。
- `jan67ShiftDayStamps`／`jan67ShiftDayValue`／`JAN67_DAY_SHIFT`／`JAN67_DAY_KEYS`
  只得 jan67MigrateSave 用，已一併刪；`LEVELS75_MID_OF` 只得遷移用，已刪。
- 刪後 `MigrateSave` 全 repo 0 命中（index.html＋tests；resync 歷史註解除外，
  見下）。
- `node --check` 兩 inline script 塊 PASS（抽 script 塊 check，`node --check
  index.html` 本身唔得）。

## 測試改動
- 刪 `tests/test_story210_migrate_logic.js`（12 個斷言）。
- `tests/test_jan67_logic.js`：刪舊檔 +65 日遷移 §5／§6／§7＋`v66SaveBase()`＋
  `oldEpochDate`＋`JAN67_DAY_SHIFT` extract／斷言；§4 開局文字、§1–§3 留；
  fresh() 斷言改註解。
- `tests/test_years66_logic.js`：刪 §5 遷移段斷言；§6 新檔段留，改名。
- `tests/test_jan67_static.py`：block 斷言、DAY_SHIFT／DAY_KEYS 斷言、
  接線次序斷言→負面 guard（normalizeSaveObj body 無 MigrateSave、
  storyGate113Scrub 之前無遷移呼叫）。
- `tests/test_years66_static.py`：block 斷言、掛點→負面 guard。
- `tests/test_levels75_static.py`：MID_OF、函數表、掛點→負面 guard。
- `tests/test_levels75_logic.js`：CONSTS 減 MID_OF、FNS 減 migrate、§5 全刪。
- `tests/test_story_gate113_static.py:40`：hook_ok 改錨（scrub 在 calib60 之前＋
  body 無 MigrateSave）。

## 釘行 resync（qa228/resync228.py）
- Suite B1 305/20：除 13 項穩定 FAIL 外，另有 7 檔釘行漂移 FAIL
  （gift185／rom176／tang152／tang171／tang173／text125／travel114），
  全部純行號漂移，無內容問題。
- resync228.py：difflib 對位核實被刪 170 行恰好係預期集合，其餘 63,005 行
  全部跟分段映射（<=31646 不變／31648–31695 −1／31736–31743 −41／
  31798–32141 −95／32143–33782 −96／33794–36705 −107／>=36769 −170）；
  58 個釘行舊新內容逐字相同；travel114 FREE 33 行全部帶旗、COUNT 12 行
  全部冇旗。7 檔重寫後逐個覆驗 ALL PASS。
- 殘留：6 檔測試嘅 v210 resync 歷史註解仍提及 `c2n210MigrateSave`
  （gift185／rom176／tang171／tang173／text125／travel114）——係歷史記錄，
  唔係 live 引用，留返唔改。

## Suite
- A（pristine main a58c0b9）：313/13＝基線。
- B（工作副本，resync 後）：**312/13**（減已刪遷移測試 1 檔；同一 13 項穩定 FAIL
  清單：flash51／giglib36／pacing35／poster59／rumor49／slot50／
  soft_tip_111_restore／start53／weave43／weave44／weave49／wf5_87／wrap38）。
  零回歸。

## 落地
- 分支 v20a228 → rebase 上 main → squash merge → push main → curl 核實線上
  index.html 同 main 逐 byte 相同 → 刪工作副本 linji-work228＋分支。
