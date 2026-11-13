# v170 Phase 1 調查報告 — 頒獎禮提名人卡片人像＋人物企位

- 調查分支：`v20a170`，HEAD `fc1a1aa`（main 當時最新，遊戲 `280af68`）；對照常駐 clone `~/workspace/linji-repo`（main）。
- 工作副本：`~/workspace/linji-work170/`；調查日期 2026-11-13；**只讀調查，零 code 改動、零生成、零 commit**。
- 觸發：用戶 2026-11-13 11:23 睇完 v168 review 截圖追加兩點：①其他提名人要用 Pixellab 生成 character，風格先統一（提名卡得阿偉有圖，其他三張係深色字卡）；②提名人物要由觀眾席移上舞台。
- 基準截圖 case（`~/workspace/linji-design-review-v168/`，`drive168.json`）：**`won_932`** — 典禮 `award_harbour_film`（影藝獎），**1991 年**，`bestOutcome: won`，`tier: nominee`，代表作《幻彩舞影》（`repGigId63: gig_1988_film_lion_autumn_high`），類別「年度票房話題綠葉」。同屆提名三人：**廖炳星《離岸的信》、陸柏言《半張船票》、魏詠男《離岸燈》**。截圖尺寸 430×932（`won_932`＝高 932；`won_700`＝430×700，闊度同為 430）。

## A. fellows 池（提名人係邊啲人）

### A1. 來源函數與兩輪機制

- 唯一來源：`awards63Fellows(ceremony, year)`，`index.html` L46656–46707。呼叫點：排程嗰陣 `buildAwardPack`（L45297–45302）計一次存入 pack（`c.fellows63 = fl63`，每類別共用同一份；`winner63 = fellows63[0]`，只限 nominated 類別），之後全程讀 pack，唔再重計。
- 上限 **3 位 fellows**（`out.length >= 3` 即停，L46674／L46690）。舞台 slots＝3 fellows＋阿偉＝**4 個**（won／nominated）；gallery（旁聽）無阿偉，**3 個**。卡列張數跟 slots 走：won／nominated 係 4 張卡（阿偉＋3 fellows），gallery 係 0 張卡（`cardsData` 只喺 `best !== "gallery"` 先起，L46173）。
- **第一輪（真主演，L46671–46680）**：候選＝嗰年＋嗰媒介（`ceremony.matchTypes`）嘅全部 gig（`awards63AllGigs`，L46625：`GIGS`＋`STORY_WIRE.gigsByYear`），排除玩家自己殺青過嘅（`S.wrapHistory`，L46663），按**片酬高→低**排序，每位星只取一部（`used[starId]`），主演經 `leadStar59Of(g)`＋`LEADSTAR59` 對照表（L32290 起）回填；有主演但冇像素 sprite 嘅星（註明例子：彭少祺，`POSTER59_STAR_IDS["彭少祺"] = null`）**直接唔要**（L46683–46684）。
- **第二輪（池兜底，L46685–46705）**：第一輪唔夠 3 位嗰陣，對冇主演數據嘅作品按媒介喺 `AWARDS63_POOL` 抽星。seed＝`[year, ceremonyId, medium].join("/")` 經 FNV-1a（`awards63KeySeed`，L46588）＋mulberry32（`awards63SeededRng`，L46594）——**同一場次可重現，唔用裸 `Math.random()`**。抽法 `awards63WeightedPick`（L46603）：未用過嘅池星按權重抽，唔重複，池抽乾返 `""`。
- **加權＝v147 同一套機制，已核實**：`AWARDS63_TIER_WEIGHT`（L46590–46593）＋註解（L46583–46587）寫明來源係 `PLAN_ERA_STAR_TARGETS_v1.md`「巔峰年」——巔峰 1990–92＝當紅頂級 **×3**（陸柏言 1990、蘇芷茵 1991、廖炳星 1992、駱家聲 1990、葉敏芝 1992）；1988–89＝上一代當紅 **×2**（麥震東 1988、齊鎮海 1988、鍾楚凝 1989）；1984–85＝過氣 **×1**（魏詠男 1985、顧明輝 1984）。池外星唔入池，唔使權重。分佈驗證見 `tests/test_awards63_logic.js` §(6)（L160–181）：2000 seeds，首抽頂級佔比 film 理論 0.64／均勻 0.50、tv 0.60／0.50、music 0.86／0.67、ad 0.60／0.40，誤差 ±0.06 內 PASS。

### A2. 全部可能人選（按媒介池＋權重）

`AWARDS63_POOL`（L46575–46580）＋`POSTER59_STAR_IDS`（L32284–32289，11 名，彭少祺 `null`）：

| 媒介 | 池（starId） | 權重 | 權重總和 | 首抽理論佔比 |
|---|---|---|---|---|
| film | luk_baakyin 陸柏言 ×3、liu_bingxing 廖炳星 ×3、mak_zhendong 麥震東 ×2、chai_zanhoi 齊鎮海 ×2、lok_gasing 駱家聲 ×3、ngai_wingnaam 魏詠男 ×1 | 3,3,2,2,3,1 | 14 | 頂級 21.4%／人，上一代 14.3%／人，過氣 7.1% |
| tv | chai_zanhoi 齊鎮海 ×2、yip_manji 葉敏芝 ×3、luk_baakyin 陸柏言 ×3、chung_choning 鍾楚凝 ×2 | 2,3,3,2 | 10 | 頂級 30%／人，上一代 20%／人 |
| music | lok_gasing 駱家聲 ×3、gu_mingfai 顧明輝 ×1、liu_bingxing 廖炳星 ×3 | 3,1,3 | 7 | 頂級 42.9%／人，過氣 14.3% |
| ad | so_jiyan 蘇芷茵 ×3、chung_choning 鍾楚凝 ×2、luk_baakyin 陸柏言 ×3、ngai_wingnaam 魏詠男 ×1、gu_mingfai 顧明輝 ×1 | 3,2,3,1,1 | 10 | 頂級 30%／人，上一代 20%，過氣 10%／人 |

