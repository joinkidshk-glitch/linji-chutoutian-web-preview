# NOTES_V20A214 — 頒獎結果卡報紙公佈＋模板術語修正（工人 2）

分支 `v20a214`，基底 HEAD `0dd568a`（工人 1：晨報核心渲染器＋NP214 CSS，未落地、未 push）。
**本票唔落地、唔 push。**做完即停，等統籌派下一棒。

## 分工（工人 1 vs 工人 2）

- 工人 1（已入 HEAD `0dd568a`）：NP214 CSS（`.paper-sheet.np214-*`）、helpers（`fmtNewspaperDate`、
  `newspaperFullName214`、`np214ShowPage`、`np214DateLabel`）、`renderMorningPaperHtml` 重寫做 v11 版式、
  `buildNewspaperEdition`／`commitMorningPaper` 日期口徑統一、新測試
  `tests/test_newspaper214_core_logic.js`／`tests/test_newspaper214_core_static.js`。
- 工人 2（本票）：下面全部。其餘工人範圍一字唔郁（見 §5）。

## 1. `renderAwardResultHtml` 重寫做一張報紙公佈

- 版式跟樣本 v11（`~/workspace/linji-newspaper-sample/index.html`）：報頭 A「維港日報」＋粗幼雙線＋
  `VICTORIA HARBOUR DAILY`；日期行＝典禮日＋1 嘅遊戲日期（`fmtNewspaperDate`，例如 dayIndex 151 →
  1990年6月2日 星期六）；大標題＝`pack.press.headline`；副題＝`pack.press.dek`；主文兩欄
  （`np214-body2`）＋右直欄「影視娛樂」（`np214-sidebar`，快訊行＋模糊填充字）；版尾；第二版切換
  （`np214ShowPage`）。
- **第二版係銷量榜**（樣本 v11 嗰頁）：大標題＝得主奪獎行、副題＝focus 格嗰句、內文＝快訊行＋收尾句。
  任務書第 1 點「主文兩欄（…＋銷量／票房／收視餘韻行）」字面可以讀做第一版內文——已按樣本放第二版，
  等統籌確認。
- 保留（舊測試逐項覆驗，見 §4）：focus 格行先（v192 C3）、同屆提名行只出一次（v186 C1）、落選安慰行
  何生「差少少啫，唔緊要，下年再嚟過。」（v147 D2）、代表作行（`psr-rep62`）、weakHint 診斷
  （`psr-weak62`）、聲望／信用行逐字（`幕前聲望 +X · 業內信用 +Y`）。
- 典禮小檔案（`np214-factbox`）：只用遊戲已有真實資料（典禮／地點／得主／入圍），唔作新事實。
  行頭用「得獎／入圍」唔用獎項 label——舊測試計 label 只可以出一次（test_awards186／192），
  label 只喺內文行出。**圖說同樣唔寫獎項 label**（同樣本圖說寫「新人獎」有輕微出入，已喺 helper 註解講明）。
- `presentAwardResult` modal 掣「收下這晚」不變；`enqueueNewspaperFromAward`（翌日晨報）標題／副題／
  聲望／排期／去重一字唔郁，結果卡報紙同晨報用同一份 `pack.press` 文案，唔會出兩次唔同標題。

## 2. v211 意圖融入新版式（基底冇 v211 code，只跟意圖）

- A1：`presentAwardResult` 唔再叫 `toast()`（結果卡本身就係公佈）。推辭嗰個 toast 留喺
  `presentAwardInvite`，唔入呢段。
- B2：won 版銷量／票房／收視第二版用真實得主數據——`awardWinner149`／`awardWinLine149`
  （旁聽：得主奪獎行；won：玩家奪獎行；冇得主資料：跌返 displayName 散場行）。**「典禮後仍有人提起」
  呢句 stub 已經拎走**（渲染結果 0 命中，新測試 c4 釘死）。
- C1：同屆提名行加「★為得主」圖例（見 §3）。
- v211 C3 請柬席位去重係請柬嗰邊，唔入範圍，等 rebase（見 §6）。

## 3. ★統一（🏆 金底 chip → ★）

改咗嘅地方（報紙／頒獎結果路徑，只有呢兩處）：
- `awards63FellowsHtml`：得主標記 `iconHtml112("🏆") + " "` → `"★ "`；圖例 `（🏆 為得主）` →
  `（★為得主）`。金底 chip CSS rule（`.psr-fellows63 img.ic112`）留喺度，典禮 glamour／reveal 嗰邊
  仲用緊。
- `renderAwardResultHtml`：重寫嗰陣票根式卡片（`psr-press`／`psr-news`／metric stub）成個拎走，
  自然唔再有 🏆。

留返嘅地方（唔郁）：
- 手帳獎項頁 `renderAwardsPane62` 嘅 `fellowsWinHtml128`（v186 測試明言唔郁）。
- 典禮舞台 revealCap／glamour cap（v208 流程）。
- `.awd63-card.win::after` CSS、`EMOJI_ICON112` 註冊表、圖標組。
- 註解入面提到 `iconHtml112("🏆")` 係講明邊啲唔郁，唔係 code——測試驗「唔再用」嗰陣先剝走
  `/* */` 註解再驗（test_awards207_static.py C2、test_newspaper214_award_static.py S02／S03）。

## 4. 相片

- 入 repo 嘅檔（`assets/story/newspaper/`，WebP 灰階細檔）：
  - `photo_awi_ceremony.webp`：520×658，30,654 bytes（原 1280×1620，1,752,636 bytes）。
  - `photo_lok_ceremony.webp`：520×642，45,166 bytes（原 1348×1664，2,231,177 bytes）。
  - 合共 ~75KB；2M 原檔冇入 repo。
- 做法：PIL `convert('L')` → resize 闊 520 → WebP q80 method 6；像素灰階抽樣最大色差 ≤2／255，
  CSS 仲有 `grayscale(1)` 兜底。
- **預製黑白版 `photo_*_bw.png` 唔用得**：嗰兩張係另一批頭肩肖像（Lok 著皮褸、Awei 著便裝褸，
  冇舞台／獎座／燕尾服），唔係典禮現場相嘅黑白版——圖說講「台上接過獎座／身穿燕尾服」嗰陣唔可以
  用佢哋。所以由彩色典禮原檔直接轉灰階（「做法由你定」授權範圍內）。
