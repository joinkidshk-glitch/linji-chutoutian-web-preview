# NOTES v20a185 — 修 v183 review 新 B1＋C1（送禮選擇器 700 遮擋＋「×N」孤兒行）

- 基底 main `01ddcaa`（v183 NOTES；live v183，5,329,880 bytes sha `9890d43e…`）
- 分支 `v20a185`，工作副本 `~/workspace/linji-work185/`；**唔落地**（工人只做實作＋驗證＋commit＋push 分支）
- 範圍：淨係修呈現層（modal 幾何＋卡片換行）。唔改 SAVE key（`starVolunteer_map_v19w`）、softRev（`s107`）、`?v=`（`v20a10`）；唔郁 `content/` pack JSON；唔郁頒獎禮舞台 code；唔改鎖邏輯／rel／fav 數值。

## 1. 改動清單（淨 2 行 index.html 改、0 行加減）

| 檔 | 改動 |
|---|---|
| `index.html` L3850 | v183 C7 media query 行後追加 v185 規則（同一行，零淨行數）：`#gift-pick-list .act{ min-width:0 }`＋`.n` 行 flex＋`.gift-pick-name` ellipsis／nowrap＋`.gift-pick-count` nowrap＋`.ic112` 唔縮 |
| `index.html` L58596 | `openGiftPick` row 模板：卡名入 `<span class="gift-pick-name">`、數量入 `<span class="gift-pick-count">×N</span>`，舊裸 `${item.name} ×${count}` 清走；偏好標記行／「選」掣／icon 呼叫唔郁 |
| `tests/test_gift185_logic.js`（新） | 抽真 row 模板 literal 評值＋v185 CSS 規則斷言，20 項 |
| `tests/test_gift185_static.py`（新） | 靜態斷言（紅線／CSS／模板／作用域／零淨行數），19 項 |
| `tests/test_icons112_static.py` L58 | `render gift give` 期望字串跟返新模板（icon 呼叫本身唔郁，淨係包多層 span；見 §5） |

- 總行數 60127 不變（`git diff --numstat` 2+/2-），kwan151／tang152／rom176 行號釘全部唔使 resync（suite 已證實三檔全 PASS）。

## 2. 修法選擇：路線 (a)——卡片矮返，一眼全見，唔靠碌

- **B1 揀 (a)**，唔係 (b)。原因有二：
  1. **C1 修正本身已經令卡片矮返**：名由 2 行變 1 行（38→20px），卡片 85→67px，list 443→351px，尾行 bottom 659→585，已經清過取消掣欄頂（605–614），有 20–29px 裕度。唔使再加 bottom padding／改 scroll 行為。
  2. **(b) 嗰條路其實一直都通**：實測 `qa185/probe185_geom.py` 證實 review「碌唔郁」只係量錯元素——`#gift-pick-list` 本身 `scrollHeight == clientHeight == 443`（佢唔係 scroller），但上層 `#modal-inner` 係 `overflow-y:auto`，`scrollHeight 513 ／ clientHeight 439`，最大 scroll 74px；碌到底之後尾行 bottom 659→585，10 張中心點＋「選」全部命中。但靠用戶自己發現「呢個 modal 入面可以碌」唔係修好，(a) 一眼全見先係正路。修完之後 modal-inner 已經唔使碌（`scrollHeight == clientHeight == 421`）。
- **C1 修法**：名 span `flex:1 ＋ min-width:0 ＋ overflow:hidden ＋ text-overflow:ellipsis ＋ white-space:nowrap`，數量 span `flex:0 0 auto ＋ nowrap`。名＋×N 永遠同一行，唔會有孤兒數量行。

### 實作途中捉到嘅第二個 bug（已一併修）

- 第一版淨加 ellipsis，未加 `.act min-width:0`：`white-space:nowrap` 令名 span 嘅 min-content 變成全名闊度，grid 軌 `1fr ＝ minmax(auto, 1fr)` 撐闊——左欄卡 212px、右欄卡 173px，成個 grid 393px 闊過 list（342px），右欄伸出 modal 外（x 去到 437），右欄 5 張「選」掣中心點 `elementFromPoint` 命中 `BODY`（撳唔到）。加 `#gift-pick-list .act{ min-width:0 !important; }` 之後兩欄均等 167px，10 張「選」全部命中 `DIV.cost`。見 `qa185/probe185_cost.py` 前後對照。

