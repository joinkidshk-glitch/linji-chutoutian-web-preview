# NOTES — v20a197 全站掣位修復（B1–B7＋C1–C7＋D1）

- 分支：`v20a197`，基底 main `2760680`（v191 NOTES，遊戲 `f2a6b0c`）
- 工作副本：`~/workspace/linji-work197/`
- 任務：用戶 2026-11-13 21:11 拍板「一次過修晒」全站掣位 review（`~/workspace/linji-design-review-buttons/REVIEW.md`）嘅 B1–B7＋C1–C7＋刪 D1 印章掣
- 狀態：實作＋靜態驗證＋932／700／頒獎禮實駕全部完成；已 commit＋push（`39bdd83`＋第二 commit 見 §10）
- **唔落地**（落地由統籌做）

## 0. 總覽：逐項修法

| 項 | 修法 | 驗證 |
|---|---|---|
| B1 兩種「下一句」 | 巧遇 `.e79-btn` 由右下角 88px 文字鏈改全寬深色掣 `flex:0 1 370px; width:370px; max-width:100%; margin:0 auto; min-height:44px`（深色 `#2e2113`／金邊，置中）；`.e79-choice` 同樣 370px 置中；`.e79-box` 底 padding 12→9px，掣底離 viewport 底 9px，同主線 `(30,879) 370×44`（932）／`(30,647)`（700）完全一致。對話盒本身保持全闊（唔郁文字排版）。v20a108「下一句改文字鏈」設計作廢（註解已更新）。 | 靜態 PASS；實駕見 §9 |
| B2 手帳確認掣變形 | 新 helper `syncConfirmPlanStamp197(locked)`（L37277 起）做 `<button>`／`<span>` 節點互換，保留 id／class／text／title／aria-label；換返 button 嗰陣重綁 `onclick=confirmPlan`。未確認態＝正常掣，確認後＝同一幾何嘅非掣 `<span>` 印章。CSS：`.is-locked` 改 `flex:1 1 auto; width:auto; height:52px; margin:0; display:flex;align-items:center;justify-content:center`（`font-size:24px`、3px double 紅框、斜 -4.5°、.32em 全部保留）；`#nb-actions:has(.is-locked)` 拎走 `justify-content:center`；700 media 規則 margin 改 `0`（舊 `4px auto 3px` 會令 auto margin 搶走 flex 空間）；v145 鎖定態 bar padding 5px→6px（同未確認態一致，印章 y 唔差 1px）。「還原」唔再消失：`renderNotebook()` 入面永遠 `display:inline-block`＋`disabled=!editable`，加 CSS `#btn-reset-plan:disabled{opacity:.35; cursor:not-allowed}`。快捷列 `#nb-quick` 鎖定態繼續隱藏。 | 靜態 PASS；實駕見 §9 |
| B3 頒獎禮「跳過 ⏩」逐 beat 跳位 | stage.innerHTML 入面跳過掣由 frame 層搬入 `.awd62-canvaswrap`（480×360 固定比例，`position:relative`），CSS `top:8px;right:8px` 不變；glamour overlay z-index 2、skip z-index 3，掣照樣喺上面。 | 靜態 PASS；實駕見 §9（soft 模式） |
| B4 日結板三粒掣跟內容郁 | 加 `#mask.day-res:not(.tut-on).modal{ height:min(78dvh,78svh,720px)!important;}`，矮屏 media（max-height:820px）內加 `height:min(92dvh,92svh,720px)`。`#modal-inner` 本來就捲得郁（flex:1 1 0%＋overflow-y:auto）。三條日結路徑都掛 `day-res`：`afterDayModal()`、`presentRestSleepDayEnd()`、第二日結路徑。只郁幾何，唔郁流程邏輯（v196 協調，見 §8）。 | 靜態 PASS；實駕見 §9 |
| B5「返回地圖」三個位三種大細 | 決定跟 **modal 底部全寬 44px**（全站 modal／sheet CTA 既有 pattern）。地點 sheet `#loc-close` 加 `flex:1 1 100%; width:100%; min-height:44px`；手帳 `#home-back-map-tabs` 保留頁頂右位置＋吊牌形，但高 38→44px（`min-height:44px; height:44px`）；日結 modal 嗰粒已經係全寬，唔郁。`#home-back-map`（強制日／soft 日改名「繼續行程」／「開始今日行程」）唔郁流程。**點解唔跟手帳嗰粒頁頂右 104×42**：手帳吊牌係常駐頂部 chrome（有繩＋斜角＋牛皮紙造型），唔係流程 CTA——拉闊做全寬會毀咗佢嘅吊牌身份；反過來 modal／sheet 嘅「返回地圖」本身已經係流程出口，全寬 44px 係全站 modal CTA 既有規格，改動最小、一致性最高。 | 靜態 PASS；實駕見 §9 |
| B6 地圖「過一日」開 sheet 走位＋出 viewport | v18a compact HUD 規則成段拎走，改做 `.map-wrap.sheet-open.map-hint{ position:sticky!important; bottom:12px!important;... max-width:none; max-height:none; overflow:visible; font-size:.82rem; padding:11px 12px 12px;}`，幾何同乾淨態完全一致（連 `.map-hint-help`／`.map-hint-story` 嘅 `display:none` 一併拎走）。**代價**：v18a compact 日期 HUD 拎走（日期照舊喺頂欄＋hint 入面）。**殘留風險**：B6 下移成因至今未完全解開——v18a `top:42px` 只解釋到 +42px，review 量度係 +126–144px；懷疑涉及 openLoc 嘅 scrollIntoView／#app scrollTop（A1 舊患）或內容增長。sticky 頂唔住向上捲（pin 低嗰陣 scrollMapPinIntoView 會將 hint 捲上去）——實駕量度裁決，唔得就 fallback（搬 hint 出 scroller）。 | 靜態 PASS；實駕見 §9 |
| B7 手帳分類掣初 paint 俾 sticky bar 冚住 | `.notebook` 加 `padding-bottom:84px`（700 media 內 61px）；另加 helper `revealCatTabs197()`（只喺 `scrollTop===0` 初 paint 嗰陣，如果分類掣底俾 bar 冚住，就將 `#notebook` 捲到剛好令分類掣完全見到；玩家自己碌過就唔郁），喺 `enterHome()`（renderNotebook 之後）同 `setHomeTab()` 尾（tab==="plan" 嗰陣）呼叫。**關鍵判斷**：padding 處方本身喺 scrollTop=0 嗰陣郁唔到分類掣位置（padding 喺內容尾），所以唔可以盲目跟處方——nudge 先係令「初 paint 見晒撳到」成立嘅機制，呢個偏差如實記錄。 | 靜態 PASS；實駕見 §9 |
| C1 主分頁使用中嗰格大啲高啲 | `#home-tabs.home-tab.on` 高 38→32px（保留紙面色／粗體／`margin-bottom:-1.5px`／shadow；用色／底線區分，五格固定 58×32、同一條 y）。 | 靜態 PASS；實駕見 §9 |
| C2 地圖底部主掣同一位兩個身份 | 加 `#v-map.map-hint #map-end-day{ background:#fffdf6!important; color:#3a2e22!important; border:2px solid #8a6f4d!important; box-shadow:none!important;}`（紙色）；「開始今日行程」留返金色實色（`.map-start-today` L117 金底 `#C9A227`）。 | 靜態 PASS；實駕見 §9 |
| C3 地點 sheet 行動掣高矮唔齊 | `#loc-sheet.sheet.act` 固定 `height:60px!important; overflow:hidden`；`.n` 單行截短（nowrap＋ellipsis）；`.h` 單行截短（`-webkit-line-clamp:1`）。 | 靜態 PASS；實駕見 §9 |
| C4 肯定行次序倒轉 | **成因已解開**：全部 modal DOM 次序本身已經係肯定行先（出席→推辭、確定→取消，105 個 label／role 配對逐個審計過）；唯一反轉機制係 tut-on CSS：`#mask.tut-on #modal-btns button.p{order:1}` 但 `.g` 預設 `order:0`，所以 tut-on 嗰陣推辭（.g）走去出席（.p）上面——drive 量度嗰陣 mask 有 `tut-on` class 證實咗。修法：加 `#mask.tut-on #modal-btns button{ order:1!important;}`（特指度 (2,1,1)，低過 `.tut-skip`／`.tut-replay-step` 嘅 (2,2,1)，教學掣 order:2／3 唔受影響；非教學 modal 掣一律 order:1，次序跟 DOM）。**全局規則：肯定／主動作永遠在上（DOM 第一粒＝視覺最上）**——同過一日確認 modal、報紙／結果卡、教學「下一步→跳過」嘅現行大多數一致，亦係教學本身註明嘅規則（"Primary always first in DOM and in CSS order"），宜家擴展到全站。請柬 DOM 係 `[{ label: "出席", role: "p", on: attend}, { label: "推辭", role: "g", on: skip}]`（L46313 起，`presentAwardInvite()`）；`git log -S` 證實呢個次序自 v20a7 已有。**點解揀「肯定行在上」**：現行大多數 modal 已經係咁（過一日確認、報紙／結果卡都係肯定行先），跟大多數改動最小；教學掣本身註明同一條規則，唔係新發明。 | 靜態 PASS；實駕見 §9 |
| C5 抉擇卡高矮唔一 | `.story-play.sp-choice` 改 `min-height:64px; display:flex; flex-direction:column; justify-content:center`（短句置中）。 | 靜態 PASS；實駕見 §9 |
| C6 通告板 54px 大罅 | **成因已核實：54px 入面係分組頭。** 通告板 `doScout()`（L57028 起）：未達標卡包喺 `<details class="gig-locked108"><summary>未達標／長遠目標（N 張）——點開睇</summary>` 入面；CSS L5285 `.gig-locked108{margin-top:8px; border-top:1px dashed; padding-top:6px}`＋summary 細字。修法：summary 做返明顯分組標題——`.gig-locked108{margin-top:12px; border-top:2px solid #cbb98d; padding-top:0}`；summary `display:block; padding:10px; background:#efe6cf; font-size:.85rem; font-weight:800; color:#3a2e22; border-bottom:1px solid #cbb98d; margin-bottom:8px`；開合提示改由 CSS `::after` 出（`▸ 點開睇`／`▾ 點開收起`），summary 字串改做「未達標／長遠目標（N 張）」（唔再寫死「點開睇」）。 | 靜態 PASS；實駕見 §9 |
| C7 手帳分頁撞名 | sub-tab `#htab-plan` 文字「行程」→「本週安排」（HTML 直接改；`applyPhase2Steps56TabLabel()` 只郁 `htab-rumor`，唔會寫返；冇測試硬計呢個字串；L5474 註解同步更新）。 | 靜態 PASS；實駕見 §9（已量到「本週安排」） |
| D1 刪「行程已定」印章掣 | 鎖定態嘅 `#btn-confirm-plan` 由 `<button>` 改做純文字／印章（紅印章視覺不變，唔係掣）。同 B2 同一粒掣一齊做：未確認態係正常掣（固定幾何），確認後變返同一幾何嘅非掣印章文字，唔改名唔改大細唔移位。 | 靜態 PASS；實駕見 §9 |

