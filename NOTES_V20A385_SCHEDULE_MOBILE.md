# v385 行程頁手機版面修正

用戶 2026-11-22 18:27 iPhone 截圖：手帳「本週安排」七格格仔紙表右欄被截斷。

## 根因（實駕量度，Playwright 390×844 dsf 2）
- `#nb-days` clientWidth 304px、scrollWidth 686px；grid 固定 220.7px×3；
  週二 right=515、週三 right=748，超出 390 畫面。
- `repeat(3,1fr)` 嘅 `1fr` 下限係 `auto`（min-content），長片名撐爆每格。

## 修法（GPT-6.2-sol 方案，原稿 linji-drive385/gpt_plan.txt）
- 全寬：`repeat(3,minmax(0,1fr))`＋`.day-row`/`.nm`/`.wd` `min-width:0`＋
  文字 `overflow-wrap:anywhere`，桌面防撐爆、欄數不變。
- ≤767px：兩欄 `repeat(2,minmax(0,1fr))`、gap 8px、第七格獨佔末行；
  日期 15px/1.35、活動 14px/1.45；觸控 ≥44px（格高 118px 不變）。
- Notebook 本已 flex column 堆疊，唔郁結構；玩法邏輯不變。

## 驗證（linji-drive385/）
- 修前 before_measure.json／before_390_schedule.png；修後 after_measure.json：
  390px 每格 148px、allInside=true、scrollWidth=clientWidth；桌面 118px×3 正常。
- 零 page error。

## 不變
SAVE key／softRev／產品 `?v=`／贏線 0.875／floor 140／warnLine 180／E1 門檻 350。