### 幾何（700，430×700，女角選擇器）

|  | 修前（review probe_c7.json＋我覆核） | 修後 |
|---|---|---|
| 卡片高 | 85px（名 2 行 38px＋.h 2 行 30px） | 67px（名 1 行 20px） |
| list | top 216／bottom 659／高 443 | top 234／bottom 585／高 351 |
| 取消掣欄頂 | 605–614（兩次量度有 ±9px 浮動） | 605–614（唔郁） |
| 尾行 bottom vs 掣欄頂 | 659 ＞ 614，遮 45px | 585 ≤ 605，清 20px（drive run 掣欄頂 614，清 29px） |
| 尾行中心點命中 | `DIV.btnrow`（遮住） | 卡片本身（10/10） |
| 尾行「選」中心點命中 | `DIV.btnrow`／`BUTTON.g`（遮住） | `DIV.cost`（10/10） |
| modal-inner scroll | 需碌 74px 先見尾行 | 唔使碌（scrollH＝clientH＝421） |

- 星選擇器 700：尾行 bottom 587 ≤ 掣欄頂 614（清 27px），10/10 命中；長 sub 行（3 行）都 fit。
- 932 對照：單欄 list 可碌係正常，唔郁。碌到底後尾行 bottom 813 ≤ 掣欄頂 850（女角／星一致），尾行「選」命中。

### 已知取捨：名 ellipsis 截斷（寫低，唔係漏驗）

- 700 兩欄卡片名 span 得 85px 闊：10 件入面 6 件名被截（`scrollWidth ＞ clientWidth`）：菠蘿油＋奶茶券（91）、實用不銹鋼保溫瓶（104）、採訪用空白拍紙簿（104）、蘭芳咖啡豆小包（91）、原創卡帶（獨立樂隊）（130）、海外時裝雜誌合訂（104）；其餘 4 件全見。
- 截後每件剩返頭 5–7 字＋「…」，件件之間仍然分得開（例：「原創卡帶（獨立…」）；撳入確認 modal 會顯示全名（「把「原創卡帶（獨立樂隊）」送給…」）。C1 驗收只係要求「名＋×N 同行、唔准孤兒行」，呢個取捨符合驗收；想全名唔截要改版面（例如「選」掣移到底行），嗰個係另一票。

## 3. 新測試

- `tests/test_gift185_logic.js`：**20/20 PASS**。抽 `openGiftPick` 真 row 模板 literal，用 stub（最長名「原創卡帶（獨立樂隊）」＋「實用不銹鋼保溫瓶」）評值，驗渲染 HTML 有名／數量 spans、次序、冇裸「名 ×N」、有「選」掣；另驗 v185 CSS 規則在位＋C7 兩欄原封不動。
- `tests/test_gift185_static.py`：**19/19 PASS**。紅線（SAVE／softRev／?v=／總行數 60127）＋B1／C1 CSS＋模板 spans＋舊裸字串清走＋作用域鎖喺 `#gift-pick-list`（禮品店 list 唔郁）。

### 反證（pristine main `01ddcaa`，單檔抽取 `/tmp/pristine185.html`，唔 full clone）

- logic：**14 FAIL**（8 項 spans／結構＋6 項 CSS／標記，扣起「選」掣／C7 兩欄嗰 3 項照 PASS——證明新斷言針對 v185 改動，唔係乜都 FAIL），exit 1，唔 crash。
- static：**10 FAIL**（B1／C1 全部＋作用域），紅線／C7 舊斷言照 PASS，exit 1，唔 crash。
- 證據：`qa185/counter_logic_pristine.txt`、`qa185/counter_static_pristine.txt`。

## 4. 全套 A/B（`qa131/run_suite.sh`）

