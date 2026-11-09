# v20a58 休息加體能 bug 修復（基線 v20a56，4,314,004 → 4,313,981 bytes，−23）

用戶實玩報告：休息會莫名其妙加體能。根因（主代理已定位）：遊戲冇獨立精力值，疲勞只用壓力表達，但休息系動作結算誤將「回復」寫入可訓練屬性 `stamina`（體能，通告要求會查），等於瞓覺免費練功。本版只刪增益、唔調任何數值平衡；改動共 **10 行**（diff 20 行含改前改後），外科式，方便疊喺 v20a57 之上出貨。

## 逐行改動清單（行號以 v20a56 index.html 為準）

| # | 行 | 位置 | 改前 | 改後 |
|---|---|---|---|---|
| 1 | 28448 | `resolvePlannedDay` 週計劃 rest 日 | `notes=apply({stamina:20+R(0,8), stress:-(18+R(0,8))})` | `notes=apply({stress:-(18+R(0,8))})` |
| 2 | 28449 | 同上 home_chore 日 | `notes=apply({stamina:8+R(0,4), money:R(0,200), stress:-(6+R(0,4))})` | `notes=apply({money:R(0,200), stress:-(6+R(0,4))})`（money 原封） |
| 3 | 37255 | `doRest()` 地點「休息室歇陣」 | `apply({stamina:16+R(0,8), stress:-(14+R(0,8))})` | `apply({stress:-(14+R(0,8))})` |
| 4 | 28010 | `endBrowseDayGoHome()` 提早休息（選單獨立掣＋二次確認嗰條） | `apply({stamina:6+R(0,4), stress:-(4+R(0,4))})` | `apply({stress:-(4+R(0,4))})` |
| 5 | 26369 | PLAN_ITEMS rest hint | `hint:"大回復體能 · 減壓"` | `hint:"瞓足一日 · 大減壓"` |
| 6 | 26370 | PLAN_ITEMS home_chore hint | `hint:"小回復＋減壓"` | `hint:"執屋 · 小減壓"` |
| 7 | 26181 | `courseForStatKey` 映射 | `stamina:"rest"` | `stamina:null`（同 fame/popularity 同級：冇課程捷徑，行 map 模式） |
| 8 | 26192 | `preferredLocForTrainTarget` rest 分支條件 | `if(stat==="stamina" \|\| stat==="stress" \|\| courseId==="rest")` | `if(stat==="stress" \|\| courseId==="rest")` |
| 9 | 26227 | `bestTrainJumpForGig` map 模式標籤 | 一律 `去地圖接單攞幕前聲望（…）` | fame/popularity 先用聲望版；其他（含 stamina）用中性 `去地圖接單（…）`，唔再對體能缺口講錯話 |
| 10 | 35901 | 地點 sheet doRest 掣副標籤（**清單外追加一處，同類文案對齊，可獨立還原**） | `add("休息室歇陣","回復／減壓","+1日", …)` | `add("休息室歇陣","減壓","+1日", …)`——doRest 改後只減壓，「回復」字眼會誤導，故同步改；只係一個詞 |

壓力減免幅度、home_chore 嘅 money、其餘效果全部原封；冇掂 SAVE key／softRev／?v=。

## ⚠️ 目標建議嘅重要發現：遊戲根本冇「體能訓練課程」

主代理原指示係「stamina 改指真正嘅體能訓練課程」。全檔核實後：**唔存在**。現有課程得 8 個（COURSE_DEFS＋訓練日結算逐個核對）：train_acting（演技）、train_stage（台風）、train_vocal（歌藝）、train_looks（外貌＋魅力，hint 寫「健身造型」但**結算唔加 stamina**）、train_charm（魅力）、train_iq（智商＋演技）、train_acting_mid、train_stage_mid——冇一個加體能。`train_jump` 只係按鈕 CSS class，唔係課程。

所以冇得「指返去邊個 course」：指去 train_looks 一樣係呃玩家（上完堂體能唔升）。本版採最細誠實修法：stamina 同 fame/popularity 同級回 `null` → 建議退返「去地圖接單」中性提示，唔再叫人休息升體能。若產品上想要真・體能訓練（例如加一課「體能鍛鍊」），嗰個係內容新增，唔喺 bug 修復範圍，留畀主代理／用戶定奪。

## Flavor／事件掃描結論（全檔 `apply`/delta 含 stamina 嘅位已全數列齊）

### 已修（恆常、可由玩家主動重複嘅休息系路徑）：上表 #1–#4 四條，冇漏。

### 冇郁・留畀主代理定奪：週結自動 flavor（27121–27129，settleWeek 內）
- 27122：`S.stamina<12` 時 `apply({fame:-2, stamina:5, stress:5})`＋WEEK_LOW_STA 文案——見底救濟。
- 27126：`stressAtEnd<75` 時 `apply({stamina:8, stress:-6})`＋WEEKEND_SOFT 文案（「週末。睡到自然醒，體能慢慢回來。」）——註解自稱「Weekend soft recovery」。
- 27129：其餘情況 `apply({stamina:4})`＋「週末稍歇，壓力後遺仍在。」

