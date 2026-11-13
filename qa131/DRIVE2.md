# v157 drive2 實駕結果（DRIVE2）

- **正本跑次：run5**（`qa131/drive157.py`，本地鏡像 port 8971，390×844，`?softPreview=1`）
- **日期**：2026-11-13；run5 用時 550 秒，**EXIT=0**
- **pageerror 總數：0；HTTP404：0**（`drive157.json`：`errors: []`、`http404: []`）
- **日誌**：`qa131/drive157.json`（run5 覆寫）；原始 log `/tmp/drive157_run5.log`
- **結論：6 個 phase 全部 PASS**（A/B/C/D/E/F）。Phase E 喺 run2f／run3 兩次唔完整之後，經三次腳本修正＋probe 驗證，run5 終於全通。

## Phase A — N1–N5 全程：PASS

| 節點 | 途徑 | 句數 | done | 首句 |
|---|---|---|---|---|
| C1 第一日：冇價 | ui（事務所 offer「播劇情：第一日：冇價」） | 16 | true | 何生事務所嘅冷氣夠凍，檯面攤開兩份通告。 |
| C2 | force | 11 | true | 片場後巷充滿住煙味同茶記嘅油煙味，幾個老臨記圍埋一齊吹水。 |
| C3 | force | 14 | true | 廠景燈光大亮，副導正喺度調較機位。 |
| C4 何生攤記數簿 | **ui**（offer「播劇情：何生攤記數簿」） | 8 | true | 何生事務所內煙霧彌漫，何生將本殘舊記數簿拍喺枱面，旁邊放住張密密麻麻嘅通告紙。 |
| C5 | force | 12 | true | 片場休息角，等埋位嗰陣空檔。 |

- 抉擇（run5 同 run2f 一致）：C1 idx0 跟張子駿班底；C2 idx0 留低打聽人脈；C3 idx0 當場發難硬碰；C4 idx1 咬牙接下通告；C5 idx0 老實說出所知。
- C1 `route_tv: false`。
- **C4 由 force 變 ui**：run2f／run3 係 force；run5 因為 `open_location_ui` 補咗 enc79 攔截後清走 overlay（見「腳本修正」），開事務所嗰陣撞到嘅攔截唔再遮住 offer，C4 offer 第一次經 UI 撳到。C2／C3／C5 仍然係 offer 唔見（sheet 無對應「播劇情：」掣）而行 force-start——內容＋done 旗本身驗到，offer 唔見嘅原因係 drive 嘅 stale-sheet／導航問題，見「附帶觀察」。

## Phase B — 關鍵閘：PASS（8 項全部如預期）

| 檢查 | 結果 |
|---|---|
| C18 day 300（1990-10-28 前）唔開 | `false` ✓ |
| C18 day 334（1990-12-01）開 | `true`，15 句，首句「1990 年冬，年尾。中環何生事務所，何生將你嗰份來年行程表推到你面前。」 ✓ |
| C11 無 C7 唔開 | `false` ✓ |
| C11 有 C7 開 | `true`，15 句，beat2「阿偉今日嚟做後台幫工，順便等一個企位機會。」 ✓ |
| C15 無 tag 唔開 | `false` ✓ |
| C15 有 tag 開 | `true`，11 句 ✓ |
| C17 day 1065（1992-12-01）無獎唔開 | `false` ✓ |
| C17 day 1065 有獎開 | `true` ✓ |
| C17 backstop day 1096（1993-01-01）無獎都開 | `true` ✓ |

## Phase C — 審計斷裂逐支驗：PASS（13 項全部如預期）

| 檢查 | 結果 |
|---|---|
| C16 播完＋`flag_vocal_train` 已寫 | `C16_done: true`、`C16_train_flag: true` ✓ |
| `ching_after_train` when() 真 | `true`（C16 done＋train 旗） ✓ |
| `ching_after_polish` when()（train 已揀，polish 互斥） | `false` ✓（正確：polish 未揀） |
| C9 調停旗 | `C9_mediate_flag: true` ✓ |
| `gu_loan` when()（1991＋tier≥2） | `true` ✓ |
| C14 未定旗 | `C14_undecided_flag: true` ✓ |
| `chai_repay` when()（tier≥2＋C14 done） | `true` ✓ |
| 人脈網靜態對照表 | `network_map_present: true` ✓ |
| 人脈網 live 旗（C2 揀留低） | `{stay: true, hustle: false}` ✓ |
| WF1 ECHO89 回響（3 行上限） | 3 句：「嗰日你講過想自己開公司——嗰粒種子，收科都仲喺度生根。」／「你揀咗穩打穩扎磨手藝嗰條路——三年行落嚟，你嘅戲，係咁磨出嚟嘅。」／「賭枱邊嗰晚，你企喺側邊睇足全程——睇人賭，學到嘅嘢多過自己落場賭。」（第 4 支 `gamble_quiet` 俾 ECHO89 3 行上限截咗，係設計原意） ✓ |
| C5 `flag_choi_honest` 寫入＋讀取 | `C5_choi_honest_written: true`、`C5_flag_choi_honest_read: true`（經 global `StoryOC.getFlag`） ✓ |

