# Soft QA — `SOFT_PROGRESS_SEED_C3_C5_DENG_v1` · 2026-11-04（Asia/Hong_Kong）

> json SHA8 **`bd86ed8c`** · md SHA8 **`a2bfdaf1`**  
> Paths：`/workspace/star-volunteer-web/content/` ＝ store-cbdfa415（bytes equal）  
> Soft≠PASS · **唔 tip LIVE** · **唔改 LIVE week-gate** · 89–92 HOLD

## Overall

**PASS**（靜態／對 stub Soft A 引擎規則）

| Decision | Value |
|---|---|
| Soft tip seed files → iOS content | **YES** |
| Soft tip `?softSeed=` 注入器 | **YES**（瀏覽器抽樣前置；見下） |
| LIVE tip / 抬 `?v=` | **NO** |
| Browser C3–C5／鄧 meet | **PENDING**（等 Soft 注入器 LIVE Soft PR） |

## Checklist

| # | Item | Result |
|---|---|---|
| 1 | SHA8 對齊宣稱 | **PASS** json `bd86ed8c`／md `a2bfdaf1`；content＝store |
| 2 | meta `liveWeekGateStillActive`＋`tipForbidden` | **PASS** true／true |
| 3 | Soft A：C3 fame=16（>15）；neg fame=15 FAIL；禁誤寫 fame>16 作門檻 | **PASS**（禁句只出現在「禁誤寫」說明） |
| 4 | C4 favor≥1@agency_ho ∧ loc；stub softLogic AND | **PASS** |
| 5 | C5 autumn＋choi/hau；rival_gao 唔入 seed rumors | **PASS** |
| 6 | 鄧 meet：C5 done＋favor≥1@agency；push+ 唔測 | **PASS** |
| 7 | 五種子 eval vs stub `cba0e877` | **PASS** 全開 |
| 8 | negativeChecks | **PASS** 全 GOOD |

## Soft eval（對 stub trigger）

| Seed | Beat | Result |
|---|---|---|
| `seed_c3_ready` | C3 | PASS |
| `seed_c4_ready` | C4 | PASS |
| `seed_c5_ready` | C5 | PASS |
| `seed_deng_meet_ready` | R_tang_meet | PASS |
| `seed_chain_shortest` | R_tang_meet | PASS |

Neg：fame15 FAIL／fame16 PASS／favor0 FAIL／summer FAIL／缺 C5 FAIL — 全 GOOD。

## Browser blocker（唔擋種子 PASS）

LIVE `?v=19w` **未掛** seed JSON（Pages 404）且無 `?softSeed=` 注入。  
`calendarSeason()` 跟 `dayIndex` 日曆，唔直接讀 seed.`season` → Soft 注入器必須：

1. 合入 `content/SOFT_PROGRESS_SEED_C3_C5_DENG_v1.json`（＋md）
2. Soft-only：`?softBehaviorGate=1&softSeed=<id>`（或 console hook）把 state map 入 `S`：
   - `dayIndex = (week-1)*7`（對齊 `weekNumNow`）
   - `S.fame`；`S.story.done[Cx]=true`；`S.story.favor.agency_ho`；`S.story.gigCount`
   - rumors → `S.story.rumors`／notebook／mockRumors 之一（`liveRumors` 讀得到）
   - **season**：Soft 覆蓋 `calendarSeason` 或揀令日曆＝秋／冬嘅 dayIndex（C5／鄧）
   - 開檔後 `atLoc`／進對應 loc sheet 再觸發
3. **唔 tip LIVE**；僅 Soft PR

## Footer

Soft≠PASS。種子靜態 PASS ≠ 產品 PASS；瀏覽器 C3–C5／鄧 meet 等 Soft 注入器後再抽。
