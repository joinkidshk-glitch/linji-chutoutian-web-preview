# NOTES V20A40 — 新 UI 接入第二期（對話場景分層化）

性質：soft 預覽換膚/換圖＋資產解析接駁。唔改 SAVE key（starVolunteer_map_v19w）、softRev（s107）、產品 ?v=（v20a10）；唔改 content pack；唔改 StoryPlay 對話邏輯／劇情數據／advance／選項／鎖。工作副本 `~/workspace/linji-work40/`（基線＝已合併 main 嘅 v20a39 版，2,857,580 bytes）。

## 1. 素材路線結論：binary 入唔到 repo → 行內嵌（MAP_IMG 前例）

開工前實測 GitHub MCP `create_or_update_file`：

- 開咗探針分支 `probe-assets-v20a40`，用 `create_or_update_file` 傳一張 179 bytes 測試 PNG 嘅 base64 字串去 `assets/ui/_probe.png`（commit 379838b）。
- 回讀 raw 檔驗證：**檔入面存嘅係 base64 字串本身（220 bytes 純文字，同輸入逐字元一致），唔係解碼後嘅 PNG**——即呢條 MCP 通道同 snapshot push 一樣只搬 UTF-8 文字，binary 過唔到。探針檔已用 `delete_file` 清走（commit 2fb87ec），探針分支留底作證據。
- 結論：**外部 assets 路徑此路不通**，二期改行偵察報告 §7 嘅後備路線——精選素材轉 data URI 內嵌（跟一期 MAP_IMG 做法），接駁位跟返現有機制（`spBustUrl`／`spBgImageCandidates`／`LOC_SHEET_BG`），唔另起爐灶。

## 2. 改動清單（全檔差異核對：只有以下 6 處）

1. **新增內嵌素材常數**（MAP_IMG 常數行之後）：`UI40_SCENE`（5 張場景 JPEG data URI）、`UI40_STAND`（企立 WebP 去背 data URI；初版 14 張，壓縮跟進後 10 張，見 §9）、`UI40_BG_BY_KEY`（StoryPlay bg key → 場景對應表）。
2. **v20a40 皮膚層**（主 `<style>` 段最尾、v20a39 皮膚層之後）：`.sp-bust.sp-bust-stand` 企立呈現（absolute 左下、height 100% 舞台、無框無底、object-fit contain）、`.sp-stage:has(.sp-bust-stand)` 提升舞台高度（min 47dvh/336px、max 54dvh/368px）、`.sp-stage-inner:has(.sp-bust-stand)` 改 static 令企立以舞台為定位基準、`.sp-plate` 米紙化（米紙漸變＋金邊＋內高光，speaker 名改啡金）、`.sp-choice` 同色系微調。舊 bust（冇 stand class）版面完全唔受影響。
3. **`spBustUrl` 加企立優先 hook**（StoryPlay 內，函數頭 2 行，try/catch＋typeof 防禦）：命中 `UI40_STAND` 就回傳 data URI；其餘角色行返原有候選鏈原封不動。另加細 helper `spBustIsStand40()` 畀模板判斷。
4. **`spBgImageCandidates` 加內嵌場景優先 hook**：命中 `UI40_BG_BY_KEY` 嘅 key 將 data URI 插入候選首位（data URI 必載入成功，後面檔案候選保留做 fallback）；其餘 key（tvb_kowloon／tvb_harbour／ad_*／bg_c1_* 其他等）行返舊鏈。
5. **對話模板立繪 img 加條件 class**：`spBustIsStand40(cur.speakerId)` 為真先加 `sp-bust-stand`（只加 class，模板結構／屬性／onerror 鏈冇改；企立圖萬一載入失敗，`data-sp-bust-fallbacks` 依舊指向舊 bust 檔，自動退回舊圖）。
6. **`LOC_SHEET_BG` 換值 9 項**：改指向 `UI40_SCENE.*`（見 §3 表）；其餘 4 項沿用 repo 舊圖路徑。

## 3. 地點 → 場景圖對應表（LOC_SHEET_BG＋StoryPlay bg 共用同一批內嵌圖）

