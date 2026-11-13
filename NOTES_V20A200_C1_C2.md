# NOTES_V20A200 — 修 v194 設計 review C1＋C2（＋v192 殘留 nominee 行）

- 分支：`v20a200`（基底 main `a1a6681`＝v194；唔落地，落地由統籌做）
- 範圍：純文案三處＋一行標籤，計數／判定／計分／門檻／報紙模板一字唔郁。
  `index.html` 淨 +12 行（註解 +9／分流 +3），總行數 60667 → 60679。
- SAVE key `starVolunteer_map_v19w`、softRev `s107`、`?v=v20a10`、content pack JSON 全部唔郁。

## 1. 改咗咩（檔＋行）

### C1：gap 句加「今年」（邀請函＋季前提示兩邊一齊加，講法一致）
- `index.html` L46639–46641 `awards62GateLineHtml`：gap 句由「仲差 N 部 X 作品先夠入圍
  （而家 a/b）」改做「**今年**仲差 N 部 X 作品先夠入圍（而家 a/b）」。
- `index.html` L46728–46729 `awards62SeasonHints`：季前提示同一句加「今年」——
  「今季就係「維港街招・年度廣告賞」：**今年**仲差 1 部廣告作品先夠入圍——呢排接廣告通告要留神。」
- 計數規則本身唔郁：`countYearMediumWraps` 繼續按 `wrappedDay` 曆法年計入嗰屆，
  跨年作品唔計（既定口徑）；`gapWorks = wrapMin - wraps` 唔郁。
  揀「今年」唔揀「呢屆」（review 建議例用「今年」；「今年」同提示入面其他行
  「今年你係贏嗰格嘅大熱」「今年好接近贏嗰格」講法一致）。

### C2：旁聽請柬 rep 行改寫法（唔係刪行）
- `index.html` L47571–47577 `awards63InviteBitHtml`：按 `pack.tier === "gallery"` 分流——
  gallery 嗰陣「你今年憑《X》**入場觀禮**。」；nominee／won 照舊「你今年憑《X》爭獎。」。
  海報＋同屆提名照留。
- `index.html` L46157 `renderAwardInviteHtml` 嘅 fallback 行同樣分流（唔會兜返舊寫法）。
- 揀改寫法唔揀唔出呢行：呢行同時帶海報＋同屆提名，刪行會一併刪走嗰兩樣。
  其餘「爭獎」唔郁：nominee 閘句（L46629「嗰年 N 部作品，憑《X》爭獎」）係真爭獎，照舊。

### v192 殘留（對過，改咗）：nominee「今晚獎項」行改標籤，唔改 slate
- `index.html` L46143–46147 `renderAwardInviteHtml`：非 gallery 分支標籤由
  「今晚獎項：…」改做「**你爭嘅獎項：…**」；slate 照舊淨列你爭嗰 1–2 格，
  唔加女獎／（觀禮）標記。
- 點解改：同 C2 同一類問題——標籤話係全晚獎項，內容淨係你爭嗰啲；改標籤係最小修法，
  標籤仲短咗，零溢出風險。gallery 嗰邊 v192 C4 全 slate＋（觀禮）唔郁。
- 舊 `tests/test_awards192_logic.js` C4 斷言同步更新（標籤新寫法＋註解說明，見 §4）。

## 2. 新測試（38 項，全部 PASS；反證乾淨 FAIL）

- `tests/test_awards200_logic.js`（16 項，真執行函數）：
  C1 邀請函 gap 句逐字（廣告 0/1 原案＋電影 1/2）、夠數唔出 gap 句、
  nominee 分支唔郁、季前提示真執行逐字（stub 季度／旗標／standing）、
  C2 rep 行分流（gallery 入場觀禮／nominee 爭獎／冇代表作唔出）、
  成張請柬（gallery 零「爭獎」＋gap 有「今年」＋席位／全 slate 唔郁；
  nominee「你爭嘅獎項」＋rep 照舊爭獎；gallery 仲係「今晚獎項」＋觀禮）。
