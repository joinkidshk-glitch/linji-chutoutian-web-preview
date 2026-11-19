# NOTES_V20A333_NGAI_WALK_PAST_STUNT_GATE.md — v333 B2 魏腿修正版選項 (i)

## 一、問題（已核實係真）

- `gig_br89_stunt_ngai` 全 repo 0 命中（舊庫情報通告，v229 換庫嗰陣消失）。
- `ngai_walk_past` 有寫無讀：唯一寫入係 Beat 2 選擇 C DLG `flags: ["ngai_walk_past"]`
  （index.html L36751，v331 base），全檔 0 讀者。
- Walk_past 玩家 Beat 3（`ngai_repay`）永遠唔開：餐飯債權唯一授出點係 Beat 2 選擇 A、
  `ngai_tea` 唯一寫入點係 Beat 2 選擇 B，beats 一次性——呢個係已拍板保留嘅 G-NGAI-5
  「錯過成段」，唔係 bug，唔郁。
- 但草稿設計嘅第二重後果完全失落：Beat 2 後果 C 寫明「Beat 4 交心閘加多一重（要先做埋
  `gig_br89_stunt_ngai` 替身缺位先開）」，暖版交心閘完全唔讀 `ngai_walk_past`——
  walk_past 玩家儲夠 T3 就播暖版交心，零額外步驟。

## 二、完美做法（修正版選項 i；否決咗嘅做法見 §五）

將「替身缺位」由「某一張通告」改做「任何一張動作替身通告」：

- `roleLabel === "動作替身"` 嘅通告全庫 17 張，橫跨 1990 春–1992 秋。低門檻選擇：
  film_114（1991 秋，演技 18＝開局值）、film_201（1992 春，淨體能 70）。
  任何正常玩家喺交心之前（T3＋1992 年）都有最少三個季度可以做到，**無死位**。
- `gig_1991_film_206` 本身係 17 張之一（cast 仲有魏詠男做女主角，敘事上最啱），
  所以修正版包埋 NOTES_V20A278 L54 嗰個原意，唔係推翻佢。
- 機制已經喺度，唔使新嘢：殺青通用寫 `S.flags["done_"+gigId]`（L21315），
  `roleLabel` 已經係現成嘅類別欄，`done_` 已經係現成嘅追蹤。

## 三、改動（index.html 淨 +7 行，47,249 → 47,256）

1. **新 helper（舊 L39872 之後，`enc79BeatOpen` 之後）**，7 行：
   `enc79HasDoneStuntDouble()`——掃 `GIGS`，任何一張 `roleLabel === "動作替身"`
   且 `S.flags["done_"+g.id] > 0` 就返 true；try/catch 兜底 false。
2. **暖版 heart 閘（舊 L40237 → 新 L40244）加一個軟條件**，模式同 v328 A4 一樣：
   `&& !(starId==="ngai_wingnaam" && (S.flags||{}).ngai_walk_past && !enc79HasDoneStuntDouble())`
   ——walk_past 玩家未做過替身工，暖版交心唔開；做過就開；非 walk_past 玩家完全唔受影響。
   註解加咗 v20a333 B2 一句（刻意唔寫旗名全寫，免得 `ngai_walk_past` 命中數由 2 變 3，
   驗收計數先至有意義）。

**絕對唔郁**：`ngai_repay` 閘（新 L41780）、冷版 heart（新 L40239）、`gig_1991_film_206`
本身（tier／req／年份）、`done_` 寫入（L21315）、`enc79PickBeat` 次序、
`ngai_rain_stand`／`ngai_rain_hold_back`、SAVE key／softRev／`?v=`。

## 四、測試

- 新檔 `tests/test_r333_ngai_stunt_gate.js`，20 項，**ALL PASS**：
  - (A) walk_past＋無替身殺青 → 暖版 heart 唔開（0 句）；做過 film_206 → 開（13 句）；
    做過 film_201（淨體能）→ 開（13 句，證明唔係淨認 film_206）；
    只做過非替身通告 tv_205 群演 → 唔開；無 walk_past 旗 → 照開（13 句，唔受影響）；
    walk_past 做埋嗰陣 heart 句數同無旗一致（13＝13）。
  - (B) 冷版 heart 閘唔郁：`ngai_rain_hold_back` → 冷版照播（7 句）、暖版唔播；
    壞旗＋walk_past＋做過替身 → 照播冷版（唔係暖版）。
  - (C) 提攜閘唔郁：`ngai_patron` T4 → 開；＋walk_past → 照開；＋walk_past＋替身 → 照開；T3 → 唔開。
  - (D) helper 單元：無 done_ 旗 → false；只做過非替身通告 → false；做過 film_114 → true。
  - (E) 靜態：暖版閘有新條件；`ngai_walk_past` 授出 1 處＋讀者 1 處（共 2 命中）；
    `gig_br89_stunt_ngai` 全檔 0 命中；helper 定義在位。
  - 寫測試嗰陣捉到一個自家錯誤：`asVar` 漏咗 `=` 前後空格，`const` 留喺 eval 作用域出唔返嚟
    （`ENC79_BEATS is not defined`）——已跟返 r328 寫法修正。
