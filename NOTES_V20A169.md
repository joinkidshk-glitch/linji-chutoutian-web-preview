# v20a169 NOTES — v164 design review B1＋B2＋C1＋C2 修復

- 基底：main `5e6a6b0`（v20a168 遊戲 commit）。工作期間 main 郁咗兩次：v167 落地（遊戲 `280af68`）＋NOTES `fc1a1aa`；落實時要 rebase 上最新 main（試驗紀錄見 §5）。
- 範圍：用戶 2026-11-13 11:02 拍板修晒 v164 review（`~/workspace/linji-design-review-v164/REVIEW.md`，A 0／B 2／C 2）四項。**唔落地**：本票只做調查＋實作＋測試＋實駕＋NOTES，交統籌驗證＋落地。
- Diff：`index.html` **+44／−5**，全部同行改動（零行數漂移），除咗檔案尾新增 `applyTangGift169()` 一個函數；**唔使 resync 任何釘行測試**（kwan151／tang152／travel114 全部原樣 PASS）。

## §1 B1 — 送禮掣費用欄「免費」同實際狀態矛盾（修法：加返入 `known105` 清單）

- 根因已核實：`giftGateBadge()`（L56996）回傳 `庫存空`／`今日已送`，但 `add()` 嘅 `known105` 清單（L53782）冇呢兩個字串 → 被當 flavor 移入 hint 行，費用欄跌返 `免費`；庫存空態「庫存空」四字更因 hint 已含「庫存空空」子串被 dedup 丟失。
- 修法（一行，同行改動）：`known105` 加 `"庫存空","今日已送"`。
- 棄用方案：將 gate badge 渲染喺費用欄以外——改動面大，收益同加清單一樣。
- 實駕驗證（§4）：有庫存 `免費`＋hint「不耗日 · 只用今日送禮次數」；已送 `今日已送`；庫存空 `庫存空`＋hint「庫存空空——可先去油麻地廟街禮品檔看看。」

## §2 B2 — 要事區兩張 push 卡重疊（pre-existing v152，唔係 v164 回歸）

修法（三部分，全部同行改動，零行漂移）：
1. **badge 入文字欄**：`ux68OrganizeLocSheet()`（L32201）由 `it.btn.appendChild(s)` 改做 `(it.btn.querySelector(".act-txt118")||it.btn).appendChild(s)`——badge 由 `.act` 嘅 row flex 第 4 個 item（被擠到 min-content 闊度變 7 行直欄、縱跨兩卡），改為簡介之下橫排紅字（`w 227 h 17`，一行）。
2. **容器由 grid 轉 flex 直欄**：`#loc-sheet.sheet.locpanel118 #loc-acts{ display:flex !important; flex-direction:column !important; }`，寫喺 `.ux68-why` 行旁邊（唔寫入 `#loc-acts` 原規則行——原因見下文 locfull120 陷阱）。
3. **掣唔縮**：`#loc-sheet.sheet.locpanel118 #loc-acts .act{ flex-shrink:0; }`——容器唔夠高嗰陣改內滾，唔壓縮卡高。

### 點解淨係搬 badge 唔夠（實駕揭發嘅第二層根因）

- 第一輪實駕（只搬 badge）：badge 橫排入框，但兩卡仍然 h=50、badge y 346–363 跌出卡外（卡 292–342）。Live probe 證實：`#loc-acts` 係 `display:grid`，`.act` 預設 `align-self:stretch`，卡被夾喺約 50px 行高；文字欄實測 91px（簡介＋badge），掣 `scrollHeight` 68 vs `clientHeight` 46——內容溢出框外。純 DIV clone 同樣約 48px，證實唔係 `<button>` 元素 quirks。
- 機制：grid auto 行高跟 **max-content** 計——max-content 排版唔換行，長簡介單行計出嚟只係約 50px；實際闊度 338px 嗰陣文字換行要 115px，但行高唔會跟住長。
- `align-self:start` 都唔夠（試過）：掣本身回復 115px，但行高照舊 50px、兩卡 y 距照舊 57px（50＋7 gap）→ 依然重疊（gap −58）。根治一定要改容器：flex 直欄令卡高＝內容高。
- 實測（probe_b2d，flex 直欄＋flex-shrink:0）：重疊前 `黃金檔期之爭 after 午夜場後的試探`；修後零重疊，兩張 push 卡各 115px、全闊 338px，其餘掣按內容高 55–68px（送禮掣庫存空態 hint 兩行 → 68px，都係內容高，唔再被夾），間距 7px 保留。

### locfull120 陷阱（中途發現，已經修好）

