# NOTES_V20A171 — v169 review C1＋C2 修復

- 分支：`v20a171`（工作副本 `~/workspace/linji-work171/`）
- 基底：main `56141a3`（遊戲 `1259ad8`，v169 上線版；線上 5,251,706 bytes sha `c0bbc07d…`）
- 範圍：淨修 v169 review 兩項 C 級（C1 push 並存態最尾掣要碌先見＋C2 鎖住態同可送態分唔到）。
  唔郁：v167 review C1（接受現狀）、咖啡豆句、push1 到唔到、玫瑰扣庫存、v170／v149。
- 改動總覽：`index.html` 淨 6 行同行改動（6 insertions／6 deletions），總行數 59171 不變，
  openLoc DEF 行 53690 不變——test_tang152／travel114／kwan151 釘行全部唔使 resync。
  新測試 `tests/test_tang171_static.py`（22 項）＋實駕 `qa171/drive171.py`（3 case）。
- **已落地**：遊戲 commit `6d08c7c`，線上 5,254,126 bytes sha `faebbd6a…` 已核實；落地紀錄見 §7。

## §1. C1——push 並存態最尾掣要碌先見（首屏冇提示）

### 問題（v169 review）
事務所地點板，要事區兩個 push 並存嗰陣成版掣總高 814px，超出 `#loc-acts` 可視高
（932：clientH 610；700：clientH 380）。首屏最尾一個掣「同何生傾談」完全喺摺線之下
（932 底 y988、700 底 y986）；碌得到（`#loc-acts` 係 `overflow-y: auto` 內滾），
但首屏冇明顯提示——最後可見掣「聽風聲」係完整嘅，下方直接係「未開放（1）」區，
中間冇半截掣做「下面仲有嘢」提示；12px scrollbar 唔顯眼。

### 修法選擇：acts 區底加淡出漸變（揀咗呢個）
- **揀淡出漸變，唔揀接受現狀**：用戶已拍板要修。
- **唔揀摺起「同何生傾談」等低優先掣**：會改掣可用性（撳多一下先見到掣），風險大；
  而家問題只係「唔知下面仲有嘢」，唔係「掣太多」。
- **唔揀加提示字（例如「下面仲有 ↓」）**：要改 DOM 結構（加元素＋定位＋隨捲動隱藏），
  blast radius 大過一個純 CSS 漸變。
- **唔揀收窄掣高／縮短卡片**：會整壞 v169 B2（兩卡各 h115、gap 7px、重疊 0 係修好狀態），
  唔值得為 C 級慳幾十 px 而郁 B 級修法。

### 實現（同行改動，零行數漂移）
1. CSS（append 入 L4832 v169 行）：`#loc-sheet.sheet.locpanel118 #loc-acts.loc-acts-more171::after`
   ——`position:sticky; bottom:0`，30px 高淡出漸變（透明 → `#f8f1de`，即係 acts 卡底色），
   `pointer-events:none`（唔攔點擊）、`z-index:5`（冚喺掣上面）。
2. 唔佔位：`margin-top:-30px` 抵消 30px 高；`margin-bottom:-7px` 抵消 `#loc-acts` flex
   row-gap 7px——實駕驗過：掛 class 前後 `scrollHeight` 同為 814，唔會多出捲動空間，
   亦唔會令捲到底嗰陣跳動。呢個 7px 耦合寫咗喺 CSS 註解＋靜態測試入面，之後改 gap 要一併改。
3. JS `window.syncLocActsFade171()`（append 入 L54434 resize 守門行，掛 `window` 等
   openLoc／scroll／resize 三處都讀到）：條件係 `scrollHeight > clientHeight + 4`
   而且 `scrollTop + clientHeight < scrollHeight - 4` 先掛 `loc-acts-more171` class；
   捲到底自動除返 class，漸變消失、最尾掣全見；內容唔超出可視高嗰陣唔掛 class，零視覺變化。
4. 呼叫點四處（全部同行 append）：openLoc 尾、openLoc 內 rAF（scrollTop 歸零之後）、
   `#loc-acts` scroll listener（接喺 resize 守門行，一次）、window resize handler。
   openLoc 係 acts 唯一渲染路徑，render 完即計一次；scroll／resize 兜底。