- 用法（新 helper `np214AwardPhoto214(pack, opts)`，插喺 `renderAwardResultHtml` 前面）：
  - 玩家 won／nominated → 陳偉翔相；否則得主係駱家聲 → 駱家聲相；其他得主冇相 → 唔出相。
  - `opts.declined` 嗰陣跳過玩家分支（推辭咗冇去，唔可以用陳偉翔相）。
  - src 先搵 `NEWS82_IMGS[key]`，再跌返常量 `NP214_AWARD_PHOTOS_214[key]`（`assets/story/newspaper/` 路徑），
    兩個都冇 → null。
  - 結果卡：第一版＝得主相；第二版＝玩家相（只限入圍落選嗰陣——玩家贏嗰陣第一版已經係陳偉翔相，唔重複；
    旁聽冇玩家相）。
  - 圖說：won＋rep →「陳偉翔在台上接過獎座，憑《rep》奪獎。」；nominated＋rep →「陳偉翔身穿燕尾服出席
    〈displayName〉，憑《rep》入圍。」；lok＋title →「駱家聲在台上接過獎座，憑《title》奪獎。」。
    圖說唔寫獎項 label（見 §1）。
- 晨報 imgKey：**已接通**。`enqueueNewspaperFromAward` 頂加 `imgKey214`（經同一 helper），兩個
  `enqueueNewspaperItem` 呼叫（declined 分支一個、最後共用一個）各加 `imgKey: imgKey214` 一欄。
  `enqueueNewspaperItem` 本身已存 `imgKey`、`buildNewspaperEdition` 已帶 `imgKey`、工人 1 渲染器已支援
  `NEWS82_IMGS` 相片——所以只差呢一個欄就接通，標題／副題／聲望／排期／去重一字唔郁；冇相嗰陣
  imgKey 係 `""`，晨報唔出相。另加咗載入注入：`news_images_v82.json` 賦值之後 merge 兩 key 入
  `NEWS82_IMGS`（唔覆蓋已有值，try/catch 包住）。
- 缺口：冇。兩張相都接咗結果卡＋晨報。

## 5. 術語＋書面語掃蕩

- **content pack JSON 零檔改過**（`git diff --name-only` 驗過，`content/` 0 命中；新測試 X05 釘死）。
  全部行覆寫／注入／載入正規化。
- Inline 模板字面改咗 **9 處**：
  - `VENUE99_INVITE_DEK` 音樂「碟市邊個上鏡」→「邊個上台領獎」（1）
  - `VENUE99_PRESS_DEK` 音樂「有臨記席名字第一次出現」→「陳偉翔嘅名第一次出現」（1）
  - `VENUE99_NEWS_LINE` 音樂「碟市掌聲未完」→「掌聲未完」（1）
  - `AWARDS188_CATEGORIES` 音樂 4 句：「你記住碟市點樣叫人名」→「你記住樂壇點樣叫人名」×3、
    「碟市仲有下一更」→「樂壇仲有下一更」×1（各用獨有上文做錨點，唔用全局 sed——
    TEXTFIX55_EXACT 嘅 key 入面有同一子串）
  - `awardsPickPressNews` fallback「臨記席都有鏡頭掃過」→「觀禮席都有鏡頭掃過」（1）
  - `awardsMetricEchoLabel` map `sales:"銷量／碟市"`→`sales:"銷量榜"`（1）
- `TEXTFIX55_EXACT` 新加 **6 條**（STUB_AWARDS_CEREMONY_v1.json 舊字串，載入正規化保底）：
  「唱片年終有金碟夜。你收到一張席位信——碟市邊個上鏡，席上見。」→「…邊個上台領獎，席上見。」；
  「你坐席上，聽人謝唱片公司。你記住碟市點樣叫人名。」→「…樂壇點樣叫人名。」；
  「金碟夜，碟市多個名」→「金碟夜新人輩出」；
  「星河金碟夜結束。有臨記席名字第一次出現喺典禮側記。」→「…陳偉翔嘅名第一次出現喺典禮側記。」；
  「金碟夜散場：碟市掌聲未完。」→「金碟夜散場：掌聲未完。」；
  「台慶頒獎夜散場：臨記席都有鏡頭掃過。」→「台慶頒獎夜散場：觀禮席都有鏡頭掃過。」。
- `TEXTFIX55_GIG_SUB` 新加 **1 條**：`["夜半靈異主題曲主唱", "夜半靈異"]`（gigs_1988.json L11325 title
  「《夜半靈異主題曲主唱》主唱」→「《夜半靈異》主唱」、L11327 workTitle→「夜半靈異」；
  內嵌 fallback 同步，因為 `syncGigsForCalendarYear` 將所有 gig 都 map 經 `normalizeGigRecord`）。
- `content/STUB_NEWSPAPER_MORNING_SOFT_v1.json` L333 rumorEcho「碟市成績好」——已由 TEXTFIX55_EXACT
  現有條目覆蓋（key 完全一致，載入即修），唔使加。
- 全檔 grep 核實：`index.html` 入面「碟市／臨記席」剩低嘅只有 TEXTFIX55_EXACT 嘅舊字串 key
  （6 條新＋1 條舊 rumorEcho）＋註解，冇玩家面模板字串（新測試 T07／T08 釘死：攞走 EXACT 塊＋
  全部 `/* */` 註解之後全檔 0 命中）。
- 其餘報紙文案已掃過：「臨記組／臨記生涯／臨記歲月」係正常用詞（玩家本身就係臨記）；「幕前聲望」
  由 newsOpts phrases 載入轉「聲望」；「電視城」同樣已轉；唔再有其他一般讀者唔識嘅術語。
- 報紙自己嘅文字一律書面語；人物原話引述例外，可保留口語但必須放引號內（新寫嘅文案跟呢個規則）。

## 6. 唔郁（本票範圍外）

- `renderMorningPaperHtml`／`buildNewspaperEdition`／`commitMorningPaper`／NP214 CSS（工人 1 嘅）。
- `enqueueNewspaperFromWrap`、`press94*`、殺青報紙（工人 3）；base 唔出殺青報紙＋推出日提及
  （`qa214/PENDING_BASE_NO_PAPER.md`，唔入 commit）——推出日而家冇排報機制，建議另開票。
- WF3 世界事件模板、story 報紙模板、典禮流程（v208 逐格＋v211／v212）、v213 請柬提前＋晚上播。
- `press94RoleClass` 見報門檻分類器、聲望幅度、剪報上限 40。
- `qa214/` 係統籌筆記，唔入 commit。

## 7. 測試

- `node --check`（抽 inline script 段）：PASS。
- 新測試（全部跟工人 1／186／192 嘅寫法：logic 用 extractFn／extractConst＋eval＋ok()；static 用
  slice＋chk()）：
  - `tests/test_newspaper214_award_logic.js`：**45/45 PASS**。段：(a) 報紙版式 (b) 保留項
    (c) v211 意圖（metric 第二版真數據、三態 won／nominated／gallery）(d) 相片揀相 9 項
    (e) 術語正規化（TEXTFIX55_EXACT 6 句走一遍＋GIG_SUB 兩欄位）(f) 報紙路徑零 🏆／零術語。
  - `tests/test_newspaper214_award_static.py`：**44 項 PASS**。段：(1) 報紙版式 (2) ★統一
    (3) 相片（檔存在＋＜100KB＋灰階抽樣＋晨報 imgKey）(4) 術語掃蕩（9 處字面＋6 條 EXACT＋
    1 條 GIG_SUB＋全檔 T07／T08）(5) presentAwardResult 唔再 toast (6) 紅線（SAVE key／?v=／softRev／
    content JSON 唔郁）。
