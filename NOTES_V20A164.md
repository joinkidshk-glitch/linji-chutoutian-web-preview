# NOTES — v20a164 鄧麗萍送禮補完（v152 殘留）

- **版本**：v20a164
- **分支**：`v20a164`（工作副本 `~/workspace/linji-work164/`，基底 main `222a984`＝v152）
- **狀態**：實作＋驗證完成，**唔落地**（唔 merge、唔 push main、唔開 PR，等統籌）
- **任務來源**：用戶 2026-11-13 09:22 拍板開票，補 v152 殘留「實用禮物專屬反應句 live 行唔到」

## §1. 調查結果（先做，唔好假設——有兩處範圍假設錯咗）

### 1.1 `gift_prefs.json` tang entry：likes／dislikes 真係空
`content/gift_prefs.json` → `npcs.tang`：`relKey: "rel_tang"`、`requireFlagsAny: ["flag_tang_open"]`、`mapNpcId: null`、`likes: []`、`dislikes: []`。`prefKind()`（index.html L30373 一帶）由 likes／dislikes 查分流，空即永遠 neutral——v152 殘留原因 ① 屬實。

### 1.2 `gift_react_copy.json` tang 反應句：齊晒，但咖啡豆唔係 liked
`byKey`／`entries` 共有 6 句 tang 專屬句：
- `:liked` ×3：`gift_fountain_pen`（`GR-tang-pen｜liked`）、`gift_desk_calculator`（`GR-tang-calc｜liked`）、`gift_dress_watch`（`GR-tang-watch｜liked`）
- `:dislike` ×1：`gift_rose_premium`（`GR-tang-rose｜dislike`）
- `:neutral` ×2：`gift_memo_pad`（`GR-tang-memo｜neutral`）、`gift_coffee_beans`（`GR-tang-coffee｜neutral`）

**出入 1（任務原假設錯）**：任務話 likes＝名筆／計數機／腕表／**咖啡豆**（四樣，對應已有 `:liked` 句）——實情係**咖啡豆只有 `:neutral` 句，冇 `:liked` 句**。`reactionEntry()` 查唔到 `tang:gift_coffee_beans:liked` 會跌返 `tang:gift_coffee_beans:neutral` 句，但 `calcDelta()` 會計 +2（liked）——句（「夜更對帳用得着，放那邊，我自己煮」）同數（+2）打架。**決定：likes 只入三件（名筆／計數機／腕表），咖啡豆唔入 likes，行 neutral（+1＋專屬 neutral 句）**。要四件齊 liked 嘅話，要另寫一條咖啡豆 `:liked` 句（新玩家面文案，等用戶／統籌決定，唔喺呢票自作主張寫）。

### 1.3 四件貨根本唔喺商店（任務未提及嘅第二個缺口）
`content/items_gifts.json` 只有 10 件 MVP 貨（菠蘿油／蛋撻／保溫瓶／髮夾／拍紙簿／咖啡豆／卡帶／手作甜品／時裝雜誌／香水），`content/shops.json` `shop_street_mk` 亦只得呢 10 格——**名筆／計數機／腕表／玫瑰四個 itemId 喺成個商店系統唔存在**，冇得買就冇得送。反應句同 prefs 係寫好咗，但貨本身從未上架（PLAN_GIFT_SHOP MVP subset 只包 10 件）。**決定：經載入正規化一併注入埋貨＋上架**（見 §2），唔直改 pack JSON。價錢跟現行 uncommon 帶，pack 入面冇呢四件貨嘅定價來源：名筆 $550／計數機 $280／腕表 $650／玫瑰 $600，每週補貨 2／2／1／2。附帶效果：玫瑰上架後，Vera／采兒嗰邊嘅 `:liked` 玫瑰句（`GR-vera-rose_premium｜liked`、`GR-choi-rose｜liked`）亦同時打通——同病，順手，唔另開票。

