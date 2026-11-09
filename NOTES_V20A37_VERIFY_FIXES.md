# NOTES · v20a37 驗證修復包（VERIFY_FIXES）

背景：「引導包 v20a34＋節奏包 v20a35」兩包齊後嘅驗證試玩（2026-11-09，新檔玩到第 6 週）
通過 8 項、未過／新發現 10 項。本票逐項修復，每項都先用真碼追蹤「玩家實際見到嗰個
畫面係邊個函數出、數據邊度嚟」，測試行返嗰條真路徑（tests/test_verify37_logic.js／
test_verify37_static.py），唔再行替身路徑。

基線說明：本票開工時 v20a36 補庫包（PR #132）剛合併，分支以合併後嘅 main 為基線
（v20a35＋v20a36），兩票改動區域唔重疊，rebase 零衝突。

紅線：冇改 SAVE key（starVolunteer_map_v19w）、softRev（s107）、?v=（v20a10）、
content pack JSON（第 5 項 pack 模板問題用填充層正規化解決，見下）。

---

## 必修 1：雙軌白話解釋實機冇出現

**根源（實證）**：`dualTrackExplainHtml34(result)` 本身接線冇錯——`StoryPlay.showResult`
真係有 call 佢，`StoryOC.applyChoice` 真係有回傳 `result.dual`。死因係觸發條件：
v20a34 定「result.dual 有正增益（dStage>0 或 dCredit>0）先出」，但查真 pack
（story_detail_c1_to_c17.json）——C1 兩揀（先學做動作戲／先賺）同 C2 兩揀
（留人脈／趕通告）嘅 `effects.stats` 全部係 `{}` 空表，ripple 亦冇 creditDelta，
即第一、二幕結算嘅 dStage／dCredit **結構上永遠係 0**，正增益條件喺真路徑永不觸發。
玩家見到嘅「聲望 5／信用 10」只係 dualResultHtml 顯示嘅絕對值，唔係增益。
**之前點解測試過但實機唔得**：v20a34 段六測試係齋 call 函數餵假 result
（`{dual:{dStage:2}}`），假數據有正 delta 所以過——測試行嘅唔係玩家條路徑。
旗 guidanceDualExplained34 實機從未燒過（冇出過解釋），修好後第一次結算即出，符合原意。

**修法**：觸發改做「第一次事態結算展示雙軌面板（result 帶 dual 物件）就出」，
唔再要求正 delta；仍然只出一次（同一旗）。假呼叫（冇 result／冇 dual 物件）唔出唔燒旗。

**驗證**：test_verify37 段一——真 listOpen offer → 真 StoryPlay.start('C1') →
skipToChoices → pickChoice('C1_a') → 捕捉真 showResult modal：解釋出現＋旗已燒；
再真播 C2（第 4 週＋傳聞＋隔日＋通告數，行軟閘真 trigger）結算：唔再重出。
同一測試行落舊碼（v20a35）會 FAIL 喺呢兩項，反證有效。
連帶改舊測試：test_guidance34_logic 段六＋test_guidance34_static 嗰項斷言本身就係
釘住錯誤觸發條件，改為新約（有真結算 dual 物件＋只出一次），理由同上。

## 必修 2：報紙頭條＋殺青反響重複／寫錯劇名

**(a) 頭條固定句式——根源**：`newspaperWrapFaceLines` 嘅 headline 係單一固定句式
（`《X》殺青 臨記飾演Y`／無角色版 `入鏡`），v20a35 只俾 dek 加咗尾句變體池，
冇覆蓋 headline 路徑。**測試過實機唔得嘅原因**：v20a35 段五測試只斷言 dek 定版／變化，
冇掂 headline。
**修法**：headline 加變體池 6 款（有角色／無角色各 6），沿用 dek 定版原則——
以「作品＋角色」hash 定版：同一作品每次同一句、唔同作品唔同句式。
句式刻意避開「男主／男一／男星」字眼（newspaperWrapFadeLines 會掃全文）。
連帶改舊測試：test_weave31_logic 三條頭條斷言釘死舊單一句式，改守稱呼層不變量
（anon 用臨記唔出名／named 出阿偉／titled 出人氣新人阿偉＋角色在場）。

