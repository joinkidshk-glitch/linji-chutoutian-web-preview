# NOTES V20A39 — 新 UI 接入第一期（HUD＋地圖＋通告紙卡）

性質：soft 預覽換膚/換圖。唔改 SAVE key（starVolunteer_map_v19w）、softRev（s107）、產品 ?v=（v20a10）；唔改 content pack；唔改 gigsForLocSeasonBoard／doAudition／castingNoticeDetailHtml／StoryPlay 邏輯。跟偵察報告 `linji-ui-integration-recon.md` 嘅切入點施工。

## 改動清單（全檔差異核對：只有以下 5 處）

1. **換地圖圖源**：`MAP_IMG` 常數（原行 4008）嘅 data URI 換成新大地圖正式版（來源 `linji-native-design/p1/scenes/world-map-final-v2-clean.png`，轉 JPEG 寬 1080、quality 80；新圖 1080×1432、JPEG 345,584 bytes、base64 460,780 字元；舊 payload 145,780 字元）。fallback 邏輯（冇 MAP_IMG 時行 `assets/hk_map.jpg`，drawMap＋尾段初始化兩處）冇郁。**【已被文末「地圖 v3（B 決策）修訂」取代：用戶拍板 B 案（補畫地圖）後，地圖已再換成 v3 定版 `world-map-v3-final.png`，座標亦按 v3 重標；本項 v2 圖源敘述只作歷史記錄。】**
2. **LOCS 座標重新標定**：13 個工作地點 x/y 全換（見下表；逐行核實除 x/y 之外所有欄位——name/area/type/region/emoji/lab/desc/residentNpc——原封不動）。
3. **HUD 換膚＋壓力條**：
   - 主 `<style>` 段最尾（`</style>` 之前）加「v20a39 新 UI 皮膚層」一段（約 98 行）：覆寫 `#map-bar`、`#map-dual-hud`、`.chip` 做米紙牌＋金邊＋柔和陰影；只改外觀屬性，冇郁 position/display 等佈局關鍵屬性；冇碰 `.map-pins`（避行 1474 `!important` 雷區）。
   - `#map-dual-hud` 靜態模板內新增 `<div class="hud-stress">`（標籤「壓力」＋軌道＋數字，id：hud-stress／hud-stress-fill／hud-stress-val）。
   - `paintBar()` 函數尾（adBoardToast 塊之後）以 `try{...}catch(_e){}` 防禦式加一段：用現成 `S.stress` 同步壓力條寬度（0–100 鉗制）、數字、warn（≥52）／danger（≥90）class——門檻同現行 chip-stress 一致。冇改 paintBar 既有任何一行。
4. **通告紙卡換膚（純 CSS）**：皮膚層覆寫 `.gig-teaser`——底色＋`--phys-notice` 紙紋底圖（cover）、金邊、紙卡陰影、頂部圖釘 `::before`、`.gt-title`/`.gt-meta`/`.gt-hint` 色調微調、`.g-seal` 加投影＋微傾（印章保留）。`gigBoardTeaserHtml` 模板冇改，`.gig-teaser` class 同 `data-gid` 保留（doScout 綁掣不受影響）。冇喺卡面造簽約金／違約金等唔存在嘅欄位。
5. **loc-sheet 輕換膚**：皮膚層以 `#app #loc-sheet.sheet` 覆寫底色漸變、金邊、頂部陰影、grab 色；結構冇改。

## LOCS 座標表（舊 → 新，% ；釘尖落點）【A 版，已作廢——v3 座標見文末修訂節】

標定方法：視覺定位工具喺新地圖逐棟建築攞位（電視塔／廠棚／茶餐廳／跑道／攤檔／戲院／醫院／唐樓／衛星碟大樓等），再用 PIL 將 13 點＋6 NPC 標記繪圖核對（`locs-check.png`，工作副本內）。全部點對點距離 ≥7.6%，唔會觸發 drawMap 嘅 CLUSTER（7.5%）扇形錯開。

| id | 名稱 | 舊 (x,y) | 新 (x,y) | 落點依據 |
|---|---|---|---|---|
| tvb_longmen | 星河電視台 | 74,36 | **34,12** | 地圖唯一電視塔（天線＋衛星碟） |
| film_lion | 獅子山製片 | 56,14 | **78,12** | 片場大棚正中 |
| film_cotton | 紅棉影業 | 48,54 | **71,17** | 片場區西南草地（廠棚旁） |
| film_harbour | 維港電影 | 20,66 | **88,13** | 片場吊臂基座旁 |
| tvb_harbour | 海港廣播 | 90,52 | **84,21** | 片場區東南草岸（清水灣台址靠片場） |
| cafe_cha | 金龍茶餐廳 | 26,32 | **19,21** | 綠帆布茶餐廳建築正中 |
| rec_hk | 香江唱片 | 40,36 | **37,33** | 廟街攤檔排西段（旺角街面） |
| tvb_kowloon | 九龍電視台 | 64,46 | **53,26** | 北岸路口空地（攤檔東北、跑道西；圖上冇第二座電視台，取地理鄰近位） |
| ad_central | 中環廣告 | 33,73 | **83,53** | 戲院大樓（旭日招牌座） |
| ad_adm | 金鐘創意 | 47,67 | **85,65** | 玻璃幕牆商業大樓 |
| rec_wanchai | 灣仔唱片 | 61,74 | **63,64** | 南岸中段褐色商業樓 |
| rec_star | 天星音樂 | 75,68 | **77,81** | 雙衛星碟大樓（南岸音樂/廣播區） |
| agency_ho | 何生事務所 | 16,90 | **23,86** | 左下唐樓（沿舊圖左下角事務所位） |

