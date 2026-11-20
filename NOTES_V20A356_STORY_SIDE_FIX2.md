# v356 NOTES — 支線＋感情線複檢 (a) 類證實矛盾修復（玩家面）

Base: v355 (main `df8b792`)。Suite: 398 PASS／9 FAIL（同基線一致，九項 pre-existing：flash51／slot50／soft_tip_111_restore／start53／weave43_static／weave44_static／weave49_static／wf5_87／wrap38）。

來源：`~/workspace/linji-story-review-side/verification.md`＋`REPORT.md`（GPT-6.2 支線＋感情線複檢 220 項；v355 修嚴重 7 項，今次修餘下 (a) 類證實矛盾 69 項）。唔修：系統性旁白廣東話口語化約 50 處（成層問題另票）、(b) 待潤飾類、soft 層鄧麗萍清理、4 項文風取捨、1 項部分證實（s7 A8 tang stub 已知設計）。

## 修復 69 項（按核實表編號）

**rival_mentor（19）**：s1 A1（ko meet 選項 label 改接過通告當面警告）、A2（hakfan push2 簡介補導演叫回廠）、A3（hakfan ending「第一次不以家世開場」→「這次不再提家世」）、A4（化妝間→走廊 setting＋簡介）；s2 A1（tsijun crisis B0 前加路線中立交代句：兩張通告點揀都留低個位）、A2（fong ending「傷後復出」→「約阿偉見面」）、A3（「再跳過」→「再練過」＋cold label/notes「不再做替身」→「不再跟班底」）、A4（tsijun ending setting 後台走廊→酒會＋B3/選項改應酬講法）、A5（push2 B2＋ending B1 換講法，保留 meet 原句）；s3 A1（tong ending 標題「教室窗邊的去留」→「天台的去留」）、A2（簡介改中立＋B1「你留得低」→「你今日企喺呢度」）、A3（ho meet setting 改何生事務所走廊人龍）、A4（ho push2 setting 改事務所枱面通告）、A5（C_ho_ending_complete label「留在穩陣線」→「跟他走穩陣線」）、A6（ho ending setting 補頒獎禮散場後簽約剛完）；s4 A2（lei crisis phase P1.5→P3）、A3（簡介「阿偉拒絕後」→「阿偉怎樣表態，雷勁都沒有即刻發惡」）、A4（C_gao_meet_safe notes 改「高文瀚記住了這個答案」）、A5（gao push1/push2/crisis B2 刪「呢個位由我決定」，ending 保留反轉）。

**lan_xu（5）**：s5 A2（lan meet 簡介刪派牌，JSON＋WF2 覆寫同步）、A4（lan ending B8「嗌下一組埋位」→「收拾通告牌」）、A5（B0 加第二句：人事部嗰張紙冇簽，留低做場記）；s7 A5（xu meet B3 改中立只報名字＋B4 刪「幾機靈喎」＋polite notes 補贊助細節；B3 其後加長補 wf2 字數底線）、A6（xu ending B6 刪退錶＋回禮句改懸置，尾句補字數）。

**vera_hiu_choi（4）**：s7 A1（C_choi_meet_b notes 改「采兒覺得他答得太圓」）、A2（C_choi_push1_b notes 改只畀方向冇畀料）、A3（C_choi_ending_he notes 加「兩個人講明了，正式拍拖」；rom159PrepareNode public/quiet notes 同步加「兩個人正式拍拖」）、A4（C_choi_ending_be notes 改始終冇行埋嗰步）。

**yip_so（5）**：s8 A1（C_yip_crisis_clear notes 同步＋rom159PrepareNode 新增 R_yip_crisis 分流：flag_yip_leaked 在位時換「死口唔認」變體，rel_yip −1，唔寫清白旗）、A3（yip ending B0 刪「由第一日佢企出嚟擋記者」）、A5（so ending when 1990秋→1990冬）、A6（so meet B2「沒有人讓開」→「記者沒有散開的意思」＋B4 換寫法）、A7（so ending B2＋B4 換收尾，同 yip 分開）。

**覆寫表／prepareNode（4）**：s6 A1（V158 覆寫 hiu meet 簡介「兩人約好交換消息」→「她想跟阿偉交換消息」）、A6（enc158PrepareNode family_go 分支補 synopsis）、A7（ending 加 hiu_lost_role 變體 beats[2]，且非 deal_signed）；s7 A3 見上。

