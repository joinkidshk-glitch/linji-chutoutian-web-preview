# NOTES_V20A229 — 新通告引擎實裝（M 240 張＋真五級＋觸發／即派／合約）

- Base：main `95baf7e`（v228）。分支 `v229`，8 批落地：B1 年份分流＋days 映射（`9afc402`）、B2 真五級（`d7c0e2f`）、B3 換庫（`e6cc582`）、B4 提名＋擔正計數（`f2769ef`）、B5 觸發系統＋BR89（`96168cf`）、B6 即派＋定期合約（`0ef8920`）、B7 報紙＋忠告卡＋stub 債（`40986c3`）、B8 測試收尾（`bf7f3cc`）＋統籌補修空洞測試（awards204 LEADSTAR59）。
- 審計＋覆驗報告：`~/workspace/linji-v229/AUDIT229.md`、`~/workspace/linji-v229/VERIFICATION229.md`（repo 外）。

## 落地內容

- **換庫**：舊通告庫全部刪走（5 個舊 pack 351 張＋6 個舊版檔＋4 個 PATCH JSON＋內嵌 fallback 137 張＋ENTRY_GIGS_1988＋code-side 內容池 NAT92／BR89／EXODUS／RIVAL／WF3／INTEL／FAVOR_DUE／MID／GIGS36 等，全部清空；merge 注入模式留返）。新庫 `content/gigs_new.json` 240 張係唯一來源（作品 141／臨記通告 93／補拍 6；五級 76／73／51／17／23；1990 高級 0 張）。舊庫 id 全 repo 0 命中（BR89 映射鍵已換新庫 id；剩低命中只喺歷史文件／assets 海報檔名，D-12 處理）。
- **A1 年份**：新 pack 載入跳過 YEARS66 ＋2（walker 層分流＋normalize 守衛，雙重保險；舊 pack 照舊 ＋2）。年份 1990–1992 唔郁。
- **days 映射**：normalize 加 `days→shootDaysHint`（240 張 effectiveShootDays＝days）。
- **D-1 真五級**：chance（1.0／1.0／0.9／0.82／0.82）、fameFloor（0／0／16／32／32）、resolveRoleScale／gigTierKey／tierOrder／DUR90／gigBreachFee／難度星／等消息日數全部五級化。舊三級經機械級對位相容。
- **D-3／A4 提名計數**：countYearMediumWraps 改讀 category，只計作品。
- **A5 擔正計數器**：`S.leadStats229.byMedium`（film／tv／music／variety／ad），殺青嗰刻寫入，跨年累加；結局梯 E1／FK／TK 改讀佢。
- **A6 觸發系統**：mergeTriggerGigs，6 種 kind（credit／award／fame／story／rel／rival）；觸發前隱藏，觸發後上板（已觸發豁免錯峰，季節窗照舊），標「引薦」／「邀約」，D-11 通知經情報站／何生（toast，一生一次）。
- **A7 BR89**：映射擴充到 13 張新庫 id；R-4 雙觸發 OR（credit_enc83_gu_patron 或還錢結算完成）。
- **獎項對照**：pack 15 個 award id 對返 repo cat_*；4 張無對應改典禮級觸發（gig_1991_film_112 影藝獎提名、gig_1992_rec_107／108 金碟夜得獎、gig_1992_ad_107 廣告賞提名），唔發明新獎項 id；新開 `S.awardsResults` 獎項級紀錄。
- **D-14**：《星夜迷離》閘由 intel_lu_burst 改做陸柏言好感 tier≥2（T2＋週期）；傳聞系統本身今票唔刪。
- **A8 即派機制**：抉擇落定嗰晚記低 gig id，第二朝何生電話直接獲聘入行程（跳過試鏡＋等消息）；主線 N4→film_114、N5→tv_122、N6_a→tv_105、N6F_a→film_110、N18→tv_121；支線 11 live＋顧 Beat2 2 draft（遊戲未有嗰個抉擇，入口已備）。
- **A12 定期合約制**：N-3（2 週×$4,900＝$9,800）／N-4（2 週×$4,200＝$8,400），簽約一次、按週出糧、唔使再試鏡、殺青計作品、板面鎖死。
- **A10 報紙**：press94RoleClass category 先行，240/240 分類啱（修正前 34 張臨記通告誤判 named）；臨記級殺青唔出報紙照舊。
- **A9 作品圖**：接通告頁零海報已驗；poster59Path 仍係 stub（回 ""），D-12 出圖批先恢復。
- **Q6 忠告卡**：憑 rumor_chung_advice，下一次文藝片試鏡多一句鍾楚凝忠告（對白原話），用一次即清；掛試鏡流程，唔掛傳聞框架。
- **Q11**：刪 debt_slot_ngai_01 stub 債（STUB_FAVOR_DEBT_SEASON_v1.json 一行），全 repo 0 命中。
- **武指／慈善騷渠道**：武指＝下一次武打通告免試鏡／武師班一堂免費；慈善騷＝下一次司儀類通告免試鏡／台風要求放寬（渠道方向已定，待新設計數字）。
- **刪舊表**：TIER110／REQ110／NAME93／LEADSTAR59／CLEAN100／POSTER59_DATA 等；退役舊測試 11 檔（giglib36／gigreq110／name93／gig56／poster59_static 等）。
- **新測試**：test_gig229_* 8 檔共 483 斷言（years 50／tiers 97／pack 50／counts 51／trigger 78／grant 75／press94_advice 51／stagger 31），全部 PASS。

