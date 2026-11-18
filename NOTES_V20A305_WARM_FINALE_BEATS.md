# NOTES_V20A305 — Q18 五線 warm finale beats

- 版本：v20a305（Q18）
- 基線：main `2890489`（v304，suite 367／9）
- 結果：suite 368／9（基線 367／9；+1 係新測試 test_r305_warm_finale.js；9 項 pre-existing FAIL 不變：flash51／slot50／soft_tip_111_restore／start53／weave43_static／weave44_static／weave49_static／wf5_87／wrap38）；Pages md5 `b011862d8d3ec191983f3b214240fe4b`／4,692,106 bytes（見 §7）
- 新測試：`tests/test_r305_warm_finale.js`（78 項，ALL PASS）
- 行數：index.html 47194 → 47229（＋35 行：3 段收科對白 28 行＋3 條 registry 閘 3 行＋齊尾句分流 4 行，鍾 registry 調序淨 0 行）

## §1 設計：五線唔係一式五份——3 個新 beat＋2 線判斷

Q18 題目話「五線各開一個 warm finale beat」，但親查草稿＋live 之後，實際分流係：

| 線 | 做法 | 原因 |
|---|---|---|
| 駱家聲 lok | 新 beat `lok_finale` | 草稿好收尾 5 句有逐字稿、無 beat |
| 魏詠男 ngai | 新 beat `ngai_finale` | 草稿好收尾 5 句有逐字稿、無 beat |
| 齊鎮海 chai | 新 beat `chai_finale` | 草稿好收尾 6 句有逐字稿、無 beat（尾句按 Beat 5 分流，見 §3） |
| 鍾楚凝 chung | **唔另開**；registry 調序（提攜排送別之前） | 草稿 Beat 5 暖版本身就係送別＋引薦齊播，兩者都已 live；另開一幕會同「佢已經去咗加拿大」撞（見 §4） |
| 程天諾 ching | **唔另開** | 草稿 Beat 5 暖版本身就係 after_train＋patron＋stageup 齊播，全部已 live；無獨立收科場面可開（見 §5） |

前例跟足陸／彭：`luk_finale`（T4＋1992 冬＋壞旗分流，暖版授 `enc79_luk_finale`）、`pang_finale`（T3＋1992 冬＋`beatsDone.pang_n17`＋三旗）。三個新 finale 閘同樣係「T4＋1992 冬＋提攜已播＋patron 暖閘同一組排除條件」，grants() 授 `enc79_<line>_finale=1`（跟 luk 前例；pang_finale 無 grants，唔跟）。

## §2 三個新 finale beats（對白＝草稿暖版收科逐字，旁白轉書面語）

對白來源：`~/workspace/linji-story-sidelines/drafts/batch2-lok-ngai-chai-pang.md`（駱 L376–389／魏 L798–804／齊 L1173–1180）。S／A 對白照原文廣東話；N 旁白按語言規則轉書面語（同 v278 冷版／翻唱版入稿做法一致——草稿旁白本身係混合口語，live 一律書面語）。

- `lok_finale`（`ENC83_DLG_lok_gasing.beats`，registry 排 `lok_patron` 之後、最尾）：閘 T4＋1992 冬＋`beatsDone.lok_patron`＋唔係 `lok_join_rant`／`lok_loose_row`／`lok_cover_first`。場面：頒獎禮之後嗰晚，香江唱片後巷，駱抱住支結他，阿偉坐樓梯級隔籬。「歌係自己嘅，嗰種實淨，冇人攞得走」→「我唱咗十幾年，輸俾排榜遊戲…」→「監製嗰邊，我提過你個名…歌仲喺度，人就唔好俾人收埋。」
- `ngai_finale`（`ENC83_DLG_ngai_wingnaam.beats`，排 `ngai_patron` 之後、最尾）：閘 T4＋1992 冬＋`beatsDone.ngai_patron`＋唔係 `ngai_rain_hold_back`／`ngai_patron_honest`。場面：頒獎禮之後嗰晚，維港電影後巷，木箱上面一人一支汽水。「呢行唔記得邊個紅過，只記得邊個仲企得穩」→「你而家企到呢個位，記得扶返啲肯捱嘅後生…」→「我個電話仲打得通…」
- `chai_finale`（`ENC83_DLG_chai_zanhoi.beats`，排 `chai_patron` 之後、最尾）：閘 T4＋1992 冬＋`beatsDone.chai_patron`＋唔係 `chai_silent`／`chai_comfort`／`chai_loose_fear`。場面：頒獎禮之後嗰晚，星河電視台古裝街，城門前面。「阿偉，唔知由幾時開始，我同你講嘢，唔再當你係企後面嗰個臨時演員喇」→「人同人之間，過咗嗰條線，就唔同晒…」→尾句見 §3。

