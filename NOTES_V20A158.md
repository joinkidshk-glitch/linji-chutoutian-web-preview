# NOTES_V20A158 — 人情免試鏡渠道（G-M1／G-PANG-1）＋支線抉擇即派 8 行

- 工作副本：`~/workspace/linji-work158r`，分支 `v158`，base `947cf56`。只改工作副本，未 merge、未 push。
- 範圍：任務書三項（2.4／2.9／2.11）。BR89 13 對、2.3 G-G2 雙觸發、2.12 G-C2 忠告卡原封不動（`git diff` 核實零改動；新測試 T8 釘死 13 對逐字相同）。
- 2.13／2.14（R5）、2.15／2.25（舊 id 已消失）、2.16–2.24／2.26 唔做；感情線、Vera／海媚／鄧麗萍死檔、傳聞刪除、新通告唔掂；2.10 冇加 trigger 去 gig_1991_film_104。

## 1. 兩條免試鏡渠道（v20a158 block，`index.html` L44247–L44389，chungAdvice 後／doAudition 前）

共用模式（跟 Q6 忠告卡同一掛點風格）：
- 持有指定債權（未兌現、未絕響）＋通告啱類別＋`canAudition(gig).ok` → 詳情頁／通告卡出金色提示行，詳情頁多一個「用人情免試鏡」掣。渠道唔繞過聲望／能力硬閘。
- 用咗就保證獲聘（p=1），跳過試鏡日同等消息等待，唔耗日（打個電話，唔行 `confirmSpendDay`／`tickDay`）。
- 兌現嗰刻消耗債權（照 `br89OnGigComplete` 模式：`redeemedBy`＋line 附加「已兌現」＋`syncNotebookMirror()`，v259 口徑下唔再計結局數、唔可以重用）；同時經 `aud91CreatePending` 記一筆 ok:true、revealDay 翌日（即日＋1）嘅等消息記錄，聽朝晨鏈 `aud91PresentDue` 呈現（沿用 GRANT229 即派模式），簽約金跟 v91 獲聘流程（片酬 30% 即付、餘額殺青入帳）。
- 唔做嘅嘢：武師班本身已免費，「一堂免費」替代方案無意義，只做免試鏡；「台風放寬」未定，彭渠道只做免試鏡。

| 渠道 | 債權 | Matcher（新庫實數） | debtor |
|---|---|---|---|
| 2.4 G-M1 武指照應 | `credit_enc79_mak_wuzhi` | genre 動作／武俠＋category 作品 → **20 張**（任務書「32 張」係 genre 總數，含 12 張臨記通告；category 一篩，臨記散工例如 gig_1990_film_206 碼頭搬運已排除） | 紅棉武指 |
| 2.9 G-PANG-1 彭慈善 | `credit_enc84_pang_charity` | type 綜藝＋roleLabel 含「主持」 → **5 張**（gig_1990_variety_101／105、gig_1991_variety_103／104、gig_1992_variety_102，同任務書一致） | 彭少祺 |

函數：`favor158CreditHeld`／`isMakWuzhiGig158`／`isPangCharityGig158`／`favor158ChannelForGig`／`favor158ChannelHintHtml`／`favor158SpendCredit`／`favor158UseChannel`（確認 modal：確認／取消；取消返詳情頁）／`favor158RedeemChannel`（守衛：渠道＋未等緊消息同一張＋等消息未滿 3 張）。

