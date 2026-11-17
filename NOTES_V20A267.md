# NOTES — v20a267 傳聞系統刪除＋打聽變情報站

- 分支：`v20a267`（工作副本 `linji-work267`，基底 main `9bb08fc`／v266）
- 拍板：用戶 2026-11-14 拍板成個傳聞系統刪除（「很雞肋」）；同日拍板打聽變情報站——直接話玩家知邊度有工開、邊個星喺邊度出沒，唔使經傳聞卡。
- 紅線：SAVE key `starVolunteer_map_v19w`（10 次）、`"v20a10"`（7 次）、softRev `s107` 全部不變；`?v=` 不變。`node --check`（抽出主 script）通過。
- 淨行數：`index.html` 46942 → 45543（count('\n') 計，淨 −1399 行）。注意：v266 測試名內「總行數 46953」本身已比真數多 11（git HEAD 實數 46942），帳本鏈承接該 +11 舊差，今次只補 v267 真 delta −1399。

## 刪咗啲乜（逐項，grep 零殘留已核實）

全部以下識別碼喺 `index.html` 命中 0（2026-11-17 晚核實，另加 `rivalryResultRumor`／`romwind:`／`WF4_FRAG_SEEDS`／`rumor_wf4_`／`rumor_fen_exodus_tip` 亦係 0）：

`mockRumors`、`S.notebook.rumors` 鏡像、`S.mockJournalSeeded` 傳聞播種、`seedFreeplayRumorShells`、`MOCK_RUMOR_SEEDS`、`MERGE_FRAGS`、`MERGE_PAIRS`、`MERGE_FLOW`、`findMergePair`、`heardPickIds`、`mockMergePick`、`INTEL_FLAGS`／`ensureIntelFlags`／`setIntelFlag`／`hasIntelFlag`／`hasMergedIntel`、`INTEL_USE_POINTS`、`INTEL_CARD_USE_POINTS89`、`enc79HasMerged`、`enc79GrantFrag`／`enc79GrantRumorCard`、`wf3GrantRumor`、`mergeIntelGigs`／`INTEL_HIDDEN_GIGS`、`mergeWf3Gigs`、`stepRumor`／`rumorAny`／`liveRumors`／`evalTrigger_AND_softRumor`／`rumorHearHint`／`rumorPlayerTitle`／`rumorSeedsRequired`、`pushNewspaperRumor`、`SIDE_PAPER_FRAGS`、`TEXTFIX55_RUMORS`、`EXODUS_RUMOR_SEEDS`、`EXODUS_FEN_INTEL`、`wf4SeedFrags`／`WF4_FRAG_SEEDS`、`S.story.rumors` soft 遷移鏡像、`rumorStateLabel`／`displayRumor`／`familySafeRumorText`、`MOCK_TOAST.rumorGained`、`noteWeekHighlight("rumor", …)` 兩處、`renderRumorPane`＋`#home-pane-rumor`＋`#htab-rumor`（按鈕＋全部 CSS）＋`BOOK70_TAB_GROUP` 內 `rumor:"news"`（改 `clippings`，修咗一個 live blank-page bug：news 組預設 sub-tab 指住已刪傳聞頁）、`setHomeTab("rumor")` 跳轉、`markRumorTutorialDone`／`rumorTutorialDone`＋教學「揀兩張拼合」步驟、`MOCK_ASK` 5 個 `grantsRumorId` 欄位、`RUMOR_STATE_ZH`、`WEAK_WHISPER`／`.weak-whisper`、`tutorialFxFingerErr`、`mockIntelHits`、`br89HoldsCard`／`br89CardUsePointForGig`／`br89CardUsePointForStar`、`intelLineForGig`／`intelSightLineFor`、`rivalryResultRumor`（連埋 `mergeRivalGigs` 入面 try/catch 包住嘅死呼叫一併清走）、`content/STUB_RUMOR_FRAGMENTS_v1.json`（刪檔）。

其餘清理：`ensureMockJournal` 改做 debts-only（`S.mockDebts` 初始化、`ensureFavorLedger`、`ensureFamilyHomeDebt`、`seedExodusFenPair`、`healMayDebtCopy`、`syncNotebookMirror` 原封保留）；`S.intelFlags` 成個刪（舊存檔殘留自然失效）；三個 stale 註解＋「未聽聞」兩個死渲染分支一併清走；`iconHtml112("✨")` 隨 `intelLineForGig` 一併消失（板卡唔再有逐張情報行）。

