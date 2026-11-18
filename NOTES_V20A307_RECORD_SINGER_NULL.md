# NOTES_V20A307 — B1：10 張玩家主唱唱片 gig 改 null＋補真唱片通告

- 版本：v20a307；基線 main `3a81eac`（v306，suite 369／9）
- 目標：10 張玩家主唱唱片 gig 嘅 singer／singerGender 改 null，令提名人收集唔再將玩家主唱計成星主唱；同時補真唱片通告，令每格男歌手提名人返返 3 個。
- 提名人收集邏輯唔郁（D-v2「只讀新庫真陣容」不變；`awards63Fellows` 照舊）。

## §1 10 張改 null（`content/gigs_new.json`，其餘欄全部唔郁）

| id | 作品 | 原 singer | tier | 季節 | pay |
| --- | --- | --- | --- | --- | --- |
| gig_1990_rec_106 | 《節拍飛揚》快歌男主唱 | luk_baakyin／M | 初級 | 夏 | [120,144] |
| gig_1990_rec_107 | 《燃燒青春》大碟主唱 | lok_gasing／M | 初級 | 秋 | [540,675] |
| gig_1990_rec_109 | 《不羈少年》新人單曲主唱 | lok_gasing／M | 初級 | 春 | [180,216] |
| gig_1990_rec_110 | 《白頭相守》大碟主唱 | gu_mingfai／M | 中級 | 冬 | [990,1188] |
| gig_1991_rec_105 | 《風雨搖滾路》搖滾主唱 | lok_gasing／M | 初級 | 春 | [540,675] |
| gig_1991_rec_107 | 《情濃款款》大碟主唱 | luk_baakyin／M | 中級 | 秋 | [990,1188] |
| gig_1991_rec_108 | 《全城狂歡夜》大碟主唱 | luk_baakyin／M | 中級 | 冬 | [990,1188] |
| gig_1992_rec_102 | 《硬漢柔情》新人搖滾主唱 | lok_gasing／M | 初級 | 夏 | [180,216] |
| gig_1992_rec_105 | 《當年情懷》大碟主唱 | gu_mingfai／M | 中級 | 春 | [990,1188] |
| gig_1992_rec_109 | 《熱血狂奔》大碟主唱 | luk_baakyin／M | 高級 | 冬 | [2000,2400] |

10 張全部 singer／singerGender 改 null；title／pay／tier／season／year／category／req 全部唔郁（測試 A 逐張對返）。

## §2 補 4 張真唱片通告——唔係 brief 嘅 3 張（原因見 §3）

| id | 作品 | 歌手 | 玩家崗位 | tier | 季節 | pay | days |
| --- | --- | --- | --- | --- | --- | --- | --- |
| gig_1990_rec_114 | 《星光閃耀》MV 男主角 | luk_baakyin／M | MV 男主角 | 中級 | 秋 | [330,396] | 3 |
| gig_1990_rec_115 | 《風中勁草》配唱歌手 | lok_gasing／M | 配唱歌手 | 初級 | 夏 | [540,675] | 9 |
| gig_1991_rec_113 | 《午夜快車》配唱歌手 | lok_gasing／M | 配唱歌手 | 初級 | 冬 | [540,675] | 9 |
| gig_1992_rec_112 | 《追風少年》MV 男主角 | lok_gasing／M | MV 男主角 | 中級 | 春 | [330,396] | 3 |

- 全部 category 作品、type 唱片通告；星真正主唱，玩家做配唱／MV 男主角，唔係主唱。
- 歌手揀法：由 live 池覆核嗰年缺邊個男歌手——1990 缺 luk＋lok，1991 缺 lok，1992 缺 lok（見 §3）。
- 新名唔含年份數字；workTitle 全庫唔撞（註：庫內原有 6 對重名 workTitle 係 pre-existing _301 續集對，唔係今次引入）。
- pay／tier 跟返同類唱片通告水平（大碟配唱 [540,675] 初級／MTV 男主角 [330,396] 中級，對照 rec_101／rec_105／rec_109）。
- id 選號注意：新 gig 原擬用 rec_111／112（1990）＋rec_111（1991），但呢三個 id 喺 test_gig229_grant.js `SIDE_DEAD11` 反證清單入面（v255 舊庫已刪 id，必須繼續唔喺庫），用咗會令 T0 反證失效；所以改用 rec_114／115（1990）＋rec_113（1991），1992 沿用 rec_112（唔喺反證清單）。
- 季節刻意避開斷言：1990 兩張唔係冬（test_gig291 W2 斷言 1990 冬 40 張）；1990 兩張唔係高級／稀有（W2 斷言 1990 高級 1 張 film_304）。
- 1990 男歌手格次序守住：gu 1188＞lok 675＞luk 396，同 test_gig291 W3 預期 [gu，lok，luk] 一致。

