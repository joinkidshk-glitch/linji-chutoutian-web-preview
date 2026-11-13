# NOTES — v20a170 Phase 1：提名人企位修正＋提名卡人像樣本（調查＋樣本，唔落地）

## §0 摘要

- **用戶追加（2026-11-13 11:23，睇完 v168 review 截圖）**：① 其他提名人要用 Pixellab 生成 character，風格先統一（而家得阿偉有圖，其他三張係深色字卡）；② 提名人物而家唔係企舞台上，似跌咗喺觀眾席（腳位同椅面差唔多高），要移上舞台。
- **Phase 1 範圍**：調查＋樣本＋企位修正，**唔落地**。等用戶睇過樣本先決定做唔做全套。
- **工作副本**：`~/workspace/linji-work170/`，分支 `v20a170`，基底 `fc1a1aa`（遊戲 `280af68`，v167）。企位修正已 commit `69a3553`（唔 push）；調查報告＋樣本頁＋生成資產未 commit（untracked）。
- **Phase 2（方案 C，新舞台-only 底圖，見 §7）**：已實作＋驗證完成，**唔落地**。FLOOR 155→193；新圖 Pixellab 生成（2 次，餘額 4,573→4,571）；實駕 4 case 全 PASS、0 pageerror；全套 pristine 229／12 vs 工作版 230／12，零回歸。F1／F3 判斷見 §7.5。
- **結論先講**：
  - 企位修正：**一行 `FLOOR 194→155`**（＋後備平台頂一併改），9 個 beat 跟同一個常數郁；實駕腳底 canvas y 155，舞台頂顯示 y 差 0.0；前後對照決定性（四個人由白椅之間移到紅幕布前面嘅舞台上面）。
  - 樣本卡：廖炳星 Pixellab character 生成咗（總花費 **3 次**），但三變體對照顯示——**現成 bust 裁切 (b) 比 Pixellab 像素 (c) 更啱卡片**：(b) 成本 0 次、乾淨二次元動畫風、面大表情清；(c) 128px 全身入 78×117 框，面得約 18px 高、表情睇唔清，兼像素 fellow＋海報阿偉並排仍然唔統一。工人建議先睇 (b)。
  - **待拍板**（§5）：卡片人像風格路向、人像語義（作品→人物）、生成範圍、v149 先後次序。

## §1 調查結論（報告：`INVESTIGATION.md`，240 行）

### §1.1 fellows 池（提名人係邊啲人）
- 唯一來源 **`awards63Fellows()`**（`index.html` L46656–46707），上限 **3 位＋阿偉＝4 張卡**（gallery 3 張、0 卡列）。
- 兩輪機制：第一輪按片酬序取真主演（`LEADSTAR59`，137 key 全部係 `gig_1988_*`，即**只有 1990 年有數據；1991／1992 永遠行第二輪**）；第二輪按媒介池加權隨機（v147 機制，已核實係同一套：頂級 ×3／上一代 ×2／過氣 ×1，seed＝year／ceremonyId／medium）。池共 **10 星（程天諾永不入池）**。
- 作品名唔係隨機配——係 gig 自帶作品名（`work59WorkOf` 抽《》）。won_932 三對：《離岸的信》[28000,48000]、《半張船票》、《離岸燈》，全部 1991 電影 gig。
- **廖炳星點解常出現**：1990 電影片酬序排第 2（《詭校夜話》[35000,41900]，玩家殺青咗頭位嗰部就變第 1）；1991／92 film 第二輪首抽 21.4%、3 抽內出現 61.0%（Monte Carlo 20 萬次）；佢係 `fellows[0]` 兼 gallery／nominated 預設得主。但要講明：佢唔係單一機制第一名——陸柏言三池 ×3、1990 排佢前面。
- **更正**：程天諾 unlockYear 1992、鍾楚凝 1992 秋冬 p=0.25 係**巧遇系統**條件，唔係頒獎禮閘（鍾楚凝喺 tv／ad 池 ×2，全年無閘）。

