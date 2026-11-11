# v20a108・文字清理包（NOTES）

> 範圍：文案精煉 only。唔改數值／機制／劇本情節，唔掂其他審計項。
> Base：main `8d19640`（v20a106）。分支：`v108-text`（只 push 分支，合併由統籌做）。
> **注意：工作期間 v107 入咗 main（`d5c41e8`）**。`git diff --name-only 8d19640..d5c41e8` 證實 v107 只掂 `NOTES_V20A107.md`、8 張新 fullbody 圖、`qa107/*`、兩隻新 test 檔（`test_dlg107_*`），`index.html` 零改動——同本包零重疊，合併預計乾淨。本包維持 `8d19640` base，唔自行 rebase。

## 逐項處置表

### 覆核（分批③已做項，全部「已修・覆核通過」，無需修）
| 項 | 覆核結果 |
|---|---|
| S-3 | B01 卡已瘦身；規則行 `#plan-teach105` 常駐（無逐畫面觸發，trade-off 保留） |
| S-10 | `storyMapHintHtml`「›」釘死＋副行截首句 |
| S-19 | `confirmPlan` 直行；`stressImpactLine34` 全句化；`#nb-stress-detail105` 在位 |
| S-23 | `openLoc` 費用正規化（$X／免費／+1日） |
| S-24 | 唔郁（統籌裁決）。事務所板無「江湖撈家」；E5 指向喺人情頁 |
| S-28 | `gigGapLine34`「現值／需 X（差 N）」 |
| S-35 | 獲聘 modal 三段式（結果→簽約金行→殺青結算行），無成功率行——**本次實駕再驗通過** |
| S-37 | 殺青結算只留 `payWrapNote(sh)` 一段 |
| S-39 | 生活費提示用結算日星期，六／日先出 |
| S-44 | `card_biao_winter`「就嚟到期」；toast 無重複 |
| S-45 | `farMerged105`「第 X–17 幕…逐幕揭曉」 |

### 新做
| 項 | 處置 | 改動 |
|---|---|---|
| S-26 地點板括號說明重複 | **已修** | `openLoc` 加 `S.flags.seenLocWhoHint26`：首次「暫時未見熟人（熟人會隨日子／時段出入；地圖標亮＝在場）」，之後只「暫時未見熟人」 |
| S-42 系統 modal 電報式 | **已修** | `TUTORIAL_ZH_HK` 7 組系統句（MAP／BOARD／TRAIN／NPC／DONE／AUD_FAIL／SHOOT，body＋bodyAlt）全組潤飾；另加 `TEXTFIX55_EXACT` **37 對**（見下「關鍵發現」） |
| S-49 完結一日兩個名 | **已修** | 統一「過一日」：地圖金掣×2、☰選單、確認 modal 標題「確認過一日？」＋掣「確定過一日」。回顧記錄 `early_rest` 標籤「提早休息」刻意保留（S-14 執行類型） |
| S-50 設定 modal「完成」 | **已修** | `openSettingsModal` 關閉掣「完成」→「關閉」（全檔唯一 `label:"完成"`） |
| S-15 提早休息＝小休級 | **已修** | 確認 body 加「呢次只係小休，減壓有限，唔似得瞓足一日咁將壓力清零。」；日結板標題「休息（週X）」→「小休（週X）」。減壓數值不變 |
| S-41 報紙時序易誤會 | **已修（方案 a）** | TEXTFIX 加 `"電視城臨記班底添新血": "入行消息：電視台臨記班底添新血"`，改寫 `np_story_c1_tv_01` kicker，加來源語境；唔改出報機制 |
| S-47 作品牆承諾過頭 | **已修（文案方案）** | 空牆＋note 改做真規則：「有作品圖嘅製作，殺青之後先上牆；冇海報嘅製作（例如電視特輯），完成咗只會記入拍攝簿，唔會上牆。」補圖方案唔做 |

## S-42 關鍵發現（必讀）
Live 教學**唔行 inline `TUTORIAL_ZH_HK` const**：開機 fetch `content/tutorial_zh_HK.json` 成個換走佢，再經 `textfix55SimplePack` 用 `TEXTFIX55_EXACT` 清洗。第一次實駕教學重播見舊句，證實淨改 inline 係死路。修復：覆寫表加／改 37 對（34 新＋4 更新），pack 異文（包括 stale「再打開選單「事態」」→改做進度掣句，順帶對齊 HUB77）全部對應新句；37 個 key 驗證過最多只出現喺一個 content 檔，無跨 pack 碰撞。`content/*.json` 本身無郁。

## S-47 偏離任務建議嘅理據
任務建議寫「電影／有名有姓劇集先有作品圖」，但數據核查推翻咗：海報覆蓋 69 個 gig，橫跨全部 5 類（廣告 15、綜藝 7、電視劇 9、電影 20、唱片通告 18）；唯一無海報嘅電視特輯 gig 得一個（`gig_1988_entry_winter_cny_crowd`《賀歲特輯》）。用類別承諾會講大話，所以文案寫真規則並點名電視特輯。

