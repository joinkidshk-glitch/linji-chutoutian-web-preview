# NOTES_V20A224 — 書面語「佢」跟進票：59 句真旁白改寫

- 日期：2026-11-15
- 基線：main `9ce1f4e`（v222；v223 when-fix 已在歷史入面）
- 範圍：`~/workspace/linji-language-audit-v2/work/fixlist_v224.json`——`fix` 59 句（`leave` 70 句絕對唔郁）。522 池外旁白、ENDING410_ADJ_RUMOR 一律唔郁（等 parent 裁定）。

## §1 改動內容

- **recount.py v4.1**（工具檔，唔係遊戲 code）：`strip_quoted` 加埋『』（同「」／""／“”一樣剔走）＋修正史註解。
- **59 句逐句改寫**（改前逐字核對原文，全部相符，0 句跳過）：WF4 46 句（label 抉擇掣為主，按 G2 當 UI 文字；tx／out 按旁白）、SPINE_1989 3、SPINE_1990 1、SPINE_WF1 1、HINT_SOFT 1（同 SPINE_1989 一句重複，兩個位置一齊改）、ROMANCE_OVR 1（R_hiu_meet）、ENC79_LIU／MAK／YIP 各 1、gift_react 1、P1 EVENTS inline-only 1（TRAIN_RESULT_stamina）、story_detail C1 1（兩處同句一齊改）。要點：佢→他／她、畀→給、晒→完／光、埋→到／在／完、啱啱→剛剛、隔籬→隔壁、膊頭→肩膀、手指公→拇指、嗌→喊、即刻→立刻、落→下／進、話（動詞）→說／告訴、call（動詞）→傳呼（Call機作名詞保留）。
- **三個 JSON**：`content/gift_react_copy.json`（`system.unmet` →「需要先完成對應的相遇劇情，或與對方成功傾談一次。」）、`content/story_detail_c1_to_c17.json`（C1 兩處「今天沒有人 call 他」→「今天沒有人傳呼他」）、`content/events_zh_HK.json`（補入 `TRAIN_RESULT_stamina` 全組 3 句，中間一句係已改寫版）。
- **兩個 inline 鏡像**（fixlist 以外，同一訊息嘅玩家可見鏡像）：[56a] `TEXTFIX55_EXACT` key＋value 一齊改做新書面語（identity entry）；[56b] `canGive` inline fallback（約 L30918）「需要先完成對應相遇劇情，或同佢成功傾談一次」→新句。查核：`sysLine("unmet", …)` 從未被叫，真正玩家可見嘅係 canGive fallback。
- **測試 pin 更新 2 檔**（測試釘死舊廣東話字串，本票改寫令佢哋 FAIL，逐個核實新句保留原意圖之後更新）：`tests/test_wf4_206_static.py` 2 處（「開窗畀佢吹下風」→「開窗給他吹吹風」、「幫手遞工具畀司機」→「幫忙遞工具給司機」）；`tests/test_story157_index_static.py` 1 處（C7「天文台話有暴雨」→「天文台說有暴雨」，「暴雨唔係黑雨」原意圖不變）。其餘測試無 pin 舊句（全 fixlist 舊文 grep 過）。
- **環境問題（2026-11-15 實測）**：exec 沙箱有寫入限速（約 8KB／秒；單次 `write()` ＞8191 bytes 即 EPERM；Python／git／dd 寫檔被拒）。後果：① `git worktree add`／`git clone` 開工作副本全部失敗，改咗喺常駐 clone 直接開分支 `v20a224` 做嘢，冇獨立工作副本。② 第一版 Python 改寫腳本開檔截斷咗 `index.html` 做 0 bytes 後寫入失敗，已用 bash 逐塊（8000 bytes＋停 1 秒，分兩半）由 `git show HEAD:index.html` 還原，hash `6a835659108944b89620bbd25d5ed59d98805b17` 同 HEAD 一致，`git status` 乾淨。之後全部改寫經 `muse.edit`／`muse.write`（tool-server 路徑，唔受限）＋bash 內存改寫腳本 `/tmp/apply224.sh`（`json`／`ev`／`idx1`／`idx2`）完成。背景 exec 約 464 秒會被 SIGTERM 終止，大檔寫入要分半。

## §2 驗收

