# NOTES · v20a38 收尾修復包（WRAP_FIXES）

背景：v20a37 再驗證試玩（2026-11-09 實機，新檔 3 次殺青）大半通過，淨返三個問題：
殺青反響跨次重複、反響文案唔跟場景、手帳拍攝中卡冇待入帳標示。本票逐項修復，
測試行真路徑（tests/test_wrap38_logic.js／test_wrap38_static.py）。

紅線：冇改 SAVE key（starVolunteer_map_v19w）、softRev（s107）、?v=（v20a10）、
content pack JSON。新存檔欄 S.psrRecent38 係加喺既有 S 物件（save 本身成個
JSON.stringify(S)），舊檔冇呢欄自動當空，唔使改 SAVE key。

---

## 基線同步（開工前）

主副本 ~/workspace/linji-work/ 開工時停喺 v20a36 世代（分支狀態）；v20a37 喺獨立副本
linji-work37 做完已入 main（merge commit d62289d，main head 經 connector 核實）。
同步做法：將 v20a37 推入 repo 嗰 8 個路徑（以 linji-work37 嘅 snapshot sync 紀錄為準：
index.html、NOTES_V20A37_VERIFY_FIXES.md、tests/test_verify37_logic.js、
tests/test_verify37_static.py、tests/test_guidance34_logic.js、
tests/test_guidance34_static.py、tests/test_weave31_logic.js、
tests/fixtures/behavior_gate_c1_c5.json）由 linji-work37 overlay 落 linji-work；
再 curl 線上部署版逐字節 cmp——2,482,922 bytes 完全一致，先至落手。
（教訓：第一次 diff 輸出俾 head 截斷，漏抄 test_weave31_logic.js，即刻俾基線測試
3 條 headline FAIL 捉返，已補抄並做完整 diff 複查至零差異。）
兩份 sync 紀錄（linji-work／linji-work37）條目本身冇衝突：前者去到 v20a36 分支
commit e4e6729，後者係 v20a37 分支 commit 5eb80b3；以 repo 最新 main（d62289d）
為準同步，如上。

---

## 修復 1：殺青反響跨次重複

**根源（實證）**：v20a35/37 嘅防重複係 `psrPickNoRepeat35`＋`_psrLastPick35`——
只記**最近 1 張**、而且係 module 變數**唔入存檔**（session 一完即清零）。
池大嗰啲 channel 冇事，但收視關注（metrics ratings 池得 2 張靠交替先冇事）、
電視週刊（press 電視 typed 池 3 張）呢啲細池：第 1 次抽 A、第 2 次被迫非 A、
第 3 次 A 已唔喺「最近 1 張」記憶入面，照出——實機第 1、3 次逐字相同就係咁嚟。
另外仲有一個隱藏消耗：`buildPostShootRewardPack` 舊流程每份 pack 抽齊
press/news/fans 三個 channel 再 shuffle 揀 1–2 張入卡，**冇入卡嗰啲抽選一樣
改寫 _psrLastPick35**，令顯示出嚟嗰啲卡嘅輪替俾隱形抽選夾亂。

**修法**：
- 新 `S.psrRecent38[channel]`：每 channel 存最近 **3 張**出過嘅卡 id（最新喺頭，
  入存檔、跨 session 有效）。`psrRecent38()` 懶建立＋爛值自癒（唔係陣列就重置）。
- `psrPickNoRepeat35` 改行記憶排除：排除最近 min(3, 池大細−1) 張——保證至少
  留返 1 張候選；萬一排除到空（記憶同細池交疊）逐級放寬（3→2→1→0），永不死鎖。
  S 唔存在嗰陣退化用返 `_psrLastPick35` 最近 1 張（舊行為，測試 sandbox 兼容）。
- `buildPostShootRewardPack` 改做**入選先抽**：先 shuffle channel 次序、定
  入選 1–2 個 channel，先抽入選嗰啲模板嚟組卡；press 因為 pressSeed（報紙種子）
  每份都要用，照每份抽（佢嘅「出」就係報紙＋入卡兩路）。咁記憶記嘅係真・出過
  嘅卡，顯示層面嘅最近 3 次（池夠大時）保證唔重複。

**驗證**（test_wrap38 段一，真 buildPostShootRewardPack）：綜藝連組 24 份——
fans（any 池 5 張）出現序列最近 3 次內零重複；press（typed 池 3 張）最近 2 次內
零重複（池細自動放寬）；metrics（池 2 張）唔連續重複；記憶真入 S.psrRecent38
且最新一張對得返；舊存檔冇欄／爛欄（字串、數字）組裝唔爆。

---

## 修復 2：反響文案唔跟場景

**根源**：反響池有幾張場景味強嘅卡冇任何適配標籤，`postShootPickTemplate` 只按
工種（matchTypes）分池——《天星碼頭》（電視劇）同任何電視劇共用 typed 池，
「深宵廠景煞科」嗰張（夜晚＋廠景）照抽得中，碼頭日間外景完全唔對味。

