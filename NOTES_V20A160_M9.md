# NOTES — v20a160 M9 頒獎禮贏分支音效（fanfare＋掌聲）

- 分支：`v20a160-m9`（工作副本 `~/workspace/linji-work160-m9`，基底 main `e08a070`＝v148）
- 狀態：code＋新測試＋實駕進行中（見 §7／§8）
- 範圍：**只做 M9**（M6／M4／M1／M5 唔掂，嗰啲係其他 v160 工人嘅票）。音頻範圍嚴格限於頒獎禮贏分支；
  全套 BGM／聲效工作仍然等用戶開工信號，冇擴大、冇加其他音效、冇加開關 UI。
- 唔開 PR、唔推 main（落地由統籌做）。SAVE key／softRev／`?v=` 一律無郁；無直改 content pack JSON。
- index.html：58,904 → **58,945 行（＋41 行）**（M9 helper 插入 41 行；reveal 觸發行 1 行換 1 行，行數不變）

## 1. 資產（用戶 2026-11-13 07:15 試聽後揀咗 take 1）

| 檔 | 來源 | 入 repo 位置 | 大細 | 校驗 |
|---|---|---|---|---|
| fanfare take 1 | `~/workspace/linji-work147/samples147/m9_fanfare_take1.mp3`（song `7b828b44-9c8e-4756-832d-e46746a26164`，19.92s，120 BPM，純音樂） | `assets/audio/awards_fanfare.mp3` | 462,979 bytes | sha256 `442b2676a15606177ddda4c42e5ccc6ce85938a57abff4bec13d74e7cbdfb040`；ffprobe 19.944s／48kHz stereo；ffmpeg 全檔解碼零錯誤 |
| 掌聲 | `~/workspace/linji-work147/samples147/m9_applause.wav`（clip `4f116190-1a37-4177-a231-f84b5d70843d`，3.16s，16-bit stereo 44.1kHz WAV） | `assets/audio/awards_applause.mp3` | 74,973 bytes | 見 §2 |

- **take 2（`m9_fanfare_take2.mp3`，song `654e1434-701b-4fa5-8f0c-74dcd7f90adc`，19.88s）唔用，唔准入 repo**——
  新測試三重堵（assets/ 冇 take2 檔、index.html 冇 `take2` 字串、入 repo 嗰隻 fanfare sha256 唔係 take2 嗰隻
  `25e691cf…`）。
- 唔准新生成：兩隻聲都係 samples147 現成樣本，零生成成本。
- 位置決定：**新目錄 `assets/audio/`**（遊戲暫時冇音頻目錄；`assets/fx/` 係 mp4 像素動畫，唔係聲軌，放埋一齊會混淆）。
  檔名望落知係咩：`awards_fanfare.mp3`／`awards_applause.mp3`。

## 2. 掌聲 WAV → MP3 轉換決定

- 工具：系統 `ffmpeg` 8.1.2（`/usr/bin/ffmpeg`，現成有，唔使裝）。
- 指令：`ffmpeg -i m9_applause.wav -codec:a libmp3lame -q:a 2 assets/audio/awards_applause.mp3`
  （VBR 約 190kbps；fanfare 保持 MP3 原樣，冇重編）。
- 結果：557,134 → **74,973 bytes（慳 86.5%）**；時長完全一致 **3.157914s**；44.1kHz stereo 不變。
- 音質檢查（客觀，未經人耳試聽）：兩檔 `volumedetect` 完全一致——mean_volume −25.9 dB、max_volume −8.6 dB；
  ffmpeg 全檔解碼零錯誤；MP3 頭係 ID3（唔係 RIFF，證明唔係 WAV 原檔扮 MP3）。
- 原 WAV 留喺 samples147（唔入 repo），需要無損版嗰陣返去攞。

## 3. 落點＋時序（code 位置，main e08a070 行號 → 工作版行號）

- 現況：index.html 之前完全冇現成 audio 機制（`new Audio`／`<audio` 係 0 結果；"Audio" 全檔只出現 2 次——
  設定頁 prefs 註解同埋 `playSightChime()` 嘅 WebAudio oscillator 雙音 chime，兩者都同頒獎無關，唔郁）。