- 反證（pristine main `f58f19c`）：logic 測試乾淨 FAIL（`MISSING: fmtNewspaperDate,
  newspaperFullName214, np214AwardPhoto214, NP214_AWARD_PHOTOS_214`，exit 1，唔 crash）；
  static 測試 `RESULT FAIL 31`（31/44 FAIL，exit 1，唔 crash）。
  反證做法：`git show f58f19c:index.html` 抽出嚟＋兩個新測試放 `~/workspace/pristine214-counter/`
  跑完即刪。留意：`/tmp` 係 512M tmpfs，成個 repo archive（~800MB）塞爆咗佢（連 `git worktree add`
  都因此失敗）；反證唔好喺 /tmp 做全 repo 拷貝。
- 覆驗舊測試（全部 PASS，零回歸）：
  - static：`test_awards207_static.py`、`test_awards208_static.py`、
    `test_newspaper214_core_static.py`（工人 1）、`test_awards186_static.py`、`test_awards62_static.py`。
  - logic：`test_awards208_logic.js`、`test_awards186_logic.js`、`test_awards192_logic.js`、
    `test_awards178_logic.js`、`test_polish48_logic.js`、`test_newspaper214_core_logic.js`（工人 1）。
- 兩份舊測試要更新斷言（規格已改，唔係回歸）：
  - `tests/test_awards207_static.py` C2：fellows 得主標記由 `iconHtml112("🏆")` 改做 ★
    （驗 `"★ "`＋`★為得主`＋剝走註解後冇 `iconHtml112("🏆")`；金底 chip CSS rule 嗰句唔郁）。
  - `tests/test_awards186_static.py` C1：結果卡改做報紙，press 內容升做報頭大標題（`np214-headline`），
    唔再係 `psr-press` 卡；fellows 行仍然喺類別行之後（`np214-body2` 入面）。
- 唔跑全套（工人 4 做），唔實駕（工人 4 做）。

## 8. Rebase 注意

- **v211**（結果卡修法）：v211 改咗 `renderAwardResultHtml`／`presentAwardResult` 同一區——
  rebase 嗰陣會撞。合併要 keep v214 呢版（佢已經融入咗 v211 嘅 A1／B2／C1 意圖）；v211 嘅 C3
  請柬席位去重係請柬嗰邊，v214 冇掂過，要另外跟。
- **v213**（請柬提前＋晚上播）：掂 `presentAwardInvite`／`presentAwardResult` 一帶；我嘅
  `presentAwardResult` 改動只係刪咗一行 toast，衝突範圍細，但要對返。
- **v212**（典禮流程修復）：掂 `awards62PlayCeremony` 一帶，同我改嘅函數（render／fellows／
  enqueue）冇直接重疊；`awardWinner149` 我冇郁過。
- 落地次序（統籌定）：v211 → v212 → v209 → v213 → v214。

## 9. 改動一覽（`git diff --stat`）

- `index.html`（231 行變動）：`NP214_AWARD_PHOTOS_214` const＋NEWS82_IMGS merge 注入；
  TEXTFIX55_EXACT ＋6 條、TEXTFIX55_GIG_SUB ＋1 條；VENUE99 3 處、AWARDS188 4 句、
  `awardsPickPressNews` fallback、`awardsMetricEchoLabel` map；`awards63FellowsHtml` ★改法；
  `np214AwardPhoto214` 新 helper；`renderAwardResultHtml` 重寫；`presentAwardResult` 刪 toast；
  `enqueueNewspaperFromAward` ＋imgKey（2 處）。
- `assets/story/newspaper/photo_awi_ceremony.webp`、`photo_lok_ceremony.webp`（新）。
- `tests/test_newspaper214_award_logic.js`、`tests/test_newspaper214_award_static.py`（新）。
- `tests/test_awards186_static.py`、`tests/test_awards207_static.py`（斷言更新，見 §7）。

---

# NOTES_V20A214 — 殺青報紙＋WF3／story 報紙＋第二版厚度（工人 3）

分支 `v20a214`，基底 HEAD `ee27af9`（工人 1 核心渲染器＋工人 2 頒獎報紙已完成，未落地、未 push）。
**本票唔落地、唔 push。**做完即停，等統籌派下一棒測試＋實駕。

## 1. base 級殺青唔出報紙（用戶 2026-11-14 18:14＋18:15 已拍板）

- 截法：`enqueueNewspaperFromWrap`（`index.html` 約 L49314）入面，`press94IsBaseRole(gig94,
  labelHint94)` 為真嗰陣**直接 `return null`**，唔入隊、唔留去重 key（同一通告第日再殺青
  照排，唔會俾舊填位項食咗）。閘口係通告級別（`press94RoleClass`），唔係聲望——聲望低唔係
  唔出報嘅原因；named 級 fame＜15 照行 #104 淡紙。
- `press94FillLines` **成個刪咗**（連註解）：grep 全檔，報紙路徑只剩 `enqueueNewspaperFromWrap`
  一個用量，冇其他用量；刪後全檔只剩退役說明註解一處提到個名，冇死 code。分類器
  （`press94RoleClass`）＋「臨」徽章（`press94TierBadge`，通告卡照用）＋第一次點名里程碑
  （`press94ClaimFirstNamed`，只限真點名 nameTier 非 anon）全部留返。
- `enqueueNewspaperItem` 嘅 `press94` 欄位留返（舊隊列殘留填位項照解析，唔爆），但再冇
  `press94: "fill"` 寫入；註解已更新講明填位退役。
- **「一名臨記」留返**：named 級＋fame＜15 照行 `newspaperWrapFadeLines`（anon），新測試
  B06／B07 釘死（fame 5 男主角殺青照出報、fameDelta 0、文案含「一名臨記」）。
- 殺青當晚「殺青獎勵」sheet（`presentPostShootReward`）一字唔郁。

## 2. 空隊列唔出晨報（核實結果：本身啱，唔使修，加測試釘死）

- `newspaperDueItems(day)` 只係 filter `publishDay <= day`；`pullDueNewspaperEdition()`
  空隊列回 `null`（`if(!due.length) return null`），`presentDueMorningPaper` 唔彈——本身
  已經啱，冇改過呢兩個函數。base 殺青回 null 之後，嗰朝淨係得 base 殺青到期就係空隊列，
  走同一條路。核實方法：新邏輯測試 C01–C03（淨 base 入隊→day 4 `newspaperDueItems`
  空、`pullDueNewspaperEdition()` null、`pendingMorningPaper` 空）＋內置 `newspaperCheck()`
  ferry 段改寫（`ferry_next_none214`／`ferry_fame214`／`ferry_clip214`）。

