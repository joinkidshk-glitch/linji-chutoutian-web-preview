# 頁眉閘
Soft≠PASS｜唔 tip｜唔改 LIVE week-gate｜89–92 HOLD｜出圖 HOLD

# 目的
?v=19w 已通行為閘 Soft flag／C1 cafe；C3–C5＋鄧未操到（week1 未達門檻）→ 用 Soft 種子加速抽樣。

# Soft A 數值表
- C1：loc=cafe_cha; weekMin floor=1
- C2：needDone C1; weekMin=4; gigCountMin=3; rumor tvb_rules_gossip; loc tvb_longmen|cafe_cha
- C3：needDone C2; weekMin=6; loc tvb_longmen; rumor gao_steal_spotlight; fame>15（fameMin=16, fameCompare='>', tag fameMin_16）；禁誤寫 fame>16
- C4：needDone C3; weekMin=8; loc=agency_ho; favorMin≥1 @ agency_ho AND（favorTarget=agency_ho, softLogic=AND）
- C5：needDone C4; weekMin=9; loc cafe_cha|tvb_longmen; seasonAny autumn|winter; rumorSoftPriority; rumorAny choi_recent_news,hau_ching_recent_news
- 鄧 R_tang_meet：needDone C5 + favorMin>=1 @agency_ho; Mock meet only; rel_tang_threshold=2; push+ HOLD

# 種子說明
## seed_c3_ready
- 目標：C3 觸發就緒
- 注入 state：week=6, fame=16, loc=tvb_longmen, rumors 含 gao_steal_spotlight
- 期望結果：可開 C3
- 負例：fame=15 會 FAIL（必須 >15，即 fameMin=16）

## seed_c4_ready
- 目標：C4 觸發就緒
- 注入 state：week=8, favor.agency_ho=1, loc=agency_ho
- 期望結果：可開 C4
- 負例：favor=0 會 FAIL

## seed_c5_ready
- 目標：C5 觸發就緒
- 注入 state：week=9, season=autumn, rumors 含 choi/hau，無 rival_gao
- 期望結果：可開 C5
- 負例：season=summer 會 FAIL

## seed_deng_meet_ready
- 目標：鄧 R_tang_meet 觸發就緒
- 注入 state：C5 done, favor.agency_ho>=1
- 期望結果：可開 Mock meet
- 負例：缺 C5 會 FAIL

## seed_chain_shortest
- 目標：最短路徑累積
- 注入 state：由 week1 累積至 week10 鄧 meet
- 期望結果：完整觸發鏈驗證

# 最短路徑步驟
若無注入工具，按 Soft weekMin 地板自然推進＋手動補數值：
1. Week 1：觸發 C1 (cafe_cha)
2. Week 4：補 gigCount>=3 及 tvb_rules_gossip，觸發 C2
3. Week 6：補 fame=16 及 gao_steal_spotlight，觸發 C3
4. Week 8：補 agency_ho 好感度>=1，loc 轉 agency_ho，觸發 C4（何生好感度提升）
5. Week 9：補 season=autumn 及 choi/hau rumors，觸發 C5
6. Week 10：觸發鄧 R_tang_meet (Mock)

# Out of scope
- LIVE tip
- 改 week-gate 預設
- 89–92 時代線
- 出圖
- 鄧 push+

# 文末註
本版經 qwen3.7-max。
refs SHA8：stub `cba0e877`｜engine PLAN `8450130d`｜鄧 PLAN `043a70ff`｜鄧 Mock `f5986e81`。
Blocker：Soft≠PASS｜唔 tip｜唔改 LIVE week-gate｜89–92 HOLD｜出圖 HOLD｜鄧 push+ HOLD。