### 驗證（實駕數字，見 §4）
932＋700：首屏 `hasMore=true`、漸變 sticky 30px＋linear-gradient、最後可見掣「聽風聲」
半截＋淡出；捲到底 `hasMore=false`、「同何生傾談」全見、`scrollHeight` 814 前後不變；
捲返頂提示返嚟。B2 守門：兩卡 h115、gap 7px、重疊 0、badge 喺卡內橫排。

## §2. C2——鎖住態同可送態視覺上分唔到

### 問題（v169 review）
事務所「送禮：鄧麗萍」掣三態費用欄只係字唔同——「免費」／「今日已送」／「庫存空」
全部同一個紅色 `#c43c2a`、同一個 800 weight、同一個米色掣底；掣本身 `disabled=false`、
`aria-disabled` 無、`opacity: 1`，鎖住態完全冇變灰／變暗／變淡。

### 修法選擇：鎖住態掣身變灰（只做視覺區分，唔改點擊行為）
- **邊度加 class**：`add()` 入面，費用欄 `cost105` 係「庫存空」／「今日已送」嗰陣加
  `act-locked171`（同行 append 入 L53877 掣建立行）。呢兩個狀態字只由 `giftGateBadge()`
  出，唔會誤傷其他掣；而且一次過覆蓋晒所有送禮掣（鄧麗萍＋其餘 NPC 經
  `addLocTalkGiftActs` 嗰啲），唔使逐個 call site 加。
- **灰成點**：掣底 `#e6dfcc`（灰米）＋邊框 `#a89a7c`（灰），標題／hint `opacity:.72` 微淡；
  費用欄轉深啡灰 `#6b5636`（唔再係紅）。可送態（「免費」紅 `#C43C2A` 800 weight、
  米色掣底）一字唔郁。
- **對比度**：鎖住態費用欄 `#6b5636` on `#e6dfcc`＝**5.25:1**（靜態測試實算），
  高過 B1 實測 4.21:1 底線，唔會灰到讀唔到。揀呢隻深啡灰而唔係淺灰，就係為咗保住對比度。
- **唔用 `opacity` 成個掣變淡**：全掣 opacity 會將費用欄紅字同掣底一齊溝淡去場景圖底色，
  對比度跌穿 4.21:1；分開處理（掣底轉灰＋費用欄轉深色）先保得住可讀性。
- **唔用真 `disabled`**：`disabled` 會禁撳，toast 就唔會出，行為變咗（而家撳鎖住態會出
  toast 講原因，係 v169 已驗證嘅防線）。只做視覺區分：`disabled` 唔郁、`aria-disabled`
  唔加、click handler 唔郁、toast 唔郁。

### 驗證（實駕數字，見 §4）
三態 live 計算樣式：可送態無 `act-locked171`、費用欄紅 `rgb(196, 60, 42)`、掣底
`rgb(245, 230, 192)`；今日已送／庫存空態有 `act-locked171`、費用欄 `rgb(107, 86, 54)`
（＝`#6b5636`）、掣底 `rgb(230, 223, 204)`（＝`#e6dfcc`）、標題 opacity 0.72、
`disabled=false`；撳鎖住態出 toast（「人情急不來；今天先到這裡。」／
「庫存空空——可先去油麻地廟街禮品檔看看。」）可見。B1 守門：三態費用欄文字照啱。

## §3. 測試

### 新測試 `tests/test_tang171_static.py`——22/22 PASS
- C1（8 項）：淡出漸變規則存在（`loc-acts-more171::after`＋linear-gradient）、sticky＋
  30px＋`margin-top:-30px`＋`margin-bottom:-7px` 唔佔位、`pointer-events:none`、
  sync 函數存在＋條件啱、scroll listener 已接、openLoc 尾＋rAF 有呼叫（`syncLocActsFade171();`
  出現 ≥4 次）、B2 守門（flex 直欄＋`flex-shrink:0`、badge 仲係入文字欄）。
