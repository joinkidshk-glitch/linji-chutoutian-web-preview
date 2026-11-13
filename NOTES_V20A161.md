# NOTES_V20A161 — 首頁簡介句收窄＋置左，避開阿偉塊面

分支 `v20a161`，基於 `e08a070`（v148 main）。**唔落地，唔開 PR**——實作＋測試＋實駕完成，等另行安排落地。

## 1. 問題（探針實證，唔係估）

- 簡介句 `.start-intro`（L5520，文字不變）：置中、max-width:332px，box x29–361。
- 企位 `#start-standee`：`right:-10px; bottom:170px; height:min(52%,430px)`（v53），390×844 實測 x120.5–400、y244–674。
- 塊面框（實證方法：抽出內嵌 `UI40_STAND.awi` 原圖 325×500，膚色像素檢測＋逐行闊度分析）：
面（膚）原圖 x64–184、y67–177（下巴約 y177，y180 起闊度由 76–114 跌到 39＝頸）；頭（髮＋面）原圖 x36–204、y2–177。
- Pristine 三種 viewport 實測（`qa161/probe_pristine.json`，`?softPreview=1`，0 pageerror）：

| viewport | glyphs vs 面 | glyphs vs 頭（髮） | intro box vs 面 |
|---|---|---|---|
| 390×844 | 0（面頂 y301.6，字底 y262.4） | **144.4×16.7＝2411.5px²**（第二行字壓住頭頂髮） | 0（box 底 274.7，面頂 301.6，隙 26.9px） |
| 390×932 | 0 | 0（隙 112.1px） | 0 |
| 390×700 | **87.4×41.4＝3618.4px²**（兩行字直壓塊面，眼→口鼻區） | 122.3×41.4＝5063.2px² | 87.4×55.3＝4833.2px² |

- 附註：任務簡述寫面約「y284–330、x280–360」，同實測（844：面 x175.5–278.7、y301.6–396.2）唔夾——以今次探針＋原圖分析為準，簡述數字可能係舊版／另一量度。

## 2. 改動（只改 CSS，14 行淨加）

`index.html` v53 區塊之後新增 `v20a161` 區塊（L4780 前後）：

```css
#app #v-start.start52.start-intro{
margin:2px 0 0; max-width:140px; text-align:left;
}
```

- 收窄 332→140px、置左（margin-left:0，靠 `.start-head` 20px padding 落位 x=20；box 右緣 160，字最遠只到 x=141）。
- **企位唔郁**：`#start-standee` 零改動（bottom:170px／height:min(52%,430px)；移低會撞到底部紙條掣）。唔使企位微調方案——收窄置左已清乾淨。
- 文字本身唔改；柔霧底、字體、行高、標題、掣、soft-tip 全部沿用。唔郁任何劇情內容、旗標、節點、通告、地圖、content pack JSON。SAVE key（`starVolunteer_map_v19w`）、softRev（`s107`）、`?v=`（`v20a10`）不變。
- 副作用：簡介句由 2 行變 5 行（box 高 64.7→131.6px），「埋／位」跨行斷開；底部選單係 `margin-top:auto` 釘底，唔受影響（見 §3）。

## 3. 實駕量度（工作版，`qa161/probe_work.json`＋三張截圖 `qa161/shots161/start_390x{844,932,700}_work.png`）

企位三種 viewport 同 pristine 逐 pixel 相同（844：x120.5、y244、279.5×430；932：y332；700：x163.4、y166、236.6×364）。

| viewport | glyphs vs 面 | glyphs vs 頭 | 字右緣 → 面左緣／髮左緣 | intro box | 選單／掣／soft-tip |
|---|---|---|---|---|---|
| 390×844 | **0** | **0** | 清 34.5px／10.5px | x20–160，y210–341.7 | 同 pristine 一樣（menu y640.6–760.6、btn-new y656.4–722.7、soft-tip y766.6–816） |
| 390×932 | **0** | **0** | 清 34.5px／10.5px | x20–160，y212.9–344.5 | 同 pristine 一樣（menu y728.6–848.6、btn-new y744.4–810.7、soft-tip y854.6–904） |
| 390×700 | **0** | **0** | 清 69.0px／48.6px | x20–160，y205.4–337.1 | 同 pristine 一樣（menu y496.6–616.6、btn-new y512.4–578.7、soft-tip y622.6–672） |

- 844 box 右緣 160 vs 髮左緣 151.5：box 水平重疊 8.5px，但柔霧係 radial-gradient、邊緣淡出到透明，字清 10.5px；截圖目視確認霧邊唔掂髮。
- 三張截圖目視：塊面＋頭髮完全露出，標題／副題／掣／底部提示零新碰撞。
- 6 次載入（pristine＋工作版 × 3 viewport）全部 **0 pageerror**。

## 4. 測試

