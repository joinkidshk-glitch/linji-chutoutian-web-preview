# NOTES_V20A204 — 補女星入獎池（音樂＋電影優先）＋提名人性別分流

## §0 設計（統籌 2026-11-14 12:13 定，寫死）

### 背景（已核實）
- 12 紅星得 4 女：蘇芷茵、鍾楚凝、魏詠男、葉敏芝；其餘 8 男。
- `AWARDS63_POOL`（index.html L47817 起）：電影 6 池得 1 女（魏詠男）、電視 4 池得 2 女、**音樂 3 池得 0 女**、廣告 5 池得 3 女。15 個獎有 7 個女獎。
- 玩家（男）永遠入唔到女獎池——code 註解（L45997）：女獎只係典禮獎項表嘅完整 slate。
- **機制漏洞**：`buildAwardResultPack` 將同一份 fellows 名單貼落 pack 入面所有類別，winner63＝fellows[0]。旁聽模式（tier gallery）eligible 係空，pool188 跌返全表，抽中女獎類別嗰陣得主就係名單第一個，可以係男星——機制上「廖炳星攞最佳女主角」會發生，未喺實玩證實過。
- 整體 31 人名冊女角 12 個，問題集中喺獎項用得著嘅女星得 4 個。藍若曦本身係玉女歌手但唔喺獎池。

### 決定 1：藍若曦升格入音樂池
- **藍若曦入音樂池**（唔係全新創作）。理由：佢已經係玉女歌手（cast_main brief），有全身圖 6 張（`assets/story/fullbody/lan_ruoxi_*.webp`：base／sad／serious／shy／smile／think），升格成本最低。
- **感情線唔郁**：獎池唔掂 `S.story.rel`；佢攞最佳女歌手同佢感情弧線（玉女歌手上位）一致，唔衝突。
- 要補：`POSTER59_STAR_IDS`「藍若曦」→`lan_ruoxi`、`AWARDS63_POOL.music` 加 `lan_ruoxi`、`AWARDS63_TIER_WEIGHT` `lan_ruoxi: 3`（巔峰 1991，按 1990–92＝×3 規則）、PixelLab character ＋ `px_lan_ruoxi_{east,south,west}.png`。

### 決定 2：新創 2 位女星（共 3 人入池，女星 4→7）
- **沈映雪**（`shum_yingsuet`），約 27，女，**音樂池**。archetype：抒情歌后，情歌唱到街知巷聞，唱腔細膩帶鼻音，碟市長青。巔峰 1990 → weight ×3。
  - 樣貌 brief（跟 `PLAN_CHAR_LOOKS_REF_v1.md` era_stars 格式）：鵝蛋面，眉眼溫婉，眼尾微垂，唇形飽滿，長直黑髮及肩，妝容清淡。服裝：淺色針織開襟衫配長裙，或白色恤衫配高腰長褲，珍珠耳環——90 年代初玉女歌手與實力唱將之間嘅氣質。出圖筆記：Bust shot；溫柔淺笑，眼神柔和，頭微側。
  - 靈感對照（DEV only，玩家面永禁真名）：90 年代初抒情歌后 archetype，唔指名任何真人。
- **江詩盈**（`kong_siying`），約 24，女，**電影池**。archetype：文藝片女主角，氣質冷冽，演技細膩，影展常客，新晉影后大熱。巔峰 1992 → weight ×3。
  - 樣貌 brief：面型偏方帶高級感，五官立體，眼大有神，鼻樑高挺，短髮齊耳或低馬尾，妝容偏淡。服裝：黑色高領冷衫配長褲，或絲質連身裙配西裝外套，簡約冷色調。出圖筆記：Bust shot；眼神冷靜帶距離感，嘴角微抿。
  - 同鍾楚凝區分：鍾楚凝＝成熟嫵媚大青衣（濃妝紅唇）；江詩盈＝年輕文藝冷面（淡妝短髮）。唔好畫到撞款。
  - 靈感對照（DEV only，玩家面永禁真名）：90 年代初文藝片女主角 archetype，唔指名任何真人。
