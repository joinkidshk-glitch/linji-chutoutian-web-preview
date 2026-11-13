# NOTES_V20A173 — v171 review C1＋C2 修復

**分支** `v20a173`（工作副本 `~/workspace/linji-work173`），基底 `e8c3a73`（v170 已落地，
main `59fdf54`，線上 5,254,542 bytes sha `651c26e7…` 已核實）。
**範圍**：用戶 2026-11-13 12:50 拍板，修晒 v171 review C1＋C2（報告
`~/workspace/linji-design-review-v171/REVIEW.md`，A 0／B 0／C 2）。**唔落地**——統籌落地。
**改動**：`index.html` L4832 同行 2 處（加 0 行，總行數 59173 不變；openLoc DEF 行 53692 不變；
kwan151／tang152／travel114 釘行唔使 resync）＋`tests/test_tang171_static.py` 2 條斷言跟新值
＋新 `tests/test_tang173_static.py`（21 項）＋實駕 `qa173/drive173.py`／`drive173.json`／`shots173/`。

## 更正數字（v171 NOTES §4 錯，review 已證實；唔另改 v171 NOTES，喺呢度寫啱）
- `scrollH` 係 **814**（唔係 821）。掛 class／除 class／sync 還原全部 814。
- 932 首屏被淡出冚住嘅係「還人情」底 **22px**（「聽風聲」只得 1px，唔係半截）；
  700 被切嗰個係「送禮：鄧麗萍」成 30px（visFrac 0.84）。

## §1. C1——932 淡出提示偏弱
**問題**：同一個 30px 淡出，932 首屏只冚住「還人情」底 22px、掣睇落完整（visFrac 1），
700 就明顯切＋溶走（送禮掣 visFrac 0.84）。932 玩家唔留神好易當咗係裝飾性漸變。
**修法選擇**：跟報告建議揀 (a)——漸變實色 stop 由 78% 提早到 **60%**，一行：
`linear-gradient(to bottom, rgba(248,241,222,0), #f8f1de 78%)` → `#f8f1de 60%)`。
唔揀 (b) 加高到 40px：(a) 純視覺改動，幾何影響最細；實測夠就唔做 (b)（見 §4 實測）。
唔郁掣高／卡片（B2）：高仲係 30px、`margin-top:-30px`＋`margin-bottom:-7px` 抵消唔郁。
**點解 60% 夠**：78% 時實色線喺淡出區 23.4px 處（932「還人情」底 851 仲未到實色線 852，
成個掣底只係半透明漸變，睇落完整）；60% 時實色線喺 18px 處，掣底 4px 完全溶入底色＋
上面 18px 漸變加深，半截掣提示明顯咗。
**實測**（`qa173/drive173.json`，`c1_932`／`c1_700` PASS）：
- 932 首屏：還人情 zoneOverlap **22**、**belowSolid 4**（底 4px 完全溶入底色）、
  聽風聲 zoneOverlap 1、fade 區中心 elementFromPoint 命中「還人情」（`pointer-events:none`
  生效，唔攔點擊）；`::after` 背景 live 序列化為 `linear-gradient(rgba(248, 241, 222, 0),
  rgb(248, 241, 222) 60%)`。
- 700 首屏：送禮掣 zoneOverlap **30**、visFrac **0.84**、belowSolid 12。
- `scrollH` 頂／底 **814／814**；捲到底 hasMore false、最尾掣「同何生傾談」全見；
  捲返頂提示返嚟；resize 932→700／700→932 之後 hasMore 照 true、scrollH 照 814。
- B2 守門：兩卡各 **h115**、gap **7px**、重疊 0、badge 喺卡內橫排。

