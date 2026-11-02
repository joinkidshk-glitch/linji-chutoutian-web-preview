# Phase1 文案交付清單（書面語）

語域：全面繁體書面語（用戶已批）。DeepSeek 已產 detail；**已接入** `index.html`（2026-11-02）。

| 檔案 | 內容 | 數量 |
|---|---|---|
| `COPY_PLAN_v1.md` | 可執行計劃 | — |
| `events_zh_HK.json` | 試鏡／拍攝／週結／訓練事件模板 | 20 鍵／59 句 |
| `story_beats_phase1.json` | 四章開結＋B01–B10 | 4 章／10 beat |
| `npc_lines_core.json` | HTML 六人對話池 | 6×30＝180 句 |
| `gigs_1988.json` | 既有年庫（本階段不重產） | 30 則；僅 QA 預留 |

## 接入方式
- `index.html` 內嵌 `NPC_LINES_CORE` / `EVENTS_ZH_HK` / `STORY_BEATS_PHASE1`（與 GIGS 相同，兼容 `file://`）
- 啟動時 `refreshCopyPacksFromDisk()` 嘗試 `fetch('content/….json')`，失敗則保留內嵌快照
- 備份：`index.html.bak-before-copy-wire`
