# NOTES_V20A159_P1 — 感情線重排實裝 Phase 1（曉晴／采兒／Vera）

- 分支：`v20a159`，base main `e08a070`（v148）。**唔落地**：唔 merge、唔 push，等統籌驗證。
- 設計來源：`~/workspace/linji-story-sidelines/romance-revamp-draft.md`（383 行）。
- 範圍：排他鎖系統＋約會系統＋送禮分層（三人）＋costsDay 殘留＋「全佳 7 分」查實＋三條弧線 commit 骨架。
  唔做：藍／徐／海媚任何內容（Phase 2／3）；寶珊手工禮物；鄧麗萍（v152 刪緊）；12 星巧遇（ENC79）唔郁。
- 紀律：唔改 SAVE key（`starVolunteer_map_v19w`）／softRev（`s107`）／`?v=`（`v20a10`）；
  唔直改 content pack JSON（喜好分層＋反應句經載入後覆寫 `rom159ApplyGiftOverrides`，runtime 注入）；
  R_hiu_* 故事節點本身唔郁（v158 支線票嗰邊做緊，落地由統籌 rebase 對衝突）。

## 1. 改動對照

| 位置 | 改動 |
|---|---|
| `StoryOC.bumpRel`（L24796 前後） | 排他鎖中央凍結：鎖定後非鎖定女角 rel 加減都唔計（return 現值）；首次衝上 rel 5 經 `rom159CheckLock` 鎖定／rel 4 軟提示 |
| `GiftShop.prefKind` | 最愛分層：`favorites` 先於 `likes`，回傳 `"favorite"` |
| `GiftShop.calcDelta` | 最愛 +2；有最愛分層嗰位喜歡 +1（冇分層嗰位如藍／徐／鄧維持原 +2，唔郁佢哋經濟）；普通 +1；唔鍾意 -1；重複減半不變 |
| `GiftShop.reactionEntry`／`reactionLine` | 最愛無專屬句 → 退回同 item 喜歡句（唔直接跌去普通句）；fallback 加最愛行 |
| `GiftShop.canGive`／`giveGift` | 鎖定拒收：鎖定後其他女角唔收禮，禮物唔扣（`canGive`＋`giveGift` 雙重擋） |
| `GiftShop.giveGift` 回傳 | **拎走 `costsDay:true` 殘留值**（送禮唔耗日，現行試玩閘規則；呼叫方 `doGiveGift` 一向睇 `softSocialCostsDay`，唔睇呢欄） |
| `openGiftPick` | 偏好標記加「最愛」 |
| `giftGateBadge` | 鎖定拒收 badge 顯示「已鎖定」（唔係「未開放」） |
| pack 載入後（L31594） | 呼叫 `rom159ApplyGiftOverrides()`（必須喺 `GIFT_PREFS`／`GIFT_REACT` 兩句賦值之後，否則注入嘅 byKey 會俾 pack 賦值蓋走） |
| `commit48Available` | 加排他鎖條件：只可以 commit 鎖定嗰位；未鎖嗰陣 `rom159LockedWho` 內含遷移（舊檔有人已 ≥5 即鎖佢） |
| `StoryPlay.start` 預備鉤（L27242） | 加 `rom159PrepareNode`（contra98 之後） |
| `addLocTalkGiftActs` | 傾談掣撞到封頂嗰陣留返、撳落去只講原因；加「約佢出街」掣（未達條件嗰陣同樣留掣講原因，唔靜默消失） |
| `doTalk` | 撞到上限閘（有未完成節點 offer 嗰陣照傾得）；傾談成功計一次撞到；傾談結果 modal 加「約佢出街」＋「交換電話號碼」掣 |
| `people72Html`／`renderPeoplePane` | 手帳人脈頁加「感情線」一格（六人狀態＋鎖定橫幅＋本週撞到／約會／電話＋Call 機約掣） |
| `openLoc`／`enterHome` | `rom159FlushNotices()`：rel 4／rel 5 待發通知彈 modal 一次（劇情進行中／已有 modal 嗰陣唔彈，下次再試） |
| ROM159 主 block（L41675 起） | `ROM159_WOMEN`／`ROM159_DATES`／`ROM159_XU_PRICES`／`ROM159_GIFT_OVERRIDES`＋全部 `rom159*` 函數＋`CMT_vera_commit` 節點＋`COMMIT48_DEFS.CMT_vera_commit` |
| `tests/test_rom159_static.py`（新） | 76 項：紀律＋標記＋行號釘＋costsDay＋全佳＋pack sha 對照＋pristine 反證 |
| `tests/test_rom159_logic.js`（新） | 69 項：抽 ROM159 純函數＋stub 跑行為（鎖／遷移／送禮拒收／約會閘／撞期／結局預備鉤／覆寫數據；C2／D2 共 6 項係 CheckLock 修正嗰陣加） |
| `qa159/resync_travel114.py`（新） | travel114 行號 resync 腳本（一次性：--apply 後測試入面已係新行號，重跑會 KeyError，見 §8） |
| `qa159/drive159.py`／`qa159/probe159.py`／`qa159/probe2.py`（新） | 實駕腳本＋兩支 probe（probe 係 run 3 失敗診斷用，唔係交付測試） |

