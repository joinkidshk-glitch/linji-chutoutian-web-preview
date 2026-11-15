# NOTES_V20A232 — 補寫《星夜迷離》臨時替工（新庫第 241 張）

- Base：main `e3d1333`（v231 RW-1；分支原 base `1b0dad9` v230，落地前 rebase 上 v231，零衝突）
- 原因：v229 偏離第 1 項——新庫 240 張入面《星夜迷離》0 命中，陸柏言支線 Beat 3 替工通告 live 開唔到。用戶 2026-11-16 03:36 拍板：加一張新通告，做第 241 張，唔改現有通告。
- 攻略定位（canonical guide 唯讀核實）：陸柏言支線 Beat 3〈轉〉——替工通告《星夜迷離》臨時替工，片酬 $3,100，頂整晚；閘門 T2＋週期開（T2＝好感 tier ≥2），唔靠打聽；場景 1990–1991 年獅子山茶水間；殺青後天王團隊人情 ＋1（`credit_wf3_lu_team`）；旗對照表：`luk_cover_night`＝完成替工通告 `gig_intel_lu_standin`。

## 新通告

- `gig_1991_tv_122`｜《星夜迷離》臨時替工｜電視劇｜1991｜冬｜初級｜臨記通告｜文藝｜星河電視台（`tvb_longmen`）｜`leadStarId: luk_baakyin`｜roleLabel「替身」｜days 1（`tv_cameo_short`）｜req 體能 70｜hard 0.43｜pay [2900, 3300]（中位數 $3,100＝攻略定價）｜fame [5, 12]
- trigger：`{"kind":"rel","npcId":"luk_baakyin","relMin":25}`（T2；v229 D-14 已將舊閘 `intel_lu_burst` 改做 tier ≥2，唔用舊閘；`INTEL_HIDDEN_GIGS` 池留空，唔留雙重閘）
- 文案（由頭新寫，香港式書面語；舊庫已全刪，0 照抄）：
  - blurb：「《星夜迷離》劇組臨時需要替工，頂替陸柏言的整晚夜戲，通宵拍攝至天明。」
  - synopsis：「星河電視台劇集《星夜迷離》拍攝夜戲，劇組臨時缺人，需要替工頂替整晚戲份。阿偉站在主角的位置，完成走位與對白，陪劇組捱到天明。拍攝於電視城搭景，通宵進行，現場由副導指揮。陸柏言的狀態不佳，劇組上下都繃緊神經，這一晚的表現，全組人都看在眼裡。」
  - roleHint：「頂替整晚夜戲，體能要夠；走位與對白一次記準，不可拖慢劇組進度。」
  - discoverNote：「陸柏言近況不佳，劇組隨時需要替工頂替整晚演出，留意通告欄。」
- 年份／季節理據：攻略 Beat 3 窗口 1990–1991；引擎一張通告只得一年一季，1991 覆蓋最廣；陸柏言 (year, season) 主演上限 3 張——1991 夏／秋已滿 3 張，1991 冬得 1 張（加落去變 2 張，合規）；冬窗（上板約 1991-10-02 至 1992-02-28）覆蓋最遲，兼顧 Beat 4／N14 前哨（1992 春末）之前完成。
- 舊 id `gig_intel_lu_standin` 絕對唔可以用返（已喺舊 id 清單入面）；新 id 用 `gig_1991_tv_122`（1991 TV 現有最大號 121 之後）。
- 級別／類別理據：初級（SPEC：觸發通告級別同觸發獨立，初級＋trigger 合法；稀有會加 fameFloor 32 錯閘＋改稀有計數）；臨記通告（替身通告 roleLabel 含「替身」，引擎判 base，唔出報紙；`workTitle` 空、無 `posterBrief`，跟 SPEC）。

## 計數變化

- 新庫 240→**241** 張；觸發 46→**47** 張（rel 2→3）；初級 73→74；臨記通告 93→94；1991 年 79→80；有 `leadStarId` 152→153；錯峰合資格 228→229（241－12 入門）。
- 設計檔同步：`~/workspace/linji-gig-redesign/gigs/gigs_all.json`（241 張）＋`gigs_tv.json`（64 張）＋`verify_gigs.py`（期望數更新）＋`VERIFICATION.md` §13。

## 片酬例外（窄幅）

- 日薪中位數 $3,100 遠超初級帶 $500–900。處理：keep 攻略定價 $3,100（攻略兩處明言，一晚緊急替工天王組高薪請人；一次過、rel 閘限定，唔可以農場），`verify_gigs.py` Q6 加 `PAY_BAND_EXEMPT = {"gig_1991_tv_122"}`（只豁免呢張嘅日薪帶檢查，格式／臨記通告 $5,000 上限檢查照行）；`tests/test_dur90_logic.js` DAILY_ALLOW_229 表加 `gig_1991_tv_122:3100`（同 4 張 1992 稀有大碟一樣表列釘死）。
- 唔改 tier 做稀有（會改稀有計數 23→24、加 fameFloor 32 錯閘）；唔改 pay 落帶（會違反攻略明言數字）。

## 驗證

- `python3 verify_gigs.py gigs_all.json` → **ERROR 0／WARNING 0**；`gigs_tv.json` 同樣 PASS。
- `node --check`：index.html 兩塊 inline script 全部 OK（本票無改 index.html）。
- gig229 測試 8 檔全 PASS（pack／trigger／years／grant／press94_advice／stagger／counts／tiers）。
- 觸發鏈（in-memory，test_gig229_trigger.js T1＋T7）：陸好感 24→唔開、25→開（T2）、標籤＝邀約；新庫有且只有一張《星夜迷離》（`gig_1991_tv_122`）；`INTEL_HIDDEN_GIGS` 池留空，無雙重閘。
- 獎項／提名計數唔受影響：臨記通告唔計提名（press94：named 141 不變、base 99→100）；擔正計數器（counts）PASS。
- 全套 suite（工作副本，rebase 後）：**PASS 312／FAIL 10**，同基線一致；10 項 FAIL 全部已知 pre-existing（flash51／rumor49／slot50／soft_tip_111_restore／start53／weave43／weave44／weave49／wf5_87／wrap38）。第一輪 suite 309／13 係因為 dur90／fix88／nat92 三檔有硬編碼 240／46 期望未同步，已一併更新（見下），重跑後返基線。
- 改動測試檔（除 gig229 8 檔外）：`test_dur90_logic.js`（A4 240→241、B1／B4 標籤、DAILY_ALLOW_229 加例外、B2 標籤改 5 張表列例外）、`test_fix88_logic.js`（A1 240→241）、`test_nat92_logic.js`（F2 228→229、E0 46→47）。

## 已知限制（向用戶講明）

- 新系統得一個季節窗口（1991 冬），唔係攻略講嘅「週期開」。
- T2 喺 1992 年 2 月之後先達到嘅玩家會錯過暖版路徑（行冷版，屬設計內結果）。
- 冬窗尾段（1992 年 1–2 月）輕微超出攻略「1990–1991 年」窗口。
- `mergeIntelGigs` 空池＋舊註解（話「要補寫新庫版」）已過時，屬後續清走死碼範圍，唔喺本票郁 index.html。
- live 實駕押後（瀏覽器死咗）：觸發前隱藏→T2 後上板→接通告→殺青嘅實機全程，等瀏覽器恢復再跑。