## 三個硬效果現況＋處理

1. **《星夜迷離》臨時替工**：已在 `content/gigs_new.json`（`trigger: {kind:"rel", npcId:"luk_baakyin", relMin:25}`）。核實發現 `triggerGigOn` 嘅 `rel` case 只讀 `S.npcs[npcId]`，而星好感從來只喺 `S.stars[sid].fav`——呢個 trigger 喺 live 從來觸發唔到（v232 設計假設錯，佢嘅 T7 測試只 mock `S.npcs`）。**已修**：`rel` case 改讀星好感（`enc79StarState`／`S.stars[...].fav`，`Math.max` 埋舊 `S.npcs` fallback）。順帶解鎖埋另外兩張 rel trigger 通告（`gig_1992_film_204` liu_bingxing ≥60、`gig_1992_tv_203` luk_baakyin ≥60）。
2. **W3_ho_liao（WF3 鏈 B）**：閘由 `hasIntelFlag("intel_liao_money")` 改做廖炳星 enc79 tier ≥1（`enc79StarState("liu_bingxing").fav`，tier ≥1 即 fav ≥10，見過廖就開）。**注意：brief 寫嘅 `enc79TierOf(S.npcs.liao_bingxing)` 喺 live 永遠唔會觸發**——`S.npcs` 從來冇星 id（`liao_bingxing` 根本唔係 key，星 id 係 `liu_bingxing`），故用星好感讀法。`when`→「識咗廖炳星之後」；synopsis 改寫做識咗廖嗰組啲人；beat「你拼到嗰單嘢，算你醒目」→「你聽到嗰啲嘢，算你醒目」；`actHint`→「關於廖炳星嗰組——何生有句說話想提點你」。GRANT229 映射（W3_ho_liao_a/b → gig_1990_tv_209/210）原封不動。`syncGig(WF3_LIAO_GIG)` 呼叫唔存在，唔使清。
3. **N8_d（WF3 選美後台葉敏芝疑雲）**：`wf3PrepareNode82` 嘅 `hasIntelFlag("intel_yip_truth")` 檢查已刪，**N8_d 改做無條件**（保留「已有 N8_d 唔重加」去重）。notes 改寫做場內聽風聲得知；對白句「我都係聽嚟聽去拼返出嚟先知係誤會」係角色口語，保留。yip echo 嘅 `knew` 改做 `StoryOC.getFlag("flag_yip_warned82")`。`fongCardHigh` 第二個 disjunct（`hasIntelFlag("intel_mak_injury")`）已刪，只留 `StoryOC.isDone("A_fong_crisis")`；fong mid/high 嘅 `wf3GrantRumor` 改做直接 toast（武行口風／高危預警）；wf3 harvest 入面 `wrapped=false` 死分支連 grant 一齊刪。

## 其他閘改動

- **gu_loan 前奏**：`br89HoldsCard("rumor_gu_money_heard")` 改做顧明輝 enc79 tier ≥1（同樣原因，唔用 brief 嘅 `S.npcs.gu_mingfai` 讀法；`beat.id==="gu_loan" && tier>=1`，`tier` 係 buildScript 作用域內 `enc79TierOf(st.fav)`）；`flag_mediate_gu_debt` 下游分版保留。`gu_foreshadow` 嘅 `enc79GrantRumorCard` 改做直接 toast 嗰句後台消息。
- **陸／廖／麥情報節拍**（`luk_intel`／`liu_repay`／`mak_intel`／`mak_respect`）：`enc79HasMerged(...)` 條件全部刪除，而家只睇 tier（例如 `luk_intel`：`enc79TierOf(st.fav)>=2`）。`chung_farewell` 嘅忠告改記旗 `S.flags.chungAdviceHeld229 = 1`（Q6，`chungAdviceCardHeld229` 改讀呢個旗；`CHUNG_ADVICE_CARD_ID229` 已刪）。
- **N2／N5 soft 閘**：`evalTrigger_AND_softRumor` → `evalTrigger_AND`，`rumorSeedsRequired`／`S.story.rumors` 全部刪除；N2／N5 而家唔使聽傳聞就開。`progressToward`／`softLockPlayerLine`／`storyMainProgressLine` 入面「未聽聞」／「聽到傳聞：」行全部刪除。
- **rivalryScore**：傳聞 +1 點已刪，而家 N3 完成 +2、報紙 `rival:gao` +1，上限 3（`gig_1991_film_102` 要 3 分）。
- **BR89 單卡使用點系統**成個刪除（見上）；`enc79ChoiceFx` 路由不變（`liu_decline` 等 fx 名仲喺度），但 `enc79RunChoiceFx` 入面推辭／沉默等分支唔再派任何嘢（唔派卡、唔派債權）。
- **訓練微事件**：`ev.fragId` 唔再派碎片卡，改為無條件行 `fragFallback`（人氣 +1）＋fallback 文案。
- **WF4 碎片庫**（`WF4_FRAG_SEEDS`／`wf4SeedFrags`）成個刪除；鏈 F 氛圍靠 WF4 日常事件本身＋報紙。**Exodus-Fen**：`EXODUS_FEN_INTEL`／`rumor_fen_exodus_tip` 已刪，芬姐口風改做離港 toast 副文（「臨走佢漏咗句片場口風畀你。」）；Fen 債權／債項播種（`seedExodusFenPair`）保留。