## 2. 排他鎖（已拍板，照做）

- 閘值：邊個先到 **rel 5** 即鎖定（`flag_romance_locked`＋`S.flags.romance_locked_who`，存 `S.flags`——`StoryOC.setFlag` 只存 boolean，存唔到邊個）。
- 鎖定前六人可平行培養；鎖定後唔可以轉；crisis BE 唔解鎖。
- rel 4 軟提示：「你哋越嚟越近……再行落去，就要揀喇。」（toast＋手帳／地點 modal，每人一次）。
- rel 5 即場提示：「你心入面已經有人喇。其他人唔會再同你親近落去。」（toast 即刻＋modal 下次開地點／入屋嗰陣彈一次；劇情進行中唔彈）。
- 鎖定後其他女角行為表（逐項實作）：
  - 傾談：照傾得，純對白（傾談本身唔寫 `S.story.rel`；故事節點入面嘅 rel 加成經 `bumpRel` 中央凍結）。
  - 送禮：唔收，禮物唔扣（`canGive`＋`giveGift` 雙重擋；地點面板 badge「已鎖定」）。
  - 約會：掣唔開，寫明原因（面板掣／選擇器／手帳 Call 機掣同一閘 `rom159DateGate`）。
  - 撞到：照撞到，地圖出沒唔變；撞到對白會變——呢期未寫變體對白（見未解決 §6 第 3 項）。
  - 主線／支線節點：照播，rel 加成凍結（`bumpRel` 中央）。
  - 已鎖定嗰位：一切照常。
- 鎖定唔影響事業線：通告／訓練／頒獎禮／結局事業軸照行（鎖只凍結感情 rel）。
- 舊檔遷移：未鎖但有人已 ≥5（舊檔／直接寫入）→ 第一次讀鎖嗰陣鎖最高嗰位，同分按 hiu＞choi＞vera＞lan＞xu＞mei。
- 海媚嗰行：名禁令由 v151 拎走——未落地之前，本票唔寫佢真名，玩家面一律用稱號「嗰位當紅花旦」。

## 3. 約會系統

- 三個入口：① 地點面板「約佢出街」掣 ② 傾談結果 modal「約佢出街」掣（撞到即場約）③ 手帳人脈頁「Call 機約佢出街」掣（要先喺傾談嗰陣撳「交換電話號碼」；Call 機＋電話亭，唔係大哥大）。
- 第一次約一定要見過面先（`talkMetOk` 或 meet 節點 done）。
- 地點（現有 15 地點，唔發明新地點；事務所／醫院唔做約會地點）：
  - 林曉晴：星河電視台廠景天台 $60／獅子山製片外景 $40／廟街夜市 $50／金龍茶餐廳 $35。
  - 周采兒：紅棉影業首映 $90／海港廣播 $60／金龍茶餐廳 $35。
  - Vera：中環廣告 $120／金鐘創意 $110／天星音樂 $80／金龍茶餐廳 $35。
