# NOTES_V20A137_MAP.md — v20a137 地圖 cover 放大＋拎走地區名＋可撳範圍樣本

## 拍板背景（用戶 2026-11-12）
- 21:03：**做 cover 裁圖放大**——430×932 屏地圖圖高而家 509pt（闊度-bound），v135 卡收細後騰出嘅位變咗卡下面 229pt 羊皮紙。改 cover 裁圖，令 932 屏地圖圖高放大、食埋嗰啲羊皮紙位。
- 21:03：**大地圖唔需要地區名**——拎走 12 個真實地區名細字層（中環／金鐘／灣仔等）。15 個地點名保留。
- 21:04（追加，入 v137）：**大地圖建築物可撳範圍要明確顯示**——而家係隱形熱區，玩家要一眼見到邊度撳得。形式跟地圖墨水風一致（淡描邊／光暈，唔用返之前用戶話醜嘅釘）。**先出樣本截圖，唔好直接入遊戲**——拍板先接入。

## 幾何分析：點解唔裁源圖
- 現況（基線 `qa137/drive137_pre2.json`）：圖 `assets/hk_map_v6.jpg` 1376×1824（比例 0.7542）；`#app` 闊 cap 390px → 舞台闊 384 固定；contain 之下圖高＝384÷0.7542＝**509pt**，已經係上限。
- 建築 span 實測 x≈95–1300px（闊約 1250px，見 `qa137/map_grid.jpg` 5% 網格對照）：矩形裁源圖只會令比例更闊、更矮（裁到建築 bbox 係 0.806，圖高得返 476）——**所以源圖唔郁**（`MAP_IMG` 照舊 `assets/hk_map_v6.jpg`），改 cover 顯示。
- 新制：polaroid 恢復 `flex:1` 食返 wrap 剩位；well 變 flex column 置中；舞台 `aspect-ratio:1270/1824`（窗闊＝384×1824÷舞台高；1270＝建築 span 1240＋30 安全邊），384 闊嗰陣高 **551pt（509→551，+42）**；`max-height:100%` 令 700 短屏舞台跟返 well 高（514，唔爆版）。`object-position:60% 50%`：932 窗 [~63,~1334]，建築 95–1300 兩邊各留 ~30px；700 近乎全幅（窗 [~8,~1371]）。
- v20a43 教訓：cover 會裁圖邊，熱區百分比對位靠彩數——所以今次熱區唔再靠靜態 %，改 JS live 換算（見下）。

## 改動清單（index.html，＋103 行淨）
- **CSS 層**（`</style>` 之前，＋23 行）：`#app .map-polaroid{flex:1 1 auto}`、`#app .map-well{flex:1 1 auto;height:100%;display:flex;flex-direction:column;justify-content:center}`、`#app .map-stage{flex:0 0 auto;width:100%;height:auto;aspect-ratio:1270/1824;max-height:100%}`、`#app .map-img{width:100%;height:100%;object-fit:cover;object-position:60% 50%}`。
- **JS 換算**（drawMap 之前，＋73 行）：`MAP137_NATURAL={w:1376,h:1824}`、`map137CoverTransform()`（由即場渲染幾何：舞台盒＋圖 natural 尺寸＋computed object-position 計 cover 換算；contain 嗰陣回傳 null＝identity）、`map137ImgPctToStagePct()`、`positionMapLabels137()`（.mn68＋.md97-venue99 由 inline style anchor 存入 dataset 再即場定位；**橫向 clamp**：錨點太貼邊嗰陣夾返入舞台——見「切字修復」）。
- **drawMap hook**（＋6 行）：fan-out 後 `placed`（圖 %）換做舞台 % 先定位；pinPos／btn 定位／goPin 最近針邏輯全部自動跟舞台 % 行，唔使改。drawMap 尾（＋2 行）：呼叫 `positionMapLabels137()`。
- **resize 監聽**（＋9 行）：debounced 160ms，叫 `scheduleStoryMapRedraw("resize137")`（內含 drawMap）。
- **HTML**：刪 12 個 `.md97` 地區 div（鑽石山／清水灣／旺角／九龍城／油麻地／紅磡／尖沙咀／中環／金鐘／薄扶林／灣仔／銅鑼灣），**金禧大酒店會場標籤保留**；容器 `#map-districts97` 保留；註解更新。15 個 `.mn68` 地點名＋LOCS x/y 唔郁（圖 % 係 source of truth）；熱區仍 52px。
- **回滾**：刪 CSS 段＋JS 段＋還原 12 地區名 div，drawMap 會跌返 contain % 定位。

