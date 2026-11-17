# NOTES_V20A159 — 感情線大改＋約會層實裝（統籌筆記）

- 分支：`v159`，工作副本 `~/workspace/linji-work159b`（clone 式，origin 係常駐 clone 本地路徑），base main `846e952`（v154）。舊工作副本 `~/workspace/linji-work159`（worktree，origin github.com，直推風險）冇郁過，落地後等 parent 決定清唔清。
- 設計來源：`~/workspace/linji-story-sidelines/romance-revamp-draft.md`（§9.3 新次序 P1 曉晴／采兒／藍、P2 徐／葉、P3 蘇）、`~/workspace/linji-costume-home/DESIGN.md`、`~/workspace/linji-economy-redesign/DESIGN.md` §4.8。
- 範圍：感情線重排（Vera／海媚出局，葉／蘇入局；排他鎖；喜好分層＋分流；R_yip_*／R_so_* 新寫；藍 crisis 重寫；蘇層級閘）＋約會層（37 場、Q7 價錢、地圖兩層、6 新地點＋6 張場景圖）。
- **唔入呢版（分拆後續）**：服裝＋屋企（P1 四件衫 #1／#4／#10／#8 未逐件確認＋32 張圖成本大，等用戶確認後另開票）、撞到對白變體（草稿 §2.2，另開票）、采兒 HE 代價後續節點、徐寶珊「唔賣得」禮物（未拍板）、Vera／海媚／鄧麗萍死檔刪除（另一票；呢版只拆感情線 offer 路徑）。

## 1. Cherry-pick 舊 Phase 1（commit 6cc403c）

- 舊 commit `cd3ca66`（2026-11-13，base e08a070，Phase 1：曉晴／采兒／Vera）cherry-pick 上現行 main，4 檔衝突、10＋4 段，全部解決（見 §2）。新檔（NOTES_V20A159_P1.md、qa159/、test_rom159_*）乾淨入。
- 驗證：主 script `node --check` SYNTAX_OK；`test_rom159_logic.js` 69/69 PASS（機制本身喺現行 main 照行）；`test_rom159_static.py` 撞 `content/story_detail_c1_to_c17.json` 唔存在（現行 main 已改名 `story_detail_n1_to_n17.json`，A 工人修）。
- 主線 JSON 已核實：Vera／海媚／mei 零命中（"vera" 1 命中係 "coverage" 包含嘅子串），N6／N16 唔使郁——草稿 §8.17 的 C6／C13 重寫問題喺 live 已唔存在。

## 2. 衝突解決紀錄

- GiftShop 三段（prefKind／reactionLine／calcDelta）：一律取 HEAD（v20a183 B2）。原因：v183 已實裝最愛分層，最愛同喜歡同數 +2，同草稿 §5.3（「最愛／喜歡同數 ＋2」）一致；舊 Phase 1 的喜歡 +1 已過時。舊 reactionLine 有亂碼字串（顯示問題，檔內實為「你記性真好」）。
- Pack 載入（L14812）：取 HEAD（Tang＋rom176 覆寫）＋插入 rom159ApplyGiftOverrides 呼叫。rom159（romance npcs）同 rom176（星＋mei）寫唔同 key，唔重疊，次序唔影響。
- commit48Available：舊鎖檢查塊＋HEAD 的 1992 秋 return；修舊註解錯字「1990 秋」→「1992 秋」、「三人」→「六人」。
- addLocTalkGiftActs：取 HEAD（v20a176：女角唔喺地點板傾談／送禮＋v20a236 reconfirm）。舊地點面板約會掣唔要——v176 之下女角唔喺地點板，約會三入口改行撞到／傾談／手帳 Call 機（舊 code 嗰三處已合併入嚟，L25758／L39515／L25960）。
- openLoc：HEAD toast（書面語）＋舊 rom159FlushNotices 呼叫。
- doTalk：HEAD toast（書面語）＋舊 rom159TalkCapped 檢查。
- openGiftPick：取 HEAD（"★ 最愛"，v20a183）。
- people72Html：HEAD return＋舊 rom159PeopleHtml 附加。
- test_text125／test_travel114：取 HEAD（舊錨點行號已過時）；最終 resync 喺整合嗰陣按實量重做。
- test_weave46：合併 HEAD（三個申報＋lan_block／lan_block183／tfix_block）＋舊 rom159_block 申報＋條件。
- 教訓：cherry-pick 後 `git add` 衝突檔會靜默 stage 咗有 marker 的版本——第一次 commit 9171054 錯收入有 marker 的 test_travel114，已 `git reset HEAD~1` 還原、重做 travel114 解決、再 commit 6cc403c。commit 前一定要 `grep -rn "^<<<<<<<" ` 核實零 marker。

