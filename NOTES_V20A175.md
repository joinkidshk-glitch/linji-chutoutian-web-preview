# NOTES_V20A175 — 修 v153 review C1＋C2

工作副本 `~/workspace/linji-work175/`，分支 `v20a175`，基底 main `a618a5d`（v174 NOTES；遊戲 `e2add29`，線上 5,269,914 bytes sha `3af45a51…`）。
用戶 2026-11-13 14:14 拍板修晒 v153 review 嗰兩項 C 級。**本票唔落地**（落地由統籌做，唔 push）。
報告來源：`~/workspace/linji-design-review-v153/REVIEW.md`（結論 A 0／B 0／C 2）。

## §0 總覽

| 項 | 修法 | 驗收結果 |
|---|---|---|
| C1 | 開放行 note 刪「已經開放——」四隻字，變「返地圖嗰陣就會播出。（場景：…）」；tag 嗰粒「已開放」保留 | C17／C18 行「已開放」各得一次（tag），note 唔再重複；932＋700 DOM＋截圖雙重確認 |
| C2 | 開頁嗰陣仲生效嘅全域 toast 收容做進度頁頂部 in-flow banner（`.prog175-banner`，`.prog71-wrap` 第一個仔，將 list 向下推）；toast() 喺進度頁開住嗰陣觸發亦直接行 banner；1.8 秒後平滑收起（max-height／opacity 過渡）再移除 | 932＋700 各 8 次開頁全 PASS：overlay `#toast` 全程熄、banner 靜態置頂、行 14–15 elementFromPoint 命中行本身、banner 同行 14–15 零相交；live-fire 兩尺寸都 PASS（`#toast` 全程 0 次著）；0 pageerror |

改動：`index.html` 淨 ＋78 行（C2 banner CSS ＋10／toast() 分流 ＋15／prog175 helpers ＋51／render adopt ＋2；C1 同行改 0 淨行）＋新測試 1 檔＋6 檔舊測試 resync（釘行漂移，見 §5）。
全套（第二次 rebase 後重驗，基底 `a41b789`，見 §4／§8）：pristine `238／12` → 工作版 **`239／12`**（＋1 係新測試，12 項穩定 FAIL 同一批，零回歸）。
實駕：`qa175/drive175.py`，C1 932＋700、adoption 8/8＋live-fire 1/1 兩個尺寸，**全部 PASS、0 pageerror**。

## §1 C1——開放行「已開放」講兩次（文字紀律）

**問題**：進度頁已開放行（C17、C18）結構係 tag `<span class="prog71-tag open">已開放</span>` ＋ note `<p class="prog71-note">已經開放——返地圖嗰陣就會播出。（場景：…）</p>`——同一行「已開放」出現兩次。

**修法**（照 review 建議）：note 刪「已經開放——」四隻字，變成「返地圖嗰陣就會播出。（場景：…）」；tag 嗰粒保留。全站開放行共用同一 code 位（`renderProgressPane71` 入面唯一一個 `const openBody`），一次過改晒，C17／C18 行一樣，將來其他開放幕同一 pattern。

**驗證**：`test_prog175_static.py` 斷言 openBody 行冇「已經開放」、tag 保留、開放行得返一次「開放」狀態字；實駕 seed 態（1992-12-05，C1–C16 done）932＋700：C17 行「第 17 幕三年收科已開放返地圖嗰陣就會播出。（場景：星河電視台）」、C18 行一樣結構，`openCount` 各＝1，note 各以「返地圖嗰陣就會播出。（場景：」開頭。截圖 `qa175/shots/progress_banner_top_932.png`／`_700.png` 目視確認。

## §2 C2——進度頁開頁短暫提示遮住第 14–15 幕（狀態可讀）

