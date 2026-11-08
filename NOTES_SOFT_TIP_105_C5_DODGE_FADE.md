# NOTES · Soft tip #105 — C5 迴避次日淡紙

> **狀態：** Soft≠PASS｜**唔 tip LIVE**｜SAVE `starVolunteer_map_v19w`｜產品 `?v=20a10` 唔抬  
> **softRev：** `s105`  
> **預覽：** `https://joinkidshk-glitch.github.io/linji-chutoutian-web-preview/?v=20a10&softBehaviorGate=1&softRev=s105`  
> `<html data-soft-rev="s105">` 先算載到今次 index。89–92 HOLD。出圖 HOLD。  
> 基線：Soft tip #104 main `41010210`／softRev=`s104`。

## 玩家面

- 主線 C5《采兒小訪題》揀「藉故迴避不答」之後，當日仍然唔彈整張報。
- 下一曆日朝早出淡紙：頭條「避談敏感話題 阿偉借故離開採訪」，版面寫「這則未再改聲望。」
- 收下之後聲望唔加。剪報留低呢一則。
- 用「全日休息」或「加速本週剩餘」過日，返到地圖或下一朝，逾期淡紙仍會彈，唔會永遠留喺佇列。
- 秋日頒獎請柬可以先出。揀「稍後」之後，未收嘅朝早報紙會跟住出。

## 根因

- 真實 C5 節點 `C5_c` 的 `effects.flags` 已經係 `choi_dodge`。`StoryOC.applyChoice` 會入佇列 `story:C5:dodge`、`fameDelta` 0、`publishDay = dayIndex+1`。種子 `np_story_c5_dodge_01` 用得著，冇改文案。
- `BehaviorGate.rivalGao_onlyC3ChoiceFlags` 唔會削走 `choi_dodge`。
- 自然試玩唔見紙，係朝早呈現被截住：
  - `presentDueMorningPaper` 在 `_weekAccel` 時直接返回，加速會靜默吞掉到期嗰朝。
  - 提早休息踏入下一曆日之後先出休息結算，淡紙未彈。
  - 返地圖時秋日頒獎請柬排喺報紙前面。揀「稍後」會同 `goToMapForBrowse` 對撞，請柬當日不再彈，淡紙亦唔出，剪報一直係舊嘅。

## 本票做咗咩

- 加速途中、非地圖日，先彈逾期朝早報，玩家收下之後先繼續吞日。
- 提早休息同地點休息踏日之後，淡紙先於休息結算。
- 頒獎請柬只有真係彈出先截住返地圖。今日已「稍後」就交返朝早報紙，唔再遞迴。
- 種子未就緒時暫存嘅劇情報，喺朝早彈報前再沖一次。
- `__newspaper.check()` 用真實載入嘅 C5／`C5_c` 走 `applyChoice` → 推日 → `present`（包括加速旗）→ 收下 → 剪報。合成 dodge 斷言仍然保留。

## 本票唔做

- 唔 tip LIVE；唔抬 SAVE；唔抬產品 `?v=20a10`。
- 唔出圖；89–92 HOLD。
- 唔加新劇本種子。唔改 C1–C4／周刊／殺青淡紙規則。

## Console

- `__newspaper.check()`（框架同主線載入後）應 `{ ok:true, softRev:"s105", version:"v20a10", softStatus:"≠PASS" }`

## QA

新分頁開上面條 URL。入秋打完《采兒小訪題》，揀「藉故迴避不答」。當日冇整張報。下一朝有淡紙，聲望唔加，剪報有頭條。若果用加速或休息過日，返地圖之後逾期淡紙仍會出。