- 新 helper `awards160PlayWinAudio()`（工作版約 L46158，`awards62PlayCeremony` 正前面）：
  典禮專用、最小——按需要先建 `Audio` 元素，唔經全域 BGM／SFX 系統，唔加開關 UI。
  常數：`AWARDS160_FANFARE_SRC`／`AWARDS160_APPLAUSE_SRC`／`AWARDS160_APPLAUSE_DELAY_MS = 900`。
- 觸發點（唯一）：`awards62PlayCeremony` 入面 `advance()` 嗰行（工作版約 L46485）——
  `if(beats[beatIdx].id === "reveal" && best === "won"){ spawnConfetti(); try{ awards160PlayWinAudio(); }catch(_e){} }`。
  揀呢度嘅原因：`advance()` 單向行 beat，reveal 係單一 beat，跳過掣行 `finish()` 唔經 `advance()`——
  所以每場贏典禮只會觸發一次；撳畫面快進跳到 reveal 都一樣只觸發一次；gallery／nominated 嘅 reveal 唔係 `won`，
  行唔到呢行。
- 時序決定：**揭曉嗰刻 fanfare 起；掌聲 900ms 後疊上去**（觀眾歡呼跟住音樂起），兩條聲軌重疊播。
  fanfare 約 20 秒，會播過典禮完結（結果卡嗰陣仲響緊）——Audio 物件唔掛喺舞台 DOM，舞台拆走唔影響播放；
  跳過掣唔停音（揭曉前跳過就根本未播，見 §8 won_skip 對照）。
- 靜音：fanfare 跟 `prefs.bgmMuted`、掌聲跟 `prefs.sfxMuted`；音量跟 `prefs.volume`（預設 70 → 0.70）。
  設定頁「音效／音樂」行而家未開掣（v20a105 UI105 S-48：「即將推出」），兩者預設都係 false——
  即係而家預設會播；BGM 包接線嗰陣呢度自動跟埋，唔使再改。**冇加任何新開關 UI**（範圍紀律）。
- QA 鉤：`window.__awards160Audio`＝`{ fanfare, applause }`，每邊 `idle → attempted → playing／blocked／muted／error`。
  實駕用嚟證實觸發有發生（見 §8）。

## 4. 瀏覽器自動播放政策（限制，寫死喺 code 註解＋呢度）

- 揭曉係計時器（rAF loop）觸發，未必喺用戶手勢入面，`play()` 有機會被瀏覽器拒絕。
- 處理：`play()` 回傳嘅 promise 一律 `.then(playing)／.catch(blocked)`，**靜默失敗，絕對唔可以令典禮流程報錯／停低**；
  helper 本身全程 try/catch，呼叫點再包多一層 try/catch。
- 實情：玩家係撳「出席」入場（用戶手勢，sticky activation），揭曉喺 ~6.75 秒之後，Chrome 嗰套一般會放行；
  但唔靠呢個假設——拒絕嗰陣只係冇聲，典禮照行。

## 5. headless 實駕限制（限制，寫死喺 code 註解＋呢度）

- **headless 未必出到聲**——實駕驗「冇 pageerror＋觸發邏輯＋mp3 真係有經網絡攞」，唔扮驗到聲。
  旗標 `playing`／`blocked` 只作觀察記錄；`attempted` 先係觸發證明。
- 人耳試聽：fanfare take 1 用戶已試聽揀咗（07:15）；掌聲 WAV→MP3 轉換只做咗客觀對照（§2），
  未經人耳試聽——最終上線前建議用戶實機聽一次揭曉嗰段。

## 6. 測試

