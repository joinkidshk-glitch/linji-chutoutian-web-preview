# NOTES_V20A253 — 主線後期批（N13–N17＋F4／G4）

- 基線：main `a228c99`（v255 已落地，庫 276 張）；本票 branch `v20a253` 由 `72716fb` 開工，落地前 rebase 上 `a228c99`（見 §6）。
- 落地後庫：**282 張**（作品 159／臨記通告 117／補拍 6；1990:111／1991:95／1992:76）。
- GRANT229_CHOICE：34 → **44 鍵**（C 組 10 鍵；N13_c 不派）。

## 1. 主線 JSON（工人 B，commit 83982ed → rebase 後 7e83954）

- `content/story_detail_n1_to_n17.json`：節點 21 → 22（加 `N17_epi`，見 §4）。
- Beats：N13 9→13、N14 12→16、N15 7→10、N16 7→11、N17 15→19（B 加 4 拍湯場，後由工人 C 搬去 `N17_epi`，N17 返 15 拍）。
- 標題（只改 `title` 欄）：N13「企邊」→「高爾夫球」、N15「偶像實力之爭」→「錄音室」、N16「賀歲片」→「飛紙仔」、N17「三年埋單」→「意向」；N14「樂壇前哨」不變。N17 `aftermathHint` 手帳頁名同步改「意向」。
- N14 `when`＋`pacing.when`「1990秋」→「1990春末」（source 舊曆，YEARS66 載入自動 +2，顯示 1992 春末；絕對無手改顯示年）。
- N17 按 v235 清理：`qa.phase5.beat_counts` N17:8→19（N15:7→10 一併更正）；`effects_note` 改做新口徑。beats／choices／synopsis 本身已係 v235 口徑。
- 場面寫法跟 v251：開場敘述香港式書面語、對白＋阿偉（心諗）留廣東話、心諗 beat 用 `speaker: 阿偉 / kind: player` 加括號。黑名單 15 詞零命中；`flags_written` 唔郁。

## 2. 通告：C 組即派 11 位置（工人 A，commit 97c3280 → rebase 後 d0134d0）

重用標準 R1–R5（媒介／級別／季節窗口／角色戲路／無系統衝突）；已編配他用（ENC79 池、現有 GRANT229、BR89 引薦、人情兌現、《星夜迷離》）唔可以再指。

| 位置 | 規格 | 判決 | 新／重用 gig |
|---|---|---|---|
| N13_a《黃金線》 | TV／中級／作品／1992夏 | NEW | `gig_1992_tv_114`《黃金線》男配角（星河長篇劇常駐男配；tv_107《黃金球道》R4 唔過：球會職員時裝處境劇） |
| N13_b《西環新組》 | 電影／中級／作品／1992夏 | REUSE | `gig_1992_film_102`《西環新組》男配角（標題／格位全啱；V249 建議嘅舊 film_102《笑星大作戰》已不存在） |
| N13_c | — | 唔派 | v249 已裁決 |
| N14_a《主打歌》MV | 唱片／高級／作品／1992春／主唱陸柏言／演技 85、歌藝 55、台風 65 | NEW | `gig_1992_rec_111`《主打歌》MV：銅鑼灣街頭男主角（rec_108 同名同主唱同 req，但 1992秋，R3 唔過；rec_108 留返做普通 gig，唔刪） |
| N14_b《樂壇洗牌》 | 唱片／初級／臨記通告／1992春 | REUSE | `gig_1992_rec_201`《樂壇洗牌》新人合唱單曲：旺角和音男聲 |
| N14_c《頒獎禮前哨》 | 廣告／中級／作品／1992春 | NEW | `gig_1992_ad_109`《頒獎禮前哨》廣告主角（西裝，productGender M，品牌紳度） |
| N15_a《櫥窗少年》 | 廣告／中級／作品／1992秋 | NEW | `gig_1992_ad_110`《櫥窗少年》廣告主角（寫真集，品牌金廊映像） |
| N15_b 影展主題歌鋼琴版錄音 | 唱片／中級／臨記通告／1992秋 | REUSE | `gig_1992_rec_202` 影展主題歌鋼琴版錄音（主唱沈映雪） |
| N16_a《賀歲大鑊：廟街兄弟》 | 電影／中級／作品／1992冬 | NEW | `gig_1992_film_113`《賀歲大鑊：廟街兄弟》男配角（笑匠拍檔男二；V249 話 REUSE film_102，但新庫 film_102 已係《西環新組》N13_b 用咗；film_103 R5 硬失敗：trigger `credit_enc83_liu_patron`） |
| N16_b《笑爆賀歲》 | 電影／中級／作品／1992冬 | REUSE（附帶偏差，見 §7） | `gig_1992_film_104`《笑爆賀歲》男配角（玩家角色係「泰斗的徒弟」，唔係規格「茶樓太子爺」） |
| N16_c《聖誕中環》 | 廣告／中級／作品／1992冬 | NEW | `gig_1992_ad_111`《聖誕中環》廣告主角（聖誕禮物，品牌樂安百貨） |

