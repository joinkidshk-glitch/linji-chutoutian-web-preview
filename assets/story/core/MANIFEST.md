# Core／Romance／cast busts — MANIFEST

> **時間：** 2026-11-05（Asia/Hong_Kong）  
> **LOOKS：** `content/PLAN_CHAR_LOOKS_REF_v1.md`  
> **Pipeline：** cursor GenerateImage（refs=`hero_awi.jpg`＋`c1/char_hero_bust_default.png`＋npc identity when present）→ Pillow **864×1152** PNG；cream studio  
> **Style lock（HARD · 用戶 2026-11-05）：** 平面 2D anime／VN cel-shade；清黑線；大眼高光；硬邊陰影；禁半寫實／相片膚／細密髮絲／softbox  
> **狀態：** CORE 六角 **style-lock redo**（default＋smile＋frown ×6＝18 PNG）已安裝；**core／romance silhouette_far Soft×6**（2026-11-05）已裝，Soft 遠觀先掛；**sil 光邊 Soft polish**（2026-11-05）已換 core×6 `*_silhouette_far.png`（同 era×5；淡暖 rim＋淡 halo；bak `bak_pre_sil_light_edge_soft_polish_20261105/` 唔入本 PR）；**sil rim／halo Soft polish**（2026-11-05）已換 core×6（同 era×5；cream rim／漫射／halo；唔改 shape；bak `bak_pre_sil_rim_halo_soft_polish_20261105/` 唔入本 PR）；**Soft A② sil cream 略深 rim Soft polish**（2026-11-05）已換 core×6（同 era×5；warm RIM `[178,162,140]`／rim_strength 0.66／depth 5.5／halo α peak 20；solid Jaccard 1.0；唔改 shape；bak `bak_pre_sil_cream_rim_soft_polish_20261105/` 唔入本 PR）；**Soft≠PASS**；唔 tip LIVE；**1989–1992 HOLD**  
> **本輪：** bust live 18（bak 省略，GD 允許）＋新建 `*_silhouette_far.png` ×6（無舊 sil bak）。`?v=` 仍 `19w`。SAVE `starVolunteer_map_v19w`。  
> StoryPlay 先 probe `assets/story/core/{id}_bust_{expr}.png?v=19w`；六個 core stem 優先用檔案 bust。張子駿 `default`／`raise_brow` 亦優先用 `char_cheung_bust_*.png?v=19w`（四路同 MD5）。其餘臉仍用內嵌肖像。遠觀剪影唔入 bust probe；Soft gate 先掛 `assets/story/core/{id}_silhouette_far.png?v=19w`。唔改 era_stars 剪影。

## Style-lock MD5（2026-11-05）

| file | md5 |
|---|---|
| `vera_bust_default.png` | `a4410583f8c3192a0dcabc44c32e1b01` |
| `vera_bust_smile.png` | `66628bc843a7f51a2398a81d5cb5a3a0` |
| `vera_bust_frown.png` | `14185d4a73c3dc934851dceb0058b191` |
| `chow_choiyi_bust_default.png` | `11c9a476c106afb4028263aa2788c57b` |
| `chow_choiyi_bust_smile.png` | `b5b6ddef940389d6665e1e27c37daf57` |
| `chow_choiyi_bust_frown.png` | `af5de32daab2772c5e5116196db5aa4b` |
| `ko_chunkit_bust_default.png` | `95e0447f3e3f28ed205dc0db3aa0c8f9` |
| `ko_chunkit_bust_smile.png` | `22bb9c5476c78e8b75d9259b97e05c2a` |
| `ko_chunkit_bust_frown.png` | `7ed9b6be4177c5d6fe58a86d25bd1e41` |
| `tang_laiping_bust_default.png` | `e4476a6ecfe3e5a449fc79f299fe1593` |
| `tang_laiping_bust_smile.png` | `7efece904b8356269feee28e577f98da` |
| `tang_laiping_bust_frown.png` | `707d008e1c04fc4b579a35ed245155d8` |
| `lin_hiu_bust_default.png` | `b1fdb1392adf28a470f89d8483a79e6a` |
| `lin_hiu_bust_smile.png` | `39c3c82ee520d9ac17b6aaaf3d6308fb` |
| `lin_hiu_bust_frown.png` | `e3a2c9cd26e25620d16c07edaaa99314` |
| `lui_ging_bust_default.png` | `0ae23dc7b3f80913212cf77402071030` |
| `lui_ging_bust_smile.png` | `af388f6d41dbe0f2eb65d186ff8975bb` |
| `lui_ging_bust_frown.png` | `5ce1633376fa228e7020db247247dd9a` |

