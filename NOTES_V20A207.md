# NOTES_V20A207 — v204 設計 review B2／B3＋C1–C5 修復（B1 按設計唔修）

## §0 範圍

- 來源：`~/workspace/linji-design-review-v204/REVIEW.md`（A 0／B 3／C 5），2026-11-14。
- 用戶 2026-11-14 14:33 拍板一次過修晒 B1–B3＋C1–C5；**2026-11-14 14:35 用戶再拍板 B1「不畫」**——魏詠男唔重畫，B1 結案為「按設計，唔修」。本票實做七項：B2、B3、C1、C2、C3、C4、C5。
- 基底：main `9e338d6`（v204 已落地，遊戲 `9436c71`）。分支 `v20a207`，工作副本 `~/workspace/linji-work207`。**唔落地**（落地次序：v205 先、v206 其次、v207 最後）。

## §1 B1 結案：按設計，唔修（用戶 2026-11-14 14:35 拍板「不畫」）

- Review 原指：魏詠男喺最佳女配角舞台望落似男角（短刺髮＋深青黑褸＋嚴肅面，同阿偉幾乎同一 silhouette），建議重畫一張 px 加女性辨識特徵。
- 用戶決定唔畫，原因：**佢原本設計就係剛強味，唔係畫錯**。舞台上面望落似男角係佢角色本身嘅剛強味，唔係缺陷；重畫佢女性化會背叛角色設定。
- 設計依據（`~/workspace/user/files/PLAN_CHAR_LOOKS_REF_v1.md` L83，`ngai_wingnaam`）：38 歲女、過氣武打女星，面型偏圓但下顎有力、眼神凌厲帶英氣、眉形粗且直、身型勻稱有肌肉線條、運動外套配背心／寬鬆功夫衫配束腳褲、武館實戰感。
- 處理：現有 3 檔 px（`assets/story/awards/px_ngai_wingnaam_{south,east,west}.png`）**原封不動**，唔改 code、唔改圖。B1 工人已於開工約 1 分鐘後叫停，唯一產物係一份未提交嘅 PixelLab prompt 草稿（已刪），**零 generations 花費**（餘額維持 3,889.67／5,000），無新 character 開過。

## §2 B2–B3／C1–C5（code 工人實做＋驗證，2026-11-14）

**改動總覽**：`index.html` 淨 +34 行（61432→**61466**；`git diff --numstat` 98 insertions／64 deletions）。**全部同行／原位改，之後再冇加行**——C3 提名版跟進＋C1 暗罩都係同行改（dimVeil207 係 1 行 compact helper 駁喺 spotlight207 收尾），行數維持 61466，resync pins 唔使重做。冇改 SAVE key／softRev／產品 `?v=`；冇直改 content pack JSON（C4 兩句係 inline JS const）。

### B2 舞台放大（932＋700 空帶收窄）
- 邏輯 canvas 480×360→**480×432（10:9）**，backing 720×540→**720×648**，`FLOOR` 262→**314**（地板 y274–372，98px＝22.7%；觀眾帶 y379–432，53px）。`awards181DrawBase` 用 H 衍生常數（`rb=H*36/360`、`curtB=H*228/360`、`floorB=H*310/360`、`edgeB=H*316/360`、`sy(y)=y*H/360`）。人物 dispH：fellow 112→**136**、player 116→**140**、tuxedo 112→**136**。獎盃 glyph：tuxedo −110→**−129**（頂 y185，board 底 179.3，gap 5.7；底 203，頭頂 206，gap 3px）、fellow 胸口 −52→**−61**。lightPool 高 99→**120**。彩紙 reset y>364→**436**。Glamour overlay aspect 480/360→**480/432**。舞台 `align-items:safe center`＋`overflow-y:auto`。提名版 700 慳位微調：caption padding 10→8px、tap margin 8→6px、cards margin-top 10→8px。
- 點解 H=432 唔係 480：H=480 會頂爆提名版 700 frame（617+99−8=708＞676 可用）。
- 實駕量度（pristine→修後）：932 frame y259→**232**、canvas 高 307→**366**；700 frame y143→**116**、canvas 366。932 上下空帶仍有（直向 viewport 闊度綁死，框闊 406 封頂），改善幅度溫和——殘留，見下。

