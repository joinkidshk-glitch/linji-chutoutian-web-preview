# NOTES v20a201 — 修 v199 設計 review 唯一 C1：s1 全身組闊過 s2／s3

- 分支 `v20a201`，基底 main `2c1a680`（v199 遊戲 `5f5be18`）。**統籌接手後 rebase 上最新 main `2de5026`（v197＋v200 已落地），新 commit `6179b91`，零衝突**——中途 pick 俾 untracked `qa201/samples201/`＋`__pycache__` 阻住（移開先繼續到；samples201 已搬返，唔入 repo）。rebase 後新測試＋相關 5 檔逐個覆驗全部 PASS（見 §6 補註）。落地嗰陣 main 可能再郁（v196 落地緊），要再 rebase 核對。
- 用戶 2026-11-14 00:10 拍板「修，s1 重裁做返同闊」。只做實作＋驗證＋NOTES，**唔落地**（落地由統籌做）。
- 改動：8 張 s1 全身圖全部換新（同路徑覆蓋，loader 零改動）＋`index.html` 1 行（hero_awi bust data URI 換值，行數不變 60711）＋測試 2 新 4 改（見 §6）。
- PixelLab 餘額本票**零消耗**——全身賽璐璐圖沿用 v195／v199 嘅 media pipeline 路線（見 §2）。

## 1. 問題＋量度：重裁唔得，8 張全部要重生

review（`~/workspace/linji-design-review-v199/REVIEW.md` C1）：s1 AR 0.343 vs s2／s3 0.278；932 同高 635.4px 下 serious box 闊 [213.2, 177.7, 192.7]px（s1 比 s2 闊 +20.0%）、angry [218.9, 191.3, 191.3]px（+14.4%）。三張頭頂齊平，係 DLG199 高度正規化（REF AR 0.345）嘅副作用。

**張數更正：review 話 9 張，實際係 8 張**（angry／base／sad／serious／shy／smile／surprise／think；PIL 數過 `assets/story/fullbody/awi_*.webp` 全庫 24 張，s1＝8）。「9」係 review 數錯，8 張全部做齊。

舊圖 PIL 實量（HEAD）：

| 表情 | 舊尺寸 | 舊 AR | 內容 bbox AR（non-cream，alpha>120） |
|---|---|---|---|
| angry | 930×2699 | 0.3446 | 0.335（serious 同款量法：x[20,914] w=895，AR 0.326） |
| base | 480×1400 | 0.3429 | 0.333（半解像度舊檔） |
| sad | 933×2784 | 0.3351 | — |
| serious | 936×2789 | 0.3356 | 0.326 |
| shy | 932×2777 | 0.3356 | — |
| smile | 936×2791 | 0.3354 | — |
| surprise | 936×2786 | 0.3360 | — |
| think | 932×2778 | 0.3355 | — |

**重裁唔可行——逐張驗過，全部改重生**：目標 AR 0.28 要每邊裁 ~77px；診斷圖（`/tmp/qa201/diag_awi_serious_crop028.png`，工作副本外，已刪）顯示裁切線會切左袖＋右手手指＋地面影。米白光邊係圖最外層像素（每行採樣都係 (244,234,210)），裁兩側空白等於裁人物本身。8 張姿勢／構圖近乎同一套（serious vs smile 並排目視姿勢一樣），所以 8 張一致判重生，唔係逐張揀。任務書「唔好靜靜將成組轉晒做重生」——呢度係量度證據話成組都裁唔到，唔係偷懶。

## 2. 重生：media pipeline（唔係 PixelLab），風格錨＋s1 造型

