# Era Stars bust／silhouette — MANIFEST

> **時間：** 2026-11-05（Asia/Hong_Kong）  
> **Brief：** `content/ART_BRIEF_MVP_ERA_STARS_v1.md`  
> **LOOKS：** `content/PLAN_CHAR_LOOKS_REF_v1.md` §C  
> **Pipeline：** cursor **GenerateImage**（refs `hero_awi.jpg`＋`char_hero_bust_default.png`）→ Pillow cover-crop **864×1152** PNG  
> **狀態：** **Soft tip 2026-11-05** — **luk leather v5b**＋**liu chow-vibe v10**＋**yip starlet-v3**＋**so jade-v4**＋**ngai kara-v5**（各 bust×3）。5 人 ×3 表情＝15 live bust。ngai kara-v2 已由 kara-v5 取代，唔再係 live。**Soft nits expr** 已換 so smile／luk smile／ngai×3（bak `bak_pre_soft_nits_expr_20261105/` 唔入本 PR）。**silhouettes v2** 5／5 `*_silhouette_far.png` 已入 Soft（bak 唔入本 PR）。挑眉 `raise_brow` 後排、唔動。Soft≠PASS；**唔 tip LIVE**；**1989–1992 HOLD**；`?v=` 仍 `19w`；SAVE `starVolunteer_map_v19w`

## Style-lock MD5（installed live）

| file | MD5 |
|---|---|
| `liu_bingxing_bust_default.png` | `a3005d4508817a3acfd4c53a6d5d1518` |
| `liu_bingxing_bust_frown.png` | `11582108cabd5d8b7cd53be13788b962` |
| `liu_bingxing_bust_smile.png` | `9429f734da9f95a6ef172ffeb5fdda6d` |
| `luk_baakyin_bust_default.png` | `f0bc02d8db898c1d6799b8cabed342c7` |
| `luk_baakyin_bust_frown.png` | `d379b32269a427c4695399c46c553b3a` |
| `luk_baakyin_bust_smile.png` | `202a6200b9a7bf019d63d8e5c1dd440c` |
| `ngai_wingnaam_bust_default.png` | `1729ee30129632fd13ed3bad8a297537` |
| `ngai_wingnaam_bust_frown.png` | `8a4ef50ea433990fb77dcba4db6d90d4` |
| `ngai_wingnaam_bust_smile.png` | `fea5a4769558bed238a71b6e0273b77b` |
| `so_jiyan_bust_default.png` | `912b8dc594c26038efb5db86e4fbd99e` |
| `so_jiyan_bust_frown.png` | `f0c0347ebfb54d00993428404ab2e231` |
| `so_jiyan_bust_smile.png` | `0b8199617ea0366081a34ff3d8f5a64d` |
| `yip_manji_bust_default.png` | `247b7569c204d9ff3b9e091611fec5e9` |
| `yip_manji_bust_frown.png` | `9d7e2b8ea12a6cd8bfcf92972cba34d9` |
| `yip_manji_bust_smile.png` | `d40c3dd713eef51dfee0615b59eebf1f` |

## Inventory