- 約會耗一日（`tickDay`，嗰日唔接通告、唔訓練）；約之前選擇器列明每個地方使幾多。
- 頻率：每人每週最多 1 次；一星期只可以約一個人（`dateWeekWho`）。
- 回報：約會本身唔加分，場內一個抉擇先加減——講啱 +1／講錯 -1（每場 12 個地點各一組專屬對白）。
- 撞期取捨（簡化版 C10 模式，唔做完整分支樹）：約會嗰日撞正拍攝日（`weekPlan` 係 `shoot:`）／試鏡日（`weekPlan` 係 `job:`，即已報名待試鏡）→ 彈一個掣抉擇：
  - 「陪佢去約會」：約會照去，嗰日拍攝／試鏡開唔到工，檔期拖後（shoot 嗰日唔執行，限期壓力留返——唔係假代價）。
  - 「開工行先（好感 -1）」：唔去，rel -1。
- 簡化說明（寫死，唔好日後當 bug）：
  - 草稿話「約定聽日」，實裝做**即日赴約**：約會耗嘅就係今日，唔寫入聽日排程（排程引擎冇「聽日約會」槽位，硬寫會撞爛 `weekPlan`）；邀約文案一律寫「今日收工」，唔寫「聽日」。
  - 電話約唔另開電話亭畫面：交換電話號碼後，喺屋企手帳「人脈」頁撳「Call 機約佢」即開同一個約會選擇器（Call 機留言本身唔耗日，約會本身耗一日）。

## 4. 送禮機制（只做曉晴／采兒／Vera）

- 分層（載入後覆寫，pack JSON 零改動）：
  - 林曉晴：最愛 2——菠蘿油＋奶茶券、美珍蛋撻禮盒；喜歡——保溫瓶、手作甜品盒、原創卡帶、髮夾組；唔鍾意（無）。
  - 周采兒：最愛 2——蘭芳咖啡豆小包、採訪用空白拍紙簿；喜歡——原創卡帶；**新增唔鍾意 2——淡香水試用裝、海外時裝雜誌合訂**（已拍板）。
  - Vera：最愛 2——海外時裝雜誌合訂、淡香水試用裝；喜歡——簡潔髮夾組；唔鍾意（現行）——菠蘿油、蛋撻禮盒。
- 分層數值：最愛 +2／喜歡 +1（有分層嗰位先；藍／徐／鄧冇分層，喜歡維持原 +2）／普通 +1／唔鍾意 -1；重複減半、每週軟頂 +2 不變。
- 反應文案：8 句新寫（最愛 6＋采兒 dislike 2），理由跟草稿 §4.2（禮物意思由收禮物嗰個人嘅故事決定；同一盒手作甜品唔同人唔同意思——嗰個對照係 Phase 2 藍／徐先寫得齊）。
- 機制沿用現行：每日每人 1 份、每週軟頂、重複減半、唔耗日。
- 寶珊手工禮物唔喺呢期（Phase 2）；藍／徐／海媚 prefs 唔喺呢期。

## 5. 「全佳 7 分」查實結果

- **code 入面唔存在「全佳」呢個閘門。** `index.html`／`content/`／`tests/` grep「全佳」零命中（pristine e08a070 同樣零命中）。
- 「全佳 7 分」只係 rel 累積上限嘅校準說明，出處：
  - `index.html` COMMIT48 註解：「每條線 meet(1)＋push1(2)＋push2(2)＋crisis(2) 理論最高 7」；
  - `~/workspace/linji-story-sidelines/index.html` L181／L263、 `~/workspace/linji-branch-audit.md` L111：「rel 累積門檻 6（全佳路徑 7 分，任何一個負選項即出局）」。
