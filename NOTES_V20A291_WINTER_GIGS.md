# NOTES_V20A291 — Q3：補 1990 冬開局通告

- 基線：main `2f7f0d7`（v290 已落地，suite 353／9）；工作分支 `v291-winter-gigs`。
- 庫 289 張 → **302 張**；1990 年 111 張 → **124 張**；1990 冬季 27 張 → **40 張**。

## 1. 設計拆解（已核實，唔係假設）

### 1.1 開局板面冬季淨 9 張嘅真正原因

用 index.html 真函數（`gigsForLocSeasonBoard`／`gigSeasonHidden88`／`gigBoardPosted92`／`nat92PostIntervals`）模擬（`/tmp/sim291.js`）：

- day 0（1990-01-01，冬）27 張冬季通告**全部可見**上板——可見性唔係問題。
- 但開局數值（演技 18／台風 14／歌藝 14／外貌 22／魅力 16／智商 20／體能 75）之下，只得 **9 張 req 全數達標**：ad_201、film_101、film_207、rec_204、tv_208、tv_210、tv_214、variety_201、variety_202。其餘 18 張要演技 24–72／歌藝 16–45／台風 18–30，先有訓練／升呢先接得到。
- 所以缺口係「開局即刻接得到嘅冬季選擇」，唔係冬季通告總數。新增 9 張開局可接冬季通告，開局可接數 9 → **18 張**。
- 冬季窗機制（唔改 code）：冬通告有兩個上板窗——年初窗（1–2 月，開局即見）＋錨定提早窗（10 月起，趕 12 月檔期）；新通告跟同一機制自動行，`nat92PostIntervals` 按 year／season 衍生，唔使加欄位。

### 1.2 1990 高級缺口

- 1990 全年零高級／稀有（P3 舊斷言）。新加 **1 張高級**（克制：只 1 張，開局玩家 req 唔夠，接唔到，板面顯示「暫未能報」做目標）。
- 高級 pattern 跟現成 `gig_1991_film_209`／`gig_1991_tv_210`：tier 高級＋category 臨記通告＋req 演技 70／體能 80＋pay [510,630]。高級唔係靠片酬定義，係靠門檻同崗位。
- 新高級通告**唔加 trigger**（P7 觸發通告維持 34 張），只靠 req 鎖住。

### 1.3 命名（跟 RESEARCH-v2，唔憑空諗）

- 電影四字為主（§1.1：四字佔 50%）、賀歲吉祥詞只用喺賀歲檔（§1.2 #10）；電視劇四字為主、處境劇口語生活詞（§2.2 #7）；歌名用「時間／天氣＋情感」句式（§3.2c）；廣告寫明產品（§4.4）；綜藝用已核實檔期（§5：仁濟慈善騷 1 月、台慶月 10–12 月）。
- 候選名全部對過 `research-film-raw.md`／`research-tv-record-raw.md`＋現庫 workTitle／title，零撞真實作品名、零撞現庫名（`刀光劍影`現庫已有、`一家人`現庫已有，已剔走）。
- **G-1 合規**：1990 年賀歲片（1 月 18–24 日上映）拍攝通告唔寫。`film_302`《喜氣洋洋》係 **1991 年賀歲片**（農曆新年 1991 年 2 月 15 日），1990 年冬拍攝，行足提早週期；其餘新電影係聖誕檔／冬日檔，唔係賀歲片拍攝。
- 新名唔含年份數字；唔用真人名做玩家面角色。

### 1.4 獎項提名人收集：零影響（刻意設計，唔係巧合）

`awards63Fellows` 每格取 3 個，按片酬（pay[1]）降序、每星一部；只計 category 作品。1990 年各格第三名片酬（門檻）已計出：

| 格 | 第三名 pay[1] |
|---|---|
| 電影男主角／女主角／男配角／女配角 | 420 |
| 電視男主角／女主角 | 1480；男配角 204；女配角 1080 |
| 廣告男主角 65；女主角 76；男配角 76；女配角 130 |
| 男歌手 144；女歌手 152；司儀 65 |

