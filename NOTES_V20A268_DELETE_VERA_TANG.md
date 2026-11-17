# NOTES_V20A268 — 角色刪除實裝（Vera／鄧麗萍死檔／死條目／死引用）

基底 main `491958a`（v267）。分支 `v20a268`。工作副本 `~/workspace/linji-work268`。
範圍：只刪已確認死嘅檔／條目／引用；唔改任何 live 行為（唔改數值、唔改流程、唔改其他角色）。
刪完遊戲行為同刪之前一模一樣（除咗死檔唔見咗）。SAVE key／softRev／?v= 唔郁。

## 一、刪咗乜（逐項＋零引用證據）

### A. 檔案刪除（11 檔，`git rm`）

| 檔 | 零引用證據 |
|---|---|
| `content/story_detail_romance_tang.json` | v152 已停載（loader 零 `get("…")`）；唯一讀取位係測試 fixture（test_contra98_logic.js 讀佢做 CONTRA98 數據來源——見 B 項，同步清走）。DengLine 排片線行 mock（`MOCK_STORY_DENG_LINE_*`），唔讀呢個檔。 |
| `assets/story/core/vera_bust_default.png`／`vera_bust_smile.png`／`vera_bust_frown.png` | `spBustCandidates` 動態砌檔名，Vera 節點已死（meet playerOffer:false，後續節點旗永遠寫唔到），live 永遠唔會砌出呢啲路徑；index.html＋content 零檔名命中。 |
| `assets/story/core/vera_silhouette_far.png` | `coreSilhouetteFarSrc` 動態砌檔名；live 遠觀 `STAR_SIGHTINGS` 只有 10 星，無 vera。 |
| `assets/story/fullbody/vera_base.webp`／`vera_smile.webp`／`vera_serious.webp`／`vera_angry.webp` | `dlg106Candidates` 動態砌檔名；Vera 感情線節點已死，live 對話永遠唔會播到 Vera 句（live JSON 入面 Vera 講者句只喺死節點）。 |
| `assets/npc_vera.jpg`／`assets/dialog/npc_vera.jpg` | index.html 零 `npc_vera.jpg` 命中（`PORTRAITS.npc_vera` 係 base64 內嵌，唔係檔案，留返）。 |

### B. `index.html` 條目刪除（45544 → 45308 行，淨 −236）

| 位置 | 刪除內容 | 零引用證據 |
|---|---|---|
| `ROMANCE_WF2_OVERRIDES`（舊 L6897–L7129） | R_vera_* 5 條覆寫（−233 行） | JSON 節點已刪；覆寫表合併視圖 SRC 唔再命中 vera 節點（test_wf2_81_logic.js apply 命中 10→5，淨 lan）。 |
| `STORY_MEET_SOFT`（舊 L7806） | `R_vera_meet: { npc: "stylist", … }` 一行 | meet playerOffer:false，`openMeetOffer` 永不寫入 offers。 |
| `STORY_SCENE_OVERRIDE154`（舊 L11240） | `"R_vera_meet":"bg_loc_tvb_longmen",` 一行 | 節點已死，覆寫永不命中。 |
| `CONTRA98_WHEN_FIX`（舊 L14908／L14914） | `R_vera_ending`／`R_vera_crisis` 兩段（行內段刪，0 行） | 節點數據已唔存在；fixer 輸入從來只係 [main, rom1, rom2, rom3, rival]。winter_finale 計數 8→7。 |
| `CONTRA98_WHEN_FIX`（舊 L14684） | `R_tang_push2`／`R_tang_crisis` 一行（−1 行） | 節點數據只喺已刪嘅 romance_tang.json；fixer 輸入從來唔包呢個 pack，兩行係死項（v152 起已經係 no-op）。FIX98 計數 25→21（冬 11→10／秋 14→11）。 |

另：3 處 tang 檔名註解改字（舊 L6728／L8251／L15024），唔再提 `story_detail_romance_tang.json`；`story_detail_romance_tang.json` 喺 index.html 殘留 0。

