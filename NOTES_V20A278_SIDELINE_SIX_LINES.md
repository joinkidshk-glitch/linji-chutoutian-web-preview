# NOTES_V20A278 — 六線草稿抉擇全面實裝（支線補完跟進票，PLAN §4–§9）

## 背景

- v273 獨立核實發現：六線草稿旗（約 90 個）repo 0 命中，draft Beat 1–5 抉擇樹未實裝——PLAN §4–§9「維持」係設計 verdict，唔係 code 存在聲明；每線骨架在位（first／heart／beats／ChoiceFx）。
- 範圍判定（見 §1）：parent brief 寫「六線＝陸柏言、廖炳星、顧明輝、麥震東、駱家聲、魏詠男（PLAN §4–§9 逐線對）」係自相矛盾——**PLAN §4–§9 實際係駱家聲、魏詠男、齊鎮海、彭少祺、鍾楚凝、程天諾六線**；v273 發現亦係呢六線草稿旗 0 命中；跟進項 G-CHAI-2／G-PANG-2 亦指向 §4–§9。**實裝範圍定為 PLAN §4–§9（駱／魏／齊／彭／鍾／程）**。廖／顧／麥／陸已喺 v269／v271／v273 做咗；剩低嘅 §1–§3 C→B 升級（1.10／1.11／1.13／1.14／1.17，分開即派）要新庫通告對位，設計未定稿，列入未實裝清單，唔自行創作。
- 盤點表：`~/workspace/linji-sideline278-inventory.md`（49KB）。基線 main `d26a59f`（v277），`index.html` 45,503 行；新庫 `content/gigs_new.json` 287 張。
- 本票唔改 SAVE key（`starVolunteer_map_v19w`）、softRev（`s107`）、產品 `?v=`（`v20a10`）。

## §1 盤點結果（實裝前）

- 六線抉擇點總數：**30 點**（駱 6／魏 6／齊 5／彭 5／鍾 4／程 4），選項 67 個，抉擇旗 **67 支**。
- 67 支草稿抉擇旗**全部缺失**（66 支 repo 0 命中；唯一例外 `chai_silent` 僅 fx token 字串 1 命中，`enc79RunChoiceFx` 無 handler）。
- 30 個抉擇點全部缺旗＋即派＋下游讀取，其中 **12 點連選項 seg 都無**，要新寫對白＋新 seg。
- 59 行即派有 id，**全部係舊庫死 id**（新庫 0 命中），去重 53 張；「無即派」8 行係設計，唔加 row。
- §14 Q2–Q13 其實**全部已答**（`DECISIONS.md` 2026-11-15 21:41–21:46），brief 話未答係 PLAN 寫嗰陣嘅狀態，已過時；真正未落地嘅係實裝。
- 已落地、唔使 v278 再做：G-C2（鍾忠告卡，`chungAdviceHeld229` 旗制＋文藝片試鏡提示在位）；G-C1 已由 v274 落地（`gig_1991_film_213`《秋日絮語》）；G-CHAI-3 已滿足（`chai_repay` L37021 已係「企邊嗰場風波」；N13 回望 L13417–19 三處仍寫「站隊那場波」，唔屬 G-CHAI-3，唔好混淆）。

## §2 對上一手計劃嘅修正（逐段對過草稿後）

上一手計劃話「8 個新 beats」，逐段對過草稿後修正：**5 個所謂新 beat 嘅抉擇其實係喺現有 beat 場面尾**（草稿對白就係現有 beat 嘅場面），另開 beat 會重複場面＋要寫草稿冇嘅 setup 對白（自行創作）。修訂如下：

- **真正新 beats 只 3 個**：`lok_cover`（駱 B3 翻唱，獨立場面，草稿有 7 句對白）、`ngai_rain`（魏 B3b 暴雨救場，獨立場面，草稿有 3 句）、`chai_fear`（齊 B2 飯堂，獨立場面，草稿得 setup 一句＋抉擇後對白）。
- **5 處改為現有 beat 加 choices**：`pang_intel`（彭 B2 留名，唔開 `pang_signup`）、`chung_intel`（鍾 B2 跟指點，唔開 `chung_director`）、`chung_f_clue`（鍾 B3 守口，唔開 `chung_quiet`）、`ching_rival`（程 B2 留低，唔開 `ching_stay`）、`ching_e4`（程 B3 城中四子，唔開 `ching_four`）。GRANT229 seg key 同 ChoiceFx seg 一律跟現有 beat id（例如 `beat:pang_intel`，唔係 `beat:pang_signup`）。
- **冷版 heart 修訂**：草稿只畀咗鍾完整冷版對白（4 句，金鐘細房）同程冷版開場一句（「今晚唔講喇」）。駱／魏／齊草稿只寫「行冷版交心」，無冷版對白——**唔自行寫冷版對白**，改為暖版 heart 加排除式閘（有壞旗就唔播暖版，播 pool），冷版對白列入未實裝（等設計拍板）。彭 heart：有 `pang_absent_night` 就唔播（「交心唔開」），冷版由 `pang_finale_cold` 承接。
- **`ngai_patron` 授債權方式修訂**：vouch／honest 抉擇本身就喺 `ngai_patron` beat 上，beat 嘅 `grants()` 播出嗰陣未知玩家揀邊個，唔可以無條件授 `credit_enc83_ngai_patron`（揀 honest 嗰陣唔授）。**拆走 `ngai_patron` 嘅 grants()**，改由 `enc79RunChoiceFx` 新 handler `ngai_vouch` 授債權（跟 `pang_helped` 模式）。其餘五線 patron beat 無 choices 在身，grants() 照舊。
- **`chai_repay_cold` 唔開**：草稿無冷版回報對白（冷收尾 4 句已做 `chai_patron_cold` 內容）。暖版 `chai_repay` 加 `!chai_silent` 排除式閘；silent 嗰陣無回報 beat 播，冷後果由 `chai_patron_cold` 承接。
- **彭收尾 beats 例外**：上一手「唔另開 finale beats」適用於其餘五線（冷收科做冷版 patron beat 內容）。彭收尾（麵檔）係獨立場面，既唔係 `pang_n17` 亦唔係 `pang_patron` 內容，唔開 beat 就無處安放——**照開 `pang_finale`／`pang_finale_cold`**（跟陸 `luk_finale` 前例）。暖版收科（好收尾）對白其餘五線同樣有草稿但無 beat，記入未實裝（將來 finale-beat 票）。
- **齊暖版 patron 閘補多一項**：草稿 Beat 5 冷收尾觸發係「`chai_silent` 或 `chai_comfort`」，上一手閘（`!chai_comfort &&!chai_loose_fear`）漏咗 silent——暖版閘應為 `!chai_silent &&!chai_comfort &&!chai_loose_fear`；冷版閘為三者 OR。
- **魏 `ngai_repay` 閘放寬**（草稿寫法）：由「持有餐飯債權」改做「持有餐飯債權 OR `ngai_tea` 旗」；買茶嗰邊行冷版變體（將 repay DLG 第 2 句「還人情」換做順手教冷版句）。

