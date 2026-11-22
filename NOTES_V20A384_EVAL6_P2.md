# v20a384 第六輪評估 P2 七項收尾

對象：live v383（main `8daa316`）。報告：`~/workspace/linji-playtest-eval6-2026-11-22/REPORT.md`。
UI 規格：GPT-6.2-sol（88api2，原稿 `~/workspace/linji-drive384/gpt_ui384.txt`＋`gpt_ui384b.txt`，brief 寫明終極目標原生 iOS app）。

## 逐項核實與實裝

1. **蘇先傾談開 meet 後送禮入口被待播劇情擋（W1 P2-1）**——核實：`rom176TryIntercept` 喺 `enc79StoryPendingAt(locId)` 為真時唔觸發（劇情優先，設計意圖）；蘇 meet 節點喺灣仔唱片（主場）eval 通過後，該地點長期「待播」，巧遇連送禮入口被擋，玩家無提示。實裝（跟 GPT 規格，唔改劇情優先機制）：地點面板有待播劇情、且此地係女角出沒點、且今日有女角在場（`rom176EnsureDay().presence`）時，喺「播劇情」掣上方出淺琥珀便箋「{地點}有一段待播劇情。請先播放劇情；巧遇暫時不會觸發。」（`.story-pending384`，#FFF1D6／#654617／左條 #B47A28）。播完劇情返面板重新判斷，冇待播即唔出。

2. **補位試鏡 7 日窗詳情頁無顯示（W2 P2-2）**——核實：自費試鏡有 `tape383DeadlineText`＋詳情行，補位冇。實裝：新增 `intel381DeadlineText(g)`（kept＋同 gigId → `intel381FmtDay(keptDay+7)`，同 tape383 同口徑），詳情頁加「補位試鏡／請於 {日期} 前到場試鏡」行（`intel381DetailRow384`，同自費行同一位置同元件）。未覆電（msg）唔出。

3. **自費試鏡 teaser 無截止日（W2 P2-3）**——核實：teaser 短卡只有「自費試鏡」pill，截止日要入詳情先見（長卡已有 `tape383-note`）。實裝：新增 `tape383DeadlineShortText(g)`（「M月D日截止」），teaser 標籤列加同色 pill（GPT 規格：同標籤同列，唔加高卡）。

4. **壓力 draft 生成時點邊界 wk17（W3 P2-4）**——核實：`defaultWeekPlan` 只讀生成嗰刻 `S.stress`；wk17 生成時未跨 80、翌日 97，只得兩日休息。實裝：判休息日數改用「現壓力同 `previewWeekStress(plan).peak` 取高」（`stress384`），峰值跨 80 即三日休息、跨 60 即兩日。低壓行為不變（邏輯測試 D2）。

5. **雙拍攝爭位餓死尾日（W3 P2-5）**——核實：`lockShootsIntoDraft` 按 `S.shoots` 陣列序填位，後入嘅長拍攝可搶晒星期位，剩 1 日嘅近限期通告排唔到而逾期取消。實裝：填位前按 `deadlineDay` 升序排序（`shoots384`），近限期先得位。休息位跳過（v380）不變。

6. **三線 crisis 挽回同葉／蘇鎖法唔對稱（W4 P2-6）——唔改設計，確認交代**：曉晴／采兒／徐 crisis 壞抉擇只寫 crisis 旗＋跌 rel（曉晴／采兒 −2、徐 −1），唔寫 BE 旗、唔鎖 CMT，約會升返 rel 6 後 CMT 照出——呢個係設計如此（W4 真玩證實，任務前提已修正）。葉／蘇 crisis 路線旗（`flag_yip_be_route`／`flag_so_played_safe`）同曉晴 `hiu_family_go` 嘅鎖法係另一套（路線本身不可逆）。兩套鎖法並存係有意設計：crisis「一時揀錯」可挽回，ending／路線抉擇不可逆。本票唔加鎖、唔改數值。

7. **藍 ending「HE：」文案殘留（W4 P2-7）**——核實：`C_lan_ending_he` notes 以「HE：」開頭（v380 dev 用語清理後殘留，玩家面可見；全檔僅此一處，另一處係 code comment）。實裝：跟 GPT 文案改「他們正式拍拖了。她把那句話包成約定，他接住了——不只這一頓飯，還有往後的每一餐。」（刪 dev 標籤，保留「正式拍拖」口徑）。

## 唔郁
SAVE key／softRev／產品 `?v=`／贏線 0.875／floor 140／warnLine 180／E1 門檻 350／試鏡判定／頒獎／結局判定／劇情優先機制全部不變。

## 測試
- 新邏輯測試 `tests/test_eval6_384_logic.js`（A 補位截止閘、B 自費短截止、C 雙拍攝排序、D 壓力峰值判休息）全 PASS。
- Playwright 實駕（`~/workspace/linji-drive384/probe384.py`，種子 1991-01-01＋kept 雙槽）：teaser 顯示「補位／自費試鏡／1月14日截止」；詳情頁「自費試鏡／請於 1991年1月14日 前到場試鏡」＋「補位試鏡／請於 1991年1月14日 前到場試鏡」兩行齊（截圖 probe384_detail.png）；HE 舊文案消失、新文案在位；零 page error。第 1 項便箋需「待播＋女角在場」同場先出，今次種子未觸發該組合，便箋路徑以 code 核實＋零 error 為據，留待下輪真玩覆核。
- 全套 suite 見 `~/workspace/suite384*.txt`（基線 402／9，九項 pre-existing 不變；8 項行號釘 resync `qa384/resync384.py`）。