### C. `content/story_detail_romance_vera_hiu_choi.json`（手術式文字編輯，唔 reflow）

- 刪 5 個 R_vera_* 節點（brace matching 逐個刪），nodes 15→10（淨低 R_hiu_*／R_choi_* 各 5 條）。
- Metadata：version `1.3.1`→`1.3.2`；source／romanceLines／qa.models／頂層 models／qa.lines 去 vera；`qa.node_count` 15→10；`nodesWithOC` 15→10；softHoldCleared 去 Vera 項；刪 `pcSilent_vera`（連前逗號）；finish_reasons 去 vera；edits 兩處去 Vera／R_vera＋加 v1.3.2 條目（寫法避開 vera 字串）。
- 驗證：`json.loads` 通過；檔內 `vera`／`Vera` 零殘留（case-insensitive）；git diff 9 insertions／472 deletions。

## 二、決定唔刪（連原因）

- **NPCS `stylist`（Vera 造型師）＋`mei`（關海媚）**：live。stylist 係地圖 NPC（傾談／送禮／探病、ENDING410_NPC_NAMES、MAP_NPC_TO_KEY）；mei 係巧遇角色，N10 完成後解鎖（`rom176MeiUnlocked()`）。v159 註解明言「NPCS mei／vera 條目留返，唔喺呢度刪」。
- **`gift_prefs.json` vera 條目**：live。stylist 送禮經 `mapNpcId:"stylist"`＋`gift_met_stylist`／`gift_talked_stylist` 旗，唔靠死咗嘅 `flag_vera_met_*`。
- **`gift_prefs.json` tang 條目**：live（v152 刻意保留）。DengLine 排片線（meet＋push1／push2／crisis，閘門 `flag_tang_open ∧ rel_tang≥2`）仍然行緊。
- **SP176 `mei` 條目**：live。SP176 覆寫表套入 `GIFT_PREFS.npcs`，mei 巧遇解鎖後可送禮。
- **`tang_laiping_*` 全部圖片**：live。鄧麗萍喺 `story_detail_romance_lan_xu.json` 講 3 句（R_lan_* 節點）；`SP_CORE_STEM`＋`DLG106_GAZE`＋`CORE_SIL_FAR_IDS` 都有佢，bust／fullbody 經動態探測到。
- **`kwan_hoimei_base.webp`＋`kwan_hoimei_serious.webp`**：live。base 經 `PORTRAITS.npc_mei`；serious 經巧遇對話 `dlg106Candidates("kwan_hoimei")` 可達。
- **結局／舊檔讀取位**：`endingDual410`／`commit48` 嘅 vera 行（新 L12652／L25188，`vera: line("R_vera_meet", "rel_vera", "R_vera_crisis", "flag_vera_commit")`）、`BR89_HEBE_FLAGS` 嘅 `flag_vera_he`／`be`、`TEXTFIX55_NOTE_EXACT` vera 條目、`relMap` 嘅 `rel_vera`、L14213 `flag_vera_t5`／`flag_vera_push` 檢查、`test_weave48_static.py:89` 嘅 rel 鍵——全部讀舊存檔狀態，刪咗會改舊檔行為，所以保留。
- **註冊表／Gaze／剪影登記**：`SP_SPEAKER_REG` vera、`SP_CORE_STEM` vera、`DLG106_GAZE` vera、`CORE_SIL_FAR_IDS`＋`CORE_SIL_SIGHT` vera、`PORTRAITS.npc_vera`（base64 內嵌，唔係檔案）——保留。`__phase3.check` 自檢斷言 `coreSilhouetteFarSrc("vera")` 回傳字串，刪登記會整爛自檢；檔案本身死，所以只刪檔唔刪登記。
- **`assets/story/core/MANIFEST.md`**：2026-11-05 歷史文件，vera 行已過時但無測試讀佢，唔郁。
- **`tests/fixtures/story_detail_romance_vera_hiu_choi.json`＋`tests/fixtures/romance_wf2_v80.json`**：凍結測試副本，`test_weave48_logic.js`／`test_weave410_logic.js`／`test_wf2_81_logic.js` 用佢哋測舊檔 vera「almost」路徑（嗰條路保留緊），唔郁。
- **WF2 覆寫表以外嘅 Vera 註解**（L5367 闊度註解、L25431–25483 ROM159 註解、L13272–13282、L39183–39197 等）：歷史說明，保留。
- **`tang` 字串誤傷警告**：`test_tang152`／`test_tang171`／`test_tang173` 等測試檔名嘅 `tang` 唔係鄧麗萍；`mei` 會撞現役新星 `wu_meilam`（胡美琳，絕對唔好刪）同 `kwan_hoimei`。

