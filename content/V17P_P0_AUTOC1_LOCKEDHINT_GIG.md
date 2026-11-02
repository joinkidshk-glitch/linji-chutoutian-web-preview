# V17P_P0_AUTOC1_LOCKEDHINT_GIG

**SAVE：** `starVolunteer_map_v17p`  
**時間：** 2026-11-03（Asia/Hong_Kong）  
**預覽：** `joinkidshk-glitch/linji-chutoutian-web-preview`（lean Pages）  
**HOLD：** Soft≠PASS；唔 formal publish；出圖暫緩

## 對標（tester v17o FAIL）

| # | P0 | 根因 | 修法 |
|---|---|---|---|
| 1 | 教學後唔自動開 C1 | `autoPushC1IfNeeded` 只 ensure offer／map tip；`startNew` `afterDone=showB01HomeModal` →「先看事態／開始寫手帳」；`maybeNudgeStoryEntry` 再要手動「打開事態」 | `postTutorialEntry`：教學結束 → `autoPushC1IfNeeded({play:true})` → `StoryPlay.start('C1')`；結算後再 `showB01HomeModal`（`pendingB01AfterStory`） |
| 2 | 「即將可出」露 `AND need_done:C1`… | `playOpenPicker` 用 `reasons[0].replace(/^need_done:/…)`；實際 reason 係 `AND need_done:C1`，`^` 唔命中 | 改讀 row.`lockedHint`／`StoryOC.playerReasonFrom`（HINT JSON／soft 表） |
| 3 | 通告板露 `era_1988_spring_grassroot`；header「工。」；「跳過教學」裁 | `eraTagDisplay` 直接 return raw `eraTag`；tut-skip `min-width:0`＋modal overflow | `eraTagDisplay` 優先 `boardNote`／人話 map；`.t` nowrap ellipsis＋title keep-all；tut-skip `max-content`／nowrap／modal overflow visible |

## 改動檔

- `/workspace/star-volunteer-web/index.html`
  - `SAVE` → `starVolunteer_map_v17p`
  - `autoPushC1IfNeeded(opts)` / `postTutorialEntry` / `startNew` / `finishTutorial`
  - `StoryPlay.playOpenPicker` locked rows
  - `eraTagDisplay` + gig CSS
  - tut-skip CSS；`showResult` → `drawMap` + `flushPendingB01`

## Nit

- C3→C4 stale story-pin：結算後即 `drawMap()`（cheap）。若仍偶發 HOLD。

## 自檢

- [x] SAVE＝v17p
- [x] 教學後路徑唔再以 B01「先看事態」作 C1 唯一入口
- [x] locked 列唔靠 raw `AND need_done`
- [x] era_* 唔直接上板
- [ ] Soft≠PASS；出圖未做

## 產物

- NOTES：本檔 + `/workspace/star-volunteer-qa-playthrough/V17P_P0_AUTOC1_LOCKEDHINT_GIG.md`
- tar：`/workspace/star-volunteer-web-v17p.tar.gz`

## Ship

- commit：`c62bc4e`（`c62bc4eb233992b6ed58c3d8682e57a2d9dae2ab`）· 2026-11-03 01:05 HKT
- URL：https://joinkidshk-glitch.github.io/linji-chutoutian-web-preview/（`?v=17p`，清 `starVolunteer_map_*`）
- curl-verify：SAVE v17p + `postTutorialEntry` + `flushPendingB01` + era `boardNote`；LIVE HTML size 1152183；NOTES path OK
- tar：`/workspace/star-volunteer-web-v17p.tar.gz`
- Soft≠PASS；出圖暫緩