## 切字修復（實駕捉到）
- 第一版 post drive 嘅 932 截圖見到左緣兩個名俾 polaroid 框邊切走半隻字：**金龍茶餐廳**（錨 11% → stage x=15）同**金禧大酒店**（錨 11% → stage x=16），兩個都係 translate(-50%) 置中，左緣跌出舞台（x=23）。
- 修法：`positionMapLabels137()` 加橫向 clamp（錨點夾去 `[w/2+2, W−w/2−2]`）。修後兩個名 x=25（舞台內 2px 邊距），15 名＋會場標籤全部喺舞台入面（兩屏 drive 數字核實）。縱向唔使夾（頂錨 ≥2%＋負 offset 落點 ≥9px）。

## 實駕量度（Playwright，`qa137/drive137.py`，基線 pre2 vs 實作 post2）
| | 430×932 pre | 430×932 post | 430×700 pre | 430×700 post |
|---|---|---|---|---|
| 圖高（img／stage） | 384×509 | **384×552（+43）** | 384×509（可見 495） | 384×494（可見 494） |
| 卡底羊皮紙 | 229pt | **12pt** | 12pt | 12pt |
| 卡高 | 121 | 121 | 121 | 121 |
| 針／地點名／地區名／會場 | 15／15／13／1 | **15／15／0／1** | 15／15／13／1 | **15／15／0／1** |
| 逐針實撳 | 15/15 | **15/15** | 15/15 | **15/15** |
| page errors | 0 | 0 | 0 | 0 |
|  verdict | FAIL（地區名 13） | **PASS** | FAIL（地區名 13） | **PASS** |

- 700 可見圖高 495→494（−1pt）：之前 img 全高 509 溢出 polaroid 14px（得 495 可見），而家 cover 裁走嗰 14px，建築唔受影響；針／名全部重對、15/15 撳得中，唔係回歸。
- 932 針位（stage %，post2 實測）：ad_adm 87.09/60、ad_central 64.33/57、agency_ho 21.00/86、cafe_cha 11.24/16、film_cotton 68.67/11、film_harbour 81.67/18、film_lion 51.33/12、gift_shop 41.58/35、hospital 41.58/73、rec_hk 27.50/24、rec_star 82.75/82、rec_wanchai 73.00/77、tvb_harbour 92.50/15、tvb_kowloon 35.08/45、tvb_longmen 39.41/14。932 係 height-bound，y% 不變、x% 按 `new_x% = old_x%×1.082−4.84` 換算；700 係 width-bound，近乎 identity（y% 微調 ±1.5% 係上下各裁 ~27px 圖邊）。
- 截圖：`qa137/shots/post2_430x932.png`、`qa137/shots/post2_430x700.png`（左緣兩名修復後完整可見）。
- Probe 修復（drive137.py）：sheet 標題改 substring 檢查（標題係「圖標＋名 · 地區」）；統一 `advance_story()`（下一句／繼續，否則第一個可見掣——ENC79 三選唔會空轉）；每單前 `ensure_on_map()`＋reset `S.travel114`（probe 專用，改 live S 唔郁存檔）。

## 地區名拎走
- 刪 12 個 `.md97` 地區 div（HTML，index.html 約 L5426–5431 段）；`.md97`／`.map-districts97` CSS 保留（會場標籤仲用緊）；`#map-districts97` 容器保留。
- 驗證：兩屏 drive 地區名 0、會場標籤 1（金禧大酒店，932 位置 (25,326)，舞台內）。

