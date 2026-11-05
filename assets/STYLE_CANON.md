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

- 已 redo：`char_cheung_bust_default.png` MD5 `920321c6`（c1／story／dialog／npc 四路同 MD5）。`char_cheung_bust_raise_brow.png` style-lock 當時 `5224f3dc`；live 見下方 Soft nit `8a8d01a9`
- LOOKS：粗黑框眼鏡、卡其多口袋攝影背心、洗水牛仔恤、聽筒。準繩仍係 `hero_awi.jpg`＋`char_hero_bust_default.png`
- bak：`assets/story/c1/char_cheung_bust_{default,raise_brow}_pre_style_lock_bak.png`（舊高領半寫實）
- 身份 jpg `assets/npc_cheung.jpg` 仍係高領較年長記帳，本輪唔改
- Soft≠PASS；唔 tip LIVE；`?v=` 仍 `19w`；89–92 HOLD；silhouettes 後掛

## Style-lock ERA_STARS redo（2026-11-05 Asia/Hong_Kong）

- 已 redo：`story/era_stars/{luk_baakyin,yip_manji,so_jiyan,liu_bingxing,ngai_wingnaam}_bust_{default,smile,frown}.png`（15）
- Refs：`hero_awi.jpg`＋`story/c1/char_hero_bust_default.png`
- 本 Soft tip 只合 live bust PNG（bak 留盤、唔入本 PR）
- silhouettes **v2 2026-11-05**：5／5 `*_silhouette_far.png` 已入 Soft。Soft gate 遠觀先顯示剪影；Soft off／LIVE 仍文字＋音。preferFile 未加 era_stars bust path。`bak_pre_silhouette_v2/` 唔入本 PR
- Soft≠PASS；唔 tip LIVE；`?v=` 仍 `19w`；89–92 HOLD

- 2026-11-05 luk leather v5b：`luk_baakyin` bust×3 改黑皮褸＋白 Tee＋正面理領（對開阿偉西裝白恤）；GenerateImage；bak `era_stars/bak_pre_luk_leather_v5/` 留盤、唔入本 PR；Soft≠PASS；唔 tip LIVE；`?v=` 仍 `19w`。

- 2026-11-05 liu chow-vibe v10：`liu_bingxing` bust×3 花恤衫正面；周星馳／吳孟達 LOOKS 氣質（禁一比一抄臉）；GenerateImage；bak `bak_pre_liu_chow_v10/` 留盤、唔入本 PR；Soft≠PASS；唔 tip LIVE；`?v=` 仍 `19w`。

- 2026-11-05 yip starlet-v3：`yip_manji` bust×3 露肩 dusty-rose；邱淑貞／張敏 LOOKS 氣質（禁抄臉）；GenerateImage；bak `bak_pre_yip_starlet_v3/` 留盤、唔入本 PR；Soft≠PASS；唔 tip LIVE；`?v=` 仍 `19w`。

- 2026-11-05 so jade-v4：`so_jiyan` bust×3 正面開襟＋碎花；周慧敏氣質（禁抄臉）；阿偉 cel-shade；GenerateImage；bak `bak_pre_so_jade_v4/` 留盤、唔入本 PR；Soft≠PASS；唔 tip LIVE；`?v=` 仍 `19w`。

- 2026-11-05 ngai kara-v5：`ngai_wingnaam` bust×3 正面理領＋navy；惠英紅氣質；低馬尾統一；style 鎖阿偉；style＋pose redo（替 kara-v2，v2 唔再係 live）；GenerateImage；bak `bak_pre_ngai_kara_v5/` 留盤、唔入本 PR；Soft≠PASS；唔 tip LIVE；`?v=` 仍 `19w`。

- 2026-11-05 era silhouettes v2：`{luk_baakyin,liu_bingxing,ngai_wingnaam,yip_manji,so_jiyan}_silhouette_far.png`；GenerateImage＋RGBA 透明底；Soft≠PASS；唔 tip LIVE；`?v=` 仍 `19w`。

- 2026-11-05 Soft nits expr：`so_jiyan_bust_smile`＋`luk_baakyin_bust_smile`＋`ngai_wingnaam` bust×3；GenerateImage；bak `era_stars/bak_pre_soft_nits_expr_20261105/` 留盤、唔入本 PR；挑眉 `char_hero_bust_raise_brow` 未入本 pack、唔動；Soft≠PASS；唔 tip LIVE；`?v=` 仍 `19w`；89–92 HOLD。

## raise_brow Soft nit（2026-11-05 Asia/Hong_Kong）

- 已換：`char_hero_bust_raise_brow.png` MD5 `59dab337`；`char_cheung_bust_raise_brow.png` MD5 `8a8d01a9`（c1／story／dialog／npc 四路同 MD5）
- 對開 style-lock：hero `63670d1b`、Cheung `5224f3dc`。bak `story/c1/bak_pre_raise_brow_soft_nit_20261105/` 留盤、唔入本 PR
- Pipeline：GenerateImage（mark-guide＋`hero_awi`／default refs）
- Soft nits（唔擋 Soft tip）：額上橫紋偏強（尤其 hero）；Cheung 挑眉峰仍可再抬
- Soft≠PASS；唔 tip LIVE；`?v=` 仍 `19w`；SAVE `starVolunteer_map_v19w`；89–92 HOLD
- Pack：`/workspace/star-volunteer-web-raise-brow-soft-nit.tar.gz`

## luk frown Soft nit（2026-11-05 Asia/Hong_Kong）

- 只換：`story/era_stars/luk_baakyin_bust_frown.png` MD5 `d379b322`。default `f0bc02d8`／smile `202a6200` 唔動（smile 來自 Soft tip #24）
- 對開舊 frown `9e134222`。bak `era_stars/bak_pre_luk_frown_soft_nit_20261105/` 留盤、唔入本 PR
- Soft nits（唔擋 Soft tip）：怒氣線可再強；眉峰 V 可再銳
- Soft≠PASS；唔 tip LIVE；`?v=` 仍 `19w`；SAVE `starVolunteer_map_v19w`；89–92 HOLD
- Pack：`/workspace/star-volunteer-web-luk-frown-soft-nit.tar.gz`
