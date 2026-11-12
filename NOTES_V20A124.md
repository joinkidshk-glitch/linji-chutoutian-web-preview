# v20a124 AUD91FIX R2：試鏡公佈 timer 碰撞修復（Pair A＋Pair B＋三連撞）

- 日期：2026-11-12
- 基底：main `9eecc01`（v120，測試基線 165／12）——評估基準 `dc12744`（v122）期間 v120 已合併，
  本包開工嗰陣已 rebase 上最新 main（rebase 乾淨，零衝突；舊基底實駕 25／25 喺 rebase 後重跑一次，同樣 25／25）。
- 工作副本：`~/workspace/linji-work124`（`linji-work123` 已被 v123 表情補圖工作佔用；版號 v124——v123 已有
  `v123-expr` 分支在途，下一個空閒號係 v124）。分支 `v124-aud91r2`。
- 來源：評估 `~/workspace/linji-aud91-invest/R2_EVAL.md`＋重現 `~/workspace/linji-aud91-invest/r2/NOTES_R2.md`
  （驅動 `r2/drive_r2b.py`，方法學以修正輪為準）。

## 問題（R2，已實機證實）

timer 對 timer：入屋／讀檔繼續嗰陣，遊戲自己排咗兩個 timer，後面嗰個 modal 喺 aud91 modal 開咗
30–40ms 之後取代佢，`_aud91Presenting` 旗 stranded。

- **Pair A**（enterHome 內 +50ms aud91 vs +90ms 強制結局）：aud91 modal 出現 17ms 後被
  「1990 年尾 · 事務所評核」modal 取代；嗰單公佈永遠唔見（`aud91PresentOne` 呈現前已剔除 pending）。
- **Pair B**（讀檔繼續 +50ms aud91 vs +80ms 回家結算 modal）：aud91 被「回家結算」modal 取代；
  之後**成個 session 所有試鏡公佈靜默，直至 reload**（第二播種探針係乾淨證據）。
- **三連撞**（reload＋week105＋pendingEnding，評估未測）：三個 timer 連環撞。

## 改動（index.html，淨 +22 行；唔改 content pack JSON、唔郁 SAVE key／softRev／`?v=`）

行號係合併前工作版（基底 `9eecc01`）：

1. **Pair A — `enterHome` 強制結局 timer（36850–36862 行）**：舊裸
   `setTimeout(()=>{ try{ conseq61PresentForcedEnding(); }catch(_e){} }, 90)` 改做
   `_presentForcedEnding124`——`_aud91Presenting` 真嗰陣隔 300ms 再 check，直至旗清先
   `conseq61PresentForcedEnding()`。初次延遲維持 90ms，前置條件（`pendingEnding`＋未結局）不變。
2. **Pair B — `contFromSlot` 回家結算 timer（57531–57543 行）**：同一 guard——
   `_presentSettlement124`，旗真嗰陣 defer 300ms，直至旗清先開結算 modal。初次延遲維持 80ms，
   modal 內容（標題／「編排新一週行程」掣／唔重扣行字）一字不變。
3. **三連撞序列化（評估推薦方案之外嘅追加，見下節）**：
   - `var _week105SettlePending124／_week105SettleDone124`（56250–56255 行，`_aud91Presenting` 隔籬）。
   - `contFromSlot` week105 分支入 `enterHome` 之前記 `pending=true、done=false`（57529 行）。
   - 結算 modal 掣加 `on`＋`opts.onDismiss` 一齊記 `done=true`（掣撳／遮罩點走都計，57536–57541 行；
     `modal()` 掣 onclick 先 `_modalDismiss=null` 再行 `on()` 再 `closeModal()`，加 `on` 唔影響關 modal）。
   - 強制結局 guard 加多一重等：有結算等緊嗰陣，等埋結算 modal 被㩒走先出結局（36858 行）。
4. **唔做：`modal()` 通用 guard**（先行舊 `_modalDismiss` 再覆寫）——reentrancy 問題，評估 §4 已否決；
   本包 `modal()` 一字冇郁（靜態測試釘死）。

### 點解要追加三連撞序列化（唔照單跟評估 §4）

評估話「兩個 timer 輪流 poll，邊個先等到旗清就邊個先出」，預期順序係 aud91 → 結算 → 強制結局。
但兩個 guard 嘅 poll cadence 係獨立 300ms 迴圈，相位差由註冊時間差決定（結算 timer 喺 `enterHome`
尾段 `renderNotebook` 等行完先註冊，強制結局 timer 喺 `enterHome` 中段註冊，相位差唔係名義上嘅
80 vs 90ms）。若果強制結局嗰邊先等到旗清，結算 modal 會喺結局 modal 出咗之後取代佢——結局 modal
冇 `onDismiss`，玩家會見到結算、㩒走佢之後跌入一個已寫 E7 但未行結局流程嘅手帳，結局呈現要等下次
reload 先經 `ending78Locked()` 補出。為咗令三連撞順序**決定性**係 aud91 → 結算 → 強制結局，加咗
上面第 3 點（+6 行）：結算開咗未走嗰陣強制結局 guard 繼續 defer。Pair A（無 week105）同 Pair B
（無 pendingEnding）完全唔受影響（pending 假即過）。

