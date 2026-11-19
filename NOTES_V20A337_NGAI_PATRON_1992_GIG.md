# v20a337：魏詠男引薦第二張 gig_1992_film_207《虎嘯龍吟》（G-NGAI-3 BUG-2）

## 問題

G-NGAI-3 全鏈實駕（`~/workspace/linji-drive-ngai3/CHECKLIST.md` BUG-2）發現：魏詠男提攜債權
`credit_enc83_ngai_patron`（「打女引薦」）只掛一張兌現通告 `gig_1991_film_212`《鐵橋風雲》
（1991 夏，film_harbour）。patron beat 無年份閘（實駕 S7a 本身 1992-01-23 播出授債權），
板 pool 只由當年 GIGS 組成（`syncGigsForCalendarYear`），所以：

- 1992 年播 patron → 授一筆永遠兌唔到嘅債權（實駕 S10b：1992-03-11 持債權入 film_harbour，整塊板空）；
- 1991 年底播、未喺年內接 film_212（窗口至 1991-08-31）→ 同樣死。

其他三位有提攜嘅星都有第二年兌現通告（陸 film_114 1992／彭 variety_106 1992／駱 rec_112 1992），魏無。

## 改動（跟陸柏言 film_101→film_114 接力前例）

1. **新通告 `gig_1992_film_207`《虎嘯龍吟》江湖拳手阿虎**（`content/gigs_new.json`，插入 film_212 之後）：
   1992 春、film_harbour、電影、高級、作品、動作、男主角（film_lead_big）。
   數字逐項照抄 film_212（陸前例係完全同規格）：24 日、pay [4416,5184]、req 演技 130＋體能 90、
   fame [35,55]、hard 0.58、同 cast（leadM null＝玩家、leadF ngai_wingnaam、
   supportM mak_zhendong、supportF wu_meilam）、trigger credit `credit_enc83_ngai_patron`、
   storyKeys `["ngai_wingnaam"]`、discoverNote「魏詠男引薦：江湖拳手阿虎，憑人情入組。」。
   新片名／blurb／synopsis／roleHint／posterBrief 按同 cast 新戲寫（書面語）。
   季節揀春：提早窗由 1991-12-31 起（春 span [3,5]＋60 日），1991 秋冬授債權嘅玩家等到年尾就見到；
   1992 年 6 月後授債權仍屬同陸／彭一樣嘅既有缺口（唔另開冬張）。
   通告庫 322 → 323（1992 年 87 → 88）。
2. **BR89 map 加第 19 對**（`index.html`，同行追加，零行數漂移，47,296 行不變）：
   `gig_1992_film_207:"credit_enc83_ngai_patron"`，同 film_212 同一筆債權；
   殺青邊張都經 `br89OnGigComplete` 標 redeemedBy，另一張經 `br89GigOn` 讀 redeemedBy 自動落板；
   人情卡「可以換」經 `creditRedeemLine283` 反查自動出兩張名。header 註解同步加 v20a337 一句。
3. **唔郁**：film_212、ngai_patron beat 授債權段（L40038）、其他三位嘅兌現通告、GRANT229_ENC79 全部行。

## 測試

- 新測試 `tests/test_r337_ngai_patron_1992.js`（26 項 ALL PASS，跟 test_r319 模式）：
  靜態欄位逐項對 film_212、trigger／storyKeys、BR89 19 對、年份池分開唔污染；
  無債權／他人債權唔上板；持債權兩張都開＋季節窗四點（1991-12-15 未入／1992-01-15 入窗／
  1992-03-15 可見／1992-06-15 過季）＋1991 夏 film_212 可見 film_207 未入；
  殺青互斥兩邊＋line 更新＋generic283 跳過＋H 出兩張名；
  GRANT229「講大話」照派 film_114、film_207 無即派行；舊檔唔 crash、絕響唔開。
- Count 斷言同步（323／38／27／19／88／311 等）：test_gig229_pack（五級分布高級 20→21、
  作品 195→196、cast 253→254、影視廣告作品 133→134）、test_gig229_grant／press94（named 186→187）／
  years／trigger（T8 19 對）／stagger 冇 count、test_nat92_logic（F2 310→311、E0 37→38）、
  test_r286／r299／r302／r304／r305／r306／r307／r309／r310／r311／r312／r313／r314／r315／r316／
  r317／r318／r319／r320／r321／r322、test_r5_283／r5_284、test_sideline158（武打 matcher 22→23：
  film_207 係動作＋作品，入紅棉武指渠道，同 film_212 一致）、test_sideline273／274（A2 加魏例外）／280、
  test_br89_logic、test_awei195_logic（1992 真男主角 7→8）、test_gig291_winter。
- **全套 suite：390／9**（v336 基線 389／9＋新測試檔 1 項；9 FAIL 同基線逐項一致，零回歸）。
  第一跑 377／22 係漏咗 13 個 count 斷言檔，逐個補齊後回 390／9。
- **實駕覆驗**（`~/workspace/linji-drive337/`，本地 serve 工作副本，ngai3 harness 改指本地）：
  - v337a（1992-03-11 持債權）：板見《虎嘯龍吟》＋引薦 tag（未達標段，種子演技低，同 S10a 口徑），
    片酬 $4,800／24 日，唔見《鐵橋風雲》——PASS，截圖 `v337a-board-film_harbour.png`。
  - v337b（1991-07-16 持債權）：板見《鐵橋風雲》＋引薦 tag，唔見《虎嘯龍吟》——PASS。
  - v337c（1992-03-11 無債權）：板空，唔見《虎嘯龍吟》——正確隱藏（check 記 FAIL 係對照組語義，行為啱）。

## 跟進

- MEMORY.md 按 brief 無直接改——版本進度行仲寫「截至 v336」，要 parent 更新做 v337
  （suite 390／9、通告庫 323 張、index.html 47,296 行不變；G-NGAI-3 BUG-2 已修）。
- 攻略（artifact）魏線引薦兌現表如有列 film_212，建議同步加 film_207 一行（唔喺本票範圍）。
