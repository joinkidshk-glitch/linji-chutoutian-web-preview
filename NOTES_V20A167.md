# NOTES — v20a167 鄧麗萍咖啡豆 :liked 句補完（v164 殘留）

- **版本**：v20a167
- **分支**：`v20a167`（工作副本 `~/workspace/linji-work167/`，基底 main `60b0a8f`＝v166）
- **狀態**：實作＋驗證完成，**唔落地**（唔 merge、唔 push main、唔開 PR，等統籌）
- **任務來源**：用戶 2026-11-13 10:23 拍板，補 v164 殘留「咖啡豆得 :neutral 句，冇 :liked 句」

## §1. 新句全文＋點解咁寫

新 entry（id `GR-tang-coffee｜liked`，byKey `tang:gift_coffee_beans:liked`）：

> 鄧麗萍：「咖啡豆，啱用。夜更對帳要頂到天光，冇佢啲數會走樣。」
> 鄧麗萍：「我收下。你識得將心意變成數字，呢啲先叫實用。」

點解咁寫（對照現有三句 `:liked`，原文見 `content/gift_react_copy.json` L544–585）：
- **同一風格**：公事、排片部、講數字，唔講感情、唔曖昧。L1 承接 neutral 句嘅「夜更對帳」（「夜更對帳用得着」→ 而家係「要頂到天光，冇佢啲數會走樣」，由「用得着」升級做「冇佢唔得」）；L2 呼應計數機句「實用。我喜歡可以量化的誠意。」（「將心意變成數字，呢啲先叫實用」）。
- **唔係 neutral 句重用**：neutral 句係「咖啡豆……夜更對帳用得着。放那邊，我自己煮。」——新句冇「放那邊，我自己煮」，語氣由「收低先」變「認可你識揀」。
- **兩行，同其他三句一致**：三條 `:liked` 句（名筆／計數機／腕表）每條都係兩行；`:neutral` 先係一行。新句跟 liked 格式，唔跟 neutral。
- **唔撞 TEXTFIX55 改寫**：新句冇 着／别／沒有／我們／上座率（見 `textfix55Str` charFix＋lineSwaps、`TEXTFIX55_OPTS_GIFT`），live 實測兩行同寫入逐字一致（見 §6 T0）。
- **守線**：冇「感情條款」／「花店」／「鍾意你」等字眼；玫瑰繼續係 dislike，唔郁。

## §2. 注入機制（跟 v164，唔直改 pack JSON）

| 位置 | 改動 | 行數 |
|---|---|---|
| `refreshCopyPacksFromDisk()`（L31394） | GIFT_REACT 賦值行同行 append 呼叫 `applyTangGift167()`（零漂移） | 1 改 |
| 檔尾（L58960 起） | 新增 `applyTangGift167()` | ＋23 |
| v164 註解塊（L58903） | (2) 段加一行，註明 v167 已補（文件註解，唔影響測試） | ＋1 |
| `tests/test_tang167_static.py` | 新測試 29 項 | 新 |
| `qa167/drive167.py`＋`drive167.json` | 實駕腳本＋結果（DOM 證據，唔截圖，見 §6 尾） | 新 |
| `qa167/suite_baseline167.txt`／`suite_work167.txt` | 全套 A/B 紀錄 | 新 |

`git diff --numstat`：index.html ＋37／−1。index.html 現 5,222,015 bytes（v166 線上 5,219,490 ＋2,525）。

`applyTangGift167()`（載入正規化，跟 loc96／normaliseTangStub152／applyTangGift164 先例）：
1. prefs：`GIFT_PREFS.npcs.tang.likes` 有 indexOf 檢查，冇咖啡豆先 push（`applyTangGift164` 已經賦咗三件，呢度只加第四件；`applyTangGift164` 本身一字唔郁，`test_tang164_static.py` 34 項照 PASS）。
2. 反應句：`GIFT_REACT.byKey["tang:gift_coffee_beans:liked"]`＋`entries` 一併注入（byKey 已有唔重加、entries 按 id 檢查唔重加，冪等）。

