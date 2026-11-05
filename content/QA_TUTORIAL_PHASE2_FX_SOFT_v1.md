# QA｜教學 Phase2 步5–6 FX Soft（GD 自判）

> Soft≠PASS｜唔 tip LIVE｜唔抬 ?v=｜89–92 HOLD｜美術交貨時碼位仍 HOLD。其後 FX wire Done Soft（#24 `ff1d5eed`）：`step5_drag_guide`／`step6_merge_fx`＝`soft`，`artHold:false`。下文「wire HOLD／selfCheck 仍要求 fx_hold」係美術交貨當時記錄，唔再當 FX HOLD。

## Specs 來源

- `TUTORIAL_PHASE2_SOFT_NITS`（美術交貨時 qa-pr23／Pages：`step5_drag_guide=HOLD`，`step6_merge_fx=HOLD`，`artHold:true`。其後 #24 已改 `soft`／`artHold:false`）
- `PLAN_TUTORIAL_PHASE2_WALKTHROUGH_SOFT_v1` 步序 5–6 缺漏
- `PLAN_TUTORIAL_PHASE2_STEPS_5_6_COPY_SOFT_v1` Out of scope：FX→GD
- `PLAN_UI_SYSTEM_DESIGN_v1`：邊緣 Glow＋蓋章 Stamp
- `UI_PHYSICAL_CANON.md`／既有 `toast/stamp_complete.png`

## 自判

| 檢查 | 結果 |
|---|---|
| 步5 拖曳引導三件套（finger／path／slot） | OK |
| 步6 拼合 edge／burst／stamp | OK |
| 無 AI 漢字 | OK（「合」＝Noto） |
| 透明層可用 | OK（RGBA） |
| AI burst 洋紅殘影 | 已棄；只用 procedural burst |
| procedural finger 過抽象 | 降為 `*_proc`；主用 AI finger |
| wire／CSS 接入 | **HOLD**（本 pack 只美術） |
| tip LIVE／抬 ?v= | **未做** |

## 結論

**美術 Soft 可交 tester QC**。Overall Soft≠PASS。上表「wire／CSS 接入 HOLD」同「接線前唔改 HOLD」係本 pack 只交美術當時；#24 之後 selfCheck 要求 `step5_drag_guide`／`step6_merge_fx`＝`soft` 且 `artHold===false`（唔再係 fx_hold）。
