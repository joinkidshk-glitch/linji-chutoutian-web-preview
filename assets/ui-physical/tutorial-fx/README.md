# tutorial-fx｜教學 Phase2 步5–6 Soft FX（GD）

> Soft≠PASS｜唔 tip LIVE｜唔抬 ?v=｜89–92 HOLD｜出圖跟 Soft 合  
> 對齊：`TUTORIAL_PHASE2_SOFT_NITS.step5_drag_guide`／`step6_merge_fx`（Soft tip wire 2026-11-05：`index.html` Soft gate 已接；`artHold` 已清。Soft≠PASS｜唔 tip LIVE｜`?v=` 仍 19w）  
> 色票跟 `UI_PHYSICAL_CANON.md`（gold `#C9A227`／stamp_red `#C43C2A`／cream）  
> 中文印章僅 Noto；禁止 AI 漢字。

## 步5｜拖曳引導

| 檔 | 用途 |
|----|------|
| `fx_drag_finger.png` | 主：拖曳手指指示（GenerateImage＋chroma；cel／HUD） |
| `fx_drag_finger_proc.png` | 備：純 procedural 扁平手（可換） |
| `fx_drag_path_arrow.png` | 虛線拖曳路徑箭頭 |
| `fx_slot_highlight.png` | 目標槽高亮框（dashed gold） |
| `fx_card_lift_shadow.png` | 提起卡片時陰影 |
| `fx_coach_pulse_dot.png` | coach 脈衝小點 |

## 步6｜拼合 FX

| 檔 | 用途 |
|----|------|
| `fx_merge_edge_glow.png` | 兩卡靠近邊緣金光（透明中心） |
| `fx_merge_burst.png` | 拼合成功放射火花 |
| `fx_merge_stamp_ok.png` | 成功蓋章「合」（Noto，對齊 stamp_complete 風格） |
| `fx_merge_fail_mark.png` | 失敗淡紅 X 圈（無字） |

可重用既有：`toast/stamp_complete.png`（「完成」）。

## Wire（Soft tip 2026-11-05）

- 步5：Soft gate 先 loop finger＋path（1.1s），slot_highlight 疊目標卡；lift shadow／coach pulse 可選。預設 `fx_drag_finger.png`；proc 只係 onerror fallback。
- 步6：is-near／is-glow 疊 `fx_merge_edge_glow`；成功 burst→stamp_ok；失敗 fail_mark。
- **唔改** `tutorial_zh_HK.json`；**唔 tip LIVE**；Soft off／LIVE 唔強制 FX。`TUTORIAL_PHASE2_SOFT_NITS.artHold` 已清。Soft nits：finger 略偏 HUD；proc 抽象；lift shadow 淡；pulse jagged。

## MD5

- `fx_card_lift_shadow.png` `f593eae9de9012468d1c9b007174a79b` (8609 B)
- `fx_coach_pulse_dot.png` `3884280da59d34d3da81f852a3196bc9` (7936 B)
- `fx_drag_finger.png` `f84db9218ec3f518ae9bcfecac5e734f` (66635 B)
- `fx_drag_finger_proc.png` `e02bdbdb22e66e4ff797959fe7a49cfc` (6098 B)
- `fx_drag_path_arrow.png` `65f140fe9d489380ccd5c3de418792af` (16708 B)
- `fx_merge_burst.png` `5f76190e233b26959bfafa4a09d571fd` (74956 B)
- `fx_merge_edge_glow.png` `b240a3dd112babfd2190e432dc1e4dc8` (18104 B)
- `fx_merge_fail_mark.png` `5238a0b648ca13e9cc077bdc4f6f9fad` (8463 B)
- `fx_merge_stamp_ok.png` `b700142dff930d9a0d9d9add9c912bae` (42482 B)
- `fx_slot_highlight.png` `4861297418a6f25667232a990cc0d8ad` (10014 B)
