# NOTES_V20A212 — v208 設計 review 七項修復（頒獎禮逐格流程）

分支 `v20a212`，基底 main `f58f19c`（v208 已上線）。**Hold：唔落地、唔 push，等統籌派落地。**
工作副本 `~/workspace/linji-work212`；實駕／測試／resync 檔案喺 `qa212/`（`drive212.py`、`rerun212.py`、`probe_c1.py`、`probe_nest.py`、`probe_nest2.py`、`resync212.py`、`apply_resync212.py`、`drive212.json`、`suite212_base.txt`、`suite212_work.txt`、`suite212_work2.txt`、`shots212/`）。

## 修法＋驗證（每項一句）

- **A1（won glamour beat 跳過掣遮 cap 尾段）**：揀方案 (a)——glamour 期間收起跳過掣（`syncGlamour` 按 `isGlam212` toggle `glamour-hide`；CSS `.awd62-skip.glamour-hide{display:none}`），cap 文字唔郁。實駕：won 932＋700 glamour 探針（+900ms）skip `display:none`、cap 全文「最佳男配角：《新春大吉》」在場；截圖目視 cap 三行全部可見，右下角無掣。
- **B1（非玩家格得主重複）**：`awards208NightCats` 加 `used212` set＋`key212`（星｜作品）；後格揀第一位未贏過組合嘅提名人，池唔夠 fallback＝`fellows[0]`（唔死局）；懸念句三句輪換 `SUSPENSE212`（第一格沿用舊句，ms 唔郁）。實駕 film／music／ad 三晚得主組合全部去重（film：男配 陸柏言《歲歲平安》／女配 鍾楚凝《凶樓夜半怪談》／女主 蘇芷茵《春日新潮時裝特輯》／男主 廖炳星《三年》），懸念句唔重複。邊界（刻意）：玩家格 won 得主 null 唔入 used；玩家格 nominated 嘅 `winner63` 豁免（結果卡／報紙／log 讀 `pack.categories`，唔郁），但預先登記入 `used212`，令前面 gallery 格避開嗰個組合；fellows 池本身唔改。
- **C1（格標題 beat 卡列全空 ~170px 黑洞）**：`syncCards` 加 catTitle 分支（加 `on`＋`preview212`；提名 beat 除返），CSS `.awd63-cards.preview212 .awd63-card{opacity:.22;transform:none}`——dimmed 剪影，等宣佈先上色上名。**追加根因修復（實駕捉到，見下節）**：`applyCatState208` 舊 code 將成個 `<div class="awd63-cards">` 容器塞入 `cardsEl.innerHTML`，巢狀第二層冇 `.on`／`.preview212`，base rule `visibility:hidden` 令第 2 格起全部卡片隱形——改做 `cardsHtmlFor208` → 只回傳內層卡片嘅 `cardsInnerHtmlFor208`，容器外殼只喺建台嗰陣加一次。實駕：catTitle 期間 preview 卡可見——DOM（全部格 `cardsPrev`＋`visibility:visible`）＋截圖（音樂尾格 dim_pct 32.04%、廣告 cat2 42.81%，對照全空 0.0%）；目視三張 dimmed 卡（名＋作品可讀）。
- **C2（提名 beat 卡片追唔上字幕 ~0.1–0.5s）**：`advance()` 嗰刻即刻 `syncCards(beats[beatIdx], 0)`（卡片同字幕同一 JS task 出），loop 逐 tick 跟進照舊。實駕：每句提名字幕第一次見到 → 第一張卡 `shown>=1` 嘅 lag 全部 ≤250ms（上限），7 場全過。
- **C3（宣佈嗰位「行前＋光池」靜態睇唔出）**：提名 beat 改用 reveal 級 `spotlight207` 光柱＋行前 10→16（`fwdY212 = Math.round(16 * fwd208)`）；懸念 beat 照舊 `lightPool`。實駕：同一 slot 宣佈嗰陣 vs 未宣佈嗰陣，side-band 亮度宣佈嗰邊高（film_nom nom1／nom2 對照）。
- **C4（walkup 初段阿偉同陸柏言重疊）**：walkup 期間，行經路線上嘅提名人（`slotCx(i) < targetX` 且 `wp < 1`）`alpha 0.45`＋`y: -10`；行到埗（`wp = 1`）還原。實駕＋目視 walkup_mid／late：阿偉由台左行入，陸柏言淡色褪後，兩人唔重疊。
- **C5（最佳女歌手格得 2 位提名人，台中留空）**：`slotCx` 加 `if(slots.length === 2) return [200, 280][i]`（置中，80 gap）；3 位 `[75, 240, 405]` 唔郁；音樂池數據唔郁。實駕：figure centres 實測 198／278（目標 200／280 ±25），目視兩人置中。

