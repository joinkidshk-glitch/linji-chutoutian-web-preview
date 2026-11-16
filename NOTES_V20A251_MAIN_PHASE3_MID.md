# NOTES_V20A251_MAIN_PHASE3_MID

v20a251：主線實裝中期批（N7–N12＋N19＋近鏡 closeup39）。
基底 main `3994f56`（v250）。工作副本 `linji-work251`，分支 `v20a251`。
三路工人：A 主線 JSON、B 16 張新通告、C `index.html` 接線＋測試；統籌核實＋resync＋落地。

## 1. 改動總覽（25 檔，＋932／−136）

| 檔 | 改動 |
|---|---|
| `content/story_detail_n1_to_n17.json` | 21 節點（20→21）：7 標題＋7 場面 21 beats＋closeup39 新節點＋3 處對白微調＋N19 artId |
| `content/gigs_new.json` | 251→267（＋16 張即派新通告，＋519／−0） |
| `index.html` | GRANT229 加 B 組 17 鍵（17→34 鍵，零 wildcard）；44205→44222 行 |
| `tests/`（15 檔＋1 新） | 計數 251→267、釘行 resync＋17、9 項 A 改動 resync、新載入模擬 `test_gig229_v251_c.js`（35 項） |

## 2. 逐章改動（主線 JSON，工人 A＋統籌）

- **標題統一**（用戶拍板短詞）：N7 暴雨、N8 化妝間、N9 卡座、N10 酒廊、N11 黑西裝與舊風褸、N12 墊、N19 賭枱。Fallback 表（CALIB60／STORY_TITLE_SOFT）唔郁，跟 v250 前例。
- **對白重抽**：live JSON 做底、施工單做 delta，逐字 set-diff（對白 93 句、系統 61 句）。實改 3 處：N8_c 引開記者句補外層 `"`（施工單 §13 明言刻意）、N10_a notes「忠誠」句重寫做何生派工多句「呢單信得過你先俾你」、N12 `openConditionsNote` 年份 1990 春→1992 春。其餘 RW-2 漂移全部 keep live。
- **鋪墊場面 7 個**（21 個新 beats，插各章開頭）：N8 葉敏芝嗰年、N9 阿偉度唔出橋、N10 顧明輝嗰陣＋劇組等錢過年、N11 兩單細工、N12 麥震東嗰一跌、N19 賭片熱。N7 場面一「嗰場近鏡」唔加（closeup39 已承載）。
- **closeup39 獨立節點**（`nodes[7]`，N6F 之後）：`pacing.weekMin: 39`，`when: "1988秋"`（YEARS66 自動 +2 顯示 1990 秋，無手改），beats 3 個（攻略正文＋兩句草稿轉寫書面語），`choices: []`（StoryPlay 已支援空抉擇，出「完成這一節」），`openConditions: ["week_min:39","season_autumn"]`（GATE 無此節點，JSON 欄係真閘）。內容已對返攻略正本 `closeup39` article（L745–762）。
- **N19 artId 補 `story_c19`**：規律 `story_c<舊編號>`（C19→story_c19）；`spChoiceBgCandidates` 搵唔到跌返背景，唔會爛；其餘六章全部「有名無圖」，跟慣例。

### 統籌決定（對照攻略正本後改，parent 可推翻）

1. **N8 B8「你而家做乜」**：live 寫「我」，但攻略正本對白 blockquote 同施工單都寫「你」——live 係孤例，改返「你」。
2. **N19 場面一跟攻略**：老臨記首句「熱過兩次」→「熱過一輪」；阿偉心諗「只差 98 萬」成句刪除——攻略明確「數字只寫在報紙，不寫入對白」，98 萬只留報紙 M5。JSON 而家 98 萬 0 命中。N19 beats 12→11。
3. **N12「一筆數」維持**：keep live（brief 已定）；攻略 L1126 註釋話遊戲原文係「係帳」已經過時，列入攻略跟進項（§9）。
4. **「唔好多嘴」「認返嗰兩句」keep live 係啱嘅**——攻略正本同 live 一致，施工單嗰邊先係舊版。
5. **closeup39**：locId `film_lion` 確認（攻略無寫地點；片場棚前例 N6F／N19）；prevMain 留空（無來源指明前置，週次＋季節閘已夠）；phase P2、title 近鏡維持。

## 3. 即派接線（GRANT229，工人 C）

B 組 17 鍵，全部何生傳呼口吻廣東話 reason，改寫自施工單 §10.2：

