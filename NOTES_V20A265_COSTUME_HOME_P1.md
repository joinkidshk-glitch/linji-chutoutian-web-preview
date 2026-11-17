# NOTES — v20a265：服裝＋屋企系統 P1（COSTUME265）

- 分支：`v20a265`（基底 main `120c683`，v162）
- 設計權威：`~/workspace/linji-costume-home/DESIGN.md`（§1 服裝表／§2 服裝店／§3 屋企／§4 瞓覺／§5 衣櫃）
- 狀態：實裝完成，靜態測試＋`node --check` 通過，全套 suite 進行中（見下文）

## 實裝對照（逐項對設計）

### §1 服裝數據表（12 件全表）
- `const COSTUME265`（`index.html`，NPCS 之後，`/* ===== v20a265 COSTUME265` 塊頭）：
  #1 白恤衫牛仔褲 $120（外貌+1、魅力+1、無鎖、店賣、awi_c1）／#2 波鞋套裝 $150（體能+1、外貌+1、awi_c2）／
  #3 黑皮褸 $300（外貌+2、魅力+1、聲望≥15、awi_c3）／#4 合身深藍西裝 $600（外貌+2、魅力+2、聲望≥25、店賣、awi_c4）／
  #5 灰色三件頭 $900（外貌+3、魅力+2、台風+1、級數≥1、awi_c5）／#6 晚宴禮服 $1,500（外貌+3、魅力+3、台風+1、級數≥2＋聲望≥40、awi_c6）／
  #7 牛仔舞台服 $250（台風+2、歌藝+2、歌藝≥20、awi_c7）／#8 亮片舞台裝 $500（台風+3、魅力+1、歌藝≥25、店賣、awi_c8）／
  #9 閃粉舞衣 $800（台風+3、魅力+2、歌藝+1、級數≥2、awi_c9）／#10 武師練功服 $150（體能+2、演技+1、無鎖、店賣、awi_c10）／
  #11 民初長衫 $400（演技+3、台風+1、演技≥35、awi_c11）／#12 古裝戲服 $600（演技+2、外貌+2、演技≥30、awi_c12）。
  全套 $6,270（v261 經濟重做逐項重錨值）。P1 店只賣 4 件（#1／#4／#10／#8），其餘 8 件 `shop:false` 入表唔賣（P2）。
- Helpers：`COSTUME265_MAX_PER_STAT=4`、`COSTUME265_EXPRS`（8 表情）、`costume265ById`、`costume265EnsureWardrobe`、
  `costume265Tier()`（max(即時 tier, playerTierMax)，跟 dlg106「升咗就唔跌返」規則，免跨年鎖返）、
  `costume265UnlockReason`／`costume265Unlocked`、`costume265EquippedDef`、`costume265BonusMap`（每圍上限 +4）、
  `costume265EffStat`、`costume265BonusText`、`buyCostume265`、`costume265Equip`、`costume265SleepAvailable`、
  `costume265Sleep`、`openClothingShop265`、`renderWardrobe265`、`wireHome265`。
- **有效數值，永遠唔寫入 `S.*`**：`costume265BonusMap`／`costume265EffStat` 只計唔寫；
  靜態測試掃成個 COSTUME265 塊，唔准出現 `S.<七圍／聲望／壓力>` 賦值；錢只准喺 `buyCostume265` 入面扣。
- 門檻檢查：`reqGap()` 用 `costume265EffStat(k)` 計 have（即 `canAudition` 門檻）；`gigMissingReqGaps()` 嘅 cur 同樣改有效數值；
  通告詳情 `reqGridHtml` 嘅 `push30v2` 用有效數值做「現」，有衫貢獻就加 ` · 衫 +N`。聲望唔受衫影響。

### §2 服裝店
- LOCS 加 `clothing_shop`「花園街成衣店」（旺角，type:"shop"，region:"kln"，x:24 y:30，emoji:"✨"）。
  emoji 用 `✨`（已喺 EMOJI_ICON112 對照），唔用 `👕`（冇手繪圖標對照，會跌返 raw emoji）。
- 座標 keep (24,30)：同約會層戲院 (22,32) 只差 2.83%，但兩層永不同時顯示，pin／label 撞位只計同層；
  同層最近點：rec_hk (30,24) 8.5%、cafe_cha 16.7%，全部 ≥7.5%。test_map159 距離檢查改做同層先計。