- **決定：保留概念，唔設獨立閘門。** Commit 閘門照舊係 rel ≥6＋crisis done＋1992 秋窗＋排他鎖係佢；7 只係話「全佳路徑最多攞到 7」，門檻 6 容許一次次佳。唔係舊規劃稿殘留，係審計文件嘅講法——草稿 §8 第 13 項話「本稿唔知佢係咩」係因為草稿作者冇對返 COMMIT48 註解。
- Static test 釘死：`全佳` 全檔只出現一次（ROM159 註解嘅查實說明，L41703）。

## 6. 數字定值表（實裝定值，唔使再問）

| 項 | 定值 |
|---|---|
| 排他鎖閘值 | rel 5 鎖定；rel 6 commit（沿用 COMMIT48） |
| rel 4 軟提示 | 每人一次，toast＋modal |
| 約會價錢 | 曉晴 35–60／采兒 35–90／Vera 35–120（分地點，見 §3）；通用茶餐廳 $35 |
| 徐寶珊價錢表（Phase 2 用，呢期只定價） | 中環 $150／金鐘 $140／首映 $120／天星 $100／茶餐廳 $35 |
| 約會抉擇 rel | 好 +1／差 -1（每場一個抉擇） |
| 每週約會 | 每人每週 1 次；一星期只約一個人 |
| 每週撞到上限 | 每人每週傾談 3 次（有未完成節點 offer 嗰陣照傾得） |
| 送禮分層 | 最愛 +2／喜歡 +1（有分層者）／普通 +1／唔鍾意 -1；重複減半；每週軟頂 +2 |
| 撞期代價 | 陪佢＝嗰日拍攝／試鏡開唔到工（檔期拖後）；事業行先＝rel -1 |

## 7. 三條弧線實裝

- pack `R_*_ending` 已有專屬 HE／BE（唔改 pack JSON）：
  - 林曉晴《留低》：HE「留低」／BE「機場送別」。「走」收尾只係 BE 收尾，唔係中途關閉條線；中途移民壓力係 crisis 內容，唔提前關閉 commit（有歧義照呢句，唔自己發明規則）。
  - 周采兒《寫真話》：HE「低調真情」／BE「頭條換關係」。HE 喺 ending 節點再拆公開／低調二揀一（兩種都係 HE）：公開寫 `flag_choi_public`＋fame +1（頭條壓力）、低調唔加 fame（長期忍住唔講）。拆分經 `rom159PrepareNode` 淺拷貝，pack 原 choice 一字唔郁。
  - Vera《睇到我本人》：HE「睇到我本人」／BE「收返專業距離」。本期新寫 `CMT_vera_commit`（1992 秋＠天星音樂，`speakerId:"vera"`），等同曉晴／采兒嘅 CMT offer；曉晴／采兒 CMT 節點沿用 v20a31 原文。
- Commit 閘門骨架（`commit48Available`）：rel ≥6＋crisis done＋1992 秋窗＋**排他鎖係佢**（新增；舊有雙線互斥 `otherFlag` 留返，鎖係真正把關）。
- 排他鎖喺 ending 節點嘅執行（`rom159PrepareNode`，contra98 之後）：
  - 鎖咗第二個嗰陣，呢條線嘅 HE choice 換成「坦白」差一步變體（只寫自己線 BE 旗，唔寫 commit）——跟 v20a98 CONTRA98 先例（commit 旗已立嗰陣佢會先換，呢度守嘅係「鎖咗未 commit」嗰段）。
  - 唔鎖／鎖係佢嗰陣，節點原樣播。

## 8. 測試

