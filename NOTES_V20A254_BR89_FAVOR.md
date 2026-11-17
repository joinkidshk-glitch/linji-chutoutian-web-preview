# v20a254 — 人情兌現全盤・通告／BR89（工人 A）

日期：2026-11-17。分支 `v20a254`，基線 main `f8e486a`（v20a256）。
範圍：只改 `index.html`（BR89 映射表＋`br89GigOn` R-4 接線＋`FAVOR_DUE_CFG`／`FAVOR_DUE_GIGS`）
＋`tests/test_br89_*.js`、`tests/test_gig229_*.js`；`content/gigs_new.json` 0 改動（282 張不變，
設計庫 `gigs_new_v2.json` md5 一致 `423c6cd00b5674cba59d7501737a2d47`）。

## 1. 任務 1 — BR89 13 對重對（核心）

### 問題根源（獨立核實）
- live `BR89_PATRON_OF_GIG`（舊 L25459）係舊庫（`a39ad34`，267 張）id，v252 新庫起 id
  全部重洗；舊 13 對同新庫 credit trigger **0 張對得上**（v252 T8 已釘死：3 張錯配、
  9 張目標已無 trigger、1 張消失 `gig_1991_variety_108`）。`git show a39ad34:index.html`
  證實舊表同舊庫 13 張 credit-trigger gig 逐對吻合（舊 title＋trigger）。
- 舊 code-side 4 張兌現 gig（`gig_br89_patron_luk／pang／ching`、`gig_br89_liu_priority`）
  喺新庫 0 命中（已刪，`BR89_GIGS` 已清空，唔留死 id——映射表本身已無呢啲 id）。

### 方法（v255 同一套：舊庫還原＋title／全文雙重搜尋，REUSE 優先）
舊 title → 新庫搜尋 → 對 `trigger.creditId`。結果：**13 張全部 REUSE，0 張新開**。

| # | 債權 | 舊 gig（舊庫） | 新 gig（REUSE） | 理由 |
|---|---|---|---|---|
| 1 | `credit_enc83_luk_patron` 陸柏言 | `gig_1991_film_106`《江河歲月》 | `gig_1991_film_101`《江河歲月》 | 同名；blurb「憑陸柏言引薦入組」 |
| 2 | `credit_enc84_pang_patron` 彭少祺 | `gig_1991_variety_108`《台慶大騷》 | `gig_1991_variety_203`《台慶大騷》 | 同名；舊 id 已消失，新庫接班者 |
| 3 | `credit_enc84_ching_patron` 程天諾 | `gig_1992_rec_102`《夜場匯演》 | `gig_1992_rec_106`《夜場匯演》 | 同名；舊 id 新庫改做駱《硬漢柔情》（錯配根源） |
| 4 | `credit_enc79_liu_priority` 廖炳星 | `gig_1991_film_107`《笑住過肥年・外傳》 | `gig_1991_film_103`《笑住過肥年・外傳》 | 同名 |
| 5 | `credit_enc83_liu_patron` 廖炳星 | `gig_1992_film_102`《笑星大作戰》 | `gig_1992_film_103`《吉星笑哈哈》 | 賀歲喜劇、廖 leadM、1992 電影；新庫另有 `gig_1991_film_109` 同債權，行通用 credit 規則，表只取一張 canonical |
| 6 | `credit_enc83_mak_patron` 麥震東 | `gig_1992_film_103`《鐵拳出擊》 | `gig_1991_film_110`《鐵拳王》 | blurb「憑麥震東引薦入組」動作替身 |
| 7 | `credit_enc83_yip_patron` 葉敏芝 | `gig_1992_tv_103`《對手戲》 | `gig_1992_tv_105`《摩登一家人》 | trigger creditOwner 葉敏芝；葉飾演新潮女兒 |
| 8 | `credit_enc83_gu_patron` 顧明輝 | `gig_1991_rec_102`《夜總會暖場夜》 | `gig_1992_rec_105`《當年情懷》 | blurb「顧明輝引薦並監製」大碟主唱；R-4 接線跟住搬（見下） |
| 9 | `credit_enc84_so_patron` 蘇芷茵 | `gig_1992_tv_104`《愛在陽光下》 | `gig_1991_ad_102`《秀髮如瀑》 | trigger creditOwner 蘇芷茵；舊 id 新庫改做齊《滬上往事》（錯配根源） |
| 10 | `credit_enc84_chung_patron` 鍾楚凝 | `gig_1992_film_104`《離港那天》 | `gig_1991_tv_108`《深秋情緣》 | trigger creditOwner 鍾楚凝；鍾飾演舊情人 |
| 11 | `credit_enc83_lok_patron` 駱家聲 | `gig_1992_rec_103`《主打歌》MV | `gig_1992_rec_102`《硬漢柔情》 | blurb「駱家聲引薦的新人搖滾單曲」 |
| 12 | `credit_enc83_ngai_patron` 魏詠男 | `gig_1992_film_105`《鐵橋風雲》 | `gig_1991_film_111`《雪山雙劍傳》 | blurb「憑魏詠男引薦入組」武打配角 |
| 13 | `credit_enc83_chai_patron` 齊鎮海 | `gig_1992_film_106`《油麻地夜班》 | `gig_1992_tv_104`《滬上往事》 | trigger creditOwner 齊鎮海；齊飾演滬上商人 |