次序保證：registry 排提攜之後，`enc79PickBeat` 按次序回第一個開到嘅 beat；finale 閘另加 `beatsDone.<line>_patron`（跟 pang_finale 要求 `beatsDone.pang_n17` 嘅前例），雙重保證 finale 一定喺提攜之後先播。冷版照舊行提攜冷版（`patron_cold`，壞旗玩家 finale 閘唔開）；翻唱玩家行 `patron_cover`，唔播 finale（cover 唔係暖版，`beatsDone.lok_patron` 唔會落）。

收尾獎勵：finale 唔叫 `sideline280GrantCompletion`——暖版聲望＋2／信用淨＋2 喺提攜嗰陣已經派咗（lok／chai 經 patron grants，ngai 經 vouch fx／e4grudge），finale 唔重派。

## §3 齊尾句分流（草稿好收尾變體二）

草稿後果欄寫明：Beat 5 揀 try_new → 尾句係 wrap 句「殺青喇，阿偉。同你做呢套戲，我冇睇錯人。嚟緊嗰條路點行，你自己企穩，我會喺後面望住。」；揀 play_safe → 尾句係 cap 句「阿偉，今日傾到呢度先啦，我仲有場戲要默。你有呢份心，我領咗，不過有啲路，仲要慢慢行，唔好急。」兩句都係遊戲原文（`ENC83_FRAME_chai_zanhoi` cap／wrap），按選項分流。

實裝：finale 對白預設用 wrap 句（try_new 版）；`enc79BuildScript` 入面加 flag-based 尾句換句（跟 v278 齊 silent 換尾句／魏 repay 換第 2 句同一 pattern）：`chai_play_safe` 嗰陣將尾句換做 cap 句。FRAME cap／wrap 本身一行都唔郁（留畀 Q19 v306）。

留意：cap 句同時係冷版 patron_cold 嘅收尾句——草稿本身就係咁設計（冷收尾＝cap 句單獨成場；暖版 play_safe＝六句對話以 cap 句收尾），場面其餘五句完全唔同，唔係重用冷版。

## §4 鍾線判斷：唔另開，調序先係真正嘅修復

草稿 Beat 5（`batch3-chung-ching.md` L205–239）暖版結構本身就係兩幕齊播：

- 送別 `chung_farewell`（T2，1992 秋／冬，天星送別；授 `chungAdviceHeld229`）＋
- 引薦 `chung_patron`（T4，引薦債權 `credit_enc84_chung_patron`＋收尾獎勵）

兩者都已 live，草稿暖版無第三幕、無獨立收科對白。另開一個 finale beat 要憑空寫對白（違反「對白用草稿」），而且播完送別之後佢嘅出沒率歸零（`enc79PresenceP` L39662：`beatsDone.chung_farewell` → `{ p:0, share:0 }`），finale 根本無機會播——送別之後開唔到，送別之前又同送別撞（兩次告別）。

但親查嗰陣捉到一個真缺陷（v305 附帶修復，唔另開票）：舊 registry 次序係 farewell 行先過 patron。遲到 T4 嘅暖版玩家（1992 秋／冬先上 T4）會先播送別，之後出沒 P=0，提攜永遠攞唔到——暖版收科得一半（有送別、無引薦、無收尾獎勵）。早到 T4 嘅玩家唔受影響（提攜無年份閘，1992 秋前已播）。

修復：registry 調序，`patron_cold`＋`patron` 排 `farewell` 之前（閘同對白一行都唔郁）。遲到 T4 暖版玩家：先播提攜（攞引薦＋收尾獎勵），下次先播送別；冷版玩家：先播提攜冷版、後送別；T2 玩家：提攜閘唔開（要 T4），送別照播。v302 報紙花邊（`beatsDone.chung_farewell`）同結局回望讀嘅都係 beatsDone，唔受次序影響。

## §5 程線判斷：唔另開

草稿 Beat 5（`batch3-chung-ching.md` L481–520）暖版結構本身就係三件套齊播：

- `ching_after_train`（N15 苦練版，`flag_vocal_train`）＋
- `ching_patron`（T4 引薦，`credit_enc84_ching_patron`＋收尾獎勵；閘見 Q24，v311 會改嚴格版）＋
- stageup 升段收束（`ENC84_FRAME_ching_tinlok.stageup`）

