# v138 死檔判決補充（2026-11-12，分類覆核）

判死標準：用 `qa138/classify138.js` 抽 index.html 真 `dlg106ResolveCategory`
（同 runtime 同一個分類器）分類 **live 文本**（index.html 運行版節點＋mock），
唔係 pack 舊文本。Live 嗰陣冇一句分類到嗰個表情 → 圖永遠播唔到 → 死檔。
（跟 v127 教訓：唔好為死線補圖；修死檔本身係另一票——內容／引擎改動。）

## 判死 1：lin_hiu_serious.webp（連曉 serious）

- 唯一證據句（pack `content/story_detail_romance_vera_hiu_choi.json` R_hiu_meet）：
  「不過你要記住，有些助導比較挑剔，你要先打聽清楚他們的喜好，免得白走一趟。」
  → 分類器：**serious**（pack 文本本身係啱嘅）。
- 但實玩播唔到，兩個原因疊加：
  1. `StoryPlay.start(R_hiu_meet, {force:true})` → **False**（probe 證實）。
     `StoryPlay.start` 入面 DualMeet 段（`IDS=["R_hiu_meet","R_choi_meet"]`）
     行喺 force check 之前；mock `MOCK_STORY_DUAL_MEET_THICKEN_SOFT_v1.json`
     已載入，`openGates.R_hiu_meet.needDone=["C3"]`，新遊戲 C3 未做 → 閘 fail，
     force:true 都擋唔住。
  2. 就算滿足 C3 過閘，`meetNode()` 會將節點換成 **mock 加厚版**（6 beats，
     全部 DeepSeek 書面語，講通告紙／何生介紹臨記）——入面**完全冇 serious 句**。
     Mock 3 句林曉晴對白分類：neutral／neutral／sad。
- 結論：**pack 嗰句永遠播唔到；mock 版冇 serious 句。lin_hiu_serious.webp 死檔。**
- 修復方向（另一票）：mock R_hiu_meet 加一句 serious 台詞，或將 pack 版重新曝光。

## 判死 2：tsui_poushan_serious.webp（徐寶珊 serious）

- 兩條證據句都係 **pack 舊文本**（書面語），分類器話 serious：
  1. 「挺機靈。做臨時演員也要有記性，記住誰是客人、誰是老闆，你才有機會站前一點。」
  2. 「我不需要你記住我幫過你，我想知道你當我是什麼人。合作夥伴？還是其他？」
- 但運行版節點係 index.html 入面嘅重寫版（廣東話），pack 被主幹覆寫：
  - `R_xu_meet`（L23100）：「幾機靈喎。做臨記都要有記性，記得住邊個係客、
    邊個係老闆，識睇人眉頭眼額，你先有機會企前啲。」→ 分類 **neutral → base**
    （probe 實駕證實：播到呢句嗰陣渲染 `tsui_poushan_base.webp`）。
  - `R_xu_ending`（live 4 句）：angry／happy(smile)／neutral／neutral。
  - 全量核實：index.html 全部 **17 句 live 徐寶珊句**分類 =
    neutral 12／angry 1／think 1／shy 1／surprise 1／happy 1，**serious 0**。
- 結論：**冇任何一句 live 徐寶珊句分類 serious。tsui_poushan_serious.webp 死檔。**
- 修復方向（另一票）：live R_xu_* 節點加一句 serious 台詞（或重寫現有句令分類器畀 serious）。
- 附帶發現（下一批候選，唔入 v138）：live 徐寶珊句有 1 句 angry（ending「今晚係慈善晚宴…」）、
  1 句 think、1 句 surprise、1 句 happy——庫入面冇 `tsui_poushan_angry/think/surprise/smile`
  檔（得 base／serious／shy），呢啲句現時跌返 base。

## 生檔覆核（同批分類器，全部 live 正確）

| 句 | 分類 | 結果 |
|---|---|---|
| fen_serious_1「你唔同，你肯做啲冇人想做嘅嘢…」 | serious | 生 |
| fen_sad「驕傲少少唔怕，最怕你哋呢班後生…」 | sad | 生 |
| ho surprise「呢排成日有人嚟問我攞主意：走，定唔走…」 | surprise | 生 |
| chung angry「有天份冇用功，一樣企唔穩…」 | angry | 生 |
| lok smile「唔使你唱到幾勁，嗰段得幾句…」 | happy→smile | 生 |