## §3 實裝清單（按線）

### 3.1 DLG（`index.html`，67 支旗全部落 `flags:` 欄位，各 1 次）

- **Part A（45 支現有 choice 加 flags）**：六線 first／heart／已有 choices 嘅 beats 逐個加旗。現有 DLG labels 係書面語，維持不變，唔重寫。
- **Part B1（9 個現有 beat 加 choices，18 支新旗）**：`lok_foreshadow`（B2a 守口／講出去）、`ngai_patron`（B5 照實講／唔講大話）、`chai_repay`（B5 試新角／穩陣）、`pang_n17`（B5 食麵／瞓）、`pang_intel`（B2 留名）、`chung_intel`（B2 跟指點）、`chung_f_clue`（B3 守口）、`ching_rival`（B2 留低）、`ching_e4`（B3 城中四子）。抉擇後對白全部照抄草稿廣東話原文；N 句用書面語（草稿 N 句有廣東話要轉寫，意思唔變，照 v271 前例）。**新 labels 一律廣東話**（v269／v271 慣例；新 label 係玩家講出嚟嘅選擇，等同對白）。
- **Part B2（3 新 beats＋6 冷版 patron＋2 彭收尾＋鍾 heartCold，6 支新旗）**：
- 新 beats：`lok_cover`（駱 B3 翻唱，7 句，閘 T2–T3＋1991 冬＋`lok_kept_row`）、`ngai_rain`（魏 B3b 暴雨救場，3 句＋武指嗰句用 N 帶引述，閘 N7 已做＋1991 夏–秋）、`chai_fear`（齊 B2 飯堂，1 句 N setup＋choices，閘 N3 之後＋1990–1991）。
- 冷版 patron beats（排暖版前，v269 模式；收科對白做內容，無債權、無 choices）：`lok_patron_cold`、`lok_patron_cover`（翻唱收尾）、`ngai_patron_cold`、`chai_patron_cold`、`chung_patron_cold`、`ching_patron_cold`。
- 彭收尾：`pang_finale`（好收尾 7 句）、`pang_finale_cold`（冷收尾 5 句）。
- 鍾 `heartCold`（`heart` 隔籬新 seg，4 句、無 choices）：金鐘細房冷版對白。
- **67 支旗**：駱 13（`lok_first_stand`／`lok_first_quiet`／`lok_first_mock`／`lok_kept_row`／`lok_loose_row`／`lok_tried_harmony`／`lok_honest_not_ready`／`lok_stand_original`／`lok_cover_first`／`lok_heard_whole`／`lok_praised_song`／`lok_calm_truth`／`lok_join_rant`）；魏 14（`ngai_first_soda`／`ngai_first_tissue`／`ngai_first_walkaway`／`ngai_meal_treat`／`ngai_tea`／`ngai_walk_past`／`ngai_learn_serious`／`ngai_learn_later`／`ngai_rain_stand`／`ngai_rain_hold_back`／`ngai_heart_learn`／`ngai_heart_shy`／`ngai_patron_vouch`／`ngai_patron_honest`）；齊 11（`chai_first_right`／`chai_first_honest`／`chai_first_bluff`／`chai_kept_fear`／`chai_loose_fear`／`chai_advise_stop`／`chai_silent`／`chai_truth_change`／`chai_comfort`／`chai_try_new`／`chai_play_safe`）；彭 11（`pang_first_admire`／`pang_first_polite`／`pang_first_fake`／`pang_showed_up`／`pang_late`／`pang_cover_night`／`pang_absent_night`／`pang_listened`／`pang_brushed_off`／`pang_noodle_night`／`pang_early_night`）；鍾 9（`chung_first_humble`／`chung_first_silent`／`chung_first_backtalk`／`chung_tried_director`／`chung_stayed_lane`／`chung_kept_quiet`／`chung_loose_talk`／`chung_listened`／`chung_asked_return`）；程 9（`ching_first_grit`／`ching_first_water`／`ching_first_blunt`／`ching_stayed_late`／`ching_left_early`／`ching_back_train`／`ching_back_polish`／`ching_stand_slow`／`ching_stand_fast`）。
- 注意：`lok_foreshadow` A label「守口，話冇咩事」同 `chung_f_clue` A label 完全相同，flags 插入按表範圍錨定，唔可以用 label 做全局唯一錨。`chai_silent` 字串同時係 v269 遺留 fx token，`flags: ["chai_silent"]` 同 `fx:"chai_silent"` 各 1 次，兩種機制唔衝突。
- N15 兩支旗 `flag_vocal_train`／`flag_vocal_polish` 已在 code，唔使加。