- 名／id 撞名檢查：沈映雪、江詩盈、shum_yingsuet、kong_siying 全部唔撞現有名冊（31 人＋12 星＋11 老闆＋鄧麗萍）；實作嗰陣再 grep 核實一次。
- 入池後：music `[lok_gasing, gu_mingfai, liu_bingxing, lan_ruoxi, shum_yingsuet]` ＝ 2 女／5；film `[luk_baakyin, liu_bingxing, mak_zhendong, chai_zanhoi, lok_gasing, ngai_wingnaam, kong_siying]` ＝ 2 女／7；tv 2 女／4、ad 3 女／5 不變。
- 每位新星要補：`POSTER59_STAR_IDS` 名→id、`AWARDS63_POOL`、`AWARDS63_TIER_WEIGHT`（兩位都係 ×3）、PixelLab character ＋ px 三向圖。**唔改 `LEADSTAR59`**——新星冇作品，唔可以扮做現有通告嘅主演；新星只經第二輪（加權隨機）入 fellows。

### 決定 3：Scope 底線
- 入獎池＋有樣（PixelLab character＋舞台 px 圖＋名牌顯示）＋性別分流。**巧遇內容／支線／感情線唔入呢票**。
- 新星唔上對話舞台（冇巧遇），**唔使全身圖**；藍若曦已有全身圖，唔使重做。寫清楚，唔好多做。
- 女星名牌顯示：名要喺提名行／結果卡／報紙正確顯示（`awards63StarName` 經 `POSTER59_STAR_IDS` 反查，補咗對照就得；實作嗰陣 grep 所有 starId→名嘅表，唔好漏）。

### 決定 4：性別分流設計
- 新加女性 id 集（例如 `AWARDS204_FEMALE_STARS`），7 位女星 id：`so_jiyan`、`chung_choning`、`ngai_wingnaam`、`yip_manji`、`lan_ruoxi`、`shum_yingsuet`、`kong_siying`。預設男，唔使列男表。
- `awards63Fellows(ceremony, year, gender)`：第三參數可選（`""`／唔傳＝唔過濾，舊行為不變，舊 call site＋舊測試唔爛）。
  - 第一輪（真主演按片酬）：候選星性別要啱 `gender` 先入。
  - 第二輪（加權隨機）：pool 先按性別過濾再抽。
  - 高俊傑特別名額（v178 第三步，男）：只可以入男獎／混合類別，唔可以入女獎。
  - seed 要加埋類別 id（或 gender），每類別獨立可重現，唔好男女共用同一隨機序列。
- `buildAwardResultPack`：逐個類別計 fellows（`c.fellows63 = awards63Fellows(ceremony, year, c.gender || "")`），唔再全 pack 共用同一份。winner63／gallery 得主（fellows[0]）自動跟住啱性別。
- 最佳新人獎（gender `""`）：唔過濾，男女混合不變。
- 防守：過濾後池空（理論上唔會，呢票之後女池最少 2 人）→ fellows＝[]，唔 crash；單元測試要覆蓋呢個邊緣情況。

## §1 實作（工人填）
（工人 2026-11-14 完成，分支 `v20a204`，基底 main `6e45cdb`）

### 改動清單（index.html，＋53／−21，淨 ＋32 行，總行數 61167→61199）
- `POSTER59_STAR_IDS`（L32519 起）：加「藍若曦」→`lan_ruoxi`、「沈映雪」→`shum_yingsuet`、「江詩盈」→`kong_siying`。名／id 撞名再 grep 核實：三名＋三 id 喺 31 人＋12 星＋11 老闆＋鄧麗萍名冊零撞（改前 index.html／content／docs 全庫 0 命中）。
- `AWARDS63_POOL`：music 加 `lan_ruoxi`、`shum_yingsuet`（→2 女／5），film 加 `kong_siying`（→2 女／7）；tv／ad 不變。
- `AWARDS63_TIER_WEIGHT`：新三位都係 ×3（巔峰 1990–92 規則）；舊 10 星權重一字不變。
- 新增 `AWARDS204_FEMALE_STARS`（7 位女星 id）＋ helper `awards204StarGender(starId)`（女→"f"，其餘→"m"，唔使列男表）。
- `awards63Fellows(ceremony, year, gender, catId)`：第三參數 gender 可選（"m"／"f"／""／唔傳＝唔過濾）、第四參數 catId 可選。
  - 第一輪真主演：性別唔啱跳過（`genderOk204`）。
  - 第二輪池抽：pool 先按性別過濾再抽（過濾後池空→`awards63WeightedPick` 返 ""，fellows＝[]，唔 crash）。
  - 高俊傑特別名額（v178，男）：`gender !== "f"` 先入，唔入女獎。
  - seed：舊式呼叫（唔傳 gender／catId）沿用舊三元 seed `[year, id, medium]`，抽籤結果同舊版逐字一致（舊 signature 行為不變，v178 測試零改動照 PASS）；傳咗 gender／catId 先加落 seed——每類別獨立可重現，男女唔共用同一序列。