- 路線：跟 v195／v199——PixelLab documented 端點只出 pixel art，唔合 880×3056 乾淨賽璐璐全身圖規格。風格錨 `~/workspace/linji-native-design/style-anchor-awei-anime.jpg`（乾淨賽璐璐、大啡眼、黑碎瀏海、深藍西裝褸＋白恤衫開領、鬆身 bomber 臨記衫）。
- 試點 base 先行：canvas＝舊 `awi_serious.webp` 全解像度＋風格錨；prompt：同一角色／姿勢（左手插袋、右臂自然垂低、面微向右）、中性表情、企位收窄、人物闊 ≈ 高嘅 28%、白底、**唔要地面影**、米白光邊 RGB 243,233,210。結果 784×2800、AR 恰好 0.280、RGB——目視接受（同一個人／同姿勢／同衫、中性面、光邊留返、無影）。
- 其餘 7 張：canvas＝新 base raw＋舊表情檔做面部參照＋錨；prompt「keep this exact figure/pose/outfit/framing, change ONLY the face to [expression]」。表情規格：serious（眉壓低、平嘴）、angry（眉斜壓＋眉心紋、眼眯、嘴角向下、舊 s1 angry 嗰兩點淡紅面印）、sad（眉頭內抬、眼垂、嘴角向下）、shy（淡紅暈、眼望側邊、靦腆笑）、smile（大笑、彎眼）、surprise（眼大、眉抬、嘴微張）、think（眼望上／側邊、一邊眉微抬、平嘴）。raw 全部 832×3024、AR 0.2751。
- 面部對照 strip（`/tmp/qa201/faces_new_vs_old.png`，工作副本外，已刪；上＝新、下＝舊）：8 個表情全部讀得出、互相分明；新面比舊面略為側面，但成組一致。身軀一致性（頸以下 vs 新 base）：mean|d| 7.7–11.4、frac>30 係 5–10%（重生 shading 差異，姿勢一樣）。
- s2／s3 本來就無灰色地面影（量過底部行），重生照要求無影——一致。

## 3. 焗入：`qa201/bake201.py`（改編自 v199 `bake199.py`）

- 白底 flood-cut（near-white＝min≥240、max-min≤15、連通到畫框；米白光邊 max-min=33，安全唔會俾切走）、gaussian feather 0.8、人物掂畫框先 pad 32px 白邊、存 WebP q92。
- AR 正規化到目標 **0.280 ±0.004**，只裁／補**透明側邊 margin**，永遠唔掂人物：base raw 已係 0.2800，唔使郁；其餘 7 張 raw 0.2751，各裁 15px／邊透明 margin → 0.2801。
- 光邊驗證（v107／v199 口徑）：ring 米白 frac ≥0.95、遠處米白 px＝0、畫框透明 ≥0.99、內部 vs raw。
- bake 期間修咗兩個 bug（已入 `bake201.py`）：① 內部對照忘記將 raw RGB 放去 padded canvas 嘅 offset（差值 197.6 假陽性），改用明確 offset `ox,oy = PAD - cut_each + pad_each, PAD`；② 內部差值門檻 <1.0 太嚴（WebP q92 recompression 噪音 ~1.2–1.6），放寬到 <2.0（真錯位會係幾十到幾百）。

逐張結果（全部 OK，`qa201/samples201/bake201_results.json`）：

| 表情 | 舊 AR | 新尺寸 | 新 AR | 人物 bbox（w×h） | figHfrac | 光邊 ring／遠處米白／畫框透明 | 內部差值 |
|---|---|---|---|---|---|---|---|
| base | 0.3429 | 784×2800 | 0.2800 | 730×2747 | 0.981 | 1.0／0／1.0 | 1.247 |
| serious | 0.3356 | 865×3088 | 0.2801 | 789×2968 | 0.961 | 1.0／0／1.0 | 1.629 |
| angry | 0.3446 | 865×3088 | 0.2801 | 787×2960 | 0.959 | 1.0／0／1.0 | 1.594 |
| sad | 0.3351 | 865×3088 | 0.2801 | 787×2965 | 0.960 | 1.0／0／1.0 | 1.584 |
| shy | 0.3356 | 865×3088 | 0.2801 | 787×2966 | 0.960 | 1.0／0／1.0 | 1.625 |
| smile | 0.3354 | 865×3088 | 0.2801 | 788×2963 | 0.959 | 1.0／0／1.0 | 1.611 |
| surprise | 0.3360 | 865×3088 | 0.2801 | 788×2964 | 0.960 | 1.0／0／1.0 | 1.620 |
| think | 0.3355 | 865×3088 | 0.2801 | 792×2960 | 0.959 | 1.0／0／1.0 | 1.639 |

