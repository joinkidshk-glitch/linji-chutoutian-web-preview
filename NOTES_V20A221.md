# NOTES_V20A221 — 書面語改寫 P2：遊戲主線旁白

- 日期：2026-11-15
- 基線：main `a45479e`（v220）
- 範圍：書面語改寫票 P2（遊戲邊主線旁白）。RECOUNT-REPORT live 確數 2,411（SPINE inline 1,805＋story_detail C1–C5 606；C6–C17 pack 死檔 27 唔郁）。

## §1 改動內容

- 431 句全部改寫（五個工人並行）：SPINE_1990 100 句／SPINE_1989 96 句／story_detail C1–C5 93 句／SPINE_C6 24＋C17 20＋WF1 25＋BR89 21 句／HINT_SOFT 43＋TRAJ_WRAP 9 句。
- 套用方式：index.html 按 offset 換字串字面量（338 處）；story_detail 按 JSON path 設值＋dump（93 處，round-trip 已驗證 byte-identical）。
- 覆核：工人 14 個 note 逐項睇過——9 項接受；1 項統籌改寫（story_detail C1 標題「第一日：冇價」→工人「第一天：毫無身價」，改回「第一日：無價」，保住雙關）；C17 synopsis「nn」核實源頭係 `\n\n` 轉義，工人真正換行正確還原。
- 對白零郁動：SPINE 對白層、story_detail 對白層、「」／『』引文全部保留廣東話（G5）。

## §2 驗收

- recount.py（遊戲邊）：P2 live 2,411 → **37**，其中 27 係 C6–C17 死檔（刻意唔郁）；live 殘留只得 10 個，逐個核實全部合法——講數 ×2、講明 ×2、講價 ×4（全部書面語固定詞）、『』G5 引文 ×2（嘅／嚟各 1）。
- P1 維持 0；P3 池數字零變動。
- `node --check`：index.html 兩塊 inline script 全部通過。
- 全套 suite A／B：**309／13，FAIL 清單一模一樣，零回歸**（A＝pristine main `a45479e`，B＝工作副本；中途 B 曾經 296／26——13 個 pin 死舊廣東話字串嘅測試，見下文測試期望維護，修好後重跑回復 309／13）。
- git diff：index.html 618 行＋story_detail 186 行＋測試檔 13 檔＋fixture 1 檔，只係改寫句＋釘死字串同步，零結構改動。
- **測試期望維護（必要，唔係放寬）**：P2 改寫觸發 13 個 pin 死舊廣東話字串嘅測試（br89／c17route153／cleanup100／contra98／gate136／story157_index／story157_pack／story198×2／text55／weave48×2／wf1_80）。逐個斷言核實新文字保留原意圖（珍姐＋糖水、事務所、無雙軌術語、setting 保留路線名前綴、C17 1990冬＋台慶之後＋散場、flags／stats／tags 不變）之後，將釘死字串更新做新書面語版＋fixture C17 兩抉擇（label＋notes）同步；其餘斷言零郁動。另修兩處工人漏網：C5 標題／synopsis「辣手問題」還原（本身已係書面語，TEXTFIX55 釘死，唔准擅改棘手）；C6F-0011「route 旗」DEV 術語跟 C6-0013 改做「第一天那個選擇」。

## §3 落地

- 分支 `v20a221` → squash merge → main，（待填 HEAD／線上 bytes／sha）。
- 工作副本 `linji-work221` 落地後刪除；pristine 對照 `linji-pristine221` 已刪除。

## §4 殘留／跟進

- recount 唔計 `journalCandidate` 欄（G4 阿偉第一人稱獨白，留廣東話正確）同 `nodeRipple` 死碼（G9，P3 刪）。
- recount strip_quoted 只剔「」，唔剔『』：SPINE_1990-0079 兩個『』引文標記（嘅／嚟）會一直殘留，屬 G5 合法，唔係漏網。
- P3（隨機事件等 2,535＋G1／G9／G10）→ v222。
