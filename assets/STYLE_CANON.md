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
- Soft≠PASS；唔 tip LIVE；89–92 HOLD
- 2026-11-05 core／romance silhouette_far Soft×6：`story/core/{lin_hiu,chow_choiyi,vera,ko_chunkit,tang_laiping,lui_ging}_silhouette_far.png`；864×1152 RGBA 透明底近黑；Soft 遠觀先掛（`?v=19w`）；新建無 bak。唔改 era_stars 剪影。Soft≠PASS；唔 tip LIVE；89–92 HOLD

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

- 2026-11-05 era sil Soft polish×3：`{yip_manji,so_jiyan,luk_baakyin}_silhouette_far.png` redo（露肩／bare-arm、肘外＋手前、quiff↑）；`liu`／`ngai` sil 當時未動；GenerateImage 彩色全身→Pillow RGBA 近黑 `(18,18,20)`；bak `era_stars/bak_pre_silhouette_soft_polish_20261105/` 留盤、唔入本 PR；pack `/workspace/star-volunteer-web-era-sil-soft-polish.tar.gz`；Soft≠PASS；唔 tip LIVE；`?v=` 仍 `19w`；89–92 HOLD。

- 2026-11-05 ngai zip sil Soft nit：只換 `ngai_wingnaam_silhouette_far.png` MD5 `899c7f7d`（對 v2 `31555755`：高領 zip／低馬尾／理領）；liu／yip／so／luk sil 未動；864×1152 RGBA 近黑 `(18,18,20)`、無五官；bak `era_stars/bak_pre_ngai_zip_sil_soft_nit_20261105/` 留盤、唔入本 PR；遠觀 wire 仍 `?v=19w`、唔改 `index.html`；Soft nits（唔擋）：遠距可讀成連帽；理領空隙弱；無光邊；Soft≠PASS；唔 tip LIVE；89–92 HOLD。

- 2026-11-05 yip／liu smile↔default Soft nit：`yip_manji`＋`liu_bingxing` bust_{default,smile}；GenerateImage；bak `era_stars/bak_pre_yip_liu_smile_default_soft_nit_20261105/` 留盤、唔入本 PR；pack `/workspace/star-volunteer-web-yip-liu-smile-default-soft-nit.tar.gz`；yip frown 未動；Soft≠PASS；唔 tip LIVE；`?v=` 仍 `19w`；89–92 HOLD。

- 2026-11-05 liu frown Soft nit：`liu_bingxing_bust_frown` 吃癟下撇對開 default／smile（chow-vibe v10 wardrobe／cel-shade lock；default `f39379d5`／smile `3b3c7fb4` 未動；yip frown `9d7e2b8e` 未動）；GenerateImage；bak `era_stars/bak_pre_liu_frown_soft_nit_20261105/` 留盤、唔入本 PR；pack `/workspace/star-volunteer-web-liu-frown-soft-nit.tar.gz`；併入同一 Soft tip；Soft≠PASS；唔 tip LIVE；`?v=` 仍 `19w`；89–92 HOLD。

- 2026-11-05 yip energy Soft nit：`yip_manji_bust_{default,smile}` 嬌俏眨眼／咬唇能量＋smile 更暖露齒眼閃↑（starlet-v3 露肩 dusty-rose／cel-shade lock；frown `9d7e2b8e` 未動；對開 tip #30 default `b338280b`／smile `6e7b1a2b`；live MD5 `08384068`／`f1688fb4`）；GenerateImage；bak `era_stars/bak_pre_yip_energy_soft_nit_20261105/` 留盤、唔入本 PR；pack `/workspace/star-volunteer-web-yip-energy-soft-nit.tar.gz` MD5 `77ab9fa9`；Soft≠PASS；唔 tip LIVE；`?v=` 仍 `19w`；89–92 HOLD。

- 2026-11-05 so／yip frown Soft nit：`so_jiyan_bust_frown`＋`yip_manji_bust_frown`（夾眉下撇不高興／雙目睜下撇咬唇；jade-v4／starlet-v3 wardrobe／cel-shade lock；default／smile 未動；live MD5 `dbe0ce32`／`d50275e8`；舊 `f0c0347e`／`9d7e2b8e`）；GenerateImage；bak `era_stars/bak_pre_so_yip_frown_soft_nit_20261105/` 留盤、唔入本 PR；pack `/workspace/star-volunteer-web-so-yip-frown-soft-nit.tar.gz`；Soft≠PASS；唔 tip LIVE；`?v=` 仍 `19w`；89–92 HOLD。