## Romance MVP

| id | display | files | dims | notes |
|---|---|---|---|---|
| `lin_hiu` | 林曉晴 | `lin_hiu_bust_{default,smile,frown}.png`＋`lin_hiu_silhouette_far.png` | 864×1152 | style-lock anime；粉藍針織＋白蕾絲娃娃領＋絲巾；親切／露齒／委屈。sil＝裙裝雙手身前（Soft 新建）＋**光邊 Soft polish**（當時 MD5 `2345fa2b`；prior `bcc3601d`）＋**sil rim／halo Soft polish**（當時 MD5 `fe35b9c7`；prior 光邊 `2345fa2b`）＋**Soft A② cream 略深 rim Soft polish**（MD5 `6a0f9985`；prior rim／halo `fe35b9c7`） |
| `chow_choiyi` | 周采兒 | `chow_choiyi_bust_{default,smile,frown}.png`＋`chow_choiyi_silhouette_far.png` | 864×1152 | style-lock anime；駝風褸＋千鳥格＋空白記者證；銳利／壞笑／質疑。sil＝長風褸＋靴＋手插袋（Soft 新建）＋**光邊 Soft polish**（當時 MD5 `c808e004`；prior `4fbe5b19`）＋**sil rim／halo Soft polish**（當時 MD5 `abd30eb1`；prior 光邊 `c808e004`）＋**Soft A② cream 略深 rim Soft polish**（MD5 `638e4f2d`；prior rim／halo `abd30eb1`） |

## Core

| id | display | files | dims | notes |
|---|---|---|---|---|
| `vera` | Vera | `vera_bust_{default,smile,frown}.png`＋`vera_silhouette_far.png` | 864×1152 | style-lock anime；短捲齊耳、煙燻＋暗紅唇、黑墊肩＋**blank 軟尺**（無刻度字）＋大金環；咬筆／挑眉自信／撇嘴。sil＝墊肩西裝＋手近腰（Soft 新建）＋**光邊 Soft polish**（當時 MD5 `2e44ff61`；prior `7240595e`）＋**sil rim／halo Soft polish**（當時 MD5 `e5426266`；prior 光邊 `2e44ff61`）＋**Soft A② cream 略深 rim Soft polish**（MD5 `dc9baf9f`；prior rim／halo `e5426266`） |
| `ko_chunkit` | 高俊傑 | `ko_chunkit_bust_{default,smile,frown}.png`＋`ko_chunkit_silhouette_far.png` | 864×1152 | style-lock anime；紅皮褸＋黑 tee＋粗銀鏈；囂張／冷笑／不耐。sil＝biker 皮褸＋一手插袋（Soft 新建）＋**光邊 Soft polish**（當時 MD5 `5a808447`；prior `34c47352`）＋**sil rim／halo Soft polish**（當時 MD5 `22e421fc`；prior 光邊 `5a808447`）＋**Soft A② cream 略深 rim Soft polish**（MD5 `ad22b50e`；prior rim／halo `22e421fc`） |

## cast_main