- 逐個直接跑受影響檔全部 PASS：r333、r328（A4 兩腿唔受影響）、r304（冷版）、sideline278。
- 全套 suite：**TOTAL PASS 387 FAIL 9**＝v331 基線 386／9＋新檔 1 項；
  9 項 FAIL 同基線逐項一致（flash51／slot50／soft_tip_111_restore／start53／
  weave43_static／weave44_static／weave49_static／wf5_87／wrap38），零回歸。

## 五、resync（qa333/resync333.py）

helper 插入令其後錨點一律 +7（舊 L39872 之後）。difflib 對位核實純漂移：
淨 +7，只得 2 處非 equal hunk——insert helper 7 行＋gate 行 replace 1 行。
5 檔測試 resync：

- gift185：總行數鏈＋v333 +7（47249→47256）。
- tang171／tang173：總行數鏈＋v333 +7；openLoc DEF 42471→42478（label＋鏈＋
  `len(lines) >= 42478`＋`lines[42477]`——頭一版漏咗 index／guard，逐個跑先捉到，
  已補返入 resync 腳本）。
- rom176：4 個釘行各 +7（40703→40710、41053→41060、42356→42363、42512→42519；
  6321／14772 喺插入點之前唔郁；L55647 等名唔郁）。
- travel114：COUNT 4 處＋FREE 24 處＋DEF 42471→42478 各 +7（≤39871 者唔郁）；
  逐行核實新錨點係 openLoc( 呼叫點（FREE 帶旗、COUNT 唔帶旗）。

## 六、否決咗嘅做法（記錄在案）

- **選項 (ii) 為 walk_past 寫冷版 repay**：違反已拍板 G-NGAI-5（PLAN.md L107＋
  DECISIONS-2026-11-15 附錄 B 明文「魏 Beat 2 趕時間走→Beat 3 唔開」係四處
  「錯過成段」之一，用戶拍板保留）。買茶嗰邊已經有冷版；walk_past「唔開」本身就係設計。
- **NOTES_V20A278 L54 字面設計（淨認 film_206）**：三處錯——(1) `enc83GigDone` 唔存在，
  真機制係通用 `done_` 旗；(2) film_206 係 1991 年夏一季限定，1991 年秋／冬或 1992 年
  先第一次撞到魏詠男嘅玩家永遠做唔到，交心要 T3＋1992 年嗰陣已經落咗板一年，永久鎖死，
  違反 PLAN §11「遲啲開」原則；(3) 佢唔係「臨記通告」嗰隻：tier 中級，要試鏡，
  req 演技 55／體能 75，唔練演技嘅玩家同樣永久鎖死。雙重死位。
- **選項 (iii) 接受現狀**：次選後備。損失係真但唔大（walk_past 已經有實質代價），
  但既然有無死位嘅乾淨做法，唔應該白白放棄草稿設計嘅第二重後果。

## 七、驗收

1. `grep -n "ngai_walk_past" index.html` ＝ 授出 1 處（L36751）＋讀者 1 處（新 L40244）。
2. `grep -n "enc79HasDoneStuntDouble" index.html` ＝ 定義＋呼叫。
3. `gig_br89_stunt_ngai` 全 repo 仍然 0 命中（唔復活舊 id）。
4. 全套 suite 387／9，9 項 FAIL 同基線逐項一致，零回歸。
5. `ngai_repay` 閘、冷版 heart、film_206、SAVE key／softRev／`?v=` 全部原封不動。
6. 常駐 clone 跑完 suite 後 `git checkout -- qa296/derive296.json` 還原（衍生檔唔入版）。

## 八、落地

- 內容 commit `0ec35f0` → 常駐 clone squash merge → **main `2a258d3`**，已 push；
  `git ls-remote` 核實一致。
- Pages 核實：curl 比對 byte-identical，index.html md5
  `93256439bf124ca7bf7912589f05b6dd`／4,700,994 bytes；
  `tests/test_r333_ngai_stunt_gate.js` HTTP 200。
- 工作副本已刪；常駐 clone tracked 乾淨，`qa296/derive296.json` 已還原（衍生檔唔入版）。