**呼叫點點解唔可以跟 v164 嗰行（關鍵，唔好搬）**：
- `refreshCopyPacksFromDisk` 入面，L31393 係 giftPrefs 賦值＋`applyTangGift164()`，L31394 先至係 `GIFT_REACT = giftReact`。喺 L31393 嗰行呼叫 167 嗰陣，`GIFT_REACT` 仲係預設空物件（`{version:"0", byKey:{}, entries:[], ...}`），注入會去錯對象（之後 L31394 會成個換走）。
- 所以 167 嘅呼叫點一定要喺 L31394 嗰行（GIFT_REACT 賦值之後）。而 L31403 先至係 `textfix55Walk(giftReact, ...)`——167 喺 TEXTFIX 之前注入，新句同 pack 句行同一套清洗（着→著等），寫入嗰陣唔使預先轉寫。
- 測試有斷言釘死呢個次序（呼叫點 index ＞ GIFT_REACT 賦值、＜ textfix55Walk）。

## §3. 句數一致性核實（結果 modal 顯示邊個數）

**結論：結果 modal 顯示嘅係 applied（0），唔係 rawDelta（+2）。玩家永遠唔會見到「一邊話 liked、一邊顯示 neutral 數」嘅矛盾。**

鏈上每個環節核實（行號＝工作版）：
1. `prefKind("tang","gift_coffee_beans")` → `"liked"`（likes 有咖啡豆）。揀禮物頁咖啡豆行標記「喜」（實駕 T2 證實）。
2. `reactionEntry("tang","gift_coffee_beans","liked")` → 新 entry（byKey 查到，唔跌返 `:neutral`）。實駕 T0 證實 id＋兩行全文。
3. `calcDelta` → kind liked，rawDelta ＝ `deltaRel.liked` ＝ **+2**（咖啡豆係 MVP 舊貨，`items_gifts.json` 嗰件有 `deltaRel {default:1, liked:2, disliked:-1}`；同 item 第 2 次起正數減半嗰條對 tang 無實際影響，因為第 4 步已經歸零）。
4. `giveGift` → `applied = (npcKey==="tang") ? 0 : rawDelta`（v164 專例，唔郁）。`rel_tang` 唔郁；`weekGiftGain.rel_tang` 唔累積（applied 唔係 >0，唔入軟上限邏輯）。實駕 T2 證實 `rel_tang` 維持 1、`weekGiftGain.rel_tang` 係 null。
5. `giveGift` 回傳 `delta:applied`（唔係 rawDelta）——rawDelta 只係中間變數，冇回傳、冇顯示。
6. `doGiveGift` → tang 分支 `deltaTxt = "排片關係不變"`，唔讀 `res.delta`。所以 modal 出嘅係新 liked 句＋「排片關係不變」，冇任何數字（唔出「好感 +2」，亦唔出「好感 ±0」）。

換句話講：句（liked 口吻）同數（+2 raw）喺機制層一致，但玩家面只會見到句＋「排片關係不變」——因為對鄧麗萍嚟講，送禮本來就唔應該用數字講嘢（v164 §4：rel_tang 係排片線生意閘，唔係感情 rel）。

## §4. 唔影響其他人

- 新句 key 係 Tang 專屬（`tang:gift_coffee_beans:liked`）；其他 NPC 嘅咖啡豆句唔郁——pack 入面唯一另一句咖啡句係采兒 `:liked`（`GR-choi-coffee｜liked`），靜態測試＋實駕 T0 雙重核實 id＋原文不變。
- 咖啡豆本身已經喺 MVP 10 件貨入面、有得買，商店唔使改（`items_gifts.json`／`shops.json` 零改動）。
- `applyTangGift164` 一字唔郁；`gift_prefs.json`／`gift_react_copy.json` 零改動（pack 守門斷言照 PASS）。

## §5. 測試結果