**(b) 「收視關注」三連一字不差——根源（實證）**：嗰欄係 PSR metrics channel、
metricKind=ratings。增補後 ratings 池有 2 張（metric_rate_01＋psr35_metric_rate_02），
唔係池得一張。死因係 `buildPostShootRewardPack` 對 metrics **抽兩次**：先
`postShootPickTemplate("metrics", …)`（內部已經行 psrPickNoRepeat35），再用 metricKind
命中池經 psrPickNoRepeat35 重抽。兩次抽選共用 `_psrLastPick35["metrics"]`：
第一次抽 X（記 X）、第二次被迫抽 ≠X 嘅 Y（記 Y）；下一份 pack 第一次被迫 ≠Y→X、
第二次被迫 ≠X→Y——**由第二份起最終結果永遠鎖死 Y**，防重複機制反被自己打敗。
**測試過實機唔得嘅原因**：v20a35 段四只驗證 press／fans 渠道嘅變化同組裝完整，
冇連組多份嚟驗 metrics 欄。
**修法**：metrics 每份 pack 只抽一次——先計 metricKind 命中池，非空就用
psrPickNoRepeat35 抽一次，空先 fallback 去 postShootPickTemplate（嗰次係唯一抽選）。

**(c) 寫錯劇名——根源（實證）**：增補池 `PSR_EXTRA_TEMPLATES_35.press` 嘅
`psr35_press_tv_02` headline 寫死「夜班廠景收工」——v20a35 作者將中階通告《夜班廠景》
嘅專屬風味寫入通用電視池（matchTypes [電視劇，綜藝]），任何電視劇殺青抽中就寫錯劇名
（實機《天星碼頭》嗰份就係咁）。成個增補池已逐張審計：只有呢一張有具名作品，其餘皆通用。
**修法**：去具名——headline 改「深宵廠景煞科，新面孔企到尾」、dek 改「嗰組趕夜班…」
（保留夜班風味、冇 proper noun）。

**驗證**：段二——真 buildPostShootRewardPack 連組 30 份電視劇殺青：收視關注
templateId ≥2 款輪替＋冇連續兩份相同（舊碼全 30 份鎖死同一張，測試行舊碼即 FAIL）；
連組 60 份《天星碼頭》：冇一份出現「夜班廠景」、改好嗰張有入輪替；
真 newspaperWrapFaceLines ×12 個作品：頭條句式骨架（抽走作品／角色／稱呼後）≥3 款、
每條都帶返自己作品＋角色、同一作品重組定版。

## 必修 3：聲望唔兌現——查證結論：唔係落帳 bug，係文案誤導

**追蹤**：`doAudition` 成功路徑抽 fame/pop 後只 `apply({acting, stress})`——兩個數
存入 `scheduleShoot` 嘅 shoot record，去到**殺青嗰日** `resolvePlannedDay` wrap 分支
先 `daily.fame += sh.fame` 經 apply 落帳。手帳「已獲聘」卡本身有展示待入帳數字。
《靈異屋邨夜話》拍 9 日，試鏡喺第 4 週尾，殺青落喺第 6 週中後段——試玩停嗰陣大概率
未殺青，聲望「冇郁」係未兌現、唔係冇兌現。**真路徑模擬實證**（段三）：3 日電視劇、
對話 +5／+17 → 獲聘嗰刻 S.fame 不變、第 1／2 拍攝日不變、殺青日 17→22／10→27，
分毫不差。所以唔使改落帳邏輯。
**真問題**：(i) 對話行「完成後約酬 $X · 聲望 +5 · 人氣 +17」冇講幾時兌現，
玩家自然以為即時入帳；(ii) 手帳排程獲聘路徑（resolvePlannedDay 入面 job: 分支）
notes 根本冇呢行，同 doAudition 唔一致。
**修法**：兩條獲聘路徑統一改文案做「殺青後入帳：約酬 $X · 聲望 +N · 人氣 +M
（未殺青前唔會加，拍完嗰日先入帳）」；手帳「拍攝中／已獲聘」卡嗰行加「（殺青後入帳）」。
數字來源不變（同 shoot record 同源）。

## 必修 4：週行程頁「上週內容＋下週標頭」