### 1.4 送禮機制現行規則（核實）
- 入口：`GiftShop.canGive(npcKey)`——pref 存在＋`flagOk`（tang：`flag_tang_open`，或 `gift_met_tang`／`gift_talked_tang`；tang 冇傾談路徑，實際只認 `flag_tang_open`）＋每日每人 1 次（`lastGiveDay[relKey]`）＋庫存非空。未見面前 `canGive("tang")` 回 `tangLocked`：「院線那邊，還未到送禮的時候。」
- 分流：`prefKind` likes→`liked`、dislikes→`dislike`、其餘→`neutral`；`reactionEntry` 查 `byKey[npc:item:pref]`，缺專屬先跌返同 item `:neutral`，再跌返該角任意 `:neutral`，最後先係佔位句。
- 數字：`calcDelta` 用 item `deltaRel`（新貨沿用 `{default:1, liked:2, disliked:-1}`）；同 item 第 2 次起正數減半；每週淨好感軟 +2（`weekGiftGain[relKey]`）；`giveGift` 經 `StoryOC.bumpRel(relKey, applied)` 加去 `S.story.rel`。
- 耗日：soft 預覽下唔耗日（`softSocialCostsDay()` false → 「不耗日 · 只用今日送禮次數」）；live 耗 1 日——tang 沿用同一條路，唔另設。
- UI：`MAP_NPC_TO_KEY = { stylist:"vera", colleague:"hiu", reporter:"choi" }`（tang 唔喺入面）；地點板送禮掣經 `addLocTalkGiftActs(add, L, npcId)`（要地圖 NPC id）；`openGiftPick(npcKey, L)` 本身唔認 map NPC，只認 npcKey；結果 modal 經 `doGiveGift` 顯示 `好感 ±N`。

### 1.5 DENG 排片線見面場合（核實）
鄧麗萍唯一出現場合係**事務所（`agency_ho`）地點板**：`DengLine.meetAvailable()`（C5 完成＋favor≥1＠agency_ho＋身處事務所）出「鄧麗萍約談排片」掣 → `playMeet()`；push1／push2／crisis 掣同一版面（`pushAvailable` 逐節出）。佢唔係 `NPCS` 成員、冇 `homes`、唔係任何地點駐場 NPC（`residentNpc` 只有何生喺 agency_ho）。`R_tang_meet_stub`（rom2 pack）係 `stub:true`＋`playerOffer:false`，`isStubNode` 過濾，永不入玩家列表——佢嗰 +1 唔會喺 live 行到。

### 1.6 rel_tang 經濟（核實——呢個係 §4 嘅關鍵）
- live 唯一 pre-gate `rel_tang` 來源：meet data 抉擇 `C_tang_meet_data`（`flag_tang_open`＋`rel_tang: 1`）；wait 抉擇 +0、唔寫 flag。
- push1 閘門：`flag_tang_open ∧ rel_tang ≥ 2`（`DengLine.pushGate`，threshold 2）。
- push 節點內抉擇各 +1（入閘之後先攞到）。
- **即係話：見面後 `rel_tang` 停喺 1，live 再無其他 +1 來源，push1 喺 live 現時係到唔到嘅**（只可以經 `debugUnlockTangPush`／`seed_deng_push_ready` 開）。呢個係 pre-existing 缺口，**唔喺呢票修**（改排片閘門係另一設計決定），但佢直接決定 §4 嘅處理：送禮絕對唔可以加 `rel_tang`——否則送禮就變成 live 唯一開 push1 嘅途徑，即係用錢買通排片線。

## §2. 改動一覽（index.html 為主，唔直改 content pack JSON）

| 位置 | 改動 | 行數 |
|---|---|---|
| `giveGift()`（L30482） | tang 專例：`applied = (npcKey==="tang") ? 0 : rawDelta`（同行改，零漂移） | 1 改 |
| `refreshCopyPacksFromDisk()`（L31388） | giftPrefs 賦值行同行 append 呼叫 `applyTangGift164()`（零漂移） | 1 改 |
| `openLoc()` 事務所 DengLine 塊（L53764–53779） | 新增「送禮：鄧麗萍」掣（見 §3） | ＋16 |
| `openGiftPick()`（L57400） | tang 副標：「每日限送 1 次 · 送禮只係公事心意，唔會改變排片關係」（同行改） | 1 改 |
| `doGiveGift()`（L57433） | tang 結果行：「排片關係不變」（同行改） | 1 改 |
| `inv72Html()`（L57466） | 庫存提示加「或者喺事務所見過鄧麗萍之後」（同行改） | 1 改 |
| 檔尾（L58777 起） | 新增 `applyTangGift164()`（見下） | ＋52 |
| `EMOJI_ICON112`（L34640） | 加 4 個新圖標對照（見 §5） | 1 改 |
| `assets/icons/` | 新增 `icon_gift_pen.png`／`icon_gift_calculator.png`／`icon_gift_watch.png`／`icon_gift_rose.png`（256×256 透明底，見 §5） | ＋4 檔 |
| `tests/test_tang164_static.py` | 新測試 34 項 | ＋143 行 |
| `tests/test_icons112_logic.js` | EXPECT ＋4、欄位值總數 33→37 | ＋4／−3 |
| `tests/test_icons112_static.py` | stem 清單 ＋4、總數 35→39 | ＋4／−3 |
| `tests/test_travel114_static.py` | resync ＋16（見 §6） | ＋18／−15 |
| `qa164/drive164.py`＋`drive164.json` | 實駕腳本＋結果（DOM 證據；截圖剔走，見 §7 尾） | 新 |

