# v20a109 B・舊 bust 換新（列表縮圖）

> 範圍：`index.html` 嘅 `PORTRAITS` map（7 個內嵌 base64 JPEG 舊頭像）換成由
> v106/v107 全身基本款裁出嘅頭肩縮圖；人情頁每一個角色（6 NPCS＋12 紅星）
> 都要有新圖；阿偉頁頭像跟成長級數。**唔掂對話舞台身高比（A 線）**。
> Base：main `546007d`（v108）。分支 `v109-bust`，由 main 開出，只 push 分支，唔合併。
> 紀律：SAVE key `starVolunteer_map_v19w`／softRev `s107`／產品 `?v=` `v20a10` 全冇郁；
> content JSON 一律唔改；唔重新生成任何圖（裁切 only）。

## 1. 消費者審計表（grep 實證，全部取值）

### PORTRAITS（7 鍵，舊值全數換走）

| 消費者 | 位置 | 用法 | 改動 |
|---|---|---|---|
| 手帳頁頭阿偉像 `#home-awi`（56×74px） | `enterHome` L36399 | `img.src = PORTRAITS.hero_awi` | **改**：行 `bust109HeroSrc()`（跟級數，見 §4）；其餘不變 |
| 傾談 modal `.dlg-portrait`（≤180×240） | `doTalk` L55386＋3 個 modal 分支 | `PORTRAITS[npc.face]` | 零改動（key 不變，值換新即生效） |
| 手帳人情頁 `.people-row`（40×52px） | `people72Html` L56057 | `PORTRAITS[n.face]` | 零改動（同上） |
| 開局畫面 `#start-hero`（`hidden`） | boot L57168 | `PORTRAITS.hero_awi` | 零改動（隱藏元素；boot 時 tier 必然係 0→s1，同新值一致） |
| 開局導入 modal 後備 | `showB01HomeModal` L56668 | `uiIcon("start_guide") \|\| PORTRAITS.hero_awi` | 零改動（`start_guide` 恆真，後備從未觸發；即使觸發都係新圖） |
| 舊 story-play bust 後備鏈 | `spBustCandidates` L26649 | `PORTRAITS[pk]`（`pk` 來自 `SP_SPEAKER_REG.portraitsKey`，7 個有 key 嘅講者） | 零改動（鏈尾自動出新圖；見下註） |
| （定義） | L5234–5241 | 7 鍵：`hero_awi`、`npc_cheung`、`npc_chow`、`npc_ho`、`npc_ko`、`npc_lin`、`npc_vera` | 7 行值全換：JPEG → WebP 裁圖 |

註：`spBustUrl` 嗰條舊分支（L27330）而家只會喺**冇全身圖嘅泛稱講者**
（`generic_crew` 等 10 個，全部唔喺 `DLG106_GAZE`）先行到，而嗰啲講者
`spBustUrl` 一早回 `""`（行剪影「影」），唔經 PORTRAITS。全部 19 個具名
`SP_SPEAKER_REG` 講者都有全身圖，行 DLG106 分支；PORTRAITS 喺 story-play
只係 `spDlgCharsHtml` 候補鏈尾（L27032）——新值令條尾都唔會再跌返舊圖。

### `n.face` 全部取值（NPCS，6 個）

| NPCS id | 名 | `face` | 全身基本款 | 新縮圖 |
|---|---|---|---|---|
| colleague | 林曉晴 | `npc_lin` | `lin_hiu_base.webp` | PORTRAITS.`npc_lin` |
| director | 張子駿 | `npc_cheung` | `cheung_tsijun_base.webp` | PORTRAITS.`npc_cheung` |
| stylist | Vera | `npc_vera` | `vera_base.webp` | PORTRAITS.`npc_vera` |
| rival | 高俊傑 | `npc_ko` | `ko_chunkit_base.webp` | PORTRAITS.`npc_ko` |
| reporter | 周采兒 | `npc_chow` | `chow_choiyi_base.webp` | PORTRAITS.`npc_chow` |
| agent | 何生 | `npc_ho` | `ho_sang_base.webp` | PORTRAITS.`npc_ho` |

6 個 face 值全部喺 PORTRAITS 入面，零缺圖。

### 人情頁紅星段（12 星，唔經 PORTRAITS）

