# v20a108・UI 後續修復包（NOTES・統籌總交代）

> 範圍：審計 `~/workspace/linji-ui-audit/UI_AUDIT.md` 後續包——D-8 二期、文字清理（分批③）、視覺統一（分批④ B 級）、對話呈現微調（用戶 2026-11-12 04:03／04:18 實機反饋）。
> Base：main `d5c41e8`（v20a107 已入；v107 只掂 NOTES／8 張新圖／`qa107/*`／兩隻新 test 檔，`index.html` 零改動）。
> 四分支（只 push 分支，由統籌 squash 合併入 main）：`v108-d8`（`9a8227d`）、`v108-text`（`7723956`）、`v108-visual`（`8822dad`）、`v108-dlg`（`64c00df`）。
> 合併 commits：`407e468`（dlg）→ `394fc7d`（text）→ `036a2f4`（visual，解衝突）→ `ad3b7c1`（d8，解衝突）→ `57251bf`（測試跟進）。
> 紀律：SAVE key `starVolunteer_map_v19w`／softRev `s107`／產品 `?v=` `v20a10` 全冇郁；唔直改 content pack JSON；唔改數值／機制（文案包除外見註）。

## 1. D-8 第二階段：WF4 隨機事件具名講者行新對話組件
分支 `v108-d8`。WF4 盤點 36 事件：全身資產講者只得一位（阿偉）；具名但冇資產（阿媽、霞姐、阿成、昌叔、表姨媽＋25 個功能／泛稱講者）行舊呈現。
| 路徑 | 事件 |
|---|---|
| NEW 獨角阿偉（逐句行 DLG106 舞台：場景圖底＋企立＋表情＋明暗） | cha02、home01、st01、st03、boss01、boss02、boss03、day02（阿偉句表情：neutral×5、think×1、sad×1、happy×1） |
| OLD v105 舊呈現 | 其餘 28 單（set01–set10、cha01、cha03、cha04、home02–04、st02、st04–st11、day01、day03、day04） |
- 新增 `wf4SpeakerId108`／`wf4OnTableIds108`／`wf4DlgExtraCands108`（候補鏈同巧遇一致：UI40 企立→c1 bust→ENC105 剪影→SVG 兜底）／`wf4DlgCharsHtml108`／`wf4BeatStageHtml108`；`wf4PlayEvent` 只改 `beatHtml` 分流。抉擇／結算屏維持舊文字。內容 JSON 零改動。
- 分工護欄：WF4 只 call 現成 DLG106 入口，唔掂組件 CSS／幾何／渲染函數（初版加過嘅 `.wf4-play` 幾何 CSS 已拆返；logic 測試有三條護欄釘死）。
- **雙全身喺 WF4 做唔到**：冇任何一單有兩個有資產講者；三人事件（boss01–03）同樣只出阿偉獨角。要雙全身就要幫阿媽／霞姐等出全身圖（新美術，唔喺今包範圍）。
- **未達標（老實申報）**：modal 內舞台沿用組件原有 in-flow 幾何，實測舞台 342×168px、人物 34×100px——數據層表情切換正確（base 0.6 → think／sad 1.0，圖檔 naturalWidth＞0），但肉眼幾乎睇唔到表情切換。修正屬舞台幾何，歸 v108-dlg 嗰邊；合併後實駕再驗仍然細（見 §7 問題 #2），未修。
- 詳情見 `NOTES_V20A108_D8.md`（D-8 工人原檔，已入 main）＋工作紀錄 `~/workspace/linji-work108a/notes.md`。

## 2. 文字清理包（分批③）
分支 `v108-text`。

