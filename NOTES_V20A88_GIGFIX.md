# v20a88 通告荒修復包（FIX88＋EARLY88）

基底：v20a87（線上 5,213,044 bytes）→ 本包 5,237,050 bytes（+24,006）。
依據：`linji-early-gig-diagnosis.md`（主因 v66 `__y66w` 幻影門檻／次因 v67 冬季入門池真空／結構因冬季初級帶校準）＋用戶 2026-11-11 拍板（Fix B 揀「加冬季入門通告」；通告提早出現原則）。
紀律：冇改 SAVE key（starVolunteer_map_v19w）／softRev（s107）／產品?v=（v20a10）；冇直改任何 content pack JSON（修復行正規化＋內嵌注入，照 v36 先例）。

## 1. Fix A — 幻影門檻根治（必修）

- 成因：pack 載入時 `years66Walk` 幫每個物件打 enumerable 戳 `__y66w=1`，連每張 gig 嘅 `req` 都中；`reqGap` 盲數 `req` 所有鍵，玩家永遠缺 `__y66w` 一項 → 自 v66 起 1990–92 庫存 248 張有 242 張（97.6%）從未接得到，1991/92 庫存 100% 死庫。
- 修法（兩層，冇郁 walker 本身）：
- `normalizeGigRecord` 新增 FIX88-A 段（緊接 v36 sing/dance 修正之後）：`req` 只保留 `GIG_REQ_KEYS88` 七個真屬性鍵（acting/stage/vocal/looks/charm/iq/stamina），其餘剝走；copy-on-write、門檻數值一概唔改、冪等。所有年份 pack 入池必經此處，一處根治。
- `reqGap` 加防禦：只數真屬性鍵——未經 normalize 嘅注入工／舊檔快照就算帶工程鍵都唔再鎖死玩家。詳情頁差額行（gigMissingReqGaps 等）食 normalize 後嘅 gig，`__y66w` 亂碼行一併消失。
- 復活數字（遊戲原函數行真管線量度）：修前五包 351/351 張 req 含幻影鍵、滿屬狀態可過 req 閘 = 0/351（三年庫存 0/248）；修後殘留 = 0、滿屬可過 = 351/351（三年庫存 248/248）。復活通告同 v59 主演回填／v85 海報查表對照：POSTER85 59 張管線後主演全數在位（59/59，測試 D1 釘死）。

## 2. Fix B — 冬季入門工 6＋冬季橋接工 6（用戶親自揀 B，純加法）

- 冬季入門 `WINTER_ENTRY_GIGS_88`（經 `mergeEntryGigsIntoPool` 同春季入門同一條路入池，entryTier）：賀歲片場趕檔場務（film_lion・req 空）、年宵花市廣告路人（ad_central・looks22/charm16）、賀歲特輯拜年群演（tvb_longmen・acting15）、戲院人潮賀歲片臨記（film_harbour・acting12）、賀年食品試食手模（ad_adm・looks20）、賀年歌錄音室和唱（rec_star・vocal12）。門檻跟春季入門同一把尺（全部 ≤ 開局屬性），payExact 450–900 跟入門帶（420–950）。
- 冬季橋接 `WINTER_BRIDGE_GIGS_88`＋`mergeWinterBridge88()`（LIVE，跟 mergeMidGigs35 慣例：只喺 1990 入池、跨年自動移除）：賀歲喜劇茶樓伙計（film_cotton・acting26・2日）、新春特輯醒獅隊員（tvb_harbour・stage20+stamina60）、年貨大街試食主角（ad_central・looks28/charm22）、賀年歌 MTV 群演（rec_wanchai・vocal20/charm20）、冬日外景追逐群戲（film_lion・acting24+stamina65・2日）、冬日單元劇鄰里配角（tvb_kowloon・acting30/iq22・2日）。
- 校準依據：開局 acting18/stage14/vocal14/looks22/charm16/iq20/stamina75；診斷實測認真訓練約 1 週 acting24/looks29/charm22、2 週 acting≈30/stage22。橋接 req 全部落喺 1–3 週可達位置（測試 B7 釘曲線上限、B8 證 fresh 接到 ≤2/6 唔係白送、B9 證 day-14 進度接到 4/6）。
- 1990 年一月開局係賀歲檔尾水：入門工用急拍短工（1 日殺青）呈現，releaseLabel 寫明趕賀歲檔；春季入門 6 張原封唔郁。

## 3. EARLY88 — 通告提早出現原則（用戶 2026-11-11 07:47 新增要求）