- 2026-11-05 yip wink Soft nit：`yip_manji_bust_{default,smile}` 雙目睜＋閉唇微 smirk（收斂 energy 強 wink）／smile 露齒暖笑＋眼閃（starlet-v3 露肩 dusty-rose／cel-shade lock；frown `d50275e8` 未動；對開 energy Soft tip default `08384068`／smile `f1688fb4`；live MD5 `fe28eb9b`／`86a75894`）；GenerateImage；bak `era_stars/bak_pre_yip_wink_soft_nit_20261105/` 留盤、唔入本 PR；pack `/workspace/star-volunteer-web-yip-wink-soft-nit.tar.gz`；Soft≠PASS；唔 tip LIVE；`?v=` 仍 `19w`；89–92 HOLD。

- 2026-11-05 so／yip frown polish Soft nit：`so_jiyan_bust_frown`＋`yip_manji_bust_frown`（夾眉下撇保留、眉薄／怒感收約 5–10%；雙目睜＋咬唇嬌俏敗興↑；jade-v4／starlet-v3 wardrobe／cel-shade lock；default／smile 未動；live MD5 `4e9d521c`／`33152c22`；舊 Soft tip `dbe0ce32`／`d50275e8`；yip default／smile wink `fe28eb9b`／`86a75894` 未動）；GenerateImage；bak `era_stars/bak_pre_so_yip_frown_polish_soft_nit_20261105/` 留盤、唔入本 PR；pack `/workspace/star-volunteer-web-so-yip-frown-polish-soft-nit.tar.gz`；Soft≠PASS；唔 tip LIVE；`?v=` 仍 `19w`；89–92 HOLD。

- 2026-11-05 sil shape Soft nit：`{yip_manji,so_jiyan,luk_baakyin,ngai_wingnaam}_silhouette_far.png` redo shape（yip 肩凹清／so 叉腰手前可讀／luk quiff↑／ngai 高領 zip；live MD5 `ba8ad339`／`2602dda9`／`022489bc`／`c0f0d41e`；prior 光邊 `b29c5efc`／`30fec574`／`45d03628`／`79f2e144`）；`liu` `4bbf6e7f`／core／bust 未動；GenerateImage 彩色全身→Pillow RGBA 近黑 `(18,18,20)`＋tip#32 soft warm rim／halo；唔做 C cream-rim big redo；bak `era_stars/bak_pre_sil_shape_soft_nit_20261105/` 留盤、唔入本 PR；pack `/workspace/star-volunteer-web-sil-shape-soft-nit.tar.gz`；Soft nits（唔擋）：luk／ngai 理領空隙；ngai 連帽遠距；QC：統籌 Style PASS with nits；Soft≠PASS；唔 tip LIVE；唔抬 `?v=`；89–92 HOLD。

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

## so energy Soft nit（2026-11-05 Asia/Hong_Kong）

- 只換：`story/era_stars/so_jiyan_bust_default.png` MD5 `2cc1a570`；`so_jiyan_bust_smile.png` MD5 `e57ab12a`。frown `f0c0347e` 唔動（jade-v4 lock）
- jade-v4 wardrobe／正面／cel-shade lock（奶油開襟＋碎花）。Pipeline：GenerateImage → 864×1152 RGB
- 對開舊 default `912b8dc5`／smile `0b819961`。bak `era_stars/bak_pre_so_energy_soft_nit_20261105/` 留盤、唔入本 PR
- Soft nits（唔擋 Soft tip）：default 嘴角仍偏親切微笑（可選再收、專推眼閃）；modern polish 線密度；default NEW RGB vs bak RGBA（記帳 only）
- Soft≠PASS；唔 tip LIVE；`?v=` 仍 `19w`；SAVE `starVolunteer_map_v19w`；89–92 HOLD
- Pack：`/workspace/star-volunteer-web-so-energy-soft-nit.tar.gz`

## ngai age Soft nit（2026-11-05 Asia/Hong_Kong）