## §2. C2——鎖住態 hint 冇跟標題淡
**問題**：標題 `.n` opacity 0.72，但 hint `.h` 實測 opacity 1。根因：舊 rule L2016
`#loc-sheet.sheet .act .h { …; opacity: 1 !important; … }` 用 `!important` 贏咗 v171 條
無 `!important` 嘅 `#app #loc-sheet.sheet .act.act-locked171 .h { opacity:.72; }`。
**修法**：v171 條 `.h` 規則加 `!important`，一行（同行 `.cost`／掣底嗰兩條一樣寫法）：
`.act.act-locked171 .h{ opacity:.72 !important; }`。特異性 (2,4,0)（#app＋#loc-sheet）
贏舊 rule (1,3,0)，hint 返 0.72。
**實測**（`qa173/drive173.json`，`c2` PASS，live computed-style）：
- 鎖住態（今日已送／庫存空）：標題 opacity **0.72**、hint opacity **0.72**、
  hint 色 `rgb(58, 46, 34)`（#3a2e22）、掣底 `rgb(230, 223, 204)`（#e6dfcc）、
  費用欄 `rgb(107, 86, 54)`（#6b5636，5.25:1）；hint 混合後 `rgb(106, 96, 82)` on
  #e6dfcc＝**4.63:1** ≥ 4.5，照讀到。
- 可送態唔郁：標題／hint opacity 1、掣底 `rgb(245, 230, 192)`、費用欄「免費」紅
  `rgb(196, 60, 42)`（4.21:1，v169 B1 已確立底線，刻意唔郁）。
- 撳鎖住態照有 toast（「人情急不來；今天先到這裡。」／「庫存空空——可先去油麻地廟街
  禮品檔看看。」），**唔開揀禮物 modal**（`modal_visible() == false`）；disabled false。
- B1 三態照啱（免費／今日已送／庫存空）；送名筆流程正常（「排片關係不變」結果句照舊）。
**對比度細節**：送禮掣係 `act-priority`，hint 色由 L2040 `#3a2e22` 定（唔係 L2016
`#5a4328`）；0.72 混合後 4.63:1。非 priority 鎖住掣 hint 色會係 #5a4328，混合後只得
3.64:1——呢個板得一粒送禮掣（priority），其他地點 NPC 送禮掣未逐個 live 驗（見 §6）。

## §3. 途中捉到嘅真 bug——註解嵌套吞咗鎖住底 rule（已修，v173 本票造成）
第一輪 drive c2 FAIL：`sent_btn_bg_grey`／`empty_btn_bg_grey`——鎖住態掣底 live 係
`rgb(245, 230, 192)`（#f5e6c0，priority 底），唔係 `rgb(230, 223, 204)`（#e6dfcc）。
cascade 探針（`/tmp/cascade173.py`，見 §7）證實：`matchesLocked == true`、`inApp == true`，
但成個 stylesheet 入面**完全冇** `#app #loc-sheet.sheet .act.act-locked171` 呢條 background
rule（cssRules idx 1482 位置唔存在）；.n／.h opacity 規則就正常生效。
**根因**：我最初喺 L4832 兩段註解入面各插咗一段 `/* v20a173 … */`——CSS 註解唔可以嵌套，
第一個 `*/` 就閂咗外層註解。C2 嗰段：我插嗰段嘅 `*/` 提早閂咗 v171 C2 註解，註解殘尾
「；費用欄轉深啡灰 #6b5636…撳落去照有 toast 講原因 */」變成裸文，CSS parser 當佢係
malformed rule prelude，連同鎖住底 rule 嘅 selector 一齊吞埋（直至下一個 `{…}` block），
成條 background rule 消失；.n／.h／.cost 三條喺後面，parser 恢復後正常解析，所以淨係底色死。
靜態測試驗唔到（佢只驗 CSS 文本存在）——正正係 v171 review 講嗰類盲點。
**修法**：將 L4832 兩段註解各合併成**一個**正常註解（v171 原文＋v173 附註，唔再有嵌套
`/*…*/`），鎖住底 rule 返返註解之外。修後 cascade 探針：鎖住 rule live（cssRules idx 1482，
`rgb(230, 223, 204) important`），掣底返 #e6dfcc；重跑 drive c2 PASS。
**防倒退**：`test_tang173_static.py` 加咗 L4832 註解平衡斷言（`/*` 數＝`*/` 數＋鎖住底 rule
前面最後一個 `/*` 早過最後一個 `*/`，即 rule 唔喺註解入面）。

