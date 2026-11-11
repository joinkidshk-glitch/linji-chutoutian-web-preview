# NOTES_V20A109_HEIGHT — v20a109 A 線：對話舞台 per-character 身高比

- 分支：`v109-height`（由 main `546007d`＝v108 開出；工作副本 `~/workspace/linji-work109a/`）
- 範圍：只做 A 線（身高比）。PORTRAITS／舊 bust 一律唔掂（B 線另一工人做緊；靜態測試只斷言 PORTRAITS map 仲喺度）。
- 唔改 SAVE key／softRev／`?v=`。唔加圖（真檔仍係 96 張）。

## 問題（已核實）

v108 之前對話舞台將每個人縮放到同一高度（基礎高 60%），身高差完全唔見。
用戶 2026-11-12 實玩巧遇彭少祺段：彭生應該較矮，而家同阿偉一樣高，比例奇怪。
實駕 pre 證實：阿偉×彭少祺首句「哎，收工啦收工啦，各位辛苦晒，聽日準時呀！」，
兩人同高 506.4px、頭頂同一水平（topDiff 0.0）。

## 身高比表 `DLG109_HEIGHT_SCALE`（阿偉＝1.00 基準）

渲染高＝DLG108 fitted 基礎高（上限 60%）× 身高比；腳底 `bottom:10%` 唔郁
（v108 遮腿設計不變），矮咗只係頭頂低咗。單人步同樣 × 比；未知 id／舊圖後備 → 1.00。

| 檔 | 比 | 渲染高（基礎 60%） | 成員 | 理據 |
|---|---|---|---|---|
| 矮 | 0.85 | 51%（≈430px） | `pang_siuki` | brief 明言「身型偏胖但靈活、面型圓潤」＋金牌司儀靈感對照係矮個司儀；全身圖 AR 0.376，比阿偉 0.343 闊 9%，矮胖型全庫最明顯；用戶實玩指定要矮。頭頂比阿偉低約 76px——低一截，唔變 Q 版（Q 版約 0.6–0.7 連頭身比都變，呢度只係縮 15%）。 |
| 高 | 1.05 | 63%（≈532px） | `gu_mingfai`、`ching_tinlok` | 兩人 AR 係全庫最瘦兩名（0.232／0.267），圖中腿長身窄；brief 亦有修長線索（顧：面型偏瘦、溫文爾雅、長風褸；程：面型偏長、跳唱歌手陽光修長形象）。 |
| 中 | 1.00 | 60%（≈506px） | 其餘 31 個 id（含 `awi`／`awi_s2`／`awi_s3`） | brief 無身高線索者一律唔估身高（唔准逐個估 cm，brief 冇寫）。闊度差異由 AR 本身表達——例如方小龍 AR 0.413 闊身、Vera 0.382，佢哋係闊唔係矮；何生「略發福」亦係闊度唔係高度。阿偉三階段同一人，冇長高證據，一律 1.00。 |

表覆蓋 `DLG106_GAZE` 全部 34 個 id（1＋2＋31）。全部數值喺 0.80–1.10 之間，
彭少祺 0.85 ＜ 0.90。量度備註：包圍盒量度失效（每張全身圖人物都撐滿畫布，
h_frac ≈ 0.998），所以高度差唔能夠由圖量出嚟——分檔理據係 brief 文字＋目測
身形＋AR（闊高比），已喺上面逐項寫明，唔係假精確量度。

## 實作（`index.html`，+67／−7 行）

- 新增 DLG109 模組（DLG108 模組之後）：`DLG109_HEIGHT_SCALE`＋`dlg109HeightScale(id)`＋
  `dlg109ScaledPct(basePct, id)`，出口 `window.DLG109 = { SCALE, scale, scaledPct }`。
- `dlg108FitPct` 加兩個可選參數 `(scaleL, scaleR)`（預設 1）：闊度計數用
  `pct × scale × AR`，即係收細判定計埋身高比之後嘅實際闊度；6 參舊調用零變
  （test_dlg108_logic 全部 PASS 實證）。
- `dlg108FitApply`：舞台 `--dlg108-char-h` 繼續放 fitted「基礎高」；再逐張圖落
  inline `height`＝基礎高 × 各自身高比。角色 id 來源雙路：主線 `data-dlg-id`，
  巧遇 `_sid106`（`paintChar106` 落）；搵唔到 → 1.00。
- CSS 一字唔郁（`.dlg106-char`／`.e79-char` 仍係 `height:var(--dlg108-char-h,60%)`＋
  `bottom:10%`）；DLG108 註解＋CSS 註解加咗 v109 說明。WF4 隨機事件冇 onload
  `__dlg108Fit` 掛鉤（沿用 60% fallback），屬 D-8 二期範圍，今次唔郁。

## 量度表（實駕 390×844，`qa109a/drive109a.py`，新遊戲槽 3）

