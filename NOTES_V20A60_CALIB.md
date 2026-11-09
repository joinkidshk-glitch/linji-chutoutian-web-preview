# NOTES v20a60 — 全弧校準包（CALIB60）

依據：`~/workspace/linji-fullarc-report.md` 五大發現（數值通脹／經濟兩極／節點無聲漏失／聲樂盲點／tutorialFx bug）。
用戶 2026-11-10 04:13 拍板「照建議全套校準」。本版只做校準，唔加新系統。

**硬規則遵守**：SAVE key（`starVolunteer_map_v19w`）、softRev（`s107`）、產品 `?v=`（`v20a10`）冇郁；冇改 content pack JSON；`resolveEnding410` 結局門檻、感情線 commit 條件冇郁；節點觸發條件（STORY_GATE_3Y）冇郁。index 4,686,517 → 4,701,779 bytes（+15,262，純 code）。

**測試**：全套 54/54 files PASS（基線 52＋新增 2）；新測試 `tests/test_calib60_logic.js`（66 斷言）＋`tests/test_calib60_static.py`（32 斷言），兩套對 v20a59 index 行都 FAIL（反證成立）；全檔 script `node --check` OK。

---

## 1. 數值遞減／軟頂（回應發現 ③ 數值通脹）

**問題**：拍攝日逐日加屬性冇遞減／上限，E1 三門檻（dual 125／fame 60／credit 55）開局第 25 週前全過，結局 dual 係門檻 8–10 倍。

**改咗邊度**（index 內 `apply()` 之後新增 CALIB60 區塊）：
- `CALIB60_FAME_BANDS` / `CALIB60_ATTR_BANDS`：按「增益嗰刻嘅現值」查表嘅遞減帶。
  - FAME 帶（fame／popularity 共用）：現值 <5 → ×1.0；<14 → ×0.30；<28 → ×0.22；<50 → ×0.17；<85 → ×0.14；<140 → ×0.12；<230 → ×0.10；其後 ×0.08。
  - ATTR 帶（acting／stage／vocal／looks／charm／iq）：<28 → ×1.0；<55 → ×0.36；<110 → ×0.25；<190 → ×0.19；其後 ×0.14。
- `calib60BankedGain(key, v, cur)`：縮放後嘅小數增益唔丟棄，存入存檔新欄 `S.calib60Bank`（每屬性一個餘額），儲夠 1 點先落地——避免「細增益永遠歸零」嘅死區；bank 以 1e-6 四捨五入殺浮點漂移（25×0.08 要準確 =2）。
- `applyCalib60(delta)`：`apply()` 嘅校準版包裝——正增益經 banking 縮放，**負增益、壓力、體能、錢一律原額**（懲罰唔打折、回復唔縮水）。
- 接線（恆常來源先縮）：`resolvePlannedDay` 拍攝日＋殺青合併 delta、訓練鏈 9 課、街頭／茶記散工；`applyTrainLesson` 9 課；3 處直接寫 `S.fame +=` 嘅散工／試鏡／茶記位改行 `calib60FameGain()`。
- **刻意唔縮**（NOTES 明記）：劇情抉擇獎勵（`applyChoice` 獨立路徑——一次性敘事回報，兼有 weave 測試鎖原額）、`industryCreditDelta` 敘事增量（劇情／對手／報紙／殺青 meta——一次性）、里程碑／社交微增益。信用係派生值（fame×0.5＋stage×0.3＋acting×0.2−壓力罰＋敘事增量），源頭縮咗佢自然跟住慢，唔使另設信用帶。
- 沙盒相容：兩個被舊測試抽函數嘅 caller（`resolvePlannedDay`／`applyTrainLesson`）用 `applyGain60` alias（`typeof applyCalib60==="function" ? applyCalib60 : apply`）——正式環境永遠行校準版；舊測試沙盒冇抽新函數時退回 `apply`，唔好為咗測試改斷言。

**點解呢組參數**：用全弧真數據回放調出嚟（唔係拍腦袋）——逐週 [fame, stage, acting, stress, credit] 快照（arcA 全 143 週；arcC 用 ×0.75 密度模擬「穩定認真玩」101 週），逐項 delta 經遞減帶＋banking，再用遊戲自己嘅 `dualTrackNumbers` 公式重算信用。未校準回放先要重現報告基線（A 第 23 週／C 第 18 週過 dual 125）先證明回放忠實；調到 v10 參數組為止。

