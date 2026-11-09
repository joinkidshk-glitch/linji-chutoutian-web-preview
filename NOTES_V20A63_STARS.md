# v20a63「頒獎禮群星版」NOTES

基底 v20a62（4,780,447 bytes）→ 本版 4,880,445 bytes（+99,998）。冇推 repo。
用戶兩項追加：①像素阿偉要跟返定版人物設計（改用真立繪像素化，唔再手繪 pixel map）；②頒獎禮要有其他提名作品＋紅星像素版出場做對手。外加追加③：頒獎禮利用已有作品圖（poster59 海報）。

## 一、像素角色：真立繪像素化管線

管線（/tmp/awd63/make_sprites.py，PIL）：
企立原圖（米白底）→ 邊緣 flood-fill 去底（種子限 bg 色距 ≤26、fill thresh 30；再以最大連通域清理底色口袋）→ 色彩 ×1.18／對比 ×1.06 增強 → 裁人物 bbox → LANCZOS 縮至高 72px → MEDIANCUT 量化 26 色（無抖動）→ alpha 二值化（≥110）→ PNG optimize。

- 阿偉來源：`p0/standing` stage3 企立——深藍西裝褸＋白恤衫開領、**冇呔**，同風格錨（style-anchor-awei-anime.jpg）同款造型同面相（黑髮豐盈碎瀏海、大啡眼、粗眉、溫和笑）。v62 手繪 sprite 條紅呔係錯版，已成套撤走（AWARDS62_PAL62／SPR_STAND／SPR_HOLD／awards62DrawSprite 全刪，static 鎖死唔准返嚟）。
- 阿偉捧杯幀：企姿幀胸前以 PIL 合成像素金杯（細版，杯闊 13px，加兩點膚色手指提示），金色跟 v62 既有色（#f2c14e／#ffe98f／#c8891d）。
- 紅星池（10 位）：即 POSTER59_STAR_IDS 有 id 兼有企立圖嘅全部紅星——陸柏言、廖炳星、齊鎮海、麥震東、駱家聲、鍾楚凝、蘇芷茵、魏詠男、顧明輝、葉敏芝。咁揀嘅原因：LEADSTAR59 派得出嘅主演必然喺呢 10 位之內，任何 fellow 都有像素樣出場，唔會出現「有名冇樣」。顧明輝用 v2 企立（中分頭＋憂鬱眼神，細尺寸辨識度高過 v1）。
- **程天諾唔喺池內、sprite 表亦冇佢**：佢唔喺 POSTER59_STAR_IDS（1988 零出場紅線），衍生層面結構性冇可能出場。
- 媒介池（兜底派位用）：film［陸/廖/麥/齊/駱/魏］、tv［齊/葉/陸/鍾］、music［駱/顧/廖］、ad［蘇/鍾/陸/魏/顧］。

體積帳（PNG 原始 bytes → base64 字元）：
| sprite | 尺寸 | PNG bytes |
|---|---|---|
| awei | 43×72 | 4,111 |
| awei_hold | 43×72 | 4,285 |
| luk_baakyin 陸柏言 | 49×72 | 4,237 |
| liu_bingxing 廖炳星 | 37×72 | 5,250 |
| chai_zanhoi 齊鎮海 | 62×72 | 5,294 |
| mak_zhendong 麥震東 | 50×72 | 4,869 |
| lok_gasing 駱家聲 | 53×72 | 6,253 |
| chung_choning 鍾楚凝 | 58×72 | 6,717 |
| so_jiyan 蘇芷茵 | 51×72 | 5,625 |
| ngai_wingnaam 魏詠男 | 48×72 | 5,303 |
| gu_mingfai 顧明輝(v2) | 34×72 | 3,964 |
| yip_manji 葉敏芝 | 66×72 | 6,670 |
| **合計** | | **62,578 B → base64 83,720 字元**（預算 ≤120KB，達標）|