- **出現條件**：池內星**無年份閘、無 unlock 條件**（awards code 內零年份檢查）。唯一出現條件係 (a) 第一輪：嗰年嗰媒介有佢做主演嘅 gig（1990 年先有，即 `LEADSTAR59` 覆蓋範圍）；或 (b) 第二輪：嗰年嗰媒介有冇主演數據嘅 gig 可供配對。**程天諾永不出現**（池內根本冇佢；`tests/test_awards63_logic.js` L4 註明「唔出程天諾（1990 零出場紅線，池內根本冇佢）」）。
- **任務附帶例子更正**：「程天諾 unlockYear 1992、鍾楚凝 1992 秋冬 p=0.25」係**巧遇系統**嘅條件，唔係頒獎禮閘——`~/workspace/linji-encounter-design.md` L78：程天諾 1992-01-01 前 `P(出)＝0`，1992 先真人登場；L79：鍾楚凝 1992 秋起 `P(出)` 降至 **25%**（移民潮暗線鏈 F 星級回音）。頒獎禮入面：程天諾任何年份都唔入池；鍾楚凝 tv／ad 池 ×2，全年無閘。
- **第二輪出現率（Monte Carlo，200,000 次，seed 20261113，假設 3 次兜底抽籤＝1991／1992 年情況）**：

| 媒介 | 各星「3 抽內至少出現一次」機率 |
|---|---|
| film | 陸柏言 61.2%、廖炳星 61.0%、駱家聲 61.0%、麥震東 45.7%、齊鎮海 45.9%、魏詠男 25.2% |
| tv | 葉敏芝 82.3%、陸柏言 82.3%、齊鎮海 67.7%、鍾楚凝 67.7% |
| music | **駱家聲／顧明輝／廖炳星全部 100%**（池得 3 人，抽 3 次，唔重複） |
| ad | 蘇芷茵 79.1%、陸柏言 79.3%、鍾楚凝 65.3%、魏詠男 38.3%、顧明輝 38.0% |

### A3. 作品名點嚟（唔係隨機配）

- 作品名＝**嗰部 gig 嘅作品名**，經 `work59WorkOf(h, g)`（L32537–32543）：優先 `workTitle` 欄，否則由 gig `title` 用 `/《(.+?)》/` 抽出書名號內文。**星同作品唔係隨機配對**：第一輪係 gig 自帶主演；第二輪係 gig（按片酬序）＋抽出嚟嘅星綁埋一齊，`assigned: true`（L46701），星名同作品名喺 fellows 記錄入面一齊存落 pack。
- won_932 三個配對全部係第二輪（見 A4），作品全部嚟自 `content/gigs_1989.json`（遊戲年 1991＝id 舊曆 1989＋2，`awards63GigYear` L46643／v20a66 規則）：

| fellow | 作品 | gigId | type | pay（片酬序） |
|---|---|---|---|---|
| 廖炳星 | 《離岸的信》 | gig_1989_film_09（「《離岸的信》歸僑青年阿信」） | 電影 | [28000, 48000]（1991 電影最高） |
| 陸柏言 | 《半張船票》 | gig_1989_film_04（「《半張船票》碼頭夜戲：猶豫的腳步」） | 電影 | [9000, 16000] |
| 魏詠男 | 《離岸燈》 | gig_1989_film_03（「《離岸燈》送機一場：不說出口的再見」） | 電影 | [8000, 15000] |

### A4. 點解廖炳星最常出現（數字拆解）

- **先講結論：佢唔係單一機制嘅第一名；「最常出現」係三層疊加＋fixture 效應，數字如下。**
- (1) **1990 年第一輪（有 LEADSTAR59 數據嗰年）**：`LEADSTAR59` 137 個 key **全部係 `gig_1988_*`**（遊戲年 1990；1991／1992 零覆蓋——所以 1991／1992 典禮**永遠行第二輪**，`tests/test_awards63_logic.js` L3／L103–107 已斷言：1991 fellows 全部 `assigned=true`）。電影類 LEADSTAR59 分佈：齊鎮海 8、陸柏言 8、**廖炳星 7**、麥震東 5、駱家聲 5、鍾楚凝 2、蘇芷茵 1、彭少祺 1（後者 null sprite，排除）。全媒介 LEADSTAR59 總數：陸柏言 33、齊鎮海 22、彭少祺 21（排除）、**廖炳星 18**、駱家聲 18、蘇芷茵 9、麥震東 6、鍾楚凝 6、葉敏芝 6、顧明輝 2。
- (2) **1990 年電影片酬序**：測試 mock（`tests/test_awards63_logic.js` L46–60，真實 LEADSTAR59 值）— 陸柏言《夜海鎗火》[40000,48000] 排第一，**廖炳星《詭校夜話》[35000,41900] 排第二**，麥震東第三；若玩家殺青過《夜海鎗火》（L101–103），`fl[0]` 即變廖炳星。**即係話：1990 電影典禮，廖炳星恆常係第 1–2 位對手。**
- (3) **1991／1992 年第二輪**：film 池首抽 21.4%、3 抽內出現 61.0%（同陸柏言／駱家聲並列最高一檔）；music 池 100% 出現（池得 3 人）。won_932 正正係呢個機制：最高片酬 gig《離岸的信》攞**第一次**加權抽籤，抽中 ×3 嘅廖炳星，於是佢成 `fellows[0]`——而 `fellows[0]` 同時係 gallery／nominated 類別嘅**預設得主**（`winner63 = fellows[0]`，L45300；`awards62CeremonyBeats` gallery 段 L46049：`得主＝fellows[0]`）。
- (4) **佢唔係唯一最高**：陸柏言喺 film／tv／ad 三池都係 ×3，1990 電影片酬序仲排佢前面；tv 池葉敏芝／陸柏言出現率（82.3%）高過佢。用戶印象中「最常出現」主要嚟自 1991 電影 fixture（佢係 `fellows[0]`＋預設得主）同 1990 年第 1–2 位排名——報告如實列出，唔誇大做「第一」。
- **廖炳星角色設定**：31 角色名冊（`PLAN_CHAR_LOOKS_REF_v1.md` §C，時代紅星 12 人之一，`era_star｜MVP`，約 30 歲，男）＋`PLAN_ERA_STAR_TARGETS_v1.md` §2：archetype「無厘頭喜劇笑匠，片場爆肚王，票房靈藥」，**巔峰年 1992**，MVP 子集四人之一（陸柏言、廖炳星、魏詠男、葉敏芝，`linji-art-assets-plan.md` L18）。樣貌 brief 全文見 §B5。

