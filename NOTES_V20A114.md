# NOTES_V20A114 — 每日入地點出行額度（v20a114）

分支 `v20a114`（由 main `0bb85b2` 開出，唔掂 main，未合併、未推 main）。
用戶拍板 2026-11-12 07:09＋07:11 更正：入地點每日限 2 次，每次入場都計，連重入同一地點都計。

## 1. 實作摘要（`index.html`，+約 3KB）

- **常量**：`const TRAVEL114_DAILY_CAP = 2;`（`ENC79_DAILY_CAP` 下一行）。
- **狀態**：`S.travel114 = { day, used }`，跟 save 走（`JSON.stringify(S)` 整體存檔；
  `normalizeSaveObj` 只補預設值，唔會洗走未知欄；`saveQ()`／`saveToSlot()` 原樣）。
- **Helpers**（ENC79 常量區之後）：
  - `travel114State()`：lazy init——舊檔冇呢欄 → `{day: S.dayIndex, used: 0}`（滿額，
    唔會一載入就鎖死）；`day` 唔同今日就 rollover 歸零（唔靠日結鈎，週加速／跳日都啱；
    同一日重新載入唔會重置）。
  - `travel114Remain()`：`max(0, 2 - used)`。
  - `travel114IsFree(opts, id)`：免費只認四旗（`forceRestore`／`encDone`／`wf4Done`／
    `travelFree`）＋ `id==="home"` 守衛。**唔用 `atLoc === id` 做判據**——已核實
    `closeSheet()` 唔清 `atLoc`（入面只得一句註解「atLoc 留低」），返地圖再撳返同一地點嗰陣
    `atLoc` 仍然等於嗰個地點，分唔到「返轉頭」同「再入場」；而家規則係再入場都計，更加唔可以用佢嚟免費。
  - `travel114TrySpend(opts, id)`：免費 → `true`（唔計）；用晒 → `false`；否則 `used+1` → `true`。
- **閘口**（`openLoc`，三個 early return——`ending78Gate`／`isStoryPlayActive`／
  `todayIsForcedDay`——之後、`enc79TryIntercept` 之前）：被擋嘅入場唔擲巧遇；成功入場嗰次就算
  觸發咗巧遇都照計。被擋嗰陣 `toast("今日出行額度用完——今日已經去咗 2 個地方，聽日再去。")`
  然後 `return`（唔開 sheet、唔擲巧遇、唔扣數；玩家留喺原地，唔 kick 返地圖）。
  計數入場即 `saveQ()`，重新載入同一日唔可以刷返額度。
  閘口用 `typeof travel114TrySpend==="function"` 守衛——跟返下面 enc79／wf4 攔截嘅慣例；
  原因：`test_weave47_logic.js` 抽真 `openLoc` eval，sandbox 入面冇呢個 helper，
  裸引用會 `ReferenceError`（初版撞到，已修，見 §4）。
- **地圖顯示**：`drawMap` 每次渲染都刷新 `#map-hint` 入面嘅
  `<span class="map-hint-travel">`——有剩餘：「今日出行：仲可以去 N 個地方」；
  用盡：「今日出行額度已用完，聽日再去」。額度用完嗰陣，地圖釘同底欄地點掣加
  `travel-locked` class（CSS：釘 `opacity:.55`＋灰階、底欄掣 `opacity:.5`＋灰階），唔只靠 toast。
- **唔改**：`SAVE` key（`starVolunteer_map_v19w`）、softRev（`s107`）、產品 `?v=`（`v20a10`）、
  `ENC79_DAILY_CAP`（巧遇日上限維持 2 次不變）。

## 2. 核實過嘅前提（開工前實測，唔係照抄 brief）

- **LOCS 冇「屋企」**：15 個地點（`film_lion`／`rec_hk`／`tvb_longmen`／`tvb_kowloon`／
  `tvb_harbour`／`film_cotton`／`film_harbour`／`ad_central`／`ad_adm`／`rec_wanchai`／
  `rec_star`／`cafe_cha`／`agency_ho`／`gift_shop`／`hospital`），冇 `id:"home"`。
  屋企係行程動作（`enterHome`／`endBrowseDayGoHome`），唔經 `openLoc`；`id==="home"` 只係守衛。