- `buildAwardResultPack`：類別物件加 `gender: cat.gender||""`；逐個類別計 fellows（`awards63Fellows(ceremony, year, c.gender || "", c.id)`），唔再全 pack 共用同一份。winner63／gallery 得主（fellows[0]）自動跟住啱性別；新人獎（gender ""）混合不變。
- 註解更新（唔改行為）：AWARDS63 區「紅星池 10 位」→13 位；v186 結果卡「各類共用同一份名單」→每類各自一份；v181 預載「12 人 × 3 向」→15 人 × 3 向。
- 唔郁：`LEADSTAR59`（新星只經第二輪入 fellows）、SAVE key（`starVolunteer_map_v19w`）、softRev（s107）、`?v=`（v20a10）、content pack JSON（零直改）。

### PixelLab 美術（3 位 × create-character-v3，1 call＝3 次，共 9 次）
- 餘額：開工前 3,973.67／5,000 → 完成後 3,964.67／5,000（Tier 2 Pixel Artisan，active）。
- 藍若曦 `b65c7069-1b7b-4a3f-b32d-c51b0064114e`（job `e2826990`）；沈映雪 `7dfc9968-258a-4caf-a841-b04b1cff5bc2`（job `c6633462`）；江詩盈 `b8b1ec05-322c-4690-ae68-f4a0549f02e9`（job `fa97c362`）。body 格式跟 v170 廖炳星樣本（128×128、8 方向、`view: side`、`template_id: mannequin`、`no_background: true`）；prompt 用 NOTES §0 brief＋官方風格錨文字（乾淨二次元動畫風，平塗賽璐璐、清線條、大眼少年感），零真人姓名。
- 三向圖下載：`get-character` 嘅 `rotation_urls`（south／east／west）經 curl 下載（urllib 連續 IncompleteRead，轉 curl --retry 先掂；參見 `samples204/fetch204.py`）。
- 正規化（`samples204/fetch204.py`，NEAREST）：原圖 alpha bbox 高 121–124px、腳底貼畫布底邊（y128），逐張 scale 到高 102px、腳底 y115、橫向置中——同現有 12 人錨一致（128×128、bbox 高 102、底 y115）。9 檔全部驗收通過。
- 目視驗收（`samples204/compare204.png`，4x）：藍＝白蕾絲荷葉邊裙＋珍珠耳環＋及腰黑長直髮＋酒窩淺笑，啱 brief；沈＝淺色針織開襟衫＋長裙＋及肩直髮＋溫婉淺笑，啱 brief；江＝黑高領冷衫＋長褲＋齊耳短 bob＋冷面，啱 brief，同鍾楚凝（濃妝紅唇大青衣）零撞款。藍條裙係及地長裙，裙襬喺腳底線，唔係裁斷（同鍾楚凝長裙拖底同理）。
- 新星 px 檔（9 檔，`assets/story/awards/`）：`px_lan_ruoxi_{south,east,west}.png`、`px_shum_yingsuet_{south,east,west}.png`、`px_kong_siying_{south,east,west}.png`。舞台 `loadPx(f.starId, d)` 按 fellow starId 逐個載，唔使另加對照——新星自動搵到圖（實駕 resource timing＋截圖核實）。
- 殘留觀察（唔係問題）：三位原圖腳底全部貼住 128 畫布底邊（舊 10 位原圖腳底 y114–118，有約 10px 邊）；正規化後已同錨一致，舞台腳底同線，實駕截圖核實。