### 覆核（分批③已做項，全部「已修・覆核通過」，無需修）
| 項 | 覆核結果 |
|---|---|
| S-3 | B01 卡已瘦身；規則行 `#plan-teach105` 常駐（無逐畫面觸發，trade-off 保留） |
| S-10 | `storyMapHintHtml`「›」釘死＋副行截首句 |
| S-19 | `confirmPlan` 直行；`stressImpactLine34` 全句化；`#nb-stress-detail105` 在位 |
| S-23 | `openLoc` 費用正規化（$X／免費／+1日） |
| S-24 | 唔郁（統籌裁決）。事務所板無「江湖撈家」；E5 指向喺人情頁 |
| S-28 | `gigGapLine34`「現值／需 X（差 N）」 |
| S-35 | 獲聘 modal 三段式（結果→簽約金行→殺青結算行），無成功率行——本次實駕再驗通過 |
| S-37 | 殺青結算只留 `payWrapNote(sh)` 一段 |
| S-39 | 生活費提示用結算日星期，六／日先出 |
| S-44 | `card_biao_winter`「就嚟到期」；toast 無重複 |
| S-45 | `farMerged105`「第 X–17 幕…逐幕揭曉」 |

### 新做
| 項 | 處置 | 改動 |
|---|---|---|
| S-26 地點板括號說明重複 | **已修** | `openLoc` 加 `S.flags.seenLocWhoHint26`：首次「暫時未見熟人（熟人會隨日子／時段出入；地圖標亮＝在場）」，之後只「暫時未見熟人」 |
| S-42 系統 modal 電報式 | **已修** | `TUTORIAL_ZH_HK` 7 組系統句（MAP／BOARD／TRAIN／NPC／DONE／AUD_FAIL／SHOOT，body＋bodyAlt）全組潤飾；另加 `TEXTFIX55_EXACT` **37 對**（見「關鍵發現」） |
| S-49 完結一日兩個名 | **已修** | 統一「過一日」：地圖金掣×2、☰選單、確認 modal 標題「確認過一日？」＋掣「確定過一日」。回顧記錄 `early_rest` 標籤「提早休息」刻意保留（S-14 執行類型） |
| S-50 設定 modal「完成」 | **已修** | `openSettingsModal` 關閉掣「完成」→「關閉」（全檔唯一 `label:"完成"`） |
| S-15 提早休息＝小休級 | **已修** | 確認 body 加「呢次只係小休，減壓有限，唔似得瞓足一日咁將壓力清零。」；日結板標題「休息（週X）」→「小休（週X）」。減壓數值不變 |
| S-41 報紙時序易誤會 | **已修（方案 a）** | TEXTFIX 加 `"電視城臨記班底添新血": "入行消息：電視台臨記班底添新血"`，改寫 `np_story_c1_tv_01` kicker，加來源語境；唔改出報機制 |
| S-47 作品牆承諾過頭 | **已修（文案方案）** | 空牆＋note 改做真規則：「有作品圖嘅製作，殺青之後先上牆；冇海報嘅製作（例如電視特輯），完成咗只會記入拍攝簿，唔會上牆。」補圖方案唔做 |

### S-42 關鍵發現（必讀）
Live 教學**唔行 inline `TUTORIAL_ZH_HK` const**：開機 fetch `content/tutorial_zh_HK.json` 成個換走佢，再經 `textfix55SimplePack` 用 `TEXTFIX55_EXACT` 清洗。第一次實駕教學重播見舊句，證實淨改 inline 係死路。修復：覆寫表加／改 37 對（34 新＋4 更新），pack 異文（包括 stale「再打開選單「事態」」→改做進度掣句，順帶對齊 HUB77）全部對應新句；37 個 key 驗證過最多只出現喺一個 content 檔，無跨 pack 碰撞。`content/*.json` 本身無郁。**以後改教學文案必須經 `TEXTFIX55_EXACT`（或改 pack），淨改 inline 係死路。**

### S-47 偏離任務建議嘅理據
任務建議寫「電影／有名有姓劇集先有作品圖」，但數據核查推翻咗：海報覆蓋 69 個 gig，橫跨全部 5 類（廣告 15、綜藝 7、電視劇 9、電影 20、唱片通告 18）；唯一無海報嘅電視特輯 gig 得一個（`gig_1988_entry_winter_cny_crowd`《賀歲特輯》）。用類別承諾會講大話，所以文案寫真規則並點名電視特輯。