## Phase D — 程天諾真觸發：PASS

- 掃 day 973–1000（天星音樂）：day 973 無巧遇；**day 974 程天諾觸發**，overlay meta「巧遇 · 程天諾」，首句「喂，你哋睇住呀，我程天諾唔會一世靠部機㗎，遲早有一日，我唱live唱到全場企起身！」
- 10 句 after_train 對白已錄，包括修音／live／練唱內容：「人哋成日話我靠修音……最屈辱嗰下，係連我自己都知，佢哋講嘅，有一半係真㗎。」／「認咗嗰一半，先有機會練返另外嗰一半返嚟呀。」
- `when_live: true`；`seen_other: []`（run5 呢輪 day 973 無其他星；run2f 同一路徑 day 973 見過魏詠男——日種子出沒盤逐日唔同，唔係回歸）。
- 截圖 `ching_enc.png`（run5 覆寫 run2f 同名檔；內容同一觸發）。

## Phase E — F4／G4：PASS（run5 終於全通）

### F4（何生問：走定留，`F4_stay_mind`）
- Seed day **900**（1992-06-19，夏）。開事務所 sheet 11 個掣，見到卡「**何生有句說話想同你講**／收工時分，何生叫你坐低一陣——唔係講通告，係講去留。」（另有「未開放（1）」＝未到 12 月嘅 C17 offer）。
- 開門嗰陣撞正 enc79 攔截「**巧遇 · 魏詠男**」，清走 overlay 後 sheet 先 render（見「腳本修正」第 5 項）。
- 播 4 句：首句（旁白）「1992 年夏，黃昏收工時分。何生事務所對面街，移民顧問公司門口排住長龍，排到轉角。呢排茶餐廳同片場最常聽到嘅開場白，係『邊個邊個全家走咗』——講到好似講緊天氣咁。」；何生兩句（「太空人」／「你呢——你有冇諗過走？」）；阿偉一句。
- 3 個抉擇；揀 idx0「何生，我唔走。呢度先係我嘅地方。」→ **`flag_stay_mind: true`** ✓
- 截圖 `f4_mid.png`（新）。

### G4（阿媽煲咗湯，`G4_family_job`）
- Seed day 1065（1992-12-01，冬）。路徑：☰ 選單 → 手帳 → 人情頁 →「屋企有話同你講」卡 →「**返屋企講清楚**」掣（`home_hit: true`、`favor_tab: true`）。
- 播 4 句：首句（旁白）「1992 年年尾，阿偉返屋企食飯。阿媽煲咗老火湯，湯面浮住一層油，將碗湯推前少少——佢今晚有話要講，成餐飯都心不在焉。表叔喺銀行嗰邊，薦到一份文職，月月有糧出，年尾雙糧。佢想聽你親口講。」；阿媽兩句；阿偉一句。
- 2 個抉擇；揀 idx1「阿媽，我想繼續做落去。」→ **`flag_family_job_decline: true`** ✓
- 截圖 `g4_mid.png`（run3 已有，run5 覆寫）。
- 附帶：人情頁卡標題係寫死嘅「屋企有話同你講」，唔跟節點標題「阿媽煲咗湯」（NOTES §7.7 已知）。

## Phase F — C17 全程（fresh page，播完即結局）：PASS

