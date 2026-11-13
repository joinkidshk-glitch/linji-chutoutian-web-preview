# NOTES_V20A178 — 高俊傑上頒獎禮（已落地，分支 `v20a178`）

狀態：**已落地 main `ba43b9e`（2026-11-13 15:33 HKT），線上 5,277,347 bytes sha `cfa17f2a…` 已核實同 repo HEAD:index.html 一致。**
Character 由用戶生成（`bbaa5bf2-a598-4863-ba5a-47cc7cc4fe03`），驗收過關，入池已落地；
**Q 版 sprite 衍生已按用戶 2026-11-13 15:11 方向剝走（見 §10），舞台圖由 v180 接手。**

**§10 取代聲明：以下 §§4.6／5／8 入面「sprite 已落地／齊 37 張」嘅講法係剝走前嘅歷史紀錄，
已被 §10 取代——而家 AWARDS64_SPRITES 返返 34 張，高俊傑舞台位跌返剪影（預期中間狀態）。**

## 0. 更正紀錄（2026-11-13 14:29）

- 原 brief 第 2 步「經 connector 開 character」作廢：**PixelLab character 由用戶自己生成，
  工人一隻都唔開，唔用 PixelLab 生成 API**。
- 本票至今 **PixelLab 零調用、零 generations 花費**：開工嗰陣一次 `pixellab.py balance`
  未完成就 aborted，無結果；之後再冇叫過 connector。任務話餘額 4,316／5,000，未經我核實。
- 以下 (a) 驗收方法、(b) 入池年份核實、(c) code 閱讀、測試、NOTES 草稿已做完；
  (d)(e) 實裝、(f) 全套＋實駕、提交，等 character 到先繼續。

## 0b. 落地紀錄（2026-11-13 14:38–14:55 HKT，接手實作；見 §8）

- Character 到咗（用戶生成），驗收過關（§1 補量度）；反證重跑吻合（logic 4 FAIL／4 PASS、
  static 4 FAIL／9 PASS，exit 1，無 crash）。
- 入池已落地（§4 補實裝細節、§8 測試／全套／實駕結果）；sprite 衍生其後按用戶方向剝走，見 §10。

## 1. 高俊傑樣貌 brief（已核實，驗收準則）

來源：`~/workspace/user/files/PLAN_CHAR_LOOKS_REF_v1.md` L44，`ko_chunkit`，23 歲男，core。
面：棱角分明，劍眉星目但眼神帶點傲氣，下顎線銳利；髮型係當時流行嘅中分微長曲髮，
略遮半邊眼。衫：**鮮紅色皮褸（Biker jacket，brief 列紅色先，揀紅色）**，內搭黑色緊身 V 領
T-shirt，配粗銀鏈頸飾。神態：default 囂張揚起下巴，smile 挑釁冷笑，frown 不耐煩反白眼。
- prompt 永禁真人名：靈感對照（鄭伊健早期、郭富城 90 初）只限 DEV 內部，唔准寫入 prompt；
  禁一比一肖像抄臉。
- 唔好同張克凡撈亂：張克凡（`cheung_hakfan`，22 歲星二代對手）係另一人，直立微捲短髮＋
  黑皮褸白 Tee——高俊傑係中分微長曲髮＋紅皮褸黑 Tee。

### 驗收（收到 character 之後先做）

1. 下載 south.png，用系統 `python3`＋PIL 量高，對阿偉 v2 錨：**高 102px、頭頂 y13、腳底 y114**。
2. 目視對 brief：中分微長曲髮略遮半邊眼、紅皮褸黑 Tee、粗銀鏈、囂張神態。
3. 記低新 character id＋量度。唔啱唔入卡，寫入 NOTES 等拍板。

### 已經喺遊戲入面嘅高俊傑資產（唔使重做）

- `UI40_STAND` 有 `ko_chunkit` 企立 WebP（index.html L5911，內嵌 data URI）——對話／企立已有圖。
- 名→id 映射：`index.html` L27150 `"高俊傑":"ko_chunkit"`；L27179 `ko_chunkit: { artId:"char_ko", ... display:"高俊傑" }`。
- 佢**唔係**紅星：`POSTER59_STAR_IDS`（L32338）冇高俊傑；`LEADSTAR59` 全表冇一張通告以佢做主演；
  `AWARDS63_POOL`／`AWARDS63_TIER_WEIGHT` 亦冇佢。呢個係佢要行「特別名額」而唔係入池嘅原因。

### 驗收結果（2026-11-13 14:40，PASS，入卡）

- Character：`bbaa5bf2-a598-4863-ba5a-47cc7cc4fe03`，completed，128×128，8 方向；
  south.png 已下載存 `samples178/ko_chunkit_south.png`（6,731 bytes，SHA256
  `fc20c55bc818aa2f74c56b9fd0a647df16a8eda856fd7cee8c0ae872ceebce8f`）。
- PIL 量度 alpha bbox：`(40, 12, 87, 116)`——**高 104px、頭頂 y12、腳底 y115**
  （最後有像素行 y115；bbox 下界 exclusive 116）。對阿偉 v2 錨（高 102、頭頂 y13、腳底 y114）：
  高 ＋2px、頭頂 −1、腳底 ＋1，實質同一 framing，PASS。
- 目視對 brief（四項全部吻合，唔係張克凡）：中分微長曲髮略遮半邊眼（左幅垂低遮左眼上半）、
  鮮紅皮褸＋黑緊身 V 領 Tee、頸上有粗銀鏈、囂張神態（劍眉＋半瞇眼＋挑釁冷笑）。
  張克凡係直立微捲短髮＋黑皮褸白 Tee——呢隻紅褸黑 Tee，分得清。

## 2. 入池年份核實：1991 年起（1990 排除有設定理據）

結論：**1991 年起先入池**。設定話佢 1990 已經係對手——但係同級臨記對手，唔係提名級人物；
1990 入池會同設定打架；1991 夏 C12 係佢第一次企到同阿偉同一張枱爭頂級位置，係轉折點。

證據（全部有出處）：

- **1990 春 N3／C3（W8–12）**：三年版主幹 L33——茶水間情報「高仔搶鏡」，落旗
  `rival_gao_hard`／`rival_gao_endure`。對手關係 1990 春已成立。
