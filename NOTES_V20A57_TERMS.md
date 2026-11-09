# NOTES V20A57 — 術語清理（跟 linji-terminology-audit.md A/B/C 三表）

基線 v20a56（4,314,004 bytes）→ v20a57（4,317,038 bytes，+3,034）。
用戶拍板：事態→劇情（2026-11-09）；其餘 A 類直接改、B 類照審計有限度建議、C 類零郁。
硬規則遵守：冇改 pack JSON 原檔（pack 側一律經 TEXTFIX55/57 清洗層）、冇改 SAVE key／softRev／?v=／邏輯／數值。
實作方式：index 側用 JS tokenizer 只改字串字面＋HTML 文字節點（註解、識別子唔郁）；pack 側喺 TEXTFIX55 區塊內加 TEXTFIX57 表＋4 個 hook。

## A 類

### A1 事態→劇情
- index 字串內 **82 處**（頂欄 chip title/aria、選單、地圖提示、picker 全組、手帳標題、教學、結局/報紙「劇情見報」、內嵌自檢 fixture＋斷言同步）。
- HTML 文字節點 **3 處**（tokenizer 掃唔到、另外手改）：頂欄 chip 標籤、主選單掣、地圖圖例。
- 「事態未解鎖」→「劇情未開放」**6 處**（同 B1 合併處理，含 picker fallback 同 gate reason 字串，全檔一致改名，行為不變）。
- 「相遇事態」→「相遇劇情」：index 直用字串 1 處＋pack（gift_react 欄）經 PHRASES。
- pack 側：TEXTFIX57_PHRASES 加 `事態→劇情`，所有 walked 字串（story/tutorial/gig 欄外）自動覆蓋。
- 保留：TUTORIAL_ZH_HK 嘅 `source` provenance 欄（`hard-gate／事態入口`，metadata 永不出街，改咗反而失真）。

### A2 聲量→聲望
- index 字串 **18 處**（主幹 hint、結局文案「幕前聲量」→「幕前聲望」、rival gig 文案等）＋ pack 側 PHRASES 全包覆蓋（pack 出街面本身已零聲量，屬保險）。
- 生造動詞改寫 **14 處**：nodeRipple「揚聲量」→「升聲望」×7、「沉信用」→「跌信用」×6、「沉『惜身』口碑」→「落個『惜身』口碑」×1，逐句順返語法。
- resolveEnding410 嘅 reasons 審計字串（內部、唔出街）一併轉「聲望」保持一致。
- **合法保留**：① 內嵌自檢 QA 探針 `"聲量"` ×9——自檢正係靠佢驗證玩家面零聲量，改咗自檢即失效；② fame 來源比對 alias `which==="幕前聲量"`（內部 code，認舊 pack 標籤用）；③ `openConditionsNote` 兩處「聲量>28／>50」——SKIP_KEY 內部 legacy 對照欄，清洗層本身 skip、永不出街。

### A3 刷新→更新（2 處）
- toast「廣告通告欄已刷新（約兩週一次）」→「廣告通告欄更新咗：有新通告」；連帶 stamp 比對正則 `通告欄已刷新`→`通告欄更新咗`（同新文案保持同一行為，屬文案同步唔係改邏輯）。
- pack 側：「情報刷新，去金龍茶餐廳聽下新風聲。」經 EXACT 改「有新情報，去金龍茶餐廳聽下新風聲。」

### A4 點擊→撳
- index 玩家面唯一出街句喺 v20a55 已修（TEXTFIX55_EXACT value 已係「撳嚟揀都得」）；index 其餘「點擊」全屬註解。**v57 index 零新增改動**；pack 側 PHRASES 加 `點擊→撳` 做保險（教學變體句）。

## B 類（有限度）

### B1 解鎖→未開放／開放咗（index 30 處＋pack）
- index：解鎖手帳「X」→開放手帳「X」×5；UNLOCK_CHARM/IQ 事件句「新課程解鎖」→「新課程開咗」×2；進階演技課／台風課提示 ×2＋魅力／觀察課 fallback ×2；手帳「訓練」已解鎖→開放咗 ×2（頁面＋toast）；「尚未解鎖送禮」→「送禮未開放」；「解鎖後可排入手帳」→「報名後可排入手帳」；好感階梯句「→ 解鎖『X』」→「就開到『X』」×2；「好感解鎖：」標籤→「好感門檻：」；「→ 解鎖第2幕情報」→「→ 會有第2幕情報」×2（引號內行動名原封不動）；trainHint「解鎖訓練」→「報名後可練」；內嵌教學「訓練解鎖試鏡」→「訓練夠先報得試鏡」＋內文 ×3；未解鎖→未開放 ×6（見 A1）。
- pack：TEXTFIX57_EXACT 加 UNLOCK 兩句、教學兩句（連帶有後綴變體共 3 條）、裸值 `"未解鎖"→"未開放"`（story_detail 全部節點 lockedHint 命中）。

### B2 選角標籤：只改兩個值
- 「動作演員」→「身手好」：index **6 處成套**（STORY_GATE_3Y C8/C15 tagAny、GIGS36 tagOnComplete ×3、requiresCastingTagAny ×1）；pack registry（STUB_CASTING_TAGS）經新增清洗步：textfix55Freeplay 載入後 walk registry——label 靠 EXACT 全字串改名、labelToId 靠 walk object-key 改名（TEXTFIX57_KEY_RENAME），id（tag_action/tag_diva）不變。
- 「大牌」→「耍大牌」：index **2 處**（ENDING_NEG_TAGS410、WEAK_MARKS 耳語池）。
- 舊存檔相容：gates 靠 id 命中本來唔受 label 改名影響；顯示經 registry 以 id 對返新 label；另喺 `ensureCastingTagsState` 加冪等遷移，將存檔內舊 label（字串形／object 形）就地正規化，連 ENDING_NEG_TAGS410 嘅 label 命中都唔會失。
- 保留：散文「大牌藝人／大牌檔期／大牌歌手」、對白「唔係大牌」、標籤系統名「選角標籤」本身。