- figHfrac 0.959–0.981，喺現有 s2／s3  spread 入面（s2 angry 0.956、s2 base 1.000）。人物完整：透明底佔比 0.414–0.439（範圍 0.30–0.45），人物唔掂畫框，四角 alpha 皆 0。
- 目視：finals contact sheet（`/tmp/qa201/finals_sheet.png`，工作副本外，已刪）——8 張同一瘦身軀、光邊完整；triple serious（`/tmp/qa201/triple_serious.png`）——s1 唔再明顯闊過 s2／s3（s3 serious 仲略闊，佢本身 AR 0.3032，見 §8）。
- sha（頭 12 位；全 sha 見 `tests/test_awei201_static.py` NEW_S1／OLD_S1）：base 舊 `33138b6679ce`→新 `3472eb79e0ef`；serious 舊 `54d1d2f81cd0`→新 `feafa77b60ba`；angry 舊 `8508c88d22f5`→新 `d9fd6ea920e8`；sad 舊 `edb5c850751c`→新 `b3955b771909`；shy 舊 `5c3f09a1b9c8`→新 `5c0022a27f5d`；smile 舊 `51c51a33e7ee`→新 `eb9e8c14b5ce`；surprise 舊 `51c75ab01233`→新 `13cee91ce5fb`；think 舊 `3e2650f9a353`→新 `2d4ef8776e4d`。

## 4. Bust：hero_awi 由新 base 重焗（跟住換埋）

- `hero_awi` bust 係由 `awi_base.webp` 焗出嚟嘅 PORTRAITS data URI——base 換咗，bust 唔跟會同對話舞台唔一致。
- `qa201/crop201.py`（抄 v199 `crop199.py`，FRAC 0.24、同一恤衫 tweak、淨係 hero_awi；舊記錄 `qa199/crop199.json`）→ `qa201/crop201.json`（1 鍵；box [176,7,683,666]、sha `c7d39ee3c18a…`、8,724 bytes）。舊 vs 新 bust 2× 對照（`/tmp/qa201/bust_old_vs_new.png`，工作副本外，已刪）：同一個人／同 framing／同恤衫處理，新面略為側面——接受。
- `qa201/bake201_bust.py` 焗入 index.html：**1 行改動，行數不變（60711）**；其餘 20 個 bust 零郁，`awi_s3` bust 零郁。

## 5. 快取：同路徑覆蓋，唔改 loader、唔升版本參數

- 查過 fullbody URL 組成：`dlg106Candidates`（L26880）`assets/story/fullbody/{stem}_{expr}.webp?v=20a106`（＋`.png` fallback）；`dlg119Candidates`（shadow）、L60003 start-standee `awi_base.webp?v=20a106`、L53533 tp128 同款。
- 「唔改 `?v=`」紀律指嘅係**頁面 URL `?v=20a10`**（soft index，`index.html` L10–16：「Product?v= stays 20a10」），唔係 asset `?v=20a106`。
- Live 查過：GitHub Pages 派 `awi_base.webp` 帶 `Cache-Control: max-age=600`、ETag、Last-Modified Fri 13 Nov 2026 15:58:08 GMT。
- **決定：同路徑覆蓋，loader 零改動、`?v=` 唔升**——跟 v199 前例（s2／s3 angry 同路徑換，`?v=` 留喺 20a106）；10 分鐘 max-age 即係傳播最多 ~10 分鐘。

## 6. 測試

