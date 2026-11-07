# v19z29 — 次列明顯 muted 一行＋「全部地點」入頂欄

Branch `fix/playtest-topbar-all-locs-v19z29`. Follows merged `v19z28` (`3ea3660` / #78).

用戶：`v19z28` 睇唔出分別。核對 live `index.html`：次列 **早已** 係 `.dual-compact` 一行（唔係三欄）；但「顯示全部地點」仍浮喺 `.map-focus-bar`（地圖上），只改咗 padding／透明度，手機幾乎無感。

## Fix（純 chrome）

| 項 | 做法 |
|----|------|
| 核對 | 確認 z28 次列已係一行 mid-dot；問題係「顯示全部」仍浮地圖 |
| 次列 | 同一 muted 色階（標籤／數字／季節同色），更明顯讀成一條：`聲量N · 1988春 · 信用N` |
| 掣 | 文案 **「顯示全部地點」→「全部地點」**（開掣後 **「只亮有事」**） |
| 位置 | `#map-show-all-locs` **移入** `#map-bar` `.bar-secondary` 右緣（對齊 ☰）；舊 `.map-focus-bar` 隱藏 |
| 圖例 | `map-legend` top 由 28px → 8px（地圖頂唔再留浮掣空位） |

## Cache bust

`?v=19z28` → `?v=19z29`

## Out of scope

- 經濟／事態／Gate／手帳邏輯
- 主列再改排版

## Soft≠PASS

純 CSS／markup／掣文案；唔改 BehaviorGate／soft flag。

## Verify

`https://joinkidshk-glitch.github.io/linji-chutoutian-web-preview/?v=19z29&softBehaviorGate=1`（硬重整）

**相對 z28 應見到：**

1. 地圖頂 **再無**「顯示全部地點」浮掣
2. 頂欄第二行右側出現短掣 **「全部地點」**（同 ☰ 右緣齊）
3. 第二行字更淡、像一條連續細字（唔似三欄）