`enc79PeopleHtml`（L51153）已見紅星行 `enc79StandCandidates`：首選
`assets/story/era_stars/<id>_stand_default.png`（v105 舊企立圖，864×1152），
未見過行剪影。呢段如果唔郁，人情頁上半截新圖、下半截舊圖——所以今包一併換：
`enc79PeopleHtml` 加 3 行，`BUST109_EXTRA[def.id]`（新裁圖）`unshift` 入
`cands` 做首選，舊企立圖退做 `onerror` 後備（`cands[1]`）。**冇改
`enc79StandCandidates` 本身**，巧遇候補鏈（`enc79PlayEncounter`）原封不動。
未見過嘅紅星**維持剪影**（刻意嘅「未揭面」狀態，唔係缺圖——見 §5 註）。

### UI40_STAND（10 個舊企立 WebP，審計結果：仲用緊，但今包唔掂）

| 消費者 | 位置 | 用途 | 处置 |
|---|---|---|---|
| `spBustUrl` 首選 | L26661 | 舊 story-play：10 個講者優先出企立圖 | 唔郁（只係 DLG106 候補鏈尾） |
| WF4 對話後備鏈尾 | `wf4DlgExtraCands108` L39396（awi） | WF4 獨角阿偉後備 | 唔郁 |
| 紅星企立後備 | `enc79StandCandidates` L50999（`luk_baakyin`） | 巧遇後備第 4 候選 | 唔郁 |
| 巧遇阿偉後備鏈尾 | `extraCands106` L51042（awi） | 巧遇後備 | 唔郁 |
| 開局畫面企立 | boot L57171 `#start-standee` | **開始畫面可見嘅阿偉企立（舊圖）** | 唔郁（見下註） |

註：`UI40_STAND.awi` 喺開始畫面仍然係可見舊圖。換佢要成張全身圖唔係頭肩裁圖，
超出 B 線「列表縮圖」範圍；v108 S-5 已將開局導入圖換咗新全身（`b01GuideHtml108`），
`start-standee` 本身留低——交統籌決定係咪另開一包（估計一行：`src` 指去
`assets/story/fullbody/awi_base.webp`，但要驗 CSS 幾何 `height:min(44%,372px)`）。
`UI40_STAND` 其餘 9 個只喺深層後備鏈出現（全身圖齊全嗰陣唔會渲染），
留返同 start-standee 一齊處理，唔喺今包逐個拆。守門測試釘死 10 鍵原封不動，
防誤改。

## 2. 新縮圖清單（21 張，邊個角色對邊張圖）

全部由 `assets/story/fullbody/*_base.webp` 裁出（基本款，neutral 表情），
240×312 WebP q80，米白底 `#F2EBD8`（見 §3）。檔案＋hash 見 `qa109b/crop109.json`；
裁出嘅 WebP 原檔留喺 `qa109b/busts/` 供核對（index 入面嘅值就係呢批嘢嘅 base64）。

| 用途 | Key | 來源全身圖 | WebP bytes | b64 字元 |
|---|---|---|---|---|
| PORTRAITS.`hero_awi`（阿偉 s1） | `awi` | `awi_base.webp` | 8,016 | 10,688 |
| PORTRAITS.`npc_cheung`（張子駿） | `cheung_tsijun` | `cheung_tsijun_base.webp` | 11,182 | 14,912 |
| PORTRAITS.`npc_chow`（周采兒） | `chow_choiyi` | `chow_choiyi_base.webp` | 14,208 | 18,944 |
| PORTRAITS.`npc_ho`（何生） | `ho_sang` | `ho_sang_base.webp` | 10,990 | 14,656 |
| PORTRAITS.`npc_ko`（高俊傑） | `ko_chunkit` | `ko_chunkit_base.webp` | 10,714 | 14,288 |
| PORTRAITS.`npc_lin`（林曉晴） | `lin_hiu` | `lin_hiu_base.webp` | 14,932 | 19,912 |
| PORTRAITS.`npc_vera`（Vera） | `vera` | `vera_base.webp` | 8,924 | 11,900 |
| BUST109_EXTRA.`awi_s2`（阿偉 s2） | `awi_s2` | `awi_s2_base.webp` | 7,080 | 9,440 |
| BUST109_EXTRA.`awi_s3`（阿偉 s3） | `awi_s3` | `awi_s3_base.webp` | 6,566 | 8,756 |
| BUST109_EXTRA.`luk_baakyin`（陸柏言） | — | `luk_baakyin_base.webp` | 5,610 | 7,480 |
| BUST109_EXTRA.`liu_bingxing`（廖炳星） | — | `liu_bingxing_base.webp` | 14,896 | 19,864 |
| BUST109_EXTRA.`ngai_wingnaam`（魏詠男） | — | `ngai_wingnaam_base.webp` | 8,730 | 11,640 |
| BUST109_EXTRA.`yip_manji`（葉敏芝） | — | `yip_manji_base.webp` | 12,176 | 16,236 |
| BUST109_EXTRA.`mak_zhendong`（麥震東） | — | `mak_zhendong_base.webp` | 6,836 | 9,116 |
| BUST109_EXTRA.`lok_gasing`（駱家聲） | — | `lok_gasing_base.webp` | 11,878 | 15,840 |
| BUST109_EXTRA.`pang_siuki`（彭少祺） | — | `pang_siuki_base.webp` | 12,640 | 16,856 |
| BUST109_EXTRA.`chung_choning`（鍾楚凝） | — | `chung_choning_base.webp` | 13,380 | 17,840 |
| BUST109_EXTRA.`gu_mingfai`（顧明輝） | — | `gu_mingfai_base.webp` | 7,700 | 10,268 |
| BUST109_EXTRA.`so_jiyan`（蘇芷茵） | — | `so_jiyan_base.webp` | 8,528 | 11,372 |
| BUST109_EXTRA.`chai_zanhoi`（齊鎮海） | — | `chai_zanhoi_base.webp` | 7,266 | 9,688 |
| BUST109_EXTRA.`ching_tinlok`（程天諾） | — | `ching_tinlok_base.webp` | 7,872 | 10,496 |

