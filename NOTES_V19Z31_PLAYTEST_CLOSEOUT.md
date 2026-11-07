# v19z31 — playtest backlog closeout（經濟 · 加速返看 · 選單 CTA · C2 路徑）

Branch `fix/playtest-closeout-v19z31`. Follows merged `v19z30` (`9a351ee` / #80).

用戶：「全部做完再告訴我」。本輪一次收齊剩餘玩測項；開完 PR 直接 merge。

## Done

| # | Item | What |
|---|------|------|
| 1 | 早期經濟 W1–4 | **核實仍生效**：`livingCostRoll` 頭4週 $1,400–1,800（中位 $1,600）；第5週起 $2,000–2,800。開局 $12,000 + 入場片酬可撐。無需再削生活費。 |
| 2 | 加速「本週最值得返看」 | **核實仍接線**：`weekBestReplayLine` 已掛加速摘要／加速完成卡；`noteWeekHighlight` 掛事態／通告／傳聞／傾談。補：行程訓練日一律 `weekTrainDone++`（先前只有 acting 會計），令無通告週仍可顯示訓練返看。 |
| 3 | 傾談／送禮 + 地點 CTA | **核實**：`ensureLocSheetInteractive`／`sheet-live`／soft 強制解鎖仍在；傾談／送禮結算後 soft 重開 loc。庫存空加「去香江唱片小賣」CTA。 |
| 4 | 人脈／拍攝簿／人情債 | **加深可玩路徑**：人脈每卡「去找 · 地點」→ `openLoc`；拍攝簿空／有貨都有「去通告欄／相關地點」；人情債 pane soft／早期自動種教學債＋空態「去何生事務所」。還款／傾談／通告欄唔再係純 stub。 |
| 5 | 通告 3／3 → 第2幕 | **修＋保底**：`liveGigCount` 取 `max(story.gigCount, done_* flags)`；殺青時 `S.story.gigCount++`；soft 入場試鏡保底 ≥78%；C2 前 soft 板面保底 **3** 張可報入場；缺 `tvb_rules_gossip` 時金龍／事務所提示打聽／請教；殺青 toast「通告進度 x／3」。 |
| 6 | 角色自訂 | **跳過**（見下） |

## Deferred / skipped

| Item | Why |
|------|-----|
| 角色自訂（改名／換造型／頭像） | 不便宜：主角「阿偉」硬編碼於標題、頂欄、NPC 對白、事態文案與肖像 key（`hero_awi`）；無備用造型資產；改名會令整段港產對白人稱錯位。試玩優先保主線可通。若要做，應另開「新局自訂名＋少量稱謂替換」專案，唔塞呢輪 closeout。 |

## Soft≠PASS

- 唔改 BehaviorGate parsers／`featureFlag_softBehaviorGatePreview`／`gatePath`／C2 stub 門檻數字本身（仍 weekMin=4、gigCountMin=3、rumor）
- soft 只加：入場試鏡保底、板面 need=3、進度 toast／打聽提示、教學債種子
- 唔 tip LIVE

## Verify

`https://joinkidshk-glitch.github.io/linji-chutoutian-web-preview/?v=19z31&softBehaviorGate=1`（硬重整）

1. 新局 W1–4 週末生活費落在 $1,400–1,800；壓力預覽寫「頭4週優惠」
2. 加速本週剩餘 → 摘要有「本週最值得返看：…」
3. 選單人脈 →「去找」開地點可傾談；拍攝簿空 →「去通告欄」；人情債有教學債可「去還」
4. 入場通告試鏡多數可過；殺青見「通告進度 x／3」；板面 soft 至少 3 張可報直至 C2
5. C1 後第3週起去金龍／事務所 → 可聽 `tvb_rules_gossip`；第4週＋3 殺青＋情報 → C2 可播

## Key files

- `index.html` — closeout 邏輯／CTA／cache `?v=19z31`
- `NOTES_V19Z31_PLAYTEST_CLOSEOUT.md` — 本檔
