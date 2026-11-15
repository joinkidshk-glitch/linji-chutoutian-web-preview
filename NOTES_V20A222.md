# NOTES_V20A222 — 書面語改寫 P3：事件／感情／對手線旁白＋G1／G9／G10

- 日期：2026-11-15
- 基線：main `3e8dfba`（v223，when 顯示值修復；P3 分支原本基底 v221 `7574287`，v223 落地後 rebase 上去，零衝突）
- 範圍：書面語改寫票 P3（遊戲邊事件等）。RECOUNT-REPORT live 確數 2,535（重抽對新 main：917 句／2,584 標記）；另 G1 刪 echo、G9 刪 nodeRipple、G10 修簡體字。
- **修正後基線（見 §1 尾）**：抽取器／recount tokenizer 漏咗 WF4 `sp`／`tx` 欄位，P3 基線應為 **2,948**（＋413，全部嚟自 WF4 旁白 beats），唔係 2,535。

## §1 改動內容

- 917 句全部改寫（五個工人並行）：WF4 471 句／ROMANCE_OVR 170 句／RIVAL_OVR 48 句／ENC79 94 句（LU 19＋LIU 10＋MAK 48＋YIP 17）／WF4_FRAG 28＋NEWS82 12＋NP_GAL 4＋SUSPENSE212 2 句／TUTORIAL 24＋freeplay STUB 34＋story_detail rival_mentor 22＋romance_tang 5＋vera_hiu_choi 3 句。
- 套用方式：index.html 按 offset 換字串字面量（781 處）；JSON 按 path 設值（STUB 27＋rival_mentor 8＋romance_tang 1 處）。實改 817 處，new==old 跳過 100 句。
- **對白誤抽（P3 新發現，大問題，已修）**：ROMANCE_OVR 170 項當中有 47 句係角色對白（林曉晴 28／徐寶珊 17／助導 2），抽取嗰陣 beat 物件 `speaker` 寫喺 `lines` 之後，分類器誤判做旁白，工人改寫咗做書面語。統籌用 beat 對位檢測腳本（`/tmp/detect_dialogue.py`，嚴格＋寬鬆兩版 regex 一致 47 句）逐句還原 `new=old`，note 寫明原因。RIVAL_OVR 0 句；P2 六池覆核全部 0 句（v221 無此問題）。教訓：抽取器唔可以假設 speaker 喺 lines 之前，之後抽取要先做 beat 對位檢測。
- **WF4-0083 統籌修正**：工人版「跟他買魚」代詞方向錯——「同佢買魚」嘅佢係阿姐（買魚對象），應係「她」；句尾「呢」改「的」。新文：「阿姐開心得多送了兩條蔥給他，說回去跟左鄰右舍說，那個電視上的年輕人就是跟她買魚的。」
- **ENC79「發言者：」對白**：23 句開頭「發言者：」嘅巧遇對白句留廣東話，抽查（保鑣／PA／武指開頭）正確，接受。STUB 5 句 playerFaceLine 第一人稱獨白留廣東話（G4），抽查正確。RIVAL_OVR-0023 冒號後無引號直接引述留廣東話，接受。
- **G1 刪報紙 echo**：index.html 25 個 rumorEcho 字串欄位（13 有內容＋12 空）＋7 個 echo 物件＋plumbing 兩處（`rumorEcho: ev.rumorEcho` 抄寫、ev.echo → mockRumors 推送塊）。注意：echo 行尾帶住事件物件嘅關括號（` } },`），第一版腳本成行刪走令 7 個 NEWS82 事件冇咗結尾，`node --check` 即刻捉到，修復補返 6 個 `},`＋1 個 `}`。教訓：刪行之前要睇埋行尾有冇帶結構符號。
- **G9 刪 nodeRipple 死碼**：index.html 14 處＋STUB 5 處＋SANDBOX 5 處。注意：SANDBOX 嘅 nodeRipple 係每組最後一欄（無尾逗號），刪行要一併拎走上一行尾逗號，否則 JSON 非法（`json.loads` 即刻捉到）。STUB 嘅係中間欄，直接刪行就得。
- **G10 簡體字**：content/gift_react_copy.json 软→軟 ×2、别→別 ×2。
- TUTORIAL resync：inline 24 句改寫即係 resync（live 行 content/tutorial_zh_HK.json，已經係書面語，唔郁佢）。
- apply_work.py allowlist 加咗 7 個「講＋動詞」書面語固定詞（講電話／講起／講著／講回／講解／講大道理／講了）；補漏嗰陣再加「返貨」（書面商業用語，唱片返貨）。
- **P3 補漏① WF4 旁白 beats（W-C 觀察 #1 觸發，413 標記）**：`DAILY_EVENTS_WF4` 入面 112 句 `sp:"旁白"` 嘅 `tx` 全數未改寫——tokenizer 只認 `speaker`／`lines`，唔認 WF4 用嘅 `sp`／`tx` 欄位，抽取＋recount 一齊漏咗。根治：recount.py（NARRATION_FIELDS 加 `tx`；tokenize_js 視 `sp` 為 speaker）＋extract_work.py（tokenize_js_pos 同樣修正）。修正後基線：P3 2,535 → **2,948**（＋413；其餘池零變動；`sp`／`tx` 全檔只出現喺 WF4，231 次，修正無副作用）。抽出 109 句（413 標記，3 句 0 標記唔抽）→ W-E 改寫 → 覆核（109/109、結構一致、禁詞 0、殘留只得「返貨」1 個合法固定詞；抽查 0001／0006／0037／0050／0109＋G5 引文項 0025 全部意思保留、行話保留）→ 套用（offset 因為 pack 同步移位＋14，要重抽先套；實改 109 處）。驗收：WF4 415 → **3**（講×2＋返×1，全部 core 0，合法固定詞）。
- **P3 補漏② 教學 pack 同步（47 標記，runtime 可見）**：`TEXTFIX55_EXACT`／`TEXTFIX57_EXACT` 喺載入嗰陣將 live JSON 句（key）換成 inline 句（value），所以玩家見到嘅教學句係 pack 值，唔係 JSON 原文——P3 只改 inline，pack 值仲係 v108 廣東話，實機教學句仍見廣東話。核實：pack 280 項入面 49 個 key 仍在 loaded JSON（live），其中教學 30 個 key、value 標記 47。同步咗 29 個教學 pack 值（21 個 done 項＋TUT_MAP 0001＋0010 兩句版＋TUT_TRAIN 4 句＋短版 2 句；腳本 `work/rewrite/pack_sync_tutorial.py`，逐項斷言次數；TEXTFIX57 入面另有 1 個 TUT_TRAIN title 值）。連帶修咗 TUT_MAP body[0] 首句（見下）＋TUT_TRAIN 4 句（見下）＋TUT_TRAIN title（「訓練夠先報得試鏡」→「訓練夠了才報得試鏡」）。驗證：模擬 pack 查表，runtime 教學句標記 47 → **0**；text108 0 fails。
- **P3 補漏③ TUT_MAP body[0] 首句（text108 第 12 個 FAIL，W-C 提議案）**：P3 寫法首句逐字撞返 v17b 電報句「地圖上的地點，就是你可以去的地方」，而測試「新句在位」同「舊電報句已清」用緊同一條字串——W-C 話「測試唔使再改」係錯嘅，改遊戲文字之後「新句在位」嗰個 pin 都要跟住改。歷史核實：v17b 嗰句係獨立短句（電報句）；v108 將兩短句合併做一句廣東話長句，測試自此釘死舊短句；P3 機械還原撞返舊短句。拍板（統籌）：首句改做「地圖上標示的地點，都是你可以前往的地方」（W-C 提議案首句；次句保留 P3 寫法），測試兩個 pin 一併更新。TUT_TRAIN 4 句一併改做書面語（0 標記但 pack 令佢哋 runtime 可見，唔改玩家仍見廣東話味；inline＋pack＋測試 pin 一齊改）。
- **P3 補漏④ rom183 LINE183（runtime 覆寫漏網）**：`rom183ApplyLineOverrides()` 硬寫 `const LINE183 = "去佢哋常出沒嘅地方，..."`，喺載入嗰陣 append 入 TUT_MAP body[1]／bodyAlt[1]（玩家可見）。改做書面語版，rom183 測試 pin 一併更新。C1／C3 嗰啲 Cantonese runtime 覆寫（greet／gift react）係對白，唔郁。另查 jan67OpeningTextFix（JAN67 map 值 0 標記）無漏網。