- 新測試：`tests/test_rom159_static.py` **76 項，0 FAIL**；`tests/test_rom159_logic.js` **69／69 PASS**（原 63＋CheckLock 修正嗰陣加 C2／D2 共 6）。
- 反證：兩份新測試對 pristine（`~/workspace/linji-pristine159-full/`，e08a070 完整樹）乾淨 FAIL——static 嘅 ROM159 標記／CMT_vera／鎖條件全部唔存在，logic 抽唔到函數；唔 crash。主 script 抽出 `node --check` → `SYNTAX_OK`。
- 全套 A/B（`qa131/run_suite.sh`，正確基線＝pristine e08a070 完整樹 `~/workspace/linji-pristine159-full/`）：**pristine 211 PASS／12 FAIL；工作版 213 PASS／12 FAIL**；diff 只差我兩份新測試。12 項 FAIL 全部係 pre-existing 穩定項，逐個對 pristine 覆驗都係 FAIL（`test_flash51_static.py`、`test_giglib36_static.py`、`test_pacing35_static.py`、`test_poster59_static.py`、`test_rumor49_static.py`、`test_slot50_static.py`、`test_soft_tip_111_restore.py`、`test_start53_static.py`、`test_weave43_static.py`、`test_weave44_static.py`、`test_weave49_static.py`、`test_wrap38_static.py`）。**零回歸。**注意：最小 pristine 副本（`~/workspace/linji-pristine159/`，淨 index.html＋tests＋content）跑出嚟 152／71 係假象——缺 assets 等目錄，唔係有效基線；唔好再用。`test_conseq61_logic.js` 工作版 PASS 82／0。
- 逐份直接覆驗（工作版＋pristine 對照）：`test_br89_deadflag_lint.js` PASS；`test_text55_static.py` ALL PASS；`test_text125_static.py` RESULT PASS；`test_travel114_static.py` RESULT PASS；`test_weave46_static.py` ALL PASS；`test_conseq61_logic.js` PASS 82／0。
- **修正紀錄（全套 A/B 初跑後逐份覆驗捉到 6 項，全部已修）**：
  1. `flag_choi_public` 死旗（br89 捉到）：寫咗但零讀取。修：`endingRomanceState48` 加真正讀取位（`line()` 第 5 參數 `publicFlag`，choi 行傳 `"flag_choi_public"`，`out.public = choice47StoryFlag(publicFlag)`），淨 +4 行。
  2. text55 A6：我嘅註解有「試玩閘」字串，改字做「現行唔耗日規則」，行數不變。
  3. weave46 藍若曦：`ROM159_WOMEN` lan 行有「藍若曦」，測試加 `rom159_block` slice＋放寬條件（附 v20a159 申報註解）。
  4. text125：三個行號漂移（bumpRel ＋8、GiftShop 淨 ＋29）resync，附 v159 註解。
  5. travel114：27 FAIL——行號漂移＋3 個新 `openLoc(` 呼叫點（`rom159ConfirmDate` 約會撞期 modal，全部 `travelFree:true`）。`qa159/resync_travel114.py` 核實舊 44 行係新 47 行嘅子序列 → `--apply`：COUNT 13 不變、FREE 27→30、DEF 53562→54281、WRAPPER 44171→44868。
  6. **CheckLock 遷移食通知 bug（真 bug，實駕 T2 捉到）**：舊 `rom159CheckLock` 先行 `rom159EnsureLock()`——bumpRel 已經先加數（rel 已係 6），遷移見到 ≥5 即靜默鎖咗，跳過門檻分支，lock pendingNotice＋toast 全失（鎖定旗照立，手帳照顯示）。修：先用原始旗 `S.flags.flag_romance_locked` 判斷門檻（≥5 → `rom159SetLock(who, false)` 出通知＋toast；≥4 → 軟提示），遷移放最後只留返舊檔／非 bumpRel 路徑靜默補鎖。Logic test C 段原本捉唔到（CheckLock(5) 嗰陣 rel 仲係 4，冇模擬「先加數」次序）——已修正測試次序＋加 C2（rel 已係 6 嗰陣 CheckLock(6) 都要有 lock 通知＋toast）＋D2（直接 EnsureLock 照舊靜默）。