**根因（實駕＋靜態雙重查明）**：全域 `#toast` 係 `#app` 底部 `position:absolute` overlay（1.8 秒自動消失）。觸發點係 B01 導入 modal「去何生事務所睇劇情（會用預設行程）」掣（`showB01HomeModal`，index.html 約 L58690）：撳掣 → `show("v-map")` ＋ 80ms 後 `openLoc(agency_ho)` ＋ `toast("已用預設行程 · 到何生事務所可播開局劇情")`。1.8 秒內開進度頁，overlay 仲生效，底部位置啱啱蓋住第 14 幕「站隊」／第 15 幕「高危替身」（review 實駕 4 次開頁入面出現 1 次；pre-existing，同 B3 無關）。另一處類似 toast（L38785 屋企提示掣「到現場可播劇情」）唔係呢句，冇改錯。實駕探針證實時序：撳 B01 掣後約 0.2 秒 toast 著、約 1.8–2.0 秒熄，地點 sheet 開、無 enc79 攔截。

**修法（照 review 建議，唔成個 toast 系統重寫）**：
1. 新 CSS `.prog175-banner`（`.prog71-note` 之後）：`position:static` in-flow 置頂，金底紙卡樣（配合 prog71），`max-height`／`opacity`／`margin`／`padding` 0.3s 過渡；收起態 `.bye`（`max-height:0`＋`opacity:0`）。
2. 新 `prog175ShowBanner(msg)`：喺 `#progress-list .prog71-wrap` 第一個仔插入 banner（「主線進度」標題上面，review 建議位置），字句原樣搬（`textContent`），1.8 秒後加 `.bye` 平滑收起、350ms 後移除；重複觸發重置計時。
3. 新 `prog175AdoptToast()`：`renderProgressPane71` 尾段呼叫——開頁 render 嗰陣若 `#toast.on` 仲生效，將佢嘅字收容入 banner，同時收起 overlay（清 `toast._t` 計時＋除 `on`／`has-stamp`／`has-sub`＋清內容＋`aria-hidden`＋拎走 `#app` 嘅 `toast-up`／`keep-sheet`，唔留暗影 slab）。
4. `toast()` 分流：手帳進度頁開住嗰陣（`#v-home.on` **且** `#home-pane-progress.on`——兩重判斷缺一不可：離開手帳去返地圖嗰陣 progress pane 會留返 `on` class，淨睇 pane 會誤判，將地圖提示吞咗入隱藏咗嘅手帳），提示直接行 banner，唔行 overlay；banner 唔到就跌返 overlay（唔吞提示）。字句本身唔變（有 `sub` 嗰陣先至用 ` — ` 串埋；C2 嗰句冇 sub，原句不變）。`#toast` 本身定位／計時／dedup 一律唔郁。

**唔揀嘅路**：成個 toast 系統改頂部 in-flow——會掂晒地圖／手帳／訓練等全部提示，風險唔值得；淨縮短顯示時間／只首次開頁先出——治唔到「遮行」本身，review 建議嘅 banner 先係正解。

**驗證（實駕，見 §7）**：932＋700 各 8 次開頁（全部真路徑：fresh game → B01 掣 → 300ms 內開進度頁，開頁前 toast 實證著緊原句），開頁即刻＋1 秒後量度：overlay 熄、banner 靜態置頂（y302–338，`firstChild`）、行 14–15 命中行本身、banner 同行 14–15 零相交；約 2 秒 banner 入 `.bye`、約 2.6 秒移除。Live-fire（B01 掣＋`#chip-story` 同一個 JS task 撳，toast 喺進度頁開住嗰陣先觸發）：`#toast` 全程 0 次著（932 採樣 0/9、700 採樣 0/4——採樣疏係 headless timer 節流，overlay 本身長 1.8 秒，著咗一定捉到；量度嗰陣 toastOn 亦係 false），banner 照出、行唔遮。0 pageerror。

**實駕量度方法學（兩點要講明）**：
- 行 14–15 嘅 `elementFromPoint` 要先將行 15 scroll 入視野中央先量：banner 將 list 向下推約 42px（首行 y370→412），行 15 中心跌到 932 viewport 之下（y~942），唔 scroll 嗰陣 `elementFromPoint` 回 null——唔係遮住，係摺疊位之下。量度 script 曾經有呢個假 fail（另加 `rowRects` key 錯：存 14/15、讀 13/14），已修正，修正後 8/8＋live-fire 全 PASS。
- 頭一版實駕用同一個 browser context 跑 8 次，iteration 2–8 搵唔到 B01 modal（save 殘留）。改為每 iteration 全新 context，8/8 穩定重現。

