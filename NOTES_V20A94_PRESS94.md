# NOTES v20a94 PRESS94 — 見報門檻＋臨記級「臨」徽章

基底：v20a93（git main 4997f92，線上 5,345,271 bytes／sha256 18d2b5da…）。
緣起：用戶實玩捉到——聲望 7 做《賀年歌精選》唱片幫工，殺青後《樂壇速遞》出成條玩家標題「臨記拍畢《賀年歌精選》唱片幫工收工見報」。臨記/幫工殺青見報脫離現實，又同主線 B09/C3「第一次見報紙寫你名」里程碑（采兒小訪線）自相矛盾。追加（同日 13:44）：臨記級通告 UI 標記改用「臨」字，判定同見報門檻共用同一分類器。本包兩部分一次出貨，純邏輯＋顯示層，冇郁任何通告數據。

## 一、管線圖（改動前實讀 v93 index.html）

- 殺青 → `queuePostShootRewardOnWrap(sh)`（唯一生產呼叫點）→ `enqueueNewspaperFromWrap(sh, pack, opts)`：subject=`newspaperWrapSubject`（`newspaperLookupGig` 查 GIGS→work/roleLabel/type）；face=`newspaperWrapFaceLines` 組標題；chrome=`newspaperPickTemplate("wrap_success", medium)`。入隊 publishDay=shootDay+2，eventKey=`wrap:<gigId>:<shootDay>`（per-gig 去重喺 `newspaperEventSeen`）。
- **bug 本體**：fame<15 行淡紙（#104）只將 fameDelta 歸 0＋標題匿名化（`newspaperWrapFadeLines`），標題照出——低聲望幫工一樣有玩家標題。
- 稱呼層 `newspaperNameTier`：anon fame<15／named 15–39／titled ≥40（常數 15/40 不變）。
- 砌版 `buildNewspaperEdition`：排序 world（頭版級 2／花邊級 1）＞|fameDelta|＞award；head=第一、其餘 ≤3 做短訊、尾加 `paperSideItemForDay(day)` 定版花邊。`commitMorningPaper` 入帳 fameDelta 總和、入剪報（上限 40）、`pushNewspaperRumor`（頭條/短訊 echo 入傳聞池）。
- 碎片池只收 SIDE_PAPER_FRAGS 登記嘅 side 花邊（`paperSideItemForDay`）——**wrap 項目本身從來唔入碎片池**，見下第五節。
- `familyPaperEchoTick`（鏈 G）只讀 `newspaperNameTier()`（fame 層級），唔讀標題 → 唔受閘影響，冇郁。
- 聲望/人氣：報紙 fameDelta 同殺青數值本來就分開結算（殺青入帳喺 shoot 本體，報紙只係呈現＋其 fameDelta 係獨立一筆）——本包唔郁任何數值路徑；入閘項目 fameDelta 本來喺淡紙下就係 0，fill 沿用 0。

## 二、見報門檻劃法（PRESS94 分類器，見報同徽章共用）

新函數 `press94RoleClass(gig, labelHint)` 回傳 `"base"`（入閘）／`"named"`（夠格），`press94TierBadge(gig)` 係徽章唯一入口。判定次序（label 優先於 scale——用戶原案《賀年歌精選》roleScale=rec_album 齋睇 scale 會誤判，label「唱片幫工」先捉到）：

1. softBridge 常駐散工家族 → base（機制簽名，v93 豁免族 30 張全入閘）。
2. 逐個來源掃標籤字串 [gig.roleLabel、標題去《》後綴、殺青 labelHint]：
   - 含「替身」→ base（唔出樣，恆基層；優先於下行 STRONG，避免「替身主角」類誤放）；
   - STRONG 詞 `主角|男主|女主|主演|主唱` → named；
   - BASE 詞 `臨記|臨時演員|臨時群演|群演|路人|途人|幫工|和音|和唱|伴舞|舞者|班底|散工|舉牌|充場|群戲|過場|閒角|客串|特約|熟手|頂位|助手|場務|武行|手模|試音|遞水` → base；
   - NAMED 詞 `配角|男配|女配|男二|女二|隊長|模特|嘉賓|領唱|領舞` → named。
