# NOTES_V20A231 — RW-1：N4–N9 逐句重寫

- 日期：2026-11-16
- Base：main HEAD `1b0dad9`（v230）
- 範圍：`content/story_detail_n1_to_n17.json` 入面 N4–N9 全文逐句重寫（對白輕口語＋旁白／notes／label／提示語香港式書面語，逐句唔係逐詞換）；`index.html` 刪 TEXTFIX55 映射 11 條＋N6／N6F synopsis「對稱下游」改做 DEV 註解；`tests/test_story157_pack_static.py` sha 錨點 1 處。
- 唔做：N1–N3（已完成）、N10 以後、通告檔、報紙包、新庫／引擎區一律未掂；Vera 內容（N6 beats[2]＋choices[0]）一字未動，留 v159。

## 數字（獨立核實）

- 改咗 **87 處字串**（N4 9／N5 13／N6 23／N7 16／N8 15／N9 11；共用行重複計：N4 rb[3].l0 ×2、N5 rb[3].l1 ×3）；CJK 葉片句數 447 → 440；範圍內 77 處字串／121 句保留未改（本身已合標準，逐句大聲讀過）。
- **TEXTFIX55_EXACT 拆咗 8 條**（179→171）、**NOTE_EXACT 拆咗 3 條**（39→36）；其餘各組 0 條。改前實測：EXACT 8 處命中＋NOTE_EXACT 2 全命中＋1 死 key，載入模擬 16 處 diffs；改後實測：各組 0 命中，載入模擬只剩 2 處 pre-existing diffs（N4 lockedHint「未解鎖」→「未開放」TEXTFIX57 正名＋N6 Vera notes 補句號），**87 處新句 0 處受覆寫**。
- EXACT 值藏事實修正：N6「兩個都等」→ live「三個都等」（Vera＋曉晴＋采兒），新源頭已用「三個」；三條 lockedHint 條目先重寫源頭做短版書面語提示再刪（源頭含數字／Vera 外洩，唔可以直接刪）。
- N6／N6F synopsis：主線 synopsis 無玩家面渲染點（listOpen 只用 title／playerHint／lockedHint／nextHint），按任務指示改做 DEV 註解＋共用短版書面語簡介；兩 synopsis 相同＋含「每集都找你」，滿足 test_story157_index_static 錨點。
- 測試改動 1 項：story157 `nodes[5-16]` sha 重算（`1a0f1be4…` → `fa09c15b…`）；N10–N17 已核實一字未動。
- 禁詞掃描：禁詞表 0 命中（「點擊」0）；獨立「整天」0、「快要」0、「喲」0；對白開場「明白／知道」0；系統旁白第二人稱「你」0（起草版 2 處已修正）；新 notes 無數字／flag_／rel_／P2／route_／standing；年份一律未動。

## 驗收

- Read-aloud test：10 句試讀（改動最大／最難嗰 10 句）全部一次讀順，0 句要停低重讀；5 組 before／after 抽查確認逐句重寫。
- `vm.Script` 編譯 `index.html` 全部 2 個 inline script block（3,781,203 字元）通過；`index.html` 行數不變（48,220 行）。
- 全套 suite：**312 PASS／10 FAIL，FAIL 名單同 v230 基線逐項相同，零新 FAIL**（flash51／rumor49／slot50／soft_tip_111_restore／start53／weave43／weave44／weave49／wf5_87／wrap38）；story157／story157_index 全部 ALL PASS。中間曾跌一格（311／11，N6／N6F synopsis 錨點），統一共用版後回復。
- Live drive：未做（瀏覽器死，押後）。

## 發現（後批留意，最重要一項）

1. **JSON N6–N9 運行時被 inline 覆寫遮蔽，改動唔到玩家面前。** `applyStorySpineOverrides46()` 將 JSON N7／N8／N9 換成 `STORY_SPINE_NODES_1989` 內嵌版，`applyStorySpineOverrides48()` 將 JSON N6 換成 `STORY_SPINE_NODES_N6` 內嵌版。Live 玩家見到嘅係內嵌版（N6《角落那張桌子》／N7《暴雨救場》／N8《選美後台》／N9《茶餐廳度橋》）。**本批 JSON 改動即時生效嘅只有 N4／N5。** 內嵌版 N6＋N6F＋N7＋N8＋N9 合共 465 句，要另開跟進批。RW-2 同理：JSON N10／N11 被 1989 表遮蔽、N12–N16 被 1990 表遮蔽，開工前要先定邊邊做準。
2. 主線 synopsis 無玩家面渲染點；JSON 17 條 synopsis 係咪全部改做 DEV 註解／短版簡介，留待 RW-2 一併定。
3. N4 年份不一致（`when` 1988春 vs beats[0] 1988年夏）、N5 共用收尾行「說了一半」三分支同一句，內容問題未改，等核實。
4. 全本實寫估算修正：RW-0 62.5%＋RW-1 53.6%，兩批合計 255／445＝57.3%；全本 9,060 句推算約 5,200 句（約 5,000–5,500），低過計劃 6,000–6,500 約 15–20%。分章差異大（N4／N5 約三成，N6–N8 七至八成，視乎對白本身係廣東話定普通話書面語）。
5. 工作報告：`~/workspace/linji-language-sample/RW1_WORKLOG.md`（數字總表、87 處 before／after、77 處保留清單、10 句試讀、TEXTFIX55 逐組實測表、測試改動、驗收證據、發現）。

## RW-1 verdict：通過（附跟進）

JSON N4–N9 重寫完成，載入層乾淨，suite 零回歸。但玩家面前 N6–N9 仍係未重寫嘅內嵌版——跟進批要處理 465 句 inline 主幹節點，唔可以當 RW-1 已經覆蓋玩家可見嘅 N6–N9。