## 驗收

- `node --check` 全檔過（每批）。
- Suite：`qa131/run_suite.sh` **312 PASS／10 FAIL**。10 項 FAIL 全部係已知 pre-existing（flash51／rumor49／slot50／soft_tip_111_restore／start53／weave43／weave44／weave49／wf5_87／wrap38），逐個直接跑對照 main 95baf7e 失敗原因逐字相同。演變：312/13→313/13→314/13→307/10→308/10→309/10→310/10→311/10→312/10（B3 退役 giglib36／poster59＋修好 pacing35，少咗 3 項）。
- In-memory 抽查全部 PASS：240 張載入（1990:94／1991:79／1992:67）、1990 板面、觸發隱藏→上板、即派映射、五級乘數、60 日提早窗邊界。
- SAVE key／softRev（s107）／?v=（v20a10）零改動。

## 偏離 SPEC／已知缺口（等裁定，唔阻落地）

1. **《星夜迷離》新庫 0 命中**：陸支線 Beat 3 替工通告寫漏咗，live 開唔到。唔可以私自加第 241 張——要另開票補寫（加一張／改一張現有觸發通告）。
2. **新庫分布缺口**（B3 量度，已釘入測試）：① 4 張稀有大碟日薪 3080，微超 DUR90「高」帶上限 3000（gig_1992_rec_107–110）；② 九龍電視台首週入門缺口（唯一冬季 1990 工要演技 30／68，開局演技 18 報唔到）；③ 94 個零 loc-week（1990:38／1991:18／1992:38），錯峰保底填唔到。
3. **7 張臨記通告按 SPEC §2.9 表照計擔正**（例 gig_1990_ad_110 臨記 ad_av 廣告主角、gig_1992_variety_106 臨記 variety_special 主持頂位）——表本身無 category 過濾；要加過濾係 spec 問題，唔係實裝 bug。角色閘（awards188IsLead）仍可經臨記通告開。
4. **seal_rare.png 未有**：稀有 tier 冇對應印章圖，onerror 隱藏唔爛圖，但稀有卡暫時冇印章——美術批補一張。
5. **FAVOR_DUE 幫忙通告**：新庫無教學債對應通告，gigId 繼續 null（只剩現金／禮物還款路）。
6. **Rival 第 2／3 輪**：同一張 gig id 重用撞已完成，B5 閘住唔開局；rematch 邏輯另開票重寫。
7. **D-11 通知時機**：觸發通知喺首次開板嗰陣先發，唔係觸發條件達成嗰刻。
8. **B6 commit message 數字筆誤**：寫咗新測試「73 斷言」，實際係 75（code 同測試本身無錯）。

## 要 live 實駕先判到（瀏覽器死，押後）

開局→第 39 週第一張配角、頒獎禮全程、引薦／即派實機流程、新庫真載入、1990 板面豐富度、報紙分類實機、忠告卡實機。
