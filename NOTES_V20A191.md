# NOTES v20a191 — C6F 幕號修復（A＋B）

- 基底：main `dcf1b72`（v187；遊戲 `fe09b67`，線上 5,310,960 bytes sha `c02b36ec…`）
- 分支：`v20a191`（工作副本 `~/workspace/linji-work191/`）
- 拍板：用戶 2026-11-13 19:40「A＋B 一齊做」
- 調查報告：`~/workspace/linji-work-c6f-inv/INVESTIGATION.md`

## 1. 問題

用戶以為第 20 幕無故完成，其實 C6F 真係播過——第 15 週返地圖嗰陣 v165 強制播自動彈出
C6F，但場景從來唔講自己係「第 20 幕」（幕內標題只係「角落嗰張枱」），進度頁標題係另一套
（「片場跟班」），玩家唔認得。根因係「強制播＋編號」溝通缺口，唔係數據 bug。
舊排法 `order71` 將 C6F 排第 20（`[["C1",1],…["C17",17],["C18",18],["C19",19],["C6F",20]]`），
C18／C19 同樣係插入幕，一併誤導。

## 2. 標籤方案（A）

新增共用函數 `storyActLabel(id)`（index.html 約 L44064，`prog71Title` 前面，全域）——
進度頁、場景頂、地圖下一幕提示三處同一來源，唔准兩邊各寫一套字：

| id | 標籤 | 理由 |
|----|------|------|
| C1–C17 | 第 N 幕 | 主幹順序號 |
| C6 | 第 6 幕・電視線 | 同一幕路線雙生，對稱後綴 |
| C6F | 第 6 幕・電影線 | 跟住 C6，唔再叫第 20 幕 |
| C18 | 番外・1990 冬 | 時間錨番外，跟 `CALIB60_NODE_WINDOWS` whenLabel |
| C19 | 番外・1991 春 | 同上 |
| 非主線（巧遇／隨機事件／支線） | `""` | 唔出幕號行 |

另有 `storyActIsInsert(id)`（只認 C6F／C18／C19）。

- `prog71Rows` 嘅 `order71` 顯示次序改跟 `ORDER165`（播次序）：C1–C5、C6、[C6F、]C18、[C19、]C7–C17。
  C6F 跟住 C6；C18／C19 喺 C6 同 C7 之間（1990 冬／1991 春時序上啱啱喺 C6 1990 春同 C7 1991 夏之間）。
- **內部 n 保留唔郁**（C6F=20、C18=18、C19=19），供 far-merge（v105）同逐項揭曉（v80／v153，
  `lastDetailN71` 閾值）用，行為同 v153 一模一樣（實際只有 C18 可經呢條路出逐項，
  C19／C6F 永遠唔出——同 v153 行為一致，唔係新 bug）。
- 遠幕合併 guard：鎖住又未到逐項嘅插入幕唔出獨立行、亦唔觸發合併行（維持 v153 舊行為：
  插入幕未開嗰陣喺進度頁唔見，開放／完成先出現；合併行只由主幹遠幕觸發，印喺第一個主幹遠幕位置——
  插入幕而家排喺 C6 同 C7 之間，唔加 guard 會令合併行提早印喺逐項行上面）。
  寫法：`if(storyActIsInsert(r.id)) return;`（放喺 detailSet 分支之後、far-merge block 之前）。
- 前置句（`prog71GateItems`／`prog71StubItems`）改行共用幕號：
  `"先完成"+(storyActLabel(d) || ("第 "+…+" 幕"))+"〈"+prog71Title(d)+"〉"`。
  關鍵例：C19 前置 C18 印「先完成番外・1990 冬〈上岸路〉」，唔再印「先完成第 18 幕」。
- 四行模板改 `r.label || ("第 "+r.n+" 幕")`（`rows.push` 加 `label:storyActLabel(id)`）。

### v153 B3 原意處理

v153 B3 幕次序 1–20 嘅原意：C18／C19／C6F 排喺 C17 之後，係為咗防 C17＋C18 齊開嗰陣撳錯
「播呢幕」掣。v165 已拎走「播呢幕」掣，強制播冇得逐行撳，次序再唔會造成誤撳，
所以原意已唔使守。已寫入 code 註解（order71 附近）＋本 NOTES。

### 範圍延伸：地圖下一幕提示

