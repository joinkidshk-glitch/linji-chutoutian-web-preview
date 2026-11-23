# v20a388 第九輪補跑 P2 四項收尾

日期：2026-11-23。基線：v387（main `99ab746`，suite 405 PASS／9 FAIL）。
來源：`~/workspace/linji-playtest-eval9-2026-11-22/REPORT.md`（第九輪補跑，冇新 P0/P1，P2 四項）。
證據：`~/workspace/linji-drive388/`（GPT 原稿 gpt_ui388.txt、probe388.py／probe388b.py／probe388c.py＋JSON＋截圖）。

## 修正（逐項對 live code 核實後實裝）

### ① 頒獎舞台腳燈圖層次序（W1 P2）
- 根因：`.awd62-stage` 第二規則（舊 L807）聚光燈漸層列第一（不透明）、腳燈暖光列第二——CSS 先列層畫上面，腳燈被遮蔽，像素實測舞台下半全 `#0c0913`。
- 修法（GPT-6.2-sol 方案，原稿 `gpt_ui388.txt`）：兩層對調，腳燈放第一、聚光燈做底，`.16` 透明度不變。
- 實駕驗證（probe388.py）：390px 舞台截圖取樣——高度 98% 處 (36,29,28)，比原本 `#0c0913` 更暖更亮；75% 處 (12,9,19) 維持底色，合 GPT 驗收準則。

### ② 地點面板「未開放」摺疊掣 44px（W2 P2）
- `.ux68-locked-toggle`（舊 L5235）無 min-height，實測高 39px。
- 修法：加 `min-height:44px`（同 v387 口徑）。實駕量度高 44px。

### ③ 預設計劃填位唔跨限期（W3 P2）
- 根因：`lockShootsIntoDraft` 填位唔睇 deadline——剩 2 日、限期喺週頭嗰陣，預設排限期前後各一格，限期後嗰格永遠執行唔到，`processOverdueShoots` 照樣取消扣違約金（W3 一年真玩 6 次違約有 3 次屬此型）。信任預設計劃嘅正常玩家會中招。
- 修法：填位前計本週週一曆日（`di388 - di388%7`，唔經 weekdayIdx 呼叫，測試沙盒冇 stub 都行到）；只填曆日 ≤ `deadlineDay` 嘅格。救援段：限期喺本週內而限期前非休息格唔夠，先覆寫限期前休息格（休息最後，同 v20a386 次序）——唔覆寫就必違約，覆寫只係少一日休息。限期喺下週唔覆寫（留待下週填位）；無 `deadlineDay`（舊檔）行為不變。
- 範圍：只改預設填位 `lockShootsIntoDraft`；人手排程路 `placeShootOnPlan`／`previewShootPlacement` 有 modal 警告，唔郁。
- 測試：`test_eval9_388_logic.js` C 段（限期後唔填／救援覆寫／下週唔覆寫／第六輪 C 場景回歸／無限期照舊）。

### ④ 跨年殺青計數器 desync（W4 P2）
- 根因：殺青結算四處用 `GIGS.find` 查 gig——GIGS 只得當年庫。1990 通告喺 1991 年殺青（W4 實測 `gig_1990_tv_113` day 366）查唔到，`end95AddWrap`／`end229AddWrap`／`contractCredit361OnWrap` 三計數器跳過、wrapHistory 角色欄空白（wrapHistory 101 vs careerStats95.total 100）。
- 修法：四處改用 `grant229GigById`（v20a336 既有：先查當年 GIGS，搵唔到查 `STORY_WIRE.gigsByYear` 三年全庫＋`normalizeGigRecord`，同入池版一致）；`typeof` 守衛＋舊 `GIGS.find` fallback。變數名 `_bg56`／`_g95`／`_wg59w`／`_brg56` 同呼叫形狀保留（靜態測試釘住）。
- Scope 核實：殺青結算同 `grant229GigById` 同喺主 script IIFE（L7003–49402）內；同一結算塊已有 `genericCreditOnGigComplete283` 同式呼叫先例。
- 驗證：node 邏輯測試 D 段（抽真函數，GIGS 缺 1990 通告時全庫查到）；實駕 probe388c 證實 `gigsByYear[1990]` pack 真有 `gig_1990_tv_113` 連 roleScale／tier 分類欄位。
- 備註：`end229DeriveLeadStats`（舊檔種子衍生）同樣淨查當年 GIGS，但有 wrapHistory 角色欄 fallback；今次修好 wrapHistory 寫入後 fallback 數據齊，衍生路唔另改。

## 測試
- 新邏輯測試 `tests/test_eval9_388_logic.js`（A 圖層次序／B 44px／C 填位五案／D 跨年查全庫）。
- 行號釘 resync：index.html 淨 +18 行（全部喺 lockShootsIntoDraft）；`qa388/resync388.py`（difflib 映射、單次掃描 dict 查表）更新 gift185／rom159／rom176／tang171／tang173／travel114 六檔釘行＋總行數鏈（49386→49404，鏈尾加 `＋v388 +18`），逐個直接覆驗通過。
- Suite：見落地回報（基線 405／9 ＋新測試 1）。

## 唔郁
SAVE key／softRev／產品 `?v=`／贏線 0.875／floor 140／warnLine 180／E1 門檻 350／試鏡判定／頒獎計分／結局判定／實際壓力入水全部不變。
