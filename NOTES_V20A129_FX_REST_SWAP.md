# NOTES_V20A129 — 休息片換入 PixelLab 瞓覺片 v3（原檔覆蓋 fx_rest.mp4）

## 拍板
- 用戶 2026-11-12 14:54 話 v3「這個 ok 了」：瞓覺片 v3 正式換入遊戲，取代舊嘅 fx_rest.mp4（舊嗰條 samples19 像素瞓覺片用戶多次話唔 ok）。
- v3 來源：`~/workspace/linji-rest-pixellab-sample/rest_sleep_v3.mp4`（36,212 bytes；960×540、24fps、3.0 秒、72 幀；全程淨係瞓緊覺呼吸 loop，夜晚到底，冇起床、冇晨光、冇 Zzz）。
- 樣本驗證已喺換入前做完（見 `SAMPLE_NOTES_V2.md`＋v3 組裝紀錄）：呼吸 loop 13 幀逐格量度係真・平靜呼吸（250–515 px／幀，loop 收口順滑）；v3 組裝 0 次生成。

## 改動（2 個檔案）
| 檔 | 改動 |
|---|---|
| `assets/fx/fx_rest.mp4` | 原檔覆蓋：舊 14,606 bytes（samples19 像素瞓覺片）→ 新 36,212 bytes（PixelLab v3），sha256 `c1057a3f613474826b992e0b55c850bde08ea6370b98d5691ec8810083894c59` |
| `index.html`（1 行，L54995） | `restSleepFxHtml()` 嘅 cache-buster 由 `?v=20a10` 升做 `?v=20a129`，即係播放 URL 由 `assets/fx/fx_rest.mp4?v=20a10` 變 `assets/fx/fx_rest.mp4?v=20a129` |

## 點解要改呢 1 行（查證結論）
- `restSleepFxHtml()` 本來將 `REST_SLEEP_FX_SRC` 後面加 `?v=20a10`（同產品版本同值）；其餘 7 條 fx 片（`actFx102Html`）一樣係 `?v=20a10`。
- 同路徑覆蓋而 URL 不變，返嚟嘅用戶瀏覽器會繼續播舊片（repo 已有教訓：app 按路徑快取，同路徑覆蓋後用戶仍見舊圖，要用新檔名或升版本參數繞過）。
- 跟返 v102 前例：背景圖用每資產版本參數（`?v=20a104`），產品 `?v=` 不變。所以淨係升呢條休息片自己嘅參數做 `20a129`，其餘 7 條片＋產品 `?v=`＋SAVE key＋softRev 全部不變。
- 舊檔 `assets/fx/awei-rest-sleep.mp4`（v102 寫實片）照舊保留唔刪。

## 守門測試
- `tests/test_fx129_static.py`：新片存在＋byte 數 36,212＋ffprobe 格式（960×540、24fps、3.0 秒、72 幀）＋`restSleepFxHtml` 帶 `?v=20a129`＋其餘 7 條片仲係 `?v=20a10`＋SAVE／softRev／產品 `?v=` 紅線。PASS；pristine 反證 FAIL（舊片 14,606 bytes、冇 `?v=20a129`），成立。
- 全套：pristine 基線 **175 PASS／12 FAIL**（實測，`qa129/suite_baseline126.txt`）；分支 **176 PASS／12 FAIL**（`qa129/suite_work129.txt`），FAIL 清單同基線完全一致，零回歸（＋1 PASS 係新測試）。
- 過程記錄：初版 index.html 註解入面寫咗 `?v=20a104` 字樣，令 `test_scene104_static.py` 嘅硬計數由 16 變 17 而 FAIL——已將註解改寫（唔再出現該字串），重跑全套後 PASS。教訓：唔好喺 index.html 註解入面寫其他測試硬計嘅版本字串。

## 實駕
- Playwright 390×844、`?softPreview=1`、本地鏡像（工作副本 `python3 -m http.server`），新遊戲（slot 3）→ 入星河電視台（tv 型地點先有「休息室歇陣」掣；事務所 type=agency 冇）→ 撳「休息室歇陣」→ 過確認 → 日結板出 `#rest-sleep-video`。
- **Branch PASS**：video `src`＝`assets/fx/fx_rest.mp4?v=20a129`、readyState 4、960×540、3 秒、currentTime 1.88→3.0（播完）、served fx 36,212 bytes／sha `c1057a3f…` 同本地檔一致、**0 pageerror、0 http404**；截圖 `qa129/shots/branch_rest_sleep.png` 見新片（月夜睡房、阿偉瞓喺床度全身）。
- **Pristine 對照 PASS**（同一腳本）：video `src`＝`?v=20a10`、舊片 14,606 bytes／sha `5f8d8366…`、同樣播完、0 pageerror；截圖 `qa129/shots/pristine_rest_sleep.png` 見舊片（細頭＋Zzz、啡牆）——兩邊視覺上明顯唔同，證實實駕真係分得出新舊片。
- 過程記錄：① 初版 drive 入錯何生事務所（agency 冇休息掣），轉星河電視台後 PASS；② 8952 port 俾另一統籌嘅 server 佔住，轉 8955（冇 kill 佢）。

## 合併紀錄
- main commit：`be21881`（squash，PR #183，分支 `v129-rest-swap` `f297847`；基底 v20a126 `c71526a`）
- 線上核實：index.html 200、5,161,329 bytes、sha256 `e04c3109c0cd6559f3e66d7ff12c2e80020b6e5307757e723cc844b47b172dc5`（同 origin/main 完全一致）；`assets/fx/fx_rest.mp4` 200、36,212 bytes、sha256 `c1057a3f613474826b992e0b55c850bde08ea6370b98d5691ec8810083894c59`（同 origin/main／v3 原檔完全一致）
- 測試：全套 **176 PASS／12 FAIL**（基線 v126 main 175／12＋1 新測試；FAIL 清單同基線一致，零回歸）。
- 實駕：休息日日結板播新片（`fx_rest.mp4?v=20a129`、readyState 4、960×540、currentTime 1.88→3.0），0 pageerror；pristine 對照播舊片（`?v=20a10`）。

## 回滾
- 成個 squash 係一個 commit：`git revert <squash>` 即退返 v126 狀態（舊片＋舊 `?v=20a10` 一併落返嚟）。
- 單檔回滾：`git checkout origin/main -- assets/fx/fx_rest.mp4` ＋還原 index.html 嗰 1 行即可。