## 3. 定值表（四個工人共用，唔好各自改）

### 3.1 ROM159_WOMEN（六行）
- hiu: rel_hiu, 林曉晴, npcId "colleague", phase 1, meet R_hiu_meet, spots [hiu_roof, hiu_location, hiu_market, hiu_harbour, hiu_beach, hiu_airport, hiu_cafe]
- choi: rel_choi, 周采兒, npcId "reporter", phase 1, meet R_choi_meet, spots [choi_premiere, choi_radio, choi_cafe, choi_lounge, choi_cinema]
- lan: rel_lan, 藍若曦, npcId "lan", phase 1, meet R_lan_meet, spots [lan_studio, lan_ktv, lan_rec, lan_lounge, lan_beach, lan_cafe]
- xu: rel_xu, 徐寶珊, npcId "xu", phase 1, meet R_xu_meet, spots [xu_central, xu_adm, xu_premiere, xu_star, xu_peak, xu_cinema, xu_cafe]
- yip: rel_yip, 葉敏芝, npcId null, phase 2, meet R_yip_meet, spots [yip_rec, yip_ktv, yip_peak, yip_cinema, yip_lounge, yip_cafe]
- so: rel_so, 蘇芷茵, npcId null, phase 3, meet R_so_meet, spots [so_rec, so_central, so_harbour, so_airport, so_beach, so_cafe]

### 3.2 ROM159_DATES（37 場）
- hiu（7）：hiu_roof 天台 tvb_longmen $4；hiu_location 外景 film_lion $4；hiu_market 廟街 gift_shop $20；hiu_harbour 海傍 date_harbour $6；hiu_beach 淺水灣 date_beach $6；hiu_airport 啟德 date_airport $6；hiu_cafe 茶記 cafe_cha $45
- choi（5）：choi_premiere 首映 film_cotton $58；choi_radio 電台 tvb_harbour $4；choi_cafe 茶記 cafe_cha $45；choi_lounge 酒廊 date_lounge $50；choi_cinema 戲院 date_cinema $58
- lan（6）：lan_studio 星河廠景 tvb_longmen $4；lan_ktv 九龍電視台 tvb_kowloon $4；lan_rec 錄音室 rec_hk $4；lan_lounge 酒廊 date_lounge $50；lan_beach 淺水灣 date_beach $6；lan_cafe 茶記 cafe_cha $45
- xu（7）：xu_central 中環廣告 ad_central $4；xu_adm 金鐘創意 ad_adm $4；xu_premiere 紅棉首映 film_cotton $58；xu_star 天星商場活動 rec_star $6；xu_peak 山頂 date_peak $6；xu_cinema 戲院 date_cinema $58；xu_cafe 茶記 cafe_cha $45
- yip（6）：yip_rec 香江唱片 rec_hk $4；yip_ktv 九龍電視台 tvb_kowloon $4；yip_peak 山頂 date_peak $6；yip_cinema 戲院 date_cinema $58；yip_lounge 酒廊 date_lounge $50；yip_cafe 茶記 cafe_cha $45
- so（6）：so_rec 灣仔唱片 rec_wanchai $4；so_central 中環廣告 ad_central $4；so_harbour 海傍 date_harbour $6；so_airport 啟德 date_airport $6；so_beach 淺水灣 date_beach $6；so_cafe 茶記 cafe_cha $45
- 價錢帶（Q7）：散步 $0–6、廟街 $10–30、茶記 $40–50、戲院／首映 $40–76、酒廊 $40–60（**酒廊 $50 係推算，§4.8 表無此項，待確認**）。

