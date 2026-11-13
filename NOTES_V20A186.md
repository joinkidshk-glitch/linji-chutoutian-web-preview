# NOTES — v20a186：修 v184 設計 review 新 C1（結果卡「同屆提名」行重複兩次）

- **任務**：用戶 2026-11-13 18:24 拍板「修：同屆提名行只出一次」（v184 review 新 C1，C 級）。
- **基底**：main `b1b6092`（v181 NOTES；遊戲 `15d97fa`）；分支 `v20a186`；開工 `git fetch origin` 核實 main 未郁，無需 rebase。
  index.html 基底 sha `1cbaed3d…` 同常駐 clone main 核對一致。
- **問題**：頒獎禮一次有兩個獎項類別嗰陣，結果卡（`renderAwardResultHtml`）每張類別卡下面各有一行
  完全一樣嘅「同屆提名（🏆為得主）：🏆葉敏芝《渡輪燈火》、鍾楚凝《星光夜》、高俊傑《潮汐家庭》」。
  唔係 v184 引入（v182 已有嘅逐類別出卡結構），係 2 類實駕先清楚見到。證據：review 報告
  `~/workspace/linji-design-review-v184/REVIEW.md` 新 C1 一節、`shots/ko_result_430x932b.png`、
  `drive184_review.json` ko_932b 嘅 `result_card.body`（同屆提名出現兩次）。

## §1 修法（只改呈現層，唔改數據／判定）

`renderAwardResultHtml`（index.html，淨 ＋4 行：＋6／−2）：
- 拎走逐類別卡內嘅 `felBit63`（每類 `awards63FellowsHtml(c)`）。
- 排序後取第一個有 `fellows63` 嘅類別（`felCat186`，`cats.find(...)`；同場各類共用同一屆名單），
  經同一 helper `awards63FellowsHtml(felCat186)` 出一次，叫 `felBit186`，放喺 `${catsHtml}` 之後、
  報紙卡（`psr-press`）之前——卡底獨立一行（`.psr-cards` flex column 嘅直接子元素）。
- 冇任何類別有 fellows 嗰陣出空字串，唔出空行；第一類冇、第二類有嗰陣照出第二類嗰份。
- 唔郁：`awards63FellowsHtml` 本身（得主標記＋名單格式）、`buildAwardResultPack` fellows 衍生、
  請柬 `awards63InviteBitHtml`、獎項頁 `fellowsTxt`、v184 C2 固定 id 排序、kicker／rep／weak／comfort 行、
  贏線 `0.875`、SAVE key／softRev／`?v=`。

## §2 新測試（logic 14 項＋static 17 項，全部 PASS）

- `tests/test_awards186_logic.js`（14/14）：兩類嗰陣「同屆提名」＝1 次、`psr-fellows63` 節點＝1 個、
  名單逐字不變（「葉敏芝《渡輪燈火》、鍾楚凝《星光夜》、高俊傑《潮汐家庭》」只出一次）、
  同屆提名行喺兩張類別卡之後（卡底獨立一行）、kicker 次序唔郁（id 序：新人先、面孔後）、
  得主標記仲喺名單入面、報紙卡＋餘韻卡＋雙軌行齊；單類維持 1 行；冇 fellows＝0 行唔出空行；
  首類無 fellows、次類有嗰陣照出一次。
- `tests/test_awards186_static.py`（17/17）：逐類別 `felBit63` 已拎走、`felBit186` 經同一 helper、
  helper 喺結果卡只呼叫一次、行喺 `${catsHtml}` 之後報紙卡之前、冇 fellows 唔出空行、請柬／獎項頁／
  build 層／helper 本身唔郁、硬規則（SAVE／s107／v20a10／贏線 0.875）。
- **反證**（pristine main `b1b6092` index，sha `1cbaed3d…`）：logic 4 項 FAIL（兩類計數／節點數／
  名單逐字／位置）、static 5 項 FAIL，全部乾淨 FAIL 無 crash。單類／冇 fellows 等守門項喺 pristine 照 PASS，
  證明反證只係掂到修法本身。
- 相關測試逐個直接覆驗：`test_awards63_logic.js`／`test_awards63_static.py`／`test_awards184_static.py`／
  `test_awards181_logic.js`／`test_awards181_static.py` 全部 PASS。

## §3 行號釘 resync（淨 ＋4 行引起，舊例做法）

index.html 淨 ＋4 行（插入點 L45783–45826），其後行號釘一律 ＋4；插入點之前
（kwan151／tang152 L4862、WRAPPER 44353、NPCS lan、GIFT_REACT）唔郁。
用 `/tmp/resync186.py` 單次掃描 dict 查表（每粒舊釘核實只出現一次先換，唔逐對 re.sub），
36 粒釘全數一次換妥：
- `test_gift185_static.py`：總行數 60151→60155。
- `test_tang171_static.py`／`test_tang173_static.py`：總行數 60151→60155、openLoc DEF 54647→54651。
- `test_rom176_static.py`：53077→53081、53445→53449、54584→54588、54678→54682。
- `test_travel114_static.py`：COUNT 58707→58711、58885→58889、59028→59032、59049→59053；
  FREE 52900 之後 22 處各 ＋4；DEF 54647→54651、WRAPPER 44353 唔郁；COUNT 12／FREE 34 不變。
  五檔 resync 後逐檔直接跑全部 PASS。resync 期間一度將淨行數誤計為 ＋6，實為 ＋4
  （＋6／−2，總行數 60151→60155 實量作準）；另 logic 測試初版計類別卡嗰陣誤將餘韻卡
  （同用 `psr-card psr-metrics`）計入，已改為數類別 label。

