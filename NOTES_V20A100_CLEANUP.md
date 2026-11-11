# v20a100 CLEANUP：矛盾審計清理包（基底 v20a99／git 62ba441）

劇情矛盾審計（`linji-contradiction-audit.md`）v98 修完硬矛盾 9 項之後，淨返輕微 14 項＋存疑 11 項，今包一次過逐項處置。**每項都有處置（修／唔修＋理由），冇靜靜雞跳過。** 紀律：唔改 SAVE key／softRev／?v=；唔直改 runtime pack JSON（故事／通告文本一律行覆寫／清洗／正規化層；檔案層 dev 檔 protagonist／worldview／cast_main／gift_react 係今包明文要求嘅衛生對象，先至直接正規化）；玩法數值除 B-03 指明項外冇郁；結局判定冇郁（B-07／B-08／B-09 只改呈現文本）。

## 逐項處置表

### 必做（用戶已拍板／方向已定）

| 編號 | 處置 | 證據／理由 | 改咗邊度 |
|---|---|---|---|
| B-10 兩位芬姐 | **修：分名** | 用戶 2026-11-11 17:18 拍板「係兩個人，改名分開」。全 index「芬姐」71 處逐處分類：副導演嗰位（鏈 F EXODUS_FEN／WF4 相識送別／結局回收／speaker 註冊）全保留；茶水檔嗰位得 3 處玩家文本。新名「珍姐」：珍／蓮／娥／英／梅／雲／娟／好／華／冰姐 grep 全部零撞名；年代合理、讀音同芬姐（fan1）分得開（zan1）；唔用霞姐（WF4 已有霞姐） | index：C9 糧單句「茶水芬姐」→「茶水珍姐」、C9 standup resultBeats「芬姐嗰日」→「珍姐嗰日」、v96 醫院探病「茶水檔芬姐」→「茶水檔珍姐」、LOC96 註解同步＋加 B-10 分名註記。守門：test_cleanup100_static B10 組（茶水芬姐／茶水檔芬姐清零、珍姐三處到位、芬姐唔同茶水檔／糖水／探病／醫院語境同行——茶水「帳」係片場地點、副導演相識場喺嗰度屬合法語境，唔喺守門範圍）＋test_loc96_logic 探病斷言改版；實駕 hosp96VisitNote 出珍姐句 |
| B-03 藍 PA 機械殘留 | **修（stat）＋唔拆旗（有理由）** | push1「一齊捱過」抉擇殘留 stats.music:1——嗰幕係對通告牌／走位冇唱歌，而且查實 applyChoice 根本冇 music 映射（落 story.soft 死數，零效果）。改做同場景最貼嘅真屬性 stage（台風）+1；同場另一抉擇 music:0 一併改 stage:0。`flag_family_marriage`：crisis 兩抉擇共用——全 index grep 證實**冇任何讀取方**（ocAny 鏈、結局判定、回望都唔讀；v31 覆寫註解已交代佢係 pack 遺留旗名、只作鏈上標記），拆旗要郁 flags_written 一致性同舊檔語義而零收益，決定唔拆 | index ROMANCE_LAN_PA_OVERRIDES.R_lan_push1 兩抉擇 stats＋覆寫註解加 B-03 說明段。連帶測試改版：test_weave48（比較前將 pack 嗰兩處 music 正規化做 stage、註明唯一例外）、test_wf2_81 fixture lanPa.R_lan_push1 兩處 stats 同步（其餘 fixture 原貌）；新測試 test_cleanup100_logic B03 組守住（全藍線冇 stats.music、stage:1、旗保留、flags_written 不變） |
| A-12 C18／C19 章戳 | **修（顯示層）** | pacing.weekMin 96／110 係舊曆殘留；名義窗第 48–61／61–74 週。實閘 evalGate3Y 唔讀 pacing（現況不變），只修顯示 | index STORY_SPINE_NODES_WF1：C18 weekMin 96→48、C19 110→61。驗證：真 storyWeekStamp 出「約第48週／約第61週」（logic 測試）；實駕合併後節點 pacing＝48／61；WF1 其他節點冇掂 |
| A-08 程天諾封王鎖 | **修** | 同線下游 lok_e4grudge／ching_e4 本身以 enc83NewsOut("E4") 做鎖，E4 刊出係鏈上拍點，畀佢加返上游 story 鎖同全鏈一致。用既有 enc83NodeDone("C16")（經 StoryOC.isDone／done_C16 旗）。慢玩家：未做 C16 順延，做完下一個 tick 照刊；正常弧 C16 喺 1992 秋窗（day 974–1064）完成、E4 原訂 day 1015 喺窗內，唔會鎖死 | index news82Tick 加 E4 閘（return 跳過本則）；ensureNews82 舊檔歸檔同樣唔好搶先歸檔 E4（留返順延刊出）。驗證：logic 測試五場景（E5 照刊／E4 未做唔刊／做完照刊／舊檔唔歸檔／舊檔補刊） |