- **WF4 A_ko 線 5 節點**（`wf4build86/rival_a.js`；index.html L40961 起同一內容已落地）：
  `A_ko_meet` 錄影廠走廊搶紙本通告、圍讀鬥節奏、台慶排舞室爭鏡位、台慶前夕爭刪環節——
  全部係**同級搶位**，唔係頒獎禮提名級交手。`A_ko_ending` 賀歲片開鏡，`CONTRA98_WHEN_FIX`
  定為 **1990冬**（index.html L31382）：「你個名而家唔使我讀，都有人識喇」——到 1990 冬
  先至開始有人識， rivalry 先至成熟（「值得企埋一齊做對手嘅人」）。
- **C10 台慶位 vs 陪伴（1990冬，W40–44）**：`story_detail_c1_to_c17.json` C10——台慶夜後台，
  高俊傑為爭取演出黃金時段位置同阿偉正面交鋒。1990 冬佢仲係爭緊**演出位置**，唔係攞獎。
- **C12 賀歲搶位 vs 關係危機（1991夏，W80–84）**：同一檔案 C12——「1991年夏，賀歲檔與台慶級
  位置開搶。高文瀚要阿偉連軸綵排守住位置，高俊傑亦在爭同一席」，地點係星河電視台高層會議室。
  呢個係佢第一次喺高層場合爭頂級位置——1991 起做提名對手先至講得通。
- **結局設計**（`linji-endings-design.md`）：`rival_gao_hard`／`endure` 只改結局段落入面佢出現嘅
  方式（對台／和解／餽情報回收，鏈 E），冇年份閘，唔同 1991 門檻衝突。
- **通告主演零紀錄**：全庫搜尋，冇一張通告以高俊傑做主演（`LEADSTAR59` 無佢；gigs JSON
  提佢嗰句只係「高俊傑那類人會搶前排」——synopsis 形容詞，唔係主演）。第一輪（真主演）永遠
  搵唔到佢，係特別名額存在嘅前提。
- 年份粒度：`awards63Fellows(ceremony, year)` 只食年份，唔食月份——門檻定喺年（1991 起），
  唔會細分到 1991 夏先開。1991 春廣告賞理論上佢「早咗半季」入池，係年粒度簡化，已記錄，
  唔另開月閘。

## 3. Code 閱讀（基底 main 9eea029，index.html 共 59,356 行）

- `awards63Fellows(ceremony, year)` — L46866 起。兩輪唔郁：
  第一輪真主演（`leadStar59Of`＋`POSTER59_STAR_IDS`，按片酬序、每星一部、冇 sprite 嘅主演
  如彭少祺唔攞）；第二輪 `AWARDS63_POOL`（L46781）加權抽（`AWARDS63_TIER_WEIGHT`＋
  `awards63SeededRng(awards63KeySeed([year, ceremonyId, medium]))`，v20a147）；上限 3 位
  fellows＋阿偉（`out.length >= 3` 封頂）。
- `AWARDS64_SPRITES` — L46738 起，34 張 Q 版 44×50（企姿 11＋捧杯 1＋行 A/B 22），
  base64 約 28KB（上限 130KB，見 test_awards63_static.py）。
- 舞台：`awards62PlayCeremony` — L46429 起 `loadSpr(f.starId)`／`_walkA`／`_walkB` 逐個
  fellow 通用載入，載唔到跌返剪影，唔穿崩。`slotCx`／`FLOOR` 等幾何 v177 改緊，**本票唔郁
  舞台幾何**，sprite 尺寸跟現行 44×50。
- 卡片：`awards62PlayCeremony` L46367–46369 — `cardsData` 用 `fellows.forEach` 通用 builder：
  `poster = f.poster || posterOf(f.gigId)`，有 poster 用 poster 圖，冇就 `.awd63-csscard`
  （大媒介圖標＋細字典禮名），卡底 `.t` 片名＋`.s` 星名。**決定：高俊傑跟同一條規則——
  有掛靠作品 poster 就用 poster，冇就 CSS 卡；唔用 fullbody 裁頭肩，唔用 Q 版放大，唔另起一套。**
  （佢雖然已有 `UI40_STAND` 企立圖，但卡片渲染從來唔食 fullbody，唔為佢破例。）
- 接線：`buildAwardResultPack` L45464 衍生 `fellows63`／`winner63`（nominated 嗰陣 `winner63 =
  fl63[0]`）；`awards63FellowsHtml` L46929 唱名；請柬／結果卡／獎項頁全部經 `fellows63`，
  新 fellow 自動跟到——唔使逐處改。
- 得主邊緣情況：現行規則 `winner63 = fellows[0]`（nominated）／gallery 照 `fellows[0]` 取。
  高俊傑排最後（append）或者取代最後一位（replace），正常唔會係 [0]；唯一例外係佢係唯一
  fellow 嗰陣（前兩輪零產出＋佢補位）——嗰陣佢照規則做得主，同任何 fellow 一樣，唔另設特例。

## 4. 實裝規格（草稿，等 character 驗收過先落手）

喺 `awards63Fellows` 兩輪之後加第三步「v20a178 同輩對手特別名額」：

1. 閘：`year >= 1991`，否則跳過。`out` 已有 `ko_chunkit` 就跳過（防重）。
2. Seeded 抽選：`awards63SeededRng(awards63KeySeed([year, ceremony.id, medium, "ko"].join("/")))`，
   `rng() < 0.5` 先入（草稿概率 0.5；落手嗰陣定實，測試掃得闊，0<p<1 都 PASS）。
   用 seeded，唔用裸 `Math.random()`（同第二輪同一規矩，結果可重現、存入 pack）。
3. 掛靠作品：搵一張冇主演嘅 cand（`!c.starId`）做佢嘅提名作品，攞 title／gigId／poster。
   - `out.length < 3` 且有未掛靠嘅冇主演 cand → append。
   - `out.length === 3` → 取代最後一位 `assigned:true`（第二輪兜底位）嘅 fellow，
     **繼承被取代者嘅 title／gigId／poster**（保證有作品名＋卡片圖，唔會撞名）。
     三位全部係第一輪真主演嗰陣唔入（唔逼走真主演）。
   - 冇啱嘅 cand 嗰陣唔入。
4. Entry：`{ starId:"ko_chunkit", star:"高俊傑", title, gigId, poster, assigned:true }`。
   `star` 要直接寫「高俊傑」——`awards63StarName("ko_chunkit")` 回 `""`（見 §1），而
   `POSTER59_STAR_IDS` **刻意唔加佢**（嗰個 map 係海報／主演邏輯，加咗會誤導 poster／lead 判定）。
5. 唔郁：`AWARDS63_POOL`、`AWARDS63_TIER_WEIGHT`、兩輪抽選、上限 3、SAVE key
   （`starVolunteer_map_v19w`）、softRev、產品 `?v=`；唔直改 content pack JSON。
