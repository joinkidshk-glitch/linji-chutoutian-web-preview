# NOTES_V20A335 — 板短卡補返人情免試鏡金色提示

- 工作副本：`~/workspace/linji-work335`，分支 `v335`，base `1219f34`（v334）。
- 問題：v158 實駕抽檢（77 PASS／2 FAIL）唯一發現——金提示 `favor158Html` 只寫喺
  `gigCardHtml`，live 唯一 call 位係手帳「待試鏡（未獲聘）」列表（L46187）；板上兩層短卡
  各自另行渲染，零 `favor158` 引用。實測持有 `credit_enc79_mak_wuzhi`＋《街頭快跑》上板，
  卡面零 `.gold` 元素；彭渠道一樣。玩家喺板上唔知邊張可以用人情免試鏡，要逐張撳入詳情
  先見到。詳情頁金提示＋掣本身正常，功能識得，淨係板卡呢層漏咗。v20a158 註解話
  「卡面多一行金色提示」喺板上從來冇實現過。

## 一、改動（index.html 淨 +16 行，47,256 → 47,272；兩層）

### 第一層：modal 板短卡 `gigBoardTeaserHtml`（舊 L18001，＋7 行）
- 加 `favor158Html` 計算（同 `gigCardHtml` 同一寫法＋`typeof` 守衛＋try／catch），template
  內插 `${favor158Html}`（`${intelMark}` 之後、`${gapHtml}` 之前）。提示文案／樣式同詳情頁
  同一行（`favor158ChannelHintHtml(g)` 原文 `<p class="gold">`，唔另寫一套字）；
  `favor158ChannelForGig` 本身只喺 canAudition 過關＋持有對應債權＋啱類別嗰陣先返非空，
  唔使另加閘。彭渠道用減半台風計資格，鎖定卡都可能出提示（同詳情頁鎖定分支 v20a300 一致）。
- CSS（舊 L2937 `.gt-hint` 之後，＋2 行）：`.gig-teaser .gold{ font-size:.72rem;
  line-height:1.45; margin:6px 0 0; }`——短卡版式收細（跟 `.gt-meta` 同級），金色本身沿用
  全局 `.gold`／modal 內深金粗體 rule。
- `showTutBoardStage` 用同一 `gigBoardTeaserHtml`，一併受惠，唔使另改。

### 第二層：地點面板接通告掣 `addLocGigActs`（舊 L42396，＋9 行）
- 實駕覆驗發現：mak 場景 A1 檢查嗰層係地點面板 `#loc-acts` 嘅 `button.act` 短卡
  （截圖 `mak-board.png` 親見：「接通告：《街頭快跑》動作替身」係 act 掣），唔經
  `gigBoardTeaserHtml`，第一層覆蓋唔到，A1 FAIL（hint=''）。
- 修法：`addLocGigActs` 內計 `favor158Gold`（`favor158ChannelForGig(g).hint` 包做
  `<div class="gold">`；同一閘，唔使另加），經 `add()` 新加嘅選填第 6 參數 `extraHtml`
  傳入三個接通告掣分支（鎖定／試鏡入口／ready；已獲聘「查看檔期」掣唔傳）。
  唔放 `.h`——`.h` 係單行截短（`-webkit-line-clamp: 1`），放咗都睇唔到；改放掣內獨立金行。
- `add()`（舊 L42636）簽名加 `extraHtml`＋2 行註解，innerHTML 喺 `.h` 之後插
  `${extraHtml||""}`；舊 call 位全部唔傳，行為不變。
- CSS（舊 L2089 `#loc-sheet.sheet .act .h` 之後，＋2 行）：
  `#loc-sheet.sheet .act .gold{ color:#8a5a00; font-weight:700; font-size:.66rem;
  line-height:1.4; margin-top:2px; }`——深金免同米白掣底撞色，掣內描述尺寸。
- 註：brief 話「doScout 短卡 markup 兩處」唔準確——doScout 只負責 modal 板
  （經 `gigBoardTeaserHtml`）；`#loc-acts` 掣由 `addLocGigActs` 另行渲染，兩層要分開補。