## 3. 殺青報紙相片：通告作品海報

- 新 helper `np214WrapPoster214(gigId)`（放 `np214AwardPhoto214` 之後）：`gigId` →
  `poster59Path`（遊戲已有對應關係，唔自創）：POSTER59 base64 10 張＋POSTER85 檔案
  59 張，**共 69 張通告有海報**；`content/gigs_*.json` 351 張通告入面**其餘 282 張冇
  海報，唔出相，唔可以亂用唔關事嘅相**。key＝`np214_poster_<id>`（去 `gig_` 前綴），
  唔撞 WF3（`E1`–`E6`）同頒獎（`np214_award_*`）；註冊入 `NEWS82_IMGS`（工人 1 渲染器
  ＋剪報共用同一註冊表；`news_images_v82.json` 原檔唔郁），相片經渲染器黑白半調出
  （`.np214-photo`／`.np214-short-img` 自帶 grayscale 濾鏡）。
- 接入：`enqueueNewspaperFromWrap` named 路徑最後 `enqueueNewspaperItem` 加
  `imgKey: poster214 ? poster214.key : ""`——named／anon 都有相（相係作品海報，唔係
  玩家相，anon 一樣啱用）；冇海報嗰陣 `imgKey` 係 `""`，渲染器唔出相。base 路徑早已
  return null，唔會帶相。
- 有相例子：`gig_1988_film_04` → `assets/posters/poster-1988_film_04.webp`；
  POSTER59-only `gig_1988_film_03` → base64 data URI。冇相例子：`gig_1988_ad_01`
  等 282 張（新測試 D04／B09 釘死）。

## 4. WF3 世界事件報紙＋story 報紙（核實結果：本身啱，唔使修，加測試釘死）

- WF3：7 個世界事件全部 3 段 `paras`＋`imgKey`（`E1`–`E6`，全部喺
  `news_images_v82.json` 有 key）；`news82Tick` 入隊嗰陣 `dek:""`，所以新版式入面
  副題行（`dekStrip`）唔出、三段正文＋相出得啱，副題／正文唔重複（新測試 E01–E04）。
  做短訊嗰陣 `dek = paras.join("")`，出一次（E05）。
- story：`enqueueNewspaperFromStory` 冇 `imgKey`／冇 `paras`——單段 `dek` 做 lead 出
  一次、冇相（E06–E09），啱（story 模板本身冇相，唔可以亂配）。
- `buildNewspaperEdition` 排序（world 優先）／＞3 則摺疊（「同日還有 N 則」）／sideItem
  花邊全部唔郁（E10／E11 釘死）；`commitMorningPaper` 聲望結算、剪報上限 40、
  頒獎翌日／殺青＋2 嘅日子全部唔郁。

## 5. 第二版厚度：加真內容，唔係薄版接受

- 決定：**加樣本 v11 嗰兩個廣告格**（真內容）＋渲染器原有模糊填充字繼續做底層填充
  （shorts ≤2 先出），唔成版模糊字。花絮框唔加——樣本第二版嗰個花絮框係頒獎專屬
  （何生安慰＋入圍名單），唔係通用晨報內容，硬搬會失真。
- 新 helper `np214Page2Ads214()`：星光卡拉 OK（虛構；歡唱 $38／小時；旺角彌敦道
  123 號 3 樓；電話 388 4567）＋金龍茶餐廳（遊戲內真實地點，油麻地；菠蘿油・
  絲襪奶茶；通宵營業）——樣本 v11 原文一字唔改。用工人 1 已備好嘅 `.np214-adbox`
  CSS（之前未被引用，等呢格），**唔加新 CSS**（靜態測試 S26 釘死 4 條 rule 唔變）。
- 接入：廣告係**渲染層**出，唔入 `shorts`——唔計聲望、唔入傳聞、唔入剪報 short 數，
  edition 數據唔郁（F05 釘死）。每份有第二版嘅晨報都出（報紙固定欄位，同真報紙
  每日廣告一樣）；冇短訊嗰陣根本冇第二版，廣告亦唔出（F04，現有行為不變）。

## 6. 邊欄：留返，唔硬塞

- 工人 1 留低嘅「影視娛樂」欄名＋裝飾填充字留返：冇啱用嘅真內容可以搬入去——花邊
  短訊（`paperSideItemForDay`）已經喺第二版短訊列，搬入邊欄會同第二版重複；邊欄
  唔值得為填而填。靜態測試 S22 釘死邊欄原狀。

## 7. 工人 1 函數唯一觸碰點（報返統籌知）

- `renderMorningPaperHtml` 只加咗**一行**插入（第二版 `<div class="np214-shorts">`
  之後）：`${(typeof np214Page2Ads214==="function") ? np214Page2Ads214() : ""}`。
  渲染器其他行、NP214 CSS、`fmtNewspaperDate`、`newspaperFullName214`、
  `buildNewspaperEdition` 全部唔郁。呢行係第 5 節廣告格必需嘅唯一接入口；rebase
  嗰陣工人 1 嗰邊如果改咗第二版結構，呢行要對返。

## 8. 唔郁（本票範圍外）

- `renderAwardResultHtml`／頒獎報紙／術語（工人 2 嘅）；`renderMorningPaperHtml`
  其餘部分／NP214 CSS／`fmtNewspaperDate`／`newspaperFullName214`（工人 1 嘅，除 §7
  一行插入）；`buildNewspaperEdition` 排序、`commitMorningPaper` 聲望結算、剪報上限
  40、頒獎翌日／殺青＋2 嘅日子；典禮流程、v211／v212／v213 嘅改動。
- **推出日提及（用戶 18:19）：另開票，唔入 v214**——冇加 release 機制（靜態測試
  S16 釘死：冇 `source: "release"`／`releaseDay`）；範圍邊界＋建議形式見
  `qa214/PENDING_BASE_NO_PAPER.md`（統籌筆記，唔入 commit）。
- `qa214/` 係統籌筆記，唔入 commit。

## 9. 測試

- `node --check`（抽最大 inline script 段，4,445,266 字元）：PASS。
- 新測試（全部跟工人 1／2 嘅寫法：logic 用 extractFn／extractConst＋eval＋ok()；
  static 用 slice＋chk()）：
  - `tests/test_newspaper214_wrap_logic.js`：**46/46 PASS**。段：(a) base 閘 8 項
    （gig 崗位／labelHint／scale-only／fame 20 照截／唔 claim 第一次點名）
    (b) named 照舊＋淡紙 10 項（排期／聲望／第一次點名一次／「一名臨記」留返／
    有相／冇相）(c) 空隊列 5 項（淨 base 嗰朝 null＋named 到期先出）(d) 海報
    helper 5 項（檔案／base64／冇相 null／key 唔撞）(e) WF3／story 11 項
    （三段＋相／副題唔重複／story 單段一次／排序／摺疊）(f) 第二版廣告 5 項
    (g) 邊欄 1 項。
  - `tests/test_newspaper214_wrap_static.py`：**26/26 PASS**。段：(1) base 退役
    (2) 相片 (3) WF3／story＋排序／摺疊＋冇 release 機制 (4) 廣告＋邊欄
    (5) 紅線（工人 1／2 範圍唔郁、冇新 CSS）。