### B3「跳過」掣唔再遮「角度」pill
- `.awd62-skip` `top:8px`→**`bottom:8px`**（canvaswrap 右下角＝地板前緣＋深色觀眾帶，人物腳底之下，唔遮任何 strip）。仲喺 canvaswrap 入面，z-index 3。
- 實駕：pristine 掣 rect x327–410 y267–305，同右 strip（「角度」pill，x225–408 y296–320）重疊 81×9＝729px²，pill 數字全遮；修後掣 y552–590（932）／436–474（700），重疊 **0**，掣喺下半。

### C1 揭曉得主 spotlight（兩輪：先 spotlight，後暗罩）
- 第一輪：新 `spotlight207(cx,w,fy)`（光柱 y40→腳底＋加光光池＋地面光暈），揭曉贏分支 `lightPool`→`spotlight207(fp.x,72,…)`、落選者 0.7→**0.55**；非贏分支 `spotlight207(fp.x,66,…)`、對手 0.6→**0.5**、玩家落選 0.9→**0.6**。Suspense 光池唔郁。
- **第一輪實駕 FAIL，根因係量度＋渲染雙重問題**：(a) 量度 bug——suspense beat caption「得獎者是……」本身含「得獎」，drive 影咗 suspense 唔係 reveal；slot 位亦錯（2 fellows 係 cx180/300，唔係硬編 75/240）。(b) 渲染真問題——舞台底係光色（白簾＋淺木地板），落選者 alpha 0.5 半透明只會令光底透出嚟，望落仲光過得主：實測得主 179.6 vs 落選者 179.0（gallery 932），提名版得主 93.9 vs 落選者 104.7（得主更暗）。
- 第二輪（最終）：新 `dimVeil207(cx)`（1 行 compact helper：橫向漸變暗罩，中間 0.45、邊緣漸隱，覆蓋 cx±30、FLOOR−118 至 FLOOR+6）；揭曉兩分支落選者改**實色 alpha 1＋`dimVeil207(slotCx(i))`**，唔再靠 alpha 減淡。得主 spotlight 不變。
- 最終實駕亮度（winner−loser，門檻 ≥12）：gallery 932 **183.1 vs 122.9（+60.2）**、gallery 700 **181.4 vs 123.7（+57.7）**、提名 700 **149.7 vs 117.7（+32.0）**、film gallery 932 **154.2 vs 121.1（+33.1）**。截圖目視：得主光、落選者企喺暗柱入面，一眼分到。
- drive 量度修正（`qa207/drive207.py`）：加 `slot_cxs(n)`＋`reveal_slots(fp,best,caption)`（由 caption `(\S+)憑《` 攞得主星名、由 `fp['cats']` 攞 fellows 次序計 settled cx，含 `fwd64` 向中間移 22%）；reveal 判定改為 `"得獎" in cap and cap.strip() != "得獎者是……"`,再等 **700ms**（winner 企定）先影相；記錄 `reveal_caption`＋`reveal_slots`。

### C2 結果卡獎盃金底 chip
- L818 金 chip 規則 selector 擴大，加 **`.psr-fellows63 img.ic112`**（同 glamour cap＋reveal caption 一樣：`#f2c14e` 底、22px），覆蓋 fellows 行 head legend 同得主標記。1x 睇截圖認到係獎盃（reveal caption 嗰隻同款金 chip 清晰可見）。