## B. 現有美術盤點（邊啲人有圖、邊啲要生成）

### B1. 全身圖 `assets/story/fullbody/`（現行對話舞台風格錨，乾淨二次元動畫風）

10 位池星**全部有 `_base.webp`**（基本款，neutral 表情），尺寸比例約 1:3.0–3.4（闊：高）：

| starId（顯示名） | 檔案數（含 base） | 表情檔（除 base 外） | `_base.webp` 尺寸 |
|---|---|---|---|
| luk_baakyin 陸柏言 | 5 | angry、sad、serious、smile | 443×1428 |
| liu_bingxing 廖炳星 | 7 | sad、serious、shy、smile、surprise、think（**欠 angry**） | 718×2476 |
| mak_zhendong 麥震東 | 5 | sad、serious、smile（欠 angry——v138 已判死 2 張等修復票，見 MEMORY） | 426×1408 |
| chai_zanhoi 齊鎮海 | 6 | angry、serious、shy、smile、think | 711×2394 |
| lok_gasing 駱家聲 | 6 | angry、serious、shy、smile、surprise | 576×1849 |
| ngai_wingnaam 魏詠男 | 7 | angry、sad、serious、smile、surprise、think | 453×1446 |
| yip_manji 葉敏芝 | 7 | angry、sad、serious、shy、smile、surprise | 904×2364 |
| gu_mingfai 顧明輝 | 7 | angry、sad、serious、shy、smile、think | 604×2604 |
| so_jiyan 蘇芷茵 | 6 | sad、serious、shy、smile、surprise | 830×2438 |
| chung_choning 鍾楚凝 | 6 | angry、sad、serious、smile、think | 825×2448 |

- 池星全身圖共 **62 檔**。v138 後全庫覆蓋 569／593＝95.9%（`NOTES_V20A138.md`）；卡片只需要 `_base`，所以**10 位全部齊 base**，表情缺口（廖炳星／麥震東欠 angry 等）唔影響卡片。
- 注意：v138 review A1 指出 6 張新表情衫／髮走樣（陸柏言 ×3、麥震東 ×2、鍾楚凝 angry）要重生——**base 檔唔喺嗰 6 張入面**，base 全部係 v106 定版批次。

### B2. Bust（頭肩圖）

- `assets/story/era_stars/*_bust_default.png`（864×1152，3:4，米白底）：**6 位有**——陸柏言、廖炳星、駱家聲、魏詠男、蘇芷茵、葉敏芝；其中陸柏言／廖炳星／魏詠男／蘇芷茵／葉敏芝另有 `_bust_frown.png`／`_bust_smile.png`（駱家聲得 default 一張）。
- **4 位冇 bust**：齊鎮海、鍾楚凝、顧明輝、麥震東（得 `*_stand_default.png` 舊企立圖，864×1152，v105 批次，現行只做 onerror 後備——`NOTES_V20A109_BUST.md` L46）。
- 風格核實（目視 `liu_bingxing_bust_default.png`）：乾淨二次元動畫風、米白底、花恤衫、挑眉壞笑、頭微傾——**同 brief 同 fullbody 同一風格家族**，唔係舊錯風。但「每張 bust 嘅面同對應 fullbody base 係咪同一張面」**未逐張像素核實**（Phase 2 樣本對照要做；v138 A1 嘅衫／髮走樣教訓正正係呢類問題）。
- v109 新 bust（240×312 WebP q80、米白底 `#F2EBD8`，由 fullbody 裁出）只覆蓋 7 個 PORTRAITS key（阿偉＋何生／張子駿／周采兒／高俊傑／林曉晴／Vera），原檔留喺 `qa109b/busts/`、值 inline 入 `PORTRAITS`，**唔包括任何 era 星**——era 星 bust 唔行呢條路徑。
- 舞台 Q 版 sprite：`AWARDS64_SPRITES`（`index.html` L46529 起，Q 版 44×50，`gen_chibi2.py` 逐格繪製，34 張：企姿 12＋行 A/B 22）——**10 位池星全部有企姿＋walkA／walkB**，另加 `awei`／`awei_hold`／`awei_walkA`／`awei_walkB`。**舞台人物唔使生成**；要生成嘅只係卡片人像。另外阿偉燕尾服 `assets/story/awards/awei_tuxedo.png`（128×128，Pixellab state `7577440c-…`，見 L46517–46527）係贏分支 reveal／glamour 專用，唔係卡片圖。

### B3. 提名卡而家嘅設計（函數＋CSS＋尺寸）