合計 21 張，b64 總共 **280,192 字元**；舊 7 張係 235,593 字元——
成套 21 張新圖只係比舊 7 張多 **44,599 字元**（`index.html`
5,023,304 → 5,070,946 bytes，+47,642，+0.95%）。
舊 `hero_awi` 一張已經 98,871 字元，新嘅只係 10,688。

## 3. 技術取捨：繼續內嵌 base64，唔行資產檔案路徑

決定：**PORTRAITS 繼承內嵌 base64（今次換成 WebP 值）；新增 `BUST109_EXTRA`
map 同樣內嵌。** 理由：

1. **後備鏈語義依賴 `data:` URI。** `spBustCandidates`／`spBustUrl` 視
   `data:` 開頭為「必定存在、優先回傳」，而且 `spBustFallbackAttr` 會將
   `data:` 值排除出 fallback 清單。改行資產路徑會令呢個保證命中跌落一串
   可能 404 嘅舊 bust 檔案（era／core／npc／story／dialog）後面，舊
   story-play 分支會多咗 404 閃爍——為咗一張縮圖去重寫條鏈，唔值。
2. **零 fetch、零 404 面。** 人情頁／傾談 modal／頁頭係最高頻畫面；
   內嵌圖同 `index.html` 一齊到，離線／file:// 都得，唔使驗載入＋快取。
3. **體積唔係問題。** 見 §2：21 張新圖總共先多 44,599 字元，仲細過
   MAP97 之前內嵌地圖嗰級。資產路徑慳返嘅 280KB（~5.5%）唔值得用上面
   兩點去換。
4. **沿用現有慣例。** 細頭像（PORTRAITS／UI40）一向內嵌；大圖（地圖、
   全身、場景）行資產路徑——今包守呢條分界，唔係開新例。

代價（老實寫）：`index.html` 大咗 0.95%；以後換 bust 要改 code 唔係換檔。
兩點都係已知且接受範圍內。

## 4. 裁切幾何（實量，唔係估）

量度（`qa109b/measure109.py` → `measure109.json`）：21 張基本款嘅人物
由頭到腳幾乎佔滿成個畫布高（`fig_h_frac` 0.996–1.000），頭頂 y≈0–4px；
頭闊喺 y=2% 約 158–209px，肩膊由 y≈20% 起急速闊開（y=30% 闊 418–651px）。
所以唔使搵頭——頭就係圖頂。

統一一條規則（`qa109b/crop109.py`，零 per-character 例外）：

- `Hc = 0.30 × fig_h`（頭＋肩到胸口中段；0.28／0.32／0.36 三方對照見
  `qa109b/crop_compare.png`——0.28 面太大、何生舉手入鏡；0.36 面太細，
  40px 顯示嗰陣認唔到；0.30 係中間點）