`storyMainProgressLine`（地圖下一幕提示）一併改用 `storyActLabel`——已開放分支 `openActLbl`、
下一幕 `actLbl71`，舊 `actN`／`` `第 ${n} 幕〈${t}〉已經開咗` `` 已拎走。否則地圖提示仍會印
「第 18 幕」。顯示層、同一 label 函數，順手做埋，寫明係範圍延伸。

### 保留嘅 pre-existing quirk（今次唔修）

鎖住嘅插入幕喺主線未行晒嗰陣喺進度頁唔會出獨立行（`renderProgressPane71` far-merge fallback
`if(!farNs.length) return;` 會 skip 咗），直至開放／完成先突然出現，加深「無故出現」感覺。
今次保留舊行為唔修（guard 寫法維持 v153 行為）；要修要另開票改 far-merge 語義。

### 唔郁

C6／C6F／C18／C19 嘅開放條件、劇情內容、抉擇、旗標、`storyGate113Scrub`、強制播候選
（C 同 D 呢次唔做）。SAVE key、softRev（s107）、`?v=`（v20a10）唔郁；唔直改 content pack JSON；
`ORDER165` 唔郁。

## 3. 場景頂幕號（B）

StoryPlay `render()` beats mode 開場 head（`sp-head-opening`，只喺第一句閃現，v105 D-7）：
加咗幕號行 `${actLabel191?`<p class="sp-act191">${esc(actLabel191)}：${esc(actTitle191)}</p>`:""}`，
放喺 `sp-meta` 同 `<h3>` 節點標題之間。格式例：「第 6 幕・電影線：片場跟班」
（幕號＋進度頁標題 `prog71Title(n.id)`，唔係淨拼數字落節點 title）。
只限主線幕（`storyActLabel` 回 `""` 嗰陣唔出呢行，巧遇／隨機事件／支線唔郁）。
抉擇屏唔加 head（v128 A3 原意保留）。

### CSS 對比修正（實駕截圖捉到，v20a46 教訓重演）

第一版 `.sp-act191` 用深啡 `#4a2e10`——實駕 A_film 截圖證實壓喺深色場景圖頂＋漸變上面幾乎睇唔清，
而上面「主線 · 1990」白字就清楚。根因同 v20a46 一模一樣：通用規則
`#mask:not(.tut-on) .modal p{color:#3a2e22 !important}` 會強制深色，head 入面嘅 meta／h3／progress
全部靠 `#mask.story-play-on` 淺色＋`!important`＋文字陰影先睇到。修法：原行換成 mask-scope 規則
（L2428，單行替換，**淨行數 0**，唔使 resync）：

```css
#mask.story-play-on .story-play .sp-head .sp-act191{display:block;margin:0 0 2px;font-size:.85rem;font-weight:800;line-height:1.4;color:rgba(245,234,210,.95) !important;text-shadow:0 1px 2px rgba(0,0,0,.6)}
```

實駕 A_fix 證實 computed color `rgba(245, 234, 210, 0.95)`＋陰影＋可見，截圖米白粗體清晰可讀。

## 4. 改動一覽（index.html，淨 +47 行：60155→60202）

Hunks（舊行號→淨增）：CSS L2424 +2（後尾壓返淨 0，見 §3）；StoryPlay head L28071 +7；
`storyMainProgressLine` L38616 +1、L38624 +1、L38697 0；`storyActLabel`+`storyActIsInsert` L44042 +21；
GateItems L44078 +1；StubItems L44121 0；order71 註解 L44161 +7；`rows.push` 加 `label:storyActLabel(id)`
L44175 0；detailSet 註解 L44250 +2；四行模板改 `r.label || ("第 "+r.n+" 幕")`（L44263／44272／44282，0）；
插入幕 guard L44295 +5。`ORDER165`（L38447）唔郁。

Shift map（舊行→新行增量，逐行內容對位核實過 23 個探針全部 MATCH）：≤2424 為 0；2425–28071 為 +2；
28072–38616 為 +9；38617–38624 為 +10；38625–44042 為 +11；44043–44078 為 +32；44079–44161 為 +33；
44162–44250 為 +40；44251–44295 為 +42；≥44296 為 +47。

## 5. 測試

### 新測試（`tests/test_story191_logic.js`＋`tests/test_story191_static.py`，全部 PASS）