- 新測試 `tests/test_awards160_m9_static.py`：**34 項，工作版 34/34 ALL PASS**。
  斷言：take 1 入 repo（sha256＋大細）／掌聲係 MP3（ID3 頭、唔係 RIFF、<200KB）／take 2 三重堵／
  helper 在位（`new Audio`、`.catch`、跟 `bgmMuted`／`sfxMuted`、讀 `volume`、900ms 延遲、QA 旗標）／
  觸發只此一處（定義＋呼叫各 1 次、喺 `awards62PlayCeremony` 入面、reveal＋won 同 `spawnConfetti()` 一行、
  包 try/catch）／全檔 `new Audio` 只得一個／兩條音源常數各只用一次／QA 旗標只喺 M9 區塊出現／
  SAVE key／softRev `s107`／`version:"v20a10"` 不變。
- **反證**：同一測試對 pristine main（`e08a070`，`~/workspace/pristine160-m9/index.html`）——
  **29 項 FAIL、exit 1、冇 crash**（見 `qa160-m9/test_pristine.txt`；工作版結果見 `qa160-m9/test_work.txt`）。
  Pristine 嗰 6 項 PASS 係空泛通過（SAVE key／softRev／version 本來就啱、冇 take2 檔／字串、fanfare sha 唔係 take2
  因為根本冇檔）——檔案整體 FAIL，先係反證成立嘅證據。
- 全套 A/B（入口 `qa131/run_suite.sh`）：
  - 開工基線（乾淨工作副本，開工嗰陣核實）：**211 PASS／12 FAIL**。
    （任務書寫 210／12 係舊數——210 係 v146 數字；v148 落地後 main 已經係 211／12，v156 NOTES 亦確認基線係 211。）
    12 項 FAIL 全部係 pre-existing（flash51／giglib36／pacing35／poster59／rumor49／slot50／
    soft_tip_111_restore／start53／weave43／weave44／weave49／wrap38），見 `qa160-m9/suite_baseline.txt`。
  - 工作版第一輪：**176 PASS／48 FAIL**——唔係回歸，係已知波動（v151 教訓，已入 AGENTS.md：
    同一 repo 連續跑出 211/12、137/86、200/23，失敗項每次唔同、全部係 .py，逐個直接跑全部 PASS）。
    今輪 48 項入面 12 項係穩定 pre-existing，其餘 36 項全部係 .py；逐個直接重跑：**34 項 PASS**，
    剩低 2 項係真係我改動引起嘅行號／字串漂移（見 §7，已修）。
  - 工作版第二輪（修復後）：**173 PASS／51 FAIL**——同樣係波動（全部 51 項都係 .py，零 .js FAIL；
    相關測試 travel114／ui105／awards160／awards62／awards63／awards64／fix65／venue99 全部喺套內直接 PASS，
    我嘅新測試亦喺套內 PASS）。12 項穩定 pre-existing 全部在列；其餘 39 項逐個直接重跑**全部 PASS**。
    另加頒獎家族＋受影響測試直接覆驗 12 檔全部 PASS——合共 **51 PASS／0 FAIL**，見 `qa160-m9/direct_rerun2.txt`。
  - **結論：真實狀態 212 PASS／12 FAIL（基線 211／12 ＋新測試 1 檔），零回歸。**
    套內總數 176/48、173/51 兩次都係 .py 波動假象，按 v151 做法以直接覆驗為準。

## 7. 修復：兩項真漂移（第一輪全套捉到，唔係波動）

### 7.1 `tests/test_ui105_static.py` —— 我嘅 helper 註解撞咗「即將推出」唯一性

- ui105 斷言設定頁「即將推出」全檔只出現一次；我 helper 註解寫咗「設定頁『音效／音樂』行而家係『即將推出』」，
  變咗兩次。
- 修法：註解改做「設定頁『音效／音樂』行而家未開掣」（行數不變；新測試檔註解同步改寫）。
  之後 ui105 直接跑 **ALL PASS**。

### 7.2 `tests/test_travel114_static.py` —— M9 helper 插入令釘行漂移 ＋41

