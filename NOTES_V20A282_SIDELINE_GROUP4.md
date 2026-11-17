# NOTES_V20A282 — 支線補完第 ④ 組 §14 決議落地（遊戲 code 部分）

- 版本：v282（base main `fbf66a4` v281；suite 基線 345／9）
- 範圍：WORKORDER §14（4.1–4.5）＋ DECISIONS Q3／Q4／Q11／Q12／Q13（2026-11-15 已拍板）
- 攻略文字改動唔喺本票（parent 之後 artifact.edit 做）；本票只做遊戲 code＋L5023 確認研究。

## 實質 code 改動：只有 Q12 殘留三行（index.html L13417–13419）

ECHO89 結局回望陣列三句「站隊那場波」→「企邊那場波」（最小改動，句式不變）：

| 行 | 改前 | 改後 |
|---|---|---|
| L13417 `flag_side_tv` | 站隊那場波，你選擇留在星河——由臨記捱出頭的地方，你沒有忘本。 | 企邊那場波，你選擇留在星河——由臨記捱出頭的地方，你沒有忘本。 |
| L13418 `flag_side_film` | 站隊那場波，你選擇跟電影公司那邊行——那一步踏出去，就沒有回頭路。 | 企邊那場波，你選擇跟電影公司那邊行——那一步踏出去，就沒有回頭路。 |
| L13419 `flag_side_undecided` | 站隊那場波，你兩邊都沒有應死——門開得久，會自己關上，這句你到埋單都記得。 | 企邊那場波，你兩邊都沒有應死——門開得久，會自己關上，這句你到埋單都記得。 |

