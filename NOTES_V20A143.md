# NOTES_V20A143 — 手帳內臟紙面化（v141 review B1＋B2＋B3）

用戶 2026-11-12 拍板修 v141 review 頭三項。基底 main `4832b85`（v141）；分支 `v20a143`。**落地前 rebase 到最新 main `a1b0920`（v144 已上線：紅星巧遇頻率收緊）**，見下「Rebase」節。

## 改咗邊幾處（index.html，淨 +43 行；唔郁 content pack JSON）
- **CSS 段**（`</style>` 前，`/* === v20a143 BOOK143 === */`）：全部三項樣式。手寫字體棧／紅墨 `#c0452c`／紙面 `#f5eddc`／`#fbf3df` 跟 v141。
- **B1 編輯態掣群紙面化**：
  - 快捷四掣（`.nb-quick > button`，直屬先命中，唔搶 `#nb-train71-wrap` 入面訓練選擇器掣）：紙標籤 `#fbf3df`＋1px 金邊 `#b99b62`＋radius 3px＋手寫字 15px（`!important` 蓋 v17l 嘅 `.72rem !important`）。
  - 複製 chip：radius 3px 紙標籤，選中紅墨邊；預設三掣同款；「套用複製」`.ink` 由深啡實底改紅墨字（淡紅底＋2px 紅框）。
  - 每行「複製」（`.day-row .cp`）：透明底＋虛線底線＋手寫墨字 13px，唔再係米色 pill（仍係 `role=button`）。
  - 底部 bar（`.nb-actions`）：深色底改紙面色 `#f5eddc`＋金邊頂線。
  - 「還原」（`#nb-actions #btn-reset-plan`）：手寫墨字＋虛線底線；2×id＋`!important` 搶贏 904 行 grouped `.nb-actions button.paper !important`。
  - 可編輯態「確定」（`#nb-actions #btn-confirm-plan:not(.is-locked)`）：紅墨字掣（2px 實線紅框＋淡紅底＋手寫字 18px＋letter-spacing .14em），仍然係撳得嘅掣；`:not(.is-locked)` 保鎖定態印章完全唔受影響；同樣 2×id＋`!important` 搶贏 904 行 grouped `.nb-actions button.ink !important`。
  - 功能一個都唔少：id／class／onclick 綁定零改動（見 logic 測試）。
- **B2 其餘四組 subtab**：照 plan 組做法，經 `:not([data-hsubgroup="plan"])` 擴展——手寫字 17px、未選褪色 `#a08a68`、選中紅墨手畫圈（同一 SVG，同 v141 plan 組一模一樣）；容器排版同 plan 組一樣（gap 22px、左 inset 46px）。**v141 plan 組原規則原封不動**，內容面板唔郁。
- **B3 短屏印章收細**：`@media (max-height:780px)`——印章 24px→20px、padding／margin 收窄＋`#nb-actions` padding 收窄；932 唔入 media query，印章 24px／3px double／斜 -4.5° 原封不動。

## 舊規則搶贏兩鑊（同 v141 一樣，實駕量度核實）
- 904 行 grouped `!important` 蓋 `.nb-actions button.paper／.ink` → 還原／確定要用 2×id＋`!important`。
- v17l 蓋 `.nb-quick button` font-size `.72rem !important` → 手寫 15px 要 `!important`。

## 測試
- 新：`tests/test_book143_static.py`（19 斷言）＋`tests/test_book143_logic.js`（8 斷言，接線唔郁＋共用 `setHomeTab`）。
- 反證（pristine main `4832b85`，`git show` 出嚟嘅 index）：static **13 FAIL**／logic **1 FAIL**；工作副本 **ALL PASS**。v141 兩測試工作副本照舊 ALL PASS。
- 全套（`qa131/run_suite.sh`）：基線 **PASS 196／FAIL 12**；本票 **PASS 198／FAIL 12**（FAIL 清單完全一致，12 個係 pristine 已有；+2 係新測試）＝零回歸。
- 舊測試 rebase（純行號漂移，difflib 核實淨係 BOOK143 段插入、內容逐行相同，唔改語義；淨 +43 行）：
  - `test_map54_static.py`：allowlist 加 v20a143（同 v141 加 v20a141 一樣做法）。
  - `test_text125_static.py`：三個錨點 +43（27631→27674、27744→27787、33342→33385）。
  - `test_travel114_static.py`：COUNT 13＋FREE 27 行＋DEF／WRAPPER 全部 +43（53143→53186、43938→43981）。
  - 三個 rebase 後測試喺 pristine 照樣 FAIL（行號對返舊版），工作副本 PASS。

