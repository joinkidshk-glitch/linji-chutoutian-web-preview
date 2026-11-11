# v20a110 IMPLEMENT NOTES：通告級別與要求對齊（OVR110）實作＋測試紀錄

- **分支**：`v110-gigreq`，由 main `8e9e773`（v20a109）開；工作副本：git worktree `~/workspace/linji-work110-repo`（主 clone `~/workspace/linji-repo` 當時 checkout 緊 v113-story-gates 分支兼有未提交改動，為免掂到在途 v111／v113／v114 嘅工作，v110 用獨立 worktree 做，同一 repo、同一 remote）。
- **審計**：`~/workspace/linji-work110/audit110.md`；改動表 `req_overrides110.json`（246 張）＋`tier_overrides110.json`（96 張）；注入片段 `ovr110_snippet.js`（原樣貼入，零改動）；驗收模擬 `sim110.js`＋`sim110.json`。

## 1. 改動內容（index.html，+16 行，零刪改原有行）

- `normalizeGigRecord` 之前貼入 `ovr110_snippet.js` 全文（`TIER110` 96 id、`REQ110` 246 id、`ovr110Apply(o)`；`null`＝剔走該要求項；冪等）。
- `normalizeGigRecord` 內、NAME93 呼叫之後加一行：`try{ ovr110Apply(o); }catch(_o110){}`（排 DUR90／NAME93／CLEAN100 之後，LEADSTAR59／NAME93 先例）。
- 唔改 content pack JSON（`git diff --name-only HEAD -- content/` 空）、唔改 SAVE key／softRev／`?v=`（static 測試斷言）。
- 覆蓋核實：改動表全部 id 都喺全池（去重 469 張：5 年 pack＋全部注入家族＋GIGS36）存在；觸及去重 **273 張**（見 §8 筆誤說明）；抽樣 grep＋node 驗證（logic 測試 B 段）。

## 2. 三級要求帶數字＋推導理據（audit §2，照抄審計結論）

- **帶（六主屬性最高要求）**：初 0–40／中 41–110／高 111–200。體能另軸（起點 75、唔遞減）：初 ≤110／中 ≤200／高 ≤400。總負擔上限（由開局滿足全部要求項所需總堂數）：初 ≤15／中 ≤60／高 ≤150 堂。副項預算：初 8／中 25／高 60 堂。
- **推導**：開局單項初值演技 18／台風 14／歌藝 14／外貌 22／魅力 16／智商 20／體能 75；訓練期望增益 L1 +5／L2 +7／L3 +9.5，CALIB60 遞減（<28 ×1.0、<55 ×0.36、<110 ×0.25、<190 ×0.19、≥190 ×0.14），體能唔入遞減。堂數換算：40→7–8 堂、110→35–36 堂、200→86–88 堂、260→131–133 堂、350→199–201 堂。初上限 40＝頭一個月、每週上兩三堂就掂到；中上限 110＝一季專攻可達；高上限 200＝終局前專攻一項可達。E1 門檻（雙軌 ≥350＋獎＋≥2 媒介擔正＋≥1 主線鏈）同高帶頂 200 無衝突（E1 要雙軌總和＋成就，唔係單項 350）。
- **改前災情**：1988 pack（1990 年池）171 張入面 146 張脫節（85%），中級中位最高要求 360、高級 820，沿用舊五年版／Qwen 尺度；1991／92 年池相反，要求過低（中位 26–32）。

## 3. 內容優先定級原則（audit §3.3，用戶 2026-11-12 06:52 拍板）

- 逐張先由內容判斷屬於邊級，再對齊另一邊——內容係主角就升 tier，唔准為保「臨」印硬壓要求；內容係臨記就 keep tier 降要求。
- 崗位名主角級（男主角／女主角／主演／主唱／領銜／擔正／單元主角）→高（長製作 ≥7 日或主角 roleScale；短製作主角→中）；配角級（配角／男二／女二／嘉賓／領唱／領舞／模特／隊長）→中；基層（臨記／群演／路人／和音／伴舞／場務／助手／替身／手模／試音／閒角／客串／特約／熟手／頂位／班底／散工）→初。synopsis 自述做基層崗位亦判初。片酬／工期／聲望回報係 tier 嘅回響，唔係獨立證據。主角＋基層詞衝突→人工判（最後 0 張 REVIEW）。
- 手動覆核 9 項（逐項理由見改動表 JSON）：`tv_06`／`tv_07` 替身雜務→中（跟足一季長劇全勤跟組，唔係日薪臨記）；`film_harbour_winter_high` 主要替身、`film_lion_autumn_high` 主要伴舞、`film_harbour_summer_high` 動作特約→中（王牌替身／首席伴舞兼指導／25 日有對白近景武打；原則：指定明星專屬替身係技術工種可升中，伴舞／跟組／班底可換工唔升）；`rec_04` 合唱嘉賓→高（keep，紅館級）；`gig_1990_film_08` 短片男主角→中（keep，單元主角級）；`winter88_bridge_tv_unit` 冬日單元劇鄰里配角→初；`film_harbour_high` 特約男主→高（keep，全片中心人物，「特約」係名銜誤植，改名留殘留）；`tv_08` 伴舞臨記→初（3 日綜藝伴舞，唔同 16–30 日全勤替身）。