### 3.2 Part C（ChoiceFx／RunChoiceFx／GRANT229／registry／BuildScript／heart）

- **ChoiceFx 12 新分支**：好選項 ＋3、中央抉擇 ＋5／＋3、中性 ＋1、負面 0／−2，沿用 live `enc79ChoiceFx` 慣用數，唔跟 PLAN／WORKORDER 建議值。lok_foreshadow 守口＋3／講兩句−2；lok_cover 企硬＋5／唱住先＋3；ngai_rain 衝入＋5／企埋一邊 0；chai_fear 守口＋3／講兩句−2；pang_intel 一早去＋3／遲咗 0；chung_intel 跟指點＋3／跑熟路＋1；chung_f_clue 守口＋3／講兩句−2；ching_rival 留低＋3／走先＋1；ching_e4 撐練＋5／紅先算＋1；ngai_patron 照實講＋3 fx `ngai_vouch`／唔講大話＋1（**注意：兩選項都含「照實講」，A 靠「企得穩」分流，B 靠「講大話」分流**）；chai_repay 唔同＋3／穩陣＋1；pang_n17 雲吞麵＋3／返屋企瞓＋1。
- **RunChoiceFx `ngai_vouch`**：授 `credit_enc83_ngai_patron`（打女引薦）；`ngai_patron` registry entry 嘅 grants() 已拆走（全檔只剩 RunChoiceFx handler 一處授呢筆債權）。
- **GRANT229_ENC79 57 行**（表由 17 行增至 74 行；新行全部非空 key、按 seg 分組、A→B→C 次序；原因廣東話，寫明新庫 gig 標題＋角色；見 §4 全表）。
- **Registry 閘門**：
- **延遲開（Beat-1-C）**：用 `st.seen>=2` 實現，唔使新旗。mock 旗只可能喺初遇（seen＝1）嗰陣落，Beat 2 beat 嘅 when 加 `!mock旗 || st.seen>=2`，即係「再撞多一次先開」。N-5 語義一律當「遲啲開」，唔係永久鎖死。四處：駱 mock→`lok_foreshadow`、魏 walkaway→`ngai_help`、齊 bluff→`chai_fear`、彭 fake→`pang_intel`。
- **心閘加多一重**：駱 mock→要 `lok_help` 已播（beatsDone）；魏 walk_past→要替身缺位 gig 已殺青（`S.flags["done_gig_1991_film_206"]`，經 `enc83GigDone`；玩家可喺板面接呢張臨記通告）；齊 bluff→要 `chai_choice` 已播（beatsDone，唔係 advise 旗本身，否則變永久鎖）。
- **魏 `ngai_repay` 閘放寬**：由「持有餐飯債權」改做「持有餐飯債權 OR `ngai_tea` 旗」；買茶嗰邊行冷版變體（將 repay DLG 第 2 句「還人情」換做順手教冷版句）。
- **Patron 暖版排除式閘**：駱暖 `lok_patron` 加 `!lok_join_rant &&!lok_loose_row &&!lok_cover_first`；魏暖 `ngai_patron` 加 `!ngai_rain_hold_back &&!ngai_patron_honest`（grants() 拆走）；齊暖 `chai_patron` 加 `!chai_silent &&!chai_comfort &&!chai_loose_fear`；鍾暖 `chung_patron` 加 `!chung_loose_talk &&!chung_asked_return`；程暖 `ching_patron` 加 `enc87StoryFlag("flag_vocal_train") &&!ching_back_polish &&!ching_stand_fast`。彭 patron 唔郁（債權照喺 T4 授；B5 抉擇只影響收尾＋preshow 即派）。
- **冷版 patron 閘**：`lok_patron_cold`＝T4＋（loose_row OR join_rant）；`lok_patron_cover`＝T4＋cover_first＋!loose_row＋!join_rant；`ngai_patron_cold`＝T4＋（hold_back OR honest）；`chai_patron_cold`＝T4＋（silent OR comfort OR loose_fear）；`chung_patron_cold`＝T4＋（loose_talk OR asked_return）；`ching_patron_cold`＝T4＋（flag_vocal_polish OR back_polish OR stand_fast）。
- **彭收尾閘**：`pang_finale`＝T3＋1992 冬＋beatsDone.pang_n17＋cover＋listened＋noodle；`pang_finale_cold`＝T3＋1992 冬＋beatsDone.pang_n17＋（absent OR brushed_off OR early_night）。
- **其餘閘跟 live**：`lok_help` 維持 T3＋歌藝 vocal≥35；`pang_help` 維持無年份閘；`chai_repay` 維持 N13 done 後備路，加 `!chai_silent` 排除式閘，唔收窄；`lok_e4grudge` 維持 T1＋E4 已出；`lok_cover` 閘 T2–T3＋1991 冬＋`lok_kept_row`（正閘，跟草稿「守口先開」）；`ngai_rain` 閘 T2＋N7 已做＋1991 夏–秋；`chai_fear` 閘 T1–T2＋1990–1991＋N3 已做。
- **Registry 順序**：駱 `['lok_foreshadow','lok_intel','lok_help','lok_cover','lok_recover','lok_e4grudge','lok_patron_cold','lok_patron_cover','lok_patron']`；魏 `['ngai_intel','ngai_help','ngai_repay','ngai_rain','ngai_patron_cold','ngai_patron']`；齊 `['chai_intel','chai_fear','chai_choice','chai_repay','chai_patron_cold','chai_patron']`；彭 `['pang_intel','pang_help','pang_n17','pang_finale_cold','pang_finale','pang_patron']`；鍾 `['chung_review','chung_intel','chung_f_clue','chung_farewell','chung_patron_cold','chung_patron']`；程 `['ching_e4','ching_rival','ching_after_train','ching_after_polish','ching_patron_cold','ching_patron']`。
- **Heart 分支改動**：暖版 heart 加排除式閘——駱 `!lok_loose_row`（cover_first 唔閘 heart）、魏 `!ngai_rain_hold_back`、齊 `!chai_loose_fear`；鍾有 `chung_loose_talk` 就播 `heartCold` 代替 `heart`；彭有 `pang_absent_night` 就唔播 heart（pool 代替）；程有 `ching_back_polish` 就 heart 首句換做「今晚唔講喇。」（lines-array 換句，唔另開 seg）。heart 條件鏈係 `else if`，各星分支互斥；程 back_polish 優先於 stayed_late（冷開場壓過認領句）。
- **BuildScript beat 變體**（v269 模式；認領變體用 N 行，v271 前例；中段變體按草稿落喺敘事啱嘅位，唔係一律第 2 位）：
- 駱 foreshadow（stand）：prepend N 行「（佢認得你——走廊嗰陣，肯出聲為佢講句好話嗰個。）」；駱 patron（heard_whole／praised_song）：插喺「約咗監製老友食飯」句之後（index 3），「呢個後生仔，肯由頭聽到尾。」／「呢個後生仔，識聽。」；駱 heart：tried 問句「呢段你聽唔聽得出我想講咩？」插喺「你聽清楚，呢一段」之後（index 5）；cover_first 停低句「呢首，我唔知仲唱唔唱得出。」插喺結他第一粒音 N 句之後（index 4）；honest 收尾附加「有啲歌，我而家唱畀你聽，你都未必接得住。」（三變體可疊加，插入次序按 index 由大到細，唔會移位）。
- 魏 help（soda）：第 2 位插「你嚟得啱。」；魏 rain（serious／later）：插喺「想起嗰句」N 行之後（index 2），N 行「（佢企得穩，落地屈膝卸力，魏詠男教嗰套，佢記得晒，武指睇在眼內。）」／「（佢企位唔穩，武指要嗌多句，佢先企得返穩。）」；魏 patron：learn 第 2 位插「你係肯跌嗰個。」；shy 收尾附加「肯跌，先學得嚟。」（live patron 開場無呢句，只喺 heart B 選項入面，搬唔到；按草稿「變收尾句」意圖附加做收尾句）。
- 齊 intel（right）：第 2 位插「上次嗰場戲之後，我有留意你，你開工幾定性。」（落 `chai_intel`，唔係 `chai_fear`——草稿 Beat 2 開場＝化妝間走廊，飯堂抉擇係 Beat 2 下半段）；齊 heart：advise_stop 首句前插「你講中晒。」；silent 換尾句＋剝 choices（尾句「你覺得我應該點行？」換做「你唔使答我，我自己諗。」）。
- 彭 intel（admire）：prepend N 行「（佢認得你——嗰個讚佢記性嘅後生仔。）」；彭 n17（listened／brushed_off）：**唔做變體**——listened 變體已在 live DLG（第 2 句 N 行已寫「第一個行埋嚟」），brushed_off 無逐字替換稿（改開場流程要自行寫句），旗嘅後果由 `pang_finale`／`pang_finale_cold` 閘承接。
- 鍾 intel（humble／silent／backtalk）：prepend N 行認領句三變體；鍾 patron（tried）：第 2 位插「佢去試過嗰邊。」；stayed_lane 無變體（引薦照開，少呢句）。
- 程 rival（grit／water／blunt）：prepend N 行認領句三變體；程 heart：stayed_late 第 2 位插 N 行「（佢記得你嗰晚留低過，肯同你講真話。）」；back_polish 換首句（見 heart 分支）。
- **魏 `ngai_repay` 冷版**：`ngai_tea` 且無餐飯債權嗰陣，第 2 句「上次你幫過我，我魏詠男唔欠人嘅。今日還返俾你——教你兵器套路，學咗一世受用。」換做「今日得閒，順手教你兵器套路，學咗一世受用。」；有餐飯債權照行暖版。
- **唔做嘅變體**：駱 heart stand_original（草稿話「歌係自己嘅」嗰句變第一句，但 live heart 段六已有呢句，點變體待定，唔好靜默重複）；齊 patron try_new／play_safe（FRAME cap／wrap 分流，FRAME 機制本身唔喺 v278 改）；程 ching_e4 N15 旗變體（草稿話 N15 苦練／修音改變佢對「功夫就要追得上個名」嘅回應，但嗰句係抉擇後對白，改抉擇後行唔係 v269 開場插入模式，要另設計）；彭 pang_help showed_up／late 閘（草稿話遲咗嗰陣 Beat 3 唔開，但 live pang_help 閘係 N11，v278 無加閘，遲咗照可頂班；即派行已分流）。