## §3 新測試

`tests/test_prog175_static.py`（26 項，工作版 **26/26 PASS**）：
- C1：openBody 冇「已經開放」／note 仲係「返地圖嗰陣就會播出。」／tag 保留／開放行得返一次「開放」狀態字／全站得一個 openBody 定義。
- C2：`prog175ShowBanner`／`prog175AdoptToast` 定義、banner CSS 在位＋`position:static`（唔係 fixed／absolute）＋收起有過渡＋`.bye`（`max-height:0`＋`opacity:0`）、banner 插 `.prog71-wrap` 最頂（`insertBefore(b, wrap.firstChild)`）、字句原樣搬、1.8 秒後先收起、adopt 只收 `#toast.on`＋收起 overlay（清計時＋除 class＋清內容）＋拎走 `toast-up`、`renderProgressPane71` 尾段有呼 adopt、`toast()` 喺進度頁開住嗰陣行 banner（要 `#v-home.on`＋pane.on）＋banner 唔到跌返 overlay、`#toast` 本身定位唔郁。
- 基線：SAVE key／softRev／`?v=` 不變、開放行場景文案仲喺度、B01 提示字句本身唔變。

**反證**：喺 pristine `f09fa1b` 上重行（rebase 後，`~/workspace/linji-pristine175r/index.html`，跑完已清走），**19 項新斷言乾淨 FAIL**（C1 2 項＋C2 17 項），7 項基線 PASS，唔 crash（exit 1）。工作版 26/26 PASS。

**反證更正（第二次 rebase，見 §8）**：逐行再數，斷言級實際係 **18 項 FAIL＋8 項基線 PASS**（C1 2 項＋C2 16 項；「19」嗰陣係 `grep -c '^FAIL'` 連 `FAILURES:` 摘要行一併計埋，多咗 1；C2 17 項入面「#toast 本身定位唔郁」係基線，本來就 PASS）。喺 pristine `a41b789` 上重行（`~/workspace/linji-pristine175r2/`，跑完已清走），同樣 18 FAIL／8 PASS、exit 1、唔 crash——FAIL 清單正好係 v175 全部新斷言（C1 2＋C2 16），基線 8 項全 PASS。

## §4 全套 A/B

`qa131/run_suite.sh`：
- Pristine `f09fa1b`（v177；worktree `~/workspace/linji-pristine175r/` detached，跑完已清走）：**236／12**，見 `qa175/suite_pristine.txt`。
- 工作版：**237／12**，見 `qa175/suite_work.txt`。FAIL 集同基線**完全一致**（12 項 pre-existing：flash51、giglib36、pacing35、poster59、rumor49、slot50、soft_tip_111_restore、start53、weave43、weave44、weave49、wrap38），兩份 txt diff 淨係多咗 `PASS tests/test_prog175_static.py` 一行，＋1 正好係新加嘅測試。**零回歸**。（開工嗰輪基底 `a618a5d` 係 234／12 → 235／12；rebase 後基底變 `f09fa1b`，數字跟住變，見 §8。）

**第二次 rebase 後重驗（基底 `a41b789`，見 §8）**：
- Pristine `a41b789`（v179 NOTES；worktree `~/workspace/linji-pristine175r2/` detached，跑完已清走）：**238／12**，見 `qa175/suite_pristine2.txt`。FAIL 12 項同上批一致。
- 工作版：初跑 **238／13**——多出嚟嗰項係 `tests/test_story179_static.py` FAIL，唔係回歸，係 v179 測試同 v175 C1 撞咗（見 §8 衝突處理：v179 測試斷言 openBody 仲有「已經開放——」，v175 C1 已經刪咗）。跟 §8 修咗測試斷言之後重跑：**239／12**，見 `qa175/suite_work2.txt`（覆寫咗初跑嗰版）。兩份 txt diff 淨係多咗 `PASS tests/test_prog175_static.py` 一行，＋1 正好係新加嘅測試，FAIL 12 項同一批。**零回歸**。

