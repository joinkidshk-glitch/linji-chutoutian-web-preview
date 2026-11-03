# NOTES v18t — 通告卡真・接通告 player UX

**日期：** 2026-11-03（Asia/Hong_Kong）  
**SAVE：** `starVolunteer_map_v18t`  
**Soft≠PASS · 出圖 HOLD**  
**URL：** https://joinkidshk-glitch.github.io/linji-chutoutian-web-preview/?v=18t

## Content

| 檔 | version | note |
|---|---|---|
| `content/gigs_1988.json` | **2.3.1**（不變） | 天星 brand 維持 |

## index.html（玩家面文案／版式）

1. **reqHtml**：改試鏡條件表格式。達標＝`聲望 達標`／能力 `達標`；未達＝`… 未達（要≥N）`。**無**`（你N）`、`差N`。
2. **gateShortReason**（卡鎖 `🔒 …`）：`試鏡門檻未達：聲望、台風、…`——列齊未達類別（聲望＋能力），**無**差距數字。
3. **gateTrainHint**／canAudition 聲望 reason：同步去工程口吻（toast 亦讀似通告條件）。
4. **meta**：`片酬約 $ …`＋`檔期：約 N 日 · 逢週…拍攝 · 限期 N 日`；CSS 全 theme 取消 `nowrap`／ellipsis，可換行完整可見。
5. **synopsis**：全文顯示；**刪** `.syn-toggle`「展開」掣（`wireGigCardSynToggles` 留無害）。
6. **rate**：`可試鏡 · 預估取錄約 N%`（可搏註：條件未齊仍可搏）。

## Tester checklist

- [ ] `?v=18t` 硬 reload；SAVE `starVolunteer_map_v18t`
- [ ] 天星合唱錄音卡：無「你12」「差4」；見「試鏡條件／試鏡門檻未達」
- [ ] 片酬＋檔期行完整可見（可換行，無…裁切）
- [ ] 無「展開」掣；synopsis 全文
- [ ] gigs JSON 仍 2.3.1；邏輯門檻未改

Soft≠PASS。