### C3 700 結果卡三格報紙＋聲望行齊見（兩輪）
- 第一輪（gallery 夠，提名版唔夠）：新 `.awd-sheet` 緊縮 block（L4130 後）：cards gap 8→**5px**、card padding 10→**6px 10px**、title .92→.88rem、body lh 1.35、kicker mb 1px、fellows 12px/lh 1.4/mt 2px、sub mb 6px、h mb 2px、dual mt 4px（慳 ~73px）。新 mask class `awd-sheet-on`：`#mask.awd-sheet-on:not(.tut-on).modal{max-height:min(88dvh,88svh,720px)!important}`（932 cap 720 不變）；`modal()` 由 `opts.awardSheet` 開關，`closeModal()` 清走，`presentAwardResult` 傳 `{awardSheet:true}`。註：淨收緊唔夠（gallery 700 缺口 140px：scroll 579 vs client 439），要加 cap。
- 第二輪（提名版跟進）：提名版 700 仍碌（scroll 601 vs client 509，第三格報紙「銷量／碟市」卡淨見 kicker、數值＋dual 行喺 fold 之下）→ cap 88→**94dvh**（700 modal 658px／inner ~551px；932 仍 min(94dvh,720px)=720）＋`#modal-btns` margin-top 4px／padding 6px 0 calc(8px＋safe-area)＋modal 上下 padding 8px；`.awd-sheet` 第二輪收緊：eyebrow mb 8→2px、cards margin 6px 0 8px→**2px 0 4px**、card padding 6→**5px** 10px、weak62 margin 6→2／padding 6→4／lh 1.5→1.35、comfort147 `margin:2px 0 0;font-size:.85rem;line-height:1.35`（註：`.modal p` L445 已將佢 margin 定做 `0 0 8px`，呢度只慳 ~8px 唔係初估 32px）、fellows mt 2→0／lh 1.4→1.3、sub mb 6→2、h margin 2→0、dual mt 4→2。估計總共慳 ~118px（缺口 92px）。
- 最終實駕：gallery 700 scroll/client **439/439**、提名 700 **550/550**、gallery 932 439/439、film 932 453/453——**全部唔碌**，三格報紙＋幕前聲望行齊見。
- 附帶發現：L3271 `#mask:not(.tut-on).modal{max-height:min(78dvh,720px)!important}` 會殺死 L1822 `@media (max-height:820px)` 嘅 88dvh relief（700 實測 modal 546 唔係 616）——今次用咗 scoped class（先例：`#mask.casting-sheet-on.modal` 88dvh、`#mask.day-res.modal` 92dvh）繞過，唔郁全域規則。

### C4 請柬斜槓寫法
- `VENUE99_INVITE_DEK`（inline JS const，唔係 pack JSON）：`award_harbour_ad`＋`award_harbour_film`「旁聽／入圍席位信」→「**席位信**」，其餘字句不變；音樂場照舊。實駕 film gallery 請柬確認：「你收到一張席位信——票房餘溫同台下掌聲，你揀。」

### C5 地圖「中環廣告」標籤
- `#map-names68` 嗰個 div inline style `left:60%`→**`left:51%`**（top `calc(57% + 30px)` 不變）。冇加新 CSS 規則（AGENTS.md L802 警告）；其餘 14 個標籤唔郁。
- 實駕量度：label 56×15，x188 y499；中心比率 (188+28−23)/384＝**0.503**（wrap 384 闊），喺地圖入面。截圖目視：地圖全見，「中環廣告」四隻字完整喺藍塔左邊，冇俾大廈遮（對照 review：舊位「廣」字俾塔遮半）。
- **量度陷阱（兩重）**：(a) game JS 開地圖後會將 inline left 寫成 px（`'192.956px'`），所以 drive 唔可以直接比 `'51%'`——改用 wrap 闊度計中心位比率（inline 51% 本身由 ui142／ux68 靜態釘死）。(b) new_game 後畫面係手帳頁，地圖未開（labels 0×0）；撳「返回地圖」之後**開場 C1 會全屏自動播，遮住地圖**——第一版 drive 嘅 map 截圖影住何生事務所，量度到嘅只係 DOM 數字。最終 drive 嘅 map case 會播完開場：撳「下一句」×17→抉擇（揀「跟張子駿班底學動作戲」；注意係**張子駿**唔係張子健）→再撳「下一句」→結算撳「關閉」，先量度＋截圖；加 `C5_no_story_overlay` 檢查（冇可見「下一句」掣）。