### 前後對照（節錄；完整清單見 `~/workspace/linji-work108b/notes.md`）
- TUT_MAP：「地圖上的地點，就是你可以去的地方；先點地點才看到行動。」→「地圖上面嘅地點，就係你可以去嘅地方；要先撳入地點，先睇到有咩行動。」
- TUT_BOARD：「通告欄可先免費查看；條件未合顯示暫未能報，達標後可接通告（耗一日）。」→「通告欄可以免費睇住先；條件未合嗰啲會顯示「暫未能報」，達標之後先接得通告（接通告要用一日）。」
- TUT_TRAIN alt：「訓練累計夠，社交與觀察課就會開放。」→「訓練儲夠數，魅力課同觀察課就會開放。」（順帶修正 stale 術語 社交課→魅力課）
- TUT_SHOOT：「獲聘後，拍攝日已排進行程。／開工前看手帳和行程，跟進度。」→「獲聘之後，拍攝日已經排咗進行程。／開工之前，記得睇手帳同行程，跟住上面嘅安排去做。」
- TUT_DONE：「教學先到這裡（可跳過；選單可重看）。」→「教學先到呢度（可以跳過；之後喺選單重看）。」——「再撳地圖上嘅「進度」掣」一句刻意保留原字（`test_hub77_static.py` 釘死）。
- S-49：「逛完・過一日」／「提早休息（過一日）」／「確認提早休息？」／「確定休息 +1日」→「過一日」／「過一日」／「確認過一日？」／「確定過一日」。
- S-15：「今日會完結並進入下一日（等同休息）。」→「今日會完結並進入下一日。呢次只係小休，減壓有限，唔似得瞓足一日咁將壓力清零。」；日結標題「休息（週一）」→「小休（週一）」。
- S-41 kicker：「電視城臨記班底添新血」→「入行消息：電視台臨記班底添新血」。
- S-47 空牆：見上表。
- 附註：真獲聘 modal 標題係「獲聘！」，唔係「何生來電」（後者只係落選／資料對唔返分支）。

## 3. 視覺統一包（分批④・B 級）
分支 `v108-visual`。對 v106 逐項重新核實：D-1／D-4 已修（v106，唔修）；其餘按下表修。
| 項 | 處置 |
|---|---|
| D-5 對話框統一 | **已修**：`.e79-box` 改米紙框＋名／行改深色；「巧遇 · 名」頂標籤保留作區別 |
| S-1 主頁規則字壓相底 | **已修**：半透明紙底＋深色字 |
| S-2 兩個停用掣並列 | **已修**：冇存檔隱藏兩粒大掣，只留一粒細「讀檔」入口 |
| S-4 導入 dim 成個殼 | **已修**：dim 用漸變，殼底（量度所得 110px）以上透明，只 dim 內容／地圖區 |
| S-5 開局導入圖舊資產 | **已修**：新事務所場景圖＋阿偉／何生新全身企立合成場景（`b01GuideHtml108()`；舊圖只做退路） |
| S-7 地圖標籤擠迫 | **已修**：逐個微調座標＋地區名光暈加厚，唔重畫地圖（鑽石山 38%/6.5%、九龍城 58%/31.5%、紅磡 52%/38%、金禧 11%/44.5%、薄扶林 41%/65%、維港電影 80%/+38px、廟街禮品 44%/−44px） |
| S-8 進度入口重複 | **已修**：頂欄 `chip-story` button→span 純徽章，刪 click 接線；地圖 pill 留唯一入口 |
| S-9 劇情高亮似 debug 框 | **已修**：改圓形柔光＋呼吸脈動（`storyGlow108`），唔用直角線框。靜態截圖唔係成日睇到（呼吸暗相位偏淡），computed style 證實運行中，效果偏含蓄 |
| S-11 HUD 壓力唔易讀 | **已修**：數字加粗；danger 門檻 90→70（`paintBar` HUD＋`stChip` 兩處齊改 70）＋脈動；「爆表」文案 90 保留 |
| S-18 ⧉ 複製掣無標籤 | **已修**：加可見「複製」字（保留 ⧉＋title；唔改做「套用全週」——`openCopyFromDay` 係揀目標日） |
| S-20 編輯頁 CTA 三層疊 | **已修**：「返回地圖」改細掣置中，主 CTA 只留確定 |
| S-27 卡片酬雙數字 | **已修**：卡面只留牌面一個數（新 card 變體 `gigPayExactText(g,{card:true})`），詳情保留區間 |
| S-29 第一日大半唔接得 | **已修**：可接置頂＋未達標預設摺疊（`<details class="gig-locked108">`，唔改門檻／排序邏輯以外） |
| S-33 詳情欠簽約金／違約金行 | **已修**：摘要區加「簽約金 $X（接通告後即收）」行；違約金只喺有數嗰陣先出（實測 $120；`gigBreachFee` 唔郁） |
| S-34 離開掣搶眼 | **已修**：鮮橙實色大掣改淺色文字掣 |
| S-36 等試鏡消息入口深 | **已修**：地圖底部卡加「等緊 N 張試鏡回音」行（有先顯示） |
- 全部改動喺 `index.html`（34 處替換＋3 處第二輪修正，全部 count=1 斷言）＋新守門 `tests/test_ui108_static.py`（64 檢查；pristine 反證 FAIL 51 項）。
- 6× 404 係 v106 已有缺口（`chung_choning_think`、`ho_sang_sad` 表情檔未入庫），唔係本包引入；見 §7 問題 #1（鍾楚凝 think／smile 缺檔已確認為實質問題）。

