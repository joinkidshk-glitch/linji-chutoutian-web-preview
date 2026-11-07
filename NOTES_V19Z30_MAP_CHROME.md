# v19z30 — 地圖 chrome 收斂包（圖例 · 事態進度 · HUD／對白／閒置針）

Branch `fix/playtest-map-chrome-v19z30`. Follows merged `v19z29` (`b408059` / #79).

用戶「繼續」沉浸打磨：唔再開細 PR 逐項問 merge；一次過收齊剩餘 chrome nits（唔加新功能）。

## Changes

| # | Item | What |
|---|------|------|
| 1 | 圖例縮高 | `#map-legend`：padding／字級／icon 再收；`flex-wrap:nowrap`＋`max-height:20px`，手機少佔垂直位 |
| 2 | 事態進度條突出 | `.map-hint-story` 改金邊／左金條半透明板；字色 `#FFE7A0`、略加大。有進度時 help 行淡化減嘈。開事態文案去掉「（金框／劇針…）」括註 |
| 3 | HUD nit | `.bar-tools`／事態 chip `overflow:visible`、`flex-shrink:0`，避免右簇同 ☰ 擠走／裁切 |
| 4 | 對白單一「下一句」＋針鎖 | 再硬藏 `.sp-actions`／內層 next／skip；`story-play-lock` 擴至 polaroid／stage／legend／hint。`setStoryPlayLock`：**unlock 時還原** `#map-pins` pointer-events（先前 unlock 後父層仍 `none`） |
| 5 | 閒置針再淡 | 預設 `.pin.idle` opacity **.14**；「全部地點」時 **.52**（唔再 .78），有事做針仍 opacity 1 |
| 6 | Cache bust | `?v=19z29` → `?v=19z30` |

## Out of scope

- 新功能、經濟再調、BehaviorGate／soft flag、頂欄主列再改（維持 z29）
- 無關重構

## Soft≠PASS

純 CSS／pointer／短文案；唔改 soft parsers／`featureFlag_softBehaviorGatePreview`／`gatePath`。

## Verify

`https://joinkidshk-glitch.github.io/linji-chutoutian-web-preview/?v=19z30&softBehaviorGate=1`（硬重整）

1. 地圖頂圖例一行、高度明顯矮過 z29
2. 底欄事態進度（通告 x／3 · 第2幕即將）有金邊板，一眼見到
3. 頂欄右「事態｜☰」完整可見、唔裁
4. 播事態：只有底 `#modal-btns`「下一句」；點地圖針／polaroid 唔搶點；關事態後針可再點
5. 預設閒置針好淡；「全部地點」先略亮；有通告／情報／事態針仍醒目
