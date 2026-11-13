# v170 Phase 1 — 提名卡人像接入路徑（用戶拍板全套先做，呢份只係路徑，唔係實作）

## 渲染點（邊個函數）

- 卡列由 `awards62PlayCeremony`（`index.html` L46141 起）內 L46171–46181 起 `cardsData`＋`cardsHtml`。
- `cardsData`：阿偉一張（`me: true`，`poster: posterOf(pack.repGigId63)`）＋每位 fellow 一張（`poster: f.poster || posterOf(f.gigId)`）。
- `cardsHtml`（L46176–46179）：media 係 `<img poster>` 或 `<div class="awd63-csscard">《作品名》</div>`，之後 `.t`（作品名）＋`.s`（人名）。
- **接入點就係呢度**：fellow 卡嘅 media 由「作品海報／csscard」改做「人像圖」。最小改動：`cardsData` 每位 fellow 加 `portrait` 欄（`starId → 圖路徑` 對照表），`cardsHtml` 嘅 media 分流改做「有 portrait 先出人像 img，否則沿用而家 poster／csscard」——咁未齊圖嘅星自動跌返現況，唔會穿窿。
- 顯示時機唔使改：`syncCards`（L46339–46346，names／suspense／reveal／comfort 期間 `.on`，逐張 `200 + i*380ms`）＋`syncGlamour`（v168，glamour 期間 `visibility:hidden` 留位）照舊。
- **注意 v149 未落地**：v149 B3 已經改咗 csscard 結構（媒介圖標＋典禮名，唔再印片名）＋卡加 `win` 旗／🏆角標。接入一定要建基於**落咗地嘅 v149 結構**做（人像取代邊個區——成個 media 定圖標區——要同 v149 B3 一齊定），唔好喺 v149 之前自立一套。另見 INVESTIGATION.md §D3（glamour overlay rebase 衝突）。
- **語義決定（要拍板）**：media 區而家係「作品」位；放人像即係卡面由作品變人物，作品海報唔再出現。定係人像＋作品名並存（要改卡結構／卡高），唔係工人決定。

## 圖放邊、咩尺寸

- 建議新目錄 `assets/story/awards/portraits/`（典禮卡片專用，唔同 `assets/story/fullbody/`／`assets/story/era_stars/` 混埋）：
  - bust 裁切路線：`<starId>_card.png`，2:3，建議 240×360（卡面顯示 78×117，2× 留餘量；v109 bust 係 240×312 WebP q80 同級做法）。
  - Pixellab 路線：`<starId>_pixel.png`，south 幀原檔 128×128（透明底），顯示嗰陣 `object-fit: cover`＋`image-rendering: pixelated`；注意卡面 `img` 預設底係 `#2b2118` 深啡——透明像素圖會坐喺深底上面，樣本頁 (c) 就係呢個效果。
- 卡本身唔使改尺寸：`.awd63-card` 88px 闊、`img` `aspect-ratio: 2/3`＋`object-fit: cover`、`.t` 11px 高 30px、`.s` 10px 高 15px，照舊。

## 要幾多個 character／state（Pixellab 路線先計）

- 每位池星 **1 個 character**（`create-character-v3`，from-scratch，128×128，8 方向，`view: side`，`template_id: mannequin`，`no_background: true`）。
- **state 唔使另外開**：character 本身個預設 state（`Idle`）嘅 south 幀就係企立圖；動畫／行幀卡片用唔著。
- 實測單價：**3 次／個**（公式 1 pixen＋ceil(128²×8／65536)＝1＋2；廖炳星實測 4576→4573，job 用量 `usage.generations: 3.0`）。10 位約 **30 次**，餘額 4,573 夠用（佔 0.7%）。
- 阿偉卡去留要拍板：佢已有 v2 character（`49907fa9-077f-4f59-aaba-45d3a06958fb`，128×128，8 方向），換像素 0 次新生成；唔換就像素 fellow＋海報阿偉並存，風格仍然唔統一（樣本頁已示範）。

## 其餘 9 位池星點算

| 星（live id） | 現成 bust | 做法 |
|---|---|---|
| 陸柏言 `luk_baakyin` | 有（864×1152） | bust 裁切，0 次；或 Pixellab 生成，3 次 |
| 廖炳星 `liu_bingxing` | 有（864×1152） | **已做樣本**：bust 裁 `liao_bust_crop_2x3.png`（504×756）＋Pixellab character `1c3c608c-f6ed-4c1b-8edd-4b9cae2cba7e` south 幀 |
| 駱家聲 `lok_gasing` | 有（864×1152） | 同上 |
| 魏詠男 `ngai_wingnaam` | 有（864×1152） | 同上 |
| 蘇芷茵 `so_jiyan` | 有（864×1152） | 同上 |
| 葉敏芝 `yip_manji` | 有（864×1152） | 同上 |
| 齊鎮海 `chai_zanhoi` | 冇 | 零生成方案：fullbody `_base.webp`（711×2394）裁頭肩，v109 同款；或 Pixellab 生成，3 次 |
| 鍾楚凝 `chung_choning` | 冇 | 同上（fullbody 825×2448） |
| 顧明輝 `gu_mingfai` | 冇 | 同上（fullbody 604×2604） |
| 麥震東 `mak_zhendong` | 冇 | 同上（fullbody 426×1408） |

- **零生成全套（路線 1）**：6 位 bust 裁切＋4 位 fullbody 裁頭肩，Pixellab 成本 0 次；每張要逐張定裁切框（每人體型／頭位唔同，fullbody 尺寸由 426×1408 至 904×2364）。
- **Pixellab 全套（路線 2）**：10 個 character，約 30 次；逐位用各自 brief 生成（prompt 永禁真人姓名；brief 檔 4 個 id 錯字警告：`mak_jandung`→`mak_zhendong`、`chai_janhoi`→`chai_zanhoi`、`ching_tinok`→`ching_tinlok`、`pang_siugei`→`pang_siuki`——跟 live id，唔跟 brief 檔）。
- **混合（路線 3）**：fellow 用 bust／fullbody 裁切、阿偉卡留海報——接受海報 vs 人像唔同類，成本 0 次。
- 驗收（Phase 2 實作嗰陣）：每位星卡面實駕核實——面同對應 fullbody base 係咪同一張面（v138 A1 衫／髮走樣教訓）、2:3 框有冇裁走關鍵部位、像素路線面部可讀性（廖炳星樣本：全身 128px 入 78×117 框，面約 18px 高，表情弱——全套行像素路線要預呢個 trade-off，或者改試像素頭像特寫做法）。

## 唔做嘅嘢

- 舞台 Q 版 sprite（`AWARDS64_SPRITES`，10 位齊企姿＋walkA／walkB）唔使生成；企位修正（FLOOR 194→~155）係另一組工人嗰條線。
- 唔掂 `index.html`、唔改 content pack JSON；呢份文件本身唔係 code。