- 新測試 `tests/test_start161_static.py`（12 項）：基線守衛（SAVE／softRev／?v=、簡介句文字、v52＋v53 企位／簡介句基線）＋v161 斷言（區塊在場、max-width:140px、text-align:left、margin:2px 0 0、區塊內只得一條 intro 規則、註解有量度數字）。
- 反證：喺 pristine main（`e08a070`，`/tmp/index_pristine161.html`）上行 → **7 項 FAIL**（exit 1）；工作版 → **12/12 PASS**。
- 全套 A/B：見 §5。

## 5. 全套 A/B

- Pristine（`~/workspace/pristine160`，e08a070，乾淨）：**211 PASS／12 FAIL**（`qa161/suite_pristine161.txt`）。注意：簡述話基線係 210，實測係 211——差 1 個係 `test_taxi148_static.py`：v148 基線檔（`qa148/suite_baseline148.txt`）係喺 v146 樹上面跑，嗰陣未有呢個測試檔；e08a070 樹有 223 個測試檔，211＋12＝223。12 項 FAIL 同 v148 基線檔逐項相同。
- 工作版（`qa161/suite_work161.txt`）：全套跑咗兩次，總數波動（第一次 177／47、第二次 197／27）——同 AGENTS.md v151 教訓一致（同一 repo 連續跑出唔同總數，失敗項每次唔同、全部係 .py，逐個直接跑全部 PASS）。所以唔信總數，信 FAIL 清單＋逐個覆驗：
  - 12 項穩定 FAIL 兩次都喺度，同 pristine 逐項相同，零新增、零消失。
  - 第二次多出嚟嘅 15 項 FAIL（aud91／aud91fix122／aud91fix124／awards62／awards63／awards64_chibi／awards64／book141／book143／book145／book70／br89／bust109／calib60／dlg107，全部 .py）逐個直接重跑 → **15/15 PASS**。
  - 第一次多出嚟嘅 35 項逐個重跑 → 33 PASS，剩低 2 項（text125／travel114）係真漂移，見 §5.1，已 resync 修復。
  - 新測試 `test_start161_static.py` 兩次全套都 PASS。
- 有效結論：**212 PASS／12 FAIL，零回歸**（211＋新測試 1；12 項穩定 FAIL 不變）。

### 5.1 行號漂移 resync（真問題，已修復，唔係波動）

- 本票 index.html 淨插入 14 行（舊行 4771 之後），令兩個寫死行號嘅測試失效：
  - `test_travel114_static.py`：COUNT／FREE／DEF／WRAPPER 全部釘行 ≥4772，整體＋14。
  - `test_text125_static.py`：currentLine 27800／advance 27913／familySafe 33516，整體＋14。