### 3.3 本 session 驗收嗰陣捉到再修嘅 4 處 code 問題

新測試第一輪跑出 10 項 FAIL，逐個 debug 後分 code／test 兩邊修：

1. **GRANT229 key 錯**：`first:chai_zanhoi` B 行 key「唔記得」對唔上 live 書面語 label「老實說：不記得，剛才沒留心」——key 改做「不記得」（唯一命中 B 選項）。
2. **`ngai_help` 漏咗延遲開閘**：Part C 腳本無將 `!ngai_first_walkaway || st.seen>=2` 落去 `ngai_help` when（其餘三線有）。已補返，跟同一寫法。
3. **`ngai_patron` 暖版閘漏 `!ngai_patron_honest`**：Part C 只加咗 `!ngai_rain_hold_back`，honest 嗰陣暖／冷兩版齊開。已補 `&&!ngai_patron_honest`（冷版閘本身係 hold_back OR honest，暖版必須兩者都排除，先至互斥）。
4. **駱 registry 順序錯**：`lok_recover` 排咗 `lok_cover` 前面；草稿時序係 cover（1991 冬）先、recover（1992）後，測試期望亦係 cover 在前。已對調兩行（兩 beat 年份閘互不重疊，唔影響 live 播出次序邏輯）。
5. **`heartCold` 插入語法錯**（Part B2 腳本 bug）：`heartCold` 前面缺咗 heart 物件嘅 `},`，兼多咗一個錯位 `},`——修咗兩處，六個 DLG 全部 `new Function` parse 通過。

