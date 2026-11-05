Soft≠PASS｜教學 Phase2 步5–6 FX Soft｜GD｜唔 tip LIVE｜唔抬 ?v=｜89–92 HOLD｜出圖跟 Soft 合

> Soft tip wire 2026-11-05：`index.html` 已接 Soft gate。`step5_drag_guide`／`step6_merge_fx`＝`soft`，`artHold`＝false。下文「仍 HOLD」係美術交貨原文。

# ART_BRIEF_TUTORIAL_PHASE2_FX_SOFT_v1

## 0. Goal

補齊 `TUTORIAL_PHASE2_SOFT_NITS` 缺漏美術：

- `step5_drag_guide`：手帳傳聞拖曳引導（手指／路徑／槽高亮）
- `step6_merge_fx`：拼合邊緣光／成功 burst＋蓋章／失敗標

對齊 `PLAN_TUTORIAL_PHASE2_WALKTHROUGH_SOFT_v1` 步序 5–6、`PLAN_TUTORIAL_PHASE2_STEPS_5_6_COPY_SOFT_v1`（FX→GD）、`PLAN_UI_SYSTEM_DESIGN_v1`（邊緣 Glow＋Stamp）、`UI_PHYSICAL_CANON.md`。

## 1. Inventory（前→後）

| 項 | 前 | 後 |
|---|---|---|
| 拖曳手指／路徑／槽高亮 | 缺（僅 coach 文案） | Soft PNG 於 `assets/ui-physical/tutorial-fx/` |
| 拼合 edge glow／burst／stamp | CSS box-shadow／文字 stamp 為主；缺獨立 FX 層 | Soft PNG 層 |
| `stamp_complete` | 已有 toast 完成印 | 保留；另加拼合「合」印 |
| index `TUTORIAL_PHASE2_SOFT_NITS` | HOLD | **仍 HOLD（本輪只交美術 Soft；唔假造 wire PASS）** |

## 2. 產物路徑

根：`assets/ui-physical/tutorial-fx/`（見該目錄 `README.md`＋MD5）

| artId | 檔 | 尺寸 | 造法 |
|---|---|---|---|
| fx_drag_finger | fx_drag_finger.png | 320² | GenerateImage＋magenta chroma |
| fx_drag_finger_proc | fx_drag_finger_proc.png | 320² | Pillow procedural 備選 |
| fx_drag_path_arrow | fx_drag_path_arrow.png | 320² | Pillow |
| fx_slot_highlight | fx_slot_highlight.png | 360×200 | Pillow |
| fx_card_lift_shadow | fx_card_lift_shadow.png | 300×80 | Pillow |
| fx_coach_pulse_dot | fx_coach_pulse_dot.png | 96² | Pillow |
| fx_merge_edge_glow | fx_merge_edge_glow.png | 420×280 | Pillow（透明中心） |
| fx_merge_burst | fx_merge_burst.png | 384² | Pillow |
| fx_merge_stamp_ok | fx_merge_stamp_ok.png | 320² | Pillow＋Noto「合」 |
| fx_merge_fail_mark | fx_merge_fail_mark.png | 256² | Pillow（無字） |

## 3. Soft≠PASS 閘

- Soft 美術 pack ≠ wire PASS ≠ LIVE tip
- 禁抬 `?v=`；禁改主教學 `tutorial_zh_HK.json`
- 禁 AI 漢字（印章只用本機 Noto）
- 89–92 HOLD；剪影另線

## 4. Acceptance（美術 Soft）

- [x] 步5 最少：finger＋path＋slot
- [x] 步6 最少：edge_glow＋burst＋stamp_ok（fail 可選已交）
- [x] 透明 PNG／色票對齊 canon
- [ ] wire／動畫接入（**未做 · HOLD**）
- [ ] tester QC visual（交 pack）