### §1.2 現有美術盤點
- 10 位池星**全部有全身圖 `_base.webp`**（62 檔，卡片夠用）；bust（864×1152）有 **6 位**（陸柏言、廖炳星、魏詠男、蘇芷茵、駱家聲、葉敏芝），**冇 bust 嘅 4 位：齊鎮海、鍾楚凝、顧明輝、麥震東**（得 v105 舊企立圖；零生成方案係由 fullbody 裁頭肩，v109 同款）。
- 舞台 Q 版 sprite 10 位齊晒，唔使生成。
- 卡片而家：**88×172px，media 區 78×117（2:3）**，深色字卡係 `.awd63-csscard` 降級設計（無 poster 作品先出），阿偉卡有《幻彩舞影》海報所以唔係字卡。
- 廖炳星樣貌 brief 全文已逐字抄入 `INVESTIGATION.md`（prompt 永禁真人姓名；另附 brief 檔 4 個 id 錯字警告，跟 live id 唔好跟 brief 檔）。
- **風格提醒**：Pixellab 像素人像 vs 阿偉卡動畫海報 vs 現成動畫 bust 係三種風格——fellow 用像素、阿偉留海報仍然唔統一；三條路列咗喺調查報告。

### §1.3 舞台幾何
- PIL 量度底圖（424×240）：紅幕布 y64–155、**舞台頂線 y≈155–156**、正面 y162–179、紅地毯 y≈180 起、椅頂 y≈165。
- 現時 `FLOOR = 194`（L46247，單一常數），腳底低過舞台頂 **39 canvas px**（932／700 兩個 viewport 都係 38 顯示 px；canvas 顯示 412.8×233.5，縮放 0.974；FLOOR 顯示 y 932→385、700→269；舞台頂 932→347、700→231——**見 §2.4 更正：實測舞台頂顯示 y 係 932→352.6、700→236.6**）。
- 人物 x：4 slots 94／166／238／310（阿偉 166），3 slots 130／202／274；行前 x 向中心移 22%、y＋7（腳 201）。
- **walkup 更正**：walkup beat 冇 canvas 路徑，阿偉行上台係 DOM GIF overlay（144×144、9 幀，路徑焗死喺 GIF 入面），v170 郁唔到。

### §1.4 v149 兼容
- 分支 `v20a149` HEAD `da90957`，未落地、有未 commit 改動，**base 滯後到只包 v147，未含 v160／v166／v168**。
- v149 幾何改動：stage 直向 flex＋上下觀眾帶、canvas backing 636×360＋`setTransform(1.5)`（邏輯座標唔郁）、M5 彩紙 GIF、彩紙 46→90 粒、跳過掣入框、B3 卡片 win 旗＋csscard 改媒介圖標＋典禮名。
- **v149 完全冇掂 FLOOR／slotCx，零直接衝突**。但有兩個 rebase 隱患：① v149 將 glamour overlay 搬去 stage 層，會倒退 v166 B1（frame 層對齊 canvas），rebase 嗰陣必須解決；② v149 base 冇 walkup／tuxedo／M1 底圖，rebase 要逐項對。
- 建議次序：等 v149 落地＋解決 glamour 衝突，先做 v170 嘅改動；v149 落地後要重驗嘅 5 項已列入調查報告。

### §1.5 Pixellab 餘額
- 即時查核：**4,576／5,000**（Tier 2 Pixel Artisan，active），由 02:19 嘅 4,601 用多咗 25 次。`create-character-v3` API 未試過，單價未知，要先試一個再報（參考：1-direction object 10 次／個）。

## §2 企位修正（commit `69a3553`，唔 push）

### §2.1 改動 diff（淨 2 處 code，`index.html` ＋7／−5 行）
- **`FLOOR = 194 → 155`**（`awards62PlayCeremony` L46246，原地改一行）：調查結論核實咗先用——工人自己用 PIL 行掃描底圖：y156 全行暗線（darkfrac 0.95，均亮 29），y157 起急亮（椅／台面），舞台頂線確係 y≈155–156；舊 194 低過舞台頂 39 canvas px。
- **後備舞台 `awards62FallbackStage` 平台頂一併改**：側幕／金邊 `H-52=188 → H-85=155`，平台正面由 155 伸到 `H-22=218`（高 63），金線 `H-56 → H-89=151` 橫跨頂邊；底部／椅列（H-22／H-26）唔郁。
- **唔郁**：slotCx（94／166／238／310；130／202／274）、dispH（48／50／64）、fwd64（x 向中心 22%、y＋7）、walkup GIF、glamour overlay（v166）、卡列隱藏（v168）、SAVE key、softRev、`?v=`、content pack。9 個 beat 全部跟同一個常數郁（pan／enter／names／suspense／reveal／comfort／glamour；open／walkup／out canvas 本來就冇人物——逐個核實過）。