### 測試檔改動
- 新：`tests/test_awards204_logic.js`（25 項）、`tests/test_awards204_static.py`（21 項）。
- 改：`tests/test_awards63_logic.js`——加權分佈期望跟池變（TIER_TOP147 加新三位；理論值 film 12/17≈71%／music 12/13≈92%，tv／ad 不變；「權重表齊晒池內 10 星」→13 星；斷言邏輯本身唔變，性質照舊）。
- 改：`tests/test_awards63_static.py`——fellows 簽名斷言跟新簽名（`function awards63Fellows(ceremony, year, gender, catId)`）。
- Resync（`qa204/resync204.py`，git diff hunk 對位＋逐粒內容逐字核實純漂移，單次掃描替換）：6 檔釘行測試（gift185／rom176／tang171／tang173／text125／travel114；COUNT 12＋FREE 33＋DEF＋WRAPPER 全數核實）。註：resync 途中撞過兩鑊——(a) 腳本入面 `\\n` 轉義層數錯（寫入檔變 4 個 backslash，改用 chr(92) 計數修正）；(b) travel114 FREE 區註解有 `{travelFree}` 個 `}`，`[^}]*` 截 block 截錯，改逐行抽獨立數字行。兩鑊都已修正，resync 通過。

## §2 驗證（工人填，統籌獨立重驗）
（工人 2026-11-14）

### 新測試＋反證
- `node tests/test_awards204_logic.js index.html`：**25/25 PASS**（池組成／權重／名反查／第一輪分流／第二輪分流／女獎零高俊傑 96 組合／新人獎混合／舊 signature 同一結果／(gender,catId) 可重現／過濾後零候選→[] 唔 crash）。
- `python3 tests/test_awards204_static.py index.html`：**21/21 PASS**（入池／女性集／簽名／三處性別閘／逐類別計／新星 px 9 檔齊＋錨尺寸／硬規則 SAVE／LEADSTAR59／softRev／?v=）。
- 反證（pristine main `6e45cdb`，`/tmp/pristine204.html`）：logic 乾淨 FAIL 25 項 exit 1（抽唔到 `AWARDS204_FEMALE_STARS` 即逐項 FAIL，唔 crash）；static FAILED 16（其餘 5 項係舊有內容，照 PASS）。
- 舊測試覆驗：`test_awards63_logic.js` ALL PASS、`test_awards63_static.py` ALL PASS、`test_awards178_logic.js` ALL PASS、`test_awards178_static.py` ALL PASS、`test_awards181_static.py` ALL PASS（px 36 檔舊檢查唔受新檔影響）。

### 全套 `qa131/run_suite.sh`
- 跑 A（resync 前）：279/19——多 6 項係行號漂移（見上 resync 清單）。
- 跑 B（resync 後，`qa204_suite_workB.txt`）：**285 PASS／13 FAIL**。FAIL 清單同基線 283/13 逐項一致（flash51／giglib36／pacing35／poster59／rumor49／slot50／soft_tip_111_restore／start53／weave43／weave44／weave49／wf5_87／wrap38——全部 pre-existing），**零回歸**；＋2 PASS 係新嘅兩個 v204 測試檔。

