# V18A_PLAYER_UX_P0P1

**SAVE：** `starVolunteer_map_v18a`  
**時間：** 2026-11-03（Asia/Hong_Kong）  
**預覽：** `joinkidshk-glitch/linji-chutoutian-web-preview`  
**HOLD：** Soft≠PASS；唔 publish；出圖暫緩  
**契約：** JSON **1.2.4** + `HINT_PACING_P0_v1.md` + tester 玩家角度 P0/P1

## P0

| # | 項 | 修法 |
|---|---|---|
| 1 | 即將可出真實閘 | 鎖行用 JSON `lockedHint`；另加 `storyWeekStamp`／`sp-lock-week`（when 或 weekMin + 隔日） |
| 2 | C1 完唔再推開局先練 | map／home／nudge／tips／afterDay 過濾已完成 C1；B01 文案改「只播一次」；本週章節唔再夾「去星河播 C1」 |
| 3 | C1 章戳 | 跟 JSON 1.2.4 `when: 1988春 / W1-2`（LIVE 由 1.2.3／W3-4 升級）；事態可播行顯示 week stamp |

## P1

| # | 項 | 修法 |
|---|---|---|
| 1 | 手帳 HUD 三行擠 | `home-date` 只留日期·地區；狀態改 `home-stats` pill 行 |
| 2 | 休息卡蓋舊日 HUD | rest／home_chore：`day-res` mask 留頂欄；完成日→而家；loc sheet 開時 map-hint 改頂部精簡日期唔再 display:none |
| 3 | 未達門檻 vs 32% | **軟搏保留**（初階 canAudition 故意放行）；文案改「可搏／搏一搏」；真硬鎖先寫「未達門檻·硬鎖唔能試」。唔再一律寫🔒未達門檻卻仲有試鏡掣 |
| 4 | 接線／年份 | 玩家 build 預設 `hidden`；只 `?debug=1` 或 `localStorage.starVolunteer_debug=1` |

## Soft-try 決策（NOTES）

- `canAudition` 初階允許缺 ≤1 項／總差 ≤10 → 成功率可低至約三成＝**可搏**，唔係 UI 自相矛盾。
- 硬鎖（`!gate.ok`）按鈕 disabled，copy「硬鎖唔能試」。

## Tester 覆測（清 SAVE）

1. 清 `localStorage` `starVolunteer_map_*` 後開 `?v=18a`
2. C1 播完 → 事態／地圖／B01／本週章節唔再叫去星河重播「先練／先賺」
3. 即將可出：見 week／隔日口吻 + 鎖行 week pill；C1 header／when＝W1-2
4. 手帳頂：兩行可讀（日期｜狀態 pills）
5. 休息（地圖休息室或手帳全日休息）：見「完成日→而家」；頂欄日期唔完全被蓋死
6. 通告板：軟搏卡寫「可搏」；硬鎖卡先寫未達門檻
7. 選單無「接線／年份」；加 `?debug=1` 先見

## Ship

- URL：https://joinkidshk-glitch.github.io/linji-chutoutian-web-preview/?v=18a
- tar：`/workspace/star-volunteer-web-v18a.tar.gz`
- Soft≠PASS · 出圖 HOLD
