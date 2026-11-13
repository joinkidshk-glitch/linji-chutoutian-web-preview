# NOTES_V20A184 — 修 v182 設計 review 新 C1＋C2

**落地**：遊戲 commit `454ed8e`，線上核實 5,331,174 bytes sha `dbefbaa2…`，同 repo `HEAD:index.html` 完全一致（push main 一次成功；第一次 curl 仲係 v183 舊版，Pages 部署滯後，等約 100 秒後重 curl 攞到新版）。`git fsck` 乾淨（淨 dangling blob／tree，無錯誤）。

- **分支**：`v20a184`，基底 main `01ddcaa`（v183 NOTES 已落地：遊戲 `7497c9e`＋NOTES `01ddcaa`，live 5,329,880 bytes sha `9890d43e…`）。**Rebase 已做完**（`b5cf756`，由 `6ed68f8` rebase 上 `01ddcaa`，diff 淨 v184 改動，見 §5）；接手嗰陣 main 仍係 `01ddcaa`，唔使再 rebase。
- **範圍**：v182 review（`~/workspace/linji-design-review-v182/REVIEW.md`）兩項新 C 級，全部修晒。工人唔落地（唔 squash merge、唔 push main、唔開設計 review）。
- **紅線遵守**：SAVE key（`starVolunteer_map_v19w`）、softRev（`s107`）、`?v=`（`v20a10`）唔郁；`content/` pack JSON 零改動；獎項集合／文案一字唔郁；得主標記（`awd63-card win` 金框＋🏆 角標）唔郁。

## §1 改動

### C1 — 三張提名卡下半同色（`index.html`，`awards62PlayCeremony` 內）
- **現況**：三張 CSS 卡漸變都係 `linear-gradient(160deg, <tint>, #241736)`，第二 stop 全場同一隻 `#241736`，卡面下半約 40% 面積三張一模一樣。
- **修法**：加平行 palette `AWDS63_DEEPS184`（按卡位 index 對位 tint，第一 stop 唔郁）：
  - 紫 `#3a2a4a` → `#241736`（keep）
  - 綠 `#274a3a` → `#122a1e`（深綠）
  - 酒紅 `#4a2a2e` → `#2c1518`（深紅）
  - 其餘三色（第 4–6 張卡用）：`#2a3a4a` → `#141f2b`、`#4a3a20` → `#2a1e0c`、`#33355e` → `#1b1c38`
  - 六隻 deep 全部各不相同、全部比對位 tint 深（靜態測試量度 luminance 斷言）。
- 漸變改用 `linear-gradient(160deg, tint182, deep184)`；色板數量、第一 stop、卡面文字（大字首字 30px＋全名＋「電視」細行）唔郁。CSS class `.awd63-csscard` 預設漸變（紫卡對）唔郁。

### C2 — 同一場 pack 獎項次序唔穩定（`index.html`，呈現層）
- **根源（查清楚，唔係估）**：`buildAwardResultPack` 每次 build 都 Fisher-Yates shuffle 啲 categories 再 slice（`shuffled` 段，`Math.random()`）。同一場 1991 星河台慶、同一播種，兩次 build 次序可以掉轉——review 嘅 932／700 `found.pack.cats` 正係咁。本票實駕 run 5 重現到：raw pack 次序 932 係 `[cat_popular_face, cat_newcomer_tv]`、700 係 `[cat_newcomer_tv, cat_popular_face]`，兩邊掉轉。
- **修法**：呈現層固定排序，唔郁評估次序。新增 helper `awardsCatsSorted184(pack)`：`pack.categories.slice()`（copy，唔郁原 pack）再按獎項 id `localeCompare` 排。請柬「今晚獎項」行（`renderAwardInviteHtml`）＋結果卡每類別卡片（`renderAwardResultHtml`）同用呢個 helper。
  - 排序結果：`cat_newcomer_tv`（最佳電視新人（臨記組））先、`cat_popular_face`（最受歡迎螢幕面孔）後。
  - `buildAwardResultPack` 嘅 shuffle 段原封唔郁（評估／抽選邏輯唔係本票範圍）；`commitAwardToLog`／`awards63FocusCat` 等數據層唔郁。

## §2 驗證數字

