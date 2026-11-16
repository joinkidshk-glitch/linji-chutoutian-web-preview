# NOTES_V20A252_gig-library-landing.md — v20a252 通告庫全量重生成落地

**日期**：2026-11-16｜**基線**：live main `a39ad34`（v251，suite 314／11）｜**結果**：suite **315／10**（只剩 10 項已知 pre-existing FAIL）
**庫**：`content/gigs_new.json` 換做 regen-v2 最終版＋補 2 張故事 gig，**269 張**（作品 153／臨記通告 110／補拍 6；1990:105／1991:94／1992:70；頂層版本 `gigs_new v2`）

## 改咗咩

### 1. 換庫（content/gigs_new.json）
- 由 `~/workspace/linji-gig-redesign/regen-v2/gigs_new_v2.json` 換入，md5 一致。
- 36 張作品通告由臨記升初級（互斥規則）、22 個新名、ad_102 productGender F→N（1992 年 F≥2 已批例外）、15 張臨記通告升初級——全部喺 regen-v2 完成，呢票只係換入。
- `gig_1990_film_203`《水塘夜戲》浸水屍體維持臨記（N4 故事通告，唔郁）。

### 2. 補 2 張故事 gig（GRANT229 重對發現新庫漏咗，唔補唔可以出貨）
- `gig_1990_film_113`《龍鳳茶樓》男配角（電影／初級／作品／1990夏／12日／長期合約，cast 廖炳星／胡美琳／韓秀婷＋玩家男配角格，fame [18,31]、pay [7200,8400]）。
- `gig_1991_variety_109`《咪高峰夜》卡拉OK擂台暖場（綜藝／初級／作品／1991秋／2日，host 彭少祺、嘉賓顧明輝／沈映雪／藍若曦，fame [20,35]、pay [1100,1300]）。
- 兩邊庫（regen-v2 源檔＋工作副本）同步，md5 一致；其餘 267 張零改動。

### 3. GRANT229 重對（34 鍵：32 成功＋2 補 gig）
- 31 個舊 id 喺新庫根本唔存在，3 個存在但內容已換——全部重對，唔可以照抄。
- 新庫 grant gig 集中喺 2xx 系列（storyKeys 標節點）。N4_b 正確對到 `film_203`《水塘夜戲》（臨記）；N6_a→`tv_107`《一家親》（長期合約）；N6F_a→新 `film_113`；N8_a→新 `variety_109`。
- `CONTRACT229_GIGS` 更新做 `{ tv_107, film_113 }`（舊 `film_110` 已變《鐵血幹探》，剔走）。
- 幾處角色／標題漂移已接受（storyKeys＋媒介／級別／類別／季節全部啱，而且係全庫唯一候選）：N7_b 照相館客人→《老相館》沖曬學徒、N11_a 講數二佬→《龍虎夜廟街》跟班、N12_b 武館師弟→《小武館》學徒、N19_a 清潔工→《街燈昏黃時》青年、N19_b 讀信工人→《一頁家書》代筆青年。

### 4. 頒獎引擎（D-v2-1／D-v2-2／D-v2-3）
- `awards63Fellows` 重寫讀 `cast`（電影／電視／廣告讀四角、唱片讀 `singer`、新人獎混合、最佳司儀讀 `host`）；`AWARDS63_POOL`／`AWARDS63_TIER_WEIGHT`／`awards63WeightedPick` 成個刪除；第二輪池抽＋高俊傑特別名額刪除（grep 零殘留）。
- 加最佳司儀一格（`cat_tv_host`，星河台慶，fellows 讀綜藝作品 `host` 欄，中性唔分性別）；電視演技四格 `matchTypes` 由 `["電視劇","綜藝"]` 改做 `["電視劇"]`；順帶接 `awards188WorkRole`／`awards188CatEligible` host 分支。
- `AWARDS204_FEMALE_STARS` 加胡美琳／韓秀婷，女星 7→9。
- `awards188IsSupport` 改讀 cast（新 `awards188PlayerCastSlot` 交叉核對，兩邊唔夾就唔認）；`awards188IsLead` 刻意冇郁（委派去結局梯判準，庫入面 roleLabel 同 cast 一致，唔會打架）——不對稱留返 parent 決定。
- 驗證：16 格 × 3 年真庫實跑 459 項 PASS、0 FAIL（每格啱啱 3 個對手、星唔重複、全部有 sprite、男女純正、逐格對返真）。途中捉到真 bug 修咗：`singerGender` 係大寫 M／F，第一版小寫比較令歌手格出 0 個。

### 5. 詳情頁＋作品牆（D-v2-6／D-v2-3）
- 詳情頁按 SPEC §6.2 分流：電影／電視四角陣容＋導演＋簡介、廣告代言人＋產品（名＋類別＋品牌）＋適合性別、唱片主唱＋歌種＋形式、綜藝主持＋嘉賓＋環節、臨記通告唔顯示陣容（簡介用 blurb）、補拍只加「原製作」一行。玩家格一律標「應徵中」。板卡維持 §6.1（唔出主演行、唔出成品海報），零改動。
- 作品牆主演行改陣容行；舊檔 `wrapHistory` 字串保留，無 cast 跌返舊制。附帶修好 3 張綜藝作品 director 誤出導演行。
- 新測試 `tests/test_cast252_logic.js`（68 PASS）。

