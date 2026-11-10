# NOTES V20A80 — 劇情豐富化 WF1：後段加厚＋真空帶補幕

基底 v20a79（4,798,020 bytes）。本包只做內容加厚同補幕，冇改 SAVE key／softRev／`?v=`、冇改 content pack JSON、冇改任何節點 ID／觸發閘規則／既有抉擇數值後果方向／感情 commit 旗。

## 一、後段加厚（C6–C17，覆寫表原位加厚）

做法：只插入新拍＋加長 resultBeats＋6 幕各加一個第三抉擇；既有 beats／choices／effects 逐字保留（以 v79 fixture 子序列＋前綴驗證，見新測試）。字數口徑：beats／resultBeats 內 lines 字元總數。

| 幕 | beats 拍數 | beats 字數 | resultBeats 字數 | choices |
|---|---|---|---|---|
| C6 飯堂閒角 | 5 → 9 | 218 → 480 | 98 → 223 | 2 |
| C7 暴雨救場 | 5 → 9 | 217 → 461 | 82 → 285 | 2 → 3（+C7_c 同心協力，旗 flag_rain_split） |
| C11 選美後台 | 5 → 8 | 211 → 428 | 71 → 276 | 2 → 3（+C11_c，旗 flag_miss_deflect） |
| C8 茶餐廳度橋 | 5 → 9 | 181 → 450 | 72 → 226 | 2 |
| C9 年尾追數 | 5 → 9 | 202 → 519 | 71 → 363 | 2 → 3（+C9_c，旗 flag_mediate_gu_debt） |
| C10 戲路定型 | 5 → 9 | 224 → 506 | 72 → 233 | 2 |
| C15 高危替身 | 5 → 9 | 214 → 505 | 97 → 270 | 2 |
| C14 站隊 | 5 → 8 | 278 → 516 | 91 → 342 | 2 → 3（+C14_c，旗 flag_side_undecided） |
| C12 樂壇前哨 | 5 → 9 | 253 → 562 | 83 → 369 | 2 → 3（+C12_c，旗 flag_fans_mediate） |
| C16 偶像實力之爭 | 5 → 9 | 290 → 691 | 90 → 258 | 2 |
| C13 賀歲片 | 5 → 9 | 272 → 627 | 96 → 403 | 2 → 3（+C13_c，旗 flag_newyear_twotakes） |
| C17 三年收科 | 5 → 10 | 281 → 717 | —（見下） | 2（逐字不變） |

12 幕合計：beats 2,841 → 6,462 字；resultBeats 923 → 3,248 字。

- 補嘅主要係：後果拍（揀完嘅下文／漣漪）、人物反應拍、年代質地（通宵飛紙仔、歌迷會拉票、盆菜團年、修音 vs 苦練等，照年代映射庫）。
- C17 特別處理：只加 beats（紅地氈／何生交代／舊場務重遇／回望收束），**choices 整段逐字冇掂**——其 choices 播放時由 `ending410EveNode` 動態重建（帶 ending410Key），唔准靜態改。新拍冇寫死邊個攞獎、冇劇透結局判定。
- 新第三抉擇一律：新旗（已入該幕 flags_written）、stats 幅度唔勁過同幕既有抉擇、resultBeats ≥60 字。全部屬可選分支，唔改主線走向。

## 二、真空帶補 2 幕（新表 STORY_SPINE_NODES_WF1）

1990 冬 → 1991 春約半年主線零節點，補兩幕。新表＋注入函數 `applyStoryWf1Nodes80()`（冪等 push 入 STORY_WIRE.main.nodes），call 位喺 `applyStorySpineOverrides410()` 之後、`textfix55StoryPack(main)` 之前；新表已加入 YEARS66 靜態 walk list（walker 冪等）。節點內文年份跟全書慣例寫舊標籤，YEARS66 載入 +2 顯示。

| 幕 | 標題 | 時窗（真曆） | 地點 | 題材 | 規模 |
|---|---|---|---|---|---|
| C18 | 上岸路 | 1990 年冬（gate：yearMin 1990＋冬；when 舊標籤「1988冬」） | 何生事務所 agency_ho | M14 自組公司風向＋何生問事業想像，輕咬屋企線 | 10 拍 561 字＋後果 183 字 |
| C19 | 賭枱邊 | 1991 年春（gate：yearMin 1991＋春；when 舊標籤「1989春」） | 獅子山製片 film_lion | M17 賭片跟風潮，臨記視角 | 10 拍 579 字＋後果 163 字 |

- 兩幕 gate 都**冇 needDone**：插入幕唔卡主線，玩家漏咗唔會塞住後段。
- 進度頁：`prog71Rows()` 改用次序清單，C18／C19 排喺 C6 之後、C7 之前（時序位），標籤照衍生出「第 18 幕」「第 19 幕」；四態（未開放／已開放／已完成／已錯過）行返既有衍生。CALIB60_NODE_WINDOWS／TITLES 已登記兩幕（時窗提示同 missed 登記）。
- 旗：C18 `flag_wf1_studio_dream`（rel_ho+1／credit+1）、`flag_wf1_steady_craft`（credit+2）；C19 `flag_wf1_gamble_quiet`（credit+2）、`flag_wf1_gamble_observe`（credit+1／fame+1）。幅度同主線抉擇同級。

## 三、自作判斷（計劃冇寫死，照既有慣例處理）

1. **C18 何生 speakerId 剝除**：原稿何生拍帶 `speakerId:"agent"`，但主線 C1–C17 何生一律冇 speakerId；整合時剝走，跟返慣例零風險。
2. **「彭兆基」正名唔喺本包處理**：底本 C10 等處用舊名「彭兆基」（全檔 33 處），LIVE 正名係「彭少祺」；屬另一正名工程，WF1 只跟底本保留原文，建議另案處理。
3. **進度頁編號**：新幕照 C 編號出「第 18 幕／第 19 幕」，唔另造顯示編號；排序按故事時序插入，唔重排既有幕。
4. **C17 resultBeats 門檻豁免**：因其 choices 動態重建，靜態冇 resultBeats；測試已註明豁免理由。
5. **進度頁逐項名額修正**：`renderProgressPane71` 原本「最近兩幕未開放列足逐項」嘅名額會俾插入幕食咗（B2 場景 C7 逐項消失，俾既有測試捉到）——改為名額只數主線幕（`detailSet71`），C18／C19 排入主線逐項範圍內先跟住出逐項，遠幕防劇透維持。屬行為修正，progress71 測試零改動 PASS 返；另 calib60 漏失預期同 ux68 主檔上限兩處既有斷言已原位改版並註明原因。

## 四、測試

- 新增 `tests/test_wf1_80_logic.js`（160 項：加厚完整性／後果拍／fixture 零回歸／新抉擇幅度／補幕可達性規則／注入冪等／紅線）＋ `tests/test_wf1_80_static.py`（框架在位／call 位順序／基線不變）＋ fixture `tests/fixtures/spine_c6_c17_v79.json`。
- 反證：兩新測試喺 v20a79 index 上行 → FAIL（冇 WF1 表抽取即 throw／標記缺失）。
- 全套 tests：90/90 檔案 PASS（基線 88＋新 2）。
- 真 UI 實駕（槽 3、本地鏡像）：見 verify80/。

## 五、已知唔喺本包

- 彭兆基正名（見上）；WF2–WF5 按豐富化計劃次序續行；巧遇 Phase 2/3 排 WF3。
