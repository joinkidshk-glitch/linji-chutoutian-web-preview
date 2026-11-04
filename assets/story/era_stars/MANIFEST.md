# Era Stars bust／silhouette — MANIFEST

> **時間：** 2026-11-05（Asia/Hong_Kong）  
> **Brief：** `content/ART_BRIEF_MVP_ERA_STARS_v1.md`  
> **LOOKS：** `content/PLAN_CHAR_LOOKS_REF_v1.md` §C  
> **Pipeline：** cursor **GenerateImage**（refs `hero_awi.jpg`＋`char_hero_bust_default.png`）→ Pillow cover-crop **864×1152** PNG  
> **狀態：** **Style-lock redo 2026-11-05** — 5 人 ×3 表情＝15 bust 已換平面動畫／cel-shade；Soft≠PASS；**唔 tip LIVE**；**1989–1992 HOLD**；**silhouettes 後掛（未動）**

## Style-lock MD5（installed live）

| file | MD5 |
|---|---|
| `liu_bingxing_bust_default.png` | `7c82553e3b6f47c4609486e23c23361f` |
| `liu_bingxing_bust_frown.png` | `2eb8d4bb888f19f80ae80202e6e5e166` |
| `liu_bingxing_bust_smile.png` | `225d30e6214c14c185e302d984fe239f` |
| `luk_baakyin_bust_default.png` | `1b8f1229b3cac9dc54d62454d4c417b0` |
| `luk_baakyin_bust_frown.png` | `b6cbfd292a4a14048727ea351012ca9b` |
| `luk_baakyin_bust_smile.png` | `44ec979ade01184b81629adcf4143e60` |
| `ngai_wingnaam_bust_default.png` | `90305768c0bf93c538b6c6a8e84d554c` |
| `ngai_wingnaam_bust_frown.png` | `1e86e3dbca3c7d0c35c500df25924992` |
| `ngai_wingnaam_bust_smile.png` | `796214d76561cc8e6c1553a42827e7a1` |
| `so_jiyan_bust_default.png` | `f54d3e27db3b11cc2eb2bdd9d9bfbc77` |
| `so_jiyan_bust_frown.png` | `ae224754340405678b5d58a00112e207` |
| `so_jiyan_bust_smile.png` | `9d2473603c34be753bc551c7c4450629` |
| `yip_manji_bust_default.png` | `e8860a880fd1c46c88b577699c6a1fb1` |
| `yip_manji_bust_frown.png` | `0782825acadecc6978f271f0c3c09f60` |
| `yip_manji_bust_smile.png` | `bd9695324fc950a0b8d4dba03a045d89` |

## Inventory

| id | display | files | dims | notes |
|---|---|---|---|---|
| `luk_baakyin` | 陸柏言 | `*_bust_{default,smile,frown}.png` | 864×1152 | 雙排扣 oversized 西裝＋高領；default／smile／frown；style-lock 2026-11-05 |
| `yip_manji` | 葉敏芝 | bust×3 | 864×1152 | 貼身 dusty-rose 針織＋高腰感；自信／笑／鼓腮 pout |
| `so_jiyan` | 蘇芷茵 | bust×3 | 864×1152 | 淺色開襟＋碎花；恬靜／淺笑／微憂 |
| `liu_bingxing` | 廖炳星 | bust×3 | 864×1152 | 花恤衫；微翹／壞笑／吃癟 |
| `ngai_wingnaam` | 魏詠男 | bust×3 | 864×1152 | 純色 navy 運動外套（無三白條）＋黑背心；frown 性別漂 v1 已 regen |

**Bust 底：** cream studio ~`#F2EBD8`（跟 C1／阿偉）。  
**bak：** 舊稿留盤，未入本 PR（tar 只有 live 15）。  
**Silhouette：** 本 repo 無 `*_silhouette_*`。本輪唔加、唔改。遠觀仍係純文字，bust 未掛上畫面。`?v=` 仍 `19w`。SAVE `starVolunteer_map_v19w`。

## Soft nits（唔擋；Soft≠PASS）

1. `luk_baakyin` smile／default 表情差偏細；酒窩未夠明顯  
2. `yip_manji` smile 眨眼／咬唇能量偏弱（較接近溫柔笑）  
3. `liu_bingxing` smile 挑眉峰可再強；花恤印花略密  
4. **優先** `ngai_wingnaam` 髮型跨表情未統一（smile 高馬尾 vs default／frown 低馬尾）；年齡觀感略偏年輕於 LOOKS ~38  
5. 整體略 modern polished anime／manhwa 線密度（同 core Soft nit），仍係平面 2D 家族——非先前半寫實漂移  
6. Prompt 禁真藝名；LOOKS 靈感只作氣質／wardrobe

## Gates

Soft≠PASS｜唔 tip LIVE｜唔 wake iOS｜89–92 HOLD｜silhouettes 後掛｜`?v=` 仍 `19w`｜SAVE `starVolunteer_map_v19w`

## Pack

`/workspace/star-volunteer-web-style-lock-era-stars.tar.gz`（15 live PNG＋MANIFEST＋STYLE_CANON；bak 留盤）

## Related

- Prior MVP：`/workspace/star-volunteer-web-era-stars-mvp.tar.gz`；ngai fix `/workspace/star-volunteer-web-era-ngai-cork-fix.tar.gz`
- Core style-lock：`/workspace/star-volunteer-web-style-lock-core-busts.tar.gz`
- Cheung style-lock：`/workspace/star-volunteer-web-style-lock-cheung.tar.gz`
- QA：`/workspace/qa-gd-style-lock-era-20261105.md`
