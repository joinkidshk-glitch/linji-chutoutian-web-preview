# NOTES_V20A211 — 修 v207 設計 review 七項（A1＋B1＋B2＋C1–C3＋B7）

- **分支**：`v20a211`，base main `b7ddb37`（遊戲 `1a9ac75`）。**Hold 分支，唔落地、唔 push**（v208 落地緊；rebase 留返落地嗰陣做）。
- **證據**：review `~/workspace/linji-design-review-v207/REVIEW.md`；基線實駕 `qa211/drive211_baseline.json`（pristine，未改 code，10 場 0/10——預期失敗全部重現）；工作版實駕 `qa211/drive211.json`；實駕腳本 `qa211/drive211.py`（沿 `qa188/drive188.py` helpers：`new_game`／`seed`／`force_pack_try`，經 `window.__awards.debugForceSeasonWindow`）；新測試 `tests/test_awards211_static.py`（47 項）；舊測試 resync 腳本 `qa211/resync211.py`；改動腳本 `qa211/apply211.py`。
- **唔直改 content pack JSON**：全部改動都係 `index.html` 內呈現層／helper，pack 數據／判定一字唔郁。

## §1 每項修法

### A1 — 700 提名版結果卡眉題俾 toast 票根遮住
- **根源**：`presentAwardResult` 開卡之後自己再叫 `toast(…・結果, {stamp:true})`——toast z540 企喺 modal 之上，700 提名版 modal 頂 y34–53，眉題 y44–83，成行／半行俾 toast（y8–76）蓋住。基線實駕：music_nom_700 重疊 4160px²、film_nom_700 重疊 6400px²，結果卡開出嗰刻 `toastOn=true`。
- **修法**：新增 `hideToast211()`（清 `toast._t` 計時＋`on/has-stamp/has-sub`＋children＋aria＋`app.toast-up`，寫法跟 `prog175AdoptToast` 同一套），`presentAwardResult` 開卡前叫佢，刪走開卡後嗰句 `toast()`。`toast()` 本身一字唔改，其他 toast 用途唔受影響；結果 modal 94dvh cap 唔郁。
- **驗證**：10 場結果卡開出嗰刻 `toastOn=false`、眉題重疊 0px²；2 秒後再驗仍然 off（唔係靠 1.8s timer 自然熄先過關）。

### B1 — 932 上下黑帶各 232px（49.8%）
- **修法**：雙幾何——`HS211 = innerHeight ≥850 ? 540 : 432`（高 viewport 用 480×540，×1.25；矮 viewport 留 480×432）。揀雙幾何嘅原因：700 提名版 frame 已經 644px（＋C2 字幕釘死後 668px），canvas 再高會頂爆 700 viewport 出捲軸；932 先有空間放大。`HSC211 = HS211/432`，FLOOR（314→393）／人物 dispH（136／140→170／175）／光池（120→150）／glyph（−129／−61→−161／−76）／閃粉 y 帶／彩紙底界（HS211＋4）／glamour overlay aspect（inline `480/HS211`，CSS 480/432 留做短 viewport 後備）／canvas backing（`Math.round(HS211*1.5)`，432→648／540→810）全部按比例換算，跟 v207 B2 ×1.2 同一做法。闊度唔郁（W 480、slotCx 間距 120、setTransform 1.5）、唔拉伸、drawBase 地板比例唔郁（22.7%）、觀眾暗帶唔加唔減、**舞台-only 方向不變（冇加返觀眾席／紅地毯／觀眾剪影帶）**。
- **驗證（實駕）**：gallery 932 frame y232→**175**、h469→**583**，上下黑帶各 **232→175px（−57px，−24.6%）**；won／提名 932 frame h758，黑帶 87px；提名 700 frame h668（y16，總高 692＜700，唔出捲軸）；人物比例唔變形（FLOOR 佔 canvas 高 72.7% 兩邊一致；企位 slotCx 唔郁）；揭曉亮度差全部 ≥12（見 B7 下）。