### §2.2 測試
- 新 `tests/test_awards170_static.py`：**40 項全 PASS**；反證對 pristine `fc1a1aa`：9 項 FAIL（全部係新值斷言，守衛全 PASS，唔 crash）。
- **全套 A/B**：pristine **227／12** vs 工作版 **228／12**，FAIL 清單逐項完全一致（12 項穩定 pre-existing），**零回歸**。
- 中途工作版一度 227／13，多出嚟嗰項係 `test_travel114_static.py`——工人加咗 2 行註解令佢釘行漂移；已按慣例 resync（`qa170/resync_travel114_170.py`：43 個 openLoc 呼叫點逐字一致、釘行內容逐行相同；DEF 53610→53612，WRAPPER 44104 唔郁；COUNT 13／FREE 27 不變）。`test_awards64_chibi_static.py` 嘅 FLOOR 釘值 194→155 一併更新；kwan151／tang152 直接跑 PASS。

### §2.3 實駕（`qa170/drive170.py`，本地鏡像＋Playwright，DOM 層量度為主）
- **4 case 一次過全 PASS、0 pageerror**：won_932／won_700／gallery_932／nominated_932。逐幀 drawImage hook 量腳底（canvas y）：

| beat | 腳底（canvas y） |
|---|---|
| pan／enter／names／suspense／comfort | **155**（min／med／max 全部 155） |
| reveal 行前 | **162**（fellow）／**162.5**（燕尾服阿偉，Math.round 頂位 ＋0.5） |
| glamour 燕尾服 | **155.5**（同上 rounding） |
| slot x | 4 slots 94／166／238／310、gallery 130／202／274，實測逐值吻合 |

- **前後對照**：v168 before（`won_932_beat_reveal.png`）四個人企白椅之間、腳底同椅面齊高；家下四個人企紅幕布前面嘅舞台上面，講台喺阿偉同第三人之間露出嚟。`won_700` 同 932 一致。
- **gallery 中央 slot**：x202 嗰位企講台前面，講台遮咗下半截、上半截露出——調查預期嘅可接受狀態，目視自然，唔使移位。
- **walkup GIF 照行**（walkOn＋img complete，冇掂過）；glamour 燕尾服企舞台上面，v166 並置佈局＋海報 panel 完好，卡列隱藏照舊。
- 證據：`qa170/drive170.json`（4 case 全 PASS）、`qa170/shots/`（36 張逐 beat 截圖）、`qa170/suite_pristine170.txt`／`suite_work170.txt`。

### §2.4 更正任務 brief 一個數字
- 舞台頂顯示 y 實測係 **932→352.6、700→236.6**，唔係 brief 寫嘅 347／231——因為 canvas 實測係 border box 406×233（唔係 412.8）、content 頂 207／91（唔係調查估算嘅 196／80），scale 0.939。腳底顯示值同舞台頂顯示值差 0.0（±3 容差內）；錨本身（canvas y155）係 PIL 獨立核實，唔受呢個影響。

## §3 樣本卡（廖炳星，唔掂 `index.html`、唔 commit、唔 push）

### §3.1 Pixellab 實際成本
- 餘額核實（開工前）：**4,576／5,000**，同調查報告一致。
- `create-character-v3` 首次試用：**1 個 call，3 次**——job 用量 `usage.generations: 3.0`，餘額 **4,576 → 4,573**。同 OpenAPI 公式完全吻合：from-scratch 128×128 係 1（pixen）＋ceil(128²×8／65536)＝1＋2。遠低於 50 次停手線，唔使停。
- 冇其他收費 call：balance／list／get-character／job polling 全部 0 次。**總花費 3 次**。
- Character：id `1c3c608c-f6ed-4c1b-8edd-4b9cae2cba7e`（名「廖炳星」，state「Idle」，128×128，8 方向，view side，template mannequin，no_background）；job `3d2accc5-c712-405c-8c11-30c931eebc45`，約 3 分半鐘完成。**唔使另外開 state**——預設 Idle state 嘅 south 幀就係企立圖。Prompt 用調查報告逐字抄嘅 brief 元素（瘦面、顴骨突出、精靈市井眼神、嘴角微翹、挑眉壞笑、頭微傾、花恤衫＋寬鬆西褲），**零真人姓名**；風格錨＋阿偉 v2 character（`49907fa9…`）做參照（view side 跟阿偉做法）。

### §3.2 產出檔案
- 樣本頁：`sample_liao_card.html`（卡 CSS 逐字照抄 live L788–797：卡 88×172、media 78×117 2:3、.t 11px／.s 10px）
- 截圖：`samples170/sample_liao_card_932.png`、`samples170/sample_liao_card_700.png`（430 闊，Playwright 實渲；兩張 full-page 內容相同）
- 生成資產（全部喺 `samples170/`，**未入 repo `assets/`**）：`liao_pixellab_south.png`（128×128 RGBA，人物 bbox x37–87／y4–124，全身企立）、`liao_bust_crop_2x3.png`（bust 864×1152 裁 504×756，2:3）、`liao_character_body.json`（請求原文）、`liao_character_create.json`、`shot170.py`
- 接入路徑：`samples170/INTEGRATION_PATH.md`

