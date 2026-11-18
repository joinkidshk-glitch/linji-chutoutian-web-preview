# NOTES_V20A286_LOAD_YEAR_SYNC

## 問題（parent 2026-11-18 live Playwright 實測發現）
讀入 1991／1992 年存檔後，`GIGS` 仍然係 1990 年庫（111 張、`gigsYearActive=1990`），
要翻一日先變返當年庫。期間開通告板會見到舊年通告，當年通告（包括決戰通告
《霓虹夜影》gig_1991_film_102）唔上板。決戰本身（RIVAL_CFG、rivalry 開局）完全
正確，唔係 v285 嘅錯。

## 根因（live main 親查，行號以 main 983f707 計）
- `syncGigsForCalendarYear(force)`（index.html L13722）按 `dateObj().getFullYear()`
  由 `STORY_WIRE.gigsByYear[y]` 重建 GIGS；force=false 時已同步就 early return。
- Caller 得三處：L13765（previewJumpCalendarYear，QA 工具）、L14851（pack loader
  init——存檔未 load、dayIndex 仲係 0，所以 sync 去 1990）、L19659（advanceDay）。
- 讀檔入口 `contFromSlot(slot)`（L45678）入面完全冇 call sync：`S=loadFromSlot(n)`
  還原 dayIndex 之後，只做 fix-up（StoryOC.ensure、weekPlan scrub、syncDualTracks
  L45702、ensureEntryTierBoardFill L45704），然後就去地圖／planner。板可以喺翻日
  之前就開到，所以見到舊年庫。

## 修法（最小改動，兩處）
1. `contFromSlot`：`syncDualTracks(S);`（L45702）之後、`atLoc=null;` 之後、
   `ensureEntryTierBoardFill()`（L45704）之前，加 guarded call（風格跟 advanceDay
   L19659）：
   `try{ if(typeof syncGigsForCalendarYear==="function") syncGigsForCalendarYear(false); }catch(_e){}`
   - force=false：1990 年存檔早已同步，early return，零行為改變。
   - 順序唔可以調轉：sync 會成個 GIGS 重建，y≠1990 時唔再 merge 入門池；
     放喺 ensureEntryTierBoardFill 之後會洗走啱啱注入嘅入門通告。
   - 呢個位置喺所有 early-return 分支（ending78Locked、week105 結算、softSeed、
     homeEditable）之前，所以全部讀檔路徑都受惠。
2. `maybeApplySoftSeed`：`applySoftSeedState(seed)` 之後、`presentSoftSeed(res)` 之前
   補同一 guarded call。`applySoftSeedState` 會改 `S.dayIndex = (week-1)*7`
   （L14292），而 `presentSoftSeed` 會直開地圖甚至直開地點（openLoc），唔補就會
   攞住舊年庫開板。softSeed 係 QA 專用路徑，真玩家唔行，但一併修好求一致。

## 唔改嘅嘢
- RIVAL_CFG／rivalry／film_102／film_109 接駁一概唔郁。
- SAVE key（starVolunteer_map_v19w）、softRev、產品 `?v=` 唔郁。
- 1990 年行為零改變（early return）。

## 測試
- 新 `tests/test_r286_load_year_sync.js`，13 項全過：
  - A1–A5 靜態：兩個 sync 呼叫喺正確位置＋順序＋guarded。
  - B1 庫 counts 111／99／79，共 289。
  - B2 dateObj：dayIndex 651→1991、1000→1992、100→1990。
  - B3–B5 1991 load：sync 後 GIGS 99 張、yearActive 1991、含 film_102、冇 1990 通告；
    film_102 內容啱（《霓虹夜影》男主角／秋／film_harbour／pay [4416,5184]／
    req 演技 130 體能 90）；sync 唔 call mergeEntryGigsIntoPool。
  - B6 1992 load：79 張、yearActive 1992、含 film_114《海角歸人》。
  - B7 1990 load no-op：同一陣列、長度不變、入門 marker 仲喺度、唔 call mergeEntry。
  - B8 已同步 1991：early return，同一陣列。
- 舊 `tests/test_r285_rival_cfg.js` 12 項全過（零回歸）。

## 釘行 resync（v286 插入 9 行引致，2026-11-18）
- 兩處插入共 +9 行（softSeed sync＋3＠舊 L14392 之後、contFromSlot sync＋6＠舊
  L45704 之後），令 9 個釘行靜態測試 fail：gift185、kwan151、rom159、rom176、
  tang152、tang171、tang173、text125、travel114。
- 驗證方法：9 個測試喺 pristine main 983f707 全部 PASS、喺工作副本全部 FAIL，
  證明係今版插入引致，唔係 flaky；逐粒釘行用舊檔內容對位新檔內容，全部逐字
  相同，純漂移（84 粒 pins＋tang152 3 粒 0-based index，mismatch 0）。
- Resync 規則：舊行 ＜14392 唔郁、14392–45703 各 ＋3、≥45704 各 ＋9；總行數
  46301→46310。逐檔更新（詳見各測試檔頭 `# v20a286 resync` 註解；ok() 名入面
  嘅 L 號係歷史標籤，唔郁）：
  - gift185：總行數 46301→46310（鏈尾 ＋v286 +9）。
  - kwan151：B2 14427→14430、N3 14461→14464、N4 14426→14429、B3／B4／B5
    14545→14548、N5 14554→14557。
  - rom159：25204→25207、26038→26041、14815→14818、25953→25956、全佳
    25232→25235。
  - rom176：14813→14816、39859→39862、40217→40220、41434→41437、41590→41593。
  - tang152：lines()[14740]→[14743]、lines()[14867]→[14870]。
  - tang171／tang173：總行數 46301→46310（鏈尾 ＋v286 +9）、openLoc DEF
    41549→41552（鏈尾 ＋v286 +3）、guard 41555→41558／lines[41548]→[41551]。
  - text125：16472→16475。
  - travel114：COUNT 12 處＋FREE 29 處（≥14392 者）各 ＋3、DEF 41549→41552、
    WRAPPER 28782→28785。
- Resync 後 9 個測試逐個直接跑全部 PASS；新 r286 測試 13 項、r285 測試 12 項
  亦全過。Resync 腳本留喺 /tmp/resync286.py（tmpfs，唔入 repo）。

## 全套 suite
- 第一跑（resync 前）：TOTAL PASS 341 FAIL 18——9 項基線 FAIL 照舊＋9 項釘行
  FAIL（上節）。第二跑（resync 後，待填）。

## 落地
- （待填：main commit、Pages 核實）