全部已 live，草稿暖版無獨立收科場面可開。冷版收束 4 句草稿（「你而家企到呢個位…」）未實裝，但嗰個係冷版收尾，Q18 範圍係暖版，唔郁，記入殘留。

## §6 守住嘅嘢

- patron／patron_cold 閘同對白一行都唔郁（測試 S 段釘實）；luk_finale／pang_finale 唔郁。
- 齊 FRAME cap／wrap 一行都唔郁（Q19 v306 範圍）。
- 舊檔唔 crash：finale 閘只讀 `S.flags`、`st.beatsDone`（舊檔無 beatsDone 嗰陣 `enc79EnsureStars` 補預設）、`yearSeasonNow()`，同 luk_finale 同一讀法；測試 G 段用得 fav／met 嘅舊檔驗過。
- gigs_new.json 仍係 302 張。

## §7 測試

- 新測試 `tests/test_r305_warm_finale.js`：78 項，ALL PASS。
  - (A) 數據：三個 finale 句數（5／5／6）、無 choices、講者齊、旁白書面語、草稿關鍵句逐句在位；finale 同 patron_cold 零逐句重用；registry 排提攜之後。
  - (B) 分流：暖版齊晒→播 finale；壞旗→finale 唔開、提攜冷版照開；1992 秋／1991 冬→唔開；T3→唔開；提攜未播→唔開、先播提攜。
  - (C) 播完：落 `enc79_<line>_finale` 旗、beatsDone 記低、唔重播。
  - (D) 齊尾句：try_new→wrap 句、play_safe→cap 句、play_safe 播完照落旗。
  - (E) 鍾：無 finale beat；提攜排送別之前；遲到 T4 先提攜後送別；T2 送別照播；冷版先提攜冷版後送別；提攜授債權。
  - (F) 程：無 finale beat；after_train＋patron 暖閘照開。
  - (G) 舊檔三線唔 crash、照播 finale。
  - (S) 靜態：三線提攜閘／對白／冷版對白、鍾送別閘＋授旗＋授債權、程提攜閘、陸／彭 finale、齊 FRAME cap／wrap、gigs 302 張、finale 唔叫收尾獎勵。
- 全套 suite：368／9（基線 367／9；+1 係新測試 test_r305_warm_finale.js；9 項 pre-existing FAIL 預期不變：flash51／slot50／soft_tip_111_restore／start53／weave43_static／weave44_static／weave49_static／wf5_87／wrap38）。
  - 第一輪 360／17：8 項新 FAIL 全部係釘行漂移＋期望順序（唔係功能回歸）——enc83／enc84／sideline278 嘅 EXPECT 節拍表順序（v305 故意改咗）、travel114／tang171／tang173／rom176／gift185 嘅釘行（＋35 行漂移）。`qa305/resync305.py` 按 difflib 對位核實純漂移後重寫釘行（單次掃描 dict 查表；段邊界：＜36874 唔郁、36874–37537 ＋9、37538–37843 ＋18、37844–40171 ＋28、40172–41711 ＋32、41712–41732 ＋33、41733–41740 ＋34、≥41741 ＋35；chung 調序三行淨 0 行，今次無釘行命中）。重跑後 8 項全過，第二輪 368／9。
  - 附帶：suite 每次重跑會再生 `qa296/derive296.json`（v296 分類器衍生盤點檔；今次因新對白多咗 189 行），跟 v304 前例，唔入版，已還原。

## §8 殘留／跟進（唔喺 v305 範圍）

1. 程冷版收束 4 句草稿（batch3 L513–519）未實裝——冷版收尾，Q18 暖版範圍外，日後冷版票跟進。
2. 駱草稿暖閘嚴格版有 `lok_stand_original`（Beat 3 翻唱抉擇未建，live 無呢支旗），finale 閘用 patron 排除式（同收尾獎勵判定一致），唔用草稿嚴格版。Beat 3 翻唱抉擇建好嗰陣先再對。
3. 魏草稿暖閘嚴格版有 `ngai_rain_stand`＋`ngai_patron_vouch`；live 暖版判定（v280）用排除式（唔係 rain_hold_back／patron_honest），finale 跟返 live 口徑。vouch 旗本身由 patron 抉擇 fx 授，唔係獨立閘旗。
4. 齊 FRAME cap／wrap 兩個版本（Q19，v306）——finale 尾句分流已做，FRAME 本身留畀 v306。