| id | display | files | dims | notes |
|---|---|---|---|---|
| `tang_laiping` | 鄧麗萍 | `tang_laiping_bust_{default,smile,frown}.png`＋`tang_laiping_silhouette_far.png` | 864×1152 | style-lock anime；黑墊肩＋白飄帶領＋眼鏡、低馬尾；冷酷／薄笑／審視。sil＝抱臂套裝＋低馬尾＋飄帶領結（Soft 新建）＋**光邊 Soft polish**（當時 MD5 `54910d1f`；prior `0e8943c2`）＋**sil rim／halo Soft polish**（當時 MD5 `df71baa7`；prior 光邊 `54910d1f`）＋**Soft A② cream 略深 rim Soft polish**（MD5 `595d9c95`；prior rim／halo `df71baa7`） |
| `lui_ging` | 雷勁 | `lui_ging_bust_{default,smile,frown}.png`＋`lui_ging_silhouette_far.png` | 864×1152 | style-lock anime；花恤衫敞開＋粗金鏈、大背頭、眉骨舊疤；抱胸／冷笑／兇狠。sil＝抱胸壯碩＋恤衫領（Soft 新建）＋**光邊 Soft polish**（當時 MD5 `4c3d1f0f`；prior `991d7f0e`）＋**sil rim／halo Soft polish**（當時 MD5 `3aa128c0`；prior 光邊 `4c3d1f0f`）＋**Soft A② cream 略深 rim Soft polish**（MD5 `ec62dea1`；prior rim／halo `3aa128c0`） |

## C1 expression wave（沿用）

| file | action | notes |
|---|---|---|
| `c1/char_ho_bust_frown.png`（＋dialog） | REDO | 更強邊緣；bak=`*_pre_fix_bak.png` |
| `c1/char_ho_bust_smile.png`（＋dialog） | NEW | 溫暖笑 |
| `c1/char_hero_bust_raise_brow.png` | style-lock 2026-11-05 | 四路同 MD5 `63670d1b`（c1／story／dialog／npc）；bak `c1/char_hero_bust_raise_brow_pre_style_lock_bak.png`（舊半寫實 `e99f2dd3`）；StoryPlay 仍先 probe c1／dialog |

何生表情（唔喺 core 目錄）：`assets/story/c1/char_ho_bust_{frown,smile}.png` 同 `assets/dialog/` 鏡像。皺眉 bak：`assets/story/c1/char_ho_bust_frown_pre_fix_bak.png`。

## Soft notes

- Prompt 禁真藝名；original fictional only。
- Soft≠PASS；唔 tip LIVE；89–92 HOLD。`?v=` 仍 `19w`。SAVE `starVolunteer_map_v19w`。
- **silhouette_far Soft×6（2026-11-05 Asia/Hong_Kong）：** `{lin_hiu,chow_choiyi,vera,ko_chunkit,tang_laiping,lui_ging}_silhouette_far.png`；864×1152 RGBA 透明底近黑 fill；GenerateImage→Pillow；**新建**（無舊檔 bak）。Soft gate 開先喺遠觀顯示 `assets/story/core/{id}_silhouette_far.png?v=19w`；Soft 關／LIVE 仍係文字＋chime，唔強制出圖。當時唔改 era_stars 剪影。
- **silhouette 光邊 Soft polish（2026-11-05 Asia/Hong_Kong）：** 同上 core×6 Pillow／scipy EDT 淡場景光邊（深心 fill `(18,18,20)` 保留；soft warm rim＋淡 halo；無五官）。同 PR 換 era×5。遠觀 wire 仍 `coreSilhouetteFarSrc` → `?v=19w`（本 PR 唔改 `index.html`、唔抬 `?v=`）。bak `bak_pre_sil_light_edge_soft_polish_20261105/`、compare／QA md／REPORT **唔入**本 PR。
- **silhouette rim／halo Soft polish（2026-11-05 Asia/Hong_Kong）：** 同上 core×6 對 tip#32 Soft nits（cream rim／漫射／halo）。Pillow／scipy EDT 更深環境漫射 rim＋更闊更淡 outer halo；深心 fill `(18,18,20)` exact；solid Jaccard 1.0（唔改 shape／wardrobe）。同 PR 換 era×5。遠觀 wire 仍 `coreSilhouetteFarSrc` → `?v=19w`（本 PR 唔改 `index.html`、唔抬 `?v=`、唔改 bust／CSS）。bak `bak_pre_sil_rim_halo_soft_polish_20261105/`、compare／qa **唔入**本 PR。
- **silhouette Soft A② cream 略深 rim／對比 Soft polish（2026-11-05 Asia/Hong_Kong）：** 同上 core×6（同 era×5）。對 C 殘餘 cream 底 rim 近隱形：略加深 warm RIM RGB `[178,162,140]`／rim_strength 0.66／depth 5.5；halo 保持淡（α peak 20）；soft_max≤92；深心 fill `(18,18,20)` exact；solid Jaccard 1.0（唔改 shape／wardrobe）。遠觀 wire 仍 `coreSilhouetteFarSrc` → `?v=19w`（本 PR 唔改 `index.html`、唔抬 `?v=`、唔改 bust／CSS）。bak `bak_pre_sil_cream_rim_soft_polish_20261105/`、compare／qa／REPORT **唔入**本 PR。本 PR 唔併 #40／bust／CSS／Soft A③。

