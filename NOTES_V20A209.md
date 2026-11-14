# NOTES_V20A209 — 藍若曦 6 張全身圖補米白光邊

## §1 背景
- 用戶 2026-11-14 14:59 重申「所有角色都要描白邊」。即時實測：v205 新出嘅
  藍若曦 6 張全身圖完全冇米白光邊——最外 3px 不透明帶米白佔比 base 0.23%／
  sad 0.12%／serious 0.17%／shy 0.16%／smile 0.16%／think 0.25%，對照
  `lin_hiu_base.webp` 100%。v205 設計 review 冇捉到呢點。違反既定規則
  （米白光邊約 3 CSS px、RGB(243,233,210)、焗入圖檔），要修。
- 本票只做光邊。v205 review 其餘項目（B2／C1／C2／C3）用戶未拍板，唔喺本票。

## §2 改動（6 檔，同檔名覆蓋；index.html 零改動；code 零改動）
- `assets/story/fullbody/lan_ruoxi_base.webp`（792×2448，不變）
- `assets/story/fullbody/lan_ruoxi_sad.webp`（762×2350，不變）
- `assets/story/fullbody/lan_ruoxi_serious.webp`（763×2352，不變）
- `assets/story/fullbody/lan_ruoxi_shy.webp`（764×2352，不變）
- `assets/story/fullbody/lan_ruoxi_smile.webp`（764×2353，不變）
- `assets/story/fullbody/lan_ruoxi_think.webp`（757×2349，不變）
- 檔案變大約 190KB → 約 224KB（webp q95；見 §3）。
- 舊版 sha（main a426947 實量；base 同 NOTES_V20A205 §6 一致）：
  base `9ecf648e…`、sad `1dd25bf5…`、serious `9157a11e…`、shy `a72b1b1c…`、
  smile `a4b2e146…`、think `e2a720c5…`（全值見測試檔 OLD_SHA）。

## §3 方法
- 對照量度（`lin_hiu_base.webp`）：最外 3px 帶米白 100%；光邊闊度
  mode 16px（median 17，左右／底一致）；光邊色 (244,234,210)≈規格
  (243,233,210)；最外像素 alpha 約 204、次層約 253（兩級羽化）。
  16 圖像 px ≈ 3.3 CSS px（圖高 ~2400px、舞台顯示 ~500px），吻合「約 3 CSS px」。
- 做法（腳本 `/tmp/v209_outline.py`，工作副本外，唔入 repo）：
  core＝alpha≥128 → Euclidean distance transform → ring＝0<dist≤16px →
  米白 (243,233,210) 層（外緣兩級羽化 alpha 200／250）→ 原圖 composite
  喺光邊層上面（保留人物本身羽化邊）→ webp q95 method 6。
  光邊只向外加，唔食裙邊（原像素唔郁；白裙完整，見實駕截圖）。
- 迭代：第一版用 Chebyshev（8-neighbour）擴張——band test 過（99.64%），但
  v107 口徑 far-cream FAIL（~5000px：對角線角位歐氏距離 ~22.6px，超出
  r+1=18）；第二版改歐氏圓盤（distance transform），far＝0。由 v205 原始檔
  重建，唔係喺第一版上面再疊。
- 人物保存核實：實心內部 RGB 漂移平均 ~0.9（q95 重編碼噪聲；max 12–14，
  ~150px／~800k 超過 8）；實心像素數 +1.1%——邊緣羽化像素喺米白層上面
  變成不透明，同參照 bake 機制一致，唔係人物變大。
- 參照檔本身都係 tight crop（四邊 margin 皆 0），lan 原檔亦然（T0 B0）——
  光邊喺畫框邊緣截斷，同參照行為一致，唔使加 padding。