A/B 對照圖（原圖 bust vs 像素 ×5 最近鄰，存 `awd63-compare/`）：
cmp-awei.png、cmp-luk_baakyin.png、cmp-liu_bingxing.png、cmp-chai_zanhoi.png、cmp-mak_zhendong.png、cmp-lok_gasing.png、cmp-chung_choning.png、cmp-so_jiyan.png、cmp-ngai_wingnaam.png、cmp-gu_mingfai.png（v1）、cmp-gu_mingfai_v2.png（定版）、cmp-yip_manji.png、cmp-group.png（群像一覽）。
自評：阿偉一眼認得（髮型輪廓／眉眼／深藍西裝白恤衫）；紅星之間靠髮型＋衫色分得開（廖炳星花恤、齊鎮海深色西裝、駱家聲黑皮褸、蘇芷茵長直黑髮、葉敏芝啡鬈髮）。

## 二、提名對手（fellows）衍生邏輯（awards63Fellows）

喺 buildAwardResultPack 計完每個類別後衍生，掛 `cat.fellows63`；類別 outcome=nominated 時 `cat.winner63 = fellows[0]`（最強對手奪獎，玩家入圍未贏嗰陣由佢捧杯）。
規則：
1. 候選＝全部 pack 通告（GIGS＋STORY_WIRE.gigsByYear 去重）中：年份符、type ∈ ceremony.matchTypes、**唔喺玩家 wrapHistory**（自己有份嘅作品唔做對手）、有片名。
2. 主演＝leadStar59Of（LEADSTAR59 對照表，唔用 favorDelta/rumor）；雙主演取第一位。主演冇 POSTER59_STAR_IDS（即冇像素 sprite，如彭兆基）嘅作品**成部剔除**，唔攞嚟做對手。
3. 第一輪：真主演對手按片酬（payExact／pay 上限）降序，每位星只取一部（取最高 pay 嗰部），最多 3 位。
4. 第二輪兜底（1989/1990 未回填主演嗰啲）：淨返冇主演嘅候選作品，按媒介紅星池以 gig id 雜湊確定性輪派（同一年同媒介結果穩定、唔重複派同一位星），標記 `assigned:true`。
5. 真人紅線：唔作真人；池內全屬遊戲虛構紅星；程天諾結構性缺席。

呈現接線：
- 請柬（renderAwardInviteHtml → awards63InviteBitHtml）：「憑《X》爭獎」行＋focus 類別「同屆提名：星《作品》…」細字。
- 結果卡（awards63FellowsHtml）：每類別卡加「同屆提名」行；入圍未贏嗰類標 🏆 喺得主身上＋「（🏆 為得主）」。
- awardsLog（commitAwardToLog）：類別**只加** `fellows63:[{star,title}]` 同 `winner63:"星名"` 兩欄，舊欄位語義不變；獎項頁（renderAwardsPane62）順手顯示同屆提名＋🏆 得主（舊 log 冇呢兩欄就唔出，唔崩）。

## 三、像素動畫改版（沿用 v62 canvas 引擎：424×240、125ms tick ≈8fps、pixelated、可跳過、降級保留）

台位：對手一排（≤3）＋玩家插第二位；旁聽嗰晚玩家唔上台。圖未載好／失敗 → 深色剪影頂住（唔穿崩）。

beats（awards62CeremonyBeats 改版）：
| beat | ms | 畫面 |
|---|---|---|
| open | 1200 | 舞台亮起，對手群像漸入 |
| enter | 1100 | 玩家由右行入台位 |
| names | 2400 | 全員企位；字幕逐個唱名（阿偉＋各對手 星：《作品》）；**作品卡列逐張浮現**（見第四節） |
| suspense | 1400 | 全場壓暗，聚光逐位掃過提名者（其餘變暗 0.45） |
| reveal | 2100 | 得獎：光池打阿偉＋捧杯幀＋金紙屑＋對手變暗；入圍：**光池打得主對手＋佢胸前金杯 glyph＋微跳**，阿偉原地，caption 唱出「🏆 X憑《Y》得獎／你嘅《Z》入圍到最後——差少少，下年再嚟」 |
| glamour | 1800 | 只限得獎＋得獎作品有海報（見第四節） |
| out | 500 | 淡出 |

旁聽（gallery）：open → pan（2000，鏡頭輕移掃過台上群星）→ out，全長 3.7s。
全長：得獎冇海報 8.7s（同 v62 一致）、得獎有海報 10.5s、入圍 8.7s。

## 四、海報利用（poster59，全經 poster59Path 重用既有 data URI，冇重複編碼；POSTER59_DATA 全檔仍只一份）