## 1. B2 自然觸發點核實結果（U5）

**已核實：冇自動確認。** 觸發點就係玩家自己撳「確定本週行程」→ `confirmPlan()` → `commitPlanAndGo()`（L37563）設 `S.homeEditable=false` → 再入返手帳時 `renderNotebook()` 切鎖定態。Review 嘅「自動確認」係 drive setup（`drive_buttons.py` new_game L157–160）撳咗真嘅確認掣造成。另一處 `S.homeEditable=false`（L30915）係 soft-seed 載入路徑，唔係 LIVE 自然流程。

## 2. C6 成因核實結果（U3）

**已核實：54px 入面係分組頭**（見 §0 C6 行）。`doScout()` 未達標卡包喺 `<details class="gig-locked108">` 入面，summary 就係嗰 54px。

## 3. U1–U6 處置

- **U1**（休息日結板 modal 內「返回地圖」scoped 實撳）：實駕見 §9。
- **U2**（通告板詳情掣列）：實駕見 §9。
- **U3**（C6 成因）：已核實，見 §2。
- **U4**（TVB sheet 入口被額度擋嗰陣嘅狀態）：code 已讀——`openLoc()` 入面 `travel114TrySpend` 失敗就 toast＋return，唔開 sheet、唔擲巧遇、唔扣數（L55010 起）；`#loc-title` 殘留舊文字只係 stale flag，sheet 唔會開。實駕確認見 §9。
- **U5**（B2 自然觸發點）：已核實，見 §1。
- **U6**（複製流程兩組掣）：**已核實：兩組掣係同一個流程兩個入口，唔係重複。** 逐日「⧉ 複製」（`openCopyFromDay(dayIdx)`，L37221）同快捷列「複製到…」（`toggleCopyPanel`）都係開同一個 `#nb-copy-wrap` panel（chips＋「套用複製」`applyCopyToTargets()`）；分別只係 source 日嘅揀法（逐日掣＝嗰日；快捷列＝當前選中日）。唔使合併。實駕再確認一次，見 §9。另：逐日複製掣係 `.day-row` 入面嘅 `<span class="cp" role="button">`，只喺可編輯態先生成；鎖定態 `openCopyFromDay` 有 `if(!S.homeEditable) return;` 守門。

## 4. 靜態驗證

- 新測試 `tests/test_buttons197_static.py`（32 項）：B1–B7／C1–C7／D1／D2／D3 逐項。反證：喺 pristine main `2760680` 上面 23 FAIL（淨係 9 項基線／唔郁類 PASS：SAVE key、印章視覺舊值、跳過 CSS、day-res count、日結全寬舊值、教學掣次序、DOM 次序舊值、D3、D2），乾淨，唔 crash。
- 更新咗 7 份舊測試（因為改動令佢哋嘅斷言過時，全部係刻意改動，唔係靜默繞過）：`test_book141_static.py`（C1 38→32px；鎖定邏輯改 helper；「還原」改 disabled 灰態）、`test_book143_static.py`（700 規則 margin:0；C1 32px）、`test_book145_static.py`（700 規則 margin:0；C1 32px；footer padding 5px→6px）、`test_dlg108_static.py`（e79-btn／e79-choice 新全寬掣字串；DLG108 文字鏈設計作廢）、`test_awards166_static.py`（B3 skip 掣新次序：canvas＜skip＜glamHtml）、`test_book143_logic.js`／`test_book145_logic.js`（鎖定邏輯改 helper 字串）。另修咗註解入面寫咗 `font-size:24px` 會令 `src.count('font-size:24px') == 1` 嗰個測試 FAIL 嘅問題（已拎走嗰句，count 返去 1）。
- **verify37 真問題＋修法**：`test_verify37_logic.js` 係 slice 式 eval harness——佢逐個抽 `renderNotebook` 等函數出嚟 eval，沙盒 stub 預先定義晒 renderNotebook 調用嘅外部函數。我嘅 renderNotebook 改為呼叫 `syncConfirmPlanStamp197`，harness 冇呢個 stub → `ReferenceError: syncConfirmPlanStamp197 is not defined`，成個 test crash。修法：harness 加 stub `var syncConfirmPlanStamp197 = function(){};`（同其他 stub 一樣，沙盒唔測印章）。修後 66 PASS、exit 0。

