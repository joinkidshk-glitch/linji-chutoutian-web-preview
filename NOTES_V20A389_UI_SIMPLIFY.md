# v20a389 — UI 簡化（用戶 2026-11-23 08:58 批准開票）

依據：`linji-ui-simplify-2026-11-23/DECISIONS.md`（用戶逐條拍板十項）＋ `REPORT.md` 共識項。
GPT-6.2-sol 加強方案：`linji-drive389/gpt_ui389_plan.md`（拉柄手勢、進度 badge 抽屜、人情分段掣、傾談名牌貼紙、鎖定標籤＋差額格式）。
只改 UI 呈現同入口，唔改遊戲規則數字（SAVE key／softRev／產品 `?v=`／贏線 0.875／floor 140／warnLine 180／E1 門檻 350／試鏡判定／頒獎計分／結局判定全部不變）。

## 拍板十項落地

1. **逐張通告掣收埋入通告欄**：地點面板刪逐張「試鏡入口／接通告／查看檔期／暫未能報」掣（`addLocGigActs`／`addLocBridgeActs` 刪除；soft bridge 釘板改 openLoc 直接呼叫 `pinSoftBridgeOnBoard`），只留「通告欄（N）」一粒入口（N = `gigsForLocSeasonBoard` 數目，計算前先 `syncGigsForCalendarYear(false)` 同 advanceDay 一致，讀檔後未翻日唔會顯示（0））。ux68 matcher／icon matcher 改 `/^通告欄/`，tutorial 板標題改「通告欄 · 」。
2. **刪地圖打聽快捷掣**：移除 `#btn-ask369`＋`openAskPicker369`＋CSS；地點面板打聽保留。
3. **手帳重組 4 組 7 子頁**：行程（本週安排、衣櫃）、事業（作品、獎項、回憶）、帳本（帳目、庫存、資料卡）、人情（單頁分段掣「人情債｜人脈」）。衣櫃由獨立按鈕改子頁（`#home-pane-wardrobe`，`renderWardrobe265` 不變）；資料卡新頁 `renderStats389Pane()` 讀 `ledgerStatsParts()`；稱號摺疊入作品頁（`<details>`）；剪報併入回憶頁；進度子頁取消——本週安排頁加「進度 · 第N幕」badge，撳開 modal 抽屜（`#progress-list`，`renderProgressPane71` 原封）；`setHomeTab` 入口重定向（progress→plan＋開抽屜、tags→works、clippings→memory），所有 `enterHome("progress")` 呼叫不變。
4. **刪 ☰選單「手帳」掣，改拉柄**：地圖加 `#book389-handle`（「手帳 ↑」，44px，safe-area 上方），click 或 touch 向上掃 >24px 入手帳（同舊選單路徑 `kickScheduleIfNeeded()` → `goJournalFromMenu()`）。
5. **地圖「進度」掣保留唔改名**（冇郁）。
6. **傾談收埋去在場角色列**：工作地點（film/tv/music/ad）唔再出面板「同X傾談」掣，改渲染 `#loc-talk389` 名牌貼紙（人名＋「💬 傾談 · {talkCostLabel()}」），同 `confirmChoice236`→`doTalk` 流程；女角（rom176）照舊唔出。非工作地點不變。
7. **晨報「第二版」保留**（冇郁）。
8. **試鏡公佈照舊彈窗**（冇郁）。
9. **導演／製作人／播出檔期欄位保留**（冇郁；導演經 `gigProducerLineHtml` 摘要區渲染）。
10. **片酬＋簽約金分開兩行**（冇郁，原本已分行）。

## 共識項落地