- sheet 照抄禮品店買賣流程（查擁有→查鎖→查錢→扣錢→入 `S.wardrobe.owned`→`saveQ()`，買嘢唔耗日）；
  鎖住嗰陣卡面寫明要求。負責人「成衣店老闆娘」功能角色，唔開好感／巧遇；
  `locpanel118OwnerFor` 返 null（老闆娘暫無企立圖，跟 hospital 同例）。
- 場景圖 `assets/story/locs/bg_loc_clothing_shop.jpg`：另一工人已生成，檔案已喺工作副本（untracked，見下文）；
  code 寫路徑＋`applyLocSheetBg` 404 探測已擴到認呢個檔名（404 行中性漸變底）。

### §3 屋企
- LOCS 加 `home`「阿偉屋企」（深水埗唐樓，新 type:"home"，region:"kln"，x:20 y:44，emoji:"🏠"）。
  同層最近點 tvb_kowloon (37,45) 17.0% ≥7.5%。兩個新點都唔設 layer（預設片場層），唔入約會層。
- 場景圖用現成 `assets/story/locs/bg_wf4_home.jpg`（已入庫），唔使新圖。
- `openLoc` 加 `id==="home"` 分支（`atLoc=null; enterHome(null, false); return;`——唔開地點 sheet、唔擲巧遇／WF4）；
  返地圖行 `book70ExitHome()`，唔加新出口；`#home-back-map` bypass 唔喺呢票解決。
- sheet＝而家嗰個手帳畫面（同一套 tabs／數據源，唔複製第二份 UI），新增 ① 瞓覺掣 ② 衣櫃入口。
- `locpanel118OwnerFor`：home 返 null（屋企唔開 sheet）。

### §4 瞓覺
- ＝全日休息 reskin，同一條數（壓力清零、耗一日）：確認 modal 講明「今日就咁完咗，聽朝見。瞓足一日，壓力清零。」
  → hosp96／病假 gate → `writeTodayPlan("rest")`＋`apply({stress:-S.stress})`＋`recordExec105Day("rest")`＋`tickDay()`
  ＋`presentRestSleepDayEnd({sleep265:true, confirmStartSchedule:true})`（跟 doRest 嘅 presentDueMorningPaper 次序）。
- 呈現：行入屋企＋「zzz」浮字（`sleep265ZzzHtml()`，三個 span 浮動畫 `sleep265float`，2.2s 輪流延遲＋cap「瞓足一日，壓力清零。」），
  唔畫瞓低身體，**唔用 `fx_rest.mp4`**。
- Gate（`costume265SleepAvailable`）：`S.homeEditable` 為真／已結局／劇情進行中／`todayIsForcedDay()`（shoot:/job:）嗰陣唔出掣；
  今日已耗就唔出掣。瞓覺嗰日唔可以再排訓練／通告／小休，唔可以同全日休息疊加。瞓覺只清壓力，唔回體能／其他數值。

### §5 衣櫃
- 手帳加「衣櫃」區（著緊邊套／擁有嘅衫／換衫），換衫免費、即時、唔耗日、唔耗出行額度。
  `S.wardrobe = { owned: [], equipped: null }`（`fresh()`＋`normalizeSaveObj()` 補預設，舊檔 owned:[]／equipped:null＝著返階段造型）。
- 著緊衫嗰陣：對話舞台 `dlg106AweiStem` 加一層（有著衫→衫嘅 stem，冇→階段 stem；衫圖未入庫嗰陣 `dlg106Candidates` 候補鏈跌返 `awi`，唔出破圖；
  `dlg106GazeEntry` 對 costume stem 會跌返 `T["awi"]`）；頁頭 bust `bust109HeroSrc` 用衫嘅 base 全身圖直出（object-fit:cover 置頂裁，同 v109 做法；
  圖未到之前 onerror 跌返階段 bust）。除低返去階段造型。級數升咗唔自動除衫。頒獎禮燕尾服唔郁。
- 衫圖檔名約定：`assets/story/fullbody/awi_c1_<expr>.webp`／`awi_c4_…`／`awi_c10_…`／`awi_c8_…`（expr＝base／angry／sad／serious／shy／smile／surprise／think）。
  另一工人已生成晒 4 套 × 8 表情＝32 檔，檔案已喺工作副本（untracked，見下文）。

