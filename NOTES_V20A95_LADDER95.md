# v20a95 LADDER95 結局梯擴充 — NOTES（定案）

日期：2026-11-11。基底 v20a94（6dc51e9，5,360,588 bytes／sha256 02e0803c…）；本包主檔 5,386,704 bytes。
規格：`~/workspace/linji-ending-ladder-draft.md`（梯表）＋用戶 2026-11-11 12:37 四項拍板。唔改 SAVE key／softRev／?v=；唔郁通告數據、感情軸、去留軸、E6/E7 觸發、E4 救回門檻。

## 接線圖（現行 → 本包）

- 判定入口不變：`resolveEnding410(st, opts)`（純函數、唯讀）→ `ending410AfterEveChoice` 寫 `S.ending410` → `showEndingSummary410／endingSummaryHtml410` 呈現；鎖定走 `ending78Gate`（不變）。
- 現行判定（本包前）：E1（聲望≥60／信用≥55／雙軌≥125／負標籤≤1）→ E4 → E2 → E3 → E5 → E0；E6 只認 opts.quit。
- 本包判定次序：E6（opts.quit，不變）＞ E1（收緊＋質性閘）＞ E4（不變）＞ SS 一線巨星 ＞ FK 影壇天王 ＞ TK 電視天王 ＞ SK 歌王 ＞ GH 金牌司儀 ＞ CK 喜劇泰斗 ＞ AK 動作巨星 ＞ ID 人氣偶像 ＞ CR 實力派演員 ＞ E2（不變、下移）＞ E3（條件不變＋變體）＞ E5（不變）＞ E0。
- 新數據：累計計數器 `S.careerStats95`（見下），判定經 `careerStats95Of(st)` 唯讀取得（有存檔計數器用存檔；冇就即場由 wrapHistory 衍生，唔寫入）。

## 累計計數器 careerStats95

結構：`{ total, byMedium:{film,tv,music,variety,ad}, leadByMedium:{…}, tvLongLeads, genreIdentified, genreComedy, genreAction, backstageWorks }`。

- 寫入點：殺青結算喺 wrapHistory unshift **之前**加 `end95AddWrap(S, _g95, sh)`（_g95 按 sh.gigId 喺 GIGS 搵返張通告；時機係關鍵——end95AddWrap 首次會以當刻未含本單嘅 wrapHistory 衍生種子，遲咗入會雙計本單；結算點本身一單一入，唔另做去重）。
- 回填：`normalizeSaveObj` 加一行——舊檔載入嗰陣冇計數器就以 wrapHistory 衍生種子寫入存檔物件。
- **回填口徑同局限（唔扮全）**：wrapHistory 上限 30 條——舊檔升級前做過超過 30 單嘅玩家，計數器種子只數到最近 30 單，更早嘅作品數唔返。所以舊檔玩家嘅媒介／擔正／片種計數係**下限**，唔係全史；新局（本包後開局）由第一單起全計，先係完整口徑。判定唔會因此 crash：缺失一律當零／衍生值。
- 分類（`end95ClassifyWrap(gig)`，同 v94 press94 口徑銜接）：
  - 媒介：type 電影→film、電視劇→tv、唱片通告／唱片→music、綜藝→variety、廣告→ad。
  - 擔正（lead）：roleScale ∈ {film_lead_big, film_second_lead, tv_lead_long, tv_lead, tv_second_lead, music_lead, ad_lead}，或 roleLabel／標題命中 PRESS94_STRONG_NAMED（主角|男主|女主|主演|主唱）；含「替身」恆唔計（跟 press94）。rec_album／mtv 等模糊帶淨靠標籤命中先計擔正。
  - 電視長劇擔正：tv 擔正 且（scale=tv_lead_long 或 totalDays≥15）。
  - 片種：先 genreLabel／genre（真標籤，唔計同媒介名一樣嗰啲佔位值）——含喜劇/諧/搞笑/笑片→comedy、動作/武打/警匪/江湖/槍戰/武俠/功夫→action、其他真標籤→other；冇真標籤先以 workTitle＋title＋roleLabel 關鍵字補（笑/喜劇/諧星/搞笑…→comedy；武打/武師/功夫/槍/警匪/江湖/劍/拳…→action；兩邊同中就唔計）。
  - 幕後工：roleLabel／genre 命中幕後關鍵字（幕後/後期/製作/編劇/剪接/場記/副導/統籌）計 backstageWorks（E3 變體用）。

## 片種標籤覆蓋率（離線全池 475 張實測，audit93 pool）