- 第一版將 `display:flex` 寫入 `#loc-acts` 原規則行（L3727）嗰陣，全套跌到 226／13——`test_locfull120_static.py`「素底態：深色字＋冇暗角」FAIL。
- 根因：`block_of("v20a120 LOCFULL120", length=9000)` 用固定 9000 字元窗切段；我嗰段長註解（約 180 字）喺窗內，推走窗尾 `.locpanel118-nobg #loc-title`／`text-shadow:none` 規則。**教訓：唔好喺 LOCFULL120 段內加長註解。**修法：flex 規則搬去 `.ux68-why` 行（L4832，窗外），`#loc-acts` 原規則行還原 pristine，全套返返 227／12。

## §3 C1 — 名筆 `:liked` 第一句疑似筆誤（修法：改字，唔重寫）

- 出處已核實：`content/gift_react_copy.json`，`byKey` `tang:gift_fountain_pen:liked` 同 `entries` id `GR-tang-pen｜liked`（`｜`＝U+FF5C，byte-verified）兩份同一句：`…你至少知道我不是靠感人情書辦事的人。`TEXTFIX55 冇呢句嘅映射；新句唔含 TEXTFIX 觸發字。
- 新句全文（只改呢句其餘一字唔郁）：
  `鄧麗萍：「名筆。簽名、批檔期、改數字，都用得着。你至少知道我不是靠感情、靠人情辦事的人。」`
  ——跟 review 建議字眼；第一句「名筆。簽名、批檔期、改數字，都用得着。」同第二句「謝謝…」不變，鄧麗萍公事、講數字口吻不變。
- 做法：唔直改 content pack JSON。新 `applyTangGift169()` 載入正規化覆寫 `byKey`＋`entries` 兩份（pack 入面同一句出現兩次，兩邊一齊改，否則 `reactionEntry`（行 byKey）同 entries 掃描唔一致）；只喺現句含「感人情書」嗰陣先改——pack 日後已修正就唔會俾呢度覆寫返。
- 呼叫點：`refreshCopyPacksFromDisk` 嘅 `GiftShop.ensureSave()` 行（同行 append，零行漂）。一定要喺 `GIFT_REACT` 賦值之後、`textfix55Walk(giftReact)` 之前；揀呢行唔揀 `GIFT_REACT` 賦值行，係為避開 v167 喺嗰行掛嘅 `applyTangGift167()` 呼叫。

## §4 C2 — 四件新貨排商店 list 第 11–14 位（修法：置頂，唔分組）

- 機制已核實：`shopList()` 按 `shop.stock` 陣列次序渲染；`applyTangGift164()` 將四件新貨 append 到第 11–14 位。
- 修法：`applyTangGift169()` 將四個 itemId 穩定移到 `shop_street_mk` stock 陣頭（次序：名筆／計數機／腕表／玫瑰；其餘 10 件相對次序不變）；冪等（已經係頭四位就唔郁）。只係顯示次序：`restockIfNeeded()` 由 stock 陣逐行建 `shopStock` 字典，count 不變；舊檔 shopStock 字典本身唔受影響。
- 棄用方案：分組（「排片部實用」）——商店 modal 係扁平 rows，分組頭要改 render；hint 講明要碌落去——唔解決問題。置頂最簡單直接。

## 測試

- 新 `tests/test_tang169_static.py`：**29/29 PASS**（B1 三態費用欄、B2 badge 入文字欄＋flex 直欄＋flex-shrink:0＋闊度不變、C1 新句＋pack guard＋v167 範圍 guard（`gift_coffee_beans` 唔喺 C1／C2 路徑）、C2 置頂＋count／restock 不變、紀律）。
- 反證（pristine `5e6a6b0`，`git show 5e6a6b0:index.html`）：**14 FAIL**（13 項新行為斷言＋1 項 flex 斷言），無 crash。其中 1 項 PASS 係空洞（`textfix55Walk` 次序檢查喺 pristine 搵唔到 -1）——同 tang164 已記錄嘅空洞 PASS 同一個模式，有實質 hook 斷言配對。
- 相關測試全 PASS，零 resync：tang164、tang152、travel114（＋logic）、kwan151、ux68、locpanel118、target74、icons112 static＋logic、locfull120。
- 主 script `node --check` SYNTAX-OK。

## 全套 A/B（`qa131/run_suite.sh`）

- 基線：pristine 樹 `~/workspace/pristine169-tree`（git worktree，detached @`5e6a6b0`，238 個測試檔）→ **226 PASS／12 FAIL**，`qa169/suite_baseline169.txt`。
- 工作版（最終樹）→ **227 PASS／12 FAIL**，`qa169/suite_work169.txt`。FAIL 集合兩邊完全相同：flash51、giglib36、pacing35、poster59、rumor49、slot50、soft_tip_111_restore、start53、weave43、weave44、weave49、wrap38（全部 pre-existing）。工作版＝基線＋1（新測試檔），零回歸。
- 註：v168 NOTES 寫同一 commit 係 224／12，但實測基線係 226／12；以實測數字為準。
- 中途插曲：第一版 flex 規則寫錯位嗰陣全套曾經跌到 226／13（locfull120，見 §2 陷阱），搬位後返返 227／12。