**修法**（克制版）：新 `PSR_SCENE_TAGS38` 標籤表（index 側，以模板 id 對照，
pack 卡同增補卡一視同仁），**只標 3 張**明顯場景綁定嘅卡（逐張審計成池後嘅
結論，其餘全部係通用文案，唔標＝永遠合資格）：

| 模板 id | 文案 | 標籤 | 理由 |
| :--- | :--- | :--- | :--- |
| psr35_press_tv_02 | 深宵廠景煞科，新面孔企到尾 | night + studio | 深宵＋廠景，dek 仲有「趕夜班」 |
| psr35_press_film_02 | 外景煞科，新人臨記跟足全程 | outdoor + day | dek「嗰場外景曬足成日」，夜景都唔啱 |
| psr35_news_film_02 | 電影組外景煞科，武指點名讚新人 | outdoor | 明示外景；冇時間味，夜景外景照啱 |

冇標嘅例子（刻意保留通用）：press_tv_01「廠景殺青」係電視工嘅行內通用講法、
fans 廠門口／街口係出現地點唔係拍攝場景、psr35_press_rec_02「錄到半夜」本身
俾唱片通告 matchTypes 鎖死、場景錯配風險低——按「範圍克制」唔標。

**場景推導**（`psrSceneForShoot38`，保守）：用 shoot record 嘅 workTitle／title
＋以 gigId 查返 GIGS 原工嘅 workTitle／title／blurb／synopsis／roleHint 拼成
文本，關鍵字推導：夜（夜／深宵／夜半／夜景／晚間）、外景（外景／碼頭／海傍／
街景／街頭／天台／沙灘等）、廠景（廠景／廠內／片廠／攝影棚／錄音室；有外景
關鍵字嗰陣外景優先，唔疊 studio，費事「電視廠街景」呢類誤判）。外景＋冇夜
關鍵字 → 補 day。推唔出任何標籤 → 回 null＝唔過濾（寧願用通用抽選，唔好
過度過濾）。`psrSceneFilter38`：標籤卡要全部標籤命中先留低；濾到空 → 回退
原池（安全 fallback）。四個 channel（press／news／streetFans／metrics 命中池
＋metrics fallback）統一經 `postShootPickTemplate(channel, gigType, scene38)`
或同一 filter 入口，冇旁路。

**驗證**（段二，真組裝各 60 份）：《天星碼頭》夜晚廠景卡 0 次；夜晚廠景電視工
（《深宵疑雲》廠景群演）抽中 ≥3 次（唔係一刀切封殺）；日間外景電影工 press／
news 外景卡各抽得返；夜晚外景（《猛鬼碼頭夜話》）「曬足成日」卡 0 次；冇關鍵字
嘅工（推唔出場景）夜晚廠景卡仍然入池（冇過度過濾）。
連帶更新 test_verify37 段二 (c)：舊斷言「《天星碼頭》要抽中深宵廠景卡」係
v20a37「去具名後要入返輪替」嘅驗法，俾 v20a38 場景適配正式取代——改斷言
碼頭工永不抽中＋夜晚廠景工抽得返；test_verify37_static item2b 嘅 fallback
呼叫字串同步加 scene38 參數（單抽不變量冇變）。

---

## 修復 3：手帳「拍攝中」卡冇待入帳標示

**根源（實證）**：v20a37 支票將「（殺青後入帳）」加咗落 `showJobs()`（拍攝簿
modal）張卡——嗰張真係有齊數。但玩家日常喺**手帳行程編排**見到嗰張拍攝中卡
係 `workItems()` 出嘅行：hint 寫「檔期已定：共 X 日製作 · 進度 a/b · 剩餘 c 日
· 拍攝限期：…（餘 N 曆日）；…；逾期將扣除違約金 $…」——檔期／進度／限期／
違約金齊晒，唯獨冇入帳標示。加錯卡，唔係冇加。

**修法**：新 `shootPendingLine38(sh)`——用返 shoot record 已存嘅待入帳數
（pay／fame／popularity，同 showJobs 同源，scheduleShoot 獲聘嗰刻已鎖定，
唔使補存）；`workItems()` 嗰行 hint 尾加「 · 殺青後入帳：約酬 $X · 聲望 +Y ·
人氣 +Z」。舊 record 缺欄／非數字 → 畀返嗰個欄位唔出；三個數全缺 → 只出
定性版「殺青後入帳」，保證唔出 NaN。

**驗證**（段三，真 workItems）：新 record（$1,164／+5／+17）出齊正確數額＋
保留原檔期／進度字樣；舊 record（冇三個欄）出定性版、冇 NaN、冇約酬；
半舊 record（得 pay）出約酬、冇 NaN。

---

## 測試總覽

- 新增 tests/test_wrap38_logic.js（三段、全真路徑）＋tests/test_wrap38_static.py。
- 改舊測試兩處（理由見上）：test_verify37_logic 段二 (c) 斷言＋抽取清單
  （加 psrRecent38／psrSceneForShoot38／psrSceneFilter38／PSR_SCENE_TAGS38）、
  test_verify37_static item2b 字串。
- 既有全套（logic 24 檔＋static 27 檔）＋新測試全過，零回歸；
  index.html 主 script node 語法檢查 OK。
