# NOTES v20a69 — STAGE69 台風訓練報名入口接線（細包）

基底 v20a68（PR #168）。用戶 2026-11-10 12:19 拍板開呢個細包。唔改 SAVE key
`starVolunteer_map_v19w`、softRev `s107`、產品 `?v=v20a10`；冇改 content pack JSON。
tests：70 基線＋新增 test_stage69_logic／test_stage69_static ＝ **72/72 全綠**（repo 根目錄 cwd 跑）；
新測試喺 v68 index 上行會 FAIL（logic 8 項／static 4 項），反證成立。

## 問題（v68 盤點發現，v68 之前已存在）

台風訓練（train_stage）有增益表（兩條結算路徑都有完整 case）、有堂數計法、
進階台風解鎖又依賴佢堂數（台風 3 堂），但佢唔喺 `TRAIN_BY_TYPE`、唔喺
`COURSE_ENROLL_EXTRA`、唔喺 `maybeUnlockMidCourses` 任何開放規則入面——
玩家冇任何路徑令 `S.enrolled.train_stage` 變 true，堂數永遠 0，進階台風永遠解鎖唔到。
連帶症狀：通告詳情「去練台風」捷徑（`preferredLocForTrainTarget`）一路將 train_stage
別名去 train_acting（送玩家去上演技堂頂替）；v68 指南對佢只能標「暫未有報名入口」。

全課程盤點（9 課逐課對照接線位）：主課（演技/歌藝/外貌）駐 TRAIN_BY_TYPE；
附帶課（魅力/智商/武師班）駐 COURSE_ENROLL_EXTRA＋累計堂數自動開放；
進階課靠所屬基礎課堂數開放。**得 train_stage 一課三邊都冇**，冇其他同類缺口。

## 接線決定（全部跟既有附帶課模式，冇發明新機制、冇改任何數值）

附帶課嘅既有模式（魅力/智商/武師班三課一致）＝ ①駐一類地點嘅 COURSE_ENROLL_EXTRA
（喺嗰類地點報主課嗰日有機會附帶開放）＋ ②maybeUnlockMidCourses 累計堂數自動開放
＋ ③ux68UnlockRule 指南鏡像。台風照跟：

1. **駐點：電視台（tv）**。`COURSE_ENROLL_EXTRA.tv: ["train_charm"]` →
   `["train_charm", "train_stage"]`。理據：台風＝鏡頭感／走位／綜藝場控（進階台風 hint
   就係「綜藝場控」），係電視台嘅本行；既有捷徑函數本身都係將台風目標指去電視台；
   tv 現有附帶得魅力一課，容量同 film（智商＋武師班兩課）相若。
2. **自動開放：任何訓練累計 2 堂**（同魅力同級——兩課都係早期表演系選修；
   武師班 3 堂／智商 4 堂係較後嘅專業課）。`maybeUnlockMidCourses` 喺魅力判定之後
   加一段同構判定，開放訊息跟進階課款式「台風課開放咗。」（冇 UNLOCK_STAGE 事件行，
   唔新造文案池）。
3. **指南鏡像同步**（v68 NOTES 訂明嘅同步義務）：`ux68UnlockRule` 加
   `case "train_stage"`（need「任何訓練累計 2 堂」、have 即時計）。
   指南地點欄本身零改動——`ux68CourseLocs` 由 COURSE_ENROLL_EXTRA 衍生，
   接線後自動列出星河電視台／九龍電視台／海港廣播（報主課附帶），狀態自動由
   「暫未有報名入口」變「未開放——任何訓練累計 2 堂（而家 N／2）；亦可喺…附帶開放」，
   前往自動指去星河電視台。實機已證（新遊戲指南截圖）。
4. **捷徑去別名**：`preferredLocForTrainTarget` 將 train_stage 拆出獨立分支，
   回傳 train_stage 本人＋電視台（格式跟武師班分支一致）；演技分支行為不變。
   修好之後，通告欠台風嗰陣「去練台風」會真係送玩家去報台風，唔再借演技堂頂替。

**冇郁**：增益表（台風 +4~6／壓力 +8~12 兩路徑原封）、堂數計法、進階台風門檻（3 堂）、
學費（台風本身免費）、TRAIN_BY_TYPE 主課表、其他課程嘅駐點／門檻、SAVE/softRev/?v=。

## 測試改動說明（一項基線斷言改版）

`tests/test_ux68_logic.js` 有一項斷言係 v68 當時將缺口「老實標示」嘅行為
（台風狀態＝「暫未有報名入口」）釘死。本包嘅目的就係消滅呢個狀態，故該斷言
改為新正確行為（條件進度＋電視台附帶途徑、唔再標冇入口），並喺原位寫明改版原因；
改版後斷言喺 v68 index 上行會 FAIL（已實證，啱啱好只 FAIL 呢一項），
同新測試一齊構成反證。其餘 69 個基線檔案零改動、全綠。

## 實機驗證（真 UI 駕駛，gate-on、槽 3、420px、本地鏡像；證據 verify69/）

- A 新遊戲：指南台風行新狀態＋三間電視台＋前往真達星河電視台 sheet（訓練分組＋
  報名掣齊）；零 pageerror。
- B 改植真存檔（演技已練 1 堂）→ 星河電視台真撳「進行演技訓練」報名一堂：
  結算 modal 同場列明「台風訓練｜手帳「訓練」可排」——即嗰一撳同時經附帶＋累計
  兩路徑開通台風；enrolled 真多咗 train_stage、演技堂數 1→2、錢冇扣（免費）。
- B 續：排今日行程 train_stage 真執行兩堂（增益 +4／+5、堂數逐堂 +1、費用 $0；
  其中一堂跨週結算另扣生活費 $1,300 係週結算唔係學費，modal 有「一週完結」明示）；
  第 3 堂結算 modal 直出「進階台風課開放咗」，enrolled 多咗 train_stage_mid；
  指南即時顯示進階台風「已開放」、台風訓練「已練 3 次」。
- D v68 構建存檔喺 v69 構建繼續：dayIndex／money 一致、指南（連台風新狀態）／
  地圖 13 墨字標籤如常；零 pageerror。
- 駕駛備註：「開始今日行程」會連跑其後已排嘅日子（本駕駛將其餘日子排 rest 隔離）；
  改植只限安排狀態（堂數/日數/行程槽位），所有斷言動作（報名、執行、解鎖、指南）
  全部經真 UI 同真遊戲碼。
