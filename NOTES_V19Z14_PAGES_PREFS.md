# v19z14 — Pages deploy + familySafe prefs migration

Branch `fix/playtest-pages-v19z14`. Follow-up to v19z13（PR #63）：程式已合上 `main`，但 GitHub Pages **deploy 逾時**，線上仍餵 v19z12 HTML。

## Root cause（Pages）

- Workflow run `42344578840`（merge #63 / `782874c`）：`build` 成功上傳 artifact ≈174MB，`deploy` 卡喺 `actions/deploy-pages` **`syncing_files`**，約 10 分鐘後 `Timeout reached, aborting!`（預設 timeout 600000ms）。
- Pages API status：`errored` / `Page build failed.`
- Live `Last-Modified: Sat, 07 Nov 2026 05:28:53 GMT`＝上一成功建置（v19z12，`familySafeContent:false`）。
- Artifact 大小同成功嘅 v19z12 建置接近（≈174MB）→ 較似 CDN sync 短暫故障／超時，唔係新增巨型檔。NOTES／content 增量可忽略。

## Fixes（本版）

| # | Issue | Fix |
|---|-------|-----|
| 1 | Pages 未更新 → 複測誤判 z13 FAIL | 再推一版觸發建置；合併後 **poll 到 `built`／actions success** 先算完 |
| 2 | 瀏覽器仍有舊 localStorage `familySafeContent:false`（z12 default） | `loadPrefs()`：若 `familySafeContent===false` 且 `familySafeUserSet!==true` → 升為 `null` 並寫回（一次遷移） |
| 3 | 用戶顯式關閉要保留 | 設定「完成」讀家庭友善 checkbox 時設 `familySafeUserSet=true`；之後唔再當 legacy 遷移 |
| 4 | Cache bust | `?v=19z13` → `?v=19z14` |

已核對（沿用 z13）：

- `defaultPrefs().familySafeContent` 仍為 `null`
- `contentFilterOn`：true／false 強制；null → soft gate
- `modal` 按鈕仍 **先 `on()` 再 `closeModal()`**（設定表單可讀）

## Soft≠PASS

- 唔改 `featureFlag_softBehaviorGatePreview`／`gatePath` 名
- soft=1 + 新／已遷移 prefs → 家庭友善開；用戶喺設定取消勾選（`false` + `familySafeUserSet`）仍可關

## Verify

`https://joinkidshk-glitch.github.io/linji-chutoutian-web-preview/?v=19z14&softBehaviorGate=1`

1. `curl` live index 見到 `familySafeContent:null`（同 `?v=19z14`）
2. soft 新局／舊 prefs（曾被 z12 寫死 false）→ 金龍「後巷食糖水」、C1 無「抽煙」
3. 設定取消「家庭友善」→ 完成 → 再開仍關；原文恢復
4. Pages：`gh run list`／`pages/builds` status **`built`**（唔止 push）

## If deploy times out again

1. `gh run rerun <run_id> --failed` 或 `gh api -X POST .../pages/builds`
2. 考慮改 Actions 上傳時排除 `NOTES_*.md`／舊 `content/*soft*.json` 備份（artifact 仍以 `assets/` 為主 ≈186MB，slim 幅度有限）
3. 報告 exact blocker（仍 `syncing_files` timeout 就係 GitHub 側）

Auth: t3u（繼續改善）；複測續行 t6u／pt6u
