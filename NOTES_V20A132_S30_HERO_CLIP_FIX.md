# NOTES_V20A132 — S-30 通告詳情卡標題被切（v128 回歸修復）

## 現象（用戶 2026-11-12 18:27 實機截圖捉到，已確認）
S-30 通告詳情卡（金鐘創意／方樂怡）喺真 iPhone（430×932）上面：
通告名俾人攔腰切斷，只見字頭一半；成個摘要（類型、要求格、片酬、檔期、簡介）
俾擠到得返十幾 px，實際睇唔到；掣仲撳得，但玩家唔知自己開緊邊張通告。

## 根源（v128 回歸）
v128（commit `d8c4560`，A 批 N18）將 `.cn-issuer30v2` 由 `height:240px` 改成
`height:auto`。當時前提係錯嘅——NOTES 寫「bust 圖 240×312，舊容器會裁走 46px」，
但實情 11 張老闆圖全部係**全身圖**（480×1424 起，比例 ~3.0；240×312 係 v109
bust 縮圖嘅尺寸，唔係老闆 hero 檔）。`height:auto` 之後全身圖渲染成 609px 高
（方樂怡；沈卓衡 689px），modal 上限 `min(88dvh,760px)`，真機上 dvh 細咗
（Safari 工具列）＋掣列 `env(safe-area-inset-bottom)` 加 ~34px，sheet frame
（`flex:1 1 0%`、`min-height:0`、`overflow:hidden`）吸晒所有擠壓，縮到 16–24px，
標題 h2 俾 frame 剪走下半截，body 捲軸得返 12px，撳極都出唔返標題。
Headless 測試捉唔到（dvh＝全高、safe-area＝0）。

## 修法（最小改動，還原 v116 批准嘅樣）
- `index.html` L5075：`#mask.casting-sheet-on #modal-inner .cn-issuer30v2`
  `height:auto` → **`height:240px`**（`overflow:hidden` 本來就有，圖由底裁走，
  頭＋胸口留低＝v116「老闆胸口以上企卡頂」原設計）。名牌
  `.cn-issuer-cap30v2` 嘅 `bottom:106px` 唔郁（本來就係為 240px 高設計）。
- 數字驗算：hero footprint 240−100（負 margin）＝140px；最細情況
  （modal 88dvh≈616＋掣列連 safe-area ~123）frame 都有 616−140−123＝353px，
  標題＋摘要一定有位。唔用 dvh 相對值。
- `tests/test_ui128a4_static.py` N18 斷言 resync：v128 嗰句 `height:auto`
  係釘死咗錯誤前提，改返斷言 `height:240px`，註解寫明原因。

## 測試
- 新靜態測試 `tests/test_ui132_s30hero_static.py`（7 項）：工作副本全 PASS；
  對 pristine（`4f4b96a`）乾淨 FAIL（2 項）——反證成立。
- 新 drive 回歸 `qa132/drive132.py`（經 UI：新遊戲 slot 3 → 全部地點 →
  金鐘創意／星河電視台 → 撳通告行；斷言 h2 完全可見 clippedByFrame ≤ 0
  ＋sheet body ≥120px）：
  - 工作副本：430×700 方樂怡 heroH 240／clip −307／bodyH 277 PASS；
    430×932 對照 heroH 240／clip −451／bodyH 421 PASS；
    390×700 沈卓衡 heroH 240／clip −307／bodyH 277 PASS；0 error／0 404。
  - Pristine 反證：430×700 heroH 609／clip **+20**／bodyH 12 FAIL；
    390×700 heroH 689／clip **+20**／bodyH 12 FAIL；
    430×932 clip −82 但 bodyH 52 FAIL——同用戶截圖一模一樣。
  - 前後對照截圖：`qa132/shots/132_430x700_adm.png`（修復後：胸口以上
    crop、名牌唔遮面、標題＋要求格＋片酬＋檔期齊晒）；
    `qa132/drive132_pristine.json` 存反證數字。
- 全套測試（新鮮 pristine worktree `4f4b96a` 做 baseline）：
  baseline **188 PASS／12 FAIL**；工作副本 **189 PASS／12 FAIL**，
  FAIL 列表完全一致——零回歸（+1＝新靜態測試）。

## 紅線
SAVE key、softRev s107、產品 `?v=` v20a10 全部唔郁；`content/` 零改動。

## 落地
分支 `v20a132`（基底 main `4f4b96a`）→ 常駐 clone squash merge 入 main →
push main（經 deploy key，唔開 PR）。線上核實見下文。

## 線上核實（push 後約 2 分鐘，curl）
- main commit：`d0edc18`（squash，分支 `v20a132` `1cfe9ee`）
- 線上 index.html：**5,178,992 bytes、sha256 `ca76094705f630fda0c537f1891559274707d1a7e8d31beb6f3f7d48d1736778`**，
  同 repo 完全一致。唔使重觸發。
