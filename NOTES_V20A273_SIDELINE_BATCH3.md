# v20a273 支線補完第三批 NOTES

- 基線：main `f2d3dfb`（v272，suite 337／9）。本版 suite **338／9**（新檔 `tests/test_sideline273_logic.js` 50 項；九項 FAIL 全部係已知 pre-existing：flash51／slot50／soft_tip_111_restore／start53／weave43_static／weave44_static／weave49_static／wf5_87／wrap38，零回歸）。
- index.html 45,466 → 45,500 行（淨 +34）。SAVE key（`starVolunteer_map_v19w`）、softRev（`s107`）、產品 `?v=`（`v20a10`）不變。
- 工作期間 v272 落地（main `f25df08` → `f2d3dfb`），分支已 rebase 上新 main，零衝突；resync 在新基線上重做一次（見下文）。
- 攻略側 1.16／1.18／1.19 未掂（parent 負責）。`~/MEMORY.md` 未改。

## (a) 顧明輝 heart fx 關鍵字 bug——做咗

- `heart:gu_mingfai` fx 由 `has("天光")?3:1` 改做 `has("天亮")?3:1`，對返 live DLG label「陪他坐到天亮，不出聲」（語言重寫改咗 label，fx 關鍵字漏改）。揀呢個選項而家 fav +3（之前錯加 +1）；另一選項「勸他戒賭，重新來過」維持 +1。
- 舊測試同步 live label：`tests/test_enc83_logic.js` L159（名「天光」→「天亮」）、`tests/test_sideline271_logic.js` L157（同上）。
- 新測試加回歸 guard：舊廣東話 label「陪佢坐到天光，唔出聲」而家只加 +1，證明 fx 跟 live label，唔跟舊詞。

## (b) 顧 Beat 2 抉擇實裝（WORKORDER 1.14）——做咗

### 出現位置設計（決定）

- **抉擇落喺現成 `gu_tease` 天台 beat**（`ENC83_DLG_gu_mingfai.beats.gu_tease`），唔開新 beat。原因：draft 嘅天台抉擇收尾句，live 已經有——顧嘅警告「嗰樣嘢，你一世都唔好掂。」（`gu_tease` lines 尾句）；抉擇就係玩家對呢句警告嘅回應，位置同語境完全對得上。
- 閘不變：1991 年、tier ≥2、N10 未完（`gu_tease` 本身嘅 when）。PickBeat 排 `gu_loan` 之前（同一 tier 段內次序）。
- 兩選項（寫旗，行 v269 機制 B+，`opt.flags` → `S.flags`）：
  - 「應承他，自己一世都不碰賭」→ `gu_promise_clean`，fav +2，對白 A「明輝哥，我應承你：嗰樣嘢，我一世都唔掂。」／S「……你咁講，我信你。後生仔，唔好行我呢條路。」
  - 「問回他：「那你自己呢？」」→ `gu_ask_back`，fav +2，對白 A「明輝哥，咁你自己呢？」／S「……你問到我答唔到。呢個問題，我自己都問咗自己好多次。」
  - fav 兩邊都係 +2：WORKORDER 無寫 Beat 2 數值，分化靠旗＋分開即派，唔靠 fav 差。
- 即派分開：`enc79ChoiceFx` 返 `fx:"gu_promise_clean"`／`fx:"gu_ask_back"`；`enc79RunChoiceFx` 呼叫 `grant229RecordDraft(fx)`。DRAFT 表本身唔郁（佢係唯一映射；`GRANT229_ENC79` 表唔加行）。應承 → `gig_1991_rec_201`（卡拉OK影碟和音歌手）；問返 → `gig_1991_rec_207`（《電視劇金曲錄音》和音歌手）。兩張都係唱片通告／初級／1991；`dueDay = day+1`（聽朝何生電話，行 GRANT229 晨鏈）；一生一次（`grant229_recorded_` 旗防重派）。
- 後續讀取（WORKORDER 1.14 錨點原文，一字不改）：
  - Beat 3（`gu_loan` 開場）：有 `gu_promise_clean` → 插「你嗰日應承過我，今日我先敢同你開口。」（`beat:gu_loan_promise273`）；無旗唔插。
  - Beat 4（heart 交心）：有 `gu_ask_back` → 喺 heart 首句之後插「你嗰日問我，我自己呢——我答你唔到，而家我答你：我輸咗。」（變體 seg copy，唔改原 DLG）；無旗照開 heart，唔插。