- 原則：`gig.season` 係上映／播出季，唔係接工季。季節通告上板窗改為 **[上映季首日 − 60 日，上映季尾日]**（`gigSeasonEarlyVisible88`，以 gig.year 錨定；60 日 = 「提早一至兩個月」上沿，對應拍攝一至兩個月嘅長製作）。
- 接線：新判準 `gigSeasonHidden88`（錯季 AND 未入提早窗先藏）取代四處 v18k 硬藏——`gigsForLocSeasonBoard`、`entryGigPoolLive`、`openLoc` 板面 scrub（舊檔殘留列唔再誤刪提早窗通告）、`tipGig` 推薦池。四處都加 typeof 防禦：抽函數測試沙盒冇 88 函數時自動回退 v18k 語義。排序仍用 seasonRank（當季優先、提早窗排後），`seasonTipHtml` 對提早窗通告出「提早招募：趕 X 季檔期…而家接工、拍完先上映」。
- Fix B 按新規則自洽：冬季工 1990 年一月靠當季（冬）上板；1991/92 冬季由各年庫存冬批＋提早窗（10 月中起上板）承接，唔靠入門池（入門池本來就只服務 1990 開局年）。
- 卡面資訊：詳情頁摘要加一行「檔期」（`gigReleaseLine88`）：gig 有 `releaseLabel` 就用佢（12 張新工寫明賀歲檔／農曆新年前等），冇就按上映季＋年份衍生「預計上映／播出／推出：YYYY 年 X 季」。已接／拍攝中／已殺青通告唔經板面函數，完全唔受影響；舊檔載入即用新判準，冇遷移需要。

## 4. Fix C — 守門測試

- `tests/test_fix88_logic.js`（25 斷言）：A 全庫管線 req 淨化＋滿屬可過閘＋reqGap 防禦；B day-0 冬季普查（可接 12 ≥ 3、冬入門 6/6、春入門提早窗 ≥4/6）＋橋接校準三段；C 提早窗五點（春 day0 上板／6 月落板、夏 3 月未入窗／4 月入窗、賀歲 9 月未上板／10 月上板／上映後唔出現）＋上映行；D POSTER85 主演 59/59＋入門池非空。對 v87 index 抽取即 FAIL（反證成立）。
- `tests/test_fix88_static.py`：標記／紀律／12 張新工 id／四處接線字面。
- 舊測試原位改版 1 檔（有意變更，註明原因）：`test_poster85_static.py` 主檔大小上限跟 v88 有意增長更新（5,237,050）。

## 5. 驗證

- 全套 tests A/B 對 pristine v87 基線：基線 93 PASS／12 FAIL（環境性 static 名單）；本包 PASS 數 = 基線 + 新 2 檔，FAIL 名單同基線逐檔一致，**零回歸**。（施工中一度多 6 個邏輯 FAIL，根源係新頂層參照喺抽函數沙盒未定義，已用 typeof 防禦回退全數修復，唔使改舊斷言。）
- node --check（主 script 抽查）OK。
- 真 UI 實駕（槽 3、本地鏡像，證據 `verify88/`，詳見 verify88/ACCEPTANCE88.md）：認真新玩家政策行 day 0–29——day 0 冬季可接 12 張（≥3 ✓）、第一張接到嘅工 day 0（≤7 ✓）、成功預訂 31 次／完成數下限 23（≥4 ✓）、金錢 $12,000→$12,523（峰值 $12,618，唔再純淨流出 ✓）、pageerror 0 ✓。
- 供應普查（原函數）：day-0 冬季板面 修前 35 卡 0 可接 → 修後 87 卡 12 可接。

## 6. 自作判斷清單

1. 提早窗用固定 60 日（「一至兩個月」上沿）：長製作（電影）拍攝期最長，用上沿先唔會出現「上映前一個月先上板、拍唔切」嘅反效果；短工種提早多幾週上板無害（applyDeadline／shootDeadline 機制本身會輪換）。
2. 冇郁 `years66Walk` 本體：戳記仲喺記憶體入面嘅 pack 原物件度，但入池唯一閘口（normalizeGigRecord）剝清＋reqGap 防禦，效果等同根治而唔冒改 walker 影響存檔遷移／故事表 remap 嘅風險。
3. 冬季橋接只做 1990 年：1991/92 冬季玩家已有一年以上進度，各年庫存冬批（修復後復活）＋提早窗足夠承接；入門／橋接係開局年專用供應，同 ENTRY_GIGS_1988／MID_GIGS_1988_35 既有慣例一致。
4. 「檔期」行只加喺詳情頁摘要，冇改短卡版面（短卡已有 seasonTipHtml 提早招募提示承接）。