- Seed：day 1065＋`S.story.done.C13 = true`＋`S.awardsFlags["1992/award_singho_tv"] = "done"`；`plain_start("C17")` → `gate_open: true`。
- 22 句（run5 計數；run2f 36／run3 23——`step_story` 逐字 reveal 嗰陣長句會重複計一次，係計數方式差異，內容相同：首句、抉擇、結局三跑一致）。
- 首句：「1992 年冬末，星河電視台會議室。冬台慶啱啱完，彩紙仲喺走廊掃唔切。何生將張流程表攤喺枱面，張子駿坐喺對面，阿偉坐喺中間。」
- 內容覆核：`meeting_room: true`（會議室場景）、`taiwan: true`（何生講台灣水緊嗰段有出現）。
- 2 個抉擇：「順其自然：照呢三年嘅路，行到邊度就邊度…」／「收山諗諗：接屋企嗰份穩陣工，唔再做呢行…」；揀「順其自然」→ **`S.ending410 = {career: "E0", eveKey: "natural"}`**，結局畫面「三年收科」E0 正文出現（「頒獎禮嗰晚，你坐喺中間嗰幾行——唔係最前，亦唔係最後…」）。
- 截圖 `c17_mid.png`、`c17_after_choice.png`。

## 截圖清單（`qa131/shots157/`，run5 覆寫同名檔）

| 檔 | 內容 |
|---|---|
| `c1_mid.png`、`c1_after.png` | C1 播放中／播完 |
| `c2_after.png`、`c3_after.png`、`c4_after.png`、`c5_after.png` | C2–C5 播完 |
| `c11_mid.png`、`c15_mid.png`、`c18_mid.png` | C11／C15／C18 播放中 |
| `ching_enc.png` | Phase D 程天諾巧遇 overlay |
| `f4_mid.png` | **新**：F4 播放中（run5） |
| `g4_mid.png` | G4 播放中（run3 首出，run5 覆寫） |
| `c17_mid.png`、`c17_after_choice.png` | C17 播放中／揀完「順其自然」後結局畫面 |

第一輪 9 張（c1–c5、c11、c15、c18）已由 run2 起同名覆寫——腳本設計如此，run2f／run3／run5 每次全跑都會覆寫；內容同一節點同一觸發，無遺失新證據。

## 腳本修正（只改 `qa131/drive157.py`，遊戲檔／NOTES／測試檔一概無掂）

1. **Phase C step 上限 12/14 → 24**（C16／C9／C14／C5）：live 重寫節點 beats 多過舊 pack，12 步未到抉擇屏就斷。
2. **IIFE-internal 探針 helpers**：主 script 係 IIFE（`index.html` L17），`enc87StoryFlag`／`enc83NodeDone`／`enc79TierOf`／`endingFlag410`／`ENC79_BEATS`／`endingInserts410` 全部唔係 global。加咗 `JS_D157_HELPERS`，經已暴露嘅 `window.S`／`window.StoryOC` 逐字複製函數體做 live 讀法（`__d157_flag`／`__d157_nodeDone`／`__d157_tier`／`__d157_year`／`__d157_echo89`），唔係新 seed 方法。`network_map_present` 改做 Python 靜態 grep＋live 旗讀法。
3. **Phase D 重寫**：掃 day 973–1000；用 overlay `.e79-meta`（「巧遇 · {名}」）認星，唔用 `.e79-name`（旁白句嗰陣係空，run2c 誤認魏詠男）；非目標巧遇經 `dismiss_encounter()` 清走，記入 `seen_other`。
4. **導航修正**：`open_location_ui` 先關 sheet 再開；文字掣唔得試 `#map-area-list button[data-loc]`；再唔得試 `.pin.<type>` click（`LOC_PIN`，agency 唯一）。`try_offer_in_sheet` 加 `story_prefix` 參數：主線只撳「播劇情：」開頭掣，F4 卡式掣先用 `#loc-sheet` 範圍子字串。教訓（run2d／2e 兩次）：「劇情」呢類通字／全頁子字串一定誤撳支線掣。
5. **Phase E 兩大修正（run3→run5）**：
   - **F4 seed 日改 881 → 900**：`CHOICE47_DEFS.F4_stay_mind` 閘係 1992-夏；`calendarSeason()` 月份制（6–8 月＝夏）。day 881＝1992-05-31 仍係春，卡唔出——run2f 就係咁輸；邊界係 day 882＝1992-06-01（`date -d` 核實）。probe_e／e3 實證 day 890／900 卡出、播到、落旗。
   - **G4 路徑改行手帳人情頁**：屋企唔係地圖地點（LOCS 無 home id，`index.html` L51732 註明「LOCS 現時冇屋企地點」），地圖撳「屋企」永遠唔會成功（run2f `home_hit: null` 就係咁嚟）。正確路徑：☰ 選單 → 手帳 → 人情頁（`#hgroup-favor`）→ `data-choice47="G4_family_job"` 卡「返屋企講清楚」。probe_e3 實證。
   - **enc79 攔截後清走 overlay**：`open_location_ui` 開門後若 `#enc79-overlay` 仲喺 DOM，清走佢等 sheet render——入場撞正有星在場（兼無主線待播壓住）會先彈全屏巧遇，sheet 要等巧遇完先出。run3 Phase E 就係咁輸：day 900 開事務所撞正魏詠男攔截，sheet 得返「返回地圖」（probe_e5 實證 `ovInDom: true`、sheet 空；反證 probe_e4 fresh 局 C1 未 done，主線壓住攔截，開門即見 sheet）。run5 證實：開事務所攔截「巧遇 · 魏詠男」，清走後 sheet 11 掣，F4 卡在列。
   - **Phase D 掃描傳 `dismiss_intercept=False`**：run4 教訓——開門即清 overlay 會令 D 喺讀 meta 之前清走程天諾攔截，D 永遠捉唔到目標（run4 掃到 979 已經錯過 ching＋陸柏言兩次攔截，要中途 kill）。D 自己讀完 meta 先 dismiss。