## §4 即派對位最終表（57 行，2026-11-17 核實定稿）

對位原則：沿用 v158 前例（統籌自行揀新庫通告做即派對位，逐行寫明標題＋理由，唔算自行創作）。優先配媒介＋級別，其次角色／genre，年份最次（grant229 唔受季節閘限制）。**排除集共 102 個 id**（index.html 入面 73 個 gigId 引用＋新庫 33 張 trigger gig，4 個重疊）。57 行全部通過核實：存在、無 trigger、唔在排除集。去重後 51 張 distinct gig，6 對共用（全部係草稿本身重用同一舊 id，刻意保留）。GRANT229 key 係 label 子串，按 seg 過濾；新 label 係廣東話，key 要跟新 label。原因廣東話，跟現有表慣例（「第二朝，X話：……」），寫明實際新庫 gig 標題＋角色，唔照抄草稿舊 id。

**本 session 更正咗早前 mapping 嘅錯誤**（以 live 數據為準）：① 12 張初版對位已被其他機制授出（主線 GRANT229_CHOICE N2／N7／N8／N10／N12／N13／N14／N16／N19、顧 GRANT229_DRAFT／n10after），全部已換走；② 早前「1992 film 中級可用 0 張」係 genre 限定（文藝），實際有 3 張（film_102／104／113）；③ 早前「1992 tv 初級 3 張已全部用晒」係錯，實際有 4 張（tv_101–104），全部男配角，程 B2 B 仍用 tv_205（角色啱）。