核對圖覆核修正咗 3 點先定案：tvb_harbour 原定 (90,22) 落咗水邊 → 收返 (84,21)；tvb_kowloon 原定 (57,29) 疊住攤檔尾 → 移 (53,26)；film_harbour 微調 (88,13) 拉開同 tvb_harbour 距離。

### 關於「6 個 NPC 座標」嘅事實更正

偵察報告寫 LOCS 共 19 項（13 地點＋6 NPC），但實檔核實：`const LOCS` 只有 13 項；6 個 NPC 喺獨立 `NPCS` 表，**本身冇 x/y**——佢哋喺地圖上係以「熟人」標記騎喺地點釘呈現（`S.locNpc` 每日派位自 `NPCS.homes`；何生另有 `residentNpc:"agent"` 駐 agency_ho）。所以標定 13 個地點釘已經覆蓋晒 19 個顯示點，唔使亦唔應該畀 NPC 新造座標欄位。核對圖上嘅藍點係 NPC 主要出沒位（homes 首位）嘅示意標記，唔係遊戲釘：林曉晴／高俊傑→tvb_longmen 旁、張子駿→film_cotton 旁、Vera→ad_central 旁、周采兒→rec_star 旁、何生→agency_ho 旁。

### 地圖上冇遊戲地點嘅建築（本期不處理）【v2 圖敘述，v3 更正見修訂節】

新地圖仲有兩棟冇對應 LOCS 嘅建築：紅地氈大禮堂（約 17,44；原型「頒獎禮場館」）同醫院（約 44,75）——遊戲本身冇頒獎禮／醫院地點，本期唔加新地點，純裝飾。原型嘅「阿偉屋企」pin 同理（遊戲冇屋企地點；左下唐樓由 agency_ho 沿用舊位承接）。**【v3 更正：v3 定版地圖已按 B 決策為 13 個地點逐一畫咗專屬地標建築（見修訂節），唐樓係 agency_ho 嘅專屬建築（大白招牌板），唔再係「沿用舊位承接」；紅地氈大禮堂（v3 約 12,44）同醫院（v3 約 38,75）喺 v3 仍然冇對應遊戲地點，維持純裝飾。】**

## 已知限制／留待二、三期

- 場景圖（LOC_SHEET_BG 13 張）同 StoryPlay 立繪／場景分層係二期，本期冇掂；loc-sheet 只換膚，底圖機制沿用舊圖。
- 報紙實物化係三期，本期冇掂 `.paper-sheet`。
- `.gig-teaser` 紙紋用現有 `--phys-notice` 外部素材（notice_paper.png）；新出嘅通告紙素材（ui-gig-paper）未換入 token（換 token 屬一行改，但要另行核實新圖同卡尺寸嘅裁切效果，留待實機對照後決定）。
- HUD 壓力條係新增 DOM；舊存檔／其他呼叫 paintBar 嘅路徑全部經同一函數餵數，冇額外接線。元素缺失時 try/catch 靜靜跳過。
- 地圖比例變咗（舊圖同新圖長寬比唔同）：drawMap 用百分比座標＋容器高度對位，座標已按新圖重標； polaroid 框（--phys-polaroid）冇改，實機要留意框同圖嘅貼合。

## 驗證結果（工作副本 ~/workspace/linji-work39）

- 基線（未改檔）：repo tests/ 全套 30 檔（16 node 邏輯＋14 python 靜態，連 fixtures 7 檔同 NOTES 依賴 3 檔一齊下載）**全 PASS**。
- 改後：全套 30 檔 **全 PASS**（同基線一致；冇測試釘 LOCS 座標或 MAP 圖內容，所以冇「預期內數據變更」型 fail）。
- `node --check`：全檔 2 個 script 段抽出逐個驗，syntax OK。
- 逐行差異核對（vs 原檔備份）：改動只有上述 5 處，冇計劃外改動；LOCS 逐行核實除 x/y 外冇欄位差異。
- 紅線 grep：`const SAVE = "starVolunteer_map_v19w"` 在位；`softRev=s107` 在位；`"v20a10"` 自檢字串在位。
- 檔大小：2,489,163 → **2,809,084 bytes**（+319,921，主要是地圖 base64 变大）。**【v3 修訂後為 2,857,580 bytes，見修訂節。】**

## 地圖 v3（B 決策）修訂

