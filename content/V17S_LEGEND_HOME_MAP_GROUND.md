# V17S_LEGEND_HOME_MAP_GROUND

**SAVE：** `starVolunteer_map_v17s`  
**時間：** 2026-11-03 ~04:20（Asia/Hong_Kong）  
**預覽：** `joinkidshk-glitch/linji-chutoutian-web-preview`（lean Pages）  
**HOLD：** Soft≠PASS；唔 formal publish；出圖暫緩

## 對標（夜間自主｜劇情可發現性＋地圖日常接地）

延續 v17r PASS；本輪唔開新長劇情，只補「睇到針＝知係事態」同「手帳知去邊」。

| # | 項 | 根因 | 修法 |
|---|---|---|---|
| 1 | 地圖有「劇」角標，圖例無對應 | legend 只有有板／情報／熟人／非本區 | 圖例加「劇」事態（同 pin `.mark-story`） |
| 2 | map-hint 只講板／情報 | help 句未提事態 | help 改「有板／情報／「劇」事態見圖例」；story 弱提示加「金框／劇針」 |
| 3 | 手帳事態句唔接地圖 | `storyHomeHintHtml` 只有標題 | open 時加「地圖去「星河…」」；open 空則下一主線 lockedHint 一句＋回地圖（PLAN_MAP (B)） |

## 改動檔

- `/workspace/star-volunteer-web/index.html`（SAVE→v17s；legend；CSS；map-hint；storyHome／wire）
- 本 NOTES

## 自檢

- [x] SAVE＝v17s
- [x] legend 有 lg-story／「劇」事態
- [x] soft C5／era_* 路徑未改（延續 v17q／v17r）
- [ ] Soft≠PASS；出圖未做
- [ ] 瀏覽器覆測待跑

## Ship

- （push 後填 commit／curl-verify）
- URL：https://joinkidshk-glitch.github.io/linji-chutoutian-web-preview/?v=17s （清 `starVolunteer_map_*`）