| file | MD5 | note |
|---|---|---|
| `lin_hiu_silhouette_far.png` | `6a0f9985089c77494129d10b0437d421` | Soft A② cream 略深 rim Soft polish；prior rim／halo `fe35b9c7`；光邊 `2345fa2b`；Soft×6 `bcc3601d` |
| `chow_choiyi_silhouette_far.png` | `638e4f2d10b391aa907f452ee06051e3` | Soft A② cream 略深 rim Soft polish；prior rim／halo `abd30eb1`；光邊 `c808e004`；Soft×6 `4fbe5b19` |
| `vera_silhouette_far.png` | `dc9baf9fc7f876d400771742d38b6a24` | Soft A② cream 略深 rim Soft polish；prior rim／halo `e5426266`；光邊 `2e44ff61`；Soft×6 `7240595e` |
| `ko_chunkit_silhouette_far.png` | `ad22b50e5f5e5089e7058f6e58093b88` | Soft A② cream 略深 rim Soft polish；prior rim／halo `22e421fc`；光邊 `5a808447`；Soft×6 `34c47352` |
| `tang_laiping_silhouette_far.png` | `595d9c95c9dfe481b42d47250ded07a4` | Soft A② cream 略深 rim Soft polish；prior rim／halo `df71baa7`；光邊 `54910d1f`；Soft×6 `0e8943c2` |
| `lui_ging_silhouette_far.png` | `ec62dea1daf2512fba746478813a6fd6` | Soft A② cream 略深 rim Soft polish；prior rim／halo `3aa128c0`；光邊 `4c3d1f0f`；Soft×6 `991d7f0e` |

- Soft nits（silhouette，唔擋 Soft tip）：vera 軟尺／耳環／咬筆弱；ko 銀鏈弱；lui 開襟金鏈／背頭弱；lin 手握弱；chow 記者證弱；α 邊薄於 era；vera↔ko 站姿偏近。**光邊 Soft polish 未處理呢批 shape nits。** **sil rim／halo Soft polish 2026-11-05 已換 core×6**（更深漫射 rim＋更闊更淡 halo；唔改 shape）。**Soft A② cream 略深 rim Soft polish 2026-11-05 已換 core×6**（warm RIM `[178,162,140]`／rim_strength 0.66／depth 5.5／halo α peak 20；solid Jaccard 1.0；唔改 shape）。shape nits 仍未本輪處理。
- Tester style-lock **18／18 PASS**（無半寫實膚紋）。
- Soft nits（bust，唔擋；本 PR 唔再開圖）：Vera 軟尺或有細刻度線但無數字；Ko 內搭偏 crew／中分未夠清晰；Tang 眼鏡偏細銀框而非完全無框；Lui 舊疤略明顯；整體略偏 modern polished anime／manhwa，仍係平面 2D；`lin_hiu` default≈smile。

## Packs

- `/workspace/star-volunteer-web-locs-companies-sojiyan.tar.gz`
- `/workspace/star-volunteer-web-c1-expr-romance.tar.gz`
- `/workspace/star-volunteer-web-core-cast-busts.tar.gz`
- `/workspace/star-volunteer-web-hold-redo-hero-vera.tar.gz`
- `/workspace/star-volunteer-web-style-lock-core-busts.tar.gz` ← live 18 bust（bak 未附）
- `/workspace/star-volunteer-web-core-silhouettes-soft.tar.gz` ← silhouette_far Soft×6
- `/workspace/star-volunteer-web-sil-light-edge-soft-polish.tar.gz` MD5 `a615445f89fa9c0d8f6b89372af63e16` ← sil 光邊 Soft polish（core×6＋era×5；bak／compare／QA md／REPORT 唔入本 PR）
- `/workspace/star-volunteer-web-sil-rim-halo-soft-polish.tar.gz` ← sil rim／halo Soft polish（core×6＋era×5；bak／compare／qa 唔入本 PR；bust／CSS／?v= 未動）
- `/workspace/star-volunteer-web-sil-cream-rim-soft-polish.tar.gz` MD5 `088cb66cbd7f7e1cd34bf302fe968a44` ← **本輪 Soft A② sil cream 略深 rim Soft polish**（core×6＋era×5；bak／compare／qa／REPORT 唔入本 PR；bust／CSS／?v= 未動；唔併 #40／bust／CSS／Soft A③）

