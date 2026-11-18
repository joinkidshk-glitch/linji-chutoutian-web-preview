# NOTES_V20A317_CHAI_ECHO_TV114

v20a317（Q17 後續／D-11 §3.6B 支線回響）：齊鎮海 `gig_1991_tv_114`《亂世將軍傳》升格做支線回響通告。
基線 main `260b1d7`（v316，suite 379／9）。

## 1. 改動（三樣，跟 v316 一式三樣）

| 位置 | 改動 |
|---|---|
| `content/gigs_new.json` tv_114 | 加 `storyKeys: ["chai_zanhoi"]`＋`trigger: {kind:"credit", creditId:"credit_enc83_chai_patron", creditOwner:"齊鎮海"}`；其餘欄位一行都唔郁（title／tier 高級／type 電視劇／year 1991／season 秋／days 30／pay [6000,7200]／genre 歷史傳記／cast leadM null、leadF chung_choning、supportM chai_zanhoi、supportF kong_siying） |
| `index.html` BR89 註解 | 加第 17 對註解（同 film_206《油麻地夜班》同一筆債權，支線回響通告） |
| `index.html` `BR89_PATRON_OF_GIG` | 加 `gig_1991_tv_114:"credit_enc83_chai_patron"`（排 film_206 隔籬，註解寫明同 film_206 同一筆） |

守住：`chai_patron` 暖版閘（排除式）／冷版閘／對白／grants、`GRANT229_ENC79`「停一停」行、film_206 全部唔郁；genre 保持歷史傳記，唔發明新值；唔加 discoverNote（通知由 `mergeTriggerGigs` 何生 toast 包辦）；舊檔唔 crash。

## 2. 設計判斷（已定）

① 齊只係 supportM 配角格——接受。SPEC §3.6B 只要求「電視劇主角／古裝劇通告｜高級」——主角指玩家崗位，tv_114 玩家係男主角、高級、電視劇，三項全中；v316 駱前例更弱都收咗（rec_112 cast 係 null）；戲內關係就係提攜關係。② 歷史傳記 genre 計古裝劇：全庫 27 個 genre 值入面根本冇「古裝」呢個值；歷史傳記（6 張）就係年代劇桶，同時包古裝同民初，正正就係 SPEC 齊定位「古裝／民初劇」；為一張 gig 發明新 genre 值會斷 genre 分類。

## 3. 計數

- 庫維持 306 張；trigger 35→**36 張**、credit 24→**25 張**（BR89 17＋通用 8）。
- BR89 映射 16→**17 對**。
- 1991 秋電視高級開放板通告 1→**0 張**：tv_114 轉 trigger 閘，tv_210 本來已經 fame 閘（fameMin 40）——D-4／D-11 既定機制，唔係回歸（同 v316 1992 春唱片中級 6→5 一樣）。
- `index.html` 淨 +2 行（47283→47285）：BR89 表頭註解 ＋1、tv_114 映射行 ＋1。

## 4. 測試

新檔 `tests/test_r317_chai_echo.js`，22 項全 PASS：
- (0) 靜態：庫 306、trigger 36／credit 25、BR89 17 對逐對啱、tv_114 tag＋trigger 齊、其餘欄位逐項對照唔郁、chai_patron 兩閘唔郁、film_206 唔郁、1991 秋 TV 高級開放板 0 張。
- (1) 唔持債 → tv_114＋film_206 都唔開；持其他債（駱）→ 唔開。
- (2) 持齊債 → 兩張雙雙上板（`triggerGigOn`／`br89GigOn`）；季節窗：1991-07-01 未入窗、1991-09-15 可見（秋 span [9,11]＋提早 60 日）。
- (3) 殺青邊張，另一張自動落板（redeemedBy）；人情卡「可以換」出齊《油麻地夜班》＋《亂世將軍傳》兩張名。
- (4) GRANT229 共存：`chai_choice`「停一停」唔使持債照派 tv_114（`grant229Record`／`grant229DeliverOne` 全程唔讀 `triggerGigOn`）；「唔出聲」照派 tv_207。
- (5) 舊檔唔 crash（無債權／無 mockCredits／絕響債權）。

舊斷言同步（計數 35→36、credit 24→25、BR89 16→17 對）：
`test_gig229_trigger.js`（T0／T8／T10＋BR89_EXPECT）、`test_gig229_pack.js`（P7）、`test_br89_logic.js`（H1＋EXPECT13）、`test_r5_283_logic.js`、`test_r5_284_logic.js`、`test_sideline158_logic.js`（BR89_EXPECTED）、`test_sideline273_logic.js`、**`test_sideline274_logic.js`**（A1／A2／D1——A2 例外擴充：齊 chai 同駱 lok 一樣，同一筆債權兩張兌現 gig；D2 標籤同步）、`test_r316_lok_echo.js`（EXPECT16→EXPECT17）、`test_nat92_logic.js`（E0 MAXED 36 張）、`test_gig291_winter.js`（標籤）。

**附帶發現**：brief 只列咗 gig229_trigger＋r316 兩檔，但 suite 首跑揭出另外 8 檔寫死舊計數（pack／br89／r5_283／r5_284／sideline158／sideline273／sideline274／nat92）＋gig291 標籤，全部已同步。A2「每筆債權只兌現一張」前提而家對齊 chai 例外（同陸 luk、駱 lok 一樣）。

靜態釘行漂移：`qa317/resync317.py`（difflib 核實純漂移，鏡 v316 寫法）resync 咗 gift185／tang171／tang173／rom176／travel114 五檔。教訓：resync 腳本唔好照抄上一版嘅舊基數——v317 基線 DEF 已經係 42492（唔係 v316 基線嘅 42490），WRAPPER 29105，rom176 釘行 40724／41074／42377／42533；第一次跑喺 check() 嗰陣捉到，修正後重跑先完成。

## 5. Suite／落地

- 全套：**TOTAL PASS 380 FAIL 9**（基線 379／9，＋1 係新測試檔；9 項 FAIL 全部已知 pre-existing：flash51／slot50／soft_tip_111_restore／start53／weave43／44／49_static／wf5_87／wrap38）。
- `qa296/derive296.json` suite 再生嗰份已還原，唔入版。
- Main HEAD：`681b91d`（內容 commit 同上）
- Pages：index.html md5 `2f49cfa2e3880e15fd9d007ec3c0d95f`／4,700,136 bytes，v317 標記在位（2 處）

## 6. 唔包（另票）

齊 patron 閘改嚴格版（暖版閘排除式 vs sideline280 嚴格版 chai_truth_change＋chai_try_new 脫鈎）——v318 之後另開票，唔摻入 v317。