- 渲染點：`awards62PlayCeremony`（L46141 起）內 L46171–46181。`cardsData`：阿偉一張（`me: true`，poster＝`posterOf(pack.repGigId63)`）＋每位 fellow 一張（poster＝`f.poster || posterOf(f.gigId)`，即係該 fellow 作品嘅**作品海報**，唔係人像）。`poster59Path` 只覆蓋十部試點作品；冇海報就跌入 `.awd63-csscard`。
- 卡片 HTML（L46176–46179）：`<div class="awd63-card[ me]">` ＋ media（`<img>` 海報 或 `<div class="awd63-csscard">《作品名》</div>`）＋ `<div class="t">《作品名》</div>` ＋ `<div class="s">人名</div>`。
- 點解深色字卡：`.awd63-csscard`（L797）本身就係深紫漸變（`linear-gradient(160deg,#3a2a4a,#241736)`）＋金字 13px＋`#8a6d2f` 邊框——係「無圖作品」嘅降級設計，唔係 bug。won_932 三張 fellow 卡全部無 poster（《離岸的信》《半張船票》《離岸燈》三部都唔係 poster59 十部試點），所以三張都係深色字卡；阿偉卡有《幻彩舞影》海報（`poster-1988_film_lion_autumn_high.webp`，600×627）。
- 尺寸（CSS L788–797＋實測 `won_932_beat_reveal.png`）：`.awd63-card` **寬 88px**、padding 5px、gap 8px、`.awd63-cards` margin-top 10px；media 區 `aspect-ratio: 2/3`（即 **78×117px**）＋ `.t` 高 30px（11px 字，兩行）＋ `.s` 高 15px（10px 字）＋上下 padding 10px → **成張卡約 88×172px**（實測：卡頂 y≈448、卡底 y≈617–620 @932 viewport）。4 張卡總闊 4×88＋3×8＝376px，frame 闊 412.8px（430 viewport）→ 置中，x≈27–403。
- 顯示時機：`syncCards`（L46339–46346）——names／suspense／reveal／comfort 期間 `.on`，names 期間逐張延遲 `200 + i*380ms` 出現；`syncGlamour`（L46347–46350，v168 C1）——glamour 期間 `visibility:hidden` 留位隱藏，下一 beat 恢復。
- **人像應該放邊**：media 區（78×117，2:3）係唯一放得落人像嘅位，有兩個做法（設計決定，見 §B4）：(i) 人像**取代**作品海報／csscard（卡面變成人像＋片名＋人名，作品海報唔再出現）；(ii) 人像**加喺** media 區以外（要改卡結構／尺寸，卡高會變）。bust（864×1152，3:4）入 2:3 框用 `object-fit: cover` 會裁走上下約 11%；fullbody 裁頭肩（v109 同款做法：取全身圖頂部約 30% 高度做 240×312）比例上更啱，但要逐張定裁切框（每人體型／頭位唔同，見 B1 尺寸差異：由 426×1408 至 904×2364）。

### B4. 生成清單（結論）

| 類別 | 人選 | 依據 |
|---|---|---|
| **用現成 bust（零生成，Phase 2 樣本對照面容先用）** | 陸柏言、廖炳星、魏詠男、蘇芷茵、駱家聲、葉敏芝 | `assets/story/era_stars/<id>_bust_default.png`，864×1152，風格同 fullbody 同族 |
| **冇 bust，要補（零生成方案：由 fullbody `_base.webp` 裁頭肩，v109 同款）** | 齊鎮海、鍾楚凝、顧明輝、麥震東 | 得舊 `*_stand_default.png`（v105，後備用）；fullbody base 齊晒 |
| **若用戶堅持「Pixellab 生成 character」做卡片人像** | 10 位池星全部（＋阿偉卡去留要拍板） | 見下段風格提醒 |
| **唔使生成** | 全部 10 位嘅舞台 Q 版 sprite（AWARDS64 齊晒企姿＋行幀）；阿偉（已有 Pixellab character v2＋tuxedo） | — |

- **風格提醒（請統籌／用戶拍板，唔係工人決定）**：用戶原話「用 Pixellab 生成 character，風格先統一」。現況有**三種風格並存**：(a) 阿偉卡＝動畫風作品海報（唔係 Pixellab）；(b) 現成 bust／fullbody＝乾淨二次元動畫風（風格錨）；(c) Pixellab character＝像素風（阿偉 v2 character 128×128、tuxedo PNG）。如果 fellow 卡用 (c) 像素人像、阿偉卡留 (a) 動畫海報，**風格仍然唔統一**——要統一有三條路：(1) 四張卡全部用 (b) 現成 bust／fullbody 裁圖（零生成，最快，同主線舞台同一風格）；(2) 四張卡全部用 (c) Pixellab 像素人像（阿偉卡都要換，佢已有 v2 character 可 export；fellow 要新開 10 個 character）；(3) fellow 卡用 (b)、阿偉卡照舊（接受海報 vs 人像唔同類）。**工人建議先畀用戶睇 (1) 嘅樣本（廖炳星 bust 已有，直接上卡睇效果）再決定係咪行 (2)。**
- Pixellab character 成本未明：`create-character-v3` API 未試過（CONNECTOR.md 註明 untested）；阿偉 v2 character 係 2026-11-12 喺網站手動開（id `49907fa9-077f-4f59-aaba-45d3a06958fb`，128×128，8 方向）。若行 (2)，每位星一個 character，成本要 Phase 2 先試一個再報（參考：1-direction object 10 次／個，見 §E）。

### B5. 廖炳星樣貌 brief 全文（工人生成嗰陣用；prompt 永禁真人姓名）

來源：`~/workspace/user/files/PLAN_CHAR_LOOKS_REF_v1.md` §C 表格，`liu_bingxing` 行（L79），**逐字抄錄**：

> | liu_bingxing | 廖炳星 | era_star｜MVP | 約 30 | 男 | 面型偏瘦，顴骨突出，眼神精靈帶點市井狡黠，嘴角天生微翹，笑起來有誇張的動態感。 | 花恤衫配寬鬆西褲，或復古格仔衫配背帶，帶點不羈與隨性。 | Bust shot；挑眉壞笑，眼神帶點玩世不恭，頭部微傾。 | 周星馳／吳孟達 | 取年輕笑匠的無厘頭與機靈氣質，表情可略帶誇張但唔好抄招牌動作；禁一比一肖像抄臉。 |