- 兩處舊註釋已更新：`GRANT229_DRAFT` 頭註（唔再寫「遊戲未有呢個抉擇」）＋`grant229RecordDraft` 頭註（唔再寫「現時無呼叫點」）。
- `tests/test_gig229_grant.js` T2 舊斷言（「得定義＋註解，唔經任何 hook 呼叫」）已改做新現實：定義＋註解＋`enc79RunChoiceFx` 呼叫點（出現 3 次＋含 `grant229RecordDraft(fx)`）。

### 錯過特性（設計備註，唔使修）

- N10〈酒廊〉`when: "1989冬"`（顯示年；runtime YEARS66 SHIFT=2 → 玩家面 1991 冬）。如果玩家 1991 年內顧未到 tier 2 就先完成 N10，Beat 2 永遠錯過——同 `gu_foreshadow` 嘅 1991 限定窗口同一種軟錯過（soft-miss），唔係死鎖：Beat 2 兩個旗只影響讀返變體句＋兩張和音即派，唔閘任何結局／heart（顧 heart 本身無旗閘）。

## (c) 其餘六條線 code 側核實（PLAN §4–§9）——做咗（核實＋修 5 處同類 bug；草稿 Beat 樹未實裝，留跟進票）

### 關鍵發現：PLAN §4–§9「維持」係設計 verdict，唔係 code 存在聲明

- 六線草稿旗（PLAN §4–§9 Beat 1–5 抉擇旗，約 90 個）repo 0 命中，唯一例外 `chai_silent` 只係 `enc79ChoiceFx` 入面一個 fx token（1 處），無任何讀取。六線 draft Beat 1–5 抉擇樹 live 未實裝——同 v158／v269／v271 之前廖／顧／麥嘅狀態一樣。全面實裝係另一批跟進票，唔係 v273 範圍。
- 但 live 每線都有實裝骨架，全部在位：`first`＋`heart` DLG、ChoiceFx、beats（每線 ≥4 個，含幫手／交心／引薦 beat）、`GRANT229_ENC79` 無六線 beat 行（17 行即派表：初遇 9 行＋支線抉擇 8 行，分屬廖／顧／麥 4 個 seg，見 (d) M-1）。
- 1.18 勘誤 code 側無嘢：`gig_rec_02`／`gig_wf3_liao_stage` repo 0 命中（舊庫 gig，已隨舊庫死）。

### 逐線核實結果（對過嘅位＋結論）

| 線 | 對過 | 結論 |
|---|---|---|
| 駱家聲 | first／heart ChoiceFx（live label）、beats（lok_help／lok_e4grudge／lok_patron）、DLG、草稿旗 0 命中、GRANT229 行 0 | 骨架在位；修 2 處 fx（見下）；draft Beat 2b／3／4／5 抉擇樹未實裝 |
| 魏詠男 | 同上（ngai_help／ngai_repay／ngai_patron；ngai_meal $150 授債已在位） | 骨架在位；fx 全部啱；draft Beat 3／4 抉擇未實裝 |
| 齊鎮海 | 同上（chai_choice／chai_repay／chai_patron；`chai_repay` 係 N13-linked 回報 beat，唔係 draft Beat 5） | 骨架在位；fx 全部啱；draft Beat 2／3／5 抉擇未實裝；G-CHAI-3 已係「企邊嗰場風波」 |
| 彭少祺 | 同上（pang_help／pang_n17／pang_patron；G-PANG-1 渠道見 (d)） | 骨架在位；fx 全部啱；draft Beat 2／3 抉擇未實裝 |
| 鍾楚凝 | 同上（chung_review／chung_farewell／chung_patron；G-C2 忠告卡見 (d)） | 骨架在位；fx 全部啱；draft Beat 2／3 抉擇未實裝 |
| 程天諾 | 同上（ching_e4／ching_after_train／ching_patron） | 骨架在位；修 2 處 fx（見下）；draft Beat 2／3 抉擇未實裝 |

### 修咗嘅 5 處 fx 關鍵字 bug（全部同 (a) 一個 bug 類：語言重寫改 label，fx 關鍵字漏改／太闊）

