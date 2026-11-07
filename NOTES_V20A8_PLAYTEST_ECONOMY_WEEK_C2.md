# NOTES · Freeplay v20a8 — 24週玩測三修（經濟 · 週確認 · C2 餘件）

> **時間：** 2026-11-07（Asia/Hong_Kong）  
> **狀態：** Soft≠PASS；**唔 tip LIVE**；SAVE `starVolunteer_map_v19w`（只加 flag 電報位，唔抬 key）  
> **預覽：** `?v=20a8&softBehaviorGate=1`  
> **來源：** 24 週 Soft 試玩（v20a7）改善項 1–3

## 本輪修咗咩

### 1) 經濟死亡螺旋＋$0 電報
- **Soft 生活費緩坡**（`livingCostBand`；LIVE 不變）  
  - W1–4：$1,400–1,800（舊）  
  - Soft W5–8：$1,600–2,200  
  - Soft W9–12：$1,800–2,400  
  - 之後／LIVE：$2,000–2,800  
- **Soft 入場通告片酬 ×1.35**（`entryTier` 獲聘鎖薪時）  
- **$0／偏緊電報**：`moneyThreatLevel` → HUD 上色、`#map-money-tip`、週結旁白、壓力預覽警告  
- **翻身 CTA 文案**：通告欄入場工＋金龍／事務所打聽（唔 tip LIVE）

### 2) 「確定本週行程」UX
- 按鈕常顯；**編輯態**＝「確定本週行程」（開壓力預覽）；**唯讀態**＝ disabled「行程已定 · 下週一可改」+ `is-locked` 樣式  
- `#nb-plan-mode` 橫幅分清「計劃模式」vs「唯讀手帳」  
- 唯讀隱藏快捷「全日休息／訓練／清空」；標題改「編輯本週行程」／「本週行程（唯讀）」  
- `confirmPlan` 鎖定態 toast 講清楚；預覽 modal 失敗則直接提交（唔靜默）

### 3) C2 閘不透明
- `BehaviorGate.progressToward` 加 `remain[]`／`lockLine`（通告／週／傳聞／地點／人情／聲望）  
- `storyMainProgressLine` 優先展示具體未達項（例如「未聽聞「電視城廠景生存守則」」「到金龍茶餐廳或…」）  
- **唔改** C2 stub 門檻數字（仍 weekMin=4、gigCountMin=3、rumor）

## Soft≠PASS
- 唔改 `featureFlag_softBehaviorGatePreview`／`gatePath`／BehaviorGate parsers  
- 生活費緩坡＋入場片酬倍率只喺 Soft  
- 唔 tip LIVE

## Verify
`https://joinkidshk-glitch.github.io/linji-chutoutian-web-preview/?v=20a8&softBehaviorGate=1`（硬重整）

1. Soft 新局：壓力預覽生活費 W5 起寫「試玩緩坡」；LIVE 無 flag 仍係 $2,000–2,800  
2. Soft 接入場通告 → 獲聘片酬約高 35%  
3. 把錢花到 $0（或 console `S.money=0; refreshMoneyHud()`）→ 頂欄存款轉紅＋地圖現金提示＋翻身句  
4. 週結現款低過下週預估 → 結算旁白有警告  
5. 週一排行程：見「計劃模式」橫幅＋「確定本週行程」→ 壓力預覽 → 確定出發  
6. 行程已定／週中開手帳：橫幅「唯讀」；確定鍵灰＋「行程已定 · 下週一可改」；快捷列隱藏；誤撳有 toast  
7. C1 後未湊齊 C2：地圖事態進度唔止「通告 2／3 · 第2幕即將」，要列出週／傳聞／地點等餘件  
8. `BehaviorGate.progressToward({beatId:"C2"})` → `remain` 陣列有具體字

## 檔案
- `index.html` — 經濟／HUD／週確認／C2 進度；`?v=20a8`  
- `content/SCHEMA_FREEPLAY_FRAMEWORK_v1.json` — meta v20a8  
- `docs/CONTENT_CONTRACT.md` — 框架標 v20a8  
- `NOTES_V20A8_PLAYTEST_ECONOMY_WEEK_C2.md` — 本檔

## Retest（合埋後）

- Merge：`be9da6c`（PR #90）
- GH Pages HTML 已含 `?v=20a8`×31、`livingCostBand`、`moneyThreatLevel`、`nb-plan-mode`、確定鍵鎖定文案
- 單元抽樣：Soft W5／W9 緩坡帶正確；LIVE W5 仍 full $2k–2.8k；$0→broke、$500→critical
- Soft≠PASS；唔 tip LIVE；SAVE 未抬