### 6. 殺青好感四角分格（D-v2-4）
- `enc79OnWrap` 改讀 `gig.cast`：好評主角格 +3／配角格 +1，劣評主角格 +1／配角格 0，玩家格唔計，null 格跳過；`workedWith` 保留；舊庫 gig 跌返舊制。

### 7. Poster 三格幀＋POSTER59 接線
- 彭少祺／胡美琳／韓秀婷各 south／east／west 三格（128×128 RGBA PNG），入 `assets/story/awards/px_<id>_<dir>.png`，共 9 張。Pixellab `export-spritesheet` 免費出口，餘額不變。
- `POSTER59_STAR_IDS`：彭少祺 null→`pang_siuki`，加 `wu_meilam`、`hon_sauting`。
- 新幀同舊幀有 1–2px 位置偏差（同一 sprite，像素數一致，無實質影響）。兩處舊註釋／補位行（L15394「名冊以外兩位」、leadStar59Of 內 `byId.pang_siuki`）而家冗餘但無害，未清。

### 8. 庫數據校準（suite 捉到，16 張 days／pay）
- 16 張 `days` 跌出 `roleScale` 帶（大碟 2–3 日、電影男主角 12 日、MTV 4／10 日等），全部改 days（大碟一律 9 日、電影男主角 22 日、MTV 3 日、電視長劇男主角 30 日、武師替身 3 日），pay 跟日數郁、日薪留喺帶內，hi／lo ≤1.25；寫明日數嘅簡介句子同步改咗。
- 另 5 張日薪出帶（dur90 B2）一併修好。六批＋full check 重跑全部 exit 0。

### 9. 測試更新
- `tests/test_fix88_logic.js` 已刪（D1 作廢）；`test_fix88_static.py` 留返（FIX88 機制本身仲喺度，只改 B3 一個數）。
- poster59／awards63／204／178／188 測試按 cast 模型重寫；gig229 家族／dur90／awei195／nat92／pacing35／weave47 按新庫真實數字更新；6 檔行數釘 resync（純漂移，逐行核實）。
- 分年期望更新：105／94／70（舊庫實際係 104／94／69，唔係早前講嘅 93／70）；版本字串統一做 `gigs_new v2`。

## 驗收

- **全套 suite：TOTAL PASS 315 FAIL 10**（獨立重跑兩次，FAIL 名單逐字相同）。10 項全部係已知 pre-existing FAIL：flash51／rumor49／slot50／soft_tip_111_restore／start53／weave43／weave44／weave49／wf5_87／wrap38。總數 325 不變（＋1 test_cast252、−1 fix88 logic）。
- 六批 regen 驗證＋full_verify_checks.py 全部 exit 0、硬 FAIL 0（film 41／tv 41／music 30／ad-variety 41／E1 57／E2 53）。
- `node --check`：改過嘅 .js 全部 PASS；index.html 兩個 inline script 塊抽出檢查 PASS。

## 已知缺口（測試已釘死，唔係呢票範圍，留返跟進）

1. **BR89_PATRON_OF_GIG 13 對同新庫 credit trigger 0 張對得上**（3 錯配會令持真債開唔到＋9 張目標已無 credit trigger＋1 張消失）。另 R-4 還錢結算路只接舊 id（新庫顧引薦 gig `rec_105` 唔開）、殺青鉤唔標新庫廖引薦 gig（`film_103`/1991）。建議跟 v253 人情兌現全盤一齊做。
2. **GRANT229_ENC79／DRAFT 11 張死 id**（9＋2，映射仲指住佢哋，無接班者）。另開票重對。
3. **劣評分支喺新庫下實際死咗**：新庫 fame 最低 [5,10]，`sh.fame ≤ 1` 永不成立，每張殺青都係好評。想劣評真係發生到，要另加真正嘅評價信號。
4. **5 位名冊外女星（藍若曦／江詩盈／沈映雪／胡美琳／韓秀婷）殺青唔加 enc79 好感**（201 個格次）——同舊制行為一致。
5. **唱片 9 張語義含糊**：玩家做大碟主唱，但 `singer` 照填監製星。詳情頁跟 SPEC 照出星名；如果 `singer` 應該係 null（玩家格），要數據嗰邊改庫。
6. **殺青海報 caption（`wrapPoster59Html`）未改**：而家因 poster59Path 回空而唔顯示；D-12 出圖嗰陣要同款改陣容行。
7. **1990 冬季板面薄**：可見 27 張，臨記 4 張（全部零要求），開局報得 9 張；全年 1990 開局報得 55 張。16→4 屬實，但「開局冇嘢接」唔屬實。冬季得 9 張係薄啲，補唔補要拍板先至做。
8. 結果卡／典禮 beats 入面搵高俊傑同場嗰兩段顯示層而家永遠唔觸發（D-v2-2 已刪名額），刪唔刪係產品決定，未郁。

## 清理
- 工作副本落地後刪除；`~/workspace/linji-work-gig-rewrite`（已否決嘅重寫票）一併刪除。
