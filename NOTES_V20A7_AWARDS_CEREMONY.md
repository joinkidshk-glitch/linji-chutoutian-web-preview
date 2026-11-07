# NOTES · Freeplay v20a7 — 定期頒獎禮（四媒介輕量殼）

> **時間：** 2026-11-07（Asia/Hong_Kong）  
> **狀態：** Soft≠PASS；四軌引擎已落地；**唔 tip LIVE**；**獎項顯示名暫用 placeholder**（內容 bot 之後改 `displayName`）  
> **預覽：** `?v=20a7&softBehaviorGate=1`  
> **SAVE：** `starVolunteer_map_v19w`（只加 `awardsLog`／`awardsFlags`）  
> **設計：** `NOTES_V20A7_AWARDS_CEREMONY_DESIGN.md`  
> **契約：** `docs/CONTENT_CONTRACT.md` §3.6

## 本輪加咗咩

1. **四軌季節排程（Soft only）**
   - 春 `award_harbour_ad` 維港街招・年度廣告賞  
   - 夏 `award_golddisc_music` 星河金碟夜  
   - 秋 `award_harbour_film` 維港影藝獎  
   - 冬 `award_singho_tv` 星河台慶・年度頒獎夜  
2. **共用 UX：** 邀請 sheet（出席／推辞／稍後）→ 結果＋傳媒合併 sheet；**跳過紅地毯**  
3. **tier：** `gallery`｜`nominee`；第一年偏觀禮／入圍  
4. **對齊殺青** `matchTypes`／`metricEcho`（關注度／銷量／票房／收視）  
5. **C10 防疊** 只影響電視軌  
6. **pending 單槽＋FIFO 排隊**；稍後＝當日 snooze（唔即刻再弹）；關 sheet 後經 `goToMapForBrowse` 還原 CTA  
7. **API：** `__awards.check`／`preview`／`debugForceSeasonWindow`／`log`／`flags`

## 檔案

- `content/SCHEMA_AWARDS_CEREMONY_v1.json`（`implemented:true`）  
- `content/STUB_AWARDS_CEREMONY_v1.json`  
- `content/SCHEMA_FREEPLAY_FRAMEWORK_v1.json` meta → v20a7＋`awardsCeremony`  
- `docs/CONTENT_CONTRACT.md` §3.6  
- `index.html` 引擎＋hydrate＋loader＋map wire；`?v=20a7`

## Verify

```js
await __freeplay.load();
__freeplay.check();     // ok:true；infra:"v20a7"；awardsCeremony:true；四軌 id
__awards.check();       // ok:true
__awards.preview({ ceremonyId:"award_harbour_ad", year:1988, forceTier:"gallery" });
__awards.preview({ ceremonyId:"award_golddisc_music", year:1988, forceTier:"nominee" });
__awards.preview({ ceremonyId:"award_harbour_film", year:1988, forceTier:"nominee" });
__awards.preview({ ceremonyId:"award_singho_tv", year:1988, forceTier:"nominee" });
__awards.debugForceSeasonWindow("award_harbour_ad");
// 出席 → 結果 sheet → 關後地圖 CTA 仍可開
```

## 內容 bot

只改 stub 文案／`displayName`（**之後落實獎名**）；唔改 id、cadence、matchTypes、threshold、SAVE、BehaviorGate。禁真獎名／真藝名；`nextHint` 必須空。

## HOLD

tip LIVE／抬 SAVE／紅地毯／真獎名／街坊人氣票獨立典禮／89–92 獎季／長 romance
