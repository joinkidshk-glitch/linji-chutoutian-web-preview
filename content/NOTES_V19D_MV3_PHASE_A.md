# NOTES｜v19d 通告 Detail MV3 Phase A 欄序

**日期：** 2026-11-03（Asia/Hong_Kong）  
**SAVE：** `starVolunteer_map_v19d`  
**預覽：** https://joinkidshk-glitch.github.io/linji-chutoutian-web-preview/?v=19d  
**狀態：** Soft≠PASS · 出圖 HOLD · 唔 publish  
**對齊：** `PLAN_GIG_MV3_ALIGN_v1` **Phase A**（§1 欄序；§5 `limits` 顯示派生）  
**保留：** `PLAN_GIG_PAY_EXACT_v1`、`PLAN_GIG_BREACH_FEE_v1`、條件 v1.1 `名：>N`、v19c synopsis clip、sticky 底掣  
**19c URL 唔破：** `?v=19c` 仍為上一 tip；本 tip 新 tip `19d`

---

## Phase A 做咗

Detail 欄位精神／順序：

1. **作品名**（橙頭）  
2. **類型** 粗 `type` pill；**`genreLabel` 有且唔同粗類先加細類 pill**（無則唔造）  
3. **難易度 ★**（stars row，近類型）  
4. **角色／職位**：`roleLabel` → 否則 `roleHint` → 否則 `roleScale` 短 stub → 全空隱藏列  
5. **條件** `名：>N`（綠／紅）  
6. **每週／總天**  
7. **片酬** exact  
8. **違約金**  
9. **特殊限制**：有內容先顯示；**無則整列唔出**（無舊「特殊 —」stub）  
10. **導演**（＋可選 `producer` 行）  
11. **通告期間**  
12. **劇情簡介**（框內滾；唔再喺簡介下重覆 roleNote）

**無簽約。** 屬性仍用現行 stamina/acting/iq/charm/looks/stage；**唔讀** `vocal`／`speech`。  
本 tip **唔批量改 JSON**（Phase B 劇本補 `genreLabel`／`roleLabel`／`limits`）。

### `limits` 顯示派生（PLAN §5）

- `gender` `male`／`female` → 限男性／限女性；`any`／缺＝唔出句  
- `licenses[]` → `須持有：…`（頓號）  
- `groupOnly` → 須以組合／團體報名  
- `minAge`／`maxAge` → 年齡句  
- `notes[]` 原樣  
- 全空後 fallback：`specialReq` string／array  
- 仍無內容 → **唔顯示「特殊限制」塊**

---

## 鏡射／部署

`sv-phone-preview` → `/tmp/linji-chutoutian-web-preview` push `main`（no force）。

Soft≠PASS · 出圖 HOLD