### 應該做（玩家可見唔順）

| 編號 | 處置 | 證據／理由 | 改咗邊度 |
|---|---|---|---|
| A-04 C2／C3 頁首「春」 | **修** | 同 C1（v98 A-03）同批問題：C2 閘 1990 年 1 月、C3 2 月上旬，同屬冬季；跟 v98 CONTRA98_WHEN_FIX 做法（when 用 walk 前舊曆值） | index 新增 CLEAN100_WHEN_FIX（C2→1988冬/W4-5、C3→1988冬/W6-8），contra98FixNodeWhen 兼讀。實駕：載入後 when＝「1990冬 / W4-5」「1990冬 / W6-8」、頁首「主線 · 1990冬」；連帶 test_contra98_logic 抽取補 CLEAN100_WHEN_FIX |
| A-05 C5「秋日午後」 | **修** | C5 冇季節閘（phase＋rel 閘），關係肢可以春季／冬季先開播；軟預覽路徑本身都係用 calendarSeason 蓋過佢。正文三處「秋日午後」（synopsis／setting／beats 首句）改唔綁季節；頁首改行實時曆法（見 A-06） | TEXTFIX55_EXACT 加三條（pack 原文保留、行覆寫層，有守門斷言證明）。實駕：載入後 C5 全文「秋日午後」清零 |
| A-06 支線中段五節點季節標 | **修（頁首行實時曆法；唔加季節閘）** | 五節點（A_tsijun_crisis／A_fong_push2／A_fong_crisis／R_tang_meet／R_xu_meet）只有 phase 閘、P3 喺 1992 年 1 月已達，任何寫死季節都會同大半玩家播出日打架；加 seasonIn 閘會改玩法（推遲可播窗），唔係清理包該做嘅事。跟 soft lane 對 C5 嘅 calendarSeason 口徑：頁首用當下曆法年＋季，永遠同 HUD 日期一致 | index spPlayerMeta 加 CLEAN100 實時曆法分支（C5＋五節點共六個 id）；logic 測試驗 day 0→1990冬、day 75→1990春、day 800→1992春，一般節點行返舊路徑冇誤傷 |
| A-07 《靈幻喜劇迎春夜》標「春季」 | **修** | 春節屬冬；唔郁 gigReleaseLine88 衍生對照表（其他真・春季通告靠佢）。跟 v93 NAME93 先例喺 normalizeGigRecord 尾層按 id 俾 releaseLabel（函數有 label 就優先用） | index 新增 CLEAN100_GIG_RELEASE＋normalizeGigRecord 套用。驗證：實機 sync 後 GIGS 嗰張有 label「預計播出：1990 年農曆新年特輯」、其他春季通告零 label；logic 對照證明冇 label 時先衍生「春季」 |
| B-04 鍾楚凝 heart 年份閘 | **修** | heart 全段以加拿大安排為前提，伏筆 beat chung_f_clue 本身 year>=1991 先開；T3/T4 opener 同樣以安排為前提（「我啲安排搞到七七八八」），一併處理先唔會 opener 漏口 | index enc79BuildScript：新增 chungPre91（year<1991）——opener 封頂 T2、heart 唔播（照行 pool），1991 年起原狀。驗證：真 buildScript 實測 1990（day 100）heart 唔出＋opener T2、1991（day 400）heart 照出 |
| B-05 鍾楚凝 farewell 離場 | **修** | farewell 講明「最後一次見面」；跟芬姐離港後唔再出現嘅既有處理一致。離場判定用 beatsDone.chung_farewell（beat 播完先行，舊檔冇呢隻旗即未播、零影響） | index enc79PresenceP：farewell 播完 presence 回 {p:0}；endingExodusScene410：玩家冇自己走＋farewell 播過先加回收段（冇去送機、茶餐廳窗邊舉涼茶）。驗證：logic（presence 0.25→0）＋結局函數實測有／冇旗兩版 |
| B-06 gu_n10after 開場 | **修** | 跟 v89 BR89 對 gu_loan 嘅前置分版先例同一手法：按 C9 三路旗換開場第一句，其餘 beat 不變（「冇俾嗰張枱食埋」係顧明輝自己賭債自述，三路成立） | index enc79BuildScript beat 分支加 beatSeg100 分版：standup→「你企出嚟幫成組人出聲之後」；mediate→「幫顧明輝同何生爭取到分期之後」；chase→原句；無旗→中性「嗰排台慶前後嘅事過咗之後」。驗證：真 buildScript 四場景全過 |
| B-07 GH 格回望 | **修（只改呈現）** | 入格三路（end95PangProgress：好感≥45／提攜債權／C10）——回望跟返玩家真行嗰路；判定冇郁 | index endingCareerScene410 GH case 分三版：C10 做完→原慈善騷句；好感≥45→「點醒你」版；其餘（債權路）→「留低嗰份提攜」版。驗證：三場景實測 |
| B-09 E5 格虛構細節 | **修（只改呈現）** | 「兩個新人一個入圍一個攞獎」全遊戲冇旗下新人系統／紀錄撐住，刪實績改唔落實嘅抒情句 | index endingCareerScene410 E5 case：改「手底下嗰班新人坐喺前排，望住台上，眼入面有光——嗰種光，你認得」 |
| B-08 曉晴 commit 高格版 | **修（只改呈現）** | 原版預設曉晴攞獎座＋兩人一個攞獎一個入圍，系統冇曉晴得獎紀錄、E1/E2 入格亦冇硬性得獎要求（E1 質性閘先有玩家 win 要求）。改按玩家 awardsLog 真憑據（end95Awards.hasWin）分版：真贏過先講玩家獎座；冇贏過用唔落實邊個攞獎嘅版本（連原低格版「佢嗰套戲入咗圍」嘅虛構都一併收走） | index endingRomanceScene410 hiu commit 分支重寫。驗證：冇 win 版冇「獎座／一個攞獎」字眼、有 win 版先出獎座 |
| B-12／C-05 稱呼線 | **修＋定線守門** | 全 15 處逐處分類（結構分類器）：T4 opener 2、king 6、heart 1、finale beat 1、patron beat 2、T3 pool 2——定線：T4+（T4／king／heart／patron／finale）先准用全名「偉翔」（親密語境，屬設計），T3 或以下一律「阿偉」；只修早過分界嗰 2 處 | index：陸柏言 pool T3「偉翔，紅館嗰場綵排」→阿偉；駱家聲 pool T3「偉翔，我以前夾過隊樂隊」→阿偉。守門：test_cleanup100_static 分類器逐處驗段位（v100 13 處全合線；v99 嗰 2 處會俾佢捉到） |
| C-08 C1 事務所句 | **修** | 場景係中環何生事務所；TEXTFIX55_PHRASES 本身會將「星河電視城」轉「星河電視台」，轉完仍然錯語境，所以用 EXACT 成句改做唔綁場地 | TEXTFIX55_EXACT 加一條：「帶住幾分星河電視城特有嘅急促」→「帶住幾分呢行特有嘅急促」。實駕：載入後 C1 舊句清零、新句在位 |