## 情報站改法（打聽結果點顯示）

- **`S.intelAsked`**（新，action id → day）：`fresh()` 加入，取代「已聽過」卡鎖；問過即永久鎖住，toast「呢單情報已經聽過。」
- **`MOCK_ASK`**：5 個 `grantsRumorId` 改做 `intelText`，直接用返 `MOCK_RUMOR_SEEDS` 對應 id 嗰段文字做結果（書面語化：刪「聽聞／據聞」，「密密」→「頻密」）。`applyMockAsk` 回傳 `{ok, added, toast: intelText, rumorId: null, intelTitle, intelText}`，唔寫卡。5 段文字：tvb_rules「入廠拍劇最忌遲到及亂闖直播區，務必跟隨場記用餐。」（茶餐廳＋事務所兩處共用）、gao「高俊傑昨日拍戲時擅自加戲搶鏡，遭導演當場斥責。」、hiu「曉晴剛拍畢古裝劇，近期轉接時裝喜劇，急需反應敏捷的臨記。」、choi「采兒最近頻密接拍賀歲片，更想物色新臨記做替身。」
- **`act_cha_hall_tea`（大堂飲茶）**：`enc79TeaListen` 改做直接講情報——有風聲嗰陣直接講星名＋地點＋「3 日內有效」；冇風聲嗰陣直接講一句 `ENC79_TEA_POOL` 茶池文字；女角風聲（romwhisper）同理。唔寫卡，冇「已持有保底」。
- **`act_ho_rumor`（何生聽風聲）**：`enc79AgencyWind` 照行（`enc79GrantWhisper` 只寫 state），結果直接講星名＋地點＋3 日窗，另加板上有通告就嚟開鏡嘅提示；同日再聽係「今日啲風聲講完喇」，但何生人情照加。
- **風聲系統保留、只寫 state**：`S.starWhispers`／`S.romWhispers`（3 日窗）、`enc79GrantWhisper`／`rom176GrantWhisper`（唔寫卡、唔叫 `ensureMockJournal`）、`enc79PaperWhisper`（`commitMorningPaper` 行 `edition.shorts` 入面 `source==="side"` 嗰 3 張：`side_lu_concert`→陸柏言、`side_liao_newfilm`→廖炳星、`side_mak_wrap`→麥震東，直開風聲窗；其餘 9 張純顯示）。
- **「邊度有工開」**：(a) 打聽結果直接講情報文字，(b) 風聲結果直接講星名＋地點＋時限，(c) 通告板本身就係「邊度有工開」嘅來源。**冇發明新 helper 列出當日邊啲地點有通告**——搵唔到現成 helper，唔另起系統。

## 測試

