# V18J_CHOICE_UX

**SAVE：** `starVolunteer_map_v18j`  
**時間：** 2026-11-03（Asia/Hong_Kong）  
**預覽：** `joinkidshk-glitch/linji-chutoutian-web-preview`  
**HOLD：** Soft≠PASS；全量出圖未開

## 做咗咩

| # | 項 | 做法 |
|---|---|---|
| 1 | **Choices 底圖** | choices 分支改 `spChoiceBgClass`／`spChoiceBgCandidates`：跟最後 beat `bg`／`locId` → node.locId；C1 優先 `bg_c1_tea_restaurant`；另試 `artId`／`story_c1_pack_preview`。寫入 `data-sp-bg-fallbacks` 俾 `__spApplyBgPhotos` |
| 2 | **Stage 高度** | `.sp-mode-choices` min-height ~180／height 200（唔再用 max-height:120 灰條） |
| 3 | **玩家 meta** | `spPlayerMeta`：C1／forced → **「主線 · 1988春」**（用戶拍板）；唔再顯示 `C主線`／裸 `P1` |
| 4 | **Forced chrome** | C1（`spIsForcedStory`／`_sess.forced`）：藏 modal「先返回」；藏「跳至選項」；outside dismiss → re-render 唔 abort |
| 5 | SAVE | `…_v18i` → `starVolunteer_map_v18j` |
| 6 | 未改 | Soft≠PASS；全量出圖 HOLD；`advance`／`__spApplyBgPhotos` 保留 |
| 7 | **No double-tap zoom** | viewport `maximum-scale=1, user-scalable=no`；CSS `touch-action: manipulation` on html/body/button/a/[role=button]/.sp-* |

## Tester 覆測（清 SAVE）

1. `?v=18j` 硬 refresh；SAVE=`starVolunteer_map_v18j`
2. C1 對白／選擇頭 meta＝「主線 · 1988春」（無 C主線／P1）
3. 選擇頁 `.sp-bg-layer` 有 `data-sp-bg-fallbacks`＋實圖（茶餐廳），唔係短灰條
4. C1 無「先返回」／無「跳至選項」；要撳完對白再揀選項
5. Soft≠PASS

## curl-verify（填 ship 後）

- SAVE=`starVolunteer_map_v18j`
- HTML：`spPlayerMeta` · `主線 · 1988春` · `sp-mode-choices` · `data-sp-bg-fallbacks` · `forcedChrome` · `function advance()` · `__spApplyBgPhotos = function`

## Ship

- feature commit（choices UX）：`44bf8db5702c` (`44bf8db5702c52359f466c6373b124c585620f22`)
- anti-zoom：`63ed2c885347` (`63ed2c885347a117d35496b2c40d4a51a2960ca8`)
- tip／NOTES：`14e0eb5c2e3b` (`14e0eb5c2e3be39a6aecd14b653e1a7b629c917e`)
- URL：https://joinkidshk-glitch.github.io/linji-chutoutian-web-preview/?v=18j
- Soft≠PASS · 全量出圖 HOLD