- travel114 硬釘 openLoc 呼叫點行號；M9 helper 喺 L46143 插入 41 行，插入點之後嘅釘全部漂移。
- 修法：`qa160-m9/resync_travel114_160.py`（difflib 對位 pristine e08a070 → 工作版）核實純漂移——
  唯一改動係 insert 段（舊 46143 → 新 46143–46183）＋ trigger 行 1 換 1；44 個 openLoc 呼叫點序列逐字一致；
  COUNT 13／FREE 27 內容逐行相同。之後更新釘行：COUNT 5 處 ＋41（57592→57633、57759→57800、
  57902→57943、57923→57964、58373→58414）、FREE 15 處 ＋41（52437→52478、52556→52597、
  53449→53490、53831→53872、53853→53894、53988→54029、55625→55666、57036→57077、
  57369→57410、57487→57528、57488→57529、57523→57564、57524→57565、57543→57584、
  57558→57599）、DEF 53562→**53603**、WRAPPER 44171 不變（插入點在其後）；測試檔加咗 resync 歷史註解行。
  之後 travel114 直接跑 **RESULT PASS**。

## 8. 實駕（Playwright，`qa160-m9/drive160.py`，port 8982——8972 已讓俾 M6，見下）

- 腳本沿用 `qa147/drive147.py` 模式（新遊戲 → 地圖 → `window.__awards.debugForceSeasonWindow` 強制典禮 →
  UI 撳「出席」；播種直接寫 live `S`＋localStorage，唔經 `saveQ`）。
- 贏分支種子：fame 200／stage 60／acting 60／`industryCreditDelta` 100（雙軌拉滿：
  `dualTrackNumbers` 計 stageVolume＝fame＝200、industryCredit＝230，兩軌 normPrimary 都係 1.0）＋
  1991 年 4 部電影擔正（`roleScale: film_lead_big`，q＝1.00）＋2 部電視劇擔正（跨桶借分 repPower 0.08）——
  base＝0.40×1＋0.42×1＋0.08＝**0.90**；taste ±0.05 → 單類別贏率 75%，兩類別 ~94%／次；
  `force_won` 重骰最多 6 次直至 `bestOutcome==="won"`（重試前撳「推辭」——唔可以用 dismiss_once，
  請柬第一個掣係「出席」；`debugForceSeasonWindow` 下次會清 flag 再排隊，所以推辭後重 force 安全）。
- Cases（全部 430×932）：
  - `won_932`：**PASS（16/16）**——強制 film won（兩類別都贏，score 0.904／0.888，force 1 次就中）→ 出席 →
    reveal caption「得獎！影壇新面孔（臨記組）」t=6367；**fanfare 同一個 poll 內 attempted（t=6367）**；
    掌聲 t=7007 attempted（觀測差 640ms，900ms 規格＋輪詢粒度，見下面 verify）；兩者 t=7280 已係 `playing`；
    兩隻 mp3 都有經網絡攞（transferSize 463,279／75,273 bytes＝成隻檔）；典禮總長 10,369ms；
    結果卡有「得獎」＋同屆提名；**0 pageerror**。
  - `won_skip_932`：**PASS（7/7）**——強制 won → 出席 → 揭曉前（~1s）撳「跳過 ⏩」→
    旗標維持未觸發（`finalFlag: null`），結果卡照出（證明只係揭曉觸發）。
  - `gallery_932`：**PASS（8/8）**——強制 gallery → 出席 → 睇完整場（總長 9,356ms，6 beats 唱名＋揭曉廖炳星）→
    旗標維持未觸發、**零 audio 資源請求**（證明只限贏分支）。
- **OVERALL 3/3 PASS**（`qa160-m9/drive160.json`＋`qa160-m9/shots/`；第一輪 00:06 已經 3/3，之後因 port 事故重跑一次，
  見下——兩輪數字一致）。
- 時序驗證（`qa160-m9/verify_timing.py`，`verify_timing.json`）：**PASS（8/8）**——單次原子 evaluate 同時讀
  caption＋旗標＋`performance.now()`，消除兩次 evaluate 之間嘅 skew：
  reveal caption 同 fanfare attempt **同一個 performance.now() 時間戳（36769）**——同一個 `advance()` 入面發生，
  唔係早一個 beat；掌聲 37869（觀測差 1100ms；真值＝fanfare＋900ms setTimeout，觀測差包含輪詢 lag，
  同 drive160 嗰 640ms 一樣係「首次見到」嘅粒度，唔係規格偏差）；兩者最終 `playing`；0 pageerror。