- (a) 標籤函數＋C6F 開放／C18 開放／新遊戲 pane 唔見「第 20／18／19 幕」；
- (b) `prog71Rows` 行次序＝ORDER165 次序、每行 `label === storyActLabel(id)`；
- (c) 遠幕合併「第 4–17 幕」／「第 8–17 幕」位置＋區間、鎖住插入幕唔出獨立行；
- (d) 舊存檔（C1–C5＋C6F done、film route、第 15 週）載入後「第 6 幕・電影線 ✓ 已完成」喺 C7 之前、C6 行喺其前；
- (e) C19 前置句「先完成番外・1990 冬〈上岸路〉」＋地圖提示「第 6 幕・電視線〈飯堂閒角〉」。
- static 另覆蓋：`.sp-act191` mask-scope 淺色＋`!important`＋陰影、冇深色 base rule。
- Harness 跟 `test_progress71_logic.js` 格式；`loadGame` 追加 C6F／C18／C19 最細節點（id／phase／locId／title 跟真節點：
  C6F P1.5／film_lion／「角落嗰張枱」；C18 P2／agency_ho／「上岸路」；C19 P2／film_lion／「賭枱邊」；
  `playerOffer:true`——因 fixture `tests/fixtures/story_detail_c1_to_c17.json` 只含 C1–C17，
  `listOpen` 開唔到佢哋；閘由 `STORY_GATE_3Y` 評）。Pristine 守衛：冇 `storyActLabel` 嗰陣逐組印 FAIL 後 exit 1，唔 crash。

### 更新咗嘅舊測試（因 v191 改咗行為，全部 PASS）

- `test_wf1_80_static.py`：order71 斷言改為 `["C6",6],["C6F",20],["C18",18],["C19",19],["C7",7]` 在位。
- `test_c17route153_static.py` B3：顯示次序改為 C1–C6、C6F、C18、C19、C7–C17；內部 n multiset 仍係 1–20；header 註解更新。
- `test_progress71_logic.js` A3：改為 `'第 6 幕・電視線〈飯堂閒角〉'`；buildSrc 加抽 `storyActLabel`＋`storyActIsInsert`
  （pristine 冇嗰陣用空 stub 頂住，等斷言乾淨 FAIL，唔喺 extractFn 拋錯 crash）。
- `test_verify37_logic.js` seg7：改為 `'第 6 幕・電視線〈飯堂閒角〉'`；buildSrc 加抽 `storyActLabel`＋`prog71Title`（同上 stub 守衛；
  此檔亦抽 StoryPlay IIFE 並真跑 `StoryPlay.start('C1'/'C2')`）。
- `test_story179_logic.js`：eval 加抽 `storyActLabel`（同上 stub 守衛；其 C3/C4/C5 斷言「先完成第 2 幕〈C2〉」等渲染字不變）。

### Resync：11 個釘行測試因淨 +47 行漂移，逐行內容對位核實後重算（全部而家 PASS）

用 `/tmp/resync191.py`＋`/tmp/resync191b.py`（單次用腳本，唔好重跑——重跑會 double-shift；
travel114 曾因此 double-shift，要還原重做一次）。內容逐字相同，純漂移：
`test_gift185_static.py`（總行數 60155→60202）；`test_kwan151_static.py`（13 個 pin）；
`test_tang152_static.py`（3 處）；`test_tang171_static.py`／`test_tang173_static.py`（總行數＋DEF＋pin）；
`test_text125_static.py`（3 處）；`test_travel114_static.py`（COUNT 12 處＋FREE 34 處＋DEF／WRAPPER）；
`test_rom176_static.py`（6 個 pin）；`test_story172_static.py`／`test_story179_static.py`
（`'先完成第 ' in stub` 改為 `'"先完成"+(storyActLabel(d)' in stub`，渲染字不變）；
`test_v155_static.py`（order71 全字串改為新次序）。11 檔頭各補咗一條 v191 resync 註解（第 2 行）。
教訓：resync 腳本唔可以重跑（sub_map／shift_block 唔係冪等）；每次跑完要用 `git status` 核實邊啲檔郁咗。

### 反證（pristine index.html，`git show HEAD:index.html` 放喺 `/tmp/c6f-pristine/index.html`，測試檔實體複製過去——唔可以用 symlink，否則 `__dirname` 解析返真實路徑讀咗改過嘅檔）

