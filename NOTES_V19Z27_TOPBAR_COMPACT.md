# v19z27 — 頂欄慳位（$金額）＋事態淡亮

Branch `fix/playtest-topbar-compact-v19z27`. Follows merged `v19z26` (`28a9cae` / #76).

用戶回饋：頂欄右靠已 OK；下一步慳「存款」二字、事態無未讀時淡顯示。

## Fix（純 chrome）

| 項 | 做法 |
|----|------|
| 主列金額 | 去掉「存款」標籤；顯示 `$`＋`#c-money`（id 不變 → `refreshMoneyHud`／`paintBar` 照刷） |
| 事態 chip | **常駐**可見；無 `.on`／無未讀 → muted（opacity≈0.42、淡金邊）；有 pending → `.on` 亮＋badge |
| 佈局 | 左：阿偉｜$金額；右：事態｜☰；`bar-tools { margin-left:auto !important }` 維持 |
| 灰板 | 無 |

## Cache bust

`?v=19z26` → `?v=19z27`（index.html assets／tutorial／locs／era stems）

## Out of scope

- 經濟／事態／Gate／手帳邏輯
- 次列合併成一條細字
- 重繪 `hud_shell_bar.png`

## Soft≠PASS

純 CSS／markup／chip 顯示節奏；唔改 BehaviorGate／soft flag。

## Verify

`https://joinkidshk-glitch.github.io/linji-chutoutian-web-preview/?v=19z27&softBehaviorGate=1`（硬重整）

1. ~390px：主列左「阿偉｜$12,000」（無「存款」二字），右「事態｜☰」
2. 無可播事態時「事態」仍見但淡；有未讀時亮＋數字 badge
3. 點淡事態仍可開事態列表；☰ 正常
4. 消費／還債後金額仍即時更新
5. 右靠未回退（中間留空）
