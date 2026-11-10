# v20a83 ENC83 — 紅星巧遇 Phase 2（魏詠男／顧明輝／駱家聲／齊鎮海）＋ T4 提攜通用機制

基底 v20a82（4,974,159 bytes，tests 94/94）。設計權威：`linji-encounter-design.md`（D1–D9 已拍板）。
唔改 SAVE key（starVolunteer_map_v19w）／softRev（s107）／產品 ?v=（v20a10）；唔改 content pack JSON；新內容全部疊加喺 ENC79 框架之上。

## 範圍

Phase 2 四星全套接入（出沒盤行 Phase 1 既有 `ENC79_STARS` 註冊、本包補對白／節拍／框架句／試點旗）：

| 星 | 主場／副場 | 出沒窗 | 五層對白句數（DLG 計） | 綁鏈 |
|---|---|---|---|---|
| 魏詠男 ngai_wingnaam | film_harbour／agency_ho | 1991 春・夏 | 119 | 人情渠道＋N7 咬合：情報拍（邊組缺替身）→幫手拍（1991+，大排檔抉擇）→還人情拍（傳授企位） |
| 顧明輝 gu_mingfai | tvb_harbour／cafe_cha | 1991 秋・冬 | 129 | N10 咬合：財務預告（1991）→C9 前預告拍→**借錢拍**→還款／壞帳後續拍→C9 後上岸拍 |
| 駱家聲 lok_gasing | tvb_longmen／rec_hk | 1992 春・夏 | 122 | 樂壇線預熱 N14/15：1990 得罪高層伏筆→樂壇情報→和音幫手拍（T3＋歌藝 ≥35）→1992 回暖拍→**E4 唔忿拍（gate 喺報紙 E4 刊出之後）** |
| 齊鎮海 chai_zanhoi | tvb_longmen／tvb_harbour | 1990 春・夏、1992 春・夏 | 117 | N3/N13 咬合＋M10 挖角潮：電視城情報拍→1992 站隊前抉擇拍（勸停爛劇／沉默，fx 分岔傳聞卡）→站隊回收拍（flag_side_*／C14） |

四星合計 487 句（連 FRAME 框架句 507 句）。每星：first 初遇定場戲（3 抉擇）／openers T0–T4／address 四級稱呼／heart 心聲（2 抉擇）／pool T1–T3／beats 鏈節拍＋提攜拍。

## T4 提攜核查結論（D2）

**Phase 1 未實作提攜**：開工時 grep v82 ENC79 模組全段，「提攜／引薦／patron／refer」零命中。本包補通用機制，覆蓋全八星：
- 每星一條 `*_patron` 節拍：好感到 T4（自己人，fav ≥70）先開，排喺鏈節拍最尾唔搶鏈戲；
- Phase 1 四星（陸柏言／廖炳星／麥震東／葉敏芝）專屬提攜段（各 6 句）喺 ENC83 模組 merge 入佢哋既有對白 beats；Phase 2 四星提攜段喺各自 DLG 內；
- 節拍完成經 `enc79GrantCredit` 登記一筆「引薦」債權入 favorLedger（一星一次，冪等）——行 D2「引薦→信用門」方向，冇另建隱藏通告系統（自作判斷）。

## 顧明輝借錢接駁（唔另起一套債）

借錢方向係「佢欠玩家」，所以入債權側，唔入 mockDebts（嗰邊係玩家欠人）：
- 借出：`enc83GuLoanStart(lvl)`——金額＝玩家身家 20%（10 元取整、上限 $5000；借一半減半），少於 $50 唔成債（佢婉拒）；扣錢＋經 `enc79GrantCredit` 開 `credit_enc83_gu_loan` 入 `S.mockCredits`＋favorLedger 計數；due 旗寫入 `S.flags.enc83_gu_loan_due`（借出日 +28 日）。台詞唔寫死金額（金額只出現喺債權標題／toast 嘅動態字串）。
- 結算：`enc83GuLoanTick()` 掛喺 advanceDay（同 favorDueTick／wf3SettleTick 並列）；到期以借出日做種子判定（全數借出還款率 30%、借一半 50%——大概率壞帳）；結算記入 `S.favorDueSettled`（同 favorDue 教學債同一本結算登記）、債權移出未收清單；還款→錢入帳＋傳聞卡 rumor_gu_loan_repaid；壞帳→傳聞卡 rumor_gu_loan_gone。後續拍 gu_after_repay／gu_after_default 按結算旗開。

## 其他自作判斷

- 魏詠男幫手拍餐費定 $150（大排檔一餐；錢唔夠就唔扣唔開債權，台詞照行）。
- 駱家聲和音拍歌藝門檻定 `S.vocal ≥ 35`（中段水平）；E4 唔忿拍嚴格 gate 喺 `S.news82.pub/arc` 有 E4 之後（1992-10 刊出），之前只出「俾人標籤二線」嘅一般不忿（伏筆／pool 段），冇預知邊四個入選。
- 齊鎮海回收拍閘：LIVE 站隊節點係 C14，以 `flag_side_film/tv/undecided` 或 C14 完成為準（設計 N13 對應）；顧明輝以 C9 為 N10 對應節點。
- 顧明輝句數 129 畧高過 brief 100–125 上限：借錢線有還款／壞帳雙後續拍，內容需要，保留。

## 驗證

- node --check：主 script＋四份對白檔全 PASS。
- 新測試：tests/test_enc83_logic.js（註冊／五層／fx／節拍閘／借錢全週期／提攜八星／攔截／舊檔兼容）＋ tests/test_enc83_static.py（基線／接線／紅線）——全 PASS；對 v82 index 行邏輯測試 FAIL（反證成立）。
- 既有 tests 全套照跑（基線 94）全 PASS。
- 種子模擬（enc79PresenceP＋enc79EnsureDay 全期 1,096 日，口徑同 Phase 1）：見 PR 匯報。
- 真 UI 實駕（槽 3）：強制出沒魏詠男完整播完巧遇入 sheet，截圖存 verify83/，pageerror 0。