### B2 — won 版銷量／碟市卡 stub 句
- **根源**：`awardWinner149` 喺 won 分支刻意回 null（得主係阿偉，唔係對手），`renderAwardResultHtml` 嘅 metric 卡 `win149 ? … : stub` 跌返「——典禮後仍有人提起。」。
- **修法**：加 `win211 = win149 || (won 類別 ? {star:"阿偉", title: wonCat.repWorkTitle || pack.repWork62} : null)`，metric 卡改用 `awardWinLine149(win211)`，沿用同一模板。作品名動態取，唔寫死。gallery／提名版（win149 有對手）唔郁；冇得主嗰陣 stub 分支保留。
- **驗證**：won 三格——music「銷量／碟市——阿偉憑《冬日暖歌賀歲合唱》奪獎，典禮後仍有人提起。」、film「票房話題——阿偉憑《新春大吉》奪獎，典禮後仍有人提起。」；全場結果卡 stub 句「——典禮後仍有人提起。」0 命中。ad won 實玩攞唔到（20 seeds 無 won，見 §4），但修法係 medium-agnostic（同一模板＋同一 won 類別邏輯），film＋music 已證實。

### C1 — won 版「同屆提名」行無圖例／得主標記
- **修法**：`awards63FellowsHtml` 喺 `c.outcome === "won"` 嗰陣，喺 fellows 名單前加玩家一行「🏆 阿偉《代表作》」（`iconHtml112("🏆")` 金底 chip，同 v207 C2 一致；代表作由 `c.repWorkTitle` 動態取），行首一併加「（🏆 為得主）」圖例。gallery／提名版邏輯（winner63／fellows[0] fallback）唔郁。
- **驗證**：won 版同屆提名行「同屆提名（🏆 為得主）：🏆 阿偉《冬日暖歌賀歲合唱》、駱家聲《熱浪之夏》、…」（film 版阿偉《新春大吉》）；gallery／提名版圖例照舊。

### C2 — names→reveal frame 跳位 7–12px
- **根源（基線實測）**：字幕框高度隨字幕行數變——names 69px／suspense 54px／reveal 54–93px；frame 差＝字幕差（gallery Δ15、music 提名 700 Δ24，逐 px 吻合）。唔係卡列收起（`syncCards` 從來唔會喺 reveal 收卡，卡列 `visibility:hidden` 留位一直有效）。
- **修法**：`.awd62-caption` 由 `min-height:54px` 改做 `height:93px`（全域 `border-box`，93 即總高＝實測最長揭曉字幕 3 行高；1–2 行留空唔縮）。空字幕 beat（walkup／glamour）`display:none` 維持不變——嗰兩段跳位係 v174 已接受嘅 trade-off（glamour 同時收起卡列）。
- **驗證**：10 場 names→reveal frame 位移 **0px**（高差 0px），932＋700、提名／贏獎／旁聽三版全部 0。

### C3 — 請柬席位兩行重複
- **修法**：`renderAwardInviteHtml` 嘅 `tierBit`（「席位：…」）喺 gallery 嗰陣唔出（`(pack.tier === "gallery") ? ""`），留返 gate 行「今晚席位：觀禮。」；nominee 嗰陣 gate 行係入圍門檻句、唔講席位，`tierBit`「席位：入圍／提名」保留（唔係成個刪，否則提名版請柬會冇咗席位資訊）。
- **驗證**：三份 gallery 請柬（film／ad／music）「席位：旁聽席」0 命中，席位行各只得「今晚席位：觀禮。」一行；提名版請柬「席位：入圍／提名」保留。

### B7 — 揭曉 spotlight 改做由上射落嚟嘅光柱（用戶 2026-11-14 16:46 追加）
- **原狀**：`spotlight207` 係直身光柱（上下同闊，`fillRect(cx-w/2-14, 40, w+28, F-40)`，望落似光管），用戶睇完揭曉截圖要求改做由上射落嚟嘅光柱。
- **修法**：保留 `spotlight207(cx, w, fy)` 簽名＋兩個呼叫點（won 72／非贏 66，跟 `fp.x` 得主 slot 企位），入面改做梯形光柱：上窄（`topW = w×0.5`）由框頂 **y=0** 起，下闊（`botW = w＋44`）到腳底 F；暖白縱向漸變（0.42→0.20）＋中央亮芯梯形（收窄版，方向感）＋腳底光池／光灘保留。喺 canvas 層畫、得主人物之前畫（人物唔會被光蓋住）；DOM 文字層（橫額／數字條／白牌／字幕／卡列）喺 canvas 之上，唔會被遮。`dimVeil207` 落選者暗罩一字唔郁；suspense 照舊 `lightPool`。
- **驗證**：揭曉亮度差（得主 vs 落選者，門檻 ≥12）——全部 ≥26.5（見 §3 實駕表）；光柱 canvas 像素直讀（6 個高度取樣，見 §3）：框頂亮度差 +85 至 +103、腳底亮度差 +4.7 至 +12.7、中段暖色偏移（R−B）+15 至 +27。**量度方法註**：暖白光柱喺米白幕布上亮度差本來細（R 升 B 跌互相抵消，y200 亮度差 −0.7 但暖色差 +17），所以中段改用量暖色偏移——探針 `qa211/probe_beam211.py` 校準（music_nom_700：y80／140／200 暖色差 +20／+27／+17）。截圖 `qa211/shots211/v211_*_reveal.png` 肉眼可見光柱由框頂連到得主腳底。

