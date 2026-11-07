# v19z23 — 頂欄扁平（去灰板）

Branch `fix/playtest-topbar-flat-v19z23`. Follows merged `v19z22` (`17ed86d` / #72).

用戶回饋：兩行方向啱，但中間「存款／事態」像浮咗一塊灰板，蓋住第二行「1988 春」，視覺仍亂。

## Cause

1. `hud_shell_bar.png` 係單行薄板；兩行高度用 `center/cover` 會把中間深灰凹槽＋兩側 tally 撐成浮層。
2. 全域 `.chip { background: rgba(42,36,30,.82) }` 令「事態」再疊一塊不透明灰 pill。

## Fix（純 chrome）

| 項 | 做法 |
|----|------|
| 共用底 | `.bar` 改扁平 `linear-gradient(180deg,#4a433c,#2E2A26)`；唔再貼 stretched `phys-hud-bar` |
| 存款 | 主列純金字＋標籤；透明底／無邊／無陰影；高 28px 同「阿偉」 |
| 事態 | 透明底＋細金邊 pill；高 28px；數字橙點保留；仍靠 `.on` 顯示 |
| ☰ | 同高 28px、透明底＋細金邊，同事態一個系統 |
| 兩行 | 保留：主列 阿偉 · 存款 · 事態 · ☰；次列 聲量／季節／信用 |
| Toast | `top` 72→68px（略扁） |

## Cache bust

`?v=19z22` → `?v=19z23`（index.html assets／tutorial／locs／era stems）

## Out of scope

- 經濟／事態／Gate／手帳邏輯
- 重繪 `hud_shell_bar.png` 資產
- 新功能

## Soft≠PASS

純 CSS／markup 節奏；唔改 BehaviorGate／soft flag。

## Verify

`https://joinkidshk-glitch.github.io/linji-chutoutian-web-preview/?v=19z23&softBehaviorGate=1`（硬重整）

1. ~390px：頂欄兩行；**無**中間浮灰板；「1988 春」唔被蓋
2. 存款＝純金字；事態＝細透明 pill（有事時）；☰ 同高
3. 字唔重疊；「阿偉」完整
4. 事態 chip 可開；☰ 選單正常
5. 回歸：v19z19–z22 傾談／sheet／地圖針／對白下一句