- 新檔 `tests/test_rumor267_static.py`（取代已刪 `tests/test_rumor49_static.py`）：斷言傳聞頁／`#home-pane-rumor`／`renderRumorPane`／`mockRumors`／`MERGE_PAIRS`／`INTEL_FLAGS`／`mergeIntelGigs`／`rumor_gu_money_heard` 全部消失；W3_ho_liao avail 讀廖 tier；N8_d 無條件；`gig_1991_tv_203` trigger 係 rel／luk_baakyin／25；紅線（SAVE 10 次、`"v20a10"` 7 次、softRev `s107`）；`node --check` 通過。**全 PASS。**
- 改寫／重寫嘅測試（全部逐檔跑過，PASS）：`test_wf3_82_logic.js`＋`test_wf3_82_static.py`、`test_gig229_trigger.js`、`test_gig229_press94_advice.js`、`test_br89_logic.js`（F 拼合／卡使用點改消失斷言；B6 推辭唔再派卡；G2 改 tier 閘）、`test_br89_static.py`、`test_enc79_logic.js`（風聲 state-only、茶＝直接情報、luk_intel 只睇 tier、MOCK_ASK intelText）、`test_enc83_logic.js`、`test_enc84_logic.js`（五張預告卡 grants 已刪；鍾告別改記旗）、`test_guidance34_logic.js`（§b 傳聞閘刪除；§d 傳聞頁改消失斷言；教學債改直接補種）、`test_book143_logic.js`、`test_book145_logic.js`、`test_pacing35_logic.js`（訓練八卦改 fallback 人氣 +1；b4 改相對量度，修 flaky——b1 真隨機可能先加人氣）、`test_progress71_logic.js`（「聽到傳聞：」行已刪）、`test_rom176_logic.js`（romwind 卡已刪）、`test_verify37_logic.js`（seg9 打聽直接出情報文字＋已問鎖）、`test_story179_logic.js`＋`test_story179_static.py`（「聽到傳聞」提示守衛改驗已刪）、`test_weave32_logic.js`（成檔重寫做退役測試：花邊池 39 則保留＋commitMorningPaper → enc79PaperWhisper）、`test_weave42_logic.js`（Fen 口風改 toast 副文）、`test_weave43_logic.js`（刪 §1 兩個死抽取 `MERGE_FRAGS`／`EXODUS_RUMOR_SEEDS`）、`test_wf4_86_logic.js`（§5 碎片庫改消失斷言）、`test_rival_board_r2.js`（`rivalryResultRumor` 已刪；連埋 index.html 入面 try/catch 死呼叫一併清走）。
- 靜態 resync（純行號漂移，按內容重對、逐字核實；ok() 名內歷史行號標籤不變）：`test_kwan151_static.py`（14 釘）、`test_rom159_static.py`（7 釘）、`test_rom176_static.py`（6 釘＋romwind 改驗 state）、`test_tang152_static.py`（3 釘）、`test_tang171_static.py`／`test_tang173_static.py`／`test_gift185_static.py`（總行數＋openLoc DEF＋L4862 同行）、`test_travel114_static.py`（40 免費＋12 計數＋DEF 42125→40785＋WRAPPER 29882→28803，逐行旗檢查照過）、`test_text125_static.py`（三錨點 11754→11533、11896→11675、17157→16707）。
- 驗過唔使改、直接 PASS 嘅：`test_weave44_logic.js`、`test_cast252_logic.js`、`test_poster59_logic.js`、`test_nat92_logic.js`、`test_br89_favor_due.js`、`test_br89_deadflag_lint.js`、`test_cleanup100_enc.js`、`test_cleanup100_logic.js`、`test_gig229_counts.js`、`test_ladder95_logic.js`、`test_levels75_logic.js`、`test_aud91_logic.js`、`test_qa101_logic.js`、`test_rest58_logic.js`、`test_stamina58_logic.js`、`test_story191_logic.js`、`test_story198_logic.js`、`test_rom183_logic.js`、`test_release215_logic.js`、`test_weave410_logic.js`、`test_weave46_logic.js`、`test_weave48_logic.js`、`test_wf4_193_logic.js`、`test_wf4_203_logic.js`、`test_wf4_206c1_logic.js`。
- 之前已改好嘅靜態檔（今輪覆驗 PASS）：`test_weave45_static.py`、`test_newspaper214_wrap_static.py`、`test_weave47_static.py`、`test_book70_static.py`、`test_book141_static.py`、`test_book143_static.py`、`test_book145_static.py`、`test_c17route153_static.py`、`test_story172_static.py`、`test_story_gate113_static.py`、`test_guidance34_static.py`、`test_reconfirm236_static.py`、`test_polish48_static.py`、`test_contrast76_static.py`、`test_awards194_static.py`、`test_calib60_static.py`、`test_text55_static.py`、`test_enc79_static.py`、`test_enc84_static.py`、`test_verify37_static.py`、`test_wf4_86_static.py`、`test_ui128a4_static.py`、`test_icons112_static.py`、`test_years66_logic.js`、`test_jan67_logic.js`、`test_calib60_logic.js`、`test_aud91_logic.js`、`test_enc144_logic.js`。