### 任務 B（唔入分支，等用戶拍板）
- **S-30 通告詳情實物化**：demo 頁＋改前／改後截圖＋可套用 patch，喺工作副本 `~/workspace/linji-work108c/qa108c/s30/`（`demo_s30.html`、`before_s30.png`、`after_patch_detail.png`、`s30_physicalisation.patch`、`make_patch.py`、`drive_s30.py`）。驗證：`git apply --check` 通過、`node --check` 通過、實駕零 pageerror。**未套用，等拍板。**
- **圖標組 S-17／S-22／S-38／S-46**：樣本喺 `~/workspace/linji-icon-sample/`（README.md、12 隻透明底 PNG、`demo_schedule_editor.html`＋截圖）。全量估算約 24–28 隻（樣本 12＋尚欠約 12–16）；**未做全量替換，等拍板。**

## 4. 對話呈現微調（用戶 2026-11-12 04:03／04:18 實機反饋）
分支 `v108-dlg`。用戶喺電話實玩 v106 巧遇鍾楚凝段，兩張截圖（`C6B974BA…`／`EEB886FA…`，旁白句）。

### 第 1 項——地面錨線被取代，改行對話框遮腿（04:18 追加）
地面錨線方案**唔做**（舊分析嗰套錨線 code 已全數移除，repo 內零殘留）。改法：人物高 **60%** 舞台高、腳底 `bottom:10%` 伸到對話框後面，框不透明，框頂去到人物膝頭至小腿中段（主線牌頂＝人物高 78.9%、巧遇盒頂＝81.8%）。腳唔再係畫面錨點，腳浮問題自然解決。
- **96 張重測**（v106 88＋v107 8，PIL 實量）：阿偉×何生 60% 淨空 **20.2px**、阿偉×鍾楚凝 **33.7px**（size-test 舊批 17／30px，新批鬆 3.2px，60% 仍然啱）；最闊現實配對方小龍＋Vera 合計 0.795，60% 重疊 ~24px，上限 **54.6%**；561 個 base 配對有 **55 個** 60% 下淨空 ＜12px——自動收細係通用規則。v107 8 張新圖全部窄身表情裁切，數字同 88 張時完全一樣。
- **per-pair 自動收細**：`dlg108FitPct` 用載入圖 `naturalWidth/naturalHeight` 實測闊高比（唔用 base 表——葉曼芝表情闊高比差 0.10），淨空 ＜12px 降高到啱為止。測試頁用遊戲本體真模組跑最闊配對：方小龍＋Vera → **55.4%、淨空 12.2px**、零交疊。
- 實駕（390×844）：主線人物高 487.2、腳底 740.8；巧遇高 506.4、腳底 759.6；淨空主線 13.8–17.4px、巧遇 30.1px；`elementFromPoint` 遮腿探測全部命中牌／盒本身、永不命中 IMG。**場景錨線表：無**（被取代方案唔做）。
- 觀察：C1 雙人淨空實測 13.8–17.4px，細過靜態測試期望 19–21.5px——靜態計數用 844px 高計，實機舞台高 812px（頂欄佔 32px），無重疊無穿幫，純數字出入。