背景：A 版地圖（v2）上面只有部分地點有對應建築，其餘靠地理鄰近估位。用戶 2026-11-09 拍板揀 **B 案：補畫地圖，加入埋缺咗嘅地標**——即係唔用「按地理大約標」，要補畫地圖，令 13 個工作地點各有獨立可辨認地標（3 間電視台、3 間電影公司、3 間唱片公司、2 間廣告公司＋茶餐廳＋事務所）。美術按此出咗 v3 定版地圖，本節記錄換圖＋按 v3 重標座標；本節內容取代上文所有 v2 地圖／A 版座標敘述。一期其餘改動（HUD 皮膚＋壓力條、通告紙卡、loc-sheet 換膚）原封不動。

### 換圖

- 來源：`linji-native-design/p1/scenes/world-map-v3-final.png`（1376×1824）。
- 處理同上次一致：轉 JPEG 寬 1080（1080×1432）、quality 80 → JPEG 381,956 bytes、base64 509,276 字元（v2 payload 為 460,780 字元），替換 `MAP_IMG` 常數嘅 data URI。fallback 邏輯冇郁。

### LOCS 座標表（A 版 → v3 版，% ；釘尖落點）

標定方法：視覺定位工具喺 v3 圖逐棟建築攞 bbox 取中心，再用 PIL 將 13 點＋6 NPC 出沒位（藍點示意）繪圖核對（`locs-check-v3.png`，工作副本內），逐點 read 驗證全部落喺對應建築之上先定案。主代理目測估位同定位結果大致吻合，一處明顯修正：film_lion 估位 (56.5,13.5) 偏右，實測嗰間棚中心喺 (52,12)。全部點對點最細距離 10.3%（film_harbour↔tvb_harbour、rec_wanchai↔rec_star），唔會觸發 drawMap 嘅 CLUSTER（7.5%）扇形錯開。

| id | 名稱 | A 版 (x,y) | v3 版 (x,y) | 落點依據（v3 專屬地標） |
|---|---|---|---|---|
| cafe_cha | 金龍茶餐廳 | 19,21 | **15,16** | 左上綠色茶餐廳建築正中 |
| rec_hk | 香江唱片 | 37,33 | **30,24** | 黑膠唱片大樓（巨型唱片喺屋頂） |
| tvb_longmen | 星河電視台 | 34,12 | **41,14** | 全圖最高電視塔塔身 |
| film_lion | 獅子山製片 | 78,12 | **52,12** | 獅子頭山丘前面嗰間廠棚 |
| film_cotton | 紅棉影業 | 71,17 | **68,11** | 中間大棚（紅木棉樹喺佢右邊） |
| film_harbour | 維港電影 | 88,13 | **80,18** | 近海嗰間廠棚（衛星碟平台下面） |
| tvb_harbour | 海港廣播 | 84,21 | **90,15** | 碼頭平台雙衛星碟 |
| tvb_kowloon | 九龍電視台 | 53,26 | **37,45** | 橋頭格仔天線陣矮樓（紅地氈禮堂右邊、橋左端） |
| ad_central | 中環廣告 | 83,53 | **64,57** | 全圖最高玻璃塔塔身 |
| ad_adm | 金鐘創意 | 85,65 | **85,60** | 階梯圓頂塔 |
| rec_wanchai | 灣仔唱片 | 63,64 | **72,77** | 音符標誌大樓 |
| rec_star | 天星音樂 | 77,81 | **81,82** | 星形屋頂大樓（渡輪碼頭旁） |
| agency_ho | 何生事務所 | 23,86 | **24,86** | 左下唐樓大白招牌板 |

逐行核實：LOCS 除 x/y 之外所有欄位（name/area/type/region/emoji/lab/desc/residentNpc）同原檔完全一致（座標遮罩後逐字元比對相同）。6 NPC 冇 x/y、以熟人標記騎地點釘嘅更正（見上文）喺 v3 維持不變；核對圖藍點係 homes 首位示意：林曉晴／高俊傑→tvb_longmen、張子駿→film_cotton、Vera→ad_central、周采兒→rec_star、何生→agency_ho。

v3 圖上仍然冇對應遊戲地點嘅建築：紅地氈大禮堂（約 12,44）同醫院（約 38,75）——遊戲冇頒獎禮／醫院地點，維持純裝飾，唔加新地點。另外留意：v3 地圖比例同 v2 相同（1376×1824），polaroid 框貼合考慮同 A 版一致。

### 修訂驗證結果

- `node --check`：全檔 2 個 script 段抽出逐個驗，syntax OK。
- repo tests/ 全套 30 檔（16 node 邏輯＋14 python 靜態）：**30/30 全 PASS**（同 A 版一致；static 測試要喺副本根目錄以 `python3 tests/<file> index.html` 行，喺 tests/ 目錄內直接行會因相對路徑搵唔到 index.html 而 fail，屬執行方式問題、唔係改動引起）。
- 紅線 grep：`const SAVE = "starVolunteer_map_v19w"`、`softRev=s107`、`"v20a10"` 自檢字串全部在位；一期皮膚層（v20a39 皮膚層註解、hud-stress、.gig-teaser 覆寫）核實仍在。
- 檔大小：2,809,084（A 版）→ **2,857,580 bytes**（+48,496，同地圖 payload 增幅 509,276−460,780 完全吻合，證明今次改動只有換圖＋改座標）。
