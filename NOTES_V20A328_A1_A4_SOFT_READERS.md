# NOTES_V20A328 — A1＋A4 軟讀者／閘變體（v328）

- Base：main `fdde0ca`（v327，通告庫 322 張，index.html 47,244 行）。
- 內容：A1 `flag_choi_spin_repaid` 加軟條件讀者（v322 模式）＋ A4 N-5 Beat 4 暖版交心「加多一重閘」（駱＋齊兩腿；魏腿除外，見 triage B2）。
- 偵察 brief：`~/workspace/linji-brief-small-followups-triage.md` A1／A4 節。

## 一、改動（index.html 淨 ＋18 行：47,244 → 47,262）

### A1（`choi299PrepareNode`，舊 L27706 起）
- 舊 L27705 註解行 1→2（＋1）：加 v20a328 A1 說明＋「只處理 R_choi_push1／R_choi_push2」。
- 舊 L27708 `if(!node || node.id!=="R_choi_push1") return null;` 改做 `if(!node) return null;`（同行，0 行）。
- 舊 L27710 之後插入 push2 分支 17 行：`node.id==="R_choi_push2"` 嗰陣，`enc87StoryFlag("flag_choi_spin_repaid")` 在位先回 copy——beats[0] 首句插「你上次肯等我查證，今次我唔會再問包裝版。」（玩家面廣東話），其餘 beats／choices 原樣；無旗回 null。淺拷貝（beats 逐 beat 拷 lines、choices 逐個拷 effects），原節點唔郁。`R_choi_crisis` 唔加（二揀一，揀咗 push2）。
- 唔郁任何閘／數值：push2-a rel＋2 照舊；spin 全佳路線 rel 仍係 6，剛好夠 COMMIT48_REL_MIN 6。
- 呼叫點：StoryPlay.start L10700 對每個節點都 call `choi299PrepareNode(node)`，push2 行得到。

### A4（暖版 heart 閘，舊 L40219 → 新 L40237，同行改寫，0 行）
- 加兩個 conjunct：
  - 駱：`!(starId==="lok_gasing" && (S.flags||{}).lok_first_mock && !(st.beatsDone||{}).lok_help)`（先做埋試和音）。
  - 齊：`!(starId==="chai_zanhoi" && (S.flags||{}).chai_first_bluff && !(st.beatsDone||{}).chai_choice)`（先做埋 Beat 3 勸停）。
- 遲啲開，唔係永久鎖死；無旗玩家唔受影響。冷版 heart（新 L40232）／提攜閘（`lok_patron`／`chai_patron` when）唔郁。
- 旗本身已寫入（DLG `flags` 欄：`lok_first_mock` L37201、`chai_first_bluff` L37561）；`st.beatsDone` 係按 beat id 計嘅物件（L39521／L39850 寫法）。

## 二、測試

### 新／擴充（逐個直接跑全部 PASS）
- `tests/test_r299_three_flags.js` 擴充 C7（9 項）：無旗 → push2 null；有旗 → 回 copy、beats 仍係 6 段、beats[0] 首句回call（肯等我查證／唔會再問包裝版）、原 3 句照在位（加句唔係換句）、choices 數值唔郁（push2-a rel＋2）、原節點唔郁、`S.story.flags` 有旗同效、只有 `choi_spin`（無 repaid 旗）→ null。
- `tests/test_r328_heart_gate_a4.js` 新檔（20 項，仿 `test_r308_lok_heart_cover.js` harness 抽 `enc79BuildScript` 實跑）：
  - (A) 駱：mock 未做 lok_help → heart 0 段；做埋 → 13 段；無旗未做 → 13 段；句數一致。
  - (B) 齊：bluff 未做 chai_choice → heart 0 段；做埋 → 14 段；無旗未做 → 14 段；句數一致。
  - (C) 冷版 heart 唔郁：`chai_loose_fear` → 冷版 7 段＋暖版 0 段；`lok_loose_row` 同理。
  - (D) 提攜閘唔郁：lok_patron T4＋calm_truth → 開（加 mock 旗照開）、無 calm_truth → 唔開；chai_patron 同理（bluff 旗唔影響提攜）。
  - (E) 靜態：暖版閘行有齊兩個新條件。
- **測試教訓（B 組初版 2 FAIL，唔係 code 錯）**：`chai_choice` 嘅 when 係 1991–1992＋T2——year 1992 嗰陣，刪咗 beatsDone 會令嗰 beat 本身開返，build 會播 beat 而唔係 heart（唔係閘擋住）。「未做嗰步」嗰兩組改用 year 1990，等 beat 因年份閂埋，淨返暖版閘決定播唔播 heart。駱嗰邊無呢個問題（`lok_help` when 要 vocal≥35，sandbox 無 vocal → beat 閂埋）。

### Resync（`qa328/resync328.py`，difflib 核實純漂移）
- difflib 對位：淨 ＋18，只得 4 處非 equal hunk（註解 1→2、if 同行改寫、插入 push2 分支 17 行、暖版閘同行改寫）。
- 5 檔測試 resync：gift185（總行數）、tang171／tang173（總行數＋openLoc DEF 42453→42471＋guard 42459→42477＋`lines[42452]`→`lines[42470]`）、rom176（4 釘行各 ＋18：40685→40703、41035→41053、42338→42356、42494→42512；ok() 名 L55647 等係歷史名，唔郁）、travel114（COUNT 5 處＋FREE 26 處＋DEF 42453→42471＋WRAPPER 29065→29083；＜27705 者唔郁）。
- **resync 教訓**：初版漏咗 tang171／tang173 嘅 `== 47244` 值（名改咗，值未改），兩檔各剩 1 FAIL；已補返（script 亦已修正，`== 47244 → == 47262` 各 1 處）。以後 resync 逐對核對「名＋值」一齊改。

### 全套 suite
- 第一跑 381／14：多出 5 項全部係 ＋18 行漂移（gift185／rom176／tang171／tang173／travel114），resync 後逐個直接跑全部 PASS。
- 第二跑（已 commit 樹）：**TOTAL PASS 386 FAIL 9**＝基線（385＋新檔 r328 1 項）＋9 項已知 pre-existing FAIL（flash51／slot50／soft_tip_111_restore／start53／weave43_static／weave44_static／weave49_static／wf5_87／wrap38），零回歸。

## 三、驗收
- `grep -n "flag_choi_spin_repaid" index.html`：授出 1 處（新 L27751）＋讀者 1 處（新 L27713）＋註解 2 處。
- A4 新條件 `lok_first_mock && !(st.beatsDone||{}).lok_help`／`chai_first_bluff && !(st.beatsDone||{}).chai_choice` 各 1 命中（暖版閘行）。
- 冷版 heart（新 L40232）、提攜 when、SAVE key／softRev／`?v=` 原封不動。
- 總行數 47,262；通告庫仍係 322 張。

## 四、殘留／跟進（唔開票，記低）
- Triage B1–B4 留待設計拍板（§10 項 10 閘門出入、魏腿 `gig_br89_stunt_ngai` 已消失、D-13 修訂、E2 守衛門檻）。
- 下一票按 triage 建議：v329 A2（`promptAudition` 死函數刪除）、v330 A3（E2 普查 tier 名修正，measure-first）、v331 A5（SPEC docs 清理）、v332 攻略 A6（a)–(f)，須 parent 授權後行 repair 流程。

## 五、合併＋部署（待填）