- **行程執行唔經 `openLoc`**：`resolvePlannedDay`（37079–38003 行區間）本體零 `openLoc(` 呼叫；
  該區間唯一一處 `openLoc(locId)`（37797，改後行號）係 `maybeNudgeStoryEntry` 嘅進度頁
  「去現場播劇情」，玩家主動撳掣，計數。所以唔使為行程加 bypass。
- **`closeSheet()` 唔清 `atLoc`**：全文 `atLoc =` 只得 seed 傳送（30224／30228／30232）、
  `atLoc = null`（42754，`goToMapForBrowse` 附近）同頁內測試區；`closeSheet` 本體零 `atLoc` 賦值。

## 3. 計數規則清單（改後行號）

### 計（13 處，玩家主動導航，預設計數，唔加旗）

| 行 | 呼叫點 | 理據 |
|---|---|---|
| 31388 | `ux68GoLoc` 手帳「前往」 | 玩家喺手帳撳「前往」 |
| 34686 | 訓練建議「去報名」 | 玩家撳建議掣去報名地點 |
| 36799 | 訓練報名導航 | 玩家撳報名，系統帶去地點 |
| 37797 | 進度頁「去現場播劇情」 | 玩家撳掣去現場 |
| 38153、38156 | 地圖釘 `goPin`（最近針／後備 `L.id`） | 玩家撳地圖釘 |
| 38187 | 地圖底欄地點掣 | 玩家撳底欄掣 |
| 42683 | 人情債「去事務所」 | 玩家撳「去事務所」 |
| 56090 | `inv72GoShop` 去禮品檔 | 玩家撳庫存「去禮品檔」 |
| 56257 | `people72GoLoc` | 玩家撳人脈「去」 |
| 56400 | `jobs72GoBoard` | 玩家撳工作「去通告欄」 |
| 56421 | `jobs72GoLoc` | 玩家撳工作「去地點」 |
| 56871 | 開局屋企 modal「去睇劇情」 | 玩家撳「去睇劇情」 |

### 唔計（27 處）

| 行 | 呼叫點 | 理據 |
|---|---|---|
| 24189、52128 | 劇情播完刷新（`markDone` fallback／`refreshLocAfterStory`） | 重開 `atLoc`，返去原本嗰個地點，唔係新入場 |
| 27509 | `leaveStory` 離開劇情 | 同上，重開 `atLoc` |
| 30109、30110、30122、30123、30134、30135 | 病倒流程送去 `hospital`（體檢確認 modal「唔住」／dismiss、買體檢後「好，返去開工」／dismiss、醫院說明「明白」／dismiss） | 系統送去醫院，玩家已經喺醫院板，modal 關閉只係重開返同一板 |
| 30238 | 故事 seed 就緒，系統傳送去劇情地點 | 系統傳送，唔係玩家行 |
| 39642 | `wf4Fire` 完，`{wf4Done:true}` | 已有旗，確認唔計即可，冇再加旗 |
| 42340 | 人情債流程尾 `after()` 重開 `L.id` | 玩家仲喺 L（還款 sheet 喺 L 開出），返去而家身處地點 |
| 42363 | 人情債「取消」重開 `L.id` | 同上（**brief 未列**，開工核實上下文後補入——同一 `openDebtRepaySheet`、同一 `L`、同一「返去而家身處地點」理據；若果家長認為取消應該計，改返一行就得） |
| 51149、51237 | 巧遇播完，`{encDone:true}` | 已有旗，確認唔計即可 |
| 52504、52526 | 「劇情已完成」toast 後重開 `L.id` | 玩家仲喺 L，撳「播劇情」先發現已完成，唔係新入場 |
| 52661 | 聽完傳聞後 `reopen` | 返去而家身處地點 |
| 54130 | `{forceRestore:true}` | 已有旗，確認唔計即可 |
| 55540 | 傾談結果 modal `go`（唔耗日嗰條路） | 玩家仲喺 L；`spendDay` 嗰條路行 `runScheduleFromToday()`，唔叫 `openLoc` |
| 55867 | `promptAudition` 入面 `back` | 試鏡門檻唔過，返去而家身處地點 |
| 55985、55986、56021、56022 | 禮物店／送禮 modal 關閉／dismiss 後重開 `L.id` | 返去而家身處地點 |
| 56041 | `doGiveGift` 失敗後重開 `L.id` | 返去而家身處地點 |
| 56056 | 送禮結果 modal `go`（唔耗日嗰條路） | 同 55540 |

