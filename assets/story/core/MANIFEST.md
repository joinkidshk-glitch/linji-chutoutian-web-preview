# Core／Romance／cast busts — MANIFEST

> **時間：** 2026-11-05（Asia/Hong_Kong）  
> **LOOKS：** `content/PLAN_CHAR_LOOKS_REF_v1.md`  
> **Pipeline：** cursor GenerateImage（refs=`hero_awi.jpg`＋`c1/char_hero_bust_default.png`＋npc identity when present）→ Pillow **864×1152** PNG；cream studio  
> **Style lock（HARD · 用戶 2026-11-05）：** 平面 2D anime／VN cel-shade；清黑線；大眼高光；硬邊陰影；禁半寫實／相片膚／細密髮絲／softbox  
> **狀態：** CORE 六角 **style-lock redo**（default＋smile＋frown ×6＝18 PNG）已安裝；**core／romance silhouette_far Soft×6**（2026-11-05）已裝，Soft 遠觀先掛；**Soft≠PASS**；唔 tip LIVE；**1989–1992 HOLD**  
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
| `lin_hiu` | 林曉晴 | `lin_hiu_bust_{default,smile,frown}.png`＋`lin_hiu_silhouette_far.png` | 864×1152 | style-lock anime；粉藍針織＋白蕾絲娃娃領＋絲巾；親切／露齒／委屈。sil＝裙裝雙手身前（Soft 新建） |
| `chow_choiyi` | 周采兒 | `chow_choiyi_bust_{default,smile,frown}.png`＋`chow_choiyi_silhouette_far.png` | 864×1152 | style-lock anime；駝風褸＋千鳥格＋空白記者證；銳利／壞笑／質疑。sil＝長風褸＋靴＋手插袋（Soft 新建） |

## Core

| id | display | files | dims | notes |
|---|---|---|---|---|
| `vera` | Vera | `vera_bust_{default,smile,frown}.png`＋`vera_silhouette_far.png` | 864×1152 | style-lock anime；短捲齊耳、煙燻＋暗紅唇、黑墊肩＋**blank 軟尺**（無刻度字）＋大金環；咬筆／挑眉自信／撇嘴。sil＝墊肩西裝＋手近腰（Soft 新建） |
| `ko_chunkit` | 高俊傑 | `ko_chunkit_bust_{default,smile,frown}.png`＋`ko_chunkit_silhouette_far.png` | 864×1152 | style-lock anime；紅皮褸＋黑 tee＋粗銀鏈；囂張／冷笑／不耐。sil＝biker 皮褸＋一手插袋（Soft 新建） |

## cast_main

| id | display | files | dims | notes |
|---|---|---|---|---|
| `tang_laiping` | 鄧麗萍 | `tang_laiping_bust_{default,smile,frown}.png`＋`tang_laiping_silhouette_far.png` | 864×1152 | style-lock anime；黑墊肩＋白飄帶領＋眼鏡、低馬尾；冷酷／薄笑／審視。sil＝抱臂套裝＋低馬尾＋飄帶領結（Soft 新建） |
| `lui_ging` | 雷勁 | `lui_ging_bust_{default,smile,frown}.png`＋`lui_ging_silhouette_far.png` | 864×1152 | style-lock anime；花恤衫敞開＋粗金鏈、大背頭、眉骨舊疤；抱胸／冷笑／兇狠。sil＝抱胸壯碩＋恤衫領（Soft 新建） |

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
- **silhouette_far Soft×6（2026-11-05 Asia/Hong_Kong）：** `{lin_hiu,chow_choiyi,vera,ko_chunkit,tang_laiping,lui_ging}_silhouette_far.png`；864×1152 RGBA 透明底近黑 fill；GenerateImage→Pillow；**新建**（無舊檔 bak）。Soft gate 開先喺遠觀顯示 `assets/story/core/{id}_silhouette_far.png?v=19w`；Soft 關／LIVE 仍係文字＋chime，唔強制出圖。唔改 era_stars 剪影。

| file | MD5 |
|---|---|
| `lin_hiu_silhouette_far.png` | `bcc3601dff02c5183f582074ee9a86c8` |
| `chow_choiyi_silhouette_far.png` | `4fbe5b19a5b0980d5f9ed131f165b1e2` |
| `vera_silhouette_far.png` | `7240595e20484256f9f2967907ace770` |
| `ko_chunkit_silhouette_far.png` | `34c4735252ee938943770fa8ced31ff6` |
| `tang_laiping_silhouette_far.png` | `0e8943c2d3e6128d4aa14f36773acb02` |
| `lui_ging_silhouette_far.png` | `991d7f0ec90792d7a21e5d7251164c4b` |

- Soft nits（silhouette，唔擋 Soft tip）：vera 軟尺／耳環／咬筆弱；ko 銀鏈弱；lui 開襟金鏈／背頭弱；lin 手握弱；chow 記者證弱；α 邊薄於 era；vera↔ko 站姿偏近。
- Tester style-lock **18／18 PASS**（無半寫實膚紋）。
- Soft nits（bust，唔擋；本 PR 唔再開圖）：Vera 軟尺或有細刻度線但無數字；Ko 內搭偏 crew／中分未夠清晰；Tang 眼鏡偏細銀框而非完全無框；Lui 舊疤略明顯；整體略偏 modern polished anime／manhwa，仍係平面 2D；`lin_hiu` default≈smile。

## Packs

- `/workspace/star-volunteer-web-locs-companies-sojiyan.tar.gz`
- `/workspace/star-volunteer-web-c1-expr-romance.tar.gz`
- `/workspace/star-volunteer-web-core-cast-busts.tar.gz`
- `/workspace/star-volunteer-web-hold-redo-hero-vera.tar.gz`
- `/workspace/star-volunteer-web-style-lock-core-busts.tar.gz` ← live 18 bust（bak 未附）
- `/workspace/star-volunteer-web-core-silhouettes-soft.tar.gz` ← **本輪 silhouette_far Soft×6**
