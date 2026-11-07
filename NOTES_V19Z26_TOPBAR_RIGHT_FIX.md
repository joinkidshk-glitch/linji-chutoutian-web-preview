# v19z26 — 頂欄右靠加固（事態｜☰）

Branch `fix/playtest-topbar-right-fix-v19z26`. Follows merged `v19z25` (`37f86a0` / #75).

## 問題

用戶回饋「事態①｜☰」仍未靠右。根因：較早規則 `.bar-primary .bar-tools{margin-left:0}`／`.bar .bar-tools{margin-left:0 !important}` 會把右側簇壓返左邊；Pages 亦曾仍派舊 chrome。v19z25 已改 `auto`，本包再加固選擇器同 cache bust，確保任何後規則都唔再把 `margin-left` 清零。

## Fix（純 chrome）

| 項 | 做法 |
|----|------|
| 主列 | 左：阿偉｜存款；右：事態｜☰ |
| `.bar-tools` | `.bar .bar-tools, .bar .bar-primary .bar-tools { margin-left:auto !important }`；`flex:0 0 auto !important`；`justify-content:flex-end` |
| 存款 | 維持 `margin-left:0 !important`（唔搶右） |
| 事態 chip | `.on` 先顯示；唔改邏輯 |
| 灰板 | 無 |

## Cache bust

`?v=19z25` → `?v=19z26`（index.html assets／tutorial／locs／era stems）

## Out of scope

- 經濟／事態／Gate／手帳邏輯
- 省略「存款」二字、淡事態、次列合併
- 重繪 `hud_shell_bar.png`

## Soft≠PASS

純 CSS／cache；唔改 BehaviorGate／soft flag。

## Verify

`https://joinkidshk-glitch.github.io/linji-chutoutian-web-preview/?v=19z26&softBehaviorGate=1`（硬重整）

1. ~390px：主列左「阿偉｜存款」，右「事態｜☰」；中間留空
2. 本地 CSS 檢查：無後規則把 `.bar-tools` 的 `margin-left` 設為 `0`
3. 事態 `.on` 可見；☰ 選單正常
4. 次列聲量／季節／信用不變