- 新 logic：5 組 FAIL（(a)–(e) 各一），乾淨、無 crash、exit 1。
- 新 static：18 項新 A/B 斷言 FAIL，基線斷言 PASS。
- 已更新舊測試：progress71_logic 淨 1 FAIL（A3）、verify37_logic 淨 1 FAIL（seg7）、wf1_80_static 淨 1 FAIL（新次序）、
  c17route153_static 淨 1 FAIL（B3 顯示次序）；story179_logic 喺 pristine 全 PASS（預期，v191 唔郁 C1 鎖行文字）。
  wf1_80／c17route153 反證要補齊 `/tmp/c6f-pristine/NOTES_V20A80_WF1.md`＋`content/STUB_STORY_BEATS_FREEPLAY_SLOTS_v1.json`，
  否則多咗路徑 artifact FAIL。

### 全套 suite

- Pristine 基線：第一次跑 224/43 係波動（v151 教訓）；第二次跑 **255 PASS／12 FAIL**（`/tmp/suite191_pristineB.txt`）。
  12 項穩定 FAIL：flash51、giglib36、pacing35、poster59、rumor49、slot50、soft_tip_111_restore、start53、weave43、weave44、weave49、wrap38。
- Work 版：**257 PASS／12 FAIL**，連跑三次 B／C／D 全部一樣（`/tmp/suite191_workB.txt`／`workC.txt`／`workD.txt`），
  FAIL 清單同基線一模一樣。＋2 PASS 係兩個新測試檔。Suite A 曾經 246/23，係因為嗰陣 11 個釘行測試未 resync——已修好，唔係波動。
- 相關測試逐個直接覆驗：`test_wf4_86_logic.js`、test_ui105_static、test_ui128a3_static 全部 PASS（佢哋抽 StoryPlay IIFE／sp-head）。

## 6. 實駕（Playwright，本地鏡像＋`python3 -m http.server`，LIVE 模式）

腳本 `qa191/drive191.py`（沿用調查報告 `drive_c6f2.py` 已驗證流程：新局→經 UI 真打 C1 揀路線→播種 C2–C5＋跳週→
開茶餐廳 sheet→閂 sheet→強制播彈出；播種前處理 new_game 後已自動開咗嘅 C1 stale session），
報告 `qa191/drive191_report.json`，截圖 `qa191/shots/`。0 pageerror、0 http fail。

- **A_film（932）**：C1 電影線→第 15 週→強制播 C6F，場景頂「第 6 幕・電影線：片場跟班」，
  節點標題仲係「角落嗰張枱」→播完 C6F done→進度頁「第 6 幕・電影線 ✓ 已完成」，成頁冇「第 20／18／19 幕」。9 項 PASS。
- **B_tv（932）**：C1 電視線→第 15 週→強制播 C6，場景頂「第 6 幕・電視線：飯堂閒角」→播完→
  進度頁「第 6 幕・電視線 ✓ 已完成」。9 項 PASS。
- **C_c18（932）**：C1 電視線→播種 C2–C6 done＋第 49 週（1990 冬）→強制播 C18，
  場景頂「番外・1990 冬：上岸路」→播完→進度頁「番外・1990 冬 ✓ 已完成」。9 項 PASS。
- **D_old（700）**：初版 1 項 FAIL 係腳本問題——直接 call `saveQ()`，但佢唔係 window 暴露函數
  （主 script 係 IIFE 內部定義，`ReferenceError: saveQ is not defined`），唔係遊戲問題；
  當時其餘 8 項照樣 PASS（遊戲自動存檔已寫咗去 active slot，reload 後槽 1 照載到 C6F done）。
  重跑 `qa191/drive191_D.py`（報告 `qa191/drive191_report_D.json`）改用任務指定方法——
  直接寫 localStorage key `starVolunteer_map_v19w`（slot 1）→ reload → 讀檔槽 1 →
  C6F 仲係 done → 700 闊進度頁「第 6 幕・電影線 ✓ 已完成」，C6 行喺 C6F 行之前（雙生並排）。10 項 PASS。
- **A_fix（932，`qa191/drive191_Afix.py`，報告 `drive191_report_Afix.json`）**：CSS 淺色修正後重跑——
  `.sp-act191` computed color `rgba(245, 234, 210, 0.95)`、有文字陰影、可見；截圖 `A_fix_story_open.png`
  米白粗體清晰可讀；播完＋進度頁照舊。6 項 PASS。