| 配對 | 基礎高 | 渲染高（pre → post） | 頭頂差（post） | 中間淨空（pre → post） | 備註 |
|---|---|---|---|---|---|
| C1 主線 阿偉×何生 | 60% | 60%／60% → 不變 | 0.0px | 13.8px → 13.8px | 同一句「學動作戲聽落紮實啲…」（pre step 5／post step 6，同一句；步數差係行句時序，量度值一致）。牌頂 638px 不變。 |
| 巧遇 阿偉×彭少祺＠中環廣告 | 60% | 506.4／506.4px → 506.4／**430.4px** | **＋76.0px**（彭生低一截） | 13.6px → **39.1px** | 首句「哎，收工啦…」；dayIndex 427 撞到；inline 高 60%／51%。 |
| 巧遇 阿偉×鍾楚凝＠天星音樂 | 60% | 506.4／506.4px → 不變 | 0.0px | 30.1px → 30.1px | 首句旁白「天星音樂嗰邊搞影展酒會…」；dayIndex 424；兩人皆 1.00，v108 不變。 |
| 巧遇 阿偉×顧明輝＠海港廣播 | 60% | 506.4／506.4px → 506.4／**531.7px** | **−25.3px**（顧生高一截） | 83.4px → 77.5px | 首句旁白「海港廣播電台門外…」；dayIndex 0 即撞到；inline 高 60%／63%。 |
| 最闊配對 方小龍＋Vera | 55.4%（fitted） | 55.4%／55.4% → 不變 | — | 計算值：60% 基礎淨空 −24.5px → 自動收細照觸發 | 計數值（`dlg108FitPct` 實測輸出 55.4%），唔係實駕——兩個都唔係可觸發巧遇嘅星，冇可玩配對；兩人皆 1.00，v108 規則不變。 |

- 腳底：三段巧遇＋C1 全部人物 bottom 伸到對話框後面（遮腿不變；彭生矮咗之後
  腳一樣藏喺框後，見 post 截圖）。
- pre／post 同一日／同一句（顧 day 0、彭 day 427、鍾 day 424，三段首句逐字相同）。

## 改前／改後對照圖

`~/workspace/linji-work109a/qa109a/shots/`（390×844，device_scale_factor=2）：

- 阿偉×彭少祺：`pre_enc_pang.png` → `post_enc_pang.png`（同一句「哎，收工啦…」）
- 阿偉×顧明輝：`pre_enc_gu.png` → `post_enc_gu.png`（同一句旁白）
- 阿偉×鍾楚凝：`pre_enc_chung.png` → `post_enc_chung.png`（不變，對照用）
- C1 阿偉×何生：`pre_c1_awixho.png` → `post_c1_awixho.png`（不變，對照用）

目測：post 彭生頭頂明顯低過阿偉，矮胖身形不變 Q 版；顧生頭頂高過阿偉約一截；
鍾楚凝／何生同 pre 一模一樣。顧明輝段兩人偏暗係旁白步明暗（pre 已經一樣），
唔係 109 引起。

## 測試

- 新測試 `tests/test_dlg109_height_logic.js`：**34 PASS**（身高比表覆蓋 34 id／
  範圍 0.80–1.10／彭 0.85／顧・程 1.05／scaledPct 51%・60%・63%／fitPct 舊調用
  零變／fitApply mock DOM 逐張 inline 高：雙人＋單人＋未知 id＋未載入；反證 3 項）。
- 新測試 `tests/test_dlg109_height_static.py`：**33 PASS**（SAVE／softRev／`?v=` 不變／
  接線＋反證／表覆蓋＋範圍＋實數＋反證／遮腿幾何不變／PORTRAITS 仲喺度／PIL 重測
  pang 0.376／gu 0.232／ching 0.267／awi 0.343＋計埋身高比嘅配對淨空）。
- `node --check` 全檔：`node --check index.html` 本身唔食 `.html` 副檔名
  （ERR_UNKNOWN_FILE_EXTENSION），改抽兩個 `<script>` 塊出嚟
  `/tmp/index109_check.js` 再 `node --check` → **PASS**。
- 全套測試 A/B（`qa109a/run_suite.py`，沿用 qa108d runner）：
  基線 `qa109a/suite_base109a.txt`＝**142 PASS／12 FAIL**；
  工作樹 `qa109a/suite_work109a.txt`＝**144 PASS／12 FAIL**，FAIL 清單逐字相同
  （12 個環境性 static FAIL：flash51／giglib36／pacing35／poster59／rumor49／
  slot50／soft_tip_111_restore／start53／weave43／weave44／weave49／wrap38）。
  ＋2＝兩隻新測試，**零新增回歸**。
- 實駕 0 pageerror。console 404：pre／post 同數 8 宗，係缺表情檔 fallback
  （今次驗到 `ho_sang_angry.webp`／`.png` 缺檔；鍾楚凝 think／smile 缺檔係
  v108 已知），pre 已有，唔係 109 引起。

## 駕駛備註（畀下一手）

- `enc79PlayEncounter` 等函數唔係全域（成個主 script 包喺 IIFE 入面，只係
  `window.DLG106`／`window.DLG108`／`window.__dlg108Fit` 等有出口）——
  唔可以直接 evaluate 開巧遇，要行玩法入場：`S.dayIndex＝d；S.starDay＝null`
  逐日重骰＋撳地點掣（108v 配方；腳本 `qa109a/drive109a.py`）。
- 認星唔可以用名牌：顧明輝首句係旁白（名牌空白），要用 `.e79-char` 嘅
  `data-dlg-id`／`_sid106` 認。次序要顧行先（顧 day 0 即撞；排最後嗰陣
  18 日都撞唔到，原因未深究——疑似之前兩段巧遇改咗 S.starDay／地圖狀態，
  現行腳本顧→彭→鍾次序穩定撞到，唔好亂調次序）。
- 彭少祺段首句有講者名，鍾／顧首句係旁白——pre／post 對照以首句為準，
  三段首句逐字相同已驗證。

## 未做／留待統籌

- B 線（PORTRAITS／舊 bust 換新圖）唔喺呢包，唔好喺合併嗰陣撈埋。
- WF4 隨機事件舞台未套 DLG108／DLG109（D-8 二期範圍）。
- 最闊配對（方小龍＋Vera）只有計數值，無實駕值（見量度表備註）。
- `ho_sang_angry.webp`／`.png` 缺檔（C1 行句嗰陣 fallback 404）——舊問題，
  未修，留待另開一票。
