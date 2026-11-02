# V17O_STORY_ENTRY_STORYPLAY

**SAVE：** `starVolunteer_map_v17o`  
**時間：** 2026-11-03（Asia/Hong_Kong）  
**預覽：** `joinkidshk-glitch/linji-chutoutian-web-preview`（lean Pages）  
**HOLD：** Soft≠PASS；唔 publish 正式；出圖暫緩

## PLAN_MAP 0a–0e + (A)(B)

| # | 項 | 實作 |
|---|---|---|
| 0a | 開局自動推 C1 | `autoPushC1IfNeeded` + JSON `playerOffer:true`；`paintStoryEntryHints` 呼叫 |
| 0b | StoryPlay 手感／`ev.ok` | `StoryPlay.start` 用 `ev.ok`（擋 phaseSoft）；stub／offer 閘 |
| 0c | 入口可發現 | 頂欄／選單「事態」；chip；home／B01／教學文案 |
| 0d | C1 進度 | `markDone` → `syncPhaseFromProgress` + map tips |
| 0e | 一屏無滾／觸控≥44 | `#mask.story-play-on`；`.sp-scroll` overflow hidden；btn min 44 |
| (A) | 地圖 tip + loc「播事態」 | `refreshStoryMapTips`（`kind:"story"`）；`openLoc` act；pin `.has-story-tip` |
| (B) | 結算 next／locked hint | `showResult` 讀 JSON `nextHint`／下一主線 `lockedHint` |

## Script-lock + HINT JSON 1.2

- **優先** `story_detail_c1_to_c17.json` **1.2** 欄：`locId`／`playerHint`／`lockedHint`／`nextHint`／`playerOffer`；`storyHintPack`／`storyNodeLocId` soft 僅缺欄後備（`HINT_C1C5_MAP_v1.md`／`STORY_*_SOFT`）
- loc：C1–C3／C5＝`tvb_longmen`；C4＝`ad_central`
- C5 `thresholds.rel_choi_threshold`＝**2**（`resolveThreshold` 讀 JSON，缺則 script_lock 2）
- `playerOffer` 缺省／omit＝false；C1–C5 JSON `true`

## PLAYER_OFFER_MEET_v1（push 前必須）

- 15 平行 meet（romance／rival）`playerOffer:false` — **永不**入玩家 `listOpen({player:true})` 計數／事態列表
- `hasPlayerOffer`：`false` 先拒；`true` 可入；omit 要 `offers` 袋
- `openMeetOffer`／入地／傾偈：**拒** `playerOffer===false`
- 接線 `showWireDebug` 用 `debug:true, player:false, all:true` 睇全量

## 文案

- 書面語現代港語；入口統一「事態」（唔再用「可出劇情」）
- C5 `nextHint` 文案 nits：已知、script 後改；引擎照讀欄

## 自檢（本機）

- [x] SAVE＝v17o
- [x] JSON 1.2 C1–C5 四 hint＋loc＋offer true；C5 thresh 2
- [x] 15 meet offer false；listOpen player 硬濾
- [x] Soft≠PASS；出圖未做

## 產物

- `/workspace/star-volunteer-web/index.html`
- `/workspace/star-volunteer-web/content/story_detail_c1_to_c17.json`（1.2）
- `/workspace/star-volunteer-web/content/HINT_C1C5_MAP_v1.md`
- `/workspace/star-volunteer-web/content/PLAYER_OFFER_MEET_v1.md`
- tar：`/workspace/star-volunteer-web-v17o.tar.gz`