### §3.3 三變體風格對照結論
- **(a) 現況深色字卡**：live 就係咁，`.awd63-csscard` 降級設計唔係 bug；問題係三張 fellow 卡得作品名＋人名，冇人像。
- **(b) 現成 bust 裁切**：乾淨二次元動畫風，同主線舞台／fullbody 同一家族；面大，挑眉壞笑＋頭微傾＋花恤衫同 brief 一字不差；**成本 0 次**。目視驗證過，裁切框 x180–684／y40–796，面完整無裁走。
- **(c) Pixellab 生成人像**：做到，但有兩個 trade-off 必須畀用戶睇到：① character 係**像素風全身 sprite**，唔係動畫風 bust；衫跟到 brief，但 128px 全身入 78×117 框，**面得約 18px 高，表情睇唔清**（樣本頁有 ×2 放大對照）；② **像素 fellow＋海報阿偉並排，風格仍然唔統一**——要真統一，要麼四張卡全部行 (b)，要麼四張卡全部行像素（阿偉卡都要換做佢個 v2 character，0 次新生成）。工人建議先睇 (b)。
- 另一個語義點（樣本頁有寫）：(b)(c) 都將 media 區由「作品」位變「人物」位，作品海報唔再出現，唔止換圖。

### §3.4 接入路徑摘要
- 渲染點：`awards62PlayCeremony` 內 L46171–46181 `cardsData`／`cardsHtml`——fellow 加 `portrait` 欄，media 分流「有 portrait 先出人像，否則沿用 poster／csscard」（未齊圖自動跌返現況）。`syncCards`／`syncGlamour` 唔使改。**但要等 v149 落地**：v149 B3 已改 csscard 結構（媒介圖標＋典禮名）＋卡加 `win` 旗，接入要建基於落咗地嘅 v149 結構，唔好自立一套；人像取代成個 media 定圖標區要同 v149 B3 一齊定。
- 圖路徑建議：`assets/story/awards/portraits/<starId>_card.png`（bust 路線 2:3，240×360）或 `<starId>_pixel.png`（像素路線 south 幀 128×128，透明底，卡面 `img` 底 `#2b2118` 深啡＋`image-rendering: pixelated`）。卡尺寸唔使改。
- 調查結論核實結果：全部吻合——卡 88×172／media 78×117、bust 6 位有／4 位冇、10 位全部有 fullbody base、廖炳星 `liu_bingxing` id 無錯。

## §4 生成清單＋成本預算

| 人 | 現成圖 | 全套路線 (b) bust 裁切 | 全套路線 (c) Pixellab 像素 |
|---|---|---|---|
| 廖炳星 | bust 有 | 已出樣本，0 次 | 已生成 character，3 次（做咗） |
| 陸柏言 | bust 有 | 裁切，0 次 | 3 次 |
| 魏詠男 | bust 有 | 裁切，0 次 | 3 次 |
| 蘇芷茵 | bust 有 | 裁切，0 次 | 3 次 |
| 駱家聲 | bust 有 | 裁切，0 次 | 3 次 |
| 葉敏芝 | bust 有 | 裁切，0 次 | 3 次 |
| 齊鎮海 | 得 fullbody | fullbody 裁頭肩，0 次（要逐張定裁切框） | 3 次 |
| 鍾楚凝 | 得 fullbody | fullbody 裁頭肩，0 次 | 3 次 |
| 顧明輝 | 得 fullbody | fullbody 裁頭肩，0 次 | 3 次 |
| 麥震東 | 得 fullbody | fullbody 裁頭肩，0 次 | 3 次 |
| **合計** | — | **0 次** | **約 30 次**（10 位；廖炳星已做，剩 27 次） |

- 阿偉卡換像素：0 次（已有 v2 character `49907fa9…`，south 幀即用）。
- 零生成路線注意：(b) bust 同對應 fullbody base 係咪同一張面，未逐張像素核實（Phase 2 實作驗收嗰陣要做；v138 A1 教訓——衫色／髮長走樣）。
- 像素路線注意：面部可讀性弱（全身 128px 入細框）係結構性 trade-off；若用戶堅持像素但要面大，要另試像素頭像特寫做法／成本，未試。

## §5 待拍板事項（等用戶睇過樣本先決定）

