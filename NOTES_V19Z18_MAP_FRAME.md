# v19z18 — 地圖黃色拍立得邊框太粗

Branch `fix/playtest-map-frame-v19z18`. Follows merged map UX（`v19z17`）。

玩測回饋：大地圖外圈 cream／黃色 polaroid mat（`map_polaroid_frame.png`／`--phys-polaroid`）邊框太粗，搶視線。

## 改動

| # | Issue | Fix |
|---|-------|-----|
| 1 | 厚 cream polaroid 框圍住衛星地圖 | `.map-polaroid`：**唔再畫** `background: var(--phys-polaroid)`；`padding:0`（取消 contentRectNorm 厚 mat） |
| 2 | 邊緣仍要有輕微分隔 | 只留 **1px** 浅金線（`rgba(201,162,39,.42)`）+ 細圓角；唔再係厚 cream mat |
| 3 | 相井外露 | `.map-well` overflow hidden；`.map-wrap` 暗底，避免 cream 滲邊 |
| 4 | Cache bust | `?v=19z17` → `?v=19z18` |

**保留**：`assets/ui-physical/map-frame/map_polaroid_frame.png` 檔案本身（可日後重用）；DOM `#map-polaroid`／`.map-well`／針／「有事做」層次（v19z17）。唔改 soft BehaviorGate parsers／`featureFlag_softBehaviorGatePreview`／`gatePath`。唔 tip LIVE。

## Soft≠PASS

- 唔改 BehaviorGate 解析器或 soft flag 預設
- 純地圖 chrome／視覺；唔改事態閘、通告 JSON、扣日規則

## Verify

`https://joinkidshk-glitch.github.io/linji-chutoutian-web-preview/?v=19z18&softBehaviorGate=1`

1. 地圖外圈**冇**厚黃色／cream polaroid 框；最多一條幼金線
2. 衛星圖幾乎貼邊填滿 `#map-polaroid` 區域
3. v19z17 回歸：冇區篩選掣；「顯示全部地點」仍在；有事做針仍亮
4. B2／B1：教學「去金龍播事態」仍可播 C1
