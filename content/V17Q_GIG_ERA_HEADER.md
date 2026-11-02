# V17Q_GIG_ERA_HEADER

**SAVE：** `starVolunteer_map_v17q`  
**時間：** 2026-11-03（Asia/Hong_Kong）  
**預覽：** `joinkidshk-glitch/linji-chutoutian-web-preview`（lean Pages）  
**HOLD：** Soft≠PASS；唔 formal publish；出圖暫緩

## 對標（tester v17p FAIL · P0-3 only）

PASS 已確認：auto C1、lockedHint、「跳過教學」、開局事態=1。

### P0-3 通告板（星河「只睇通告板」）

| 漏點 | 根因 | 修法 |
|---|---|---|
| 發現區＋片場人情卡下仍見 `era_1988_spring_grassroot`（兩張／兩行） | `normalizeGigRecord` 把 **string** `eraTag` **原樣**寫入 `eraTagLabel`；`eraTagDisplay` **優先 return eraTagLabel**，令 v17p 嘅 boardNote／humanize **永遠行唔到** | `normalizeGigRecord` 用人話／`boardNote` 寫 label；`eraTagDisplay` **先 boardNote**，拒 `era_*`；`gigCardHtml` `stripEraIdsInText` |
| header／subtitle「失敗唔開／工。」 | 板頭文案 `…失敗唔開工。` 窄屏 keep-all 仍喺「開｜工。」斷開 | 改短句＋換行：`約試鏡日＝先預約（失敗則不開拍）`；`.board-lead` keep-all；發現句尾「龍套開工」顯示改「龍套開拍」 |

## 改動

- `/workspace/star-volunteer-web/index.html`
  - `looksLikeEraId` / `humanizeEraId` / `normalizeGigRecord` / `eraTagDisplay` / `stripEraIdsInText`
  - `gigCardHtml` discover／era 消毒
  - `doScout` board-lead 文案＋CSS
  - SAVE → `starVolunteer_map_v17q`

## 產物

- NOTES：本檔 + `/workspace/star-volunteer-qa-playthrough/V17Q_GIG_ERA_HEADER.md`
- tar：`/workspace/star-volunteer-web-v17q.tar.gz`
