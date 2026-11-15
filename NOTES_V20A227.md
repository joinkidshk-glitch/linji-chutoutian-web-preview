# NOTES_V20A227 — v206 C1 修復：WF4 day24 信件房 banner 裁切位

- 基底：main `7e05a4d`（v226 書面語 522 池外旁白）；分支 `v20a227`；工作副本 `linji-work227`。
- 問題（`~/workspace/linji-design-review-v206/REVIEW.md` C1）：day24 隨機事件「電視台那封沒有署名的信」（`wf4_ev_day24`），場景圖 `bg_loc_tvb_kowloon.jpg` 本身確實有成疊信件＋佈告板，但 WF4 banner（`.wf4-scene105`，高 150px，`background-size:cover`，`background-position:center`）只裁到電視牆＋窗，第一眼只讀到「電視台」，唔讀到「信件房」。文案講緊「執信嗰陣搵到封冇名信」，圖文關聯得一半。
- 用戶拍板（2026-11-15 19:04）：調 banner 裁切位／focal 位，令枱面信件入鏡；唔改遮腿設計，唔出新圖。

## §1 改動

- `index.html`：`scenePos146` ternary 加 kowloon 分支——`bg_loc_tvb_kowloon.jpg` 用 `background-position:center 80%`（淨 +2 行：註解 1 行→3 行，chain 原地換值）。
- 量度（系統 python3＋PIL，原圖 720×1280 直倒；模擬手機窗口 366×150）：信件疊 y 75.5–82%、打字機 y 61.8–69.8%、佈告板 y 52.8–70.8%、電視牆 y 16.8–55.6%。現行 center 50% 帶 y 38.5–61.5%（電視牆＋窗，信件零曝光）；**新 80% 帶 y 61.6–84.6%（打字機＋信件疊＋佈告板底入晒鏡）**，已用 PIL crop 圖目視確認。
- 範圍：WF4 圖映射入面只有 day24 用呢張圖；地點圖映射（`tvb_kowloon`）同 StoryPlay 漸變後備唔行 WF4 banner，唔受影響。改動只影響 day24 WF4 banner。
- kwan151／tang152 唔受影響：零 CSS 改動（淨係 JS 一行＋註解）。

## §2 測試

- 新增 `tests/test_wf4_227_c1_static.py`（9 斷言：SAVE key／softRev／`?v=` 不變、day24 映射唔郁、80% 分流、80% 只出現一次、v20a227 C1 註解在場、四圖同一 ternary、其餘三圖仲喺度、共用 center 唔郁、舞台 sp-bg-layer 唔郁）。
- `tests/test_taxi148_static.py` exact-chain 斷言已更新（加 kowloon 分支）。
- Resync：`qa227/resync227.py`——index.html 淨 +2 行（註解 1 行→3 行，插入點舊 L41729；chain 原地換值行數不變），difflib 對位核實純漂移（舊行 ≤41729 不變、≥41730 者 +2，例外 0 項；56 錨點逐字相同：travel114 FREE 33＋COUNT 12＋DEF／WRAPPER、rom176 7、tang171／173 DEF 各 1；travel114 語義核實 FREE 全部帶旗、COUNT 全部冇旗）。單次掃描 dict 查表一次過改（撞值對 56284→56286／56286→56288 核實無重複、無丟失）。更新 5 檔釘行（rom176 4 處、travel114 COUNT／FREE／DEF／WRAPPER、gift185／tang171／tang173 總行數＋DEF 公式，全部 +2 並加 v227 項；總行數 63132→63134、DEF 57527→57529、WRAPPER 45641→45643）。

## §3 驗證

- `node --check` PASS（兩個 inline script 塊）。
- 相關測試逐個全過（13 個）：test_wf4_227_c1_static、test_taxi148_static、test_mask146_static、test_ui105_static、test_ui134_wf4scene_static、test_wf4_203_static、test_wf4_203_logic、test_wf4dlg108_logic、test_rom176_static、test_travel114_static、test_gift185_static、test_tang171_static、test_tang173_static。
- Suite B：**312／13，FAIL 清單同基線 A（311／13）一模一樣（13 項穩定 FAIL）——零回歸**。+1 PASS 係新增嘅 test_wf4_227_c1_static。
- Live drive：未跑——瀏覽器自 2026-11-15 08:48 起已死（Chromium SIGTRAP exit 133），等恢復後補跑 day24 banner 信件入鏡實駕覆驗。