## §4 測試
- 新測試 `tests/test_lan209_outline_static.py`：**44 項全綠，0 FAIL**。
  - 6 張：存在、尺寸不變、sha 同 v205 舊版唔同、四角 alpha 0；
  - 最外 3px 帶米白佔比：base 99.99%、sad 100.00%、serious 100.00%、
    shy 100.00%、smile 100.00%、think 100.00%（門檻 ≥0.95）；
  - v107 口徑 ring 米白 1.0000（r=17）、零遠處米白（0）；
  - 對照 lin_hiu_base 100.00%／ring 1.0000；
  - 基線：SAVE key／softRev／產品 ?v= 不變。
  - 反證：舊版 band share（0.12–0.25%）→ checker 全部報問題；現版零問題。
- 反證（pristine main a426947，常駐 clone）：同一測試 **13 項 FAIL**
  （6 張 sha＋6 張 band＋反證現版項），乾淨 FAIL。
- 全套 A/B（`qa131/run_suite.sh`，兩參數）：
  - 工作版：**288／13**；pristine（main a426947）：**287／13**。
  - 差 1 PASS 係本票新測試；13 項 FAIL 逐項同 v205 基線一致
    （flash51／giglib36／pacing35／poster59／rumor49／slot50／
    soft_tip_111_restore／start53／weave43／weave44／weave49／wf5_87／wrap38），
    work-only／pristine-only FAIL 皆空，**零回歸**。
  - 注意：第一次全套跑到一半俾我嘅 `pkill -f "http.server 20992"` 誤殺
    （pattern 撞到自己 shell 嘅 command line，連帶終止咗 suite；教訓：
    pkill 唔好用含 command line 字串嘅 pattern，要用精確 pid／port 匹配）；
    第二次重跑完整。

## §5 實駕（本地鏡像＋Playwright，腳本 `qa209/drive209.py`，log `qa209/drive209.json`）
- 播晒 R_lan 4 節（meet／push1／crisis／ending；serious 嗰節冇對白，唔入舞台）：
  base／shy／smile／sad／think 逐個表情上台，6 張 webp HTTP 全部 200，
  0 pageerror，破圖 0。
- 光邊喺舞台底色上面清楚見到（見 `qa209/shots/v209_R_lan_meet_smile_s3.png`）：
  成個剪影一圈米白，頭髮／蝴蝶結／黃上衣／白裙／腿全部有邊，白裙唔見食邊。
- 變暗跟隨：旁白句（R_lan_meet s2／s5、crisis s3、ending s2／s6／s7）嗰陣
  同一張 img 嘅 filter 係 `brightness(0.6)`，光邊連人物一齊變暗
  （見 `qa209/shots/v209_R_lan_meet_base_s2.png` 對照 s3）；講者句係
  `brightness(1)`。光邊焗入圖檔，所以必然跟住變暗，DOM＋截圖雙重證實。
- 36 條 console 404 全部係已知缺圖（`rom_lan_*` 5 檔 ×3 副檔名＋
  `bg_loc_home_airport`，curl HEAD 核實全部 404；v205 已記錄 pre-existing，
  同本票無關）。headless_shell 截圖對白文字有殘影（已知 artifact），
  以 DOM 文字為準。
- 備註：藍若曦只喺 R_lan 5 節有對白，全部 pcSilent、阿偉唔上台——所以
  「聽者變暗」只能夠用旁白句（單人 0.60）驗證，冇雙人聽者場面可以驗；
  機制本身係同一張 img 嘅 filter，雙人場面亦一樣跟隨。

## §6 落地前檢查（本票 HOLD，唔落地）
- 分支 `v20a209`（基底 main a426947），實裝 commit `9653d6a`（6 張 webp＋
  新測試＋qa209 證據）；本 NOTES 另作 commit。工作副本 `linji-work209`。
- 落地次序：v205 → v206 → v207 → v208 → v209；等 parent 安排，唔好自行落地。
- 快取：同路徑覆蓋，fullbody `?v=20a106` 不變；GitHub Pages max-age=600，
  傳播 ≤10 分鐘（同 v205 一樣）。

