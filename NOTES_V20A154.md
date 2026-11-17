# NOTES_V20A154 — v138 設計 review A1＋B1＋B2＋B3 修復

基底：main `e08a070`（v148）。分支 `v20a154`，工作副本 `~/workspace/linji-work154/`。
報告：`~/workspace/linji-design-review-v138/REVIEW.md`（55 張截圖）。
**唔落地**——實作＋測試＋實駕，交統籌驗證＋落地。

## A1 — 重生 6 張走樣表情（鎖死衫色／髮長）

做法跟 v138 同一套：base 圖＋風格錨做參照，成張重生，只換面部表情；
米白光邊 RGB(243,233,210) 焗入圖（腳本 `qa154/work154_proc.py`＋`qa154/bake154.py`，
焗邊 6/6 PASS，far_cream=0，冇雙重邊）。教訓：陸柏言 base 著嘅係**黑高領**，
gen1 寫咗白恤衫係新偏差，gen2 用 resume_from_snapshot_id 逐張修正返黑高領。

量度方法（同 review）：軀幹帶 y 0.30–0.45、x 0.30–0.70、alpha>128 像素平均 RGB，
對 base 取 L1 距離；鍾楚凝用量側髮像素（y 0.45–0.75、x 外側 25%）。

| 圖 | 舊 L1／fringe | 新 L1／fringe | 目標 |
|---|---|---|---|
| luk_baakyin angry（軀幹） | 35 | 4（測試實量 3） | ≤19 |
| luk_baakyin sad（軀幹） | 37 | 3（測試實量 2） | ≤19 |
| luk_baakyin smile（軀幹） | 36 | 4（測試實量 3） | ≤19 |
| luk_baakyin angry（頸 V 區 y 0.20–0.30） | 29 | 3（測試實量 2） | ≤19 |
| mak_zhendong angry | 15 | 8（測試實量 9） | ≤19 |
| mak_zhendong smile | 16 | 2（測試實量 2） | ≤19 |
| chung_choning angry 側髮 | 203,797（base 105,191） | 127,286（測試實量 128,050；base 105,958） | ~base 水平（測試閾值 ≤140,000） |

（舊／新 L1 係 `qa154/measure154_gen2.json`；括號內係 `tests/test_expr154_static.py`
獨立重算，±1 係取樣邊界四捨五入，全部遠低於閾值。）

入庫：`qa154/baked154/*.webp` 已覆蓋 `assets/story/fullbody/` 同路徑 6 張，
其餘 29 張唔郁。原檔喺 `gen154/`（唔入 repo），對照圖 `qc154/compare_*.png`／`face_*.png`。

cache-buster：三條表情載入路徑（主線／WF4／巧遇）全部經 `dlg106Candidates`；
喺佢入面加 `DLG154_CACHE` map（6 個 stem→`"20a154"`），`addStem` 用佢；
其餘 29 張／boss 圖／影圖維持 `?v=20a106` 唔郁。

## B1 — 主線舞台 plate 填滿到底

實量基線（probe `qa154/probe154_b1.py`，430×932／430×700）：
plate bottom 844／612，離 viewport 底 88px；88px = `.sp-stage-inner` padding-bottom 66px
＋ `#modal-inner` padding-bottom 12px（L3506 規則，(2,2,0) 蓋過 L4218 `padding:0`）
＋ `.modal` 外圍 10px inset。

修法（只限對白／旁白模式，抉擇屏唔郁）：
1. `.sp-stage-inner` padding-bottom 66px → `env(safe-area-inset-bottom,0px)`；
2. `#modal-inner` padding-bottom 12px → 0（`#mask.story-play-on:not(.tut-on) #modal-inner`，
   (2,2,0) 同 L3506 打和，靠後排位置贏）；
3. `.dlg106-plate` 高 118 → **170px**（內容 96px＋上 pad 10px＋底 pad 61px＋border 2px，
   全域 border-box；底 pad 61px = `#modal-btns` 高，文字唔俾掣列遮）；
   舊 bust 路徑 `.sp-plate` 同樣加底 pad 61px；
4. 對白／旁白模式 `#modal-btns` 漸變 → transparent（唔好喺米白 plate 底染深色）。

落地後 plate bottom = modal 底（922@932／690@700），離 viewport 剩 10px
（`.modal` 外圍 inset，成個 modal 四邊一樣，唔係 plate 缺口；巧遇 overlay 係
`position:fixed;inset:0` 逃出 app 框先至做到 0px，主線 modal 唔重構就去唔到 0）。
人物腳底 bottom:10%，plate 頂 726→752@932，仍遮小腿中段以下，v108 遮腿設計不變。
實駕量度見下文 §實駕 B1。

## B2 — 單人舞台補場景圖