- 核實工具 `qa161/resync161.py`（跟 qa147 做法）：刪走 14 行插入段得出嘅 prev 同 `git HEAD:index.html` **逐字相同**；difflib 對位 44 個 openLoc( 呼叫點序列逐字一致；COUNT 13／FREE 27／DEF 53562→53576／WRAPPER 44171→44185／TEXT125 三行內容逐字相同，純漂移。RESULT PASS。
- 跟住將兩個測試嘅釘行＋14（連 0-based index `ls[27799]`→`ls[27813]` 等一併移；初版漏咗 index，補返後先 PASS），註解加 v161 resync trail。
- 覆驗：工作版 text125 PASS、travel114 PASS；resync 後嘅測試喺 pristine 上 FAIL（travel114 FAIL 27、text125 FAIL 1）——預期之內（行號鎖咗新版），證明 resync 唔係空心。
- 另：`test_start53_static.py` 係 12 項穩定 FAIL 之一，pristine 同工作版失敗輸出逐字相同，唔受本票影響。

## 6. 衝突監察（v157／v158／v159）

- 開工核實（2026-11-13 07:2x）：`~/workspace/linji-work157/`、`~/workspace/linji-work158/` HEAD 同係 `e08a070`、工作區乾淨、`git diff main -- index.html` 入面 `start-intro`／`start-standee`／`start52`／`start-bg` 改動數＝**0**。
- 本票只改 `index.html` 一處 v161 CSS 區塊（`.start-intro` 一條規則）＋新增 `tests/test_start161_static.py`＋`qa161/`，冇掂 v157／v158 範圍（主線／支線內容）。
- 收尾再核實（2026-11-13，commit 前）：v157／v158 HEAD 仍然係 `e08a070`，`git diff main -- index.html` 入面 `start-intro`／`start-standee`／`start52`／`start-bg` 改動數仍然係 **0**。本票冇掂佢哋範圍。
- **main 已郁（落地注意）**：本票開工嗰陣 main 係 `e08a070`；做到中途 v156（main `9c850f9`／GitHub `0c7ebbb`）同 v151（main `86e391d`／GitHub `faa40207…`）先後落地，而家常駐 clone main 係 `86e391d`。本分支基於 `e08a070`，落地要 rebase 上 `86e391d`；rebase 後 travel114／text125 嘅釘行要再 resync（v151 本身都帶 +15 行漂移，v156 亦有；resync 方法見 `qa161/resync161.py`）。
- 已知 v157／v158／v159 重疊（R_hiu_*、C5 alias）係嗰幾票嘅事，今票冇發現新重疊。

## 8. 落地 rebase（兩次，main 郁咗兩次）

- **第一次 rebase 上 `9346a8e`（v151 main）**：隧道改行持久化 `~/workspace/gh_tunnel.py`（18080 已死；work161 舊設定已換，`git fetch origin` 驗過）；`test_text125_static.py`／`test_travel114_static.py` 衝突純行號漂移，用 `qa161/resolve_rebase161.py` 解（HEAD 值 +14）；`test_kwan151_static.py` 13 個釘行同樣要 +14（brief 冇列，用 `qa161/resolve_kwan151_rebase.py` 修復＋逐行核實）；`qa161/resync161_rebase.py` RESULT PASS；新測試＋相關測試逐個直跑 PASS；全套工作版第二輪 187／40，27 項多出嚟嘅逐個直跑 28/28 PASS（波動假 FAIL）；pristine（9346a8e）重跑 **214／12**，FAIL 逐項係 12 項穩定 pre-existing。
- **第二次 rebase 上 `bf612bc`（v155 落地嗰陣 main 郁咗）**：`index.html` 自動合併乾淨（v161 區塊同 v155 改動唔同區）；三份測試衝突，全部純行號漂移——取 bf612bc 版再用 `qa161/resolve_rebase161_v155.py` 一律 +14（difflib 對位＋逐行錨點核實，RESULT PASS；舊 `resync161_rebase.py` 係第一次 rebase 嘅，硬計 9346a8e 釘行，已取代；換號嗰陣跳過 v155 歷史註解嗰行，`25744→25761`／`DEF 53601→53618` 原封不動）。`git rebase --continue` 嗰陣 EDITOR 未設會停低，要用 `GIT_EDITOR=true`（唔好 pipe 去 head，見 AGENTS.md v146 教訓）。隧道再跟 AGENTS.md 新教訓（v157）：`core.sshCommand` 加 `-o UserKnownHostsFile=/home/hatch/.ssh/known_hosts`，唔用 `StrictHostKeyChecking=no`；host key 核實係真 GitHub（`SHA256:+DiY3wvvV6TuJJhbpZisF/zLDA0zPMSvHdkr4UvCOqU`）。
- **第三次 rebase 上 `150e3ef`**（v155 NOTES 補錄 commit，淨改 `NOTES_V20A155.md`，零衝突乾淨過）。
- **最終全套 A/B（bf612bc／150e3ef 底，`qa161/suite_v155_pristine.txt`／`suite_v155_work.txt`）**：pristine **215 PASS／12 FAIL**，工作版 **216 PASS／12 FAIL**——FAIL 清單逐項相同，全部係 12 項穩定 pre-existing（flash51／giglib36／pacing35／poster59／rumor49／slot50／soft_tip_111_restore／start53／weave43／weave44／weave49／wrap38），工作版多出嚟嗰 1 個 PASS 就係新測試 `test_start161_static.py`。**零回歸，准落地。**
- 落地 commit／線上核實：見本檔落地後補錄（main 上另一個 NOTES commit）。

## 9. 檔案

- 改動：`index.html`（＋14 行，v161 區塊）
- 新測試：`tests/test_start161_static.py`
- 行號 resync：`tests/test_travel114_static.py`（釘行＋14）、`tests/test_text125_static.py`（釘行＋14，連 0-based index）、核實工具 `qa161/resync161.py`（RESULT PASS）
- 探針：`qa161/probe161.py`（量 rect＋截圖）、`qa161/face161.py`（舊版皮膚檢測，已被原圖分析取代，數字以 §1 原圖框為準）、`qa161/probe_pristine.json`、`qa161/probe_work.json`、`qa161/shots161/`（6 張全版＋6 張企位截圖）、`qa161/awi_raw.webp`（抽出嘅企位原圖，DEV 留檔）
- 全套紀錄：`qa161/suite_pristine161.txt`、`qa161/suite_work161.txt`
- 落地 rebase 紀錄：`qa161/resolve_rebase161.py`、`qa161/resolve_kwan151_rebase.py`、`qa161/resync161_rebase.py`（第一次 rebase 上 9346a8e）、`qa161/resolve_rebase161_v155.py`（第二次 rebase 上 bf612bc，RESULT PASS）、`qa161/suite_rebase_pristine2.txt`（pristine 9346a8e：214／12）、`qa161/suite_rebase_work.txt`（214／13，kwan151 未 resync）、`qa161/suite_rebase_work2.txt`（187／40，波動）、`qa161/suite_v155_pristine.txt`（pristine 150e3ef：215／12）、`qa161/suite_v155_work.txt`（工作版：216／12）