- R-4 雙觸發：`br89GigOn` 硬編碼由舊 `gig_1991_rec_102` 搬去 `gig_1992_rec_105`
  （舊 id 新庫係無 trigger 嘅《鄉謠》，還錢路原本斷咗；T2／T2b 改用真 gig 驗，缺口已補）。
- 新開 gig：0 張。唔郁：結局計數口徑、E4／E5／E3 門檻、SAVE key／softRev／`?v=`、romance／rival JSON。

### 測試更新（舊測試釘死咗漂移，唔係回歸）
- `tests/test_br89_logic.js`：EXPECT13 → 新 13 對；R-4 樣本 id → `gig_1992_rec_105`；H7 fixture → `gig_1991_film_101`。
- `tests/test_br89_static.py`：BR89_13 → 新 13 對；R-4 斷言 id → `gig_1992_rec_105`。
- `tests/test_gig229_trigger.js`：T2 改用真 gig `gig_1992_rec_105`（唔再用合成樣本）；T2b 尾斷言反轉——還錢旗而家開到（接線缺口已補）；T8 EXPECT → 新 13 對，match 斷言由 0／3／9 改做 13／0／0，漂移註解改做修復註解。
- `tests/test_gig229_v251_c.js` §4：mak 樣本改做 liu（`gig_1992_film_103` 而家對 liu）；廖優先 `gig_1991_film_103` 由「唔標記（缺口已釘）」改做「有標記（v252 缺口已修）」。

## 2. 任務 2 — F1 幫忙通告（D3：補）

- live 機制核實：`favorDueTick` 讀 `FAVOR_DUE_CFG.gigId`（wrapped 檢查 `wrapHistory`／`done_<gigId>`）＋
  `mergeFavorGigs` 讀 `FAVOR_DUE_GIGS`（`favorState==="called"` 且 4 日窗口內先注入 `GIGS`，
  其餘時間移除）；`mergeFavorGigs` 掛喺 `gigsForLocSeasonBoard` 開頭。`gigId: null`／`[]` 嗰陣
  兩條路都係 no-op，只剩現金／禮物還款路。`gig_favor_ho_errand` 全 repo 0 命中（v229 刪咗）。
- 做法：**恢復 v20a17 原裝 special gig 接線**（唔入庫存——新庫版幫忙通告無 trigger kind 可接，
  入庫會郁 282 張計數／六批驗證／§1.1 矩陣；code-side 注入唔受年／季／NAT92 錯峰影響：
  id 唔合 `gig_\d{4}_` 格式 → `nat92StaggerEligible` false → 照常上板；season「不限」→ `seasonRank` 0）。
  內容不變：`gig_favor_ho_errand`《晨光劇場》臨時人手、事務所板（`agency_ho`）、$500 定額、
  1 日工、4 日窗（`applyDeadlineDays:4`）；改動三點：tier 舊「初」→新五級「臨記」、
  補 `category:"臨記通告"`、刪死 data `favorDelta`＋唔再寫 `era_*` id（`eraTag` 拎走）。
  `FAVOR_DUE_CFG.gigId` 填返 `gig_favor_ho_errand`；`favorDueTick` 嘅 rel +2／−3、ledger
  記帳（`repaid_help` 計 settled、`void_expired` 唔計）全部照舊機制行，唔郁 code。
