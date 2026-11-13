# NOTES v20a194：頒獎禮拆 soft 閘，正式 tip LIVE

- 基底：main `2374637`（v195 NOTES；遊戲 `4f47077`，線上 5,343,979 bytes sha `369e4c96…` 已核實）
- 分支：`v20a194`（工作副本 `~/workspace/linji-work194`；常駐 clone 當時 rebase 緊 v198，工作樹有衝突檔——本票淨係攞常駐 clone 做 clone 來源，冇掂佢工作樹）
- 狀態：**已實作＋已測試＋已實駕，未落地**（落地由統籌做）
- 根因報告：`~/workspace/linji-work-awards-missing/INVESTIGATION.md`

## 1. 改咗乜（index.html 淨 +65 行：68 增 −3 刪，總行數 60609→60674）

| 位置 | 改動 |
|---|---|
| `queueAwardsOnSeasonWindow`（舊 L46070） | **拆走閘行** `if(!awardsSoftOn() && !opts.force) return [];`，換 3 行註解。頒獎禮唔再跟 soft 旗標，live 模式照常排期。`awardsSoftOn()` 本身保留、語義唔郁（淨係得呢一個呼叫者，拆咗之後佢暫時零呼叫者，但框架共用函數唔刪除）。`opts.force` 保留（除錯路 `awardsDebugForceSeasonWindow` 照用）。 |
| `awards194ApplyMetaTip(FW)`（新，`awards188ApplyNpOverlay` 之後）＋ `loadFreeplayFramework` 呼叫 | **pack meta tip 行覆寫層**：載入嗰陣將 `FREEPLAY_FW.awardsSchema.meta`／`awardsStub.meta` 嘅 `softStatus` 改做 `"PASS"`，note 嗰句 `Soft≠PASS; no tip LIVE` 改做 `v20a194: tipped LIVE`。**磁碟上兩個 JSON 一字唔郁**（見 §2 點解）。 |
| `awardsCheck()` | 加兩項核實：① **live_queue 探針**——用 `forceCeremonyId` 跳季節／週數（唔跳旗標／build）即場 queue 一次，live 下返唔到嘢就 fail；快照＋`finally` 還原晒 flags／`_pendingAward`／queue／`S.pendingAwardPack`，自檢零副作用。② **meta_tip 核實**——runtime 兩個 pack meta 唔係 `PASS` 就 fail。return 嘅 `softStatus:"≠PASS"` → `"PASS"`。 |
| 頒獎禮區 header 註解 | `Soft≠PASS; no tip LIVE` → `v20a194 tipped LIVE (soft 閘已拆)`。 |
| 5 檔釘行測試 resync | `gift185`／`rom176`／`tang171`／`tang173`／`travel114`：淨 +65 行漂移，釘行按 difflib 映射更新（見 §4）。 |

**唔郁嘅嘢**：C17 `awardResolved`（L19726／L25529–25538）零 code 改——開閘之後自動變返有意義（實駕 §5D 證實）；季前提示 `awards62SeasonHints` 零改（本來就冇閘，而家佢講嘅嘢終於係真嘅，實駕 §5C 對得上）；贏線 0.875／計分／提名門檻／15 個獎項／典禮演出／SAVE key／softRev s107／`?v=v20a10` 全部唔郁；B2 廣告男主角贏唔到唔喺呢票。

## 2. 點解 meta tip 行覆寫，唔直改 content JSON

任務原話係「兩個 pack 嘅 `softStatus` 正式改狀態」，開工先 survey 咗：