1. `first:lok_gasing`：`has("撐")` → `has("好話")`。舊關鍵字對唔上 live label「出聲為他說句好話：這些歌是好聽的」——講好話嗰個選項錯加 +1（應 +3），連帶點頭／笑佢兩臂錯位。
2. `first:ching_tinlok`：`has("練到天光")` → `has("練到天亮")`，`has("遞支水")` → `has("遞一瓶水")`。三個選項之前全部錯加 −2（練到天亮應 +3、遞水應 +1）。
3. `first:so_jiyan`（蘇芷茵，v159 新線，PLAN §4–§9 覆蓋範圍外但同一 audit 捉到）：`has("護住")` → `has("護著")`。護著嗰個選項錯加 −2（應 +3）。
4. `heart:lok_gasing`：`has("聽")` → `has("彈完整首")`。舊關鍵字太闊——兩選項都含「聽」（「讚他那首歌好聽」有「聽」字），讚嗰邊錯加 +3；改精準關鍵字分返 +3／+1（全線 heart 一律首選 +3／次選 +1）。
5. (a) 顧 heart：`has("天光")` → `has("天亮")`（見上）。

### 脆弱但結果啱——留原樣，記低

- `heart:chung_choning` `has("出聲")`：靠「靜靜聽，不出聲」入面嘅「不出聲」子串命中，靜聽 +3 係設計意圖。字面脆弱，行為啱，唔郁。
- `beat:lok_e4grudge` `has("鬧")`：miss 咗「陪他一起罵」，但兩臂都係 +1，結果一樣，唔郁。

### 舊測試 label 同步（live label）

- `test_enc83_logic.js` L158：駱 label →「出聲為他說句好話：這些歌是好聽的」（名「駱撐」→「駱好話」）；顧 first label →「靜靜站在那裡，聽他哼完那段舊歌」。
- `test_enc84_logic.js` L168：蘇 label →「護著她進升降機，一句也不多說」／「讓開站到一邊，不阻礙別人工作」（名「護住」→「護著」）；L170：程三 label →「說自己當年怎樣熬：被人笑的時候，我也是練到天亮」／「靜靜遞一瓶水給他，不出聲」／「笑他的唱功：你唱那兩句真的不行」。
- 唔郁：`test_gig229_grant.js` L257–265／`test_sideline271_logic.js` L57／65／151／153 廖／麥 label——live 廣東話原文，已經 PASS。

## (d) PLAN §10 即派第一批 25 項——做咗（核實＋釘測試；G-L2 半完成留跟進票）

對位一律以 live `content/gigs_new.json` 為準；舊庫 gig id／tier／媒介唔照抄（v254 REUSE 決定咗 live 數值，同 draft 舊庫規格有出入嗰啲以 live 為準）。