## §5 resync（釘行漂移，唔係回歸）

`index.html` 淨 ＋78 行，六檔釘行測試一度 FAIL——全部係行號漂移，內容逐行相同（`difflib.SequenceMatcher` 對位核實，pristine `a618a5d` vs 工作版；移位帶：舊行 ＜4957 不變、4957–33708 者 ＋10、33709–44116 者 ＋25、44117–44207 者 ＋76、≥44208 者 ＋78）。按紀律人手 resync：單次掃描 dict 查表（`/tmp/resync175.py`／`/tmp/resync175b.py`，跑完即棄，唔入 repo），全行精確匹配且 count==1 先至換，唔逐對 `re.sub`、唔用 blanket replace（行頭歷史註解嘅 prose 數字唔郁）；逐檔加返 resync 歷史註解行。

| 檔 | 錨點 | 移位 |
|---|---|---|
| `test_kwan151_static.py` | 13 個錨點（25598／25939／25987／26206／25942–25944／27147／27180／30946／30954／30955／30997） | 全部 ＋10（當中 B4／C5 係假 PASS，已一併 resync） |
| `test_tang152_static.py` | HELD 25758、normaliser 31436、loader 31580 | 全部 ＋10 |
| `test_tang171_static.py` | 總行數、openLoc DEF | 59341→**59419**、53860→**53938** |
| `test_tang173_static.py` | 總行數、openLoc DEF（L4845 喺 CSS 插入點之前，唔郁） | 59341→**59419**、53860→**53938** |
| `test_text125_static.py` | currentLine 27672、advance 27801、familySafe 33494 | 全部 ＋10（→27682／27811／33504） |
| `test_travel114_static.py` | COUNT 13＋FREE 27＋DEF＋WRAPPER | 按移位帶重算（COUNT 13／FREE 27 數目不變，DEF 53860→53938、WRAPPER 44235→44313） |

Resync 後六檔逐個直接覆驗全部 PASS，全套重跑 235／12（見 §4）。

## §6 紀律

- SAVE key（`starVolunteer_map_v19w`）、softRev（`s107`）、產品 `?v=` 唔郁（新測試＋全套基線斷言覆蓋）。
- 唔直改 content pack JSON；`index.html` 註解冇寫其他測試硬計嘅版本字串；新加註解只講 v175 機制。
- 冇用 `git rebase --continue`，冇 pipe 去 head。

## §7 實駕

`qa175/drive175.py`（沿用 `drive153r.py` 嘅 serve／new_game／seed／open_progress helpers；本地鏡像＋`python3 -m http.server` port 8175，`?softPreview=1`，`chrome-headless-shell`，`xvfb-run -a` 完整 Chromium 語境——實際以 `pwenv49` ＋ headless shell 跑，DOM 證據為準，截圖對返 DOM 數字）。Seed：1992-12-05 day 1069、C1–C16 done、C10 done（review 同款）；C2 播種改 C2–C16 done、C1 唔 done（留返 B01 go 掣，行數照樣 18 行）。

| 檢查 | 932 | 700 |
|---|---|---|
| C1：行數 18、開放行 2、每行「已開放」×1、note「返地圖嗰陣就會播出。（場景：…）」 | PASS | PASS |
| C2 adoption：開頁 8 次（真路徑，開頁前 toast 實證著緊原句） | **8/8 PASS** | **8/8 PASS** |
| C2 live-fire：toast 喺進度頁開住嗰陣觸發 | **PASS**（`#toast` 0/9 著） | **PASS**（`#toast` 0/4 著） |
| pageerror | 0 | 0 |

