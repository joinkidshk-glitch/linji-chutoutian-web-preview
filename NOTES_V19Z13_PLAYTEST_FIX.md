# v19z13 — playtest fix（v19z12 複測 FAIL #5 + 新問題）

Branch `fix/playtest-improve-v19z13`. Source: `/workspace/playtest/linji-chutoutian-v19z12-retest.md`.

## Fixes

| # | Pri | Issue | Fix |
|---|-----|-------|-----|
| 1 | High | soft gate 無法啟用家庭友善（#5） | `defaultPrefs().familySafeContent` 改 `null`（未設定）；`contentFilterOn`：`true` 強制開、`false` 強制關、null／未設定 → 跟 `featureFlag_softBehaviorGatePreview`／`softPreviewOn`。soft URL 無顯式關閉時顯示食糖水、C1 無「抽煙」 |
| 2 | High | 設定「完成」存唔到 | `modal` 按鈕改 **先 `on()` 再 `closeModal()`**；用 `_modalGen` 若 `on` 開咗新 modal 就唔 close。設定讀 checkbox 時 DOM 仍在 |
| 3 | Med | 中週點日仍顯示「週一（唯讀）」 | `syncDateChrome` 唔再強制 `.on`／`planSelDay=today`；選日交俾 `renderNotebook`／用戶點選 |
| 4 | Polish | 設定亂寫死 false | 家庭友善勾選同 soft 預設一致時存 `null`（跟 gate），避免 live 撳完成誤強制關 |

## Cache

`?v=19z12` → `?v=19z13`

Prefs key 仍 `starVolunteer_prefs_v19z9`（相容；`familySafeContent` 可選 null／true／false）。

## Soft≠PASS

- 唔改 `featureFlag_softBehaviorGatePreview`／`gatePath` 名
- 家庭友善：soft 未顯式關 → filter 開；設定可強制開／關

## Verify

`https://joinkidshk-glitch.github.io/linji-chutoutian-web-preview/?v=19z13&softBehaviorGate=1`

1. soft 新局 → 金龍見「後巷食糖水搭訕」而非「後巷食煙」；C1 開場無「抽煙」
2. 設定勾「家庭友善內容」→ 完成 → 再開仍勾住；取消勾選可強制關 soft 替換
3. 訓練過日到週三 → 返手帳 → 點週三 → 右側「行程 · 週三（唯讀）」（唔卡週一）
4. live（無 soft）預設仍成人文案；設定可手動開家庭友善

## Deferred

- live 事態列表 pacing「約第 N 週」lockedHint 全面 soft-hide（複測 #4 觀察項；C1 結算 nextHint 已喺 z12 清）
- 完整音訊接線、手帳週列完全分層重排（沿用 z12 deferred）

Auth: t3u