`git diff --numstat`：index.html ＋74／−6；其餘三測試檔如上。index.html 現 5,234,752 bytes。

### `applyTangGift164()`（載入正規化，跟 loc96／normaliseTangStub152 先例）
檔尾函數，refreshCopyPacksFromDisk 嘅 giftPrefs 賦值行呼叫（function declaration hoisting，檔尾定義都用到）：
1. prefs：`GIFT_PREFS.npcs.tang.likes = ["gift_fountain_pen","gift_desk_calculator","gift_dress_watch"]`；`dislikes = ["gift_rose_premium"]`（咖啡豆刻意唔入，見 §1.2）。
2. 貨品：`GIFT_ITEMS.items` 注入四件（名／emoji／分類／rarity／價錢／tags／`deltaRel {default:1, liked:2, disliked:-1}`／`unlock {week_min:1, fame_min:0}`），已存在唔重複加（冪等）。
3. 上架：`shop_street_mk` stock 注入四格（2／2／1／2，每週補貨）。
4. 舊檔補格：`S.giftMeta.shopStock.shop_street_mk` 缺嘅四格補返滿數——否則同週內已有 shopStock 嘅舊檔要等下星期先見到貨（`restockIfNeeded` 同週唔重建）。

## §3. UI 入口選擇理由

**揀咗：事務所地點板加「送禮：鄧麗萍」掣，見面後（`flag_tang_open`）先出，行現成 `openGiftPick("tang", L)`。**

- 事務所係佢唯一出現場合（meet／push 掣都喺呢度，§1.5）——送禮掣跟埋同一版面，玩家識咗佢之後自然見到，唔使估。
- 唔行 `addLocTalkGiftActs`：嗰個 helper 要地圖 NPC id 再經 `MAP_NPC_TO_KEY` 查 romance key；tang 唔係地圖 NPC，硬加對應會將佢寫入「傾談／送禮熟人」嗰套地圖 NPC 語義，唔啱。`openGiftPick` 本身只認 npcKey，唔使經嗰層。
- 唔開新地點、唔開新一套送禮流程（任務明令），掣嘅 hint／badge／優先級沿用現成 `giftHintLabel`／`giftGateBadge` 同「庫存空／今日已送都出掣、撳落去先 toast」嘅慣例。
- 見面前唔出掣（唔係出鎖住掣）：見面本身就係發現路徑（約談掣），未見過佢嗰陣出個鎖住嘅送禮掣只會令人困惑；`canGive` 嘅 `tangLocked` 文案留返做第二道防線。
- 副標＋結果行要講明唔加關係（見 §4）：揀禮物頁 tang 副標改做公事版，結果行唔再出「好感 ±0」——否則 UI 自己講大話（話一星期最多 +2 好感，但實際 +0）。

## §4. rel 問題結論

**現行送禮機制會加 `rel_tang`**——`giveGift` 經 `StoryOC.bumpRel("rel_tang", applied)` 加去 `S.story.rel`。`rel_tang` 唔係感情 rel，係**排片線生意閘門貨幣**（push1 要 ≥2，見 §1.6），亦唔係 S.npcs 傾談好感嗰套。

