# NOTES_V20A234 — 語言重寫 RW-2 Phase 2：刪內嵌表，JSON 做唯一來源

Base：main `d90eaf9`（v233 已落地並經獨立核實）。分支：`v20a234`。
工作報告全文：`~/workspace/linji-language-sample/RW2B_WORKLOG.md`。

## 做咗乜

刪五個內嵌主線覆寫表＋覆寫機制，`content/story_detail_n1_to_n17.json`（19 個節點）做唯一來源：

- 刪表（base 行號）：`STORY_SPINE_NODES_N6`（L8677–8880）、`STORY_SPINE_NODES_1989`（L6603–7666）、`STORY_SPINE_NODES_1990`（L7667–8676）、`STORY_SPINE_NODES_WF1`（L9012–9389 一部分）、`STORY_SPINE_NODE_N17_410`（L16611–16814）。
- 刪函數：`applyStorySpineOverrides46`、`applyStorySpineOverrides48`（主線分支；lan 分支保留，改名 `applyRomanceLanOverrides48`）、`applyStorySpineOverrides410`、`applyStoryWf1Nodes80`。
- 刪載入呼叫：46／48／410／WF1 呼叫＋`L18454` walk 清單入面四個表；保留 lan 單一呼叫。
- `calib60NodeTitle` 改由 `STORY_WIRE.main.nodes` 讀標題（fallback 值不變）。
- 清死碼：`qa.phase5.endings_names_lock`（十個舊結局名）已刪；`STORY_HINT_SOFT` 釋義版 `lockedHint` 經核實係**活碼**（`storyHintPack`／`storyFaceLine` 讀緊），**留低唔郁**。
- `STORY_SPINE_NODES_BR89`（N6F）、`ROMANCE_LAN_PA_OVERRIDES`、`ending410EveNode`、`STORY_HINT_SOFT` 全部保留。

## YEARS66 裁定（已核實，唔係估）

JSON `main` pack 載入嗰陣行 `years66Walk`（`refreshCopyPacksFromDisk`，L18562 新行號附近：`[main, rom1, rom2, rival, gateStub, dengMock, dengPushMock, dualMock].forEach(p=>years66Walk(p, null))`）；`when` 唔喺 `YEARS66_SKIP_KEYS`，`eraTag` 喺（內部用，唔郁）。所以：

- JSON N17 `when: "1990冬"`（舊曆 source）→ 顯示 `1992冬`。**JSON 一字唔使改，冇 double-shift。**
- N1–N19 全部顯示年份已逐個核實（載入檢查 61 項全過）：N1 1990冬／N2 1990冬／N3 1990冬／N4 1990春／N5 1990秋／N6 1990／N7 1991夏／N8 1991夏末／秋／N9 1991秋／N10 1991冬／N11 1991冬末／N12 1992春／N13 1992夏／N14 1992秋／N15 1992秋末／N16 1992冬／N17 1992冬／N18 1990冬／N19 1991春。walk 冪等（`__y66w` 旗）。
- N1–N5 同 base 逐字一致；`gigs_new.json` 同 base 一致。

## 驗收

- `node --check`：兩個 inline script block 全過。
- 載入檢查（`/tmp/v234_loadcheck.js`，用 index.html 真函數模擬載入路徑）：**61 過／0 失敗**。N1–N19 齊、N18／N19 在場、N17 靜態保底兩則（natural／quit_job）、`ENDING410_CHOICE_IDS` 六意向 a–f 在場、六個 eve 選項鍵全部定義；state sweep 五個可達（natural／quit_job／to_backstage／quit_leave／leave_follow）。
- sha 釘：`nodes[5:]` sha 不變（`1be6aa08d6574537f8c6b209b41045f4efe09ec1f692a6f6028932860a8c12b7`）；`test_story157_pack_static.py` 全過，測試冇刪。
- 全套 suite：**312／10，零回歸**（10 項 FAIL 同基線完全一致：flash51／rumor49／slot50／soft_tip_111_restore／start53／weave43／weave44／weave49／wf5_87／wrap38）。中途曾跌到 300／22——12 項係刪表引起嘅測試回歸（3 項內容斷言改指 JSON pack、9 項行號釘 resync），已逐項修好，全部係測試側改動，遊戲 code 冇為咗遷就測試而改。
- `index.html`：24 insertions、2,893 deletions（總行數 48,220 → 45,351，淨 −2,869）。JSON：淨刪 12 行（`endings_names_lock`）。
- 全 repo grep 六個標識：live code 零命中；剩低嘅只有四檔測試嘅「不存在」斷言（執法機制本身）＋凍結歷史記錄（`NOTES_V20A*.md`、`qa131/SUITE3_AB.md`、`qa149/pristine_index.html`），一律唔郁。

## 新發現（pre-existing，唔係 v234 引起，另開票）

- `to_support`（E3 → 行一格返 E2 爭男配）喺現行 v95 梯下**到唔到**：`ending410EveNode` 用同一個 state 同時做 `resolveEnding410`（base E3 要求 E2 分支唔成立：信用 ＜42 或聲望 ＜35）同 `endingE2Eligible410`（要求信用 ≥42 且聲望 ≥35），兩者互斥。410 邏輯本身 v234 一行都冇郁（diff 證實）。六意向 id a–f 同六個選項鍵全部在場；實際可達係五個。
- `tests/fixtures/story_detail_n1_to_n17.json` 極舊（v157 前，17 節點），只係 `test_weave46/48/410_logic.js` 以外嘅測試用緊；今次冇郁佢（嗰三檔已轉 live pack），留待日後清理。

## 未做

- Live 實駕押後（瀏覽器死）：開局→第 39 週第一張配角、頒獎禮全程、引薦／即派實機、新庫真載入、1990 板面、報紙分類、忠告卡。
