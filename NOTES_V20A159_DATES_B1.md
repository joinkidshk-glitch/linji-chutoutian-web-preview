# NOTES_V20A159_DATES_B1 — v159 約會工人 B1（約會場次＋價錢）

分支 `v159-dates`（基底 branch v159 `6cc403c`，Phase 1 機制已 cherry-pick）。
只改 `ROM159_DATES`（index.html 約 L25427 起）＋新增測試 `tests/test_date159_static.py`。
唔郁：ROM159_WOMEN（A 工人）、LOCS／drawMap／地點 sheet（B2 工人）、prefs／commit offer／
鏈 D／loader、gift_prefs.json pack、主線 JSON、服裝／屋企、SAVE key／softRev／?v=。

## 做咗乜

1. **刪 vera_* 4 場**：vera_central／vera_admiralty／vera_star／vera_cafe 全刪。
   DATES 塊內已無任何 `vera_`／`Vera` 殘留。ROM159_WOMEN 入面 vera spots 行未郁（A 工人擁有，
   佢更新嗰陣先清）；date picker 本身有 `if(!sp) return "";` 守衛，刪咗 DATES 唔會爆。
2. **全部場次按 Q7 定值表重定價**（經濟重做 DESIGN.md §4.8，已拍板 2026-11-17）：
   散步類（天台／外景／廠景／錄音室／電台／廣告場合）$4；海傍／山頂／淺水灣／啟德 $6；
   廟街 $20；茶記 $45；戲院／首映 $58；酒廊唱歌 $50。
   舊場 7 個只改 cost 數字，intro／good／bad 文字一字未郁（diff 核實）：
   hiu_roof 60→4、hiu_location 40→4、hiu_market 50→20、hiu_cafe 35→45、
   choi_premiere 90→58、choi_radio 60→4、choi_cafe 35→45。
   **酒廊 $50 係推算，待確認**——§4.8 寫明 1990 年未有多房式 K 場、收費搵唔到；
   Q8 已將地點改做「酒廊唱歌」，價錢用 $50 推算值（喺 $40–60 帶內），等用戶／統籌確認。
3. **新寫 30 場，六人共 37 場**（每場 intro＋good｛label，line｝＋bad｛label，line｝）：
   hiu 7（新：harbour／beach／airport）、choi 5（新：lounge／cinema）、
   lan 6（全新：studio／ktv／rec／lounge／beach／cafe）、xu 7（全新）、
   yip 6（全新）、so 6（全新）。
   對白跟每人弧線＋地點性格（草稿 §1／§3.2）：同一地點唔同人有唔同意思——
   茶記：曉晴收工食飯、采兒爆料、藍唞氣、寶珊放低身段、葉練歌後唞氣、蘇冇記者嘅地方；
   海傍／機場／沙灘對蘇係「肯俾阿偉見到佢唔做樣嗰面」；山頂對葉係「企高啲睇返自己」、
   對寶珊係「肯放低身段」；錄音室半首歌係藍條線核心。
   語言：對白廣東話；標題／提示／旁白香港式書面語；場面文字唔寫數字承諾（無 +1／-1／加分字眼）。
4. **新測試 `tests/test_date159_static.py`（493 項，0 FAIL）**：
   37 場齊全（每人 7／5／6／7／6／6）、每場 intro＋good＋bad 齊全、
   cost 全部喺 Q7 帶內（散步 $0–6、海傍等 $0–6、廟街 $10–30、茶記 $40–50、
   戲院／首映 $40–76、酒廊 $40–60）＋逐場定值對照、locId 全部係已知地點或 date_* 新點、
   無 vera_* 殘留、good／bad 唔係同一句。機制唔郁，唔寫 logic 測試。
   6 個新 locId（date_harbour／date_peak／date_lounge／date_cinema／date_beach／date_airport）
   係 B2 工人加緊嘅 LOCS，呢個 clone 入面未有——DATES 照寫，測試唔斷言佢哋喺 LOCS 入面。

## 驗證

- `node --check`（抽最大 `<script>` 塊，3,716,962 字元）：PASS。
- 全套 `bash qa131/run_suite.sh`：
  - 基線（乾淨 `6cc403c`）：**TOTAL PASS 310 FAIL 21**。
  - 改完：**TOTAL PASS 310 FAIL 22**（多 1 個檔：新測試 PASS，見下）。
  - 新測試 `tests/test_date159_static.py`：PASS（493 checks, 0 FAIL）。

## 前／後 FAIL 名單對照

基線 21 個 FAIL（全部 pre-existing，改前已有）：
test_flash51_static、test_gift185_static、test_kwan151_static、test_rom159_static、
test_rom176_static、test_rom183_static、test_rumor49_static、test_slot50_static、
test_soft_tip_111_restore、test_start53_static、test_tang152_static、test_tang171_static、
test_tang173_static、test_text125_static、test_travel114_static、test_weave43_static、
test_weave44_static、test_weave46_static、test_weave49_static、test_wf5_87_static、
test_wrap38_static。

改完 22 個 FAIL＝基線 21 個＋**新增 1 個：`tests/test_rom159_logic.js`（68 PASS／1 FAIL）**。
唯一 FAIL 項：`I 約會地點：全部係現有 15 地點`（L257）。

## 新增 FAIL 嘅原因（已知，唔係我改錯）

A 工人嘅 logic test L257 硬寫 15 個現有地點 id，要求 `ROM159_DATES` 全部 locId 喺呢個
list 入面。呢個斷言係 Phase 1 嗰陣寫嘅，當時約會地點全部係現有 15 地點。
B1 任務本身要求 6 個新 locId（date_*，B2 工人加緊嘅 LOCS，呢個 clone 未有），
所以呢個斷言必然 FAIL——唔係改錯，係分工時序問題。
注意：就算 B2 落地加咗 date_* 入 LOCS，呢個斷言**仍然會 FAIL**，因為 test 硬寫 15 個 id；
要 A 工人更新斷言（例如放寬做「已知地點或 date_* 新點」，同 test_date159_static.py 嘅寫法），
先至會綠。呢個測試 A 工人擁有，B1 無權改，留返畀統籌／A 跟進。

其餘兩個相關說明：
- `test_rom159_static.py` 基線同改完都係 FAIL，原因相同（pre-existing）：(1) pack 路徑已改名
  （`story_detail_c1_to_c17.json` → `story_detail_n1_to_n17.json`，C→N 統一），測試撞
  `FileNotFoundError`；(2) 行號釘過時（ROM159 block 頭喺 L25380，測試釘 L41675）。
  兩個都同 B1 改動無關，B1 無權改（A 工人擁有）。
- `rom159DateButtonInfo`／`rom159OpenDatePicker` 對未入 LOCS 嘅 date_* locId 有守衛
  （`LOCS.find(...)||{}` fallback 用 `sp.label`；缺失 spot 返空字串），
  喺 B2 LOCS 落地之前，約會選擇器會顯示 label 而唔會爆。

## 留低／未解決

- 酒廊唱歌 $50 係推算值，待確認（見上）。
- ROM159_WOMEN spots 表仍係 Phase 1（hiu 4／choi 3／vera 4／lan・xu・mei 空）——A 工人更新嗰陣，
  DATES key 必須同佢 spots 表一字不差（見任務表）；B1 嘅 DATES key 已照任務表寫齊。
- date_* 6 個新點嘅 LOCS＋地圖熱區＋地點 sheet 係 B2 工人範圍，呢個 clone 未有。
- 實機驗證押後（瀏覽器死，沿用之前各票做法；待統籌安排實機抽檢）。
