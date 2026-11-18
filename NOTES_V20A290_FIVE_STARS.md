# v20a290：Q2——五位名冊外女星入紅星系統（NOTES）

- 任務：Q2（用戶 2026-11-18 13:01 拍板）：藍若曦、江詩盈、沈映雪、胡美琳、韓秀婷入紅星系統
  （ENC79_STARS 名冊 12 → 17）。parent 已核實前提（main d2455a0）：五位 id 全部由 gig 庫 cast 欄位核實；
  `enc79StarDef` 搵唔到返 null、`enc79EnsureStars` lazy-init、`enc79OnWrap` grant `if(!def) return false`
  就係五位殺青好感被跳過嘅原因。
- 工作目錄 `~/workspace/linji-work290`，分支 `v290-five-stars`，HEAD `d2455a0`。

## §1 設計拆解（每位星）

地點 id 全部用現有 17 個片場層地點（LOCS L6246–6311），唔開新地點。五位嘅主場／副場
全部揀已經喺 13 個巧遇可達地點併集入面嘅地點（見 §5），所以 `reachLocs` 維持 13 個，
`LOC_SHEET_BG` 逐地點場景檔全部現成，唔使補場景圖。

| 星 | id | 主場 primary | 副場 secondary | area | win（加權窗口，唔係閘） |
|---|---|---|---|---|---|
| 藍若曦 | lan_ruoxi | film_cotton 紅棉影業 | agency_ho 何生事務所 | 片場嗰邊 | [[1990,"秋"],[1991,"夏"]] |
| 江詩盈 | kong_siying | film_harbour 維港電影 | tvb_kowloon 九龍電視台 | 片場嗰邊 | [[1991,"春"],[1991,"秋"]] |
| 沈映雪 | shum_yingsuet | rec_wanchai 灣仔唱片 | tvb_harbour 海港廣播 | 唱片公司嗰邊 | [[1990,"秋"],[1991,"秋"]] |
| 胡美琳 | wu_meilam | film_lion 獅子山製片 | tvb_longmen 星河電視台 | 片場嗰邊 | [[1990,"春"],[1990,"夏"],[1990,"秋"]] |
| 韓秀婷 | hon_sauting | rec_star 天星音樂 | rec_hk 香江唱片 | 唱片公司嗰邊 | [[1991,"夏"],[1991,"秋"]] |

- win 格式跟現有（`[[年份,"季"],...]`，`enc79PresenceP`：窗內 P 0.5→0.75／share 0.65→0.80；`win:[]`
  先係全年無加權，見 pang_siuki）。理據：藍 1990–91（PA 起步→錄音室半首歌）、江文藝片
  （維港電影專做藝術／寫實題材；春／秋影展季）、沈抒情歌后（秋日抒情檔期）、胡 1990 巔峰
  （1990 春夏秋三窗）、韓 1991 巔峰（1991 夏秋兩窗）。冇人用 `unlockYear`（唔係 1992 先出場嘅星）。
- 藍若曦主場／副場避撞核實（§4）：film_cotton＋agency_ho，唔係感情線／支線地點。
- 江：film_harbour（維港電影 desc「喜歡藝術與寫實題材」——文藝片女主角啱晒）＋tvb_kowloon
  （單元劇為主，文藝單元劇出沒）。
- 沈：rec_wanchai（錄音室林立）＋tvb_harbour（desc 寫明「海港電台錄音室，歌手做訪問、宣傳新歌都來這裡」）。
- 胡：film_lion（大片廠，花旦主場）＋tvb_longmen（處境劇／綜藝，電視花旦）。
- 韓：rec_star（銅鑼灣潮流廠牌，MV 與宣傳——跳唱天后）＋rec_hk（舞蹈室練舞）。

## §2 送禮喜好（星層，`rom176ApplyGiftOverrides` SP176 格式：最愛 2／喜歡 2／唔鍾意 1–2）

禮物 item id 只有 10 隻（`content/items_gifts.json`），全部沿用現有，唔開新禮物。
分流靠入口唔靠禮物：星層 prefs 鍵係全 id（`lan_ruoxi`），感情層鍵係短鍵（`lan`／`yip`／`so`），
兩套 `GIFT_PREFS.npcs` 條目唔會互相覆寫（`rom176` 行 L14816 先，`rom159` 行 L14818 後，寫唔同鍵）。