1. **第一版係直改 JSON**（兩個 pack `softStatus` → `PASS`＋note）。全套即刻捉到 3 項紅線測試失敗：`aud91fix122`／`aud91fix124`／`gigreq110`——佢哋行 `git diff --name-only HEAD -- content/`，要求 content JSON **零改動**（v157 只豁免 `story_detail_c1_to_c17.json`）。呢條係 repo 既定紀律，v188 獎項名都係行覆寫／注入（`awards188ApplyNpOverlay`），唔係我諗出嚟嘅。
2. 於是**還原兩個 JSON**（而家 `git diff` 入面 content 零改動），改行覆寫層：`awards194ApplyMetaTip` 跟足 v188 模式，喺 `loadFreeplayFramework` 入面 `awards188` 覆寫之後呼叫。磁碟上 pack 繼續係 `≠PASS`，runtime meta 先係 `PASS`——自檢 `meta_tip` 驗嘅就係 runtime 值。
3. 呢個決定係**跟任務條件句做**（「如果 meta 要經覆寫表／注入先改得，照 repo 紀律做」），唔係繞過。統籌如果想磁碟都改做 `PASS`，要另外豁免／改嗰 3 條紅線測試，先可以直改。

## 3. softStatus 各讀者 survey（開工先做齊，分清楚先郁手）

`index.html` 入面 `softStatus` 全部 10 處（`softStatus:"≠PASS"` 6 處＋`softStatus!=="≠PASS"` 3 處＋`awardsCheck` return 1 處）：

| 行（舊） | 讀者 | 處理 |
|---|---|---|
| L28604／28661／28693 | Tutorial Phase2 steps 5–6 overlay（`phase2Steps56Copy`／loader／自檢） | **唔郁**——唔關頒獎禮事，係框架共用寫法 |
| L45277 | `postShootRewardCheck` return | **唔郁**——殺青獎勵，唔關頒獎禮事 |
| L46305 | `awardsCheck` return | **改做 `"PASS"`**（頒獎禮專屬）＋加 live_queue／meta_tip 探針 |
| L49340 | `newspaperCheck` return | **唔郁**——報紙，唔關頒獎禮事 |
| L49516 | `__freeplay.check` return | **唔郁**——成個 freeplay 框架 |
| L54641 | Phase3 inline mock meta | **唔郁**——紅星遠觀 mock |
| L57497 | `restSleepFxCheck` return | **唔郁**——休息片 |
| L25745 | freeplay-slots stub 字面 | **唔郁** |
| content 兩個 pack | `SCHEMA_AWARDS_CEREMONY_v1.json`／`STUB_AWARDS_CEREMONY_v1.json` meta | **磁碟唔郁**（§2）；runtime 經覆寫改做 `PASS` |

另核實：**冇任何 code 讀 `FREEPLAY_FW.awardsSchema.meta.softStatus`／`awardsStub.meta.softStatus`**（loader `loadFreeplayFramework` 直接 fetch 入 FW，唔驗 meta），所以覆寫唔會撞 loader；`awardsSoftOn()` 唯一呼叫者就係拆走咗嗰行閘。

## 4. 新測試 59 項（logic 26＋static 33），反證乾淨 FAIL

- `tests/test_awards194_logic.js`（26 項）：真 pack JSON＋真排期函數，build／render 用 stub。覆寫後 meta PASS＋note 改＋冪等；`awardsSoftOn()` 語義唔郁；LIVE 三窗（春／夏／冬）各返 1；done 旗標唔重排；C10 讓路照延期；debug force 路照 work；`awardsCheck` ok＋`softStatus:"PASS"`＋零副作用＋invited 旗標／pending pack 原樣還原；meta 未 tip 嗰陣 `awardsCheck` fail（`meta_tip`，live_queue 本身照過）。
- `tests/test_awards194_static.js`（33 項）：閘行唔見、queue 體（除註解）唔再提 `awardsSoftOn`、函數保留；磁碟 JSON 仲係 `≠PASS`（紅線）＋覆寫函數／呼叫次序／4 場門檻一字唔郁；`awardsCheck` 有 live_queue＋meta_tip、全檔 `softStatus:"PASS"` 恰好 1 處、`≠PASS` 仲有 6 處；其餘 5 類讀者唔郁；SAVE／softRev／`?v=`／C17 閘唔郁。
- **反證**：對 pristine main `2374637` index 行兩份測試 → 各 FAIL 4 項（反證守衛），exit 1，唔 crash。

