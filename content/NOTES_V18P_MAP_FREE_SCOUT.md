# NOTES_V18P_MAP_FREE_SCOUT

**SAVE：** `starVolunteer_map_v18p`  
**時間：** 2026-11-03（Asia/Hong_Kong）  
**預覽：** `joinkidshk-glitch/linji-chutoutian-web-preview`  
**HOLD：** Soft≠PASS；全量出圖未開；唔 publish

## 用戶拍板 UX

「到處逛逛」**唔再分港島／九龍／新界**——唔使按區鎖地圖；玩家可自由選大地圖任何地方。

## 做咗咩

| # | 項 | 做法 |
|---|---|---|
| 1 | Plan UI | browse 只留 `scout_all`「到處逛逛」；移除 `scout_nt`／`scout_kln`／`scout_island` 選項 |
| 2 | Migration | `scrubStaleJobs`＋`cont()`：舊區閘 id → `scout_all`；`defaultWeekPlan` 全用 `scout_all` |
| 3 | Map gate | `scoutRegionLock()` 永遠 `null`；刪 `lockLine`／`outLocked`／「今日只限」「今日鎖定」「只可點X」toast；區 tab 只做檢視／捲動過濾 |
| 4 | Contrast P0 | 區 tab 未選 cream；`#map-hint` 底欄 cream／浅金；狀態 `.stat .l/.v` cream on dark cell；教學 Skip 恢復實心 `.g` 掣（唔再 underline link） |
| 5 | Legend | 「非本區」隱藏（lock retired） |
| 6 | SAVE | `…_v18o` → `starVolunteer_map_v18p` |

## 唔改

- gigs_1989–92（仍等用戶拍板 → 之後 ?v=18q）
- StoryPlay／季節邏輯／shoot PLAN（僅 scout 遷移）

## Tester 覆測

1. `?v=18p`；SAVE=`starVolunteer_map_v18p`
2. 手帳 browse：只有一個「到處逛逛」
3. 逛逛日：地圖任區針可點；無「今日只限X」；區 tab 可篩／捲但唔鎖
4. 區 tab 未選字清晰；底欄「今日計劃」高對比；狀態九格標籤／數字可讀；教學 Skip 係掣
5. Soft≠PASS

## Ship

- feature commit： ()
- tip／NOTES： ()
- URL：https://joinkidshk-glitch.github.io/linji-chutoutian-web-preview/?v=18p
- Soft≠PASS · 全量出圖 HOLD