| id | display | files | dims | notes |
|---|---|---|---|---|
| `luk_baakyin` | 陸柏言 | `*_bust_{default,smile,frown}.png` + `*_silhouette_far.png`（**sil v2**） | 864×1152 | **leather v5b**＋**smile Soft nit 2026-11-05**（露齒酒窩）＋**frown Soft nit 2026-11-05**（深 V 皺眉＋下撇嘴；MD5 `d379b322`）。default `f0bc02d8`／smile `202a6200` 唔動。bak `bak_pre_luk_leather_v5/`＋`bak_pre_soft_nits_expr_20261105/`＋`bak_pre_luk_frown_soft_nit_20261105/` 留盤，唔入本 PR |
| `yip_manji` | 葉敏芝 | bust×3 + sil **v2** | 864×1152 | **starlet-v3 2026-11-05**：露肩 dusty-rose；邱淑貞／張敏氣質（禁抄臉）；GenerateImage。bak `bak_pre_yip_starlet_v3/` 留盤，唔入本 PR |
| `so_jiyan` | 蘇芷茵 | bust×3 + `*_silhouette_far.png`（**sil v2 新建**） | 864×1152 | **jade-v4**＋**smile Soft nit 2026-11-05**（暖笑露齒提示）。bak `bak_pre_so_jade_v4/`＋`bak_pre_soft_nits_expr_20261105/` 留盤，唔入本 PR |
| `liu_bingxing` | 廖炳星 | bust×3 + sil **v2** | 864×1152 | **chow-vibe v10 2026-11-05**：花恤衫正面；周星馳氣質（禁抄臉）；GenerateImage。bak `bak_pre_liu_chow_v10/` 留盤，唔入本 PR |
| `ngai_wingnaam` | 魏詠男 | bust×3 + sil **v2** | 864×1152 | **kara-v5**＋**Soft nits expr 2026-11-05×3**（表情差拉開；年齡仍偏嫩）。kara-v2 唔再係 live。bak `bak_pre_ngai_kara_v5/`＋`bak_pre_soft_nits_expr_20261105/` 留盤，唔入本 PR |

**Bust 底：** cream studio ~`#F2EBD8`（跟 C1／阿偉）。  
**本 Soft tip：** 15 live bust PNG 仍在（其中 so smile、luk smile、ngai default／smile／frown 換 Soft nits expr）；另加 5 live `*_silhouette_far.png`。preferFile 仍未加 era_stars bust path。Soft gate（`BehaviorGate.gatePath()==="soft"`）遠觀 modal 喺 distanceLook 之上顯示 `{starId}_silhouette_far.png`；Soft off／LIVE 仍係文字＋音（Phase3 B）。蘇芷茵無地圖遠觀釘（主表仍 4 人）；Soft `__phase3.sight("so_jiyan")` 先開佢張剪影。  
**bak：** 舊稿留盤，未入本 PR。`bak_pre_silhouette_v2/` 同 `bak_pre_soft_nits_expr_20261105/` **唔入**本 PR。  
**Silhouette v2（2026-11-05 Asia/Hong_Kong）：** 5／5 `*_silhouette_far.png` GenerateImage→Pillow 864×1152 RGBA 透明底近黑 fill；wardrobe 跟 live bust。`?v=` 仍 `19w`。SAVE `starVolunteer_map_v19w`。

| file | MD5 |
|---|---|
| `luk_baakyin_silhouette_far.png` | `03fdc270f7936a065d6ab51df3f0d6c6` |
| `liu_bingxing_silhouette_far.png` | `1238929c711bbdf4fd7252be441554c1` |
| `ngai_wingnaam_silhouette_far.png` | `3155575564277cee4ced9ec00c557a48` |
| `yip_manji_silhouette_far.png` | `b606c5a1615b27173041bb22f2a10b0b` |
| `so_jiyan_silhouette_far.png` | `e37e095a42f41367d8043948762b2ae9` |

## Soft nits（唔擋；Soft≠PASS）

1. `luk_baakyin` smile Soft nit **2026-11-05 已換**（露齒＋酒窩；MD5 `202a6200`）；**frown Soft nit 2026-11-05 已換**（深 V 皺眉＋鼻樑壓＋下撇嘴；MD5 `d379b322`；對開 default smirk／smile 露齒）。Soft nits（唔擋）：怒氣線可再強；眉峰 V 可再銳  
2. `so_jiyan` smile Soft nit **2026-11-05 已換**（暖笑露齒提示；MD5 `0b819961`）；能量仍可再推  
3. `ngai_wingnaam` Soft nits expr **2026-11-05 已換×3**（default／smile／frown MD5 `1729ee30`／`fea5a476`／`8a4ef50e`）；**年齡仍偏嫩**（~38 未清）。kara-v2 已由 v5 取代，唔再係 live  
4. `yip_manji` starlet-v3：咬唇／眨眼能量仍可再推；default↔smile 差可再拉開  
5. `liu_bingxing` chow-vibe v10：default↔smile 差可再拉開；frown 吃癟可再強  
6. 整體略 modern polished anime／manhwa 線密度（同 core Soft nit），仍係平面 2D 家族——非先前半寫實漂移  
7. Prompt 禁真藝名；LOOKS 靈感只作氣質／wardrobe  
8. `char_hero_bust_raise_brow` 挑眉 Soft nit **未入本 pack**、後排、唔動  
9. **sil v2（唔擋）** `yip_manji`：袖線讀成長袖貼身，對開 bust 露肩 dusty-rose  
10. **sil v2（唔擋）** `so_jiyan`：手位偏身前輕握／身側  
11. **sil v2（唔擋）** `luk_baakyin`：髮頂體積可比 bust 再推  
12. **sil v2（唔擋）** 全套無淡場景光邊（純透明底近黑形）  
13. **sil v2（唔擋）** `ngai_wingnaam`：跟 live bust 高領 zip，唔跟舊 brief「短打」字面

