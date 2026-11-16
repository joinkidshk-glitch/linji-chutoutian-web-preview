# NOTES_V20A242_RW5_LAN_DELETE

版本：v20a242（RW-5 續：LAN 覆寫表刪除）
日期：2026-11-16
Base：main 1e4cff9（v241）

## 目的

v241 刪咗 WF4／WF2 覆寫表，但 `ROMANCE_LAN_PA_OVERRIDES` 留低，理由係「0／5 一致」——呢個判斷錯咗。
獨立核實證實：覆寫表成個取代 JSON 節點（`applyRomanceLanOverrides48()` 入面 `lx.nodes[i] = ROMANCE_LAN_PA_OVERRIDES[node.id]`），
而表係舊版（每節點 3 段 beats、`when` 1990秋），JSON（RW-3 改好）係 5–9 段 beats、`when` 1991春／1992。
即 live 藍若曦線玩家見到嘅係舊文，RW-3 嗰 31 處 lan 改寫俾遮住咗。本票刪走成個 LAN 覆寫層，JSON 做唯一來源。

## 改動（index.html 淨 −144 行，44,608 → 44,464 行）

1. 刪 `ROMANCE_LAN_PA_OVERRIDES` 成個表（舊 L6600–6732，133 行 → 2 行 v242 註解）。
2. 刪 `applyRomanceLanOverrides48()` 函數定義＋註解（舊 L7562–7576）。
3. 刪 `refreshCopyPacksFromDisk` 入面嘅呼叫點（舊 L15041–15042 → 1 行 v242 註解）。
4. `CONTRA98_WHEN_FIX` 補兩行：`R_lan_crisis:["1990秋","era_1990_autumn_transfer"]`、`R_lan_ending:["1990秋","era_1990_autumn_finale"]`（沿用舊表值）。
   原因：JSON crisis `when` 1991春／ending 1992 係顯示值；唔加表行，經 `contra98FixNodeWhen`＋`years66Walk`（+2）後顯示變 1993春／1994，衝破 1992 遊戲邊界；
   加表行後顯示 1992秋，同刪表前一致。其他三節點（meet 1989、push1 1989秋、push2 1989）walk 後係 1991／1991秋，正常。
   分層要講清楚：覆寫階段（rom2 賦值後、年份管線前）生效版 when＝JSON 原值；完整管線後顯示年由 fix 表管，同其他感情線結尾節點一致。

## JSON 修正（content/story_detail_romance_lan_xu.json，僅 11+/7−，文案零郁）

- R_lan_push1／push2／crisis／ending 加 `"playerOffer": false`（meet 本來已有）。引擎 `hasPlayerOffer` 同玩家列表排除邏輯讀 `playerOffer === false`；
  JSON 原本缺呢個鍵，刪表會令呢四節點突然入玩家列表。
- R_lan_push1 兩抉擇 `stats.music` → `stats.stage`（v20a100 CLEAN100 修正之前只喺表入面，JSON 仲係 music；music 鍵 applyChoice 無映射，係死數）。

## 唔郁嘅嘢

- `ROMANCE_WF2_OVERRIDES` 剩低 10 條（lan 5 條 synopsis／beats 同 JSON 一致，無害；vera 5 條等 v159 刪 Vera 嗰陣一併處理）。
- 零邏輯／數值／旗標／判定改動；只刪覆寫層＋上面兩項 JSON 結構修正。

## 載入模擬（行返遊戲載入路徑，唔係齋對文字）

方法（`/tmp/sim242_load.js`）：抽 index.html 真函數（`applyRomanceWf2Overrides81`、`normaliseTangStub152`、`textfix55StoryPack`＋TEXTFIX55/57 全表、`contra98FixNodeWhen`、`years66Walk`），
按 `refreshCopyPacksFromDisk` 次序行：rom2＝JSON → `STORY_WIRE.romance.lanXu = rom2` → WF2 → normalise → TEXTFIX → contra98Fix → years66Walk，對照 JSON 原值。

結果 SIM PASS：
- A 段（WF2＋TEXTFIX 之後、年份管線之前）：5 節點 beats／when／synopsis／title／setting／choices／playerOffer 全部同 JSON 一致。
  beats：meet 6、push1 5、push2 5、crisis 5、ending 9；when：meet 1989、push1 1989秋、push2 1989、crisis 1991春、ending 1992。
  （WF2 嗰步只行到 lan 5 節點，因為模擬只載 rom2，冇載 rom1；真路徑 vera 5 節點會一併行，合共 10。）
- B 段（全年管線之後）：meet 1991、push1 1991秋、push2 1991、crisis 1992秋、ending 1992秋；年份越界（>1992）0 個。
  synopsis＝RW-3 新文（例：meet「藍若曦是星河電視台的場記。那天早上廠景門口人擠人…」）。

## 測試

- 7 檔直接受影響（weave48_logic／cleanup100_logic／weave48_static／wf2_81_logic／wf2_81_static／contra98_logic／weave46_static）：改做 JSON 直出斷言，全部 PASS。
  其中 contra98_logic 全域守門而家正式覆蓋 R_lan_*（舊豁免已刪），加 fix 行後通過；FIX98 節點數 23→25。
- 9 檔釘行 resync（v242 刪行令釘行漂移，內容逐行核實純漂移，唔係回歸）：
  contra98_static（23→25）、gift185_static（總行數 44608→44464）、kwan151_static（13 釘行各 −146）、
  rom176_static（5 釘行：載入點 −143、其餘 −144）、tang152_static（3 釘行：−146／−143／−144）、
  tang171_static／tang173_static（總行數＋openLoc DEF 40009→39865）、text125_static（3 錨點：−146／−146／−144）、
  travel114_static（COUNT 12＋FREE 35＋DEF＋WRAPPER 共 49 錨點，逐行對位零 mismatch；DEF 40009→39865、WRAPPER 28019→27875）。
- inline script blocks：`vm.Script` 編譯 2/2 通過。
- 全套 suite（工作副本）：**TOTAL PASS 314 FAIL 10**，FAIL 清單同 v241 基線已知 10 項完全一致
  （flash51／rumor49／slot50／soft_tip_111_restore／start53／weave43／weave44／weave49／wf5_87／wrap38），零回歸。
  注意：suite 第一次誤跑咗常駐 clone（v241 舊碼，314／10）；重跑工作副本先見 305／19，逐個覆驗證實 9 項新 FAIL 全部係釘行漂移，修好後重跑先係 314／10。
- 已刪名全檔只剩兩行 v242 註解引文（index.html grep 2 命中，均為註解）。

## 工作報告

`~/workspace/linji-language-sample/RW5B_LAN_DELETE_WORKLOG.md`