## sil 光邊 Soft polish core×6 2026-11-05 (Asia/Hong_Kong)
- 只換 live：`lin_hiu_silhouette_far.png` MD5 `2345fa2b11fdad426bd1e7d381042f2d`；`chow_choiyi_silhouette_far.png` MD5 `c808e00485eb321005e9641db7e26b41`；`vera_silhouette_far.png` MD5 `2e44ff61c96caa02f475bae2947ce979`；`ko_chunkit_silhouette_far.png` MD5 `5a808447df7f49002b98fa975d702606`；`tang_laiping_silhouette_far.png` MD5 `54910d1f7d2639e69ce56e22b5ac6692`；`lui_ging_silhouette_far.png` MD5 `4c3d1f0f8ad236e90924016ebb915a92`（864×1152 RGBA）。同 PR 換 era×5
- 唔動：bust×18、`index.html`、gigs、其他 assets。遠觀 wire 仍 `coreSilhouetteFarSrc` → `assets/story/core/{id}_silhouette_far.png?v=19w`
- 對開 prior Soft×6：lin `bcc3601dff02c5183f582074ee9a86c8`；chow `4fbe5b19a5b0980d5f9ed131f165b1e2`；vera `7240595e20484256f9f2967907ace770`；ko `34c4735252ee938943770fa8ced31ff6`；tang `0e8943c2d3e6128d4aa14f36773acb02`；lui `991d7f0ec90792d7a21e5d7251164c4b`。bak `bak_pre_sil_light_edge_soft_polish_20261105/` 留盤、唔入本 PR
- 目標：淡場景光邊。深心 fill exact `(18,18,20)`；soft warm rim＋淡 halo；soft_max RGB 92／88／82；無五官；wardrobe Jaccard 1.000
- Soft nits（唔擋 Soft tip）：cream／亮底 rim 近隱形；rim 可再漫射；halo 可再淡。prior sil shape nits 未本輪處理（軟尺／銀鏈／金鏈／手握／記者證／vera↔ko 站姿）
- QC：統籌 Style PASS with nits。Soft≠PASS｜唔 tip LIVE｜唔抬 ?v=｜SAVE `starVolunteer_map_v19w`｜89–92 HOLD
- Pack：`/workspace/star-volunteer-web-sil-light-edge-soft-polish.tar.gz` MD5 `a615445f89fa9c0d8f6b89372af63e16`

