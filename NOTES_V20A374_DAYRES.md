# v20a374 日結算卡改版（劇組日簿）

用戶 2026-11-22 06:58 實玩截圖三張（拍攝中／休息／咖啡店駐場日結卡），評價「這些畫面都不太理想」。
先諮詢 GPT-6.2-sol（88api2）出方案，原稿 `~/workspace/linji-drive374/gpt_plan.txt`，按方案實裝。
**只改呈現**：結算邏輯／數值／日期推進／流程一律唔郁；唔改 SAVE key／softRev／產品 `?v=`／贏線 0.875／floor 140／warnLine 180。

## 改咗乜

1. **卡高跟內容（空白收縮）**：`#mask.day-res .modal` 由固定 `height:min(78dvh,78svh,720px)` 改 `height:auto; max-height:min(92dvh,92svh,720px)`；矮屏 media block 同步改 auto。短卡（休息）實測 435px（舊 ~660px），長卡（殺青）720px 上限、內容喺 #modal-inner 內捲、掣列照 sticky。掣列位置唔再跨卡固定——係有意改變（GPT 方案「短卡貼內容」），兩個靜態測試期望值同步 resync（test_dayend189／test_buttons197，斷言改認新規則字串）。
2. **版式分區（#mask.day-res 專屬 CSS）**：標題 1.22rem 粗體；「聽日」行改紙籤標籤；日期行搬上抬頭（dayLine 加 class `dayres-date374`，三條日結路徑模板次序改為 h3→聽日→日期→畫面；v202 測試釘嘅 `<h3>${title}</h3>${dayEndNextLine202(ended)}` 前綴不變）；今日畫面統一橫幅 154px（矮屏 128px）：fx 片 full-width cover（基底 `.act-fx102 video` 200px 規則保留畀非 day-res 場景，day-res 內覆寫）。
3. **數值分組（formatResultNotes／formatRestSleepDeltas）**：新 `resLine374` 分類——單一 good/bad 增量行做簿頁短列（名稱左、數字右、兩格並排；現金獨佔全寬）；gold 標題行做區段標籤（上加分隔線）；其餘（敘述／警示／支票／事件盒）原 HTML 不動、全寬。拍攝進度加金色進度條（讀 meta.hint 既有「進度 X/Y」數字，純呈現）。`.result-line` class 全保留（v362 逐行入場動畫照行）。
4. **冇片活動補圖（dayResStill374）**：咖啡店駐場＝fx_train_b 室內演出定格（新檔 `assets/fx/still_cafe374.jpg`，由既有片抽幀）；街頭表演＝fx_shoot_ext 街景定格裁走攝製器材（`assets/fx/still_street374.jpg`）；收拾房間＝主角立繪 `char_hero_bust_default.png`；病假＝`char_hero_bust_eyes_down.png`（conseq61 兩處 afterDayModal 傳 still374:"sick"）。全部既有資產，唔用佔位圖形／emoji。瞓覺卡（sleep265 zzz）跟 v265 用戶定案不變。
5. **事件紙條**：`#setchoice35box` 牛皮紙底（#E9DEC5）＋選項掣全寬 ≥44px（原有次序／流程不變）。
6. **底部操作**：掣列 margin 收近；dismiss 提示字由 .78rem 放大至 .84rem（modal-note202，day-res 內）。加速連結維持 v189 全寬細連結（測試釘住，唔改做並排掣——GPT 建議嘅 238+88 並排同 v189 拍板衝突，取捨保留現行，NOTES 交代）。
7. **動畫**：卡入場由下方 20px 升起 240ms（dayresIn374）；prefers-reduced-motion 停用。數值浮字 statPop369／殺青紅印／逐行入場沿用。

## 驗證

- 實駕（Playwright 390×844，證據 `~/workspace/linji-drive374/`）：休息卡 435px 無空肚；咖啡卡有圖＋數值分組；街演／家務卡定格圖＋紙籤；拍攝卡進度條＋事件紙條；殺青長卡 720px 上限內捲。零 page error。
- resLine374 分類以 node 抽函數驗證 6 類行（進度／增量／現金／區段／警示／敘述）輸出正確。
- Suite：**TOTAL PASS 400 FAIL 9**，九項同 v373 基線完全一致（flash51／slot50／soft_tip_111_restore／start53／weave43／44／49／wf5_87／wrap38）。首跑 387/22：5 個 logic 測試抽唔到新外置函數（分類器改嵌 formatResultNotes 內解決）；8 個靜態行號釘檔 difflib resync（`qa374/resync374.py`，含 rom159 全佳行人手核實 26349→26464）。

## 未做／取捨

- GPT 建議主掣 238＋加速 88 並排：同 v189「加速降級做細連結」拍板＋測試釘衝突，今票保留細連結，只收近距離＋放大提示字。
- GPT 建議「聽日」行搬去底部操作區：v202 測試釘住抬頭位置（第一屏見去向係 v202 拍板），保留抬頭，改紙籤樣式。