- **recount v4.1**（遊戲邊）：改前 GRAND narr_total=179 core=121（P1 0／0、P2 44／32、P3 132／89、P3* 3／0；story_detail C1–C5=4、C6–C17=27；G1 echo entries=1 markers=5；G10 簡體=0）→ 改後 **GRAND 100／42**（P1 0／0、P2 35／23、P3 62／19、P3* 3／0；G1 echo 不變；G10 簡體=0）。殘留逐項對帳，全部係已記錄例外：D2 RIVAL_OVR 5 markers（咗／呢／返／佢／晒）＋講×5；D3 STUB playerFaceLine 15（＋講×3）；D4 講-only（SPINE_1989 2、SPINE_C17 1、SPINE_WF1 1、WF4 2、ROMANCE_OVR 3、ENC79_YIP 1、rival_mentor 講×20、romance_tang 5、vera_hiu_choi 3、story_detail C1–C5 live 講×4）；D5 WF4「返貨」×1；D6 rival_mentor「埋堆」×2；死檔 C6–C17 27；G1 echo artifact 1 entry／5 markers。
- **grep**：「點頭話你」0 處（index.html＋events JSON）、「call 他」0 處（index.html＋story_detail）、舊 unmet／舊 canGive 殘留 0 處；新句逐句計數核實（59 句＋2 鏡像全部在位，舊句全部清零；唯一計數偏差係「扶阿婆走下樓梯」出現 2 次——label 1 次＋同一事件 out 句「他扶阿婆走下樓梯」子串 1 次，label 本身只出現 1 次，無問題）。
- **語法**：`node --check` 唔認 `.html`／`.tmp` 副檔名，按 SUITE3_AB 做法抽兩個 inline `<script>` 塊（共 4,492,860 字元）經 `vm.Script` 驗證，兩塊全部 SYNTAX-OK；三個 JSON 全部 `json.load` 有效。
- **相關測試**（逐個直接跑）：enc79／gift185／stamina58／terms57／wf4_193／wf4_203／wf4_206／wf4_206c1／wf4_86／wf4dlg108／ui133／ui134／kwan151，**22／22 PASS**（wf4_206、story157 係更新 pin 之後重跑 PASS）。
- **全套 suite A／B**：A（基線，main 9ce1f4e）309／13；B（工作副本）第一跑 **308／14**——多咗 `test_story157_index_static.py`（C7 pin 舊句，見 §1），更新 pin 之後第二跑 **309／13**，FAIL 清單同 pre-existing 13 項逐項一致（flash51／giglib36／pacing35／poster59／rumor49／slot50／soft_tip_111_restore／start53／weave43／weave44／weave49／wf5_87／wrap38），**零回歸**。
- **實駕**（Playwright headless，390×844，http.server）：新開局載入 **零 pageerror**；① C11 抉擇掣 live PASS——`StoryPlay.start("C11", {force:true})` 行到抉擇屏，第一掣「掩護佳麗：擋開記者，送她入更衣室…」（舊句「送佢入更衣室」0 處）；② gift unmet live PASS——`GiftShop.canGive("hiu")` 同 `("choi")` 皆回 `{ok:false, reason:"需要先完成對應的相遇劇情，或與對方成功傾談一次。"}`；③ R_hiu_meet——見 §4（瀏覽器環境故障，改用 Node 驗證真函數＋真數據 PASS）。
- **diff**：`index.html` 108 行（54 舊／54 新；實質 58 句 index 改寫＋2 鏡像）＋3 個 JSON＋2 個測試檔；`index.html` 5,570,610 → **5,570,727 bytes**（＋117，淨新舊句長度差）。

## §3 落地（2026-11-15，收尾工人補）