- 淨效果：6 張 NEW 作品，0 張新臨記通告；庫 276→282。
- 六批 regen 驗證＋`full_verify_checks.py` 全部 exit 0、硬 FAIL 0（認證標準 WORKS 0/0、E1 0/0）。`gigs_new.json` 同 `~/workspace/linji-gig-redesign/regen-v2/gigs_new_v2.json` byte-identical。
- Verify 腳本期望＋SPEC-v2.md §1＋full-verify.md §3 已同步（只存喺 `~/workspace/linji-gig-redesign/regen-v2/`，唔係 repo 入面；見 §7）。

## 3. index.html：ECHO89／N16 債權／D7／F4／G4／湯場 hook／N14 季節（工人 C，commit 753bed0 → rebase 後 b4e7264）

- **N14 閘門**：`STORY_GATE_3Y` N14 `seasonIn: ["秋"]` → `["夏","秋"]`。理據：N13 本身閘夏，完成已是夏／秋；單改春要等到 1993，N14＋N15＋N17 全死（軟鎖）。故事時間春末但最早可播係夏，相差約一個月，係鏈次序逼出嚟嘅取捨，已寫入閘註解。`CALIB60_NODE_WINDOWS` N14 同步 `seasons:["夏","秋"]`、`whenLabel:"1992 年夏／秋"`。實測真 `evalGate3Y`：1992-07-01 夏開、1992-09-01 秋開、1992-05-31 春末唔開、fame 50 唔開、N13 未 done 唔開。
- **ECHO89 9 句**：插 `endingInserts410` 陣列最前（章節次序 N13→F4→N15→N16），上限 3→4（一名玩家最多同時中 4 支新旗）。旗：`flag_side_tv`／`flag_side_film`／`flag_side_undecided`（N13）、`flag_stay_mind`／`flag_leave_mind`／`flag_undecided_mind`（F4）、`flag_vocal_polish`／`flag_vocal_train`（N15）、`flag_newyear_improv`（N16）。`qa131/drive157.py` 硬編碼副本已同步。
- **N16 債權 `credit_c13_newyear` 結局頁兌現**：持有未兌現債權行到結局頁，出一句專屬回望（副導「出年賀歲片開拍，第一個打俾你」→ 1993 年賀歲片優先試鏡位，遊戲期外結局文案交代）；標示 `redeemedBy = "ending_c13_newyear"`（防之後經 gig 重複兌現）；通用已兌現區塊濾除此債權，免出錯句。無此債權嘅玩家無事發生。
- **D7 核實**：作品類即派 gig 計一個作品（`careerStats95.total`＋1、入作品牆、計提名數），臨記通告類只計 total，唔入牆／唔計提名。測試 `test_gig229_grant.js` T11（11 個斷言）釘死。
- **F4／G4 標題**：`CHOICE47_NODES` title：F4「何生問：走定留」→「太空人」、G4「阿媽煲咗湯」→「一碗湯」。
- **N14 季節同步**：`lockedHint`「秋天才開放」→「夏天起開放」；`openConditionsNote`「1990 秋」→「1990 夏／秋」；beat 4「1990 年秋，天星音樂大堂」→「1990 年春末，天星音樂大堂」；`eraTag` → `era_1990_spring_music`。
- **標題平行表同步**：`STORY_TITLE_SOFT`（N13→高爾夫球、N15→錄音室、N16→飛紙仔、N17→意向）、`CALIB60_NODE_TITLES`、`STORY_HINT_SOFT` nextHint（N12→高爾夫球、N14→錄音室、N15→飛紙仔）、N14 lockedHint「秋才開啟」→「夏起開啟」、N13 nextHint 季節「秋」→「夏／秋」。「1992 年冬 · 三年埋單」（結局卡日期行）同「三年埋單・手帳總結」（總結頁標題）係結局本身嘅名，留返唔郁。
- **N17 湯場 hook（§4）**。

## 4. N17 尾聲湯場（獨立節點 `N17_epi`）

