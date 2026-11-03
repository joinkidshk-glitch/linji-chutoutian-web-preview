# NOTES｜v18u DeepSeek 玩家面中文過濾

**日期：** 2026-11-03（Asia/Hong_Kong）  
**SAVE：** `starVolunteer_map_v18u`  
**預覽：** https://joinkidshk-glitch.github.io/linji-chutoutian-web-preview/?v=18u  
**狀態：** Soft≠PASS · 出圖 HOLD · 唔 publish

## 本輪

跟 `HANDOFF_DS_PLAYER_ZH_FILTER_v1` §5＋`DS_PLAYER_ZH_FILTER_TABLE_v1.json`（66 條）抬預覽：

1. **index.html 硬編碼**玩家字串：圖例「有板」→「有通告」；hint「通告欄免費」；lead「免費查看通告」；空板／只查看通告欄／事態 empty／手帳 empty／modal／toast「拍攝檔期已定」；跑通告；傾談；刪硬鎖／唔能試／睇板／通告板／薄本／拍攝鎖定（玩家面）。
2. **嵌入同步** `NPC_LINES_CORE`／`STORY_BEATS_PHASE1`／`TUTORIAL_ZH_HK` ← LIVE content JSON（fetch 仍以 `?v=SAVE` 覆蓋）。
3. **對齊** `PLAN_GIG_CARD_PLAYER_COPY_v1`（已於 v18t：gate／reqHtml／無展開 synopsis）。
4. **gigs** 不變（2.3.1 天星）。

## SHA16（content／）

| 檔 | SHA16 |
|---|---|
| tutorial_zh_HK.json | `8e1efc59751267d5` |
| npc_lines_core.json | `74044efce1996f4f` |
| worldview.json | `b01d186e38c0a504` |
| story_beats_phase1.json | `96fad0d682edd9ca` |
| protagonist.json | `dd3f98cf6b6f60fd` |

## 殘餘禁詞 grep

`有板|睇板|通告板|跑板|薄本|硬鎖|唔能試|拍攝鎖定` → **玩家面 0**（註解／NOTES 忽略）。

## 鏡射

`sv-phone-preview` → `star-volunteer-web` → `/tmp/linji-chutoutian-web-preview` push `main`（no force）。

Soft≠PASS · 出圖 HOLD