### 出行額度／地點數
- 屋企免費：`travel114IsFree("home")` 守衛已存在，核實仲在；入服裝店照計 1 次（`travel114IsFree` 冇 clothing_shop 豁免）。
- 地點數 15→17（片場層）、LOCS 總數 21→23。掃晒「15 地點」硬編碼：LOCS／MAP159／drawMap／mn68／ROM159／LOC_SHEET_BG／locpanel118 註解全部改返 17。

## 測試

- 新檔 `tests/test_costume265_static.py`：**83 項，全部 PASS**（`python3 tests/test_costume265_static.py`，exit 0）。
  覆蓋：12 件價錢／加成／解鎖／stem／shop 同設計一致、全套 $6,270、P1 店只賣 4 件、每圍上限 +4、
  加成函數存在且唔寫入 `S.*`（掃成個 COSTUME265 塊：零 `S.<圍／聲望／壓力>` 賦值；錢只喺 buyCostume265 扣）、
  門檻＋卡面行有效數值、買衫流程標記齊（擁有／解鎖／錢／扣錢／入 owned／saveQ／唔耗日／P2 衫守門）、
  瞓覺掣／衣櫃入口標記齊（確認文案／壓力清零／耗一日／唔用 fx_rest／zzz 呈現／gate 四項）、
  地點數 17／23、home 免費／shop 計 1 次、舊檔相容、紅線三項（SAVE key／softRev／?v=）不變、P2／P3 零偷渡（N11／耐久／混搭／場合加成／套裝效果／第二間店／衫送禮／感情線掛鈎）。
  **唔斷言衫圖檔案存在**（另一工人平行生成，免次序耦合；統籌最後統一驗）。
- 舊測試更新（21→23，全部 PASS）：`test_map159_static.py`（LOCS 23、mn 23、距離檢查改同層先計＋新點 label 齊）、
  `test_map97_static.py`（mn 23＋名 set、LOCS 23）、`test_ui137_map_static.py`（mn 23＋名 set）、
  `test_awards207_static.py:146`（mn68 23）、`test_date159_static.py:136`（LOCS 23）、
  `test_ux68_static.py`（labels 23＋spec 補 2 新點位置：成衣店 (24,30,-,52)、屋企 (20,44,+,34)）、
  `test_venue99_static.py:47`（LOCS 23）、`test_locpanel118_static.py`（§6 bg_loc_ 15→16＋clothing_shop 路徑斷言＋home bg_wf4_home.jpg 路徑＋實存；
  §2 加新點 id 齊＋owner 返 null 斷言；標題 15→17）。
- `node --check`：抽最大 `<script>` block（4,340,129 bytes）→ **PASS**。
- 全套 `bash qa131/run_suite.sh`：**最終 330 PASS／10 FAIL（基線 329／10，零回歸）**。
  第一輪 309／31——21 項新增 FAIL 全屬 resync 範圍（見下文），逐項修好後第二輪 330／10。
  10 項 FAIL 同基線完全一致（flash51／rumor49／slot50／soft_tip_111_restore／start53／weave43／weave44／weave49／wf5_87／wrap38），
  全部係已知 pre-existing。新測試檔 `test_costume265_static.py` 喺 suite 入面 PASS。
  `index.html` 淨 +378 行（46236→46614；openLoc DEF 41447→41797，DEF 之前淨 +350）。

## Resync（suite 第一輪 309／31 → 第二輪 330／10，零回歸）

新增 FAIL 21 項，分四類，全部係合法漂移／計數，唔係回歸：

1. **計數＋1（瞓覺係新嘅全日休息／確認路徑）**：`test_fix65_static.py`（`apply({stress:-S.stress})` 2→3 處：排程 rest＋doRest＋瞓覺 reskin）；
   `test_flow45_static.py`（`confirmStartSchedule: true` 3→4 處，加瞓覺卡檢查）；`test_reconfirm236_static.py`
   （`confirmChoice236(` 12→13 次，加 C7 買衫先確認後扣錢）。