3. 再睇 scale（resolvedScale||roleScale||resolveRoleScale）：
   - BASE 帶 {ad_extra_day, tv_extra_day, tv_regular_extra, film_action_extra, film_extra_short, film_stunt, tv_cameo_short} → base；
   - NAMED 帶 {film_lead_big, film_support_main, tv_lead_long, tv_support_main, film_second_lead, tv_second_lead, tv_lead, film_support, tv_support, ad_lead, ad_print, photobook, music_lead, music_guest, ad_support, film_support_short} → named，**例外**：film/tv_support_main 且 ROLE_SCALE_BAND 日數帶 ∈1..8（v93 A4 判例：單場戲小崗位掛 support_main 模板）→ base；
   - 模糊帶（rec_album／film_support_small／variety_ep／variety_special／ad_av／mtv／music_support）預設 named——A 級海報＋署名崗位（專輯主唱、單元配角等）落呢格，合「配角級或以上先見報」條款；其中 film_support_small 無標籤嗰批實審多為單場戲小角色，同 A4 精神一致歸 base 由標籤層處理（見離線普查明細）。
4. 認唔出／出錯 → named（唔過閘，保舊行為，唔好誤殺）。

離線普查（v93 判後池 475 張，分類器鏡像跑）：**base 212／named 257**。按 tier：初 base 160／named 85；中 base 51／named 113；高 base 7／named 59。錨點對照（v93 判處書＋用戶原案：EXPECT_BASE 44 張＋EXPECT_NAMED 19 張）**0 不符**；softBridge 30/30 base；移民潮急聘族 5/5 base（資深臨記/熟手/頂位）。

接線：`enqueueNewspaperFromWrap` 喺 chrome 計好之後判級——入閘即場 return fill 項目（第三節），唔入閘行原路徑一字不改。兩處呼叫都有 `typeof` 守衛（離線抽函數測試環境冇 press94* 嗰陣退回舊行為，同 repo 慣例）。

## 三、頭條填位（fill）

- 填位生成器 `press94FillLines(subject, gig)`：主演=`leadStar59Of(gig)` 或 `gig.starHint.name`；按 medium（film/tv/music/ad/any）出 headline/dek/rumor 變體池，有主演以「主演＋製作」為主角，冇就純製作消息（煞科/錄製完成/趕檔期）；作品名 hash 定版揀變體（同 `_headPick37` 款）。全書面語、唔提玩家、唔提阿偉。
- 項目欄位沿用 chrome（eventKey/入隊日/出版日/報紙名/clipLabel/templateId/templateEventKey），fameDelta=0，另帶 `press94:"fill"` 標記。殺青畫面＋手帳交代完全冇郁（只係唔上報紙標題）。
- **優先序**：唔使新排序——`buildNewspaperEdition` 本來就將 world 項目（年代事件 NEWS82 級 fameDelta 大／頭版級）排喺 wrap 前面；fill 嘅 fameDelta=0，同日有年代事件/紅星大新聞嗰陣 fill 自動落短訊位，冇大新聞嗰陣 fill 先做頭條。即實際優先序＝年代事件＞紅星/劇情正紙＞製作消息，同 brief 要求一致。
- **防重複**：①eventKey per-gig+shootDay 去重（同一單工只入隊一次，沿用）；②短時間內唔會連日出同一作品——一單工殺青只得一次；③變體按作品名 hash 定版，唔會同一作品兩日出唔同講法；④唔同作品用各自標題，唔存在全域同一句填位連日重複。頁內自檢 p94_fill_repeat 斷言兩單唔同 base 工出兩條唔同 fill 標題、且都唔 claim 里程碑。

## 四、第一次夠格見報（里程碑銜接）