1. **卡片人像風格路向**：(b) 全部 bust 裁切（成本 0、風格同主線同一家族、面大）／(c) 全部像素（成本約 30 次，阿偉卡都要換埋 v2 像素先真統一）／混合（像素 fellow＋海報阿偉——仍然唔統一，唔建議）。工人建議先睇 (b)。
2. **人像語義**：media 區由「作品」位變「人物」位——fellow 卡唔再出作品海報，作品名只留文字。係咪接受？（阿偉卡保留海報定一齊換人物？）
3. **企位修正 FLOOR 155**：Phase 1 改動已驗證完成，可唔可以落地（要 rebase 上最新 main，見 §6）？
4. **生成範圍**：10 位一次過定先做 3 位（邊 3 位？）——廖炳星已做樣本，剩低 9 位。
5. **v149 先後次序**：卡片接入要等 v149 落地（B3 結構）；企位修正同 v149 零直接衝突，但 v149 rebase 有兩個隱患（§1.4），落地次序要定。

## §6 環境／main 變動／殘留

- **main 已經郁咗**：Phase 1 開工 base `fc1a1aa`，而家常駐 clone main 係 `9b95de0`（v165 NOTES；遊戲 `b754fac`，v165 已落地——決策 (c) 兩條返回路徑都掛，線上 5,247,634 bytes sha `dcb32841…`）。v170 落地嗰陣要 rebase（企位改動得兩處、零直接衝突，rebase 應該乾淨）。
- **Phase 2 rebase 已做（見 §7.1）**：分支已 rebase 上最新 main **`56141a3`**（v169 已落地，線上 5,251,706 bytes sha `c0bbc07d…`），新 HEAD **`37e2185`**（Phase 1 內容不變，行號 resync 咗）。main 喺 Phase 2 開工前後冇再郁（fetch 核實 origin/main＝56141a3）。
- **環境插曲**：企位工人中途用 `git archive` 解去 `/tmp` 塞爆咗 512M tmpfs（100%），已即刻清走，恢復 26%；之後 pristine 對照改用 `git worktree`（已移除）。Suite 數字無受影響。另：10:50–11:01 HKT 寫入 EPERM 惡化已恢復；Chromium 死過，實駕證據以 DOM 層為主。
- **殘留**：(b) bust 同 fullbody base 同面未逐張像素核實（Phase 2 驗收）；像素頭像特寫做法未試；v149 落地後 glamour 並置＋卡列隱藏＋企位要重驗；v147 B1 舞台細＋B2 報紙唔講賽果（v149 處理中，狀態不變）；掌聲 MP3 未經人耳試聽。
- **Phase 1 唔落地**：分支 `v20a170`，企位 commit `69a3553`；`INVESTIGATION.md`、`sample_liao_card.html`、`samples170/` 未 commit；唔派 review。

## §7 Phase 2：新舞台-only 底圖（方案 C，實作＋驗證，唔落地）

### §7.1 Rebase（base `fc1a1aa` → main `56141a3`，新 HEAD `37e2185`）
- 開工先 `git fetch origin main` 核實 main 未郁（origin/main＝main＝`56141a3`，v169）。
- `git rebase main`：`index.html` 自動合併（diff vs main 得返 Phase 1 兩處：FallbackStage ＋2 行註解＋H-85、FLOOR 155）；唯一衝突係 `tests/test_travel114_static.py`——純行號漂移（main 經 v157／v165／v169 resync 過）。
- 解決方法：取 HEAD 版（main 數字）＋ `qa170/resync_travel114_170.py` 更新到新 base（OLD 改 `56141a3`、插入點 L46098、DEF 53690→53692、WRAPPER 44172 唔郁；單次掃描 dict 查表，冇逐對 re.sub）。核實全 OK：COUNT 13／FREE 27 釘行逐行相同、DEF 行內容吻合、openLoc 呼叫點序列 43 vs 43 一致。套用後 `test_travel114_static.py` PASS；`test_text125_static.py` 唔受影響（PASS，冇釘行喺漂移區）。
- `GIT_EDITOR=true git rebase --continue`（環境冇 EDITOR；冇 pipe 去 head）。Rebase 完成，HEAD `37e2185`。`core.sshCommand` 已核實行 `~/workspace/gh_tunnel.py`（18080 已死）；git identity 已設（Muse／muse@localhost）。