## §4 全套 A/B

套件入口 `qa131/run_suite.sh`：
- 常駐 clone main（`b1b6092`，真基線）：**251 PASS／12 FAIL**（12 項穩定 FAIL：
  flash51／giglib36／pacing35／poster59／rumor49／slot50／soft_tip_111_restore／start53／
  weave43／weave44／weave49／wrap38）。
- 工作副本（＋2 份新測試）：**253 PASS／12 FAIL**——FAIL 清單同基線逐項相同，零回歸。
  （中途一次工作副本跑出 248／17，額外 5 項全部係上述行號釘漂移，resync 後回復 253／12；
  另一次經 `/tmp` symlink 根目錄跑嘅 pristine 對照出 247／18，係 symlink 根目錄欠 NOTES／content
  造成嘅環境噪音，唔係產品問題——真基線以常駐 clone 直接跑嘅 251／12 為準。）

## §5 實駕（`qa186/drive186.py`，Playwright＋本地 http.server，LIVE 模式）

- **4/4 PASS，15 項檢查 ×4，0 pageerror**。場次：1991 星河台慶 `award_singho_tv`、nominated；
  fellows 葉敏芝／鍾楚凝／高俊傑（得主葉敏芝）；唱名高俊傑 t≈3330–3503ms；典禮全長約 10.9–11.0 秒。
- 兩類＋單類齊晒（run1：ko_932b 兩類；run2：ko_700a 兩類，其餘三跑單類；raw cat 次序掉轉嗰跑
  請柬／kicker 照按 id 序出「新人先、面孔後」）：
  - ko_932a（932，1 類）：同屆提名 1 次、名單逐字 1 次、`.psr-fellows63` 1 個、felIdx 1＝n_cats、press 緊接其後。
  - ko_932b（932，2 類）：同屆提名 **1 次**（舊版 2 次）、名單逐字 1 次、felIdx 2＝n_cats。
  - ko_700a（700，2 類）：同上，1 次。
  - ko_700b（700，1 類）：同屆提名 1 次，維持原樣。
- DOM 順序（兩類例）：`[cat-metrics, cat-metrics, psr-fellows63, psr-press, psr-news, psr-metrics（餘韻）]`——
  同屆提名行喺最後一張類別卡之後、報紙卡之前，唔喺任何類別卡入面。
- 請柬行唔郁（兩類：「今晚獎項：最佳電視新人（臨記組）、最受歡迎螢幕面孔」）；結果卡 kicker 唔郁。
- 實駕中途發現 probe 寫法問題（唔係產品問題）：第一版位置斷言用 `lastMetricIdx`，撈埋餘韻卡
  （同用 `psr-metrics` class）令四跑 FAIL——改為 `felIdx == n_cats` 後 4/4 PASS；產品喺兩版 probe
  之下同屆提名計數全部都係 1 次。
- 產物：`qa186/drive186.py`、`qa186/drive186.json`、`qa186/shots/`（每跑請柬＋結果卡截圖）。

## §6 Diff 摘要

- `index.html`：＋6／−2，淨 ＋4 行（只改 `renderAwardResultHtml`）。
- `tests/test_awards186_logic.js`、`tests/test_awards186_static.py`：新增。
- `tests/test_gift185_static.py`／`test_rom176_static.py`／`test_tang171_static.py`／
  `test_tang173_static.py`／`test_travel114_static.py`：行號釘 resync（＋4 漂移）＋註解。
- `qa186/`：實駕腳本＋JSON＋截圖。
- 未改：SAVE key、softRev、`?v=`、content pack JSON、判定／fellows 池／贏線。

## §7 殘留／跟進

- 無。C1 已修好，唔使開設計 review（按任務指示，落地由統籌處理）。

## §8 落地紀錄（統籌）

- 落地：2026-11-13 約 18:47 HKT，main `b1b6092` → 遊戲 `fc76b9e`（squash merge，無需 rebase，main 落地期間未郁）。
- 統籌親自核實：diff index.html 淨 ＋4 行（只改 `renderAwardResultHtml`）；新測試 logic 14/14＋static 17/17 我親自重跑 PASS；反證對 pristine `b1b6092` logic 4 FAIL＋static 5 FAIL 乾淨；相關測試 awards63 logic/static、awards184 static、awards181 logic/static 全部 PASS；resync 五檔純行號漂移 ＋4；實駕結果卡截圖我親自睇過，同屆提名行只出一次。
- 線上：我親自 curl 核實 5,309,088 bytes、sha256 `b9976b56af55ac24a8ae474f9f81dc027cdf62a7095b820f979d48d13c91e50e`，同 repo HEAD:index.html 完全一致（push 後等約 90 秒部署先攞到新版）。
- `git fsck` 乾淨。設計 review 已派（`~/workspace/linji-design-review-v186/`）。