- **CheckLock 修正後遺症（resync 2）**：修正淨 +4 行（`rom159CheckLock` 41889 段），其後全部行號錨點再 +4，但兩份 static 測試當時未重跑——`test_rom159_static.py` CMT_vera 釘 42289→實際 42293、`test_travel114_static.py` 21 FAIL（其後錨點全部錯 4 行）。已 resync：rom159_static 42289→42293；travel114 其後錨點全部 +4（FREE 42088/42089/42165→42092/42093/42169、DEF 54281→54285、WRAPPER 44868→44872、COUNT 44445/58324/58491/58644/58665/59115 各 +4；COUNT 13／FREE 30 不變），直接 grep 實量核實（DEF／WRAPPER／3 新 FREE 行逐行對返內容）。`qa159/resync_travel114.py` 係一次性腳本（--apply 後測試入面已係新行號，重跑會將新行號當舊行號對位而 KeyError——唔係測試錯，唔使修）。
- 實駕（本地鏡像＋Playwright，`qa159/drive159.py`，56 項）：**run 5：56／56 PASS，0 pageerror，exit 0**；run 4：55／56（淨 T4 電話交換斷言 `is True` 太嚴，code 存 1 係正確值）。
  - Run 1：46／56（T2 CheckLock 真 bug＋T1／T2 notice modal 未彈＋T3b 斷言錯＋T3d 同日傾談上限＋T6 撞期 modal 入唔到）。
  - Run 2：44／56（CheckLock 修正後 T6 全過，但 T1／T2 notice modal 仍然未彈、T4 傾談流程問題浮現）。
  - Run 3：44／56（同 run 2；T1／T2 notice modal、T3b、T4 全組 9 項 fail）。
  - **Run 3 失敗根因（兩支 probe 逐項證實，見 `qa159/probe159.py`／`qa159/probe2.py`）**：
    - T1／T2 notice modal：code 啱，drive 唔夠力。關閉送禮結果 modal 之後會彈入場劇情攔截「飛紙仔殺到埋身」（4 beats：繼續→睇落去→二揀一→好），flush 喺 modal 開住嗰陣正確 defer；probe2 逐步行完劇情→`mt=''`→重開地點→第 5 步 notice modal 即彈（pending 清走）。舊版 `wait_notice_modal` 30 tries 照計夠行，但 run 3 兩次都耗盡——改做 40 tries＋逐步 log 之後 run 4 即過。**唔係 code 問題，唔改 flush。**
    - T3b：code 啱，run 3 係 flake。Probe2 原樣重演 T3a→T3b：pre_mt=''、post_mt=''、toast 正確，條件成立；run 4 同樣斷言即過（pre_mt='' post_mt=''）。
    - T4 全組：**drive bug**。傾談開場係「揀一句開場」二揀一（「問近期有咩通告」／「隨便寒暄兩句」），舊版 `advance_talk` 只識撳「謝謝，我會去睇」／「再傾兩句近況」，行唔到結果 modal。已加開場二揀一撳掣＋tries 10→12；run 4：T4 8／9 過（約會全程：選擇器 $60／揀天台／場面／好抉擇 +1／扣 $60／耗一日／本週計數 1）。
    - T4 唯一剩低嗰項「電話交換成功」：code 存 `st.phone[who] = 1`（同 `softWarn[who] = 1` 一致），讀取口 `rom159HasPhone` 用 truthy（`!!(...)`），1 係正確值；drive 斷言用 `is True` 太嚴（Playwright 傳返嚟 Python `1 is True` → False）。已改做 truthy 斷言，run 5 重跑確認。
  - Run 4 其餘已驗證：鎖定本身（flags＋手帳「已鎖定」橫幅）、三人約會（天台 $60／首映 $90／中環 $120，扣錢／耗一日／rel ±1／每週計數）、送禮分層（喜歡 +1、唔鍾意 -1、最愛 +2、送禮結果文案夾 prefs）、鎖定後送禮拒收（禮物唔扣、rel 唔郁）、傾談照開、T6 撞期 modal（手帳 Call 機開選擇器 → 撞期 modal「今日原本要拍攝：《測試戲》…陪佢去約會／開工行先（好感 -1）」→ 陪佢 → 約會場面 → rel 2→3＋耗一日）。拍攝日係強制日：`openLoc` 先跑拍攝，撞期 modal 只能經手帳 Call 機路徑觸發（地點面板入唔到）。
  - 實駕截圖：`qa159/shots/`（t1_soft、t2_lock、t2_handbook、t4_picker、t4_scene、t4_result、t6_conflict）。

