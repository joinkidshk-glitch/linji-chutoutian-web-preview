> Soft≠PASS｜試玩擋玩 C2｜`tvb_rules_gossip` 缺線｜唔 tip LIVE｜89–92 HOLD｜經 qwen3.7-max＋DeepSeek

# SOFT_RUMOR_BEHAVIOR_GATE_PLAYTEST_FIX_v1

## 診斷
C2 Soft stub `rumorAny: ["tvb_rules_gossip"]`，但 Soft mock 傳聞／金龍打聽／何生聽風 **從不發** 此 id（只見紅星八卦／`hint:act_*`）→ 第 6 週仍鎖死。截圖：`playtest-shots/27-rumors-journal.png`。

一併缺線（稍後會擋）：`gao_steal_spotlight`（C3）、`choi_recent_news`／`hau_ching_recent_news`（C5）。

## Soft 產物
- JSON：`SOFT_RUMOR_BEHAVIOR_GATE_PLAYTEST_FIX_v1.json` SHA **`2dda90aa`**
- 通告 notes：見 gigs **3.2.9-soft**（靈異／動作喜劇槍戰矛盾）

## iOS Soft tip 必合
1. `MOCK_RUMOR_SEEDS` 加入 4 則（id 原樣）
2. `MOCK_ASK` 加入 5 則 `mockAskAdds`
3. `applyMockAsk`：有 `grantsRumorId` 時入手帳 **id＝grantsRumorId**（唔用 `hint:…`）

## 驗收
- 金龍「打聽電視城規矩」或何生「請教入廠守則」→ 手帳出現 id `tvb_rules_gossip`
- C1 done＋week≥4＋gigCount≥3＋loc 合＋已聽 `tvb_rules_gossip` → C2 可開