- Pristine 基線（worktree `01ddcaa`，`/tmp` 係 512M tmpfs 唔 full clone，worktree 用完已刪）：**246 PASS／12 FAIL**。
- 工作版第一跑：**247 PASS／13 FAIL**——多咗 `test_icons112_static.py`（佢咬死舊模板字串 `${iconHtml112(...)} ${item.name}`，見 §5）。
- 修 icons112 期望字串後第二跑：**248 PASS／12 FAIL**（+2 正好係兩份新測試）。
- **FAIL 清單逐項相同**（pristine vs 工作版 diff 零差異）：`test_flash51_static.py`、`test_giglib36_static.py`、`test_pacing35_static.py`、`test_poster59_static.py`、`test_rumor49_static.py`、`test_slot50_static.py`、`test_soft_tip_111_restore.py`、`test_start53_static.py`、`test_weave43_static.py`、`test_weave44_static.py`、`test_weave49_static.py`、`test_wrap38_static.py`——全部係已知 12 項穩定 FAIL，**零回歸**。
- 相關測試逐個直接覆驗：gift185 logic／static、rom183 logic／static、rom176 logic／static、icons112、kwan151、tang152 全部 PASS。
- 證據：`qa185/suite_pristine185.txt`、`qa185/suite_work185.txt`（247/13 第一跑）、`qa185/suite_work185b.txt`（248/12 定版）。

## 5. icons112 嗰項 FAIL 係乜（已修，唔係回歸）

- `tests/test_icons112_static.py:58` 斷言 `'${iconHtml112(item.emoji||"🎁")} ${item.name}' in html`。v185 將 `${item.name}` 包入 `<span class="gift-pick-name">`，字串唔再連續。
- icon 呼叫本身一字唔郁（同一位置、同一參數），只係包多層 span 做 ellipsis——測試意圖（「give 行有用 iconHtml112 渲染」）仍然成立，所以更新期望字串為新模板字串＋加 v185 註解，唔係放寬斷言。修後 icons112 全 PASS。

## 6. 實駕（Playwright，`qa185/drive185.py`，本地鏡像＋http.server，唔直連 github.io）

4 case 全 PASS，0 pageerror。證據 `qa185/drive185.json`＋截圖 `qa185/*_430x700.png`／`*_430x932.png`。

| case | checks | 關鍵數字 |
|---|---|---|
| woman_700（林曉晴） | 12/12 | 10 行全命中（卡片＋「選」）；尾行 bottom 585 ≤ 掣欄頂 614；名全部 1 行；尾行「選」真滑鼠點擊 → 確認 modal「淡香水試用裝」→ 送出 → 結果「好感 +1」，rel 0→1 |
| woman_932 | 12/12 | 單欄可碌（scrollH 710＞clientH 617）；碌到底尾行 bottom 813 ≤ 850、尾行全命中；尾行「選」實撳送出＋1 |
| star_700（廖炳星，ENC79 播完對話先開板） | 17/17 | 尾行 bottom 587 ≤ 614；10/10 命中；名 1 行；「★ 最愛」標記完整；尾行「選」實撳 → 確認 modal 有 dislike 預警句 → 送出 → 結果「好感 -1」（淡香水對廖炳星係 dislike，-1 先啱） |
| star_932 | 17/17 | 同 932 對照，碌到底尾行 813 ≤ 850，實撳送出 -1 |

- 932 第一眼尾行喺摺疊下面係正常 modal 行為（drive 會碌到底再驗，唔當 FAIL）；700 係一眼全見，唔使碌。
- 截圖以 DOM 量度為準（headless_shell 有 stale frame 殘影可能）；`woman_pick_430x700.png`／`star_pick_430x700.png` 目視：5 行全見、尾行「選」清晒、×3 全部同名一行、冇孤兒行。

## 7. 其他驗證

- 主 script `node --check`（抽兩段 inline script 合併驗，Node 24 拒 `.html`）：**PASS**。
- `node tests/test_gift185_logic.js`／`python3 tests/test_gift185_static.py` 工作版全過（見 §3）；`test_rom183_*` 全過（C7 兩欄意圖未郁）。

## 8. 殘留

