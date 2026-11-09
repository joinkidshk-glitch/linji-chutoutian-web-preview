# NOTES v20a59 — 作品圖＋主演接入（POSTER59）

基線：v20a58（linji-work58f，index 4,318,371 bytes）→ 本版 index **4,686,517 bytes**（LEADSTAR59 對照表 +17,576；海報 data URI 內嵌 +350,570）。海報交付形態已改內嵌（見 §3 修訂），唔再行外部檔。冇推 repo。

**二次縮碼（2026-11-10）**：首版內嵌（380w／q66）成個推送包（index＋NOTES＋測試＋fixture）約 **5.17MB 實測撞 HTTP 413**；已知成功推送總量為 4.45MB。海報遂由 PNG master 再縮至 **闊 340／WebP q60**：binary 330,126 → **262,460 bytes**、base64 payload 440,180 → **349,956 字元**、index 4,776,741 → **4,686,517 bytes**。340 版重新砌總覽圖對照原 contact sheet：十張構圖／人物一致、圖內無字、面容認得出（顯示最闊只係作品牆卡 ~170 CSS px，340w 啱用）。

## 1. leadStar 欄位（數據層）

- 新增區塊 `/* ===== v20a59 POSTER59 =====`，喺 `normalizeGigRecord`（全入池唯一咽喉）加一層 hook：`leadStar59Apply(o)`，跟 TEXTFIX55／BRIDGE56 既有模式（try＋typeof 守衞、冪等、只認 gig id）。**冇改任何 pack JSON。**
- `LEADSTAR59`：gig id → 主演顯示名，來源＝`linji-poster-casting-1988.md` 選角表 v1「建議主演」欄，**1988 年 137 部常規製作全數回填**（已核實：137 個 key 恰好＝1988 包 143 張減入門 6 張；入門／MID／softBridge 全部唔入表）。
- 值格式：單主演＝人名；雙主演／主持＋嘉賓（5 部）以「、」連接：`gig_1988_var_02`、`gig_1988_var_04`（彭兆基、葉敏芝）、`gig_1988_tvb_longmen_summer_high`（彭兆基、齊鎮海）、`gig_1988_fill_harbour_autumn`（彭兆基、顧明輝）、`gig_1988_var_05`（彭兆基、陸柏言）。
- 唯一 null：`gig_1988_ad_adm_autumn_low`《秋裝街頭隨拍輯》——選角表定為素人無星（文案自證），作品照入作品牆，只係冇主演欄。
- `POSTER59_STAR_IDS`：主演名 → 既有 era-star stub id（luk_baakyin／liu_bingxing／chai_zanhoi／mak_zhendong／ngai_wingnaam／chung_choning／so_jiyan／lok_gasing／gu_mingfai／yip_manji），normalize 時順手寫 `o.leadStarId`（取第一主演）。
  - ⚠️ 發現：**彭兆基冇 stub id**。stub 名冊入面近似嘅係 `pang_siuki`＝**彭少祺**，查實係另一個角色（廣告樓大堂／賭錢傳聞嗰位），唔係金牌司儀彭兆基，冇冒認——`POSTER59_STAR_IDS["彭兆基"]=null`，佢主演嘅通告只出名、冇 id。要唔要幫彭兆基補返個正式 star id，留畀主代理／內容側定。
- favorDelta／rumorKeys 維持原義（人情／傳聞），冇攞嚟做主演（選角表 F2 紅旗）。

## 2. 顯示位

