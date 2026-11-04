# Phase 2 location environments — MANIFEST

> 2026-11-04（Asia/Hong_Kong）  
> LOOKS master: `content/PLAN_CHAR_LOOKS_REF_v1.md`（SHA 48ea7aac… verified）  
> Pipeline: **cursor GenerateImage** → crop/cover **720×1280** JPG q≈85  
> Soft≠PASS。**唔改 LIVE 碼**。**1989–1992 資產 HOLD**。

## Files

| artId / key | file | size | dims | notes |
|---|---|---:|---|---|
| `bg_loc_cafe_cha` | `bg_loc_cafe_cha.jpg` | ~149 KB | 720×1280 | 金龍茶餐廳 interior；晚八〇港式茶餐廳卡座＋凍奶茶＋油煙／蒸氣；空白牌／空木框；無人臉；無商標／無水印／無烘焙中文 |
| `bg_loc_agency_ho` | `bg_loc_agency_ho.jpg` | ~170 KB | 720×1280 | 何生事務所；煙灰缸／劇本紙堆／電話／檯燈＋螢光；香煙煙霧；軟木板字輕改；無真藝人相／無商標；無人臉。SHA256 `43acc91f…` |

## LocId wiring (engine)

| locId | preferred bg key |
|---|---|
| `cafe_cha` | `bg_loc_cafe_cha` |
| `agency_ho` | `bg_loc_agency_ho` |

C1 chapter tea (`assets/story/c1/bg_c1_tea_restaurant.jpg`) 仍作 C1 beat 用；本檔＝**地圖 loc master**，可改進 C1 茶餐廳 vibe。

## QC checklist

- [x] 720×1280 vertical
- [x] 無人臉／無英雄 bust
- [x] 無水印
- [ ] Soft：agency 紙張／corkboard 若有可讀殘影 → 下輪 blur／重出（本輪目檢偏抽象筆觸）
- Soft≠PASS

## Pack

見 `/workspace/star-volunteer-web-phase2-locs-hud.tar.gz`