新通告避影響嘅做法（三選一，每張都符合其中一種）：

- **category 臨記通告**（film_304、film_305、ad_303）：獎項唔計，片酬／cast 任意。
- **cast／singer／host 用該格現有頭三名星**（film_303、tv_304、rec_303、variety_302）：去重後唔會新增提名人，名次不變。
- **片酬低過該格第三名**（film_302、tv_302、tv_303、ad_302、rec_302、variety_303）：排唔入頭三。
- 另：`variety_302` host 彭少祺片酬 130 同陸柏言並列第一，id 排序令陸柏言續任第一，彭少祺第二、顧明輝第三，順序不變；彭少祺代表作名由《星聲歌唱大賽》變《仁濟慈善夜》，測試無斷言司儀格代表作名（只斷言星名順序）。
- **film_303 換角教訓（實測捉到兩次）**：`awards63Fellows` 按星去重，取該星該格最高片酬嗰部做代表作。第一次用麥震東做男配角（pay 1430）令佢由配角格第三名升上第一名，破配角格順序斷言；第二次改麥震東做男主角（pay 1430）令佢嘅代表作由《鐵血拳手》變《寒江雪》，破無 catId 舊呼叫「第三位係麥震東《鐵血拳手》」斷言。最終定案：男主角廖炳星（代表作續為《笑匠出山》，id 排序不變）、男配角陸柏言（已是該格第一名）、女主角鍾楚凝、女配角魏詠男（兩人代表作不變）。教訓：**中級以上作品選角，唔可以淨睇「該星係咪頭三名」，要睇「該星喺該格嘅最高片酬代表作會唔會變」**——包括無 catId 舊呼叫嗰條路（讀 cast 首格）。
- 新唱片全部 singer 有星（rec_302 藍若曦 130＜152；rec_303 顧明輝 1188＝現有第一，去重不變），**無一張改動提名人收集**；測試期望一個字唔使改（除咗總數斷言，見 §3）。

## 2. 新通告清單（13 張，全部 year 1990、season 冬）

### 電影 ×4

| id | tier／category | 作品／崗位 | loc | days | pay | req | cast（leadM／leadF／supportM／supportF） |
|---|---|---|---|---|---|---|---|
| gig_1990_film_302 | 初級／作品 | 《喜氣洋洋》賀歲喜劇男配角 | film_cotton | 4 | [240,280] | 演技 15 | 廖炳星／胡美琳／麥震東／韓秀婷 |
| gig_1990_film_303 | 中級／作品 | 《寒江雪》文藝片男配角 | film_harbour | 12 | [1210,1430] | 演技 70 | 廖炳星／鍾楚凝／陸柏言／魏詠男 |
| gig_1990_film_304 | 高級／臨記通告 | 聖誕檔武打替身 | film_harbour | 3 | [510,630] | 演技 70／體能 80 | 麥震東／魏詠男／齊鎮海／鍾楚凝 |
| gig_1990_film_305 | 臨記／臨記通告 | 冬夜街頭群演 | film_cotton | 2 | [55,65] | — | 廖炳星／胡美琳／駱家聲／韓秀婷 |

### 電視劇 ×3

| id | tier／category | 作品／崗位 | loc | days | pay | req | cast |
|---|---|---|---|---|---|---|---|
| gig_1990_tv_302 | 初級／作品 | 《左鄰右里》時裝處境男配角 | tvb_harbour | 4 | [245,295] | 演技 18 | 廖炳星／胡美琳／齊鎮海／蘇芷茵 |
| gig_1990_tv_303 | 初級／作品 | 《歡樂滿屋》時裝處境男配角 | tvb_kowloon | 4 | [245,295] | 演技 15 | 麥震東／藍若曦／陸柏言／韓秀婷 |
| gig_1990_tv_304 | 中級／作品 | 《重案幹探》警匪男配角 | tvb_kowloon | 12 | [1200,1480] | 演技 70 | 麥震東／鍾楚凝／陸柏言／魏詠男 |

