# NOTES_V20A126 — 表情補圖批（6 張新表情）

## 合併紀錄
- main commit：`2c97668`（squash，分支 `v126-expr` `351ded3`；基底 v20a125 `f671d28`）
- 線上核實：index.html 200、5,161,148 bytes、sha256 `8f08858aff911075dabf7cb8b18732146d7d36425d5f6a56f2830aaa686c518a`（同 v125 完全一致，零改動）；6 張新圖全部 200＋byte／sha 對上（fong_siulung_smile 106,654 B、pang_siuki_serious 173,454 B、gu_mingfai_smile 128,582 B、yip_manji_serious 177,120 B、lan_ruoxi_shy 212,768 B、ching_tinlok_sad 160,644 B）。新圖推 main 後即檢 404（Pages 部署滯後），約 2.5 分鐘後覆檢全數 200。
- 測試：全套 **175 PASS／12 FAIL**（基線 v125 main 173／12＋2 新測試；FAIL 清單同基線一致，零回歸）。
- 實駕：6 張目標全部實機渲染見齊（4 張巧遇真 UI 路徑＋2 張主線合成 force-start；見下），目標 404 由 9 → 0，0 pageerror。

## 新圖清單（6 張，`assets/story/fullbody/`，全部焗入米白光邊 RGB(243,233,210)）
| 檔 | 用途（句數） |
|---|---|
| `fong_siulung_smile.webp` | 方小龍 happy（5 句） |
| `pang_siuki_serious.webp` | 彭少祺 serious（4 句） |
| `gu_mingfai_smile.webp` | 顧明輝 happy（4 句） |
| `yip_manji_serious.webp` | 葉敏芝 serious（4 句） |
| `lan_ruoxi_shy.webp` | 藍若曦 shy（4 句） |
| `ching_tinlok_sad.webp` | 程天諾 sad（4 句） |

- 出圖：跟 v106／v107／v123 規格，帶風格錨（乾淨二次元動畫風）改現有 base 生成圖表情（`linji-fullbody-batch/gen/{stem}_base_gen1.png`）；QC **6 pass／0 marginal／0 紅旗**，總擲數 6。去背比例差全部 ≤0.010、全部單一連通體；腿間白楔掃描零可疑洞，唔使行 wedge fix。葉敏芝圖邊緣米白像素 12.7%（佢件米白冷衫本身貼近米白，唔係生成器描邊），顯示無礙。生成＋QC 詳見 `linji-work126-keep/NOTES_GEN126.md`（工作目錄，唔入庫）。
- 覆蓋率（`qa126/coverage126.py`，全語料 2,644 行）：**458／593（77.2%）→ 483／593（81.5%），＋25 句**。阿偉 s1／s2／s3 不變（188／188、184／188、184／188）。
- 593 分母核對（v125 更正數字）：CHOICE47／WF3／COMMIT48 嘅 text beats（真正唔顯示嘅 51 句＋resultBeats 35 句，連 WF4 intro／送別計 73–76 句）逐句對過 `lines_classified.json`（2,644 行）——**0 句命中**，即 593 分母從來唔包呢批，v125 令佢哋顯示到亦唔影響覆蓋率，唔使改分母。

## 數人頭斷言（合併計數，v123＋v126）
- `assets/story/fullbody/` 總數：140 → v126 加 6 張＝**146**。
- 非 boss webp（dlg108／dlg109 重測用）：115 → v126 加 6 張＝**121**。
- 受影響測試：`test_dlg107_static.py`（146）、`test_dlg108_static.py`（121）、
`test_dlg109_height_static.py`（121）、`test_dlg119_static.py`（140→146）、
`test_dlg123_static.py`（140→146）、`test_dlg126_static.py`（146）。全部 PASS。
- index.html、content pack JSON、SAVE key、softRev、產品 `?v=` 零改動。

## 守門測試
- `tests/test_dlg126_static.py`：6 張新資產存在＋WebP 檔頭＋＞50KB＋總數 146＋
檔名規則＋硬編碼句數＋全域增益合計 25＋烘焙報告＋基線不變量。PASS；
pristine 反證 FAIL（缺檔），成立。
- `tests/test_dlg126_logic.js`：6 張首選＋6 句真實對白分類＋反證（舊圖冇被搶、
未知講者回 []、垃圾輸入回 neutral）。PASS；
pristine 上 PASS（只驗解析器，唔驗檔案存在——檔案存在由 static 守門）。