### 3.3 喜好分層（rom159ApplyGiftOverrides）
- hiu: 最愛 [菠蘿油，蛋撻]、喜歡 [保溫瓶，甜品盒，卡帶，髮夾]、唔鍾意 []
- choi: 最愛 [咖啡豆，拍紙簿]、喜歡 [卡帶]、唔鍾意 [香水，雜誌]
- lan: 最愛 [甜品盒，卡帶]、喜歡 [菠蘿油，蛋撻，保溫瓶]、唔鍾意 [香水]
- xu: 最愛 [保溫瓶，卡帶]、喜歡 [咖啡豆，拍紙簿]、唔鍾意 [菠蘿油，甜品盒，蛋撻]
- yip: 最愛 [卡帶，咖啡豆]、喜歡 [髮夾，保溫瓶]、唔鍾意 [香水，雜誌]
- so: 最愛 [卡帶，拍紙簿]、喜歡 [甜品盒，保溫瓶，咖啡豆]、唔鍾意 [香水，雜誌]
- 星層 prefs（rom176，已有，唔郁）：葉最愛香水＋雜誌、蘇最愛香水＋髮夾——同感情層倒轉係刻意設計，分流靠入口。

### 3.4 新地點＋場景圖
- LOCS id：date_harbour／date_peak／date_lounge／date_cinema／date_beach／date_airport
- 圖檔：assets/story/locs/bg_159_harbour.jpg／bg_159_peak.jpg／bg_159_lounge.jpg／bg_159_cinema.jpg／bg_159_beach.jpg／bg_159_airport.jpg（C 工人 staging：~/workspace/linji-159-images/）

## 4. 工人分工

- A（v159-romance，clone linji-work159a）：R_yip_*／R_so_* 新 JSON＋loader、藍 crisis 重寫、鏈 D 改編、WOMEN 換人、ROM176 換人、prefs＋反應文案、commit offer（刪 vera，加 lan／xu／yip／so）、蘇層級閘、分流核實、test_rom159_* 適配＋新測試。
- B1（v159-dates，clone linji-work159b1）：DATES 37 場（刪 vera 4 場、重定價、寫 30 場新場面）＋test_date159_static.py。唔掂 WOMEN／LOCS。
- B2（v159-map，clone linji-work159b2）：6 新 LOCS＋層切換＋sheet＋bg 對照＋約會對象列＋日常用途（巧遇第三點）＋test_map159_static.py。唔掂 WOMEN／DATES。
- C（場景圖，staging linji-159-images/）：6 張場景圖（真實香港相參照先＋PixelLab 生成）＋MANIFEST.md。唔入 repo。

## 5. 整合待辦（統籌）