6. Sprite：`AWARDS64_SPRITES` 加 3 條 key——`ko_chunkit`／`ko_chunkit_walkA`／
   `ko_chunkit_walkB`，44×50，**由新 character 衍生**（south 幀出發）。衍生方法等 character
   到先定：v64 嗰批係 `gen_chibi2.py` 開羅語法逐格繪製，唔係直接縮圖；由 character 衍生嗰陣
   要對齊現行 Q 版比例／線條，方法未定，唔喺度憑空寫死。

   **落地方案（2026-11-13，照現行 Q 版比例重繪，唔係 PIL 縮圖）**：
   對照 `samples178/ko_compare.png` 證實直接縮圖唔得——等比縮到 44×50 得 23px 闊
   （現行 34px），頭細身長腿長，同枱 11 張 Q 版唔係同一語言；拉闊到 34px 會壓扁變形。
   所以沿用 v20a64 `gen_chibi2.py` 模板（44×50、扁闊方頭 26 格≈52%、腳 8 格、1px
   深啡紫描邊、平塗），新畫 `p_ko`（生成器 `samples178/gen_ko_chibi.py`，import
   v64 模板函數）：中分微長曲髮（左幅垂到 y16 略遮左眼上半、右幅 y11、中間分界露額）、
   stern 劍眉＋narrow 半瞇眼＋不對稱挑釁冷笑、鮮紅皮褸（182,28,32）＋黑 V 領 Tee＋
   頸上一行粗銀鏈＋斜拉鏈銀點、叉腰企姿。走路幀沿用同一 `build()` 機制
   （walkA 上身沉 +1px＋左腳踏前、walkB 右腳踏前）。
   對照 `samples178/ko_q版_compare.png`：同 awei／luk／lok 並排，頭身比例／線條／
   描邊一致，紅褸＋銀鏈＋冷笑認得返係高俊傑。生成 PNG 存 `samples178/ko_chunkit*.png`
   （企姿 bbox (4,0,40,50) 36×50，對現行 34×50；walkA diff 426px／walkB 92px，
   同 awei 344／102 同一量級）；base64 已入 `AWARDS64_SPRITES`，共 37 張，
   註解數目 34→37 已更新。

## 5. 測試（已寫，未落實裝；反證已跑）

- `tests/test_awards178_logic.js`（node，抽 index 真函數 eval）：
  (1) 1990 四媒介×24 ceremony id＝96 組合零出現；(2) 1991／1992 同掃 192 組合有出有唔出；
  (3) 入池結構（starId／star／title／gigId／assigned）；(4) 上限 3＋minimal 場景核實第一輪
  真主演唔會俾佢逼走；(5) 唱名（真實入池樣本，唔用假 sample 頂）；(6) 池／權重唔郁＋
  `awards63StarName('ko_chunkit') === ''`。
- `tests/test_awards178_static.py`（python，find-based 切片，**冇寫死行號**，rebase 漂移唔使
  人手 resync）：v178 標記＋1991 閘＋ko＋星名在位；池／權重冇佢；封頂仲喺度；舞台＋卡片
  行通用路徑；SAVE key 不變；`POSTER59_STAR_IDS` 唔加佢。Sprite 三條 key 檢查留喺檔尾註解，
  等 sprite 落地先開。**已開返（見 §8）：企姿＋行幀＋齊 37 張三項全部 PASS——其後按用戶方向
  剝走（見 §10），而家 static178 係 13/13，唔再驗 sprite。**
- **反證（對而家未改嘅 index，＝pristine main 9eea029）**：
  - logic：`node tests/test_awards178_logic.js` → **4 FAIL**（1991 入池／結構／第一輪核實／唱名），
    其餘 4 項 PASS（1990 零出現／上限 3／池權重唔郁／星名查唔到），exit 1，**無 crash**。
  - static：`python3 tests/test_awards178_static.py` → **4 FAIL**（v178 標記／年閘／starId／星名），
    其餘 9 項 PASS（池權重唔郁／封頂／舞台＋卡片通用路徑／SAVE key／POSTER59 唔加佢），exit 1，無 crash。
  - 註：static (4) 通用路徑項喺 pristine PASS 係預期之內——佢哋證明現行路徑已覆蓋新 fellow，
    唔使新 code；logic (5) 唱名喺 pristine FAIL 係因為用真實入池樣本（零樣本即 FAIL）。

## 6. 待辦（收到 character 之後）——全部做完，見 §8

1. 驗收 character（§1）：south.png PIL 量度＋目視。唔過 → 寫 NOTES 停低等拍板。→ **PASS 入卡**
2. 過咗 → 按 §4 實裝入池＋衍生 3 張 sprite（方法嗰陣定）＋開返 static 檔尾 sprite 檢查。→ **做完**
3. 跑新測試要全 PASS；`qa131/run_suite.sh` 對 pristine 基線 A/B（12 項 pre-existing FAIL 以外零回歸；
   suite 數字會波動，判斷睇穩定 12 FAIL＋相關測試逐個直接覆驗）。→ **全 PASS，零回歸**
4. 實駕 932／700：播到有佢做 fellow 嗰場（唱名＋卡片＋舞台三樣齊），0 pageerror。
   播種存檔直接寫 localStorage（key `starVolunteer_map_v19w`，slot 1）；強制播行 live 模式，
   唔用 `?softPreview=1`（v165 B1 教訓）；Playwright venv `/home/hatch/pwenv49/bin/python`
   （冇 PIL，圖像處理用系統 `python3`）；本地鏡像＋`python3 -m http.server`。→ **2/2 PASS**
5. 補 NOTES（character id＋量度、測試＋實駕結果、殘留問題），commit，`git push origin v20a178`
   （origin 係常駐 clone 本地路徑，**唔推 GitHub**，落地由統籌做）。`git add` 新檔案要明確列出。→ **見 §8**

## 7. 殘留／注意

- v177 舞台加闊改緊舞台幾何：本票 sprite 尺寸跟現行 44×50，唔郁幾何；rebase 上 v177 嗰陣要
  對一次舞台 code 有冇改到 `loadSpr`／`slotCx`（測試用 find-based 切片，行號漂移唔影響）。
- 1991 春廣告賞「早半季」係年粒度簡化（見 §2），唔另開月閘。
- ~~衍生 sprite 方法未定（見 §4.6），等 character 到先決定，唔好喺未見圖之前寫死。~~
  已定：照 Q 版比例重繪（見 §4.6）。