## 三、已知殘留（刻意，唔係漏網）

- `story_detail_romance_tang.json` 檔名喺已載入 JSON 入面仲有 6 處 metadata 字串（唔係載入路徑，loader 永遠唔會讀）：
  `story_detail_n1_to_n17.json` 嘅 `alignedWith`；`story_detail_romance_lan_xu.json` 嘅 `supersededByFile`／`notes_tang`／`rule`；
  兩份 DengLine mock 嘅 `oldRomanceRef`。另有兩份 doc（`content/PLAYER_OFFER_MEET_v1.md`、`content/QA_WIRING_STORY_PLAY_v1.md`）提及。
  新測試 `test_delete268_static.py` §7 釘死：檔名只准出現喺呢啲 metadata 欄位。
- `R_vera_` 喺 index.html 殘留 3 命中：WF2 表頭註解 1 次（刻意註明已刪）＋結局舊檔讀取行 2 次（見上）。
- `test_contra98_logic.js` B-01 合成節點測試（`prep98({ id: 'R_vera_ending', choices: []}) === null`）保留——測 prep 函數邏輯，唔依賴 pack 數據。
- `tests/audit_wf5.js`（唔喺 suite 入面）`loadPack` 遇缺檔回 null，刪 tang 檔唔會整爛佢。

## 四、測試更新（resync：`qa268/resync268.py`，difflib 對位逐行核實純漂移）

- `tests/test_tang152_static.py`：§6 改寫（tang 檔已刪，唔再斷言存在）；winter_finale 8→7；3 個釘行（HELD 9521→9287、normaliseTangStub152 14975→14739、stub 呼叫行 15102→14866）。
- `tests/test_wf2_81_logic.js`：刪 `LINES.vera`；覆寫表計數 10→5；合併視圖 25→20；`HALF_END` 刪 `R_vera_ending`；`ENDKW` 刪 `R_vera_ending`；beats≥200 迴圈改淨 xu；apply 命中 10→5；fixture regex 窄化做 hiu|choi。
- `tests/test_wf2_81_static.py`：WF2 斷言改做 lan 5 條在位＋`'"R_vera_meet": {'` 唔喺區內；覆寫表字節量 >15KB→>7KB（實 8378）。
- `tests/test_contra98_logic.js`：`PACK_FILES` 刪 tang 檔；`FIX98` 25→21（冬 11→10／秋 14→11）；「四個支線 pack」→「三個」；`overYear` 豁免刪 `R_tang_ending` 一項（數據來源已無）；B-01 合成節點測試保留。
- `tests/test_contra98_static.py`：FIX98 25→21；winter_finale 8→7；B-02 兩句 Vera 覆寫文案斷言改做「已隨節點刪除」。
- `tests/test_expr154_static.py`：R_vera_meet 場景覆寫斷言改做斷言唔存在；R_hiu_ending 保留。
- `tests/test_dlg138_static.py`：NEW 表刪 `vera_serious.webp` 一行；fullbody 總數 241→237（v268 刪 4 張 vera 全身圖）；實線句數合計 54→53；「37 張」改 36（NEW 相關；焗邊報告 `qa138/bake_results138.json` 嗰幾項保持 37，因為 bake 檔本身無改）。
- `tests/test_rom159_static.py`：pack SHA 清單刪 vera_hiu_choi.json＋romance_tang.json，加 v268 精確替代斷言（vera 檔＝pristine 版減 5 個 R_vera_* 節點，nodes 15→10，version 1.3.2；tang 檔唔存在）；7 個釘行（25431→25195、8480→8246、26265→26029、10950→10716、15050→14814、26180→25944、全佳註解 25459→25223）。
- `tests/test_newspaper214_award_static.py`、`tests/test_aud91fix122_static.py`、`tests/test_aud91fix124_static.py`：各加 `_v268_allowed = {'content/story_detail_romance_tang.json'}`（git-status 內容檢查豁免）。
- 新測試 `tests/test_delete268_static.py`（57 項）：刪檔唔存在、檔名喺 index.html 零命中、已載入 pack 無 R_vera_* 節點／R_tang_* 只剩 stub、vhc 零 vera＋nodes 10、WF2／SCENE／MEET_SOFT／CONTRA98 四區無 `R_vera_`、保留項在位、tang 檔名只准喺 metadata 字串、紅線（SAVE／?v=／softRev）、`node --check`。
- `tests/test_wf5_87_static.py` 係基線已知 FAIL（BASE 目錄 `~/workspace/linji-work86` 已唔存在），唔郁。

