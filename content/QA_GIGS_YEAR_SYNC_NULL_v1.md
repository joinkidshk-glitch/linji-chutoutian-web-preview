# QA_GIGS_YEAR_SYNC_NULL_v1 — 年庫切換 boot crash

**日期**：2026-11-03（Asia/Hong_Kong）  
**Verdict**：**FAIL（blocker）** · Soft≠PASS · 出圖暫緩  
**範圍**：瀏覽器 HTTP `http://127.0.0.1:8765/` · gigs 1989–1992 年曆切換

## 現象
硬 reload 後開「接線資料」原文：
`Cannot read properties of null (reading 'dayIndex')`  
顯示：`通告：30 · 年庫：? · 來源：內嵌 fallback · 當季 春 · high 0`  
未切到 1989+；未見 `gig_1989_`／`gig_1990_`／…；星河通告板未驗。

## Root cause
- `let S=null`（約 L3115）
- boot 末尾 `refreshCopyPacksFromDisk()` → `syncGigsForCalendarYear(true)` → `dateObj()`
- `dateObj()`（約 L4148–4151）寫 `S.dayIndex` **無** null guard
- 對照：`calendarSeason()` 已用 `(S&&S.dayIndex)||0`

## 建議修法（交 iOS）
```js
function dateObj(){
  const dt = new Date(START.y, START.m-1, START.d + ((S&&S.dayIndex)||0));
  return dt;
}
```
建議一併：`fmtDate()` 內 `(S&&S.dayIndex)||0`。

## 覆測清單（修後）
1. 硬 reload → Console `[WIRING] year 1988 gigs … fromFile true`；接線資料年庫＝1988、無 dayIndex 錯
2. 日曆推到 1989／90／91／92 → 年庫跟隨；通告 id 前綴 `gig_19xx_`；high 春夏各≥4（92 秋冬收束另計）
3. 星河電視台通告板可開、優先排序 OK

## 狀態
1989–1992 **文件 QA 仍 PASS with nits**；**瀏覽器年切 FAIL／SKIP** 直至此修。  
電話預覽可推接線＋年庫檔，但 **未修前唔好當跨年已通**。