**處理：鄧麗萍送禮 delta 強制 0**（`giveGift` 入面 `applied = (npcKey==="tang") ? 0 : rawDelta`）：
- liked（＋2）／neutral（＋1）／dislike（−1）一律唔郁 `rel_tang`——送禮唔會推進排片線，亦唔會扣減見面攞返嚟嗰 +1。
- `weekGiftGain` 唔累積（applied 唔係 >0，唔入軟上限邏輯）；`lastGiveDay` 照寫（每日 1 次照計）；`givenCount` 照計（重複減半對 tang 冇實際影響，因為 applied 已經係 0）；庫存照扣（同其他 dislike 一致——玫瑰句話「花我不收」但件貨照扣，係通用機制嘅 pre-existing 行為，Vera 嘅「拿回去吧」都一樣，呢票唔改）。
- UI 誠實化：揀禮物頁副標＋結果行「排片關係不變」講明，唔再出「好感 ±0」／「一星期最多 +2 好感」。
- 感情線守門：`tang_commit`／`R_tang_ending`／HE／BE 繼續零引用；`MAP_NPC_TO_KEY` 唔郁；玫瑰繼續係純公事拒收（live TEXTFIX 版：「玫瑰？呢度係排片部，唔係花店。想傾檔期，帶數據嚟。」）；`relMap` 冇 `rel_tang`（v152 已刪）。
- 殘留缺口（唔喺呢票修，見 §1.6）：push1 喺 live 到唔到（`rel_tang` 見面後停喺 1）。送禮唔補呢個缺口——補咗就係用錢買閘門。

## §5. 圖標組附帶工作（全套跑出嚟嘅回歸）

新貨四隻 emoji（🖊️🧮⌚🌹）一加，`tests/test_icons112_logic.js` 即 FAIL——佢窮舉全檔 `icon:`／`emoji:` 欄位值，要求每隻都有 `EMOJI_ICON112` 對照（33→37）同對應圖檔。按 v112／v128 A5 先例補齊，唔係放寬測試：
- 生成 4 隻新圖（`qa164/icons_raw/` 留底原圖，media pipeline 以 `icon_gift_perfume.png` 做風格參照出圖）→ PIL 轉換：去白底（白→透明，墨色統一 `#3a2e22`）、內容最長邊縮到 228px 置中 256×256 透明底（同現有 8 隻禮物圖同一 framing）。QC：四隻 256px 下都讀得清主體（筆斜放連筆尖／計數機顯示＋4×4 掣／腕表圓面＋錶帶／三枝玫瑰紮埋），24px 退化程度同已批核樣本一致。
- `EMOJI_ICON112` 加 `"🖊️":"gift_pen", "🧮":"gift_calculator", "⌚":"gift_watch", "🌹":"gift_rose"`（逐 byte 核實同 item emoji 一致：🖊️＝U+1F58A＋VS16、🧮＝U+1F9EE、⌚＝U+231A、🌹＝U+1F339）。
- `test_icons112_logic.js`：EXPECT ＋4、欄位值總數 33→37；`test_icons112_static.py`：stem 清單 ＋4、總數 35→39。兩檔皆 PASS。

## §6. 行號漂移／resync

- 同行改動（零漂移）：giveGift、loader 呼叫、openGiftPick、doGiveGift、inv72、EMOJI_ICON112。
- ＋16 行：事務所掣一段（舊 L53764–53779）。`test_travel114_static.py` 免費／計數清單行號 ＞53763 者 ＋16——`/tmp/resync164.py` 單次掃描 dict 查表（跟 AGENTS.md v160 教訓，唔逐對 re.sub）：15 個錨點內容逐行相同、零 mismatch，25 個插入點以下錨點不變；COUNT 13／FREE 27 不變，DEF 53425／WRAPPER 44029 不變。
- ＋52 行：檔尾 `applyTangGift164()`（L58777 起）——喺 `runSoftP0Checks` 測試區之後，travel114 唔受影響；`test_tang152` 釘行（25696／31316／31460）全部喺插入點之前，唔使 resync。

## §7. 測試結果

### 新測試 `tests/test_tang164_static.py`：34/34 PASS
斷言：SAVE key／softRev／?v= 不變；接線（函數在位＋同行呼叫）；prefs 覆寫（三件 liked＋玫瑰 dislike＋咖啡豆唔入 likes）；貨品注入（價錢＋上架數＋舊檔補格＋冪等）；圖標對照＋四隻圖檔齊；giveGift tang 專例；UI 入口（事務所掣＋見面閘＋副標＋結果行＋庫存提示）；pack JSON 守門（`gift_prefs.json` tang 仲係空、見面閘留返、`items_gifts.json` 仲係 10 件、`shops.json` 仲係 10 格、反應句 id 對得上、咖啡豆冇 `:liked` 句）；感情線守門（commit／ending／HE／BE 零引用、閘門唔郁、MAP 唔郁、tangLocked 文案在位）。
**反證**：對 pristine（`222a984`）跑，16 項新行為斷言乾淨 FAIL、16 項守門 PASS（JSON／感情線守門喺 pristine 都 PASS 係預期——佢哋守嘅係「pack 冇郁過＋v152 已經清乾淨」；「咖啡豆唔入 likes」喺 pristine 係空函數體下嘅空泛 PASS，實質約束靠工作版嗰次）。全程唔 crash。