- `tests/test_awards200_static.py`（22 項）：兩邊 gap 句有「今年」＋舊寫法清走、
  計數口徑唔郁（`awardsYearFromDay(h.wrappedDay!=null ? h.wrappedDay : h.dayIndex)`、
  `gapWorks` 定義）、rep 行分流＋fallback 分流、海報＋同屆提名照留、
  nominee 標籤改咗／gallery 唔郁、SAVE／softRev／?v= 唔郁、
  8 款贏獎報紙 headline 逐字不變（模板 `{playerName}` 代位）。
- 反證：兩檔對 pristine main `a1a6681` index（`/tmp/pristine200_index.html`，
  常駐 clone `git show` 抽出）→ 反證守衛 3 項乾淨 FAIL，唔 crash。

## 3. 全套 A/B（`qa131/run_suite.sh`，複製版 node／python）

- Baseline（pristine main `a1a6681`）：**271 PASS／12 FAIL**（12 項穩定 pre-existing）。
- 初版 work：268／17——多咗 5 項 FAIL，全部係我淨 +12 行令釘行漂移，
  唔係邏輯回歸：`test_gift185_static.py`／`test_rom176_static.py`／
  `test_tang171_static.py`／`test_tang173_static.py`／`test_travel114_static.py`
  （總行數釘 60667、openLoc DEF 55160、rom176 line() 釘、travel114 COUNT／FREE 釘）。
- Resync（`qa200/resync200.py`，difflib 對位核實純漂移先寫入）：
  總行數 60679、DEF 55160→55172、rom176 4 釘各 +12、travel114 set 內 26 個數字各 +12
  （≥47571 者；之前唔郁；COUNT 12／FREE 34 不變；WRAPPER 44436 唔郁）。
  註：rom176 檢查名入面嘅 L53050／L53415 等係舊版殘留標籤（pristine 嗰陣已經唔對數），
  數字本身先係釘，今次只改數字，名唔郁。
- Resync 後 work：**273 PASS／12 FAIL**——FAIL 清單同 baseline 逐字一致
  （淨係總數 271→273，因為新加 2 個測試檔都 PASS）。
  相關測試逐個直接覆驗：5 項 resync 檔全部 PASS（gift185／rom176／tang171 22/22／
  tang173 21/21／travel114 PASS）＋新測試 2 檔 PASS＋`test_awards192_logic.js` PASS。

## 4. 改埋嘅測試檔

- `tests/test_awards192_logic.js`：C4 nominee 斷言由「今晚獎項：…」改做
  「你爭嘅獎項：…」（v192 NOTES 本身寫明呢行等下一票拍板，呢票就係嗰一票；
  檔頭註解同步更新）。其餘斷言（gallery 全 slate＋觀禮、女獎只係列名）唔郁。
- `tests/test_gift185_static.py`／`test_rom176_static.py`／`test_tang171_static.py`／
  `test_tang173_static.py`／`test_travel114_static.py`：淨係 resync 釘行（見 §3），
  斷言邏輯一字唔郁。

## 5. 實駕（`qa200/drive200.py`，LIVE 裸 URL，Playwright venv＋headless shell，本地 serve port 20090）

- 13 case，0 pageerror，0 failed request。結果：`qa200/drive200.json`，截圖 `qa200/shots200/`（45 張）。
- C1 live（`c1_ad_gap_932`／`700`，PASS）：v194 原案重現——上一年 2 部廣告臨記
  （wrappedDay 1990-09-15），1991 春季廣告賞，live `queue()` 返 1 部 gallery pack，
  `presentAward()` 彈請柬。季前提示逐字＝「今季就係「維港街招・年度廣告賞」：
  **今年**仲差 1 部廣告作品先夠入圍——呢排接廣告通告要留神。」；請柬逐字＝
  「今晚席位：觀禮。**今年**仲差 1 部廣告作品先夠入圍（而家 0/1）；聲望／業內信用未到入圍基本盤。」
  （另帶雙軌未達標句，正確）；請柬零「爭獎」、零溢出（403/403）。
- C2（`c2_film_gal_932`／`700`，PASS）：同年 2 部電影臨記位，gallery 請柬逐字＝
  「你今年憑《江邊小鎮》**入場觀禮**。」；成張請柬零「爭獎」；角色閘句
  「嗰年未做過主角／配角級作品，入圍唔到演員獎」照在；全 slate＋（觀禮）＋旁聽席唔郁；
  請柬零溢出（932／700）。
