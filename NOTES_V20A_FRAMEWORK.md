# v20a0 — Freeplay PROGRAM FRAMEWORK（schema／stub／UI 殼）

Branch `feat/freeplay-framework-v20a0`. Follows merged `v19z31` (`4d89f46` / #81).

用戶：「開工」搭 program 框架，之後另一 bot 豐富劇情對白。本輪 **唔發明長篇粵語劇情弧**；Soft≠PASS；開完 PR **直接 merge**。

## Thesis 對齊

| 計劃點 | 框架落地 |
|---|---|
| 藏 nextHint | 既有 `BehaviorGate.nextHint_neverShow`；契約強制 `nextHint:""`；`__freeplay.nextHintHidden()` |
| 雙軌聲量／信用 | 既有；契約＋`effects.stats.stageVolume`／`industryCredit`；標籤可帶 delta |
| 選角標籤 | `STUB_CASTING_TAGS_v1.json`＋`S.castingTags`＋手帳「標籤」殼；殺青 `tagOnComplete` sink |
| 噂碎片 | `STUB_RUMOR_FRAGMENTS_v1.json`＋既有傳聞 pane；空 text 唔自動灌（等內容 bot） |
| 人情債×季節 | `STUB_FAVOR_DEBT_SEASON_v1.json`＋既有人情債 pane |
| MVP 紅星遠觀 | 既有 `STAR_SIGHTINGS` 四 id；stub overlay；`yip_manzi`→`yip_manji` |
| cafe_cha／agency_ho | 既有 LOCS（確認仍在） |
| CONTENT CONTRACT | `docs/CONTENT_CONTRACT.md` |

## Deliverables

1. `docs/CONTENT_CONTRACT.md` — 內容 bot 必讀  
2. `NOTES_V20A_FRAMEWORK.md` — 本檔  
3. `content/SCHEMA_FREEPLAY_FRAMEWORK_v1.json`  
4. `content/STUB_ERA_STARS_MVP_v1.json`  
5. `content/STUB_RUMOR_FRAGMENTS_v1.json`  
6. `content/STUB_FAVOR_DEBT_SEASON_v1.json`  
7. `content/STUB_CASTING_TAGS_v1.json`  
8. `content/STUB_STORY_BEATS_FREEPLAY_SLOTS_v1.json` — C1–C5 空槽  
9. `index.html` — `?v=20a0`；`FreeplayFramework` loader；標籤 tab；殺青／事態 tags sink  

## 另一 bot 應編輯

見契約 §3。精簡：

- **必填主戰場：** `STUB_STORY_BEATS_FREEPLAY_SLOTS_v1.json`（`playerFaceLine`／`beats[].lines`／choice `label`）  
- **噂文案：** `STUB_RUMOR_FRAGMENTS_v1.json` → `text`  
- **債條文案：** `STUB_FAVOR_DEBT_SEASON_v1.json` → `line`／`title`  
- **紅星短句（可選）：** `STUB_ERA_STARS_MVP_v1.json` rumorTeaser／silhouette（仍遠觀 only）  
- **唔好改：** BehaviorGate、SAVE key、閘數字、真藝名、長對話樹  

## Soft≠PASS

- 唔 tip LIVE  
- stub 文案以佔位為主；LIVE 遠觀句喺 stub 仍係「文案待補」時**保留**既有短句  
- 噂空 text **唔**自動入手帳（避免空白卡洗版）  

## Verify

`https://joinkidshk-glitch.github.io/linji-chutoutian-web-preview/?v=20a0&softBehaviorGate=1`（硬重整）

1. 控制台 `window.__freeplay.check()` → `{ ok:true }`  
2. 手帳有「標籤」分頁；空態有殼文案  
3. 傳聞／人情債分頁仍在  
4. 金龍茶餐廳／何生事務所 pin 仍在；對應 loc 可開遠觀（廖炳星＠茶餐廳等）  
5. 事態／地圖 tip **無** nextHint pacing 長文  
6. 殺青帶 `tagOnComplete` 嘅通告 → 標籤 pane 出現對應名  

## Key ids

`luk_baakyin` · `liu_bingxing` · `ngai_wingnaam` · `yip_manji`（別名 `yip_manzi`→`yip_manji`）
