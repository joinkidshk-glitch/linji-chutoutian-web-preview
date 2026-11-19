# NOTES_V20A338 — wf3SettleTick 信用改寫 delta（v287 實駕真 bug）

## 背景
- v287 廖炳星 Beat 5 冷版實駕（~/workspace/linji-drive-liu287/CHECKLIST.md）搵到真 bug：steady 結算「行內信用 +2」永遠落唔到袋（實測 industryCredit 48→48、industryCreditDelta 0→0，toast 照講 +2）。
- 基線：main 04556b9（v337，通告庫 323 張，index.html 47,296 行，suite 390／9）。

## 機制（開工前喺工作副本核實）
- industryCredit 係派生值：`dualTrackNumbers`（L16642）= baseCredit(fame/stage/acting/stress) + `industryCreditDelta`；`syncDualTracks`（L16657）將 `S.industryCredit` 覆寫做派生值（L16661 `s.industryCredit = n.industryCredit`）。
- 兩處直接寫鏡像欄再 sync，即刻俾冚走：
  1. L27851（steady 結算）：`S.industryCredit = Math.max(0, (Number(S.industryCredit)||0) + 2);` → L27852 sync。+2 永遠落唔到。
  2. L27911（收割過期）：`S.industryCredit = Math.max(0, (Number(S.industryCredit)||0) - 2);` → L27912 sync。−2 罰則同樣永遠落唔到。
- 正確寫法係寫 `industryCreditDelta`（`sideline280GrantCompletion` L39829：`S.industryCreditDelta = (Number(S.industryCreditDelta)||0) + 1;`＋sync，實測落袋）。派生值本身喺 dualTrackNumbers 已 clamp ≥0，delta 唔使再 clamp。
- S.fame 直接寫唔受影響（fame 係派生公式輸入，唔係輸出）。

## 改動（同行改動，行數不變 47,296，零釘行漂移）
1. L27851 → `S.industryCreditDelta = (Number(S.industryCreditDelta)||0) + 2;`（sync 照舊行，鏡像即時更新）。
2. L27911 → `S.industryCreditDelta = (Number(S.industryCreditDelta)||0) - 2;`。
3. 唔郁：toast 文案（「行內信用 +2／−2」而家先真係兌現）、報紙、結算旗（liaoSettled／liaoHarvestDone／liaoHarvestExpired）、SAVE key。

## 全檔掃描結果（grep `industryCredit =／+=／−=／++／−−`＋`.industryCredit`＋`industryCredit:`＋括號寫法，逐個判斷）
| 位置 | 寫法 | 判斷 |
|---|---|---|
| L16651 | `const industryCredit = Math.max(0, baseCredit + extra);` | dualTrackNumbers 內局部 const，非狀態寫入。唔郁。 |
| L16661 | `s.industryCredit = n.industryCredit;` | syncDualTracks 本身（brief 明文除外）。唔郁。 |
| L27851 | `S.industryCredit = ... + 2` | **BUG（steady）→ 改寫 delta。** |
| L27911 | `S.industryCredit = ... - 2` | **BUG（過期）→ 改寫 delta。** |
| L8346／L8380 | `statsApplied.industryCredit = ...` | 本地累加器欄位，L8427 套用時寫 `S.industryCreditDelta`（正確路徑）。唔郁。 |
| L8426–8427 | `S.industryCreditDelta = ... + Number(statsApplied.industryCredit);` | 正確寫法。唔郁。 |
| 其餘 `.industryCredit` 命中（L8434、L8725、L12460、L12563、L12645、L12959、L16688、L17045、L17423、L17578、L20487、L22088、L25032、L28804、L29980、L30315、L30711、L30817、L31411、L31724、L31824 等） | 全部係讀取／顯示／回傳字面量（dual 報告、fallback 預設、獎勵表 pick、rewardsApplied pack 欄） | 非狀態寫入。唔郁。 |
| `industryCredit:` 字面量（L8434、L12460、L12563、L16658、L16686、L17045、L17426、L22086、L25031、L27805、L30704、L30817、L31086、L31469、L31837、L45822、L45829） | 本地回傳／報告物件 | 非狀態寫入。唔郁。 |
| 括號寫法 `["industryCredit"]` | 0 命中 | — |
| normalizeSaveObj（L16144） | 無 industryCredit 寫入（只補 week/money/fame/stage/dayIndex） | 無遷移寫法要處理。 |

結論：同類 bug 全檔只有 wf3SettleTick 兩處，已全部改寫 delta。靜態守衛（test_r338 D5）：全檔 `S.industryCredit` 直寫（=／+=／−=）0 命中。

## 測試同步（舊測試釘住舊寫法）
- `tests/test_sideline282_logic.js` L56：靜態字串斷言 Q13_overdue_credit_minus2 改釘新 delta 寫法（意圖不變：過期分支信用 −2 在位）。
- `tests/test_wf3_82_logic.js`：兩處斷言由「鏡像 ±2」改「delta ±2」（該測試 syncDualTracks 係 no-op stub，舊斷言靠直寫鏡像先過；真 sync 落袋由新測試驗）。
- `tests/test_wf3_279_logic.js`：同上兩處（穩陣 +2／過期 −2 改驗 delta）。

## 新測試
- `tests/test_r338_wf3_credit_delta.js`，19 項：A steady（delta +2、真 sync 後鏡像 10→12、冪等、toast 文案）、B 過期（delta −2、鏡像 10→8、冪等、唔計 settled）、C steal 不變（+$800、delta／鏡像唔郁、記債）、D 靜態（舊字串清零、新字串在位、全檔直寫 0 命中、statsApplied 路徑不變）。用真 dualTrackNumbers/syncDualTracks（唔 stub）。
- 反證：喺 v337 index 上行 → 10 項乾淨 FAIL（A1×2／A2／B1×2／B2／D1–D4），證明測試真係驗到修復。

## 實駕覆驗
- 本地 serve 工作副本（md5 對版 `9dc6e675…`），liu287 harness 改指本地（`~/workspace/linji-drive338/drive338.py`）重播：
  - **steady**：`steady-credit+2: PASS | industryCredit 48 -> 50`（v287 係 48→48 FAIL）——修復成立。sideline280 兩項 FAIL 照舊（live 設計：獎勵要 clash_stand 先派，唔係 bug，同 v287）。
  - **probe_settle**：`probe_settle-delta-moved: PASS | industryCreditDelta 0 -> 2`（v287 係 0→0）——持久通道真係郁。`probe_settle-credit+2: FAIL | industryCredit 10 -> 50` 係 harness 種子假象：種子鏡像寫死 10，但種子 fame=80 派生 baseCredit=48，首次 sync 校正做 48+2=50；delta 0→2 精確，唔係 bug。
- 證據：`~/workspace/linji-drive338/`（harness＋截圖＋run_steady_v338.log／run_probe_v338.log）。

## 落地
- （落地時補：main commit、Pages md5、suite 總數。）