### 新測試 `tests/test_awards184_static.py` — 22 項
- C1（11 項）：DEEPS palette 在位 6 色對位 tints；tint palette 原 6 色唔郁；實駕三張第二 stop 各不相同（紫 `#241736`／綠深綠／酒紅深紅）；紫卡 keep `#241736`；綠／酒紅唔再係 `#241736`；六隻 deep 各不相同；每隻 deep 比對位 tint 深；漸變用 `deep184` 變量；deep 按卡位 index 揀；卡面文字唔郁；得主標記 CSS 唔郁。
- C2（8 項）：helper 在位、按 id 排序、slice copy 唔郁原 pack；請柬行用固定排序；結果卡同用固定排序；獎項集合／文案唔郁；build 層 shuffle 原封；唔直改 content pack。
- 硬規則（3 項）：SAVE key／softRev／`?v=` 不變。
- **結果：工作版 22/22 ALL PASS。反證：對 pristine main（`6ed68f8`）8 項乾淨 FAIL（C1 3 項＋C2 5 項，全部斷言 fail，唔 crash）。**

### 全套 A/B（`qa131/run_suite.sh`）
- **Pristine A**（`6ed68f8`，`~/workspace/pristine184tmp` 已刪）：**244 PASS／12 FAIL**——12 項正好係穩定基線（flash51／giglib36／pacing35／poster59／rumor49／slot50／soft_tip_111_restore／start53／weave43／weave44／weave49／wrap38）。
- **工作版 A**：241/16——多出 4 項（rom176／tang171／tang173／travel114），逐個直接跑證實唔係噪音，係 v184 插行（淨 ＋16 行）令釘行測試漂移（見 §3 resync）。
- **工作版 B**（resync 後）：**245 PASS／12 FAIL**——FAIL 清單同 pristine 基線 12 項逐項相同，零回歸（＋1 PASS 係新測試）。
- 附註：`/tmp` 係 512M tmpfs，成個 repo 抽唔入（`git worktree add` 亦因同原因失敗，唔關 repo 事）；pristine A/B 副本放 `~/workspace/pristine184tmp`（734M），驗完已刪。

### Resync（`qa184/resync184.py`）
- v184 index.html 淨 ＋16 行：C2 helper ＋9（L45748）／請柬註解 ＋1／結果卡註解 ＋1／C1 DEEPS ＋4（L46479）／漸變 ＋1 淨。全部插入點都喺 openLoc DEF（54510）之前，之後者一律 ＋16。
- 方法跟 resync182：difflib 對 `6ed68f8` index 逐行對位，5 個非 equal hunk 全部落喺 [45747, 46490]，新總行數 60026；釘行逐粒核實舊行內容＝新行內容（純漂移）。
- Resync 四檔：`test_rom176_static.py`（53050→53066／53415→53431／54447→54463／54541→54557）、`test_tang171_static.py`（總行數 60010→60026、DEF 54510→54526）、`test_tang173_static.py`（同上；CSS L4847 喺插入點之前唔郁）、`test_travel114_static.py`（COUNT 13／FREE 33 逐粒映射、DEF 54510→54526、WRAPPER 44337 唔郁）。Resync 後四檔逐個直接跑全部 PASS（rom176 ALL PASS／tang171 22/22／tang173 21/21／travel114 RESULT PASS）。

### 實駕（`qa184/drive184.py`，本地鏡像＋`python3 -m http.server`，port 18482）
- 場次：1991 星河台慶 `award_singho_tv` nominated，高俊傑《潮汐家庭》做 fellow，得主葉敏芝；430×932／430×700。
- **run 5（2-cat 關鍵跑，`qa184/drive184_run5.json`）2/2 PASS，0 pageerror**，`c2_cross_same=True`：
  - **C1**：DOM computed 漸變第二 stop 兩 viewport 完全一樣——葉 `#3a2a4a → #241736`、鍾 `#274a3a → #122a1e`、高 `#4a2a2e → #2c1518`（第一 stop 預期值亦吻合）；像素層 ko_cards 截圖每張卡上／下 20% 帶平均色三張互異（下帶 [106,92,98]／[96,106,84]／[111,90,78]，兩兩距離 ≥12）；目視 `ko_cards_430x932.png` 三張卡上下半都分得開（紫／綠／酒紅）；得主標記唔郁（葉敏芝卡 `awd63-card win`）。
  - **C2**：raw pack 次序兩邊掉轉（見 §1），但請柬行兩邊一字相同——「今晚獎項：最佳電視新人（臨記組）、最受歡迎螢幕面孔」；結果卡 kickers 次序兩邊亦相同（新人先、面孔後）。跨 viewport `c2_cross_same=True`。
  - 其餘沿用 v182 覆驗全部 PASS：唱名高俊傑 t≈3420ms（932）／3489ms（700）；剪影 4056 粒（兩 viewport 同 v182 數字一致）、紅褸 0 粒；典禮全長約 10.9 秒；請柬 modal 401px（932）／405px（700）、黑空 28px；獎項頁提名行 320＝320、日期行 144＝144。