| 星 | 最愛 fav（+4） | 喜歡 like（+2） | 唔鍾意 dis（−2） | 理據 |
|---|---|---|---|---|
| 藍若曦 | coffee_beans、memo_pad | thermos、egg_tart_box | fashion_mag | 場記捱夜：咖啡頂住＋拍紙簿記通告；唔睇時裝雜誌。感情層最愛係 handmade_sweet＋cassette_indie（ROM159），星層最愛零重疊。 |
| 江詩盈 | memo_pad、cassette_indie | coffee_beans、handmade_sweet | fashion_mag | 文藝片女主角：拍紙簿記角色筆記＋聽歌入戲；唔睇八卦時裝。 |
| 沈映雪 | cassette_indie、thermos | coffee_beans、handmade_sweet | pineapple_bun_set | 抒情歌后：聽歌＋護嗓暖水；唔食街坊菠蘿油。 |
| 胡美琳 | perfume_sample、hair_clip_set | fashion_mag、handmade_sweet | thermos | 影視花旦：淡香＋髮夾襯造型；保溫瓶太老土。 |
| 韓秀婷 | cassette_indie、coffee_beans | thermos、memo_pad | perfume_sample、fashion_mag | 跳唱天后：練舞聽歌＋捱夜咖啡；流汗練舞唔用香水／雜誌。 |

反應句跟現有格式：FAV176 每星 2 條 item-specific 最愛句（共 +10 條）、GEN176 每星各 1 條
liked／dislike 通用句（共 +10 條）。`GIFT_REACT` 條目總數 48 → 68（見 §6 舊測試更新）。

## §3 升段／上限／回望句（每星 3＋1＋1）

對白廣東話口語；旁白（N 行）書面語。唔寫到同感情線承諾重疊——HE 係正式拍拖，
紅星線升段只講行內交情（認得你、企得埋、肯提點），唔預支任何親密關係。
藍若曦升段句特別避開「等埋我收工」呢類感情線承諾句（感情線 HE 句見 L25959–25966）。

- 藍若曦 stageup：S「咦，你又嚟跟組呀。」／S「通告牌我派完喇，坐低抖陣啦，唔好企喺度阻住人。」／
  N「場記嗰邊冇再趕你走——肯留你喺度食埋個晏，已經係自己人先有嘅待遇。」
  cap：S「等你擔正嗰日，我哋先再傾呢啲。」wrap：S「上次同組，你執通告牌嗰手快過我哋成班人，導演有讚你。」
- 江詩盈 stageup：S「你又嚟探班？」／S「文藝片唔係人人啱睇，你肯坐低睇晒成場，已經好難得。」／
  N「佢冇再將你當普通臨記——肯同你講戲，已經係將你當行內人。」
  cap：S「有啲戲，要你企到嗰個位，先講得明。」wrap：S「上次嗰套文藝片，你嗰場企得穩，導演有提起你。」
- 沈映雪 stageup：S「又係你。」／S「錄音室門口唔係邊個都企得，你企咗咁耐，我留意到。」／
  N「佢講嘢把聲放輕咗——錄音室入面，呢個就係熟人先有嘅待遇。」
  cap：S「等你唱到主角嗰日，我哋先再慢慢傾。」wrap：S「上次嗰首歌，你和音嗰句穩陣，監製有講起你。」
- 胡美琳 stageup：S「咦，臨記仔，又見到你。」／S「我趕住埋位，長話短說啦——你肯企喺度等，我記住。」／
  N「佢冇再由助手隔開你——花旦肯直接同你講嘢，成個廠景冇幾個人有。」
  cap：S「等你紅到有人專登嚟等你嗰日，我哋先再傾。」wrap：S「上次嗰套戲，你嗰場做得唔錯，廠景啲人有提起你。」
- 韓秀婷 stageup：S「喂，練舞室嗰個，又係你！」／S「跳唱呢行，肯睇人練舞練到尾嘅人唔多，你係其中一個。」／
  N「佢冇再將你當路人——肯叫你入練舞室坐，已經係自己人先有嘅待遇。」
  cap：S「等你企上台嗰日，我哋先再慢慢傾。」wrap：S「上次嗰場騷，你企得穩，班dancer有講起你。」

## §4 藍若曦特別處理（感情線＋支線《企出嚟》）

- 兩套數分開：紅星好感 `S.stars.lan_ruoxi.fav`（ENC79，傾談／送禮／殺青）vs 感情線
  `rel_lan`（ROM159，`ROM159_WOMEN.lan`，短鍵 `lan`）。送禮 prefs 亦分鍵（`lan_ruoxi` vs `lan`），
  唔會互相覆寫（§2）。紅星線唔讀／唔寫 `rel_lan`、`flag_lan_commit`。
