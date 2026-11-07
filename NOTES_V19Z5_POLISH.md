# v19z5 — playtest polish（v19z4 煙測輕微項）

Branch `fix/playtest-polish-v19z5`. Three minor smokes from official `?v=19z4`.

## Root causes & fixes

| # | Smoke nit | Root cause | Fix |
|---|-----------|------------|-----|
| 1 | 週結旁白黏住 `−$ 2,120第1週完…` | 生活費曾以 `apply({money:-paid})` 的 `<span class="bad">−$ …</span>` 與旁白同一 `notes.join`；v19z4 已丟棄 return，但仍可能殘留／視覺黏連 | `stripSettleMoneyNoise` 清旁白金額 span；`settle-block`（淨結餘＋生活費次行）與 `.settle-flavor` 旁白分欄；里程碑獎金入帳但不把 ±$ 大字塞入旁白 |
| 2 | 傾談解鎖後庫存空仍標「未開放」 | CTA badge 一律 `gate.ok?cost:"未開放"`，庫存空／今日已送也算唔 ok | `giftGateBadge`：庫存空→「庫存空」、今日額滿→「今日已送」；「未開放」只用於真正未解鎖 |
| 3 | 選單「返屋企」有時唔完日 | `data-m=home` 只 `enterHome(null,false)`，地圖自由日唔 `tickDay`，看似 no-op | `goHomeFromMenu`／`endBrowseDayGoHome`：地圖自由日走休息式完日（寫 `rest`＋`tickDay`＋日結 modal）；已在手帳／事態中／非自由日唔亂過日 |

## Cache

`?v=19z4` → `?v=19z5`

## Verify

`https://joinkidshk-glitch.github.io/linji-chutoutian-web-preview/?v=19z5&softBehaviorGate=1`

1. 週結展開：主數字＝本週淨結餘；旁白「第N週…」前無 `−$ …` 黏字；生活費只在次行
2. 傾談林曉晴後、庫存空 → 送禮 badge＝「庫存空」（唔係「未開放」）；未傾談仍＝「未開放」
3. 地圖自由日開選單「返屋企」→ 日出「返屋企歇一日」結算並過日（等同休息路徑）