### 42325／43080 分類決定（brief 點名要交代）

- **42325（改後 42340）→ 唔計**：`openDebtRepaySheet(debtId, L, opts)` 嘅 `after()`；
  `L` 係開還款 sheet 嗰陣傳入嘅地點（事務所），玩家還款前已經身處 L，還完重開 L 係「返去」唔係「去」。
  `fromJournal=true` 嗰陣 `after()` 行 `closeSheet()` 直接返手帳／地圖，連 `openLoc` 都唔叫。
- **43080（改後 43095）→ wrapper 轉發 opts**：`window.__phase2.openLoc` 由
  `function(id){ openLoc(id); }` 改成 `function(id, opts){ openLoc(id, opts); }`。
  呢個係 QA／debug harness 對外 API，repo 入面（`index.html`／`tests/`／`qa*/`）**零呼叫點**
  用佢；改成轉發 opts 等將來經佢入嚟嘅呼叫都可以帶 `travelFree`。本身唔計入計／唔計清單。
- **57207（改後 57258）→ 頁內測試 code，唔改**：喺 `runSoftP0Checks()`（57183–57318 行）
  入面，`S.dayIndex += 7; … openLoc("ad_central")` 係斷言測試（`bad("ui_row")` 等），
  唔係玩家路徑。57300 係同一函數入面嘅字串檢查
  （`showB01HomeModal.toString().indexOf("openLoc(\"cafe_cha\")")`），唔係呼叫，唔改。

## 4. 測試

- **基線**（乾淨 main `0bb85b2`，開工前實測，`qa114/suite_baseline114.txt`）：
  **146 PASS／12 FAIL**。家長 brief 話 142／12，實測係 146／12——差嗰 4 係 v109 兩包
  新加嘅測試檔（`qa109b/suite_baseline109b.txt` 142→工作版 144，再加之後嘅包）；
  12 FAIL 清單同已知環境性 static FAIL 逐字相同
  （flash51／giglib36／pacing35／poster59／rumor49／slot50／soft_tip_111_restore／
  start53／weave43／weave44／weave49／wrap38）。
- **新測試**（`tests/test_travel114_logic.js`、`tests/test_travel114_static.py`）：
  logic 30 斷言全 PASS、static 68 斷言全 PASS。
  Logic 覆蓋：第一次計 1、第二個唔同地點計 2、第三次被擋（used 唔郁）；**重入同一地點都計**
  （兩次入 `cafe_cha` 用晒額度，第三次被擋）；四旗＋屋企唔計；換日 rollover；
  舊檔初值滿額；save／load round-trip 後 used 一致；反證兩則（cap 改 99 → 第三次放行；
  計數行刪走 → used 永遠 0、第三次唔被擋）。
  Static 覆蓋：常量逐字、閘口喺 `enc79TryIntercept` 之前／`todayIsForcedDay` 之後、
  toast 文案逐字、計數即 `saveQ`、地圖剩餘次數行＋鎖定視覺、**呼叫點分類覆蓋**
  （全部 44 處 `openLoc(` 逐個核對：免費 27＋計數 13＋定義／wrapper／測試區 4，零漏網；
  免費清單逐行驗帶旗、計清單逐行驗冇帶旗）、SAVE／softRev／`?v=` 唔變。
