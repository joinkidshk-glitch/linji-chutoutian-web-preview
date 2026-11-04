> Soft≠PASS｜唔 tip LIVE｜出圖 HOLD｜89–92 HOLD｜玩家面禁真藝名／禁「Ho 哥」→「何生」／favor `agency_ho`｜經 qwen3.7-max

# PLAN_STORY_BEHAVIOR_GATE_FULL_ALIGN_SOFT_v1

## §1 範圍／Out of scope
- **範圍**：P1 行為閘 FULL 對齊（C1–C5），Soft A 已鎖邏輯落地，修正 FULL 舊表偏差。
- **Out of scope**：唔 tip LIVE；唔改 LIVE week-gate；唔改 89–92；出圖 HOLD；唔改 choice/flags id。

## §2 FULL vs Soft 對齊矩陣（C1–C5 表）

| beatId | FULL 意圖（摘要） | Soft 已鎖 | 偏差標記 | 處理（Soft 準／已知偏差） | stub／engine 對齊 |
|---|---|---|---|---|---|
| C1 | loc=agency_ho（舊表） | loc=`cafe_cha`；weekMin 保留地板 | 已知偏差→Soft 以已拍板為準 | Soft 準 C1=cafe_cha | stub `cba0e877` |
| C2 | needDone C1；weekMin=4；gigCountMin=3；rumor tvb_rules_gossip；loc tvb_longmen\|cafe_cha | 同左 | 無偏差 | Soft 準 | engine slice `8450130d` |
| C3 | needDone C2；weekMin=6；loc tvb_longmen；rumor gao_steal_spotlight；fame>15 | fameMin=16／fameCompare='>'／tag fameMin_16 | 無偏差 | Soft 準 | engine slice `8450130d` |
| C4 | 人情債>0 或 loc（偏 OR）；舊文「Ho 哥」 | needDone C3；weekMin=8；loc=agency_ho；favorMin≥1 @ agency_ho AND（favorTarget=agency_ho, softLogic=AND） | 已知偏差→Soft 以已拍板為準（禁 Ho 哥→何生，偏 OR→AND） | Soft 準 C4=AND favor≥1@agency_ho | stub `cba0e877` |
| C5 | needDone C4；weekMin=9；loc cafe_cha\|tvb_longmen；seasonAny autumn\|winter；rumorSoftPriority；rumorAny choi_recent_news,hau_ching_recent_news | 同左，**rival_gao 唔混入 C5** | 無偏差 | Soft 準 | engine slice `8450130d` |

## §3 tip 前 checklist
- [x] feature flag 合流：Soft 開關模型已對齊（`featureFlag_softBehaviorGatePreview`＝Soft 行為閘 opt-in，唯一 query／localStorage 解析；`gatePath()` 只呼叫呢個旗，回 `"soft"`｜`"live"`。Soft on：C1–C5 同既有 Deng／雙女／seed／chrome 守衛只行 stub trigger／evalOrder。Soft off／非 Soft：只行 week-gate，softSeed 唔注入）。LIVE week-gate 退休仍 HOLD／`tipForbidden`。唔等於 tip LIVE。ENGINE_SLICE §6「tip 前唔合流」仍指唔退休 LIVE 週數閘。
- [ ] evalOrder 一字對齊 engine slice（needDone → minDaysAfterPrev → weekMin_floor → locIdAny → favor_AND_loc → fameCompare → gigCountMin → seasonAny → rumorSoftPriority → tagAny → relAny）
- [ ] C1 cafe_cha／C3 fameMin16／C4 AND favor≥1@agency_ho／C5 rumor soft＋秋冬
- [ ] rival_gao 唔入 C5
- [ ] 禁工程詞／禁 Ho 哥／禁真藝名／玩家面「何生」
- [ ] nextHint 藏（#15 已 tip Soft 先返回；持續驗）
- [ ] LIVE week-gate 仍 active（`liveWeekGateStillActive()` runtime 仍 true；stub／slice 同旗仍 true）
- [ ] tipForbidden 直至 tester OK＋明示 tip
- [ ] Soft≠PASS

## §4 Soft 瀏覽器建議驗點（逐步）
1. **seed 載入**：確認 `bd86ed8c` 風格可複用，softSeed OK，?v=19w 載入正常。
2. **loc 驗證**：C1 必須 `cafe_cha` 觸發；C4 必須 `agency_ho`。
3. **fame 驗證**：C3 正測 fame=16 PASS；負測 fame=15 FAIL。
4. **favor 驗證**：C4 正測 favor=1 @ `agency_ho` PASS；負測 favor=0 FAIL。
5. **season 驗證**：C5 正測 autumn/winter PASS；負測 summer FAIL。
6. **rumor 驗證**：C5 確認 `choi_recent_news` 或 `hau_ching_recent_news` 觸發；負測 `rival_gao` 唔應開 C5。

## §5 Soft A/B
- 唔使（沿 Soft A 已鎖）。
- tip 合流節奏：唔使／或僅節奏諮詢。

## §6 建議驗點摘要
1. C1 loc=`cafe_cha` 觸發正常，無舊表 agency_ho 殘留。
2. C3 fame=15 FAIL，fame=16 PASS，fameCompare='>' 運作正確。
3. C4 favor=0 FAIL，favor≥1 @ `agency_ho` PASS，softLogic=AND 生效。
4. C4 玩家面顯示「何生」，絕無「Ho 哥」或真藝名。
5. C5 season=summer FAIL，autumn/winter PASS。
6. C5 `rival_gao` 唔觸發，rumorSoftPriority 順序正確。
7. evalOrder 嚴格按 engine slice `8450130d` 順序執行。
8. feature flag 合流 Soft 已交付（開關模型對齊；`gatePath` 只跟 `featureFlag_softBehaviorGatePreview`）。LIVE week-gate 退休仍 HOLD（`liveWeekGateStillActive` 仍 active、`tipForbidden` 仍 true）。Soft≠PASS。唔 tip LIVE。

## §7 Acceptance／Out of scope
- **Acceptance**：Soft A 行為閘 C1-C5 邏輯完全對齊 engine slice `8450130d` 及 stub `cba0e877`，FULL 舊表偏差已修正並以 Soft 拍板為準，玩家面用語合規。
- **Out of scope**：唔 tip LIVE；唔改 LIVE week-gate；唔改 89–92；出圖 HOLD；唔改 choice/flags id。

---
*文末註：經 qwen3.7-max；refs soft PLAN `126c2434`／engine `8450130d`／stub `cba0e877`／FULL PLAN_STORY_QWEN37_FULL_v1.md*