- 實駕限制（重申）：旗標 `playing` 係指 `play()` promise resolve 咗＋mp3 成隻攞咗——headless 未必出到聲，
  **唔扮驗到聲**。人耳試聽留待用戶實機（§10）。
- **Port 佔用事故（實駕教訓，已修，唔係 game code 問題）**：中途有一次 verify run 播足成場贏典禮但旗標永遠唔郁——
  查實係 port 8972 俾 M6 兄弟工人嘅 server 佔咗（`linji-work160-m6`，pid 94145，00:15:56 起），我哋嗰邊 bind 失敗
  （Popen stderr 去咗 DEVNULL，靜默無聲），browser 載咗佢哋嗰份 index.html——game 照玩、典禮照贏，但完全冇 M9 code。
  附帶捉到兩個 harness 漏：① `run_once()` 入面 `check_served()` 喺 try／finally 出面，失敗嗰陣 server 漏咗唔死
  （8982 漏過一隻，pid 96297，已手動殺咗）；②「新遊戲」click 等 navigation 喺負載大嗰陣超過 5s。
  修法：port 改 **8982**（未佔用）＋開 browser 之前 `check_served()` 驗派緊嗰份有齊三個 M9 標記（重試 15 次，server 起身慢都得）＋
  `stop_server()`（terminate→wait 5s→kill 兜底）＋check 入 try／finally＋「新遊戲」click timeout 5s→30s。
  修好之後 verify＋drive160 全數一次過 PASS，8982 跑完乾淨（無殘留 listener）。**唔好再用 8972**（M6 嗰邊仲用緊）。

## 9. 檔案

- 改動：`index.html`（＋41 行）；`tests/test_travel114_static.py`（釘行 resync＋歷史註解，§7.2）。
- 新增：`assets/audio/awards_fanfare.mp3`、`assets/audio/awards_applause.mp3`、
  `tests/test_awards160_m9_static.py`、`qa160-m9/drive160.py`、`qa160-m9/verify_timing.py`、
  `qa160-m9/resync_travel114_160.py`、`NOTES_V20A160_M9.md`（本檔）。
- 證據：`qa160-m9/test_work.txt`（新測試工作版 34/34）、`qa160-m9/test_pristine.txt`（反證 29 FAIL）、
  `qa160-m9/suite_baseline.txt`（基線 211/12）、`qa160-m9/suite_work.txt`（工作版第一輪 176/48，波動＋2 真漂移）、
  `qa160-m9/suite_work2.txt`（工作版第二輪 173/51，全係 flaky .py，逐個直接覆驗 51/0）、`qa160-m9/direct_rerun2.txt`、
  `qa160-m9/drive160.json`＋`qa160-m9/shots/`（5 張，實駕 3/3 PASS）、`qa160-m9/verify_timing.json`（時序驗證 8/8 PASS）。
- Scratch（唔入 commit）：`~/workspace/pristine160-m9/index.html`（e08a070 抽出嚟做反證／resync 對照）。

## 10. 未解決事項

- 掌聲 MP3 轉換未經人耳試聽（只做咗客觀對照，§2）；fanfare take 1 用戶已試聽。最終上線前建議用戶實機聽一次揭曉嗰段。
- 主分支喺我開工期間郁咗：v156（main `9c850f9`）＋v151（main `86e391d`）已落地；本分支基底仍然係 e08a070（v148）。
  落地嗰陣統籌要 rebase——留意 `tests/test_travel114_static.py` 釘行係跟本分支行號 resync 過，rebase 後可能要再 resync 一次。
- 全套 suite 數字會波動（v151 教訓）：判斷回歸要睇「12 項穩定 FAIL＋相關測試逐個直接覆驗」，唔好齋信一次總數。