## Fix-up 根源（2026-11-12 實查，續補）

### chung_choning_angry —— 生檔，唔係死檔（softPreview-only 壓制）

- 失敗鏈（已逐層證實）：
  1. e_chung_heart days 365–376 trace：chung 喺 368、370–373 喺 rec_star 出沒盤，
     撳「天星」成功，但 overlay 永遠 False（`triggered` 恒 0）。
  2. 排除：farewell 離港閘（beatsDone 已排除 chung_farewell，佢照樣喺盤度）；
     PILOT（`ENC84_DLG_chung_choning` 存在，L50681，註冊 L52495）；
     冷卻（lastDay=-99）；每日上限（triggered=0）；T3 opener 封頂（只限 1991 年**前**，
     L51685，1991 年起回復原狀）。
  3. 對照實驗：同一 setup、同一日 368、同一地點 rec_star，seed 陸柏言一樣唔觸發；
     但 day 0 rec_star seed 陸柏言即刻觸發（overlay 陸柏言，triggered=1）。
     → 唔係星嘅問題，係 **日子／地點**嘅問題。
  4. 決定性證據：用 expose 咗嘅 `StoryOC.listOpen`＋`storyNodeLocId` 實測 day 368——
     open 節點 C1（loc `agency_ho`）＋**C9（loc `rec_star`）**。
     `enc79StoryPendingAt("rec_star")` 因此回 true → 攔截被壓住（「主線待播優先」）。
  5. 點解 C9 係 rec_star：`storyNodeLocId` 先問 soft behavior gate（mock），
     mock 將 C9 嘅 loc 寫做 rec_star；硬表 `STORY_LOC_SOFT[C9]` 係 tvb_harbour。
- **關鍵：soft gate 係 opt-in**（`?softPreview=1`／`?softBehaviorGate=1`／localStorage，
  預設 false）。**Live 遊戲（唔開 softPreview）C9 嘅 loc 係 tvb_harbour，
  rec_star 唔受壓，chung_angry 播得到。**所以呢張唔係死檔，係 drive 環境（softPreview）
  下嘅閘口問題。
- 修法（已入 drive）：e_chung_heart seed 加 `story_done=["C9"]`（模擬已做完 C9 嘅
  中期玩家——C9 係關鍵路徑恢復節點，1991 冬行到 T3 嗰陣正常玩家已經做咗），
  `enc79StoryPendingAt` 讀到 done 即放行。**證實有效：fix-up 嗰陣 day 368 overlay
  即刻觸發。**
- **第二重修正（section 標籤又錯）**：C9 閘清除後，播出嚟嘅係 heart 線
  （「阿偉，坐陣啦，我啲安排搞到七七八八…」移民主題），唔係 angry。
  實查 `ENC84_DLG_chung_choning`：angry 句「有天份冇用功，一樣企唔穩。」喺
  **`pool.T3[0]`**，唔係 T3 opener（resolver 嘅 section 標籤再次錯）。
  修法：seed 加 `heartDone=True`（無 beat＋無 heart → pool T3[0] 首段）。
  **證實有效：fix-up 3 前嗰輪已見 `chung_choning_angry.webp`（34/35）。**

### s_fen_intro —— 撳針間歇性靜默失效（非遊戲內容問題）

- 現象：新遊戲後第一次撳地圖針（DOM .click()／Playwright 撳掣都試過）間歇性乜都唔發生——
  sheet 唔開、`S.visited` 唔加、冇 toast、冇 pageerror；第二次撳即開。
  （probe12：#1 失敗 → #2 即開；probe10：事務所 #1 開 → 海港 #2 開。）
  排除：forced day（plan 係 `scout_all`）、出行額度（used=0）、story 進行中、
  閘全部 loc-independent 但事務所開得到。疑似首次 openLoc 嗰陣有異步初始化未完，
  render 靜默吞咗（try/catch），第二次先齊料——機制未完全證實。
- 修法（已入 drive）：`open_loc_retry()`——撳針後驗 sheet 開咗未（標題 ≠「地點」），
  未開就重撳，最多 3 次；開咗唔再撳（唔浪費出行額度）。ENC phases 唔使改
  （逐日試本身已經係重試；chung 嗰 12 日全部失敗係 C9 閘，唔係撳針問題）。
