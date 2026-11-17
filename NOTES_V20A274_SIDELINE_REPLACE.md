# NOTES — v20a274 支線人情引薦通告「取代票」

- 分支：`v20a274`（clone 式工作副本 `~/workspace/linji-work274`，由 main `9ef4f81` 起步）
- 性質：**取代，唔係新增**。用戶 2026-11-17 20:24 拍板「換做施工單嗰 6 張」。
- 背景：6 筆人情債權原本各有一張引薦通告在位（v254 remap＋v273 測試釘死），開多 6 張會雙重兌現。今次開 5 張新、駱用現成 `gig_1992_rec_111` 接駁、拆 6 張舊 trigger；舊 6 張變普通板通告。
- Suite：**339 PASS／9 FAIL**（`bash qa131/run_suite.sh`；基線 338／9，＋1 係新增測試檔）。9 項 FAIL 同基線名單逐項對過，全部係已知 pre-existing：flash51／slot50／soft_tip_111_restore／start53／weave43_static／weave44_static／weave49_static／wf5_87／wrap38。
- 未改：SAVE key（`starVolunteer_map_v19w`）、softRev（`s107`）、產品 `?v=`（`v20a10`）——`test_br89_static.py` 釘死。

## 1. 五張新通告（庫 282→287 張）

新 gig id 全部用 2xx 系列下一個未用過嘅號（開工前 grep 核實；2xx 係 v252／v253／v255 加 gig 嗰系）。

| 債權 | 新 gig id | 通告 | 媒介／級／類 | 年季 | 日數／片酬（總數） | 日薪 | fame | cast／singer |
|---|---|---|---|---|---|---|---|---|
| 麥 `credit_enc83_mak_patron` | `gig_1991_film_211` | 《武館群英》武打配角 | 電影／中級／作品 | 1991 春 | 12 日／[1210,1430] | 100.8–119.2 | [28,45] | leadM 麥震東、leadF 江詩盈、supportM null（玩家）、supportF 葉敏芝 |
| 魏 `credit_enc83_ngai_patron` | `gig_1991_film_212` | 《鐵橋風雲》熱血拳手阿龍 | 電影／高級／作品 | 1991 夏 | 24 日／[4416,5184] | 184–216 | [35,55] | leadM null（玩家男主角）、leadF 魏詠男、supportM 麥震東、supportF 胡美琳 |
| 齊 `credit_enc83_chai_patron` | `gig_1992_film_206` | 《油麻地夜班》江湖短打：麻將館看場 | 電影／中級／作品 | 1992 **秋** | 12 日／[1210,1430] | 100.8–119.2 | [32,50] | leadM 齊鎮海、leadF 江詩盈、supportM null（玩家）、supportF 葉敏芝 |
| 鍾 `credit_enc84_chung_patron` | `gig_1991_film_213` | 《秋日絮語》男配角 | 電影／中級／作品 | 1991 秋 | 12 日／[1210,1430] | 100.8–119.2 | [28,45] | leadM 陸柏言、leadF 江詩盈、supportM null（玩家）、supportF 鍾楚凝 |
| 顧 `credit_enc83_gu_patron` | `gig_1992_rec_205` | 《夜總會登台暖場》暖場歌手 | 唱片／中級／作品 | 1992 春 | 2 日／[220,264] | 110–132 | [32,50] | singer 顧明輝（男）、format 單曲、songType 抒情、roleScale mtv |

- 片酬全部跟 peer gig 實際慣例（live pay 係成個拍攝期總數，唔係 SPEC §7.1 單日數）：中級電影男配角 12 日 peer 係 [1210,1430]（`gig_1991_film_101` 等）；高級電影男主角 24 日 peer 係 [4416,5184]（`gig_1991_film_102`）；中級唱片 2 日 peer 係 [200,240]（`gig_1991_rec_203`，日薪 100–120）／[220,264] 日薪 110–132 對齊中級大碟日薪帶。全部 `hi ≤ lo×1.25`、日薪落 SPEC §7.1 帶（中級 90–160／高級 160–300）。
- 年份／季節：默認跟被取代嗰張，**齊例外**（見下）。
- req／hard 全部抄同級 peer：麥 acting 50／stamina 70（`gig_1991_film_205` 武行）；魏 acting 130／stamina 90、hard 0.58（`gig_1991_film_102`）；齊／鍾 acting 75（`gig_1991_film_101`）；顧 vocal 32／stage 30（`gig_1991_rec_203`）。
- 每張有 `discoverNote`「…引薦：…，憑人情入組。」＋blurb 引薦字句＋`posterBrief`＋`storyKeys`（引薦人）。

### 齊季節：1992 夏→秋（Q13）
被取代 `gig_1992_tv_104` 係 1992 夏，但齊鎮海 1992 夏 leadM 作品已有 3 部（`tv_102`／`tv_104`／`tv_107`），Q13 季上限係 3，夏檔再加會超標。改 1992 秋（齊秋檔 leadM 0 部）。江湖片秋檔亦合上映提早規律。