- `Wc = Hc × 10/13`（顯示比例 40:52；傾談 modal 3/4 會輕微裁邊，唔穿幫）
- `top = max(0, fig_top − 0.01×fig_h)`（實測全部係 0，頭髮唔裁）
- `cx = 頭帶中心 x`（y=2%–12% 不透明像素嘅 centroid x；全部 ≈0.50，
  側身嘅程天諾／顧明輝都置中）
- `left = clamp(cx − Wc/2, 0, W − Wc)`（廖炳星、顧明輝掂到 0 邊界，
  驗過面唔出框）
- 底：不透明米白 `#F2EBD8`（同 era-star bust 底色、舊 JPEG 頭像觀感一致；
  焗入圖嘅米白光邊喺呢個底上面自然隱形，唔會有光暈）
- 輸出：LANCZOS 縮到 **240×312**（人情頁 40×52 嘅 6x、頁頭 56×74 嘅 ~4.3x、
  傾談 modal 最大 180×240 嘅 1.33x、舊 story-play bust 最大 148px 嘅 1.6x），
  WebP q80。

QC：21 張接觸表 `qa109b/contact_busts.png` 逐張目檢——面全部入框置中、
冇裁頭／裁下巴／裁面邊；何生舉手喺 0.30 剛好出框，唔會半隻手吊喺邊。
`qa109b/contact_bases.png` 係 21 張全身原圖對照。

## 5. 阿偉 s1/s2/s3 規則

跟現行 `dlg106AweiStem()` 同一條規則（`enc79PlayerTier`：0 臨記／1 配角／
2 主角／3 天王），唔另起一套：

| tier | 頁頭像 | 來源 |
|---|---|---|
| 0、1 | s1＝`PORTRAITS.hero_awi`（`awi_base`） | 舊 key 原值換新 |
| 2 | s2＝`BUST109_EXTRA.awi_s2` | 新增 |
| 3 | s3＝`BUST109_EXTRA.awi_s3` | 新增 |

實作：DLG106 模組內加 `bust109HeroSrc()`（跟 `dlg106AweiStem` 隔籬，
`enc79PlayerTier` 未載入／拋錯／`BUST109_EXTRA` 缺失嗰陣全部退 s1，
兩邊都冇先回 `""`）；`enterHome` 改行佢（一行）。開局畫面 `#start-hero`
（`hidden`）留喺 `PORTRAITS.hero_awi`——boot 嗰陣未讀檔，tier 必然係 0，
s1 係正確值，唔使郁。

註（未見紅星剪影）：12 星入面得 5 個有 `*_silhouette_far.png`
（陸／廖／魏／葉／蘇）；其餘 7 個未見嗰陣 `eraSilhouetteFarSrc` 回空，
嗰行唔出圖——係舊有行為，唔係今包缺圖。實駕對照用蘇芷茵做未見
（有剪影檔，驗到 0.55 透明剪影仲喺度）。

## 6. 改前／改後截圖（`qa109b/shots/`）

實駕 `qa109b/drive109.py`（390×844，Playwright，槽 3；同一個 save 先後行
pristine 同新版，state 完全相同：6 NPCS 好感 55、12 紅星 fav 參差）。

| 截圖 | 內容 |
|---|---|
| `people_before_top.png` | 改前人情頁頂部（6 NPCS 舊 JPEG＋頁頭舊阿偉） |
| `people_after_top.png` | 改後人情頁頂部（6 NPCS 新圖＋頁頭新阿偉 s1） |
| `people_before_s0/s1/s2.png` | 改前全列表分段（s0 頂行、s1 中段紅星、s2 尾段） |
| `people_after_s0/s1/s2.png` | 改後全列表分段（同上；18 行全部入鏡） |
| `people_before_full.png`／`people_after_full.png` | full_page 截圖（註：`#people-list` 係內部捲動容器，full_page 只捉到 viewport——全列表目檢以 s0–s2 分段為準） |
| `talk_after.png` | 傾談 modal（何生新圖，180px 闊，清晰） |
| `hero_t0/t2/t3.png` | 頁頭像 tier 0／2／3（s1 藍褸／s2 灰西裝／s3 深藍西裝，肉眼可分） |
| `compat_before_saved.png`／`compat_after_restored.png` | 舊檔相容前後 |

改前實測：NPCS 全部 `data:image/jpeg` 320×426；紅星全部
`*_stand_default.png` 864×1152。改後實測：17 個已見角色全部
`data:image/webp` 240×312（`complete=true`）；未見蘇芷茵維持剪影。

## 7. 測試結果

### 新守門測試（2 檔，全部 PASS）

