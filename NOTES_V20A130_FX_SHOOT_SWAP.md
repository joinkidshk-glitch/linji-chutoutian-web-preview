# NOTES_V20A130 — 拍攝片換入 PixelLab character-animation 版（原檔覆蓋 fx_shoot.mp4）

## 拍板
- 用戶 2026-11-12 16:32 話「用這個放在遊戲看看」：將新 fx_shoot 片放入遊戲，畀用戶喺實機見到。
- 用戶 16:33 澄清：**用未放大嘅版本（1.0x），唔係 1.3x**。換入嗰條係 `fx_shoot_charanim.mp4`（46,231 bytes；960×540、24fps、3.0 秒、72 幀），1.3x 版（`fx_shoot_charanim_13x.mp4`，71,087 bytes）留檔，唔入遊戲。
- 試驗性換入：揮手 loop 接受與否＋場景顏色兩個決定仲未落，呢次純粹畀用戶實機睇新片。
- 新片來源：character-animation 路線——新 state「開心舉手」`6d2b54a4`（由 v2 `49907fa9` 開）→ `POST /animate-character` 9 幀 → 透明底疊落場景 `shoot_scene3.png` 機械式合成。塊面全程係阿偉（零鬍鬚、零嗌口、零光暈）；動作係左右手交替揮舞，唔係淨右手舉起→放低；場景青綠幕布顏色未調（之後獨立一步）。

