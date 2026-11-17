# NOTES v20a258 — N4 季節定案：改夏

- **拍板**：用戶 2026-11-17 08:25 揀「以『夏』為準」。
- **基線**：main `147c525`（v254）。

## 改動（工作副本 `linji-work258`，6 檔）

| 檔 | 改動 |
|---|---|
| `content/story_detail_n1_to_n17.json` N4 | `when` 1988春 / W8-9 → **1988夏 / W22-23**；`eraTag` → `era_1988_summer_grassroot`；`openConditions` week_min:8 → **22**；`pacing` weekMin 8 → 22＋when 同步 |
| `content/SANDBOX_BEHAVIOR_GATE_N1_N5_SOFT_STUB_v1.json` N4 | trigger.weekMin 8 → **22**；legacyWeekMin 8 → 22；relockNotes 加註 v20a258 |
| `content/STUB_STORY_BEATS_FREEPLAY_SLOTS_v1.json` N4 | trigger.weekMin 8 → **22**；when／eraTag 同步改夏 |
| `content/gigs_new.json` film_203《水塘夜戲》 | season 春 → **夏**（庫 282 張零增減） |
| `index.html`（BehaviorGate selfCheck） | floors N4:8 → **22**；c4base week:8 → **22** |
| `tests/test_story157_pack_static.py` | GATES N4 同步新值＋歷史註解一行（nodes[5:] sha 唔受影響，N4 係 nodes[3]） |

另同步設計目錄 `~/workspace/linji-gig-redesign/regen-v2/gigs_new_v2.json` film_203 season → 夏（設計 copy 同 repo 本來 282/282 完全一致，只差呢一格；`full_verify_checks.py` exit 0，無 FAIL）。

## 週數點定：W22-23

- 遊戲曆 1990-01-01 起，6 月 1 日係第 22 週（day 151），即夏天第一週；W22 橫跨 5 月 28 日–6 月 3 日，含 6 月 1–3 日。
- 窗口闊度跟返原本 2 週（W8-9 → W22-23）；N3 春末 W6-8 → N4 夏 W22-23 → N5 秋 W36，成個第一年平均分佈。

## 閘邏輯核實（唔好淨改字面）

- **live 閘係 stub trigger**：v249 D8 落實，`liveWeekGateStillActive()` 回 false，N1–N5 live 行 stub trigger（`evalTrigger_AND_softRumor`）。JSON 嘅 openConditions／pacing 係舊 week-gate 遺留＋設計紀錄（test_story157 釘死），照改求一致。
- **slots overlay 會贏 stub**：`applyFreeplaySlots` 用 `Object.assign` 將 slots trigger 蓋落 byId——slots 唔改，runtime 會將 weekMin 蓋返 8。所以 stub＋slots 兩邊都要改 22。
- **selfCheck 釘 post-overlay 值**：floors N4:8→22、c4base week:8→22；Python 模擬 stub＋slots overlay 後 floors 五項全啱。
- **eraTag 唔改會穿幫**：live 標籤路 `spPlayerMeta` 讀 `eraTag||when`，eraTag 優先；N4 舊 `era_1988_spring_grassroot` 會令標籤繼續出春。N4 獨立開 `era_1988_summer_grassroot`（N1 繼續用 spring，唔郁）。核實：live 標籤「主線 · 1990夏」、Soft 路季節字「夏」、humanizeEraId「1988 夏 · 草根檔」。
- **film_203 季節欄唔閘派發**：`mergeTriggerGigs`／`triggerGigOn`／`grant229RecordFromChoice` 零 season 檢查；season 只係板面顯示標籤。GRANT229 N4_b → film_203 映射唔郁。
- **beats 正文唔郁**：JSON beats[0] 本來就係「1988年夏」。

## 驗證

- JS 語法：抽兩個 `<script>` 塊 `node --check` 通過。
- 個別測試 ALL PASS：story157 pack／index、pacing35、nat92（static）、gig229 grant、story_gate113、story179、story191、story165。
- 全套 suite：見 commit 訊息（預期 316／10，十項已知 pre-existing）。
- `full_verify_checks.py`（設計 copy）：exit 0，無 FAIL。

## 新發現（未修，唔阻落地）

- **live N4 播嘅係 slots 對白，唔係 JSON 對白**：`applyFreeplaySlotsToSoftGate` 逢 slots 有 playable beats 就 `storyNode.beats = slot.beats.slice()`；N4 slots 有 8 拍實文。所以 JSON beats[0]「1988年夏」嗰句 live 唔會播出；slots 版 N4 對白本身無季節戳。季節定案嘅依據仍然成立（標籤＋閘＋施工單＋攻略），但「故事第一句寫夏」只係 JSON 層證據，唔係播出層。攻略引文對 JSON（v254 重對做法）唔受影響。
- Slots N4 嘅 when／eraTag 字串唔會被 overlay 寫入節點（只抄 trigger／locId／playerFaceLine／beats／choices），今次同步改夏只為檔案一致。

## 刻意留返

- `tests/test_story179_logic.js` CASES.N4（weekMin:8／week:4）：自包含場景，測鎖定提示文字，唔讀 live 值；week 4＜22 照樣鎖定，唔郁。
- `content/story_beats_phase1.json` B08 "W8-9"：舊 phase-1 beats 檔（另一套章系統），唔係 N4 節點，唔郁。
- `tests/fixtures/` 凍結快照唔郁；N1 eraTag 唔郁。
- 攻略側唔使改（N4 blockquote 已由引文重對 edit 改返夏；重對表有 13 行 N4，builder 回報 NEW MISSING=0）。

## 待實機驗證（瀏覽器死，押後）

- N4 第 22 週夏天開閘；章標籤顯示 1990夏；N4 播 slots 對白。
