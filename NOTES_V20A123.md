# NOTES_V20A123 — 表情補圖批（12 張新表情）

## 合併紀錄
- main commit：`1255f18`（squash，基底 v20a119 `76a85d2`）
- 分支：`v123-expr`（已推，commit `2e19339`；合併時 main 先後有 v120／v124／v119 落地，
rebase 兩次：第一次上 `3be1b3d`（v124），第二次上 `76a85d2`（v119）；
v119 合併嗰陣 `test_dlg107/108/109_static.py` 數人頭斷言撞咗，解衝突合併計數見下）
- 線上核實：index.html 5,159,938 bytes，sha `e771c824fc91fe0ed42567727746aee218e1b2baeca81344fc3855a1d70aaeb5`，
同本地一致（v123 零 index.html 改動，index 同 v119 一模一樣）。
新圖線上抽驗：6 張抽驗全部 200＋byte 對數（`awi_s2_surprise` 177,586、
`chung_choning_think` 213,522、`liu_bingxing_shy` 338,292、`awi_angry` 210,264、
`pang_siuki_surprise` 246,352、`ho_sang_angry` 194,260）。
註：推 main 後即檢嗰陣新圖仲係 404（Pages 部署滯後約 2 分鐘，index 啱只係因為
index.html 本身冇變）；等 2.5 分鐘再覆檢，6 張全部 200 對數，部署已出。
- 測試：全套 **171 PASS／12 FAIL**（基線 v119 main＋2 新測試＝170／13，
第 13 個 FAIL 係 `test_dlg123_static.py` 喺 pristine 嘅反證；FAIL 清單其餘 12 項同基線一致，零回歸）。
合併前對 v124 main 亦驗過一次：169／12，零回歸。

## 新圖清單（12 張，`assets/story/fullbody/`，全部焗入米白光邊 RGB(243,233,210)）
| 檔 | 用途（句數） |
|---|---|
| `awi_s2_surprise.webp`／`awi_s3_surprise.webp` | 阿偉 s2／s3 surprise（各 27 句） |
| `awi_s2_sad.webp`／`awi_s3_sad.webp` | 阿偉 s2／s3 sad（各 20 句） |
| `awi_s2_shy.webp`／`awi_s3_shy.webp` | 阿偉 s2／s3 shy（各 14 句） |
| `awi_angry.webp` | 阿偉 angry（4 句；s2／s3 冇自己 angry 圖，候補鏈經呢張先退 base） |
| `chung_choning_think.webp` | 鍾楚凝 think（4 句） |
| `chung_choning_smile.webp` | 鍾楚凝 smile（happy 3 句） |
| `ho_sang_angry.webp` | 何生 angry（4 句） |
| `liu_bingxing_shy.webp` | 廖炳星 shy（2 句） |
| `pang_siuki_surprise.webp` | 彭少祺 surprise（2 句） |

- 出圖：跟 v106／v107 規格，帶風格錨（乾淨二次元動畫風）改現有 base 圖表情；
QC **11 pass／1 marginal（鍾楚凝 think——讀落稍似擔憂，唔同 serious／sad，4 句可用，唔重擲）／0 紅旗**。
`awi_angry` 腿間白楔＋`liu_bingxing_shy` 鞋間白縫已修（`qa123/fix_wedge123.py`，唔使重擲）。
5 張圖邊緣有生成器留低嘅薄米白描邊（顯示尺寸下只係令光邊厚少於 1px，已記錄，唔影響）。
- 覆蓋率（`qa123/coverage123.py`，全語料 2,644 行）：**439／593（74.0%）→ 458／593（77.2%），＋19 句**。
阿偉 s1：188／188（**100%**）；s2／s3：123／188（65.4%）→ 184／188（**97.9%**），
淨返 angry 4 句——runtime 候補鏈行 `awi_angry.webp`，實際顯示 100%。