- **跟進發現（probe_fen，2026-11-12 15:40 左右）**：海港針中心俾嘢遮住，
  Playwright click 做 hit-test 會 timeout（pin 可見 52×52 但 `click_first` 回 None），
  所以 `open_loc_retry` 改用 DOM `.click()`（繞過 hit-testing；probe10/12 證實開到）。
  地圖區列表掣（`#map-area-list button[data-loc]`）係死路——onclick 係空、
  DOM click 完全無反應（probe_fen2 證實），只有 pin 先係 live。
- **跟進發現（fix-up 2 輪）**：sheet 開咗但 action 掣「芬姐喺茶水帳揚手叫你」
  撳唔到——Playwright click 喺滑入中嘅 sheet 上 actionability timeout。
  修法：`play_offer` 改用 DOM `.click()` 撳 action 掣＋搵唔到嗰陣 dump sheet 標題
  同 acts（診斷用）。**證實有效：fix-up 3（15:48）`extra_ad_fen_sad.webp` 見到，
  35/35 生檔齊晒，OVERALL PASS。**截圖證實芬姐 sad 表情＋「驕傲少少唔怕…」嗰句
  （typewriter 進行中）。

## 覆蓋率重計（判死後）

- 批單 37 張 → **生 35 張**（2 張死檔除外）。
- Verdict 嘅 +66 句增益拆解：54 句真 live 實線＋3 句死檔線（lin serious 1＋tsui serious 2）
  ＋9 句 phantom（extra_ad_fen sad 同一句旁白重複誤歸，見 verdict138_final.txt）。
- **真實覆蓋率：515＋54＝569／593＝95.9%**（原目標 581／593＝98.0% 係 inventory 口徑，
  包咗 phantom＋死檔線）。
- 覆蓋唔到嘅 24 條 inventory 條目：9 phantom（盤點 bug，旁白誤歸）＋3 死檔線（內容／引擎缺口，
  另開票）＋12 死組線（v138 verdict 嗰 7 組死檔，另開票）。
- 實駕目標：35／35 生檔全部實玩見到（30 張已見，餘 5 張 fix-up 補駕）。

## Fix-up 觸發路徑（2026-11-12 實查 index.html）

- **F4（ho_sang_surprise）**：`StoryPlay.start` 搵唔到（CHOICE47_NODES 唔喺
  `StoryOC.findNode` 嘅 STORY_WIRE 五包入面）。真 UI 路徑＝地點 sheet action 掣：
  `choice47ActionsAt("agency_ho")` → 掣「何生有句說話想同你講」，
  閘：`CHOICE47_DEFS.F4_stay_mind = {year:1992, season:"夏", loc:"agency_ho"}`，
  drive 設 dayIndex 920（1992-07-08）。`choice47Play` → `StoryPlay.start(node, {force:true})`。
- **WF4_fen_intro（fen_sad＋fen_serious_1）**：同理，`wf4FenActionsAt("tvb_harbour")` →
  掣「芬姐喺茶水帳揚手叫你」，閘：`S.exodusFenSeeded=true`＋`S.exodusFenFired=false`＋未做。
  drive 設 day 400（1991 年）＋seed 兩隻旗。`wf4FenPlay` → start(node object)。
- **WF4_fen_farewell（fen_serious_2／3）**：`wf4PresentFenFarewell()` 經
  `wf4PresentPending()`（返地圖流程 `goToMapForBrowse` L37528，晨報／試鏡公佈之後，
  farewell 優先於日常事件）。觸發條件：`S.exodusFenFired=true` → `wf4FenFarewellArm`
  建 arm＋`st.fenFarewellDone=false`。**關鍵：地點 sheet 嘅「返回地圖」只係 `closeSheet`，
  唔會行 `goToMapForBrowse`**——一定要經「過一日」日結流程返地圖先觸發。
  （呢個就係 probe_story farewell 試驗失敗嘅原因。）
- **e_chung_heart**：`ALL_BEATS_MINUS("chung_choning", "chung_farewell")`——
  `enc79PresenceP` 有 CLEAN100 B-05 離港閘，beatsDone.chung_farewell 成立即 p=0 永遠唔出沒。
- **e_lok_beats**：days 0–40（hash 模擬：lok 喺 0–11 日只出沒 0、8 兩日，第 3 次 visit 喺 day 13）。