## 五、第二輪：全套 suite 初跑 316／26 → 逐項修復（17 項新 FAIL，全部係刪行／刪檔嘅連帶影響，唔係 live 行為改變）

- **行數釘（總行數 45543→45307、openLoc DEF 40785→40549）**：`test_gift185_static.py`、`test_tang171_static.py`、`test_tang173_static.py`。
- **釘行漂移（difflib 對位逐行核實純漂移，`qa268/resync_generic.py`）**：
  `test_text125_static.py`（currentLine 11533→11298、advance 11675→11440，漂 −235；applyFamilySafe 16707→16471，漂 −236）；
  `test_kwan151_static.py`（12 釘：SCENE 刪除點前 9 個 −234，之後 3 個 −235）；
  `test_rom176_static.py`（5 釘一律 −236：15048→14812、39169→38933、39527→39291、40670→40434、40826→40590）；
  `test_travel114_static.py`（COUNT 12＋FREE 40＋DEF 40785→40549＋WRAPPER 28803→28567；6530／6531 唔郁、8456 −234、14484–14610 −235、其餘 −236）。
- **名冊／總數（vera 檔已刪）**：`test_bust109_static.py`（PORTRAITS bust 留返，全身 base 檢查豁免 vera）；
  `test_dlg106_static.py`（GAZE 登記留返——resolver 仲靠佢回 candidate 路徑，見 test_dlg138_logic.js；資產檢查豁免 vera）；
  `test_dlg107／119／123／126／127_static.py`（fullbody 總數 241→237）；
  `test_dlg108_static.py`（真檔 216→212；vera base 闊高比行刪除；淨空 ＜12px 配對 115→98，1081→1035 對，PIL 實量核實）；
  `test_dlg109_height_static.py`（真檔 216→212；方小龍＋Vera 配對改做方小龍＋老年影 dim，淨空 −33.6px，同樣 ＜12）。
- **死旗**：`test_br89_deadflag_lint.js`——`flag_tang_be` 唯一「讀取位」係已刪 pack 嘅 notes 字串（HE 孖旗 `flag_tang_he` 靠 index 註解提及仲有讀取位）；按 lint 規則加 `tests/br89_flag_whitelist.json` 孖旗條目（寫入位係 DengLine push mock 軟 hold 節點，結局本身 v152 已取消，旗純記錄）。
- 其餘：`test_dlg138_logic.js`（純 resolver 測試，唔讀檔）唔郁；`test_wf5_87_static.py` 基線已知 FAIL，唔郁。

## 六、驗收

- `node --check` 主 script 通過（抽 `<script>` 第二塊跑）。
- 全套 suite：`bash qa131/run_suite.sh /home/hatch/workspace/linji-work268 /tmp/suite268.txt`，基線 332／9；結果見回報。