| key | gigId | 作品 |
|---|---|---|
| N7:N7_a／b／c | gig_1991_film_122／gig_1991_tv_123／gig_1991_tv_124 | 《半張船票》／《街角照相館》／《碼頭茶餐廳》 |
| N8:N8_a／b／c | gig_1991_variety_109／gig_1991_rec_117／gig_1991_rec_118 | 《咪高峰夜》／《打歌期電台訪問陪坐》／《唱片舖簽唱會助陣排隊區主持》 |
| N9:N9_a（REUSE）／N9_b | gig_1991_film_107／gig_1991_film_123 | 《笑住過肥年・外傳》／《棉廠秋單》 |
| N10:N10_a／b／c | gig_1991_film_124／gig_1991_film_125／gig_1991_tv_125 | 《年尾追數人》／《團年夜》／《歲晚》 |
| N11:N11_a／b | gig_1991_film_126／gig_1991_film_127 | 《龍虎夜廟街》／《沙田夜巡》 |
| N12:N12_a／b | gig_1992_film_120／gig_1992_tv_120 | 《虎門夜襲》／《武館少年》 |
| N19:N19_a／b | gig_1991_tv_126／gig_1991_tv_127 | 《街燈下》／《半頁信》 |

- 全表 17→34 鍵（15 主線舊鍵＋2 廖炳星支線鍵＋17 新鍵），零 wildcard，舊鍵一字不改（對照 HEAD 逐字核實）。
- **N9_a REUSE 防撞**：記錄端一生一次＋派發端 `grant229IsConsumed`（done／shoots／pendingAud／booked）靜默跳過，兩方向都覆蓋；T5b 探針 PASS。
- N12_a 季節 1992 春（施工單寫夏已過時，按節點 1992 春）。
- N12_b `gig_1992_tv_120`《武館少年》唔好同債權兌現 gig `gig_1991_tv_120`《暴雨外景》撈亂。

## 4. 新通告 16 張（工人 B）

251→267。全部跟 v229 SPEC＋D-6（顯示年）；文案按 CONTENT_AUDIT §6（blurb 有場景／人物／衝突、無「招募…日」；synopsis 開場一個畫面、寫明主演全名、有阻力、有時代錨）；製作名按 TITLE_AUDIT R1–R8。作品 151／151 有 posterBrief、臨記 0 有 posterBrief、leadStarId 16／16 null（待拍板，見 §8）。

## 5. 債權 3 筆（授出＋兌現鏈通）

| 債權 | 授出端（已有，工人 A 核實） | 兌現 gig |
|---|---|---|
| `credit_c7_rain` | `story46SettleTick`：`flag_rain_rescue`（N7_a） | `gig_1991_tv_120`《暴雨外景》 |
| `credit_c9_crew` | `story46SettleTick`：`flag_standup_crew`（N10_b） | `gig_1991_film_108`《月夜酒廊》 |
| `credit_c15_stunt` | `story48SettleTick`：`flag_stunt_double`（N12_a） | `gig_1992_film_113`《高空墮樓戲》 |

授出冪等；兌現經 `triggerGigOn` 通用 credit 機制（持有→上板、無債權→唔上板、已兌現→落板），載入模擬三態全部 PASS。JSON 零改動——加欄位先係自創新機制。

## 6. 開閘（D8 定案，GATE 為準）

`STORY_GATE_3Y` 7 條逐字對照 D8 附錄，全部一致，**無改**；JSON `openConditions` 零擴充（`evalToken` 表達唔到 creditGt／fameGt／dualGt，加咗係死條件）。N12 note 年份修正見 §2。

**D8 爭議（記錄在案）**：v251 brief 第 7 項寫「D8 canonical＝JSON `openConditions`」，但 v249 已落地嘅 D8.3 定案係相反——N6–N19 canonical 係 `STORY_GATE_3Y`，JSON 係 legacy 對照，唔擴充。本票按 D8.3 做。如 parent 有意推翻 D8.3 改以 JSON 為準，需明確指示。

## 7. 其餘核實