2. **LOC_SHEET_BG 計數**：`test_enc105_logic.js`（21→23：加 clothing_shop bg_loc_＋home bg_wf4_home.jpg）。
3. **fullbody 資產計數（圖工人 32 張衫圖入庫）**：`test_dlg107／119／123／126／127／138_static.py`
   （webp+png 209→241）；`test_dlg108／109_height_static.py`（webp 減 boss_ 184→216）。鏈尾加「v265 加 32 張衫圖」。
4. **釘行漂移（difflib 對位，錨點內容逐字相同）**：`test_rom159_static.py`（6 釘＋全佳行）、
   `test_rom176_static.py`（6 釘）、`test_kwan151_static.py`（14 釘）、`test_tang152_static.py`（3 釘）、
   `test_text125_static.py`（3 釘）、`test_travel114_static.py`（COUNT 12／FREE 38／DEF／WRAPPER；FREE 另加 2 處新免費點——
   買衫 modal「關閉」／onDismiss 返程 `openLoc(L.id, {travelFree:true})`，跟禮品店同例，免費清單 38→40 處；DEF 41447→41797、WRAPPER 29204→29554）、
   `test_tang171／173_static.py`（總行數鏈＋DEF 鏈＋L4862 live 行 5205→5222）、`test_gift185_static.py`（總行數鏈）。
   套用腳本 `/tmp/resync265.py`（映射＋錨點核實，0 mismatch）／`/tmp/apply_resync265.py`（每檔單次掃描 dict 查表，冪等）。

## 實裝期間嘅決定／教訓（留檔）

- **COSTUME265 塊唔可以放喺 LOCS 同 NPCS 之間**：表入面 12 個 `{ id:"cX"` 會污染用 `src.split('const LOCS')[1].split('const NPCS')[0]` 計數嘅測試
  （test_map97／test_venue99 會由 23 變 35）。已將成個 block 搬去 NPCS 之後（STAT_LABEL 之前）；LOCS..NPCS 計數回復 23。搬完 `node --check` PASS。
- test_map159 距離檢查改做同層先計（date 點只同 date 層點＋約會層共享點茶記／廟街比較；片場層新點唔入）。
  原因：成衣店 (24,30) 同約會層戲院 (22,32) 只差 2.83%，但兩層永不同時顯示（drawMap 只畫當前層），跨層距離無意義。
- test_costume265 嘅 `blk` 掃描範圍：由 block 頭 `/* ===== v20a265 COSTUME265` 到 `const STAT_LABEL`
  （block 喺 NPCS 之後；唔好用 `const NPCS` 做結尾，亦唔好用 LOCS 頭嗰個「服裝店＋屋企上地圖」註解做開頭——嗰個撞名）。

## 未做／留跟進

- **圖檔已隨呢個分支一併 commit**：另一工人已生成晒 4 套衫圖 × 8 表情＝32 檔（`assets/story/fullbody/awi_c1／c4／c8／c10_*.webp`）
  ＋服裝店場景圖 `assets/story/locs/bg_loc_clothing_shop.jpg`，檔案喺工作副本入面已齊。因為 (a) resync 後嘅 dlg 資產計數測試
  （209→241／184→216）要求呢啲檔喺樹入面，分支先至係自洽綠色；(b) 工作副本落地後會刪除，唔 commit 就會連同未追蹤檔一齊唔見。
  呢 33 個圖檔係圖工人嘅交付物，呢度只係代為入庫，唔係 code 工人嘅作品；統籌合併嗰陣核實圖工人嗰邊冇更新版（有就覆蓋）。
  工具 side 檔 `assets/story/fullbody/media-generation-last-upload-handles.json` 唔係遊戲資產，**冇** commit，留喺工作副本唔郁。
  `bg_wf4_home.jpg` 係已入庫舊檔（tracked），唔受影響。
- 成衣店老闆娘暫無企立圖，locpanel 負責人返 null（跟 hospital 同例），有圖再接。
- 實機驗證押後（瀏覽器死係已知背景狀況；呢票只做靜態＋suite）。
- P2／P3 全部未做：其餘 8 件衫上架、N11 讀衫掛鈎、第二間店、混搭、場合加成、套裝效果、耐久度、衫送禮／感情線掛鈎、
  NPC 店員開好感、瞓覺回體能或其他數值。
- `#home-back-map` bypass 唔喺呢票解決。