## Suite

- 基線（v266）：**331／10**。十項已知 pre-existing FAIL：flash51／rumor49／slot50／soft_tip_111_restore／start53／weave43／weave44／weave49／wf5_87／wrap38。
- 今輪最終跑：`bash qa131/run_suite.sh`（工作副本，outfile `/tmp/v267/suite_final2.txt`）：**TOTAL PASS 332 FAIL 9**（341 檔；基線 331／10）。
- FAIL 名單（9 檔，全部係已知 pre-existing，原因逐一覆驗未變）：flash51（softRev marker）、slot50（softRev marker）、soft_tip_111_restore（地圖篩選 toast／show-all arm，0 項提及 rumor／intel）、start53（softRev marker）、weave43_static（見下）、weave44_static（softRev）、weave49_static（softRev）、wf5_87（`FileNotFoundError: linji-work86/...`，舊工作副本路徑）、wrap38（redline softRev s111）。
- 淨變化（＋1 PASS／−1 FAIL）：舊 `test_rumor49_static.py`（已知 FAIL，softRev stale）刪走，新 `tests/test_rumor267_static.py` 全 PASS。其餘 8 檔 FAIL 同基線完全一致。
- **weave43_static 澄清**：佢嘅兩項失敗（「seed flavor copy」——`屋企人催數，從來唔出聲`呢句喺基線 `index.html` 已經唔存在；「softRev unchanged」）係 pre-existing。已用基線檔案對照核實：基線版 `test_weave43_static.py` 對基線版 `index.html` 跑出完全相同嘅兩項 FAIL。**weave43_logic 喺基線本來就 PASS**（基線版對基線版跑過，ALL PASS）——今輪佢曾經 crash 純粹係 v267 刪咗 `MERGE_FRAGS`／`EXODUS_RUMOR_SEEDS`，而佢 §1 死抽取呢兩個 const（§1 根本唔用）；刪走死抽取之後恢復 PASS，唔係修復咗舊 FAIL。
- 第一輪最終跑（`/tmp/v267/suite_final.txt`）係 329／12——嗰陣有 3 個 v267 遺漏（pacing35_logic b4 flaky 斷言、story179_logic／static 傳聞提示守衛）未修；修好之後重跑，先係上面 332／9。

## 留低嘅嘢（唔係今票範圍，記低）

- `SOFT_RUMOR_BEHAVIOR_GATE_PLAYTEST_FIX_v1.json`（診斷文件，遊戲唔載入）同 seed／fixture meta 入面嘅傳聞字眼（`meta.softALock`、`relockNotes`、`playerFaceLine`）留返做歷史記錄，冇改。
- CSS 註解約 L3443 仲提及 `tutorialPhase2FxOn`（已刪 gate 函數），註解緊貼嘅 `@keyframes tutFxFinger` 仲係 live——留返，唔郁。
- `ENDING410_ADJ_RUMOR`（結局「聽講如果…」純文案，唔讀 `mockRumors`）保留；`rumorEcho` 報紙模板欄位、`rumorKeys:[]` gig 欄位（inert，0 引用）、`star.rumorTeaser` 顯示文字、`intel:[...]` 陣列入面「聽聞…」句子、TEXTFIX55 對白數據入面「聽聞」字眼全部保留（唔係傳聞系統）。
- `test_br89_deadflag_lint.js` 嘅正則交替表仲列住 `hasIntelFlag`（已刪函數名，lint 照 PASS，因為 index.html 已經冇匹配）——留返，唔郁。
- 舊工作副本 `linji-work158` 入面仲有陸／廖／顧／麥四條支線 WIP 未落地（v266 已記錄），唔郁。

## 交代

- 冇 merge、冇 push、冇刪工作副本。分支做好＋suite 跑完，合併由統籌做。
- 改動檔案：`index.html`、`content/*.json`（5 檔：SANDBOX_BEHAVIOR_GATE、STUB_STORY_BEATS_FREEPLAY_SLOTS、SOFT_PROGRESS_SEED 兩檔、tutorial_zh_HK.json）、`content/STUB_RUMOR_FRAGMENTS_v1.json`（刪檔）、`tests/fixtures/behavior_gate_n1_n5.json`、測試檔約 60 檔（改寫＋resync；新檔 `tests/test_rumor267_static.py`，刪 `tests/test_rumor49_static.py`）。
