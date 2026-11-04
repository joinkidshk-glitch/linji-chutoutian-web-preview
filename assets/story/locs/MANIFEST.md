# Story location environments — MANIFEST

> 2026-11-04（Asia/Hong_Kong）· 19v nit fix  
> LOOKS master: `content/PLAN_CHAR_LOOKS_REF_v1.md`（SHA 48ea7aac… verified）  
> Pipeline: **cursor GenerateImage** → crop/cover **720×1280** JPG q≈85  
> Soft≠PASS。**唔改 LIVE 碼**。**1989–1992 資產 HOLD**。

## Files

| artId / key | file | size | dims | notes |
|---|---|---:|---|---|
| `bg_loc_tvb_longmen` | `bg_loc_tvb_longmen.jpg` | ~366 KB | 720×1280 | **19v mirror** from `assets/story/c1/`（同源 MD5）；星河電視台後門／片場後巷；午後；無 logo／無字；無人臉 |
| `bg_c1_tea_restaurant` | `bg_c1_tea_restaurant.jpg` | ~280 KB | 720×1280 | **19v mirror** from `assets/story/c1/`（同源 MD5）；C1 茶餐廳 beat；卡座＋凍奶茶＋油煙；空白牌；無人；與 map `cafe_cha` 分開（chapter key ≠ locId） |
| `bg_loc_cafe_cha` | `bg_loc_cafe_cha.jpg` | ~149 KB | 720×1280 | 金龍茶餐廳 interior（map loc）；晚八〇港式；空白牌／空木框；無人臉；無商標／無水印／無烘焙中文 |
| `bg_loc_agency_ho` | `bg_loc_agency_ho.jpg` | ~174 KB | 720×1280 | 何生事務所；cork **輕 Gaussian／pixelate mush＋soft feather**（紙張形狀保留、文字／臉不可讀；**非**實心米色大方塊）；desk／電話／煙灰缸未動；bak pre=`bg_loc_agency_ho_preblur_bak.jpg`；heavy=`bg_loc_agency_ho_heavysmear_bak.jpg`；無真藝人相／無商標；無人臉 |

## LocId / beat wiring

| key | preferred path | also kept |
|---|---|---|
| `tvb_longmen` → `bg_loc_tvb_longmen` | `assets/story/locs/` | `c1/` · `dialog/` · `bg/` |
| `bg_c1_tea_restaurant`（C1 beat） | `assets/story/locs/` | `c1/` · `dialog/` · `bg/` |
| `cafe_cha` → `bg_loc_cafe_cha` | `assets/story/locs/` | — |
| `agency_ho` → `bg_loc_agency_ho` | `assets/story/locs/` | — |

Preview（?v=19v）`spBgImageCandidates` 先 probe `assets/story/locs/{key}.jpg`；缺檔會 404 再 fallback dialog／c1。本輪補齊 C1 兩檔，停 console 404。

## QC checklist

- [x] 720×1280 vertical
- [x] 無人臉／無英雄 bust
- [x] 無水印
- [x] `bg_loc_tvb_longmen`／`bg_c1_tea_restaurant` HTTP 200 under `assets/story/locs/`
- [x] Soft：agency cork 輕 smear（紙張可見、文字不可讀）
- Soft≠PASS

## Pack

`/workspace/star-volunteer-web-locs-19v-align.tar.gz`