### 廣告 ×2

| id | tier／category | 作品／崗位 | loc | days | pay | req | 產品（product／productKind／性別／品牌） |
|---|---|---|---|---|---|---|---|
| gig_1990_ad_302 | 初級／作品 | 《利是迎新歲》電視廣告主角 | ad_central | 2 | [110,130] | 外貌 22／魅力 16 | 信用卡／銀行／N／裕豐銀行 |
| gig_1990_ad_303 | 初級／臨記通告 | 聖誕燈飾宣傳平面模特兒 | ad_adm | 1 | [60,72] | 外貌 18 | 聖誕燈飾／節日裝飾／N／星光燈飾 |

### 唱片 ×2（全部無 cast，作品）

| id | tier | 作品／崗位 | loc | days | pay | req | singer |
|---|---|---|---|---|---|---|---|
| gig_1990_rec_302 | 初級 | 《冬夜情歌》合唱配唱歌手 | rec_wanchai | 2 | [110,130] | 歌藝 12 | 藍若曦（F） |
| gig_1990_rec_303 | 中級 | 《冬夜星辰》大碟主唱 | rec_star | 9 | [990,1188] | 台風 30／歌藝 45 | 顧明輝（M） |

### 綜藝 ×2（全部無 cast，作品）

| id | tier | 作品／崗位 | loc | days | pay | req | host |
|---|---|---|---|---|---|---|---|
| gig_1990_variety_302 | 初級 | 《仁濟慈善夜》歌舞嘉賓 | tvb_kowloon | 2 | [110,130] | 台風 14 | 彭少祺 |
| gig_1990_variety_303 | 初級 | 《喜迎新歲》歌舞嘉賓 | tvb_longmen | 2 | [110,130] | 台風 12 | 陸柏言 |

### 地點分布（冬季）

film_cotton 0→2、film_harbour 1→3、tvb_harbour 1→2、tvb_kowloon 4→6、tvb_longmen 8→9、ad_central 1→2、ad_adm 4→5、rec_wanchai 3→4、rec_star 0→1；rec_hk 維持 2。

### 開局可接（req ≤ 開局數值）

新加 9 張：film_302、film_305、tv_302、tv_303、ad_302、ad_303、rec_302、variety_302、variety_303 → 冬季開局可接 9 張 → **18 張**。中級 3 張（film_303、tv_304、rec_303）同高級 1 張（film_304）開局接唔到，留 1990 年中後期目標。

## 3. 測試更新（刻意更新總數，唔係放寬）