### 實駕（LIVE 裸 URL，本地鏡像＋`python3 -m http.server`，唔用 `?softPreview=1`；Playwright venv `/home/hatch/pwenv49/bin/python`，瀏覽器 `/home/hatch/.cache/ms-playwright/chromium_headless_shell-1248/...`——任務寫嗰條 `/home/hatch/pw-browsers/...` 執行檔已失蹤，改用 v193 同款新下載路徑）
- 腳本 `qa204/drive204.py`（重用 qa188 drive helper：新遊戲 UI＋in-page seed＋`debugForceSeasonWindow` 建 pack 實路徑＋出席播典禮），報告 `qa204/drive204.json`，截圖 `qa204/shots204/`。
- **8/8 PASS**（音樂＋電影 × 提名／旁聽 × 932／700）：
  - 音樂提名 1990（932／700）：男歌手類別 fellows 全男（駱家聲／齊鎮海／廖炳星）＋得主男；新人獎有 fellows（混合）。
  - 音樂旁聽 1991（932／700）：最佳女歌手 fellows 全女——**藍若曦《三年》＋沈映雪《同場》**，得主女（藍若曦）；結果卡有齊兩人名；報紙頭版「星河金碟夜 藍若曦憑《三年》奪獎」。
  - 電影提名 1990（932／700）：男配角 fellows 全男（陸柏言／廖炳星／麥震東）＋得主男。
  - 電影旁聽 1991（932／700）：最佳女配角 fellows 全女——魏詠男《離岸的信》＋**江詩盈《半張船票》**，得主女；結果卡有江詩盈名；報紙頭版印得主魏詠男。
  - 舞台：6 場出席全部 stage 出現＋播完消失；唱名字幕唱出提名人；每位 focus 提名人嘅 `px_<id>_south.png` 全部有請求＋200；目視截圖核實——金碟夜舞台藍＋沈企埋一齊（白蕾絲裙／針織開襟衫，腳底同線），影藝獎舞台江詩盈（黑高領短 bob）企阿偉側邊，932／700 一致。
  - 舊 10 星照常出現（提名場 fellows 全部舊星；新星淨喺女獎第二輪出現，符合設計）。
  - 全程 0 pageerror／0 requestfailed。
- 途中修正過兩項 harness 誤判（唔係遊戲 bug，記錄喺度等統籌知）：(a) 舞台人物係 canvas 畫，唔係 `<img>`，初版用 `.awd63-card`／stage img 驗 px 係空驗——改用 resource timing＋截圖；(b) 提名場報紙係「入圍名單」印玩家名，唔印對手得主——初版驗得主名係錯期望，改做 tier-aware（gallery 驗得主名、提名驗玩家入圍名）。probe（`qa204/probe204.py`）另有全表：music/film/tv/ad × 1990–92 × f/m/mix 共 36 組 fellows，女獎零高俊傑、男獎全男、新人獎混合，全部同邏輯測試一致。
- 未驗（留統籌）：tv／ad 女獎類別實駕（邏輯層已覆，probe 全表已驗，典禮場次集中音樂＋電影優先，按設計）；第三年贏獎線實玩校準（唔喺呢票範圍）。

## §3 落地（統籌填）
（待填；注意 v203 而家做緊，落地前要 rebase 上最新 main 再重驗）

## §4 補充 — 新女星設計圖 v4（主助手 2026-11-14 13:22–13:24，用戶反饋後修訂）
- 用戶話 v1–v3 設計圖「不太像明星」，要求上網查當年香港女明星做參照。已查：林憶蓮《都市觸覺》時期（俐落西裝剪裁、黑白灰、蓬鬆短髮、淡雅妝）【Tatler】；張曼玉 1992《阮玲玉》柏林影后、經典短髮造型【東方新地／laitimes】。**參照只限風格 archetype，唔抄任何真人塊面，prompt 同 BRIEF 永禁真人姓名**（玩家面永禁真名，DEV 內部討論除外）。
- v4 新造型（BRIEF.md 已更新，設計包 `grok-characters-v204-v4.zip`）：
  - 沈映雪：摩登都會女歌手 — 修身黑西裝褸＋白恤衫＋高腰米色闊腳褲、蓬鬆短捲髮、淡雅妝、自信微笑（v3 圓面＋露齒笑太甜，唔似歌后）。
  - 江詩盈：文藝片女主角 — 經典直短髮齊顎側分、淺灰高領＋黑闊腳褲＋幼皮帶、淡雅妝、冷靜優雅（v3 低馬尾＋墨綠太隨意；直短髮＋淡妝＋簡約衫同 Vera 微捲 bob＋煙燻妝＋黑西裝分清）。