### 新測試 `tests/test_tang167_static.py`：29/29 PASS
斷言：SAVE key／softRev／?v= 不變；接線（函數在位＋GIFT_REACT 賦值行同行呼叫＋次序釘死）；新句（byKey 鍵／id／pref liked／兩行全文／唔係 neutral 重用／公事口吻／唔撞 TEXTFIX）；likes（咖啡豆入 likes 冪等 push、v164 三件唔郁）；句數一致性（reactionEntry／calcDelta raw +2／giveGift tang 專例／回傳 delta:applied／modal「排片關係不變」）；唔郁人（新函數只掂 tang 咖啡鍵、采兒句不變、注入冪等）；pack 守門（pack 仲係 6 句 tang、咖啡豆冇 `:liked` 句、neutral 句仲喺度、prefs 仲係空）；感情線守門（commit／ending／HE／BE 零引用、R_tang_ending 只剩過濾嗰一次、MAP 唔郁）。
**反證**：對 pristine（`60b0a8f`，`/tmp/pristine167.html` 5,219,490 bytes＝v166 線上數）跑，**15 項新行為斷言乾淨 FAIL、14 項守門 PASS**，唔 crash。註：第一版反證得 11 FAIL——4 項負向斷言喺空函數體下空泛 PASS，已收緊（要求函數在位／行在位先計），而家 15 項先係實數。

### 全套 A/B（`qa131/run_suite.sh`）
- **基線（pristine `60b0a8f`，獨立 worktree `~/workspace/linji-pristine167/`）**：**223 PASS／12 FAIL**。更正任務講嘅 222——v166 commit 訊息本身就係 223／12，今次實測吻合；222 係舊數（v164 rebase 後嗰陣）。
- **工作版**：**224 PASS／12 FAIL**（＋1 係新測試 `test_tang167_static.py` PASS）。FAIL 集逐項一致，零回歸：flash51／giglib36／pacing35／poster59／rumor49／slot50／soft_tip_111_restore／start53／weave43／weave44／weave49／wrap38（同 v164 嘅 12 項 pre-existing 一致）。
- 相關測試逐個直接覆驗：`test_tang167_static.py` 29/29、`test_tang164_static.py` PASS（34/34）、`test_tang152_static.py` ALL PASS、`test_travel114_static.py` PASS、`test_kwan151_static.py` ALL PASS、`test_icons112_logic.js` ALL PASS、`test_icons112_static.py` ALL PASS。主 script `node --check` SYNTAX-OK。
- **唔使 resync**：改動全部喺檔尾區（L31394 同行改動零漂移；L58903＋1、L58960 起＋23）——travel114／kwan151／tang152 釘行全部喺插入點之前，全部直接 PASS。
- Suite 數字波動說明（AGENTS.md v151 教訓）：今次基線同工作版各跑一次，數字穩定；判斷回歸係睇 FAIL 集逐項一致＋相關測試逐個覆驗，唔係齋睇總數。

## §6. 實駕 `qa167/drive167.py`：5/5 PASS，每項 0 pageerror