## 8. 落地實裝＋驗證（2026-11-13 14:38–14:55 HKT）

### 8.1 實裝（index.html 淨 +25 行，git diff 26 insertions／1 deletion）

- `awards63Fellows` 兩輪之後加第三步「v20a178 同輩對手特別名額」（L46917 附近，+21 行）：
  閘 `year >= 1991`＋防重；seeded 抽選
  `awards63SeededRng(awards63KeySeed([year, ceremony.id, medium, "ko"].join("/")))`，
  `rng() < 0.5` 先入；掛靠未用過嘅冇主演 cand（按片酬序首張）；未滿 3 就 append，
  滿 3 就取代最後一位 `assigned:true` 嘅 fellow，繼承嗰個位嘅 title／gigId／poster；
  三位全部係第一輪真主演嗰陣唔入。Entry
  `{ starId:"ko_chunkit", star:"高俊傑", title, gigId, poster, assigned:true }`。
  **取代分支唔另要一張 free cand**——被取代者本身嗰張就係掛靠作品（佢嘅 gig 就係 cand）；
  「冇啱嘅 cand 嗰陣唔入」指 append 分支冇 free no-lead cand、或者滿 3 但最後一位唔係
  兜底位。呢個解讀同測試 minimal 場景一致（嗰場本來就有 free cand）。
- `AWARDS64_SPRITES` 加 ko 3 條 key（base64，+3 行）＋註解數目 34→37（+1 行）。
- 唔郁：`AWARDS63_POOL`、`AWARDS63_TIER_WEIGHT`、兩輪抽選、上限 3、SAVE key、softRev、
  產品 `?v=`、content pack JSON、`POSTER59_STAR_IDS`；卡片＋舞台行現行通用路徑。
- `node --check`：全檔 inline script PASS。

### 8.2 新測試全 PASS

- 反證重跑（接手第一步，對未改 index）：logic 4 FAIL／4 PASS、static 4 FAIL／9 PASS，
  exit 1，無 crash——同上一手 NOTES 一致，先信佢哋。
- 落地後：`tests/test_awards178_logic.js` **8/8 ALL PASS**
  （1990 零出現；1991+ 92/192 組合有佢；結構 92 個樣本齊；上限 3；第一輪 11 場核實唔逼走；
  唱名印得出；池／權重唔郁；星名查唔到）。
  `tests/test_awards178_static.py` **16/16 ALL PASS**（含開返嘅 sprite 三項：企姿／行幀／齊 37 張）。

### 8.3 全套 A/B：零回歸

- Pristine（HEAD index＋同一套測試，`~/workspace/linji-pristine178/`，用完即清）：
  **235 PASS／14 FAIL**（14＝12 pre-existing＋2 份新 178 反證 FAIL）。
- 工作版：**237 PASS／12 FAIL**；FAIL 清單同 pristine 嗰 12 項逐項相同
  （flash51／giglib36／pacing35／poster59／rumor49／slot50／soft_tip_111_restore／
  start53／weave43／weave44／weave49／wrap38——全部係 softRev 標記等舊問題，pristine 一樣 FAIL）。
- 初跑工作版係 232／17：多出 5 項全部係 v178 自身引起，已處理——
  (a) sprite 數目基線 34→37：`test_awards63_static.py`＋`test_awards64_chibi_static.py`
  各更新（企姿／行幀 key list 加 `ko_chunkit`，數目改 37；跟 v64 當年 12→34 同一做法）；
  (b) 釘行漂移：`test_tang171_static.py`／`test_tang173_static.py`／`test_travel114_static.py`
  （v178 淨 +25 行全部喺釘行之前），`qa178/resync178.py` difflib 對位核實——只得 3 個
  hunks（註解 +1／yip 行 replace 1→4／fellows +21），44 個釘行內容逐字相同，純漂移；
  總行數 59356→59381、openLoc DEF 53875→53900、WRAPPER 44250 唔郁（＜插入點）、
  COUNT 13／FREE 27 不變（＜46738 者 +0、其後者 +25）。之後 7 份逐個重跑全部 PASS，
  全套第二跑 237／12。
- 另記：`/tmp` 得 512M，做 pristine 全量 copy 嗰陣爆滿失敗；改用 `~/workspace/linji-pristine178/`
  （HEAD index＋現行 tests／qa131＋其餘 symlink），跑完已清走。

### 8.4 實駕：2/2 PASS（`qa178/drive178.py`，LIVE 模式，唔用 `?softPreview=1`）

- 場次：1991 星河台慶 `award_singho_tv`、nominated、seed 1991-10-20（fame 120／stage 60／
  acting 60）。第一個候選典禮即有佢——fellows 葉敏芝《渡輪燈火》／鍾楚凝《星光夜》／
  **高俊傑《潮汐家庭》**（gig_1989_tv_05，assigned:true，取代第二輪兜底位繼承作品）。
- ko_932（430×932）／ko_700（430×700）各 **11/11 項 PASS，0 pageerror**：
  新遊戲→pack 有佢→請柬→出席→舞台出現→唱名 caption「入圍名單 高俊傑：《潮汐家庭》」
  （t≈3.2–3.4s）→提名卡列有佢張卡→結果卡→舞台散場。典禮全長約 10.9s。
- 舞台 sprite 證據（唱名截圖 `qa178/shots/ko_names_430x932.png`／`ko_names_430x700.png`）：
  最右企位紅褸 Q 版人仔，同枱比例一致；皮褸平塗色 (182,28,32) 實測 932 嗰張 609 粒、
  700 嗰張 608 粒，全部聚喺最右企位（932：x296–340／y391–413；700：x296–340／y275–297），
  其他人／幕布區域 0 粒完全相等。
- 兩個 drive 教訓（已寫入 drive 註解）：(1) 遊戲成個 inline script 包喺 IIFE 入面，
  `AWARDS64_SPRITES` 喺 page.evaluate 讀唔到——sprite 檢查改用截圖像素數，唔用 DOM 讀 const。
  (2) Playwright venv 冇 PIL——像素分析經 `/usr/bin/python3`＋`qa178/ko_red.py` subprocess 做。
- 觀察（唔係問題）：兩次 run 嘅 pack 類別數唔同（932 嗰次 1 個類別「最受歡迎螢幕面孔」、
  700 嗰次 2 個類別，兩個類別 fellows 一樣），同一個 seed 下類別揀選有變數；高俊傑喺兩個
  run、全部類別都有，唔影響本票。卡列用 CSS 卡（呢三張掛靠作品冇 poster，行通用跌返規則，符合規格）。