**ENC 巧遇表（32）**：s9 A1（lok foreshadow 換茶水間場面）、A2（heart label「靜靜聽他彈完整首」→「靜靜聽他彈完寫好嗰半首」＋A/S 句＋enc79ChoiceFx 關鍵字＋GRANT229 key 同步）、A3（lok_cover 勸唱回應改即時）、A4（lok_patron_cold 開場後巷→錄音室調音台）；s10 A1（pang_n17 回憶改大騷後台門口臨記堆）、A2（pang T0 改「記得嘅」版）、A3（pang_intel label 刪「／唔去」）、A4（pang_finale_cold 開場改阿偉先到）、A5（pang_finale 換句，patron 保留原句）、A6（kong T1 改中立）、A7（shum T4 換句）；s11 A2（ngai T1「買汽水嗰個」→「後巷嗰晚嗰個」）、A5（heartCold 換講法「你嗰晚未做到」）、A6（wu T4 改陪對戲企定）；s12 A1（chai heartCold 第二次合劇本→「拿起劇本」）、A2（chai_choice label→「婉拒畀意見，他是大佬，自己會想」＋回應「你唔肯講，都係一種答案」＋GRANT229 key/reason 同步）、A3（chai T4 換句）、A4（chai_finale＋FRAME wrap 刪「殺青喇」改「行到今日，你企嘅位，已經唔係企後面嗰個位…」，wrap_safe 同步改）、A5（mak_foreshadow 刪「第一次見識」）；s13 A1（liu_clash 選項 lines 改真企廖，label/flags/關鍵字唔郁）、A2（共通尾句改「他說完，不再出聲，只望著阿偉，等他表態」）、A3（liu T1「笑到拍枱」→「茶餐廳嗰個後生仔」）、A4（luk first choices[2] N 句補執劇本動作）；s14 A1（ching T1 刪「仲遞水俾我飲」）、A2（ching_e4 選項 A/S 換寫法）、A3（ching_after_train「開始半夜練唱」→「練得更密」）、A4（ching_patron「陣間」→「到時」）、A5（yip_stand「被他頂」→「被她頂」）；s15 A2（so first choices[2] A 句加「（門關上之前，阿偉開口）」）、A3（gu first 插入 N 句哼舊歌）；s16 A2（chung_patron_cold 刪「沒有再說話」）、A3（chung_f_clue choices[0] 前插茶水間追問 N 句）。

**判斷唔修（2 項交代）**：s5 A3 v355 已處理（B6 懸置＋B8「等佢接」），唔再改；s6 A8 曉晴 JSON 舊稿 BE 拍拖句屬死數據（玩家面以 V158 覆寫為準，JSON 旗標冇 live 讀者），唔修。

旗標邏輯只郁 s8 A1 分流（跟核實表修法）；年份字串／數值／SAVE key／softRev 冇郁。index.html 淨 +20 行（47,420→47,440）：WF2 B0＋1／rom159 葉 crisis 分流＋12／enc158 synopsis＋1／lost_role＋4／顧哼歌＋1／鍾追問者＋1。

## 測試改動（resync，邏輯斷言唔郁）

- Python 釘行：gift185／tang171／tang173（總行數 47440、openLoc DEF 42660）；tang152（3 釘行 +1）；rom159（6 line_has＋全佳行；rival 精確替代斷言：13 處 dict live 值更新＋_FIX356 14 處＋crisis B0 中立句 prepend）；rom159_yipso（so ending 1990冬）；rom176（5 釘行）；text125（3 釘行）；travel114（COUNT/FREE/DEF/WRAPPER 按段 shift，逐行核實 openLoc( 錨點）。
- JS 釘句：r304（魏 heartCold＋駱 patron_cold）、r305（齊 wrap＋駱）、r306（WRAP_OLD/WRAP_SAFE 常數）、r308＋sideline273（駱 heart label）、r309（pang_n17 回憶句＋finale_cold 開場）、r310（ching_e4 A/S）、r312（pang_intel label＋finale_cold）、r317＋r321＋r318（GRANT229 chai_choice key「婉拒畀意見」＋wrap_safe）。

## 實駕抽查（Playwright，`~/workspace/linji-drive356/`）

- CHECK1 共用 beats 分支（s8 A1）：播種 flag_yip_leaked → StoryPlay 播 R_yip_crisis，選項見「死口唔認」唔見「自證」（截圖 01）。
- CHECK2 地點一致（s3 A3）：A_ho_meet setting＝「何生事務所走廊，阿偉站在等見監製的人龍最末」，正文渲染一致（截圖 02）。
- CHECK3 ENC opener（s11 A2）：enc79BuildScript 非 page global，改用 r309 同款抽取 harness 函數級真跑——T1 opener 數據層＋build 層雙證「後巷嗰晚嗰個後生仔」在位、「買汽水嗰個」清零。