### 新測試（2 檔，全部 PASS）
- `tests/test_awei201_static.py` — **FAILURES: 0**。釘：8 張 s1 AR ≈0.280（±0.004）、尺寸（base 784×2800、其餘 865×3088）、新 sha＋≠舊 sha、RGBA、四角 alpha 0、透明底 0.30–0.45（實測 0.414–0.439）、米白 ring ≥0.95、遠處米白 0、人物唔掂畫框；bake201 cross-check；16 張 s2／s3 sha 原封不動；DLG199 REF 0.345 ≥ 全庫最大 AR（而家係 s3 serious 0.3032）；bust 對 `crop201.json`；反證（舊 AR＋sha → problems）。
- `tests/test_awei201_logic.js` — **RESULT PASS**。每表情 932／700 painted 闊模型（5 個表情 ≤5px；serious／angry／smile 殘留少過修前一半，見 §8）；s1 組內 spread ≤1px；高度 24 格 AR 表 spread ≤1px（全部配對＋單人）；身高比 1.05／0.85；in-test 反證（舊 s1 AR → serious 35.5px、angry 27.6px > 5px）。
- 反證（pristine fixture，`/tmp/qa201_pristine`，已刪）：抽 HEAD `index.html`＋24 張 HEAD awi 圖＋crop201.json＋bake201_results.json，新 static test → exit 1、**FAILURES: 37，乾淨 FAIL，唔 crash**。logic test 喺 pristine 照 PASS，係 by design（佢測模型＋新 AR 表＋DLG199 code，兩樣 pristine 都有；in-test 反證 §(e) 先係捉 bug 嗰格）。

### 更新測試（4 檔，全部 PASS）
- `tests/test_awei199_static.py` — **FAILURES: 0**。header §③註解；REF floor 0.3446→0.3032；s1 angry AR pin 0.3446→0.2801；`awi_angry.webp` 由 UNTOUCHED 拎走（s2／s3 serious 留返）；check_ref floor→0.3032；§② bust 優先認 crop201.json（hero_awi），crop199 認 awi_s3。註：bake199_results.json cross-check 喺呢個工作副本 skip（檔案喺 linji-work199 samples199，唔喺呢度）——pre-existing conditional skip，唔係 FAIL。
- `tests/test_bust109_static.py` — **FAILURES: 0**。加 crop201 section（hero_awi 優先認 crop201；新 sha ≠ crop201 記錄嘅舊值）。
- `tests/test_dlg108_static.py` — **RESULT PASS**（更新後，見下）。`tests/test_dlg109_height_static.py` — **RESULT PASS**（更新後，見下）。
- `tests/test_awei199_logic.js` 零郁——**RESULT PASS**（hardcoded ARs；DLG199 行為不變）。佢入面 hardcoded s2_angry 0.2880 由 v199 嗰陣已經錯（實際 0.3011），無害，唔喺呢票郁佢。

### dlg108／dlg109：舊測試釘住舊闊度，全套嗰陣捉到，已經更新
- 兩檔原本都釘 `awi base` AR＝0.343——呢個正正係 v201 有意改走嘅數。更新：0.343→0.280（＋v201 註解）。
- dlg108 連帶三個重測數一齊改（闊咗變鬆，係預期好轉，唔係回歸）：阿偉×何生 60% 淨空 20.0px→**52.0px**（範圍 19.0–21.5 → 51.0–53.0）；阿偉×鍾楚凝 33.6px→**65.6px**（32.0–35.0 → 64.5–66.5）；淨空 <12px 配對 120→**115／903**（－5 對）。最闊配對 0.813／上限 ~53% 唔郁（唔關 awi 事）。
- dlg109 其餘三個 gap 斷言（彭少祺／顧明輝 ≥12、方小龍＋Vera <12）唔使改——s1 收窄只會令淨空更大，照 PASS。

### 全套 A/B（`qa131/run_suite.sh`）
- A（pristine main `2c1a680`，worktree `~/workspace/linji-pristine201/`，detached）：**TOTAL PASS 273 FAIL 12**。
- B（工作版，修 dlg108／dlg109 之後重跑 `qa201/suite_work201b.txt`）：**TOTAL PASS 275 FAIL 12**。**FAIL 清單逐行相同**（12 項穩定 pre-existing：flash51／giglib36／pacing35／poster59／rumor49／slot50／soft_tip_111_restore／start53／weave43／weave44／weave49／wrap38），**零回歸**；+2 PASS 啱啱係兩檔新測試。
- B 第一跑係 273／14——多出嗰 2 項正正係 dlg108／dlg109 兩檔（舊 0.343 釘），修好之後清返。A run 第一次用咗相對路徑 outfile（run_suite.sh 會 `cd $ROOT`，outfile 寫唔到），重跑用絕對路徑先攞到 A 清單；A run 本身照跑完（TOTAL 273／12 喺 stdout 見到）。
- 相關測試逐個直接覆驗：awei201 static（FAILURES: 0）、awei201 logic（PASS）、awei199 static（FAILURES: 0）、awei199 logic（PASS）、bust109（FAILURES: 0）、dlg108（PASS）、dlg109（PASS）。

