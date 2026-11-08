# NOTES｜報紙系統 Soft 文案種子 v1

> 日期：2026-11-08（Asia/Hong_Kong）  
> Soft≠PASS｜**唔 tip LIVE**｜唔抬 `?v=`／SAVE｜出圖 HOLD｜89–92 HOLD  
> PLAN：`PLAN_NEWSPAPER_AND_FAME_RENAME_SOFT.md`  
> 來源：qwen3.7-max（raw：`content/_qwen_raw_newspaper_soft/`）

## 本包做咗咩
- 新建 `STUB_NEWSPAPER_MORNING_SOFT_v1.json`（preview＋sv 雙份）
- 殺青 `wrap_success` ≥15（film／tv／music／ad／any ×3）
- 得獎 `award_win` ≥8（四 medium ×2）
- 入圍 `award_nominee` ≥4（四 medium ×1）
- 虛構紙名：娛樂快報／電視週刊／星河娛樂版／樂壇速遞／消費情報
- 玩家面「聲望」；內部 `fameDelta`／`fame`
- 節奏註記：條件達成入佇列 → **第二日朝早**彈出（引擎／modal 由 Soft tip／iOS 做）

## 本包唔做
- 引擎 `newspaperQueue`／朝早 modal／剪報 pane 實作
- 聲望正名全 UI 掃（另線 Soft tip A）
- tip LIVE；抬 SAVE／產品 `?v=`；出圖；89–92

## 合入建議
1. Soft tip 讀 stub；殺青成功／頒獎結果 enqueue `eventKey`
2. 次日朝早彈出後套用 `fameDelta`（玩家面顯示「聲望」）
3. 可選：確認後餵 `rumorEcho` 入傳聞碎片
4. iOS Soft tip 與 preview index 對齊時再 bust softRev（唔抬產品 `?v=`）

## sha（寫檔時）
見交貨稿 `NEWSPAPER_SOFT_SEED_DELIVERABLE.md`。

## sha8
| 檔 | sha8 |
|---|---|
| STUB_NEWSPAPER_MORNING_SOFT_v1.json（preview＝sv） | `51e207bf` |
| SCHEMA_NEWSPAPER_MORNING_SOFT_v1.json | `1343f543` |
| NOTES（本檔寫入前基線；交貨稿為準） | 見交貨稿 |
| NEWSPAPER_SOFT_SEED_DELIVERABLE.md | 見 playtest |


## 合入 nit（Soft tip #101）
press 欄 `嗰`／`啦`／`嘅` 已改書面語：`np_wrap_film_03`、`np_win_tv_02`、`np_win_ad_02`（headline 與 clipLabel）、`np_nom_music_01`、`np_nom_ad_01`。`rumorEcho` 口語保留。原 stub sha8 `51e207bf`。