### §7.2 生成紀錄（Pixellab，總花費 **2 次**，餘額 **4,573 → 4,571／5,000**，預算 1–3 內）
- **參照相**：只用真實相 `~/workspace/linji-work147/samples147/m1_ref_island_shangrila.webp`（港島香格里拉大禮堂，1080×700）做 prompt 撰寫參照（M1 同款做法）；**冇用成品 M1 圖（`m1_ballroom.png`／舊 `bg_awards_ballroom.jpg`）做參照**。
- **`init_image` 決定（唔用）**：查過 helper＋API 文件——`pixellab.py` 係 body JSON 直傳，pixflux 支援 `init_image`／`init_image_strength` 欄位。但真實相 8 成畫面係白椅、舞台又細又遠、仲要係藍底幕布印住酒店英文名（有文字漏入風險＋舞台設計唔啱：冇紅幕布／冇講台）；crop 舞台區出嚟得約 240×150px，放大又矇。所以沿用 M1 驗證過嘅純文字生成，參照相只指導 prompt 寫法。決定＋理據留檔，唔係漏做。
- **v1**（`samples170/stage_only_v1.png`，400×224，1 次；body `stage_only_body.json`）：M1 prompt 改做舞台填滿取景——紅絲絨幕布拉開到左右邊、金講台置中、水晶吊燈頂部、暖金燈光、深木牆板；明確「No chairs, no audience, no red carpet, no people, no text, no logos」。結果：幕布／講台／吊燈／色板全部啱，**唯一瑕疵係底部有一行深色椅背**（y≈211–224，約 7% 高）。
- **v2**（`samples170/stage_only_v2.png`，400×224，1 次；body `stage_only_v2_body.json`）：v1 prompt ＋「平台填滿成個底部邊緣、冇地板／椅／觀眾／紅地毯」。結果**更差**：成行觀眾椅＋中央一條紅地毯由舞台伸到底部——模型唔可靠咁執行否定式觀眾約束。**棄用**，檔案留檔。
- **最終資產**：v1 裁走底部椅背（y0–208；椅頂由 y≈211 起，zoom 核實 `stage_only_v1_floor_zoom.png`）→ 400×208，再 LANCZOS 放大 **424×240 JPG q90**（`samples170/bg_awards_ballroom_new.jpg`，40,380 bytes）。垂直拉伸 8.8%（x 1.06×／y 1.154×），實駕截圖睇唔出變形。舊圖留檔 `samples170/bg_awards_ballroom_old.jpg`（39,211 bytes，M1 424×240），唔刪除。

### §7.3 PIL 量度＋FLOOR 決定（唔照抄 Phase 1 嘅 155）
- 最終 424×240 中央帶（x244–296）逐行掃描：幕布紅 y188–190（mean 77–79）→ y191 過渡（101）→ y192（138）→ y193（170）→ **y194 滿亮平台面（198）**，平台面 y194–~225。**舞台頂邊＝194，FLOOR＝194−1＝193**（同 Phase 1 convention：邊 −1）。
- 源圖對照：平台面後緣 source y168（過渡 y166–167）×240/208＝193.8 ≈ 194，吻合。
- 講台：zoom 核實（`samples170/final_podium_zoom.png`）頂 slab 約 y181、底座約 y210，完整在圖內，唔裁；左右幕布邊完整；無字無人無 logo 無椅無紅地毯。
- 底部 y232／y239 dark 0.04／0.17（木紋地板帶 only；舊圖底部椅區 0.29–0.55）——裁切後無椅背殘留。

### §7.4 Code 改動（`index.html` 淨 7 行原地改，行數零漂移）
- **`FLOOR = 155 → 193`**（L46328，＋新註解寫明 PIL 量度數字；舊圖頂線 155、舊值 194 企觀眾席）。
- **後備舞台 `awards62FallbackStage`**：平台頂 `H-85＝155 → H-47＝193`（＝H−(240−FLOOR)），平台正面由 193 伸到 `H-22＝218`（高 25，原 63），金線 `H-89 → H-51＝189` 橫跨頂邊；底部／椅列（H-22／H-26）唔郁。
- **唔郁**：`AWARDS62_STAGE_BG` 路徑不變（同名覆蓋）、canvas／draw()／slotCx／drawFigure／glamour overlay／panel／卡列／字幕框／跳過掣／walkup GIF 層；gallery pan beat 文案「今晚你坐喺觀禮席」唔使改（實駕確認保留）；SAVE key、softRev、`?v=`、content pack JSON 唔郁。

