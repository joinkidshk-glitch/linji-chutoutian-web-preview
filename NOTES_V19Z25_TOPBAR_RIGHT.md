# v19z25 — 頂欄右靠（事態｜☰）

Branch `fix/playtest-topbar-right-v19z25`. Follows merged `v19z24` (`7b5598e` / #74).

用戶回饋：扁平頂欄已可接受，但「事態①｜☰」想靠右；「阿偉」同存款留左。

## Fix（純 chrome）

| 項 | 做法 |
|----|------|
| 主列佈局 | 左：阿偉｜存款；右：事態｜☰（`bar-tools { margin-left:auto }`） |
| 存款 | 取消 `margin-left:auto`；貼「阿偉」左側群組 |
| 事態／☰ | 成簇靠右；間距同 z24（gap 4）；仍扁平透明 pill／細金邊 |
| 色塊／底 | 沿用 z23／z24 扁平共用底；**無**灰板 |
| 次列 | 不變：聲量｜季節｜信用 |

## Cache bust

`?v=19z24` → `?v=19z25`（index.html assets／tutorial／locs／era stems）

## Out of scope

- 經濟／事態／Gate／手帳邏輯
- 省略「存款」二字、淡事態、次列合併（另議）
- 重繪 `hud_shell_bar.png`

## Soft≠PASS

純 CSS／markup 節奏；唔改 BehaviorGate／soft flag。

## Verify

`https://joinkidshk-glitch.github.io/linji-chutoutian-web-preview/?v=19z25&softBehaviorGate=1`（硬重整）

1. ~390px：主列左「阿偉｜存款」，右「事態｜☰」；中間留空
2. 無灰板；事態＝細透明 pill；☰ 同高
3. 次列聲量／季節／信用不變
4. 事態 chip 可開；☰ 選單正常
5. 回歸：v19z19–z24 傾談／sheet／地圖針／對白下一句