**Rebase 後重跑（`qa175/drive175.py all`，`drive175.json` 已更新）**：checks 7 項全部 true、0 pageerror；C1 兩尺寸行數 18、開放行 2、每行「已開放」×1、note 開頭一致；C2 adoption 8/8＋live-fire 兩個尺寸全部 PASS；banner y302–338、首行 y412（推低 42px）、行 14 y891／行 15 y927、行 14–15 命中行本身，同工人嗰輪逐項一致；截圖 4 張 byte-identical。唯一差異係時序抖動：個別 iteration 嘅 t2s（約 2 秒）量度捉到 banner 收起中（`.bye`、h 0–6px），舊輪嗰陣已移除（null）；live-fire 採樣數 932 係 4 次、700 係 16 次（舊輪 9／4，headless timer 節流令採樣疏密浮動），`#toast` 全程 0 次著兩輪一致。**Rebase 零行為改變**。

C2 adoption 每 iteration 量度（以 932 iter1 為例，其餘 15 次同一 pattern）：開頁即刻 banner `{x:42, y:302, w:346, h:36}`（`position:static`、`firstChild`，首行 y412——banner 推低咗 42px）、`#toast.on=false`、行 14 rect `{y:891, h:30}`／行 15 `{y:927, h:30}`、banner 同兩行零相交、scroll 入視野後行 14–15 `elementFromPoint` 命中 `DIV.prog71-top`（inRow true）；約 2 秒 banner 入 `.bye`（h 收窄到 0–6px）、約 2.6 秒移除。截圖 `qa175/shots/`：`progress_banner_top_932.png`／`_700.png`（banner 置頂未捲）、`progress_banner_932.png`／`_700.png`（捲低後 C17／C18 行＋星途寄語）；影嗰陣無 modal、無 enc79 overlay（16 次 adoption 入面事務所入場 0 次彈 enc79）。結果 JSON：`qa175/drive175.json`。

**第二次 rebase 後重跑（`qa175/drive175.py all`，`drive175.json` 已更新）**：checks 7 項全部 true、0 pageerror；C1 兩尺寸行數 18、開放行 2、每行「已開放」×1、note 開頭一致；C2 adoption 8/8＋live-fire 兩個尺寸全部 PASS；banner y302–338、首行 y412、行 14 y891／行 15 y927、scroll 後行 14–15 命中 8/8、live-fire `#toast` 全程 0 次著（932 採樣 20 次、700 採樣 21 次；上輪 4／16，採樣疏密係 headless timer 節流浮動），同第一輪逐項一致；截圖 4 張已重影。唯一差異又係 t2s 時序抖動（個別 iteration 約 2 秒量度捉到 banner 收起中 `.bye` h 0–6px，上輪嗰陣已移除 null；行 15 底 y 個別 ±1px）。**Rebase 零行為改變**。

## §8 rebase 紀錄

- 開工基底：main `a618a5d`（v174 NOTES；遊戲 `e2add29`）。
- 工作期間 main 郁咗兩次（v172 落地統籌嗰邊）：`e2add29` → `9eea029`（v172）→ `7801a72`（v172 NOTES，線上 5,271,408 bytes sha `eb594747…`）。
- 落地前 rebase（2026-11-13，rebase 工人）：基底由 `a618a5d` 上最新 main `f09fa1b`（v177 頒獎禮舞台加闊；期間 main 再郁一次：`7801a72` → `f09fa1b`）。Rebase 停喺 `Rebasing (1/2)`：`ec0c100` 撞咗 6 檔釘行測試（kwan151／tang152／tang171／tang173／text125／travel114）——v172＋v177 都 resync 過，v175 嗰輪係對舊基底做。
- `index.html` 自動合併、staged，三邊改動齊晒（v175 C1 openBody 刪「已經開放——」＋C2 banner／helpers／toast() 分流、v172 `start()` 帶 `ignoreSheetLoc`、v177 FLOOR 290→250＋舞台加闊；merged 59434 行＝59356＋78，diff 淨係 v175 嗰 4 處插入＋C1 同行改）。
- 解衝突：以 `f09fa1b` 版測試檔做底，按內容錨點重新 resync（64 粒錨點逐行核實：f09fa1b 行內容喺 merged 唯一出現＋行號吻合移位帶 ≤4956 ＋0、4957–33710 ＋10、33711–44131 ＋25、44132–44222 ＋76、≥44223 ＋78；3 粒單行唔唯一，用兩行 context 唯一確認；單次掃描 dict 查表，script `/tmp/r175/resync175_rebase.py` 跑完即棄，唔入 repo；行頭歷史註解 prose 數字唔郁，只加一行新 rebase 歷史註解）。`git add` 6 檔後 `GIT_EDITOR=true git rebase --continue`（output 寫檔，冇 pipe 去 head），第二個 commit（NOTES＋qa 證據）零衝突 apply。Rebase 後 HEAD：`aeadf51`（code）＋`9bb578f`（NOTES；§8 呢段 amend 入去，amend 後 HEAD 見 git log）。
- 重驗（rebase 後最終樹，見 §4／§7）：新測試 26/26、6 檔逐個 PASS、node --check 兩段 inline script PASS；全套 pristine `f09fa1b` 236／12 → 工作版 237／12（＋1 正好係新測試，FAIL 12 項同一批，零回歸）；實駕 `qa175/drive175.py` 重跑 ALL CHECKS PASS，數字同工人嗰輪一致（rebase 零行為改變）；反證喺 pristine `f09fa1b` 上 19 項乾淨 FAIL。

