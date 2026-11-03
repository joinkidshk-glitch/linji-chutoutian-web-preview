# NOTES｜v19i Detail 拆約試鏡／試鏡預約

**日期：** 2026-11-03（Asia/Hong_Kong）  
**SAVE：** `starVolunteer_map_v19i`  
**預覽：** https://joinkidshk-glitch.github.io/linji-chutoutian-web-preview/?v=19i  
**Soft≠PASS · 唔 publish · 出圖 HOLD**

## 用戶閘
試鏡預約多餘。Casting Detail sticky 底掣只留「即場試鏡（+1日）」＋「離開」。

## 改動
1. `openCastingNoticeDetail`：刪「約試鏡日」；即場／搏一搏直呼 `doAudition`（唔再經 `promptAudition` 紙本卡）；離開仍返通告欄。
2. `promptAudition`：廢「試鏡預約」modal／約試鏡 push；gate OK 時直走 `doAudition`（地點選單「試鏡：…」入口一併收斂）。
3. `doAudition` gate 失敗：toast 後重開 Detail（唔開紙本卡）。
4. 通告欄 lead／手帳「工作」空態：唔再引導「約試鏡日」；舊 `S.booked`／`job:` 路徑仍可消化既有預約。
5. 保留 19g sticky 標題／簡介滾、19f 標籤、19e 兩欄、19h gigs_1988 2.3.2 stub 不變。

## 唔做
- 全庫重生／切圖 LIVE／Soft PASS
- 改 stub 欄位值