### 鍾新片名：《秋日絮語》理據
WORKORDER 只講「按 BR89 模式擴充一張文藝片引薦試鏡」，無片名。按 RESEARCH-v2 文藝片命名規律起名：1990–92 文藝片多用季節＋抒情意象四字名（如《阿飛正傳》《滾滾紅塵》《客途秋恨》），「秋日」係季節意象、「絮語」係抒情口語化意象，四字、無年份數字、庫內 0 撞名（grep 核實）、唔係真實作品名。麥嗰張《武館群英》同理（動作片「地點＋群體」四字；網上核實無同名真實電影，只有 1981《武館》唔同名）。魏《鐵橋風雲》、齊《油麻地夜班》用 WORKORDER 原名。

### 顧授權寫法
以**用戶 2026-11-17 20:19 補批＋20:24 換票拍板**為準。WORKORDER 2.2 寫「已拍板開（Q2）」同 DECISIONS.md Q2 記錄唔一致（Q2 得 5 張，冇顧），以今次拍板為準，NOTES 唔再寫 Q2 已批。顧級數取**中級**（WORKORDER 寫「中／初」，取中級）。

### cast 安排（Q13＋軟上限）
- 鍾唔做 leadF：鍾楚凝 1991 秋 leadF 作品已有 5 部，live 庫本身已超 Q13（同廖炳星 1990 春 lead 4 部一樣，係既有超標）；新 gig 將佢放 supportF，唔惡化。leadF 改江詩盈（1991 秋 leadF 0 部）。
- 其餘新 lead 格全部 ≤3：麥 1991 春 leadM 1→2、魏 1991 夏 leadF 2→3、陸 1991 秋 leadM 2→3、齊 1992 秋 leadM 0→1、江詩盈 1991 春 leadF 1→2／1991 秋 0→1／1992 秋 1→2。
- 軟上限（同星同媒介同年 ≤ 當年該媒介作品數一半）：1991 電影作品 16→19 張，上限 9.5；新 gig 後最高係魏／胡／鍾各 9 張，全部合標。寫入測試嘅 Q13 檢查用「唔製造新超標、唔惡化已有超標」口徑（live 庫既有超標唔喺呢票修）。

## 2. 駱接駁 `gig_1992_rec_111`（唔開新）
- 加 trigger `{kind:'credit', creditId:'credit_enc83_lok_patron', creditOwner:'駱家聲'}`，加入 `BR89_PATRON_OF_GIG`。
- blurb 頭加引薦框架「駱家聲引薦你到監製老友處試唱，憑人情入組：…」；加 discoverNote「駱家聲引薦：天星一哥新碟 MV 男主角，憑人情入組。」
- **singer 仍係陸柏言，唔郁**（故事係駱介紹你去監製老友嗰邊，試唱陸柏言新碟 MV 男主角）；cast／synopsis 主體唔郁。
- 注意：rec_111 同時係 GRANT229 N14_a 即派目標（`test_gig229_grant.js` T1），即派路徑唔受 trigger 影響。

## 3. 舊 6 張 trigger 拆除（變普通板通告）
| 舊 gig | 改動 |
|---|---|
| `gig_1991_film_110`《鐵拳王》動作替身 | 刪 trigger；刪 discoverNote；blurb 刪「憑麥震東引薦入組，」 |
| `gig_1992_rec_102`《硬漢柔情》新人搖滾主唱 | 刪 trigger；刪 discoverNote；blurb 刪「駱家聲引薦的」；synopsis 首句改「駱家聲新寫的搖滾單曲，玩家擔任單曲主唱。」（其餘 verbatim） |
| `gig_1991_film_111`《雪山雙劍傳》武打配角 | 刪 trigger；刪 discoverNote；blurb 刪「憑魏詠男引薦入組，」 |
| `gig_1992_tv_104`《滬上往事》男配角 | 淨刪 trigger（原本無引薦字句，核實後留返） |
| `gig_1991_tv_108`《深秋情緣》男配角 | 淨刪 trigger（原本無引薦字句，核實後留返） |
| `gig_1992_rec_105`《當年情懷》大碟主唱 | 刪 trigger；刪 discoverNote；blurb「顧明輝引薦並監製」→「顧明輝監製」；synopsis 首句改「顧明輝監製的情歌大碟，玩家擔任大碟主唱。」（其餘 verbatim；boardNote 無引薦字句，留返） |

cast／pay／季節／日數全部唔郁。核實：舊 6 張 trigger 欄已無、blurb／synopsis 無「引薦」字。

## 4. R-4 雙觸發搬遷
`br89GigOn` 硬編碼 `if(raw.id==="gig_1992_rec_105")` → `gig_1992_rec_205`；相關註解（BR89 註解段、R-4 註解）一併改。舊 rec_105 id 只留喺新 v274 註解一句做歷史參照（同 v254 當年留舊 id 做法一樣）。

## 5. BR89 映射（13 對，總數維持）
```
gig_1991_film_101:luk / gig_1991_variety_203:pang / gig_1992_rec_106:ching /
gig_1991_film_103:liu_priority / gig_1992_film_103:liu /
gig_1991_film_211:mak / gig_1992_tv_105:yip / gig_1992_rec_205:gu /
gig_1991_ad_102:so / gig_1991_film_213:chung /
gig_1992_rec_111:lok / gig_1991_film_212:ngai / gig_1992_film_206:chai
```
（其餘 7 對唔郁。）