### 全套 A/B（`qa131/run_suite.sh`）

- A（pristine code＋新測試）：267 PASS／14 FAIL＝12 項穩定 FAIL＋2 項新測試（預期，pristine 未有 v194）。
- B1（第一版：直改 JSON）：261／20——多出 8 項：3 項紅線（§2）＋5 項釘行漂移（§4 下）。逐個直接跑，證實全部唔係隨機波動，係我改動引起。
- B2（最終版：覆寫＋resync）：**269 PASS／12 FAIL——FAIL 清單同基線 12 項逐字相同，零回歸**（flash51／giglib36／pacing35／poster59／rumor49／slot50／soft_tip_111_restore／start53／weave43／weave44／weave49／wrap38）。

### 釘行 resync（慣例：每版更新釘行，唔係放寬測試）

`qa194/resync194.py`（difflib 對位 pristine `2374637` → 工作版）：4 個 hunks（覆寫函數 ＋25／拆閘 ＋2／自檢探針 ＋37／load 呼叫 ＋1），分段漂移 ＜45755＋0／45755–46069＋25／46070–46304＋27／46305–49383＋64／≥49384＋65。**55 個錨點內容逐字相同，BAD 0**。`qa194/apply_resync194.py` 寫入新行號：總行數 60609→60674、openLoc DEF 55102→55167、ROM176 四釘 53532→53597／53900→53965／55039→55104／55133→55198、travel114 COUNT／FREE 各按段映射（＜45755 唔郁，其後 ＋65）、WRAPPER 44443 唔郁。5 檔測試更新後逐個直接跑全部 PASS。

## 5. 實駕（Playwright 932×700，全部 LIVE 裸 URL，0 pageerror）

腳本 `qa194/drive194.py`，報告 `qa194/drive194_report.json`，截圖 `qa194/shots/`（16 張）。本地鏡像 serve sha `111985aa47b6`（＝工作版 index.html）。

| Run | 結果 |
|---|---|
| A 六窗（同一播種玩家，1990 春夏秋冬＋1991 春夏） | **6/6**：每窗 `queue()` 返 1（softFlag 全部 false）、請柬 modal → 出席 → 典禮 frame → flag done。tiers 同調查報告 SOFT 對照組逐字相同：gallery／nominated／nominated／gallery／gallery／nominated。`awardsCheck()` 六窗全部 `ok:true, fails:[], softStatus:"PASS"`。附帶：1991 夏窗 hints 啱啱出「下季就係「維港影藝獎」：仲差 2 部電影作品先夠入圍」（1991 年作品另計，正確）。 |
| B 朝早鏈（真 UI 路） | **PASS**：手帳「返回地圖」→ 地圖「開始今日行程」掣（行咗今日街頭表演，日 60→61）→ 日結板「返回地圖」→ `goToMapForBrowse()` 晨鏈彈出請柬（「定期頒獎／街招年賞請柬／維港街招・年度廣告賞 · 春 1990／金禧大酒店・大禮堂／席位：旁聽席」）→ 出席 → 典禮 frame → flag done。註：第一版 drive 叫錯掣（「開始今日行程」只喺有 soft 行程先出現；地圖掣係行程掣，唔係晨鏈掣）——debug 腳本 `qa194/dbg_b.py` 釐清咗真路徑，先至驗到。 |
| C 季前提示 vs 派柬 | **PASS**：近 miss 玩家（fame 8／credit 10、電視×2）day 60 提示「今季就係「維港街招・年度廣告賞」：仲差 1 部廣告作品先夠入圍」；day 250「今季就係「維港影藝獎」：仲差 2 部電影作品先夠入圍」——同調查報告原文逐字相同。補返 1 部廣告殺青 → 同窗 `queue()` 返 1（廣告賞）；補返 2 部電影殺青 → 返 1（影藝獎，nominated）。提示同派柬對得上。 |
| D C17 awardResolved | **PASS**：day 1065（1992-12-01，第 153 週，C10 已完成播種）TV 殺青×2 → 台慶 `queue()` 返 1 → 出席 → 典禮 frame → flag `1992/award_singho_tv` 由 `""` 變 `"done"`，`awardResolvedSatisfied: true`，dayIndex 1065 ＜ backstopDay 1096——**C17 正門開得返，唔使靠 backstop**。註：12 月係年內第 49 週，C10 未完成嗰陣台慶照舊延期（見 §6）。 |
| E 舊存檔 | **PASS**：扮 soft 模式 save（`1990/award_harbour_ad: invited`＋`pendingAwardPack`，照 `saveQ()` 寫法直寫 localStorage slot 1＋3）→ reload → 「繼續」載入，0 pageerror，flags＋pending pack 完整 → `presentAward()` 即刻彈返請柬 → 出席 → 典禮 frame → done。 |