## 數人頭斷言（合併計數，v119＋v123）
- `assets/story/fullbody/` 總數：118 → v119 加 10 張（影 9＋老臨記 1）＝128 → v123 加 12 張＝**140**。
- 非 boss webp（dlg108／dlg109 重測用）：96 → v119 加 7 張 webp＝103 → v123 加 12 張＝**115**。
- 受影響測試：`test_dlg107_static.py`（140）、`test_dlg108_static.py`（115）、
`test_dlg109_height_static.py`（115）、`test_dlg119_static.py`（128→140）、
`test_dlg123_static.py`（130→140）。全部 PASS。
- index.html、content pack JSON、SAVE key、softRev、產品 `?v=` 零改動。

## 守門測試
- `tests/test_dlg123_static.py`：12 張新資產存在＋WebP 檔頭＋＞50KB＋總數 140＋
檔名規則＋硬編碼句數＋全域增益合計 19＋烘焙報告＋基線不變量。PASS；
pristine 反證 FAIL（缺檔），成立。
- `tests/test_dlg123_logic.js`：12 張首選＋階段判定＋跨階段 angry 後備＋9 句真實對白分類＋反證。PASS；
pristine 上 PASS（只驗解析器，唔驗檔案存在——檔案存在由 static 守門）。

## 實駕（Playwright，本地鏡像，`qa123/drive123*.py`）
- drive123（A/B：pristine dc12744 vs branch）：目標 URL 404 由 **18 → 0**；
渲染見齊 3 張（`awi_angry`、`pang_siuki_surprise`、`chung_choning_smile`），
loader 首選＋fetch 200 全部 12 張 OK，0 pageerror。
教訓：overlay 首句係旁白嗰陣名牌係空嘅，用名牌認星會誤殺真巧遇；
`finish_encounter_if_any` 行嗰陣冇 log srcs——8 張目標其實喺 pristine 嗰陣已經
request 過（18 個 404），branch 嗰陣渲染咗但冇記錄到。
- drive123b（修正版：逢 overlay 行晒＋log 齊 srcs）：渲染見齊 6 張
（s2／s3 surprise＋shy、鍾 think、廖 shy），目標 404＝0，0 pageerror。
搵到嘅場：程天諾初遇（day 612，s2／s3 surprise＋shy）、廖炳星初遇（day 975，shy＋s2 surprise）、
葉敏芝 yip_choice beat（day 516，見 drive123c）。
- drive123c：Yip choice beat（1991 夏＋fav tier≥2）step 16 出 sad 句，
`awi_s2_sad`＋`awi_s3_sad` 兩張齊晒，目標 404＝0，0 pageerror，OVERALL PASS。
- 合計：**11 張巧遇目標全部實機渲染見齊**；`ho_sang_angry` 冇穩定實機路徑（4 句主線），
靠 loader 首選＋fetch 200 驗證。**0 pageerror（三場）**。
- 實駕期間撞到嘅非本批 404（已記錄，唔係回歸）：`ching_tinlok_sad.webp`（＋.png，
程天諾 sad 缺檔，實池 4 句）、`awi_s3_angry.webp`（＋.png，候補鏈試探，設計如此，
之後退返 `awi_angry.webp`）。

## 殘留（下一批）
- 最大缺口全部 ≤5 句：方小龍 happy 5、彭少祺 serious 4、顧明輝 happy 4、葉敏芝 serious 4、
藍若曦 shy 4、程天諾 sad 4（＋上文 `ching_tinlok_sad` 實駕已見 404）。
下一批建議一次過收呢批 4–5 句散項。
- `chung_choning_think` marginal（稍似擔憂）——用戶睇過實機先決定係咪重擲。
- 5 張圖薄米白描邊（見上文）——顯示無礙，留返下次出圖嗰陣留意生成器邊緣。
- `qa123/baked/`（12 張烘焙輸出，同 `assets/story/fullbody/` 重複）留喺工作目錄，未入庫。

## 回滾
- 成個 squash 係一個 commit（`1255f18`）：`git revert 1255f18` 即退返 v119 狀態
（12 張圖＋5 隻測試＋qa123 一併落返嚟；index.html 零改動，舊存檔完全唔受影響，
新圖只係令對話解析器唔再退 base——退返去只係變返退 base，唔會爛檔）。
- 單張圖回滾：刪 `assets/story/fullbody/<檔>.webp` 即可，loader 自動退下一級候補。