- **其餘跑**：run 2／3／4 亦 2/2 PASS（全部 1-cat pack——pickN 隨機，1 類嗰陣排序檢查係 vacuous；run 5 兩邊都係 2-cat 先係 C2 真憑據）。run 1 ko_700 有一項 transient FAIL（邊項未及留底，json 被下一跑覆蓋），其後連續 4 跑 8 個 case 全部 PASS，判為時序波動，唔係回歸。
- 實駕產物：`qa184/drive184.py`（＋`card_px.py` 像素輔助、`ko_red.py`／`ko_sil.py` 由 qa182 複製）、`qa184/drive184.json`（＝run 5）、`qa184/drive184_run5.json`、`qa184/run5.log`、`qa184/shots/`（10 張）。

## §3 Diff 摘要
- `index.html`：＋20／−4（淨 ＋16 行）。
- `tests/test_awards184_static.py`：新檔，22 項。
- `qa184/`：新目錄（`drive184.py`、`card_px.py`、`ko_red.py`、`ko_sil.py`、`resync184.py`、suite A/B、`drive184.json`、`drive184_run5.json`、`run5.log`、`shots/`）。
- `tests/test_rom176_static.py`／`test_tang171_static.py`／`test_tang173_static.py`／`test_travel114_static.py`：淨 resync 釘行數字＋每檔一行 resync 註解，遊戲邏輯零改動。

## §4 殘留／交接
- 無已知殘留。C2 嘅 pack 類別數目本身（1 類 vs 2 類，`pickN` 隨機）唔係本票範圍——review O3 已列明係播種／抽選產物，請柬行每次都忠實反映當次 pack；本票只保證次序固定。
- 實駕 run 1 ko_700 嗰項 transient FAIL 未捉到邊項（見 §2）；連續 4 跑全 PASS，落地嗰陣如再見到先跟。
- v183 已落地（main `01ddcaa`），本票已 rebase 上去（見 §5）；v181 進行緊，落地前要再核 main 有冇郁。
- run 1 ko_700 嗰項 transient FAIL（見 §2，未留底邊項）：按 §5 機制，極可能係同一 stale-rect race（首 poll caption 令 rect 偏低），但 run 1 嘅 json 已被覆蓋，唔能斷言；修好後連跑 8 case 全 PASS，呢類 flake 已消除。

## §5 接手重驗（rebase 上 `01ddcaa`＋run6 調查，2026-11-13）

### Rebase 核實
- Rebase 後 diff（`01ddcaa..b5cf756`）：`index.html` ＋20／−4（淨 ＋16 行：C2 helper ＋9／請柬 ＋1／結果卡 ＋1／C1 DEEPS ＋4／漸變 ＋1 淨）、新測試 `tests/test_awards184_static.py`（22 項）、resync 四檔（rom176／tang171／tang173／travel114，淨釘行數字＋一行 resync 註解）。逐檔對過：無 v183 帶入嘅雜質，resync 全部係純行號漂移（插入點 L45748／L46479，＜45748 者唔郁、其後者 ＋16；travel114 COUNT 12／FREE 34 不變、DEF 54623→54639、WRAPPER 44340 唔郁）。
- 新測試重驗：工作版 **22/22 ALL PASS**；反證對新基底 pristine `01ddcaa` **8 項乾淨 FAIL**（C1 3 項＋C2 5 項，全部斷言 fail，唔 crash；其餘 14 項 PASS）。相關測試逐個覆驗全部 PASS（awards62／63／64、tang171 22/22、tang173 21/21、travel114 RESULT PASS、rom176 ALL PASS）。
- 主 script `node --check`：兩個 inline script 段都 OK（主段 4,360,562 bytes）。