**驗證**（`test_calib60_logic.js` 回放斷言，行遊戲真函數）：
- 校準後 dual 125 到達：慢速弧（Arc A）**第 66 週**、穩定弧（Arc C×0.75）**第 57 週**，中位 **61.5 週**——入目標帶 60–75。
- 唔封死結局：Arc A 第 143 週 dual **260**（門檻 125，兩倍餘裕）、fame 60 於第 73 週到、credit 55 於第 52 週到；Arc C 第 101 週 dual **204**、終點 fame/credit 均過 E1 單項門檻。
- 單位行為：低值全額、負增益／壓力／錢唔縮、banking 儲分行為（fame 100 連續 9 次 +1 → 合共 +1；fame 500 連續 25 次 +1 → +2）全部有斷言。

**模擬假設（如實申報）**：①回放係「每週粒度 banking」近似——實機係逐日 apply，banking 頻率更高、落地只會更順，唔會更慢；②Arc C ×0.75 密度係假設情境，唔係真存檔；③回放冇建模「fame 升得慢→高階通告入場遲→原料入得更慢」嘅回饋——呢個回饋只會令到達再遲少少，方向安全（唔會令結局唔可達）；④credit 敘事增量由 CSV 派生公式倒推（credit − 公式基數，下限 0）。

---

## 2. 經濟收緊（只收中後期）（回應發現 ② 經濟兩極）

**問題**：gate-on 弧存款全程最低 $11,948、結局 $208k，錢唔構成任何決策。報告槓桿：支出隨年份／地位遞增、後期回報遞減。

**改咗邊度**：
- `livingCostBand(w)` 加 CALIB60-2 段（base 帶原封：wk1–4 mid 1600、soft wk5–8 1900、soft wk9–12 2100、其後 2400）：嗰週第一日年份（新 helper `calib60YearOfWeek(w)`，1988-03-07 起計真日曆）≥1989 先加——**1989 +$300／1990 +$600**；同年 **fame≥120 再 +$200、fame≥250 再 +$400**（取高一級，唔疊加）。lo/hi/mid 同步加，label 講明「（1989 年物價）／（・成名開支）」。`livingCostRoll`（扣款）同 `livingCostEstimate`（預覽）行同一個 band 函數，預覽同實扣永遠一致。
- `takeSoftBridgePay`：散工正薪 **fame≥200 時 ×0.75**（round）；同週補場 **$800 不變**（v56 保底閥原封）。

**紅線證明**（測試逐蚊對照）：wk1–43（1988 全年）× soft 開／關 × fame {0, 130, 300} 共 258 組，`livingCostBand(wk).mid` 同 v20a59 舊邏輯逐蚊一致——開局存款 $12,000、首年生活費、補場 $800 全部冇郁，新人保命線原封。遞增數值斷言：1989 wk50 fame 0/130/300 → 2700/2900/3100；1990 wk100 fame 0/260 → 3000/3400；散工 fame 10 正薪 3600 全額、fame 250 → 2700、補場恆 800。

**點解收得咁輕**：報告同時警告 gate-off 弧試過夏秋斷供跌到 $0——收緊只准咬中後期同高名氣玩家（佢哋正係「錢唔構成決策」嗰群）；1989 年人人加 $300/週（≈首年全期生活費嘅 12.5%）係溫和通脹，唔係懲罰。真正咬人嘅係 fame≥250 嗰級（+$1,000/週）同散工正薪打折——只影響已經唔缺錢嘅玩家。

## 3. 節點漏失提示（回應發現 ⑤ gate-on 節點可無聲漏失）

**問題**：Arc C 漏咗 10 個主線節點，零提示，照出 E1——玩家唔知自己錯過咗成段戲。