### 第 2 項——旁白 brightness：唔係 bug，係相片曝光
實駕量度（getComputedStyle）：旁白句主線 C1[18]＋巧遇 ENC[0][1][7][11] 兩人全部正正 `brightness(0.6)`；講者 1.0／聽者 0.6、電話聲 0.8／0.8 全部啱數。像素光度比釘死：同一幾何、鍾楚凝裙（旁白 vs 講者）平均光度 25.9 vs 43.2，比值 **0.600**；對照組阿偉褸（兩步都係 0.6）比值 1.000。**零程式改動。**

### 第 3 項——對話框定高＋「下一句」文字鏈，全部做到
主線牌定高 **118px**（連旁白板），全 C1 步驟恆定 118、牌頂 638。巧遇盒：對白行固定 4.65em（3 行，lineH 74.4 恆定）＋名牌行 `line-height:1.5;min-height:1.5em`（空名同有名同高 22.8px——初版只設 `min-height:1.2em` 時盒高仍差 4.8px，已修）；全部非選項步驟盒高恆定 **181.2**、盒頂 662.8（選項步驟盒向上擴至 285.2 屬正常）。「下一句」主線／巧遇都係 88×44 透明底金字底線掣（44px 撳掣高保留）；選項掣還原舊全寬深色掣，主線選項 `:has()` 排除唔會誤變文字鏈。

## 5. 合併紀錄（統籌親手做）
- 順序：`v108-dlg`（乾淨）→ `v108-text`（乾淨）→ `v108-visual`（2 處 `index.html` 衝突）→ `v108-d8`（測試檔名 add/add 衝突）。
- 衝突解法：
  1. CSS 區塊：DLG108＋UI108 兩段獨立新增，兩段都保留。
  2. e79 注入 CSS：DLG108 幾何（`position:absolute` 疊人物、z-index:5、固定行高）＋ D-5 米紙配色（淺色漸變＋深色字＋名牌行深金）合併；電話名用 D-5 藍 `#2f6fed`（米紙底適用）。
  3. 合併跟進修復：DLG108 金字「下一句」掣（`#ffd968`）喺米紙盒上幾乎睇唔到，改深金 `#8a5a00`（同名牌色一致）；合併後實駕量度對比度 **5.22:1**，截圖目視清晰。
  4. d8 測試檔同 dlg 撞名（兩邊都叫 `test_dlg108_*`）：d8 版改名 `test_wf4dlg108_logic.js`／`test_wf4dlg108_static.py`（runner glob 自動入套件）；d8 靜態斷言人物高 50%→60% 跟 DLG108 新規格（舊斷言合併版實證 FAIL、新斷言 v106 基線實證 FAIL）。
  5. `test_dlg108_static.py` 三項斷言跟合併規格：巧遇盒由深色改米紙漸變、名牌色 `#ffd968`→`#8a5a00`、「下一句」金字→深金字（舊斷言合併版實證 FAIL、新斷言 dlg 分支實證 FAIL）。
- 中途插曲：`/tmp` tmpfs 512M 爆滿（兩份舊 scratch），已清走；pristine 基線改用 `~/workspace/linji-pristine108` 工作樹（`d5c41e8`）。