- B 加喺 N17 beats 尾嘅 4 拍湯場唔可以留喺 beats 入面：(a) beats 播完先出前夕抉擇，湯場會喺揀之前播，時序倒轉；(b) E4 crisis beat 用 `splice(beats.length-1, 0, crisis)` 插最後一拍之前，會跌入湯場中間拆散成幕。
- 定案：湯場搬去獨立 JSON 節點 `N17_epi`（`title:"返屋企食湯"`，`playerOffer:false`，`choices:[]`，`openConditions:["N17"]`，`pacing.weekMin:153, minDaysAfterPrev:0, prevMain:"N17"`；4 拍原封不動，阿偉心諗「寫滿我三年行過嘅路」，無「圈格」）。
- 流程：`ending410AfterEveChoice` 拆三段——記 pending（`S.flags.pendingEnding410Epi`＋`saveQ` 落檔）→ 同步 `StoryPlay.start(N17_epi, {force:true})` → 湯場播完經 `ending410AfterEpi410` 繼續行結局判定（判定＋呈現本體抽出做 `ending410ResolvePresent410`，兩路共用）。`pickChoice` N17 hook 加守衛（湯場已接管 `_sess` 嗰陣唔清 session）；兩個 `finish-empty` 處理點截聽 `N17_epi`。Reload 死局已處理：`enterHome` 加恢復路（跟 conseq61 `pendingEnding` 模式），返屋企重播湯場，播完繼續判定；開唔到直接行判定。
- N17 beats 19→15，尾拍只剩一句回想「阿媽那碗湯」（唔係湯場本身）。
- 測試：`test_story157_pack_static.py`（節點 21→22、pack SHA 重算）、`test_story157_index_static.py`（N17 15 拍＋會議室收尾係最後一則＋N17_epi 4 拍／playerOffer:false／無圈格）、`test_weave410_logic.js`（72/0）。

## 5. GRANT229 entries（統籌，commit 1b76552 → rebase 後 f39345c）

10 鍵加喺 `GRANT229_CHOICE`（N12 之後、N19 之前；reason 跟舊例寫何生電話口吻，提及作品名＋角色）：

| key | gigId |
|---|---|
| N13:N13_a | `gig_1992_tv_114` |
| N13:N13_b | `gig_1992_film_102` |
| N14:N14_a | `gig_1992_rec_111` |
| N14:N14_b | `gig_1992_rec_201` |
| N14:N14_c | `gig_1992_ad_109` |
| N15:N15_a | `gig_1992_ad_110` |
| N15:N15_b | `gig_1992_rec_202` |
| N16:N16_a | `gig_1992_film_113` |
| N16:N16_b | `gig_1992_film_104` |
| N16:N16_c | `gig_1992_ad_111` |

- N16_b reason 按實際 gig 角色寫（「做泰斗的徒弟」），唔寫規格「茶樓太子爺」，免承諾一個 gig 入面無嘅角色（見 §7）。
- 測試同步：`test_gig229_grant.js` T0 34→44 鍵、T1 32→42 映射（加 C 組 10 個 `choiceMaps` 斷言）、「無關抉擇→唔派」改用 `N13:N13_c`（N13_a 而家係有派，舊斷言用佢做反例已失效）；`test_gig229_v251_c.js` 34→44 鍵＋C 組 10 鍵對照＋10 個 reason 非空＋N13_c 不派斷言。

## 6. Rebase 上 v255 main（`a228c99`）

- v253 開工基線係 `72716fb`；期間 v255 落地（庫 269→276，ENC79／DRAFT 11 張死 id 重對）。落地前 `git rebase origin/main`，4 個 commit 全部 replay 成功。
- 衝突只喺 A commit（97c3280）嗰步：`gigs_new.json` 自動合併（核實：對 main 淨係多 A 嘅 6 張新 gig，v255 7 張 byte-identical）；8 個測試檔共 27 個 hunk，全部係計數 276 vs 282（＋nat92 分佈數），逐個 hunk 揀 282 一邊解，`test_gig229_grant.js` 頭註合併（v255 ENC79/DRAFT 文案＋282 計數）。解完 8 檔測試全部 PASS 先繼續。
- 統籌 commit（1b76552）嗰步再撞 `test_gig229_grant.js` 頭註一個 hunk：HEAD 嘅 T0/T2（v255 live 文案）＋我嘅 T1（42 映射＋C 組）合併。
- Rebase 後 `git diff origin/main`：19 檔，+826/−124。GRANT229 keys 實測 44；兩檔 grant 測試 ALL PASS；`node --check` 通過。

## 7. 已知限制／未做完／新發現