- genreLabel 真標籤：153/475（32%）——comedy 25、action 14、other 114；其餘 208 張冇標籤、114 張係佔位（值＝媒介名）。
- 關鍵字補後可辨識：182/475（38%）；電影＋電視子集 95/235（40%）；genre 同關鍵字衝突只 3 張。
- 對判定嘅影響：喜劇／動作佔比以「可辨識樣本」為分母（genreIdentified），唔係全部作品——如果用全部作品做分母，六成作品冇標籤，兩格事實上冇人入到。另設最低樣本 genreIdentified≥6 防 1/1=100% 刷格。專攻玩家自己揀工，佢嘅可辨識樣本會自然偏向所攻片種，佔比計法成立；代價係玩家睇唔到邊張工「計片種」，差邊瓣只會講佔比差幾多，唔逐張點名。

## 質性閘讀法（E1 三項＋各格專屬）

- 獎項：`awardsLog` 任一 entry 有 category outcome==="won"（E1①；頒獎 medium ∈ film/tv/music/ad）。歌王「音樂獎」：medium==="music" 且 outcome won 或 nominated（跟草稿「提名／得獎」）。
- 主線鏈完成（E1③，任一即可）——按既有鏈收尾標記：
  - A：`S.wf3.luSettled`（替工殺青收割）或曾持有 credit_wf3_lu_team；
  - B：`S.wf3.liaoHarvestDone`（收割結算，含過期收尾）或曾持有 credit_wf3_comedy_crew；
  - C：C15 done ＋ intel_mak_injury（知情替身抉擇線行完）；
  - D：`S.wf3.yipCreditDone` 或 `S.wf3.yipEchoDone`（葉敏芝疑雲線收尾）；
  - E：flag_gao_ending_break／respect／stay 任一（高俊傑線結局旗，v89 已接入結局呈現）；
  - F：flag_stay_mind 或 flag_leave_mind（鏈 F 第 4 拍去留抉擇已作）。
  「曾持有」以 mockCredits 現存或 favorLedger.counted 已登記為準（帳本係持久登記，唔會因兌現而消失）。
- 彭少祺線進展（GH）：S.stars.pang_siu_kei.fav ≥45（T3 拍檔段）或曾持有 credit_enc84_pang_patron（T4 提攜・司儀引薦）或 C10 done（N11 慈善秀後台同佢圓場嗰幕）。
- 武師班底子（AK）：S.trainCount.train_stamina ≥5（武師班上滿一級、入二級；級別由堂數衍生，跟 LEVELS75 口徑）。
- E3 變體（只分呈現）：人情總量（`endingFavor410` total＝settled＋持有中 favor/debt/intel 債權數）≥5 → 製片老闆；否則電影作品數 ≥ 電視作品數 → 大導演；否則 → 金牌監製。

## 相鄰規則（跟新梯上下格計）

- 保留：E2⇄E3 前夕分流（to_backstage／to_support，條件同舊制：雙合資格或差少少）。
- **移除：E4→E3 轉幕後選項**。舊梯 E4 同 E3 係相鄰格，新梯兩者之間隔住成段中段梯（SS＋9 格＋E2），按拍板③「相鄰跟新梯上下格計」唔再算相鄰；E4 嘅前夕分支保留其內部 rescued／sunk 兩版（債權門檻不變）。呢個係新梯嘅必然結果，唔係刪內容：E4 玩家本來就行唔到「差少少幕後」嗰種狀態（信用 <30 + 幕後條件差少少，兩件事好少同場）。
- leave_follow（去留軸）同 quit 選項不變，唔屬事業格移動。

## 第三年頒獎截斷

結論：**E1 唔係結構上不可達**，唔使大改結構。頒獎禮按季行（每年四季都有屆），質性閘①（攞過 ≥1 個獎）可以喺第 1、2 年任何一屆，同第 3 年春／夏／秋嗰屆攞到；俾結局閘（C17，1992 冬）截斷嘅只係第 3 年冬季嗰一屆——嗰屆同 C17 撞期，全弧驗證第三輪已有實證（第三年常規頒獎被截）。即係玩家有成兩年幾嘅頒獎機會去滿足閘①；真正嘅分隔線係「攞獎」本身嘅難度（實力判定贏線 0.82＋質量加權，v62 定版），唔係冇獎可攞。按任務口徑記錄低，唔改頒獎／結局閘結構。

## 校準記錄

方法：確定性狀態構造（fame/credit 以 dualTrackNumbers 公式反推：stage/acting/stress＝0、credit＝round(fame×0.5)＋delta）＋`tests/test_ladder95_logic.js` 弧斷言（39 項全 PASS）＋真 UI 實駕一局（見下）。弧嘅玩法強度定義照 fullarc3 實測錨，冇為 PASS 改過。

**第一輪（草稿起步帶原值）——全數命中，冇調整**：

