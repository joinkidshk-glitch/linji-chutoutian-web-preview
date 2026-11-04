> Soft≠PASS｜鄧線 push1+ Soft 計劃｜**沿 Soft A｜唔使再開 A/B**｜經 qwen3.7-max｜對白 DeepSeek｜唔 tip LIVE｜出圖 HOLD｜89–92 HOLD
>
> 母 PLAN `PLAN_STORY_DENG_LINE_SOFT_v1.md` SHA8 `043a70ff`｜meet Mock SHA8 `8a80d7b9`｜本包 Mock SHA8 `9e5751a4`

# PLAN_STORY_DENG_LINE_PUSH_SOFT_v1.md（鄧麗萍可選攻略線 push1+ Soft）

## 1. 範圍與定位
- **定位**：鄧麗萍可選攻略線（院線排片）之 **push1_plus** Soft／Mock——解 HOLD 並加厚正文。
- **範圍**：`R_tang_push1`／`R_tang_push2`／`R_tang_crisis`／`R_tang_ending`。
- **meet**：引用 parentSha8=`8a80d7b9`（`MOCK_STORY_DENG_LINE_MEET_SOFT_v1.1.json`）；**唔重做 meet 正文**。
- **母計劃**：`PLAN_STORY_DENG_LINE_SOFT_v1.md`（SHA8 `043a70ff`）；Soft A 開線閘／threshold **唔重開**。
- **實裝狀態**：僅 Soft／Mock；**唔 tip LIVE**；唔改 LIVE JSON；唔改行為閘 LIVE week-gate。

## 2. Soft A/B（**唔使／沿 Soft A**）
- **結論**：**唔使**再開 Soft A/B；沿 Soft A。
- **理由**：
  1. OUTSTANDING 已標鄧 push1+ Soft A/B＝唔使。
  2. 開線閘（C5＋favorMin≥1@agency_ho）、`rel_tang_threshold=2`、chrome 季節 Soft A（A1／A2）均已鎖。
  3. 今次範圍寫死為全套 push1+（非「只做 push1–2 vs 全線」決策點）；無新深度／門檻決策。
- **建議交統籌**：**唔使 Soft A/B**（沿 Soft A；抽樣正文即可）。

## 3. 繼承鎖（寫死）
| 項 | 值 |
|---|---|
| 開線閘 | C5 完成＋`favorMin≥1` @`agency_ho`（繼承；本檔唔重開） |
| meet | parentSha8=`8a80d7b9`；本包 REFERENCE_ONLY |
| push+ openConditions | `flag_tang_open` ∧ `rel_tang≥2` |
| `rel_tang_threshold` | **2**（不變） |
| chrome playerMeta | `主線 · 1988{季}`；季節來源 seed.season／softSeasonOverride 優先 |
| 角色 | 玩家面「鄧麗萍」；id `tang_laiping`；經理人「何生」；禁「Ho 哥」／真藝名 |
| 平行 | 唔搶曉晴／采兒必經；關海媚唔升格 |

## 4. 節拍表（加厚規格）

| beatId | 類型 | when／setting | chromeSeason／playerMeta | openConditions | choices（id＋效果） | 衝突 | synopsis（阿偉） |
|---|---|---|---|---|---|---|---|
| `R_tang_push1` | push | 冬季深夜｜票房中控室（入座數字／午夜場報告） | winter／主線 · 1988冬 | flag_tang_open ∧ rel_tang≥2 | `C_tang_push1_exchange`→flag_tang_push1_exchange, rel+1<br>`C_tang_push1_prove`→flag_tang_push1_prove, rel+1 | 冷門檔期風險 vs 數據回報 | 雙方交換試映情報同冷門檔資料；她第一次主動問跨區口碑走勢。 |
| `R_tang_push2` | push | 春季午夜場後｜戲院後巷茶餐廳 | spring／主線 · 1988春 | 同上 | `C_tang_push2_business`→flag_tang_push2_business, rel+1<br>`C_tang_push2_private`→flag_tang_push2_private, rel+1 | 純商業 vs 私人試探 | 黃金檔試水對數；她提起舊文藝片蝕本往事；可繼續商業或問私人。 |
| `R_tang_crisis` | crisis | 秋季｜院線總部會議室（兩份搶黃金檔建議書） | autumn／主線 · 1988秋 | 同上 | `C_tang_crisis_data`／`favor`／`middle`→各對應 flag, rel+1 | 檔期數據 vs 人情 | 對手片搶檔；阿偉人情片爭同一位；鄧麗萍被上頭壓住要交數。 |
| `R_tang_ending` | ending | 年終檢討後｜半暗走廊＋空戲院 | winter／主線 · 1988冬 | 同上 | `C_tang_ending_he`→flag_tang_commit+flag_tang_he, rel+3, standing+1<br>`C_tang_ending_be`→flag_tang_be, rel−2 | 商業盟友 vs 感情原則 | 年終增長獲認可；她要阿偉揀並肩盟友，或用感情挑戰原則。 |

### 加厚規格（每 beat）
- 對白段：**5–7**（含系統）；`pcSilent=true`（阿偉唔出對白行）。
- UI beat schema：`kind`／`speakerId`／`emotion`／`expression`／`lines`。
- emotion 枚舉：`neutral`·`calm`·`tense`·`angry`·`warm`·`tired`·`smirk`·`worried`·`soft`·`firm`。
- expression 枚舉：`default`·`smile`·`frown`·`raise_brow`·`eyes_down`·`look_aside`。
- 出圖 HOLD：`artId` 佔位；半身／環境圖唔生成。

## 5. 與母 PLAN／chrome／行為閘
- 開線前提仍掛 C5＋agency_ho favor（行為閘 C4 咬合繼承）；本包唔改 LIVE week-gate。
- chrome Soft PR#13 已合：playerMeta 跟季節；唔 tip LIVE／唔抬 ?v=。
- 人情債：crisis「人情片」可輕掛主線人情，唔改主線核心數值（Soft／Mock only）。
- rival_gao 唔混入鄧線。

## 6. Out of Scope
- tip LIVE；抬 ?v=；改 LIVE gigs／story JSON；改行為閘 LIVE week-gate
- 出圖；89–92 深時代事件字眼
- 重做 meet；重開開線閘／改 threshold
- 關海媚升格；搶曉晴／采兒必經
- Soft＝PASS 宣稱

## 7. Acceptance Checklist
- [x] 四節拍齊＋choices／effects／flags 對齊母 PLAN
- [x] openConditions＝flag_tang_open ∧ rel_tang≥2；threshold=2 不變
- [x] 玩家面無真藝名／無 Ho 哥／無 nextHint（bannedScanHits=[]）
- [x] 禁 89–92 深時代；出圖 HOLD；tipForbidden
- [x] qwen3.7-max 用於計劃／骨架；DeepSeek 用於對白（meta.models）
- [x] content＋store SHA 一致（組裝後核對）
- [x] Soft≠PASS
- [x] Soft A/B＝唔使／沿 Soft A

## 8. Mock 交付檔
- `MOCK_STORY_DENG_LINE_PUSH_SOFT_v1.json`（SHA8 `9e5751a4`）
- `MOCK_STORY_DENG_LINE_PUSH_SOFT_v1.md`

## 9. 模型備註
- 計劃／結構／synopsis／setting／choices 骨架：`qwen3.7-max`（DashScope token-plan SE）
- 玩家面對白／label 潤稿：`deepseek-chat`（香港書面語）
- Soft≠PASS｜唔 tip LIVE

---
*DEV：未來實裝加 `"dev_only": true`／`"deng_line_soft_push": true`。玩家面禁舊稱謂／真藝名。*
