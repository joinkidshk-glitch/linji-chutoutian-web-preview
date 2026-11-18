# NOTES_V20A314 — 駱家聲 lok_patron 暖版閘加 lok_calm_truth（跟 Q24／v311 程線前例）

- 版本：v20a314（Q24 前例延伸；v314 係 v311 程線嚴格閘嘅駱線對應票）
- 基線：main `d3ecdcf`（v313 已落地，suite 376／9）
- 改動：`index.html` 1 行 ＋ 新測試 `tests/test_r314_lok_patron_strict.js`（32 項）＋ 舊測試同步 3 檔
- Suite：見 §4

## 1. 問題

`lok_patron` 暖版提攜閘係排除式，`sideline280GrantCompletion` 入面駱線暖版收尾獎勵判定係嚴格版，兩種讀法唔一致：

- 排除式（改前，L41802）：`tier>=4 && !lok_join_rant && !lok_loose_row && !lok_cover_first`，無正面旗要求
  → T4＋無旗玩家，暖版提攜照播、授 `credit_enc83_lok_patron`，但 `sideline280("lok")` warm=false，收尾獎勵（聲望＋2／信用淨＋1）唔派——提攜同獎勵脫鈎。
- 嚴格版（`sideline280GrantCompletion` L39797）：`warm = !!lok_calm_truth && !lok_join_rant && !lok_loose_row && !lok_cover_first`
- `lok_calm_truth` 係 Beat 5 `lok_e4grudge` 選擇 A（L37491，label「勸他：榜是人排的，歌是自己的」）；B 係 `lok_join_rant`。草稿依據：`~/workspace/linji-story-sidelines/drafts/batch2-lok-ngai-chai-pang.md` L361「A（`lok_calm_truth`）→ 好收尾開：`lok_patron` 引薦播出，授 `credit_enc83_lok_patron`。B（`lok_join_rant`）→ 冷收尾：引薦唔開」。

## 2. 改動（§1 唯一改動行）

`index.html` L41802 `lok_patron` 暖版閘改為嚴格版：

```js
// 改前
{ id:"lok_patron", when(st){ return enc79TierOf(st.fav)>=4 && !(S.flags||{}).lok_join_rant && !(S.flags||{}).lok_loose_row && !(S.flags||{}).lok_cover_first; }, ...
// 改後
{ id:"lok_patron", when(st){ return enc79TierOf(st.fav)>=4 && !!(S.flags||{}).lok_calm_truth && !(S.flags||{}).lok_join_rant && !(S.flags||{}).lok_loose_row && !(S.flags||{}).lok_cover_first; }, ...
```

- 同 `sideline280GrantCompletion` 駱線暖版讀法逐字一致。
- 唔郁：冷版閘 `lok_patron_cold`（L41800）、翻唱閘 `lok_patron_cover`（L41801）、`lok_finale` 閘（L41803，要 `beatsDone.lok_patron`，patron 閘一改自動約束）、patron 對白（6 句）、冷版對白（4 句）、翻唱對白（4 句）、grants（`credit_enc83_lok_patron`＋`sideline280GrantCompletion("lok")`）、收尾獎勵判定、registry 次序（e4grudge＜patron_cold＜patron_cover＜patron＜finale）、其餘五線 patron 閘。

## 3. 行為對照

| 玩家狀態 | 改前暖版 | 改後暖版 | 冷版／翻唱 | 收尾獎勵 |
|---|---|---|---|---|
| `lok_calm_truth` 齊備＋T4 | 播 | 播 | — | 派 |
| 無旗（漏做 Beat 5） | 播 | **唔播** | 唔播 | 唔派 |
| `calm_truth`＋`lok_join_rant` | 唔播 | 唔播 | 冷版播 | 唔派 |
| `calm_truth`＋`lok_loose_row` | 唔播 | 唔播 | 冷版播 | 唔派 |
| `calm_truth`＋`lok_cover_first` | 唔播 | 唔播 | 翻唱播 | 唔派 |
| 得 `lok_join_rant`（無 calm_truth） | 唔播 | 唔播 | 冷版播 | 唔派 |
| 得 `lok_cover_first`（無 calm_truth） | 唔播 | 唔播 | 翻唱播 | 唔派 |
| T3（fav 69）有 calm_truth | 唔播 | 唔播 | — | — |

漏做唔死局：`lok_e4grudge` 閘（L41799）係 T1＋E4 已出，無年份窗；grants() 叫 `sideline280GrantCompletion("lok")`。Beat 5 無窄窗，漏做玩家遲補 `lok_calm_truth` 即播暖版（測試 C「漏做趕得切」覆蓋，同 Q24 一樣）。