## 4. 和音家族判斷理據（audit §4.3）

- 《夜更和音》《新春大合唱》＋同系全部和音通告＝**初級（臨記），keep tier，降要求**。理據：①崗位本身：和音＝伴唱，唔係具名演出者；PRESS94 分類器將「和音」列為基層（base），同臨記／群演／伴舞同級。②v93 先例：伴舞／和音一律當群演級處理。③片酬帶：$3,000–$3,500／10–14 日＝日薪 $300–$350，係初級日薪帶嘅底。④工期 10–14 日係錄音 spread，唔係角色份量（同理 v93：伴舞只計被叫到嗰幾場）。⑤對照：同系《鬼馬夜更和音》（中，$4,100／13 日，req 340／340／260）內容完全一樣係和音，舊 tier 中係錯嘅——一併降做初。
- 最終值：夜更和音 {vocal:40,stage:35,charm:30}→**{vocal:10}**（零訓練即接得）；新春大合唱 {vocal:110,stage:110,charm:120}→**{vocal:15,stage:15}**（歌藝上一堂即接得）；鬼馬夜更和音 中→初，{vocal:340,stage:340,charm:260}→**{vocal:10}**；賀年大碟和唱 `nat92_rechk_win_album` 中→初，{vocal:360,stage:350,charm:290}→**{vocal:20,stage:20}**（3 堂後接得）。其餘和音通告（1989／1990／dead pack）本身已經係初級、要求 12–22，clean，唔郁。

## 5. 重要更正：見報分類器跟內容，唔跟 tier（audit §5.3）

- 用戶原話假設「見報分類器跟 tier 行」，實測 code（v94 `press94RoleClass`）係**內容分類**：角色文字係基層（臨記／群演／和音／過場…）→「臨」印＋製作消息填位；具名角色（主角／配角／嘉賓／模特…）→tier 標籤徽章＋玩家標題。
- 所以**升 tier 唔會自動除「臨」印**。27 張升 tier 入面 26 張 named，徽章跟住改；1 張例外：《櫥窗》過場模特 `gig_1990_film_01`（初→中）——標題有「過場」二字，press94 判 base，升咗 tier 個「臨」印都唔會消失。呢個唔係 bug，係分類器設計；想除印要改標題文字（「過場」→「櫥窗」），唔係改 tier。
- tier 改動實際影響：通告欄分組＋每級保底、聲望底線（中 16／高 32）、`chance()` 倍率（中 ×0.9、高 ×0.82）、DUR90 日薪帶參照。降 tier 69 張同理：具名角色降 tier 只係徽章標籤變，見報待遇不變；基層角色降 tier 後「臨」印不變。

## 6. 升 tier 清單（27 張——而家唔再係臨記）

升咗 tier 之後唔再喺臨記板出現，改去中／高級板，要聲望 ≥16／≥32 先報得。逐張理據見 `tier_overrides110.json`；板位已由 sim §5＋logic 測試 G 段核實。

