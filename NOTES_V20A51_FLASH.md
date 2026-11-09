# v20a51 入何生事務所深色長方形閃爍 — 根因＋修復

## 用戶報告
2026-11-09 21:54 實機：喺地圖篤入「何生事務所」嗰陣，有一個深啡黑漸變長方形好快閃過；
截圖捕捉到佢喺畫面右側（闊約 1/3、高約 1/3），覆蓋地圖右下＋地點 sheet 場景相右上，之後消失，sheet 內容正常。

## 根因（實錘，harness 複現同用戶截圖逐項吻合）
閃嗰個係**設計本身嘅「推門」動畫** `.push-door`（`playPushDoor()`，主檔行 31340），
只喺 `openLoc` 結尾、`id==="agency_ho"` 時呼叫（行 35449）——所以只有入何生事務所先有，其他地點冇（harness 對照 cafe_cha：全程冇 #push-door 元素）。
門板 `.push-door-slab` 漸變 `linear-gradient(90deg,#2a2118,#6b4e2e 55%,#1a1410)`、尺寸（實測）闊 65.6% × 高 26.4% 視口，
0.7s 內向右滑。佢睇落似故障閃爍，係三個缺陷疊加：

1. **門鈴一早出畫面**：`.push-door-bell`（金色「叮」）喺門框 `right:8%`，而成個門框會 translateX 到自身闊度 +86%；
   實測舊版門鈴喺 t≈215ms 已成個出咗畫面右邊（x=413 > 390）。即係成個效果約 80% 時間只剩一塊冇任何門特徵嘅深色板。
2. **門板蓋住地點 sheet**：`.push-door` z-index 45（#v-map 內），地點 sheet 只係 z-20，兩者同時出現 → 門板油漆喺場景相上面（用戶截圖＋harness 舊版截圖 `flash_agency_2.png` 都影到板蓋相角）。
3. **消失係硬切唔係淡出**：動畫 700ms，但清理 timer 喺 560ms 就加 `.done`＋inline opacity:0；
   嗰陣動畫（ease）仲喺 68%→100% 淡出段嘅前段、約 0.7–0.9 不透明 → 塊板「啪」一聲唔見（節點 820ms 先移除）。

## 修復（只限呈現／時序，冇掂遊戲邏輯、冇改 SAVE/softRev/?v=；diff 共 18 行）
1. `.push-door` z-index 45 → **15**：低過 sheet（z-20）、仍高過地圖裝飾（≤12）；門板只喺地圖帶滑行，唔再蓋 sheet／場景相。
2. `.push-door-bell` `right:8%` → **`left:6%`**：門鈴黐住門板左側，全程留喺畫面（實測新版各取樣點 right edge ≤355 < 390），成個滑行都睇得出係「有門鈴嘅門板」。
3. `playPushDoor` timer 對齊動畫：560ms timer **只藏門鈴**（保留 v19z1 SFX 時機）；新增 `_tDone` 喺 **700ms** 先落 `.done` 收尾（嗰陣動畫 100% keyframe 已係 opacity:0）；820ms 移除節點不變；新 timer handle 有 clearTimeout。

## 驗證
- 靜態測試 `tests/test_flash51_static.py`：17 斷言全 PASS；行落 v20a49 舊檔有 8 項 FAIL（反證成立）。
- repo 全套 **36/36 檔案 PASS**（原 35＋新 1）；`node --check` 兩段 script OK。
- Playwright harness（`harness/repro51.py` 舊版複現／`harness/verify51.py` 新舊對照）：
  - 舊版中段截圖 `flash_agency_2.png` 同用戶 iPhone 截圖構圖一致（板喺右側、蓋相角、冇門鈴）。
  - 新版中段截圖 `verify_fixed_midslide.png`：門板只喺地圖帶滑、sheet＋場景相完整壓喺上面、金色門鈴喺板上可見。
  - 油漆次序探針：重疊點 `elementFromPoint` 新版回傳 #loc-sheet 內元素（舊版 z-45 則為門板層）。
  - 淡出連續性：新版 t≈714ms 探得門仍係 `.on` 而 computed opacity 已係 0.058（動畫自己淡出）；舊版係 opacity 1 → 560ms timer 後直接 0。
- 檔大小：4,210,205 → **4,210,893 bytes**（+688，全文字）。

## 合併注意
本副本由 linji-work49 複製；同期另有 v20a50（存檔槽）喺 linji-work50 進行，兩邊修改位置冇重疊（本期只掂 `.push-door` CSS 兩條規則＋`playPushDoor` 一個函數），主代理可按任意次序合併。