判斷：三者都係**每週結算自動派一次**，唔係玩家可以㩒掣無限刷嘅動作，同四條休息路徑性質唔同；但效果上等於體能每週恆常 +4～+8，同「休息唔加體能」嘅裁定方向有張力（尤其 27126 明文係「瞓覺回體能」）。按任務守則冇自作主張刪——請主代理定奪：(a) 視為週末自然回復、保留；定 (b) 一併收走（27126 嘅 WEEKEND_SOFT 文案要跟住改）。靜態測試已加一條斷言鎖住 27126 現狀，方便日後改嗰陣有跡可尋。

### 冇郁・事件內容（一次性抉擇獎勵，保留）
- 36158／36168／36182：拍攝日抉擇（v20a35 setChoiceOffer 系）delta 含 stamina +4／+3／+5（「早啲返去瞓」「自己食，快啲抖下」「買罐咖啡頂住」）——屬劇情抉擇內容，每次抉擇只生效一次，唔係恆常路徑，按守則保留。

### 附註觀察（冇郁）
- Code 層面 stamina **冇任何恆常扣減位**：拍攝日 `shootDailyDelta` 唔掂 stamina；stamina 實際只做門檻（通告 req、試鏡 <25 打七折、報名訓練 <5 被擋）。即修完之後，體能嘅升跌來源剩返：初始 75、週結 flavor（上段待裁）、事件抉擇、內容包事件 delta。呢個係數值設計現況，只報告唔評論。

## 驗證
- 全套 tests **46/46 PASS**（基線 44＋新增 2）；兩個 script block `node --check` PASS。
- 新增 `tests/test_rest58_logic.js`（17 斷言）：真 apply＋真 resolvePlannedDay行 rest／home_chore、真 doRest、真 endBrowseDayGoHome——四路徑 stamina 前後不變（50→50）而 stress 有減（60→42／53／42／54）；courseForStatKey('stamina')≠'rest'、stress 保留 'rest'；stamina 建議 mode='map' 唔係 'rest'；兩條 hint 文案冇「體能／回復」兼有「減壓」。
- 新增 `tests/test_rest58_static.py`：四路徑 apply 正則核實冇 stamina（home_chore 鎖埋 money 原式）、文案字串、映射、SAVE key、27126 保留斷言。
- **反證成立**：兩套新測對 v20a56 index 均 FAIL（邏輯測 9 項 FAIL、exit 1）。
- 既有測試同步：`tests/test_flow45_static.py` 兩條「formula unchanged」鎖本身係釘住舊 bug 公式（`stamina:6+R(0,4)`／`stamina:20+R(0,8)`），已更新為 v58 新公式＋斷言舊公式消失，並加註解講明——鎖嘅用途（防靜靜漂移）保留，唔再鎖死 bug。呢個係全套入面唯一因本版而要改嘅舊測試。
- 冇推 repo。

---

# v20a58 擴展（用戶拍板：加體能訓練課程＋收埋週結暗加）

rest-only 版 4,313,981 → **4,315,337 bytes**（+1,356）。跟足現有課程結構接線，冇自創機制；冇掂 SAVE key／softRev／?v=。

## 一、新課程「武師班」train_stamina（逐處改動，行號以擴展後 index.html 為準）

| # | 行 | 位置 | 改動 |
|---|---|---|---|
| E1 | 18051 | `COURSE_DEFS` | 新增 `train_stamina: { icon:"🥋", name:"武師班", hint:"拳腳／體能", midOf:null }`（插喺 train_iq 之後、進階課之前） |
| E2 | 18057 | `COURSE_ENROLL_EXTRA` | `film: ["train_iq"]` → `film: ["train_iq", "train_stamina"]`（電影地點報名時 55% 附帶報名，照 iq 喺 film 嘅既有路徑） |
| E3 | 18078 | `EVENTS_ZH_HK`（整包同一行） | 新增 `TRAIN_RESULT_stamina` 3 句（「武師班落堂，你成身汗，腳步卻穩咗。」等）＋`UNLOCK_STAMINA` 2 句 |
| E4 | 26182 | `courseForStatKey` | `stamina:null` → `stamina:"train_stamina"`（上一手嘅誠實 null 而家有真課可指） |
| E5 | 26215–26218 | `preferredLocForTrainTarget` | 新增 train_stamina 分支：指去電影地點（`pick(l=>l.type==="film","film_lion")`，mode:"train"），照 train_iq 嘅 film 模式 |
| E6 | 26854–26857 | `maybeUnlockMidCourses` | 新增：累計訓練 ≥3 堂自動開放（夾喺魅力 total≥2 同智商 total≥4 之間，照 charm/iq 雙路徑模式：附帶報名＋自動開放） |
| E7 | 27811 | `stressDeltaForAct` 預覽表 | 新增 `train_stamina:10`（同演技/台風/歌藝同級） |
| E8 | 28454 | `resolvePlannedDay`（手帳排程堂） | 新增分支：`apply({stamina:4+R(0,2), stress:8+R(0,4)})`＋trainCount/weekTrainDone/maybeUnlockMidCourses＋TRAIN_RESULT 句，逐字照 train_acting 分支格式 |
| E9 | 36977 | `applyTrainLesson`（即場報名堂） | 同 E8 同公式同接線 |

