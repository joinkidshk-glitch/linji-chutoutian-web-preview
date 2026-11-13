# SUITE3 — v157 驗證結果（splice 再核實＋逐個測試＋全套 A/B）

- 工作副本：`~/workspace/linji-work157/`，分支 `v20a157`，基底 `e08a070`
- Pristine 對照：`~/workspace/linji-pristine155/`（基底 `e08a070`）
- 驗證員：唔落地、唔改遊戲檔；**本檔以外無改過 `NOTES_V20A157.md`／`index.html`／pack／任何測試檔**
- 日期：2026-11-13

## 1. Splice 再核實

### 方法

- 分析目錄嘅 `extract.py` 係抽設計稿 `~/workspace/linji-story-restructure/index.html`（HTML 章節 → JSON），**唔係**抽 live `index.html` 內 JS 表嘅工具，所以唔用佢；改用自寫抽取器 `/tmp/verify157_splice.js`（ephemeral，唔入 repo）：
  - 由工作副本 `index.html` 用 brace-match（跟字串／註解狀態）抽出 6 個 live 表字面量（`STORY_SPINE_NODES_C6` L21702、`STORY_SPINE_NODES_BR89` L22421、`STORY_SPINE_NODES_1989` L19626、`STORY_SPINE_NODES_1990` L20697、`STORY_SPINE_NODE_C17_410` L29672、`STORY_SPINE_NODES_WF1` L22039）＋`CHOICE47_NODES` 整表（取 `.F4_stay_mind`／`.G4_family_job` 兩 key）；
  - 同 fragments 入面嘅 `const … = {…}` 字面量各自 `eval` 後做語義 deep-compare（key／值逐層對，格式差唔計——F4／G4 fragment 鬆散格式 vs live 緊湊格式已由 eval normalize）；
  - 另抽全檔 2 個 inline `<script>` 塊（4,313,191 字元）做 `node --check`。

### 結果：10 處字面差異，全部係 NOTES 已記錄嘅刻意偏離，唔係 splice 錯

| 表 | diff 數 | 內容 | 判定 |
|---|---|---|---|
| `STORY_SPINE_NODES_C6` | 1 | `C6.beats[9].lines[1]`：「N1 嗰條 route 旗」→ live「第一日嗰個選擇」 | 刻意（NOTES §1.2：fragment 引擎術語改玩家面寫法，Q1） |
| `STORY_SPINE_NODES_BR89` | 0 | — | 0 diff |
| `STORY_SPINE_NODES_1989` | 2 | C11 synopsis「後台規矩只有一句」→「後台得一句口頭提點」；C11 beats[1]「司儀企正中嗰塊板，燈一熄，邊個都唔准過界」→「唔係規矩，係呢度嘅做法。司儀企位唔好亂企，燈光就位嗰陣唔好行過」 | 刻意（NOTES §1.4／ERA §2：場務段降級做口頭提點，司儀企位句查無來源刪走） |
| `STORY_SPINE_NODES_1990` | 0 | — | 0 diff |
| `STORY_SPINE_NODE_C17_410` | 1 | synopsis 第 2 段：fragment 係 DEV 註解（「舊版文案寫『頒獎禮前夕、開場之前』……重寫將時間改返做……」）→ live 已改寫做玩家安全寫法（「冬台慶啱啱完——獎已經頒完……今晚唔係頒獎禮之前，係收科嗰晚」） | 刻意（NOTES §1.7：整合員追加修正，synopsis 會上玩家面，唔可以留 DEV meta） |
| `STORY_SPINE_NODES_WF1` | 0 | — | 0 diff |
| `CHOICE47_NODES.F4_stay_mind` | 6 | 全部係 M39 回流口吻：3 個 `effects.notes` 短版＋3 個 `resultBeats[2]` 全句，舊「呢年開始，都有人返嚟喇」→ 新「間中都會聽到，邊個邊個攞咗居留，又返嚟搵食」／短版「間中都會聽到有人返嚟」 | 刻意（NOTES §1.8／ERA §5：F4 6 處按 `ERA_M39_M22.js` manifest 改；舊句 live 全檔 0 命中） |
| `CHOICE47_NODES.G4_family_job` | 0 | — | 0 diff |