- 地點避撞（已核實）：感情線約會點 `ROM159_DATES` lan_*＝tvb_longmen（lan_studio）、
  tvb_kowloon（lan_ktv）、rec_hk（lan_rec）、date_lounge、date_beach、cafe_cha（lan_cafe）；
  commit 場 `COMMIT48_DEFS.CMT_lan_commit` loc＝rec_hk；支線《企出嚟》場景＝錄音室（rec_hk）。
  紅星主場 film_cotton＋副場 agency_ho 全部避開——星層撞到佢嘅地方，唔係感情線專屬場景。
- 對白避撞：紅星線升段／初遇／opener 唔寫拍拖、等收工、企隔籬呢類承諾句（§3）。

## §5 實裝清單（index.html，全部加法，唔改現有 12 星任何一行）

1. `ENC79_STARS`（約 L38582）加 5 個 def（id／name／primary／secondary／area／win；無 tertiary）。
2. `ENC79_PILOT`（約 L38596）加 5 鍵＝1——**必要**：`enc79TryIntercept`（約 L39418）揀星嗰陣
   `here.filter(sid=> ENC79_PILOT[sid] ...)`，冇 PILOT 就永遠唔觸發巧遇（淨係入 presence 池、
   人脈頁、殺青，撞唔到＝送禮閘 `rom176CanGiveStarGift` 要求 `st.met` 永遠開唔到）。
3. `ENC79_STAGEUP`／`ENC79_CAP_LINES`／`ENC79_WRAP_ECHO`（約 L38603–38620）各加 5 條（§3）。
4. 初遇劇本 `ENC79_DLG_<id>` ×5（`first`＋`openers` T0–T4＋`address` extra／support／lead／king，
   擺喺 `ENC79_STARS` 之前）＋註冊行（跟 L38622–38625 四行格式）——**必要**：
   `enc79BuildScript`（約 L39148）`if(!D) return null`，冇 DIALOG 嗰陣 `enc79PlayEncounter` 靜默跌返地圖。
   對白見 NOTES 附件（寫喺 code 註解入面，唔另開檔）：初遇 6 句＋2 抉擇、opener 每段 2–3 句、
   address 每級 1–2 句；藍初遇場景寫主場 film_cotton（紅棉影業跟組），唔寫感情線場景。
5. `STAR_SIGHTINGS`（約 L40933）加 5 行（distanceLook／distanceLine／locHint／rumorTeaser／
   resultToast，locs＝主場）——`enc79SheetPresence` 先有降格描寫行，否則在場都唔顯示。
   齊／程前例係用 `ENC79_DISTANCE_EXTRA` 一句頂住；五位直接入 SIGHTINGS 全行，順便餵
   `phase3InlineMock`。
6. `rom176ApplyGiftOverrides`（約 L40128）：`NAMES176`＋`SP176`＋`FAV176`＋`GEN176` 各加 5 位（§2）。
7. `enc79OnWrap`（約 L40377）**code 唔郁**：`grant()` 讀 `enc79StarDef`，加咗 def 之後自動生效
   （主角格好評 +3／劣評 +1、配角格好評 +1／劣評 0，同四角分格同一套）。只更新頭註解
   「非名冊嘅星（藍／江／沈／胡／韓）冇狀態位，跳過」嗰段（已過時）。
8. `enc79PeopleHtml`（約 L40446）小修：冇 `BUST109_EXTRA[def.id]` 嗰陣，縮圖唔用企立／bust
   候補（五位冇 `era_stars` 企立／bust 檔，兩級 404 會出破圖），改用已入庫嘅
   `ENC105_STAND_SILHOUETTE`。12 星原行為唔變（佢哋有 BUST109 鍵）。
9. 唔郁：SAVE key／softRev／產品 `?v=`；唔直改 content pack JSON；`ENC79_PILOT` 12 星原值；
   `PAPER_TOPIC_STARS`（8 名硬編碼，唔係名冊，唔郁）；`ENC79_FIRST_ALT98`（12 星初遇副場對位，
   新星初遇劇本寫主場，唔使對位表）。

## §6 舊測試更新（名冊 12→17，舊前提過時，唔係回歸）

以下斷言寫死「12 星」／「48 條反應句」，加 5 星之後前提本身變咗，必須跟住改（改期望數字，
唔改測試邏輯；逐項喺測試檔加 v20a290 註解）：