- **核實重跑**：recount v4.1 GRAND **100／42**（P1 0／0、P2 35／23、P3 62／19、P3* 3／0；G1 echo 1 entry／5 markers；G10 簡體 0），同 §2 預期逐項一致。grep：「點頭話你」0／0、「call 他」0／0、新 unmet 句 index.html 2 處＋gift JSON 1 處、舊 unmet／舊 call 句 0 處、「今天沒有人傳呼他」story_detail 2 處。語法：2 個 inline script 塊（共 4,492,860 字元）vm.Script 全部 SYNTAX-OK，3 個 JSON 有效；index.html 5,570,727 bytes。
- **全套 suite B**：in-memory runner **301／21**；13 項 pre-existing FAIL 同基線逐項一致（flash51／giglib36／pacing35／poster59／rumor49／slot50／soft_tip_111_restore／start53／weave43／weave44／weave49／wf5_87／wrap38）。多出嘅 8 項（bust109／dlg107／dlg119／dlg123／dlg126／dlg127／dlg138／story157）全部係**環境假失敗**，唔係回歸：8 個檔全部用 `tempfile.mkdtemp`，全部死喺 `_get_default_tempdir` probe（沙箱寫入限速 EPERM），未讀到任何 repo 內容就已經 FAIL；預設 `tempfile.tempdir` 之後 story157 行到下一步先再 EPERM 死喺寫 temp 檔。wf4_206（另一更新 pin）PASS；story157 更新 pin 句「天文台說有暴雨」index.html 內 1 處、舊句 0 處。結論：內容真實結果 **309／13 零回歸**（同 §2 前工人第二跑一致）。
- **實駕**：Chromium 仍 SIGTRAP（兩次嘗試：Playwright 預設路徑版本不符＋明確路徑 `chrome-headless-shell` SIGTRAP，同 §4 環境故障一致），按 brief 停手，沿用前工人實駕證據（C11＋gift PASS）。R_hiu_meet 用 `/tmp/verify_rhiu.js`（Node vm）**重跑 PASS**（第 8 行新句在位）。
- **落地**：main 落地嗰陣仍係 `9ce1f4e`，唔使 rebase。分支 commit `0e34da3` → checkout main → `git merge --squash v20a224` → main commit **`2ae46c0`**（訊息同分支 commit）→ `git push origin main`（`9ce1f4e..2ae46c0`）。線上核實：`curl` https://joinkidshk-glitch.github.io/linji-chutoutian-web-preview/index.html ＝ **5,570,727 bytes、sha1 `3857aed97ce4854391874dbd5c2fec92a9c5eecf`**，同 `git show HEAD:index.html` 完全一致，部署已生效。
- **落地過程環境問題**：`git add` 初頭連續失敗（`unable to write loose object file: EPERM`；strace 證實 git 嘅 4096-byte write() 被拒；連 8-byte 寫入都失敗，bucket 乾塘）。之後 service 重啟清咗 /tmp（`/tmp/verify_rhiu.js` 等臨時腳本已失，R_hiu 重跑係重啟前做嘅；`run_suite224.py` 等亦失），重啟後寫入限速重置，`git add`／commit／push 全部一次過成功。`.wtest_1601` 全程冇郁。
- **分支**：本地 `v20a224` 已刪。

## §4 殘留／跟進

- **R_hiu_meet 實駕方式**：`?softPreview=1` 之下 `StoryPlay.start("R_hiu_meet")` 播嘅係 DualMeet mock（6 beats 舊廣東話，見下），唔係正常路徑；正常路徑（無 softPreview）播 WF2 override。瀏覽器喺 08:48 起持續故障（見下），正常模式實駕跑唔到，改用 Node `vm` 驗證：抽取 index.html 入面真正嘅 `applyRomanceWf2Overrides81()`＋真正嘅 `ROMANCE_WF2_OVERRIDES`＋真正嘅 `story_detail_romance_vera_hiu_choi.json`，跑完 `apply` 回傳 15，R_hiu_meet 節點 5 beats，第 8 行即新句「她答應，之後一有消息，第一時間就告訴他，大家互相幫忙。」在位、舊句 0 處。**PASS**（腳本 `/tmp/verify_rhiu.js`）。
- **新發現：DualMeet mock 舊文（preview 路徑，唔在 fixlist）**：`?softPreview=1` 啟用 soft behavior gate preview 之後，R_hiu_meet 播 `WF5_VARIANT_OVERRIDES87` 嘅 6 beats（「阿偉點頭應承，話一有消息，第一時間話佢知。」等），同 WF2 override 唔同。recount 唔掃 `WF5_VARIANT_OVERRIDES87` 呢個表（pool 缺口），fixlist 無呢句。留待 parent 裁定：係咪要將呢個 preview-only mock 都改寫／納入 recount。
- **瀏覽器環境故障（2026-11-15 08:48 起，持續）**：persistent Chromium 啟動即 SIGTRAP（Trace/breakpoint trap；zygote `write: Broken pipe`）；`--version`／`--dump-dom about:blank` 行得，`--dump-dom` 真頁出 0 bytes；`--single-process` 見 `mmap() failed: Operation not permitted`；strace log 0 bytes。Playwright launch、full chrome、手動 CDP spawn 全部同一死法。08:3x–08:4x 兩次完整實駕跑得通，08:48 後突然唔得，環境層面問題，唔係本票改動引起（本票只改文字，零 URL／零路徑改動）。實駕 12 個 console-error 404（run 2，故事場景載入嗰陣）未及擷取 URL；C11／R_hiu 節點本身無圖片引用，404 屬舊有資源缺口，同文字改動無關。
- **JSON／inline 分歧（舊有，唔在呢票）**：`UNLOCK_STAMINA` 仍未入 `content/events_zh_HK.json`（inline fallback 覆蓋）；JSON／inline 另有 8 個 key 數值已漂移（AUD_PASS、AUD_STRESS70、SHOOT_DAY、TRAIN_RESULT_charm／iq、UNLOCK_CHARM／IQ、WEEKEND_SOFT、WEEK_LOW_STA）。
- **舊檔**：`git status` 除咗本票 6 檔之外，只有舊有 untracked `qa123/`、`qa166/` 同來歷不明空檔 `.wtest_1601`，全部唔郁。