| 測試檔 | 舊斷言 | 新斷言 |
|---|---|---|
| tests/test_gig229_pack.js P0 | 289 張 | **302 張** |
| tests/test_gig229_pack.js P1 | 臨記 27／初級 152／中級 70／高級 19／稀有 21 | **臨記 28／初級 160／中級 73／高級 20／稀有 21** |
| tests/test_gig229_pack.js P2 | 作品 165／臨記通告 117／補拍 7 | **作品 175／臨記通告 120／補拍 7** |
| tests/test_gig229_pack.js P3 | 1990 年高級 0 張 | **1990 年高級 1 張**（Q3 填補缺口，刻意改） |
| tests/test_gig229_pack.js P0 每年 | 1990／1991／1992 = 111／99／79 | **124／99／79** |
| tests/test_gig229_pack.js P5 | 1990 年臨記 19 張 | **20 張** |
| tests/test_gig229_pack.js P8 | 233 張有 cast 四格；影視廣告作品 116 張 | **242 張；影視廣告作品 122 張** |
| tests/test_gig229_pack.js P8 | 唱片／綜藝作品 49 張無 cast | **53 張** |
| tests/test_gig229_press94_advice.js A10 | named 156→**166**、base 133→**136**；mtv 38→**39**（rec_302）、mtv named 20→**21**、base 18 不變 |
| tests/test_gig229_grant.js T0 | 新庫 289 張 | **302 張** |
| tests/test_gig229_press94_advice.js A10 | 289 張 | **302 張** |
| tests/test_gig229_years.js C0／C1 | 289 張；111／99／79 | **302 張；124／99／79** |
| tests/test_gig229_years.js A6 | 1991 缺庫跌返 1990（111 張） | **124 張** |
| tests/test_r286_load_year_sync.js B1／B7 | 111／99／79 共 289；B7 長度 112 | **124／99／79 共 302；B7 長度 125**（124＋1 marker） |
| tests/test_r5_284_logic.js (0) | gig_count_289 | **gig_count_302** |
| tests/test_sideline274_logic.js A1 | 庫 289 張 | **庫 302 張** |
| tests/test_sideline280_logic.js (4) | 通告庫總數 289 張 | **302 張** |
| tests/test_nat92_logic.js F2 | 錯峰合資格 277 張（289－12） | **290 張（302－12）** |
| tests/test_nat92_logic.js E2 | 三年全板 0 地點-週＝70（1990:21／1991:21／1992:28） | **＝62（1990:13／1991:21／1992:28）**——填咗 film_cotton 冬、rec_star 冬兩個靜態洞，1990 空板週減 8，係改善唔係回歸 |
| tests/test_fix88_static.py B3 | 1990 冬季臨記工 4 張 | **5 張**（＋film_305） |
| tests/test_nat92_static.py E1／E1b／E2 | 冬季臨記工 4 張；紅棉冬洞 0 張；灣仔冬 3 張 | **5 張**；**紅棉冬洞已填**（film_302＋film_305）；灣仔冬 **4 張**全部初級 |

新測試 `tests/test_gig291_winter.js`：13 張新通告 id 唯一、必填欄齊（title／type／tier／category／loc／year／season／days／pay／req／fame／blurb／synopsis／roleHint；作品有 posterBrief；影視廣告有 cast 四格；唱片有 singer／singerGender；綜藝有 host）、tier／season／year 正確、1990 冬 40 張、開局可接 18 張、獎項提名人收集零變動（1990 年電影／電視／音樂／司儀各格頭三名同舊庫一致）。

## 4. 無改動範圍

- 唔改板面過濾邏輯、唔改經濟、唔改獎項收集邏輯、唔改任何 trigger（P7 維持 34 張）。
- 魏詠男唔入任何唱片格（新唱片 singer 係藍若曦／顧明輝）。

## 5. 測試結果

- 新測試 `tests/test_gig291_winter.js`：32 項全過。
- 受影響測試逐個覆驗全過：pack／years／grant／press94／trigger／stagger／v251_c／awards63／nat92_logic／nat92_static／fix88／r286／r5_284／sideline274／sideline280。
- 全套 suite（`bash qa131/run_suite.sh`，`~/workspace/suite291.txt`）：**TOTAL PASS 354 FAIL 9**。9 項 FAIL 全部係已知 pre-existing（flash51／slot50／soft_tip_111_restore／start53／weave43_static／weave44_static／weave49_static／wf5_87／wrap38），同基線 353／9 一致；＋1 PASS 係新加嘅 test_gig291_winter.js。
- 第一輪 suite 曾經 347／16：7 項新 FAIL 全部係計數斷言（見 §3 追加表），逐項核實係庫實數變動、唔係邏輯回歸，刻意更新後重跑回復 354／9。
- Pages 核實：gigs_new.json 480,129 bytes md5 `1ec8015569f76ffd1961c9368dbaffbc`；index.html 4,711,711 bytes md5 `ab386a4bbc77edfb5914752c66ad9a21`；兩檔 curl 回來同本地 byte-identical。main HEAD `1ee6b2d`。