## §2 驗收

- recount.py（遊戲邊，修正後 tokenizer）：P3 live **2,948** → **334**（−2,614，−89%），334 全部逐項核實合法——保留句 316（47 句 ROMANCE 對白 221＋23 句 ENC79「發言者：」對白 57＋5 句 STUB G4 獨白 14＋14 句 rival_mentor 已係書面語 15＋4 句 romance_tang 4＋3 句 vera_hiu_choi 3＋2 句 WF4 講固定詞 2）＋已改寫句殘留 18（講固定詞 16＋RIVAL_OVR-0023 冒號引述 3＋WF4_FRAG-0027 『』G5 引文 1，減 WF4 beats 補漏嗰 1 個「返貨」係另計）＋WF4 beats 補漏殘留 3（講×2＋返×1，core 0，合法固定詞）。**基線修正**：原本報 2,535，係因為 tokenizer 漏咗 WF4 `sp`／`tx` 欄位（補漏①），正確基線 2,948；殘留 333→334 差 1 個，係 WF4 beats 新句入面嘅「返貨」標記（合法）。P1 維持 0；P2 維持 37。
- G1：recount entries 剩 1（`"wrapecho:"+starId` 一句 code 誤計做 echo 欄，假陽性，唔係欄位）；markers 4 係同一句。G10 簡體 0。
- `node --check`：index.html 兩塊 inline script 全部通過（rebase 後重驗一致）；5 個改過嘅 JSON 全部合法。
- 全套 suite A／B：A（pristine v223）309／13；B（工作副本）**309／13**，FAIL 清單逐項一致（13 項全部 pre-existing：flash51／giglib36／pacing35／poster59／rumor49／slot50／soft_tip_111_restore／start53／weave43／weave44／weave49／wf5_87／wrap38），**零回歸**。中途曾經 B 305／17，4 個新 FAIL 全部係教學 pack 同步改咗 runtime 可見字串、測試 pin 舊廣東話（guidance34 打聽句、rom183_logic LINE183「撞到先」→「撞到才」、terms57 B1 TUT_TRAIN title、text55 A6 TUT_NPC body）——逐個核實新句保留原意圖之後更新 pin，重跑 B 回到 309／13。
- git diff：index.html 114 行增／114 行減（巨行計；實質 781 處主批＋109 處 beats＋29 個 pack 值＋LINE183＋TUT_MAP/TUT_TRAIN 句）＋24 個測試檔（行號 resync＋pin 更新＋wf2_81／wf3_82 斷言重寫）；總行數 62,897 → 62,860（淨 −37，G1／G9 刪行所致）。

