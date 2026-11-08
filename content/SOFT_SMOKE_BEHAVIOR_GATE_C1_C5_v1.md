Soft≠PASS｜唔 tip LIVE｜出圖 HOLD｜89–92 HOLD｜禁「Ho 哥」→「何生」／favor `agency_ho`｜經 qwen3.7-max｜玩家面禁真藝名／禁工程詞

# SOFT_SMOKE_BEHAVIOR_GATE_C1_C5_v1（FULL literal 改口後）

> 2026-11-08：用戶 `full_literal_including_gates`——C1→`agency_ho`；C4→`softLogic=OR`（debt｜favor｜loc）。舊 cafe_cha／AND 正測作廢。

## 正／負測
1. [正測] C1 `agency_ho` 觸發；[負測] `cafe_cha`／`tvb_longmen` 唔開 C1。
2. [正測] C2：C1 done＋gig≥3＋`tvb_rules_gossip`＋片場|茶餐廳。
3. [正測] C3：fame>15（fameMin16）＋`gao_steal_spotlight`；[負測] fame=15。
4. [正測] C4 OR：
   - loc=`agency_ho`（favor0／debt0）→ 開
   - debt≥1（他處）→ 開
   - favor≥1 @ agency_ho 目標（他處）→ 開（Soft 近似左肢）
   - [負測] cafe_cha＋favor0＋debt0 → 鎖
5. [正測] C5 秋／冬＋傳聞種子；[負測] 夏；[負測] rival_gao 唔開 C5。
6. nextHint 玩家面唔顯示；Face 禁工程詞／Ho哥／噂。

## 引擎
- Soft 預覽 `index.html`：`stepFavor` 認 `softLogic:"OR"`＋`debtMin`；`stepLoc` 喺 OR 時 defer。
- `debtCount` 讀 `ctx.debt` 或 `S.mockDebts.length`（接 `STUB_FAVOR_DEBT_SEASON_v1`／`FREEPLAY_FW.favorDebt`）。