| 通告 | 年份／地點 | 舊→新 | 新要求（最高） | 印 |
|---|---|---|---|---|
| 《龍鳳喜餅賀春照》平面模特 `gig_1988_ad_02` | 1990／ad_adm | 初→中 | looks 45 | 徽章跟 tier 改 |
| 《天台快歌音樂錄像》領舞演員 `gig_1988_mtv_02` | 1990／rec_wanchai | 初→中 | vocal 60 | 徽章跟 tier 改 |
| 《古裝刀劍海報拍攝》武打模特兒 `gig_1988_photo_01` | 1990／ad_adm | 初→中 | looks 85 | 徽章跟 tier 改 |
| 《海傍情話》男主角（MV，1 日）`gig_1988_rec_02` | 1990／rec_wanchai | 初→中 | charm 65 | 徽章跟 tier 改 |
| 《茶客即興猜情晚會》遊戲嘉賓 `gig_1988_var_01` | 1990／tvb_longmen | 初→中 | charm 70 | 徽章跟 tier 改 |
| 《水上英雄闖龍門》參賽嘉賓 `gig_1988_var_03` | 1990／tvb_kowloon | 初→中 | stamina 135 | 徽章跟 tier 改 |
| 《智醒大挑戰》遊戲嘉賓 `gig_1988_tvb_kowloon_winter` | 1990／tvb_kowloon | 初→中 | iq 80 | 徽章跟 tier 改 |
| 《武林搞笑大擂台》遊戲嘉賓 `gig_1988_tvb_harbour_summer_low` | 1990／tvb_harbour | 初→中 | charm 75 | 徽章跟 tier 改 |
| 《歲晚遊戲大派對》遊戲嘉賓 `gig_1988_tvb_harbour_winter_low` | 1990／tvb_harbour | 初→中 | charm 75 | 徽章跟 tier 改 |
| 《炎夏武俠大競技》競技嘉賓 `gig_1988_tvb_longmen_summer_low` | 1990／tvb_longmen | 初→中 | charm 80 | 徽章跟 tier 改 |
| 《秋裝街頭隨拍輯》街頭模特兒 `gig_1988_ad_adm_autumn_low` | 1990／ad_adm | 初→中 | charm 85 | 徽章跟 tier 改 |
| 《歲晚大清貨》搶貨男主角（廣告，2 日）`g36_89_win_adm_clearance` | 1991／ad_adm | 初→中 | acting 90 | 徽章跟 tier 改 |
| 樂隊「夜渡」快歌 MTV 男主角 `gig_1989_mtv_01` | 1991／rec_star | 初→中 | looks 75 | 徽章跟 tier 改 |
| 音樂雜誌封面男配角棚拍 `gig_1989_rec_08` | 1991／rec_wanchai | 初→中 | looks 50 | 徽章跟 tier 改 |
| 《櫥窗》過場：櫥窗換裝模特 `gig_1990_film_01` | 1992／film_lion | 初→中 | looks 70 | **「臨」印不變**（標題「過場」，見 §5） |
| 《武館少年》配角：新入門師弟 `gig_1990_tv_04` | 1992／tvb_kowloon | 初→中 | acting 75 | 徽章跟 tier 改 |
| 文藝專輯《側影》概念照男配 `gig_1990_rec_03` | 1992／rec_wanchai | 初→中 | looks 50 | 徽章跟 tier 改 |
| 新晉歌手「南風」主打 MTV 男主角 `gig_1990_mtv_01` | 1992／rec_star | 初→中 | looks 70 | 徽章跟 tier 改 |
| 「星河台慶特刊」特刊平面模特 `gig_1991_ad_03` | 1991／dead | 初→中 | looks 90 | 徽章跟 tier 改 |
| 打歌快歌《門閘外》MTV 男主角 `gig_1991_mtv_01` | 1991／dead | 初→中 | looks 75 | 徽章跟 tier 改 |
| 《點唱不打烊》打歌嘉賓暖場 `gig_1991_var_06` | 1991／dead | 初→中 | charm 75 | 徽章跟 tier 改 |
| 回望輯快歌《舊路燈》MTV 男主角 `gig_1992_mtv_01` | 1992／dead | 初→中 | looks 75 | 徽章跟 tier 改 |
| 《笑住過肥年》茶樓夥計（小配角）`gig_wf3_liao_stage` | 條件／WF3 | 初→中 | req {}（故事旗係閘） | 徽章跟 tier 改 |
| 《雨夜街頭》主唱歌手 `gig_1988_rec_hk_autumn` | 1990／rec_hk | 中→高 | vocal 120 | 徽章跟 tier 改 |
| 《春日柔情》唱片主唱 `gig_1988_rec_hk_spring_mid` | 1990／rec_hk | 中→高 | vocal 125 | 徽章跟 tier 改 |
| 《嚴冬暖歌》唱片主唱 `gig_1988_rec_hk_winter_mid` | 1990／rec_hk | 中→高 | vocal 125 | 徽章跟 tier 改 |
| 《江湖兒女情歌》主唱歌手 `gig_1988_rec_star_summer` | 1990／rec_star | 初→高 | vocal 120 | 徽章跟 tier 改 |