- 新狀態 `S.press94FirstNamedDay`（0=未觸發、>0=觸發嗰單拍攝日、-1=舊檔回填）；fresh state 模板＋`normalizeSaveObj` 型別守衛已加，唔改 SAVE key/softRev。
- 觸發條件：named 級殺青項目＋`lines.nameTier!=="anon"`（即嗰次標題真係點名/稱號出到玩家）＋`press94ClaimFirstNamed(shootDay)` 成功。效果：嗰份報紙 dek 尾加一句「編輯按：這位新人的名字，第一次出現在本報的殺青消息之中。」項目帶 `firstPress94:true`。
- 舊檔回填：claim 嗰陣若剪報已有含「阿偉」嘅標題（舊版已經見過報）→ 靜默標 -1 唔再派，避免老玩家更新後無端彈里程碑。
- **同 B09/C3 唔打架**：實查 B09 原文（STORY_BEATS_PHASE1）係采兒「約了一段小訪…幾天後見報，名字第一次印在版面上」——講嘅係**專訪寫名**；本包里程碑措辭收窄去**殺青消息第一次點名**，兩件事分家唔撞。grep content/*.json＋主線閘證實劇情線冇讀 newspaper 狀態，無機械耦合，唔使改劇情側。
- 事件驅動見報（意外/得獎/緋聞/劇情 press/NEWS82）完全唔經呢條路徑，唔受閘、唔 claim 里程碑。

## 五、碎片入池處理

- 查明：碎片池（SIDE_PAPER_FRAGS）只登記 side 花邊（`paperSideItemForDay` 每日定版嗰條），wrap 項目從來唔入碎片池——所以臨記工冇「碎片聯動」要拆，fill 唔改呢條路徑。
- wrap 項目唯一入池路徑係 `pushNewspaperRumor` 嘅 rumorEcho（手帳「傳聞」行）：fill 項目嘅 rumorEcho 改用製作口吻（`press94FillLines` 嘅 rumor 欄：邊套戲煞科/邊位主演俾人提起），唔再以玩家為主語——同唔見報嘅決定一致。
- 鏈 G `familyPaperEchoTick` 只讀 fame 稱呼層，唔受影響（已喺設計階段核實）。

## 六、臨記級「臨」徽章（追加工作）

- 共用分類：`press94TierBadge(gig)` = base → {key:"extra", label:"臨"}；否則 {key:gigTierKey(gig), label:tier||"初"}。同見報門檻同一個 `press94RoleClass`，冇第二套判定。
- 改咗嘅顯示位（兩處，全部卡面渲染入口）：
  1. `gigCardHtml`（全卡：手帳待試鏡列表、未能試鏡 modal 共用）——`.t` 行級別字＋印章圖＋alt 改用 badge；
  2. `gigBoardTeaserHtml`（通告板卡）——印章圖＋alt 改用 badge。
- 已查唔使改：詳情頁 `castingNoticeDetailHtml` 本身冇級別字/印章（只有類型 pill＋難易度星）；手帳已殺青履歷行冇級別字。手帳待試鏡全卡因共用 `gigCardHtml` 自動一致。
- 新資產 `assets/ui-physical/notice/seal_extra.png`：以 seal_junior 為底保留原雙圈（中心半徑 ≥148px 原封），中心字換 Noto Sans CJK TC Bold「臨」、同色紅 (196,59,42)、字框對齊原「初」字位；生成腳本 verify94/make_seal_extra.py（workspace 留檔）。
- 純顯示層：`gigTierKey` 本身、tier 數據、篩選/排序/普查口徑全部冇郁。**篩選歸屬**：現有按 tier 篩選照跟 tier 數據行——「臨」係顯示層子集（入閘工多數屬初級，少數屬中級如 ad_08 機場臨記 tier 中），篩「初」唔會包含 tier 中嘅臨記工、篩「中」會見到佢但卡面顯示「臨」；呢個係刻意嘅：篩選按數據級數、徽章按崗位實質，NOTES 在此講明，行為同 v93 篩選結果逐張一致。

## 七、頁內自檢（newspaperCheck）改版

舊契約原位改＋註明 v20a94：ferry_gig 改 fill 面貌（有「天星碼頭」、冇「過海路人」）＋新 ferry_gate94；fade0_role 同理＋fade0_gate94；fade_crew_role（有「傲劍狂刀震江湖」、冇「跟組特約」）＋fade_crew_gate94；hi15 改「聲望 15 唔救基層崗位」：hi15_delta 改 fameDelta===0＋hi15_gate94、hi15_gig 改（有「試片」、冇「過海路人」）。其餘舊斷言（fade14*/fade_edition/hi16*/seed*/ferry_when/bucket/dedupe/next/html、#105/#106）冇郁。
新增 v94 守門段：兩單 named 工（男主角）驗第一次旗標＋編輯按句＋firstNamedDay 落值、第二次冇旗標冇句；兩單 base 工（唱片幫工）驗 fill 標記、標題唔同、冇 claim 里程碑。
真頁面實跑 A/B：v94 fails=[merge_cap, ferry_date:1990/1/5]；v93 基線 fails=[merge_cap, **ferry_face**, ferry_date:1990/1/5]——merge_cap/ferry_date 係兩版一致嘅既有環境性 fail（同日同法實跑），ferry_face 係舊契約斷言，v94 按新契約改版後 PASS；全部 *94 斷言真頁面 PASS。

## 八、測試同反證

- 新測試（入 tests 長駐）：
  - `tests/test_press94_logic.js`（29 斷言）：A01–A18 分類錨點（用戶原案唱片幫工、ad_08、softBridge、替身、A4 單場戲、嘉賓/模特/主唱 named 等）、B01–B04 徽章（臨/初/中/高）、C01–C06 填位（有主演/冇主演/唔提玩家/hash 定版）。
  - `tests/test_press94_static.py`（S01–S12）：接線位、seal_extra 資產存在、SAVE key/softRev/?v= 原值、分類器冇寫 tier、頁內新契約在位。
  - 反證：兩檔喺 v93 index 上均 FAIL（已實跑 /tmp/counter94）。