- [x] **B1 完成回報（2026-11-17 11:33 UTC）**：commit `f83567a`（分支 v159-dates，clone linji-work159b1，基底 6cc403c；3 檔＋362／−23，未 push）。DATES 37 場（hiu 7／choi 5／lan 6／xu 7／yip 6／so 6），DATES 塊內 vera 零殘留（統籌核實：grep DATES 塊無 vera／Vera；cost 帶 $4／$6／$20／$45／$50／$58 齊，合 Q7）；新測試 test_date159_static.py 493 項 0 FAIL（統籌重跑核實）。**注意**：B1 量嘅全套基線係分支基線 310／21（Phase 1 測試本身喺 6cc403c 已有 FAIL：test_rom159_static.py 撞改名＋test_rom159_logic.js L257），唔係 main 基線 319／10；整合嗰陣統籌喺 v159 分支重跑全套再對。新增唯一 FAIL 係 test_rom159_logic.js L257（Phase 1 斷言硬寫 15 地點，B2 加 LOCS 都唔會綠，要 A 更新斷言；B1 無權改）。酒廊 $50 推算待確認（已標明）。index.html 其餘 vera_* 殘留（vera_commit／vera_crisis／vera_ending 等）屬 A 範圍，唔係 B1 漏。
- [x] **C 完成回報（2026-11-17 11:35 UTC）**：6 張齊晒，staging `~/workspace/linji-159-images/`（未入 repo），MANIFEST.md＋refs 6 張＋bodies 提示詞齊。尺寸全部 720×1280（harbour 257KB／peak 245KB／lounge 155KB／cinema 145KB／beach 101KB／airport 202KB，統籌 PIL 核實）；重生 lounge 1／cinema 2／beach 1／airport 1，Pixellab 共用 11 generations（結餘 3811.67→3800.67）。統籌抽睇 harbour＋airport 兩張：構圖啱、無字、無真人；啟德雙引擎客機低飛越過九龍城舊樓＋控制塔，構圖合「睇飛機升降」主旨，**接受雙引擎，唔使為 747 用埋最後 1 次重生**。**待定（見 §6）**：Pixellab 出品本質像素畫（224×400 生成再 NEAREST 放大），質感同現成 15 張平滑動畫場景圖唔同——統籌抽睇覺得同遊戲 8 條像素風 fx 片同系、觀感唔差，但係咪接受 6 張約會圖用像素質感，要 parent／用戶拍板；圖檔名不變，之後換圖唔使改 code。
- [x] **B2 完成回報（2026-11-17 11:43 UTC）**：commit `05db875`（分支 v159-map，clone linji-work159b2，基底 6cc403c；2 檔＋367／−10，未 push）。LOCS 21 個（15 舊零改動＋6 新 `type:"date"`／`layer:"date"`；統籌核實 6 個 date_* id 齊、bg_159_ 6 檔名齊）；層切換掣掛 #map-hint、drawMap 跟層走；sheet 加 6 行 LOC_SHEET_BG（404 fallback 米紙漸變）；約會掣 helper rom159WomenAtLoc（認直接 locId＋DATES key 間接兩種寫法）；日常用途 tertiary：out roll 唔中嗰陣 20% 去第三點（ENC79 葉→酒廊、蘇→海傍；ROM176 曉晴→啟德、采兒→戲院、藍→淺水灣、徐→山頂），主場／副場率、p／share／上限／冷卻零改動；出行額度照計、層切換唔計。新測試 test_map159_static.py 39 項 ALL PASS（統籌重跑核實）。全套 310／21→304／28（B2 重跑兩次同一數字）：新 FAIL 7 檔全部預期之內——5 檔舊「15 地點」count／set 斷言（map97／ui137_map／awards207／ux68／venue99）、enc105（LOC_SHEET_BG 15→21）、icons112（4 新 emoji 🌊🌃🏖️✈️ 唔喺 EMOJI_ICON112；正確修法係補 4 張手繪圖標＋條目，唔喺本票範圍）。**整合注意**：B2 clone 嘅 test_rom159_logic.js 係 69／0（佢嗰邊 DATES 未有 date_*，所以 L257 唔會 fail）；B1 clone 係 68／1（L257）。整合後 L257 一定 fail，要 A 更新斷言。7 個舊 test 更新（count 15→21、ux68 加 6 標籤、icons112 補圖標）留統籌整合嗰陣做。
- [x] **整合 cherry-pick 完成（2026-11-17）**：A（44f5e9f＋55a4306）→ B1（857ea2b，乾淨）→ B2（7ef3182，1 段衝突：ROM176_WOMEN 取 A 四人＋B2 tertiary 欄，6 個 tertiary 齊）→ C 圖檔 6 張入 `assets/story/locs/`（md5 同 staging 一致）。WOMEN.spots 對 DATES keys 全對（6 人 37 場）、DATES locId 全部係有效 LOCS、node --check PASS。整合 commit e168946（圖＋跨工人測試 resync）。
- [x] **內容批 resync 完成（統籌親手做）**：text125（三錨點 11053→11136／11195→11278／16419→16531）／weave46（v20a159 申報：react 區＋CMT_lan_commit 區；另清走 Phase 1 cherry-pick 遺留嘅 `>>>>>>> cd3ca66` 尾巴——weave46／text125／travel114 各有，三檔共 4 處）／rom176（6 釘＋costsDay 去註解＋茶記 6→4 句＋鎖斷言改認 ROM159 已定義）／rom183（同款三項＋B1 鎖旗改認 ROM159 6 處）／kwan151（12 釘實量）／tang152（R 計數改 [rom1,rom2,rom3]＋3 釘）——六檔逐個重跑全部 PASS。
- [x] **機械批 resync 完成（工人，統籌逐檔重跑核實）**：gift185／tang171／tang173（總行數 44712→45947＋openLoc DEF 40136→41299；tang173 L4862 實量 5205 行）／travel114（difflib 對位 47 錨點純漂移；COUNT 12／FREE 35→38——新 3 處 openLoc 全部係約會返程帶 `travelFree:true` 字面，統籌睇過原碼確認歸 FREE 啱：picker 取消／dismiss＋dateScene go fallback）／map97／ui137_map／awards207／venue99／enc105／ux68（15→21，6 新標籤位置逐個實量）／icons112（37→41；4 新 emoji 🌊🌃🏖️✈️ 入 passthrough 清單，手繪圖標留 follow-up 票）。11 檔統籌逐檔重跑全部 PASS。內容批 6 檔＋v159 新測試 5 檔亦全部 PASS。
- [ ] 全套 suite 第二輪跑緊（第一輪整合後：307／27）→ 重跑結果 → squash merge → push main → Pages 核實 → 刪工作副本（linji-work159b＋各工人 clone）
- [ ] WOMEN.spots ⊇ DATES keys 核實（逐人對）
- [ ] 全套 suite（基線 319／10）＋逐檔直接覆驗＋node --check
- [ ] text125／travel114／weave46 最終 resync（按實量）
- [ ] 實機驗證押後（瀏覽器死）——記低
- [ ] squash merge → push main → Pages 核實 → 刪工作副本（linji-work159b＋各工人 clone）
- [ ] 舊 linji-work159 去留等 parent 決定

