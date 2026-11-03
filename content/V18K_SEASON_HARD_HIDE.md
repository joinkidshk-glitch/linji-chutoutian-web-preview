# V18K_SEASON_HARD_HIDE

**SAVE：** `starVolunteer_map_v18k`  
**時間：** 2026-11-03（Asia/Hong_Kong）  
**預覽：** `joinkidshk-glitch/linji-chutoutian-web-preview`  
**HOLD：** Soft≠PASS；全量出圖未開

## 做咗咩

| # | 項 | 做法 |
|---|---|---|
| 1 | **錯季硬藏** | `doScout`：`usePool = inSeason`（`seasonRank<=0`）；刪 `inSeason` 空→全 `pool` fallback；刪 `!shown` 再從全庫 take |
| 2 | **空板文案** | 冇當季／可上板時：`今日通告板冇貼。`（唔再「暫後排」露出錯季） |
| 3 | **seasonTipHtml** | 錯季 return `""`（唔再 `.season-tip.off`「暫後排」） |
| 4 | **isGigConsumed** | `done_{id}` 或 `S.shoots` 有同 `gigId` → true |
| 5 | **canAudition** | consumed → `{ok:false, reason:"呢單已殺青"}`（未獲聘仍可再試） |
| 6 | **板路徑對齊** | doScout／tipGig／ad 14 日 refresh／openLoc scrub：排除 consumed＋錯季 |
| 7 | SAVE | `…_v18j` → `starVolunteer_map_v18k` |

## Tester 覆測（清 SAVE）

1. `?v=18k` 硬 refresh；SAVE=`starVolunteer_map_v18k`
2. 春檔：海港廣播等冇當季檔 → 空板「今日通告板冇貼」；唔見夏／冬錯季卡／「暫後排」
3. 殺青一單後「只睇通告板」唔再出現該 id；試鏡入口 `呢單已殺青`
4. 拍攝中（`S.shoots`）同樣唔上板／唔可約
5. Soft≠PASS

## curl-verify（填 ship 後）

- SAVE=`starVolunteer_map_v18k`
- HTML：`const usePool = inSeason` · `isGigConsumed` · `呢單已殺青` · `今日通告板冇貼` · 無 `inSeason.length ? inSeason : pool` · 無 `fallback=[...pool]`

## Ship

- feature：`bc49d5e95e00` (`bc49d5e95e000fe625362588f3c68bfec14dba3a`)
- URL：https://joinkidshk-glitch.github.io/linji-chutoutian-web-preview/?v=18k
- Soft≠PASS · 全量出圖 HOLD