- 強制播流程本身唔郁：四個 case 全部經閂 sheet 觸發（`sheet-close`），冇用過晨鏈後備。

## 7. 殘留／跟進

1. 鎖住插入幕喺進度頁唔見（§2 quirk）——pre-existing，今次保留；要修另開票。
2. `storyActLabel` 係 C6 加後綴，所以地圖提示／A3 斷言跟住變（已更新測試，見 §5）。
3. 本票唔落地——分支已 push 去常駐 clone，等統籌 squash merge＋監察部署＋覆檢；唔開設計 review（工人範圍外）。
4. 注意：工作期間 MEMORY.md 有外部更新（v188／v189 已落地、v192 已開工）；本分支已兩輪 rebase，最終基底 `b3db32f`（見 §8），落地嗰陣統籌再對一次 main HEAD。

## 8. Rebase 上最新 main（2026-11-13 晚，工人重驗）

- 基底：`dcf1b72`（v187）→ `593a845`（v188 NOTES；含 v190 遊戲 `4283862`＋v188 遊戲 `0c29f03`）。
  開工 `git fetch origin` 核實 main 係 `593a845`，未再郁。Rebase 後單一 commit `6ea1f87`（`GIT_EDITOR=true git rebase`，
  冇 pipe 去 head，冇重複 pick 問題）。
- 衝突：`index.html` 自動合併——diff vs main 係 15 個 hunk，同原本 v191 diff（vs `dcf1b72`）逐 hunk 相同，
  v188 獎項改名（「最佳男主角」在位）＋v190 glamour panel（`.awd63-glamour` L808–811）在位，冇丟失。
  5 檔 static test 衝突，全部純行號漂移（`test_gift185_static.py`／`test_rom176_static.py`／
  `test_tang171_static.py`／`test_tang173_static.py`／`test_travel114_static.py`）。解法：取 HEAD（main）數字＋
  v191 shift map 重算，單次掃描 regex alternation 腳本（`/tmp/resolve191.py`，唔用 sequential re.sub，防撞值）。
- Shift map（difflib `SequenceMatcher` 核實）：
  - main `dcf1b72`→`593a845` 淨 **+254**：v190 淨 0（L808／810 兩處 replace）；v188 全部插入點喺舊 L45408 之後
    （replace +8、insert +217／+6／+8、replace +8、insert +2／+4、insert +1）。
  - v191 喺 main 座標嘅插入點同舊基底一樣（main 喺 L44042 之前零淨插入）：CSS L2424 +2／StoryPlay L28071 +7／
    `storyMainProgressLine` +2／`storyActLabel` L44042 +21／gate +1／order71 +7／detailSet +2／guard +5，淨 **+47**。
  - 合併後總行數 **60456**（60409＋47）。
- Resync 清單（5 檔衝突檔，錨點內容逐行對位核實純漂移）：
  - `gift185`：總行數 60409→60456。
  - `rom176`：6 針 6045→6047、31549→31558、53335→53382、53703→53750、54842→54889、54936→54983。
  - `tang171`：總行數 60409→60456、DEF 54905→54952。
  - `tang173`：同上＋L4862→L4864（合併後實量 mega-line 喺 4864）。
  - `travel114`：COUNT 12 處（58965→59012、59143→59190、59286→59333、59307→59354，其餘 +9／+11）、
    FREE 34 處（53158 之後各 +47，例如 53158→53205、59757→59804）、DEF 54905→54952、WRAPPER 44353→44400。
  - 其餘上一手 resync 過嘅檔唔使郁：`kwan151`（13 針）、`tang152`（3 處）、`text125`（3 處）、`story172`／`story179`／
    `wf1_80`／`v155`／`c17route153`／`progress71`／`verify37`／`story191`——佢哋啲針全部喺 main 插入點 L45408 之前
    （main shift 0）；kwan151 13 針＋tang152 3 針逐行對過內容啱，L802 一帶係 v190 glamour 規則（L808–811），
    v191 CSS 插喺 L2424，冇影響。