註：四張 10–13 日唱片主唱升去高級——佢哋係唱片主唱（企咪前擔正一首歌），唔係伴唱；同日薪 $300–$1,100 偏低係片酬殘留（§9），tier 同 req 照內容行，片酬另票處理。dead pack 4 張（`gig_1991_ad_03`／`gig_1991_mtv_01`／`gig_1991_var_06`／`gig_1992_mtv_01`）等加年先生效。

## 7. 測試紀錄

### 7.1 新測試（跟現行 tests/ 慣例：node＋python，抽 index 真函數 eval；有反證）

- `tests/test_gigreq110_logic.js`（45 項，全 PASS）：A 對照表＋接線（96／246 id、NAME93 之後）；B 覆蓋（全池 469、觸及 273、全部 id 存在）；C 一致性（`classify` 移植自 `audit110.py`，全池 A／B／C 清零；三年每級中位精確值）；D 開局 day-0 可接 20（≥12 底線；唔寫死上限）；E 第 2 週 rec_hk 梯子（2／8→3／8→4／8）；F 板重跑洗走對照（池內觸及通告重跑兩次不變；池後加工對照：改 req 做舊值 360 再上板，洗返 OVR110 新值——證實改動一定要落 normalize 層）；G 升 tier 27 張新 tier 正確＋三年掃描唔再以初級上板；H 冪等；I 和音家族＋升 tier 錨點。
- `tests/test_gigreq110_static.py`（22 項，全 PASS）：SAVE／softRev／`?v=` 冇變、NOTES 在位、OVR110 標記＋接線次序、錨點字面、對照表只出現一次、段內冇真藝人名、`content/*.json` 零改動（git diff）。
- **反證**：兩隻新測試喺 pristine main（`8e9e773`）上跑會 FAIL——logic 測試 **36 FAIL**（A1–A9 對照表缺失、C1 全池 251 張脫節、D1 day-0 係 14 唔係 20、E／F／G／I 錨點全失）；static 測試 **18 FAIL**（OVR110 標記／接線／錨點／NOTES 全部缺失；SAVE／softRev／`?v=`／冇真藝人名 4 項照 PASS）。已實測（見 §7.3）。

### 7.2 全套 A/B（runner：逐檔 `node tests/test_*.js`／`python3 tests/test_*.py`，exit code 計 PASS／FAIL）

| | PASS | FAIL |
|---|---|---|
| pristine main 基線（`8e9e773`，worktree 未改動前） | 146 | 12 |
| 分支 `v110-gigreq`（本包） | **148** | **12** |

- ＋2＝兩隻新測試檔；FAIL 清單逐字相同（12 個全屬已知環境性 static FAIL：`test_flash51_static.py`、`test_giglib36_static.py`、`test_pacing35_static.py`、`test_poster59_static.py`、`test_rumor49_static.py`、`test_slot50_static.py`、`test_soft_tip_111_restore.py`、`test_start53_static.py`、`test_weave43_static.py`、`test_weave44_static.py`、`test_weave49_static.py`、`test_wrap38_static.py`），**零新增回歸**。
- 主 script（抽出 inline `<script>`）`node --check` OK。註：`node --check index.html` 本身唔適用（.html 唔係 JS 檔，Node 會當 ESM 拒載；慣例係抽 script 做 check，見歷版 NOTES「主 script 抽出 `node --check` OK」）。

### 7.3 驗收模擬重跑（`sim110.js`，對住分支版 index.html）

| 檢查 | 改前 | 改後 |
|---|---|---|
| Day-0 全板可接（v92 §D 口徑） | 14 | **20**（各地點：rec_hk 2、tvb_longmen 3、film_lion 1、film_cotton 1、film_harbour 1、tvb_harbour 2、tvb_kowloon 1、ad_central 2、ad_adm 2、rec_wanchai 1、rec_star 4、其餘 0；第一週 0 違規地點） |
| 第 2 週 rec_hk 板，零訓練 | 1／8 | **2／8**（＋夜更和音） |
| 歌藝 1 堂後 | 1／8 | **3／8**（＋新春大合唱） |
| 歌藝 2 堂＋魅力 1 堂 | 1／8 | 3／8 |
| 再加台風 1 堂 | 1／8 | **4／8**（＋賀年大碟和唱；三張和音全開，剩低 4 張係領唱／主唱，合理鎖住） |
| 每級中位最高要求 1990 | 初 100／中 360／高 820 | **初 20／中 70／高 130**（n=77／60／29，範圍 0–40／45–100／120–165） |
| 每級中位最高要求 1991 | 初 18／中 32／高 65 | **初 18／中 65／高 147.5**（n=49／32／4，範圍 10–38／42–105／120–155） |
| 每級中位最高要求 1992 | 初 18／中 28／高 80 | **初 18／中 66.5／高 172.5**（n=45／32／6，範圍 10–40／45–110／120–200） |