## 9. 未解決事項

1. **撞到對白未變**：草稿 §2.2 話鎖定後撞到嗰陣「對白會變——佢哋感覺到阿偉心有所屬」。傾談對白行 `pickNpcLine`／`NPC_LINES` 通用池，冇按鎖定狀態分流嘅位——呢期未寫變體對白（傾談照傾、rel 凍結已實作）。要做要另開一票（NPC_LINES 加鎖定分支）。
2. **采兒 HE 公開／低調嘅後續代價未兌現**：公開寫 `flag_choi_public`＋fame +1。隻旗而家**唔係死旗**——`endingRomanceState48` 已讀佢（`out.public`，br89 PASS）。未兌現嘅係「頭條壓力」同「低調要長期忍住唔講」呢兩句代價嘅後續節點，兌現要 Phase 2／結局呈現嗰陣跟。
3. **Vera CMT offer 地點**：草稿冇指定 Vera commit offer 喺邊——呢期揀咗 `rec_star` 天星音樂（佢 MV 造型場合，homes 之一）。如統籌想改去電視台打歌後台，改 `COMMIT48_DEFS.CMT_vera_commit.loc`＋`CMT_vera_commit.locId`／setting 兩行就得。
4. **約會即日赴約**：見 §3 簡化說明——草稿「約定聽日」改做即日，係刻意簡化，唔係漏做。
5. **R_hiu_* 重疊**：v158 支線票同時做緊《留低》支線樣本；本票完全冇掂 R_hiu_* 節點本身，只掂共用機制（bumpRel／commit 閘／ending 預備鉤）。落地嗰陣由統籌 rebase＋對衝突。
6. **舊檔 `S.story.rel` 直接寫入路徑**：有啲 dev／遷移路徑直接寫 `S.story.rel` 唔經 `bumpRel`（例如測試／種子檔）——嗰啲唔會觸發即場鎖定，但第一次讀鎖（`rom159LockedWho`／`commit48Available`／手帳）嗰陣遷移會補鎖返。玩家正常遊玩全部經 `bumpRel`，唔受影響。
7. **通知 modal 彈出時機（已查明，唔係 code 問題）**：rel 4／rel 5 通知經 `pendingNotice`＋`rom159FlushNotices`，喺劇情進行中／已有 modal 嗰陣正確 defer。實駕 run 1–3 連續見唔到 modal，係因為關閉送禮結果 modal 之後會彈入場劇情攔截「飛紙仔殺到埋身」（4 beats），舊版 drive 嘅 `wait_notice_modal` 行唔晒；probe2 證實行完劇情→重開地點→notice modal 即彈，run 4 已過。唔改 flush。
8. **CheckLock 修正拖垮行號釘（已修，見 §8 resync 2）**：修正淨 +4 行，但兩份 static 測試當時未重跑，事後先發現 CMT_vera 釘同 travel114 21 FAIL。教訓：改親 ROM159 block 入面嘅 code（尤其 `rom159CheckLock`／`rom159SetLock` 一帶，喺全部行號錨點之前），即刻重跑 `test_rom159_static.py`＋`test_travel114_static.py`，唔好等到最後先一次過驗。
9. **T4 電話旗存 1 唔係 `true`（刻意，唔係 bug）**：`rom159PhoneExchange` 存 `st.phone[who] = 1`，同 `softWarn[who] = 1` 一致；讀取口 `rom159HasPhone` 用 truthy。Drive 斷言原本寫 `is True` 太嚴，已改 truthy。