- 對照（`~/workspace/user/files/PLAN_ERA_STAR_TARGETS_v1.md` §2）：archetype「無厘頭喜劇笑匠，片場爆肚王，票房靈藥」；**巔峰年 1992**；MVP 子集；玩家點識：片場梳化區／茶餐廳 `cafe_cha` 度橋。
- **禁令**：「靈感參考對象（DEV only；真名）」欄嘅真人姓名（周星馳／吳孟達）**絕對唔可以入生成 prompt**，亦唔可以出玩家面（玩家面永禁真藝名，見 MEMORY）。Prompt 只可以用左邊各欄：面型偏瘦、顴骨突出、眼神精靈帶點市井狡黠、嘴角天生微翹、挑眉壞笑、頭部微傾、花恤衫配寬鬆西褲（或復古格仔衫配背帶）、不羈隨性、乾淨二次元動畫風（風格錨 `~/workspace/linji-native-design/style-anchor-awei-anime.jpg`）。
- **brief 檔 id 錯字警告**：同一表格有 4 個 id 同 live 唔符，Phase 2 生成／搵檔**唔好跟 brief 檔 id**，跟 live id（`POSTER59_STAR_IDS`／fullbody 檔名）：`mak_jandung`→live `mak_zhendong`（麥震東）、`chai_janhoi`→live `chai_zanhoi`（齊鎮海）、`ching_tinok`→live `ching_tinlok`（程天諾）、`pang_siugei`→live `pang_siuki`（彭兆基／彭少祺）。廖炳星 `liu_bingxing` 本人無錯。

## C. 舞台幾何（人物企位點計）

### C1. 會場底圖入面邊度係舞台、邊度係觀眾席

底圖：`assets/story/awards/bg_awards_ballroom.jpg`，**424×240**（39,211 bytes，v160 M1 接入，參照相係港島香格里拉大禮堂實景，見 `NOTES_V20A160_M1.md`）。系統 python3＋PIL 量度（逐行／逐區 RGB 取樣＋目視核對原圖）：

| 區域（canvas 座標，424×240） | y 範圍 | 特徵（量度值） |
|---|---|---|
| 天花＋水晶吊燈 | y 0–62 | 明亮暖色，平均 RGB 約 (190–250, 150–250, 100–240) |
| 紅幕布（舞台背景） | **y 64–155** | 深紅，中央條帶 RGB 約 (150, 17, 17)；幕布頂 y≈64、底 y≈155 |
| **舞台頂面線（人物腳應該企嘅線）** | **y ≈ 155–156** | y156 中央區深色像素由 ~40/146 躍升至 131/146（平台頂邊）；y158–160 金色飾邊（gold 像素 130／73） |
| 舞台正面（深木＋金邊） | y 162–179 | 深色木面板（dark 像素 ~50/146），中央紅地毯未到 |
| 紅地毯（觀眾席地面，中央） | y ≈ 180–240 | 紅，RGB 約 (200, 70–110, 55–85) |
| 觀眾白椅（左右兩側） | y ≈ 165–230 | 椅背亮白，RGB 約 (220–235, 205–225, 165–195)；椅頂 y≈165，椅面（座位）約 y≈190–200 |

- 講台（lectern）：中央 x≈205–220、y≈135–156，企喺舞台上面、幕布前面。企位修正要留意：得主行前嗰陣唔好撞正講台（見 C3）。
- **結論：舞台平台頂面係一條線 y≈155；家下人物腳底 y＝194，低過舞台頂 39px，企咗喺紅地毯＋白椅之間（椅面高度），即係觀眾席——用戶講嘅完全啱，數字上係 39 canvas px。**

### C2. canvas 喺畫面入面嘅位置／尺寸（兩個 viewport，實測截圖）

- CSS：`.awd62-stage`（L779）`position:fixed; inset:0`  flex 置中；`.awd62-frame`（L780）`width: min(96vw, 760px)`；`canvas.awd62-canvas`（L781）`width:100%; height:auto`，backing 424×240。兩個 review viewport 闊度都係 **430**，所以 canvas 顯示尺寸兩個 viewport 相同：**412.8×233.5px**，縮放比 **0.974**（顯示 px／canvas px）。闊過 792px 嘅 viewport frame 先會封頂 760px，嗰陣 canvas 760×430、縮放 1.79（未實測，純計數）。
- 實測（`won_932_beat_reveal.png`／`won_700_beat_names.png`，金框＋深色邊框行定位）：

| viewport | canvas 內容頂 y | canvas 內容底 y | FLOOR 194 顯示 y | 舞台頂線 y155 顯示 y | 腳底低過舞台頂 |
|---|---|---|---|---|---|
| 430×932（won_932） | ≈196 | ≈432 | ≈385 | ≈347 | **38 顯示 px**（39 canvas px） |
| 430×700（won_700） | ≈80 | ≈316 | ≈269 | ≈231 | **38 顯示 px**（39 canvas px） |

- 對照量度：reveal beat 四個人物實測——fellow 頭頂 y≈337–344、腳底 y≈384（FLOOR 194）；阿偉（燕尾服，行前）腳底 y≈391（FLOOR＋7＝201）；椅頂顯示 y≈357、椅背延至 y≈420。即係話：**人物成身企喺椅背前面，腳底同椅面差唔多高**，同用戶描述逐字吻合。
- 後備舞台（`awards62FallbackStage`，L46013–46023，底圖載唔到先用）：平台頂畫喺 `H-52＝188`（金線 `H-56＝184`），FLOOR 194 同樣係企平台正面前面 6px——即使底圖失效，人物都唔係企台面。企位修正（FLOOR→155）對後備舞台同樣適用（平台頂 188 vs 腳 155 會變成企平台頂上面 33px——**後備舞台要一併改**，將平台頂畫高到 y≈150 附近，否則修正後人物會浮喺後備舞台上面；屬同一個改動，唔係另一票）。

### C3. 人物企位點樣計（函數／CSS／數字）

- 全部 canvas 人物由 `awards62PlayCeremony`（L46141 起）內聯繪圖，**冇 CSS 定位人物**（人物全部係 canvas `drawImage`，卡片先係 DOM）。
- `FLOOR = 194`（L46247，單一常數，全部 beat 共用）。`slotCx(i) = 202 + (i - (slots.length - 1) / 2) * 72`（L46248）。
  - **4 slots**（won／nominated：阿偉＋3 fellows，阿偉插喺 index 1，L46164）：cx＝**94、166、238、310**（阿偉 166；fellows 94／238／310）。
  - **3 slots**（gallery：3 fellows，無阿偉）：cx＝**130、202、274**。