### §7.5 F1／F3 判斷
- **F1（frame 上下剩餘 `#14101f` 底色）：接受現狀，唔喺呢票做。** 數字：won_932 names 截圖（430×932）舞台上深色帶 199px（21%）、字幕下深色帶約 207px（22%）——同 v147 B1 記錄嘅 pre-existing 狀態一致（frame 近三分之二係黑），P2 冇改 frame 幾何，唔係 P2 引入。Canvas **內**填充反而改善咗（舊圖下半係椅＋地毯，家下幕布邊到邊、平台填滿）。治本係 v149 B1（636×360 backing 放大 canvas）；填法建議：跟 v149 B1，或者將來喺 frame 上下加純暗景光暈——**唔可以加返觀眾席／人頭／椅**（用戶 11:59 已否決台下部分）。難睇程度：深色底係典禮夜晚氛圍一部分，舞台光猛對比強，視線集中；但上下空帶確實大，留待 v149 處理。
- **F3（源圖 400×224，v149 636×360 backing 下放大 1.59× 會軟）：接受，唔使升頻／重新生成。** ① 而家 424×240 下實駕截圖清晰，像素邊乾淨無軟化（canvas 用 `image-rendering:pixelated`）；② 636 backing 下 1.59× 放大配合 pixelated 渲染只會令像素粒變粗，唔會變模糊，符合 8-bit 風格；③ pixflux 闊度上限 400px，生成唔到更大源圖。**待 v149 落地後再驗**（呢個分支 backing 仲係 424×240）。

### §7.6 測試
- 更新：`tests/test_awards170_static.py`（FLOOR 193、fallback H-47／H-51／高 25、舊值 H-85／H-89／155／194 唔再出現、reveal 行前腳 200、講台 y≈181–210）：**42 項全 PASS**。
- 新增內容斷言：`tests/test_awards160_m1_static.py` §4（PIL：幕布底 y188–190 暗／y194–196 亮、幕布紅、講台金像素、底部無椅背）：**24 項全 PASS**（§4 新加 5 項）。
- 更新：`tests/test_awards64_chibi_static.py`（FLOOR 釘值 155→193）：**ALL PASS**。
- 相關逐個直跑 PASS：awards62／awards166／awards168／travel114／text125／kwan151／tang152。
- **反證**（乾淨 FAIL，唔 crash）：awards170 對 pristine main `56141a3` → 9 項 FAIL（全部係 P2 新值斷言，守衛 PASS）；chibi → 1 項 FAIL（FLOOR 釘值）；M1 §4 對舊底圖 → 2 項 FAIL（舞台頂邊＋底部椅背）。
- **全套 A/B**（`qa131/run_suite.sh`）：pristine（常駐 clone，`56141a3`）**229／12** vs 工作版 **230／12**；FAIL 清單逐項完全相同（12 項穩定 pre-existing：flash51／giglib36／pacing35／poster59／rumor49／slot50／soft_tip_111／start53／weave43／weave44／weave49／wrap38），唯一差別係新測試檔 `test_awards170_static.py` PASS。**零回歸**。紀錄：`qa170/suite_pristine170_p2.txt`／`suite_work170_p2.txt`（舊 Phase 1 嗰兩份唔覆蓋）。

### §7.7 實駕（`qa170/drive170_p2.py`，新一輪，截圖 `qa170/shots_p2/` 37 張，唔覆蓋 Phase 1 嗰批；結果 `qa170/drive170_p2.json`）
- **4 case 一次過全 PASS、0 pageerror**：won_932／won_700／gallery_932／nominated_932。
- 腳底（drawImage hook，canvas y）：pan／enter／names／suspense／comfort 全部 **193**（min／med／max 一致）；reveal 行前 **200**（fellow）／**200.5**（燕尾服，Math.round 頂位 ＋0.5）；glamour 燕尾服 **193.5**（同上 rounding）。slot x：4 slots 94／166／238／310、gallery 130／202／274，逐值吻合。腳底顯示值＝舞台頂顯示值（won_932 388.3／won_700 272.3／gallery＋nominated 480.3，差 0.0）。
- 目視：四個人企平台上面、講台置中露出；紅幕布填滿成個 canvas，左右邊完整；glamour 燕尾服＋海報左右並置、卡列隱藏照舊；walkup GIF 照行（walkOn＋img complete）；gallery pan 文案「今晚你坐喺觀禮席」保留；nominated comfort beat 正常。
- **names beat 截圖有約 208px 空帶**（舞台同字幕之間）：**唔係 P2 回歸**，係 pre-existing 卡列 stagger-in 時序——`syncCards` 規定 names beat 卡片逐張 `elapsed > 200 + i*380`ms 先加 `.show`，截圖喺 seg 轉換一刻（poll 150ms）捕捉到 `.awd63-cards.on` 已開但卡片未 `.show` 嘅窗口（容器有高、卡透明）；suspense 段四張卡全部可見，卡列本身正常。Phase 1 同一張截圖冇空帶，係 poll 時序撞正 `.on` 未加之前（容器 `display:none`、高 0）——兩者都係同一段 stagger 動畫嘅不同時點，唔係 P2 改壞。提一提：呢個窗口喺實玩都會出現約 1.3 秒（names 頭段卡列留白），要唔要修係 review／用戶決定，唔喺呢票。