有圖嘅位：
1. **唱名作品卡列**（DOM 層 `.awd63-cards`，喺 canvas 下方、字幕之上，唔入侵像素舞台）：names beat 逐張浮現（每 380ms 一張）。有海報（POSTER59_IDS 十部：夜海鎗火、詭校夜話、雲海劍訣、神探闖天關、飛天劍影決雌雄、樂壇新星選拔夜、春季美顏護膚輯、秋日回音試音大碟、賀歲喜劇笑滿堂、秋日鍾楚凝嗰部）→ 海報縮圖＋片名＋星名；冇海報 → 同作品牆語言嘅 CSS 片名卡（深紫金字《片名》＋星名）。玩家張卡金框＋紅色「你」圓章，同對手分得開。
2. **得獎 glamour**：bestOutcome=won 且代表作 gigId 有海報 → reveal 後加 glamour beat：全屏（stage 層）海報＋金框光暈＋「🏆 得獎／獎項：《作品》」金字，1.8s 或撳畫面過；跳過掣 z-index 喺 glamour 之上，隨時走得。冇海報就唔加呢 beat，流程冇空位。
3. **請柬細海報**：repWork 有海報嗰陣，「憑《X》爭獎」行左邊加 84px 海報（跟 v59 通告詳情 `.cn-poster59` 尺寸語言：84px、白邊、微傾 1.6deg）。
冇圖處理：1989/1990 全部作品同 1988 大部分作品都冇獨畫——卡列自動用 CSS 片名卡、請柬唔出圖位、得獎唔出 glamour，成套「有圖加分、冇圖唔穿崩」。冇為任何對手新作海報。

## 五、驗證

- 新 tests：test_awards63_logic.js（25 斷言：衍生排序/去重/自作品排除/年份隔離/池兜底確定性/程天諾紅線/beats 得主唱名/glamour 條件/focus）＋ test_awards63_static.py（35 斷言：舊 map 全撤/sprite 齊 12 張＋≤120KB/接線/海報單份/硬規則）。對 v20a62 index 行 → 雙雙 FAIL（反證成立）。
- v62 static 有一條斷言因本版撤換手繪 sprite 而更新（「阿偉精靈圖」改查 AWARDS63_SPRITES 在位＋舊 map 已撤），其餘 v62 斷言不變。
- 全套 tests：**60/60 PASS**（基線 58＋新 2）。主 script node --check OK。
- 真瀏覽器自驗（本地 server＋Playwright headless，入口 window.__awards.play62）三場全過、零 pageerror、stage 乾淨移除：
  - 得獎＋海報（《夜海鎗火》）：shot-A-names.png（群星企位＋四張海報卡＋玩家金框「你」章）、shot-A-reveal.png（阿偉捧杯＋光池＋紙屑）、shot-A-glamour.png（全屏海報＋金字，跳過掣在上層）。
  - 入圍（陸柏言奪獎）：shot-B-suspense.png（壓暗掃光）、shot-B-reveal.png（陸柏言胸前金杯＋得主 caption＋玩家差少少句）、shot-B-out.png；中途撳跳過掣亦驗過（即時完成）。
  - 旁聽：shot-C-pan.png（蘇芷茵＋鍾楚凝台上、觀禮 caption）。
  - fellows 對真數據直呼驗證：頁面內 __awards.fellows63（film,1988）→ 陸柏言《歲歲平安》、廖炳星《幽靈夜巡隊》、駱家聲《幻彩舞影》（真 pack 通告＋真主演、片酬序）。
  - 已知限制：本地工作副本係 repo 快照，冇 content pack，awards schema 喺瀏覽器 boot 唔齊，buildAwardResultPack 全路徑（build→請柬→出席→結果）未能喺本地端到端跑；該路徑由 unit（衍生邏輯）＋static（接線）＋動畫三場自驗覆蓋，實玩環境（softPreview）行到。

## 六、硬規則確認
冇改 SAVE key／softRev／?v=／pack JSON；冇郁 v60 CALIB60、v61 後果包、v62 A 部分評分公式（WIN_LINE 0.82／awards62ScoreParts 原封）；awardsLog 只加欄位；newspaper/press 串連冇郁。

---
部署記錄：PR #162 合併後首次 Pages 部署（run 42705619849）deploy 步驟失敗（本 repo 部署超時嘅已知間歇問題），以本 commit 重觸發部署。