- `drawFigure(s, i, o)`（L46286–46306）：`cx`（預設 slotCx）、`dispH`（fellow **48**、player **50**、燕尾服 **64**）、`fy = FLOOR + (o.y || 0)`、腳底對齊 `fy`、影子 `fillRect(cx - dispH*0.20, fy-3, dispH*0.40, 4)`。`drawTuxedo`（L46278–46284）：128px 原圖人物佔框 x42–87／y13–115，腳底喺原圖 y115，`dispH 64` 時人物實高 ≈51px。
- 入場：`entryPlan`（L46250–46263）——左右兩流，`from = -30`（左）／`454`（右），速度 **0.16px/ms**，逐個延遲 `rank*380ms`，walkA／walkB 每 tick 交替；到埗切企姿。最遠路程約 124–144px → 約 775–900ms＋延遲，喺 enter beat 1750ms 內行完。
- 揭曉行前：`fwd64`（L46412–46416）——`x` 向中心 212 移近 **22%**，`y +7`（腳底 194→**201**），前 500ms 行 walk 幀，企定切捧杯＋獎盃 glyph（`drawTrophyGlyph`，L46319–46325）。行前後 x：94→120、166→176（阿偉）、238→232、310→288——**冇人撞講台（x 205–220）**，修正後要重驗呢點（腳底改 155 之後，行前 y 係 162，講台 y135–156 仍然喺人物身後偏上，唔會遮腳）。
- 光池 `lightPool`（L46308–46313）：闊 62–72px、高 66px（`FLOOR-66` 至 `FLOOR`），跟住得主移。
- **walkup 阿偉路徑（更正一個誤會）**：walkup beat **冇 canvas 路徑**。`walkup` beat 嘅 canvas 只係壓暗 0.45（L46464–46469）；阿偉由觀眾席行上台係 **DOM 層 GIF overlay** `.awd62-walkup160`（L802–806，`assets/fx/awd_walkup_m4.gif`，144×144、9 幀，顯示闊 `min(72vw,300px)`＝300px @430 viewport，`image-rendering: pixelated`，置中覆蓋成個 frame）。行上台嘅路徑**焗死喺 GIF 入面**，code 改唔到佢嘅起點／終點；v170 郁唔到 walkup beat 嘅人物路徑（只可以成張 GIF 換走／改大細／改位置）。`syncWalkup`（L46351–46354）只係開／熄呢層。
- **glamour 阿偉企位**：只畫阿偉一人（L46457–46461），`slotCx(playerSlot)`＝166、`FLOOR` 194、`tuxedo: true, dispH: 64, hold: true, alpha: 0.9`——**同樣企喺觀眾席高度**，唔係舞台上面；右邊 44% 係 DOM 海報 panel（v166），左邊透明見到燕尾服。修正 FLOOR 會一併郁埋佢。

### C4. 各 beat 人物位置表（canvas 座標；FLOOR 現值 194，舞台頂 155）

`awards62CeremonyBeats`（L46017–46100）＋`draw()`（L46356–46478）。ms 係每 beat 長度。

| beat | ms | 適用 | 人物位置（canvas） | 要唔要郁（FLOOR 194→~155） |
|---|---|---|---|---|
| open | 1200 | 全部 | 無人物（空台＋漸光，L46365–46370） | 唔郁 |
| pan | 2000 | gallery | 3 fellows 企定，slotCx，FLOOR，alpha 0.95（L46372–46375） | **要郁**（跟 FLOOR） |
| enter | 1750 | won／nominated | 4 人由 x -30／454 行入 slotCx，FLOOR，walkA／B（L46377–46386） | **要郁**（行入嗰陣已經係新 FLOOR；留意入場由兩側「翼」入——新 FLOOR 155 嗰陣，入場線會貼住幕布底邊行，唔再穿過椅區，視覺上更似由側台入，要實駕核實） |
| names | 2400 | 全部 | 全部企定 slotCx，FLOOR，alpha 1＋白閃點 y150–230（L46388–46396） | **要郁** |
| suspense | 1400 | 全部 | 全部企定 slotCx，FLOOR；逐個打光（lightPool），其餘 alpha 0.45（L46398–46406） | **要郁** |
| reveal | 2100 | 全部 | 得主行前（x→中心 22%，**y＋7→腳 201**，捧杯＋獎盃 glyph）；其餘 alpha 0.6–0.7；won 另加彩紙 46 粒（L46408–46443） | **要郁**（行前腳 201→~162；獎盃 glyph 頂 y＝FLOOR＋y－64／－26，要跟住郁） |
| comfort | 2600 | nominated | 全部企定 slotCx，FLOOR；阿偉 alpha 1、得主 0.85、其餘 0.7（L46445–46453） | **要郁** |
| walkup | 2200 | won | canvas 無人物（壓暗）；DOM GIF overlay 做主角（L46464–46469） | **唔郁**（GIF 焗死；見 C3） |
| glamour | 1800 | won＋有海報 | 只畫阿偉，slotCx 166，FLOOR，燕尾服 dispH 64（L46457–46461）；fellows 唔畫 | **要郁**（跟 FLOOR；海報 panel 唔郁） |
| out | 500 | 全部 | 唔重畫人物，上一幀殘影＋漸暗 overlay（L46470–46473） | 唔郁（跟上一 beat） |

- **修正核心就係一行**：`FLOOR = 194` → **≈155**（舞台頂線 y155–156；建議值 154–156，實作嗰陣用截圖微調 ±2px）。全部企位 beat（pan／enter／names／suspense／reveal／comfort／glamour）跟住同一個常數郁，唔使逐 beat 改。附帶要跟住郁嘅只有三樣：(i) reveal 行前 `y +7`（腳 162，合理，唔使改數字）；(ii) `lightPool`（跟 FLOOR，自動）；(iii) `awards62FallbackStage` 平台頂（188→約 150，見 C2）。`slotCx` x 值、dispH、入場速度／延遲全部唔使郁。
- **企舞台上面之後嘅比例檢查**：腳 155 時，fellow 頭頂 y≈107（48px）、阿偉頭頂 y≈105（50px）、燕尾服人物頭頂 y≈104（實高 51px）——三者全部喺幕布範圍（y64–155）前面，唔會頂穿天花，唔會遮水晶燈。講台（x205–220）喺 4-slot 中央偏右，人物 x 94／166／238／310 無一正對講台；gallery 3-slot 中央位 x202 正對講台——gallery 嗰位 fellow（fellows[1]）企舞台上面嗰陣會企喺講台前面，腳 y155、講台 y135–156——**講台會俾佢遮住一半**，係可接受（人物企台前本來就遮講台）定要將中央 slot 移開，Phase 2 實駕嗰陣睇。
- **唔好郁嘅位**：卡片列（DOM，喺 canvas 下面，唔受 FLOOR 影響）、字幕框、跳過掣、walkup GIF、glamour panel。