- 附帶發現（唔係遊戲問題）：main 版 `test_tang173_static.py` 嘅 balance check（`lines[4863]`）喺 main 指向錯行
  （mega-line 喺 main 係 4862，應為 `lines[4861]`；v191 分支 pin＋balance 兩邊都係 `lines[4863]` 一致啱）。
  Rebase 後合併檔 mega-line 喺 4864，pin＋balance check 一併指向 `lines[4863]`，順手修正咗呢個 latent 錯位。
- 重驗（rebase 後最終樹 `6ea1f87`，全部重跑）：
  - 新測試 `test_story191_logic.js`＋`test_story191_static.py` 全部 PASS；相關舊測試逐個 PASS：
    `progress71_logic`、`verify37_logic`、`c17route153_static`、`story172_static`、`story179_logic`／`story179_static`、
    `wf1_80_static`、`v155_static`、`text125_static`、`kwan151_static`、`tang152_static`、`tang171_static`（22/22）、
    `tang173_static`（21/21）、`travel114_static`、`gift185_static`、`rom176_static`。
  - 反證（pristine main `593a845`，`/tmp/pristine191b/`）：story191 logic 5 組 FAIL（(a)–(e) 各一）、
    static 18 項新 A/B 斷言 FAIL、progress71 淨 1 FAIL（A3）、verify37 淨 1 FAIL（seg7）、
    wf1_80 淨 1 FAIL、c17route153 淨 1 FAIL（B3），全部乾淨、無 crash、exit 1。
  - `node --check`：兩段 inline script 全部 OK。
  - 全套 suite：工作版 **261 PASS／12 FAIL**（`qa191/suite_work191.txt`）vs pristine 基線 **259 PASS／12 FAIL**
    （`qa191/suite_pristine191.txt`，`~/workspace/linji-pristine191-suite/` 全量 archive，用完已清走），
    FAIL 清單相同（12 項穩定 FAIL），＋2 PASS 淨係兩個新測試檔，零回歸。
    教訓：`/tmp` 係 512M tmpfs，`git archive` 全 repo（447M）抽去 `/tmp` 會爆滿——基線要抽去 `~/workspace/`；
    另第一次抽淨 `index.html`＋`tests`＋`content` 跑出 201/70，係缺檔假 FAIL，唔係基線真實數字。
  - 實駕（rebase 後最終樹重跑，`qa191/drive191.py`＋`drive191_D.py`＋`drive191_Afix.py`）：
    A_film／B_tv／C_c18 全部 PASS（場景頂幕號＋進度頁標籤同 §6 一致）；D_old 初版 saveQ FAIL 係腳本問題
    （同 §6），修正版 D_old2 10 項全 PASS（slot 1 寫入＋reload 後 C6F 仲係 done，C6 行喺 C6F 行之前）；
    A_fix 6 項全 PASS（computed color `rgba(245, 234, 210, 0.95)`＋陰影＋可見）。0 pageerror、0 http fail。
- Commit＋push：NOTES 增補另一個 commit（見 log），分支 `v20a191` 用 `git push --force-with-lease origin v20a191`
  只推常駐 clone，唔推 GitHub。**本票唔落地**——等統籌 squash merge＋監察部署＋覆檢；唔開設計 review。

### 第二輪 rebase（同一晚稍後：v189 落地，main 郁到 `b3db32f`）

- 第一輪 push 嗰陣 `git fetch` 顯示 main 已郁：v189 遊戲 `b7ca827`＋NOTES `b3db32f` 已落地（日結板三粒掣）。
  即刻第二輪 rebase 上 `b3db32f`（`GIT_EDITOR=true git rebase`，兩粒 commit 逐粒 replay，冇 pipe 去 head）。
- `index.html` 自動合併——diff vs 新 main 仍然 15 個 hunk，同原本 v191 diff 相同；v189 改動在位。
  v189 shift map（difflib `SequenceMatcher`，`593a845`→`b3db32f`，淨 **+34**：insert +15（L1831 後）／+10（L3219 後）／
  delete −10（L37990–37999）／replace +3／insert +12／replace +3（L38399）／replace +1（L39380）；
  分段：≤1831 為 0、1832–3219 為 +15、3220–37989 為 +25、38000–38005 為 +15、38008–38010 為 +18、
  38011–38399 為 +30、38400–39380 為 +33、≥39381 為 +34）。v191 喺新 main 座標插入點：
  CSS 2439 +2／StoryPlay 28096 +7／storyMainProgressLine 38649 +2／storyActLabel 44076 +21／其餘同 §8，
  合併後總行數 **60490**（60443＋47）。
