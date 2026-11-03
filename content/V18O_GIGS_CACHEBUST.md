# V18O_GIGS_CACHEBUST

**SAVE：** `starVolunteer_map_v18o`  
**時間：** 2026-11-03（Asia/Hong_Kong）  
**預覽：** `joinkidshk-glitch/linji-chutoutian-web-preview`  
**HOLD：** Soft≠PASS；全量出圖未開；唔 publish

## 做咗咩

| # | 項 | 做法 |
|---|---|---|
| 1 | **content/* cache-bust** | `refreshCopyPacksFromDisk`：`fetch(content/X?v=SAVE)`；SAVE bump 即 bust 全 pack（含 gigs） |
| 2 | SAVE | `…_v18n` → `starVolunteer_map_v18o` |
| 3 | gigs JSON | **無改**；仍 LIVE 2.3.0／SHA16 `c58ccfa828e8ecf5`／n=52 |

## 背景（tester v18n nit）

唔 hard refresh 會 cache 舊 `gigs_1988.json`（35／空板）；refresh 後 console `[WIRING] gigs 52`。

## Tester 覆測（清 SAVE 或硬 refresh 一次後再測）

1. `?v=18o`；SAVE=`starVolunteer_map_v18o`
2. Network：`gigs_1988.json?v=starVolunteer_map_v18o`（或同等 bust）
3. 再開／跳板唔硬 refresh → 仍應見 52／海港春有板（唔應回 35）
4. Soft≠PASS

## curl-verify

- SAVE=`starVolunteer_map_v18o`
- get 行含 `?v="+bust`／bust←SAVE
- gigs 內容仍：version 2.3.0 · sha16 `c58ccfa828e8ecf5` · n=52

## Ship

- feature commit：`5d2755b00a1b` (`5d2755b00a1b04dee3a45223e2c356e783e6b55b`)
- tip／NOTES：`52cb10538d24` (`52cb10538d249371e42b36d015b422c861ebefb2`)
- URL：https://joinkidshk-glitch.github.io/linji-chutoutian-web-preview/?v=18o
- Soft≠PASS · 全量出圖 HOLD
