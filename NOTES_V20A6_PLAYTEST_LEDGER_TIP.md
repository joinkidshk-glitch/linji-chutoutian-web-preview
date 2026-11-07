# NOTES · Freeplay v20a6 PLAYTEST — Soft ledger tab path + stub tip strip

> **時間：** 2026-11-07（Asia/Hong_Kong）  
> **狀態：** Soft≠PASS；**唔 tip LIVE**；SAVE key 不變（`starVolunteer_map_v19w`）  
> **預覽：** `?v=20a6&softBehaviorGate=1`

## Smoke FAIL → 修

### 1) 手帳「記數」／選單「狀態」
v20a5 DOM 已有 `#htab-ledger`／`#home-pane-ledger`，但玩家路徑唔穩：

| 符號 | 角色 |
|------|------|
| `#htab-ledger` / `#home-pane-ledger` / `#ledger-list` | Soft 手帳「記數」真正渲染點 |
| `setHomeTab("ledger")` + `renderLedgerPane()` / `ledgerStatsHtml()` | 記數內容（雙軌／能力／存款） |
| `showStats()`（選單 `data-m="stats"`） | **必須**開同一記數 tab |
| `enterHome(summary, editable, initialTab)` | v20a6 第三參；`showStats` 傳 `"ledger"` |

**根因：** `enterHome` 結尾永遠 `setHomeTab("plan")`，`showStats` 只靠 `setTimeout(40ms)` 再切記數 → Soft 玩測常睇到行程／或舊「狀態」modal 印象。  
**修：** `enterHome(..., "ledger")` 同步切記數；`showStats` 唔再開 `<h3>狀態` modal（保底亦係「記數簿」）。CSS 固定 tab order，記數唔可 `display:none`。

### 2) 殺青獎勵 stub foot
`renderPostShootRewardHtml` Soft 玩家 sheet **唔再**因 `localStorage starVolunteer_devTags` 顯示  
`短訊可換；內容 bot 改 STUB_POST_SHOOT_REWARDS。`  
只喺 URL `?devTags=1` 注入；NOTES／contract 保留說明。

## 自檢
```js
await __freeplay.load();
__freeplay.check();   // ok；infra:"v20a6"；ui:ledger；唔 fail ui:stats_modal_status
__reward.check();     // stub_tip_visible 唔 fail（無 ?devTags=1）
__phase2.openLedger(); // 手帳記數 on
```

## 手動（computerUse）
1. Soft 新局 → 手帳 → 見 **行程／記數／傳聞／人情債**
2. 選單 → 狀態 → **同一記數**（唔另開「狀態」modal）
3. 殺青獎勵 sheet **無** stub foot

## 非本輪
蘇芷茵遠觀（v20a5 PASS 保留）、C2 pacing、tip LIVE、romance