## 前後對照（節錄；完整清單見 `notes.md`）
- TUT_MAP：「地圖上的地點，就是你可以去的地方；先點地點才看到行動。」→「地圖上面嘅地點，就係你可以去嘅地方；要先撳入地點，先睇到有咩行動。」
- TUT_BOARD：「通告欄可先免費查看；條件未合顯示暫未能報，達標後可接通告（耗一日）。」→「通告欄可以免費睇住先；條件未合嗰啲會顯示「暫未能報」，達標之後先接得通告（接通告要用一日）。」
- TUT_TRAIN alt：「訓練累計夠，社交與觀察課就會開放。」→「訓練儲夠數，魅力課同觀察課就會開放。」（順帶修正 stale 術語 社交課→魅力課）
- TUT_SHOOT：「獲聘後，拍攝日已排進行程。／開工前看手帳和行程，跟進度。」→「獲聘之後，拍攝日已經排咗進行程。／開工之前，記得睇手帳同行程，跟住上面嘅安排去做。」
- TUT_DONE：「教學先到這裡（可跳過；選單可重看）。」→「教學先到呢度（可以跳過；之後喺選單重看）。」——「再撳地圖上嘅「進度」掣」一句刻意保留原字（`test_hub77_static.py` 釘死）。
- S-49：「逛完・過一日」／「提早休息（過一日）」／「確認提早休息？」／「確定休息 +1日」→「過一日」／「過一日」／「確認過一日？」／「確定過一日」。
- S-15：「今日會完結並進入下一日（等同休息）。」→「今日會完結並進入下一日。呢次只係小休，減壓有限，唔似得瞓足一日咁將壓力清零。」；日結標題「休息（週一）」→「小休（週一）」。
- S-41 kicker：「電視城臨記班底添新血」→「入行消息：電視台臨記班底添新血」。
- S-47 空牆：見上表。

## 測試
- 新守門 `tests/test_text108_static.py`：紅線、S-26、S-42（inline＋TEXTFIX live 路徑）、S-49、S-50、S-15、S-41、S-47，＋11 項 v105 覆核 pins。工作副本 0 fail；pristine v106 44 fail（反證）。
- 舊斷言更新（附反證）：`test_guidance34_static.py:43,46`、`test_guidance34_logic.js:222,229,230`、`test_week105_static.py:74`、`test_qa101_static.py:54`、`test_menu72_static.py:30`（名 only）、`test_text55_logic.js:17`（A6，TEXTFIX NPC 句跟新值）。
- 全套：**135 PASS／12 FAIL**（基線 134／12；FAIL 清單完全一致，全部係已知環境性 static FAIL；+1 = 新 test 檔）。`node --check` 主 script 通過（行號 5170–56952）。
- 中途一次 transient 回歸：S-42 初稿改咗 HUB77 釘死句致 `test_hub77_static.py` FAIL，已修復。

## 實駕（`qa108b/drive108b.py`，零 pageerror）
- S-26：醫院板首次長版、第二次短版。S-42：教學重播 TUT_MAP／TUT_BOARD 新句 live；獲聘流程 TUT_SHOOT 新句 live（「獲聘之後，拍攝日已經排咗進行程。開工之前，記得睇手帳同行程，跟住上面嘅安排去做。」）。
- S-49／S-15：金掣「過一日」→「確認過一日？…呢次只係小休…」→「確定過一日」→日結板「小休（週一）壓力 -6」。
- S-41：1 月 2 日電視週刊 modal 全文——kicker「入行消息：電視台臨記班底添新血」、headline「電視台臨記班底添新血 阿偉獲青睞」。
- S-47：空牆新文案。S-50：設定 modal「關閉」。
- S-35 再驗：獲聘 modal「獲聘！《賀歲特輯》拜年群演」＋簽約金 $191 已入帳（合約 $637 嘅三成）＋餘額 $446 殺青嗰日先入帳＋殺青結算聲望 +1·人氣 +3＋支票圖（港城商業銀行）。**注意：真獲聘 modal 標題係「獲聘！」，唔係「何生來電」**（後者只係落選／資料對唔返分支）。
- 截圖：`qa108b/shots/`（`s26_*`、`s42_tut_*`、`s49_*`、`s50_settings`、`s15_*`、`s41_paper`、`s47_wall`、`b6_hired`、`b6_board`、`b6_audition`）。工作紀錄＋drive 細節見 `notes.md`（唔入 repo）。

## 留低未改／交統籌
- 「1988 年春」stale 年份（`story_beats_phase1.json` Ch1、`tutorial_zh_HK.json` TUT_WELCOME）：runtime `years66Walk` 已修正顯示，pack 未改。
- 全部玩家面劇情台詞、結局相關句：按規則留低。
- S-24 按裁決唔郁；落選 modal 成功率行按 v105 範圍留低。
- **AUD91 公佈路徑問題（遊戲機制，唔係文字包範圍，唔修）**：試鏡賀歲特輯後 `S.pendingAud` 有到期記錄（ok=true，revealDay 已到），經「提早休息日結板 → 返回地圖」等咗 4 日（1 月 3→7 日）從未公佈（300ms×10 密 poll 空 mask、空 toast；截圖證實已返地圖）；同一日改行「☰選單 → 手帳 → 事業頁 → 返回地圖」，獲聘 modal 即刻彈出。Code 層面 `goToMapForBrowse` 晨早鏈（報紙→`aud91PresentDue`→WF4）次序正確、`aud91PresentDue` 會 `return true`、`ending78Locked()` 第一週 false——點解日結板路徑唔觸發，靜態睇唔出，需要另開調查。

## 改動檔案
- `index.html`（S-26、S-42、S-49、S-50、S-15、S-41）
- `tests/test_text108_static.py`（新）、`tests/test_guidance34_static.py`、`tests/test_guidance34_logic.js`、`tests/test_week105_static.py`、`tests/test_qa101_static.py`、`tests/test_menu72_static.py`、`tests/test_text55_logic.js`
- `NOTES_V20A108.md`（本檔）