| 位 | 行為 |
|---|---|
| 通告紙卡 `gigCardHtml` | 有 leadStar 先出「主演：XXX」一行（`.lead-star`，海軍藍粗體，跟卡面語言）；冇就成行唔出，唔出空欄。卡面唔放圖：137 部得 10 部有獨畫，卡面圖文唔齊會更怪，圖留畀詳情／殺青／作品牆。 |
| 通告詳情 `castingNoticeDetailHtml` | 摘要區加「主演」列（跟片酬／日數同款 `.cn-sum-row`）；有獨畫嗰 10 部，摘要右上加一張細海報（84px、紙邊＋輕斜＋陰影，`.cn-poster59`，載入失敗自動隱藏）。 |
| 殺青結算 | wrap 時若該作有海報，結算 notes 尾加一格細圖＋片名＋主演＋「作品已收入手帳作品牆」（`wrapPoster59Html`，冇圖回空字串，唔阻流程）。 |
| 手帳「作品」頁 | 見 §4。 |

## 3. 海報資產（交付形態修訂：data URI 內嵌）

**修訂原因**：推送實測——GitHub connector 嘅 push-files 只收 UTF-8 文字檔，binary .webp 畀佢以 `is not UTF-8` 拒絕；外部圖檔根本入唔到 repo，唯一路線係 data URI 內嵌（同以往所有內嵌圖同例）。初版嘅相對路徑交付形態作廢。

**現行形態**：`POSTER59_DATA` 對照表（gig id → `data:image/webp;base64,...`）注入 index，`poster59Path()` 先過 `POSTER59_IDS` 白名單再查表回 data URI（其餘回空，唔會 404）。來源仍係 `linji-native-design/posters/` 試點成品 PNG（由 PNG master 直接編碼，唔經 600w 版二次壓縮）。

**編碼規格（三段式）**：先試闊 440／q70——binary 428,692、base64 約 571,590，index 會去到 4,907,537，超咗 ≤約 4.90MB 目標，唔搏；降 **闊 380／WebP q66**：binary 330,126、base64 440,180、index 4,776,741——但成個推送包約 5.17MB **實測撞 413**（已知成功推送總量 4.45MB）；再降 **闊 340／WebP q60（現行定版）**：binary **262,460 bytes**、base64 payload **349,956 字元**、index 增量 +350,570 → **4,686,517 bytes**。顯示最闊場景係作品牆卡 ~170 CSS px，340w 啱用；340 版砌總覽圖同原 contact sheet 對照，十張齊、構圖人物一致、圖內無字、面容認得出。

| gig id | 作品 | 主演 | 內嵌尺寸 | binary bytes |
|---|---|---|---|---|
| gig_1988_film_harbour_high | 《夜海鎗火》 | 陸柏言 | 340×355 | 18,492 |
| gig_1988_film_cotton_spring_high | 《詭校夜話》 | 廖炳星 | 340×680 | 37,342 |
| gig_1988_film_lion_summer_high | 《雲海劍訣》 | 齊鎮海 | 340×355 | 17,610 |
| gig_1988_film_03 | 《神探闖天關》 | 麥震東 | 340×355 | 30,672 |
| gig_1988_tv_03 | 《飛天劍影決雌雄》 | 齊鎮海 | 340×355 | 26,904 |
| gig_1988_film_cotton_autumn_low | 《茗香秋韻》 | 鍾楚凝 | 340×680 | 32,298 |
| gig_1988_var_04 | 《樂壇新星選拔夜》 | 彭兆基、葉敏芝 | 340×680 | 44,568 |
| gig_1988_ad_central_spring_high | 《春季美顏護膚輯》 | 蘇芷茵 | 340×355 | 8,452 |
| gig_1988_rec_03 | 《秋日回音試音大碟》 | 駱家聲 | 340×680 | 20,056 |
| gig_1988_tv_06 | 《賀歲喜劇笑滿堂》 | 陸柏言 | 340×680 | 26,066 |

**Master 保留**：闊 600／q72 版本（676,812 bytes）保留喺工作副本 `assets/posters/poster-1988-<workid>.webp`，程式已唔再引用，留畀原生版／將來高清交付用；檔名規則 `poster-<年份>-<gig id 去 gig_<年份>_ 前綴>.webp` 不變。

## 4. 作品牆（手帳新頁「作品」）