### 嚴重事故：M5 語法錯誤（已修，2026-11-14）
- 我 B2 改 backing 註釋嗰陣喺第 1 行尾加咗 `*/`，將原本兩行註釋斷開，第二行變裸 code → **`PAGEERROR: Unexpected identifier 'M5'`**，`S` 未定義，`new_game` 兩次 drive 全敗。Static 測試唔執行 JS，所以套件照過，頁面其實爛咗。修復：還原兩行註釋（第 1 行尾 `360→432；`，第 2 行尾 `。 */`）；`node --check` 抽出嚟嘅 inline script 驗證 MAIN SCRIPT SYNTAX OK。**教訓：改完 index.html 一定要 `node --check` 抽出嚟嘅主 script 先好跑 drive。**
- 附帶：第一個 debug script 漏咗 server（`python3 -m http.server 20790`，pid 46665，cwd work188）未停，搞到第二輪 debug 404——已 kill，port 20790 確認空閒。drive207.py 正確設定 `d.ROOT`／`d.PORT=20790`／`d.EXE`（drive188 預設 EXE 路徑唔存在）。

### 測試
- 新：`tests/test_awards207_static.py`，~58 項檢查（B2 幾何／B3 掣位／C1 spotlight207＋dimVeil207／C2 chip selector／C3 緊縮＋94dvh cap／C4 字眼／C5 left:51%）。**反證：pristine 48 項 FAIL，唔 crash。修後 TOTAL FAIL 0。**
- 13 個舊測試檔 resync 去新幾何（v181 前例）：`test_awards160_m1_static.py`、`test_awards160_m4_static.py`、`test_awards166_static.py`、`test_awards168_static.py`、`test_awards170_static.py`、`test_awards174_static.py`（chip selector 加 `.psr-fellows63`）、`test_awards177_static.py`、`test_awards181_static.py`、`test_awards187_logic.js`（mock render 改 `awards181DrawBase(ctx,480,432,0)`）、`test_awards187_static.py`、`test_awards190_logic.js`、`test_awards190_static.py`、`test_awards64_chibi_static.py`。關鍵值：FIG_W 46→51（dispH 136×48/128）、slot-gap 門檻 70→65px（177／181，保守 gap 69px）、board 底 149.4→179.3、glyph 頂 152→185。14 檔逐個 PASS。
- 11 檔 drift resync（suite B 新出 11 項 FAIL，全係行號漂移／有意改動，唔係產品回歸）：`qa207/resync207.py` 驗證 **73 pins，0 mismatch**（pristine 行內容＝現行行內容）；插入點（舊行號）：+12 @4130（C3 block）、+5 @5256（modal cap）、+1 @39677（modal toggle）、+1 @39697（closeModal）、+7 @47462（drawBase）、+8 @47810（spotlight）。正確 shift 區：<4130 +0；4130–5256 +12；5256–39677 +17；39677–39697 +18；39697–47462 +19；47462–47810 +26；>47810 +34。頭版 zone 表錯過一次（39697–47462 係 +19 唔係 +17，travel114 FREE 41510→**41529** 先啱）。`resync207_apply.py`＋`apply2/3/4.py`（kwan151 `line()` 同一 `ok()` 入面重複、travel114 set 尾個 `}` 要搵獨立行等坑）。11 檔逐個 PASS。
- 全套：基線 A（pristine）**287 PASS／13 FAIL**（`qa207/suite_pristineA.txt`）；B（修後、resync 前）277／24（11 項 drift pins）；C（resync 後）**288／13**，FAIL 清單同 A 一致；**D（最終 code：C3 提名版＋dimVeil207＋map 流程改動後）288／13，FAIL 清單同 A 完全一致**（`qa207/suite_workD.txt`）。**零回歸。**13 項 pre-existing FAIL（冇一項 awards 相關）：`test_flash51_static.py`、`test_giglib36_static.py`、`test_pacing35_static.py`、`test_poster59_static.py`、`test_rumor49_static.py`、`test_slot50_static.py`、`test_soft_tip_111_restore.py`、`test_start53_static.py`、`test_weave43_static.py`、`test_weave44_static.py`、`test_weave49_static.py`、`test_wf5_87_static.py`、`test_wrap38_static.py`。