**根源**：`settleWeek()` 唔換 `S.weekPlan`——要去到重新規劃（enterHome 可編輯分支／
確定行程）先換；但 `renderNotebook` 標頭永遠用當前 S.dayIndex 計週次範圍，
`syncDateChrome` 又會 live 覆寫 nb-range。週結算後、重新規劃前經非編輯路徑開手帳，
rows 係上週 plan、標頭係下週日期。
**修法**：weekPlan 加週次戳 `S.weekPlanWeek37`，喺「新一週 plan 落 weekPlan」嘅
賦值點一齊寫入（placeShootOnPlan／enterHome editable／確定行程兩路／開局種子／
缺 plan 補種／讀檔補種）；標頭改跟 plan 週次計（`nbRangeLabel37`，renderNotebook＋
syncDateChrome 共用）；顯示緊上週 plan 且非編輯時，標題改「上週行程（唯讀）」＋
模式行講明係上週已執行行程。舊檔冇戳 → 當本週，零回歸。
**驗證**：段四——真 renderNotebook（DOM stub 捕捉標頭）：戳=2＋dayIndex 第 3 週 →
範圍=第 2 週＋標題「上週行程（唯讀）」；戳=3 → 本週；冇戳 → 本週。

## 必修 5：拍攝場數 off-by-one

**根源**：模板「劇集外景：{title}第{done}場過關，餘{total}場。」——餘數填咗總場數
而唔係 total−done。同一個錯喺三處：內嵌 EVENTS_ZH_HK.SHOOT_DAY、內嵌
SHOOT_DAY_BY_TYPE["電視劇"]、同 live pack `content/events_zh_HK.json` 嘅 SHOOT_DAY。
而 `eventLine` 係 pack 優先（EVENTS 載入後成個蓋過內嵌池），淨改內嵌唔夠；
pack JSON 按紅線唔准改。
**修法**：`shootDayLine` vars 加 `remain = max(0, total−done)`；填充層正規化——
凡 SHOOT_DAY 模板（typed 路徑＋eventLine 通用路徑）入面嘅「餘{total}」一律先換做
「餘{remain}」先 fillTpl（pack 用舊寫法都即時修正）；內嵌兩處模板順手改做
「餘{remain}場」保持 fallback 潔淨。
**驗證**：段三——真 resolvePlannedDay 拍攝日：1/3 冇「餘3場」＋有「餘2場」、
1/1 冇「餘1場」＋有「餘0場」；再模擬 pack 蓋過（EVENTS 注入舊模板）→ 照出「餘2場」。

## 應修 6：事件節奏參數

**(a) 訓練微事件連出——根源**：`maybeTrainEvent35` 舊參數冇冷卻：出完嗰堂 since=0，
下一堂即刻又有 45% 再出，連出唔罕見（4 連出約 4–9%），長期頻率約 50% 貼住設計上限
（設計約每 2–3 堂一則）。兩個訓練入口共用同一計數，冇雙計 bug；同日守衛正常。
**修法**：加冷卻——出完之後嗰堂必唔出（since≤0 只 +1 唔擲）；since≥1 時 50% 擲；
since≥3 保底（最遲第 4 堂出）。長期頻率 ≈36%、永不連出、最大間隔 4 堂。
**驗證**：段三——真 resolvePlannedDay 訓練日 ×20 日 ×10 輪：實測頻率 36%、
冇任何一輪出現連續兩堂都出。

**(b) 長工抉擇太疏——根源**：`setChoiceOffer35` 舊參數間距 ≥2 曆日＋60% 擲；
拍攝日多數相鄰曆日，合資格日只剩隔日嗰啲再 ×60%，9 日工預期約 2.4 次、
下限好易得 1 次（實測 5 日 1 次唔出奇）。
**修法**：保留間距 ≥2 曆日；擲升至 75%；加保底——未出過且 doneDays≥2 必出、
距上次 ≥4 日必出。9 日工預期 3–4 次。pacing35 舊測試（Math.random=0.5 stub）仍全過。
**驗證**：段三——真 9 日拍攝路徑 ×8 輪：平均 3.8 次、每輪 ≥2 次。

## 應修 7：事態預告寫明解鎖條件

**查證**：picker「即將可出」行本身有週次戳（約第4–5週）同軟閘條件 bits，但有三個缺口：
(i) 軟閘覆寫會將 meta 清空（覆寫分支 `meta = ""`）；(ii) 條件文字冇穩定包含
「開咗去邊度播」——軟閘文案有地點嗰陣先有，冇嗰陣玩家唔知開咗去邊；
(iii) 已解鎖但唔在場嗰陣，pickerHereBlock 兜底只講「先到場，先可以播這幕。」冇地點名；
主線進度行（storyMainProgressLine）對非軟閘節點（C6+ 三年版閘）亦冇地點。
**修法**（只改呈現，唔改任何節點閘）：picker locked 行——meta 俾覆寫食咗就用
storyLockMeta（真 when／pacing／openConditions）補返；why 冇提地點就補
「（開咗去{真地點}播）」（storyNodeLocId）。pickerHereBlock 兜底改做
「去{地點名}先可以播這幕。」。主線進度行補「開咗去{地點}播」（remain 已有地點字眼就唔重複）。
**驗證**：段一——真 playOpenPicker（C1 已完成、第 2 週）：C2 行同時有「未到第 4 週」
＋「星河電視台」；真 storyMainProgressLine（C1–C5 已完成、目標 C6）：有「開咗去…播」。