6. **Phase F 抉擇屏次序**：先睇 `choices` 再睇 `active`（抉擇屏行 `.sp-choices-layout`，`.dlg106-plate` 會消失，舊次序會未讀抉擇就當播完）。揀完加捉 `S.ending410`＋結局截圖。

## 附帶觀察（drive 層面，唔係遊戲 bug 定論）

- **C4 offer stale-sheet 問題**：probe_c4 證實 day 49、C1–C3 done 嗰陣 `StoryOC.listOpen` 有 C4（P1），即 C4 本身開得；但 drive 喺 run2c／2d／2e 嘅 sheet 入面見唔到佢。run5 因為攔截清走修正，C4 第一次經 UI 攞到 offer。建議之後跟進 UI 導航／sheet 重新 render 嘅可靠性，但唔阻 drive2 結論。
- **C2／C3／C5 仍然 via=force**：sheet 入面無對應「播劇情：」offer 掣。內容＋done 旗已驗到；offer 唔見嘅原因未完全查明（可能係同一類 stale-sheet／導航問題），留待跟進。
- **F4／G4 抉擇後 `dismiss_result` 嘅行為**：F4 揀完有 3 句 resultBeats 再出結果；drive 嘅 `dismiss_result` 撳「確定／繼續／返回地圖」清走，旗驗證無受影響。
- **行數計數波動**：`step_story` 逐字 reveal 令長句有機會重複計一次；C17 三跑分別係 36／23／22 句，首句／抉擇／結局完全一致，唔係內容回歸。

## 跑次紀錄

| 跑次 | 結果 |
|---|---|
| round 1（上一任整合員） | 死 Phase B（`awardsSetFlag` 唔係 global，已修） |
| run2 | 死 Phase C：`C16 無抉擇屏`（step 上限 12 太細） |
| run2b | 死 Phase C：`enc87StoryFlag is not defined`（IIFE） |
| run2c | EXIT=0，但 D 認錯星（魏詠男）、E 全 null、F 無抉擇記錄 |
| run2d／2e | 死 Phase A C5：全頁子字串誤撳支線掣 |
| run2f | EXIT=0，A/B/C/D/F PASS；**E 全 null**（F4 seed day 881 仍係春＋G4 行錯地圖路徑） |
| run3 | EXIT=0，A/B/C/D/F PASS；**E 半通**（G4 PASS，F4 sheet 得返「返回地圖」——enc79 攔截未清） |
| run4 | 中途 kill：攔截即清修正令 Phase D 捉唔到程天諾（掃到 979 已錯過兩次攔截） |
| **run5** | **EXIT=0，6 phase 全 PASS，0 pageerror，0 HTTP404** |

## 檔案

- 腳本：`qa131/drive157.py`（本輪唯一修改嘅檔）
- 日誌：`qa131/drive157.json`（run5）、`qa131/drive157_run2_crash.log`、`drive157_run2b_crash.log`、`drive157_run2c_partial.log`、`drive157_run2d_crash.log`、`drive157_run2e_crash.log`、`drive157_run4_partial.log`（run3 log 喺 `/tmp/drive157_run3.log`；run5 log 喺 `/tmp/drive157_run5.log`）
- 探針（/tmp，唔入 repo）：`probe_c4.py`、`probe_e.py`、`probe_e2.py`、`probe_e3.py`、`probe_e4.py`、`probe_e5.py`
- `NOTES_V20A157.md` §6 未改（等 parent 合併）。
- 工作副本 `git status` 入面 `index.html`／pack／測試檔嘅修改係 v157 本身嘅實作（整合員做嘅），唔係今輪 drive 改嘅。
