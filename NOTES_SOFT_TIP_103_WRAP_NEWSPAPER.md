# NOTES · Soft tip #103 — 殺青短卡同日、本通告報紙次日朝早

> **狀態：** Soft≠PASS｜**唔 tip LIVE**｜SAVE `starVolunteer_map_v19w`｜產品 `?v=20a10` 唔抬  
> **softRev：** `s103`  
> **預覽：** `https://joinkidshk-glitch.github.io/linji-chutoutian-web-preview/?v=20a10&softBehaviorGate=1&softRev=s103`  
> `<html data-soft-rev="s103">` 先算載到今次 index。89–92 HOLD。出圖 HOLD。  
> 基線：Soft tip #102 main `3866fec`／softRev=`s102`。C1 劇情→次日報 **PASS**。Wrap→次日報 **FAIL**（自然試玩《天星碼頭》過海人潮）。

## 玩家面

- 殺青當日：仍只出「傳媒・街外・成績」短卡（「收下這份反響」）。
- 同一曆日：**唔**彈整張「收下這份剪報」。
- 下一曆日朝早（提早休息／返地圖／下一日行程耗日之前）：先彈**本通告**的 wrap 報。收下後先加該則 `fameDelta`，剪報簿留該則。
- 頭條／內文寫本作品同角色（例：《天星碼頭》／過海路人）。唔再抽一則寫住另一套劇的桶內頭條（「星河處境劇殺青 臨記融入度高」／茶客）。
- 報紙名、欄目、聲望 +1～+3 仍來自 `wrap_success` 桶。玩家面仍係「聲望」。

## 原因

`queuePostShootRewardOnWrap` 在 `resolvePlannedDay` 的 `tickDay()` **之前**入佇列，`publishDay` 用拍攝日 +1。日結一進位，玩家見到短卡的那個曆日已經等於 `publishDay`，返地圖就 `presentDueMorningPaper`。紙被當日食掉，次日朝早就冇。桶內電視模板又係固定劇情句子，唔係手上這單。

## 本票做咗咩

- `enqueueNewspaperFromWrap`：`pack.dayIndex` 當拍攝日。短卡日 = 拍攝日 +1，`publishDay` = 短卡日 +1。`eventKey` 仍係 `wrap:gigId:拍攝日`。
- 文案用本 gig 的 `workTitle`／`roleLabel`（通告欄或拍攝簿）。桶模板只借報紙名、`clipLabel`、`fameDelta`、`templateId`。
- 劇情入佇列唔改：`publishDay` 仍係選擇日 +1。#101 聲望正名唔改。
- `__newspaper.check()` 加天星碼頭回歸：短卡日唔彈、次日朝早（1988/3/11）先出本 gig、聲望只加一次、剪報有該則。C1 劇情紙斷言仍在。

## 本票唔做

- 唔 tip LIVE；唔抬 SAVE；唔抬產品 `?v=20a10`。
- 唔出圖；89–92 HOLD。
- 唔改通告板氣味演算法。唔加 C2+ 劇情。
- 自然試玩唔用 softSeed。

## Console

- `__newspaper.check()`（框架載入後）
- `__newspaper.fromWrap(sh, pack)`

## QA

新分頁開上面條 URL。接一日通告並殺青：當日只有短卡。提早休息過日之後先見整張報，頭條要係**該單**作品／角色。C1 選擇仍係當日唔彈、次日朝早先見電視週刊。HUD 仍係「聲望」。