## 應修 8：荒謬差額顯示

**界限點定**：開局屬性（fresh()）最高形象 22、演技 18；訓練一日約 +2~3 單項、
全心練一項一週約 +10~15。總差額 >80 即單項差過開局最高屬性近 4 倍，或者攤開幾項
都要 8 週以上全職訓練——四週內冇可能達標，屬長遠目標。實機例子（欠演技 322／
歌藝 636）遠超此界；界內例子（《靈異》演技差 27）照出真數有目標牽引作用，要保留。
**修法**：新增 `gigGapBoardLine37`——總差額 >80（`GIG_GAP_FAR37`）嘅卡，**通告板卡面**
（短卡＋完整卡兩處）差額行改顯示「長遠目標 · 暫未及（點開睇詳情）」唔出數字；
詳情頁（gigLockReasonLine）保留真數；唔隱藏張卡、唔改門檻、唔改排序。
「最接近」標記排除過界卡（全板得遠卡嗰陣唔亂標）。
**驗證**：段五——欠 636 卡：板面行冇數字＋詳情計法照出 636；欠 27 照出真數；
界限邊界 80 照出／81 轉長遠目標。

## 查證 9：傳聞來源唔跟實際地點——係 bug，已細修

**根源**：來源唔係冇記錄——每個打聽行動 def 本身有 `source`（實際地點），但
`applyMockAsk` 組裝嗰陣用 `rumorSource = (catalog && catalog.source) || def.source`，
**種子固定值優先**：tvb_rules_gossip 種子寫死「金龍茶餐廳」，玩家喺何生事務所經
act_ho_tvb_rules 聽返嚟都照顯示金龍茶餐廳。
**修法**：改以行動來源優先——`def.source || catalog.source`。唔使改數據結構；
開局預置碎片（冇經打聽）唔受影響。
**驗證**：段六——真 applyMockAsk：事務所請教 → 入帳來源「何生事務所」；
茶餐廳打聽 → 「金龍茶餐廳」。

## 查證 10：開局債得 3 筆——設計如此，唔使改

開局四債係：屋企債（debt_family_home，首次載入即播種）、何生春季卡（card_ho_spring）、
老張器材卡（card_zhang_spring）、教學人情（debt_ho_tutorial）。教學債**唔係開局入帳**：
佢喺 `markRumorTutorialDone` 先加——即玩家完成或者跳過傳聞拼合教學嗰刻
（設計理由：v19w 起新檔開局清空圈內債，避免 Day 1 已逾期；教學債係教學流程嘅產物）。
上一輪試玩睇人情頁嗰陣已過教學（4 筆），今輪未過（3 筆），差嗰筆就係教學債。
屬設計先後，唔係漏入帳，唔改。

## 取捨／未做

- 第 3 項冇改落帳時機（殺青先入帳係既有經濟設計，只修文案＋補齊第二條路徑顯示）。
- 第 5 項冇改 content pack JSON（紅線）；pack 側模板要等 pack 維護嗰陣先至順手改返
  「餘{remain}」，而家填充層正規化已完全覆蓋玩家可見結果。
- `_psrLastPick35` 唔入存檔、跨 session 重置，屬可接受（今次三連重複係同 session 內
  雙抽鎖死，已修）。
- 第 7 項只改預告／提示呈現，冇郁任何節點閘、C2 週數門檻同 offer 機制。

## 測試總覽

- 新增 tests/test_verify37_logic.js（六段、全真路徑）＋tests/test_verify37_static.py；
  新 fixture tests/fixtures/behavior_gate_c1_c5.json（repo content 真副本，畀軟閘真 trigger）。
- 改舊測試三處（理由見上文第 1／2(a) 項）：test_guidance34_logic 段六、
  test_guidance34_static 雙軌斷言、test_weave31_logic 三條頭條斷言。
- 既有全套（含 v20a36 giglib36）＋新測試全過；index.html script node --check OK。
- 反證：新邏輯測試行落 v20a35 原版會 FAIL 喺第 1／2／7 項嘅核心斷言，證明唔係空轉。
