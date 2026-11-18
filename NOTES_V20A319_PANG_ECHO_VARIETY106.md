# NOTES_V20A319_PANG_ECHO_VARIETY106

## 任務
彭少祺支線回響通告——新開一張 1992 秋中級綜藝主持 gig `gig_1992_variety_106`《星光慈善夜》，
補 SPEC §3.6B 彭行最後一個缺口（SPEC.md:784：彭少祺《有人聽》｜司儀／綜藝主持通告｜中級）。
§3.6B 9 張表至此全部覆蓋（廖／顧／麥／魏／鍾／程／駱 v316／齊 v317／彭 v319）。

## 為何開新 gig（四個候選比較，偵察員決定，parent 親查核實）
- (a) variety_104《歡樂大騷》升中級：唔要。季窗 1991 夏更早，T4 玩家趕唔切；要成張重寫
  req／pay／fame，郁 1991 夏綜藝矩陣；佢係 GRANT229「遲咗」即派 gig，遲到玩家無債權都會
  攞到 credit-gated 回響 gig，語義錯；彭唔喺 cast 入面。
- (b) variety_203《台慶大騷》崗位助理→主持：唔要。成條弧（Beat 2、風聲卡、收科對白 L1558）
  寫明係「助手位」，債權 line 寫「畀個機會佢企上台試下」；改佢等於推翻敘事核心。
- (d2) variety_103《樂善之夜》加 tag＋trigger：唔要。季窗一樣係 1991 秋死窗，升完都係冇人
  見到；仲會食埋 1991 秋綜藝唯一一張開放中級（開放板中級 1→0）。
- (d1) 接受 variety_203 做回響、結案唔落地：唔要。8 張已覆蓋回響通告玩家崗位全部對版，
  淨係彭唔對版；草稿「唔係缺口」講嘅係債權兌現，唔係 §3.6B。
- (c) 開新 gig：揀呢個。唔郁任何現有 gig、唔郁矩陣、唔郁 GRANT229、唔郁草稿敘事；
  1992 秋係玩家實際持有債權嗰陣，仲填補咗 1992 秋綜藝中級空位（開放板中級 0 張）。

## 實裝
1. `content/gigs_new.json` 加新 gig `gig_1992_variety_106`（排 `gig_1992_variety_105` 之後，
   id 順序）：《星光慈善夜》慈善晚會主持；綜藝／中級／作品／genre 晚會／1992 秋／2 日／
   roleScale variety_special／req 台風 45＋魅力 30／pay [200,240]／fame [28,45]／hard 0.5／
   loc tvb_kowloon／director 晚會監製／host null／guests [pang_siuki, so_jiyan, gu_mingfai]／
   segments [慈善拍賣、歌舞表演、捐款公佈]；`storyKeys: ["pang_siuki"]`＋
   `trigger: {kind:"credit", creditId:"credit_enc84_pang_patron", creditOwner:"彭少祺"}`。
   數字逐項照抄標板 `gig_1991_variety_103`《樂善之夜》（已驗證嘅中級主持標板）。
   文案按 variety_103 體例寫，書面語，彭少祺做嘉賓；roleLabel 含「主持」二字（自動入
   `isPangCharityGig158` 司儀類，將來 G-PANG-1 會自動覆蓋）。
2. `index.html` BR89 映射加第 18 對（排 variety_203 隔籬，同行）：
   `gig_1992_variety_106:"credit_enc84_pang_patron"`，註解寫明同 variety_203《台慶大騷》
   同一筆債權、支線回響通告；表頭註解加 v20a319 一行（第 18 對）。
3. 守住：variety_104／203／103／102（稀有，唔降級）、`pang_patron` 閘／對白／grants、
   GRANT229 彭行全部唔郁；舊檔唔 crash。

## 計數
- 庫 306→307 張；trigger 36→37（credit 25→26，BR89 18＋通用 8）；BR89 17→18 對；
  司儀類通告（綜藝＋roleLabel 含「主持」）5→6 張；1992 年通告 80→81 張；
  中級 75→76；作品 179→180；唱片／綜藝作品無 cast 57→58；press94 named 170→171（新 gig 係 named）。
- 1992 秋綜藝開放板維持 3 張稀有（102／201／203），中級開放 0→0（新 gig 係 trigger 閘，
  唔入開放板；D-4／D-11 既定機制，唔係回歸）。
- index.html 淨 +1 行（47285→47286，BR89 表頭註解 ＋1；映射對同行加，0 行）。

## 測試
- 新檔 `tests/test_r319_pang_echo.js` 29 項全 PASS（靜態／唔持債唔開／持債雙雙上板／
  季節窗／殺青邊張另一張落板／H 卡出齊兩張名／GRANT229 彭行唔郁／舊檔唔 crash）。
- **brief 更正**：brief 原寫季節窗「1992-08-31 未入、09-15 可見、1992-12-15 照見」同 live 函數
  `gigSeasonEarlyVisible88` 唔符（秋 span [9,11]＋提早 60 日：提早窗由 1992-07-03 起，
  季尾 1992-11-30）。實測：1992-07-01 未入、1992-08-31 已入提早窗、1992-09-15 可見、
  1992-12-15 已過季尾唔見。測試按函數實測寫，唔跟 brief 原文。
- 舊測試同步（寫死計數，唔係回歸）：gig229_trigger（T0／T8／T10＋BR89_EXPECT）、
  gig229_grant（T0）、gig229_pack（P0／P1／P2／P7／P8）、gig229_press94_advice（A10）、
  gig229_years（A6／C0／C1）、gig291_winter（W0）、nat92（F2／E0）、r286（B1／B6）、
  r299／r302／r304／r305／r306／r309／r310／r311／r312／r313／r314／r315／r318（S／C 庫總數）、
  r307（D）、r316／r317（gig_count／trig／EXPECT18）、br89_logic（H1＋EXPECT13）、
  sideline158（T1 司儀 matcher＋T8 BR89_EXPECTED）、sideline273（d）、sideline274（A1／A2／D）、
  r5_283／r5_284（(0) 計數）。另加：sideline274 A2 彭例外（credit_enc84_pang_patron 兩張
  variety_203＋variety_106，同 lok／chai 前例）。
- Static resync：`qa319/resync319.py`（difflib 核實純漂移）resync 咗 gift185／tang171／tang173／
  rom176／travel114 五檔（總行數鏈尾 ＋v319 +1；openLoc DEF 42494→42495；WRAPPER 29107→29108；
  COUNT／FREE 31 處 ＋1）。**教訓**：v319 插入點係舊 L26703（v317 行尾 */ 移去新行），
  唔係舊 L26702——第一次跑 resync 嗰陣用錯邊界，difflib 映射 None 先捉到；下次先對返
  git show 嘅舊行再定邊界，唔好憑記憶估。`qa296/derive296.json` 已還原，唔入版。

## 唔包（另開票）
- 草稿 L1545 提案（n17 好收尾第二朝派 variety_203）未實裝，live GRANT229 pang_n17 派嘅係
  ad_107／tv_301——另開票。
- G-PANG-1（慈善債權兌現渠道）仍 open；新 gig roleLabel 含「主持」會自動入司儀類，
  將來 G-PANG-1 會自動覆蓋佢。
- 陸柏言行（SPEC 表有佢、計數同生成映射冇佢）要先拍板先開票。

## §5 落地實數（待填）
- Main HEAD：
- Suite TOTAL：
- Pages index.html md5／bytes：
