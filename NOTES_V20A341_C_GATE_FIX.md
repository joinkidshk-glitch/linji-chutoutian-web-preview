# v20a341 C-id 閘門修復 — NOTES

## Bug

四個 ENC79 beat 閘用舊 C id，喺真實存檔永遠唔開：

| 位置 | beat | 舊閘 | 改後 |
|---|---|---|---|
| index.html L39872 | `liu_foreshadow` | `enc83NodeDone("C8")` | `enc83NodeDone("N9")` |
| index.html L39875 | `liu_steal`（收割鏈入口） | `enc83NodeDone("C8")` | `enc83NodeDone("N9")` |
| index.html L39877 | `liu_clash` | `enc83NodeDone("C13")` | `enc83NodeDone("N16")` |
| index.html L39882 | `mak_intel` | `enc83NodeDone("C15")` | `enc83NodeDone("N12")` |

根因：`enc83NodeDone`（L41683）→ `StoryOC.isDone(id)` 直查 `story.done[id]`，無 C→N 翻譯；劇情完成 `markDone(node.id)` 寫入 N id；全檔無 code 寫 C key 入 `story.done` 或 `done_` 旗。之前 v269／v278 等 drive 播種 C key 先開到閘，所以一直冇捉到；v279 實駕 7a 用真實存檔（只有 N9）證明閘死咗。C→N 對照跟 C2N210 表（C8→N9／C13→N16／C15→N12）。

## 改動

1. **四閘改讀 N id**（同行改動，index.html 行數不變 47,296，零釘行漂移）；註解同步改走「C8＝N9」等舊對照字句。
2. **唔留 C 翻譯層**：`enc83NodeDone` 本身唔郁（新測試 A7 釘住：直查 isDone／done_ 旗、無 C 字串）。
3. **測試同步**（播種／斷言 C key 改 N key）：
   - `tests/test_sideline269_logic.js`：L2 註解、L52 靜態斷言、L127–142 三組閘測試（標籤＋`_doneNodes.add`）、L163 pushSeg 播種。
   - `tests/test_r287_liu_patron_liao.js`：L57 靜態斷言。
   - `tests/test_wf3_279_logic.js`：L127 `liuSetup` 播種、L132 標籤。

## 全檔掃描判斷（C-id 引用逐個核對）

- **index.html**：`"C[0-9]+"` 命中只有上述四閘（code＋註解），已全改；`done_C` 零命中；單引號 C id 零命中。
- **content/story_detail_n1_to_n17.json**：C id 零命中，needDone 鏈本身已用 N id，無需改。
- **content/SANDBOX_C1_FUSION_DRAFT_v1.json**：`meta.sandbox: true`、`liveTouch: false` 嘅 2026-11-03 設計草稿，全 repo 無任何檔案載入佢——歷史草稿，唔郁。
- **tests/fixtures/spine_c6_c17_v79.json**：v79 舊脊骨 fixture，無任何測試引用（grep .js／.py 零命中）——歷史 fixture，唔郁。
- **tests/test_story198_logic.js／test_progress71_logic.js 嘅 C2N210 對照表**：測試側種子翻譯工具（將舊 C 種子轉做 N），C key 係翻譯來源、有實際用途，唔郁。
- **tests/test_hiu266_logic.js**：C 引用係移植註解＋負斷言（舊 C openConditions 唔存在），本身正確，唔郁。

## 驗證

- **新測試** `tests/test_r341_c_gate_fix.js`：**19 項 ALL PASS**（靜態 7：四閘讀 N id、C 閘零殘留、註解清、enc83NodeDone 無翻譯層；真跑 12：抽真 enc83NodeDone＋enc83Flag＋enc79TierOf＋ENC79_BEATS，StoryOC.isDone 以 _doneNodes 模擬真實存檔——播種 N9 開 foreshadow／steal、淨播種 C8 唔開；N16／N12 同理）。反證：喺 v340 index 上行 → 14 項乾淨 FAIL（行為保留斷言照過）。
- **改過嘅三個舊測試**重跑全部 ALL PASS。
- **全套 suite：394／9**（v340 基線 393／9＋新測試檔 1 項；9 FAIL 同基線逐項一致：flash51／slot50／soft_tip_111_restore／start53／weave43_static／weave44_static／weave49_static／wf5_87／wrap38）。suite 後已還原 `qa296/derive296.json`。

## 出貨

- 工作副本 `linji-work341`（clone 式），分支 `v20a341`。
- main HEAD：見落地紀錄（內容 commit＋NOTES 落地紀錄）；Pages 核實 byte-identical。
- 通告庫 323 張不變；index.html 47,296 行不變。
- 證據：`~/workspace/suite341.txt`。
