# v20a108 D-8 第二階段：WF4 隨機事件具名講者企立

底本 main `8d19640`（v20a106）。紀律：SAVE key／softRev／產品 `?v=` 全冇郁；
`DAILY_EVENTS_WF4` 零改動（static 測試對 baseline 逐字對照）；只推分支 `v108-d8`，唔 merge。

## 盤點（36 事件）
- 全身資產講者只得阿偉（awi）。新路徑 8 單（獨角阿偉）：cha02、home01、st01、st03、
  boss01、boss02、boss03、day02。舊路徑 28 單維持 v105 場景底＋純文字。
- 具名但冇資產：阿媽、霞姐、阿成、昌叔、表姨媽＋25 個功能／泛稱講者——雙全身喺 WF4
  做唔到（資產缺口，唔係接線問題）。
- 阿偉句表情：neutral×5、think（st03）、happy（boss03）、sad（day02）。

## 改動（掂過嘅函數）
- 新增：`wf4SpeakerId108`、`wf4OnTableIds108`、`wf4DlgExtraCands108`、
  `wf4DlgCharsHtml108`、`wf4BeatStageHtml108`（全部只 call 現成 DLG106 入口：
  `dlg106ResolveSides`／`dlg106Candidates`／`dlg106ResolveCategory`／`dlg106HasFullbody`／`__dlg106Err`；
  候補鏈尾段同巧遇一致：UI40 企立→bust→剪影→SVG 兜底）。
- `wf4PlayEvent`：只改 `beatHtml` 分流（有阿偉行 DLG106 舞台，冇就舊呈現；抉擇／結算維持舊文字）。
- 分工：冇掂組件 CSS／幾何／渲染函數（`spDlgCharsHtml`／`paintDlg106`／DLG106 模組零改；
  初版加過嘅 `.wf4-play` 幾何 CSS 已拆返；舞台幾何歸 v108-dlg）。
- 新增測試：`tests/test_dlg108_logic.js`、`tests/test_dlg108_static.py`（反證齊：斷資產／資產表閘／舊版）。

## 測試＋實駕
- 全套 A/B（148 檔）：工作版 136 PASS／12 FAIL；基線 134 PASS／14 FAIL
  （差額＝2 個新測試，基線舊 code 行佢哋會 FAIL；12 FAIL 兩邊逐字相同，零回歸）。
  主 script `node --check` OK。
- 實駕（本地鏡像，390×844，零 pageerror；`qa108a/drive108.py`＋`drive_log.json`＋`shots/`）：
  st03（旁白 base 0.6 → 阿偉 think 全光）、day02（→ sad 全光）、set01（舊路徑場景圖＋純文字）
  全部經真路徑 `wf4PresentPending→wf4Fire→wf4PlayEvent` 播通。
  註：主 script 包咗 IIFE，`wf4PlayEvent` 唔係全域，實駕用設 `S.wf4.pending`＋真 UI 休息入地圖觸發。

## 未達標位（老實申報）
- **人物太細**：modal 內舞台沿用組件原有 in-flow 幾何，實測舞台 342×168px、人物 28×83px，
  肉眼幾乎睇唔到表情切換（數據層 src／明暗切換正確，視覺層唔達標）。修正歸 v108-dlg，合併後再覆核。
- 雙全身未實現（見盤點）；day 事件場景底係漸變（入地圖嗰刻 `atLoc` 係 null，同 v105 行為一致）。