## 5. 全套 A/B（`qa131/run_suite.sh`）

- Suite A（我嘅版，dayend189 修好後）：**264 PASS／12 FAIL**——FAIL 清單同基線完全相同：flash51、giglib36、pacing35、poster59、rumor49、slot50、soft_tip_111_restore、start53、weave43、weave44、weave49、wrap38。（264＝263＋1 個新測試檔 test_buttons197_static.py。）
- Suite A（dayend189 修好前）：263 PASS／13 FAIL（12 基線＋test_dayend189_static.py）。
- Suite B（pristine，上一手 `git stash -u` 後跑）：**263 PASS／12 FAIL**，同一 12 項。
- 今次 Suite B 有效重跑（恢復後，`git worktree` 開 pristine `2760680` 跑，outfile 放 workspace）：**263 PASS／12 FAIL**——FAIL 清單同基線逐字相同（flash51、giglib36、pacing35、poster59、rumor49、slot50、soft_tip_111_restore、start53、weave43、weave44、weave49、wrap38）。早前嗰次 114 PASS／161 FAIL 係 EPERM 廢數（見 §10），作廢。Suite A 最終樹重跑：**264 PASS／12 FAIL**（264＝263＋1 個新測試檔），FAIL 清單同 pristine 逐字相同，新測試 `test_buttons197_static.py` PASS。零回歸確認。Worktree 已刪（`git worktree remove --force`）。
- **8 份行號測試已 resync**：用 `qa197/resync197.py`（difflib SequenceMatcher 對位，全部錨點都係 `equal` 區＝純漂移，內容逐字核實）。總漂移 +94 行（60490→60584；split 計 60491→60585）。B4 補丁喺 ~L3283 再加 9 行，之後全部錨點再 +9。映射（pristine→現時）：kwan151（25659→25714、26000→26055、26003→26058、26004→26059、26005→26060、26048→26103、26267→26322、27213→27268、27246→27301、31020→31075、31028→31083、31029→31084、31071→31126）；rom176（6072→6127、31583→31638、53416→53510、53784→53878、54923→55017、55017→55111）；tang152 0-based 索引（25818→25873、31509→31564、31653→31708）；tang171／173（總數→60584；openLoc DEF pristine 54986→55080 1-based＝0-based 55079）；tang173 L4862 行（pristine 1-based 4889→4935＝0-based 4934）；gift185（總數→60584）；text125 0-based（27783→27792、27912→27921、33613→33622）；travel114（DEF_LINE 55071→55080、WRAPPER_LINE 44518→44527、COUNT_LINES 12 項＋FREE_LINES 34 項全部 +9）。**陷阱**：resync 腳本嘅 pin 係 1-based，test 索引有啲係 0-based——tang152 傳錯 pin（31509／31653）會差一位，正確 pin 係 31510→31565／31654→31709（1-based）＝0-based 31564／31708；text125 同理但巧合抵消咗（傳 27737 得 1-based 27792，當 0-based 用即係 1-based 27793＝正確值）。travel114 wrapper 真身係 `openLoc: function(id, opts){ openLoc(id, opts);},`（現時 L44527，pristine 44434），唔係 `window.__phase2 = {`（現時 L44518，另一行）。9 份 resync 後測試逐個直接跑全部 PASS。
- **Suite A2**：262 PASS／14 FAIL——多出 wf5_87＋years66。兩份直接跑 3 次全部 PASS，懷疑波動。
- **Suite A3 重跑：264 PASS／12 FAIL，FAIL 清單同 pristine B 完全相同。** A2 嗰兩項證實係套件波動，唔係回歸（全套數字會波動，唔好齋信一次總數——呢個就係實例）。
- JS 語法 OK（兩個 script block 各自 `node --check` 通過）。
- `git status`：18 檔改動（index.html＋17 份測試）＋新檔 `tests/test_buttons197_static.py`＋`qa197/resync197.py`（resync 腳本，留檔）＋`qa197/drive197*.py`＋`qa197/drive197.json`＋`qa197/shots/`（39 張）。

## 6. 實駕量度注意事項（教訓，寫低畀下一手）

- **旋轉元素唔可以用 getBoundingClientRect 比幾何**：鎖定印章 `rotate(-4.5°)` 令 299×52 嘅 layout box 量出嚟變 299×75 bbox；手帳吊牌父層 `.tagwrap141` 有 `rotate(2.5°)`，102×44 量出嚟變 104×48。呢兩處都要用 `offsetWidth`／`offsetHeight`（未旋轉 layout box）先比得準；中心點差 <1px 亦可作佐證。Review 嘅舊數字（印章 186×67、吊牌 104×42）同樣係旋轉 bbox，唔係 layout 尺寸。
- **「還原」disabled＋快捷列隱藏係 renderNotebook 嘅狀態**：`confirmPlan()` 鎖定分支直接換印章，但 reset／quick 係 renderNotebook 先設——撳完確認即刻量會見到未重繪嘅舊態（reset 仲 enabled、quick 仲見到），要出返手帳再入過（沉澱態）先量得準。
- **開局 C1 完結會出「劇情結算」modal（進度／關閉）**：實駕 driver 一定要閂埋佢先返到地圖，唔係成個地圖段會卡住；STATE_JS 要 null-safe（`S` 喺 reload 初始化窗口可以係 null）。
- **U6 逐日複製掣只喺可編輯態先生成**（`.day-row .cp` 係 span role=button）；鎖定態量唔到係正常，唔係缺失。

## 7. 唔做／未修

- D3 地圖「進度」chip 唔刪（review 建議保留；用戶今次冇揀佢）。
- D2 日結板「返回地圖」唔喺呢票（歸 v189／v196 範圍）——B4／B5 只修擺位／統一規格，唔好刪呢粒掣。
- U1–U6：全部已核實（U1／U2／U4／U6 實駕見 §9；U3／U5 見 §1–§3）。U4 toast 文案已補捉（見 §9.1）。

## 8. v196 協調

v196（行程自動連跑）**未落地**——工作副本 `~/workspace/linji-work196/` 喺分支 `v20a196`，基底同 v197 一樣係 `2760680`，未有 commit 落 main。B4／B5 只郁擺位／幾何，唔郁日結板嘅流程邏輯（邊個掣出現、邊個掣走、自動連跑）；rebase 嗰陣對清楚。v197 淨改動 +94 行（60490→60584），集中 CSS＋`syncConfirmPlanStamp197` helper＋三處呼叫點，冇掂日結板流程。B4 補丁再加 9 行喺 ~L3283（見 §9.2）。

## 9. 實駕（Playwright，本地鏡像，LIVE；頒獎禮 soft）

環境：`/home/hatch/pwenv49/bin/python`（venv，`playwright` 喺呢度；系統 python3 冇），瀏覽器 `/home/hatch/pw-browsers/chromium_headless_shell-1248/chrome-headless-shell-linux64/chrome-headless-shell`。serve：`python3 -m http.server` port 18997，播種存檔直接寫 localStorage key `starVolunteer_map_v19w` slot 3；主 script 係 IIFE，行 UI 路徑；播完 meet／push 要先清 enc79 巧遇 overlay 先截圖；headless_shell 截圖有 stale frame 殘影，DOM 量度先係可靠證據。Driver 檔 `qa197/drive197*.py`，結果 `qa197/drive197.json`，截圖 `qa197/shots/`。

### 9.1 932 run（0 pageerror）

