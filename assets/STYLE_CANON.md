# 《臨記出頭天》visual style canon（GD）

正式遊戲名：**臨記出頭天**

## 角色肖像／bust（硬規則 · 2026-11-05 用戶確認）

**唯一準繩**：`assets/hero_awi.jpg` ＋ `assets/story/c1/char_hero_bust_default.png`

- **平面動畫／視覺小說立繪**：清晰黑線、cel-shade 硬邊陰影、大而有神的眼睛、簡化鼻線
- **禁止**：半寫實、相片感皮膚紋理、細密髮絲、寫實光影漸變（曾出錯：`char_hero_bust_raise_brow` HOLD-redo v3）
- 之後所有角色 bust／半身表情變體一律跟阿偉 default 同一套線條密度與上色，唔另開 stylized 或寫實線

## 用戶確認（沿用）

1. 肖像／立繪跟 `hero_awi.jpg`／現有人脈 NPC（含何生）——唔整批重畫（風格對齊；偏寫實者 redo）
2. 開場圖以已嵌版本／對齊阿偉 2D 為準
3. 減網頁感 UI 包：`ui-physical/`（見 UI_PHYSICAL_CANON.md）
4. 之後新圖／logo／標題字一律用 **臨記出頭天**，畫風跟阿偉立繪

誤修備份：`_style_bak/`

## Style-lock CORE redo（2026-11-05 Asia/Hong_Kong）

- 已 redo：`story/core/{vera,chow_choiyi,ko_chunkit,tang_laiping,lin_hiu,lui_ging}_bust_{default,smile,frown}.png`（18）
- Refs：`hero_awi.jpg`＋`story/c1/char_hero_bust_default.png`（＋npc identity when present）
- 本 Soft tip 只合 live 18 PNG（bak 省略，GD 允許）；`?v=` 仍 `19w`
- Soft≠PASS；唔 tip LIVE；89–92 HOLD；silhouettes 後掛

## Style-lock Cheung pair（2026-11-05 Asia/Hong_Kong）

- 已 redo：`char_cheung_bust_default.png` MD5 `920321c6`、`char_cheung_bust_raise_brow.png` MD5 `5224f3dc`（c1／story／dialog／npc 四路同 MD5）
- LOOKS：粗黑框眼鏡、卡其多口袋攝影背心、洗水牛仔恤、聽筒。準繩仍係 `hero_awi.jpg`＋`char_hero_bust_default.png`
- bak：`assets/story/c1/char_cheung_bust_{default,raise_brow}_pre_style_lock_bak.png`（舊高領半寫實）
- 身份 jpg `assets/npc_cheung.jpg` 仍係高領較年長記帳，本輪唔改
- Soft≠PASS；唔 tip LIVE；`?v=` 仍 `19w`；89–92 HOLD；silhouettes 後掛

## Style-lock ERA_STARS redo（2026-11-05 Asia/Hong_Kong）

- 已 redo：`story/era_stars/{luk_baakyin,yip_manji,so_jiyan,liu_bingxing,ngai_wingnaam}_bust_{default,smile,frown}.png`（15）
- Refs：`hero_awi.jpg`＋`story/c1/char_hero_bust_default.png`
- 本 Soft tip 只合 live 15 PNG（bak 留盤、唔入本 PR）
- silhouettes **未動**（本 repo 無 `*_silhouette_*`，亦唔加）。遠觀仍純文字
- Soft≠PASS；唔 tip LIVE；`?v=` 仍 `19w`；89–92 HOLD