## §7 殘留
- v205 review B2／C1／C2／C3 用戶未拍板；如果之後拍板修，有機會併入 v209，
  等 parent 通知。
- `rom_lan_*` 場景圖缺失（pre-existing，v205 已記錄），令 R_lan 舞台底係素色，
  光邊喺素色底上面反而更顯眼；補圖係另一票。

## §8 落地紀錄（2026-11-14，遊戲 commit `54ee62b`）
- Rebase：分支 base `a426947`（v205）→ main `eed04dc`（v212），**0 衝突**，
  兩粒 commit 乾淨落上（新 HEAD `bda8ca6`：實作 `45e0a9c`＋NOTES）。
  本票零 index.html 改動，rebase 純粹係行號／基底追趕。
- 重驗（rebase 後，工作副本）：
  - 新測試 `tests/test_lan209_outline_static.py`：**49 個斷言全綠，0 FAIL**
    （§4 寫 44 項係計數口徑：6 檔 × 7 項＋lin_hiu 對照 2＝44，另加反證 2＋
    基線 3＝49；同一檔，唔係回歸）。band share：base 99.99%、其餘 5 張
    100.00%；v107 ring 1.0000；零遠處米白。
  - 反證（pristine main `eed04dc`，同一測試）：**13 項 FAIL**
    （6 張 sha＋6 張 band＋反證現版項），band 0.12–0.25%，乾淨 FAIL。
  - 全套 A/B：pristine **296／14** vs 工作版 **297／13**。FAIL 清單只差
    lan209 一項（pristine 預期 FAIL、工作版 PASS）；其餘 13 項穩定
    pre-existing FAIL 逐項相同（flash51／giglib36／pacing35／poster59／
    rumor49／slot50／soft_tip_111_restore／start53／weave43／weave44／
    weave49／wf5_87／wrap38），**零回歸**。總數同 v212 時代唔同係因為
    v212 加 2 檔＋本票加 1 檔（293→296）。
  - 實駕重跑（`qa209/drive209.py`，本地鏡像＋Playwright）：4 節全開
    （meet 7／push1 6／crisis 6／ending 8 行），同原跑逐行一致；6 張 webp
    HTTP 全部 200；**0 pageerror**；破圖 0；旁白句 `brightness(0.6)`、
    講者句 `brightness(1)`，光邊跟住變暗（截圖親自讀過確認）。原跑
    drive log 留底 `qa209/drive209_orig_a426947.json`。
  - 404：新跑 48 條 vs 原跑 36 條——探針核實全部只係已知缺圖
    `rom_lan_*` 場景圖（每節 3 副檔名 × 多次重載；`bg_loc_home_airport`
    而家 index.html 0 引用，已唔出 404）；**冇新 404**，唔係回歸。
  - 修正 §5 一處講法：原跑同重跑上台見到嘅表情都係 base／sad／shy／
    smile 四種（serious 嗰節本身冇對白；think 喺今次行嘅路徑冇上台）。
    serious／think 靠 HTTP 200＋band test 核實；光邊焗入圖檔，靜態證明
    覆蓋晒 6 張。
- 落地：squash merge 去 main → 遊戲 commit `54ee62b`（6 張 webp＋新測試＋
  qa209 證據，45 檔）；push 第一次俾 egress proxy reset 斷線（Broken pipe，
  已知問題），重試成功；`git ls-remote` 核實 main＝`54ee62b`。
- 線上核實：index.html 唔郁（`cbad0769…`、5,487,683 bytes，同 v212 一致，
  預期之內）；6 張 webp push 後約 4 分鐘傳播完成，live sha 逐張對 repo
  一致（base `bd7923f2…`、sad `adcffb30…`、serious `e98414ed…`、
  shy `ed0a5e91…`、smile `7536aa7d…`、think `1e035184…`）。
- 落地次序下一位：v213 → v214（v214 實作完成 HEAD `5fa653e`；推出日提及
  另開細票 v215，落地次序 v209 → v213 → v214 → v215）。