## C1 追加根因調查（值得睇：第一次 drive 5/7 嘅原因）

第一次 drive212：5/7 PASS——music_gal（C5＋C1）同 ad_dec（C1）影像量度 FAIL，但 DOM 層 `cards_preview_at_cat_title` 全部 true。逐層剝開：

1. 卡列區亮度量度：music lastcat／ad cat2 截圖卡列區 mean 17.6／max 19，同全空對照帶一樣——卡真係冇畫出嚟，唔係探針閾值問題。
2. 即時探針（`qa212/probe_c1.py`）：第 1 格 catTitle 一切正常——CSSOM 有 preview 規則、卡 `opacity: 0.22`、截圖區 mean 34.1／gt50 31.7%，三張 dimmed 卡目視清晰。**第 1 格冇事。**
3. 容器普查（`qa212/probe_nest2.py`）：第 2 格起出現**兩個** `.awd63-cards` 容器——外層（`on preview212`、visible）入面巢狀多一個內層（冇 class、`visibility:hidden`），全部卡片喺內層入面，計算 `visibility: hidden`（opacity 1／0.22 都冇用）。根源：`applyCatState208` 格轉換嗰陣 `cardsEl.innerHTML = cardsHtmlFor208(cardsData)`，而 `cardsHtmlFor208` 回傳成個容器；`curCatIdx208` 起始 0（建台已設），所以第 1 格 early return 冇事，第 2 格起先巢狀。外層 probe（`querySelector('.awd63-cards')` 攞第一個）永遠顯示 visible——DOM 證據被呃咗，截圖先講真話。**呢個係 pre-existing bug（v208 或更早）**：第 2 格起提名／懸念／揭曉卡片全部隱形——v208 review 嘅音樂女歌手提名截圖亮像素 2.55%（對照有卡 13–22%）就係同一個病。
4. 修法見上文 C1（`cardsInnerHtmlFor208`，零行數淨變動，`wc -l` 維持 61753，唔使再 resync）。修完再探：cat 1 提名／cat 2 格標題／cat 2 懸念全部得返一個容器，卡 `visibility: visible`（preview 0.22／full 1）。
5. 探針本身亦執咗兩處（`drive212.py`，唔係遊戲 code）：C5 `figure_centers` 掟走掂住 frame 邊嘅紅幕布假 group（真人實測 199／278，幕布 group [0,31]／[374,405] 令 `len==2` 斷言失敗）；C1 影像檢查由 `>120 bright_pct` 改 `>50 dim_pct`（preview 卡亮度上限 ~66，>120 永遠 0%）＋截圖後補影一張防 stale frame。

## 測試

- 新 `tests/test_awards212_logic.js`（11 項，全過）：B1 去重（film 4 格／music 3 格 distinct、degenerate fallback 唔 crash、focus-nominated 預先登記、focus-won null）、懸念輪換序列＋1400ms＋全晚總秒數 50850 唔郁、揭曉 caption 跟去重後得主、fellows 池次序唔郁。
- 新 `tests/test_awards212_static.py`（**28 項**，全過；原 24＋C1 根因 4 項）：A1／B1／C1 preview／C1 巢狀根因（內層 builder／建台包殼／格轉換只換內層／冇殘留）／C2／C3／C4／C5＋唔郁守衛。
- 改 `tests/test_awards208_logic.js`（1 句斷言）：非玩家格得主由「＝fellows[0]」改「跨格去重（首格＝fellows[0]，後格揀未贏過嗰位）」。
- 改 `tests/test_awards208_static.py`（1 個錨點）：`cardsHtmlFor208` → `cardsInnerHtmlFor208`（改名，意圖唔郁）。
- 反證（pristine main `f58f19c`，`~/workspace/linji-pristine212`）：212 logic FAIL 6、212 static FAIL **18**（原 14＋根因 4）、208 logic FAIL 1（改咗嗰句）、208 static FAIL 1（改名錨點）；全部乾淨 FAIL，唔 crash。
- 相關舊測試逐個覆驗（工作版，全過）：awards63／168／174／177／178／181／182／186／187／188（logic＋static）、awards160_m4／m6／m9、awards177／178／181／182／186／187／188 static；另 gift185／kwan151／rom176／tang152／171／173／text125／travel114（resync 後，全過）。