## 4. 測試

新測試 `tests/test_r314_lok_patron_strict.js`：32 項全 PASS（`node tests/test_r314_lok_patron_strict.js`）。

- (A) 靜態 10 項：暖版閘要 `lok_calm_truth`＋仍排除三壞旗＋仍要 T4；冷版閘／翻唱閘唔郁；grants 唔郁；registry 次序唔郁；patron 對白 6 句（首句逐字）／冷版 4 句／翻唱 4 句唔郁。
- (B) `when()` 直接判定 9 項：calm_truth 齊備開閘；無旗暖／冷／翻唱都唔開；舊排除式放行組合（無旗 T4）而家閂閘；T3 閂閘；calm_truth＋任一壞旗→暖版唔播、對應冷版／翻唱播；單壞旗玩家冷版／翻唱播、暖版唔播。
- (C) 端到端 `enc79BuildScript` 5 項：calm_truth 齊備播 `beat:lok_patron`；無旗／T3／calm_truth＋join_rant 唔播；遲補 calm_truth 即播。
- (D) `sideline280` 一致 4 項：calm_truth 齊備派獎勵（fame＋2／delta＋1／doneKey）；無旗唔派；calm_truth＋join_rant 唔派；七組旗組合閘開＝獎勵派、閘閂＝獎勵唔派。
- (E) 舊檔 2 項：無旗舊檔（舊排除式暖版玩家）唔 crash、唔播暖版；calm_truth 舊檔照播暖版。
- (S) 靜態 3 項：`lok_e4grudge` 閘唔郁；`lok_finale` 閘唔郁；`gigs_new.json` 仍係 306 張。

測試教訓（v311 同款，今票再中兩次）：`when` 回傳係 falsy 值唔一定係 `false`——`&&` 鏈尾項係原始旗值（`undefined`），斷言要用 `!` 唔好用 `=== false`（初版兩項 FAIL 都係呢個原因，已改）。

全套 suite：`bash qa131/run_suite.sh`——TOTAL **PASS 377 FAIL 9**（基線 376／9；+1 係新測試檔，9 項 FAIL 全部係已知 pre-existing：flash51／slot50／soft_tip_111_restore／start53／weave43／weave44／weave49／wf5_87／wrap38）。

**舊測試同步（v311 前例）**：首跑新 FAIL 三檔，全部係舊測試 setup 未設正面旗，已同步，唔係回歸：
- `tests/test_sideline278_logic.js`（2 處）：(4)「無壞旗 → 六線暖版照開」駱嗰格先設 `S.flags.lok_calm_truth=1`；(5) 駱 patron heard_whole／praised_song 嘅 `run()` 補 `S.flags.lok_calm_truth=1`（否則 patron 唔開，變體句無從插入）。
- `tests/test_enc84_logic.js`：§9 T4 提攜 setup 補 `S.flags.lok_calm_truth=1`（跟 v311 程嗰格同一行模式）。
- `tests/test_r305_warm_finale.js`：(B)「提攜未播 → finale 唔開，先播提攜」駱嗰格補 `S.flags.lok_calm_truth=1`（否則 PickBeat 回傳 null，`.id` 撞 crash；魏／齊 patron 閘係排除式，唔使補）。

## 5. 跟進（唔喺今票做）

草稿 L323 引薦閘嘅 `lok_stand_original`＋（`lok_heard_whole` 或 `lok_praised_song`）刻意唔加：① `lok_stand_original` 嚟自 Beat 3 `lok_cover`（閘 T2–T3＋1991 冬＋`lok_kept_row`），窄窗過咗補唔返，加咗會永久鎖死錯過 Beat 3 嘅玩家，違反「漏做唔死局」；② 加咗會同已落地嘅 `sideline280` 駱線暖版讀法再脫鈎（獎勵照派、提攜唔開），要改埋獎勵判定先一致，係另一張設計票。

## 6. 落地

- main HEAD：`PLACEHOLDER_MAIN_HEAD`（內容 `PLACEHOLDER_CONTENT_HEAD`＋NOTES §5 補填）
- Pages：index.html md5 `PLACEHOLDER_PAGES_MD5`／`PLACEHOLDER_PAGES_BYTES` bytes，byte-identical
- 工作副本 `linji-work314` 已刪；`qa296/derive296.json` suite 再生嗰份已還原，唔入版
