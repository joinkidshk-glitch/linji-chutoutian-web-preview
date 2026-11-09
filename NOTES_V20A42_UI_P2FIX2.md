# NOTES V20A42 — 新 UI 接入第二期補修 2（全屏分層版面實機 FAIL 修復）

性質：soft 預覽版面修復。**純 CSS 改動**，只喺 v20a41 皮膚層段內修改 4 處（冇加新段、冇郁 v20a39/v20a40 層）；零模板、零 JS、冇新素材。唔改 SAVE key（starVolunteer_map_v19w）、softRev（s107）、產品 ?v=（v20a10）；唔改 content pack；唔改 StoryPlay 邏輯／劇情數據。

## FAIL (a) 舞台底部漏光——根因（兩個舊規則夾擊 v20a41）

實機現象：對話／選擇畫面底部約 80–90px 冇被舞台遮住，地圖底部地點列（#map-area-list，地點名＋圖示）調暗後仍可辨認、「下一句」掣壓喺上面。

1. **掣欄冇變 overlay，食咗舞台高度**：舊規則（行 3121）`#mask:not(.tut-on) #modal-btns{flex:0 0 auto !important; position:sticky !important; bottom:0 !important}` 帶 !important；v20a41 用嚟將 #modal-btns 改做底部 overlay 嘅 `:has()` 規則只寫 `position:absolute`（冇 !important），**輸咗畀 sticky !important**。結果掣欄留喺 .modal 嘅流程入面（掣高 44px＋上下 padding＋安全區 ≈ 80–90px），`#modal-inner`（flex:1 1 0%）同入面 height:100% 嘅 .story-play／.sp-stage 就矮咗嗰截，落唔到真正底邊。
2. **嗰截冇任何不透明層**：掣欄喺嗰截嘅背景係 :has 規則嘅透明頂漸變（嗰條 background 冇 !important 爭議、特異度較高所以生效）；而 #mask 自身底色方面，v20a41 寫嘅 `#mask.story-play-on{background:#0a0705}` 冇 !important，**輸咗畀舊規則 `#mask.on{background:rgba(0,0,0,.72) !important}`（行 1246）**，成個 #mask 只係一層 72% 黑嘅半透明幕。舞台冇遮到嘅地方，地圖就以約 28% 亮度透出——正係「調暗仍可辨認」嘅來源。選擇模式掣欄本身就設計成留喺流程底欄，同樣受第 2 點影響（底欄以外／周邊冇不透明承托）。

**修法（全部喺 v20a41 段內）**：
- `:has()` 對話／旁白掣欄規則：`position:absolute` → `position:absolute !important`，壓過 sticky !important，掣欄脫離流程 → #modal-inner 恢復全高 → 舞台落到真正底邊（對話牌底部原有 66px 留位唔受影響）。
- `#mask.story-play-on` 底色：`background:#0a0705` → `#0a0705 !important`，壓過 rgba(.72) !important，作用域內成個遊戲框由不透明幕承托。
- `.modal` 底色：`background:transparent !important` → `#0a0705 !important`——舞台万一再有任何子盒落唔到底，嗰截都係舞台底色而唔係地圖；場景圖本身喺 .sp-stage 內繪製，唔受 modal 底色影響。
- 選擇模式維持 v20a41 設計（掣欄留流程底欄，深色 #17100a），而家底欄前後有不透明 modal／mask 承托，成個框（舞台＋底欄）完全遮蓋；唔支援 :has 嘅舊瀏覽器同理退回流程底欄＋不透明承托，唔會再漏光。

## FAIL (b) 企立圖唔夠高——根因（max-width 撞限，唔係 % 參照盒）

實機現象：CSS 寫 height:70%，實測何生 41%、阿偉／張子駿 49%。