## 6. 待確認（回報 parent）

- **約會場景圖質感（C 工人提出，統籌抽睇後轉交）**：6 張新圖係像素畫質感（Pixellab 224×400 生成再 NEAREST 放大至 720×1280），同現成 15 張地點場景圖嘅平滑動畫質感唔同；但同遊戲 8 條像素風 fx 片同系，統籌睇過 harbour／airport 兩張覺得觀感唔差。接受定要改用其他工具重做平滑版，等拍板；圖檔名不變，換圖唔使改 code。
- 酒廊唱歌約會使費 $50（推算，§4.8 表無此項）。
- 服裝＋屋企分拆後續：P1 四件衫 #1／#4／#10／#8 未逐件確認＋32 張圖。
- 蘇層級閘數字：配角或以上（enc79PlayerTier() ≥ 1），按草稿提議＋parent brief；如用戶想改，等拍板。

## 7. 落地紀錄（統籌，2026-11-17）

- **分支**：v159（HEAD `8c800be`），由 main `846e952`（v154）起，經 Phase 1 cherry-pick `6cc403c`＋A `44f5e9f`／`55a4306`＋B1 `857ea2b`＋B2 `7ef3182`＋整合 `e168946`＋resync `8c800be`。
- **內容**：感情線換人（Vera／海媚出局，葉敏芝／蘇芷茵入局；六人可 commit，HE 正式拍拖；排他鎖 rel 5、rel 6 commit）；約會層（DATES 37 場、Q7 價錢、6 新地點＋地圖兩層、tertiary 出沒點、6 張場景圖）；藍 crisis 重寫（屋企／阿爸壓力）；蘇層級閘（配角或以上）；送禮分層＋分流核實。
- **Suite**：**324／10，零回歸**（基線 319／10；+5 係 5 檔新測試全 PASS；FAIL 10 項同基線完全一致，全部 pre-existing）。
- **Resync 要點**：index.html 淨 +1235 行；清走 Phase 1 cherry-pick 遺留嘅 `>>>>>>> cd3ca66` 尾巴 4 處（weave46／text125／travel114）；travel114 FREE 35→38（3 處約會返程帶 travelFree:true）；icons112 4 新 emoji 入 passthrough（手繪圖標 follow-up）。
- **未做／留後續**：服裝＋屋企分拆後續（P1 四件未確認＋32 張圖）；實機驗證押後（瀏覽器死）；待確認：酒廊唱歌 $50（推算）、6 張場景圖像素質感（vs 現成 15 張平滑動畫）、icons112 4 手繪圖標；A 留低：R_yip／R_so meet-offer 接線未做、鏈 D 殘留重複風險、Vera／海媚／鄧麗萍死檔留刪除票。
