# NOTES_V20A306 — Q19 齊鎮海 FRAME cap／wrap 各寫兩個版本

- 版本：v20a306（Q19）
- 基線：main `e385c82`（v305，suite 368／9）
- 結果：suite 369／9（基線 368／9；+1 係新測試 test_r306_chai_frame.js；9 項 pre-existing FAIL 不變：flash51／slot50／soft_tip_111_restore／start53／weave43_static／weave44_static／weave49_static／wf5_87／wrap38）；Pages md5 `ff8d425a1edb2e2f1ba2897d13b50eea`／4,693,683 bytes（見 §7）
- 新測試：`tests/test_r306_chai_frame.js`（35 項，ALL PASS）
- 行數：index.html 47229 → 47239（＋10 行：FRAME 新欄＋註解 4 行＋wrap 換句 3 行＋cap 換句 3 行）
- 順手執：NOTES_V20A305 header「Pages md5 ＿＿＿／＿＿＿ bytes」填返實數 `b011862d8d3ec191983f3b214240fe4b`／4,692,106 bytes。

## §1 設計：兩個版本點分，邊句係預設

題目：cap／wrap 各寫兩個版本，按 Beat 5（chai_repay）try_new／play_safe 分流。

親查 live 之後，舊嘅兩句本身已經各有傾向——唔係中立句，唔可以亂派：

- 舊 cap 句「阿偉，今日傾到呢度先啦，我仲有場戲要默。你有呢份心，我領咗，不過有啲路，仲要慢慢行，唔好急。」——「慢慢行，唔好急」就係 play_safe 嘅口徑（同 Beat 5 play_safe 選擇回應「慢慢嚟都啱。呢行捱得慢先係正常」同一路）。所以舊 cap 句＝play_safe 版，留做預設。
- 舊 wrap 句「殺青喇，阿偉。同你做呢套戲，我冇睇錯人。嚟緊嗰條路點行，你自己企穩，我會喺後面望住。」——「你自己企穩，我會喺後面望住」係放手畀佢行嗰邊，同 try_new 嘅膽色一路。所以舊 wrap 句＝try_new 版，留做預設。

新寫兩句（廣東話對白，唔係旁白）：

- cap_try（try_new 版）：「阿偉，你肯試新嘢，呢份膽色我認。不過膽色唔係火候——等你試埋嗰個角色，企得穩先，我哋先再傾。」——認咗膽色先，再話火候未夠，叫佢試埋嗰個角色先返嚟傾；同其他星 cap 句「等你…先再傾」同一體裁。
- wrap_safe（play_safe 版）：「殺青喇，阿偉。呢套戲你企得穩，冇浮冇躁，已經好難得。慢慢嚟唔係慢，係行得穩，之後嗰條路，你照咁行，我放心。」——肯定企得穩本身，唔係叫佢追；同 try_new 版「你自己企穩，我會喺後面望住」（放手望住）對照：一個係「照咁行，我放心」，一個係「你自己行，我望住」。

預設即舊句：未揀 Beat 5／舊檔（無兩旗）行為逐字唔變。

## §2 實裝：數據放 FRAME，換句喺 enc79BuildScript

跟 v278／v305 前例（flag-based 換句，唔開新表）：

1. `ENC83_FRAME_chai_zanhoi` 加 `cap_try`／`wrap_safe` 兩欄＋註解（舊 cap／wrap／stageup 一字唔郁）。註冊（L41697）唔郁——預設 cap／wrap 照舊入 `ENC79_CAP_LINES`／`ENC79_WRAP_ECHO`。
2. wrap 讀取點（enc79BuildScript，`st.wrapEcho` 分支）：play_safe 有旗就用 `ENC83_FRAME_chai_zanhoi.wrap_safe`，否則舊句。用 `typeof … !== "undefined"` 守住——其他測試 sandbox 未必有 FRAME 常數，唔守會 ReferenceError。
3. cap 讀取點（同一函數，`st.capHit` 分支）：try_new 有旗就用 `cap_try`，否則舊句；同樣 typeof 守住。
4. v305 finale 尾句換句機制一行唔郁（刻意唔統一：finale 用硬字面係 v305 剛落地嘅機制，改佢慳唔到幾多，反而多一次風險；FRAME 兩句同 finale 兩句係同一對句，註解有 cross-reference，唔會靜默分叉——r306 (D) 有回歸測試守住）。