- 先排除参照盒疑點：企立圖（.sp-bust-stand）係 position:absolute，佢嘅 containing block 唔係 .sp-stage-inner（v20a40 嘅 `:has` 規則已將有企立圖時嘅 stage-inner 設做 position:static），而係 .sp-stage；v20a41 嘅 stage 係 inset:0 全高，所以 height:70% 嘅參照係全舞台高，冇縮水。base .sp-bust 嘅 aspect-ratio:3/4 對有天然比例嘅 <img> 唔生效（實測各人高度唔同、正比於各自天然比例，亦證呢點）。
- 真正綁住嘅係 v20a41 自己寫嘅 **max-width:58%**（% 按 containing block 闊度計）。企立源圖全部高 500px，闊 325–416px（天然比例 0.650–0.832，係腰上構圖、人物撐滿成幅）：要顯示到 70% 高，闊度需要係畫面高嘅 45.5%（阿偉）至 58.2%（何生）；手機框闊／高比約 0.55，即係需要 83%–106% 嘅舞台闊度。58% 上限先到，瀏覽器就按比例將高度縮返落嚟：上限高度 = 58% × 舞台闊 ÷ 天然比例，正好得出何生 ≈41%、阿偉／張子駿 ≈49%，同實測吻合。

**修法**：v20a41 企立規則改 `height:72%; max-height:72%; max-width:94%`（唔拉伸、唔換圖）。按同一條公式推算（闊高比 0.55 嘅框）：阿偉、張子駿、曉晴、采兒、陸柏言、鄧麗萍可達 72%；雷勁 ≈68%、高俊傑 ≈68%；**何生、Vera（比例 0.83）受幾何所限約 62%**——要佢哋過 65%，max-width 要 ≥98%（人物盒闊到等於成個舞台，遮晒場景，違反構圖要求），所以接受 ~62% 並喺度申報；框越窄佢哋會再低少少，屬同一幾何限制。企立仍然企左下、對話牌（z-index 較高）壓喺前面，構圖不變。

## 改動清單（v20a41 段內共 4 處＋段首註解增補）

1. `#mask.story-play-on`：background 加 !important。
2. `#mask.story-play-on .modal`：background 由 transparent 改 #0a0705（保留 !important）。
3. `.sp-bust.sp-bust-stand`：height/max-height 70%→72%，max-width 58%→94%。
4. `:has(.sp-mode-dialogue/.sp-mode-narration) #modal-btns`：position:absolute 加 !important。
5. 段首加 v20a42 補修註解（根因摘要）。

旁白中央牌、選擇紙條下半部、地點畫面、選單、地圖底部地點列本身（非對話時）全部冇郁。

## 驗證結果（工作副本 ~/workspace/linji-work42）

- `node --check`：全檔 2 個 script 段抽出逐個驗，syntax OK。
- repo tests 全套：**30/30 PASS**（16 node 邏輯＋14 python 靜態，喺副本根目錄傳 index.html 路徑行）。
- 二期 hook 測試：**15/15 PASS**（抽真常數 UI40_STAND/UI40_SCENE/UI40_BG_BY_KEY＋真函數 spBustUrl/spBustIsStand40/spBgImageCandidates 行 node：awi/ho_sang/luk_baakyin 命中企立、awi smile 表情 fallback 企立、so_jiyan/liu_bingxing/ngai_wingnaam/yip_manji/gao_wenhan 行舊鏈、企立覆蓋＝10／場景＝5、cafe/c1_tea 首位內嵌＋保留檔案 fallback、tvb_kowloon 行檔案鏈、generic_interior 維持空）。今期 JS 零改動，此項屬防腐核對。
- 紅線 grep：`SAVE = "starVolunteer_map_v19w"` 在位、`softRev=s107` 在位、`"v20a10"` 自檢字串在位。
- 逐行差異核對（vs v20a41 已合併版）：只有上述 v20a41 段內 4 處 CSS 改動＋段首註解增補，冇計劃外改動。
- 檔大小：4,190,579 → **4,191,715 bytes**（+1,136，全屬註解文字；推送通道上限約 4.2MB，仍在安全範圍）。
