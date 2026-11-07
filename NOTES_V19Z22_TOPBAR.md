# v19z22 — 頂欄兩行（防 390px 重疊）

Branch `fix/playtest-topbar-v19z22`. Follows merged `v19z21` (`fe7ecfb`).

用戶截圖：阿偉＋幕前聲量＋1988春＋存款＋業內信用＋事態＋☰ 全塞一行，字重疊／亂。

## Layout（phone `#app` max-width 390px）

兩行頂欄，保留 1988 金／深褐 physical HUD：

| Row | Contents | Priority |
|-----|----------|----------|
| **主列** `.bar-primary` | **阿偉** \| **存款** \| **事態** \| **☰** | 常看／常點 |
| **次列** `.bar-secondary` `#map-dual-hud` | 幕前聲量 \| 1988 春 \| 業內信用 | 降一層；細字＋金線分隔 |

- `.bar` → `flex-direction:column`
- 存款移出 dual-hud 進主列（`#c-money`／`#c-money-wrap` id 不變 → `refreshMoneyHud`／`paintBar` 唔改邏輯）
- 名唔再 ellipsis；事態 chip／選單釘右
- Toast under map bar：`top` 56→72px（兩行較高）

## Cache bust

`?v=19z21` → `?v=19z22`（index.html assets／tutorial／locs／era stems）

## Out of scope

- 經濟／事態／Gate／手帳邏輯
- 新功能、重構 dual-track 數值映射

## Soft≠PASS

純 chrome／CSS／markup；唔改 BehaviorGate／soft flag。

## Verify

`https://joinkidshk-glitch.github.io/linji-chutoutian-web-preview/?v=19z22&softBehaviorGate=1`（硬重整）

1. ~390px：頂欄**兩行**，字**唔重疊**；「阿偉」完整
2. 主列見存款＋事態＋☰；次列見聲量／季節／信用
3. 存款數字仍跟 `paintBar`／消費更新
4. 事態 chip 可開；☰ 選單正常
5. 回歸：v19z19–z21 傾談／sheet／地圖針／對白下一句