- 全套 A/B（run_suite.sh 逐檔跑，基線 linji-work93）：v93 120 檔 vs v94 122 檔，diff 只剩：新增 2 個 press94 測試（PASS）＋test_wf5_87_logic 結果字串入面路徑唔同（同為 PASS 59/0）。既有環境性 FAIL 兩邊逐檔一致：test_soft_tip_111_restore（FAILURES: 21）、test_weave43_static／test_weave44_static（FAILED: softRev unchanged）。
- 語法：抽 `<script>`（2 塊）`node --check` SYNTAX_OK。
- 普查/節奏：本包冇郁通告數據、冇郁 req/pay/tier → v93 普查（day-0 可接 14、「恰好 2」32.7%）同節奏模型（片酬總額、雙軌 288）口徑不變，無間接影響。

## 九、實駕證據（真 UI，槽 3 可棄用，pageerror 0）

證據檔喺 workspace `linji-work94/verify94/run1/`（summary94.json／runlog94.jsonl／milestone_summary.json／badge_shot_summary.json／page_check94.json＋page_check93_baseline.json）。

- **場景 A**（聲望 7、《賀年歌精選》唱片幫工 @灣仔唱片）：殺青剪報 headline=「《賀年歌精選》錄製完成 趕及檔期出街」、dek=「唱片《賀年歌精選》錄製完成，唱片公司趕工出貨，趕及檔期推出。」、fameDelta=0、`S.press94FirstNamedDay=0`（冇 claim）；截圖 `A_paper.png`：《娛樂快報》1990/1/10 頭條係製作消息、花邊短訊在下、頁腳「聲望未有變動。」；殺青畫面/手帳交代如常（runlog gig_step 全程）。
- **場景 B**（聲望 20、named 工）：四單先後殺青全部照出玩家標題——《賀歲喜劇錄像男主》（男主角）、《智醒大挑戰》（遊戲嘉賓，入隊項快照 press94=""／firstPress94=false）、《迎春接福大闖關》（遊戲嘉賓）、《冬霧西裝金錶硬照》（平面模特）；截圖 `B_paper_first.png`（星河娛樂版 1990/1/18「穩陣綠葉阿偉拍畢《智醒大挑戰》 遊戲嘉賓收工見報」，聲望 +2）、`C_paper_second.png`（消費情報 1990/1/31「金牌甘草阿偉於《冬霧西裝金錶硬照》飾平面模特 殺青見報」）。
- **場景 C**（里程碑只派一次）：第一單 named 工（《賀歲喜劇錄像男主》）剪報 dek=「…擔任男主角，嗰晚唱到尾，俾人記住把聲。編輯按：這位新人的名字，第一次出現在本報的殺青消息之中。」；其後三單 dek 全部冇編輯按。補拍局 milestone_summary.json：firstNamedDay=7、pageerrors=[]；截圖 `B_paper_milestone.png`（娛樂快報 1990/1/10，編輯按句喺 dek 尾可見）。
- **徽章**：`badge_board_adm.png`（金鐘創意板，elementFromPoint 確認板面喺最前層）：《離境大堂一封信》（ad_08）印章=seal_extra「臨」，同場《龍鳳喜餅賀春照》「初」、《春季喜餅宣傳片》「中」、《金錶冬日特寫》「高」對照齊；`badge_board_central.png`（中環廣告板）：《年宵花市》《歲晚年貨街景》《便利店短片》「臨」＋《年貨大街》（試食主角）「初」對照。DOM 證據（badge_shot_summary.json）：ad_08 seal=`assets/ui-physical/notice/seal_extra.png?v=20a8`、alt=「臨」；food_ad seal=seal_junior、alt=「初」。
- 全卡 `.t` 行嘅「臨」字由離線測試以真 `gigCardHtml` 輸出斷言（B01）；實駕視覺以通告板 teaser 印章為準（用戶指定嘅主顯示位）。
- 已知非回歸 artifact（v91 本有）：長推進後首次開某地點通告板首讀空板、再開正常——本包實駕亦見地點入場巧遇層會蓋住板面，清走對話後板面正常，屬既有呈現時序，排視覺 QA 跟進。

## 十、守衛核對

- SAVE key `starVolunteer_map_v19w` 不變；softRev `s107` 不變；產品 `?v=v20a10` 不變；gig id 全不變；冇直改 content pack JSON。
- 冇改 tier/req/pay/工期任何通告數據；冇改篩選/排序邏輯；冇改數值結算路徑（殺青入帳、報紙 fameDelta 規則不變，入閘項目 fameDelta 沿用淡紙既有 0）。
- 事件驅動見報、劇情 press、NEWS82、頒獎紙 全部冇經 PRESS94 路徑，冇誤閘。