| 項 | 狀態 | 證據 |
|---|---|---|
| G-L1 廖引薦 | 已在位（v229 B5／v254） | `gig_1992_film_103`《吉星笑哈哈》trigger `credit_enc83_liu_patron`；同優先 `gig_1991_film_103`（`credit_enc79_liu_priority`）分開兩張 |
| G-G1 顧引薦 | 已在位 | `gig_1992_rec_105`《當年情懷》唱片／中級／1992，trigger `credit_enc83_gu_patron` |
| G-G2 還錢開通告 | 已在位（v229 B7） | `br89GigOn` 第二觸發：`enc83_gu_loan_result===1` 無債權都開 rec_105；未還／無結果唔開；持債權本身都開；債權已兌現＋未還 → 落板 |
| G-M1 麥免試鏡 | 已在位（v158） | `favor158ChannelForGig`：持 `credit_enc79_mak_wuzhi`＋動作／武俠＋作品 gig → 渠道開；錯類別／無債權／已兌現 → 唔開 |
| G-M2 麥引薦 | 已在位 | `gig_1991_film_110`《鐵拳王》trigger `credit_enc83_mak_patron`（live 初級，唔係 draft 話嘅中） |
| G-LOK-1 駱引薦 | 已在位 | `gig_1992_rec_102`《硬漢柔情》trigger `credit_enc83_lok_patron`（live 初級，唔係 draft 話嘅高） |
| G-LOK-2 駱新寫抉擇 | 做唔到——草稿抉擇未實裝 | live 無「唱住先／企硬」抉擇 label；留 (c) 跟進票 |
| G-NGAI-1 魏引薦 | 已在位 | `gig_1991_film_111`《雪山雙劍傳》trigger `credit_enc83_ngai_patron`（live 初級，唔係 draft 話嘅高） |
| G-NGAI-2 刪 stub 債 | 已在位（v229 B7） | `debt_slot_ngai_01` repo 0 命中 |
| G-NGAI-3 餐飯第二重兌現 | 已在位 | `gig_1992_film_101`《武館風波》武打配角（電影／初級／1992）trigger `credit_enc83_ngai_meal`；餐飯債權由 `ngai_meal` fx（$150）live 授出 |
| G-NGAI-4 魏新寫抉擇 | 做唔到——草稿抉擇未實裝 | 同 G-LOK-2 |
| G-CHAI-1 齊引薦 | 已在位 | `gig_1992_tv_104`《滬上往事》trigger `credit_enc83_chai_patron`（live 電視劇／初級，唔係 draft 話嘅電影／中） |
| G-CHAI-2 齊新寫抉擇 | 做唔到——草稿抉擇未實裝 | 同 G-LOK-2 |
| G-CHAI-3 企邊寫法 | 已在位 | live L36996 早已係「企邊嗰場風波，台入面個個都睇風向…」；舊詞「站隊」0 命中 |
| G-PANG-1 彭免試鏡 | 已在位（v158） | `favor158ChannelForGig`：持 `credit_enc84_pang_charity`＋綜藝＋主持 gig → 渠道開；錯類別 → 唔開 |
| G-PANG-2 彭新寫抉擇 | 做唔到——草稿抉擇未實裝 | 同 G-LOK-2 |
| G-C1 鍾引薦 | 已在位 | `gig_1991_tv_108`《深秋情緣》trigger `credit_enc84_chung_patron`（live 電視劇／初級，唔係 draft 話嘅電影／中） |
| G-C2 鍾忠告卡 | 已在位（v229 B7） | `chungAdviceHeld229` 旗（`chung_farewell` 授）；`chungAdviceTipForAudition229` 喺試鏡 modal＋預約分支呼叫；用一次即清（`chungAdviceSpent229`）；文藝片＝genre 文藝＋電影／電視劇＋category 作品 |
| G-L2 廖喜劇組債權 | **半完成——留跟進票** | trigger 通告在位：`gig_1992_film_202`《笑到最後》群演（電影／中級／1992）trigger `credit_wf3_comedy_crew`（`test_gig229_trigger.js` 已釘）。但債權 code 側**從來無授出**：WF3 收割授債喺 v267 成個刪走（`test_wf3_82_logic.js` 釘死「殺青唔清記仇債、唔派喜劇組債權」）；`credit_wf3_comedy_crew` 全 repo 只剩結局讀位 1 處（L12913）。重發會同 v267＋v259 R3（過期收割＝壞帳，唔計 settled）衝突；WORKORDER 2.13 亦將兌現方法留待通告重寫。跟進票要先拍板新授出路徑，唔可以喺 v273 硬湊 |
| G-L3 廖舞台通告 | 無嘢做（moot） | `gig_wf3_liao_stage` index.html＋gigs_new.json 雙 0 命中——舊庫 gig 已隨舊庫死 |
| 2.17–2.20 draft 對白 | 做唔到——草稿抉擇未實裝 | 「唱住先／企硬」只喺散文對白出現（例如 L36573–36690 駱翻唱句），無抉擇 label；留 (c) 跟進票 |
| 2.21–2.24 保留錯過整段 | 已核實無違規 | draft beat 唔喺 code；live 亦無實裝嗰啲場面、無違反保留（例如 live `chai_repay` 係 N13-linked 回報 beat，閘係 `flag_side_*`／N13，唔係 draft Beat 5） |
| 2.26 | 攻略側備註，code 無嘢 | — |
| M-1 即派機制 | 已在位 | `grant229Record`＋`grant229DueList`＋`grant229PresentDue`（晨鏈 L21339）；`GRANT229_ENC79` 覆蓋初遇 3 線×3 選項＋`beat:gu_n10after`／`beat:gu_loan`／`beat:mak_respect`／`beat:liu_repay`。六線 beat 行缺失係 (c) 跟進票範圍，唔係機制缺口 |
| BR89 映射全表 | 已在位（v229 B5／v254） | 13／13 驗證：每張新庫存在＋`trigger.creditId` 同 `BR89_PATRON_OF_GIG` 一致；包齊 §10.1 八筆債權（廖 patron／顧／麥／駱／魏／齊／鍾／廖優先）；另 `gig_1991_film_109` 經通用債權規則共用 `credit_enc83_liu_patron` |