- **B1 主線半邊**：C1 intro「下一句」連續多步全部 `(30,879) 370×44`，covered:false（三個獨立 run 一致）。
- **B1 巧遇半邊**：第 9 日 loc try 1（星河電視台）觸發，`.e79-btn` `(30,879) 370×44`，offsetW=370／offsetH=44，文字「下一句」——同主線逐 px 一致；撳一次推進成功（line 變咗，advanced:true）。
- **B2／D1**：未確認掣 `(94,870) 296×52`；鎖定沉澱態（出返手帳再入過）印章係 `<span>`，layout `offsetW=296／offsetH=52`（逐 px 一致；bbox 299×75 係 `rotate(-4.5°)` 膨脹，唔係真大細）；「還原」`disabled=true`、opacity 0.35、display block 留喺原位；快捷列 `display:none`；`S.homeEditable=false`；撳印章前後狀態完全唔變（noop=true）。D1 確認：鎖定態唔再係掣。
- **B5**：手帳吊牌 layout `offsetW=102／offsetH=44`（bbox 104×48 係父層 `.tagwrap141` `rotate(2.5°)` 膨脹）；地點 sheet 真 fullscreen 版 `#loc-close` `offsetW=348／offsetH=46`（sheet 內容全寬）。
- **B6**：乾淨地圖 vs placeholder sheet 開住，「過一日」同一個位 `(46,861) 338×45`；自由日驗證（drive197i）：乾淨 end_day `(46,861) 338×45`、hint `(32,797) 366×123`；真 fullscreen sheet（locpanel118）開住嗰陣 end_day 照樣 `(46,861) 338×45`、count=1、hint `(32,797) 366×123`——完全一致；閂 sheet 之後 end_day `(46,861) 338×45`、hint 相同。還原檢查通過。
- **B7**：初 paint nudge 有跑（scrollTop=121／16），分類掣底 855 ＜ bar 頂 859，全部見晒；可編輯態 JS 撳分類掣 `.on` 會轉（外出→訓練）。
- **C1**：五格全部 58×32、同一條 y=215，切頁唔郁。**C7**：sub-tab「本週安排」。
- **C2**：自由日「過一日」紙色 `#fffdf6`（`(46,861) 338×45`），`#map-start-today` 唔出現（兩掣輪流佔同一位）。
- **C3**：地點 sheet 五粒行動掣全部 338×60（x=41，y=514／581／648／715／782，67px pitch）。
- **C4（過一日確認）**：DOM 次序 `[確定過一日, 取消]`；直疊全寬 358×44，確定 `(36,457)` 在上、取消 `(36,509)` 在下；maskCls `mask tut-on on`，modal y=369 H=194（置中：(932−194)/2=369）；撳取消後 dayIndex 唔變（8）。diag run 量到橫排（確定 `(204,850) 110×48`、取消 `(322,850) 64×48`）——解開咗：非 tut-on 態下 base `.btnrow` 係 row 排版；tut-on 態下係 column；兩種態下 DOM 次序＝視覺次序＝肯定行先。
- **C6**：卡罅 `[8,8,71,8,8,8,8,8,8,8,8]`，71px 嗰格入面係 41px 高分組頭「未達標／長遠目標（9 張）」（bg `#efe6cf`、800 粗）。
- **U1**：rest 日結板 scoped 撳「返回地圖」成功，日由 7→8，報紙 modal 出現（「收下這份剪報」）。
- **U2**：撳第一張 `.gig-teaser` 卡（「賀歲特輯／電視特輯可接通告／片酬 $520…」）開到詳情 modal，掣列 `["接通告", "離開"]`；接通告 `(36,744) 358×44`，離開 `(36,796) 358×44`，直疊全寬，肯定行先。maskCls `mask tut-on casting-sheet-on on`。
- **U4**（乾淨態，drive197i）：事前 maskOn=false、locTitle「地點」（placeholder）、hint「仲可以去 1 個地方」、toast 空、used=1；設 used=2 再撳星河電視台：事後 maskOn=false、locTitle 仲係「地點」、hint 不變、used 停喺 2（冇扣）、sheet 冇開。**阻擋本身已驗證（冇 sheet、冇扣數）。Toast 文案已補捉（`drive197m.py`，0 pageerror）：「今日出行額度用完——今日已經去咗 2 個地方，聽日再去。」**——click 後即刻每 100ms 輪詢 `#toast`，連續 10 個樣本（ms 0–941）全部 `on: true, aria: false, cls: 'toast on'`，同 code（L55094–55096）一字不差。之前捉唔到係時序問題：toast 只顯示 1800ms 之後 `replaceChildren()` 清空，舊探針等 1000ms＋open_loc 內部等候，讀嗰陣已經過期。頭兩次受污染：第一次 sheet 根本未閂過（locSheet 成日 true 唔係有效判據；`#loc-title` 殘留「地點」只係 stale）；第二次 U2 詳情 modal（掣列「接通告／離開」）未閂乾淨（「離開」係返去通告欄，要撳「返去地點」先閂到），maskOn=true 污染成個量度。下一輪一定要先撳「返去地點」閂 modal、核實 maskOn=false 先做 U4。U4 code：`openLoc()` 入面 `travel114TrySpend` 失敗就 toast＋return，唔開 sheet、唔擲巧遇、唔扣數（L55010 起）。
- **U6**：可編輯態逐日複製開到 panel（open:true, display:block）；快捷列同樣開到（open:true, display:block）。兩組掣係同一流程兩個入口（見 §3），唔使合併。

### 9.2 B4 補丁（實駕揭露初版無效，根因＋再驗證）

- **初版 B4 規則完全無效**：soft 板 modal y=86 H=760、掣 686／739／791；rest 板 y=529 H=387、掣 756／809／861——同 review 數字逐 px 相同，兩板都係 mask class `mask tut-on on day-res`。
- 3 秒採樣證實位置穩定（唔係動畫中途）：soft 板 mask computed `align-items:center, padding:16px`；rest 板 `align-items:flex-end, padding:52px 16px 16px`。同一 class 下差異來自 v18a 規則 `body.day-res-open #mask.day-res`（L2186–2191，特指度 (1,2,1)，壓過 `#mask.tut-on` (1,1,0)）：`align-items:flex-end; padding-top:52px; background:linear-gradient(...)`。
- 拍攝板 v20a189 刻意唔加 `body.day-res-open`（保 dim 樣；註解 L38502：「唔加 body.day-res-open，唔改 dim／HUD 樣（嗰條 gradient 規則要兩個 class 齊先生效）」，只加 mask `day-res` L38504）→ tut-on 置中。休息板加咗（`presentRestSleepDayEnd` L57407＋L57437）→ v18a 貼底。兩板共用同一個 `modal()` 殼。
- Mask 定位模型：base `.mask`（L439）`position:fixed; display:flex; align-items:flex-end; justify-content:center; padding:10px`（bottom-sheet）；`#mask.tut-on`（L454）`align-items:center; padding:16px`；`#mask.tut-on.modal` max-height `min(88dvh,88svh,760px)`。Soft 置中驗算 (932−760)/2=86 ✓；rest 貼底驗算 932−387−16=529 ✓。
- **補丁**：固定高度規則唔再排除 tut-on（`#mask.day-res.modal{ height:min(78dvh,78svh,720px)!important;}`，media 內同樣），另加 `#mask.day-res{ align-items:flex-end!important;}` 統一底錨。`test_dayend189_static.py` 斷言同步更新（舊版 `:not(.tut-on)` selector 令成條規則喺教學態下完全唔生效）。
- **補丁後驗證**（drive197j，932，0 pageerror）：soft modal y=196 H=720、掣 756／809／861；rest modal y=196 H=720、掣 756／809／861；**掣 y 差 [0,0,0]，identical:true**。C4 對照（非 day-res 過一日確認）仍置中（maskAI center，modal y=369 H=194），anchor 規則冇漏出。700 態注意：tut-on max-height 帽係 min(88dvh,760px)，700 高嗰陣 modal 係 616px 唔係 644px（92dvh），但兩板一致，掣照樣齊。

