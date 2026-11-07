# v19z24 — 頂欄收緊（扁平後再密）

Branch `fix/playtest-topbar-tight-v19z24`. Follows merged `v19z23` (`70a74d3` / #73).

用戶回饋：扁平頂欄已有改進，但第一行左右仍疏、存款同事態／☰ 可再貼；第二行字級／對齊想再穩。

## Fix（純 chrome）

| 項 | 做法 |
|----|------|
| 外框 | `.bar` padding `8/12/7` → `6/10/5`；兩行 gap `4` → `2` |
| 主列 | `.bar-primary` gap `8` → `4`；存款↔事態／☰ 更貼 |
| 事態↔☰ | `.bar-tools` gap `6` → `4`；chip 左右 padding `8` → `7` |
| 存款 | 標籤／數字 gap `4` → `3`；數字 `tabular-nums` |
| 次列 | 固定高 18px；聲量／季節／信用統一 `.6rem`＋16px line-height；左右轨 `flex:1` 對齊、季節置中 |
| 色塊 | swatch 略細 `7×10`；仍扁平共用底，**無**灰板 |
| Toast | `top` 68→64px（欄略矮） |

## Cache bust

`?v=19z23` → `?v=19z24`（index.html assets／tutorial／locs／era stems）

## Out of scope

- 經濟／事態／Gate／手帳邏輯
- 重繪 `hud_shell_bar.png`
- 新功能、改兩行資訊層級

## Soft≠PASS

純 CSS／markup 節奏；唔改 BehaviorGate／soft flag。

## Verify

`https://joinkidshk-glitch.github.io/linji-chutoutian-web-preview/?v=19z24&softBehaviorGate=1`（硬重整）

1. ~390px：頂欄兩行；**無**灰板；「阿偉」完整
2. 主列：存款更貼事態／☰；事態貼 ☰；左右 padding 較 z23 窄
3. 次列：幕前聲量／1988 春／業內信用同一字級、同一行高、左右對稱
4. 事態 chip 可開；☰ 選單正常
5. 回歸：v19z19–z23 傾談／sheet／地圖針／對白下一句