## (e) 陸 heart foreshadow 放寬（用戶 2026-11-17 19:52 拍板）——做咗

- 放寬條件（按 WORKORDER 精神定）：**無年份閘、無 tier 上限**。`luk_foreshadow` 而家只要求：未守口（無 `luk_kept_secret`）＋未講漏（無 `luk_loose_talk`）＋未播過（`beatsDone`）。1990 T0／1991 T2／1992 T3／1992 冬 T4 全部開；守口／講漏／播過之後唔再開。
- 理據（wrap-fav 計數）：`enc79OnWrap` 每次陸有份嘅殺青通告都加 fav（主角好評 +3／配角 +1），唔使撞面；`ENC79_FAV_CAPS = [30,55,80,100]` 下玩家 tier ≥1 就可以靠殺青回望將陸 fav 推上 tier 3+，一次都未撞過陸。任何 tier 上限都會留低一個可達嘅永久鎖死（攞唔到 `luk_kept_secret` → heart 永遠唔開）。無上限係唯一唔鎖死嘅做法。
- 代價只係推遲一次：beat 一次性＋pick 次序排第一，遲遇只會令 `luk_intel`／`luk_tease`／finale 遲一個巧遇，唔會重複遮蔽任何嘢。1992 冬 T4 嗰陣 foreshadow 排 finale 之前（測試有釘）。
- heart 閘不變：T3 無守口旗 → heart 唔開；有旗 → 開。1990 T0 照開（舊測試口徑不變）。

## 測試

- 新檔 `tests/test_sideline273_logic.js`：**50 項**，分 (a) 4／(b) 12／(c) 9／(d) 17／(e) 8。反證：喺 v271 pristine 上行，(a)／(b)／(c) fx／抉擇／讀返斷言乾淨 FAIL。
- 更新：`test_enc83_logic.js`（駱／顧 label 同步）、`test_enc84_logic.js`（蘇／程 label 同步）、`test_sideline271_logic.js`（顧 heart label 同步）、`test_gig229_grant.js` T2（改做 v273 接線現實）。
- Resync（index.html 淨 +34；段邊界 main 座標：≤26803 ＋0、26804–36410 ＋1、36411–38465 ＋19、38466–38492 ＋21、38493–38605 ＋25、38606–38646 ＋29、≥38647 ＋34）：`test_gift185_static.py`、`test_tang171_static.py`、`test_tang173_static.py`（總行數鏈＋v273 +34；openLoc DEF 40716→40750）、`test_rom176_static.py`（4 釘行各 +34，內容逐行核實純漂移）、`test_travel114_static.py`（DEF／WRAPPER＋FREE 26 處＋COUNT 5 處按段重算，逐對命中一次，單次掃描 dict 查表）。另 v272 中途落地，分支 rebase 上 `f2d3dfb`（零衝突），resync 在新基線上重做。

## 落地記錄

- main `c5d7aa4`（squash merge v273，2026-11-17）。GitHub Pages 核實：主頁 HTTP 200、4,618,115 bytes、sha256 `e788eb6224e3d43cd24b405a2914efa3c929dd6ef66b8ca072afab0a7fa2fc46`，同本地 `index.html` 完全一致。工作副本 `linji-work273` 已刪。

## 留跟進票（唔入 v273）

1. 六線 draft Beat 1–5 抉擇樹全面實裝（(c) 發現：草稿旗 repo 0 命中；連同 GRANT229_ENC79 六線 beat 行、G-LOK-2／G-NGAI-4／G-CHAI-2／G-PANG-2、2.17–2.20）。
2. G-L2 `credit_wf3_comedy_crew` 重新授出路徑——要先拍板（v267 刪收割＋v259 R3 壞帳定性＋WORKORDER 2.13）。
3. (b) Beat 2 軟錯過備註：N10 早完成會令 Beat 2 永遠錯過（設計上接受，同 `gu_foreshadow` 1991 窗口同級）。