- Nominee 對照（`c2_nom_932`，PASS）：電影 nominee 請柬「你爭嘅獎項：最佳男主角、
  最佳男配角」＋rep 行「你今年憑《新春大吉》爭獎。」＋「今晚獎項」零出現。
- 贏獎報紙 live 重驗（`b1_*` ×8，queue＋晨報）：
  8 款 queue templateId 對準，headline＋dek 逐字＝v192 NP_EXPECT（見下表），禁字零命中；
  翌朝晨報真實出街 8/8（film／tv／music delay 1 日，ad delay 2 日——播種日係週日，
  v192 C1 已知遲一日，報紙無遺失）；手帳獎項頁有典禮名＋徽章、地圖零橫向溢出、0 pageerror。
  唯一 fail 項：8 款晨報 modal 劃一 +7px 溢出（例 film_01 602/595、music_02 623/616）——
  **pre-existing，唔係 v200 回歸**：同一 case 對 pristine `a1a6681`（sha `4ed6aa07a9cc`）
  跑，同一份晨報同樣 602/595。v200 冇郁過報紙渲染。呢票唔修（範圍外），等拍板。

  | 模板 | headline（逐字） |
  |---|---|
  | np_win_film_01 | 維港影藝獎揭曉 阿偉 奪演員獎 |
  | np_win_film_02 | 影藝獎夜 阿偉奪獎成焦點 |
  | np_win_tv_01 | 星河台慶夜 演員獎爆冷由阿偉奪得 |
  | np_win_tv_02 | 台慶夜 阿偉奪獎贏街坊票 |
  | np_win_music_01 | 星河金碟夜 阿偉奪獎跑出 |
  | np_win_music_02 | 金碟夜 阿偉奪獎 樂壇多把靚聲 |
  | np_win_ad_01 | 維港街招賞 阿偉跑出 |
  | np_win_ad_02 | 街外一鏡 阿偉奪獎贏掌聲 |
  （dek 逐字同 v192 NP_EXPECT 一致，見 `qa200/drive200.json` 各 case `newspaper_win_items`。）
- 實駕途中 drive 腳本修咗一個流程問題（唔係遊戲問題）：晨報嗰步返地圖嗰陣，
  另一場典禮（影藝獎）嘅請柬會彈出嚟擋路——drive 而家識推辭＋等典禮播完再繼續搵晨報
  （`qa200/drive200.py` `morning_paper()` 嘅 invite 分支）。

## 6. 未驗到／殘留

- 晨報 modal +7px 溢出（pre-existing，pristine 同數，見 §5）：唔喺呢票範圍，等拍板修唔修。
- 音頻未人耳試聽（同之前各版一樣）。
- v192 C1（週日報紙遲一日）同 B2（廣告 won 數據缺口）原封不動，唔係呢票範圍。
- 實駕用 debug force 建 won／nom pack（呈現路徑驗證用）；C1 用真 live queue 路徑驗過。

## 7. 統籌 rebase 上 main 2c1a680（v199 落地後）

- 工人分支基底係舊 main `a1a6681`（v194）；落地前 main 已郁到 `2c1a680`（v199＋NOTES），統籌 rebase 咗分支上新 main。
- Rebase 衝突淨係 5 檔 resync 過嘅 static test（`test_gift185／test_rom176／test_tang171／test_tang173／test_travel114_static.py`），`index.html` 乾淨合併。解法：取 main 版 5 檔，再用 `qa200/resync200_rebase.py`（OLD＝main、NEW＝rebased index）difflib 對位重算釘行——全部純漂移（總行數 60711→60723、DEF 55204→55216、WRAPPER 44480 唔郁、COUNT 12／FREE 34 內容逐字相同）。
- Rebase 後重驗：5 檔＋v200 新測試全部 PASS；全套 **275/12**（main 基線 273/12，**FAIL 清單逐字一致**，+2 PASS 係 v200 新測試），零回歸。Rebase 前工人數字（273/12，舊基線 271/12）見 §4，結論不變。
- 環境註：開工嗰陣 `/usr/bin/git`／`node`／`python3` 寫入返 EPERM，統籌用 `~/workspace/bin/` 複製版 binary 繞過（git clone／commit／push／ls-remote 全部驗過得）；工人全程用複製版，見任務書。