- 反證（pristine main `f58f19c`，`git show f58f19c:index.html` 抽出嚟＋兩個新測試
  放 `~/workspace/pristine214-counter/` 跑完即刪；content／assets 用 symlink，唔拷貝）：
  logic 測試乾淨 FAIL（`extract_all` 41／42 號 `np214WrapPoster214`／
  `np214Page2Ads214` 抽唔到，RESULT FAIL 1，exit 1，唔 crash）；static 測試
  RESULT FAIL 17（17/26 FAIL，exit 1，唔 crash）。
- 覆驗舊測試（全部 PASS，零回歸）：
  - logic：`test_press94_logic.js`（已更新，見下）、`test_wrap38_logic.js`（ALL PASS）、
    工人 1 `test_newspaper214_core_logic.js`（ALL PASS）、工人 2
    `test_newspaper214_award_logic.js`（45/45）、`test_awards186_logic.js`、
    `test_awards192_logic.js`、`test_awards208_logic.js`（全部 ALL PASS）。
  - static：`test_press94_static.py`（已更新）、工人 1
    `test_newspaper214_core_static.py`、工人 2 `test_newspaper214_award_static.py`
    （已更新 X04）、`test_awards186_static.py`、`test_awards207_static.py`、
    `test_awards208_static.py`（全部 PASS）。
  - 例外（pre-existing，唔係我引起）：`test_wrap38_static.py` 1 項 FAIL——
    `redline softRev s111 present`（現行 softRev 係 s107，檔內 `s111` 0 命中）；
    `git stash` 還原到未改 HEAD 再跑一樣 FAIL，證實改之前已經 FAIL，唔喺本票範圍。
- 舊測試要更新斷言（規格已改，唔係回歸）：
  - `tests/test_press94_logic.js`：第 C 段填位文案（6 項）改做退役斷言 3 項
    （函數已刪／入閘標記已清／閘口仍在）；分類器 A 段＋徽章 B 段一字唔郁。
  - `tests/test_press94_static.py`：S02 改做填位退役、S04 改做閘口回 null、
    S12 頁內自檢新契約改做 `ferry_gate214`／`hi15_gate214`／`p94_fill_gone214`。
  - `tests/test_newspaper214_award_static.py`：X04 由「`press94FillLines` 在位」
    改做「`press94FillLines` 唔在位」（工人 2 嗰陣 wrap 係唔郁範圍，家陣工人 3
    改咗，斷言跟住改）。
  - `index.html` 內置 `newspaperCheck()`：ferry／fadeExtra／fadeCrew／hi／p94f1·f2
    五段 base 斷言改新制（回 null＋唔入隊＋空隊列唔出晨報；`#103` 註解一併更新）；
    seed／fadeLead／hiLead／p94a·b 等 named 斷言一字唔郁。
- 唔跑全套（工人 4 做），唔實駕（工人 4 做）。實駕建議：base 殺青（例如天星碼頭
  過海路人）→＋2 日朝早無報紙；named 殺青有海報嗰陣第一版見到黑白海報相。

## 10. Rebase 注意

- **v211**（結果卡修法）：唔掂 `enqueueNewspaperFromWrap`／`press94*`／第二版廣告，
  同本票零重疊；但 v211 改咗 `renderAwardResultHtml`，而本票 §7 嗰一行插入喺
  `renderMorningPaperHtml`——兩個唔同函數，唔撞。
- **v213**（請柬提前＋晚上播）：掂 `presentAwardInvite`／`presentAwardResult` 一帶，
  同本票改嘅函數冇直接重疊。
- **v212**（典禮流程修復）：掂 `awards62PlayCeremony` 一帶，冇重疊。
- **v209**：掂藍若曦全身圖光邊，冇重疊。
- 落地次序（統籌定）：v211 → v212 → v209 → v213 → v214。本票 HEAD 未 push，
  rebase 嗰陣 `enqueueNewspaperFromWrap` 嘅 base 閘＋`newspaperCheck()` 五段新斷言
  要 keep（佢哋係用戶 18:14／18:15 已拍板嘅規格，唔係臨時改動）。

## 11. 改動一覽（`git diff --stat`）

- `index.html`（淨 −3,341 bytes）：刪 `press94FillLines`（連註解，改退役說明）；
  `enqueueNewspaperFromWrap` fill 分支改 early `return null`＋named 路徑加 `imgKey`；
  新 helper `np214WrapPoster214`＋`np214Page2Ads214`；`renderMorningPaperHtml`
  第二版加一行廣告插入；`enqueueNewspaperItem` press94 註解更新；內置
  `newspaperCheck()` 五段 base 斷言改新制。
- `tests/test_newspaper214_wrap_logic.js`、`tests/test_newspaper214_wrap_static.py`（新）。
- `tests/test_press94_logic.js`、`tests/test_press94_static.py`、
  `tests/test_newspaper214_award_static.py`（斷言更新，見 §9）。

# NOTES_V20A214 — 工人 4（最後一棒）：全套 A/B＋實駕驗證＋兩 bug 修復＋resync 收尾

## 12. 全套 A/B（pristine 現行 main `b1ca47a` vs 工作版）

- Pristine worktree `~/workspace/linji-pristine214`（detached HEAD `b1ca47a`，v211 已上線嗰版；唔用舊 `f58f19c`）。
- `qa131/run_suite.sh <repo-root> <outfile>`（outfile 一定要絕對路徑，腳本會 `cd` 去 repo root）。
- **基線：294 PASS／13 FAIL**（`qa214/suite_baseline214.txt`）；**工作版：299 PASS／13 FAIL**（`qa214/suite_work214b.txt`）。
- **FAIL 清單完全相同，零回歸。**13 項（全部 pre-existing）：`test_flash51_static.py`、`test_giglib36_static.py`、`test_pacing35_static.py`、`test_poster85_static.py`、`test_rumor49_static.py`、`test_slot50_static.py`、`test_soft_tip_111_restore.py`、`test_start53_static.py`、`test_weave43_static.py`、`test_weave44_static.py`、`test_weave49_static.py`、`test_wf5_87_static.py`、`test_wrap38_static.py`。已知：`wrap38`（`redline softRev s111 present`，現行 s107）同 `rumor49`（stale softRev 期望）。
- ＋5 淨數拆解：＋6 檔 v214 新測試全綠（`test_newspaper214_{award,core,wrap}_{logic,static}`），−1 檔 `test_awards211_static.py`——呢檔只喺 main 有，分支本身冇（見 §17，唔係回歸）。

