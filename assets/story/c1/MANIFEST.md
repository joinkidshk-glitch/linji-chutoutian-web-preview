# C1 UI-test art pack — MANIFEST

> 2026-11-03 (Asia/Hong_Kong)｜用戶開閘測 chapter（t45u）  
> Source brief: `content/ART_BRIEF_C1_UI_TEST_v1.md`  
> Pipeline: **cursor GenerateImage**（Krea Free compute = 0，未呼叫 Krea）  
> Soft ≠ PASS。無 `char_lan`／藍若曦。未 wake iOS。

## Layout note (iOS stage)

- **bg**: full stage cover-crop；vertical-friendly 9:16 (`720×1280`)
- **bust**: ~38% width，max **148px** 寬；aspect **3:4**；`object-position: top`
- Engine: beat.`bg` → beat.`locId` → node.`locId`=`tvb_longmen` → `bg_loc_tvb_longmen`

## Backgrounds

| file | artId / key | use | notes |
|---|---|---|---|
| `bg_loc_tvb_longmen.jpg` | `bg_loc_tvb_longmen` | B01／C1 預設 loc；system beat 0 | 星河電視台後門／片場後巷；午後；無 logo／無字 |
| `bg_c1_tea_restaurant.jpg` | `bg_c1_tea_restaurant` | B02＋對白主場；system／dialogue 茶餐廳 | 卡座＋凍奶茶＋油煙；空白牌；無人 |

## Busts `{artId}_bust_{expression}.png` · 864×1152 · cream studio

### char_hero（阿偉／awi）— ref `assets/hero_awi.jpg`

| file | expression | emotion map (script) | notes |
|---|---|---|---|
| `char_hero_bust_default.png` | `default` | neutral／tense→default (beat 8) | 輕微笑 |
| `char_hero_bust_eyes_down.png` | `eyes_down` | **worried** (beat 4) | 垂眼手頭緊 |
| `char_hero_bust_frown.png` | `frown` | tense／worried alt | 皺眉繃緊 |
| `char_hero_bust_raise_brow.png` | `raise_brow` | **firm** (beat 10「我選」) | Soft：表情偏自信微笑，可後輪加強眉峰 |

### char_ho（何生／ho_sang）— ref `assets/npc_ho.jpg`

| file | expression | emotion map | notes |
|---|---|---|---|
| `char_ho_bust_default.png` | `default` | firm→default (beat 2) | calm 微笑 |
| `char_ho_bust_raise_brow.png` | `raise_brow` | firm (beat 3 兩條路) | 揚眉叮囑 |
| `char_ho_bust_frown.png` | `frown` | firm／serious (beats 5,9) | Soft：邊緣偏淡，可用 raise_brow 補強 |

**warm／smile**：未另產 `char_ho_bust_smile.png` → **warm → `default`**

### char_cheung（張子駿／cheung_tsijun）— ref `assets/npc_cheung.jpg`

| file | expression | emotion map | notes |
|---|---|---|---|
| `char_cheung_bust_default.png` | `default` | firm phone (beat 7) | 聽筒＋側光 |
| `char_cheung_bust_raise_brow.png` | `raise_brow` | firm phone 加強 | 聽筒＋揚眉嚴峻 |

`firm` 臉 → 用 `raise_brow`（或 `default`）

## Emotion → expression aliases（wiring）

| emotion (JSON) | preferred expression file |
|---|---|
| neutral | `*_bust_default` |
| worried | `*_bust_eyes_down`（hero）／`frown` |
| tense | hero → `default` 或 `frown` |
| firm | `raise_brow`；ho serious → `frown` |
| warm | ho → `default` |

## Also delivered

| file | use |
|---|---|
| `story_c1_pack_preview.jpg` | moodboard collage 預覽 |
| `assets/dialog/` mirror | 同上 bust／bg 檔名副本，方便引擎佔位 |

## QC

- [x] 無烘焙亂碼中文／商標
- [x] 人臉大致跟 ref（awi 髮／外套；ho 眼鏡灰西裝；cheung 高領＋聽筒）
- Soft notes: hero `raise_brow`、ho `frown` 表情差可再 sharpen；Soft≠PASS
- 未產 lan／藍若曦（用戶＋tester 確認）

## Pack

`/workspace/star-volunteer-web-c1-art.tar.gz` → `assets/story/c1/`（＋本 MANIFEST）
