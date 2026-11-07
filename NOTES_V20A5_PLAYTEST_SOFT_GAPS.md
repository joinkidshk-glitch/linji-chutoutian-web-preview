# NOTES · Freeplay v20a5 PLAYTEST — Soft gaps（蘇芷茵針／記數／獎勵 polish）

> **時間：** 2026-11-07（Asia/Hong_Kong）  
> **狀態：** Soft≠PASS；**唔 tip LIVE**；SAVE key 不變（`starVolunteer_map_v19w`）  
> **預覽：** `?v=20a5&softBehaviorGate=1`  

## 本輪修

1. **蘇芷茵遠觀針**
   - 根因：`STAR_SIGHTINGS`／`phase3Stars()` 已有 `so_jiyan@rec_wanchai`，但地圖 `locActionFlags` 唔計遠觀＝有事；預設「只亮有事」時灣仔針被淡化藏起。
   - 修：遠觀地點 `hasStar` → `hasAction`；針上「星」標記＋圖例「遠觀」；`__phase3`／`__freeplay` 自檢 `so_jiyan` 活躍於 `rec_wanchai`。

2. **手帳「記數」分頁**
   - 玩家面 tab：行程／**記數**／傳聞／人情債（標籤仍 `?devTags=1`）。
   - 記數＝能力／存款／雙軌；選單「狀態」跳同一頁（唔另開第二套 stats UI）。

3. **殺青獎勵 polish**
   - 標題：`workTitle` 優先；剝巢狀 `《》`，sheet 只包一次 → 唔再 `《《作品》…》`。
   - Soft 玩家 sheet **唔顯示** `短訊可換；內容 bot 改 STUB_POST_SHOOT_REWARDS。`（`?devTags=1` 先見；NOTES／contract 保留）。

## 自檢

```js
await __freeplay.load();
__freeplay.check();   // ok:true；infra:"v20a5"；ui:ledger；so_jiyan_loc
__phase3.check();     // so_jiyan_active
__reward.check();     // title_double／stub_tip_visible 唔 fail
```

## 手動

1. Soft 新局 → 地圖見灣仔唱片亮針＋「星」→ 開地點有「遠觀：蘇芷茵」。
2. 手帳 →「記數」見能力／存款；選單「狀態」落入同一分頁。
3. 殺青 →「傳媒・街外・成績」標題單層《》；無 stub 工程提示。

## 非本輪

- C2 pacing、tip LIVE、89–92、LOOKS gen、romance trees