- 除上表 10 處外，**其餘全部 key／beats／choices／flags／stats／tags／閘逐值 0 diff**（每表 key 清單 live＝fragment，包括 C17 26 個 key、C6F 唔對稱 key 數目一致）。
- ERA 抽查：C17 含「一成」＝0 處；F4 舊句＝0 處；F4 新全句 ×3＋短版 ×3＝6 處（吻合 NOTES §1.8「6 處」）；C17 含「台灣」＝有（M22 照用）。
- `node --check`：全檔 inline script **PASS**。

### Pack 組（`content/story_detail_c1_to_c17.json` nodes[0–4]）

- Live vs pristine pack：nodes[0–4]（C1–C5）有改動，nodes[5–16]（C6–C17）**逐項完全相同**，top-level key 集合相同——改動範圍正好係授權嘅 C1–C5，死 pack C6–C17 零郁。
- Pack 內容本身由新測試 `test_story157_pack_static.py` 逐值核對（見 §2），124 斷言全 PASS。

**Splice 結論：實質 0 diff——10 處差異全部有 NOTES／ERA 依據嘅刻意改寫，無未解釋差異，無漏 splice。**

## 2. 逐個直接跑相關測試（15/15 PASS）

| 測試 | 結果 |
|---|---|
| `tests/test_story157_index_static.py`（新） | PASS（117 行 PASS＝115＋2 斷言，吻合 NOTES §5.1） |
| `tests/test_story157_pack_static.py`（新） | PASS（124 行 PASS 斷言，吻合 NOTES §5.1） |
| `tests/test_gate136_static.py` | PASS |
| `tests/test_weave47_static.py` | PASS |
| `tests/test_weave48_static.py` | PASS |
| `tests/test_weave48_logic.js` | PASS（67 過／0 失敗） |
| `tests/test_wf1_80_logic.js` | PASS |
| `tests/test_text125_static.py` | PASS |
| `tests/test_weave46_static.py` | PASS |
| `tests/test_travel114_static.py` | PASS |
| `tests/test_travel114_logic.js` | PASS |
| `tests/test_aud91fix122_static.py`（守衛窄化） | PASS |
| `tests/test_aud91fix124_static.py`（守衛窄化） | PASS |
| `tests/test_gigreq110_static.py`（守衛窄化） | PASS |
| `tests/test_wf5_87_static.py`（守衛窄化） | PASS |

§5.3 嗰 7 個具名更新測試＋4 個守衛窄化測試＋2 份新測試，連同 `weave48_logic.js`／`travel114_logic.js` 兩個 logic 配對檔，全部逐個直接跑 PASS。

## 3. 全套 A/B（`qa131/run_suite.sh`）

| Run | 總數 | FAIL 數 |
|---|---|---|
| 工作版 A（`qa131/suite3_workA.txt`） | **213 PASS／12 FAIL**（225 檔） | 12 |
| Pristine A（`qa131/suite3_pristineA.txt`） | **211 PASS／12 FAIL**（223 檔） | 12 |

- 總數差 ＋2＝正好係 2 份新測試（`test_story157_index_static.py`＋`test_story157_pack_static.py`），其餘 PASS 數不變。
- FAIL 清單兩邊 **逐項相同**（`diff` 零差異），全部係基線 12 項 pre-existing：

```
tests/test_flash51_static.py
tests/test_giglib36_static.py
tests/test_pacing35_static.py
tests/test_poster59_static.py
tests/test_rumor49_static.py
tests/test_slot50_static.py
tests/test_soft_tip_111_restore.py
tests/test_start53_static.py
tests/test_weave43_static.py
tests/test_weave44_static.py
tests/test_weave49_static.py
tests/test_wrap38_static.py
```

- 多出嚟嘅 FAIL：**0 項**——無需逐個重跑（重跑條件唔觸發）。
- 第二次工作版確認 run：**無跑**——兩次總數差完全由新測試數解釋（213−211＝2），FAIL 清單逐項相同，無 AGENTS.md 所講嘅大幅波動跡象。

## 4. 結論：零回歸

- Splice 實質 0 diff（10 處差異全部係 NOTES 已記錄嘅刻意改寫）。
- 相關測試 15/15 逐個直接 PASS（新測試斷言數 117／124 吻合 NOTES §5.1）。
- 全套 A/B：工作版 213／12 vs pristine 211／12，FAIL 清單逐項相同，多出 FAIL 0 項。
- **v157 工作版零回歸，可填 NOTES §5.4 為「工作副本 213 PASS／12 FAIL；pristine 211 PASS／12 FAIL；FAIL 清單逐項相同」。**
- §6 實駕（drive2）唔喺本票範圍，維持 PENDING。