- **N8 淡香水結算**：已有機制（`story46SettleTick`）：有試用裝扣 1＋`flag_miss_gift_prepared`＋toast；無就 `flag_miss_gift_missed`；冪等。載入模擬三態 PASS。無改 code。
- **N16 `credit_c13_newyear`**：庫內無 trigger gig，留 v252。
- **測試**：13 檔更新（pack 251→267、分佈、press94 mtv 50→52、nat92 E2 94→84——1991 film_lion 夏＋1992 film_lion 春兩個洞由即派新通告填咗）；gate113 新增 v251 斷言；39 個釘行 difflib resync（全部純漂移＋17）；新 `tests/test_gig229_v251_c.js` 載入模擬 35 項 ALL PASS。
- **統籌 resync（9 項 A 改動）**：wf1_80_logic（N19 beats 8–11、nodes 21）、gate136（N12 note「1992 春」例外——DEV 面閘說明，`openConditionsNote` 喺 TEXTFIX55_SKIP_KEYS，唔經 walk、唔出玩家面；同 TWF1 N19 note「1991 春」同一類例外）、story157_index（beats [9,12,13,15,12]／[10,9,12,7,7]／N18/N19 (10,11)、T1990 同類例外）、story157_pack（nodes 21、tail sha 重算 `f5446e0d…1183`）、weave46/48 logic＋static（新短詞標題，pack 側；STORY_TITLE_SOFT fallback 表唔郁）、wf1_80_static（N19 標題「賭枱」）。
- `node --check` 兩塊 inline script 都 PASS。

## 8. 驗證結果

- **全套 suite：314 PASS／11 FAIL**（325 項；v250 基底 314／10＝324 項，＋1 項新測試 PASS）。11 FAIL＝10 項 v250 pre-existing（flash51／rumor49／slot50／soft_tip_111_restore／start53／weave43／weave44／weave49／wf5_87／wrap38）＋**1 項本票已知待拍板 `test_fix88_logic.js` D1**（作品 151 張，9 張新作品＋129 缺 `leadStarId`；補主演 vs 擴大 129 式例外，等拍板——見 v250 NOTES §9.1＋V251_B_REPORT §5）。PASS 數同基底一致，零回歸。
- **verify_gigs.py：33 ERROR／0 WARNING**，全部分類已知接受：Q2 ×10（9 新作品＋129 缺 leadStarId，待拍板）、Q6 ×17（8 新＋9 v250 舊項，片酬帶 vs SPEC §2.10，收窄定修 SPEC 待拍板）、Q17 ×6（全部 v250 舊項，新 16 張零命中）。其餘全部 PASS。
- 載入模擬（統籌獨立覆核）：GRANT229 34 鍵、全部 gigId 喺 267 張庫、零 wildcard；closeup39 在位（`nodes[7]`，weekMin 39，when 1988秋，choices 0）；GATE 7 條在位；三筆債權三態 PASS。

## 9. 已知限制／留後批（唔係本票做）

1. **fix88 D1（等拍板）**：10 張作品缺 `leadStarId`（9 新＋129）。補主演逐張指派 vs 擴大例外——suite 而家 11 FAIL 就係呢一項。
2. **片酬帶 vs SPEC §2.10（等拍板）**：17 張（8 新＋9 v250）。收窄定修 SPEC。
3. **`redeemedBy` 通用缺口（新發現，留後批）**：`br89OnGigComplete` 只為 BR89 映射表 13 張設 `redeemedBy`；9 張 credit-kind trigger gig（含本票三筆）殺青後人情簿「已兌現」展示唔會顯示。影響只係表面（`isGigConsumed` 遮住唔會重派；E4／E5 計數唔讀 `redeemedBy`）。如要修，應喺殺青鉤做通用處理（任何 trigger gig 殺青都設 `redeemedBy`），**唔好**淨加三筆入映射表（會撞 H2／T8 嘅 13 張斷言）。
4. **攻略跟進項（要授權先郁 artifact）**：N12 L1126 註釋過時（話遊戲原文「係帳」，live 已係「一筆數」）；其餘攻略引文已同 live 一致。
5. **v250 遺留**：N6F 第二人稱轉換、N6 唔接邊派唔派散工、CALIB60／STORY_TITLE_SOFT 舊標題（fallback 表，唔影響顯示）、D3 F1 留 v253、D7 N16 留 v252、D11／D12 留 v252、人情 F2／F3／F5／F6／F7／F8／F9／F10 留 v253。
6. **D8 爭議**見 §6。

## 10. 實機抽檢清單（瀏覽器已死，全部押後，唔扮驗過）

- N7–N12／N19 新場面播放、標題顯示；closeup39 第 39 週秋天開閘＋空抉擇「完成這一節」。
- 17 張即派第二朝何生電話派發（尤其 N9_a REUSE 防撞兩方向、N12_a 1992 春）。
- 三筆債權：揀抉擇→翌日結算授出→人情簿顯示→兌現 gig 上板→殺青。
- N8 淡香水結算（有裝／無裝兩路）。
- N12 note「1992 春」唔出玩家面。