### 保守處理（證據兩邊企到／檔案層）

| 編號 | 處置 | 證據／理由 | 改咗邊度 |
|---|---|---|---|
| A-09 挖角新聞早 C14 一年 | **維持刊期＋最小措辭調整** | 分工證據企得住（同報 E1 係 C14 連鎖拍點、花邊池 side_poach_rumor fromYear:1991 證明挖角係持續潮）；但 E5 原第一段係事件級直述口吻，同 C14 事件本身撞款。**查證附記：任務簡報所指 E5 內文「主角級合約戰」一字不存於現行 E5 文本（grep「主角級」只命中判準系統文字）——現行三段係直述口吻，今包按等效最小改法處理：第一段改傳聞框架（盛傳／有傳／密斟／係真挖角定放風試水溫），令傳聞級（1991 新聞）同事件級（C14 本人抉擇）分工讀得出；C14 開場回指屬可選，冇做（避免再動主線文本）** | index NEWS82_EVENTS E5 第一段改寫；標題／其餘段落／echo 不變 |
| C-07 C4_b「一筆勾銷」 | **修（揀改文本，唔新起機制）** | 嗰筆係純敘事債、冇入帳本；要兌現就要新做清債路徑＋定義舊檔語義，唔成比例。改文本唔好承諾系統做唔到嘅動作：何生改口「嗰筆數我遲啲先同你計——而家，開工先」（保留施壓語氣、只承諾押後唔承諾勾銷） | TEXTFIX55_EXACT 加一條（pack 原文保留）。實駕驗證在位 |
| A-10 soft 預覽層 1988 殘留 | **部分修＋部分唔修（記錄）** | 修：頁首自檢夾具四條期望值（dualSeedChrome／dualNoSeed／choiSpringCal／choiAutumnCal）寫死 1988、實跑全 FAIL——seed／calendar 分支年份跟 START.y=1990 出，改返 1990 後自檢全綠（實駕驗證 ok:true）；when 分支 p3when 用節點自帶年份、維持 1988 係啱，冇郁。唔修：未入 fetch 清單嘅 soft 變體檔（gigs_1988_3.2.10-soft.json 145 處、SOFT_PROGRESS_SEED 檔）同 gate stub——現況零載入、LIVE 入唔到，改一份冇行為嘅歷史檔冇驗證價值兼有誤傷風險。**接線警告：日後任何 soft 檔要接返 LIVE 之前，必須先做年份正規化（行 years66 口徑），唔好直接接** | index spPlayerMeta_softSeasonSelfCheck 四條期望值＋註解 |
| A-11 protagonist／worldview dev 檔 | **修（正規化）** | 冇載入、玩家不可見，但屬現行口徑嘅門面檔，同步成本低 | content/protagonist.json：startDate 1990-01-01、birthYear 1968（保住 age 22 同 1990 開局一致）、背景「1988年春」→「1990年1月」、goals.long「四年內」→「三年內」；content/worldview.json：title《臨記埋位》、settingYears 1990–1992、playerFantasy「三年光陰」、industryEcosystem「九十年代初」、eraAnchors 刪「八九後」字眼（改「社會氣氛沉重，含蓄滲入…」） |
| B-11 cast／gift 檔案層舊身份 | **修（正規化）** | 未接線唔出街，但接線即翻發，今包拆咗佢：藍 role 歌手稿、關海媚「總編」role（兼含 1995 先有嘅狗仔隊年代錯位）、高文瀚 role「經理人」同何生重疊、gift 藍段錄音／練歌／聯姻字眼 | content/cast_main.json：藍 role→「電視台場記／PA」（personalityDetail「想掌控音樂」→「想掌控自己嘅工作」）、關海媚 role→「當紅花旦／電視台台柱」、高文瀚 role→「電視台金牌推手」（對返生效層稱呼）；content/gift_react_copy.json 藍段（entries＋byKey 鏡像共 9 處）：錄音前→開工前、舞台燈光→錄影廠燈、錄音室→廠入面、練歌→跟場、crisis 標籤「C15 聯姻壓力」→「C15 家族／名分壓力」（家族名分 lines 本身合佢富商私生女設定，保留） |
| C-06 SP_SPEAKER_REG 原名 | **修** | 潛在風險拆咗：註冊表 display 改稱號，同玩家面規則（只准稱號）一致；SP_SPEAKER_LEGACY 鍵保留作映射唔郁 | index SP_SPEAKER_REG kwan_hoimei display「關海媚」→「當紅花旦」 |
| C-10 顧明輝線「電台」用字 | **修（一句 flavor 交代）** | 歌手駐唱／訪談語境下兼營電台講得通，唔使改系統；喺地點 desc 補明文交代，讀者唔使估 | index LOCS tvb_harbour desc 加「呢度除咗電視廠，仲有海港電台嘅錄音室，歌手做訪問、打歌都嚟呢度」 |
| C-09 「附近」外景掛靠 | **唔修（記錄在案）** | 審計本身已判地理講得通（酒廊／高爾夫會所就近掛靠播放地點成立），任務明言唔使做 | 冇改動，處置在此存檔 |