### 9.3 實駕期間拆解出嚟嘅關鍵機制（全部已核實，寫低畀下一手）

- **C1 intro 故事「第一日：冇價」喺手帳首次打開嗰陣自動彈出**，蓋住成個手帳（對話板 `.sp-plate-narration105` y=748–866；`.sp-stage-inner` 全屏）。「確定出發」掣要播完故事先見到；播完故事會有「劇情結算」modal（進度／關閉），要閂埋先返到地圖。driver 一定要處理呢兩個 modal，唔係成個地圖段會卡住。
- **`ensureWeekPlanCommittedForStory()`（L37608）**：「手帳未確定時，導航／事態 CTA 靜默提交週程（唔跑 runScheduleFromToday，保留當日自由去播事態）」——有劇情播嗰陣手帳未確定，系統會靜默提交週程（`S.homeEditable=false`＋toast「行程已定」＋`renderNotebook()`）。所以開局 C1 故事一播，計劃已經鎖咗；U6 逐日複製嗰陣 `openCopyFromDay` 第一行 `if(!S.homeEditable) return;` 就靜默返；B7 分類掣喺故事播緊嗰陣俾 story overlay 蓋住撳唔到（intended modal 行為）。呢啲全部係 pre-existing 設計（v19z15／v19z16），唔係 v197 回歸。
- **鎖定態分類掣 `.on` 唔郁係 pre-existing 行為（v19z24）**：`renderNotebook()` 入面 `if(!editable) planCat = want;`（L37316）——非編輯態撳分類掣會即刻彈返去當日類別。B7 只關位置（分類掣喺 bar 上面），唔關呢個。
- **主 script 係 IIFE，只有 `S` 同 `GIGS` 係 global**（`window.S = S`，L30451／33985／48875／49379）。`saveQ`／`renderNotebook`／`toggleCopyPanel`／`openCopyFromDay`／`planSelDay`／`dayPlanLocked`／`todayPlanId`／`runScheduleFromToday`／`startTodayScheduleFromMap` 全部 `undefined`（probe_seed.py 實測 TYPEOF）。之前啲直 call 俾 try/catch 靜默吞咗，係無效探針；要經 UI（真掣 click）先驅動到內部函數。
- **seed 嘅 saveQ 靜默失敗（最大發現）**：`SEED_DAYEND_JS`／`SEED_REST_JS` 入面 `try{ saveQ();}catch(e){}`——`saveQ` 唔係 global，ReferenceError 俾 catch 吞咗，seed 返 `{ok:true}` 假象但實際冇 save 過；reload 之後載入嘅係 seed 前嘅舊存檔（預設 weekPlan、shoots 空）。所以 B4 唔可以靠 reload，一定要 **live in-memory seed、唔 reload**（review 嘅 drive_buttons2 line 237 寫明「日結板 soft（唔 reload，live seed）」）。probe_seed.py 實測：SEED_RET `{ok:true, gigId:"gig_1988_film_01", dayIndex:0, todayPlan:"shoot:probe189w", tomPlan:"street"}`；POST_SEED weekPlan 有 shoot、shoots `[probe189w, probe189f]`；但 reload＋繼續之後 weekPlan 變返預設、shoots 空。
- **標題畫面嗰陣 S 係 null（lazy init）**：reload 之後要先撳「繼續」載入存檔先有 S；STATE_JS 要 null-safe（`(typeof S!=='undefined' && S)? S.dayIndex: null`）。頭版 `<script>` 嘅 `location.replace` 只喺 soft URL（`softBehaviorGate=1`／`softPreview=1` 且 softRev 唔係 s107）先觸發，同呢個無關。
- **拍攝日執行路徑**：`startTodayScheduleFromMap()`（L37769）→ `resolvePlannedDay(id)`（L38135 起，shoot 分支）→ `afterDayModal()`。地圖「開始今日行程」掣（`#map-start-today`，L39067 綁 `startTodayScheduleFromMap`）只喺地圖重繪嗰陣按當日計劃決定出唔出現；live seed 之後地圖唔會自動重繪，所以 `#map-start-today` 唔出（得「過一日」）。
- **開局 C1 故事唔係喺「確定出發」嗰陣播**：撳「確定本週行程」嗰陣故事就開始（經 `commitPlanAndGo()` → `runScheduleFromToday()` 觸發）；`finish_intro` 要播晒佢＋閂「劇情結算」先返到地圖。
- **地點 sheet 有兩種形態**：placeholder 小 sheet（y=952，喺 viewport 外，內容「地點／點地圖針或下方本區列表選擇地點」）vs 真地點 fullscreen sheet（`locpanel118`，y=0 全屏，locTitle 如「金龍茶餐廳 · 油麻地」）。開地點嗰陣撞到故事／巧遇會搶走 sheet，要清咗佢哋再開先量到真 sheet。開 sheet 嗰陣有機會彈 enc79（diag Phase C 實測 enc:true）。
- **WF4 巧遇機制（B1 hunt 用）**：`wf4Hash` 係 FNV-1a 32-bit（offset 2166136261，prime 16777619）；`wf4Rand(key) = (wf4Hash(key) % 100000) / 100000`。`WF4_CFG = { pDay:0.30, pLoc:0.20, gapDays:2, repeatDays:45, locTriesPerDay:3, pendingMaxAge:2}`。`wf4TryLocEvent(locId)`：`st.pending` 阻擋；`st.lastDay === day` 阻擋；`wf4BaseOk()`（lastDay 起 2 日間隔、唔係報紙日、唔係強制日、唔係病假）；`enc79StoryPendingAt(locId)` 阻擋（嗰地點有主線幕等播，唔耗 try）；每日頭 3 次入場先擲；hash gate `wf4Rand("wf4loc:"+day+":"+locId+":"+locTries) >= 0.20` 就 skip；再 `wf4PickEvent("loc", locId)` 由池揀（DAILY_EVENTS_WF4 按 trig==="loc"＋ev.loc===locId 過濾，once 排除見過嘅，45 日重複冷卻，`wf4CondOk` 驗 year／season／tier／money／stress／flags）。`wf4DailyTick`：`wf4Rand("wf4day:"+day) < 0.30` 設 pending 日事件；`wf4PresentPending` 喺入地圖嗰陣播出。Daily gate 過嘅日子：day 0（0.1652）、4（0.0605）、9（0.1510）、10（0.0752）、11（0.2990）。diag run day-0 嗰次 enc 係 daily pending 事件，唔係 loc try（cafe_cha day-0 try1 gate 係 0.4623，唔過）。15 個地點 id：film_lion 獅子山製片、rec_hk 香江唱片、tvb_longmen 星河電視台、tvb_kowloon 九龍電視台、tvb_harbour 海港廣播、film_cotton 紅棉影業、film_harbour 維港電影、ad_central 中環廣告、ad_adm 金鐘創意、rec_wanchai 灣仔唱片、rec_star 天星音樂、cafe_cha 金龍茶餐廳、agency_ho 何生事務所、gift_shop 廟街禮品、hospital 仁康醫院。Gate-aware hunt 計劃喺 drive197h.py 入面計（Python FNV，`day_plan(day)` 每 try 揀一個 gate 會過嘅地點）。B1 巧遇最終喺 day 9 try 1（星河電視台）觸發。
- **todayPlanId()（L37717）讀 `S.weekPlan[weekdayIdx(S.dayIndex)]`**——week plan 係按 WEEKDAY（dayIndex%7）索引，唔係按 dayIndex。Day 0＝1990-01-01 星期一；day 8＝1990-01-09 星期二。自由日做法：設 `S.weekPlan[dayIndex%7]=null` 再經手帳來回重繪。地圖掣邏輯（L39025–39075）：`todayHasSoftSchedule()` 或 todayPlanId 係 map 日就出「開始今日行程」；冇 startToday 且 `!S.homeEditable` 且唔係強制日就出「過一日」（`#map-end-day`，v20a34＋v20a105 WEEK105 S-13 保底：任何非強制、非編輯、未有掣嘅日子一律補「過一日」，行 `confirmEarlyRestFromMenu()`）。過一日 click 行 `confirmEarlyRestFromMenu()`（L37827）：modal「確認過一日？」，掣 `[{label:"確定過一日", role:"d", on:()=>endBrowseDayGoHome()}, {label:"取消", role:"g"}]`。
- **三條日結路徑**：`afterDayModal()`（L37035）、`presentRestSleepDayEnd()`（L57365）、第二日結路徑（resolvePlannedDay 結果處理，~L38400）——三個都 call 同一個 `modal(html, btns, opts)`。拍攝板唔加 body.day-res-open（刻意，v189）；休息板加。`isRestCard = (id==="rest" || id==="home_chore")`。第二路徑：`if(isRestCard)` 加 body.day-res-open（L38457）；否則只加 mask day-res（L38504）附註解解釋點解。
- **其他 code 事實**：`#modal-btns` 基礎：`.btnrow{display:flex;gap:8px;...}`（L176）；`#modal-btns{position:sticky; bottom:0;...}`（L1794–1810）；modal 掣 `min-height:44px`（L1815）。`.awd62-stage`／`.awd62-frame`／`.awd62-canvaswrap`／`.awd62-skip` CSS 喺 L780–791；`.awd62-canvaswrap{position:relative}`。`#v-map` 結構（L5653 起）：`.bar` → `.menu` → `.map-wrap`（legend／polaroid／map-hint／map-stress-tip）→ `#loc-sheet`（absolute overlay）；`#map-hint` 喺 L5742（`.map-wrap` 內）。`openLoc()` L55080（新行號）；`scrollMapPinIntoView()` L39376 舊行號；`mapWrapEl()` L39366 舊行號。`* {box-sizing:border-box}`（L57）；`#app{width:min(390px,100%);...}`（L59）。測試目錄：`qa131/`（suite 入口 `qa131/run_suite.sh`）；`tests/`（static tests）。
- 一次 Python regex grep（搵 `#modal-btns` 規則）喺 5MB 檔上面 catastrophic backtracking，背景執行超過 100 秒，已用 process.kill 終止——教訓：唔好再用複雜 regex 掃成個 index.html；用 `grep -n`／`muse.read` 指定行號。