## 測試

- 新守門（全部 PASS；pristine main `9eecc01` 跑新測試 FAIL，反證成立）：
  - `tests/test_aud91fix124_static.py`：31 斷言——Pair A／B guard 在位＋300ms defer＋初次延遲不變（90／80ms）＋
    舊裸 timer 已刪＋前置條件／modal 內容不變＋三連撞旗宣告／pending 記法／掣 on＋onDismiss 記 done＋
    `modal()` 冇 v20a124 防守碼＋紅線（SAVE／softRev／`?v=`／content pack JSON）不變＋NOTES 在位。
    喺 pristine main 跑 **21 個斷言 FAIL**（Pair A／B guard＋三連撞＋對稱全部 FAIL；紅線／`modal()` 不變／
    內容不變嗰啲斷言照 PASS）。
  - `tests/test_aud91fix124_logic.js`（node 沙箱，抽真 guard）：26 斷言＋harness——旗真唔出結局／結算、
    再 check 旗仲真繼續 defer、旗清即刻出且唔再排 timer、一開始旗假即刻出、三連撞結算未走繼續 defer／
    走咗即刻出結局、結算掣 on／onDismiss 都記 done。喺 pristine main 跑 **harness FAIL**
   （抽唔到 `_presentForcedEnding124`）。
- 全套回歸：pristine main 基線 **165 PASS／12 FAIL**（12＝已知環境性 static FAIL：
  flash51、giglib36、pacing35、poster59、rumor49、slot50、soft_tip_111_restore、start53、weave43、
  weave44、weave49、wrap38）；工作版 **167 PASS／12 FAIL**（＋2 新守門檔），FAIL 清單逐字一致。零回歸。
  行號漂移一處：`test_travel114_static.py` 因本包淨 +22 行要 resync（`qa124/resync_travel114.py`
  核實 44 個 `openLoc(` 呼叫點序列逐字一致、內容逐行相同，純漂移；COUNT 13／FREE 27 不變，
  DEF 52492→52625、WRAPPER 43344→43477），resync 後再 PASS。
- 舊基底（`dc12744`）全套亦跑過：基線 163／12 → 工作版 163／14（14＝12＋NOTES 未寫＋travel114 漂移未 resync），
  數字同新基底一致（只差 v120 帶嚟嘅 +2 PASS）。

## 實駕（Playwright 真瀏覽器，390×844，`?softPreview=1`，本地多線程 http.server 8979＋真實 `locator.click()`）

驅動 `qa124/drive_r2fix.py`（由 `r2/drive_r2b.py` 嘅 T2b／T3b 劇本改嚟用，MutationObserver 錄影＋第二播種探針），
log `qa124/logs/r2fix.log`、截圖 `qa124/shots/r2fix_*.png`。**25／25 PASS，0 pageerror，0 console.error**
（多線程 server，r2b T3b 嗰 19× `ERR_EMPTY_RESPONSE` 測試環境因素亦冇再出現）。rebase 前後各跑一次，兩次都係 25／25。

- **T2 Pair A**：aud91「系統／本次未獲聘」+1313ms 出，企足 1.8s 強制結局唔出現、E7 未寫；
  dismiss aud91 之後 +269ms 出「1990 年尾 · 事務所評核」，E7 已寫（`review1990`），結局流程
  「下一頁 → 睇手帳總結」行完，稱號「未紅先收・未說出口的人」。
- **T3 Pair B**：reload →「繼續」→ aud91 +323ms 出，企足 1.8s 結算唔出現、未結局；
  dismiss 之後 +312ms 出「回家結算 · 第 1 週」，dismiss 後入返手帳編排步（`homeEditable=true`）；
  **第二播種探針即刻呈現**（「何生來電」+2774ms，`pend=[]`）——旗唔卡，R2 根因已除。
- **T5 三連撞**：aud91 +472ms → dismiss 後 +177ms 出結算（E7 未寫）→ dismiss 結算後 +255ms 出
  強制結局，E7 已寫，結局流程行完。順序決定性係 aud91 → 結算 → 強制結局。
- **T4 Pair B 對照**：無 aud91 嗰陣結算 modal 直出；之後播種再入屋即刻出 aud91（對照成立）。

## 殘留缺口

- **drops +40ms**（評估 §5 附註，唔入呢票）：aud91 取代 drops「拍攝檔期取消」modal，內容玩家見唔到；
  drops modal 冇 `onDismiss`、冇旗，唔 strand。將來要修可以將 drops 經 `continueFn` 鏈入 aud91。
- H1 自然觸發點仍然未搵到（v122 防守性清旗，唔影響有效性）——v122 殘留，原樣。
- `test_travel114_static.py` 寫死行號，本包 resync 咗一次；將來任何改 index.html 行數嘅包都要再 resync。

## 合併紀錄（待填）

- 分支：`v124-aud91r2`（基底 main `9eecc01`）
- 合併 main commit：
- 線上 index bytes／sha：

## 回滾

- `git revert <squash commit>`（成包只係 index.html 3 處＋2 檔新測試＋travel114 resync＋本 NOTES；
  revert 即回復 v120 行為——Pair A 嗰單公佈會再被取代、Pair B 撞完成個 session 試鏡公佈靜默）。