## sil rim／halo Soft polish core×6 2026-11-05 (Asia/Hong_Kong)
- 只換 live：`lin_hiu_silhouette_far.png` MD5 `fe35b9c733df4ae2407528b362b33e73`；`chow_choiyi_silhouette_far.png` MD5 `abd30eb1161accfb3985d414ddb2555e`；`vera_silhouette_far.png` MD5 `e5426266d7bd6da5d9e077d402c2e94a`；`ko_chunkit_silhouette_far.png` MD5 `22e421fc216f3287f5ad9abe66ea61e4`；`tang_laiping_silhouette_far.png` MD5 `df71baa75ffa467fb66bbcd5071def72`；`lui_ging_silhouette_far.png` MD5 `3aa128c0154b5d9efb8a7c02b36eb71f`（864×1152 RGBA）。同 PR 換 era×5
- 唔動：bust×18、`index.html`、gigs、index Soft UI CSS、其他 assets、`?v=`、SAVE `starVolunteer_map_v19w`、`liveWeekGateStillActive`。本 PR 唔併 #38／bust／CSS。遠觀 wire 仍 `coreSilhouetteFarSrc` → `assets/story/core/{id}_silhouette_far.png?v=19w`
- 對開 prior 光邊：lin `2345fa2b11fdad426bd1e7d381042f2d`；chow `c808e00485eb321005e9641db7e26b41`；vera `2e44ff61c96caa02f475bae2947ce979`；ko `5a808447df7f49002b98fa975d702606`；tang `54910d1f7d2639e69ce56e22b5ac6692`；lui `4c3d1f0f8ad236e90924016ebb915a92`。bak `bak_pre_sil_rim_halo_soft_polish_20261105/` 留盤、唔入本 PR
- 目標：cream rim／漫射／halo Soft polish。更深環境漫射 rim（depth 2.5→4.8、strength 0.34→0.42、RIM≈122,116,104）＋更闊更淡 outer halo（radius 6→11、α peak 52→26；soft_max≤92）。深心 fill exact `(18,18,20)`；solid Jaccard 1.0（唔改 shape／wardrobe）；無五官
- Soft nits（唔擋 Soft tip）：cream rim Soft A 後清。prior sil shape nits 未本輪處理（軟尺／銀鏈／金鏈／手握／記者證／vera↔ko 站姿）
- QC：統籌 Style PASS with nits。Soft≠PASS｜唔 tip LIVE｜唔抬 ?v=｜SAVE `starVolunteer_map_v19w`｜89–92 HOLD
- Pack：`/workspace/star-volunteer-web-sil-rim-halo-soft-polish.tar.gz`（live-only 入本 PR；bak／qa 唔入）

## Soft A② sil cream 略深 rim Soft polish core×6 2026-11-05 (Asia/Hong_Kong)
- 只換 live：`lin_hiu_silhouette_far.png` MD5 `6a0f9985089c77494129d10b0437d421`；`chow_choiyi_silhouette_far.png` MD5 `638e4f2d10b391aa907f452ee06051e3`；`vera_silhouette_far.png` MD5 `dc9baf9fc7f876d400771742d38b6a24`；`ko_chunkit_silhouette_far.png` MD5 `ad22b50e5f5e5089e7058f6e58093b88`；`tang_laiping_silhouette_far.png` MD5 `595d9c95c9dfe481b42d47250ded07a4`；`lui_ging_silhouette_far.png` MD5 `ec62dea1daf2512fba746478813a6fd6`（864×1152 RGBA）。同 PR 換 era×5
- 唔動：bust×18、`index.html`、gigs、index Soft UI CSS、其他 assets、`?v=`、SAVE `starVolunteer_map_v19w`、`liveWeekGateStillActive`。本 PR 唔併 #40／bust／CSS／Soft A③。遠觀 wire 仍 `coreSilhouetteFarSrc` → `assets/story/core/{id}_silhouette_far.png?v=19w`
- 對開 prior rim／halo：lin `fe35b9c733df4ae2407528b362b33e73`；chow `abd30eb1161accfb3985d414ddb2555e`；vera `e5426266d7bd6da5d9e077d402c2e94a`；ko `22e421fc216f3287f5ad9abe66ea61e4`；tang `df71baa75ffa467fb66bbcd5071def72`；lui `3aa128c0154b5d9efb8a7c02b36eb71f`。bak `bak_pre_sil_cream_rim_soft_polish_20261105/` 留盤、唔入本 PR
- 目標：cream 略深 rim／對比 Soft polish。略加深 warm RIM RGB `[122,116,104]→[178,162,140]`／rim_strength 0.42→0.66／depth 4.8→5.5；halo 保持淡（α peak 26→20；唔回 tip#32）；AA fringe warm bias；soft_max≤92。深心 fill exact `(18,18,20)`；solid Jaccard 1.0（唔改 shape／wardrobe）；無五官
- QC：統籌 Style PASS with nits。Soft≠PASS｜唔 tip LIVE｜唔抬 ?v=｜SAVE `starVolunteer_map_v19w`｜89–92 HOLD
- Pack：`/workspace/star-volunteer-web-sil-cream-rim-soft-polish.tar.gz` MD5 `088cb66cbd7f7e1cd34bf302fe968a44`（live-only 入本 PR；bak／qa 唔入）