- 播種：新遊戲 live＋in-page seed（S.dayIndex 等），冇用 `?softPreview=1`；localStorage
  SAVE key 未直接寫——seed 經 S，drive 唔使留 slot 1 存檔（NOTES §6 寫法係舊 drive 做法，
  今次跟 drive172 live new_game＋in-page seed，效果等同）。

### 8.5 Commit

- 分支 `v20a178`（基底 main 9eea029；main 而家仲係 7801a72，v175／v177 未落地，唔使 rebase）。
- Commit：`b0d921d`（v20a178，30 files，+2128／−35；另 NOTES 補 hash 一個細 commit 跟住）。
- `git push origin v20a178`（origin 係常駐 clone 本地路徑，唔推 GitHub；落地由統籌做）。

### 8.6 殘留

- v177 舞台加闊未落地：rebase 上 v177 嗰陣對一次 `loadSpr`／`slotCx`；本票 sprite 44×50 唔郁。
- 1991 春廣告賞「早半季」年粒度簡化（見 §2），唔另開月閘。
- 實駕觀察：同一 seed 下 pack 類別數 1 vs 2 有變數（見 §8.4），唔係本票範圍。
- `~/workspace/linji-pristine178/`（pristine A/B 對照）已清走；`/tmp/ko_probe.js`／
  `/tmp/inline178.js` 係 ephemeral，唔入 repo。

## 9. Rebase＋重驗紀錄（2026-11-13 15:00–15:30 HKT，rebase 工人）

### 9.1 Rebase：兩段式，基底最終 `a41b789`（零 conflict）

- 任務基底 main `4106b2f`（v179 code commit）。第一段 cherry-pick `b0d921d`＋`145526e`
  上 `4106b2f`：**零 conflict**，index.html 雙向 diff 乾淨——對 main 得 3 個 hunks
  （sprite 註解 +1／sprites +3 keys／fellows +21），對原 `b0d921d` 得 v177／v179
  嗰 3 個 hunks（prog71StubItems／fallback stage／ceremony），兩邊冇重疊改動。
- `git rebase origin/main` 本身兩次失敗（`pick b0d921d` 報「local changes would be
  overwritten」，工作樹明明乾淨；失敗後 todo 被 reschedule 出重複 pick，HEAD 停留
  `4106b2f`）：原因未查明，改用等效手動路徑——detached HEAD 上
  `git cherry-pick --no-commit b0d921d`＋`cherry-pick 145526e`，兩次都乾淨成功。
  教訓：呢個環境 `git rebase` sequencer 有誤判，之後 rebase 遇同類報錯可改行
  cherry-pick 等效路徑（唔好將 `rebase --continue` pipe 去 head，依舊禁）。
- 第二段：rebase 期間 main 郁咗——統籌落地 v179 NOTES commit `a41b789`
  （淨加 `NOTES_V20A179.md` 48 行，零 code 改動）。為跟「最新 main」，
  再 cherry-pick 兩 commits 上 `a41b789`，同樣零 conflict。
  最終分支：code commit `2d58c35`、NOTES commit `e80a465`，基底 `a41b789`。
  檔案總數不變：30 files，+2128／−35；index.html 59381 行（main 59356＋25）。

### 9.2 loadSpr／slotCx 對核（v177 新幾何＋v178 sprite）

- `FLOOR = 250`（v177，L46447）、`slotCx` won／nominated 4 slots
  62／162／262／362、gallery 82／162／262（L46448）全部在位。
- `loadSpr` 通用（L46438）：`fellows.forEach(f=>{ loadSpr(f.starId);
  loadSpr(f.starId + "_walkA"); loadSpr(f.starId + "_walkB"); })`——唔按 starId
  分流，`ko_chunkit` 照載。`AWARDS64_SPRITES` 三條 key 齊（企姿／walkA／walkB，
  44×50 PNG base64），共 37 張。`awards63Fellows` 第三步 L46920 在位。
- 唔使 resync：兩份新測試全部 find-based，行號漂移零影響；v178 自身 resync
  嗰 5 檔（awards63／awards64／tang171／tang173／travel114）喺新基底逐個重跑全部 PASS。
  `node --check` 抽 inline script PASS。

### 9.3 測試＋全套 A/B（新基底 `a41b789`）

- `tests/test_awards178_logic.js` **8/8 ALL PASS**；
  `tests/test_awards178_static.py` **16/16 ALL PASS**（含 sprite 三項）。
- Pristine（`a41b789` index＋同一套 tests，`~/workspace/linji-pristine178/`，
  其餘檔案 symlink，跑完已清走）：**233 PASS／19 FAIL**。
  19＝12 項穩定 pre-existing＋2 份 v178 反證 FAIL＋5 檔 v178 resync 反證 FAIL
  （awards63／awards64／tang171／tang173／travel114——佢哋喺 pristine 預期 FAIL，
  因為測試已按 v178 狀態更新）。
- 工作版：**240 PASS／12 FAIL**；FAIL 清單＝12 項穩定逐項相同
  （flash51／giglib36／pacing35／poster59／rumor49／slot50／soft_tip_111_restore／
  start53／weave43／weave44／weave49／wrap38）。差額 ＋7 正好係 2＋5，**零回歸**。
- 中途插曲（已解）：第一輪 pristine 跑出 149／103——對照目錄漏咗其餘檔案 symlink
  （測試讀 repo 內其他檔案），補返 symlink 後 233／19；另 `test_story179_static.py`
  喺 `4106b2f` 基底嗰陣兩邊都 FAIL，原因係 NOTES_V20A179.md 只喺 `a41b789`
  先有——rebase 上 `a41b789` 後工作版同 pristine 都 PASS，唔係回歸。
- 全套數字有波動（同一 pristine 目錄兩跑 232→233 係 story179 嗰項之差，唔係 flake），
  判斷以穩定 12 FAIL＋相關測試逐個覆驗為準（見上）。

### 9.4 實駕重跑：2/2 PASS（`qa178/drive178.py`，LIVE 模式，v177 新幾何）

- 場次（兩 viewport 同一場）：1991 星河台慶 `award_singho_tv`、nominated、
  seed 1991-10-20。fellows 葉敏芝《渡輪燈火》／鍾楚凝《星光夜》／
  **高俊傑《潮汐家庭》**（gig_1989_tv_05，assigned:true，取代第二輪兜底位繼承作品）。