- C2（8 項）：`add()` 鎖住態加 `act-locked171`、鎖住態 CSS（灰米底＋灰邊框）、費用欄轉
  `#6b5636`、標題／hint 微淡 .72、對比度實算 **5.25:1 ≥ 4.5**、鎖住態嗰行冇加 disabled、
  點擊行為唔郁（送禮掣照 toast 原因）、B1 守門（known105 仲有「庫存空」「今日已送」、
  `giftGateBadge` 唔郁、可送態費用欄仲係紅 `#C43C2A` 800 weight）。
- 紀律（3 項）：SAVE key／softRev／`?v=` 不變、總行數 59171、openLoc DEF 行 53690 不變。
- 反證（pristine `56141a3` index，`/tmp/pristine171_index.html`）：**12 項新行為乾淨 FAIL、
  10 項守門 PASS、零 crash**（exit 1 係預期——新行為喺 pristine 唔存在）。
- 相關測試逐個直接覆驗（工作版）：`test_tang164_static`、`test_tang169_static`、
  `test_tang152_static`、`test_kwan151_static`、`test_travel114_static`、
  `test_kwan151_textfix.js`——全部 PASS。

### 全套 A/B
- 基線 pristine `56141a3`（`qa171/suite_baseline171.txt`）：**229 PASS／12 FAIL**。
  12 FAIL 係已知 pre-existing（flash51／giglib36／pacing35／poster59／rumor49／slot50／
  soft_tip_111_restore／start53／weave43／weave44／weave49／wrap38），同 v169 基線一致。
- 工作版（`qa171/suite_work171.txt`）：**230 PASS／12 FAIL**——基線 229／12，＋1 正好係新測試
  `test_tang171_static.py`；12 FAIL 同基線逐項相同（diff 核實過，得 TOTAL 行唔同），零回歸。

## §4. 實駕 `qa171/drive171.py`（本地鏡像＋完整 Chromium＋`xvfb-run -a`，port 8181）

- 開跑前驗明正身：served `index.html` 含 markers `applyTangGift169`／`syncLocActsFade171`／
  `act-locked171`／`loc-acts-more171`。
- **c1_932 PASS／c1_700 PASS**（push 並存態，`seed_deng_push_ready` → 播 push1「情報」→ 返事務所）：
  - 首屏：`scrollH 821`（掛 class 嗰陣；除 class 後 814，同 review 數字一致）vs `clientH 610／380`，
    `hasMore=true`，`::after` sticky／30px／linear-gradient／`pointer-events:none`；
    最尾掣「同何生傾談」932 底 y988／700 底 y986（摺線之下）；`#loc-acts` 內 8 粒掣
    （＋footer「返回地圖」＝review 講嘅 9 個）。
  - 捲到底：`hasMore=false`、「同何生傾談」全見（932 y729–784／700 y497–552）、
    `scrollH` 814 前後不變（::after 唔佔位）；捲返頂提示返嚟。
  - B2 守門：兩卡各 h115、gap 7px、重疊 0、badge 喺卡內橫排一行（settle 幾何）。
  - 目視：`c1_fade_932_top.png` 底緣淡出＋「聽風聲」半截淡出，提示做到。
  - 0 pageerror。
- **c2 PASS**（`seed_deng_meet_ready` → 播 meet → 送名筆 → 今日已送；另開 context 庫存空）：
  - 可送態：無 locked class、費用欄「免費」紅 `rgb(196, 60, 42)`、掣底 `rgb(245, 230, 192)`。
  - 今日已送態：有 `act-locked171`、費用欄「今日已送」`rgb(107, 86, 54)`、掣底
    `rgb(230, 223, 204)`、標題 opacity 0.72、`disabled=false`；撳落去 toast
    「人情急不來；今天先到這裡。」可見。
  - 庫存空態：有 `act-locked171`、費用欄「庫存空」同色同底；撳落去 toast
    「庫存空空——可先去油麻地廟街禮品檔看看。」可見。
  - 附帶：送名筆流程正常（「排片關係不變」結果句照舊）、B1 三態費用欄文字照啱。
  - 目視：`c2_sent_932.png` 灰掣同周圍紅「免費」掣一眼分到。
  - 0 pageerror。