## 實駕（`qa169/drive169.py`，結果 `qa169/drive169.json`，截圖 `qa169/shots169/` 7 張，md5 全部唔同——新鮮幀）

- 工具：Playwright venv `/home/hatch/pwenv49/bin/python`；完整 Chromium（headed，`xvfb-run -a`——直接 headed 啟動無 X server 會失敗；headless_shell 截圖有殘影，DOM 係主要證據）。種子：`seed_deng_meet_ready`（播 meet，揀 data 選項「遞上」）、`seed_deng_push_ready`（自動播 push1，揀「情報」）。
- **全部四 case PASS，0 pageerror**：
  - **b1 PASS**：有庫存費用欄 `免費`＋hint「不耗日 · 只用今日送禮次數」；已送 `今日已送`；庫存空 `庫存空`＋hint「庫存空空——可先去油麻地廟街禮品檔看看。」；送名筆結果含新句、無「感人情書」、rel_tang 維持 1、名筆庫存 2→1。
  - **b2_932 PASS**：兩卡 y 292／414、各 h 115、gap 7；幾何檢查 10/10（卡夠高、badge 喺卡內、橫排、喺 `.act-txt118` 內、文字啱、兩卡唔重疊、間距 ≥5、**全版可見掣唔重疊**）；settle 後＋1s 再探針，幾何穩定。
  - **b2_700 PASS**：同上，y 290／412、各 h 115、gap 7、10/10。
  - **shop PASS**：商店次序 `[pen, calc, watch, rose, pineapple_bun, egg_tart, …]`（14 行）；買名筆 $550，錢 −550。
- HTTP 404 全部係 `rom_tang_meet_soft_hold` artId 探針（12× .jpg／.png × 多路徑，24 個 distinct）——pre-existing，v164 review 已觀察到，唔係回歸。
- 廢棄 run：run 2 用咗一個已經喺 port 8169 監聽緊嘅外來 server（serve 緊 pristine build，全部 fix 唔見晒），中途仲死埋連線——數字作廢。drive 而家用專用 port **8179**，一定自己起 server，開跑前斷言 served `index.html` 含 markers `applyTangGift169`、`flex-shrink:0`、`今日已送`（呢個檢查喺 flex 規則搬位嗰陣捉到我自己 marker 未同步更新——已修）。

## §5 Rebase 試驗（scratch worktree，唔掂交付分支）

- 目的：main 喺我開工期間由 `5e6a6b0` 郁到 `fc1a1aa`（v167 遊戲 `280af68`＋NOTES `fc1a1aa`），落地要 rebase；預先喺 scratch 試一次，記錄衝突同解法。
- 做法：`git worktree add -b scratch169 ~/workspace/scratch169-rebase 5e6a6b0`，將工作版 `index.html`＋`tests/test_tang169_static.py`＋`qa169/` 抄入，commit 做 trial commit `7e127d3`，`GIT_EDITOR=true git rebase main`（main＝`fc1a1aa`）。
- 結果：**2 個衝突，全部喺 `index.html`**（其餘檔順利套用）：
  1. **Loader 行**：v167 喺 `GIFT_REACT` 賦值行掛 `applyTangGift167()`；v169 喺 `ensureSave()` 行掛 `applyTangGift169()`。解法：兩邊呼叫都保留——`GIFT_REACT` 行 keep 167 呼叫，`ensureSave()` 行 keep 169 呼叫。次序啱：167 緊接賦值之後，169 喺 ensureSave 之後，兩個都喺 `textfix55Walk(giftReact)` 之前。
  2. **檔案尾函數**：v167 同 v169 都喺 `applyTangGift164()` 閉括號之後加一個新函數（同一插入點）。解法：兩個函數都保留，167 行先、169 行後（時序＋呼叫次序一致）；兩個函數共用同一段收尾（`    }`／`  }catch(_e){}`／`  return 1;`／`}`），每人一份。
- **陷阱（已踩中、已修好）**：我用 Python splice 解衝突嗰陣漏咗一個換行，`ensureSave()` 行同下一行 `/* v20a55 TEXTFIX … */` 註解併咗同一行，令之後全部行號 −1，`tang152` 釘行 L31531 變咗 L31530 而 FAIL。修法：補返換行做 fixup commit `fad34b4`，L31531 歸位，tang152 返 PASS。**落地 rebase 嗰陣要逐行對返行號，唔好信 splice 表面成功。**
- 驗證（rebased 樹，commit `fad34b4`）：`node --check` SYNTAX-OK；tang152／tang167／tang169／tang164／locfull120／travel114／kwan151 全 PASS；**全套 228 PASS／12 FAIL**（＝基線 226／12＋tang167＋tang169，FAIL 集合同基線完全相同，零回歸）。
- 殘留：合併後 167 函數收尾有 `}    }` 併同一行（syntax 正確，純粹醜）——scratch trial 專用，落地 rebase 嗰陣順手拆返兩行。
- Scratch 已刪除（`git worktree remove --force`＋`git branch -D scratch169`）。