- ko_932（430×932）／ko_700（430×700）各 **11/11 項 PASS，0 pageerror**：
  新遊戲→pack 有佢→請柬→出席→舞台出現→唱名 caption
  「入圍名單 高俊傑：《潮汐家庭》」（t≈3150／3266ms）→提名卡列有佢張卡→
  結果卡→舞台散場。典禮全長約 10.9s。
- 舞台 sprite 證據（唱名截圖）：皮褸平塗色 (182,28,32) 兩張都係 **607 粒**，
  全部聚喺最右企位——932：x333–378／y353–375；700：x333–378／y237–259。
  對舊幾何（932：y391–413）上移約 38px，吻合 v177 FLOOR 290→250（−40px），
  x 唔郁（最右 slot 362 企位不變）；證實 ko sprite 喺 v177 新幾何下照載、企位啱。
- 觀察（唔係問題）：932 今次 2 個類別、700 嗰次 1 個類別，同 §8.4 嗰次掉轉咗——
  同一 seed 下 pack 類別數 1 vs 2 有變數，舊觀察，唔係本票範圍。高俊傑兩個 run、
  全部類別都有。

### 9.5 提交

- 分支 `v20a178`（基底 main `a41b789`），commit `2d58c35`（code）＋`e80a465`（NOTES）。
- `git push origin v20a178 --force-with-lease`（origin 係常駐 clone 本地路徑，唔推 GitHub；
  落地由統籌做）。§8.5 嘅舊 commit hash（`b0d921d`／`145526e`）已被 rebase 取代，
  以本節為準。

## 10. 方向更正＋剝走 sprite 衍生（2026-11-13 15:11–15:40 HKT，收窄工人）

### 10.1 用戶方向更正（2026-11-13 15:11，親自話）

- 舞台上面啲人要**直接用 PixelLab character**，唔係由佢衍生一隻 Q 版出嚟。
- 本票 (e) sprite 衍生嗰步**停咗**——唔好做 Cairo Q 版衍生。v180 會另外開票做
  「舞台人物全部換做 PixelLab character 直接用」。
- 本票集中做返**入池邏輯（1991 年起特別名額）＋測試＋驗證**；高俊傑嘅舞台圖由
  v180 接手，唔使本票出。

### 10.2 剝走清單（喺分支上加新 commit，冇改寫舊 commit）

- `index.html`（59381→**59377**，即 main 59356＋21 行入池邏輯）：刪 `AWARDS64_SPRITES`
  嗰 3 條 `ko_chunkit`／`ko_chunkit_walkA`／`ko_chunkit_walkB` key（L46774–46776）
  ＋註解行「v20a178：加高俊傑 3 張…共 37 張」（L46737）。**入池邏輯一啲都冇郁**
  （`year >= 1991`、seeded 抽選、`rng() < 0.5`、取代最後一位第二輪兜底位繼承
  title／gigId／poster、唔逼走第一輪真主演、上限 3、`star:"高俊傑"`）；POOL／權重／
  SAVE key／`POSTER59_STAR_IDS` 唔郁。
- `tests/test_awards178_static.py`：刪檔尾 sprite 三項檢查（企姿／行幀／齊 37 張），
  檔頭註解改返方向更正；**13/13**。
- `tests/test_awards64_chibi_static.py`：sprite 總數 37→**34**（STARS 拎走 `ko_chunkit`，
  企姿標籤返返「阿偉＋捧杯＋10 星」）。
- `tests/test_awards63_static.py`（任務清單以外、但係同一批改動，唔跟手拎走會 FAIL）：
  SPR_KEYS 拎走 `ko_chunkit`，37→**34**。§8.3 (a) 嗰陣為容納 3 條新 key 改過嘅兩檔，
  而家成對還原。
- `tests/test_tang171_static.py`／`test_tang173_static.py`／`test_travel114_static.py`
  （任務清單以外、但係 −4 行漂移所必需）：總行數 59381→59377、openLoc DEF
  53900→**53896**；travel114 釘行＞46738 者逐項 −4（COUNT 5＋FREE 15 處，
  單次掃描 dict 查表，唔逐對 re.sub），＜46738 者唔郁，COUNT 13／FREE 27 不變，
  WRAPPER 44250 唔郁。順手修正 v178 resync 引入嘅歷史註解錯字（v172 行
  「DEF 53860→53900」改返「53860→53875」）。travel114 入面「頁內測試 code
  （57835）＋字串檢查（57877）」嗰句係舊版殘留註解（實測 range 而家係 59053–59188，
  TEST_START／TEST_END 係動態計，唔靠死行號），v178 嗰陣都冇郁過，本票唔郁佢。
- `samples178/gen_ko_chibi.py`＋衍生 PNG（`ko_chunkit.png`／`ko_chunkit_walkA.png`／
  `ko_chunkit_walkB.png`）＋對照圖（`ko_compare.png`／`ko_q版_compare.png`）：**刪除**
  （死 code，方向已廢棄）。**保留** `samples178/ko_chunkit_south.png`（用戶 character
  驗收證據，6,731 bytes，SHA256 `fc20c55b…`）＋§1 量度紀錄（高 104px、頭頂 y12、腳底 y115）。
- `tests/test_awards178_logic.js`：**唔使改**（只測入池邏輯，唔測 sprite）。
- `qa178/drive178.py`＋新增 `qa178/ko_sil.py`：驗紅褸（607 粒）嗰項改做驗證剪影
  fallback——`stage_no_ko_red_jacket`（紅褸 0 粒）＋`stage_shows_ko_silhouette`
  （剪影色 `#1d1832` ≥1000 粒、聚喺最右企位 x0≥300／x1≤415、闊高各 ≥40px）。
  `qa178/ko_red.py` 留低（用嚟證 0 粒）；`qa178/resync178.py` 留低（＋25 resync 歷史紀錄）。

### 10.3 重驗數字

- `node --check` 抽 inline script：**PASS**（2 個 script blocks）。
- 新測試：`tests/test_awards178_logic.js` **8/8 ALL PASS**；
  `tests/test_awards178_static.py` **13/13 ALL PASS**（扣起 sprite 3 項之後，
  同任務預期一致）。逐個覆驗：awards63 38/38、awards64-chibi 19/19、tang171 22/22、
  tang173 21/21、travel114 PASS。