## 實駕（`qa143/drive143.py`，port 8963，`?softPreview=1`，0 pageerror／0 HTTP404）
- 430×932＋430×700，兩屏全 PASS。
- **B1**：快捷四掣量度 15px／radius 3px／`#fbf3df`；每行複製 13px 手寫＋虛線底線；底部 bar 紙面色 `#f5eddc`；還原 15px 虛線底線；確定 18px 紅墨 2px 實線框。功能逐個撳過：全日休息（七日全變休息睡覺）→還原返原狀；全日訓練（選擇器開合＋未報名 toast）；清空本週（七日全變到處逛逛）→還原；每行複製（週一開面板→週末預設→套用複製，toast「已複製到 2 日」）→還原；複製到…（開合）；每次還原後行程同開局快照逐行一致。
- **B2**：四組 subtab 逐個切換啱 pane（作品／獎項／回憶、記數／庫存、傳聞／剪報、人情債／人脈），紅墨圈跟住選中郁（每組 `circleFollows=True`）；plan 組對照（行程→進度→行程）圈跟住郁，冇變。
- **B3**（`qa143/probe143_b3.py`，scrollTop=0＋clip-aware 量度，pristine 對照）：
  - 932：兩邊一樣——鎖定態 7/7 全見，印章 24px／67px 高、footer 84px。
  - 700 鎖定態：pristine 印章 24px／67px、footer 84px、週一–週五全＋週六得 4px 頭；本票印章 **20px／54px、footer 63px（慳 21px）**、週一–週五全＋**週六頭 25px**——即係慳返約 15px 俾多半日（半行），合乎任務寫法。完整日數維持 5 日（週六要再多 17px 先成行全見，唔係本票範圍）。
  - 700 可編輯態兩邊一樣：3 全＋週四頭。
- **唔郁嘅位核實咗**：五個大 tab 58×38／58×32；備忘紙 live（銀包 $12,000／聲望 5／信用 10）；吊牌返地圖啱；932 鎖定態印章完整（y858–925）；鎖定態還原隱藏。
- 截圖 `qa143/shots/`（20 張：每屏 editable／locked／map＋B1 rest／train／copy＋B2 四組＋plan）；量度 `qa143/drive143.json`；B3 對照 probe `qa143/probe143_b3.py`。

## 實駕教訓（留返下次）
- 可見日數唔可以用 `getBoundingClientRect` 對 `window.innerHeight` 嚟計——俾 notebook 內部捲走／俾 sticky footer 遮住嘅行都會計多咗（第一版 drive 量到 700 鎖定態 7/7，錯）。要 clip-aware（行頂 ≥ notebook 頂＋行底 ≤ nb-actions 頂）＋量度前 `scrollTop=0`（drive 撳過掣會留低 scrollTop）。probe143 用呢套定義先量到真數。
- `#htab-tags`（標籤）本身 `hidden`（pre-existing，唔係 B2 改出嚟）——B2 sweep 只驗可見掣。
- `git archive` 全量抽 pristine 會爆 `/tmp`（512M tmpfs）——對照 probe 用 pathspec 淨抽 `index.html assets content favicon.ico`（239M）先夠位。

## 取捨／已知限制
- B3 只慳 21px、週六由 4px 頭變 25px 頭，唔係成行全見——要成行要再慳多 17px（例如印章再細一級／收埋「本週行程」標題行），嗰啲超出任務寫法，留待拍板。
- 複製 chip 手寫字 13px 喺 Linux 截圖用 Noto Serif 渲染（同 v141 手寫字一樣，已知限制，iPhone 出楷體），唔當 bug。
- 訓練選擇器入面嘅掣（`.train71-pick` 等）唔喺 B1 範圍，維持原樣（`.nb-quick > button` 直屬選擇器刻意避開佢哋）。

## 紅線
SAVE key／softRev s107／產品 `?v=` v20a10 不變；content pack JSON 唔郁；index.html 註解無其他測試硬計嘅版本字串；鎖定態印章／五大 tab／備忘紙／吊牌／進度手寫行唔郁。

## Rebase（統籌做，落地前）
- 落地嗰陣 main 已行前到 `a1b0920`（v144 上線：紅星巧遇頻率收緊＋NOTES 補錄）。`git rebase origin/main`：index.html 自動合併（v144 改 51229／51327／51851＋ 區，BOOK143 段喺 `</style>` 前，唔撞）；得 `tests/test_travel114_static.py` 一個衝突（兩邊都郁咗 COUNT／FREE／DEF／WRAPPER 行號錨點）。
- 衝突解法（純行號，唔改語義）：rebase 後檔案＝HEAD＋BOOK143 插入（＋43 行，喺全部錨點之前）→ HEAD 側數字一律 ＋43（40 個錨點＋DEF 53151→53194＋WRAPPER 43938→43981；算術核實：v143 側＝orig＋43，HEAD 側＝orig＋V（V=0 或 8＝v144 淨增行數），差 43 或 35 對得上）。`test_travel114_static.py` 解完即 PASS。
- 重驗（rebase 後）：新測試 book143 static／logic 照舊 ALL PASS；map54／text125／travel114 全部 PASS；全套 **PASS 200／FAIL 12**，對新基線（v144 main，197／12）FAIL 清單完全一致＝零回歸（＋3 PASS＝2 個新測試＋`test_enc144_logic.js`——基線嗰次跑漏咗呢行，單獨跑 ALL PASS，唔係回歸）；`drive143.py` 重跑：B2 每組 circleFollows=True、700 鎖定態印章 20px／footer 63px／5 日全見、0 pageerror／0 HTTP404。

## 落地
- **main `cd40cb7`**（git 直接合併，冇開 PR；squash，分支 `v20a143`）。**線上核實通過**：index.html **5,200,760 bytes、sha256 `c04ec926191ccd89062a4e2ace47a33928f078faa898d9ad250f1d927209b7da`**，同 repo HEAD 完全一致（BOOK143 2 處）。第一次 curl 嗰陣線上仲係 v144 舊版（5,194,707 bytes、sha `9d0ad918…`），等多約 4 分鐘再驗先見到新版。
