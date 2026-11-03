# V18L_SHOOT_SCHEDULE_STUB

**SAVE：** `starVolunteer_map_v18l`  
**時間：** 2026-11-03（Asia/Hong_Kong）  
**預覽：** `joinkidshk-glitch/linji-chutoutian-web-preview`  
**規格：** `PLAN_SHOOT_CAREER_SCHEDULE_v2.md`（**廢止** v1 tier 日數下限）  
**HOLD：** Soft≠PASS；全量出圖未開；**`gigs_*.json` 未改**（劇本擁有補欄）

## 做咗咩（引擎 stub）

| # | 項 | 做法 |
|---|---|---|
| 1 | **roleScale／shootBand** | `ROLE_SCALE_BAND` 跟 v2 §1；`resolveRoleScale`（有欄用欄；否則附錄 §5 type+tier 粗映射）；`effectiveShootDays`＝hint（或缺→帶中位）**clamp 入 band**；**無**初≥3／中≥5／高≥7 |
| 2 | **shootWeekdays** | PLAN `1=一…7=日` → 引擎 `weekdayIdx` `0=一…6=日`；缺欄 fallback `[1,2,3,4,5]`；`placeShoot`／`preview`／`lockShootsIntoDraft` 只落允許星期 |
| 3 | **shootDeadlineDays** | 缺欄 `max(14, days×3)`；`scheduleShoot` 存 `hiredAtDay`／`deadlineDays`／`deadlineDay` |
| 4 | **逾期一次** | `tickDay`→`advanceDay` 後 `processOverdueShoots`：remain>0 且 `dayIndex>deadlineDay` → 掉單（唔發 pay／fame／pop）＋fame−8/−12＋stress＋12／＋16＋pop−5/−8＋`bumpNpc(agent,-1)`；文案「限期內未完成拍攝…」；`done_`＋`fail_shoot_` 防再約 |
| 5 | **UI** | 通告卡「逢週X拍攝」＋限期；手帳／拍攝簿 HUD：限期／可拍／尚欠 |
| 6 | SAVE | `…_v18k` → `starVolunteer_map_v18l` |

## 唔做

- 唔改 `gigs_1988.json`～`gigs_1992.json`（現庫 hint 仍短；引擎會 **抬入 band**，例如廣告 hint=2→`ad_av` 帶 min 3）
- 唔 publish／唔開全量出圖
- Soft≠PASS

## Tester 覆測（清 SAVE）

1. `?v=18l` 硬 refresh；SAVE=`starVolunteer_map_v18l`
2. 獲聘後手帳 shoot **只**落缺欄平日（一至五）；卡面見「逢週一、二、三、四、五拍攝」
3. 日數跟 band clamp（電影初／無 roleScale → `film_support_small` 12–15，唔再 2 日）
4. 人工把 `deadlineDay` 改細或拖過限期 → 一次掉單罰則、唔發片酬、唔再上板（「取消檔期」）
5. Soft≠PASS

## curl-verify（填 ship 後）

- SAVE=`starVolunteer_map_v18l`
- HTML：`ROLE_SCALE_BAND` · `effectiveShootDays` · `shootWeekdayOk` · `processOverdueShoots` · `限期內未完成拍攝` · **無**「初≥3／中≥5／高≥7」

## Ship

- feature：`22e3251e2d7d` (`22e3251e2d7d4c244499f2ff72d3dac7522cfa72`)
- NOTES tip：`(pending)`
- URL：https://joinkidshk-glitch.github.io/linji-chutoutian-web-preview/?v=18l
- Soft≠PASS · 全量出圖 HOLD · gigs JSON untouched