## 6. 全 repo grep 舊 id（已處理）
- 故事 JSON／頒獎池／海報 brief：**0 引用**（舊 id 只出現喺 gigs_new.json 本身、index.html BR89 區、NOTES 歷史檔、測試）。
- 殘留舊 id 全部係刻意保留：① gigs_new.json 入面舊 6 張本身（仲係普通板通告）；② index.html／測試入面新 v274 註解嘅歷史參照；③ `test_gig229_trigger.js` T1 award 合成樣本（舊庫 film_111 trigger 一字唔改，刻意唔郁——新庫 0 張 award kind）；④ `test_cast252_logic.js`／`test_poster59_logic.js`／`test_newspaper214_wrap_logic.js` 合成 wrapHistory／wrap 夾具（rec_102／film_110 欄位不變，library lookup 照舊解到）；⑤ `test_sideline158_logic.js` L184 `redeemedBy='gig_1991_film_110'`（任意已兌現 gig id）；⑥ `test_dur90_logic.js` F1b 用 film_111 做最接近樣本（日數／片酬不變）。
- 廖 patron 例外（v254 已記錄，唔郁）：`credit_enc83_liu_patron` 對兩張 gig（film_109／film_103），BR89 只取 film_103 做 canonical；「每筆債權只兌現一張」斷言只驗呢 6 筆。

## 7. 測試改動
- **新增 `tests/test_sideline274_logic.js`（26 項，全部 PASS）**：A 庫對位（287 張／trigger 33／credit 23；每筆債權只兌現一張；新 5 張欄位齊；rec_111 接駁；舊 6 張無 trigger＋無引薦字句）；B 開閘（新 6 張無債權唔開／持債權開＋標「引薦」；舊 6 張持債權 BR89 唔開；舊 6 張無 trigger＝普通板通告）；C R-4（還錢路開 rec_205 唔開 rec_105；還錢失敗唔開；債權已兌現落板）；D BR89 13 對逐對啱＋全部喺庫＋舊 id 唔再喺映射入面。
- **重寫**：`test_br89_logic.js`（H1 EXPECT13＋H3 R-4）、`test_br89_static.py`（BR89_13 清單＋R-4 id）、`test_gig229_trigger.js`（T2／T2b／T8 映射＋註解）、`test_sideline273_logic.js`（(d) G-G1／G-G2／G-M2 五對）、`test_sideline158_logic.js`（T8 映射＋T1 武打 matcher 20→22 張，見下）。
- **庫數 282→287**：`test_gig229_pack.js`（P0 287、P1 中級 68／高級 20、P2 作品 164、每年 111／98／78、P8 cast 231 張／影視廣告作品 115／唱片綜藝作品 49）、`test_gig229_grant.js`（T0 287）、`test_gig229_years.js`（C0／C1／A6 want 111／98／78）、`test_gig229_press94_advice.js`（A10 287、named 150→155、mtv 37→38 張／named 19→20）、`test_dur90_logic.js`（A4 287）、`test_nat92_logic.js`（F2 錯峰 270→275 張）、`test_awards63_logic.js`／`test_gig229_v251_c.js`（註解）。
- **連帶計數**：`test_awei195_logic.js` (g) 1991 年真男主角 7→8 部（新 film_212 係真男主角）；`test_sideline158_logic.js` T1 武打 matcher 20→22 張（新 film_211／film_212 係動作＋作品）。
- **行號 resync**（index.html 淨 +2 行，改動區舊 L26400–26450；其後錨點各 +2，逐錨點核實舊行內容＝新行內容）：`test_travel114_static.py`（COUNT 5 處＋FREE 26 處＋DEF 40750→40752＋WRAPPER 28574→28576）、`test_rom176_static.py`（4 個釘行）、`test_gift185_static.py`／`test_tang171_static.py`／`test_tang173_static.py`（總行數 45500→45502＋openLoc DEF 行 40750→40752，連 0-index `lines[40749]`→`lines[40751]`）。
- `node --check`（抽出兩段 `<script>` 合併驗證）：PASS。

## 8. 留意（畀統籌）
- SPEC-v2（`~/workspace/linji-gig-redesign/regen-v2/SPEC-v2.md`，repo 外）§1 數字已滯後：總數 282→287、作品 159→164、電影 1991 年 16→19 張／1992 年 13→14 張、唱片 1992 年 11→12 張、中級 64→68、高級 19→20。呢票無改 SPEC，留統籌決定係咪跟改。
- 顧 gig format 用「單曲」（庫內唱片 format 只有單曲／大碟／MTV／卡拉OK 四種，登台暖場無專屬 format；roleScale 用 mtv，peer 係 `gig_1991_rec_203` 演唱會和音 2 日制）。
- 1991 年真男主角 8 部、武打 matcher 22 張，係新 gig 嘅直接後果，唔係回歸。