### B3 好感一詞兩制
- 改「關係」（感情線 0–6 階梯語境）：index C5 lockedHint「（好感約到2）」→「（關係約到2）」1 處；pack 側同類句 v55 EXACT 已蓋（「好感大約到3」等）。
- 保留「好感」（/100 傾談／人情計分全系統）：aff-next、人情面板、關係階梯顯示等全部唔郁，只改其中「解鎖」字眼（見 B1），改完兩制唔再撞。
- story pack synopsis「高好感的約會對象」係敘事散文，保留並在此交代。

### B4 體力→體能（只限 gig 列要求語境）
- 走 gig 清洗：textfix55GigField 加 TEXTFIX57_GIG_REQ **13 對** pattern（體力與耐性／水性／節奏感／走位／儀態／專注力／膽量、耐性與體力、體力耐性、體力要求、考驗體力。／，、極考體力），覆蓋 pack 約 155 處要求碎句嘅主要句型；內嵌 fallback gigs 同經 normalizeGigRecord，一律受惠。
- 保留（正貨）：體力消耗、體力極限、保持體力（單獨）、耗體力、體力活、體力勞動、體力關卡；index 唯一「要夠體力」係成句散文 roleHint，保留並在此交代。

### B5 存款／現金（只改付款提示位，3 處）
- toast「現金不足 $…——債項未清。」→「存款不足…」；reason「現金亦不足 $200」×2→「存款亦不足 $200」。
- 保留：付現金 payNote、還款方法散文、「禮物／現金」cost 標籤、「現金 $200 還」掣（審計明示）。

### B6 周刊→週刊（全統一）
- index 字串 **22 處**（《星訊周刊》→《星訊週刊》、周刊小訪→週刊小訪＋內嵌檢查同步、周刊記者／編輯、結局文案）＋ pack PHRASES 全包覆蓋（romance 節點標題/場景、DUAL_MEET、報紙 stub 標題等）。
- speaker registry：保留舊 key「周刊編輯」做 alias，新增「週刊編輯」key 指同一 artId——walk 後嘅新名同未 walk 嘅舊名都 lookup 到。
- TEXTFIX55 既有 **value** 同步 2 處：結局 EXACT 值「娛樂周刊已經寫好」→「娛樂週刊」、RUMORS 值「幫周刊追緊」→「幫週刊」（keys 全部冇郁，見下）。

### B7 成功率→成數（有限度，4 處）
- 說明句「成功率受表現／壓力／信用影響」→「成數受…」×3（var-note ×2＋fallback）；chanceVarianceNote「未齊條件會拉低成功率」→「拉低成數」×1。
- **保留全數數字標籤**「成功率約 X%」「成功率 P%」等 10 處＋壓力後果句「試鏡成功率」——審計只開說明句，數字標籤係玩家決策資訊唔郁，喺度明言取捨。

## C 類
零改動。新 static test 抽查在場：拼合、人情債、手帳、殺青、通告、主線、相遇、剛聽聞等。

## TEXTFIX55 表格完整性
- 所有 TEXTFIX55 表 **key 一字冇改**（region diff 已逐行核對）；只改咗 3 個 **value**：①教學句值「訓練解鎖試鏡；…」→「訓練達標就報得試鏡；…」②結局句值「娛樂周刊」→「娛樂週刊」③RUMORS 值「幫周刊」→「幫週刊」。
- 新增物全部喺 region 內新開 TEXTFIX57 段（EXACT／PHRASES／KEY_RENAME／GIG_REQ）＋4 個 hook（textfix55Str ×2、textfix55Walk key 改名、textfix55GigField、textfix55Freeplay registry 步）。
- index 側新字串同清洗層唔打架：清洗層冇任何規則會將「劇情／聲望／週刊／開放咗／身手好／耍大牌／存款／成數」改返舊詞；唯一相關嘅報紙專用 phrase「幕前聲望→聲望」只行 pack 報紙、唔經 index 字串。

## 舊 test 同步改動（文案釘版，跟 v55 先例）
- `test_weave410_logic.js`：結局總結斷言「幕前聲量」→「幕前聲望」。
- `test_weave410_static.py`：ENDING_NEG_TAGS410 斷言改「耍大牌」版。
- `test_weave46_static.py`：gate 候選「動作演員」→「身手好」×2。
- `test_giglib36_static.py`：requiresCastingTagAny 斷言改「身手好」。
- `test_giglib36_logic.js`：fixture registry label／labelToId 改「身手好」（同新 pack 睇齊）。
- **刻意唔改**：`test_weave46_logic.js`／`test_weave48_logic.js` 嘅存檔 fixture 用舊 label「動作演員」——正好兼任舊存檔相容驗證（靠 id 命中＋遷移，照 PASS）。

## 驗證
- 新 test：`test_terms57_logic.js`（22 checks：清洗層 fixture 行 A1/A2/A3/A4/B1/B2/B4/B6）＋`test_terms57_static.py`（33 checks：tokenizer 掃玩家面字串零命中＋合法保留白名單＋C 類抽查）——對 v57 PASS、**對 v20a56 兩套都 FAIL（反證成立）**。
- 全套 tests：**46/46 PASS**（基線 44＋新 2）；主 script `node --check` OK。
- 玩家面殘留（region 外、註解外）逐個核實：聲量＝QA 探針 ×9＋alias ×1；周刊＝registry 舊 key ×1；事態＝provenance ×1；解鎖／點擊／刷新＝0（只剩註解）。