- v2／v3 設計圖已移去 `~/workspace/linji-work204/designs-v1-superseded/`（`_v2`／`_v3` 後綴）；工人直出嗰 2 隻 character（照 v1 brief）已作廢，照舊。grokbot 出圖後比較／換入：沈／江各 3 向 px 圖（分支內現有 6 檔照 v1 brief 出，要換）。
- 交付教訓：同一 `sandbox://` 路徑重用三次發圖，app 緩存令用戶見到舊圖——v4 起改用新檔名／新路徑（`grok-characters-v4/*_v4.png`、`grok-characters-v204-v4.zip`）。
- v5（2026-11-14 13:27，用戶話江詩盈衫色改一改好啲）：江高領由淺灰改暖駝色＋黑闊腳褲，塊面／髮／剪裁不變；設計包 `grok-characters-v204-v5.zip`（沈 v4＋江 v5），v4 江圖已移去 `designs-v1-superseded/kong_siying_design_v4.png`。
- **改名（2026-11-14 13:30，用戶拍板：第二個人名唔要有雪字）**：江雪盈 → **江詩盈**（`kong_sutying` → `kong_siying`）。改咗：index.html（POSTER59_STAR_IDS／AWARDS63_POOL／權重／註解）、3 個測試檔、qa204 harness（drive204.py／probe204.py）、samples204（fetch204.py／body.json／3 張 raw 圖）、3 張 px 資產檔（`px_kong_siying_{south,east,west}.png`，stage loader 按 starId 載圖，唔改名會 404）、NOTES §0＋BRIEF＋設計圖檔名＋設計包（`grok-characters-v204-v6.zip`）。改名前 grep 核實江詩盈／kong_siying 零撞名；改名後 v204 測試＋awards63 測試重跑全部 ALL PASS。**注意**：qa204/drive204.json＋shots204 截圖係改名前嘅驗證證據，入面仲係舊名，屬歷史記錄唔改；實駕重驗留待落地 rebase 後由統籌做。
- **藍若曦改版（2026-11-14 13:38–13:45，用戶拍板 v7）**：用戶話舊造型同蘇芷茵太似，要陽光啲。v2 高馬尾＋黃上衣＋白百褶裙（畫風唔似）→ v3 照原本圖改 → v4 調眼 → 用戶話兩個都唔 ok → v5 修長比例 → v6 陽光眼（有星光）→ v7 去星光版，**用戶 13:45 話「就這個」拍板**。v7：高馬尾＋黃蝴蝶結、鵝黃針織上衣＋白百褶短裙、修長身形、陽光杏眼（普通圓形光點，冇星光）。設計包已更新做 `grok-characters-v204-v7.zip`（3 位角色；BRIEF §3 改寫，舊藍若曦 character 作廢，grokbot 照新設計圖重出；舊設計圖移去 `designs-v1-superseded/lan_ruoxi_design_v1.png`）。**跟進未做**：藍若曦遊戲入面 6 張全身圖（`assets/story/fullbody/lan_ruoxi_*.webp`）要跟新造型重出（v205 已開工）；分支內 `px_lan_ruoxi_{south,east,west}.png` 已換 grokbot 版（見下「grokbot 換圖」一項），唔喺 v205 範圍。
- **grokbot 換圖（2026-11-14 13:51–13:53，用戶 13:52 拍板「換入 grokbot 版」）**：grokbot 3 隻 character 已返，全部 completed、128×128、8 方向——沈映雪 `93835a29`、江詩盈 `d7b11282`、藍若曦 `aa209230`（PixelLab 餘額 3,889.67／5,000，3 隻花咗 75 次）。由 PixelLab 下載每隻 south／east／west 三向 rotation 圖，PIL 正規化到阿偉錨（高 102、頭頂 y13、腳底 y114、橫向居中 x≈63.5），覆蓋分支內 9 檔 `px_{shum_yingsuet,kong_siying,lan_ruoxi}_{south,east,west}.png`。量度：沈 south 103／east-west 101、江 south 103／east-west 101——微調即用得；藍 south 116／east-west 109——縮到 102（同 v170 4 位提名人一樣做法）。9 檔重測全部 128×128、高 102、頭頂 y13、腳底 y114；逐張目視核實跟返設計圖（沈黑西裝＋米色闊腳褲＋蓬鬆短捲髮；江駝色高領＋黑闊腳褲＋直短髮；藍高馬尾＋黃蝴蝶結＋鵝黃上衣＋白百褶裙，冇星光）。工人直出嗰 3 隻 character（沈 `7dfc9968`／江 `b8b1ec05`／藍 `b65c7069`）全部作廢。重跑 test_awards204_logic＋test_awards204_static＋test_awards63_logic 全部 ALL PASS（static 含 px 幾何檢查）。index.html／測試邏輯冇郁。