- 弧 1 正常強弧（fullarc3 正常弧實測錨：fame 181／credit 210／雙軌 391；作品 95＝film 30／tv 28／music 20／variety 10／ad 7；擔正 film 2／tv 2／music 1；片種可辨識 34；只有提名冇攞獎；主線鏈 0）→ **SS 一線巨星** ✓（唔再自然上 E1，同拍板「正常好表現多數落中段」一致）。差邊瓣首句正確指出差個獎。
- 弧 2 近乎完美弧（fame 190／credit 215／雙軌 405；攞獎 1（電影）；擔正 film 3／tv 2／music 1；鏈 B 完成）→ **E1 天王接班** ✓，差邊瓣回「冇差」句。
- 弧 3 電影專長弧（fame 120／credit 115／雙軌 235；作品 70、電影 42＝60%、電影擔正 3；冇獎冇鏈）→ **FK 影壇天王** ✓。
- 分科探針全中：TK（電視 40/72＋長劇擔正 2、雙軌 230）、SK（唱片 36/65＋音樂提名、雙軌 230）、GH（綜藝 30/55＋彭少祺好感 50、雙軌 190）、CK（可辨識 30、喜劇 17＝57%、信用 95、雙軌 200）、AK（可辨識 28、動作 15＝54%、武師班 10 堂、雙軌 200）、ID（聲望 75／信用 45）、CR（信用 70／聲望 45）。
- E1 邊界：雙軌 350＋全閘 → E1；349＋全閘 → SS＋差邊瓣「差 1」；405＋獎＋擔正但鏈 0 → SS＋主線句；405 但得一種媒介擔正 → SS＋擔正句（SS 排專長格之前，係設計原意：未齊質性閘嘅高雙軌先落頂格）。
- 守衛探針：片種可辨識得 3（喜劇 3/3）→ genreMinSample 擋住，唔入 CK，落 E2 ✓。E3 變體三態（電影多→大導演／電視多→金牌監製／人情總量 6→製片老闆）✓。
- 計數器：衍生 7 條履歷分類全對（替身唔計擔正、場記計幕後）；addWrap 種子＋累加唔雙計；舊檔冇計數器 resolve 唔 crash 且用衍生數；resolve 純函數不變性 ✓。

**定案數字＝草稿起步帶原值，逐項零調整**：E1＝聲望 ≥70／信用 ≥65／雙軌 ≥350／負標籤 ≤1＋質性閘三項；SS＝雙軌 ≥300／聲望 ≥60／信用 ≥55／負 ≤1；FK／TK／SK＝雙軌 ≥200＋佔比 ≥50%＋各自擔正／獎項條件；GH／CK／AK＝雙軌 ≥180＋佔比 ≥50%＋各自條件；片種最低樣本 6；ID＝聲望 ≥60＋信用 30–54／負 ≤2；CR＝信用 ≥55＋聲望 35–59；E3 變體人情線 ≥5。

## 測試與驗證

- 新測試：`tests/test_ladder95_logic.js`（39 PASS）＋`tests/test_ladder95_static.py`（ALL PASS）；反證：兩者對 v94 基線 index 都 FAIL。
- 有意改版嘅舊測試（原位註明理由）：`test_weave410_logic.js`（舊 E1 命中態→新梯 E2；E4 前夕分流斷言反轉＋流程改行 natural；leave_follow 前提改用真 E1 狀態）、`test_weave410_static.py`（E4 分流分支改斷言已移除）、`test_conseq61_logic.js`（harness 補抽 LADDER95 函數——conseq61PresentForcedEnding 內部 call resolve，冇補會俾 try/catch 吞成假 FAIL；生產環境同 scope 冇呢個問題）、`test_poster85_static.py`／`test_ux68_static.py`（主檔上限按慣例原位更新：本包有意增長至 5,386,704 bytes）。
- 全套 A/B：基線 121 檔 109 PASS／12 FAIL（環境性）；本包 123 檔 111 PASS／12 FAIL——逐檔 diff 只多咗兩個新測試檔（同 PASS），**零回歸**。
- 真 UI 實駕（本地鏡像＋Playwright，構造 SS 弧存檔）：進度頁第 17 幕〈三年收科〉已開放→播呢幕→25 步推到前夕抉擇（只有順其自然／收山，冇 to_backstage ✓）→揀順其自然→SS 事業場景→手帳總結：稱號卡「一線巨星・未說出口的人」、雙軌 391、回望嗰一格兩句（獎／主線）齊；`S.ending410.career==="SS"`；pageerror 0、console error 0。證據：`verify95/`（06_map／09_story_play／10_eve_choices／11_ending_scene／12_summary.png＋drive95h.py）。註：開場有一張基線已有嘅缺圖 404（assets/story/era_stars/lok_gasing_bust_default.png，v94 同 v95 repo 都冇呢個檔，同本包無關）。