| 地點 | 新場景圖（內嵌） | 本地來源（定版） |
|---|---|---|
| cafe_cha 金龍茶餐廳 | UI40_SCENE.cafe | media-generation-anime-scene-chachaanteng（動畫風定版茶餐廳） |
| agency_ho 何生事務所 | UI40_SCENE.agency | p1/scenes/scene-agency-office |
| film_lion 獅子山製片 | UI40_SCENE.studio | p1/scenes/scene-clearwaterbay-studio |
| film_cotton 紅棉影業 | UI40_SCENE.studio（共用片場圖） | 同上 |
| film_harbour 維港電影 | UI40_SCENE.studio（共用片場圖） | 同上 |
| tvb_longmen 星河電視台 | UI40_SCENE.startv | p1/scenes/scene-startv |
| rec_hk 香江唱片 | UI40_SCENE.recording | p1/scenes/scene-recording-studio-v2（定版 v2） |
| rec_wanchai 灣仔唱片 | UI40_SCENE.recording（共用錄音室圖） | 同上 |
| rec_star 天星音樂 | UI40_SCENE.recording（共用錄音室圖） | 同上 |
| tvb_kowloon 九龍電視台 | **沿用舊圖** assets/story/locs/bg_loc_tvb_kowloon.jpg | 新場景 12 張冇第二間電視台圖，唔硬套星河圖 |
| tvb_harbour 海港廣播 | **沿用舊圖** bg_loc_tvb_harbour.jpg | 同上 |
| ad_central 中環廣告 | **沿用舊圖** bg_loc_ad_central.jpg | 新場景冇廣告公司／商業大廈內景對應 |
| ad_adm 金鐘創意 | **沿用舊圖** bg_loc_ad_adm.jpg | 同上 |

StoryPlay 側：`bg_loc_*` 對應同上表；另 `bg_c1_tea_restaurant`（C1 茶餐廳）→ cafe。

## 4. 角色 → 企立圖對應表（UI40_STAND，壓縮跟進後 10 人；見 §9）

揀選原則：StoryPlay 最常用嘅核心陣容＝主角＋SP_CORE_STEM 6＋SP_ERA_STEM 5＋何生＋張子駿（preferFile 特例位）。初版內嵌 14 人；壓縮跟進（§9）按出場頻率剔走 4 位紅星（廖炳星、魏詠男、葉敏芝、蘇芷茵），最終覆蓋 10 人，尺寸為壓縮後高 500 版（原高 620 版尺寸見 git 前版 NOTES／§9 記錄）。

| speakerId | 角色 | 本地來源（p0/standing 定版） | 壓縮後尺寸 |
|---|---|---|---|
| awi | 阿偉（stage1 臨記期） | stand-awei-stage1 | 325×500 |
| ho_sang | 何生 | stand-hosang | 416×500 |
| cheung_tsijun | 張子駿 | stand-cheungtsijun-v2 | 331×500 |
| lin_hiu | 林曉晴 | stand-linhiu | 346×500 |
| chow_choiyi | 周采兒 | stand-chowchoiyi | 346×500 |
| ko_chunkit | 高俊傑 | stand-kochunkit | 379×500 |
| vera | Vera | stand-vera（口袋修正版） | 415×500 |
| lui_ging | 雷勁 | stand-lui-ging | 373×500 |
| tang_laiping | 鄧麗萍 | stand-tang-laiping | 352×500 |
| luk_baakyin | 陸柏言 | stand-lukbaakyin | 342×500 |

壓縮跟進剔走（4 人，行返舊鏈）：liu_bingxing 廖炳星、ngai_wingnaam 魏詠男、yip_manji 葉敏芝、so_jiyan 蘇芷茵——紅星遠觀／目標層角色，出場頻率低過核心陣容；陸柏言因屬串聯鏈 A 主角且檔案最細而保留。