### run6 `cards_px_bottom_distinct` FAIL — 根因已查明，係 probe 取樣問題，唔係遊戲渲染問題
- **現象**：run4／5／7／8 全 PASS，run6 0/2 FAIL——兩個 viewport 唯一唔合格嘅 check 係 `cards_px_bottom_distinct: false`，其餘 32 項全部 true。run6 底行樣本 [160,146,128]／[164,159,131]／[162,145,121]（偏光、近乎一樣）；run4／5／7／8 底行 [106,92,98]／[96,106,84]／[111,90,78]（五次逐粒相同）。
- **重現**：接手後用舊 probe 再跑一次 run9——ko_932 又 FAIL，數值同 run6 逐粒相同（[160,146,128] 等），ko_700 PASS。舊 probe 失效率：run4–9 六跑十二 case，三 case FAIL（run6 兩 viewport＋run9 932），約 25%／case。
- **根因（已證實，唔係估）**：`watch_ceremony` 喺第一個 poll（t≈3–12ms，卡未 `.show`、仲 `visibility:hidden`）就攞 `faceRect` 存入 `cardsKo`，但 `ko_cards` 截圖遲至唱名「高俊傑」嗰句（t≈3.4s）先影——rect 同截圖相差成個 names beat。兩重 stale：
  1. 未 `.show` 嗰陣 `.awd63-card` 帶 `translateY(8px)`（L795），rect 偏低 8px；
  2. 舞台係 flex 置中，首 poll 撞正邊句 caption 會令舞台上下移——run6／run9 首 poll 已係 1 行嘅「提名者魚貫入場」caption（標題 beat 錯過咗），run7／8 首 poll 係 2 行標題 caption，rect 再偏低 9.25px。
  合共偏低 17.25px：底 20% 帶（22px）得返約 5px 係真正卡面，其餘約 17px 係卡下面嘅淺紙標題行（`.t`，紙底 `#fbf2da`）。三張卡下面嘅紙係同一隻色，底色收斂埋一齊（兩兩距離最細 7.3 ＜ 12）就 FAIL；頂帶仲喺卡入面（只係移低咗，掂多咗大字首字淺色字），所以頂帶仲 PASS。
  - **像素層證據**：run8 `ko_cards_430x932.png` 逐行掃描——csscard 漸變實測 y≈510–621（底色 `#241736` 約 (36,23,54)），y≈622 起係淺紙 (241,229,197)；舊 rect y=517.70（應為 509.70），正正差 8px translate。
  - **淡入唔係兇手**：卡後面係深色舞台 `#14101f`，半透明只會變暗；run6 係變光（向紙色），同淡入方向相反。DOM 層 computed 漸變 stops 喺 run6 全部正確（`cards_second_stops_expected` true），v184 改動本身無問題。
- **修法（只修 probe，唔郁遊戲 code，唔放寬 ≥12 門檻）**：`qa184/drive184.py` 加 `settle_cards()`——唱名「高俊傑」嗰句觸發 `ko_cards` 截圖之前，先等三張卡 `.show`＋computed opacity＝1（`cards_settled()`），再即刻重測 `stage_state`（新 rect 對準截圖嗰刻卡面）先影；`cardsKo` 亦唔再喺第一個 poll（卡未可見嗰陣）記錄。`stage_state` 每張卡加 `op` 欄。
- **重跑證明**：修好後連跑 run10–13，**8/8 case 全部 PASS**（每跑 2/2）。`settled=True`、cls 帶 `show`、op=1、rect_y 509.70（932）／393.70（700）——正正係像素掃描量到嘅真卡頂；新 cards_px 八次逐粒相同——底 [43,29,57]／[25,49,35]／[52,27,28]（真深色 stop＋淺字，兩兩距離最細約 30，遠高於門檻 12）、頂 [70,54,75]／[52,79,60]／[82,53,51]。舊「PASS」數值 [106,92,98] 等本身都含 8px 紙污染，新數值先係真卡面。
- **`c2_cross_same` 附註**：run11／run13 `cross_same=False` 但兩 case 本身全 PASS——兩個 viewport 各自抽到唔同 pack（例 run9：932 得 `cat_newcomer_tv`、700 得 `cat_popular_face`），請柬行唔同係 pack 唔同，唔係排序錯。每 case 內 `invite_awards_sorted_by_id` 全部 True（呈現行＝該 pack 按 id 排序），嗰項先係 C2 真憑據；cross 只係兩邊啱啱抽到同一 pack 先有意義（run5／run10／run12）。probe 原有設計局限，留返，唔喺本票改。

### 全套 A/B（`qa131/run_suite.sh`，rebase 後重跑）
- **Pristine A**（main `01ddcaa`，`git worktree add ~/workspace/pristine184b`，驗完已刪，`qa184/suite_pristine184.txt`）：**246 PASS／12 FAIL**。
- **工作版**（`qa184/suite_work184_new.txt`，新跑）：**247 PASS／12 FAIL**——FAIL 清單同 pristine 基線逐項相同（flash51／giglib36／pacing35／poster59／rumor49／slot50／soft_tip_111_restore／start53／weave43／weave44／weave49／wrap38，`diff` 零差異），零回歸（＋1 PASS 係新測試 `test_awards184_static.py`）。
- 舊數字（rebase 前，對 `6ed68f8`）留喺 §2 作歷史紀錄，唔再用。

### 實駕產物更新
- `qa184/drive184.py`（修 probe：`settle_cards`／`cards_settled`／`stage_state` 加 `op`）、`drive184_run8.json`（run8 存檔）、`run9.log`（舊 probe 重現 FAIL，RESULTS_JSON 在內；無獨立 run9 json——當時 drive184.json 隨後被 run10 覆蓋）、`drive184_run10.json`–`drive184_run13.json`（修好後 4 連跑全 PASS）、`run9.log`–`run13.log`、`drive184.json`（＝run13）、`shots/`（run13 嗰套）。