## §4. 測試
- 新 `tests/test_tang173_static.py`：**21/21 PASS**。斷言：fade stop 60% 存在＋78% 唔存在；
  幾何唔郁（30px＋margin 抵消）；sync 條件唔郁；B2 守門；鎖住態 `.h` 有 `!important`＋舊
  無 `!important` 嗰條唔存在；標題 .n 仲係 .72；舊 rule L2016 仲喺度；掣身／費用欄唔郁；
  冇加 disabled；B1 守門；可送態唔郁；hint 混合後對比度 4.63:1 ≥ 4.5；費用欄 5.25:1；
  SAVE key／softRev／?v= 不變；零行數漂移（59173 行、openLoc DEF 行 53692、L4832 同行）；
  L4832 註解平衡（§3 防倒退）。
- 反證：喺 pristine（基底 `e8c3a73`）index 上行，**16/21、4 項乾淨 FAIL**（兩項 C1 stop、
  兩項 C2 `.h !important`），唔 crash；其餘 17 項（守門＋紀律）PASS。
- `tests/test_tang171_static.py`：**22/22 PASS**。兩條斷言跟新值改咗（78%→60%、`.h` 加
  `!important`，附 v173 註解）；舊值斷言搬咗去 test_tang173（驗新值存在＋舊值唔存在），
  唔係刪咗守門。
- 全套 A/B（`qa131/run_suite.sh`，`qa173/suite_work173.txt`）：基線 v170 後 **231／12**
  （12 項穩定 pre-existing FAIL）；工作版 **232／12**，FAIL 清單同基線完全相同，零回歸。
  （＋1 PASS 正好係新加嘅 test_tang173。）
- 註：第一輪全套（修註解前跑）同樣係 232／12、FAIL 清單相同——靜態測試驗唔到 §3 嗰類
  解析問題，靠實駕捉到。

## §5. 實駕
`qa173/drive173.py`（由 `qa171/drive171.py` 改；播種用 drive171 同款 softSeed；port 8183；
完整 Chromium＋`xvfb-run -a`——直接跑 headless=False 會死「Missing X server」，見 §7）：
**c1_932 PASS／c1_700 PASS／c2 PASS，OVERALL PASS，0 pageerror**（三 case pageerrors 全部 []）。
證據 `qa173/drive173.json`（DOM 層數字為主）＋`qa173/shots173/` 8 張（c1 兩高度 top／scrolled、
c2 ok／sent／empty 932、送筆結果）。
- HTTP 404：24 條，全部 pre-existing artId 缺圖（`rom_tang_meet_soft_hold`／
  `rom_tang_push1_soft_hold`，同 v169／v171 記錄一致），畫面有 fallback，0 pageerror。
- 播完 meet／push 有清 enc79 overlay 先截圖；影地圖前驗 sheet 真係閂咗（v171 review 教訓——
  今次 drive 唔影地圖，唔受影響）。

## §6. 殘留／唔郁
- v172、v149／v170 典禮工作唔郁；v171 NOTES §4 數字錯唔另改，喺呢度寫啱咗（見頂）。
- 淡出同 `#loc-acts` flex row-gap 7px 有耦合（`margin-bottom:-7px` 抵消）——之後改 gap 要
  一併改，靜態測試＋實駕 `scrollH` 已釘住（814）。
- 非 priority 鎖住掣 hint 對比度：色 #5a4328 混合後只得 3.64:1（見 §2 尾）。呢個板得一粒
  送禮掣（priority，4.63:1），其他地點 NPC 送禮掣未逐個 live 驗；唔喺呢票範圍。
- (b) fade 加高到 40px 唔使做——(a) 實測夠（§1）。

## §7. 環境附註
- 寫入 EPERM 今次全程冇出現；Chromium 全程穩定。
- `pkill -f run_suite.sh` 會誤殺自己條 exec command（pattern 撞正自己）——要用
  `pkill -f "[r]un_suite.sh"` bracket trick。
- `nohup … &` 嗰句：`A && B & C` 會將 `cd` 拆去 background subshell，之後嗰句喺原 cwd 跑——
  drive 要用絕對路徑，或者分開兩句跑。
- headed Chromium 要 `xvfb-run -a`，否則「Missing X server or $DISPLAY」死 launch。
- drive173.py L395 有 `SyntaxWarning: invalid escape sequence '\d'`（JS regex `\d` 寫喺 Python
  三引號字串入面，值本身啱，純 warning；下次寫探針用 raw string 乾淨啲）。

