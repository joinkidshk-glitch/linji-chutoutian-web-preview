# NOTES_V20A77_HUB — v20a77「劇情／進度全套整合」

用戶 2026-11-10 17:46 反映：進度頁好用，但想直接喺大地圖撳掣入到；
同時坦承搞唔清「進度」同「劇情」分別。17:51 經選項拍板**全套整合**：
進度頁做唯一章節清單兼播放門口，舊劇情列表入口全部收埋。

## 改動（四項）

1. **大地圖常駐「進度」掣**（`#map-progress-btn`）：浮喺地圖右上
   （top:44px／right:8px，紙底＋金框＋墨字 pill），獨立於 hint 內容——
   hint 係內容／pending／失敗邊個狀態都撳得；撳落去行
   `enterHome(null, false, "progress")`（同 v71 hint 掣同一落點）。
   開地點 sheet 時跟 `.map-hint` 一樣隱藏，唔遮地點面板。420px 實測
   bounding box 同 legend／13 個地名標籤／釘熱區零重疊（證據 verify77/）。
   hint 金框既有撳入進度行為保留。

2. **刪 ☰ 選單「劇情」掣**：掣本體連 `#menu-story-badge` 元素同
   handler 嘅 `story-play` 分支一併移除；選單其餘（手帳／提早休息／
   系統組）冇郁。`paintStoryEntryHints` 對 badge 嘅更新本身有
   `if(badge)` 守衛，元素唔喺度自動跳過——安全降級，碼保留並加註明。

3. **頂欄 `#chip-story` 改指進度頁**：標籤「劇情」→「進度」（數字
   `#chip-story-n` 同更新機制保留）；click 改行
   `enterHome(null, false, "progress")`，唔再開 playOpenPicker，
   亦唔再先行 story commit（進度頁係手帳子頁）。`paintStoryEntryHints`
   四款 title 改「主線進度」語系：可播「主線進度 · 有 N 幕可播」／
   載入中「主線內容載入中」／暫無「主線進度（暫無可播）」／失敗
   fallback「主線內容載入唔到，請再開多次」。

4. **進度頁做播放門口**：`renderProgressPane71` 嘅「已開放」行加在場
   判定——照抄 picker（pickerHereBlock）嗰套
   `StoryOC.evalNode(node, { checkNodePhase:true, player:true })`，
   `ev.ok` 先出「播呢幕」掣＋「你而家喺 X，可以即刻播呢幕。」；
   唔在場維持「去 X 就會觸發。」文字、唔出掣。掣嘅 click 用委派掛
   `#progress-list`：先 `ensureWeekPlanCommittedForStory()`，再
   `StoryPlay.start(id)`——同地點 sheet 觸發完全同一條路徑（start
   本身會再驗在場同 homeEditable 閘）。已完成／已錯過／未開放三態
   維持 v71 原樣。順帶改寫開放行舊 fallback 文案（原本叫人「開劇情
   列表播」，列表已冇玩家入口）。

## 舊入口收尾（全部改指進度頁）

- 劇情播完畫面兩粒「劇情列表」掣 → 改名「進度」，on 改
  `enterHome(null, false, "progress")`（clearPendingB01Flag 行為保留）。
- `maybeNudgeStoryEntry` 提示 modal：掣「打開劇情」→「睇進度」；
  正文改提頂欄／地圖「進度」掣。
- `wireHomeStoryHint` fallback：有可播幕時改去進度頁（舊版開 picker）。
- 玩家文案跟進：日結算 modal「頂欄『劇情』或選單可進」、回家 modal
  兩句「頂欄『劇情』」、教學 TUT_DONE「再打開選單『劇情』」——全部
  改指「進度」掣（教學係 index 內嵌 fallback 字串；若線上 pack 覆寫
  教學文本，pack 側要同步，見報告）。

## playOpenPicker 處置：保留做死碼

函數本體同 api 導出保留，加 HUB77 註明「已冇玩家入口」。理由：
舊測試（verify37 logic/static、progress71 static）直接引用佢驗證
picker 行為，成個移除要大改三檔測試、風險唔成比例。玩家可達呼叫點
已清零——全域 `StoryPlay.playOpenPicker()` 只剩隱藏 debug 接線面板
（`?debug` 先出現）嘅「可出列表」一處，屬開發工具，唔係玩家入口。

## 冇改

SAVE key（`starVolunteer_map_v19w`）／softRev（`s107`）／產品 `?v=`
（`v20a10`）／pack JSON／章節開放判定／門檻／任何數值，一律冇掂。

## 測試

- 新增 `tests/test_hub77_static.py`（對 v76 index 行會 FAIL）。
- 原位改版：`test_menu72_static.py`（選單清單／handler 期望移除
  story-play；徽章斷言改「已移除」）、`test_terms57_static.py`
  （chip／menu 標籤斷言改 v77 形態）——原因均已喺原位註明。
