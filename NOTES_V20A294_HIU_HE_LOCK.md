# v20a294 — Q7：曉晴 HE 鎖死（hiu_family_go）

## 拍板（用戶 2026-11-18）
揀咗「勸佢跟屋企走」（`hiu_family_go`）就冇 HE——佢走咗，冇得追。鎖定後唔可以轉，BE 唔解鎖（跟六女角排他鎖規矩）。

## 背景：矛盾（v266 NOTES 已寫明係已知留低第 10 項）
- 危機 beat（`R_hiu_crisis`，`enc158PrepareNode`）`hiu_family_go` 版話佢「差啲買咗機票，不過臨上機嗰陣返轉頭喇」——話佢留低。
- 結局 beat（`R_hiu_ending`）`hiu_family_go` 版成組換成啟德機場送機——話佢走咗，冇再回頭。
- 兩段直接矛盾；HE 選擇（`C_hiu_ending_he`）當時冇閘讀 `hiu_family_go`，揀得 HE。

## 改動（index.html 淨 +17 行；base main f50b128）
1. **HE 鎖死，pack ending（`rom159PrepareNode`，L25909 起）**：`who==="hiu"` 且有 `hiu_family_go` 嗰陣，HE 選擇換成「差一步」變體（id 照舊 `C_hiu_ending_he`，label「坦白心意：佢已經跟屋企走咗」，effects 只寫 `flag_hiu_be`，stats 清空，唔寫 `flag_hiu_he`／`flag_hiu_commit`）。跟 locked／contra98 先例（HE 換成 BE 變體，唔係刪選擇）；family_go 比鎖另一位更貼呢條線，行先。無旗／未鎖嗰陣行為唔變（返 null）。
2. **HE 鎖死，CMT offer（`commit48Available`，L25061 起）**：`id==="CMT_hiu_commit"` 且有 `hiu_family_go` 就唔出 offer。防禦性閘（family_go 路 rel 理論最高 ~5，本身已經到唔到 rel 6 門檻；呢閘係明文鎖死，唔靠數值）。
3. **危機對白改寫（`enc158PrepareNode`，L27358 起）**：`hiu_family_go` 開場由「差啲買咗機票，臨上機返轉頭，呢個角色係我留低嘅理由」改做「聽你話，買咗機票喇。不過走之前，我想試埋呢個角色——呢個係我喺呢行最後一個機會。你話，我係咪傻？明知就嚟走，仲要嚟爭呢個角色。」——機票買咗、走之前試埋最後一個機會，之後試鏡競爭嗰幾段（公平競爭→助導叫入去）照接；同結局啟德送機一致（危機話要走，結局話行入閘口走咗）。

## 其他 `hiu_family_go` 讀取點覆核（全 repo grep，唔使改）
- `C_hiu_push1_c` 寫旗（L7256）／`flags_written`（L7258）：寫入點，正確。
- `R_hiu_crisis` `openConditionsAny`（L7358）：crisis 照開（改寫後嘅「最後機會」版就係為呢個節點而寫）。
- `R_hiu_ending` 走收尾成組換（L27365 起）：啟德送機，正確，唔郁。
- `CONTRA98_WHEN_FIX` 日期表（L14683）：只係 when／era 標籤，唔係旗讀取。
- 排他鎖（`rom159LockedWho`，rel 5）：唔郁——family_go 玩家行到 rel 5 鎖曉晴，結局行 BE，符合「鎖定後唔可以轉，BE 唔解鎖」。

## 刻意唔做
- 唔喺 `enc158PrepareNode` 郁 choices：v266 測試明文斷言 enc158 唔郁 choices（beat 變體層唔做閘嘅既有設計）；HE 閘放 `rom159PrepareNode`（本身就係 HE 選擇把關層）。
- 唔改 `content/story_detail_romance_vera_hiu_choi.json`：全部經 inline 覆寫層／prepare-hook 注入（跟 v266 做法）。
- 唔改排他鎖語義、唔改 `COMMIT48_REL_MIN`、SAVE key／softRev／`?v=` 唔郁。

## 測試
- 新 `tests/test_r294_hiu_he_lock.js`：24 項全過——靜態（三處 v294 標記、「返轉頭喇」已無）、危機改寫（買咗機票／唔講返轉頭／最後一個機會／競爭段照接／choices 唔郁）、危機 vs 結局一致（危機唔話留低、結局話走咗）、ending HE 換選擇（只寫 `flag_hiu_be`、BE 選擇唔郁、beats 唔郁、無旗返 null、family_go＋鎖采兒嗰陣 family_go 行先）、CMT 閘（無旗照開／有旗唔開／只限曉晴，采兒照開）。
- 舊測試覆驗：`test_hiu266_logic.js` ALL PASS、`test_rom159_logic.js` TOTAL PASS 136 FAIL 0。
- 全套 suite：`bash qa131/run_suite.sh` → **TOTAL PASS 358 FAIL 9**（`~/workspace/suite294b.txt`）。9 個 FAIL 全部係已知 pre-existing（flash51／slot50／soft_tip_111_restore／start53／weave43_static／weave44_static／weave49_static／wf5_87／wrap38）；基線 357／9 ＋新測試 1 個 PASS。
- 釘行 resync（`qa294/resync294.py`，留喺 repo）：第一輪 suite 352／15，6 檔新 FAIL 全部係行號釘漂移（index.html ＋17 行所致）；逐行對 pristine main 核實純漂移後單次掃描 dict 查表 resync——`test_rom159_static.py`（25117→25119、25951→25967、25866→25868、全佳 25145→25147）、`test_rom176_static.py`（40173→40190、40531→40548、41844→41861、42000→42017）、`test_gift185_static.py`（總行數 46717→46734）、`test_tang171_static.py`／`test_tang173_static.py`（總行數 46717→46734、openLoc DEF 41959→41976、guard 41965→41982、index 41958→41975）、`test_travel114_static.py`（COUNT 12＋FREE 40＋DEF＋WRAPPER 共 54 處錨點按段 shift：＜25061 唔郁、25061–25906 ＋2、25907–27341 ＋16、≥27342 ＋17；DEF 41959→41976、WRAPPER 28695→28712）。resync 後 6 檔逐個覆驗全過，再跑全套先返到 358／9。