### §7.8 殘留／待跟進
- v149 落地後要重驗：636 backing 下清晰度（F3）、glamour 並置、卡列隱藏、企位（FLOOR 193 喺 636 邏輯座標唔郁，但要實駕確認）；v149 B1 觀眾帶剔除嗰邊另有統籌做緊，唔好同佢打架。
- 卡片路向（bust 裁切／像素／留深色字卡）未做——等用戶拍板（§5）。
- 掌聲 MP3 未經人耳試聽（舊殘留）。
- **Phase 2 落地**：分支 `v20a170` rebase 上 v171 落地後嘅 main `6d08c7c`（見 §7.10），統籌負責落地；唔 push 分支去 GitHub（worktree 副本 origin 係 github.com，分支本身已喺常駐 clone）。

### §7.9 待 commit 內容（Phase 2 完成後一次過 commit）
- `index.html`（FLOOR＋fallback，7 行原地改）、`assets/story/awards/bg_awards_ballroom.jpg`（新圖 40,380 bytes；路徑不變）、`tests/test_awards170_static.py`／`test_awards160_m1_static.py`／`test_awards64_chibi_static.py`、`qa170/resync_travel114_170.py`（rebase 更新）、`qa170/drive170_p2.py`／`drive170_p2.json`／`shots_p2/`（37 張）、`NOTES_V20A170.md`（本 §）、Phase 1 遺留未 commit 檔（`INVESTIGATION.md`、`INVESTIGATION_PHASE2.md`、`sample_liao_card.html`、`samples170/`——Phase 2 新增：`stage_only_body.json`／`stage_only_v1.png`／`stage_only_v2_body.json`／`stage_only_v2.png`／`bg_awards_ballroom_new.jpg`／`bg_awards_ballroom_old.jpg`／`stage_only_v1_crop208.png`／三張 zoom 圖）。

### §7.10 落地前 rebase（v171 落地後，統籌）
- 核實期間 main 由 `56141a3`（v169）郁到 `6d08c7c`（v171：v169 review C1+C2 修復，地點板捲動淡出提示＋送禮掣鎖住態變灰；全套 230／12）。
- Rebase `v20a170` 上 `6d08c7c`：**零衝突**，新 HEAD `1ec5335`（Phase 2）／`9f8990f`（Phase 1）。index.html diff 對新 main 仍然淨係兩處（fallback H-47／H-51＋FLOOR 193），行數零漂移。
- **tang171 零行數漂移守門捉到 +2 行**：`tests/test_tang171_static.py`（v171 新測試）釘總行數 59171＋openLoc DEF 行 53690；P2 fallback 嗰兩行註解令 index.html 變 59173、openLoc DEF 移去 53692——係純漂移，唔係功能回歸（`grep -n` 核實 `function openLoc(id, opts){` 真係喺 53692）。修法：resync 該檔釘值 59171→59173、53690→53692（＋註解說明來源），唔刪 P2 註解。直跑 22/22 PASS。
- **最終全套 A/B**（`qa131/run_suite.sh`，統籌獨立重跑）：v171 main `6d08c7c` **230／12** vs 工作版 **231／12**；FAIL 清單逐項完全相同（12 項穩定 pre-existing：flash51／giglib36／pacing35／poster59／rumor49／slot50／soft_tip_111／start53／weave43／weave44／weave49／wrap38），唯一差別係新測試檔 `test_awards170_static.py` PASS。**零回歸**。
- 落地：常駐 clone checkout main → `git merge --squash v20a170` → commit → push main → curl 核實 bytes／sha → fsck → 派 v170 設計 review。

### §7.11 落地紀錄（統籌，2026-11-13 約 12:45 HKT）
- Game commit `59fdf54`（squash merge 自分支 `v20a170` HEAD `2a82c78`，基底 main `29d4821`）。
- 線上核實：`https://joinkidshk-glitch.github.io/linji-chutoutian-web-preview/` index.html **5,254,542 bytes、sha256 `651c26e7045fdb30234c7fd8fb1496500814f71311653b9d508bbe1e46694776`**，同 repo index.html 字節數＋sha 完全一致。`FLOOR = 193`／`H-47` 各 1 處。`git fsck --strict` 乾淨。
- Pixellab 總花費：Phase 1 3 次＋Phase 2 2 次＝**5 次**；餘額 **4,571／5,000**。
