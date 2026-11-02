# FLOW_ENG_HANDOFF_v1 — 預覽引擎（phone-preview）

- Date: 2026-11-03 Asia/Hong_Kong
- JSON：`content/story_detail_c1_to_c17.json` **1.2.3**
- Soft≠PASS · 出圖 HOLD
- 用戶批全套：when／日耗閘＋C1 下一節唔開手帳＋C5 鎖因可見

## 讀邊份

| 優先 | 檔 |
|---|---|
| 1 | `story_detail_c1_to_c17.json` **1.2.3**（`pacing`＋`openConditions` token） |
| 2 | 本檔 |
| 3 | `PLAN_FLOW_FAIL_DECISIONS_v1.md`／`QA_STORY_FLOW_V17Y_v1.md` |

`when` 字串（例 `1988春 / W4-5`）**唔使改稿**；下界已抽成 `pacing.weekMin`／`week_min:N`。

---

## 邊啲係劇本／邊啲要 eng

| # | 項 | 誰 | 期望 |
|---|---|---|---|
| **A1** | `week_min:N`／`pacing.weekMin` | **eng** 執行；JSON 已齊 | game week ≥ N 先當 openConditions 過 |
| **A2** | `days_after_prev:1`／`pacing.minDaysAfterPrev` | **eng** | 上一節相關主線完成日之後 ≥1 日曆日；**禁同日連播多節 C\***（即使 week 已達，例如 C1 喺 W4 播完唔好即開 C2） |
| **A3** | `when` 文案 | 劇本（已定） | 唔解析字串亦可；以 `pacing`／token 為準 |
| **B** | C5（及任何鎖住下一主線）鎖因 | **eng** UI | 「即將可出」／結算顯示 **`lockedHint`**；**禁** raw `need_done:`／flag id |
| **C** | 「下一節」CTA | **eng** | → 下一可播主線 `StoryPlay` 或地圖針；**永不** `showB01HomeModal`／手帳。手帳只經頂欄／chip／次要入口 |
| **D** | hint／針文案 | 劇本 **已 1.2.2+** | eng 照讀欄；頂欄「劇情」vs chip「事態」＝eng 文案統一「事態」 |

---

## Token／欄位（StoryOC）

```
openConditions AND 新增：
  week_min:4          → week >= 4
  days_after_prev:1   → days since prev mainline settle date >= 1

節點另有：
  pacing: { weekMin, minDaysAfterPrev, when?, prevMain? }
```

- **C1**：`openConditions=[]`；`pacing.minDaysAfterPrev=0`（開局可播）。
- **C2–C17**：雙寫 token＋`pacing`；eng 認其一即可。
- **days_after_prev 實作建議（防同日四連）：** 全域：當日已成功播完任一 `C*` → 其他 `C*` 當日唔入可播（locked 用下一目標 `lockedHint` 或「改日再繼續主線事態」）。`pacing.prevMain` 僅參考；C13–C15 並行以 C11 為 oc 根，仍受全域同日禁＋各自 weekMin。
- **C5** 另保留既有 `openConditionsAny`（采兒≥2 OR 夏台慶）。

### C1–C5 速查

| ID | weekMin | minDaysAfterPrev | 其他 |
|---|---|---|---|
| C1 | 3 | 0 | 開局 |
| C2 | 4 | 1 | +C1 |
| C3 | 6 | 1 | +C2 |
| C4 | 8 | 1 | +C3 |
| C5 | 9 | 1 | +C4 + Any 采兒／夏 |

---

## 驗收（交 tester 覆測前）

- [ ] 同曆日唔可 C1→C2→C3→C4 連播
- [ ] C1 結算「下一節」唔開 B01；去 C2（若已 open）或地圖／lockedHint
- [ ] C4 後 C5 未開：「即將可出」見 C5.`lockedHint`（采兒／台慶口吻），無 `need_done:`
- [ ] Lead／事態頭唔再釘死已播完嘅「先練／先賺」

## HOLD

Soft≠PASS · 出圖 · 鄧節序 · C5 裸旗 rename