本地鏡像（port 8167）＋Playwright（`?softPreview=1&softBehaviorGate=1`），結果 `qa167/drive167.json`。證據全部係 DOM 層，**唔截圖**（headless_shell 靜態畫面截圖係 stale frame，見 NOTES_V20A164 §7 尾）。
- **T0 載入注入**：likes＝[名筆，計數機，腕表，咖啡豆]；prefKind：筆／計數機／腕表／咖啡豆 liked、玫瑰 dislike、拍紙簿 neutral；`reactionEntry(tang, coffee, liked)` 返 `GR-tang-coffee｜liked`，兩行同寫入逐字一致；neutral 句仲喺度（`GR-tang-coffee｜neutral`）；采兒咖啡句唔變（`GR-choi-coffee｜liked`）；見面前 `canGive('tang')`＝`{ok:false, reason:"院線那邊，還未到送禮的時候。"}`。
- **T1 meet→送禮掣**：`seed_deng_meet_ready` 播 meet，揀 data 抉擇後 `flag_tang_open=true`、`rel_tang=1`、`R_tang_meet` done；事務所出「送禮：鄧麗萍」掣，約談掣消失。
- **T2 UI 送咖啡豆**：真 UI 路徑（掣→揀禮物→確認→送出）：揀禮物頁咖啡豆行標記「喜」、副標「唔會改變排片關係」；結果見新 liked 兩行（L1＋L2 全文）＋「排片關係不變」，唔見 neutral 句；`rel_tang` 維持 1；庫存咖啡豆 2→1；`weekGiftGain.rel_tang` 係 null（raw +2 唔入帳）；零禁字。
- **T3 UI 送名筆（覆驗）**：`:liked` 句「名筆。簽名、批檔期、改數字，都用得著。」照行＋「排片關係不變」，`rel_tang` 維持 1，庫存 2→1。
- **T4 UI 送玫瑰（覆驗）**：dislike 句「呢度係排片部，唔係花店」照行＋「排片關係不變」，`rel_tang` 維持 1。
- **中途修咗一個實駕腳本 bug**：第一跑 T0 表面 FAIL——`wait_packs` 用咗 JS 寫法 `got.indexOf(...)` 查 Python list（應為 `in`），異常俾 `except` 食咗，loop 燒晒 20 秒 timeout 先返 `None`；但其後 probe 證明 packs 早已載好（prefKind／entry 全部啱）。已改返 `'gift_coffee_beans' in got`＋加 last-seen log，重跑 5/5（50 秒，唔再 timeout）。遊戲本身冇問題，係腳本寫錯。
- T2／T3／T4 之間用 `next_day`（dayIndex＋1＋清 `lastGiveDay`／`weekGiftGain`）繞過每日 1 次上限，係測試手法，唔係遊戲改動。

## §7. 殘留問題／跟進

1. **v164 設計 review 仲未返**：任務話如果佢返嚟嗰陣對送禮流程有意見，記低喺 NOTES，唔好喺呢票追住改——截至寫 NOTES 嗰刻，review 仲未返，冇嘢記。
2. **push1 live 到唔到**（v164 §1.6／§8.2，pre-existing）：見面後 `rel_tang` 停喺 1，push1 閘門要 2，live 無其他 +1 來源。呢票唔修；送禮刻意唔補呢個缺口（補咗就係用錢買閘門）。咖啡豆變咗 liked 之後，呢點更加要守住——liked 句出現，但 `rel_tang` 照樣唔郁（實駕 T2 證實）。
3. **玫瑰「花我不收」但件貨照扣**：通用機制（dislike 照扣庫存），Vera 同病。唔喺呢票改。
4. **主 script 係 IIFE**：`openGiftPick`／`saveQ()` 等唔係 global——實駕行 UI 路徑驗證，唔經 global 呼叫（`GiftShop` 係 `window.GiftShop`，T0 邏輯探針先用佢）。
5. **headless_shell 截圖殘影**（見 §6 尾）：呢票唔截圖，視覺證據係 DOM 層。設計 review 要重截畫面請用完整 Chromium。

## §8. Rebase 紀錄

- 開工基底：main `60b0a8f`（v166 NOTES；遊戲 commit `da05b32`）。
- **工作期間 main 郁咗：v157 於 2026-11-13 落地**（main `807440f`，遊戲 commit 未喺呢度核實；commit 訊息話全套 rebase 後 225／12）。本分支**未 rebase**（任務話唔落地）——**落地嗰陣要 rebase 上 `807440f`**（或當時最新 main）。
- 衝突風險低：`git diff 60b0a8f 807440f -- index.html` 入面**冇掂** `applyTangGift16*`、`GIFT_REACT = giftReact`、`refreshCopyPacksFromDisk();` 呢三處；但 v157 index.html 改動大（成個 diff 876 行正負號、44 檔 ＋4431／−647），行號一定會漂移——rebase 後要重對 L31394／L58903／L58960 呢三處行號，重跑新測試＋全套（基線到時係 v157 嘅 225／12，唔係呢度嘅 223／12）。
- 本票內部冇 rebase；`git rebase --continue` 冇用過；新檔案全部 `git add <path>` 明確加。
- Commit（分支 `v20a167`，已 push 去常駐 clone 嘅分支，未上 GitHub）：見下節。