- `tests/test_bust109_logic.js`（47 項）：抽 DLG106 模組真身 eval，
  tier 0／1→s1、2→s2、3／99→s3；EXTRA／PORTRAITS 缺失／兩邊都冇／
  `enc79PlayerTier` 拋錯全部唔 crash 且有確定回值；全部回值係真 WebP
  data URI（RIFF／WEBP 檔頭）；反證 tier 2↔3 回值跟住變、三階段互不相同。
- `tests/test_bust109_static.py`（159 項）：舊 7 鍵行 sha256＋200 字元
  b64 前綴零殘留（hash／長度比對，舊指紋寫死＋同 `qa109b/old_portraits.json`
  交叉比對）；21 張全部 WebP 240×312、sha256 同 `qa109b/crop109.json`
  一致；NPCS 6 face／紅星 12 個全部有對應鍵；21 張全身基本款喺磁碟；
  接線（`bust109HeroSrc`、enterHome、紅星 `unshift`、4 個 PORTRAITS
  消費者、fallback 鏈、UI40_STAND 10 鍵原封不動）；反證（checker 食舊值／
  缺鍵必須報問題；抽走 `crop109.json` 一項必須 FAIL）。
- 兩檔喺 pristine main 上跑**會 FAIL**（logic 乾淨 FAIL 1 項、
  static FAIL 15 項），反證成立。
- `node --check`（主 script 抽出）：PASS。

### 附帶修復：`tests/test_ux68_static.py`

全套初跑嗰陣佢係唯一新 FAIL：佢用 JPEG-only regex 抽 `hero_awi`
量長度（原意：hero 唔好超過 100,000 bytes raw）。新 hero 係 WebP，
regex 抽唔到 → 0 → FAIL。修法：regex 改收 `jpeg|webp`，上限
100,000 不變（新 hero raw 8,016 bytes，通過幅度更大）；label 加
「v109 WebP 8,016」註明。修完喺新版 PASS，喺 pristine（舊 JPEG）亦
繼續 PASS——冇放寬到任何嘢。

### 全套 A/B

| | PASS | FAIL | FAIL 清單 |
|---|---|---|---|
| 基線（`qa109b/suite_baseline109b.txt`，未改動） | 142 | 12 | flash51／giglib36／pacing35／poster59／rumor49／slot50／soft_tip_111_restore／start53／weave43／weave44／weave49／wrap38（已知環境性 static FAIL） |
| 工作版（`qa109b/suite_work109b.txt`） | **144** | **12** | 同左，逐字相同 |

+2 PASS 就係兩隻新測試檔；**零新增回歸**。

### 實駕（`qa109b/drive109.py`，`drive_log109.json`）

**OVERALL PASS: True，零 pageerror。** 10 項全綠：改前 NPCS 全 JPEG／
改前 18 行／改後 18 行／改後 NPCS 全 WebP 240／改後紅星全 WebP 240／
未見維持剪影／舊檔相容（money 109109、dayIndex 3、mark 還原）／
頁頭 tier 0／2／3 sha 全部 match／傾談 modal WebP 240／零 pageerror。

實駕中途捉到一個 harness 假失敗（老實交代）：第一次 run 嘅 AFTER 全版
仲係舊圖——唔係遊戲問題，係 Chromium HTTP cache：換 server 後用同一個
URL `goto`，瀏覽器攞返 cache 嘅舊 `index.html`（v107 嗰次 index 零改動，
所以撞唔到）。修法：換 server 後用 `&nocache=109b` 再入（localStorage
按 origin 計，query 唔影響存檔）；重跑即 PASS。教訓已寫入 drive 註解。

## 8. 未達標位／留畀統籌

- **開始畫面企立 `UI40_STAND.awi` 仲係舊圖**（見 §1）：換法估計一行
  （`src` 指去全身 `awi_base.webp`），但要驗 CSS 幾何，唔喺 B 線範圍，
  等統籌開包。
- **`UI40_STAND` 其餘 9 張**只喺深層後備鏈出現（全身齊全嗰陣唔渲染），
  同上，一併留返。
- **未見紅星嗰 7 個冇 `*_silhouette_far.png`**（程天諾等）：未見嗰行
  唔出圖（舊行為，唔係今包引入）；要唔要補剪影，唔喺 B 線範圍。
- **對話舞台身高比（A 線）**：完全冇掂——`index.html` diff 得 4 個 hunk，
  全部喺 PORTRAITS／BUST109／enterHome／紅星段，冇任何舞台幾何改動。