## §2 測試

- **新測試**：`tests/test_awards211_static.py`，**47 項全綠**；對 pristine（`/tmp/index211_pre_apply.html`，main `b7ddb37`）跑：**30 項新斷言 FAIL**（唔 crash），17 項守衛 PASS——反證成立。
- **舊測試 resync**：B1 雙幾何令 8 檔舊測試嘅硬編碼幾何斷言失效（160_m1／170／174／177／181／187／190／207 static＋187／190 logic，全部係 FLOOR 314／dispH 136／140／glyph −129／−61／光池 120／彩紙 436／canvas 480×432／720×648 嗰族），按 v207 B2 resync 前例更新到新形式（短基準值不變，高 viewport ×HSC211；純算術斷言唔郁），腳本 `qa211/resync211.py`（逐檔核實替換次數；.js 檔頭註解由 `#` 改返 `//`，否則 node 語法錯誤）。Resync 後 10 檔全部 ALL PASS（207 檔 TOTAL FAIL 0）。
- **舊測試 resync（第二輪）**：全套 A/B 跑出 9 項新增 FAIL，全部係我淨 +42 行引起嘅機械漂移（行數釘／幾何字面）＋v200 C2 同 C3 刻意行為改動（見下）。腳本 `qa211/resync211b.py`（difflib 對位 pristine worktree vs 工作版，逐個釘行內容核實純漂移）＋`qa211/resync211c.py` 補尾＋166 嗰行 muse.edit 手改（JSON 顯示層將普通 `"` 印成 `\"`，兩次轉義誤判，逐字對比先發現檔案根本冇反斜槓）。更新：travel114（COUNT 12／FREE 33／DEF 55963→56005／WRAPPER 45180→45187）、rom176（4 釘行）、tang171／173（總行數 61491→61533、DEF 55963→56005）、gift185（總行數）、160_m4（glyph −129→`Math.round(129 * HSC211)`）、166（glamHtml 加 inline aspect-ratio）、64_chibi（FLOOR／dispH ×HSC211）、200 logic（C2 gallery 席位斷言改做去重後期望：「席位：旁聽席」0 命中＋「今晚席位：觀禮。」在場＋全 slate＋（觀禮）唔郁）。9 檔逐個對 pristine 直接覆驗（pristine 全綠、工作版 FAIL）證實係我改動引起，resync 後 9 檔全部 ALL PASS。
- **全套 A/B**：`qa131/run_suite.sh` 對 pristine worktree（`b7ddb37`）vs 工作版。pristine **291 PASS／13 FAIL**（`qa211/suite_pristine211.txt`）；工作版第一跑 283／22（9 項新增，見上）；resync 後第二跑 **292 PASS／13 FAIL**（`qa211/suite_work211.txt`），FAIL 清單同 pristine **逐項相同，零新增**（+1 PASS 係新測試 `test_awards211_static.py`）。13 項穩定 FAIL：flash51／giglib36／pacing35／poster59／rumor49／slot50／soft_tip_111_restore／start53／weave43／weave44／weave49／wf5_87／wrap38（同 pristine 一致）。註：`/tmp/index211_pre_apply.html` 喺服務重啟嗰陣俾 tmpfs 清走咗，A/B 改用 pristine worktree 做對照；worktree 已刪（磁碟紀律）。

## §3 實駕（`qa211/drive211.py`，本地 serve＋Playwright headless_shell）