### 唔郁
- `gigCardHtml`／詳情頁／兌現流程／守衛全部唔郁；手帳列表 L46187 繼續出提示（唔重複）。

## 二、測試

- 新檔 `tests/test_r335_board_favor158_hint.js`：35 項 ALL PASS。
  - A（modal 板，武指）：ready 卡有提示（字串同詳情頁逐字相同、只出一次）；無債權／
    閘未過／唔啱類別（臨記搬運、喜劇）／已兌現 → 無提示。
  - B（modal 板，彭）：ready 卡有提示；鎖定卡（全數台風 45 唔夠、減半 23 過到）有提示＋
    寫明「台風要求 45→23」＋卡態照鎖；開局台風 14《今夜歡笑》（15→8）有提示；
    減半都唔夠 → 無提示。
  - C（靜態）：teaser 呼叫、`.gig-teaser .gold`、`gigCardHtml` 原封不動、add() extraHtml
    參數、addLocGigActs 傳 favor158Gold、`.act .gold` CSS 規則。
  - D（地點掣，addLocGigActs）：武指 ready 掣有金行（文字同 `favor158ChannelForGig`
    逐字相同、標題＋成功率 hint 照常）；無債權／閘未過（鎖定掣）→ 無金行；彭鎖定掣有金行＋
    寫明 45→23；彭 ready 掣有金行；減半都唔夠 → 無金行；已獲聘「查看檔期」掣無金行。
- 全套 suite：TOTAL PASS 388 FAIL 9（v334 基線 387／9＋新檔 1 項），9 項 FAIL 同基線
  逐項一致（flash51／slot50／soft_tip_111_restore／start53／weave43_static／
  weave44_static／weave49_static／wf5_87／wrap38，全部已知 pre-existing），零回歸。
  證據 `~/workspace/suite335b.txt`。第一跑 385／12 係行號釘未 resync（rom159／tang152／
  text125），經 `qa335/resync335b.py` 補齊後回 388／9，唔係回歸。
- resync：`qa335/resync335.py`（第一層，＋7，5 檔）＋`qa335/resync335b.py`（第二層，
  總計 ＋16，10 個 difflib hunk，8 檔：rom159／tang152／text125 三檔新 resync＋
  gift185／tang171／tang173／rom176／travel114 五檔第二層 shift；逐錨內容核實純漂移）。
  三檔逐個直接跑全部 PASS（rom159 156 項、tang152、text125）。

## 三、實駕覆驗

- 用 `~/workspace/linji-drive158/drive158_run.py` harness（BASE 指去工作副本本地
  `http://127.0.0.1:18082/`，證據放 `~/workspace/linji-drive335/`，唔覆蓋 v158 原圖）：
  - mak 場景：A1-card-gold-hint **PASS**（hint='人情可用：武指照應——紅棉武指認住你，
    此武打通告無須試鏡，直接獲聘。'）；其餘 A1／A2／A3／D4 全部 PASS，0 FAIL。
    截圖 `mak-board.png` 親見金行喺「接通告：《街頭快跑》動作替身」掣內，深金兩行，版式完好。
  - pang 場景：pang-card-gold-hint **PASS**（hint='人情可用：慈善騷頂班——彭少祺開聲引薦，
    台風要求 15→8，此司儀通告無須試鏡，直接獲聘。'）；20 項 CHECK 全部 PASS，0 FAIL。
    另加一次性截圖 `pang-teaser-gold.png`：modal 板《今夜歡笑》teaser 卡金行在位，深金粗體，
    版式完好。
  - v158 原本 2 FAIL（mak／pang 板卡金提示缺失）全部清零；v335 修復嗰個唯一 bug 已實駕證實。

## 四、落地

- 內容 commit `644bce1`（工作副本分支 `v335`）→ main `e123d17`，已 push；Pages index.html
  md5 `fb55e2ed96eb5c0831115c06f30cba9c`／4,702,814 bytes，byte-identical。
- 工作副本已刪；常駐 clone tracked 乾淨，`qa296/derive296.json` 已還原。
