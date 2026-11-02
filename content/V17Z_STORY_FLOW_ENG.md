# V17Z_STORY_FLOW_ENG

**SAVE：** `starVolunteer_map_v17z`  
**時間：** 2026-11-03 ~07:14（Asia/Hong_Kong）  
**預覽：** `joinkidshk-glitch/linji-chutoutian-web-preview`  
**HOLD：** Soft≠PASS；出圖暫緩  
**契約：** `FLOW_ENG_HANDOFF_v1.md` + `story_detail_c1_to_c17.json` **1.2.3**

## Eng

| # | 項 | 修法 |
|---|---|---|
| A1 | week_min:N / pacing.weekMin | evalToken + 非 C1 注入 pacing |
| A2 | days_after_prev:1 + 同日禁 | markDone 記 lastMainDoneDay；全域同日其他 C* 唔可播 |
| B | 即將可出 | 主線 C* 一律列；文案只用 lockedHint（C5 采兒／台慶） |
| C | 「下一節」 | 永不 showB01；清 pending flag 後 start(下一節)／列表 |
| — | when 字串 | 唔解析；以 pacing／token 為準 |

## 假設
game week = floor(dayIndex/7)+1。C1 openConditions=[] 開局可播（唔強制 weekMin:3 token）。C2–C17 oc 已雙寫 week_min／days_after_prev。

## Tester 覆測
1) C1 結算「下一節」唔開手帳 B01  
2) 同曆日唔可 C1→C2→C3→C4  
3) C4 後「即將可出」見 C5 lockedHint（采兒／台慶），無 need_done:

## Ship
- commit：（push 後填）
- curl-verify：（push 後填）
- tar：`/workspace/star-volunteer-web-v17z.tar.gz`
- URL：https://joinkidshk-glitch.github.io/linji-chutoutian-web-preview/?v=17z
