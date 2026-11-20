# v20a345 FULLARC_FIX：F1 警告顯示返＋F2 結局判定加 floor 檢查

來源：full arc 實駕（`~/workspace/linji-drive-fullarc/`）三項發現，parent 已親查 live 核實。
Base：v344（main `738a834`，index.html 47,316 行，suite 397／9）。

## F1（真 bug）：年終評核警告喺正常遊玩下不可見

- 根因：警告行經 `pushFlavor` 入 settle flavor 後存入 `S.weekBoundary105.html`；
  v20a71 移除 home「本週結算」卡後，`enterHome` 唔再展示 summary，全檔唯一渲染
  settle html 嘅位置係重開遊戲嗰陣嘅補呈現 modal（contFromSlot）。`afterDayModal`
  內容唔包 summary.html。結果：連續遊玩下警告（評核／破產寬限／身體警號／現金）
  從來唔出現，玩家直接收 E7，同「警告先行」拍板不符。
- 修法：
  1. `settleWeek` 另存 `warnHtml`（cq61 評核／寬限行＋`class="bad"` 行，按 flavor
     原順序）入回傳 summary；`html`（settleBlock＋flavorHtml）同
     `S.weekBoundary105.html` 原樣保留，重開補呈現路徑不變、唔重複彈
     （contFromSlot 傳入嘅 summary 冇 warnHtml 欄，唔會觸發新 modal）。
  2. 新函數 `presentSettleWarn345(summary)`：入編排步嗰刻排隊彈「週結算提醒」
     modal（等試鏡公佈／其他 modal 完先出，retry 上限約 7.5 秒；已判強制收場
     就唔出，結局呈現本身會交代）。
  3. `enterHome` editable 時呼叫之——所有週結路徑（排程日／睡眠／休息／訓練／
     約會／傾談）最終都經 `enterHome(summary, true)`，一處覆蓋全部。
- 呈現取捨：只出警告類行，唔出成份 flavor（v20a71「資訊太多」嘅教訓保留）；
  正面／中性旁白照舊只喺重開補呈現出。

## F2（設計可達性）：1992 E7 正常玩法不可達

- 根因：1992 評核 boundaryWeek 156（floor 155），但 N17 閘 weekMin 153 令結局
  喺 12 月初觸發，搶先評核三週；idle 增長亦令 dual 好難低過 155。E7 機制本身
  經 1991 評核驗證完好，只係 1992 嗰格俾 N17 搶先。
- 修法（結局判定嗰刻補 floor 檢查）：`ending410ResolvePresent410` 喺
  `resolveEnding410` 之後、寫 `S.ending410` 之前檢查——dual 低過 1992 floor
  （讀 `CONSEQ61_REVIEWS[1992].floor`，唔寫死）改判 E7（variant `review1992`、
  title「未紅先收・…」、gaps95 清走、`earlyEnd` 跟強制收場路徑一致，
  手帳總結頁出「1992 年尾評核・提早埋單」標題）。
  - E6（玩家主動退圈）唔覆蓋，保留玩家選擇。
  - 唔郁 `resolveEnding410` 判定表（結局梯即時位置顯示唔受影響）、
    唔郁 1990／1991 評核路徑、唔郁 N17 閘時機。
  - `endingCareerScene410` E7 加 `review1992` 分支（第三年年尾版，鏡像
    review1991 寫法）；`ENDING410_CAREER_NAMES` E7 註解同步。

## F3（已判斷，唔改 code）

結局尾聲三處「1993」字句（約 L13290／L13396／L13522，行號以 v344 為準）係
結局文案向後望（其中一處自註「遊戲期外」），唔係遊戲期內時間，保留唔改。

## 測試

- 新測試 `tests/test_r345_fullarc_fix.js`（39 項 ALL PASS）：抽 live 真函數——
  conseq61SettleEval 警告生成（dist 1／2、dual 夠高唔出）、1991 評核路徑回歸
  （唔過寫 pendingEnding／過咗續約）、settleWeek 真跑 warnHtml（含 back-compat
  html／weekBoundary105）、presentSettleWarn345 真跑彈 modal（空／null／強制收場
  三個對照）、ending410ResolvePresent410 floor 覆寫（100→E7、154→E7、155 唔改、
  200 照舊 E2、E6 唔覆蓋）、review1992 場景文字。
- 反證：同一測試對 v344 舊 index.html 有 15 項乾淨 FAIL（全部係修復相關斷言），
  24 項回歸／對照照舊 PASS。
- 全套 suite：見落地紀錄（基線 397／9，新測試 +1 項預期 398／9）；
  index.html 行數 +52，釘行 resync 見 `qa345/`（如有）。

## 唔郁

- 1990／1991 評核、破產寬限、病倒機制；N17 閘；結局梯判定表；
  `resolveEnding410` 純函數本體；weekBoundary105 補呈現路徑；F3 三行 1993 字句。

## 落地紀錄

- main `8347b45`（squash merge 自分支 `v345-fullarc-fix` `d6cae74`，base 738a834）。
- index.html md5 `39b4bc461957273630790197434451cf`；Pages 傳播後 curl 核實 byte-identical。
- 全套 suite 398／9（v344 基線 397／9＋新測試 r345 一項；九項 FAIL 同既有 pre-existing 清單逐項相同）。