## 可撳範圍樣本（未入遊戲，待用戶拍板）
- 樣本頁：`qa137/sample_hotspots.html`（獨立頁，唔入 index.html）；截圖：`qa137/shots/sample_hotspots_430x932.png`。
- 形式：深啡墨線（#3a2e22）2px 淡描邊＋米紙光暈（`box-shadow:0 0 0 3px rgba(243,231,200,.55)`），圓角 12px，描出建築物輪廓；現有 52px 熱區用虛線圓做參考（遊戲唔會顯示）；地點名照遊戲原位。
- 15 建築 bbox（圖 %，由 `qa137/map_grid.jpg` 5% 網格對照量度）：
  film_lion [47,61,8,15]、rec_hk [24,36,20,28]、tvb_longmen [38,45,6,22]、tvb_kowloon [35,46,39,47]、tvb_harbour [86,95,10,16]、film_cotton [63,73,7,14]、film_harbour [74,80,16,21]、ad_central [52,69,47,67]、ad_adm [79,92,50,69]、rec_wanchai [66,75,73,81]、rec_star [77,89,77,87]、cafe_cha [7,22,11,20]、agency_ho [7,27,80,92]、gift_shop [28,53,32,38]、hospital [33,53,68,78]。
- 樣本內驗算（932 cover 幾何）：**15 範圍全部渲染；重疊：無；掠過地點名邊：無**（名完全喺範圍入面＝ok，邊框唔掠字；名掠過範圍邊先算遮）。量度期間修過嘅 bbox 衝突：海港廣播／維港電影／紅棉影業三角重疊（收窄三框）、灣仔／天星相鄰（x 76 分界）、廟街禮品框左伸去 28% 包住九龍電視台名（v20a68 名位同市集重疊，框唔可以避開個名，改為完全包住佢）、中環廣告框左伸去 52% 包住個名（名錨 60% 撞正框邊）。
- 樣本幾何同遊戲一致（同一條換算，同一 932 cover 舞台 384×552＋object-position 60% 50%）。

## 測試
- 新測試 `tests/test_ui137_map_static.py`：31 項，全 PASS；反證：對 pristine v135 行，19 項 FAIL（exit=1）。
- Resync（4 檔，全部 work PASS、pristine FAIL 反證成立）：
  - `test_travel114_static.py`：死行號重對（COUNT 13＋FREE 27＋DEF／WRAPPER；移位：CSS ＋23／地區名 HTML －10／JS ＋73＋6＋2／resize ＋9；3 處重複行文按次序對位）。
  - `test_text125_static.py`：三處死行號各 ＋13（currentLine 27558→27571、advance 27671→27684、familySafe 33269→33282）。
  - `test_ui108_static.py`：S-7 六個地區斷言由「新位在」反轉做「地區 div 已刪」；金禧＋15 地點名斷言不變。
  - `test_ui128a1_static.py`：薄扶林／灣仔／銅鑼灣三個標籤斷言反轉做「地區 div 已刪」。
  - `test_map97_static.py`／`test_venue99_static.py`：地區名 12→0（會場標籤保留，計數改數 div——v137 JS 亦引用 `.md97-venue99` 類名）。
  - `test_map54_static.py`：allowlist 加 `v20a137`。
- 全套（`qa137/run_all_tests.py`，206 檔）：**work 7149 項，7105 PASS／44 FAIL；pristine（main 673df0d，205 檔）7118 項，7074 PASS／44 FAIL——FAIL 清單完全相同（12 檔，全部 pre-existing），零回歸**。Work 多 31 項 PASS，全部來自新測試。
- 語法：兩段 inline script `node --check` 通過。

## 落地
- 工作副本 `~/workspace/linji-work137/`，分支 `v20a137`，基底 origin/main `673df0d`（v135；落地前 `git fetch` 確認 v134／v136 未行前，唔使 rebase）。
- 落地行新制：常駐 clone checkout main → `git merge --squash v20a137` → commit → push main（經 deploy key，唔開 PR）。
- **已落地（2026-11-12）：main `ea6a941`（squash，分支 `0a6afad`）；線上核實：index.html 5,185,661 bytes、sha256 `e3a8a7097ddbbb11fa5722fa6ff4188ebc97720f0afea0b0e34334e7f601241c`，同 repo 完全一致。**