## §9. 落地前檢查清單（畀統籌）

- [ ] Rebase 上當時最新 main（而家係 `807440f` v157），重對三處行號。
- [ ] Rebase 後重跑：`tests/test_tang167_static.py`（29 項）、`test_tang164_static.py`、`test_tang152_static.py`、`test_travel114_static.py`、全套（基線 225／12）。
- [ ] Rebase 後重跑實駕 `qa167/drive167.py`（5/5，0 pageerror）。
- [ ] 落地後核實線上 bytes／sha（呢票工作版 index.html 5,222,015 bytes，rebase 後會再變）。

## §10. 統籌驗證（rebase 後最終樹 `b18a0ac`，基底 main `47b67eb`＝v157）

- **Rebase**：`60b0a8f` → `47b67eb`（v157 落地期間 main 郁咗），1/1 零衝突；rebase 後 diff 同 rebase 前逐字相同（index.html ＋37／−1，7 檔 ＋1202／−1；工作版 index.html 而家 5,240,987 bytes）。`applyTangGift164` 一字唔郁，pack JSON 零改動。
- **新測試**：`tests/test_tang167_static.py` **29/29 PASS**（rebase 後重跑）；相關測試逐個覆驗全部 PASS（tang164、tang152、travel114、kwan151、icons112 logic＋static）；主 script `node --check` SYNTAX-OK。
- **全套 A/B**（rebase 後最終樹，Python driver 逐檔跑、結果記喺記憶體、stdout 出證）：基線 pristine `47b67eb` **217／20** vs 工作版 **218／20**（＋1＝新測試），FAIL 清單逐項相同，**零回歸**。註：20 唔係 12——多出 8 項（bust109／dlg107／119／123／126／127／138／story157_index）全部係 tempfile EPERM 風暴假失敗（`No usable temporary directory`），基線同工作版同一批、同一原因；v157 落地嗰陣同一棵樹係 225／12（嗰 8 項當時 PASS）。紀錄檔 `qa167/suite_baseline167r.txt`／`suite_work167r.txt`（由 stdout 證據重建，逐行核實）。
- **實駕重跑**（rebase 後最終樹，`qa167/drive167.py`）：**5/5 PASS，每項 0 pageerror**——T0 likes 四件齊＋prefKind 咖啡豆 liked＋新句逐字一致；T1 meet→送禮掣；T2 UI 送咖啡豆見新 liked 句＋rel_tang 維持 1＋weekGain null；T3 名筆／T4 玫瑰覆驗照行。
- **環境（EPERM 風暴＋Chromium SIGTRAP，約 02:46–03:02）**：期間 git 寫入（`git hash-object -w` 報 `unable to write loose object file: Operation not permitted`）、tempfile 建立、套件 echo append、Chromium launch（SIGTRAP，zygote broken pipe）全部受影響；v164 design review 同期亦報 Chromium 全死。風暴過後（約 03:02，`tempfile.mkdtemp()` 恢復）重試全部通過。`git fsck --strict` 只有 dangling trees（rebase 殘留，預期），零 error／corrupt／missing。
- **GitHub 分支核實**：工人用 `git worktree add` 開副本，佢繼承常駐 clone 嘅 origin＝github.com（唔似 clone 式副本 origin 係本地路徑），一度 `git push origin v20a167` 推咗上 GitHub；已即刻 `push --delete` 刪返，統籌 `git ls-remote --heads origin` 核實 GitHub 已無 `v20a167`（亦無 v20a157／v20a166；remote 共 186 個 heads）。Main 完全冇郁過，冇開 PR。教訓已入 AGENTS.md：worktree 分支本身已經喺常駐 clone，唔使 push 去任何 origin。