## 13. 實駕（`qa214/drive214.py`，報告 `qa214/drive214.json`，截圖 `qa214/shots214/`，29 張全部親自讀過）

- **10/10 PASS，208 項檢查，每場 0 pageerror。**run2 9/10 之後補跑 multi 一場 PASS（run2 嗰兩項係 drive 期望錯，見下）。
- 各場（seed：1990 年 day 292＝10 月 20 日；典禮日＋1＝1990年10月21日 星期日）：
  - `film_won_932`／`film_won_700`／`music_won_932`：結果報紙（報頭 A、遊戲日期、全名陳偉翔、★ 圖例＋★ 陳偉翔玩家行、得主黑白相、factbox、冇 stub、冇 toast 遮嘢）＋翌日晨報（得主相＋聲望 ＋5／＋4）PASS。
  - `film_gallery_932`：結果報紙 ★ 鍾楚凝＋圖例、factbox 得獎鍾楚凝、無相（得主唔係駱家聲／玩家，啱規格）；翌日晨報寫明得主＋陳偉翔台下見證。PASS。
  - `film_declined_932`：推辭→電視直播版（captions 有「電視轉播」）→翌日推辭報紙寫明鍾楚凝奪獎、聲望未有變動、無相。PASS。
  - `wrap_named_poster`：`gig_1988_film_03` 武師配角／《神探闖天關》→＋2 日晨報第一版黑白海報相＋編輯按第一次點名＋聲望 ＋1。PASS。
  - `wrap_anon`：同一通告 fame＜15→「一名臨記」，唔出玩家名，海報相一樣有。PASS。
  - `wrap_base`：`gig_1988_film_04` 伴舞臨記（真 base，有海報都唔出）→＋2 日朝早無報紙、無報紙 sheet。PASS。
  - `morning_multi`：5 則同日（film_03 殺青＋tv 殺青＋頒獎 gallery＋WF3 E1＋rec 殺青）→頭版係 E1、三段正文＋遊行黑白相、第二版 3 短訊＋「同日還有 1 則」＋星光卡拉 OK／金龍茶餐廳廣告格。PASS。
  - `wf3_e1`：E1 單獨成報→頭版、三段正文、遊行黑白相（138px 浮動左邊，跟樣本 v11）。PASS。
- run1→run2 期間修正嘅 drive 問題（全部係 drive 期望／數據錯，唔係 code bug）：
  - `gig_1988_film_04` 真實數據係《霓虹星途》伴舞臨記（base 級），`fromWrap` 回 null 係啱嘅——工人 3 嘅例子用咗 stub 假數據（film_lead_big）。named＋poster 場改用真 named＋有海報嘅 `gig_1988_film_03`（武師配角／《神探闖天關》／POSTER59 內嵌）；base 場用返 `film_04`（有海報但係 base，驗海報唔漏入 base 報紙）。69 張海報通告入面 59 張係 named 級、10 張係 base 級（臨記／替身 label）。
  - 世界事件 `enqueuedDay` 必須同批其他則一致——`pullDueNewspaperEdition` 只取最早 `enqueuedDay` 嗰批（run1 將 E1 設咗 294，其他三則 293，E1 成期唔入）。
  - 摺疊行「同日還有 N 則」本身係短訊一員，只放第二版（`renderMorningPaperHtml` 註解寫明）；第一版係頭條全文，唔出摺疊行。
  - 廣告名係「星光卡拉 OK」（有空格），唔係「星光卡拉OK」。
  - gallery 結果報紙唔提玩家（佢只係台下觀眾；玩家名喺翌日晨報 dek）；相片期望跟得主：陳偉翔／駱家聲先有相，其他得主冇相。
  - `wrap_base` 開住嘅 modal 係 new_game 留低嘅 C1 劇情 modal，唔係報紙——驗 `paperPresent` 唔係 `modalVisible`。

## 14. 兩隻真 bug（實駕捉到，只限新 NP214 code，已修＋補測試）

- **B1：`np214ShowPage is not defined`（8/10 場 pageerror）。**函數喺 L49893 有定義，但喺 IIFE 入面唔係 global；四處 inline `onclick="np214ShowPage(this,2/1)"`（L47267、47284、50069、50084）撳落去就爆。修法：定義後加 `try{ window.np214ShowPage = np214ShowPage; }catch(_e){}`（跟 `window.__newspaper` 同一 pattern）。測試：`test_newspaper214_core_static.py` 新 `F03b_show_page_global`。工人 1／2／3 嘅邏輯測試用 extractFn＋eval，唔經 DOM onclick，所以漏咗。
- **B2：won 版同屆提名行唔見玩家＋圖例（v211 C1 俾工人 2 誤刪）。**工人 2 將 🏆 轉 ★ 嗰陣成段 v211 C1 刪走埋——`isWon211` unshift 玩家行＋`(win || isWon211)` 圖例條件。對照 pristine `b1ca47a` 實駕證實：舊卡「同屆提名（🏆 為得主）：🏆 阿偉《新春大吉》、陸柏言…」，新報紙得返 3 個對手、無圖例、無 ★。修法：`awards63FellowsHtml` 還原嗰段，★ 版＋全名——`parts.unshift("★ 陳偉翔" + (repWorkTitle ? "《" + repWorkTitle + "》" : ""))`，`head = (win || isWon211) ? "同屆提名（★為得主）" : "同屆提名"`（報紙寫全名，唔用「阿偉」）。測試：logic 新 `c6b`／`c6c`、static 新 `S02b_won_player_row_restored`（`tests/test_newspaper214_award_logic.js`／`tests/test_newspaper214_award_static.py`）。受影響測試重跑全綠（award logic 47/47、award static、core static、`test_awards207_static.py` 0 FAIL、wrap logic／static）。
- 唔修（pre-existing，記低等拍板）：① 推辭晨報 dek 重述得主行（標題喺 dek 再出現一次，`awardGalleryCopy149`／`dek149` v149 寫法，v214 冇郁）；② 花邊短訊池 v13 舊文案兩 typo（L49740：標題「喜劇片場場爆滿」多咗個「場」、內文「要逐日mark。」英文 mark 冇空格）。

## 15. Resync 完成（`qa214/resync214.py`，13 檔全部 PASS）

