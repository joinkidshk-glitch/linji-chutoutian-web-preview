# NOTES_V20A133_WF4CLIP — WF4 隨機事件對話框短 viewport 被切（v128 回歸修復）

## 現象（用戶 2026-11-12 18:51 實機截圖）
WF4 事件 `wf4_ev_day02`「傳呼台嘅一課」第一句旁白，喺真 iPhone（430×932，dvh 約 726）
上面對話框只見到一行半，第二行字俾攔腰切斷，睇唔到。

## 根源（已重現，證據 `~/workspace/linji-wf4clip/`）
`.story-play { max-height:min(58dvh,480px); overflow:hidden; }`（v17o「一屏無滾」）
夾住 `#mask.wf4-stage-on .sp-stage { min-height:480px; }`（**v128 A3** 放大舞台嗰陣加嘅）。
dvh 700 嗰陣 story-play 上限得 406px＜舞台 480px，舞台底部（對話框）俾
`overflow:hidden` 剪走；再加 `#modal-inner` 內容 476＞可見 439，第二重剪。
430×932 嗰陣 58dvh=540→上限 480，啱啱好 fit 到，所以 headless 捉唔到。
同 S-30 標題被切（v132）同一批 v128 回歸。
重現數字（修復前，430×700）：story-play 406／stage 480（bottom 696 vs 622）／
plate 只見 61px／line bottom 652 vs plate bottom 679／inner 476/439。

## 修法（index.html 1 處，＋5 行註解）
`#mask.wf4-stage-on #modal-inner .story-play .sp-stage`：
`min-height:480px` → **`min-height:min(480px,52dvh)`**。
- dvh ≥924 先足額 480px（保 v128 批准嘅高屏觀感）；短屏按 52dvh 縮
  （dvh 700→364px、726→378px、780→406px），等舞台 fit 入 story-play
  上限同 modal-inner，唔使捲都見晒對話框。
- 52dvh 係保 480px 嘅最小整數（480/932＝51.5%）；人物隨舞台縮細，
  短屏細啲係可接受 trade-off，總好過切文。
- 唔郁 `.story-play` 58dvh 上限、modal max-height、對話框定高 118px、
  灰色舞台底（v105 既定 fallback，換場景圖係設計決定，唔入呢票）。

## 驗算（`qa133/drive133.py`，`wf4_ev_day02`，斷言 A–D）
| viewport | stage | plate 可見 | inner | 結果 |
|---|---|---|---|---|
| 430×700 | 364（＝story-play） | 118/118 | 434/434 | PASS |
| 430×726（用戶實機 dvh） | 378 | 118/118 | 447/447 | PASS |
| 430×780 | 406 | 118/118 | 476/476 | PASS |
| 430×932 | 480（同修復前完全一樣） | 118/118 | 550/550 | PASS |
修復前對照：430×700 FAIL（plate 61px）、430×932 PASS。
前後對照截圖：`qa133/shots/wf4_430x700.png`（修後）vs
`~/workspace/linji-wf4clip/shots/wf4b_430x700.png`（修前）。
最長 setting 探針（`qa133/probe_longsub.py`）：WF4 池最長 setting 係
`wf4_ev_boss01`「金龍茶餐廳，下晝三點幾，落場冇乜人」17 字（之前
51 係 byte 數，唔係字數），一行 fit 到，430×700 PASS——全池事件都受惠，
唔只 day02。

## 測試
- 新測試 `tests/test_ui133_wf4clip_static.py`（靜態守門：新寫法在＋舊寫法不在；
  對 pristine main 乾淨 FAIL 反證成立）。
- 全套：pristine baseline（ac57418 新鮮 worktree）**191 PASS／12 FAIL**；
  工作副本 **192 PASS／12 FAIL**（+1 係新測試），FAIL 清單完全一致，零回歸。
- 附帶 resync（修法令 index.html 淨 +5 行，difflib 核實純漂移）：
  `test_travel114_static.py` 43 處行號 +5、`test_text125_static.py`
  27552→27557／27665→27670／33263→33268、`test_ui128a3_static.py`
  釘住嘅 WF4 480px 字串更新做新寫法。全部重跑 PASS。

## 落地
- 分支 `v20a133`，基底 v127 後 main `ac57418`（rebase 乾淨，v127 冇郁 index.html）。
- main commit：`76dc2d9`（git 直接合併，冇開 PR）；線上核實：線上 index
  **5,179,425 bytes、sha256 `001aab3343101add6ead80c72cc0b799fe8eeb5c4fa641a2b49693ea48c35079`**
  已 curl 核實，同 repo 完全一致。

## 範圍外（唔掂）
- 灰色舞台底：v105 既定 fallback（day 事件＋地圖 atLoc null→`wf4Scene105`
  回空字串），換咩場景圖等用戶定。
- 右邊灰色 〈 掣：headless 重現唔到、頁面冇對應元素，似瀏覽器／app 層嘅嘢。