### 實駕（`qa207/drive207.py`，Playwright＋本地 server，viewport 430×932／430×700）
- 最終結果：**5／6 cases PASS**（`qa207/drive207.json`，截圖 `qa207/shots207/v207_*`）。
  - music_gal_932 PASS：B2 canvas 366、frame y232；B3 重疊 0；C1 +60.2；C3 439/439；C2 金 chip 目視 OK；零 pageerror。
  - music_gal_700 PASS：frame y116；C1 +57.7；C3 439/439。
  - music_nom_700 PASS：C1 +32.0（得主駱家聲憑《熱浪之夏》）；C3 **550/550**（提名版唔碌）；請柬確認提名人（最佳新人獎《冬日暖歌賀歲合唱》）。
  - film_gal_932 PASS：C1 +33.1（得主魏詠男憑《離岸的信》）；C4「你收到一張席位信」確認。
  - music_won_932 **FAIL（`pack_outcome_won`）——結構問題，唔係 code 問題**：60 個 seeds（fame 80／rec 3）＋三組更強 stats（1991 fame 95 rec 5；1990 fame 120 credit 50 rec 5＋film 2；1992 fame 95 rec 5）全部 `nominated`，0 won——經 `debugForceSeasonWindow`＋tier `nominee` 攞唔到 won（同 drive188 前例：ad won 要 synthetic-pay probe）。贏分支同已驗證嘅非贏分支共用同一段 `spotlight207`＋`dimVeil207` code（淨係得主係着燕尾服嘅玩家），drive 保留 skip-documented 行為（20 seeds 搵唔到就 skip）。
  - map_932 PASS：label 56×15、中心比率 0.503、喺地圖入面、冇劇情遮住；截圖係乾淨地圖。
- Pristine 對照數字（probe207）：B2 gallery 932 frame y259–674（h415）、canvas 307、上下黑帶 259／~258px；B3 重疊 729px²；C3 gallery 700 scroll 579 vs client 439（缺口 140px）、提名 700 scroll 697；C4 film 請柬原文「你收到一張旁聽／入圍席位信」；C5 label left:60%、藍塔遮半。

### 殘留／落地注意
- **B2 932 改善幅度溫和**：frame y259→232（頂帶少 27px），因為直向 viewport 闊度綁死框闊（406px），舞台唔可以再闊；要再大就要改佈局（例如框貼邊／改 canvas 比例），唔喺今票範圍。
- **Won 分支已實駕（落地統籌補驗，見 §3）**：強 seed（fame 80／credit 60／跨媒介作品）seed 1 即 won；music won 932 全場 12/12 PASS，揭曉亮度差 +51.0（得主 148.7 vs 落選者 97.7）。
- **基底已追上**：落地統籌 rebase 上 main `8cecf7f`（v206），新 HEAD `be9e748`；見 §3。