- 證據：`qa171/drive171.json`＋`qa171/shots169/`（8 張：c1 兩高度頂／捲後各 1、c2 可送／已送／庫存空／送筆結果各 1）。
  註：截圖目錄名沿用 `shots169`（由 drive169.py 複製過嚟未改名），內容係 v171 新幀。
- 教訓跟足：播完 meet／push 先清 enc79 overlay 先截圖；「過一日」掣喺 modal 下面都讀到
  visible，唔當作「已返地圖」信號（用 `back_to_map` 嘅 modal／mask／overlay 三重判斷）；
  證據以 DOM 層為主，截圖只作目視輔助。

## §5. diff 摘要（`git diff`，6 行同行改動）

| 行 | 改動 | 點解咁改 |
|---|---|---|
| L4832（v169 行尾 append） | C1 淡出漸變 `::after` 規則＋C2 `act-locked171` 四條規則 | 唔寫入 `#loc-acts` 原規則行（LOCFULL120 9000 字元窗，v169 同一理由）；零行數漂移 |
| L53877 `add()` 掣建立行 | 鎖住態加 `act-locked171` | `cost105` 係最終費用欄字，只由 `giftGateBadge` 出呢兩個狀態字；同行改動 |
| L54434 resize 守門行 | `window.syncLocActsFade171` 定義＋scroll listener 接線 | 掛 `window` 避開 block-scoped function 宣告問題；開局跑一次就接好 |
| L54435 resize handler 行 | resize 嗰陣都 sync 一次 | viewport 變咗 acts 可視高會變，提示狀態要重計 |
| L54229 openLoc rAF 行 | scrollTop 歸零後 sync 一次 | rAF 嗰刻佈局已定，計出嚟準 |
| L54237 openLoc 尾 | 渲染完 sync 一次 | openLoc 係 acts 唯一渲染路徑 |

## §6. 殘留／唔郁

- v167 review C1（liked 肯定句＋金色「排片關係不變」並存）——用戶已拍板接受現狀，唔修。
- 咖啡豆句／push1 到唔到／玫瑰扣庫存——唔喺呢票。
- v170 典禮工作、v149——唔同範圍，唔掂。
- C1 淡出漸變同 `#loc-acts` flex row-gap 7px 有耦合（`margin-bottom:-7px` 抵消）：
  之後改 gap 要一併改呢個數，靜態測試＋實駕 `scrollH_stable` 釘住咗。
- 截圖目錄名 `qa171/shots169/` 係沿用舊名（內容係 v171 新幀），下次開新 drive 記得改名。
- 環境：開工嗰陣 `/tmp`（512M tmpfs）爆滿 100%，`git archive` 解 pristine 失敗；
  已清走舊 live 檔（`/tmp` 回到 21%），pristine 樹改放 `~/workspace/pristine171-tmp/`（用完可刪）。
  寫入 EPERM 今次全程冇出現；Chromium 全程穩定，0 pageerror。

## §7. rebase／落地紀錄（統籌填）

- 基底即係最新 main `56141a3`（遊戲 `1259ad8`），唔使 rebase；分支 `v20a171` HEAD `8272e46` 由工作副本推上常駐 clone 已核實。
- Squash merge 零衝突；合併樹重驗新測試 22/22＋`node --check` SYNTAX-OK；`git fsck --strict` 只有 dangling objects（正常）＋一條 `refs/heads/v20a170: invalid reflog entry 1ec53357…`（v170 分支 reflog 問題，唔影響 main／落地，留返 v170 嗰邊清）。
- 遊戲 commit `6d08c7c`；第一次 push 斷線（Broken pipe／remote hung up，egress proxy reset），重試一次成功（`56141a3..6d08c7c main -> main`）。
- 線上核實：5,254,126 bytes、sha256 `faebbd6a…`，同 `6d08c7c:index.html` 逐字一致（HTTP 200；Pages deploy lag 約 90 秒）。
- 落地後派 v171 設計 review（報告 `~/workspace/linji-design-review-v171/REVIEW.md`）。