冇覆蓋（其餘 21 人：上列 4 人＋高文瀚、藍若曦、張克凡、關海媚、鄭威廉、唐素雲、方小龍、徐寶珊、莫少輝、金九、齊鎮海等＋generic/extra）：企立原圖本地齊全，但全部內嵌會再脹約 1MB base64；呢批角色行返舊鏈（PORTRAITS 內嵌頭像／npc 檔／剪影），留待原生期或下一輪按出場頻率補。

**去背方法**：原圖全部係純米色底 RGB（冇 alpha）。以邊界像素中位數做 bg 色、RGB 距離 <30＋邊界連通標記（scipy label）抽背景 → alpha，Gaussian 羽化 1.1px，裁邊後縮高 620、WebP q84。QA：14 人深綠底對照圖逐個睇過＋alpha 遮罩覆核。
- 口袋修正：Vera（左腰 1 處）、葉敏芝（左右腰各 1 處）手叉腰姿勢留低封閉背景口袋，用網格定位＋保守多邊形人手擦除，alpha 遮罩覆核已穿窿。
- 教訓：唔好用「全圖 dist<14 一律移除」做口袋 pass——蘇芷茵膚色（≈251,241,227）同 bg 幾乎同色，會成塊面移走；已否決，改逐人人手處理。

**阿偉階段**：只內嵌 stage1（臨記期，遊戲大半時間造型）；stage2/3 企立本地有圖，但按遊戲進度切換需要階段判斷接線，超出二期範圍，冇做。

## 5. 表情差分申報（冇硬造）

- 企立圖每人得一張（default 神情），**冇企立版 smile/frown 差分圖**；p0/expr 嗰批差分係 bust 構圖，同企立版面唔夾，冇硬接。
- 現行處理：覆蓋角色（初版 14 位、壓縮跟進後 10 位，見 §9）無論 beat 表情（smile/frown/raise_brow/eyes_down/look_aside）一律出 default 企立（emotion 色調 filter 規則照舊生效，有輕微情緒色感）；未覆蓋角色（連壓縮跟進剔走嘅 4 位紅星）行舊鏈，佢哋嘅表情差分（assets/story/core・era_stars 嘅 _bust_smile/_frown 檔）**完全冇受影響**。
- 即：機制層面表情候選保留，檔案層面企立差分待補（原生期美術清單已有表情差分項）。

## 6. 體積帳（壓縮跟進後最終版，見 §9）

| 項目 | 原始 bytes | 備註 |
|---|---|---|
| 企立 ×10（WebP 去背 h500 q80） | 324,468 | 單張 19.6–46.7KB |
| 場景 ×5（JPEG 800w q70） | 668,090 | cafe 94,628／agency 150,432／studio 140,659／startv 128,261／recording 154,110 |
| 素材 payload 合計 | 992,558 | |
| index.html | 2,857,580 → **4,184,081**（+1,326,501） | 增幅＝base64（payload ×≈1.33）＋常數/hook/CSS 程式碼 |

初版（壓縮前）體積：企立 ×14 h620 q84＝707,890、場景 ×5 960w q78＝1,070,835、payload 1,778,725、index 5,232,468——推送時撞 HTTP 413，先有 §9 壓縮跟進。

影響：首次載入（無 cache）多約 1.3MB 傳輸；data URI 喺常數層定義、唔喺開局 HTML 模板，立繪/場景都係用到先解碼。已知取捨，換取 binary 通道未通之前二期可以落地。

## 7. 驗證結果

- `node --check`：全檔 2 個 script 段逐個驗，syntax OK。
- repo 測試：基線（未改）30/30 PASS → 改後 **30/30 PASS**（16 node 邏輯＋14 python 靜態，與基線一致）。
- hook 功能測試（抽真函數喺 node 行）：初版 11 項斷言全 PASS；壓縮跟進後重行 15 項斷言全 PASS（awi/ho_sang/luk_baakyin 命中企立 data URI、smile 表情企立 fallback、so_jiyan/liu_bingxing/ngai_wingnaam/yip_manji 已剔走行返舊鏈、gao_wenhan 行返舊鏈、企立覆蓋數＝10／場景數＝5、bg_loc_cafe_cha／bg_c1_tea_restaurant 首位係內嵌圖兼保留檔案 fallback、bg_loc_tvb_kowloon 行返檔案鏈、bg_generic_interior 維持空）。詳見 §9。
- 內嵌完整性：初版抽 UI40_STAND.awi／UI40_SCENE.recording 驗 MD5；壓縮跟進後全部 15 項素材（場景 5＋企立 10）逐項解碼同新處理檔 MD5 一致。
- 紅線 grep：`starVolunteer_map_v19w`、`s107`、`"v20a10"` 全部在位冇變。