### 全套 A/B（`qa131/run_suite.sh`）
- 基線（改之前，`222a984`）：**217 PASS／12 FAIL**（FAIL＝flash51／giglib36／pacing35／poster59／rumor49／slot50／soft_tip_111_restore／start53／weave43／weave44／weave49／wrap38，全部 pre-existing）。
- 工作版第一次：217／13——多咗 `test_icons112_logic.js` FAIL（§5 新 emoji 未入對照表），其餘 12 同基線一致。
- 工作版最終（圖標補齊後）：**218 PASS／12 FAIL，FAIL 集同基線逐項一致，零回歸**（＋1 係新測試 `test_tang164_static.py` PASS）。再跑多一次確認：同樣 **218／12**，FAIL 集 md5 同基線一致，數字穩定。
- 相關測試逐個直接覆驗：`test_tang164_static.py` 34/34、`test_tang152_static.py` ALL PASS、`test_travel114_static.py` PASS、`test_icons112_logic.js` ALL PASS、`test_icons112_static.py` ALL PASS。主 script `node --check` SYNTAX-OK。

### 實駕 `qa164/drive164.py`：7/7 PASS，0 pageerror
本地鏡像（port 8164）＋Playwright（`?softPreview=1&softBehaviorGate=1`），結果 `qa164/drive164.json`。**截圖問題（已證實，唔係遊戲 bug）**：`qa164/shots164/` 8 張圖全部同一個 md5（`11dbb68ed14aacb604e6571407161866`，一格 魏詠男 故事畫面），同 DOM 狀態完全唔符——已獨立重現：新開 browser、播完 meet、開事務所、sheet on＋送禮掣在位，截出嚟依然係同一個 md5；`full_page`／`animations="disabled"`／CDP `fromSurface:false`／rAF pump＋改 opacity 全部同一個 md5；但故事 modal 播緊嗰陣截圖係新鮮嘅（probe A/B md5 唔同、畫面啱）。結論：呢個 chrome-headless-shell build 喺靜態 DOM 畫面（地圖／地點板／送禮 modal）唔出新 compositor frame，截圖永遠係首格殘影；故事 modal 有動畫 loop 先會更新。**所以 8 張圖已由 commit 剔走，唔當證據**；本票實駕證據全部係 DOM 層（modal innerText、掣清單、state probe、庫存／金錢數字），唔受影響。設計 review 要目視畫面嗰陣，要用返完整 Chromium（唔係 headless_shell）重截。
- **T0 載入注入**：packs 載入後 likes＝[名筆，計數機，腕表]；prefKind：筆／計數機／腕表 liked、玫瑰 dislike、咖啡豆／拍紙簿 neutral；四件新貨入咗 `shop_street_mk`；見面前 `canGive('tang')`＝`{ok:false, reason:"院線那邊，還未到送禮的時候。"}`。
- **T1 meet→送禮掣**：`seed_deng_meet_ready` 播 meet，揀 data 抉擇後 `flag_tang_open=true`、`rel_tang=1`、`R_tang_meet` done；事務所行動表出「送禮：鄧麗萍」掣，約談掣消失。
- **T2 UI 送名筆**：真 UI 路徑（掣→揀禮物→確認→送出）：揀禮物頁副標「唔會改變排片關係」、名筆行標記「喜」；結果見 `:liked` 專屬句「名筆。簽名、批檔期、改數字，都用得著。」（live 經 TEXTFIX55，着→著；JSON 原文係「着」）＋「排片關係不變」；`rel_tang` 維持 1；庫存名筆 2→1；撳「關閉」travelFree 返事務所。
- **T3 UI 送玫瑰**：結果見新公事拒收句「玫瑰？呢度係排片部，唔係花店。想傾檔期，帶數據嚟。」＋「排片關係不變」；`rel_tang` 維持 1（−1 唔扣）；唔見「綁架我的情緒」／「感情條款」。
- **T4 UI 送咖啡豆**：結果見 `:neutral` 專屬句「咖啡豆……夜更對帳用得著。放那邊，我自己煮。」＋「排片關係不變」；`rel_tang` 維持 1。
- **T5 買貨**：廟街禮品檔買到名筆（$550），庫存 0→1，存款 $10,000→$9,450。
- **T6 排片線照行**：`seed_deng_push_ready`，事務所 push2 掣「午夜場後的試探」＋送禮掣並存；撳 push2 播到 `R_tang_push2` done（`R_tang_push1`／`push2` 皆 done），新掣冇干擾舊掣。
- 注意：T2／T4 初版斷言用咗 JSON 原文「得着」，live 實測係 TEXTFIX55 改寫後嘅「得著」——已將 drive 斷言改返 live 字眼，唔係改遊戲。