## 6. 測試
- 新守門：`tests/test_dlg108_logic.js`（21 項）＋`tests/test_dlg108_static.py`（41 項）／`tests/test_text108_static.py`／`tests/test_ui108_static.py`（64 檢查）／`tests/test_wf4dlg108_logic.js`／`tests/test_wf4dlg108_static.py`——全部 PASS（pristine 反證齊全）。
- 全套 A/B（`qa108d/run_suite.py`）：基線 pristine main `d5c41e8` ＝ **136 PASS／12 FAIL**；合併版 ＝ **142 PASS／12 FAIL**，FAIL 清單逐字相同（12 個已知環境性 static FAIL：flash51／giglib36／pacing35／poster59／rumor49／slot50／soft_tip_111_restore／start53／weave43／weave44／weave49／wrap38）。**零回歸**；+6＝六隻新測試檔。
- `node --check` 主 script 通過。舊斷言更新（附反證）：`test_guidance34_*`、`test_week105_static.py`、`test_qa101_static.py`、`test_menu72_static.py`、`test_text55_logic.js`（文字包）、`test_dlg106_static.py`／`test_map54_static.py`（dlg 包）、`test_hub77_static.py`／`test_loc96_static.py`／`test_ux68_static.py`（視覺包）。

## 7. 合併後實駕驗收（`~/workspace/linji-work108v/`，唯讀驗證，槽 3）
對象 main `57251bf`，本地鏡像逐檔 sha 核對，390×844，**6 項全部 PASS，0 pageerror**：
1. **合併組合**：巧遇鍾楚凝＠金鐘創意（day 425）＋主線 C1——盒米紙色（同主線牌一致）；人物 506.4px＝舞台 60%，淨空 30.1px；盒頂 662.8 蓋住腳底 759.6 以下（膝頭以下 96.8px）；「下一句」深金 `#8a5a00` 文字鏈、88×44px、對比度 5.22:1；**盒高 181.2px 恆定**（9 步全數，包括 1 行句「嗯。」、2 行長句、3 行旁白；獨立重播再驗同為 181.2）；C1 牌定高 118px（17 步全數）、人物 487.2px、「下一句」金色 `#ffd968` 正常。
2. **D-8**：st03 真路徑（旁白 base 0.6 → 阿偉 `awi_think.webp` 全光，抉擇→結算通）；set01 舊路徑零 `dlg106-char`。
3. **文字**：S-26 醫院首次長版／第二次短版；S-49 三處一律「過一日」（掣「確定過一日」）；S-15 body 講明「小休，減壓有限」；S-42 教學重播見新句、舊句零出現。
4. **視覺**：S-5 B01 新事務所場景＋雙全身齊載入；S-7 七標籤零重疊；S-27 板 9 張卡每張只一個酬勞數；S-29 可接 2 張置頂＋未達標 7 張預設摺疊；S-33 詳情摘要「簽約金 約 $270（接通告後即收）」；S-36 報《年宵花市》試鏡後翌日地圖底部卡「等緊 1 張試鏡回音」。
5. **舊檔相容**：v106（`8d19640`）槽 3（money 106108／dayIndex 3／mark `v106-slot3`）喺合併版完整還原，兩輪重複驗證。
6. **錯誤**：全程 0 pageerror。
- 截圖：`~/workspace/linji-work108v/shots/`（`b1_c1_cover.png`、`b2_enc_cover.png`、`c_st03_03.png` 等）；驅動＋log 同目錄。另各工人實駕證據：`qa108a/`（D-8，已入 main）、`qa108d/`（dlg，已入 main）；文字／視覺工人實駕喺工作副本 `~/workspace/linji-work108b/qa108b/`、`~/workspace/linji-work108c/qa108c/`。

### 發現問題（未修，交統籌／用戶決定）
- **#1 鍾楚凝 think／smile 表情圖缺檔，巧遇段每次播都 404（實質問題，輕微）**：`chung_choning_think.webp`／`smile.webp`（連 `.png` 後備）全部 404——鍾楚凝全庫只得 base／sad／serious，但 ENC84 對白有 think／smile 需求。畫面唔爛（退回 base 圖，截圖正常），但每次播呢段出 6–8 個 console 404，嗰幾句永遠顯示唔到 intended 表情。修法：補兩張表情圖，或將呢段對白嘅 think／smile 需求改做已有表情。**建議下個表情細包一併補。**
- **#2 WF4 DLG106 舞台仍然好細（D-8 已申報缺口，合併後未修）**：合併版實測舞台仍係 342×168px、人物 34×100px——數據層表情切換正確，但肉眼幾乎睇唔到。dlg 分支未掂 WF4 舞台幾何。**要修就要另開一票改 WF4 modal 舞台幾何（放大／全屏化），唔係今包範圍。**
- 觀察（唔係 FAIL）：day 0 事務所 sheet 根本無「只查看通告欄」act（當季零 gig 就唔出掣，by design），板驗收要經中環廣告／海港廣播／星河電視台入。