**數值對照（點解呢個數）**：對照同級主屬性課 train_acting／train_stage／train_vocal——三者都係主屬性 +4~6（`4+R(0,2)`）、壓力 +8~12（`8+R(0,4)`）、零收費（堂費只得 train_looks 有 $800，因為係形象／造型課）。武師班逐項照抄呢一級：體能 +4~6、壓力 +8~12、免費。唔會變唯一最優解：佢只升體能（門檻型屬性），唔兼升其他屬性（唔似 train_iq 兼 +1 演技、train_looks 兼 +1 魅力），亦冇進階版。地點揀電影廠：武師班／龍虎武師係片廠班底文化，同「跟張子駿班底學動作戲」嘅動作戲線呼應；遊戲入面「武師」本身已係既有詞彙（通告角色、傳聞來源）。

**連帶效果**：上一手改動 #9 嘅中性標籤（非聲望缺口→「去地圖接單」）而家只剩 fame/popularity 行嗰條路；體能缺口會行返 train 模式標籤（未報名：「去練體能（差 X｜地點）」／已報名：「入手帳排『武師班』」），唔使再改。

## 二、收埋週結暗加（settleWeek flavor，27130–27138 一帶）

| # | 行 | 改前 | 改後 |
|---|---|---|---|
| W1 | 27131 | `apply({fame:-2, stamina:5, stress:5})`（體能 <12 救濟） | `apply({fame:-2, stress:5})`——fame/stress 原封，只刪 stamina |
| W2 | 27135 | `apply({stamina:8, stress:-6})`（週末回復）＋註解「（體能+8 壓力−6）」 | `apply({stress:-6})`＋註解改「（壓力−6）」；同行 fallback 文案「週末休息，體能回升。」→「週末休息，壓力稍降。」 |
| W3 | 27138 | `pushFlavor(apply({stamina:4}))`＋`pushFlavor("週末稍歇，壓力後遺仍在。")`（恆常） | 刪走 apply 行，只留文案行（文本身冇承諾體能，保留） |
| W4 | 18078 | `WEEKEND_SOFT`：「體能慢慢回來。」「先把體能養回來。」 | 改「整個人都鬆了。」「先把精神養回來。」（講精神/壓力回復，唔再承諾體能） |
| W5 | 18078 | `WEEK_LOW_STA` 第二句「體能不足，開工前先睡夠。」 | 改「體能不足，重通告先別接。」（刪走「瞓夠」暗示；第一句警告句同 27132 fallback 警告句保留——係提示玩家體能低，唔係回復承諾） |

收完之後，體能嘅恆常增長來源只剩武師班（＋一次性事件抉擇 delta，上一手已裁定保留）。附註觀察（冇郁）：stamina 本身冇恆常扣減位（見上文），所以冇咗週結暗加唔會造成體能只跌唔升嘅死局；`doEnroll` 嘅 stamina<5 擋報名只影響即場第一堂，手帳排程堂同自動開放唔經佢，新手初始體能 75 亦遠高於門檻。

## 三、既有測試同步（2 條斷言，因行為有意改變）

- `test_rest58_static.py`：「stamina:null」斷言 → 改斷言 `stamina:"train_stamina"`；「週結 flavor 27126 保留（範圍外）」斷言 → 改斷言暗加已收。兩處都加咗註解講明係 v58 擴展裁定，同上一手改 test_flow45_static 嘅處理一致（鎖嘅防漂移用途保留）。
- `test_rest58_logic.js` 唔使改：佢嘅斷言係「stamina 唔再指 rest／mode 唔係 rest」，新行為（指去真課程、mode=train）照樣成立。

## 四、驗證

- 全套 tests **48/48 PASS**（基線 46＋新增 2）；兩個 script block `node --check` PASS。
- 新增 `tests/test_stamina58_logic.js`（29 斷言，Math.random 釘死 0 取下限）：建議映射＋電影地點＋通告缺體能跳轉；排程堂同即場堂 stamina 50→54、trainCount 入帳；電影地點 doEnrollRun 真路徑附帶報到 train_stamina＋手帳清單見到「武師班」；累計 2 堂未開／3 堂開；週結三分支行真碼（抽 settleWeek 原文區塊 eval——抽取要用結束錨點，template literal 嘅 `${}` 會騙過括號配對）stamina 全不變、fame −2／stress +5／−6／不變各保留。
- 新增 `tests/test_stamina58_static.py`（19 斷言）：九處接線、兩路徑同公式各 2 次、暗加三式消失、舊文案清零。
- **反證成立**：將上述 13 處改動逆向還原重構 rest-only 版（重構後 4,313,981 bytes，同 rest-only 紀錄一字不差），新邏輯測對住佢 20 項 FAIL、靜態測 18 項 FAIL；同時 rest58 邏輯測對住還原版全 PASS，證明還原忠實、唔係靠整爛個檔嚟 FAIL。
- 冇推 repo。