## 連帶測試改版（有意改變行為，原位註明原因）

- `tests/test_contra98_logic.js`：抽取補 CLEAN100_WHEN_FIX（contra98FixNodeWhen 兼讀新表）。
- `tests/test_loc96_logic.js`：探病斷言「芬姐送糖水」→「珍姐送糖水」（B-10 分名）。
- `tests/test_weave48_logic.js`：藍 PA 結構比較加 B-03 唯一例外正規化（pack R_lan_push1 music→stage）。
- `tests/test_wf2_81_logic.js`＋`tests/fixtures/romance_wf2_v80.json`：lanPa.R_lan_push1 兩處 stats 跟 B-03 同步（music→stage），fixture 其餘原貌，測試檔頭已註明。

## 新增守門測試

- `tests/test_cleanup100_logic.js`（30 項）：A-04 when-fix＋頁首、A-05/A-06 實時曆法頁首、A-12 章戳、B-03、A-08 新聞閘五場景、B-05 presence、A-07 label 優先。對 v99 行 → 抽取 throw（反證）。
- `tests/test_cleanup100_enc.js`（20 項）：B-04 真 buildScript 兩年份、B-06 四路開場、B-05/B-07/B-08/B-09 真結局呈現函數、B-10 真 hosp96VisitNote、A-07 真 normalizeGigRecord。對 v99 行 → exit 1（反證）。
- `tests/test_cleanup100_static.py`（42 項）：B-10 守門掃描、B-12 段位分類器、檔案衛生、B-11 自檢夾具字串、A-09 傳聞框架、TEXTFIX 五條＋pack 原文保留、各掛點存在。對 v99 行 → 37 項 FAIL（反證）。