- §2 尾段：6 件長名 700 下 ellipsis 截 1–3 字（確認 modal 有全名）。如用戶覺得截名唔接受，另開票改版面（例如「選」掣移到底行），唔喺呢票再擴範圍。
- 700 下取消掣欄頂喺 605–614 之間浮動 ±9px（兩次量度）；修後尾行 bottom 585，裕度 20–29px，覆蓋浮動。
- Review 方法學註記已應驗：呢次新測試用 `elementFromPoint` 命中＋尾行 bottom ≤ 掣欄頂，唔再淨係 `row.bottom <= 700`。

## 9. Rebase 上 v184 main＋重驗（2026-11-13，工人重驗，唔落地）

- 新基底：常駐 clone main `77603b3`（v184 NOTES；遊戲 `454ed8e`）。開工嗰陣 `git fetch origin` 核實過，main 冇再郁（v181 未落地）。
- Rebase：`GIT_EDITOR=true git rebase origin/main`，**零衝突**，兩個 commit 原樣搬上（遊戲 `6c05b98`、NOTES `c5690d5`）。v184 改頒獎禮提名卡 tint＋請柬排序，同 gift picker 唔同面，預期一樣。
- v184 基底改動：`index.html` 淨 +16 行（60127→60143；三個 hunk：L45748 +10、L45768 +1、L46468 +5，全部喺 awards 區）。v185 本身對新基底仍然淨 0 行（`git diff 77603b3..HEAD -- index.html`：+2/−2）。
- Resync 清單（逐檔 difflib 對位核實，唔係 blanket replace）：
  - `tests/test_gift185_static.py`：唯一要改——總行數斷言 60127→**60143**（v184 加咗 16 行，v185 零淨行數不變；註解同步更新）。其餘斷言全部字串匹配，唔受行號影響。
  - kwan151／tang152／rom176／text125／travel114／tang171／tang173：逐個直接跑全部 PASS（見下），**零漂移、唔使 resync**——v184 自己已 resync 咗佢郁過嗰幾檔（rom176／tang171／tang173／travel114），其餘檔釘嘅位置喺 v184 hunk 之前。
- 新測試（重跑）：`test_gift185_logic.js` 20 項 ALL PASS；`test_gift185_static.py` 19 項 ALL PASS。
- 相關測試逐個直接跑（全部 PASS）：rom183 logic＋static、rom176 logic＋static、icons112 logic＋static、menu72 logic＋static、kwan151 static＋textfix、tang152 static、text125 logic＋static、travel114 logic＋static、tang171 static（22/22）、tang173 static（21/21）。
- 主 script `node --check`（兩段 inline script 各自驗）：**PASS**。
- 全套 A/B（`qa131/run_suite.sh`）：工作版 `qa185/suite_work185_rebase.txt` **249 PASS／12 FAIL**；pristine（`git archive 77603b3` 抽出，log 寫去 workspace scratch——`/tmp` 滿咗 512M，用唔到）`qa185/suite_pristine185_rebase.txt` **247 PASS／12 FAIL**。FAIL 清單逐項相同（flash51／giglib36／pacing35／poster59／rumor49／slot50／soft_tip_111_restore／start53／weave43／weave44／weave49／wrap38，12 項穩定 pre-existing）；工作版多 2 PASS 正好係兩份新 gift185 測試。**零回歸。**（舊基底數字：pristine 246/12、工作版 247/13——嗰陣多 1 FAIL 係 icons112 測試更新前嘅數字，rebase 後已唔存在。）
- 實駕重跑（`qa185/drive185.py all`）：**4/4 PASS，0 pageerror**——woman_700 12/12、woman_932 12/12、star_700 17/17、star_932 17/17。關鍵數字同 rebase 前逐項相同：700 尾行 bottom 585（woman）／587（star）≤ 掣欄頂 614；932 碌到底尾行 813 ≤ 850；`qa185/drive185.json` 重跑後 byte-identical（git 無改動），截圖 10 張有更新（渲染差異）。
- Commit＋push：本節寫入 NOTES 後 commit，`git push --force-with-lease origin v20a185`（origin 係常駐 clone 本地路徑，唔推 GitHub），再 `git ls-remote` 核實。