## §6 落地 rebase 紀錄（統籌，2026-11-13）

- 落地嗰陣 main 已經由工人基底 `5e6a6b0`（v168）郁到 `9b95de0`（v165 NOTES；遊戲 `b754fac`，線上 5,247,634 bytes sha `dcb32841…`——v165 劇情強制播放已落地）。Rebase 目標係 `b754fac`（NOTES commit 只加 NOTES，遊戲內容同 `b754fac` 一致；`git rebase origin/main` 嗰陣 `onto` 驗證過係 `b754fac0ceefa65b857a857cdc1851f16ad9aae4`）。
- 衝突 2 處，全部喺 `index.html`，同工人 §5 試驗相同（試驗基底係 `fc1a1aa`，實際落地基底係 `b754fac`，衝突位一樣）：
  1. Loader 行：167 呼叫留喺 `GIFT_REACT` 賦值行、169 呼叫留喺 `ensureSave()` 行，兩邊都保留。
  2. 檔尾函數：167＋169 兩個完整函數都保留（167 行先、169 行後），成段原文分別由 `HEAD`（`b754fac`）同 `1bbc29a` 抽出；**冇出現 `}    }` 併行**（已驗證唔存在）。工人試驗踩過嘅換行陷阱今次冇再出現（tang152 釘行 L31531 驗證 PASS）。
- Rebased 樹驗證（全部喺最終樹跑）：
  - `node --check`：兩個 inline script block 全部 OK（主 script 4,303,757 bytes）。
  - 相關測試全 PASS：tang169／tang167／tang164／tang152／locfull120／travel114／kwan151。
  - 全套 A/B：基線 pristine `b754fac` **228／12** vs 工作版 **229／12**，FAIL 清單逐項對過完全相同，零回歸。工作版 229＝基線 228＋tang169（`test_story165_static.py` 係 rebased 基底 `b754fac` 本身已有，唔係 v169 新增）。
  - 實駕 `drive169.py`（rebased 樹重跑，`xvfb-run -a`）：b1 28/28、b2_932 19/19、b2_700 19/19、shop 16/16，全部 PASS，0 pageerror。
- 中途插曲：①第一次跑全套嗰陣 outfile 用咗相對路徑，`run_suite.sh` 會 `cd` 入 repo 根目錄，寫檔失敗（`No such file or directory`），得總數冇清單；已用絕對路徑重跑（`qa169/suite_baseline169_b754fac.txt`／`qa169/suite_work169_rebased.txt`）。②實駕第一輪唔用 `xvfb-run`，完整 Chromium headed 啟動失敗（Missing X server）；按 NOTES 用 `xvfb-run -a` 重跑。

## 環境備註

- 10:48–11:00 VM 寫入間歇性 EPERM 惡化（brief 有講）；開工探針（/tmp＋workspace＋`git hash-object -w`）全部正常，成個工作期間寫入零問題。
- `/tmp` 係 512M tmpfs，repo `.git` 1.2G——`git clone` 入 `/tmp` 會「No space left on device」；基線用咗 persistent disk 上嘅 `git worktree`（`~/workspace/pristine169-tree`，用完可刪）。
- Chromium：完整版經 `xvfb-run -a` 先起得返；headless_shell 截圖有殘影，唔可以當唯一證據。

## 唔郁（跟 brief）

- 咖啡豆 `:liked` 句——v167 範圍（佢而家係兩句，見 MEMORY 更新）；本票只係 guard 唔掂佢。
- push1 live 到唔到（pre-existing，送禮刻意唔補 rel_tang 缺口）。
- 玫瑰 dislike 照扣庫存（通用機制）。
- Ok-state `不耗日`→`免費` 映射（UI105 S-23 已有決定）。
- SAVE key（`starVolunteer_map_v19w`）、softRev、產品 `?v=`、content pack JSON 唔郁。

## 殘留／未決

- v167 review C1（11:37 出咗，A 0／B 0／C 1）：liked 肯定句＋金色「排片關係不變」並存，新玩家可能唔明「讚完都唔郁，咁送嚟做咩」——係 v164 設計延續，唔係 v167 引入。**用戶 2026-11-13 11:42 拍板接受現狀，唔修。**唔係本票範圍。
- 本票交付分支基底仍然係 `5e6a6b0`；落地嗰陣按 §5 試驗結果 rebase 上最新 main（記得補換行陷阱檢查＋逐行對行號）。