## 8. 需用戶拍板（附對照，唔好喺冇對照下直接上線）
- **S-30 通告詳情實物化**：demo 頁＋改前／改後截圖＋可套用 patch，喺 `~/workspace/linji-work108c/qa108c/s30/`（`demo_s30.html`、`before_s30.png`、`after_patch_detail.png`、`s30_physicalisation.patch`）。**未套用，等拍板。**
- **圖標組 S-17／S-22／S-38／S-46**：12 隻細線條手繪風小圖標樣本＋行程編輯頁 demo 對照，喺 `~/workspace/linji-icon-sample/`。全量估算約 24–28 隻。**未做全量替換，等拍板。**

## 9. 未達標／留待跟進（老實申報）
- **AUD91 公佈路徑問題（遊戲機制，唔係 v108 範圍，唔修）**：試鏡賀歲特輯後 `S.pendingAud` 有到期記錄（ok=true，revealDay 已到），經「提早休息日結板 → 返回地圖」等咗 4 日（1 月 3→7 日）從未公佈（300ms×10 密 poll 空 mask、空 toast；截圖證實已返地圖）；同一日改行「☰選單 → 手帳 → 事業頁 → 返回地圖」，獲聘 modal 即刻彈出。Code 層面 `goToMapForBrowse` 晨早鏈（報紙→`aud91PresentDue`→WF4）次序正確、`aud91PresentDue` 會 `return true`、`ending78Locked()` 第一週 false——點解日結板路徑唔觸發，靜態睇唔出，**需要另開調查**。
- 鍾楚凝 think／smile 缺檔（§7 #1）；WF4 舞台太細（§7 #2）；舊 bust 路徑（非 fullbody 講者，72%/bottom 0）冇掂——v106 既有行為，DLG106 步同舊路徑步之間人物高度會有差。
- 「1988 年春」stale 年份（`story_beats_phase1.json` Ch1、`tutorial_zh_HK.json` TUT_WELCOME）：runtime `years66Walk` 已修正顯示，pack 未改。
- 全部玩家面劇情台詞、結局相關句：按規則留低。S-24 按裁決唔郁；落選 modal 成功率行按 v105 範圍留低。
- S-9 柔光喺靜態截圖唔係成日睇到（呼吸暗相位偏淡），computed style 證實運行中，效果偏含蓄。

## 10. 改動檔案
- `index.html`（四包＋合併解衝突）
- 新測試：`tests/test_dlg108_logic.js`、`tests/test_dlg108_static.py`、`tests/test_text108_static.py`、`tests/test_ui108_static.py`、`tests/test_wf4dlg108_logic.js`、`tests/test_wf4dlg108_static.py`
- 更新測試：`test_guidance34_*`、`test_week105_static.py`、`test_qa101_static.py`、`test_menu72_static.py`、`test_text55_logic.js`、`test_dlg106_static.py`、`test_map54_static.py`、`test_hub77_static.py`、`test_loc96_static.py`、`test_ux68_static.py`
- QA 證據（已入 main）：`qa108a/`（D-8）、`qa108d/`（dlg）；工作副本：`~/workspace/linji-work108b/qa108b/`（文字）、`~/workspace/linji-work108c/qa108c/`（視覺＋S-30 demo）、`~/workspace/linji-work108v/`（合併後驗收）
- `NOTES_V20A108.md`（本檔，統籌總交代，覆蓋文字工人原版）、`NOTES_V20A108_D8.md`（D-8 工人原檔）
