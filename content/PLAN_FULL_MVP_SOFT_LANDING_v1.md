> Soft≠PASS｜唔 tip LIVE｜唔抬 `?v=`／SAVE（仍 **19w**／`starVolunteer_map_v19w`）｜`liveWeekGateStillActive()` 仍 true｜89–92 HOLD｜出圖 HOLD｜禁 soft-try｜禁假造教學 5–6 FX

# PLAN_FULL_MVP_SOFT_LANDING_v1

預覽 repo 指針。Sandbox 原檔（`star-volunteer-web`／`PLAN_FULL_MVP_SOFT_LANDING_v1`）**唔喺本 repo**。本檔係對齊 2026-11-05 FULL MVP Soft 總驗嘅短 PLAN：總驗 **PASS on `717f9007`**，產品仍 **Soft≠PASS**，**唔 tip LIVE**。

總驗來源（本 repo 未收原始 REPORT／CHECKLIST 正文）：靜態清單對照＋瀏覽器抽樣。哨兵同依賴圖以下表為準。

## 狀態

| 項 | 狀態 |
|---|---|
| 基準 main | `717f9007`（Soft PR #18 UI Phase3 後） |
| FULL MVP Soft 總驗 | **PASS**（無玩家面 zero-tol；B6／B10／B13 SKIP＋理由） |
| 產品 | **Soft≠PASS** |
| LIVE | **唔 tip**。`liveWeekGateStillActive()` runtime 仍 `return true`。stub／slice `tipForbidden` 仍 true |
| SAVE／`?v=` | 仍 `starVolunteer_map_v19w`／`?v=19w` |

## 依賴圖

`Pack favor Soft → UI Phase2 →（Pack B HOLD）→ 行為閘 Soft → UI Phase3 Soft → 本總驗`

| 磚 | 狀態 | 預覽 repo 指針 |
|---|---|---|
| Pack favor Soft | Done Soft；**LIVE tip HOLD** | `content/CHANGELOG_GIGS_1988_3_2_5_SOFT.md`；gigs `version=3.2.5-soft` |
| UI Phase2 | Done Soft | `content/PLAN_UI_PHASE2_DEEPEN_v1.md`；`content/MOCK_UI_PHASE2_DEEPEN_v1.json` |
| Pack B（MV3 階 C–D 等） | **HOLD／SKIP** | 唔擋已落地磚 |
| 行為閘 Soft | Done Soft（#16 `b1d43d0c`、#17 `5ebf08c4`） | `content/NOTES_SOFT_FEATURE_FLAG_CONFLUENCE.md`；`content/PLAN_STORY_BEHAVIOR_GATE_FULL_ALIGN_SOFT_v1.md` |
| UI Phase3 Soft | Done Soft（#18 `717f9007`） | `content/NOTES_SOFT_UI_PHASE3_STAR_CASTING.md`；`content/MOCK_UI_PHASE3_STAR_CASTING_v1.json` |

近期 Soft tip：#14 `2d5002da`、#15 `f4c5cac3`、#16 `b1d43d0c`、#17 `5ebf08c4`、#18 `717f9007`。

## 驗收（總驗時）

| # | 項 | 總驗 |
|---|---|---|
| A1 | 交付標示 Soft≠PASS；唔 tip LIVE | PASS |
| A2 | 玩家面經理人「何生」；無「Ho 哥／Ho哥／ho哥」 | PASS |
| A3 | 玩家面無真實藝人名；紅星用虛構名 | PASS |
| A4 | 關海媚維持 vignette；唔升格第六攻略 | PASS |
| A5 | 89–92 深內容 | **SKIP＋HOLD** |
| A6 | 茶水間「聽講／好似」；nextHint 玩家面隱藏 | PASS（結構） |
| A7 | 雙女只 meet→rel；唔逼 commit | PASS（結構） |
| A8 | C1–C5 Soft 路徑 | PASS（結構）；FULL_ALIGN §3 深驗＝持續抽樣 |
| A9 | 紅星遠觀首輪四人（文字＋音）；齊鎮海唔上地圖 | PASS |
| A10 | Casting「接通告／暫未能報」；無第三掣 | PASS |
| S1 | Pack B／MV3 階 C–D／Casting 補庫 | SKIP＋HOLD |
| S2 | 出圖／bust／Vera | SKIP＋HOLD |
| S3 | 教學步序 5–6 FX | SKIP＋HOLD（唔假造） |
| S4 | 鄧線 | SKIP＋附錄（唔入本體必經 C1–C5） |
| S5 | LIVE tip／抬 `?v=`／SAVE／week-gate 退休 | SKIP＋HOLD |
| S6 | UI Phase4／Romance 非 MVP／Gift shop | SKIP |

## 合規哨兵（`717f9007` 起維持）

| 哨兵 | 期望 |
|---|---|
| `SAVE` | `starVolunteer_map_v19w` |
| `?v=` | `19w` |
| `liveWeekGateStillActive()` | `true` |
| `tipForbidden` | `true` |
| `isSoftTryGig()` | `false`；Casting Detail 唔讀第三掣 |
| `gatePath()` | 只跟 `featureFlag_softBehaviorGatePreview`；flag off 唔注入 `softSeed` |

抽樣 URL：`?v=19w&softBehaviorGate=1`（可加 `softSeed`）。每次先清 `localStorage` 再 hard reload。

## 同 repo 指針

- `content/PLAN_OUTSTANDING_SOFT_NEXT_v2.md`
- `content/PLAN_STORY_BEHAVIOR_GATE_FULL_ALIGN_SOFT_v1.md`
- `content/NOTES_SOFT_FEATURE_FLAG_CONFLUENCE.md`
- `content/NOTES_SOFT_UI_PHASE3_STAR_CASTING.md`
- `NOTES_V19W_SOFT_BEHAVIOR_GATE.md`
- `content/PLAN_UI_PHASE2_DEEPEN_v1.md`（見下節）

## Docs hygiene（Phase2）

`content/PLAN_UI_PHASE2_DEEPEN_v1.md` 禁令已經寫「玩家面經理人一律為『何生』，絕對無出現『Ho 哥』／『Ho哥』」。本預覽樹 **冇**「無何生」誤寫，亦 **冇** 2023 殘年。本輪唔改 Phase2 正文，玩家面字不變。

## Out of scope（維持 HOLD）

- LIVE tip、抬 `?v=`／SAVE、`liveWeekGateStillActive()`→false
- 出圖／bust
- 89–92
- 教學 5–6 FX（唔假造）
- Pack B／MV3 階 C–D／Casting 補庫
- UI Phase4／Romance 非 MVP／Gift shop

**Footer：** Soft≠PASS｜89–92 HOLD｜出圖 HOLD｜唔 tip LIVE｜唔抬 `?v=`（19w）｜`liveWeekGateStillActive===true`｜禁 soft-try