- 全套 A/B（基底 main `a41b789`，常駐 clone HEAD，落地前核實過 main 冇再郁，唔使 rebase；
  本地 `main` 分支停留喺舊 `7801a72`，對照用 `origin/main`）：
  - 工作版：**240 PASS／12 FAIL**（FAIL 係 12 項穩定 pre-existing：
    flash51／giglib36／pacing35／poster59／rumor49／slot50／soft_tip_111_restore／
    start53／weave43／weave44／weave49／wrap38）。
  - Pristine（`a41b789` index＋同一套測試，`~/workspace/linji-pristine178/`，跑完已清走）：
    **235 PASS／17 FAIL**＝12 穩定＋2 份 v178 反證 FAIL（logic／static178，預期）＋
    3 檔 resync 反證 FAIL（tang171／tang173／travel114，佢哋斷言工作版行數，預期）。
    差額 ＋5 正好係 2＋3；awards63／awards64 喺 pristine 都 PASS（34 張基線已還原），
    **零回歸**。Suite 數字（240／12）同 §9.3 嗰次一樣，唔係波動假象。
  - Suite 紀錄：`qa178/suite_work_strip.txt`、`qa178/suite_pristine_strip.txt`。

### 10.4 實駕重跑：2/2 PASS（`qa178/drive178.py`，LIVE 模式，唔用 `?softPreview=1`）

- 場次（兩 viewport 同一場）：1991 星河台慶 `award_singho_tv`、nominated、
  seed 1991-10-20。fellows 葉敏芝《渡輪燈火》／鍾楚凝《星光夜》／
  **高俊傑《潮汐家庭》**（gig_1989_tv_05，assigned:true，取代第二輪兜底位繼承作品）——
  同 §8.4／§9.4 同一場。
- ko_932（430×932）／ko_700（430×700）各 **12/12 項 PASS，0 pageerror**：
  新遊戲→pack 有佢→請柬→出席→舞台出現→唱名 caption「入圍名單 高俊傑：《潮汐家庭》」
  （t≈3392／3485ms）→提名卡列有佢張卡→結果卡→舞台散場。典禮全長約 10.9s。
- **剪影 fallback（預期中間狀態，唔係 FAIL）**：唱名截圖 `qa178/shots/ko_names_*.png`
  入面紅褸色 (182,28,32) **0 粒**（舊版 607 粒）；剪影色 `#1d1832` 兩張都係
  **4056 粒**，聚喺最右企位——932：x323–387／y318–385；700：x323–387／y202–269
  （x 完全一樣，y 差 −116 係 viewport 高差，企位啱）。舊截圖實測 silPx = 0，
  證明呢隻色只屬於降級剪影。目視核實：最右企位一個深色剪影（頭＋身兩格），同枱
  其餘三人企位齊整，唔穿崩；唱名＋卡列齊晒。
- 觀察（唔係問題）：700 嗰次 2 個類別、932 嗰次 1 個類別，同一 seed 下 pack 類別數
  1 vs 2 有變數，舊觀察（§8.4／§9.4），唔係本票範圍。高俊傑兩個 run、全部類別都有。
- 殘留：§7「本票 sprite 44×50 唔郁」嗰項已失效（sprite 已剝走）；v180 接手舞台圖
  （全部換做 PixelLab character 直接用），到時剪影 fallback 斷言要改返做 character
  斷言，`ko_sil.py`／`stage_shows_ko_silhouette` 嗰陣退役。

### 10.5 提交

- 分支 `v20a178`（基底 `a41b789`，唔使 rebase），strip commit **`69f8f63`**（第二次 rebase 後由 `e366330` 取代，見 §11）。
- `git push origin v20a178 --force-with-lease`（origin 係常駐 clone 本地路徑，唔推 GitHub；
  落地由統籌做）。

## 11. 第二次 rebase＋重驗紀錄（2026-11-13 15:22–16:00 HKT，rebase 工人）

### 11.1 Rebase：基底最終 `91f264a`（v175），兩段式＋cherry-pick 等效路徑

- 任務基底 main `91f264a`（v175 code `4ef7405`＋NOTES；v175 index.html 淨 ＋78：
  CSS ＋10（L4954）／toast() ＋15（L33708）／prog71 helpers ＋51（L44129）／adopt ＋2
  （L44220），另改咗 tang171／tang173／travel114 等 7 份測試嘅 resync 數字）。
  v175 改動同 v178 入池邏輯（fellows 第三步，新行號 46994–47014）**零重疊**——
  v175 最後一個插入點 L44220 喺 v178 插入點（46815／46850／46993）之前成 2,500 行；
  `git diff main...v20a178`（rebase 前）30 files、+3539／−28。
- 第一段：`git rebase origin/main`，pick `2d58c35`——index.html 乾淨合併（+25 行）；
  預期內衝突三檔：`test_tang171_static.py`／`test_tang173_static.py`／
  `test_travel114_static.py`（v175 同 v178 各自 resync 過同一批斷言：總行數／DEF／
  COUNT／FREE）。解法：三檔先取 v175（ours）版為底，再用 `qa178/resync178b.py`
  difflib 對位重算（OLD＝`origin/main:index.html` 59434 行、NEW＝合併後 index 59459 行；
  淨 3 個 hunks：註解 insert 1／yip 行 replace 1→4／fellows insert 21；全部釘行內容逐字
  相同，純漂移）：總行數 59434→**59459**、DEF 53953→**53978**、WRAPPER 44328 唔郁；
  travel114 COUNT／FREE：＜46815 者 ＋0、＞46992 者 ＋25。三檔逐個重跑全部 PASS
  （tang171 22/22、tang173 21/21、travel114 PASS）後 `git add`＋
  `GIT_EDITOR=true git rebase --continue`（冇 pipe）——pick 1–3 成功
  （`0174c5a`／`29e0098`／`90de32e`）。
- 第二段 sequencer 誤判（同 §9.1 同一症狀）：pick `69f8f63`（strip）嗰陣報「local
  changes would be overwritten」（工作樹明明乾淨），rebase 停咗。跟 §9.1 前例：
  `git rebase --abort`（分支指針返返 `8c011e9`，但已 rebase 嘅三個 commits 仲喺
  object store），再 `git checkout 90de32e`（detached），`git cherry-pick --no-commit
  69f8f63`——除咗同一三檔之外全部乾淨合併（index.html strip −4 行、NOTES、drive、
  awards63／64 還原 34 張、6 個死檔刪除）；三檔再用 `qa178/resync178c.py` 重算
  （OLD＝HEAD index 59459、NEW＝strip 後 index 59455；淨 2 個 delete hunks：註解 −1／
  3 條 sprite key −3；全部釘行內容逐字相同，純漂移）：總行數 59459→**59455**、
  DEF 53978→**53974**、WRAPPER 44328 唔郁。三檔重跑全部 PASS 後 commit strip
  `e366330`（取代舊基底嘅 `69f8f63`），再 `git cherry-pick 8c011e9`（NOTES，乾淨）
  得 `bf27772`。教訓補充：解衝突嗰陣第一版 regex（`re.sub` 食 `<<<<<<<`／`=======`／
  `>>>>>>>`）靜默食咗三檔尾段（117→64／118→64／239→186 行）——已由 index `:2:`
  （ours）還原，再用逐行 parser 重做；以後解衝突標記一律用逐行掃描，唔用跨行 regex。