## 7. 實駕（Playwright venv、headless-shell、本地 http.server、LIVE 裸 URL，唔用 `?softPreview=1`）

- `qa201/drive201.py`（port 8998；播種模板 `/home/hatch/workspace/linji-work195/qa195/drive195/save_template.json`，day 400、fame 30、ptm2；ENC79 用 dismiss_encounter 播完）：**66／74 PASS、0 pageerror、0 http fail**。
- 闊度實測（932，Ho 搭檔；boxH 635.4px；base 行用 live boxH × natural AR 模型，因為 base beat 會 render serious 圖，見 §8 ①）：

| 表情 | 932 三 tier 闊 [s1, s2, s3] px | spread | 700 spread |
|---|---|---|---|
| base | [177.9, 176.4, 176.6] | **1.5** ✓ | 1.2 ✓ |
| sad | — | **2.4** ✓ | — |
| shy | — | **2.4** ✓ | — |
| surprise | — | **2.2** ✓ | — |
| think | — | **1.8** ✓ | — |
| serious | [178.0, 177.7, 192.7] | 15.0（殘留，見 §8） | 12.2 |
| angry | [178.0, 191.3, 191.3] | 13.3（殘留，見 §8） | 10.9 |
| smile | [178.0, 182.0, 184.7] | 6.7（殘留，見 §8） | 5.5 |

- 高度 spread 全部 0.0–0.1px（同高不變）；搭檔高度不變；身高比顧明輝 1.050、彭少祺 0.850；單人同高；淨空 ≥12px（最窄 33.5px，700 tier3）；零溢出；遮腿 38–52px（對話框遮腿不變）；表情鏈三 tier 全部正確；s1 自然尺寸驗過。
- 8 項 FAIL 全部係 pre-existing harness 缺陷，同 v199 main drive（44／50）一模一樣，唔係回歸：home bust rect 0×0（`enterHome` 係 IIFE 內部，main drive 直 call 會 throw，屋企永遠唔開）×4；WF4 `wf4DlgCharsHtml108 is not defined`（IIFE 內部）×2；base 闊行因為 base→serious 映射量到 serious ×2（見 §8 ①）。
- `qa201/drive201_sup.py`（port 8997；UI 路徑：#chip-story「進度2」→屋企，返去用 #home-back-map-tabs；強制故事 drain 33–34 clicks）：**14／14 PASS、0 pageerror、0 http fail**。
  - 屋企 bust：rect 56×74 三 tier 一致（932 x358／y282；700 x167／y290）、complete、natW 240、src 對上新 crop201 hero_awi。
  - base 闊 live boxH × natural AR：932 [177.9, 176.4, 176.6] spread 1.5px；700 [145.2, 144.0, 144.1] spread 1.2px。
  - 聽者變暗 live 驗過：講者阿偉 `brightness(1)`、聽者何生 `brightness(0.6)`。
- 舞台截圖目視：`qa201/shots/T1_932_ho_serious_stage.png`（新 s1 瘦身、光邊完整、人物完整、何生變暗、對話框遮腿）vs `T3_932_ho_serious_stage.png`（s3 略闊、同高）。截圖喺 `qa201/shots/`＋`qa201/shots_sup/`。

## 8. 殘留／唔做（跟任務定義）＋要統籌／用戶決定嘅嘢