- 對位：f58f19c（61714 行）→ 工作版，difflib＋內容逐字核實，全部純漂移（除 kwan151 31149 拆行特殊處理：工人 2 將 `TEXTFIX55_EXACT` 成行拆開，舊目巨行落去 31337，B3／B4／B5 子串逐個核實，見 `qa214/resync214.py` 註解）。**總行數 61714→62082（淨 ＋368：工人 1–3 ＋356＋工人 4 兩 bug 修 ＋12；檔案 5,503,860 bytes）。**
- 已套用 13 檔：text125（3 錨點）、travel114（47 處＋DEF／WRAPPER）、kwan151（13 錨點）、tang152（3）、tang171（總行數＋DEF 56554）、tang173（總行數＋DEF＋L4862 live 行 4954→5124）、rom176（6）、gift185（總行數）、poster85（上限 5,503,860＋40,000）、ux68（上限 5,545,000）、book143（24px 計數 1→2，NP214 報頭）、icons112（psr kicker 退役→報紙 kicker）、venue99（場地行 kicker array＋`np214-kicker`）。
- 腳本本身三個 bug（上一棒未跑到／未發現，工人 4 修埋）：
  1. `count('\n')` pattern backslash 數錯（腳本 2 個、測試檔 1 個），tang171／173／gift185 永遠 match 唔到——改做 1 個。
  2. poster85 新文字入面字面 `% (` 冇 escape，`%` formatting 爆 `ValueError`——改做 `%%`，上限數字改用 `SIZE_NEW` 動態計。
  3. rom176 逐對 replace 撞值：54616→54984 之後，54984 嗰對將佢一併換埋做 55352（L84 兩次換錯）。改做單次掃描 dict 查表（`replace_map_once`）＋已套用 guard（54984 同時係舊號同新值，數值掃描分唔到；L84 最後用人手按 check 名定死：`line(54984)`，L85 `line(55352)`）。教訓已合併入 AGENTS.md v160 嗰條：唔好逐對 re.sub。
- 工人 4 兩 bug 修加咗 12 行（fellows ＋9、window 掛載 ＋3），插入點 L48865／L49914 之後嘅錨點一併 ＋12（travel114 26 處＋DEF、tang171／173 總行數＋DEF）；插入點之前嘅錨點唔郁（tang173 L4862 錨點 5124 唔受影響）。

## 16. 相片做法總結

- 頒獎結果報紙第一版＝得主相：玩家贏用陳偉翔典禮相（`assets/story/newspaper/photo_awi_ceremony.webp`，黑白半調）、得主係駱家聲用駱家聲相、其他得主冇相（factbox 頂位）；第二版＝玩家相只限入圍落選（贏嗰陣第一版已經係陳偉翔相，唔重複；旁聽冇玩家相）。
- 殺青報紙第一版＝作品海報黑白相：`np214WrapPoster214`→`poster59Path`（POSTER59 10 張內嵌 base64＋POSTER85 59 張檔案，共 69 張通告有海報）；anon 一樣有（作品相唔係人相）；base 級唔出報紙所以唔出相。
- WF3 世界事件＝事件相（E1 遊行相，138px 浮動左邊，跟樣本 v11）；晨報短訊有圖嗰則出黑白小圖（multi 第二版 film_03 海報大相）。
- 全部相片經 `np214AwardPhoto214`／`np214WrapPoster214` 揀相，唔係寫死；相片黑白化由 CSS（`np214-photo img` 灰階）做，唔使另外出黑白檔。

## 17. Rebase 注意（更新：分支未入 v211）

- **分支 base 係 `f58f19c`，早過 v211——v211 全部唔喺分支度**（`hideToast211`／`HS211`／`topW211`／`win211`／`wonCat211` 全部 0 命中；得 v207 舊 `spotlight207`）。rebase 上 main `b1ca47a` 嗰陣，v211 嗰邊會一次過入嚟，預期衝突區：`renderAwardResultHtml`／`presentAwardResult`（v211 A1＋B2＋C1 同 v214 報紙重寫同一函數）、`awards62PlayCeremony`（v211 B1／B7 舞台幾何，v214 唔郁，應該乾淨合併）、`renderAwardInviteHtml`（v211 C3 席位去重，v214 唔郁）。
- **`tests/test_awards211_static.py` 只喺 main 有，分支冇。**工人 4 試過帶返嚟：對住分支跑 25 項 FAIL（因為 v211 本身未入），已刪返，唔入 commit。rebase 之後呢檔會返嚟，其中 **B2（4 項）＋C1（1 項）必須按 v214 規格更新**，否則全套多 5 項 FAIL；其餘 A1／B1／C2／C3／B7 應該原封不動 PASS（v214 唔掂嗰啲區）。適配寫法（意圖不變）：
  - B2 第二版重寫：`wonCat211`／`{ star: "阿偉", ... }`／`awardWinLine149(win211)`／`const win211 = win149 ||` 全部退役，改驗 `playerWinLine214`＋`陳偉翔憑《`＋`rep214`（won 動態點名玩家＋代表作）、`metricHead214`＋`winLine214 || playerWinLine214`（第二版用真得主數據）、`const winLine214`＋`awardWinLine149(win149)`（gallery／提名版跌返 win149）；stub 後備改驗**冇**「典禮後仍有人提起」＋跌返散場句——留意：`renderAwardResultHtml` 入面有條註解本身提到呢句 stub 字串，斷言嗰陣要先剝走 `/* */` 註解，唔係會誤判。
  - C1：`parts.unshift(iconHtml112("🏆") + " 阿偉"` 改做 `parts.unshift("★ 陳偉翔"`（`isWon211`／`c.repWorkTitle`／`(win || isWon211)` 不變）。
- v211 C3 請柬席位去重未入 v214（invite code 零重疊，rebase 應該乾淨入）。
- 落地次序（統籌定）：v212 → v209 → v213 → v214。本票 HEAD 未 push。

## 18. 改動一覽（`git diff --stat`，相對 HEAD `5ebd623`）

- `index.html`（淨 ＋12 行，＋1,081 bytes）：`awards63FellowsHtml` 還原 v211 C1 won 玩家行（★＋全名陳偉翔）；`np214ShowPage` 掛 `window`（inline onclick 用）。
- `tests/test_newspaper214_award_logic.js`（＋4 行：c6b／c6c）、`tests/test_newspaper214_award_static.py`（＋1 項 S02b）、`tests/test_newspaper214_core_static.py`（＋1 項 F03b）。
- 13 檔 resync（見 §15）：`test_text125_static.py`、`test_travel114_static.py`、`test_kwan151_static.py`、`test_tang152_static.py`、`test_tang171_static.py`、`test_tang173_static.py`、`test_rom176_static.py`、`test_gift185_static.py`、`test_poster85_static.py`、`test_ux68_static.py`、`test_book143_static.py`、`test_icons112_static.py`、`test_venue99_static.py`。
- `qa214/`（唔入 commit）：`drive214.py`（run1→run2 修正）、`drive214.json`（run2＋multi 補跑）、`drive214_run1.log`／`drive214_run2.log`、`suite_baseline214.txt`、`suite_work214.txt`（run1 舊）、`suite_work214b.txt`（最終）、`resync214.py`（＋單次掃描 helper＋三 bug 修）、`probe_won_pristine.py`（pristine 對照 won ★）、`PENDING_BASE_NO_PAPER.md`（統籌筆記）。