## §3 落地

（待填）

## §4 殘留／跟進

- recount strip_quoted 只剔「」／""／“”，唔剔『』：WF4_FRAG-0027 『你哋走唔走呀？』入面 1 個「唔」會一直殘留，屬 G5 合法，唔係漏網（同 P2 SPINE_1990-0079 同一道理）。
- STUB 保留句 7 項（14 標記）：其中 5 句係 playerFaceLine 第一人稱獨白（G4，留廣東話正確），其餘 2 句係已係書面語／講固定詞。
- story_detail_c1_to_c17.json pack 死檔仲有 5 個 nodeRipple（G9 範圍外，C6–C17 死檔唔郁，留返 pack 清理票）。
- 47 句對白還原之後，recount P3 唔會跌到 0——呢批殘留屬合法（對白留廣東話），NOTES 呢度講明。
- **待 parent 定奪（範圍外，唔好擅自擴圍）**：
  - **recount pool 外旁白約 522 標記**（CHOICE47 73、COMMIT48 77、WF3_TALK 76、ENC83/84 八檔 N-line 合計 227、ENC79_TEA_POOL 25、EXODUS_RUMOR_SEEDS 24、WF4_FEN_INTRO 16、ENC79_BEATS 4）。傳聞種子／茶室池可能係已刪／將改系統嘅死碼，唔宜盲改。
  - **P1 pack 缺口（已落地 v220，實機仍見廣東話）**：TEXTFIX55/57 live entries 入面，EVENTS 9 個 key、12 標記（例如「壓力太大，個人冇晒神…」「新課程開咗：魅力課可以報名。」）＋PHASE1 2 個 key、4 標記（「周采兒在場邊多望咗兩眼…」）——P1 改咗 inline＋JSON 但冇同步 pack 值，同本票補漏②同一機制。
  - **Gift pack 2 標記**：「心領了。這份心意我記住，唔使再破費。」＋「要先喺故事入面識到佢，或者同佢傾過一次計，先送得禮。」——gift react 不在 P3 池。
  - 其餘 231 個 pack key 只在 index.html（inline／其他），對 loaded JSON 已死，唔使理。
- 下一票：攻略邊 P4–P6（另一統籌進行中）。