跟 v134 `WF4_SCENE_OVERRIDE134` 做法：`spResolveBgKey` 入面加
`STORY_SCENE_OVERRIDE154`，按 node id 優先覆寫；`spBgClass` 加 `bg_154_` 接受條件；
`spChoiceBgClass` 經 `spResolveBgKey`→跌返 `spBgClass`，一併受惠
（R_hiu_ending 結尾 commit choice 都有天台底）。

- `R_vera_meet`（Vera 見面，setting「星河電視台造型間／試裝」）：**重用現成圖**
  `assets/story/locs/bg_loc_tvb_longmen.jpg`（星河電視台內景：佈告板＋放衫手推車＋盆栽，
  同一棟樓；v103 年代重製版）。唔使新生成。
- `R_hiu_ending`（曉晴線收尾，setting「廠景天台」）：**新生成**
  `assets/story/locs/bg_154_rooftop.jpg`（720×1280，228,327 bytes，cover-crop 自 gen 圖 1152×2048）。
  參照相：Greg Girard 1989 年九龍天台實拍，存 `~/workspace/linji-work154/refs/ref_rooftop_girard1989.webp`
  （來源頁 https://ocula.com/artists/greg-girard/ ，已 curl preflight＋下載核實 570×372；
  來源記錄 `refs/SOURCES.md`）。生成圖目視 PASS：空天台＋水箱＋晾衫繩＋舊樓＋山＋海＋低飛客機，
  黃昏，冇人冇字冇水印。`spBgImageCandidates` 現成鏈已推 `assets/story/locs/<key>.jpg?v=20a104`，唔使改。

## B3 — C12 剪影聽者變暗 0.60

`spDlgCharsHtml` 入面舊行令影講者／聽者一律 bright=1；修法係刪走嗰行，
影講者／聽者一律跟返正常 bright 計算（對白／旁白模式 0.6、電話 0.8、講者 1）。
**唔郁 `dlg119Candidates`**（聽者繼續用 `_dim` 資產）同埋唔郁真人聽者；
WF4 版同巧遇中間影本身已啱，唔郁。
誠實註記：影聽者實效約 0.78（焗入）× 0.6（CSS）≈ **0.47**；filter 讀數係 0.60，
符合 review 量度方法。

`tests/test_dlg119_static.py` §5 已更新做 v154 新行為（舊斷言「影唔加 brightness filter」
已作廢，註明原因）。

## 測試

- 新測試 `tests/test_expr154_static.py`：30 項（A1 PIL 色差 7＋cache 3＋B1 source 7＋B2 6＋B3 4＋不變量 3），工作版全 PASS。
  反證：對 pristine main（`e08a070`，`/tmp/pristine154/`＋assets/content symlink）跑，
  15 PASS／**15 FAIL**、exit 1、唔 crash；15 FAIL 全部係預期嘅 v154 新斷言
  （A1 source 3＋B1 6＋B2 4＋B3 2）。
- 全套 `qa131/run_suite.sh`（`qa154/suite_work154c.txt`）：pristine **211 PASS／12 FAIL**；
  工作版（resync 後最終樹）**212 PASS／12 FAIL**，FAIL 集合同 pristine 逐項相同
  （test_flash51／giglib36／pacing35／poster59／rumor49／slot50／soft_tip_111_restore／
  start53／weave43／weave44／weave49／wrap38），**零回歸**。+1 PASS 係新加嘅
  `test_expr154_static.py`。中途一跑出過 183／41（已知波動，見 AGENTS.md v151 教訓；
  額外 29 項 flaky .py 逐個直接重跑 29/29 PASS），最終乾淨一跑 212／12 作準。
- 三個 resync（全部係 index.html 改動淨 +64 行引致嘅行號漂移，唔係功能回歸）：
  `tests/test_travel114_static.py`（DEF 53562→53626、WRAPPER 44171→44235）、
  `tests/test_dlg138_logic.js`（6 張 `?v=20a154` 刻意改動）、`tests/test_text125_static.py`
  （三處釘死行號）。三檔喺 pristine 上照樣 FAIL，證明 resync 冇放水。
- 相關測試逐個直接覆驗：`tests/test_dlg119_static.py` PASS（§5 已改 v154 行為）。

## 實駕

本地鏡像＋Playwright；實駕環境：venv `/home/hatch/pwenv49/bin/python`（冇 PIL，
圖像處理用系統 `python3`），瀏覽器 headless shell 1248，gate-on 用 `?softPreview=1`，
播種存檔直接寫 localStorage（key `starVolunteer_map_v19w`，slot 1）。

### B1 — plate 填滿到底（`qa154/probe154_b1.py` → `qa154/probe_b1.json`）
932：plate 752..922（高 170），離 viewport 底 gap **10**（原 88）；700：plate 520..690
（高 170），gap **10**。platePadBottom 61px，stageInnerPadBottom 0px，modalBtnsBg none，
行文零溢出（scrollH=clientH=43），0 pageerror。剩低 10px 係 `.modal` 外圍 inset，
唔係 plate 缺口（見上文）。

