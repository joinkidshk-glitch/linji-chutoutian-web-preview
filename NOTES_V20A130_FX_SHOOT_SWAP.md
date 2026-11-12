# NOTES_V20A130 — 拍攝片換入 PixelLab character-animation 版（原檔覆蓋 fx_shoot.mp4）

## 拍板
- 用戶 2026-11-12 16:32 話「用這個放在遊戲看看」：將新 fx_shoot 片放入遊戲，畀用戶喺實機見到。
- 用戶 16:33 澄清：**用未放大嘅版本（1.0x），唔係 1.3x**。換入嗰條係 `fx_shoot_charanim.mp4`（46,231 bytes；960×540、24fps、3.0 秒、72 幀），1.3x 版（`fx_shoot_charanim_13x.mp4`，71,087 bytes）留檔，唔入遊戲。
- 試驗性換入：揮手 loop 接受與否＋場景顏色兩個決定仲未落，呢次純粹畀用戶實機睇新片。
- 新片來源：character-animation 路線——新 state「開心舉手」`6d2b54a4`（由 v2 `49907fa9` 開）→ `POST /animate-character` 9 幀 → 透明底疊落場景 `shoot_scene3.png` 機械式合成。塊面全程係阿偉（零鬍鬚、零嗌口、零光暈）；動作係左右手交替揮舞，唔係淨右手舉起→放低；場景青綠幕布顏色未調（之後獨立一步）。

## 改動（3 個檔案）
| 檔 | 改動 |
|---|---|
| `assets/fx/fx_shoot.mp4` | 原檔覆蓋：舊 41,351 bytes（samples19 像素拍攝片）→ 新 46,231 bytes（PixelLab character-animation 1.0x 原版），sha256 `f98a2cc9fc948403df0c6cf226afbfaebfa76450ccdd65daa56f6babfa7768bc` |
| `index.html`（1 行，L55209） | `actFx102Html()` 加 shoot 專屬 early return：`kind==="shoot"` 時播放 URL 係 `assets/fx/fx_shoot.mp4?v=20a130`；其餘 7 條片繼續行共用行 `?v=20a10` |
| `tests/test_fx130_static.py` | 新守門測試（見下） |

## 點解係 early return（查證結論）
- `actFx102Html()` 本來將 `ACT_FX102` 全部 8 條片一律加 `?v=20a10`（共用行 `const src = src0 + "?v=20a10";`）。
- 同路徑覆蓋而 URL 不變，返嚟嘅用戶瀏覽器會繼續播舊片（repo 已有教訓：app 按路徑快取，同路徑覆蓋後用戶仍見舊圖，要用新檔名或升版本參數繞過）。跟返 v129 前例：只升呢條片自己嘅參數做 `20a130`，其餘 7 條片＋產品 `?v=`＋SAVE key＋softRev 全部不變。
- 唔改共用行嘅原因：`tests/test_fx129_static.py` 硬斷言嗰行字面值（`const src = src0 + "?v=20a10";`），改咗佢會令 v129 測試 FAIL；`tests/test_fx102_logic.js` 會 eval `actFx102Html`，map 值必須保持 bare path（`/^assets\/fx\/fx_[a-z_]+\.mp4$/`），所以版本唔可以寫入 map。所以用 early return 處理 shoot，共用行原封不動。
- 註解冇寫其他測試硬計嘅版本字串（v129 教訓：`?v=20a104` 計數 16、`"v20a10"` 計數 7，兩者驗過唔郁）。

## 守門測試
- `tests/test_fx130_static.py`：新片存在＋byte 數 46,231＋sha256＋ffprobe 格式（960×540、24fps、3.0 秒、72 幀）＋shoot map 唔郁＋`?v=20a130` 接線＋其餘 7 條片仲係 `?v=20a10`＋休息片 `?v=20a129` 冇郁＋SAVE／softRev／產品 `?v=` 紅線。PASS；pristine 反證 FAIL（舊片 41,351 bytes、冇 `?v=20a130`），成立。
- 全套：（待補：pristine 基線 vs 分支結果）
- `node --check`：抽 inline script 段出嚟 check（Node 24 拒 `.html` 副檔名）。（待補結果）

## 實駕
- （待補：Playwright 390×844、`?softPreview=1`、本地鏡像，新遊戲 slot 3 → 拍攝行程 → 新片播完、0 pageerror／0 http404；pristine 對照見舊片）

## 合併紀錄
- （待補：分支、PR、squash commit、線上 byte／sha 核實）

## 回滾
- 成個 squash 係一個 commit：`git revert <squash>` 即退返 v129 狀態（舊片＋舊 `?v=20a10` 一併落返嚟）。
- 單檔回滾：`git checkout origin/main -- assets/fx/fx_shoot.mp4` ＋還原 index.html 嗰 1 行即可。