## D. v149 兼容

### D1. v149 工作副本現況（查核日 2026-11-13）

- 工作副本 `~/workspace/linji-work149/`，分支 `v20a149`，HEAD `da90957`（v146 NOTES）。**未落地，有未 commit 改動**：`M index.html`、`M tests/test_text125_static.py`、`M tests/test_travel114_static.py`、`?? assets/fx/awd_confetti_m5.gif`、`?? qa149/`（測試 `qa149/test_awards149.js`＋drive＋shots）。
- **分支嚴重滯後**：base 只包到 v147（main `a3a0ac1`），**未含 v148／v150–v168**——即係未含 v160（M1 會場底圖、M4 walkup GIF、M6 燕尾服、M9 音效）、v161、v164、v166（glamour 右邊 44% panel）、v167、v168（glamour 期間隱藏卡列）。v149 落地嗰陣一定要 rebase 上當時 main，rebase 會掂返 v170 掂緊嘅同一啲位（見 D3）。
- v149 範圍（據 `qa149/test_awards149.js` 註解＋diff）：修 v147 review B1（舞台放大＋觀眾席／暗景底＋揭曉接 M5 彩紙）＋B2（報紙＋結果卡講賽果）＋B3（comfort 海報卡片名重複＋紫 panel 冇圖）＋B4（700 報紙 modal 尾句俾掣遮）。B2／B3／B4 唔掂舞台幾何，以下只列幾何相關改動。

### D2. v149 改咗邊啲舞台幾何（diff vs HEAD `da90957`，`git diff index.html`）

| 項 | 改動 | 位置 |
|---|---|---|
| 舞台佈局改直向 flex | `.awd62-stage` 加 `flex-direction:column`；`.awd62-frame` 加 `flex:none` | CSS L779–780 附近（hunk `@@ -779,7 +797,11 @@`） |
| 上下觀眾席帶（新） | `.awd62-aud149` top／bot 兩條（`flex:1 1 0; min-height:22px; width:100%`；徑向漸變畫剪影人頭，頂帶向下、底帶 `scaleY(-1)` 反轉），吸走上下剩餘空間，舞台唔再留大片純黑空帶 | CSS 新段＋`stage.innerHTML`（hunk `@@ -46191,13 +46228,19 @@`） |
| canvas backing 加大 | `<canvas width="424" height="240">` → **`width="636" height="360"`**，另包 `<div class="awd62-canvaswrap">`；`draw()` 入口加 `ctx.setTransform(1.5, 0, 0, 1.5, 0, 0)`——**邏輯座標維持 424×240** | `stage.innerHTML`＋`draw()`（hunk `@@ -46330,6 +46379,9 @@`）；註解寫明「FLOOR／slotCx／confetti／fallback 舞台全部照舊」 |
| M5 彩紙 GIF 疊加（新） | `.awd62-m5fx149` ×2（第二張 `scaleX(-1)`＋opacity .85，`z-index:2`，`assets/fx/awd_confetti_m5.gif?v=20a149`），`syncConfetti149` 喺 reveal／comfort／out 期間顯示 | DOM＋`syncConfetti149`（hunk `@@ -46207,6 +46250,12 @@`） |
| 程式彩紙加量＋擴大 | `spawnConfetti` 46→**90 粒**；任何 reveal 都 spawn（舊只限 won）；非贏 reveal＋comfort 都畫彩紙、comfort 期間繼續落 | `advance()`／`loop()`／reveal／comfort 段（hunks `@@ -46414,6 +46466,8 @@`、`@@ -46424,6 +46478,8 @@`、`@@ -46441,7 +46497,8 @@`、`@@ -46455,7 +46512,7 @@`） |
| 跳過掣入框 | `.awd62-skip` 由 `top:-10px; right:-4px`（半出框）改 `top:8px; right:8px` | CSS（hunk `@@ -779,7 +797,11 @@`） |
| B3 卡片（掂卡面結構） | `cardsData` 加 `win` 旗；`.awd63-card.win::after` 🏆 角標；**csscard 唔再印片名**，改做大媒介圖標（🎬／📺／🎵／📣）＋細字典禮名（`.awd63-cssname` 11px），片名只留卡底 `.t` 一行 | `cardsData`／cardsHtml（hunk `@@ -46175,14 +46207,19 @@`）＋CSS |
| B4 短屏 | `@media (max-height:800px)` 報紙底加 `padding-bottom: 76px`（932 唔郁） | CSS 新段 |
| B2（唔掂幾何） | 新 helpers `awardWinner149`／`awardWinLine149`／`awardGalleryCopy149`；gallery＋declined 報紙動態得主＋作品；結果卡 metricLine；log 列表同標得主 | `awards63FellowsHtml`／`renderAwardResultHtml`／`enqueueNewspaperFromAward` 等 hunks |

- **v149 完全冇掂**：`FLOOR`、`slotCx`、`drawFigure`／`drawTuxedo`／`drawSpr`、`entryPlan`、`fwd64`、beat 列表／ms、`syncCards`／`syncGlamour`、`syncWalkup`、卡片尺寸（88px 闊、2:3 media、`.t`／`.s`）。**v170 嘅 FLOOR 修正同 v149 零直接衝突**（v149 註解亦寫明邏輯座標照舊）。