- 通告詳情刪「差幾多達標」成版（`cn-train-jump`＋gapLines），只留 CTA（去訓練／手帳、去花園街成衣店）＋戲服提示行＋歌藝凍結註。
- 未達標要求格加「差 N」（`.cn-req-gap389`）；鎖定掣（cast-locked 震＋toast）刪，改詳情頂「🔒 暫未能報名」狀態標籤（`.cn-locked389`）。
- 「查看手帳／查看檔期／拍攝簿」統一「查看拍攝簿」（兩處 modal，`showJobs` 不變）。
- 約會掣未見面唔出：`addRom159DateActs` 加 `StoryOC.isDone(w.meet)` 檢查。
- 手帳「返回地圖」核實本來只得一粒（v71 已去重），冇改。
- 打聽情報去重：刪 `act_ho_tvb_rules`（同茶餐廳 `act_cha_tvb_rules` 同一段 `intelText`，全 repo 只定義一處）。
- 「免費」行動標籤改「不耗日」：`dayCostLabel(false)`＋`add()` 內 cost105 正規化器（輸入識別保留「免費」）；doScout lead「免費查看通告」→「不耗日查看通告」。訓練費 $0 顯示「免費」（`feeText`）係價格唔改。
- 「人情可兌現」組名核實本來已係「人情」＋徽章（v369），冇改。

## 驗證（Playwright 實駕，390×844 dsf 2，播種 d150 存檔，本地 HTTP 伺服器）

證據：`linji-drive389/`（probe389.json／probe389b–f.json＋截圖）。
- 地圖：打聽掣已刪、進度掣「進度」保留、拉柄 44px 可見、零橫捲（docSW 390）。
- ☰選單無「手帳」；撳拉柄入手帳成功。
- 4 組 7 子逐 tab 點擊全部可達；人情分段掣（人情債｜人脈）可切換；稱號在作品頁、剪報在回憶頁、資料卡有內容。
- 進度 badge「進度 · 第 6 幕・電視線」44px，抽屜有幕行＋✓。
- 返回地圖只一粒（`home-back-map-tabs`）。
- 工作地點面板：只有「通告欄（N）」一粒通告入口、無逐張掣、成本標籤「不耗日」無「免費」。
- 傾談貼紙：NPC 在場出貼紙（44px），撳入確認彈窗（「與何生傾談」）；女角在場唔出貼紙（葉敏芝在場實測）。
- 通告詳情（鎖定）：「🔒 暫未能報名」標籤、要求格「差 10」、無舊「差幾多達標」、CTA「去訓練／手帳」；片酬／簽約金／違約金分行、預計播出欄在。
- 約會掣：d150 未 meet 藍若曦／葉敏芝，電視台面板無約會掣（v388 對照組有，證明閘生效）；已 meet 林曉晴／周采兒茶餐廳照出。
- 情報去重：事務所面板無「入廠守則」，茶餐廳「打聽電視城規矩」保留一份。
- 全程 pageerror 0。

教訓：file:// 開頁會令 `content/*.json` fetch 失敗、通告庫空——實駕要用本地 HTTP 伺服器（`python3 -m http.server`）。

## Suite

**406 PASS／9 FAIL**（同 v388 基線完全一致，九項已知 pre-existing：flash51／slot50／soft_tip_111_restore／start53／weave43／weave44／weave49／wf5_87／wrap38）。
首跑 368／47——38 項新 FAIL 逐個覆驗：1 項真 code 問題（icons112：鎖定標籤 🔒 emoji 改 CSS 畫鎖 `.sp-lock-ico`）＋37 項測試釘舊 UI 結構／行號，按新結構 resync（行號釘經 `qa389/resync389.py` difflib 對位：travel114／rom159／rom176／gift185／tang171／tang173／tang152／text125；travel114 呼叫點總數 −2（openAskPicker369 刪除）；結構釘更新：book70／141／143／145、menu72、progress71／prog175、costume265／home272、titles162、locpanel118／ux68、r295／r335／weave47（刪已刪函數段）、contrast76／polish48／v155、loc96、text108／ui128a2、enc79／guidance34／rumor267／verify37（情報去重））。