## §8. 殘留問題／跟進

1. **咖啡豆 liked 句缺**（§1.2）：要四件齊 liked，先要一條新嘅咖啡豆 `:liked` 句（＋放入 `gift_react_copy.json` byKey／entries 或覆寫注入）。等用戶／統籌決定寫唔寫，唔喺呢票自作主張。
2. **push1 live 到唔到**（§1.6）：見面後 `rel_tang` 停喺 1，push1 閘門要 2，live 無其他 +1 來源（stub 唔播）。pre-existing，唔喺呢票修；送禮刻意唔補呢個缺口。
3. **玫瑰「花我不收」但件貨照扣**：通用機制（dislike 照扣庫存），Vera 同病。唔喺呢票改。
4. **主 script 係 IIFE**：`openGiftPick`／`saveQ()` 等唔係 global——實駕行 UI 路徑驗證，唔經 global 呼叫（`GiftShop` 係 `window.GiftShop`，T0 邏輯探針先用佢）。
5. **headless_shell 截圖殘影**（見 §7 尾）：靜態畫面截圖全部同一個 stale frame；本票視覺證據係 DOM 層，唔係圖。設計 review 要重截畫面請用完整 Chromium。

## §9. Rebase 紀錄

- 開工基底：main `222a984`（v152 NOTES；遊戲 commit `40702c7`）。
- 工作期間 main 郁咗：**v160 於 2026-11-13 09:30 落地**（main `109422b`，NOTES `276ffa1`，線上 5,213,030 bytes sha `f7010c90…`；全套 rebase 後 221／12）。本分支**未 rebase**（任務話唔落地）——**落地嗰陣要 rebase 上 `109422b`**（或當時最新 main），留意 v160 喺 L802 附近插咗 CSS 令 kwan151／tang152 釘行 ＋5，本票嘅行號（§6）要再對一次；travel114 嗰 15 個錨點亦要再核實。
- 本票內部冇 rebase；`git rebase --continue` 冇用過；新檔案全部 `git add <path>` 明確加。
- Commit（分支 `v20a164`，未 push）：`v20a164: 鄧麗萍送禮補完（prefs 覆寫＋四件新貨上架＋事務所送禮掣＋rel_tang 唔加分＋4 隻新圖標；新測試 34 項＋實駕 7/7；全套 218／12 零回歸）`——見下節。

## §9b. 統籌 rebase 紀錄（落地前）
- Rebase 上 main `276ffa1`（v160 NOTES；遊戲 commit `109422b`）：`index.html` 自動合併，diff 改動行數 80 行同原分支完全一致（純漂移）；唯一衝突 `tests/test_travel114_static.py`——v160 同 v164 各 resync 一次，統籌用單次掃描 dict 查表合併（HEAD＝v160 編號，行號 ＞53879 者 ＋16，DEF 53540／WRAPPER 44034 唔郁），`test_travel114_static.py` 重跑 PASS（COUNT 13／FREE 27 不變，全部錨點內容核實）。
- Rebase 後重驗（最終樹 `663b67c`）：新測試 tang164 34/34、tang152／travel114／icons112 logic＋static／kwan151 全部 PASS、主 script `node --check` SYNTAX-OK、全套 **222／12**（v160 基線 221／12＋1 新測試；12 項 FAIL＝flash51／giglib36／pacing35／poster59／rumor49／slot50／soft_tip_111_restore／start53／weave43／weave44／weave49／wrap38，逐項同基線一致，零回歸）、實駕 `qa164/drive164.py` 重跑 **7/7 PASS、每項 0 pageerror**（T0–T6 全部 True）。