### 9.4 700 run

**Viewport run（`run_700_197.py`，0 pageerror）**：有數據嘅探針全部同 932 一致——B2 未確認 `(94,642) 296×52`；鎖定沉澱態 offsetW=296／offsetH=52，resetDisabled=true、resetDisplay=block、resetOpacity=0.35、quickDisplay=none、homeEditable=false；印章 noop=true；B5 吊牌 offsetW=102／offsetH=44、loc-close offsetW=362／offsetH=46；B6 sheet 開住 end_day `(46,629) 338×45`、hint `(32,565) 366×123`（y 差 232＝932−700）；B7 初 paint scrollTop=345，分類掣底 631 ＜ bar 頂 635，五粒 56×50 全部見晒；C1 五格 58×32、y=215；C7「本週安排」；C2「過一日」紙色 `#fffdf6` `(46,629) 338×45`；U6 同 932 一致（afterQuick open:true）。

**聚焦 700k（`drive197k.py`，0 pageerror）**：B1 主線 8 步全部 `(30,647) 370×44`，covered:false（932 係 `(30,879)`；647＝700−44−9，同一 9px 底距）。B4：soft modal y=138 H=546、rest modal y=138 H=546，掣 520／573／625 兩板一致，差 [0,0,0]，identical:true。注意：700 modal 實際高 546px（內容高，低過 tut-on 帽 616px；§9.2 嗰個 616px 係帽，唔係實高）。底錨驗算：700−546−16=138 ✓（932：932−720−16=196 ✓）。C4 對照：確定過一日 `(36,339) 358×44` 在上、取消 `(36,391)` 在下；maskAI center，modal y=251 H=198（(700−198)/2=251 ✓，置中）。

**聚焦 700l（`drive197l.py`，C3，0 pageerror）**：clean-sheet loop attempt 1，locTitle「金龍茶餐廳 · 油麻地」；五粒行動掣全部 338×60，x=41，y=282／349／416／483／550（67px pitch）——同 932（y=514／581／648／715／782）逐項一致，y 差 232。

**Driver 備註**：viewport run 嘅 b1／b4／c2／c3 探針喺 932 同 700 都係空——viewport run 嘅 B4 用 `pg.reload()`（live seed 會丟失，saveQ 靜默失敗，見 §9.3），所以嗰啲項要靠 dedicated final run（932i／j）同 700k／700l 先量到。`drive197k.py` 嘅 `zero_pageerror` 寫咗喺 `rec` 頂層唔係 probes 入面（值 True），探針腳本小不一致，留檔。

### 9.5 頒獎禮 run（B3＋C4 請柬，soft 模式）

**`run_awards197.py`（soft，0 pageerror）**：22 個 skip 樣本；pack：bestOutcome nominated，cat 最佳男主角 nominated；典禮播到尾（comfort beat「何生拍拍你膊頭」有出）。`?softPreview=1` 會觸發頭版 `location.replace` 加 `softRev=s107&v=20a10`，要等 redirect 定先。**Wrapper 原因**：`drive197.py` 嘅 R 由空開始，單跑 awards／700 會洗走 drive197.json 入面嘅 932 結果——`run_awards197.py`／`run_700_197.py` 先預載舊 JSON 再 merge 返。

- **C4 請柬**：出席 `(36,616) 358×45` class p、order 1，**在上**；推辭 `(36,669) 358×44` class g、order 1，**在下**；maskCls `mask tut-on on`。DOM 次序＝視覺次序＝肯定行在上。**驗證通過**（review 原量度係出席 y=668／推辭 y=616，即係倒轉；宜家修好）。
- **B3 跳過掣**：22 個樣本 x=327／w=83／h=38 固定；y 係 177／178／187／219——**同 review 數字完全一樣**。聚焦探針 `probe_awards_b3.py`（數據存 `qa197/b3probe.json`＋drive197.json `awards.b3_probe`）解開咗：skip parent 全部係 `awd62-canvaswrap`；**dy＝skip.y−wrap.y＝8、dx＝315，22 個樣本全部恆定；wrapH＝307 恆定。掣已釘死喺舞台上（B3 處方達成）。** 殘留 viewport y 變化係**成個 frame 自己郁**（frameY 169／170／179／211、frameH 510–594；frame 按內容高度垂直置中，所以佢嘅頂喺 viewport 入面郁）——review 嘅量度將「掣郁」同「舞台郁」混埋一齊。轉場嗰拍（t=10506，caption 空，frameH 510、frameY 211、skip y=219）都係 frame 收縮置中造成。要令 viewport y 都固定，就要釘死 frame 頂（唔再垂直置中）——會改典禮整體垂直佈局，係設計決定，唔喺 B3 處方範圍，留返畀統籌／用戶拍板，唔喺呢票靜靜擴範圍。

## 10. EPERM 事故＋恢復＋commit 紀錄（2026-11-13）