- 只換：`story/era_stars/ngai_wingnaam_bust_default.png` MD5 `09f79211`；`ngai_wingnaam_bust_smile.png` MD5 `8f1abdaf`；`ngai_wingnaam_bust_frown.png` MD5 `5df4f5fa`
- kara-v5 lock：低馬尾＋navy zip track＋理領／黑 tee；cel-shade lock `hero_awi`。Pipeline：GenerateImage → 864×1152 RGB。唔改 era／core silhouette
- 對開舊 default `1729ee30`／smile `fea5a476`／frown `8a4ef50e`。bak `era_stars/bak_pre_ngai_age_soft_nit_20261105/` 留盤、唔入本 PR
- Soft nits（唔擋 Soft tip）：smile 年齡線略重；default 可讀略過 38；髮絲 modern polish；zip vs brief sil（本輪未改 sil）
- Soft≠PASS；唔 tip LIVE；`?v=` 仍 `19w`；SAVE `starVolunteer_map_v19w`；89–92 HOLD
- Pack：`/workspace/star-volunteer-web-ngai-age-soft-nit.tar.gz`

## era sil Soft polish×3（2026-11-05 Asia/Hong_Kong）

- 只換：`story/era_stars/yip_manji_silhouette_far.png` MD5 `41ef7a1f`；`so_jiyan_silhouette_far.png` MD5 `720e3473`；`luk_baakyin_silhouette_far.png` MD5 `194f29f2`
- 唔動：`liu_bingxing_silhouette_far.png` `1238929c`；`ngai_wingnaam_silhouette_far.png` `31555755`。bust、core sil、`index.html` 未動
- 對開 v2：yip `b606c5a1`／so `e37e095a`／luk `03fdc270`。864×1152 RGBA 透明底近黑 `(18,18,20)`、無五官。bak `era_stars/bak_pre_silhouette_soft_polish_20261105/` 留盤、唔入本 PR
- Soft 遠觀仍掛 `eraSilhouetteFarSrc` → `assets/story/era_stars/{id}_silhouette_far.png?v=19w`（Soft tip #24／#26 wire；本輪唔改碼、唔抬 `?v=`）
- Soft nits（唔擋 Soft tip）：luk 理領手遠距弱、quiff 可比 bust 再尖；so 遠距手位可歧義讀手背後；yip 肩凹、無光邊；全套無淡場景光邊；ngai zip sil 未做；liu 未動
- Soft≠PASS；唔 tip LIVE；`?v=` 仍 `19w`；SAVE `starVolunteer_map_v19w`；89–92 HOLD
- Pack：`/workspace/star-volunteer-web-era-sil-soft-polish.tar.gz`

## ngai zip sil Soft nit（2026-11-05 Asia/Hong_Kong）

- 只換：`story/era_stars/ngai_wingnaam_silhouette_far.png` MD5 `899c7f7df3567566f018115a82d89662`（864×1152 RGBA）
- 唔動：`liu_bingxing_silhouette_far.png` `1238929c`；`yip_manji_silhouette_far.png` `41ef7a1f`；`so_jiyan_silhouette_far.png` `720e3473`；`luk_baakyin_silhouette_far.png` `194f29f2`。bust×15、core sil、`index.html`、gigs 未動
- 對開 v2 `3155575564277cee4ced9ec00c557a48`。近黑 fill `(18,18,20)`、無五官。bak `era_stars/bak_pre_ngai_zip_sil_soft_nit_20261105/` 留盤、唔入本 PR
- 目標：對齊 live bust zip／高領／低馬尾／理領
- Soft 遠觀仍掛 `eraSilhouetteFarSrc` → `assets/story/era_stars/{id}_silhouette_far.png?v=19w`（本輪唔改碼、唔抬 `?v=`）
- Soft nits（唔擋 Soft tip）：遠距可讀成連帽；理領空隙弱；無光邊
- QC：統籌 Style PASS with nits。Soft≠PASS；唔 tip LIVE；`?v=` 仍 `19w`；SAVE `starVolunteer_map_v19w`；89–92 HOLD
- Pack：`/workspace/star-volunteer-web-ngai-zip-sil-soft-nit.tar.gz` MD5 `35e00f8052a144e2283b43e2d584db44`

## yip／liu smile↔default Soft nit（2026-11-05 Asia/Hong_Kong）