- `tests/test_enc79_logic.js:101`：`ENC79_STARS.length===12` → 17（「當紅花旦唔入名冊」一半唔變）。
- `tests/test_enc105_logic.js:41`：`STARS.length === 12` → 17；逐星企立實檔斷言只限原 12 星
  （新 5 星冇企立檔，改驗候補鏈：第一候補係企立路徑、尾二係入庫剪影實檔、尾係 SVG 兜底、無重複）。
  `reachLocs` 13 個唔變（§1 選址保證），D-3 斷言唔郁。
- `tests/test_bust109_static.py:177`：`len(star_ids)==12 and set(star_ids) <= set(EXTRA)` →
  `len==17 and 原 12 星 ⊆ EXTRA`；新 5 星冇 `BUST109_EXTRA` 鍵（冇全身裁圖；見 §7），唔係缺漏。
- `tests/test_rom176_logic.js` A3／A4：`GIFT_REACT.entries.length===48`／`byKey 48` → 68
  （12 星 48 條＋新 5 星 20 條；A1／A3 逐星計數只行原 12 星硬編碼表，數字唔變）。
- `tests/test_enc79_static.py:31`：ok 名「名冊 12 星」→「名冊 17 星」（斷言本身只驗 const＋兩 id，唔變）。
- `tests/test_enc105_static.py`：`STARS12` 硬編碼 12 星，唔郁。

## §7 已知限制／跟進（唔喺今票做）

- 美術：kong／shum／wu／hon 四位冇任何立繪（`assets/story/era_stars/` 無 stand／bust、
  `assets/story/fullbody/` 無 base）；lan 有 fullbody（`lan_ruoxi_base.webp`＋表情款），
  巧遇舞台經 `dlg106Candidates` 會用到，`era_stars` 企立／bust 則冇。四位要補立繪先有
  `BUST109_EXTRA` 鍵＋企立檔——另開美術票，唔喺 v290 做。未補之前，巧遇舞台行現有候補鏈
  （企立→bust→入庫剪影→SVG 兜底，唔出破圖）；人脈頁縮圖行 §5(8) 剪影。
- 支線：五位暫時冇 ENC79_BEATS 支線（warm／cold／patron／finale），只係巧遇＋送禮＋殺青好感。
  支線另開票（跟 v278 六線格式）。
- `ENC79_TEA_POOL`／風聲樞紐：新星自動入 `ENC79_STARS` 迴圈（`enc79EnsureDay`／風聲／
  `yip_stand` 揀人），唔使另加。

## §8 新測試

- `tests/test_r290_five_stars.js`（邏輯，node）：def 齊 17、主副場係有效 LOCS id、win 格式、
  `enc79StarDef`／lazy-init、殺青四角分格對五位生效（好評主角 +3／配角 +1、劣評主角 +1／配角 0、
  null 格／重複格跳過）、送禮喜好讀到（fav／like／dis 分層＋delta +4／+2／−2）、
  stageup／cap／wrap 句齊、`enc79BuildScript` 初遇＋重遇 opener 非空、PILOT 齊 5 鍵、
  presence P＞0。
- `tests/test_r290_five_stars_static.py`（靜態）：defs／PILOT／DIALOG const＋註冊／STAGEUP／CAP／
  WRAP／SP176／FAV176／GEN176／SIGHTINGS 全部齊；主副場 id 喺 LOCS 表；onWrap 舊「跳過」註解已清；
  SAVE key／softRev／`?v=` 不變。
- 釘行 resync：index.html 行數變動會令全套測試錨點漂移——對 pristine main（常駐 clone
  `~/workspace/linji-repo`）逐個驗證純漂移後 resync（單次掃描 dict 查表，唔逐對 re.sub；
  唔改測試期望本身，§6 嗰啲除外）。

## §9 數字基線

- Suite 基線 351 PASS／9 FAIL（九項已知 pre-existing FAIL：flash51／slot50／
  soft_tip_111_restore／start53／weave43_static／weave44_static／weave49_static／wf5_87／wrap38）。
  新測試 2 檔應令 PASS 351→353，FAIL 唔多過 9。
- gig 庫 cast 命中（parent 核實＋工人覆核 `content/gigs_new.json`）：wu leadF 51／supportF 34、
  kong leadF 28／supportF 25、hon leadF 10／supportF 19、shum leadF 11／supportF 12、
  lan leadF 4／supportF 18（另 singer 7）。五位全部有主角格＋配角格實例，殺青分格有嘢加。