### B2 — 兩幕場景圖（`qa154/probe154_b2.py` → `qa154/probe_b2.json`，0 pageerror）
- `R_hiu_ending`：bgClass `sp-bg-layer bg_154_rooftop has-photo`，
  bgImg `assets/story/locs/bg_154_rooftop.jpg?v=20a104`；首句「呢幾年我哋一齊經歷咗咁多……」。
- `R_vera_meet`：bgClass `sp-bg-layer bg_loc_tvb_longmen has-photo`，
  bgImg `assets/story/locs/bg_loc_tvb_longmen.jpg?v=20a104`；首句「你就係新嚟嗰個臨記？……」。
截圖：`qa154/shots154/hiu_ending_bg.png`、`vera_meet_bg.png`（天台新圖／電視台內景＋人物，plate 貼底）。

### B3 — C12 剪影聽者變暗（`qa154/probe154_b3.py` → `qa154/probe_b3.json`，1200ms／步，0 pageerror）
7 個同場命中：steps 16–18 講者陸柏言 `luk_baakyin_sad.webp` **b=1.0**，
男剪影聽者 `shadow_male_dim_base.webp` **b=0.6**（三句連續一致）；steps 19–22 旁白模式
兩者同為 0.6（正確）。截圖 `qa154/probe_b3_settled.png`。

### A1 — 6 張重生圖舞台實播（乾淨重驗 6/6，見下文「實駕污染」一段）

每目標三重驗證：DOM src 版本＋canvas 讀解碼後軀幹色＋fetch 字節 hash（同磁碟檔大小一致）
＋settle 2s 後截圖。

| 目標 | 場景／步 | src | canvas 軀幹色 | fetch 字節 |
|---|---|---|---|---|
| luk angry | e_luk_first step 10「臨記咁多個，我記唔晒。唔好阻住走廊。」 | `?v=20a154`，879×2855 | (43,27,35) 酒紅 | 173,644 |
| luk sad | C12 step 16「唔好意思，連累你哋。……」 | `?v=20a154`，877 闊 | 截圖軀幹 (41,26,33) 酒紅 | 166,126 |
| luk smile | e_luk_heart step 18「……多謝。肯靜靜聽我講晒嘅人，真係冇幾個。」 | `?v=20a154`，872×2843 | (44,31,37) 酒紅 | 168,190 |
| mak angry | e_mak_first step 14「收聲。」 | `?v=20a154`，847×2810 | (111,93,73) 橄欖綠 | 228,454 |
| mak smile | e_mak_heart step 12「捱到今日，唔係我叻，係我唔敢停。」 | `?v=20a154`，872×2850 | (110,90,71) 橄欖綠 | 234,070 |
| chung angry | e_chung_heart step 8 day 368「有天份冇用功，一樣企唔穩。……」 | `?v=20a154`，930×2750 | (63,74,76)；目視及肩捲髮 | 220,314 |

證據檔：`qa154/drive154_a1clean.json`（luk angry／mak angry）、
`qa154/drive154_a1clean2.json`（mak smile／chung angry）、`qa154/probe154_enc.log`
（luk smile，fetch＋settle 截圖 `qa154/probe_enc_smile.png`）、
`qa154/probe154_c12.py`（luk sad，fetch 166,126 bytes＝磁碟檔，截圖 `qa154/probe_c12_sad.png`）。
乾淨截圖：`qa154/shots154/clean_e_*_*.png`。0 pageerror。

### 實駕污染（重要：第一輪 a1 截圖唔可以直接用）

第一輪 `qa154/drive154_a1.py` 有兩張截圖（luk smile、luk sad）量到藍衫 (26,31,47)，
同磁碟新檔矛盾。追查證實係**測試 harness 跨污染，唔係產品問題**：
- `qa138/drive138.py` 冇 `if __name__ == "__main__"` guard，import 即跑 main；
  其 `URL` 常數喺 import 時由 `PORT=8971` 計出，事後改 `d138.PORT` 改唔到 URL。
- 同一時間另一票工人（v157）嘅 server 佔住 8971，serve 緊 `linji-work157`；
  凡係改咗 PORT 但冇改 URL 嘅 probe（repro、probe154_enc2），瀏覽器都係載入咗 v157 頁——
  證據：DOM src `?v=20a106`、naturalWidth 445（舊檔尺寸）、fetch 61,794 bytes（舊檔大小）、
  canvas 軀幹 (26,32,49) 藍——同 v157 樹入面嘅 v138 舊圖一致。