分流總表（cap／wrap 各自獨立，兩旗理論上唔會齊有，防禦寫明優先）：

| 旗 | cap 句 | wrap 句 |
|---|---|---|
| chai_try_new | cap_try（新） | 舊 wrap 句 |
| chai_play_safe | 舊 cap 句 | wrap_safe（新） |
| 無旗（未揀／舊檔） | 舊 cap 句 | 舊 wrap 句 |
| 兩旗齊有（防禦） | cap_try | wrap_safe |

## §3 守住嘅嘢

- stageup 3 句逐字唔郁；暖版閘（truth_change＋try_new）唔郁；冷版 heartCold／提攜冷版 f 郁；finale 6 句＋尾句分流唔郁；其他星 cap／wrap 唔郁。
- 舊檔唔 crash：無旗嗰陣兩句都係舊句，buildScript 照行（r306 (E) 覆蓋 fav 70／1992 冬舊檔）。
- Beat 5 抉擇本身唔郁：chai_try_new／chai_play_safe 授出點仍然唯一（各 3 處：抉擇 flags 1 處＋讀取 2 處；r306 (F) 數過）。

## §4 測試：tests/test_r306_chai_frame.js（35 項）

sandbox 跟 r305（eval 抽出 consts＋fns；加抽 `ENC83_FRAME_chai_zanhoi`，註冊照 L41697 手動做返）。

- (A) 數據 9 項：cap_try／wrap_safe 係 S 句、非空、唔等於舊句、主題分得開（膽色／試埋嗰個角色 vs 冇浮冇躁／慢慢嚟唔係慢）；stageup 3 句逐字；註冊預設係舊句。
- (B) cap 分流 6 項：try_new→cap_try、play_safe→舊 cap、未揀→舊 cap、兩旗→cap_try；capHit 唔係 true 唔出句；播完清 capHit。
- (C) wrap 分流 6 項：對稱（play_safe→wrap_safe、try_new→舊 wrap、未揀→舊 wrap、兩旗→wrap_safe；wrapEcho 唔係 true 唔出句；播完清 wrapEcho）。
- (D) 唔受影響 4 項：暖版 heart 照播（truth_change＋try_new）；壞旗播 heartCold唔播暖版 heart；finale 尾句分流照舊（try_new→wrap 句、play_safe→cap 句，6 句）。
- (E) 舊檔 3 項：無旗、fav 70、1992 冬 → 唔 crash，cap／wrap 都係舊句。
- (F) 靜態 7 項：陸 cap／wrap 唔郁；兩旗各出現 3 次；finale 機制＋6 句唔郁；提攜冷版唔郁；gigs_new.json 仍係 302 張。

## §5 resync（qa306/resync306.py）

index.html ＋10 行令 5 檔靜態測試由 PASS 變 FAIL（全係行號釘，唔係內容錯）。resync306 跟 resync305 同一套引擎：

- 插入點（舊行號）：FRAME ＋4 @舊 L37881 後（wrap 行之後；wrap 行本身加咗個逗號）；wrap 換句 ＋3 @舊 L40073 後；cap 換句 ＋3 @舊 L40247 後。
- 漂移：≤37881 唔郁、37882–40073 ＋4、40074–40247 ＋7、≥40248 ＋10；命中嘅釘行全部喺 ≥40248 段，一律 ＋10。
- 核實：--check-only 先行，4 個 rom176 釘＋54 個 travel114 釘逐行對 pristine（v305）內容逐字相同，純漂移；再落實：travel114 改 29 處（COUNT 4＋FREE 24＋DEF 1；WRAPPER 29103 唔郁）、STR_PINS 21 段（每段檔內唯一）、每檔頂加 v306 註解。
- 落實後 5 檔逐個重跑全部 ALL PASS；再跑全套 suite 見 §6。

## §6 Suite

- `bash qa131/run_suite.sh ~/workspace/linji-work306 ~/workspace/suite306.txt` → TOTAL PASS 369 FAIL 9（基線 368／9；+1 係 test_r306_chai_frame.js；9 項 pre-existing FAIL 不變）。
- 第一次跑 364／14 係 resync 未做（5 檔釘行漂移），唔係回歸；resync 後重跑 369／9。

## §7 部署

- main HEAD `7b6c6e0`（v306）
- Pages md5 `ff8d425a1edb2e2f1ba2897d13b50eea`／4,693,683 bytes（byte-identical）
- 工作副本 linji-work306 已刪。