- **回歸**：中途撞到一處——初版閘口裸引用 `travel114TrySpend`，
  `test_weave47_logic.js`（抽真 `openLoc` eval）即 `ReferenceError` FAIL。
  修法：閘口加 `typeof` 守衛（同 enc79／wf4 攔截慣例一致），weave47 即刻返 PASS；
  新測試補咗一則斷言釘死呢個守衛。
- **全套 A/B**（`qa114/suite_work114.txt`）：**148 PASS／12 FAIL**——淨係多咗兩隻新測試 PASS，
  12 FAIL 清單逐字相同，**零新增回歸**。
- `node --check`（主 script 抽出）：PASS。

## 6. Rebase 到 main `2b42ca0`（統籌跟進，v111／v112／v115 期間上線）

- 原分支基於 main `0bb85b2`；合併前 rebase 到 `2b42ca0`，**一處衝突**：地圖底欄地點掣嗰行——v112 將圖標改成 `iconHtml112(L.emoji||"")`，v114 加咗 `travel-locked` class；解法係兩邊都要（`iconHtml112`＋`travel-locked`），行號 38352。
- Rebase 後 `tests/test_travel114_static.py` 曾 FAIL（行號寫死，v111／v112／v115 喺上面加咗行，全部呼叫點行號移位；**產品 code 本身冇問題**，logic test 唔靠行號，全程 PASS）。修法：將 `FREE_LINES`／`COUNT_LINES`／`DEF_LINE`／`WRAPPER_LINE` 全部按新版實量行號更新（逐行原文＋出現次序對位，免費 27＋計數 13＋定義／wrapper，零漏網），static test 返 PASS。
- 上面 §3 嘅行號表係舊基底（`0bb85b2`）嗰版；新基底行號見 static test 入面嘅清單，分類內容不變。
- Rebase 後全套重跑：見 `qa114/suite_rebased2_114.txt`（預期 151 PASS／12 FAIL；main `2b42ca0` 基線係 149／12，淨多兩隻新測試）。

## 5. 已知限制（畀統籌／用戶定奪）

- **主線劇情地點都計數**：玩家嗰日用晒額度，劇情地點要聽日先去到。劇情窗口普遍以日／週計，
  實測未見即日死線；若果家長想劇情地點豁免，再傾（要改嘅話，`openLoc` 閘口加
  「目標地點有未播主線」豁免係一行起兩行止，但會開返刷巧遇嘅口——劇情地點好多都有星出沒）。
- **開局第一日**：舊檔初值滿額；新開局 `S.travel114` 未建，第一次入場先 lazy init，
  唔會未開始就鎖死。
- **額度唔可以刷返**：只喺 helper 入面改；取消行程／重新載入／week 加速唔掂呢個欄
  （rollover 只睇 `S.dayIndex`；計數入場即 `saveQ()`，reload 同日唔重置）。
  唯一例外：玩家手動改 localStorage——同其他所有存檔欄一樣，唔擋。
- **未做實駕**：subagent 冇 live browser；地圖剩餘次數行＋鎖定視覺＋被擋 toast
  只驗到靜態／邏輯層，實機畫面要統籌／主 agent 實駕核實。

## 7. 合併紀錄（統籌跟進）

- 合併：squash 入 main，commit `cf66865`（基底 main `4d967ed`，即 v113 合併後）；合併前全套重跑 **154 PASS／12 FAIL**（12 FAIL 為已知環境性 static FAIL，零新增）。
- 線上核實：Pages 部署約兩分鐘後對上數——`index.html` **5,101,629 bytes、sha256 `672e34db45059e61bf769aec672253d13fe4de23246ba1682d138ddf5a2dc68c`**，同本地 main 逐 byte 一致，唔使重觸發。
- 合併後冒煙實駕（main `cf66865`，本地鏡像＋Playwright，槽 3）：**6/6 PASS、0 pageerror**——地圖顯示／計數／鎖住 toast 逐字／重入同一地點都計／過一日重置／巧遇（陸柏言＠天星音樂）正常觸發。證據：`qa114/drive_merged_114.py`＋`drive_merged_114.json`＋`drive_merged_report.md`＋`shots/merged114/`（14 張）。