## 19. Rebase 上 main `d1239d4`（v213）＋重驗（落地統籌，2026-11-14）

- 分支舊 HEAD `5fa653e` → rebase 上 main `d1239d4` → 新 HEAD `8a388c4`（amend 入 rebase 適配）。`index.html` 62,352 行、5,524,996 bytes（淨 ＋358 行 vs main）。
- 衝突（全部已解＋核實）：第 2 粒 commit `ee27af9`（頒獎報紙）`index.html` 3 處，全部取 v214 呢邊——① `renderAwardResultHtml`（v211 `wonCat211`／`win211`／`metricLine` psr-card stub 版退役，留 v214 報紙 page1／page2）；② `presentAwardResult`（v214 註解留返，v211 `hideToast211()` 呼叫在場）；③ `awards63FellowsHtml`（取 v214 `head = win? "同屆提名（★為得主）"`，第 4 粒 commit 嘅 B2 修復之後補返 won 玩家行）。第 1 粒（核心渲染器）＋第 3 粒（殺青報紙）乾淨合併。第 4 粒 `5fa653e` 10 個靜態測試檔衝突，取 main 版（ours）：gift185、kwan151、poster85、rom176、tang152、tang171、tang173、text125、travel114、ux68；book143、icons112、venue99 乾淨合併。
- Rebase 後核實全部在場：B1 `window.np214ShowPage` 掛載；B2 won 玩家行 `parts.unshift("★ 陳偉翔"…)`；v213 `awardBooked213` 10 命中；v211 `HSC211`／`FLOOR = Math.round(314 * HSC211)`；v212 `cardsInnerHtmlFor208`＋`glamour-hide`；`node --check` 最大 inline script 段 PASS（4,461,680 bytes）。
- `test_awards211_static.py` B2（4 項）＋C1（1 項）已按 §17 更新做 v214 規格（`playerWinLine214`＋`陳偉翔憑《`＋`rep214`、`metricHead214`＋`winLine214 || playerWinLine214`、`const winLine214`＋`awardWinLine149(win149)`、stub「典禮後仍有人提起」剝走註解後 0 命中＋跌返散場句、C1 改 `parts.unshift("★ 陳偉翔"`）。**TOTAL FAIL 0，47 PASS**；反證對 pristine main `d1239d4`：嗰 5 項乾淨 FAIL（唔 crash）。
- c7 修復：`test_newspaper214_award_logic.js` c7（presentAwardResult 唔再叫 toast）rebase 後 FAIL——原因係 v211 嘅 `hideToast211()` 註解本身寫住 `toast()` 字面。修法：先剝走 `/* */` 註解再驗＋斷言 `hideToast211()` 在場（同 B2 stub 陷阱同一做法）。**Award logic 47/47 PASS**。
- Resync（`qa214/resync214_rebase.py`，difflib 對位＋內容逐字核實，全部純漂移）：9 檔全部 PASS——text125（3 錨點）、travel114（COUNT 12＋FREE 33＋DEF 56466→56824＋WRAPPER 45200→45390）、kwan151（13 錨點，含 31150 exact-split 特殊：TEXTFIX55_EXACT 成行俾工人 2 拆開，舊目巨行落去 31338）、tang152（3）、tang171／tang173（DEF＋總行數 61994→62352）、rom176（6）、gift185（總行數）、ux68（上限 5,510,000→5,565,000，標籤加「v214 NP214 報紙重做有意增長至 5,524,996」）。腳本中途斷過一次：`tang173 lines[4954]` 斷言寫咗 4 次，實際 8 次（`grep -c` 數行唔係數出現次數）——已修正做 8。
- 新測試全部 PASS：core／award／wrap logic＋static 六檔（award logic 47/47）；相關舊測試全部 PASS：awards211 static（47）、awards186／awards207 static、press94 static＋logic、awards208 static＋logic、awards186／awards192／wrap38／awards178／polish48 logic。
- 全套 A/B（`qa131/run_suite.sh`，pristine `d1239d4` vs 工作版；pristine 用 `linji-pristine214r` worktree）：**baseline 299 PASS／13 FAIL vs 工作版 305 PASS／13 FAIL（＋6 新檔，0 新 FAIL）**。13 項 FAIL 兩邊完全相同（flash51、giglib36、pacing35、poster59、rumor49、slot50、soft_tip_111_restore、start53、weave43、weave44、weave49、wf5_87、wrap38）——全部 pre-existing 穩定 FAIL，零回歸。
- 實駕重跑（`qa214/drive214_rebased.py`，報告 `qa214/drive214_rebased.json`，截圖 `qa214/shots214_rebased/` 35 張）：**10/10 場 PASS，223 項檢查 0 壞，0 pageerror**（film_won_932／700、music_won_932、film_gallery_932、film_declined_932、wrap_named_poster、wrap_anon、wrap_base、morning_multi、wf3_e1）。
- 實駕要適配 v213 晚上播（原版 `drive214.py` 喺 v213 流程會斷，唔係遊戲 bug）：① 新局之後遊戲停喺屋企行程手帳，唔係地圖——new_game 後即 `settle_to_map` 先；② 出席／推辭只係預約，典禮今晚先播——撳掣後設 weekPlan 全 rest、跑一日、日結板、返地圖、晚上舞台先出現；③ `run_day_via_map` 喺 settle 一次 modal-stuck 就即刻返 False，而 C1 重播尾段「劇情結算」modal 掣有 race——包咗 `run_day_retry`（最多 3 次）；④ 結果報紙／晨報相片讀數 race——`paper_ready` 等相 load 完（nw>0）先讀；⑤ v213 流程撳「收下這晚」之後晨鏈即刻自然出晨報食咗 queue——queue 一定要喺撳掣之前影低（推辭案 queue 讀到嗰陣已經空咗，因為晨鏈喺 finishSkip 之後同步跑埋）；⑥ 推辭嗰則係短訊放第二版（第一版係 C1 故事頭條），`innerText` 唔包 `display:none` 第二版——推辭三項斷言改用 sheetText＋pages 拼埋驗；得主係鍾楚凝憑《凶樓夜半怪談》奪獎，唔係玩家，符合 v149 B2。
- 附帶核實（唔係 v214 改動，實駕順便見到）：v213 晚上播＋v214 報紙一齊行得通——請柬日預約→典禮日跑一日→晚上舞台→結果報紙→翌日晨報；推辭→電視直播版→第二版短訊寫明得主。請柬顯示日期有個舊問題（force 逾期 pack 顯示「9月1日」但預約係今晚 10 月 20 日，`awards213CeremonyDayForPack` 用 `Math.max(季節首日, 今日)` 做預約日，但請柬文案讀季節首日）——只影響 debug force 逾期路徑，真實流程請柬提前 3 日唔會逾期，唔入呢票，留返 v213 跟進。