## §3 Rebase 上 v206＋重驗（落地統籌，2026-11-14）
- Rebase：分支基底 `9e338d6`（v204）→ main `8cecf7f`（v206 落地後）；新 HEAD `be9e748`。index.html 自動合併（v206 WF4 pity＋v207 spotlight 並存）；5 個測試檔衝突，全部係行號漂移——`/tmp/verify207.py` 73 錨點對位零 mismatch（v206 +25：C1 +22／C2 +3，插入點 ~41129／41271 之後；v207 +34；合併後總行數 61491），內容逐字核實純漂移；其餘 19 個 v207 resync 檔自動合併後逐個跑過，全部 PASS。教訓：rebase 解析腳本唔好靠 nearest-to-expect 揀重複行（hospital onDismiss 兩行同文，險些揀錯 30981→30994），要用算術＋內容雙重核實；解析後補換行唔見咗會黐埋下一行（tang173、travel114 COUNT `}` 各中一次，ast.parse 捉到）。
- 新測試：`tests/test_awards207_static.py` TOTAL FAIL 0；24 個 resync 檔＋2 個 logic 檔（187／190）全部 PASS；主 script `node --check` 過關。
- 全套 A/B（`qa207/suite_rebaseA.txt`／`suite_rebaseB.txt`）：pristine（main `8cecf7f`）**290／13** → 工作版 **291／13**；FAIL 清單逐項相同（13 項已知 pre-existing），+1 係本票新測試，**零回歸**。
- 實駕重跑（`qa207/drive207.py`，新 drive207.json）：**5／6 PASS**，0 pageerror；5 場檢查全 true（B2 canvas 366／frame y232、B3 重疊 0、C1 +32 至 +60、C3 439/439・550/550、C4 席位信、C5 標籤完整）。
- **Won 種子再試（今次試到，見 `qa207/won_sweep207.py`／`won_stage207.py`）**：上一任 60 seeds 攞唔到 won，係 seed 太弱（fame 80／credit 0／淨 rec 3，base 0.82＜贏線 0.875），唔係結構問題。v208 式強 seed（fame 80／credit 60／rec 3＋film_lead 2＋tv_lead 2＋ad_lead 1）四組（music 1990／1991、film 1990／1991）全部 seed 1 即 won（`qa207/won_sweep207.json`）。再用強 seed 跑 music won 932 全場（`qa207/won_stage207.json`）：**12／12 PASS**，揭曉「得獎！最佳新人獎：《冬日暖歌賀歲合唱》」，亮度差 **+51.0**（148.7 vs 97.7，門檻 ≥12），B2 frame y143／canvas 366、B3 重疊 0、C3 scroll 458＝client 458、零 pageerror。Won 分支缺口已補，唔再係殘留。
- 檔案：QA 新增 `qa207/won_sweep207.py`／`won_sweep207.json`／`won_stage207.py`／`won_stage207.json`／`suite_rebaseA.txt`／`suite_rebaseB.txt`；drive207.json＋9 張截圖重跑更新；won 截圖 4 張新增。
- 檔案：code `index.html`（61466 行）；測試 `tests/test_awards207_static.py`＋上述 24 個 resync 檔；QA `qa207/`（`probe207.py`、`drive207.py`、`resync207.py`、`resync207_apply.py`＋`apply2/3/4.py`、`suite_pristineA.txt`、`suite_workB.txt`、`suite_workC.txt`、`suite_workD.txt`、`drive207.json`、`shots207/`）。

## §4 落地紀錄（2026-11-14）
- 遊戲 commit `1a9ac75`（squash merge `v20a207`，分支 HEAD `41f97e5`，rebase 上 main `8cecf7f`）；NOTES commit 本檔。
- 線上核實：index.html **5,462,493 bytes，sha256 `ca54a4041f378e0d76a866eb346eb7d26b37b03d7e0fdc031b8f8bd7247d39b7`**，同 repo HEAD 一致（初次 curl 係舊版，Pages 部署滯後約 3 分鐘，第二次核實先一致）。
- 重驗（rebase 後）：新測試 0 FAIL；24 個 resync＋2 logic 檔全 PASS；全套 pristine 290／13 → 工作版 291／13（+1 係本票新測試，FAIL 清單逐項相同，零回歸）；實駕重跑 5／6（5 場全 true；won 場用弱 seed 攞唔到，見 §3）；won 強 seed 全場 12／12 PASS（亮度差 +51.0）。
- 落地次序：v205 → v206（`8b5c460`）→ **v207（`1a9ac75`）** → v208 → v209。