### D3. v170 企位修正要點樣同 v149 兼容

- **唔好掂（v149 擁有）**：`.awd62-stage` 直向 flex、`.awd62-aud149` 上下帶、`.awd62-canvaswrap`、canvas backing 636×360、`setTransform(1.5, …)`、`syncConfetti149`＋M5 GIF 層、`.awd62-skip` 新位、卡片 `win` 旗／🏆角標、csscard 媒介圖標＋典禮名結構、報紙／結果卡 B2 helpers。v170 唔好喺自己分支重做呢啲，亦唔好改 `~/workspace/linji-work149/` 任何檔案。
- **已知 rebase 衝突點（v149 落地嗰陣要解決，v170 要等佢解決完先落實）**：
  1. **glamour overlay 位置打架**：v149 將 `glamHtml` 由 `.awd62-frame` 入面搬去 stage 層（`aud149 bot` 後面）——`.awd63-glamour` 係 `position:absolute`，最近 positioned 祖先由 frame 變成 stage（`position:fixed`），overlay 會冚成個 stage（連上下觀眾帶），唔再對齊 canvas；**呢個改動倒退返 v166 B1**（glamour 由全幅改做只冚 canvas、右邊 44% panel）。v149 rebase 上 v166／v168 之後 main 嗰陣，glamour 必須留喺 frame 層（或等效對齊 canvas），否則 v170 嘅 glamour beat 企位（阿偉 x166／FLOOR）驗證基準會錯。
  2. **v149 base 冇 walkup／tuxedo／M1 底圖**：佢嘅 `stage.innerHTML` diff 係建基於 v146 骨架（舊 glamour 全幅 img、冇 walkup 層、冇 canvaswrap）。rebase 嗰陣 walkup GIF 層、M6 燕尾服預載、M1 底圖、`AWARDS62_STAGE_BG` 引用要逐項對返，唔可以直接套用 v149 嘅舊 hunk。
  3. **卡片結構**：v149 B3 已經改咗 csscard（媒介圖標＋典禮名）。v170 嘅人像插入點必須建基於**落咗地嘅 v149 結構**（人像取代圖標區，定係取代成個 media 區），唔好喺 v149 之前自立一套卡片結構。
- **v149 落地後要重驗（v170 嘅驗收清單）**：
  1. FLOOR→~155 之後，四個人物喺**新佈局**（上下觀眾帶＋636 backing）下嘅腳底／頭頂位置——backing 變大唔改邏輯座標，但顯示縮放唔變（CSS 闊度一樣），數字上應同 C2 一致，仍要實駕量度（932＋700）。
  2. 上下觀眾帶會唔會喺 700 高 viewport 擠壓 frame（`flex:1` 吸剩餘空間；700 高嗰陣上下帶 `min-height:22px` 各 22px，frame 剩低約 656px 高——canvas 233＋卡 172＋caption＋tap 約 470–500px，夠位，但要實測）。
  3. M5 彩紙 GIF 層（`z-index:2`，冚 canvas）喺 reveal／comfort 期間會唔會遮住移上舞台嘅人物頭頂（人物頭頂 y≈104–107 canvas，GIF 係全幅透明底彩紙，理論唔遮實物，但要目視核實）。
  4. glamour beat：overlay 對齊 canvas＋燕尾服企位（rebase 後嘅結構）＋卡列隱藏（v168）三樣一齊重驗。
  5. 後備舞台（fallback）平台頂：v149 冇掂，v170 改 FLOOR 嗰陣要一併改（見 C2）。
- **次序建議**：v149 落地＋rebase 解決 glamour 衝突 → v170 先落 FLOOR 修正＋卡片人像；唔好兩個分支同時改 `awards62PlayCeremony` 嘅 DOM 骨架。

## E. Pixellab 餘額

- 核實方法：`python3 ~/workspace/custom-connectors/custom.pixellab/bin/pixellab.py balance`（harmless read，CONNECTOR.md 指定做法），2026-11-13 調查期間即時查核。
- **現時餘額：4,576／5,000 generations**（plan：Tier 2: Pixel Artisan，status active；USD credits 0.0）。上次記錄 4,601／5,000（2026-11-13 02:19，v147 報告）→ **期間用咗 25 次**（v160 樣本等）。
- 成本參考（CONNECTOR.md，已驗證）：pixflux 單張圖 1 次；animate-with-text 5 次；1-direction object **10 次**（256×256，2026-11-12 實測 5000→4990）；`create-character-v3` API **未試過**（helper 有 command，untested；阿偉 v2 character 係網站手動開，唔係 API）。即係話：若 Phase 2 每位星開一個 Pixellab character，**單價未知，要先試一個再報**；若行 1-direction object 路線，10 位約 100 次（餘額夠，佔 2.2%）。
- CONNECTOR.md 入面「free trial 40 generations」嗰段已過時（現時係 Tier 2／5000），唔好跟。

---

## 附錄：要統籌／用戶拍板嘅嘢（工人唔決定）

1. **卡片人像風格路向**：§B4 三條路（全部用現成 bust／全部 Pixellab 像素／fellow 用 bust＋阿偉留海報）。建議先出廖炳星 bust 上卡樣本畀用戶睇。
2. **人像語義**：卡片 media 區而家係「作品海報」；放人像即係將卡面由「作品」變「人物」。v149 B3 已經將無圖卡改做媒介圖標＋典禮名——人像係取代圖標區定成個 media 區，要同 v149 B3 一齊定。
3. **企位修正值**：FLOOR 194→~155（舞台頂線 y155–156），建議實作嗰陣用截圖微調 ±2px；gallery 中央 slot（x202）會企喺講台前面，睇實駕接受唔接受。
4. **生成範圍**：若行 Pixellab 路向，生成 10 個 character（定係只做當期 3 位＋其餘按需）＋阿偉卡去留，要拍板先開工；餘額 4,576 夠用，但單價要先試。
5. **次序**：等 v149 落地＋解決 glamour rebase 衝突先做 v170 嘅 canvas／卡片改動（見 §D3）。