## 全套 A/B（`qa131/run_suite.sh`，絕對路徑出檔）

- A 基線（pristine）：**293 PASS／13 FAIL**（`qa212/suite212_base.txt`）。
- B 工作版（巢狀修復後重跑，`qa212/suite212_work2.txt`）：**295 PASS／13 FAIL**——＋2 係新加嘅 212 測試檔；FAIL 清單逐項一致，13 項全部係穩定 pre-existing（flash51、giglib36、pacing35、poster59、rumor49、slot50、soft_tip_111_restore、start53、weave43、weave44、weave49、wf5_87、wrap38）。零回歸。
- 行數：index.html 61753 行（pristine 61714，淨 ＋39）；resync 咗 10 個 static 測試嘅釘行（`qa212/resync212.py`＋`apply_resync212.py`，difflib 對位核實全部純漂移；rom176 7 處／kwan151 24 處引用係同一釘行多處重用，唔係計錯）。

## 實駕（`qa212/drive212.py`，本地鏡像＋Playwright headless_shell，live 模式）

- 第一次：5/7（C1 巢狀根因＋C5 幕布假 group＋C1 閾值三個探針／根因問題，見上文）。
- 根因修復＋探針修正後重跑兩場（`qa212/rerun212.py`）：**7/7 PASS，0 pageerror**——film_nom_932、film_won_932、film_won_700、music_gal_932、ad_dec_932、film_skip_700、map_932。
- 關鍵數字：A1 skip `display:none`＋cap 全文（932＋700）；B1 三晚得主組合全去重、懸念三句輪換；C1 音樂尾格 dim_pct 32.04%／廣告 cat2 42.81%（全空 0.0%）；C2 提名 lag 全部 ≤250ms；C3 side-band 宣佈邊光啲；C4 walkup_mid／late 目視唔重疊；C5 centres 198／278；全晚總長誤差 ±5s 內；跳過掣第 2 格即完＋結果卡即出。

## 落地注意

- 本分支只郁 `index.html`＋測試，未掂 content pack JSON。v211 改咗舞台幾何（480×540），唔喺呢個基底入面——rebase 上 main 嗰陣要留意 `slotCx`／`FLOOR`／卡列幾何有冇衝突（統籌跟）。
- `cardsHtmlFor208` 已改名做 `cardsInnerHtmlFor208`（只回傳內層卡片）；其他測試／文件再提舊名只係 label（awards182 static 第 64 行 label），斷言本身唔受影響。

## Rebase 上 main `b1ca47a`（v211 已落地；落地統籌，2026-11-14 約 19:00）

- 舊 HEAD `30d07fb`（基底 v208 `f58f19c`）→ 新 HEAD `7603f87`。**衝突 6 處**：index.html 1 處＋5 個 static 測試行號漂移（gift185、rom176、tang171、tang173、travel114）。
- index.html 衝突：v211 嘅 `FLOOR = Math.round(314 * HSC211)`（高舞台 480×540，H＝540，backing 720×810）同 v212 嘅 2-slot `[200, 280]`——兩邊都要，保留晒。v211 canvas 闊仍係 480，C5 座標唔使改。核實：`cardsInnerHtmlFor208`（L47919／47940／48040）、`.awd62-skip.glamour-hide`（L799）、FLOOR 公式（L48005）全部齊。
- 行號漂移 resync（`qa212/resync212_rebase.py`＋`resync212_rebase_apply.py`，difflib 對位）：總行數 61753→**61795**（61756＋39）；openLoc 56225→**56267**；rom176 54655→54697、55023→55065、56162→56204、56256→56298（6152／31713 唔郁）；travel114 COUNT／FREE／DEF 56267／WRAPPER 45188；kwan151／tang152 全部釘行 identity 唔郁；全部釘行喺 equal block，純漂移。
- **resync 捉到嘅 bug**：`remap_block` 用 `"}"` 做 end marker，撞到 FREE 區塊註解入面 `{travelFree}` 嘅 `}`，提早截斷，FREE 冇 remap 到——已修做 `ln.strip() == "}"`，重跑後 FREE 正確（41555→41562、54478→54520 等）。教訓：block 結尾判斷唔可以用 `"}" in line`。
- 主 inline script `node --check` 通過（4,440,115 bytes；注意：貪婪 regex `<script>(.*)</script>` 會跨 tag 抽錯，要搵最大嗰個 block）。