- **事故**：Suite B（`git stash -u` 攞 pristine）期間開始持續 EPERM。Suite B 返廢數 114 PASS／161 FAIL（harness 失效：每 test `> /tmp/suite_one.log` redirect 失敗，test 冇跑到就計 FAIL），唔係回歸。之後 `git stash pop` 連續失敗（`index.lock` 寫入 EPERM，exit 128）。我為咗繞過 index.lock 跑咗 `git archive stash@{0} | tar -x -C.`——**錯誤做法**：tar 逐個檔開寫（截斷做 0 bytes）再寫入，寫入 EPERM 失敗就留低 0-byte 檔案。結果 3488 檔顯示已改（大部分係 0 bytes），包括 index.html（0 bytes）、全部測試檔、NOTES、qa197/drive197.json。**教訓：唔好再用 tar 解壓去恢復**（截斷風險）；恢復一律用 temp＋校驗＋rename，或者等 `git stash pop` 得返。
- **EPERM 診斷**：O_EXCL 建立檔案一律 EPERM；plain 寫入逐次隨機翻動（有時 5.3MB 寫入成功，有時連 `echo test > file` 都失敗）；/tmp 寫入失敗；兩邊 repo 嘅 git object 寫入都失敗。寫入窗口按分鐘翻動。df：/tmp 512M tmpfs 用咗 26%，inode 用咗 1%；/home/hatch 150G 用咗 67%。`.git` 屬主 root:nogroup，shell 以 root（uid 0）行。恢復腳本 `~/workspace/restore197.py`（phase1 checkout-index／phase2 stash tracked 檔 md5 校驗重試／phase3 stash^3 untracked 檔／phase4 清理）＋`~/workspace/restore197b.py`（等寫入窗口）。
- **恢復**：寫入窗口喺 15:25 UTC 左右開咗。`git checkout-index -a -f` 還原全部 tracked 檔返 HEAD（pristine，index.html 60490 行）；`restore197.py 2` 還原 18 檔 tracked 改動（md5 校驗，18/18 OK）；`restore197.py 3` 還原 14 檔 untracked 工作檔（14/14 OK）；再補還原 39 張 `qa197/shots/` 截圖（39/39 OK）；`MaShanZheng-Regular.ttf`（5,857,936 bytes，tar 事故截斷做 0 bytes，checkout-index 漏咗）由 HEAD 單獨還原，md5 `741b48aa…` 同 HEAD 一致。核實：工作樹同 stash 完全一致（`git diff --quiet stash@{0} -- index.html tests/` PASS）；index.html 60584 行、md5 `eb7dce07ff3b5958bb357ce0ec8b0a27`，同事故前核實完全一致；全 repo 零 0-byte 檔（除咗正常空檔 `.nojekyll`；`qa197/b.lock`／`b.txt` 係 run 臨時檔，已刪）。兩份 scratch 目錄 `~/workspace/linji-restore197/`／`linji-restore197b/` 係垃圾，已由 phase4 清理。
- **commit＋push**：`git add` 嗰陣撞到死鎖 `.git/index.lock`（15:01 造，0 bytes，stale）——確認冇 git 程序行緊之後手動刪鎖再試。Commit `39bdd83c048857c52e8d8b383c45be37f58c8a2a`（71 檔，9437 insertions／178 deletions，工作樹乾淨）；`git push origin v20a197` 一次成功，常駐 clone `git ls-remote` 核實 `39bdd83…` 喺 `refs/heads/v20a197`。**第二 commit `f921d8b3164e8af63398634e3a2aec6e9529697a`**（25 檔：NOTES §9.4／§9.5／U4 toast／Suite B 更新＋`drive197.json` merge＋新 driver `drive197k/l/m.py`、`probe_awards_b3.py`、`run_700_197.py`、`run_awards197.py`、`b3probe.json`＋16 張新截圖），同樣已 push，常駐 clone 核實 `f921d8b…` 喺 `refs/heads/v20a197`，工作樹乾淨。**stash 仲未 drop**（`stash@{0}` WIP on v20a197: 2760680），留返做後備，落地後由統籌 drop。
- **未做**：冇。Suite B 有效重跑（§5）、700 run（§9.4）、頒獎禮 run（§9.5）、U4 toast 文案捕捉（§9.1）全部做完。殘留畀統籌／用戶拍板：B3 殘留 viewport y 變化係 frame 垂直置中造成（見 §9.5）——要釘死 frame 頂先解決，係設計決定。

## 11. Rebase 紀錄（2026-11-14，兩次 rebase）

### 11.1 第一次 rebase：上 main `2c1a680`（v195 NOTES）

- 開工核實 main HEAD `2c1a680`；基底 `2760680` 起已落地 v192／v195／v194／v198／v199；**v196 未落地**。
- `git rebase origin/main`：index.html 自動合併（60711＋94＝**60805 行**）；**8 份測試檔衝突**，全部純行號漂移，無語義衝突：`test_gift185_static.py`、`test_kwan151_static.py`、`test_rom176_static.py`、`test_tang152_static.py`、`test_tang171_static.py`、`test_tang173_static.py`、`test_text125_static.py`、`test_travel114_static.py`。
- 解法：取 HEAD（main）側＋difflib SequenceMatcher 映射（old＝`2c1a680` index.html → merged，全部錨點 equal 區，內容逐字核實）。映射（main→merged）：kwan151（31075→31130、31066→31121、27293→27348、31117→31172、31074→31129、27260→27315）；rom176（31629→31684、53634→53728、54002→54096、55141→55235、55235→55329）；tang152 0-based（31555→31610、31699→31754）；text125（27785→27840、27914→27969、33617→33672，歷史註解原封不動，另加一行 rebase 紀錄註解）；travel114 COUNT／FREE／DEF／WRAPPER 全數按映射重算（DEF 55204→55298、WRAPPER 44480→44573）；總行數 60711→60805；tang171／173 openLoc DEF 55204→55298。v197 側非衝突區嘅 pin 全部重跑 PASS，唔使再郁。
- 三個 commit 順利 replay，分支落喺 `2c1a680`（`174b4bf`／`0dc9a24`／`8d1cd23`）。
- 驗證（呢個中間樹）：新測試 `test_buttons197_static.py` **33/33 PASS**（§4 話 32 項係數錯——檔入面實際 33 個 `ok()`，grep 數過；0 FAIL）；兩段 JS `node --check` 通過；15 份 resync／相關測試＋3 份 logic JS 逐個直接跑全部 PASS；**全套 A 274/12**（`qa197/suite_rebaseA.txt`），FAIL 清單同基線逐字相同；**全套 B（pristine `2c1a680`）273/12**（`qa197/suite_rebaseB_2c1a680.txt`），同一 12 項。零回歸。

### 11.2 v200 喺 rebase 期間落地 → 第二次 rebase：上 main `4e841e5`