- 場次：10 場（music／film／ad × gallery／nominee／won × 932／700；won 用強 seed：fame 80／credit 60／rec 3＋film_lead 2＋tv_lead 2＋ad_lead 1，seed 1 即 won）。
- 結果：**9/10 PASS**（`qa211/drive211.json`，第三次跑，`qa211/drive211_work3.log`）。唯一跳過：`ad_won_932`——強 seed 20 seeds 無 won（pre-existing，見 §4），唔計分。基線（pristine）10 場 0/10，預期失敗全部重現。
- 0 pageerror（10 場全部）。
- B1：gallery 932 frame y232→175、h469→583，黑帶各 232→175px（−57px，−24.6%）；won／提名 932 frame h758，黑帶 87px；提名 700 frame h668（y16，總高 692＜700，唔出捲軸）。
- C2：10 場 names→reveal frame 位移 0px（高差 0px），932＋700、三版全部 0。
- A1：10 場結果卡開出嗰刻 `toastOn=false`、眉題重疊 0px²；2 秒後再驗仍然 off。
- B2：全場 stub 句「——典禮後仍有人提起。」0 命中；結果卡 scroll＝client 全部場次成立。
- C3：三份 gallery 請柬「席位：旁聽席」0 命中。
- 揭曉亮度差（得主 vs 落選者，同一框，門檻 ≥12）：music_gal_932 +55.5、music_gal_700 +48.7、music_nom_700 +32.9、film_nom_700 +31.6、film_gal_932 +26.5、ad_gal_932 +69.6、music_won_932 +52.5、music_won_700 +51.9、film_won_932 +47.7——**全部 ≥26.5**（基線 +27 至 +61；film_gal_932 由 +35.5 跌到 +26.5，仍然遠高於門檻）。
- B7 光柱像素直讀（6 個高度取樣，`qa211/probe_beam211.py` 校準方法）：框頂亮度差 +85 至 +103、腳底亮度差 +4.7 至 +12.7、中段暖色偏移（R−B）+15 至 +27（4 個中段取樣中至少 3 個 ≥8；第 4 個係腳底附近 F-40 暖色差 +5 至 +12）。截圖 `qa211/shots211/v211_*_reveal.png` 肉眼可見光柱由框頂連到得主腳底。

## §4 已知／殘留

- **ad won 實玩攞唔到**：強 seed 20 seeds 無 won（pre-existing，已知：廣告男主角實玩贏線到唔到，見 MEMORY 審計殘留 B2）。B2／C1 修法係 medium-agnostic，film＋music won 已證實，ad won 只係未有實駕樣本，唔係修法缺口。
- **700 提名版 frame 餘量**：字幕釘死 93px 後提名 700 frame h668（y16，總高 692／700，剩 8px）。B1 雙幾何門檻 innerHeight ≥850 就係為咗保住呢 8px——唔好將門檻降低，否則 700 提名版會出捲軸。
- **walkup／glamour beat frame 跳位**：空字幕 `display:none`＋glamour 卡列 `display:none` 仍然會令 frame 跳，係 v174 已接受嘅 trade-off，C2 只修 names→reveal（review 嗰項）。
- **報紙重設計進行緊**（用戶 2026-11-14 16:47 起，樣本另派）：結果卡將來會改做 90 年代報紙版式；本票嘅修法（toast 收起／點名得主／圖例）喺新版式入面一樣適用，唔使等。

## §5 落地紀錄（rebase＋重驗完成，待 squash merge）

- **狀態**：分支 `v20a211` 已 rebase 上 main `f58f19c`（v208），新 HEAD **`258dbe4`**；工作樹乾淨（淨係 untracked QA 證據檔）。**待 squash merge → main → push → 線上核實。**
- **Rebase（`b7ddb37` → `f58f19c`）**：**6 個衝突，全部已解，兩邊改動齊**——`index.html` 1 處（glamour HTML：v208 用 `glamRep208`，v211 加 `aspect-ratio:480/HS211`，合併後兩邊齊；核實 v211 標記齊 hideToast211 ×2、HS211 ×8、win211 ×2、caption 93px、tierBit guard、spotlight207 ×3，v208 標記齊 buildSlots208 ×3、buildCardsData208 ×3、glamRep208 ×3；總行數 61756）＋5 個 static 測試純行號漂移（gift185／rom176／tang171／tang173／travel114，`diff -U0` 26 hunks 逐個釘行核實後重寫：openLoc DEF 56228、rom176 釘 54658／55026／56165／56259、travel114 COUNT 12／FREE 33／DEF 56228／WRAPPER 45187）。`node --check` OK。6 檔重跑全部 PASS。
- **重驗（rebase 後）**：新測試 47 項全綠＋5 個 resync 測試全綠；全套 A/B pristine `linji-pristine211b`（`f58f19c`）**293／13** vs 工作版 **294／13**（+1 係新測試），FAIL 清單逐項相同，**零回歸**（13 項穩定 pre-existing FAIL 同 v208 基線一致）；實駕 `qa211/drive211e.py` **9/10 PASS**（見 §6，ad_won_932 跳過係 pre-existing）。
- **B1 重新量度（逐格流程，唔沿用單格 175px）**：932 frame y80／h773，上下黑帶各 **~80px**（v208 review ~144px、v207 232px）；700 frame y12／h683，頂黑帶 ~12px、底 ~5px。C2 names→reveal 位移 **0px**（9 場全部）。B7 光柱：框頂亮度差 **+76.7 至 +130.2**（門檻 ≥20）、腳底 **+7.1 至 +12.2**（門檻 ≥3）、中段暖色偏移 **+13 至 +27**（門檻 ≥8，3 行以上）。C1 揭曉亮度差（得主 vs 鄰位落選者）**+13.1 至 +61.2**（門檻 ≥12；最緊係 film_won_932 +13.1）。
- **落地嗰陣要做**：常駐 clone 檢查撞車 → checkout main → `git merge --squash v20a211` → commit → push main（deploy key 隧道）→ curl 線上核實 bytes＋sha → 派設計 review → 清 `linji-work211`＋`linji-pristine211b`（分支留喺常駐 clone）。落地次序 v211 → v212 → v209 → v213 → v214（v212 實作完成 hold 緊，v213／v214 已開工，唔好掂）。

