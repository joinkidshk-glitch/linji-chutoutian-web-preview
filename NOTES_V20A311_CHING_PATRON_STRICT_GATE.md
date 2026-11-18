# NOTES_V20A311 — Q24 程天諾 patron 暖版閘改嚴格版三旗齊備

- 版本：v20a311（Q24）
- 基線：main `b580c33`（v310 已落地，suite 373／9）
- 改動：`index.html` 1 行 ＋ 新測試 `tests/test_r311_ching_patron_strict.js`（30 項）
- Suite：見 §4

## 1. 問題

`ching_patron` 暖版提攜閘係排除式，`sideline280GrantCompletion` 入面程線暖版收尾獎勵判定係嚴格版，兩種讀法唔一致：

- 排除式（改前，L41899）：`tier>=4 && flag_vocal_train && !ching_back_polish && !ching_stand_fast`
  → 漏做 Beat 3（無 `ching_back_train`）或 Beat 4（無 `ching_stand_slow`）嘅玩家，照播暖版提攜、授 `credit_enc84_ching_patron`，但收尾獎勵（聲望＋2／信用淨＋2）唔派——提攜同獎勵脫鈎。
- 嚴格版（`sideline280GrantCompletion` L39821）：`flag_vocal_train && ching_back_train && ching_stand_slow`

## 2. 改動（§1 唯一改動行）

`index.html` L41899 `ching_patron` 暖版閘改為嚴格版：

```js
// 改前
{ id:"ching_patron", when(st){ return enc79TierOf(st.fav)>=4 && enc87StoryFlag("flag_vocal_train") && !(S.flags||{}).ching_back_polish && !(S.flags||{}).ching_stand_fast; }, ...
// 改後
{ id:"ching_patron", when(st){ return enc79TierOf(st.fav)>=4 && enc87StoryFlag("flag_vocal_train") && !!(S.flags||{}).ching_back_train && !!(S.flags||{}).ching_stand_slow; }, ...
```

- 同 `sideline280GrantCompletion` 程線暖版讀法逐字一致（`F = S.flags`，見 L39812）。
- 唔郁：冷版閘 `ching_patron_cold`（L41898）、patron 對白（6 句）、冷版對白（4 句）、grants（`credit_enc84_ching_patron`＋`sideline280GrantCompletion("ching")`）、收尾獎勵判定、registry 次序（e4＜patron_cold＜patron）。

## 3. 行為對照

| 玩家狀態 | 改前暖版 | 改後暖版 | 冷版 | 收尾獎勵 |
|---|---|---|---|---|
| 三旗齊備＋T4 | 播 | 播 | — | 派 |
| 缺 `ching_back_train`（漏 Beat 3） | 播 | **唔播** | 唔播（無修音旗） | 唔派 |
| 缺 `ching_stand_slow`（漏 Beat 4） | 播 | **唔播** | 唔播（無修音旗） | 唔派 |
| 得 `flag_vocal_train`（舊排除式放行組合） | 播 | **唔播** | 唔播 | 唔派 |
| 修音玩家（`ching_back_polish`） | 唔播 | 唔播 | 播 | 唔派 |
| T3（fav 69）三旗齊備 | 唔播 | 唔播 | — | — |

漏做唔死局：registry 順序 e4／heart 行先過 patron，Beat 3／4 遲做趕得切——遲補 `ching_stand_slow` 之後即播暖版（測試 C「遲做趕得切」覆蓋）。

## 4. 測試

新測試 `tests/test_r311_ching_patron_strict.js`：30 項全 PASS（`node tests/test_r311_ching_patron_strict.js`）。

- (A) 靜態 8 項：暖版閘三旗齊備＋無排除式旗＋仍要 T4；冷版閘唔郁；grants 唔郁；registry 次序唔郁；patron 對白 6 句／冷版 4 句唔郁。
- (B) `when()` 直接判定 8 項：三旗齊備開閘；缺任何一旗閂閘；舊排除式放行組合而家閂閘；T3 閂閘；修音／修音旗玩家暖版唔播、冷版播。
- (C) 端到端 `enc79BuildScript` 5 項：三旗齊備播 `beat:ching_patron`；缺 `ching_back_train`／`ching_stand_slow`／T3 唔播；遲補 `ching_stand_slow` 即播。
- (D) `sideline280` 一致 4 項：三旗齊備派獎勵（fame＋2／delta＋1／doneKey）；缺一旗唔派；五組旗組合閘開＝獎勵派、閘閂＝獎勵唔派。
- (E) 舊檔 3 項：舊排除式暖版玩家（得 `flag_vocal_train`）唔 crash、唔播暖版；三旗齊備舊檔照播；`S.story.flags` 讀法照播。
- (S) 靜態 2 項：`ching_e4` 閘唔郁；`gigs_new.json` 仍係 306 張。

測試教訓：冷版 `when` 回傳係 truthy number（`1`）唔係 `true`（`&&` 尾項係原始旗值），斷言要用 `!!` 唔好用 `=== true`。

全套 suite：`bash qa131/run_suite.sh`——TOTAL **PASS 374 FAIL 9**（基線 373／9；+1 係新測試檔，9 項 FAIL 全部係已知 pre-existing：flash51／slot50／soft_tip_111_restore／start53／weave43／weave44／weave49／wf5_87／wrap38）。

**舊測試同步（v301 前例）**：首跑 371／12，三項新 FAIL 全部係舊測試寫死舊排除式閘，已同步更新斷言，唔係回歸：
- `tests/test_enc84_logic.js`：T4 提攜 setup 補 `ching_back_train`＋`ching_stand_slow`。
- `tests/test_r305_warm_finale.js`：F 組 patron 閘 setup 補兩旗＋改名嚴格版；S 組靜態字串改新閘原文。
- `tests/test_sideline278_logic.js`：(4)「有 train 旗＋無壞旗 → 暖版開」改做「三旗齊備 → 暖版開」＋補兩旗；冷旗組改名（暖版唔開而家係因為缺正面旗）。其餘斷言（無 train 旗暖／冷都唔開、冷旗組暖唔開冷開）行為不變，照舊 PASS。

## 5. 落地

- main HEAD：（待填）
- Pages：index.html md5（待填）／bytes（待填），byte-identical 核實。
- `qa296/derive296.json`：suite 重跑再生，commit 前已還原，唔入版。
