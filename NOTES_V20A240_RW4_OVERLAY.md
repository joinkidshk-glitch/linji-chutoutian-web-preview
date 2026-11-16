# NOTES_V20A240 — RW-4 覆寫層：頒獎＋報紙＋殺青 overlay 逐句重寫

- Base：main `24fc55d`（v239）。分支 `v240`（工作副本 `linji-work240`；工人副本 `-a`／`-b`）。
- 落地：squash merge → main，push main。工作報告 `~/workspace/linji-language-sample/RW4B_OVERLAY_WORKLOG.md`（360 行；改寫清單抄自兩份工人草稿，統籌已對住 patch 逐條核實）。

## 改咗乜

RW-4（v239）改咗報紙＋頒獎 stub 源頭，但 `index.html` 入面嘅覆寫層遮住咗大半——玩家實際見到嘅新頒獎句只得 4 處。本票將覆寫層本身逐句重寫（輕口語對白＋香港式書面語旁白；報紙正式書面語，全名「陳偉翔」；典禮敘述用「阿偉」）：

| 組 | 改寫 |
|---|---|
| A：`AWARDS188_CATEGORIES`（15 catId） | 類別行 45 處（win／lose／gallery；label 獎項名唔郁） |
| A：`buildAwardResultPack` fallback 字面 | 4 處（win／gallery／lose／inviteDek；`頒獎夜請柬`／`頒獎夜`本身已係書面語，留低） |
| B：`VENUE99_*` | 14 處（INVITE_DEK 3＋PRESS_DEK 2＋NEWS_LINE 3＋NP_DEK 6；「金禧大酒店大禮堂」全部保留；4 處「聲望」改寫成畫面） |
| B：`AWARDS188_NP_WIN` | 10 處（headline 5＋dek 5；clipLabel 8 全部已係「・得獎」新名，留低） |
| B：`PSR_EXTRA_TEMPLATES_35` | 38 處（press 13＋news 7＋streetFans 10＋metrics 8；引號內街坊原話保持輕口語，G5 例外） |
| **合計** | **111 處** |

統籌合併層微調：film／ad inviteDek「一張旁聽席位的信」→「一張席位信」（v207 N4 已拍板，典禮請柬唔寫旁聽／入圍席位信；語言重寫唔推翻舊設計決定）。

## Live 新句數目（關鍵驗收）

- 頒獎類 live 新句：RW-4 後 4 處 → **本票後 85 處**（類別行 45＋VENUE99 15＋NP_WIN 21＋RW-4 stub 句 4）。
- 殺青池 live 新句：PSR 39 處新 live，連 RW-4 殺青 34 處＝73 處。
- `buildAwardResultPack` fallback 4 處屬 dormant（stub 行缺失先見到）。
- 仲有舊文遮住嘅地方（全部 dormant，玩家見唔到）：`TEXTFIX55_EXACT` NP214 死映射 value 1 條（key 已對唔返源頭，留 TEXTFIX55 收尾票；`test_newspaper214_award_static.py` T01 仲釘死呢組 value）；stub 36 處頒獎類別行係死 fallback（AWARDS188-first，永遠唔會被查詢）。

## 測試錨點更新（只改期望值、唔刪斷言）

- `test_awards188_logic.js` L203 正則改釘新 film lead_m winLine。
- `test_awards192_logic.js`／`test_awards192_static.py`：守衛＋C1 exact-match＋「還有」檢查。**「還有」ban 檢查改做精確清單**：v192 ban「還有」係粵語化要求，語言規則（2026-11-15 旁白書面語）高於舊測試；書面語「還有」係啱嘅，新檢查釘死「還有」只准出現喺 3 條 loseLine（singer_m／film lead_m／tv lead_m，跟 RW-4 stub 平行句）。
- 其餘 6 檔：`test_awards200_static.py` WIN8（5 款改全名）、`test_awards207_static.py` C4（三條 inviteDek 前綴）、`test_verify37_static.py` item2c、`test_wrap38_logic.js` b2／b3／b6（兩個 headline 常數）、`test_newspaper214_award_static.py` T03／T04。

## 核實（統籌獨立做，唔係齋信工人）

- `vm.Script` 編譯 2 個 inline script block 通過。
- 相關測試 8 檔逐個覆驗全部 PASS。
- 全套 suite：**314／10**，FAIL 名單同基線逐項一致（flash51／rumor49／slot50／soft_tip_111_restore／start53／weave43／weave44／weave49／wf5_87／wrap38）。
- TEXTFIX55：EXACT 134、NOTE_EXACT 9——同 v239 一致，本票無郁。
- 覆寫層 CJK 字串總數 196，改後殘留廣東話標記（咗／嘅／仲／嗰／喺／唔，引號內街坊原話除外）0 處。
- Pages 逐 byte 核實（見統籌回報）。

## 未做

- Live 實機抽檢押後（瀏覽器自 2026-11-15 起已死）：頒獎報紙畫面＋殺青反響卡實機抽檢。
- 下一批 RW-5：事件／NPC／教學／禮物／UI 約 1,630 句＋TEXTFIX57「點擊→撳」裁定＋DS filter 定位；NOTE_EXACT 剩 9 條；「采兒」→「周采兒」決定；WF4／WF2／LAN 內嵌覆寫表刪除決定（類比 v234）。