### 殘留闊度 spread——s2／s3 本身嘅 variance，改 s1 改唔到（**要跟進決定**）
- 修完之後，5 個表情 spread ≤5px 達標；serious 15.0px、angry 13.3px、smile 6.7px 仲超標。但呢三個殘留係 **s2／s3 自己嘅 AR variance**造成（s3 serious 0.3032、s2／s3 angry 0.3011、s3 smile 0.2907），唔係 s1——數學上改 s1 一個人改唔到。s1-vs-s2 serious gap：35.5px → **0.3px**。
- 改善幅度全部 >50%：serious 35.5→15.0、angry 27.6→13.3、smile 31.1→6.7。
- 呢票範圍係 s1 組 only；s2／s3 sha 俾 v199 測試釘死，唔可以順手郁。跟進二揀一：① 接受殘留（最大 15px，約 2.4% 闊度）；② 另開一票裁／重生 s3 serious＋s2／s3 angry（＋s3 smile 視乎門檻）。**任務書「spread ≤5px」係目標，三個表情未達標——如實報，唔扮達標。**

### Pre-existing（唔係 v201 造成，唔喺呢票修）
1. 合成 beat emotion "base" 會 render serious 圖（v199 review §限制#1）：StoryPlay 將 base→serious 映射，舞台上 emotion "base" 嘅 beat 顯示 `awi_*_serious.webp`。base 闊度改用 live boxH × natural-AR 模型喺 sup drive 驗。
2. `enterHome` 係 IIFE 內部——main drive 屋企 check 永遠 FAIL（v199 一樣）；UI 路徑 work（sup drive）。
3. `wf4DlgCharsHtml108` 係 IIFE 內部（index.html L40739）——bare global call 永遠 ReferenceError（v199 一樣）。WF4 code 零郁；static test 釘 onload 字串。
4. DLG199 註解話 REF＝「全庫最大 AR 0.345（s1 angry 930×2699）」——而家過時（最大係 s3 serious 0.3032）。任務書話唔郁 DLG199 code，所以註解留返舊樣，喺呢度記低。

### 唔入 repo
- `qa201/samples201/`（2.0M raw 生成圖＋`bake201_results.json`）唔入 repo，跟 v199 前例（samples199 唔入，留喺工作副本）；`qa201/shots/`（15M）＋`qa201/shots_sup/`（2.9M）照 v199 前例入 repo。`qa201/__pycache__/` 唔入。
- Pristine worktree `~/workspace/linji-pristine201/`（820M，detached HEAD `2c1a680`，淨係跑 suite A 用）——**交貨後要刪**（`git worktree remove --force`），唔好留喺度食 quota。`/tmp/qa201/` 診斷圖已刪；`/tmp/qa201_pristine/` 反證 fixture 已刪。

## 9. 統籌接手

- Commit 內容（`git status` 已核實）：M `assets/story/fullbody/awi_{angry,base,sad,serious,shy,smile,surprise,think}.webp`、M `index.html`、M `tests/test_awei199_static.py`、M `tests/test_bust109_static.py`、M `tests/test_dlg108_static.py`、M `tests/test_dlg109_height_static.py`；新 `tests/test_awei201_logic.js`、新 `tests/test_awei201_static.py`、新 `NOTES_V20A201.md`（本檔）、新 `qa201/`（bake201.py、bake201_bust.py、crop201.json、crop201.py、drive201.py、drive201_report.json、drive201_sup.py、drive201_sup_report.json、suite_pristine201.txt、suite_work201.txt、suite_work201b.txt、shots/、shots_sup/、busts/awi.webp；**唔包 samples201/、__pycache__/**）。
- Commit＋push 分支 `v20a201`（push 去 origin＝常駐 clone 本地路徑，唔係 GitHub；`git add` 明確列出新檔，唔好靠 `git add -u`）。**唔落地**，等統籌。
- 注意：寫 NOTES 期間 MEMORY.md 外部更新話 v197 已半落地（本地 main squash commit `2de5026`，未 push）＋v196 同時落地緊——我個分支基底 `2c1a680` 可能已經唔係最新 main，落地嗰陣統籌要 rebase／核對。
- 落地後驗收建議：curl 核實線上圖係新版（sha 對 §3 表）＋等 10 分鐘 cache 過期後實機睇一次三 tier serious／angry 對比（殘留 spread 見 §8）。