| 線 | seg | key | gigId | 通告（標題＋角色） |
|---|---|---|---|---|
| 駱 | first:lok_gasing | 好話 | gig_1990_rec_110 | 《白頭相守》大碟主唱 |
| 駱 | beat:lok_foreshadow | 守口 | gig_1990_rec_102 | 《熱力舞》和音歌手 |
| 駱 | beat:lok_help | 試試 | gig_1991_rec_109 | 《沸騰青春》MV 男主角 |
| 駱 | beat:lok_help | 未夠班 | gig_1991_rec_102 | 《鄉謠》民謠配唱歌手 |
| 駱 | beat:lok_cover | 企硬 | gig_1991_rec_204 | 音樂錄像演出 |
| 駱 | beat:lok_cover | 唱住先 | gig_1991_rec_109 | 《沸騰青春》MV 男主角（共用） |
| 駱 | heart:lok_gasing | 彈完整首 | gig_1992_rec_107 | 《霓虹舞影》MV 男主角 |
| 駱 | heart:lok_gasing | 好聽 | gig_1992_rec_105 | 《當年情懷》大碟主唱 |
| 駱 | beat:lok_e4grudge | 一起罵 | gig_1991_rec_202 | 搖滾大碟錄音和音歌手 |
| 魏 | first:ngai_wingnaam | 汽水 | gig_1990_film_110 | 《鐵血幹探》武打配角 |
| 魏 | first:ngai_wingnaam | 紙巾 | gig_1990_film_105 | 《幽靈假期》武師 |
| 魏 | beat:ngai_help | 大排檔 | gig_1991_film_206 | 飛車追逐動作替身 |
| 魏 | beat:ngai_help | 熱茶 | gig_1991_film_111 | 《雪山雙劍傳》武打配角 |
| 魏 | beat:ngai_repay | 認真學 | gig_1991_film_205 | 武館巷戰武行 |
| 魏 | beat:ngai_repay | 下次先 | gig_1990_film_210 | 茶餐廳早市熟手臨記 |
| 魏 | beat:ngai_rain | 衝入雨幕 | gig_1991_tv_112 | 《幹探追兇記》男配角 |
| 魏 | beat:ngai_rain | 企埋一邊 | gig_1991_tv_209 | 台慶劇組群演 |
| 魏 | heart:ngai_wingnaam | 認真記低 | gig_1992_film_108 | 《劍客傳》武師 |
| 魏 | heart:ngai_wingnaam | 學不來 | gig_1991_film_110 | 《鐵拳王》動作替身 |
| 魏 | beat:ngai_patron | 講大話 | gig_1991_film_114 | 《刀光劍影錄》動作替身 |
| 齊 | first:chai_zanhoi | 答得出 | gig_1990_tv_113 | 《劍嘯山河》動作替身 |
| 齊 | first:chai_zanhoi | 不記得 | gig_1990_tv_111 | 《雷霆幹探》動作替身 |
| 齊 | beat:chai_fear | 守口 | gig_1991_tv_111 | 《我係打工仔》男主角 |
| 齊 | beat:chai_choice | 停一停 | gig_1991_tv_114 | 《亂世將軍傳》男主角 |
| 齊 | beat:chai_choice | 不出聲 | gig_1991_tv_207 | 廟街夜市群演 |
| 齊 | heart:chai_zanhoi | 真話 | gig_1992_tv_107 | 《黃金球道》男配角 |
| 齊 | heart:chai_zanhoi | 安慰 | gig_1992_tv_101 | 《笑滿街》男配角 |
| 齊 | beat:chai_repay | 唔同 | gig_1992_tv_111 | 《笑匠當家記》男主角 |
| 齊 | beat:chai_repay | 穩陣 | gig_1992_tv_112 | 《硬橋硬馬》男主角 |
| 彭 | first:pang_siuki | 記性 | gig_1992_variety_103 | 《笑聲滿堂》遊戲環節嘉賓 |
| 彭 | first:pang_siuki | 多多指教 | gig_1990_variety_102 | 《星聲歌唱大賽》歌唱比賽參賽者 |
| 彭 | beat:pang_intel | 一早去 | gig_1991_variety_201 | 慈善晚會歌舞劇助演 |
| 彭 | beat:pang_intel | 遲咗 | gig_1991_variety_104 | 《歡樂大綜藝》遊戲環節主持 |
| 彭 | beat:pang_help | 頂一晚 | gig_1990_variety_202 | 台慶晚會歌舞劇助演 |
| 彭 | beat:pang_help | 來不了 | gig_1990_variety_203 | 綜合節目歌舞劇助演 |
| 彭 | heart:pang_siuki | 靜靜聽 | gig_1992_variety_201 | 台慶銀禧歌舞劇助演 |
| 彭 | heart:pang_siuki | 想多了 | gig_1992_variety_105 | 《金曲新秀大賽》歌唱比賽參賽者 |
| 彭 | beat:pang_n17 | 雲吞麵 | gig_1991_ad_107 | 《安穩一生》電視廣告主角 |
| 彭 | beat:pang_n17 | 返屋企瞓 | gig_1992_tv_301 | 《便衣幹探》補拍群演（補拍通告，1992 tv 群演，角色啱） |
| 鍾 | first:chung_choning | 受教 | gig_1990_film_104 | 《水遠山長》男配角（全庫唯一可用文藝片，級別中→初、年份 1991→1990 放寬） |
| 鍾 | first:chung_choning | 點頭 | gig_1990_film_212 | 醫院病房路人 |
| 鍾 | first:chung_choning | 不服氣 | gig_1991_film_208 | 賀歲街市群演 |
| 鍾 | beat:chung_intel | 指點 | gig_1991_film_205 | 武館巷戰武行（共用，魏 B3a A） |
| 鍾 | beat:chung_intel | 跑熟路 | gig_1990_film_210 | 茶餐廳早市熟手臨記（共用，魏 B3a B） |
| 鍾 | beat:chung_f_clue | 守口 | gig_1992_tv_109 | 《笑聲一家親》男配角 |
| 鍾 | beat:chung_f_clue | 講兩句 | gig_1990_tv_207 | 《一哥一姐》群演 |
| 鍾 | heart:chung_choning | 靜靜聽 | gig_1992_tv_110 | 《他鄉故事》男配角（tv 文藝中級 1992；**唔用** trigger gig `gig_1991_film_101`《江河歲月》，嗰張係陸柏言 BR89 債權兌現 gig） |
| 鍾 | heart:chung_choning | 會不會回來 | gig_1990_tv_213 | 古裝市集路人 |
| 程 | first:ching_tinlok | 練到天亮 | gig_1991_rec_202 | 搖滾大碟錄音和音歌手（共用，駱 B5 B） |
| 程 | first:ching_tinlok | 遞一瓶水 | gig_1992_rec_101 | 《返鄉路》民謠配唱歌手 |
| 程 | first:ching_tinlok | 笑他 | gig_1991_rec_101 | 《歡笑聲》主題曲配唱歌手 |
| 程 | beat:ching_rival | 留低 | gig_1990_rec_104 | 《同聲唱》合唱配唱歌手 |
| 程 | beat:ching_rival | 走先 | gig_1991_tv_205 | 啟德機場送機群演 |
| 程 | beat:ching_e4 | 撐佢練 | gig_1992_rec_107 | 《霓虹舞影》MV 男主角（共用，駱 B4 A） |
| 程 | beat:ching_e4 | 紅咗先算 | gig_1992_ad_105 | 《繽紛》形象廣告配角 |
| 程 | heart:ching_tinlok | 慢 | gig_1992_rec_105 | 《當年情懷》大碟主唱（共用，駱 B4 B） |
| 程 | heart:ching_tinlok | 紅了再說 | gig_1992_ad_201 | 啟德機場銀行宣傳廣告主角 |