- **v200 落地**（`4e841e5`，修 v194 review C1＋C2；index.html 淨 ＋12 行，60711→60723，改動全部喺頒獎禮區 L46184–47612；新測試 2 檔；全套 275/12）。任務目標係「最新 main」，所以即刻再 rebase 一次，唔留喺舊 main 等統籌再做。
- 第一次 `git rebase origin/main` 起步失敗：「Please commit your changes or stash them before you merge」——當時背景正跑緊 Suite B（`/tmp` scratch），懷疑並行 job 干擾 checkout／cherry-pick；等背景 job 跑完、樹乾淨之後 `git rebase --continue` 即刻行到，之後一路順利。**教訓：唔好喺 rebase 期間並行跑全套；兩個動作要串行。**
- 第二次 rebase：index.html 自動合併（60723＋94＝**60817 行**，md5 `c326e03cc9a3a7362ea10b3d68d58854`）；**5 份測試檔衝突**（v200 郁過嗰 5 份：gift185／rom176／tang171／tang173／travel114），其餘 3 份（kwan151／tang152／text125）自動合併——全部純行號漂移，無語義衝突。解法同上（old＝`4e841e5` index.html → merged，全部 equal 區）：gift185 總行數 60723→60817；rom176（31629→31684、53646→53740、54014→54108、55153→55247、55247→55341）；tang171／173 總行數 60723→60817、openLoc DEF 55216→55310；travel114 48 個 pin 全數重算（DEF 55216→55310、WRAPPER 44480→44573；COUNT／FREE 見 `qa197/suite_rebaseB2.txt` 對照，內容逐個核實）。
- 三個 commit replay 完成，分支落喺 **`4e841e5`**（`9ed7446`／`2c8c6dd`／`35926ca`）。**v196 仍然未落地**（`origin/v20a196` 分支存在，唔喺 main）；v200 只郁頒獎禮邀請函文案＋佢自己嘅測試，**B4／B5 完全唔受影響**（日結板／手帳區零改動）。
- 驗證（最終樹）：新測試 33/33 PASS；v200 新測試 `test_awards200_static.py`／`test_awards200_logic.js` PASS；15 份 resync／相關測試＋3 份 logic JS 逐個直接跑全部 PASS；兩段 JS `node --check` 通過；**全套 A 276/12**（`qa197/suite_rebaseA2.txt`，276＝275＋1 新測試檔），**全套 B（pristine `4e841e5`）275/12**（`qa197/suite_rebaseB2.txt`），FAIL 清單兩邊逐字相同（12 項穩定 FAIL）。零回歸。

### 11.3 全套 B 嘅建造方法（disk quota 逼出嚟嘅改道）

- `git worktree add` 兩次失敗：`/tmp` 版「Could not reset index file to revision 'HEAD'」；workspace 版「Disk quota exceeded」（df 仲有 48G，係 quota 唔係爆碟；細寫入正常）。
- 改道：Suite B 用 `cp` 由常駐 clone（當時 HEAD 正係目標 main）抄 index.html＋tests／＋content／＋assets／＋根目錄檔案去 `/tmp` scratch，**逐檔 md5 校驗**（index.html md5 同 `git show <main>:index.html` 一致先跑）。教訓：scratch 唔可以中途再抄——第一次 B 跑出 267/18，查出係 v200 喺跑 suite 期間落地，常駐 clone 嘅 index.html 變咗 60723 行，我中途 `find -exec cp` 根目錄檔案嗰陣將 v200 版 index.html 蓋咗入 scratch（tests 仲係 `2c1a680` 版），6 項 pin／總行數測試因此 FAIL；還原返純 `2c1a680` index.html（md5 `c5fba297…`）之後嗰 6 項逐個 PASS，全套重跑返 **273/12**。第二次 B（`4e841e5`）由頭起 scratch，md5 `d6187b8e…` 核實，一次到位 **275/12**。中間嗰份受污染嘅 `suite_rebaseB.txt`（267/18）已刪，唔留檔。

### 11.4 實駕 spot re-verification（最終樹，932，0 pageerror 全程）

新 wrapper `qa197/run_rebase932.py`（預載舊 `drive197.json`，只重跑 `run_viewport(932)` 再 merge，唔洗走舊結果；`drive197.py main()` 會成個重寫 JSON，唔可以直接跑）。結果 merge 入 `qa197/drive197.json`（舊 key 全部保留；`awards.b3_probe` 俾 `run_awards197.py` 洗走咗一次，已由 `probe_awards_b3.py` 重跑補返，見 `qa197/b3probe_rebase.json`）。

| 項 | 重驗結果（最終樹） | 舊 run 對照 |
|---|---|---|
| B1 主線「下一句」 | `final5_runs.932`：8 步全部 `(30,879) 370×44`，covered:false | 舊 932 同值 |
| B1 巧遇「下一句」 | `final5_runs.932i`：day 9 try1 星河電視台，`.e79-btn` `(30,879) 370×44`，offsetW/H 370/44，撳一次推進成功（advanced:true） | 舊 932i 逐字相同（連對白句都一樣） |
| B3 跳過掣 | `probe_awards_b3.py` 22 樣本：dy＝8、dx＝315 全部恆定，parent 全部 `awd62-canvaswrap`，wrapH 307，skip (327, 83×38)；viewport y 177／178／187／219 照舊係 frame 郁（frameY 169／170／179／211），唔係掣郁 | 舊 dy／dx 完全相同 |
| C4 請柬 | 出席 `(36,616) 358×45` order 1 在上、推辭 `(36,669) 358×44` order 1 在下，mask `tut-on on` | 舊值逐字相同 |
| C4 過一日確認（對照） | 確定過一日 `(36,457) 358×44` 在上、取消 `(36,509)` 在下；modal y=369 H=194 置中；maskAI center | 舊值逐字相同（932i＋932j 兩邊都係） |
| B6「過一日」 | 自由日：乾淨／sheet 開住／閂 sheet 三態全部 `(46,861) 338×45`，hint `(32,797) 366×123`；932 viewport run b6_sheet_open 亦同舊值 | 舊值逐字相同 |
| B4 日結板 | `932j` b4_compare：soft／rest 同為 modal y=196 H=720，掣 y [756, 809, 861] 兩板一致，**掣 y 差 [0,0,0]，identical:true**；C4 對照仍置中 | 舊 932j 同值（舊 h／i run 嗰陣係補丁前數字 y=86／529，今次新 run 係補丁後數字——差異正正係 B4 補丁生效，唔係回歸） |

- 其餘 viewport run 探針（B2／B5／B7／C1–C3／C6／U1／U2／U4／U6）重跑值同舊 run 逐字相同（`viewport_runs.932` 整個 rec 同舊 run byte-identical；`b1_mainline` 喺呢個 driver 入面新舊都係 `[]`——B1 主線實數一向喺 `final5_runs.932`，見上表）。
- 12 張截圖重拍（`qa197/shots/`）：同一場景，bytes 輕微唔同（重渲染）；`awd_01_invite.png`／`awd_02_result.png` 係 v200 改咗邀請函文案所致。
- 700 冇重跑（任務只要求 932 spot；700 專用規則冇掂到——v200 同 rebase 都冇郁 700 media 規則；舊 700k／700l 結果保留喺 `drive197.json`）。

### 11.5 事故／教訓（rebase 新增）

- **regex `.*`＋DOTALL 截斷檔（兩次中招）**：解衝突腳本 pattern 入面 `^>>>>>>> .*\n` 嘅 `.*` 喺 `re.S` 下貪婪食到檔尾，將衝突點之後成個檔刪走（第一次 8 檔全中：gift185 85→43 行；第二次 5 檔全中）。兩次都即刻發現（行數核對），用 `git checkout -m` 還原衝突態重做，修正版 pattern 用 `^>>>>>>> [^\n]*\n`（`qa197/resync197.py` 本身冇呢個問題，唔使改；正確腳本留喺 `/tmp/resolve200.py`，唔入 repo）。**以後寫解衝突 regex：marker 行一律 `[^\n]*`，解完即刻 `wc -l`＋`grep marker` 核實先 `git add`。**
- **唔好喺 rebase 期間並行跑全套**（見 §11.2）：第一次 `rebase --continue` 失敗，疑似背景 Suite B 干擾；串行重試即刻得。
- **Suite B 唔好用 `git worktree`**（disk quota，見 §11.3）：改用 cp＋md5 校驗 scratch；scratch 建好之後唔好中途再抄嘢入去。
- **stash 仲未 drop**（`stash@{0}` WIP on v20a197: 2760680），留返畀統籌。
- **唔落地**（落地由統籌做）。下一個 rebase 目標：如果 v201／v196 落地，總行數／pin 基數會再變，resync 要由新 main 重新對位；`qa197/resync197.py` 嘅 `/tmp/pristine197.html` 係舊 `2760680` 版，已過時，唔好再用——用 `/tmp/map197.py`（difflib，old＝目標 main index.html、new＝合併後 index.html）。