## §8. Rebase 紀錄
（落地唔係工人做；以下係分支狀態，畀統籌驗收用。）
- 工作副本 `~/workspace/linji-work173`，分支 `v20a173`，基底 `e8c3a73`；期間 main 冇郁過，
  唔使 rebase。
- 待 commit：`index.html`（L4832 同行）、`tests/test_tang171_static.py`（2 條斷言跟新值）、
  新 `tests/test_tang173_static.py`、`qa173/drive173.py`／`drive173.json`／`shots173/`（8 張）、
  `NOTES_V20A173.md`。
- **唔好 `git push origin`**——clone 式副本，origin 係常駐 clone 本地路徑；等統籌驗收。

## §9. 落地統籌 rebase＋重驗紀錄（2026-11-13）
- **§8 更正**：工人寫「期間 main 冇郁過」已經過時——其後 v149（遊戲 `461dc87`＋NOTES `a500536`）、v153（遊戲 `bbd318e`＋NOTES `0ecaeb3`）先後落地。落地基底改為 **`0ecaeb3`**。
- **Rebase**：分支推去常駐 clone 後 rebase 上 `origin/main`（`0ecaeb3`），新 HEAD `d06da40`（實作 `c42c1ee`＋suite 紀錄）。唯一衝突係 `tests/test_tang171_static.py` 頭註解（v153 resync 行撞 v173 更新行），解法兩邊都留＋加一行 v173 rebase 註記；`index.html` 自動合併，零衝突。
- **Resync（單次掃描 dict 查表，唔係逐對 re.sub；prose 數字逐項 grep＋`git show e8c3a73:index.html` 核實先改）**：總行數 59173→**59341**（v149 ＋97＋v153 ＋71）、openLoc DEF 53692→**53860**（＋168）、v173 CSS 同行 4832→**4845**（v149 CSS ＋13）、舊 rule L2016→**L2024**／L2040→**L2048**（各 ＋8）。改咗 `tests/test_tang173_static.py`（21 處）＋`tests/test_tang171_static.py` 標籤一行（59270→59341，check 值本身已係 59341）。`test_book143` 嗰個 4832 只係 commit hash，唔係行號，唔郁。`kwan151`／`tang152`／`travel114`（DEF 53860）本身已係新基底值，唔使 resync。
- **重驗（rebase 後最終樹）**：`test_tang173` **21/21**、`test_tang171` **22/22**、`kwan151`／`tang152`／`travel114`／`text125` 全部 PASS；`node --check` 兩段 inline script PASS。反證：`test_tang173` 喺 pristine `0ecaeb3` index 上行 **17/21**，4 項新行為斷言乾淨 FAIL（2× C1 stop、2× C2 `.h !important`），唔 crash。
- **全套 A/B**（`qa131/run_suite.sh`，pristine worktree `~/workspace/pristine173-0ecaeb3`，紀錄 `qa173/suite_pristine_0ecaeb3.txt`／`qa173/suite_rebase173.txt`）：pristine **232／12** vs 工作版 **233／12**，FAIL 清單逐項相同（12 項 pre-existing），**零回歸**（＋1 正好係新加嘅 test_tang173）。
- **實駕重跑**（`qa173/drive173.py all`，完整 Chromium＋`xvfb-run -a`，port 8183）：**c1_932 PASS／c1_700 PASS／c2 PASS，OVERALL PASS，0 pageerror**。數字同工人嗰輪完全一致：932 淡出 live 序列化 `... rgb(248, 241, 222) 60%`、「還人情」zoneOverlap 22／belowSolid 4、scrollH 814（頂／底／resize 全部 814）、700 送禮掣 zoneOverlap 30／visFrac 0.84／belowSolid 12、C2 鎖住態標題／hint 全部 opacity 0.72、可送態 1。`drive173.json`＋`shots173/` 重跑後 byte-identical（git 無改動）——rebase 零行為改變。HTTP 404 全部 pre-existing artId 缺圖（`rom_tang_*_soft_hold`）。
