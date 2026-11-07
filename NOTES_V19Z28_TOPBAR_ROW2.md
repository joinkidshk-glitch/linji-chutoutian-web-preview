# v19z28 — 頂欄次列合併＋「顯示全部地點」右緣對齊

Branch `fix/playtest-topbar-row2-v19z28`. Follows merged `v19z27` (`d7d2ad0` / #77).

用戶：頂欄可再好；下一步合併次列成一行細字，並把「顯示全部地點」對齊頂欄右緣、減浮掣感。

## Fix（純 chrome）

| 項 | 做法 |
|----|------|
| 次列 | 合併成一行：`聲量N · 1988春 · 信用N`（`.dual-compact`）；保留 `#c-stage-volume`／`#c-era`／`#c-industry-credit` |
| 季節 | `paintBar` 年份＋季節無空格（`1988春`） |
| 色塊 | 次列 swatch 隱藏（主列不變） |
| 主列 | 不變：左 阿偉｜$金額；右 事態（淡／亮）｜☰；`margin-left:auto !important` |
| 顯示全部地點 | `.map-focus-bar` 右 padding **10px** 對齊頂欄；透底、細邊、24px 高，減浮掣感；圖例 `top:28px` |

## Cache bust

`?v=19z27` → `?v=19z28`（index.html assets／tutorial／locs／era stems）

## Out of scope

- 經濟／事態／Gate／手帳邏輯
- 重繪 `hud_shell_bar.png`
- 主列再改排版

## Soft≠PASS

純 CSS／markup／era 顯示字串；唔改 BehaviorGate／soft flag。

## Verify

`https://joinkidshk-glitch.github.io/linji-chutoutian-web-preview/?v=19z28&softBehaviorGate=1`（硬重整）

1. ~390px：主列左「阿偉｜$…」、右「事態｜☰」
2. 次列一行「聲量5 · 1988春 · 信用10」（無色塊、無「幕前／業內」長標）
3. 「顯示全部地點」右緣與頂欄右側齊；掣比前版細／淡
4. 事態淡亮、金額更新、☰ 正常