**改咗邊度**（全部新 code，唔改 STORY_GATE_3Y 觸發條件）：
- `CALIB60_NODE_WINDOWS`：12 個主線節點（C6–C17）嘅「編排時窗」表（年份＋季節＋時期標籤），跟三年版主幹 N1–N17 編排（C6 1988 全年；C7 1989 夏；C11 1989 夏／秋；C8 1989 秋；C9/C10 1989 冬；C15 1990 春；C14 1990 夏；C12/C16 1990 秋；C13/C17 1990 冬）。**注意語義**：gate 本身容許遲一年同季補觸發，所以「漏失」＝過咗編排時窗未做，唔係永久死亡——補返完成會自動喺清單除名。
- `calib60MissedScan(st)`：純登記函數——已完成→除名；過窗未完成→登記入存檔新欄 `S.calib60Missed{id:{title,whenLabel,week}}`；C17 若已收科（`ending410` 存在）唔登記。標題經 `calib60NodeTitle`（先查 spine 節點表，再 fallback 本地表），只出名＋時期，唔劇透內容。全函數防禦式 try/catch，爛檔唔會炸。
- 提示面：`settleWeek` 喺 `saveQ()` 之前行 scan，新登記（上限 3 條）每條出一行結算 flavor：「錯過了：《暴雨救場》（1989 年夏）嘅時窗過咗——手帳「回憶」頁記低咗。」
- 手帳新頁「回憶」：tab 掣（作品之後）＋pane＋`renderMemoryPane60()`——列已漏節點名／時期／登記週數；空狀態有引導文案。`setHomeTab` allow 表、pane 表、`syncHomeTabExit` 已接線；CSS 跟紙面風格（`.mem-item60` 等）。
- 舊檔：`normalizeSaveObj` return 前靜靜行一次 scan 補登——**唔彈提示、唔出結算行**，開手帳先見到。手帳 render 本身只除名唔登記，唔會搶先食咗週結嗰行提示。

**驗證**：邏輯測試造日曆位斷言——1989 秋中登記 C6＋C7、C11/C8 未完窗唔登記、其後完成自動除名、1989 夏初只登記 C6、已收科唔登記 C17、舊檔 normalize 補登（C7 入、C6 已完成唔入）；靜態測試鎖接線（settleWeek／normalize／tab／pane／CSS／12 節點表齊）。

## 4. 聲樂盲點（回應發現 ④ 偏科盲點）

**問題**：聲樂可以成世凍結，唱片線靜靜鎖死；預設計劃永遠唔排歌藝，目標建議遇音樂通告缺口唔識指路。

**改咗邊度**（唔改課程數值）：
- `defaultWeekPlan`：喺演技分支之後、外形分支之前加歌藝輪替（完全跟 v58 武師班先例嘅位置邏輯）——已報名 `train_vocal` 且累計 <2 堂 → 星期二排 `train_vocal`。演技未夠 2 堂仍然優先演技；未報名唔會亂排（報名要去唱片地點，計劃唔代玩家使錢）。
- `bestTrainJumpForGig` 回傳加 `frozenVocal` 旗標：最大缺口係歌藝（vocal）且 `trainCount.train_vocal` 係 0 先 true。
- `openCastingNoticeDetail`：`frozenVocal` 時喺訓練捷徑下面加一行 `.cn-train-jump-frozen60`：「提提你：你從未練過歌藝——音樂／唱片類通告會一直欠呢一項。去唱片公司報「歌藝訓練」開咗個頭先，之後排計劃會識得輪住練。」（跟 v58 目標建議同一模式：指去邊度開頭＋講明後續點接。）

**驗證**：邏輯測試——演技夠 2＋歌藝 0 堂→排 train_vocal；演技未夠→演技優先；未報名→唔排；歌藝夠 2→輪返外形（舊次序）；第 1 週 base 不變；frozenVocal 三態（從未練 true／練過 1 堂 false／最大缺口係演技 false）＋建議地點係 music 類。

## 5. tutorialFx bug（回應細 bug：`tutorialFxFingerErr is not defined`）

**根因**：教學 FX 圖（手指圖等）嘅 `onerror="tutorialFxFingerErr(this)"` 係 inline handler，喺**全域作用域**查找函數名；但函數本身宣告喺主 script 嘅 block 作用域（`{ ... }` 之內，同檔案其他具名引用都係包喺 script 頂層先冇事），全域搵唔到 → ReferenceError（非致命，但 fallback 圖永遠唔行）。

**改法**：函數定義之後加一行顯式發布：`try{ window.tutorialFxFingerErr = tutorialFxFingerErr; }catch(_e){}`——同檔案既有做法（`window.__linjiBootMark` 等）一致，唔郁函數本體同呼叫點。

**驗證**：邏輯測試抽真函數＋發布句 eval，斷言 `window.tutorialFxFingerErr` 係函數、用假 img 行一次真係換去 `data-fx-fallback` 圖、再行唔會 loop；靜態測試鎖發布句同 inline handler 並存。

---

## 冇做／留俾後續

- 結局後日曆衝出三年框冇收尾（全弧報告觀察項）——唔屬校準五包，冇郁。
- v20a61「後果包」（早期差結局＋壓力爆煲病倒，用戶已拍板寬鬆版）——用本版新經濟／新數值曲線定地板，另開一版。
- 89/90 選角回填、A 級海報——資產通道問題（主檔已 4.70MB，推送上限約 5MB），等原生版或另覓方案。
