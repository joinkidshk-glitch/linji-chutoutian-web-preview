# HANDOFF｜C1 UI beat fields sandbox v1

**時間：** 2026-11-03（Asia/Hong_Kong）  
**HOLD：** Soft≠PASS；全量出圖未開；鄧 HOLD；playerOffer 未動。

## 狀態

| 項 | 狀態 |
|---|---|
| LIVE `story_detail_c1_to_c17` | **1.2.8**（SHA16 `a08b3ef78a96be92`）C1 11 beats 已有 `kind`／`speakerId`／`emotion`／`expression`／`bg`（對齊 ART_BRIEF §3；見 V18H／預覽 `?v=18h`） |
| Sandbox | `SANDBOX_C1_FUSION_DRAFT_v1.json` 已鏡同套字段（本票）；仍非 LIVE 來源 |
| GD art | `assets/story/c1/` 已齊最小集（hero／ho／cheung bust＋兩 bg）；無藍若曦（C1 無此角） |
| Schema | `PLAN_STORY_UI_BEAT_SCHEMA_v1` 已鎖 |

## 抽樣對照（C1）

| beat | kind | speakerId | emotion | expression | bg |
|---|---|---|---|---|---|
| 0 | system | — | — | — | bg_loc_tvb_longmen |
| 1 | system | — | — | — | bg_c1_tea_restaurant |
| 2 | dialogue | ho_sang | firm | default | bg_c1_tea_restaurant |
| 3 | dialogue | ho_sang | firm | raise_brow | bg_c1_tea_restaurant |
| 4 | dialogue | awi | worried | eyes_down | bg_c1_tea_restaurant |
| 5 | dialogue | ho_sang | firm | frown | bg_c1_tea_restaurant |
| 6 | system | — | — | — | bg_c1_tea_restaurant |
| 7 | dialogue | cheung_tsijun | firm | default | bg_c1_tea_restaurant |
| 8 | dialogue | awi | tense | default | bg_c1_tea_restaurant |
| 9 | dialogue | ho_sang | firm | frown | bg_c1_tea_restaurant |
| 10 | dialogue | awi | firm | raise_brow | bg_c1_tea_restaurant |

## Tester

公開預覽據 iOS 報已交 `?v=18h`／SAVE `starVolunteer_map_v18h`（含 P0 advance 修）。劇本側確認字段對表＝ART_BRIEF；sandbox 已補齊。**本票唔改 LIVE 文案／choices／flags。** Soft≠PASS。

## 下一刀（等叫）

- 批量 C1–C17 字段／引擎推導舊稿：另開閘  
- 全量出圖：HOLD  