- 手帳加第 7 頁：tab「作品」（`data-htab="works"`）＋ pane `#home-pane-works`／`#works-list`；`setHomeTab` allow＋渲染分支＋`syncHomeTabExit` 已接（跟其餘手帳頁同一套 chrome）。
- 數據：`S.wrapHistory` 做底，`worksWallEntries59()` 逐條過濾＋回查：
  - **入牆條件**（有名製作）：gig id ∈ LEADSTAR59，或可喺 `STORY_WIRE.gigsByYear`／現行 GIGS 回查到記錄而且唔係 entryTier／softBridge。入門工、常駐散工、MID 散工唔入牆。
  - **欄位回查**（舊存檔相容）：workTitle／roleLabel／年份優先用存檔快照（見下），冇就回查包記錄，再冇就由 entry.title 解析《》同尾段；主演／海報永遠用 gig id 查 LEADSTAR59／POSTER59_IDS，即舊存檔唔使升級都顯示得齊。
  - **新存檔快照**：wrap 入 `wrapHistory` 嗰陣順手多記 `workTitle`／`roleLabel`／`year` 三欄（純附加，舊讀檔路徑唔受影響），保證跨年之後（年包換走）崗位／年份都仲查得返。
  - 呈現：兩列海報牆（紙卡＋輕斜，跟剪報頁語言）；有獨畫出圖（3:4 裁切、圖載入失敗自動退返 CSS 卡）；冇獨畫出純 CSS 片名卡（按類型五種墨色漸變＋金邊框＋置中片名，**冇用 emoji**）；卡下顯示作品名、主演（有先出）、年份 · 阿偉崗位。
  - 已知上限：`wrapHistory` 本身只留最近 20 條（既有設計，冇改），所以作品牆最多展示最近 20 部已殺青作品；要做「全履歷」要另開持久清單，唔喺今版範圍。
- 空牆有引導文案（解釋幅牆點嚟、臨記期海報得明星樣嗰個設計位）。

## 5. 1989／1990 待辦（機制已預留）

- `LEADSTAR59` 只填 1988。1989／1990 選角表未出：嗰兩年嘅包記錄會照入作品牆（靠 gigsByYear 回查判定有名製作），主演欄留空、海報出 CSS 卡；等選角表＋海報批次出咗，喺 `LEADSTAR59`／`POSTER59_IDS` 追加入去就即刻生效，唔使改邏輯。
- 後續海報批次：A 級 59 部獨畫（選角表 §3 次序）、B 級 68 部分類圖——分類圖接入嗰陣，`poster59Path` 要加一層「類型＋年代」fallback，今版未做（避免同獨畫白名單打架）。
- 結局總結頁用作品牆做 filmography 呈現（設計檔出現位 4）未做，留畀結局批次。

## 6. 驗證

- 新增 `tests/test_poster59_logic.js`（137 表完整／回填全對／名冊核實／冪等／散工入門零主演／卡面主演行／海報 data URI 10 條齊＋解碼 WebP RIFF／作品牆舊格式回查＋過濾＋快照優先／殺青 helper）＋ `tests/test_poster59_static.py`（接線／CSS／POSTER59_DATA 10 條＋解碼 WebP magic＋同白名單一致／程式零相對路徑引用／600w master 保留核實）。交付形態修訂後已同步更新兩套斷言。
- 新增 fixture：`tests/fixtures/gigs_1988.json`（3.2.10-soft，同選角表資料源同版；之前 fixtures 冇 1988 包）。
- **全套 tests 52/52 PASS**（基線 50＋新 2）；兩套新測對 v20a58 index 均 FAIL（反證成立）；兩個 script block `node --check` PASS。二次縮碼（340/q60）後已重跑全套：52/52 PASS、`node --check` PASS；測試冇斷言寫死舊海報體積／尺寸，唔使改測試。index diff 核實只郁 POSTER59_DATA 十行＋區塊頭注釋規格字樣（380w q66 → 340w q60）。
- 硬規則：冇改 pack JSON、冇改 SAVE key／softRev／?v=／數值／經濟。