## §3 改後提名人池前後對照（awards63Fellows 口徑：作品 only＋sprite 濾鏡＋片酬序＋每星一部＋頭 3）

| 格 | 改前 | 淨改 null 後 | 補 4 張後 |
| --- | --- | --- | --- |
| 1990 男歌手 | 3（gu／lok／luk） | **1（得 gu）** | 3（gu／lok／luk） |
| 1991 男歌手 | 3（luk／lok／liu） | **2（luk／liu）** | 3（lok／luk／liu） |
| 1992 男歌手 | 3（luk／gu／lok） | **2（luk／gu）** | 3（luk／lok／gu） |
| 1990 女歌手 | 3（shum／hon／lan） | 3，唔郁 | 3，唔郁 |
| 1991 女歌手 | 3（shum／lan／so） | 3，唔郁 | 3，唔郁 |
| 1992 女歌手 | 3（lan／so／hon） | 3，唔郁 | 3，唔郁 |
| 新人獎（三年） | 各 3，男女齊 | 各 3，男女齊 | 各 3，男女齊 |

**關鍵更正——brief「1992 男歌手維持 3」係錯。**分流報告數嗰陣將程天諾（ching_tinlok，gig_1992_rec_106《夜場匯演》）計入 1992 第三位，但 `awards63HasSprite` 要求星喺 `POSTER59_STAR_IDS` 入面先計，程天諾唔入表（函數註解明寫「程天諾（唔入表）唔計」），所以 1992 淨改 null 後實際得 2 個（luk／gu）。只補 brief 嘅 3 張，1992 格會留喺 2 個，達唔到「每格返返 3 個」嘅目標；所以 1992 多補 1 張 lok_gasing（《追風少年》MV 男主角），共補 4 張，庫總數 302→**306**（唔係 305），按年 124／99／79→**126／100／80**。

## §4 測試期望更新（計數斷言，全部寫明）

- 庫總數 302→306：test_gig229_grant.js（T0）、test_gig229_pack.js（P0＋P4 標籤）、test_gig229_press94_advice.js（A10）、test_gig229_years.js（C0＋C2／C3／C4／D2／D3 標籤）、test_gig291_winter.js（W0）、test_r299_three_flags.js（S1）、test_r302_chung_farewell_paper.js（S1）、test_r304_cold_heart.js（S）、test_r305_warm_finale.js（S）、test_r306_chai_frame.js（F）、test_r5_284_logic.js（gig_count）、test_sideline274_logic.js（A1）、test_sideline280_logic.js（總數＋歷史註）。
- 按年：test_r286_load_year_sync.js B1：1990:124／1991:99／1992:79→1990:126／1991:100／1992:80，共 306。
- 錯峰合資格：test_nat92_logic.js F2：290 張（302－12 入門）→294 張（306－12 入門）；入門 12 張唔郁。
- 唔郁嘅斷言（已核實唔使改）：test_gig291 W2（1990 冬 40 張、冬季開局可接 18 張、1990 高級 1 張 film_304）、W3（1990 各格頭三名，男歌手格次序守住）、W4（魏詠男唔入唱片格、新名唔含數字、新作品名唔撞）。
- 顯示層期望更新（唔係計數，係 null 化嘅直接後果）：test_cast252_logic.js＋test_poster59_logic.js 原先斷言玩家主唱 gig 會出監製星名（detail「主唱歌手：駱家聲（男）」／牆「主唱：駱家聲」），singer 改 null 後 code 本身已有嘅 fallback 分支接手——詳情頁行「應徵中」、作品牆行「主唱：阿偉」，同電影／電視／廣告／綜藝嘅玩家格口徑一致；兩個測試已改斷言新行為，index.html v252 註解同步更新（舊註解話 singer 照填監製星，已經唔啱；改動本身行數 0 變動，唔會掂到釘行）。
- 新測試：tests/test_r307_record_singer_null.js（22 項：A 10 張 null＋欄唔郁、B 4 張新 gig 欄齊＋玩家唔係主唱、C 六格＋新人獎重計、D 總數／按年／冬／高級、E 硬規則），全部 PASS。

## §5 Suite／落地

- Suite：**370 PASS／9 FAIL**（`bash qa131/run_suite.sh`，outfile `~/workspace/suite_v307.log`；9 項 FAIL 全部係基線 pre-existing：flash51／slot50／soft_tip_111_restore／start53／weave43_static／weave44_static／weave49_static／wf5_87／wrap38；新測試 test_r307 22 項全 PASS）
- main HEAD：待填
- Pages：待填（index.html md5／bytes）