- 衝突：8 檔 static test（v189 嗰邊都 resync 咗佢哋），全部純行號漂移，同一方法解（取 HEAD 數字＋v191 shift map，
  單次掃描 `/tmp/resolve191b.py`）：`gift185`（總行數 60443→60490）、`kwan151`（13 針，25657→25659、25998→26000、
  26046→26048、26265→26267、26003→26005、26001→26003、26002→26004、31020→31029、31011→31020、27244→27246、
  31062→31071、31019→31028、27211→27213）、`rom176`（6 針 6070→6072、31574→31583、53369→53416、53737→53784、
  54876→54923、54970→55017）、`tang152`（3 處 25816→25818、31500→31509、31644→31653，0-based）、
  `tang171`（總行數＋DEF 54940→54986）、`tang173`（同上＋L4862→L4889，合併後實量 4889；v189 嗰邊 balance check
  已跟 pin 一致，上一輪發現嘅 latent 錯位喺 v189 嗰邊已經修好）、`text125`（三錨點 27736→27738、27865→27867、
  33559→33568，label 順便跟埋 code 更新）、`travel114`（COUNT 12＋FREE 34＋DEF 54939→54986＋WRAPPER 44387→44434）。
  錨點抽驗（rom176 6 針＋DEF＋L4889＋kwan151 8 針＋tang152 3 處＋text125 3 處＋travel114 抽 11 處＋WRAPPER）全部對位 OK。
- 重驗（第二輪最終樹 `29bd376`，全部重跑）：新測試 logic＋static 全部 PASS；相關舊測試逐個 PASS
  （progress71／verify37／story179 logic、c17route153／story172／story179／wf1_80／v155／text125／kwan151／tang152／
  tang171 22/22／tang173 21/21／travel114／gift185／rom176）；反證（pristine main `b3db32f`，`/tmp/pristine191c/`）：
  story191 logic 5 組 FAIL、static 18 項新 A/B 斷言 FAIL（grep 數 19 係連埋 FAILURES 匯總行，同上一輪一樣）、
  progress71 淨 1 FAIL（A3）、verify37 淨 1 FAIL（seg7）、wf1_80 淨 1 FAIL、c17route153 淨 1 FAIL（B3），
  全部乾淨、無 crash、exit 1；`node --check` 兩段 inline script OK；全套 suite 工作版 **263 PASS／12 FAIL**
  （`qa191/suite_work191b.txt`）vs pristine 基線 **261 PASS／12 FAIL**（`qa191/suite_pristine191b.txt`），
  FAIL 清單相同，＋2 PASS 淨係兩個新測試檔，零回歸；實駕 A_film／B_tv／C_c18＋D_old2＋A_fix 全 PASS，
  0 pageerror、0 http fail（主 drive D_old 嗰個 saveQ FAIL 仍然係已知腳本問題，同 §6）。
- 環境雜音（兩次撞到，唔係本票問題）：① 間歇性檔案系統靜默故障——`ls`／`cp` 一度話 `tests/test_story191_static.py`
  唔存在（同一檔案幾分鐘前後都讀到、寫到），之後唔使做任何嘢自己恢復返；反證第一次誤跑咗工作樹（STATIC_EXIT:0
  假 PASS），發現後逐個 `cp` 逐個核實先重跑，數字先可信。② `/tmp` 512M tmpfs 之前爆過一次，基線全量 archive
  改放 `~/workspace/linji-pristine191-suite/`，用完已清走。
- Commit＋push：NOTES 增補另一個 commit，分支 `v20a191` 用 `git push --force-with-lease origin v20a191` 只推常駐 clone，
  唔推 GitHub。**本票唔落地**——等統籌 squash merge＋監察部署＋覆檢；唔開設計 review。

## 9. 落地紀錄（統籌補）
- 遊戲 commit `f2a6b0c`（main `b3db32f` v189 → squash merge `v20a191`，push main 一次成功，無斷線）。
- 線上核實：5,336,448 bytes、sha256 `9eb1980d…`，同 repo `HEAD:index.html` 完全一致（Pages 部署滯後約 150 秒，第一 curl 仲係 v189 舊版）。
- `git fsck --strict` 乾淨（只有 squash merge 正常 dangling）。