## Rebase 後重驗（落地統籌，2026-11-14 約 19:00）

- 新測試逐個直接跑：212 logic（11）＋212 static（28）＋208 logic＋208 static 全綠；gift185／rom176／tang171（22／22）／tang173（21／21）／travel114／awards211 static（FAIL 0）／awards168／174／177／kwan151／tang152／text125／awards63 logic／awards178／181／182／186／187／188 static 全部 PASS。
- 全套 A/B（`qa131/run_suite.sh`，絕對路徑出檔；pristine `~/workspace/linji-pristine212b` ＝ main `b1ca47a`）：**A 基線 294 PASS／13 FAIL vs B 工作版 296 PASS／13 FAIL**——＋2 係新加嘅 212 測試檔；FAIL 清單逐項一致，13 項全部係穩定 pre-existing（flash51、giglib36、pacing35、poster59、rumor49、slot50、soft_tip_111_restore、start53、weave43、weave44、weave49、wf5_87、wrap38）。零回歸。（基線由 293→294 係 v211 加咗 awards211_static。）
- 實駕重跑（`qa212/drive212_rebased.py`，同一 seed `seed_used: 1`，寫入 `qa212/drive212_rebased.json`，唔覆蓋舊 `drive212.json`）：**7/7 PASS，0 pageerror**——film_nom_932、film_won_932、film_won_700、music_gal_932、ad_dec_932、film_skip_700、map_932。
- 關鍵數字（同舊基底 drive212.json 同 seed 對數一致）：B1 film_nom winner_keys `陸柏言|歲歲平安、鍾楚凝|凶樓夜半怪談、蘇芷茵|歲晚街頭、廖炳星|幽靈夜巡隊`（4 個 distinct；NOTES 舊版寫嘅《春日新潮時裝特輯》／《三年》係另一 seed／run，唔係呢個）；film_won 3 鍵＋玩家格 won 豁免；music_gal `廖炳星|三年、藍若曦|三年、駱家聲|三年`（星唔同，鍵 distinct）；ad_dec 4 個 distinct；懸念三句輪換（第 4 格循環返第一句）；A1 won 兩場 skip `display:none`＋cap 全文；C1 音樂尾格 dim 32.04%／廣告 cat2 42.81%（根因修復前全空 0.0%）；C2 lag 全部 ≤250ms；C3 宣佈邊光啲；C5 centres 198／278（目標 [200, 280]）。
- 註：重跑腳本尾段打印 winner 嗰陣有個小 bug（`winner` 係字串唔係 dict，`AttributeError`）——JSON 本身喺打印之前已經寫好，7/7 結果唔受影響；winner_keys 由 JSON 直接讀。

## 落地紀錄（2026-11-14 約 19:20）

- 遊戲 commit `a7be9a8`（squash merge 自分支 `v20a212` `63b987d`，基底 main `b1ca47a`）；NOTES commit（本檔）跟後補。
- 線上核實：`curl` index.html **5,487,683 bytes sha `cbad0769e5c176abab560899ea87f29636d71023780f6d15961c03f9c43a93ed`**，同 repo HEAD `a7be9a8` 一致（push 後約 4 分鐘先傳播到 Pages，初核仍係 v211 舊 sha，唔係 push 失敗）。
- 落地次序：v211 → **v212（本版）** → v209 → v213 → v214。
- 設計 review 已派（`~/workspace/linji-design-review-v212/`），重點逐項核實 v211 review 嘅 A1／B1／C1／C3／C5 喺 live 修好。