## §8b 第二次 rebase 紀錄（落地前 main 再郁，v179 落地）

- 任務派嗰陣寫明最新 main 係 `4106b2f`（v179 遊戲 commit），核實唔係就停低。但 `git fetch origin` 之後 `origin/main` 已經係 **`a41b789`**——v179 NOTES commit（`4106b2f` ＋ `NOTES_V20A179.md` 48 行，2026-11-13 15:00:34 HKT 落 main，比派票早約 40 秒；派票嗰陣話「NOTES 未 commit」嗰個快照已經過時）。`git diff 4106b2f a41b789` 證實淨係多咗 NOTES 檔一個，`index.html`／測試零郁——任務假設（v179 14 行鎖行改法、全套 238／12）全部仍然成立。判斷：停低只會浪費一轉，rebase 上真正最新 main `a41b789` 先至係今次 rebase 嘅目的（就係為咗唔好落喺舊基底）；繼續做，呢段寫明偏差，等統籌覆核。
- Rebase（`GIT_EDITOR=true git rebase origin/main`，output 寫檔，冇 pipe 去 head）：第一次 `pick aeadf51` 停喺 `Rebasing (1/2)`，話 `tests/test_kwan151_static.py`／`tests/test_text125_static.py` 嘅本地改動會俾 merge 蓋過——但工作樹本身乾淨（開工嗰陣已核實），似係間歇性寫入問題（v168 嗰輪有同類 EPERM 惡化紀錄）。`git rebase --continue` 即刻成功，零衝突：`index.html` 自動合併，兩邊齊晒（見下）。Rebase 後 HEAD：`3fba8fb`（code）＋`3ebe909`（NOTES；§8b 呢段 amend 入去，amend 後 HEAD 見 git log）。`git diff 3e40cbb 3ebe909 --stat` 正好等於 `f09fa1b..a41b789` 嗰 14 檔，證明 v175 內容零流失、零重複 apply（todo 嗰陣 `aeadf51` 出現兩次係 reschedule 殘留，唔係 apply 兩次）。
- `index.html` 合併核實（逐項 grep，唔信 auto-merge）：v175 C1 openBody 冇「已經開放」（全檔 0 命中）＋C2 `.prog175-banner`／`prog175ShowBanner`／`prog175AdoptToast`／`toast()` 分流／`renderProgressPane71` 尾段呼 adopt 全部在位；v179 鎖行標籤式「場景：X」（L44119）＋「或場景：X」（L44125）連 v179 註解在位；openBody 繼續用「（場景：X）」括號寫法——啱，v179 自己寫明「已開放行完整句式唔郁」。`git diff 4106b2f HEAD -- index.html` 淨係 v175 嗰 5 個 hunk（＋78 行淨）。
- **衝突（測試層，任務冇預見）**：v179 嘅 `tests/test_story179_static.py` 有個斷言守住 openBody 原文「已經開放——返地圖嗰陣就會播出。（場景：X）」唔變——同 v175 C1（用戶拍板刪「已經開放——」）正面撞。初跑全套工作版 238／13，多出嚟嗰項就係佢 FAIL；`test_story179_logic.js` 唔受影響。解法：跟任務「兩邊都留」嘅指示，行為兩邊保留，淨係將 v179 測試嘅斷言改做合併後嘅已批核文案——「返地圖嗰陣就會播出。（場景：X）」仲喺度、場景括號寫法仲喺度，另加反向守衛「已經開放——返地圖嗰陣就會播出。」唔准返生；檔頭註解寫明原因（v175 C1 先刪、v179「唔郁」指場景寫法＋句式）。改完工作版 11/11 PASS；喺 pristine `a41b789` 上重行，淨係呢個斷言乾淨 FAIL（exit 1、唔 crash）——反證成立，個測試而家同時守住 v179 鎖行＋v175 C1。`NOTES_V20A179.md` 本身係 v179 歷史紀錄，唔郁。呢個改動 amend 入 code commit（`3fba8fb` 嗰層），唔係 NOTES commit。
- 6 檔釘行測試：**唔使 resync**。v179 `index.html` 係 16 行換 16 行、淨行數 0（hunk `@@ -44088,16 +44088,16 @@`），錨點行號零漂移；六檔逐個直接跑全部 PASS（kwan151／tang152／tang171 22／tang173 21／text125／travel114）。`tests/test_prog175_static.py` 同 v179 測試唔同檔，冇撞檔。
- 重驗（第二次 rebase 後最終樹，見 §4／§7）：新測試 26/26、6 檔逐個 PASS、v179 測試改完 11/11 PASS、node --check 兩段 inline script PASS；全套 pristine `a41b789` 238／12 → 工作版 **239／12**（＋1 正好係新測試，FAIL 12 項同一批，零回歸；初跑 238／13 嗰次見 §4）；實駕 `qa175/drive175.py all` 重跑 ALL CHECKS PASS，數字同第一輪一致（rebase 零行為改變）；反證：新測試喺 pristine `a41b789` 上 18 項新斷言乾淨 FAIL＋8 項基線 PASS（見 §3 更正）。

