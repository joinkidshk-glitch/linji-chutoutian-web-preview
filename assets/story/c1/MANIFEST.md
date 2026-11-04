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
| `char_hero_bust_raise_brow.png` | `raise_brow` | **firm** (beat 10「我選」) | **2026-11-05 style-lock**：對齊 `hero_awi.jpg`／default 平面動畫 cel-shade（換走半寫實 e99f2dd3）；MD5 `63670d1b`；bak `*_pre_style_lock_bak`；Soft：單側挑眉峰仍可再加強 |

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
| `char_cheung_bust_default.png` | `default` | firm phone (beat 7) | **2026-11-05 style-lock**：對齊 `hero_awi`／default 平面 cel；LOOKS 背心＋黑框眼鏡＋牛仔恤＋聽筒；MD5 `920321c6`；bak `*_pre_style_lock_bak` |
| `char_cheung_bust_raise_brow.png` | `raise_brow` | firm phone 加強 | **2026-11-05 style-lock**：同上身份／服裝；單側挑眉＋額紋；MD5 `5224f3dc`；四路同 MD5；Soft：挑眉峰仍可再加強 |

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
- [x] 人臉大致跟 ref（awi 髮／外套；ho 眼鏡灰西裝；cheung LOOKS 背心／眼鏡／牛仔＋聽筒（style-lock 換走高領半寫實））
- Soft notes: hero `raise_brow` **style-lock 2026-11-05**（動畫風；挑眉 Soft nit）；ho `frown` Soft OK；Soft≠PASS（整體）
- 未產 lan／藍若曦（用戶＋tester 確認）

## Pack

`/workspace/star-volunteer-web-c1-art.tar.gz` → `assets/story/c1/`（＋本 MANIFEST）

## HOLD redo pack (2026-11-04)

`/workspace/star-volunteer-web-hold-redo-hero-vera.tar.gz` — hero raise_brow（＋dialog）＋core Vera×3＋MANIFESTs。Soft≠PASS。

## HOLD redo 2026-11-04 late
- `char_hero_bust_raise_brow.png`：v3 HOLD-redo **PASS**（單側挑眉＋額紋；閉嘴嚴肅）；dialog MD5 `e99f2dd3`；bak 保留。整體 Soft≠PASS；唔 tip LIVE。


## Style-lock redo 2026-11-05 (Asia/Hong_Kong)
用戶點名對話 bust 偏寫實、同 HUD `hero_awi.jpg` 唔同風。
- 準繩：`assets/hero_awi.jpg`＋`char_hero_bust_default.png`（平面動畫 cel-shade）
- 已換：`char_hero_bust_raise_brow.png` MD5 `63670d1b`（c1／story／dialog／npc 同 MD5）
- bak：`char_hero_bust_raise_brow_pre_style_lock_bak.png`（舊半寫實 e99f2dd3）
- Soft：單側挑眉可再加強；Fal／Krea 餘額 0，未做 edit 強化
- Soft≠PASS｜唔 tip LIVE｜89–92 HOLD｜剪影後掛

## Style-lock Cheung pair 2026-11-05 (Asia/Hong_Kong)
- `char_cheung_bust_default.png` MD5 `920321c6`（c1／story／dialog／npc 同 MD5）
- `char_cheung_bust_raise_brow.png` MD5 `5224f3dc`（同上四路）
- LOOKS：~32；粗黑框眼鏡；卡其多口袋攝影背心；洗水牛仔恤袖口捲；原子筆；聽筒（C1 電話戲）
- 準繩：`hero_awi.jpg`＋`char_hero_bust_default.png`；換走 DRIFT_REAL 高領半寫實 bak
- Soft：單側挑眉仍可再加強；原子筆數量偏 1 支；略偏 modern polished anime 線（仍平面 2D）
- 身份 jpg `assets/npc_cheung.jpg` 仍係高領較年長記帳，本輪唔改、唔再開圖
- Soft≠PASS｜唔 tip LIVE｜唔 wake iOS｜89–92 HOLD｜剪影後掛
- Pack：`/workspace/star-volunteer-web-style-lock-cheung.tar.gz`
