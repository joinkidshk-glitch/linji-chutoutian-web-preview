# NOTES_V20A324_GIG_DISTRIBUTION_GAP

## §1 改動（v324，新通告分布缺口）

補 15 張新通告（A 1 張＋B 14 張），全部初級＋作品，常駐上板，無 trigger。偵察 brief `~/workspace/linji-gig-distribution-gap-brief.md`（2026-11-19）；統籌開工前喺工作副本逐項再核實一次：庫 307 張、1990 冬 film_harbour 得 3 張全部 acting 70、14 個靜態洞逐格重數同 brief §4 表完全一致、年份／級別／媒介／類別／觸發計數同 brief §5 一致、全庫日薪最高 300（DUR90 已死）、DUR90 字串 live 0 命中。

### content/gigs_new.json（＋15 張，307→322，全部附加喺 list 尾，v291 3xx 段之後）

新 id 按（年，媒介）下一個空號：1990 film 306–307、rec 304、tv 305；1991 ad 206–208、rec 208、tv 302；1992 film 302–303、rec 206–207、tv 302–303。數字／日數／聲望全部照同級同媒介鄰近 gig 抄（電影初級 4 日 [240,280]、電視劇初級 3 日 [165,204]、廣告初級 1 日 [64,76]、唱片配唱 9 日 [540,675]）；聲望按年：1990 [18,31]、1991 [20,35]、1992 [25,40]。`year` 寫顯示年，唔手改 +2。

**A（D2 殘留，優先）**
- `gig_1990_film_306`《冬日街市》男配角：film_harbour／1990／冬／電影／初級／作品，3 日，pay [180,210]，fame [18,31]，req {}，roleScale film_support_small。cast：leadM 陸柏言、leadF 鍾楚凝、supportF 江詩盈、supportM null（玩家格）。
- 初稿 days 2 唔合 film_support_small 帶 [3,8]，effectiveShootDays 會 clamp 做 3，test_gig229_years.js D3 FAIL；改做 3 日，pay 按同級日薪 60–70 改做 [180,210]。 brief 要求 1–3 日，3 日合範圍。

**B（14 個靜態洞逐格一張）**
| # | id | 年／地點／季 | 通告 |
|---|---|---|---|
| 1 | gig_1990_film_307 | 1990 film_harbour 春 | 《春日碼頭》男配角，4 日 [240,280]，req acting 16，cast 麥震東／胡美琳／蘇芷茵 |
| 2 | gig_1990_rec_304 | 1990 rec_wanchai 春 | 《春日情歌》配唱歌手，9 日 [540,675]，req vocal 12，singer 駱家聲 M，format 大碟／songType 抒情 |
| 3 | gig_1990_tv_305 | 1990 tvb_harbour 夏 | 《夏日茶檔》男配角，3 日 [165,204]，req acting 14，cast 廖炳星／藍若曦／鍾楚凝 |
| 4 | gig_1991_ad_206 | 1991 ad_adm 春 | 《雪顏》平面模特兒，1 日 [64,76]，req looks 20，護膚霜／護膚品／F／雪顏 |
| 5 | gig_1991_ad_207 | 1991 ad_adm 秋 | 《勁步》產品廣告配角，1 日 [64,76]，req looks 18，運動鞋／運動用品／M／勁步 |
| 6 | gig_1991_ad_208 | 1991 ad_central 冬 | 《家樂麵食》產品廣告配角，1 日 [64,76]，req looks 18，即食麵／食品／N／家香味 |
| 7 | gig_1991_rec_208 | 1991 rec_wanchai 冬 | 《冬夜戀曲》配唱歌手，9 日 [540,675]，req vocal 15，singer 沈映雪 F，大碟／抒情 |
| 8 | gig_1991_tv_302 | 1991 tvb_harbour 冬 | 《寒夜茶樓》男配角，3 日 [165,204]，req acting 20，cast 齊鎮海／江詩盈／蘇芷茵 |
| 9 | gig_1992_film_302 | 1992 film_cotton 夏 | 《夏日海灘》男配角，4 日 [240,280]，req acting 20，cast 陸柏言／韓秀婷／藍若曦 |
| 10 | gig_1992_film_303 | 1992 film_harbour 冬 | 《除夕碼頭》男配角，4 日 [240,280]，req acting 22，cast 廖炳星／鍾楚凝／胡美琳 |
| 11 | gig_1992_rec_206 | 1992 rec_star 夏 | 《夏日舞曲》配唱歌手，9 日 [540,675]，req vocal 20，singer 韓秀婷 F，大碟／快歌 |
| 12 | gig_1992_rec_207 | 1992 rec_wanchai 夏 | 《海風之歌》配唱歌手，9 日 [540,675]，req vocal 18，singer 陸柏言 M，大碟／抒情 |
| 13 | gig_1992_tv_302 | 1992 tvb_harbour 秋 | 《秋日街角》男配角，3 日 [165,204]，req acting 25，cast 麥震東／蘇芷茵／江詩盈 |
| 14 | gig_1992_tv_303 | 1992 tvb_kowloon 冬 | 《冬日街坊》男配角，3 日 [165,204]，req acting 25，cast 廖炳星／胡美琳／魏詠男 |

