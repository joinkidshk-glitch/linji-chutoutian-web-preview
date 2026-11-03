# HANDOFF｜通告 Detail 招募單字段 v1

**計劃全文：** `PLAN_GIG_CASTING_NOTICE_DETAIL_v1.md`  
**條件：** `PLAN_GIG_CASTING_REQ_NUM_COPY_v1` v1.1 → `{名}：>{need}`  
**片酬：** `PLAN_GIG_PAY_EXACT_v1` → exact  
**違約金：** `PLAN_GIG_BREACH_FEE_v1` → 顯示＋逾期罰則；**無「簽約」欄**  
**參考：** `/workspace/ref-mv-casting-notice.png`  
**Soft≠PASS**／出圖 HOLD

## 欄位（更新）
作品名、類型、招募中、導演、通告期間、角色、條件、難易度、每週／總天、片酬、**違約金**、劇情簡介。  
**已刪：簽約。**

## 落地
- 條件 `演技：>60`；片酬 exact；違約金 exact（iOS 可暫 —）；逾期扣款＋fame／stress。  
- C：後補 workTitle／director／可選 payExact／breachFee。  

**MV3 對齊：** `PLAN_GIG_MV3_ALIGN_v1`（屬性映射＋genreLabel 詞庫＋roleLabel＋limits）

## 交
iOS · tester