- 產品本身三重反證：磁碟 6 檔 md5 同 `qa154/baked154/` 逐一相同（新檔）；
  載入 work154 頁嘅 probe（probe154_enc／probe154_c12／a1clean／a1clean2）全部
  `?v=20a154`＋fetch 字節＝磁碟大小＋canvas／截圖酒紅／橄欖綠；舊藍圖只剩
  `qa138/baked138/`（唔係 asset 路徑）同 git 歷史。
- 修法：重驗 probe 用截斷版 drive138（去掉 import-main block）＋獨立 port（8931，
  事前確認 free；8971／8995 分別俾 v157／review155-mirror 佔住）＋事後改 `d138.URL`＋
  PAGE guard（assert URL 含正確 port＋頁面含 `20a154`）。另發現 `stop()` 間中殺唔死
  http.server（PID 19474 殘留約 10 分鐘後自行消失），開 probe 前要先 `ss` 睇 port。
- 第一輪 a1 其餘截圖（luk angry 酒紅、mak／chung）亦唔可以直接引用——同一 run 混咗
  新舊頁；A1 6/6 以本節上表嘅乾淨重驗為準。`qa154/shots154/branch_e_*` 舊截圖留檔，
  唔好當證據用。

---

## 落地附錄（2026-11-17，v154-land）

**背景**：本票 2026-11-13 喺 `linji-work154` 做到一半（commit `de63c5d`，基底 main `e08a070` v148），
一直未合併。2026-11-17 由常駐 clone main `32d613d`（v163，父系 `6e051e7` v261）重新落地：
新 clone 式工作副本 `linji-work154r`（origin 係常駐 clone 本地路徑），分支 `v154-land`，
`git cherry-pick de63c5d` → `80ac827`。原 `linji-work154` 嘅 origin 係 github.com（直推風險），
唔用佢嚟 push；佢入面嘅 untracked `assets154/`／`gen154/`／`qa154/`／`qc154/`／`refs/` 係當時工作檔，
唔入 repo，落地唔使。

**cherry-pick 衝突**：只得 2 檔（`test_text125_static.py`、`test_travel114_static.py`），
其餘 12 檔（index.html、6 張圖、bg_154_rooftop.jpg、test_expr154_static.py、test_dlg119、test_dlg138）自動合併。
兩檔衝突全部係釘行漂移，用 difflib 單次掃描映射解決（腳本 `/tmp/resync154.py`，唔入 repo）：
text125 三釘 10994→11053／11131→11195／16355→16419；
travel114 COUNT 12＋FREE 35＋DEF 40072→40136＋WRAPPER 28024→28088，
openLoc( 呼叫點總數 53 不變（v154 零新增呼叫點）。

**第一輪全套 312／17**：7 檔新 FAIL 全部係 v154 index.html 淨 +64 行引致嘅釘行漂移，
逐個直接跑全部 FAIL（唔係波動）。第二輪 resync（腳本 `/tmp/resync154b.py`）：
- kwan151：13 釘重對（8860→8898／9201→9239／9204→9242／9205→9243／9206→9244／9249→9287／9468→9506／10469→10516／10502→10549／14300→14364／14309→14373／14310→14374／14345→14409），內容逐字核實。
- rom176：6 釘重對（6351→6389／14703→14767／38470→38534／38843→38907／40003→40067／40103→40167）。
- tang152：3 釘重對（idx 9019→9057／14631→14695／14753→14817）。
- tang171／tang173／gift185：總行數公式＋v154 +64（44648→44712，標籤 44659→44723）；DEF 40072→40136（guard 40078→40142、lines[40071]→lines[40135]）；tang173 L4862 釘 5155→5193（B1 CSS ＋38 在前）。
- awei201：loader 檢查語義更新（v154 故意改動，唔係漂移）——fullbody ?v= 由寫死 `20a106` 改做 `DLG154_CACHE[...] || "20a106"` 變量，預設仍係 20a106；6 張 v154 升 20a154 由 test_expr154_static.py 另行守門。
- resync commit `7cc8829`。

**第二輪全套 319／10**（`/tmp/suite154_land2.log`）：PASS 319＝基線 318＋新測試 test_expr154_static.py 1 項；
FAIL 10 全部係已知 pre-existing（flash51／rumor49／slot50／soft_tip_111_restore／start53／weave43／weave44／weave49／wf5_87／wrap38），**零回歸**。
`node --check` 兩段 inline script 全部 OK；受影響 5 檔（expr154／text125／travel114／dlg119／dlg138）＋resync 7 檔逐個直接跑全部 PASS。

**合併**：常駐 clone checkout main → `git merge --squash v154-land` → commit → push main（deploy key，唔開 PR）。
**實機驗證押後**（瀏覽器死）：B1 plate 填滿、A1 新表情、B2 天台場景圖、B3 剪影 0.60 未實機驗過，等瀏覽器恢復再驗。


