Soft≠PASS｜Pack favor／rumor 收斂｜1988 only｜version **3.2.5-soft**｜SHA `0390b091`｜對照 pre `3.2.4-soft`｜經 qwen3.7-max｜唔 tip LIVE｜出圖 HOLD｜89–92 HOLD｜鄧 push1+ HOLD｜0 新槽 n=137

# CHANGELOG_GIGS_1988_3_2_5_SOFT

## 摘要
按統籌「選填收齊」：填餘 **21** 則初階空 `favorDelta`／`rumorKeys`（原 Soft A 1A 刻意留空）→ Soft **3.2.5-soft**。

| 項 | 前（3.2.4-soft） | 後（3.2.5-soft） |
|---|---|---|
| n | 137 | **137**（0 新槽） |
| `favorDelta` nonempty | 116 | **137** |
| `rumorKeys` nonempty | 116 | **137** |
| unique rumorKeys | 16 | **16**（≥16） |
| 初階 `agency_ho` | 0 | **0**（禁） |
| softStatus | ≠PASS | **≠PASS** |

## 改動範圍
1. **餘 21 初階**：每則 `favorDelta=[{target:crew_{loc}, value:1}]`、`rumorKeys` 恰 1 條（沿用既有 16 keys；季節傾向）。
2. **meta**：version→3.2.5-soft；counts.withFavorDelta／withRumorKeys→137。

## 明確未改
- 唔改：`pay*`／`req`／`loc`／`season`／`tier`／文案／`isKeyGig`／`boardHookMode`／`storyKeys`／高階 favor
- 唔 tip LIVE；出圖 HOLD；89–92 HOLD；鄧 push1+ HOLD
- Soft A/B：唔使

## 產物
| 檔 | SHA8 |
|---|---|
| gigs_1988.json／gigs_1988_3.2.5-soft.json | `0390b091` |
| PATCH_GIGS_1988_FAVOR_RUMOR_REMAIN21_v1.json | （見交付表） |
| pre backup | `0f18fe14` |

## 時間
Asia/Hong_Kong 2026-11-04 約 23:30