## 改動（4 個檔案＋1 份 NOTES）
| 檔 | 改動 |
|---|---|
| `assets/fx/fx_shoot.mp4` | 原檔覆蓋：舊 41,351 bytes（samples19 像素拍攝片）→ 新 46,231 bytes（PixelLab character-animation 1.0x 原版），sha256 `f98a2cc9fc948403df0c6cf226afbfaebfa76450ccdd65daa56f6babfa7768bc` |
| `index.html`（1 行，L55209） | `actFx102Html()` 加 shoot 專屬 early return：`kind==="shoot"` 時播放 URL 係 `assets/fx/fx_shoot.mp4?v=20a130`；其餘 7 條片繼續行共用行 `?v=20a10` |
| `tests/test_fx130_static.py` | 新守門測試（見下） |
| `tests/test_travel114_static.py` | resync only：index.html +1 行（行 55209），FREE／COUNT 行號 ≥55209 者 +1（5 個 COUNT＋8 個 FREE；DEF／WRAPPER 行號不變）。`qa130/resync_travel114.py` 核實：44 個 openLoc( 呼叫點序列逐字一致、內容逐行相同，純漂移。qa130/ 本身係工作副本 scratch，唔入 repo（跟 qa127–129 前例） |

## 點解係 early return（查證結論）
- `actFx102Html()` 本來將 `ACT_FX102` 全部 8 條片一律加 `?v=20a10`（共用行 `const src = src0 + "?v=20a10";`）。
- 同路徑覆蓋而 URL 不變，返嚟嘅用戶瀏覽器會繼續播舊片（repo 已有教訓：app 按路徑快取，同路徑覆蓋後用戶仍見舊圖，要用新檔名或升版本參數繞過）。跟返 v129 前例：只升呢條片自己嘅參數做 `20a130`，其餘 7 條片＋產品 `?v=`＋SAVE key＋softRev 全部不變。
- 唔改共用行嘅原因：`tests/test_fx129_static.py` 硬斷言嗰行字面值（`const src = src0 + "?v=20a10";`），改咗佢會令 v129 測試 FAIL；`tests/test_fx102_logic.js` 會 eval `actFx102Html`，map 值必須保持 bare path（`/^assets\/fx\/fx_[a-z_]+\.mp4$/`），所以版本唔可以寫入 map。所以用 early return 處理 shoot，共用行原封不動。
- 註解冇寫其他測試硬計嘅版本字串（v129 教訓：`?v=20a104` 計數 16、`"v20a10"` 計數 7，兩者驗過唔郁）。

## 守門測試
- `tests/test_fx130_static.py`：新片存在＋byte 數 46,231＋sha256＋ffprobe 格式（960×540、24fps、3.0 秒、72 幀）＋shoot map 唔郁＋`?v=20a130` 接線＋其餘 7 條片仲係 `?v=20a10`＋休息片 `?v=20a129` 冇郁＋SAVE／softRev／產品 `?v=` 紅線。PASS；pristine 反證 FAIL（舊片 41,351 bytes、冇 `?v=20a130`），成立。
- 全套：pristine 基線（常駐 clone main d37284a）**176 PASS／12 FAIL**；分支 **177 PASS／12 FAIL**（+1 係新測試 test_fx130；FAIL 清單同基線完全一致，12 個環境性）。中途曾經多出 1 個 FAIL：`test_travel114_static.py`（硬寫行號，+1 行漂移所致）——已按既定 resync 慣例修正（見上），重跑後歸零回歸。結果檔 `qa130/suite_baseline129.txt`／`qa130/suite_work130.txt`（work-copy scratch）。
- `node --check`：抽兩段 inline script 出嚟 check（Node v24.22.1），兩段都 OK。

## 實駕（`qa130/drive130.py`，Playwright 390×844、`?softPreview=1`、本地鏡像）
- **branch（work copy，內容同 main e5c940d 一致）VERDICT PASS**：served index.html 5,161,715 bytes sha `af757c71…` 同線上值一致；served fx_shoot.mp4 46,231 bytes sha `f98a2cc9…` 同線上值一致。新遊戲 slot 3 → 地圖 → 改植拍攝日（電視劇「都市電視劇」，tvb_harbour）→ 推進 → 日結板「拍攝中：都市電視劇」出 `#act-fx102-video`，src `assets/fx/fx_shoot.mp4?v=20a130`，readyState 4、960×540、3.0 秒，currentTime 1.31→2.81（播緊，唔係靜幀），0 pageerror、0 http404。截圖 `qa130/shots/branch_shoot.png`（畫面：阿偉中央舉手揮舞、青綠幕布場景、木地板、左右配角＋場記板——即係新片，唔係舊像素片）。
- **pristine 對照（常駐 clone main d37284a）VERDICT PASS（控制組）**：同一流程播嘅係舊片 `assets/fx/fx_shoot.mp4?v=20a10`（41,351 bytes，sha `0286cb7b…`），readyState 4、960×540、播緊，0 pageerror——證明 drive 分得出新舊片。截圖 `qa130/shots/pristine_shoot.png`。

## 合併紀錄
- 分支 `v20a130`（commit `d5c9487`，工作副本 `~/workspace/linji-work130/`）。注意：工作副本嘅 origin 係常駐 clone 本地路徑，唔係 github.com——`git push origin` 只係推咗去常駐 clone；要再喺常駐 clone `git push origin v20a130` 先至真係上 GitHub（頭三次開 PR 失敗 `PullRequest.head (invalid)` 就係因為分支未上 GitHub）。
- PR #184（https://github.com/joinkidshk-glitch/linji-chutoutian-web-preview/pull/184），squash 合併入 main：**`e5c940d`**（2026-11-12）。
- 線上核實（合併後約 2 分鐘 curl，第一次即對上，唔使重觸發）：index.html **5,161,715 bytes、sha256 `af757c710b006914c968c75001a301a463492b8db55789aceded38de37ead4e0`**；`assets/fx/fx_shoot.mp4` **46,231 bytes、sha256 `f98a2cc9fc948403df0c6cf226afbfaebfa76450ccdd65daa56f6babfa7768bc`**——兩者同分支完全一致，部署即係 ground truth。
- 本 NOTES 補充段（全套／實駕／合併紀錄）由 follow-up commit 補入 main（跟 v129 前例）。

## 回滾
- 成個 squash 係一個 commit：`git revert <squash>` 即退返 v129 狀態（舊片＋舊 `?v=20a10` 一併落返嚟）。
- 單檔回滾：`git checkout origin/main -- assets/fx/fx_shoot.mp4` ＋還原 index.html 嗰 1 行即可。