- 全部作品必備 posterBrief；影視廣告全部 cast 四格（星 id 全部喺 POSTER59 已知星集）；唱片全部 singer＋singerGender＋format＋songType（**更正 brief §7**：live 59 張唱片通告全部有 format／songType 欄，brief 話「無」係錯；新唱片照 live 慣例補齊）；魏詠男唔入任何唱片 singer 格；新名唔含年份數字；15 個 workTitle 全部唔撞現庫。
- W3 獎項提名人零變動已驗證：1990 新 gig pay 全部低過各格第三名門檻（電影 420、電視男配 295、歌手男 396／女 152 上限位），1990 rec_304 singer 駱家聲 pay [540,675] 同現有最高 675 打和，id 排序代表 gig 仍係 rec_115，提名表不變。

### 測試同步（實數，唔係估）
- tests/test_gig229_pack.js：P0 307→322；P1 初級 162→177；P2 作品 180→195；P0 每年 126／100／81→130／105／87；P8 cast 四格 242→253、影視廣告作品 122→133、唱片／綜藝作品 58→62、posterBrief 標籤 164→195；P4 標籤 307→322；P8 註解同步更新。
- tests/test_gig229_grant.js：T0 307→322（註解補 v324 庫 307→322）。
- tests/test_gig229_press94_advice.js：A10_newlib_307→322；named 171→186（base 136 不變；stunt 9 張不變；mtv 41 張不變——新唱片全部 rec_album，唔入 mtv）。
- tests/test_gig229_years.js：C0 307→322；A6 按年表 126／100／81→130／105／87；A6 缺庫跌返 1990：126→130；C1 分組 126／100／81→130／105／87；C2／C3／C4／D2／D3 標籤 307→322。
- tests/test_gig291_winter.js：W0 307→322；W2 1990 冬 40→41、冬季開局可接 18→19（A gig req {} 計入）。
- tests/test_r286_load_year_sync.js：B1 126／100／81→130／105／87、共 307→322；B3 GIGS 100→105；B6 GIGS 81→87；B7 127→131（130＋marker）；B8 100→105。
- tests/test_r307_record_singer_null.js：D 總數 307→322；D 按年 126／100／81→130／105／87；D 1990 冬 40→41；D 1990 高級仍 1 張 film_304 不變。
- tests/test_nat92_logic.js：F2 stagN 295→310（322－12 入門）；D2 badLoc ['film_harbour']→[]，標籤改做「第一週 11 個地點逐日 ≥1 可接」，註解補 v324 更新；E2 普查 0 數 62（13／21／28）→**0（0／0／0）**，註解補 v324 實數＋保留 v291 舊註；(E)／(F) 頭註同步（62→0、264→310——264 本身已係舊數，今次一併修正）。
- 其餘 22 檔「S 庫 307 張」靜態守衛（r299／r302／r304／r305／r306／r309／r310／r311／r312／r313／r314／r315／r316／r317／r318／r319／r320／r321／r322／r5_284／sideline274／sideline280）：307→322；sideline280 標籤補「＋v324 15 張分布缺口 gig」。
- test_gig229_counts.js、test_gig229_stagger.js：無庫數釘，唔使改，照過。

### 唔郁
- 稀有大碟日薪 3080：已死（v261 ÷10 後全庫日薪最高 300），唔開工。
- 九龍電視台首週：已結案（v250＋v255），唔開工。
- SPEC-v2 分布要求：下一次全庫重生成嘅目標，唔係呢票範圍。
- 1990 年唔加高級（D-13；A／B 全部初級）；1990 中級維持 11 張。

## §2 驗收
- 14 個靜態洞逐格重數：全部 ≥1，靜態洞 14→0。
- D2 badLoc == []（day-0 全板可接 45 張）。
- E2 普查 0 地點-週 62→0（1990:0／1991:0／1992:0）——實測歸零，brief 預期「唔會歸零」係保守估計，實數為準；唔為咗歸零加過通告，15 張就係原定範圍。
- F2 stagN 310（322－12 入門）；E0 trigger 37 張不變；P7 trigger 37（credit 26／fame 5／rel 3／rival 1／story 1／wf3harvest 1）不變；BR89 18 對不變。
- 受影響 10 檔測試逐個直接跑全部 PASS（nat92／pack／grant／press94／years／winter／r286／r307／stagger／counts）。
- 全套 suite：見 §5（基線 385／9）。

## §3 殘留
- E2 普查歸零後，「恰好 2」占比 pct 恒 0.0%——普查函數用舊三級 tier 名「中」／「高」計數，新庫 tier 係「中級」／「高級」，永遠計唔到；pre-existing 問題，E1／E3（pct＜40）照過，呢票唔郁。
- 1992 年低門檻 gig（無 req 或 acting ≤20）全庫仍得 4 張（brief §8 旁支觀察；第三年玩家數值一般已成長，唔算分布缺口，呢票唔處理）。
- D-13（1990 高級 0 張）已被 v291 film_304 破一次，今次唔再破；D-13 本身係咪正式修訂，留畀統籌決定，唔喺呢票改 spec。

## §4 出貨
- 工作副本：linji-work324（clone 式），分支 v20a324。
- 合併：常駐 clone `git fetch`＋`git merge --squash FETCH_HEAD`，見 §5。

## §5 落地實際數
- 內容 commit：9019f8a（分支 v20a324）
- main HEAD：0f17d58
- suite：385／9（~/workspace/suite324.txt；9 項 FAIL 係已知 pre-existing：flash51／slot50／soft_tip_111_restore／start53／weave43_static／weave44_static／weave49_static／wf5_87／wrap38）
- Pages md5／bytes：index.html 3032f87432fcd6142ebd2a36172b9c3f／4,701,180（同 v323 一致，呢票 index.html 零改動）；content/gigs_new.json 5583f3884d21980df96dccb324c01e81／512,851（322 張，新 gig 在位，curl 核實 byte-identical）
- 工作副本已刪：係
