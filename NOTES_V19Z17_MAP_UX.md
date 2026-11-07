# v19z17 — 大地圖 UX：拎走區篩選 +「有事做」針強調

Branch `fix/playtest-map-ux-v19z17`. Follows merged B1／B3（`v19z16`）。

## 改動

| # | Issue | Fix |
|---|-------|-----|
| 1 | 區篩選「全部／新界／九龍／港島」搶視線、對新手唔友善 | **移除** `#region-tabs` DOM；舊 CSS 用 `.region-tabs{display:none}` 兜底；地圖永遠顯示全區 |
| 2 | 針又密又大，分唔清邊啲有事做 | 有通告／事態／熟人 → `.has-action` 全亮；其餘 → `.idle.dim` 淡化＋細針 |
| 3 | 探索仍要搵「冇事做」地點 | 頂右細掣「顯示全部地點」⇄「只亮有事做」（`mapShowAllLocs`） |
| 4 | 底欄快捷列跟區篩會變短 | 預設只列「有事做」地點（有事做排前）；開「顯示全部」先列齊；保留 `#map-area-list` |
| 5 | 近針重疊 | Cluster 扇形半徑略加大（3.8＋）；點擊近距時優先揀有事做針 |
| 6 | Cache bust | `?v=19z16` → `?v=19z17` |

**保留**：底欄快捷列表本體、圖例、地圖底圖、`region` 資料欄（給文案／`regionLabel`）、`scout_*` 行程 id。唔改 soft BehaviorGate parsers／`featureFlag_softBehaviorGatePreview`／`gatePath`。唔 tip LIVE。

## Soft≠PASS

- 唔改 BehaviorGate 解析器或 soft flag 預設
- 純地圖 UX／視覺層次；唔改事態閘、通告 JSON、扣日規則

## Verify

`https://joinkidshk-glitch.github.io/linji-chutoutian-web-preview/?v=19z17&softBehaviorGate=1`

1. 地圖頂**冇**「全部／新界／九龍／港島」四掣；改見右上「顯示全部地點」
2. 新局／有事態或通告時：金龍／有通告公司針明顯；閒置針淡＋細
3. 撳「顯示全部地點」→ 閒置針變清楚；掣文案變「只亮有事做」
4. 底欄快捷：預設多係有事做地點；開全部後列出更多
5. 撳淡針仍可開地點 sheet（唔鎖旅遊）
6. B2／B1 回歸：教學「去金龍播事態（會用預設行程）」仍可播 C1
