Soft≠PASS｜唔 tip LIVE｜出圖 HOLD｜89–92 HOLD｜禁「Ho 哥」→「何生」／favor `agency_ho`｜經 qwen3.7-max｜玩家面禁真藝名／禁工程詞

# SOFT_SMOKE_BEHAVIOR_GATE_C1_C5_v1

## 概述
短驗點表，供瀏覽器／iOS Soft 驗證 C1 至 C5 行為閘鎖。
- Refs: stub `cba0e877` / engine `8450130d` / soft PLAN `126c2434` / 對齊 PLAN `PLAN_STORY_BEHAVIOR_GATE_FULL_ALIGN_SOFT_v1.md`（本包）
- Soft A/B：唔使

## Checklist
1. [正測] C1 `cafe_cha` 觸發：seed 載入後，loc 設為 `cafe_cha`，確認事件正常觸發。
2. [正測] C3 `fameMin16`：fame 調至 16，確認 C3 閘鎖解鎖；fame=15 時確認鎖定（負測）。
3. [正測] C4 `agency_ho` favor：設定 `favor` 中 `agency_ho` ≥ 1，確認 C4 解鎖；`agency_ho` = 0 時確認鎖定（負測）。
4. [正測] C5 `autumn|winter` + rumor：season 設為 `autumn` 或 `winter`，並觸發 soft rumor，確認 C5 解鎖。
5. [負測] C5 `rival_gao` 隔離：確認 `rival_gao` 相關 rumor 唔會觸發 C5。
6. [正測] 逐步推進：seed → loc → fame → favor → season → rumor，確認狀態機無斷層。
7. [負測] 越級觸發：未完成 C3 直接推 C4 條件，確認 C4 保持鎖定。
8. [合規] 玩家面無「Ho 哥」／真藝名／工程詞；經理人顯示「何生」；nextHint 唔顯示。
9. [隔離] LIVE week-gate 仍 active；feature flag 合流仍缺口；Soft≠PASS；唔 tip LIVE；?v=19w。
10. Soft A/B：唔使（沿 Soft A 已鎖）。