## §6 實駕探針修正史（rebase 後三輪，量度方法問題，唔係遊戲回歸）

- **drive211b（4/10）**：舊探針用 pack 名匹配搵得主格，但 `debugForceSeasonWindow` 返嚟嘅 pack 只得一個 category，逐格流程第一格嘅名唔喺 pack 入面，fallback 誤揀（film_gal 腳底探針落喺落選者暗罩，讀到 40）。另揭曉 700ms 採樣嗰陣得主仲行緊，光柱頂未去到 settled 位。
- **drive211c（6/10）**：改用 DOM `.win` 卡定得主 slot＋揭曉採樣 1400ms。film_gal／ad_gal 轉綠；剩 music_gal（兩高度）＋film_won——canvas 逐格 profile＋時序採樣證實光柱本身正確（框頂 y=20 光柱喺得主身上，+0ms 行緊→+350ms 企定，光柱頂中心 ~95–100，唔係假設嘅 111）。**根因：探針假設舞台永遠 3 格**——gallery 之夜 focus 格（音樂新人獎，`awards63FocusCat` gallery fallback 返 `cats[0]`）玩家會企上台，4 格 [60／180／300／420]，得主 settled ~100；卡列得 3 張（`buildCardsData208` 要 `repTitle` 先出玩家卡，gallery repTitle 空，玩家卡唔出），所以卡數推唔到 slot 幾何。film_won 第一格係非玩家格（卡 0 唔係玩家位），舊 mapping 一樣錯。
- **drive211d（4/10）**：改由 canvas 直接探測（`JS_STAGE`：figure-band 暗像素分群＋y=20 最光窗口），企位探測本身啱（music gallery 4 個人 [99／178／299／414]、film gallery 3 個人 [110／240／404]、won 格玩家得主 [193]），但兩處探針設定錯：腳行 +38 落喺得主腿上面（讀到 46，唔係光池）；落選者取最遠嗰位，佢件花恤衫淺色拉高讀數，C1 得返 +6。
- **drive211e（9/10）**：腳行改 +45（避開腿闊 ±24px，喺光柱底半闊 ~51px 內）＋落選者改取最近嗰位（同 v207 校準一致）＋B7 wcx 直接用得主人物中心。9 場全過，0 pageerror。證據 `qa211/drive211_rebased4.json`＋截圖 `qa211/shots211e/`；探針腳本 `qa211/drive211e.py`（舊版 drive211b／c／d 留檔，唔好再跑）。
- **遊戲發現（v208 pre-existing，唔係 v211 回歸，唔喺本票修）**：gallery 之夜 focus 格玩家企上台（4 個人），但卡列得 3 張、冇玩家卡——舞台同卡列對玩家在場講法唔一致；兼 enter_pan 字幕話「今晚你坐喺觀禮席」，但玩家明明企喺台上。已報畀落地統籌（即係我）→ 轉交 parent 決定開唔開票（v212 已完成，唔好塞入去）。
- **已知**：ad won 實玩攞唔到（見 §4）；700 提名版 frame 餘量 8px，B1 門檻 innerHeight ≥850 唔好降低。