**6 對共用**：`gig_1991_rec_109`（駱 B2b A＋B3 B）、`gig_1992_rec_107`（駱 B4 A＋程 B3 A）、`gig_1992_rec_105`（駱 B4 B＋程 B4 A）、`gig_1991_rec_202`（駱 B5 B＋程 B1 A）、`gig_1991_film_205`（魏 B3a A＋鍾 B2 A）、`gig_1990_film_210`（魏 B3a B＋鍾 B2 B）。
**唔入 GRANT229 嘅兩行**：駱 B5 A（`lok_calm_truth`）本身就係 BR89 債權 `credit_enc83_lok_patron` 兌現 `gig_1992_rec_111`《主打歌》MV，經 patron 授債權嗰步交付，唔可以雙份派；魏 B5 A（`ngai_patron_vouch`）BR89 兌現 `gig_1991_film_212`《鐵橋風雲》。彭 B5 分工（PLAN §15 N-1）：即派＝preshow 廣告；BR89 兌現 `gig_br89_patron_pang`《台慶大騷》＝持有債權上板，唔使 Beat 5 再派。

## §5 測試

- **新測試** `tests/test_sideline278_logic.js`（約 120 項斷言）：(1) ChoiceFx 12 新分支（用 live label 逐個對 fav＋fx，含 ngai_patron「照實講」互斥 guard）；(2) RunChoiceFx ngai_vouch 授債權＋冪等＋ngai_patron 無 grants()＋其餘五線 patron grants() 照舊；(3) GRANT229 57 行數據驅動（gig 在位＋key 非空＋key 唯一命中同 seg 唯一 live 選項＋逐行即派正確＋一生一次＋「無即派」選項唔派＋6 對共用）；(4) registry 閘門（5 組新 beats 順序＋lok_cover／ngai_rain／chai_fear 閘＋4 組延遲開＋無旗唔延遲＋ngai_repay 放寬兩路＋chai_repay silent 閘＋六線暖／冷 patron 閘＋程無 train 旗兩版都唔開＋程有 train 旗暖版開＋無壞旗六線暖版照開＋彭收尾三組）；(5) BuildScript 變體＋heart 分流＋ngai_repay 冷版；(6) 靜態 guard（67 旗各 1 次＋新 beats DLG 在位＋heartCold 4 句＋新 labels 廣東話＋唔改 SAVE key／softRev／?v=）。
- **新測試第一輪 10 項 FAIL，修咗 4 處 code（見 §3.3）＋6 處 test**：
- test：`labelsOf` beat case 取錯 star（beat id 唔係 star id，要按前綴映射）；new labels 計數 22→24（12 seg × 2）；魏 patron／鍾 patron／魏 help BuildScript 測試要先 mark 晒前面 beats 做完（否則 PickBeat 返早 beat）；駱 warm／魏 warm／程 warm 三處 PickBeat 測試要先 mark 前面 beats 做完（T4 狀態下 earlier beats 係已做，唔 mark 係唔真實 setup；PickBeat 本身「第一個開嘅 beat」邏輯正確，唔改 code）；駱 heart honest／魏 patron shy 測試取 `hs[length-1]` 撞正 choice step `text=null`（改取最後一個非 null text）；`resetS` 加 `_ledger = null`（harness bug：`enc79GrantCredit` 經 favor ledger 冪等，`_ledger.counted` 跨 resetS 唔清，令同一 credit id 喺之後 test 再授變 no-op——(5) 魏 repay 暖版因此 pick=null；live 唔 reset S，ledger 同 S 同步，唔受影響）。
- **相關舊測試逐個覆驗，全部 PASS**（`test_enc83_logic`／`test_enc84_logic`／`test_sideline273_logic`／`test_sideline274_logic`／`test_br89_logic`／`test_gig229_grant`／`test_gig229_trigger`／`test_sideline278_logic`）。舊測試因 v278 改動要同步更新嘅地方：
- `test_enc83_logic`／`test_enc84_logic` patron 迴圈：魏改行 fx 授債權（揀「照實講」先授，`enc79RunChoiceFx(enc79ChoiceFx('beat:ngai_patron','照實講：佢得，佢企得穩').fx)`）；enc84 另補程 train 旗（`S.flags.flag_vocal_train=1`，`enc87StoryFlag` 同讀 `S.flags`；enc84 harness 嘅 resetS 冇 `S.story`）。
- `test_sideline273_logic` (c) 兩斷言翻做 v278 已實裝狀態（草稿旗 66 支全部在 html 出現＋`flags: ["chai_silent"]`；GRANT229 六線行 57 行，總 74 行）。
- `test_gig229_grant` T0：17→74 行（原 17＋v20a278 六線 57 行）。
- `test_sideline158_logic` T7：全表 17→74 行；reason 檢查 `slice(9)`→`slice(9, 17)`（只驗 v158 嗰 8 行）。
- `test_enc83_static` 提攜檢查：七星經 grants()（喺 mod 段內）＋魏經 fx（`if(fx==="ngai_vouch")`＋`enc79GrantCredit({ id:"credit_enc83_ngai_patron"` 在 src）。
- **全套 suite**：基線 342／9（v277）。第一輪 v278：336／16——7 項新 FAIL，全部係 pinned-line 漂移（`index.html` 45,503→46,030，淨 +527 行），唔係邏輯回歸。已按 v269／v271 模式 resync（`qa278/resync278.py` difflib 對位，58 處錨點內容逐字相同，純漂移；`qa278/resync278_apply.py` 單次掃描 dict 查表應用）：
- `test_travel114_static`：COUNT 12／FREE 40／DEF／WRAPPER 按段重算（＜26739 唔郁、26739–36902 ＋59、36903–40599 ＋516、≥40600 ＋527；DEF 40753→41280、WRAPPER 28577→28636）。
- `test_rom176_static`：4 釘行（39119→39635、39477→39993、40638→41165、40794→41321）。
- `test_tang171_static`／`test_tang173_static`：總行數 45503→46030、openLoc DEF 40753→41280（鏈尾加 ＋v278 +527；標籤＋lines[] guard 一併更新）。
- `test_gift185_static`：總行數 45503→46030（鏈尾加 ＋v278 +527）。
  - 上述 7 檔逐個直接跑全部 PASS。resync 後全套 suite 結果：**343／9**（`qa278/suite_v278b.txt`）——基線 342／9＋新測試 1 檔；FAIL 名單同基線完全一致（flash51／slot50／soft_tip_111_restore／start53／weave43_static／weave44_static／weave49_static／wf5_87／wrap38，9 項已知 pre-existing）。