- 只換：`story/era_stars/yip_manji_bust_default.png` MD5 `b338280b`；`yip_manji_bust_smile.png` MD5 `6e7b1a2b`；`liu_bingxing_bust_default.png` MD5 `f39379d5`；`liu_bingxing_bust_smile.png` MD5 `3b3c7fb4`
- 唔動：yip frown `9d7e2b8e`。liu frown 見下一節。唔改 sil／ngai／so／luk bust／`index.html`／gigs。starlet-v3 露肩 dusty-rose 與 chow-vibe v10 花恤衫 wardrobe／cel-shade lock。Pipeline：GenerateImage → 864×1152 RGB
- 對開舊：yip default `247b7569`／smile `d40c3dd7`；liu default `a3005d45`／smile `9429f734`。bak `era_stars/bak_pre_yip_liu_smile_default_soft_nit_20261105/` 留盤、唔入本 PR
- 目標：default 更中性閉唇；smile 露齒更明顯（liu default 唔再露齒 smirk）
- Soft nits（唔擋 Soft tip）：yip default 仍極淡嘴角；modern polish 線密度；sil light-edge 後排
- Soft≠PASS；唔 tip LIVE；`?v=` 仍 `19w`；SAVE `starVolunteer_map_v19w`；89–92 HOLD
- Pack：`/workspace/star-volunteer-web-yip-liu-smile-default-soft-nit.tar.gz` MD5 `f4b3107521e91d1cf4329ed7e13f58b9`

## liu frown Soft nit（2026-11-05 Asia/Hong_Kong）

- 只換：`story/era_stars/liu_bingxing_bust_frown.png` MD5 `82edc37f`。併入 yip／liu smile↔default 同一 Soft tip，唔另開
- 唔動：default `f39379d5`；smile `3b3c7fb4`；yip default `b338280b`；yip smile `6e7b1a2b`；yip frown `9d7e2b8e`。唔改 sil／ngai／so／luk bust／`index.html`／gigs。chow-vibe v10 花恤衫／cel-shade lock。Pipeline：GenerateImage → 864×1152 RGB
- 對開舊 frown `11582108`。bak `era_stars/bak_pre_liu_frown_soft_nit_20261105/` 留盤、唔入本 PR
- 目標：吃癟下撇＋夾眉，對開 default 閉唇微翹／smile 露齒
- Soft nits（唔擋 Soft tip）：下巴 hatch；吃癟弧略誇；線密度／modern polish。連同既有：yip default 極淡嘴角；modern polish；sil light-edge 後排
- Soft≠PASS；唔 tip LIVE；`?v=` 仍 `19w`；SAVE `starVolunteer_map_v19w`；89–92 HOLD
- Pack：`/workspace/star-volunteer-web-liu-frown-soft-nit.tar.gz` MD5 `95ac38ba3579afe88c63a6a1d186deb7`

## yip energy Soft nit（2026-11-05 Asia/Hong_Kong）

- 只換：`story/era_stars/yip_manji_bust_default.png` MD5 `08384068`；`yip_manji_bust_smile.png` MD5 `f1688fb4`（864×1152 RGB）
- 唔動：frown `9d7e2b8e`。唔改 liu／so／ngai／luk bust、silhouettes、`index.html`、gigs。starlet-v3 露肩 dusty-rose／cel-shade lock。Pipeline：GenerateImage → 864×1152 RGB
- 對開 tip #30：default `b338280b`／smile `6e7b1a2b`。bak `era_stars/bak_pre_yip_energy_soft_nit_20261105/` 留盤、唔入本 PR
- 目標：default 嬌俏眨眼＋閉唇嘴形更清晰／咬唇－微 smirk 能量；smile 更開／更暖露齒＋眼閃↑。≠so／ngai
- Soft nits（唔擋 Soft tip）：wink 可偏強；微 smirk；線密度／modern polish
- QC：統籌 Style PASS with nits。Soft≠PASS；唔 tip LIVE；`?v=` 仍 `19w`；SAVE `starVolunteer_map_v19w`；89–92 HOLD
- Pack：`/workspace/star-volunteer-web-yip-energy-soft-nit.tar.gz` MD5 `77ab9fa9c12e29f7af3b25b16a82ed82`

## sil 光邊 Soft polish（era×5＋core×6）（2026-11-05 Asia/Hong_Kong）