## Gates

Soft≠PASS｜唔 tip LIVE｜唔 wake iOS｜89–92 HOLD｜silhouettes v2 Soft tip（遠觀只限 Soft gate）｜expr nits Soft tip｜raise_brow 後排｜`?v=` 仍 `19w`｜SAVE `starVolunteer_map_v19w`

## Pack

`/workspace/star-volunteer-web-style-lock-era-stars.tar.gz`（15 live PNG＋MANIFEST＋STYLE_CANON；bak 留盤）

`/workspace/star-volunteer-web-luk-leather-v5.tar.gz`（luk×3 live；bak 留盤）

`/workspace/star-volunteer-web-liu-chow-v10.tar.gz`（liu×3 live；bak 留盤）

`/workspace/star-volunteer-web-yip-starlet-v3.tar.gz`（yip×3 live；bak 留盤）

`/workspace/star-volunteer-web-so-jade-v4.tar.gz`（so×3 live；bak 留盤）

`/workspace/star-volunteer-web-ngai-kara-v5.tar.gz`（ngai×3 live style＋pose redo，替 kara-v2；bak 留盤。v2 唔再係 live）

`/workspace/star-volunteer-web-era-silhouettes-v2.tar.gz`（sil×5 live＋MANIFEST；`bak_pre_silhouette_v2/` 留盤，唔入本 PR）

`/workspace/star-volunteer-web-era-soft-nits-expr.tar.gz`（so smile＋luk smile＋ngai×3 live；`bak_pre_soft_nits_expr_20261105/` 留盤，唔入本 PR）

`/workspace/star-volunteer-web-luk-frown-soft-nit.tar.gz`（只換 live `luk_baakyin_bust_frown.png`；bak／`_qc_refs`／QA composite 唔入本 PR）

## Related

- Prior MVP：`/workspace/star-volunteer-web-era-stars-mvp.tar.gz`；ngai fix `/workspace/star-volunteer-web-era-ngai-cork-fix.tar.gz`
- Core style-lock：`/workspace/star-volunteer-web-style-lock-core-busts.tar.gz`
- Cheung style-lock：`/workspace/star-volunteer-web-style-lock-cheung.tar.gz`
- QA：`/workspace/qa-gd-style-lock-era-20261105.md`

## luk frown Soft nit 2026-11-05 (Asia/Hong_Kong)
- 只換 live：`luk_baakyin_bust_frown.png` MD5 `d379b32269a427c4695399c46c553b3a`
- 唔動：default `f0bc02d8db898c1d6799b8cabed342c7`；smile `202a6200b9a7bf019d63d8e5c1dd440c`（Soft tip #24）
- 對開舊 frown：`9e1342229fc79f1aa85ebecb318821d0`。bak `bak_pre_luk_frown_soft_nit_20261105/` 留盤、唔入本 PR
- Soft nits（唔擋 Soft tip）：怒氣線可再強；眉峰 V 可再銳
- Soft≠PASS｜唔 tip LIVE｜唔抬 ?v=｜89–92 HOLD
- Pack：`/workspace/star-volunteer-web-luk-frown-soft-nit.tar.gz`