### 11.2 `ko_chunkit` 13 次核實（rebase 後 index.html，59455 行）

- 合共 **13 次**，全部有出處，**冇一條係殘留 sprite key**：
  原有引用 9 次——L5921 UI40_STAND 企立 WebP（data URI）；L26477 對話企位 gaze／asym
  （紅皮褸斜拉鏈）；L27016 身高比 1.00；L27160 名→id 映射；L27180 npc 映射；
  L27189 `artId:"char_ko"`／`portraitsKey:"npc_ko"`；L27229 反向映射；
  L53649 `CORE_SIL_FAR_IDS`；L53654 `distanceLook`（紅皮褸亂髮）。
  v178 入池邏輯 4 次——L46994 註解、L46998 年閘（`year >= 1991`＋防重）、L47006 append
  entry、L47010 replace entry。基底 `a41b789` 係 9 次，9＋4＝13 ✓。
- `AWARDS64_SPRITES` 區塊（L46816 起）grep `ko_chunkit` **0 次**——3 條 key
  （`ko_chunkit`／`ko_chunkit_walkA`／`ko_chunkit_walkB`）已清走；`v20a178` 全檔只出
  現 1 次（L46994 註解）。入池邏輯一字未郁（fellows 第三步 L46994–47014）。

### 11.3 測試＋全套 A/B（新基底 `91f264a`）

- `node --check` 抽 inline script：**PASS**（2 個 script blocks）。
- 新測試：`tests/test_awards178_logic.js` **8/8 ALL PASS**；
  `tests/test_awards178_static.py` **13/13 ALL PASS**（扣起 sprite 3 項之後）。
- 逐個覆驗：awards63 **39/39**、awards64-chibi **18/18**、tang171 **22/22**、
  tang173 **21/21**、travel114 **PASS**。
  更正：§10.3 寫嘅「awards63 38/38、awards64-chibi 19/19」係上一手點錯數——實測
  兩檔 `chk(` 呼叫分別係 40／19 次（含 `def chk` 本身一行），即 39／18 項；喺
  `a41b789` 基底跑同一版本一樣係 39／18，唔係 rebase 改動所致。全部 PASS，零 FAIL。
- 全套 A/B（`qa131/run_suite.sh`；pristine 用 **實體複製**成個工作副本再換入
  `91f264a` index.html，唔用 symlink——教訓：symlink 嘅 `tests/` 令 `HERE/../index.html`
  經 symlink 解返工作副本 index（`..` 喺目標目錄計），logic／travel114 會假 PASS；
  今次 pristine 嘅反證數字全部係實測）：
  - 工作版：**241 PASS／12 FAIL**（FAIL 係 12 項穩定 pre-existing：
    flash51／giglib36／pacing35／poster59／rumor49／slot50／soft_tip_111_restore／
    start53／weave43／weave44／weave49／wrap38）。
  - Pristine（`91f264a` index＋同一套測試，`~/workspace/linji-pristine178/`，跑完已清走）：
    **236 PASS／17 FAIL**＝12 穩定＋2 份 v178 反證 FAIL（logic 4 項／static178 4 項，
    逐項已核）＋3 檔 resync 反證 FAIL（tang171 3 項／tang173 3 項／travel114 16 項）。
    差額 ＋5 正好係 2＋3；awards63／awards64 喺 pristine 都 PASS（34 張基線已還原），
    **零回歸**。
  - Suite 紀錄：`qa178/suite_work_2ndrebase.txt`、`qa178/suite_pristine_2ndrebase.txt`。
  - v175 掂過嘅其餘測試（kwan151／tang152／text125／prog175／story179）喺工作版全套
    入面全部 PASS（唔喺 12 FAIL 清單），v175 改動對核完成。

### 11.4 實駕重跑：2/2 PASS（`qa178/drive178.py`，LIVE 模式，唔用 `?softPreview=1`）

- 場次（兩 viewport 同一場）：1991 星河台慶 `award_singho_tv`、nominated、
  seed 1991-10-20。fellows 葉敏芝《渡輪燈火》／鍾楚凝《星光夜》／
  **高俊傑《潮汐家庭》**（gig_1989_tv_05，assigned:true，取代第二輪兜底位繼承作品）——
  同 §8.4／§9.4／§10.4 同一場。
- ko_932（430×932）／ko_700（430×700）各 **12/12 項 PASS，0 pageerror**：
  新遊戲→pack 有佢→請柬→出席→舞台出現→唱名 caption「入圍名單 高俊傑：《潮汐家庭》」
  （t≈3430／3429ms）→提名卡列有佢張卡→結果卡→舞台散場。典禮全長約 11.0s／10.9s。
- **剪影 fallback（預期中間狀態，唔係 FAIL）**：唱名截圖 `qa178/shots/ko_names_*.png`
  入面紅褸色 (182,28,32) **0 粒**；剪影色 `#1d1832` 兩張都係 **4056 粒**，聚喺最右企位——
  932：x323–387／y318–385；700：x323–387／y202–269——同 §10.4 數字逐粒相同，企位啱。
- 觀察（唔係問題）：932 嗰次 1 個類別、700 嗰次 2 個類別，同一 seed 下 pack 類別數 1 vs 2
  有變數，舊觀察（§8.4／§9.4／§10.4），唔係本票範圍。高俊傑兩個 run、全部類別都有。

### 11.5 提交

- 分支 `v20a178`（基底 main `91f264a`），code commit `0174c5a`、NOTES `29e0098`／
  `90de32e`、strip commit **`e366330`**（取代舊基底嘅 `69f8f63`）、NOTES `bf27772`、
  本節 NOTES commit `a228e66`。
- `git push origin v20a178 --force-with-lease`（origin 係常駐 clone 本地路徑，唔推 GitHub；
  落地由統籌做）。§9.5／§10.5 嘅舊 commit hash（`2d58c35`／`e80a465`／`961943c`／
  `69f8f63`／`8c011e9`）已被 rebase 取代，以本節為準。