- 只換 live `*_silhouette_far.png` ×11（era×5＋core×6）。864×1152 RGBA。唔改 bust／index／gigs／其他 assets。遠觀 wire 仍 `eraSilhouetteFarSrc`／`coreSilhouetteFarSrc` → `?v=19w`（本輪唔改碼、唔抬 `?v=`）
- Era：`yip_manji` `b29c5efc`（prior Soft polish `41ef7a1f`）；`so_jiyan` `30fec574`（prior `720e3473`）；`luk_baakyin` `45d03628`（prior `194f29f2`）；`ngai_wingnaam` `79f2e144`（prior zip `899c7f7d`）；`liu_bingxing` `4bbf6e7f`（prior v2 `1238929c`）
- Core：`lin_hiu` `2345fa2b`（prior `bcc3601d`）；`chow_choiyi` `c808e004`（prior `4fbe5b19`）；`vera` `2e44ff61`（prior `7240595e`）；`ko_chunkit` `5a808447`（prior `34c47352`）；`tang_laiping` `54910d1f`（prior `0e8943c2`）；`lui_ging` `4c3d1f0f`（prior `991d7f0e`）
- Pipeline：Pillow／scipy EDT 淡場景光邊。深心 fill 仍 exact `(18,18,20)`；外緣 soft warm rim＋淡 halo；soft_max RGB 92／88／82；無五官；wardrobe Jaccard 1.000
- bak `era_stars|core/bak_pre_sil_light_edge_soft_polish_20261105/` 留盤、唔入本 PR。compare／QA md／REPORT 唔入本 PR
- Soft nits（唔擋 Soft tip）：cream／亮底 rim 近隱形（暗場可讀係設計目標）；rim 呈連續薄邊、可再漫射；outer halo 可再淡／再闊。prior sil shape nits 未本輪處理：yip 肩凹；so 手前遠距歧義；luk 理領遠距弱；ngai zip vs 連帽歧義
- QC：統籌 Style PASS with nits。Soft≠PASS；唔 tip LIVE；`?v=` 仍 `19w`；SAVE `starVolunteer_map_v19w`；89–92 HOLD
- Pack：`/workspace/star-volunteer-web-sil-light-edge-soft-polish.tar.gz` MD5 `a615445f89fa9c0d8f6b89372af63e16`

## so／yip frown Soft nit（2026-11-05 Asia/Hong_Kong）

- 只換：`story/era_stars/so_jiyan_bust_frown.png` MD5 `dbe0ce32`；`yip_manji_bust_frown.png` MD5 `d50275e8`（864×1152 RGB）
- 唔動：so default `2cc1a570`／smile `e57ab12a`；yip default `08384068`／smile `f1688fb4`。唔改 liu／ngai／luk bust、silhouettes、`index.html`、gigs。jade-v4／starlet-v3 wardrobe／cel-shade lock。Pipeline：GenerateImage → 864×1152 RGB
- 對開舊 frown：so `f0c0347e`／yip `9d7e2b8e`（prior RGBA）。bak `era_stars/bak_pre_so_yip_frown_soft_nit_20261105/` 留盤、唔入本 PR。preferFile 仍未加 era_stars bust path
- 目標：so 夾眉下撇不高興，對開 energy default／smile；yip 雙目睜下撇／咬唇，對開 wink default／露齒 smile
- Soft nits（唔擋 Soft tip）：so 可選再收眉粗／怒感 5%；yip 可選再推咬唇若 pout 仍偏 glare；NEW RGB vs prior RGBA（記帳 only）
- QC：統籌 Style PASS with nits。Soft≠PASS；唔 tip LIVE；`?v=` 仍 `19w`；SAVE `starVolunteer_map_v19w`；89–92 HOLD
- Pack：`/workspace/star-volunteer-web-so-yip-frown-soft-nit.tar.gz`（live-only 入本 PR；bak／qa 唔入）

## yip wink Soft nit（2026-11-05 Asia/Hong_Kong）