## 實駕（Playwright，本地鏡像，`qa126/drive126.py`）
- **巧遇 4 張（真 UI 路徑：入主場地點 → ENC79 overlay 逐句行晒）**：
  - `pang_siuki_serious`：中環廣告，T0 opener 第 4 句「阿偉，好好好，記住啦記住啦，下次見面我一定叫得出。」（seed met＋fav 5）。
  - `ching_tinlok_sad`：天星音樂 day 610–621 初遇段「再嚟！呢段尾嗰八拍……」。
  - `yip_manji_serious`：香江唱片 heart 段第 14 步「你臨記出身都爬到上嚟，點解我就唔可以靠做戲爬過去？」（seed met＋fav 50）；後備場 e3b（player tier 2＋fav 25）第 12 步亦見第二句 serious「記住，你講過嘅每一句，佢哋都可以剪到變第二個意思。」。
  - `gu_mingfai_smile`：海港廣播 heart 段第 11 步「初初掂賭，都係朋友帶去玩兩手，贏咗少少，就以為自己運氣好過人。」（seed met＋fav 50；T1 opener 場 e4 十二日只觸發一次、冇命中，唔係失敗——heart 場已覆蓋）。
- **主線 2 張（合成 force-start，見下文）**：
  - `fong_siulung_smile`：A_fong_push1 第 3 步，happy 句「跳完呢場，我請你食宵夜，哈哈！」，截圖見 `qa126/shots/branch_s1_fong_fong_siulung_smile.png`（方小龍笑面＋米白邊實機呈現，張克凡聽者變暗）。
  - `lan_ruoxi_shy`：R_lan_meet 第 1 步，shy 句「哎呀——唔好意思，唔好意思，借過！（成疊通告牌同流程表，俾人一撞，散晒一地）」。
- **目標 404：pristine 9 → branch 0**（pristine：pang ×2、ching ×1、yip ×3、gu ×1、fong ×1、lan ×1；branch：0）。**0 pageerror（branch 兩跑＋pristine 一跑）**。
- 合成原因（老實寫）：A_fong_push1／R_lan_meet 唔係進度頁主線幕，唔可以用「播呢幕」；3 日入星河電視台亦無 storylet 自動觸發。`StoryPlay.start(id)` 會被 `hasPlayerOffer` 閘擋（toast「這幕尚未在地圖出現」），要 `{force:true}` 先播得——播放器、loader、渲染全部係真，只係觸發合成（v119 合成對照先例）。`qa126/probe126.py` 記錄咗呢個探查過程。
- 實駕期間撞到嘅非本批 404（已記錄，唔係回歸）：`pang_siuki_sad`（webp＋png，彭少祺冇 sad 圖，loader 試探後退 base）、`yip_manji_angry`（同上）、`gu_mingfai_shy`（同上）。呢三個係下一批表情補圖嘅候選（見殘留）。
- 過程失誤（老實寫，唔隱瞞）：① drive126 第一版 `missing` 集合每相做完唔重計，令全部後備場都照跑（唔影響結果，只係嘥時間；已修，`note()` 用 `global missing` 重計——第一版寫 `nonlocal` 係 SyntaxError，因為 `note` 喺模組頂層，唔係閉包）。② 第一版合成用 `StoryPlay.start(id)` 無 force，兩幕 story 場行咗 5 步空轉先發現係閘擋住（探針證實 toast「這幕尚未在地圖出現」）；修好 force 之後重跑 story-only，兩張即刻見齊。

## 殘留（下一批）
- 最大缺口全部 ≤3 句：顧明輝 shy 3、彭少祺 sad 3、周刊編輯（chow_choiyi）sad 3／angry 2、葉敏芝 surprise 2、葉敏芝 angry 2、程天諾 shy／surprise／think 各 1、藍若曦 serious／think 各 1、方小龍 sad 2、顧明輝 angry／think 各 1。下一批建議一次過收呢批 ≤3 句散項（頭選：顧明輝 shy、彭少祺 sad——實駕已見 loader 試探 404）。
- 零精確覆蓋嘅角剩 5 個：鄭威廉 serious／shy 各 1、鄧麗萍（extra_ad_fen）sad 9（旁白假陽性，唔使補）、關海媚 serious 1、莫少輝 sad 1、阿金叔 happy／serious 各 1——全部 ≤2 句（除假陽性嗰 9 句），唔值得單獨開批。
- `qa126/baked/`（6 張烘焙輸出，同 `assets/story/fullbody/` 重複）留喺工作目錄，未入庫（跟 v123 同例）。

## 回滾
- 成個 squash 係一個 commit：`git revert <squash>` 即退返 v125 狀態
（6 張圖＋2 隻新測試＋5 隻測試計數＋qa126 一併落返嚟；index.html 零改動，舊存檔完全唔受影響，
新圖只係令對話解析器唔再退 base——退返去只係變返退 base，唔會爛檔）。
- 單張圖回滾：刪 `assets/story/fullbody/<檔>.webp` 即可，loader 自動退下一級候補。