- **N16_b 角色缺口**：film_104 玩家角色係「泰斗的徒弟」（賀歲義演），全文無「茶樓」，對唔上施工單規格「茶樓太子爺」。重用判決基於標題＋格位＋季節＋級別＋無 trigger＋storyKey；另開第二張《笑爆賀歲》會撞標題，更差。GRANT229 reason 已按實際角色寫。故事層要唔要改文案對齊，留俾之後決定。
- **film_113 引起 2+2 合併診斷超**（§3 認證標準依然 0/0，唔閘）：soft-cap 超 2 個（鍾楚凝電影 1992：10/9；胡美琳電影 1992：10/9）＋每媒介 Q13 超 2 個（廖炳星電影 1992冬：4；胡美琳電影 1992冬：4）；跨媒介 Q13 診斷 27→28。根因：N16_a 必須係 1992冬賀歲喜劇、廖炳星做笑匠 lead；每格第 4 個 lead 係已存在嘅 E1 extra `gig_1992_film_204`。改角方案（supportF 鍾→韓、leadF 胡→江）會削弱故事啱位，已否決；記做 full-verify.md §3／§5 診斷偏差。
- **「兌現後唔再計結局數」同 live code 出入**（工人 C 發現）：工單寫兌現後唔再計結局數，但 `endingFavor410`／`favorLedgerCounts` 嘅 `creditsHeld` 根本唔讀 `redeemedBy`，已兌現債權仍計入 E4／E5／E3 數字（BR89 已兌現嘅亦然）。標示作用係防重複兌現＋顯示，唔係扣數。玩家面兌現文案無寫呢句假 claim。若果真係要兌現扣數，要改計數口徑，係另一票。
- **N14 eraTag**：工人 A 報告話仲係 `era_1990_autumn_music`，但核實 live JSON 已經係 `era_1990_spring_music`（工人 C 已改）；A 嘅講法過時，唔使跟進。
- **N14 雙《主打歌》**：庫入面而家有兩張《主打歌》MV gig（rec_108 秋＋rec_111 春）。rec_108 係 D12 時代遺物，留返做非即派普通 gig，唔刪。
- **SOFT N1–N12 舊名滯後**（例如 N1「先學做動作戲／先賺」、N7「暴雨救場」），v250／v251 遺留，唔喺呢票範圍。
- **regen-v2 同步檔唔喺 repo**：SPEC-v2.md／full-verify.md／六批 verify 腳本期望嘅更新只存喺 `~/workspace/linji-gig-redesign/regen-v2/`（唔係 git 入面）；呢票 commit 只包 repo 入面嘅 `gigs_new.json`＋測試。統籌決定：regen-v2 目錄本身係工作區留檔，唔帶入 repo。
- **nat92 分佈釘**：E2 三年全板 0 地點-週 87→70（1990:21／1991:21／1992:28）；film_harbour 第一週全週 0 缺口仲喺度（film_110 acting 70 中級，開局接唔到），已知分佈問題，唔喺呢票範圍。F2 錯峰合資格 264→270。
- **湯場 hook 未實機驗證**：前夕揀完→湯場 4 拍→結局頁要等瀏覽器實機跑，測試只覆蓋邏輯層。
- **唔喺呢票**：N6F 第二人稱轉第三人稱、N6 唔接派唔派散工（等用戶逐條拍板）；BR89 人情對照表（跟人情兌現全盤做）；ENC79／DRAFT 死 id（v255 已落地）。

## 8. 測試

- 全套 suite（工作副本跑兩次）：第一次 **TOTAL PASS 306 FAIL 19**——9 個新 FAIL 全部係測試期望滯後（index.html 淨 +115 行令 8 個靜態釘行測試漂移＋pack 節點數 21→22），唔係功能回歸；resync 工人用 difflib 對位（`origin/main` 44,462 行 → 工作副本 44,577 行；6 個 insert 段＋14 個 replace 段，0 個 delete 段），逐個錨點核實內容逐字相同、純漂移，內容真改咗嘅錨點零個；第二次 **TOTAL PASS 315 FAIL 10**，10 項全部已知 pre-existing（flash51／rumor49／slot50／soft_tip_111_restore／start53／weave43／weave44／weave49／wf5_87／wrap38）。
- 工人 C：`test_weave410_logic.js` 72/0、`test_gig229_grant.js` T11 11 個新斷言 PASS、`test_weave410_static.py`、`test_weave47_static.py`、`test_weave48_static.py`、`test_story157_index_static.py`、`test_story157_pack_static.py`、`test_weave46_static.py`、`test_gate136_static.py`、`test_calib60_static.py`、`test_years66_static.py`、`test_weave47_logic.js`、`test_weave48_logic.js`、`test_br89_logic.js`、`test_story_gate136_logic.js`、`test_calib60_logic.js`、`test_lock78_ending.js`、`test_conseq61_logic.js` 82/0、`test_progress71_logic.js`、`test_ladder95_logic.js` 45/0；`node --check` 通過。
- 工人 A：六批 regen 驗證＋full check 全 PASS；8 個受影響測試逐個跑過 ALL PASS（pack／grant／press94／years／dur90／nat92／v251_c／awards63）。
- 統籌：rebase 後 grant 兩檔 ALL PASS；`node --check` 通過。