- 只換：`story/era_stars/yip_manji_bust_default.png` MD5 `fe28eb9b`；`yip_manji_bust_smile.png` MD5 `86a75894`（864×1152 RGB）
- 唔動：frown `d50275e8`。唔改 so／liu／ngai／luk bust、silhouettes、`index.html`、gigs。starlet-v3 露肩 dusty-rose／cel-shade lock。Pipeline：GenerateImage → 864×1152 RGB
- 對開 energy Soft tip：default `08384068`／smile `f1688fb4`。bak `era_stars/bak_pre_yip_wink_soft_nit_20261105/` 留盤、唔入本 PR。preferFile 仍未加 era_stars bust path（同 #30／#31／#34）
- 目標：default 雙目睜＋閉唇微 smirk，收斂強 wink；smile 露齒暖笑＋眼閃。frown 雙目睜下撇／咬唇 lock
- Soft nits（唔擋 Soft tip）：線密度／modern polish residual；可選再推 default 輕咬唇能量／再近阿偉 cel
- QC：統籌 Style PASS with nits。Soft≠PASS；唔 tip LIVE；`?v=` 仍 `19w`；SAVE `starVolunteer_map_v19w`；89–92 HOLD
- Pack：`/workspace/star-volunteer-web-yip-wink-soft-nit.tar.gz`（live-only 入本 PR；bak／qa 唔入）

## so／yip frown polish Soft nit（2026-11-05 Asia/Hong_Kong）

- 只換：`story/era_stars/so_jiyan_bust_frown.png` MD5 `4e9d521c`；`yip_manji_bust_frown.png` MD5 `33152c22`（864×1152 RGB）
- 唔動：so default `2cc1a570`／smile `e57ab12a`。yip default `fe28eb9b`／smile `86a75894`（wink Soft tip，本 PR 唔覆寫）。唔改 liu／ngai／luk bust、silhouettes、`index.html`、gigs。jade-v4／starlet-v3 wardrobe／cel-shade lock。Pipeline：GenerateImage → 864×1152 RGB
- 對開舊 Soft tip frown：so `dbe0ce32`／yip `d50275e8`。bak `era_stars/bak_pre_so_yip_frown_polish_soft_nit_20261105/` 留盤、唔入本 PR。preferFile 仍未加 era_stars bust path。本 PR 唔併 #35／#36
- 目標：so 夾眉下撇保留、眉薄／怒感收約 5–10%，對開 energy default／smile；yip 雙目睜＋咬唇嬌俏敗興↑，對開 wink default／露齒 smile
- Soft nits（唔擋 Soft tip）：線密度仍偏 modern polish；so 怒感若過收／過軟可回微加夾眉；yip 咬唇角度／牙齒露出量可再微調
- QC：統籌 Style PASS with nits。Soft≠PASS；唔 tip LIVE；`?v=` 仍 `19w`；SAVE `starVolunteer_map_v19w`；89–92 HOLD
- Pack：`/workspace/star-volunteer-web-so-yip-frown-polish-soft-nit.tar.gz`（live-only 入本 PR；bak／qa 唔入）

## sil shape Soft nit（2026-11-05 Asia/Hong_Kong）

- 只換：`story/era_stars/yip_manji_silhouette_far.png` MD5 `ba8ad339`；`so_jiyan_silhouette_far.png` MD5 `2602dda9`；`luk_baakyin_silhouette_far.png` MD5 `022489bc`；`ngai_wingnaam_silhouette_far.png` MD5 `c0f0d41e`（864×1152 RGBA）
- 唔動：`liu_bingxing_silhouette_far.png` `4bbf6e7f`。core×6 sil、bust×15、`index.html`、gigs 未動。遠觀 wire 仍 `eraSilhouetteFarSrc` → `?v=19w`（本輪唔改碼、唔抬 `?v=`）。唔做 C cream-rim big redo
- 對開光邊 Soft tip：yip `b29c5efc`／so `30fec574`／luk `45d03628`／ngai `79f2e144`。近黑 fill `(18,18,20)`、無五官；tip#32 soft warm rim／halo 重套。bak `era_stars/bak_pre_sil_shape_soft_nit_20261105/` 留盤、唔入本 PR
- 目標：yip 肩凹清；so 叉腰手前可讀；luk quiff↑；ngai 高領 zip
- Soft nits（唔擋 Soft tip）：luk／ngai 理領空隙；ngai 連帽遠距
- QC：統籌 Style PASS with nits。Soft≠PASS；唔 tip LIVE；`?v=` 仍 `19w`；SAVE `starVolunteer_map_v19w`；89–92 HOLD
- Pack：`/workspace/star-volunteer-web-sil-shape-soft-nit.tar.gz`（live-only 入本 PR；bak／qa 唔入）