全部同審計 `sim110.json` 一致。Day-0 20 vs 目標約 14 嘅 +6 全部係入門初工（4 張和音＋2 張客串／群戲），審計判斷為可接受、唔建議壓返 14（見 audit §8.1）。

## 8. 殘留缺口（今包唔包，另票）

1. **審計數字筆誤**：audit §1「觸及去重總數 281 張」同改動表 JSON 對唔上——實數係 96＋246−重疊 69＝**273 張**（已由 JSON／snippet／全池三邊核對：snippet TIER110／REQ110 同 JSON id 集＋值完全一致，全部 273 個 id 都喺 469 池存在）。審計好可能係重疊數計錯（61 而唔係 69）。測試斷言 273，唔跟 281；審計報告本身唔喺呢包改。
2. **內嵌 fallback 11 張 req 差異未處理**（audit §10.4）：`index.html` 內嵌 GIGS（137 張）有 11 張 req 同 pack 唔同；fallback 只喺 pack 載入失敗時先生效，未納入呢次對齊。
3. **片酬／工期異常 9 項另票**（audit §10.1）：`rec_hk_autumn` 雨夜街頭主唱 $3,900／13 日（高級主唱太低）；`film_harbour_summer_high` 動作特約 $41,900／25 日（落咗中級）；`film_04` 伴舞臨記 6 日 $4,800（落咗初級）；廣告模特家族 $16,000／2 日（落咗中級）；`g36_90_aut_lion_blockbuster` 男二 $37,500／14 日（落咗中級）；`tvb_*_high` 跟組特約 ×3 $30,000／30 日（落咗初級）；`rec_03` 試音歌手 $15,000／10 日（落咗初級）；`nat92_rechk_win_album` 和唱 $10,000／9 日（落咗初級）；`rec_hk_winter_high` 領唱特約 $26,000／10 日（落咗中級）。本包完全冇郁片酬／工期。
4. **文案殘留**：「特約男主」`film_harbour_high` 名不副實，宜改名做「男主角」；`tv_06`／`tv_07` synopsis 入面「臨記」字眼同中級定位有輕微出入。
5. **死內容**：103 張（`gigs_1991.json`／`gigs_1992.json`）永不載入；改動表有佢哋 37 張（scope=dead），等遊戲加年先生效，唔加年就無效但無害。
6. **聲望第二閘**：中要聲望 ≥16（約第 10–13 週）、高要 ≥32（約第 20–24 週）——就算 req 落帶，tier 進度都受聲望閘住。設計原意，唔係 bug；驗收要分開睇（req 問題 vs 聲望問題）。
7. **Day-0 20 vs 目標約 14**：見 §7.3——+6 全部入門初工，可接受；唔建議為壓數字重新鎖死和音。
8. **B-raise 判斷**：1991／92 pack 嘅中／高通告原 req 全部細碼（20–36），成批升去中帶／高帶——係跟驗收標準（每級中位落帶）而做嘅判斷，唔係逐張內容判斷；如果實玩覺得 1991 年中級工太難，槓桿係放寬中帶下限，唔係逐張改。
9. **1990 高級後移**：1990 年 29 張高級工最平都要 106 堂，實質係第二年先開到；如果想 1990 年都有高級工即玩，槓桿係加開幾張低要求高級工，唔係放寬高帶。
10. **C 類原先係 0**：全庫無「級別啱但個別項離群」個案；B-raise 之後有 5 張變咗 C，生成器已用副項預算夾返落去，覆核清零。

## 9. 未做嘅事（留返下一手）

- 唔合併、唔推 main（任務指定）。
- 合併後實駕＋線上核實（開局可接數、第 2 週 rec_hk 板、升 tier 通告板位）留返下一手工人做。
