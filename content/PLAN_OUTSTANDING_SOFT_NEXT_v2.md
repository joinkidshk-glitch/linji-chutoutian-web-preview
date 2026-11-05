> Soft≠PASS｜唔 tip LIVE｜出圖 HOLD｜89–92 HOLD｜玩家面禁真藝名／禁「Ho 哥」→「何生」／favor `agency_ho`｜經 qwen3.7-max

# PLAN_OUTSTANDING_SOFT_NEXT_v2

## 狀態表

| # | 項目 | 狀態 | 下一動作 | 要唔要 Soft A/B |
|---|---|---|---|---|
| 1 | Soft tip #14 Deng push | Done Soft（main `2d5002da`） | 已 tip Soft；跟進 iOS Soft 合／瀏覽器抽樣 | 唔使 |
| 2 | Soft tip #15 nextHint／notes／seed | Done Soft（main `f4c5cac3`；?v=19w） | 持續驗 | 唔使 |
| 3 | 鄧 meet Soft A | Done Soft（Mock `8a80d7b9`） | 已 PASS | 沿 Soft A |
| 4 | 鄧 push Soft | Done Soft（PLAN `44c65a88`／Mock `9e5751a4`／md `338d852f`／母 PLAN `ab90d1b7`；已 tip Soft #14） | 已 PASS | 沿 Soft A |
| 5 | Pack favor 3.2.5 | Done Soft 靜態／wiring YES（Soft `0390b091`；LIVE tip HOLD） | 等 LIVE 抬版 | 唔使 |
| 6 | 雙女加厚 Soft A | In Soft（PLAN `832f25ed`／Mock `d4e23624`；深度 A 已拍；6 beats） | 瀏覽器後續 smoke／seed | 沿 Soft A |
| 7 | 教學 Phase2（modal／copy／步5–6 FX） | Done Soft（modal 豎滾 #16 `b1d43d0c`；copy #23 `8a63e477`；FX assets＋wire #24 `ff1d5eed`，`artHold:false`。`behaviorGate:"not_bound"`＝教學 Phase2 Soft 唔強制綁 BehaviorGate C stubs，唔等於 feature-flag 合流未做。視覺 nits 可選、唔擋） | 已 tip Soft；唔再當缺拖曳／FX HOLD | 唔使 |
| 8 | **P1 行為閘 FULL 對齊** | Done Soft（feature-flag 合流已在 main：#11 `e6de2278`／#16 `b1d43d0c`／#17 `5ebf08c4`；開關模型對齊。LIVE week-gate 退休 HOLD）（PLAN soft `126c2434`／engine slice `8450130d`／stub `cba0e877`） | 已 tip Soft；`liveWeekGateStillActive()` 仍 true（唔改 false） | 沿 Soft A 已鎖 |
| 9 | chrome Soft A | Done Soft（PR#13 chrome／softSeed OK；#12 seed `bd86ed8c` 風格可複用） | 已鎖 | 沿 Soft A |
| 10 | 89–92 | HOLD | 等指示 | 唔使 |
| 11 | 出圖 | HOLD | 等指示 | 唔使 |
| 12 | LIVE tip／?v= 抬版 | HOLD（仍 19w） | 等 tester OK | 唔使 |
| 13 | OUTSTANDING v1 `a45e3b36` | **已過期**（以本 v2 為準） | 棄用 | 唔使 |
| 14 | UI Phase3 Soft：紅星遠觀＋Casting CTA | Done Soft（web 接線；`gatePath()==="soft"` 讀 `MOCK_UI_PHASE3_STAR_CASTING_v1.json`；Soft≠PASS） | tester 抽樣四星遠觀＋locked／ready；唔 tip LIVE | 遠觀 B／Toast A／第五星 B 已鎖；禁 soft-try |

## 擬轉統籌
本包 P1 行為閘 FULL 對齊及相關 Soft 交付摘要已就緒，詳細技術與驗收細節見同包 B/C/D SHA。

## UI Phase3 Soft 接線

- [x] Soft path 載入 `MOCK_UI_PHASE3_STAR_CASTING_v1.json`（fetch；失敗用 inline）
- [x] 四星遠觀文字＋既有 chime；toast 用 Mock `resultToast`；齊鎮海唔上地圖
- [x] Casting Detail：ready「接通告」／locked「暫未能報」＋離開；禁 soft-try
- [ ] LIVE tip／抬 `?v=`／SAVE（仍 19w／`starVolunteer_map_v19w`；`liveWeekGateStillActive()` 仍 true）

Soft≠PASS｜唔 tip LIVE｜出圖 HOLD｜89–92 HOLD｜唔抬 ?v=（19w）