## §9 殘留／跟進

- 無新殘留。C2 live-fire 嗰陣 openLoc 喺進度頁開住嗰陣照跑（事務所 sheet 喺地圖層開，唔搶 view），實駕證實唔影響 banner／行。
- Pristine 比對 worktree：舊嘅 `~/workspace/linji-pristine175/`（detached `a618a5d`）仲留喺 workspace，統籌核實完可清走；rebase 重驗用嘅 `~/workspace/linji-pristine175r/`（detached `f09fa1b`）跑完已清走（`git worktree remove`）；第二次 rebase 用嘅 `~/workspace/linji-pristine175r2/`（detached `a41b789`）同樣跑完已清走。
- 全套 12 項 pre-existing FAIL 同開工前一批，唔喺呢票範圍。

## §10 落地紀錄（統籌填）

- 遊戲 commit **`4ef7405`**（squash merge `v20a175`，基底 `a41b789` v179 NOTES；20 檔 ＋5813／−79）。落地前 main 冇再郁（核實嗰陣 HEAD 仲係 `a41b789`）。
- 線上核實（統籌親自 curl，兩次）：第一次仲係舊版（v179，5,271,638 bytes sha `c428f3d1…`，Pages 部署滯後）；等 90 秒後重 curl，**5,276,015 bytes、sha256 `76c39a9faeb6f89f8177941998694458cdd6fb975348cbb72b6e03e9863db3da`**，同 repo `HEAD:index.html` 完全一致。Push main 一次成功（`a41b789..4ef7405`），`git fsck` 乾淨（淨 dangling 殘留；之前嗰條 `a41b789` reflog invalid entry 已經解開——佢就係 v179 NOTES commit 本身，而家係 main 嘅祖先，唔係懸空 entry）。
- 下一票 rebase 基底改用 **`4ef7405`**（live 已係 v175）。