## 8. 已知限制／留待三期

- `.sp-stage:has(.sp-bust-stand)` 用 CSS `:has()`（2023+ 瀏覽器全支援）；唔支援嘅舊瀏覽器企立圖會 absolute 溢出舞台頂被裁——網頁版係開發載體，可接受；原生版唔受影響。
- 傾談（openLoc 內 NPC 對話 modal）唔經 StoryPlay 舞台，今期冇掂，維持文字版（跟偵察分期）。
- 報紙實物化、開始畫面／手帳收尾係三期，今期冇掂 `.paper-sheet`。
- 探針分支 `probe-assets-v20a40` 留喺 repo 作 binary 測試證據（入面探針檔已刪，淨返空樹 commit），可隨時刪。

## 9. 壓縮跟進（推送 413 後追加）

背景：初版 index 5,232,468 bytes 推送 repo 時撞 HTTP 413（request body too large；一期 2,857,580 bytes 冇事），目標壓到 ≤4,200,000 bytes。接駁邏輯（hooks／皮膚層／LOC_SHEET_BG 指向）完全冇改，只換素材 data URI 同參數。

做法同取捨：

- **企立**：唔重新去背——初版已去背＋口袋修正嘅成品只存在於 index 內嵌 WebP（work40 冇中間產物），故由內嵌版解碼出嚟做 alpha 預乘（premultiplied）Lanczos 縮放，避免邊緣光暈；高 620→500、WebP q84→q80。QA：10 人深綠底對照圖＋alpha 極值/半透明邊像素統計，冇穿冇誤殺、Vera 口袋修正保留完好。
- **場景**：原規格試 896w q72 得 825,468 bytes，連企立（463,844）payload 1,289,312 仍超預算（≤1,004,388）約 285KB；即使剔晒 5 位紅星企立（158,934）都唔夠。故場景再減一級至 **800w q70**（668,090）——場景只做手機闊度底圖，800w 仍約 1.9 倍顯示闊度，畫質影響輕微；換取核心陣容企立全數保留。
- **剔企立 4 人**：場景減級後企立預算 336,298，仍要剔走 ≥127,546。按出場頻率剔紅星 4 人：蘇芷茵（31,514）→葉敏芝（41,874）→魏詠男（28,384）→廖炳星（37,604）；陸柏言保留（串聯鏈 A 主角＋檔案最細 19,558）。剔走者 `spBustIsStand40` 回 false，自動行返舊鏈（bust／PORTRAITS／剪影），零邏輯改動。被剔 4 人嘅 h500 版已編碼備用，日後通道放寬可直接補入。
- 最終：payload 992,558（場景 668,090＋企立 324,468），index **4,184,081 bytes**（≤4,200,000，餘量 15,919）。

事故記錄：替換常數時尾項 luk_baakyin 嘅字串收尾引號一度脫落（只剩開引號），`node --check` 即時捉到（SyntaxError），已單點補回並逐項覆核全部 15 項素材 entry 均為恰好 2 個引號＋base64 可解碼，先至重行全套驗證。

壓縮後重驗（全部 PASS）：`node --check` 兩段 OK；hook 功能測試 15/15（見 §7）；repo 測試 30/30（副本根目錄傳 index.html 路徑行 static）；15 項素材解碼 MD5 同新處理檔逐項一致；紅線 grep 三項在位；同初版 scrub-diff 核對，差異只限 UI40_SCENE／UI40_STAND 兩常數塊（data URI 內容＋4 行剔除＋尾逗號）。
