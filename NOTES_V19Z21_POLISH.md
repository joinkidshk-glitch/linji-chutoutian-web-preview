# v19z21 — 沉浸式 P2 打磨（對白 · 地圖針 · 手帳 · 頂欄）

Branch `fix/playtest-polish-v19z21`. Follows merged `v19z20` (`fa82aa4`).

目標：減少搶點／錯標／視覺嘈雜，令事態對白同地圖層次更乾淨。

## Changes

| # | Item | What |
|---|------|------|
| 1 | 單一「下一句」 | `.story-play .sp-actions` **display:none**；內層按鈕隱藏。唯一主 CTA 係 `#modal-btns`「下一句」（v19z12 B1 路徑）。 |
| 2 | 事態播放鎖背景針 | 強化 `#app.story-play-lock`：`.pin`／`.pin-img`／`#map-pins`／`#map-area-list`／「顯示全部地點」`pointer-events:none`。`setStoryPlayLock(true)` 再清針 inline pointer-events，防搶「下一句」。 |
| 3 | 閒置針再淡＋減標籤 | `.pin.idle` opacity **.2**／更高 grayscale；**預設隱藏** `.plab`（唔顯示全部時）。開「顯示全部地點」先出標籤。 |
| 4 | 手帳唯讀同步 | 新增 `planCatForId`；`renderNotebook`／點日／`enterHome` 令右欄分類跟左列當日安排一致——唔再「休息睡覺」列對住「到處逛逛」選項。可編輯時點日亦跟分類；之後可手動轉 tab 改行程。 |
| 5 | 頂欄角色名 | `.bar .who`：`flex:0 0 auto`、`min-width:2.6em`、取消 `max-width:28%` ellipsis；dual-hud 先收縮。 |
| 6 | Cache bust | `?v=19z20` → `?v=19z21` |

## Out of scope

- 新功能、經濟再調、BehaviorGate／soft flag、無關重構

## Soft≠PASS

- 唔改 soft BehaviorGate parsers／`featureFlag_softBehaviorGatePreview`／`gatePath`
- 純 UI／pointer／手帳顯示同步

## Verify

`https://joinkidshk-glitch.github.io/linji-chutoutian-web-preview/?v=19z21&softBehaviorGate=1`（硬重整）

1. 播事態對白：畫面底部**只有一粒**「下一句」（唔見內層再一粒）；播緊對白時點地圖針／底欄地點 → 唔開 sheet、唔搶點
2. 地圖預設：閒置針好淡、**冇地名標籤**；有事做／事態針仍亮有「劇」；撳「顯示全部地點」先見閒置標籤
3. 手帳唯讀：點「休息睡覺」日 → 右欄自動喺「休息」分類並 highlight「休息睡覺」（唔停喺「到處逛逛」）
4. 頂欄「阿偉」完整可見（唔截成「阿…」）
5. 回歸：v19z19／z20 傾談／sheet CTA／早期生活費／事態進度底欄仍在