- 新測試 `tests/test_br89_favor_due.js`（26 項 ALL PASS）：D1 接線形狀（id／臨記／事務所板／
  4 日窗／$500／標題無年份數字／無 `favorDelta`）；D2 到期叫數（dueDay 當日+7）→ 上板；
  D3 4 日內做完 → 清債＋rel +2＋`repaid_help` 計 settled；D4 過期（day 12）→ 作廢唔計
  settled＋rel −3；D5 pending 唔注入；D6 到期前現金／禮物還咗 → `closed_other` 兜底＋唔雙計。

## 3. 任務 3 — 驗證（唔重做）

F2／F3／F6／F7／F8 係故事攻略人情兌現表（`linji-main-phase3/workorder-n1-n6-c18.md` §10）
N4／N5／N6 章內項，逐項對 live code 核實：

| 項 | 內容 | Live 現況 | 結論 |
|---|---|---|---|
| F2 | N4_a 拒絕 → `debt_c4_ho_ripple` | 債真入 `S.mockDebts`（ripple 消費者 L8047–8048，可還、計 settled）；無 dueDay、無 favorDue 循環、無叫數場面 | **未兌現，維持缺口**（要第二條 favor-due 循環，先有教學債嗰種叫數＋指定幫忙通告；本票 F1 只恢復教學債嗰條，唔擴去 F2） |
| F3 | N4_b 接下 → 何生「捱得」認可 | 抉擇 tags `["捱得"]` 經 `applyCastingTags`（L8114）真入 `S.castingTags`（`tag_endure`，＋雙軌 delta）；標籤系統有讀取（選角閘＋結局甘草軌） | **部分兌現**：標籤已落地，但無指定動作組優先通告（工作單原提案未做） |
| F6 | N5_b 打圓場 → 阿偉欠采兒一個提點（`choi_spin`） | 旗只喺旗登記表有定義（L32627），live 0 個 gameplay 讀者；之後無節點跟進 | **未兌現，維持缺口** |
| F7 | N6 電視線 → 昌叔提攜 | 昌叔只喺 N6 beats／resultBeats 出現；`flag_canteen_grind` 只喺結局頁回望文案讀（L13326）；無跟進通告 | **未兌現，維持缺口** |
| F8 | N6 電影線 → 根叔提攜 | 根叔只喺 N6 電影線 beats＋`set35_lunch` 通用放飯事件（iq+1／壓力−3，唔係提攜兌現）；`flag_studio_follow` 只喺結局頁回望文案讀（L13328）；無跟進通告 | **未兌現，維持缺口** |

- credits 三筆（v251 已接鏈，核實通過，唔重做）：授出（`story46／48SettleTick`，`test_gig229_v251_c.js` 覆蓋）
  ＋新庫 trigger gig 齊全——`credit_c7_rain` → `gig_1991_tv_204`《通宵追捕》、
  `credit_c9_crew` → `gig_1991_film_108`《月夜酒廊》、`credit_c15_stunt` → `gig_1992_film_203`
  《江湖復仇》；`triggerGigOn` 通用 credit 規則開得到。已知限制（唔喺本票改）：呢三張唔喺
  BR89 映射入面，殺青鉤 `br89OnGigComplete` 唔會標 `redeemedBy`（`test_gig229_v251_c.js` §4
  第一項釘死咗）；單次使用靠 `done_` 旗落板，唔會重複兌現同一張。
- `credit_c13_newyear`（v253 做咗，核實一次，唔郁）：新庫 0 張 trigger gig（by design）；
  結局頁兌現喺位（L13286–13302）：持有未兌現債權行到結局頁 → 兌現做 1993 年賀歲片優先試鏡位
  （文案交代，遊戲期外），標 `redeemedBy="ending_c13_newyear"`（判定之後先生效，計數唔受影響）；
  另有專屬回望句列出已兌現提攜（頭 3 筆，c13 除外）。

## 4. 驗證