- `chai_repay` 第二句本身早已係「企邊嗰場風波」（L37337），Q12 決議已滿足，唔郁。
- 改完核實：index.html「站隊」0 命中；content/*.json「站隊」0 命中；「企邊那場波」×3、「企邊嗰場風波」×1。
- 注意：DECISIONS 附錄「Q12 更正」話 repo 得 2 處「站隊」殘留、全部係 DEV 註釋（L21286、L58455）——嗰個講法已經過時：嗰兩個行號而家無「站隊」，真正殘留係上面三句玩家面結局回望文字。本票按 brief「有舊詞殘留先修」修咗佢哋。

## Q4：N15 1992 年秋末——code 側唔使改（WORKORDER 前提證偽）

WORKORDER 4.2 話 code 舊寫「1990 年秋末」（repo L19947／L19948／L21751／L21758）要同步改做「1992 年秋末」。核實結果：**四處而家嘅實際位置＋顯示值全部已經係 1992，唔使改；手改 source 反而會整壞（顯示 1994）**。

實際位置（現行 main `fbf66a4`）：
1. `index.html` L6783 — `STORY_HINT_SOFT.N15.lockedHint`：「1990 年秋末才開啟……」
2. `index.html` L6782 — `STORY_HINT_SOFT.N14.nextHint`：「下一幕「錄音室」——1990 年秋末……」
3. `content/story_detail_n1_to_n17.json` L3724 — N15 對白首句：「1990 年秋末，天星音樂舞蹈室。……」
4. N15 節點 `when` 欄：`"when": "1990秋末"`（＋`eraTag: "era_1990_autumn_idol"`）

機制（全部用真 code 驗證過，唔係推斷）：
- `refreshCopyPacksFromDisk` L14873：`[main, rom1, rom2, rom3, rival, ...].forEach(p => years66Walk(p, null))`——主線 JSON 入載嗰陣成個 walk，`when`／`beats[].lines[]`／`lockedHint` 等全部 +2。
- 同函數 L14765：`[STORY_HINT_SOFT, STORY_TITLE_SOFT, ...]` 一樣行 walk——上面第 1、2 處一樣 +2。
- 章節標籤 L11217–11220：`eraTag` 係舊曆編碼（walk 跳過），顯示嗰陣先 `years66ShiftYear` +2。
- 實證（`/tmp/q4_walk_proof.js`，抽 index.html 真實 YEARS66 block 行 node）：walk 後 N15 `when` = `"1992秋末"`；對白首句 = `"1992 年秋末，天星音樂舞蹈室。……"`；兩句 hint 顯示 1992；**若 source 改 1992，walk 會顯示 `"1994 年秋末"`**。
- 先例一致：L29045 註解「410 源字串寫 1990（when／setting／synopsis／lockedHint），靠播放時 year-walk 先顯示 1992——呢度絕對唔郁任何年份字眼」；L14417（v20a218 A1）「source 寫顯示曆，walk 會 +2，EXACT 預寫 1990 令顯示 1992」。

結論：Q4 遊戲側**零改動**。新測試第 (1) 組 9 項釘死呢個狀態（source 留 1990＋walk 顯示 1992＋double-shift guard）。

⚠️ **跟進畀 parent（攻略側）**：WORKORDER 4.2 提議 L3688 改做「code 舊寫「1990 年秋末」要同步改（遊戲側票……）」——呢句係建基於已證偽嘅前提，唔好照寫。建議 L3688 改做定稿註：「對白首句 source 寫舊曆「1990 年秋末」，YEARS66 載入 +2，顯示「1992 年秋末」；遊戲側唔使改。」L3684 不動（已經寫 1992 年秋末）。

## Q11：stub 債 code 側已清，唔使改

- `debt_slot_ngai_01`：index.html 0 命中；`content/STUB_FAVOR_DEBT_SEASON_v1.json` 0 命中（grep -c = 0）。
- 全 repo 7 命中全部喺 tests/，全部係刪除確認（`test_sideline273_logic.js:156` 釘死 code 側 0 命中；`test_gig229_press94_advice.js:192–194` 釘死 stub JSON＋html 0 命中；其餘係註釋）。
- 淨返攻略側三行（WORKORDER 2.25：L2931、L2964、L5293）由 parent artifact.edit 刪。

## Q13：過期壞帳核實通過，唔使改

`wf3SettleTick`（index.html L27424 起）過期分支（L27494–27502）：
- 設 `liaoHarvestDone = 1`、`liaoHarvestExpired = 1`，債由 `mockDebts` 濾走；
- 註解明文：「v20a259 R3：收割過期唔做，唔係「還清」，唔入帳本 settled（債銷咗，數唔計；信用照扣 −2）。」；
- `S.industryCredit -= 2`＋`syncDualTracks` 在位；
- `favorLedgerNoteSettled(` 呼叫全函數只出現 1 次（收割完成分支 L27488；過期分支之後 0 次）。
- 同 v279 測試「過期：唔計 settled」一致。Q13 決議已滿足。

## Q3：鍾線五幕齊全，唔使改

`ENC79_BEATS.chung_choning`（L40832 起）：`chung_review`（Beat 1）／`chung_intel`（Beat 2）／`chung_f_clue`（Beat 3）／`chung_farewell`（Beat 4 交心）／`chung_patron`（Beat 5 提攜；另有 `chung_patron_cold` 冷版變體）——五幕齊，維持 5 幕唔剪。交心五段澄清註係攻略側（L3413），parent 做。

## L5023 確認研究：改——程線時段「（時段 1992 年–1992 年冬）」

結論：**改**。證據（現行 main）：
- `ENC79_STARS` 程天諾（index.html L38592）：`{ id:"ching_tinlok", ..., win:[[1992,"秋"],[1992,"冬"]], unlockYear:1992 }`——巧遇池 1992 年先解鎖，窗口只得 1992 秋／冬。
- 支線見面唔可能早過 1992 年：`unlockYear:1992` 係硬閘；`chung_f_clue` 類比唔適用，程線首見 `first:ching_tinlok` 派 `gig_1992_rec_101`（1992 年通告）。
- N15 係 1992 年秋末（Q4 組已證：顯示值 1992秋末），同「1992 年–1992 年冬」夾得埋。
- 同 DECISIONS 附錄 A2（2026-11-15 統籌裁定：批准改「1992 年–1992 年冬」）一致。Parent 改攻略 L5023 嗰陣用呢個結論。

## 測試

- 新檔 `tests/test_sideline282_logic.js`：**28 項，ALL PASS**（6 組：(1) Q4 9 項／(2) Q11 2 項／(3) Q13 4 項／(4) Q12 4 項／(5) Q3 6 項／(6) L5023 3 項）。第 (1) 組抽 index.html 真實 YEARS66 block 行 node 驗證，唔係重寫邏輯。
- 測試修訂記錄：初版 (3) 組 `favorLedgerNoteSettled` 計數斷言 FAIL——原因係測試寫錯：同一呼叫點有 `typeof favorLedgerNoteSettled==="function"` 守衛＋呼叫兩處文字命中；已改計 `favorLedgerNoteSettled\(`（呼叫）= 1，code 本身無問題。
- 全套 suite：**346／9**（`bash qa131/run_suite.sh`，outfile `/tmp/suite282.txt`）——9 項全部係已知 pre-existing FAIL（flash51／slot50／soft_tip_111_restore／start53／weave43／weave44／weave49／wf5_87／wrap38），同 345／9 基線對照零回歸（＋1 係新測試檔）。

## 檔案

- `index.html`：淨 3 行改（L13417–13419），行數 ±0，唔使 resync。
- `tests/test_sideline282_logic.js`：新檔（`git add` 明確加）。
- `NOTES_V20A282_SIDELINE_GROUP4.md`：本檔。

## 留跟進

- 攻略側（parent artifact.edit）：WORKORDER 4.1 L3413 澄清註、4.2 L3688 定稿註（見上「跟進畀 parent」，唔好照 WORKORDER 原寫法）、L5023 改「1992 年–1992 年冬」（已確認）、4.3 Q11 三行刪（L2931／L2964／L5293）、4.4／4.5 無改動。
- 用戶 2026-11-18 06:32 新指令：**儀表板停做每版更新**——v282 唔派儀表板 builder；另「不要再停下來」，排隊繼續做。
