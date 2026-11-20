# v20a344：請柬註解漏出修復＋晨鏈繞鏈硬化

Base：main `2c30c80`（v343，通告庫 323 張，index.html 47,316 行，suite 396／9）。
改動：index.html 4 行同行替換（行數不變，零釘行漂移）＋新測試 1 檔。

## Bug 1（真，玩家面）：請柬漏出 JS 註解

- 現象：請柬 modal 正文出現一行 JS 註解原文
  `/* v20a218 C-B1：請柬要講明「預約」——點擊出席唔係即刻播，係預約咗嗰晚收工之後播；合成 pack（自檢假請柬）唔出呢行 */`
  （drive-192 三場請柬截圖全部有）。
- 根因：`renderAwardInviteHtml`（L31202）return 嘅 template literal 入面，
  L31232 嗰行喺 `${...}` 表達式之後、反引號之內寫咗 `/* ... */`——template
  literal 入面嘅 `/*` 唔係註解，照字面渲染。
- 修法：註解移出 template literal，改做 JS 註解放喺 `return` 後、反引號前
  （同一行，內容原樣保留，另加一句 v20a344 移出原因）。L31232 只刪走尾隨註解，
  k213 IIFE 本身一字唔郁——「出席即預約」行、合成 pack 唔出呢行嘅行為不變。

## Bug 2（潛在風險）：兩條路繞過晨鏈直接結算日

- 現象：`startTodayScheduleFromMap()`（L20768）同 `kickScheduleIfNeeded()`
  （L20844）直接 `resolvePlannedDay(id)`，唔經 `morningChain196`。drive-192
  harness 首跑程式化撳中俾 modal 遮住嘅 `#map-start-today`（真玩家撳唔到，
  屬 harness artifact），結果典禮＋報紙齊遲一日——證明呢條繞鏈路一旦被觸發
  就會靜默延遲典禮同晨報。
- 修法：兩函數改跟 `runScheduleFromToday` 同一寫法：
  `morningChain196(()=>{ resolvePlannedDay(id); }, { mapMode:false })`
  ——先行全晨鏈（昨晚典禮→殺青獎勵→請柬→晨報→試鏡消息→抉擇即派→WF4→
  病假→強制播）再跑當日行程。
- 安全判斷（逐 call site）：
  - 無遞迴：`morningChain196` 鏈尾 kick 只喺 `mapMode:true` 先行（L21235）；
    兩函數用 `mapMode:false`，內層鏈唔會再 kick 自己。
  - 無雙跑呈現：各 presenter 冇 pending 就回 false；典禮
    `awards213PlayBookedEvening` 播之前 one-shot 清旗（`awards213ClearBooked`，
    註明「唔怕重入／雙掛點重播」）；晨報 `pullDueNewspaperEdition` pull 嗰刻
    已將成批出隊寫入 `S.pendingMorningPaper`，重入只會回同一份 pending。
    從鏈尾（mapMode）入 kick 嗰陣，所有 presenter 啱啱行完回 false，內層
    第二 pass 全數跌落去 `resolvePlannedDay`，無雙彈。
  - 行為對齊：kick 強制日而家同 `runScheduleFromToday` 一致——強制播
    （`story165TryForcedPlay`，afterKind="schedule"）喺當日行程之前播，
    以前 kick 路徑會跳過強制播等下一條鏈先播。
  - kick 合約不變：仍然同步回 true（接管流程），各 caller
    `if(kickScheduleIfNeeded()) return;` 語義唔郁。
  - call site 清單（全部係用戶動作 handler 或鏈尾，冇一處喺 presenter
    modal 呈現期間併發觸發）：
    - `startTodayScheduleFromMap`：L22195 `#map-start-today` onclick；
      L46902 `leaveHomeFromNotebook("start-today")`。
    - `kickScheduleIfNeeded`：L6472 `costume265Sleep`、L20834
      `confirmEarlyRestFromMenu`、L21235 `morningChain196` 鏈尾（mapMode）、
      L42546 `openLoc` 強制日閘、L45814 `showInventory`、L45868 `showStats`、
      L46036 `showPeople`、L46270 `showJobs`（四個舊選單重定向）、
      L46905 `leaveHomeFromNotebook`、L46968 選單 home／journal。
    每一處硬化後都係「先呈現到期晨鏈內容，再跑當日行程」，只會令原本可能
    被靜默延遲嘅典禮／晨報準時，唔會多出或漏出任何呈現。

## 測試

- 新測試 `tests/test_r344_invite_comment_fix.js`（28 項 ALL PASS）：
  抽 live 真函數渲染請柬（nominee／gallery／空 pack／合成 pack 四種）斷言
  輸出唔含 `/*` 同 `v20a218`、「出席即預約」行照常出、註解文字仍喺
  index.html 做 JS 註解、template literal 區內無 `/*`；抽兩硬化函數真跑
  （stub 晨鏈／resolve），斷言先行 `morningChain196`（mapMode:false）、
  `resolvePlannedDay` 只喺鏈尾 finalFn 先行、地圖日／wrap 日／非強制日
  行為不變、兩函數體無裸 `resolvePlannedDay(id);` 直呼。
- 反證：同一測試對 v343 舊 index.html 有 15 項乾淨 FAIL（兩 bug 都捉到）。
- 相關舊測試覆驗全 PASS：dayflow196（logic＋static）、dayend189、
  guidance34、flow45、story165、awards182／184／186／192／194／200／211／
  213／62／63、gate136。
- 全套 suite：見落地紀錄（預期 397／9，九項 FAIL 同 v343 基線逐項一致）。

## 跟進提示

- drive-192 附帶觀察（唔係今票範圍）：gallery 報紙正文有廣東話口語
  （「陳偉翔坐喺台下睇完整晚——未輪到佢上台」），同報紙書面語規則有出入，
  留待之後文字潤飾處理。
- 實駕 backlog 剩 1 項：第三年贏＋1992 年 12 月結局未喺正常實玩證明。
