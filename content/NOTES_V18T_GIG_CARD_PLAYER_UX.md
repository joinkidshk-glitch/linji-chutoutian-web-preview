# NOTES v18t — 通告卡玩家面（跟 PLAN_GIG_CARD_PLAYER_COPY_v1）

**日期：** 2026-11-03（Asia/Hong_Kong）  
**SAVE：** `starVolunteer_map_v18t`  
**規格：** `content/PLAN_GIG_CARD_PLAYER_COPY_v1.md`  
**Soft≠PASS · 出圖 HOLD**  
**URL：** https://joinkidshk-glitch.github.io/linji-chutoutian-web-preview/?v=18t

## Content

| 檔 | version | note |
|---|---|---|
| `content/gigs_1988.json` | **2.3.1**（不變） | JSON 本輪唔改 |

## index.html（對照 PLAN §2–§5）

| 區 | 實作 |
|---|---|
| §2.1 `gateShortReason` | 聲望句／能力 1–2／≥3＋等／聲望+能力／兜底；板面短標 `暫未能報 · 條件未合` |
| §2.2 rate／soft | `可搏一搏 · 條件未齊`（可留單一 %）；無「成功率反映差距」括註 |
| §2.3 consumed | `本單已殺青。`／逾期組製取消／`通告已下架。` |
| §2.4 `gateTrainHint` | 兩句書面語（已報名／未報名） |
| §2.5 `reqHtml` | `演技：合／未合組製要求`；`聲望：合／未合這檔檔次`；無 ≥／你X |
| canAudition fame | §2.1 聲望句 |
| §3 meta | `酬勞約 $… · 拍攝／錄音約 N 日 · 逢週… · 獲聘後 N 日內完成`；CSS wrap 無截斷 |
| §3 weekday／HUD | `shootWeekdayLabel(…, gig)` 切拍攝／錄音；七日→每日可拍／可錄；手帳限期句 |
| §4 synopsis | 全文；無「展開」掣 |
| §5 board | lead／lock-sub 跟表 |

## Tester（PLAN §7）

- [ ] 鎖卡無「差 N」「你 X」「≥」；見「條件未合／暫未能報」
- [ ] 軟搏「可搏一搏」；無「成功率反映差距」
- [ ] 唱片：完整「錄音約 N 日」
- [ ] 無「展開」；synopsis 全文
- [ ] Soft≠PASS

Soft≠PASS。