## 驗證總覽

- 全套測試 A/B（逐檔 exit 口徑）：基線 v99 118 PASS／12 FAIL → v100 121 PASS／12 FAIL；FAIL 集逐檔一致（12 個係本機環境性 static 檔，基線同樣 FAIL），差異只有 3 個新測試 PASS——零回歸。
- 觸達審計（audit_wf5）：除標頭路徑一行外同基線逐行一致。
- 實駕（Playwright 本地鏡像，新遊戲真載入）：自檢 ok:true；C1／C4／C5 TEXTFIX 實效（舊句清零＋新句在位）；C2／C3 when＋頁首「1990冬」；C5 頁首跟曆法；C18／C19 合併後 pacing 48／61；GIGS 迎春夜 label 在位＋其他春季通告零 label；全程零 pageerror。B-04／B-05／B-06／結局三項／醫院／A-07／A-08 由 node 抽真函數測試覆蓋（IIFE 封裝函數冇全域出口，同 v98 測試同一手法）。

## 順帶發現（冇喺今包郁，交父 agent）

- `end95PangProgress` 讀好感嗰行用 `s.stars.pang_siu_kei`，但巧遇星 id 係 `pang_siuki`（ENC79_STARS）——嗰行疑似永遠攞唔到 fav 值，GH 入格「好感≥45」一路可能實際上靠唔到（靠提攜債權／C10 兩路入格）。屬 v95 判定邏輯，今包紀律係判定唔准郁，只報告唔修；GH 回望分版我用返正確 key `pang_siuki` 讀，呈現同判定喺呢一點上可能有出入（判定入到格但回望讀到 fav 值會行好感版——呈現嗰邊反而更貼玩家真實經歷）。