- **改動規模**：`index.html` 45,503→46,030 行（淨 +527）；新測試 1 檔；改測試 11 檔（8 相關＋3 resync 另計：enc83／enc84／gig229／sideline273／sideline158／enc83_static／travel114／rom176／tang171／tang173／gift185）。

## §6 未實裝清單（等設計拍板，唔自行創作）

- G-L2（`credit_wf3_comedy_crew` 授出路徑，等用戶拍板）；G-NGAI-3（武館老闆情報）；G-PANG-1 具體放寬數字；收尾獎勵數字（Q10 建議值未定稿）；Q4 code 提示文字 L6782–6783「1990 年秋末」未同步（N15 應為 1992 年秋末，攻略 live 版為準）；§1–§3 C→B 升級（1.10／1.11／1.13／1.14／1.17）；第 ③ 組收尾獎勵、第 ④ 組 §14、第 ⑤ 組 §15、R5 人情兌現（另票）；攻略側改動（parent 做）；鍾 Beat 3 報紙花邊回音（`rumor_chung_canada_heard`／`rumor_chung_farewell_truth` live 0 命中，v267 刪傳聞；`enc79PaperWhisper` 有無覆蓋「講出去」碎片未核實）；鍾規模三處講法出入（紅星章五段 vs 舊分批表 3–4 幕 vs 總則 4–5 幕，等用戶拍板）。
- **新增（本票）**：駱／魏／齊冷版 heart 對白（草稿只寫「行冷版交心」，無對白；暖版已加排除式閘，冷版待設計寫對白）；五線暖版收科（好收尾）對白有草稿但無 beat（`lok_patron` 等暖版 beat 係引薦場面，收科係 N17 之夜另一場面；將來 finale-beat 票）；齊 FRAME cap／wrap 按 try_new／play_safe 分流（FRAME 機制本身唔喺 v278 改）；駱 heart stand_original 變體（草稿話「歌係自己嘅」嗰句變第一句，但 live heart 段六已有呢句，點變體待定，唔好靜默重複）；彭 heart 1992 年閘（草稿話 T3＋1992，但 live heart 分支無年份閘，六線通用；本票唔改，記低）；彭 n17 brushed_off 變體（草稿有變體描述但無逐字替換稿，改開場流程要自行寫句；旗後果由 pang_finale_cold 閘承接）；程 ching_e4 N15 旗變體（草稿話 N15 苦練／修音改變佢對「功夫就要追得上個名」嘅回應，但嗰句係抉擇後對白，改抉擇後行唔係 v269 開場插入模式，要另設計）；程 patron 閘同草稿出入（草稿 Beat 5 暖版閘係 T4＋`flag_vocal_train`＋`ching_back_train`＋`ching_stand_slow` 三旗齊備；v278 用 v269 排除式——暖版開只要 train 旗＋無壞旗，唔要求 back_train／stand_slow；如用戶要嚴格版，要改閘）；彭 pang_help showed_up／late 閘（草稿話遲咗嗰陣 Beat 3 唔開，但 live pang_help 閘係 N11，v278 無加閘，遲咗照可頂班；即派行已分流）。