截圖抽查過（`LIVE_invite_60.png` 請柬＋出席／推辭掣齊；`LIVE_ceremony_160.png` 舞台＋「最佳新人獎／《夜更和音》」白牌），係真畫面唔係 stale frame。實駕期間 3 場典禮撳唔到「跳過」（frame 喺 poll 到之前已播完，`frame gone: true`、flag done——係典禮播完，唔係失敗）。

## 6. 未做／殘留（等統籌決定，唔係 v194 回歸）

1. **C10 未完成者嘅 1992 台慶**：12 月全月都係年內第 49–52 週，`softC10WindowActive()` 會將台慶延期到 1993 年 1–2 月（冬窗尾）；但 C17 backstop 係 1993-01-01（day 1096），呢類玩家依然行 backstop 開 C17——同 tip 之前一樣，係 pre-existing 設計，唔係 v194 整出嚟嘅。做完 C10 嘅玩家行正門（§5D 證實）。
2. **旁聽請柬 gap 行**：gallery 請柬 body 有句「仲差 1 部廣告作品先夠入圍（而家 0/1）」——播種玩家明明做過 2 部廣告（臨記／手模位，唔係 v188 提名角色，所以演員格計 0）。呢句係 `awards62GateLineHtml` 原有文案（v192 C2 只修咗音樂版），v194 冇郁過文案／計分。旁聽席上面印「仲差 N 部」係咪想講，係設計問題，等拍板。
3. **舊存檔載入日數 ＋1**：Run E 播種 dayIndex 60，reload＋「繼續」之後變 61——flags／pending pack 完整，唔影響還原。似係載入路徑本身嘅一日漂移（唔關頒獎禮事），順手記低。
4. **v192 C1（週日報紙遲一日）仲未修**：MEMORY 話遲啲先問用戶，唔急——同 v194 無關，但 tip 咗之後 live 玩家會撞到，排隊嗰陣記得。
5. **B2 廣告男主角／男配角實玩贏唔到**：唔喺呢票，冇郁贏線／計分／門檻（另開票）。
6. **`awardsSoftOn()` 而家零呼叫者**：函數保留咗（任務要求唔刪／唔改語義）。如果將來 soft 框架都唔再用佢，先至一次過清。
7. **磁碟 pack meta 仲係 `≠PASS`**：見 §2——統籌決定直改嗰陣，要同步豁免／更新 `aud91fix122`／`aud91fix124`／`gigreq110` 三條紅線測試。

## 7. 檔案清單（本分支）

- `index.html`（＋68／−3）
- `tests/test_awards194_logic.js`、`tests/test_awards194_static.js`（新，59 項）
- `tests/test_gift185_static.py`、`tests/test_rom176_static.py`、`tests/test_tang171_static.py`、`tests/test_tang173_static.py`、`tests/test_travel114_static.py`（釘行 resync，內容斷言唔郁）
- `qa194/drive194.py`、`qa194/drive194_report.json`、`qa194/shots/`（16 張）、`qa194/resync194.py`、`qa194/apply_resync194.py`、`qa194/dbg_map.py`、`qa194/dbg_b.py`
- 本 NOTES：`NOTES_V20A194_AWARDS_TIP_LIVE.md`