- 相關測試 ALL PASS：`test_br89_logic.js`、`test_br89_static.py`（FAILURES: 0）、
  `test_br89_favor_due.js`（新，26 項）、`test_br89_deadflag_lint.js`、
  `test_gig229_grant.js`、`test_gig229_trigger.js`、`test_gig229_v251_c.js`、
  `test_gig229_pack.js`、`test_gig229_counts.js`、`test_gig229_tiers.js`、
  `test_gig229_years.js`、`test_gig229_stagger.js`、`test_gig229_press94_advice.js`、
  `test_awei195_logic.js`。
- 六批驗證（設計庫，讀已凍結舊庫，未改 harness）：film-works／tv-works／music-works／
  ad-variety-works／extra-film-tv／extra-music-ad-variety 全部 exit 0、硬 FAIL 0
  （runner「FAIL=1」係已知假陽性：summary 行本身含「FAIL 0」字樣；`full_verify_checks.py` exit 0）。
- 全套 suite：`bash qa131/run_suite.sh` → **TOTAL PASS 316 FAIL 10**（基線 315／10，+1 係新加
  `test_br89_favor_due.js`；10 項 FAIL 同基線逐項一致，全部已知 pre-existing）。

## 5. 偏離／新發現（要統籌知）

1. **漂移測試 resync（文件清單外，但必須做）**：我嘅 `index.html` 改動淨 +61 行
   （FAVOR_DUE +45、BR89 表 +14、R-4 +2），令 5 個行數漂移測試由 PASS 變 FAIL
   （`test_gift185_static.py`、`test_rom176_static.py`、`test_tang171_static.py`、
   `test_tang173_static.py`、`test_travel114_static.py`——全部釘死總行數／錨點行號）。
   按 repo 慣例（每版都要更新 ledger，v253 +115 就係咁）機械更新咗呢 5 檔嘅 ledger／錨點
   （段 shift：＜22854 唔郁、22854–25452 ＋45、25453–25472 ＋59、≥25473 ＋61；每支釘逐行
   核實內容啱位先改），suite 先返到 316／10。呢 5 檔唔喺任務列出嘅可改清單入面——
   唔改佢哋，分支落地嗰陣 suite 會多 5 項回歸；改佢哋係純行號搬移，0 行為改動。
2. **廖炳星引薦有兩張新庫 gig**（`gig_1991_film_109`《笑聲震天響》＋`gig_1992_film_103`
   《吉星笑哈哈》，同一 `credit_enc83_liu_patron`）：BR89 表只取後者做 canonical
   （1992 電影，同舊年＋媒介）；前者行通用 credit 規則照開。殘留缺口：先殺青前者嗰陣，
   `br89OnGigComplete` 唔會標 `redeemedBy`（同 c7／c9／c15 一樣嘅通用-credit 限制），
   後者要靠 `done_` 旗先落板——唔會重複兌現，但債權狀態唔會標已兌現。留返另票統一
   通用 credit gig 嘅殺青標記。
3. **`content/story_detail_n1_to_n17.json` 有一行未經我手嘅改動**（工作副本開工嗰陣已經 dirty：
   N1 何生一句對白改寫，1 行入 1 行出，行數不變）——我完全冇掂過呢個檔，留返原樣，
   統籌落地嗰陣核實係邊個工人嘅。
4. F1 幫忙通告 $500 定額（`pay [450,550]`）高過 SPEC §7.1 庫存臨記帶（$250–400）——
   保留 v20a17 原裝定額（special gig 唔入庫，六批驗證唔讀佢；改 pay 會改已測試過嘅經濟行為）。
   如統籌認為要跟 §7.1，改 `pay`／`payExact` 係一行嘅事。
5. 未改：`creditsHeld` 唔讀 `redeemedBy`（已知出入，留返另一票）；F2／F6／F7／F8 缺口維持
   （見 §3，要新系統／新通告，唔係本票範圍）。

## 6. 落地檢查（統籌用）

- `git diff --stat`：`index.html`（3 個 hunks：FAVOR_DUE、BR89 表、R-4）＋測試檔
  （br89 ×3 含新檔、gig229 ×3、drift resync ×5）＋本 NOTES；`content/gigs_new.json` 無改動。
- 唔 push、唔 merge、唔刪工作副本（按任務要求，落地由統籌做）。