接線：
- `gigCardHtml`（L17893 起）：渠道適用嗰陣卡面多一行 `<p class="gold">` 提示（`favor158Html`，跟 `intelHtml` 同一 try／typeof 守衛風格）。
- `openCastingNoticeDetail`（L18863 起）：`gate.ok` 分支先加提示行，再加「用人情免試鏡」掣（排喺正常試鏡掣之後、離開掣之前）。閘未過嗰陣唔出。
- `aud91CreatePending`（L43937）：`pre.revealDay` 覆寫——有傳入就 `revealDay＝pre.revealDay`（wait＝差值），唔行 `aud91WaitDays` 2–4 日等待；無傳入照舊。另加 `favorLabel` 透傳。
- `aud91PendingHint`（L43975）：via favor158 嗰陣唔講「試鏡咗幾多日」，改講「何生聽朝會打嚟話你知——免試鏡，直接獲聘」。
- `aud91PresentOne`（L44115）：via favor158 嗰陣，第一行改「免試鏡直接獲聘，拍攝 N 日」（唔講「試鏡通過」），何生嗰句改「`${favorLabel}嗰邊應承咗，直接用你，唔使試鏡。簽約金已經過數，拍攝日而家排。」。其餘路徑零改動。

## 2. GRANT229_ENC79 加 8 行（L27006 起，全表 9→17 行）

Hook 照舊（L39606 `grant229RecordFromEnc79(step.seg, opt.label)` substring 匹配），無新 hook code。key 逐個對過 live 選項 label；reason 按草稿 `~/workspace/linji-story-sidelines/drafts/batch1-liao-gu-mak.md` 相關段落改寫做實際對位 gig 嘅標題（何生傳呼口吻）。

| # | seg | key（live 選項 label） | gigId | 作品／角色 |
|---|---|---|---|---|
| 1 | `beat:gu_n10after` | 岸（「恭喜他，終於上岸」） | `gig_1992_rec_103` | 《齊心同行》合唱男歌手 |
| 2 | `beat:gu_n10after` | 賭（「提醒他以後不要再碰賭」） | `gig_1992_rec_104` | 《銀幕影》主題曲配唱歌手 |
| 3 | `beat:gu_loan` | 一口應承（「借，一口應承」） | `gig_1991_rec_107` | 《情濃款款》大碟主唱 |
| 4 | `beat:gu_loan` | 一半（「借一半，留一些給自己」） | `gig_1991_rec_104` | 《快歌飛揚》快歌和音歌手 |
| 5 | `beat:gu_loan` | `""` 兜底（「不借，這筆錢我真的幫不了」） | `gig_1991_rec_106` | 《並肩前行》新人合唱男歌手 |
| 6 | `beat:mak_respect` | 隨時候命（「應承隨時候命」） | `gig_1991_film_108` | 《月夜酒廊》男配角 |
| 7 | `beat:mak_respect` | 驚（「老實講自己會驚」） | `gig_1992_film_107` | 《劍氣長虹》動作替身（1992 年嗰張；唔係 gig_1991_film_107《沙田夜巡》，N11_b 目標） |
| 8 | `beat:liu_repay` | 推辭（「推辭講自己排緊期」，只此一行，唔設兜底） | `gig_1991_film_109` | 《笑聲震天響》男配角 |

核實：8 張 id 全部喺 `content/gigs_new.json`（282 張）存在、兩兩唔同、唔撞 GRANT229_CHOICE／BR89／DRAFT／原有 9 行（新測試 T7 逐項釘死）。第 6 行 gig_1991_film_108 本身已有 trigger（credit_c9_crew）、第 8 行 gig_1991_film_109 本身已有 trigger（credit_enc83_liu_patron）——即派唔理 trigger，兩邊都冇郁。顧 Beat 2 DRAFT 兩行繼續 dormant；麥 Beat 2（mak_tease 無抉擇）唔加行。

## 3. 測試

- 新檔 `tests/test_sideline158_logic.js`：**84 項斷言，ALL PASS**（T1 matcher 實數／T2 渠道供應條件／T3 武指兌現一次即清＋確認 modal／T4 彭兌現／T5 三守衛／T6 翌日晨鏈呈現＋簽約金三成＋shoot.signedPaid／T7 8 行即派＋防撞／T8 BR89 13 對／T9 靜態＋舊路徑）。
- 舊測試同步：`tests/test_gig229_grant.js` T0（ENC79 行數 9→17；原 9 行 live id 斷言收窄做 `slice(0,9)`）。
- 行號釘 resync（`index.html` 淨 +165 行：gigCardHtml＋4／詳情頁＋11／GRANT229_ENC79＋15／aud91CreatePending＋3／aud91PendingHint＋2／aud91PresentOne＋1／v20a158 block＋129；difflib 對位核實內容逐字相同，純漂移；`openLoc(` 呼叫點 56 處不變）：`tests/test_travel114_static.py`（COUNT／FREE／DEF 41299→41329／WRAPPER，腳本 `qa158/resync158.py`）、`tests/test_gift185_static.py`／`tests/test_tang171_static.py`／`tests/test_tang173_static.py`（總行數 45953→46118，標籤 45964→46129；DEF 41299→41329）、`tests/test_rom159_static.py`（釘行各＋15）、`tests/test_rom176_static.py`（釘行各＋30）。

## 4. Suite

`bash qa131/run_suite.sh ~/workspace/linji-work158r ~/workspace/linji-work158r/qa158/suite158b.txt` → **TOTAL PASS 327 FAIL 10**。基線 v262 係 326／10；+1 PASS 係新測試檔，10 個 FAIL 同基線完全一致（flash51／rumor49／slot50／soft_tip_111_restore／start53／weave43／weave44／weave49／wf5_87／wrap38，全部 pre-existing），**零回歸**。統籌修 `revealDay` 即日→即日＋1 之後重跑（`qa158/suite158c.txt`）→ 同樣 TOTAL PASS 327 FAIL 10，FAIL 名單一致，零回歸。

## 5. 語法

`node --check index.html` 喺 Node v24 直接跑唔到（`ERR_UNKNOWN_FILE_EXTENSION`，.html 副檔名），跟 repo 慣例改抽兩塊 inline `<script>` 出嚟檢查：兩塊全部 PASS（見 NOTES_V20A250／V252 同一做法）。

## 6. 已知邊界（留統籌／跟進票決定，唔係 bug）

- **同日返屋企邊界——已修（統籌拍板，落地前）**：渠道 pending 嘅 `revealDay` 由即日改做即日＋1（`favor158RedeemChannel` 嗰行＋`aud91CreatePending` 註解＋block 註解一併改），嚴格第二朝晨鏈先出何生電話；同日返屋企 `enterHome` 補呈現唔會提前出（跟 GRANT229 dueDay 即日＋1 同一模式）。測試 T3／T4／T6 期望已同步改（revealDay 11、wait 1、用嗰日 dueList 未有、翌日 dueList 有）；斷言總數 83→84。
- 渠道唔耗日：用完人情嗰日玩家可以繼續行動（同正常試鏡耗一日唔同），係設計本身（人情就係代價），唔係漏洞。
- 實機驗證（瀏覽器）未做：工作副本只跑咗邏輯＋靜態測試＋全套 suite；落地後統籌安排實機抽檢。
