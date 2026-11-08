# NOTES｜劇情×報紙 Soft 文案種子 v1（Soft tip #102）

> 日期：2026-11-08（Asia/Hong_Kong）  
> Soft≠PASS｜**唔 tip LIVE**｜唔抬 `?v=`／SAVE｜出圖 HOLD｜89–92 HOLD  
> PLAN：`PLAN_STORY_NEWSPAPER_LOOP_SOFT.md`（§0 拍板＋§4 觸發＋§5.1 id）  
> 基線：Soft tip #101 main `28903874`／softRev=s101；產品 `?v=20a10`；SAVE `starVolunteer_map_v19w`  
> 來源：qwen3.7-max（raw：`content/_qwen_raw_newspaper_story_soft/`；mirror playtest）

## 本包做咗咩
- 新建 `STUB_NEWSPAPER_STORY_SOFT_v1.json`（preview＝sv 雙份）
- `story_highlight` **8** 則（C1 tv／film、C2 network／hustle、C4 harsh、C5 honest、hiu exchange、choi weekly honest）
- `story_mixed` **6** 則（C3 hard／endure、C4 refuse、C5 spin／dodge、choi weekly official）
- 欄位：id／eventKey／storyBeatId／choiceFlag／tone／paperName／headline／dek／fameDelta／clipLabel／rumorEcho／boardScentTag
- 虛構紙名沿用：娛樂快報／電視週刊／星河娛樂版／樂壇速遞／消費情報
- 玩家面「聲望」；禁「聲量」「噂」；禁真藝名／真報長弧
- R_hiu distant＝**skip 入報**，無模板（見 stub.skip）
- 節奏：事態選擇確認當日 enqueue → **次日朝早**彈出（引擎另線）

## 拍板對齊
| 題 | 決定 | 本包 |
|---|---|---|
| 周刊誠實紙 | fameDelta +1～+2（即時+1之外） | `np_story_choi_weekly_honest_01`＝**+2** |
| C5 迴避 | 出淡紙 fameDelta=0 | `np_story_c5_dodge_01`＝**0** |
| C3 硬碰 | 可 −1 | `np_story_c3_hard_01`＝**−1** |

## 本包唔做
- 引擎 `enqueueNewspaperFromStory`／朝早 modal／favorGate／boardScent 演算法
- tip LIVE；抬 SAVE／產品 `?v=`；softRev bust；出圖；89–92
- #101 press 口語 nit heal（可選；本包 **skip**）
- R_hiu distant 模板

## 合入建議（等統籌抽樣 OK → iOS Soft tip）
1. Soft tip 讀本 stub；`StoryOC.applyChoice`／DualMeet 完成後 `enqueueNewspaperFromStory`
2. 次日朝早彈出後套用 `fameDelta`（玩家面「聲望」）
3. 可選餵 `rumorEcho`（source=報紙）；`boardScentTag` 只種子，演算法 P1 HOLD
4. softRev 建議 `s102`；**唔抬** `?v=20a10`／SAVE `v19w`

## sha8
| 檔 | sha8 |
|---|---|
| STUB_NEWSPAPER_STORY_SOFT_v1.json（preview＝sv） | `4dabcb42` |
| SCHEMA_NEWSPAPER_STORY_SOFT_v1.json（preview＝sv） | `c7d266d4` |
| NOTES（本檔） | 見交貨稿寫入後 |
| NEWSPAPER_STORY_SOFT_SEED_DELIVERABLE.md | 見 playtest |

Soft≠PASS｜唔 tip LIVE
