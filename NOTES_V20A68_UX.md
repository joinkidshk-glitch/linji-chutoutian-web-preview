# NOTES v20a68 — UX 包（手帳訓練指南／地點選項整理／地圖墨字地名／重量紓緩）

基底 v20a67（PR #167）。用戶 2026-11-10 10:29–11:41 實玩反饋＋逐項拍板。唔改 SAVE key
`starVolunteer_map_v19w`、softRev `s107`、產品 `?v=v20a10`；冇改 content pack JSON。
tests：68 基線＋新增 test_ux68_logic／test_ux68_static ＝ **70/70 全綠**（新測試喺 v67 index 上行會 FAIL，反證成立）。

## 一、手帳「訓練指南」頁（新分頁 data-htab="guide"）

- 手帳加第十個分頁「訓練指南」＋ pane `#home-pane-guide`；setHomeTab allow／pane 清單／render
  分支／syncHomeTabExit journalTab 四處接線。
- 按數值列 10 項（演技／台風／歌藝／外貌／魅力／智商／體能＋幕前聲望／人氣／壓力），跟
  STAT_LABEL；撳 chip 即睇嗰個數值嘅課程。
- **課程清單同增益唔係硬編碼**：開頁時 `ux68ParseGainTable()` 解析 `applyTrainLesson` 函數
  源碼入面每課嘅 `applyGain60({...})` 字面量衍生（key: N → +N；N+R(0,M) → +N~N+M）。
  課名／icon 出 COURSE_DEFS；地點出 TRAIN_BY_TYPE（主課）＋COURSE_ENROLL_EXTRA（附帶）；
  解鎖門檻出 `ux68UnlockRule`——同 `maybeUnlockMidCourses` 逐條對應（進階演技＝演技 3 堂／
  進階台風＝台風 3 堂／魅力＝任何 2 堂／武師班＝任何 3 堂／智商＝任何 4 堂），進度即時計。
  **注意：將來改 maybeUnlockMidCourses 嘅門檻，要同步 ux68UnlockRule。**
- 外貌課學費係 `money:-Math.min(800,S.money)` 寫法，正則攞唔到，parser 特別標記
  `gains.money=[-800,-800]`，指南費用欄顯示「$800」（其餘課程免費）；上一堂一律耗 1 日。
- 每課有「前往」掣：`ux68GoLoc` 行 leaveHomeFromNotebook("map")＋openLoc(地點)，真跳轉
  （實駕證：歌藝指南撳前往 → 香江唱片 sheet 開）。
- 目標數值：每頁有「設為主攻目標」掣，存 prefs `ux68TargetStat`（loadPrefs/setPref），
  **唔入存檔**；未設時全遊戲行為同 v67 一樣。
- 聲望／人氣冇訓練課：指南老實寫明靠接通告累積＋「去大地圖」掣；壓力頁寫明全日休息
  清零規則（v65）＋休息室，前往最近片場。

## 二、地點選項整理（ux68OrganizeLocSheet，openLoc 尾後處理）

- 唔改 openLoc 本體：建完掣、開 sheet 之後行 organizer，將 `#loc-acts` 嘅掣搬入分組。
  出錯有 try/catch 包住，原 sheet 唔受影響。分組冇需要時（單一組＋冇要事＋冇未開放）唔郁原樣。
- **意圖分組**（組內保原序）：接工／訓練／社交・劇情／休息・雜項。分類 `ux68ClassifyAct`
  覆蓋現有全部掣型：播劇情（act-story）、打聽／遠觀（act-ask）、傾談、送禮、只查看通告欄、
  試鏡入口（act-bridge／軟版）、接通告、查看檔期、暫未能報、報名：／進行…訓練、休息室歇陣、
  小賣／禮品；未識別者入休息・雜項兜底，唔會漏項。實駕截圖：星河電視台五組齊全。
- **要事置頂**（「要事」組＋逐項原因 `ux68-why`），訊號全部用既有數據：
  ① 可播劇情掣（act-story 非完成）→「劇情待觸發：《…》」；
  ② 何生人情到期（favorDueDebt：favorState=called 剩 ≤4 日／pending dueDay 剩 ≤3 日）
     → 只喺事務所嘅「還人情 / 送禮」掣升格，原因帶日數；
  ③ 已獲聘拍攝 deadlineDay 剩 ≤3 日 → 「查看檔期」掣；
  ④ 通告季尾落欄：board 通告 season ＝ 而家季節而且季尾剩 ≤10 日（`ux68SeasonEndLeft`
     按 START＋dayIndex 推季尾日期）→「呢張通告今季尾落欄（仲有 N 日）」；
  ⑤ CALIB60_NODE_WINDOWS 節點時窗去到今季尾而且地點吻合（STORY_LOC_SOFT）→ 要事區出
     一行提示（冇掣可升嗰陣都提）。
  實駕證：事務所同時出 ①＋②；星河電視台出 ④。
- **未開放摺疊**：disabled／費用欄（`.cost`）＝「未開放」／已完成劇情（act-story-done）
  收入預設收起嘅「未開放（n）▸」區，撳開先見；掣本身照開到詳情頁睇條件。
  實駕證：低數值秋季存檔金鐘創意出「未開放（1）▸」，展開正常。
  （教訓：add() 模板費用欄 class 係 `.cost` 唔係 `.c`——第一版分類器讀錯 class，
  靠實駕 dump 先捉到；邏輯測試嘅 fake button 已改跟真模板。）
- **目標標示**：設咗目標後，訓練掣（該地點主課增益含目標數值）／休息室歇陣（目標＝壓力）／
  試鏡・接通告掣（目標＝聲望或人氣）加 `▲數值名` 細標（紙底金邊膠囊，跟現有 UI 語言，
  冇用 emoji）。實駕證：目標歌藝 → 香江唱片報名掣有「▲歌藝」。

## 三、大地圖地名：方案 B「墨字標注」（用戶 11:41 最終拍板，取代小木牌 v2–v4）

- `#map-stage` 內加靜態層 `#map-names68`（13 個 `.mn68`），pointer-events:none，
  唔擋 v43 隱形熱區（實駕：真座標 click 命中 pin 開 sheet）。
- 款式照定版樣板 `linji-map-names-sample/index-alt-b.html`：深啡墨字 #43301c、12.5px、
  font-weight 800、字距 .08em、紙色 #f3e7c8 多向光暈 text-shadow；冇牌、冇底框、
  淨地名冇地區行。位置沿 v4 貼建築位逐個抄（left／top 見 index；靜態測試逐個釘死）。
- 驗收（420px 闊真 UI）：stage 384×509 下 13 標籤 bbox **逐對零重疊、冇出界**（自動量度
  PASS）；截圖對圖核實：墨字貼建築邊、冇成行壓住建築主體、可讀（verify68/shot_map_names.png）。
- 地區移入地點 sheet 標題：`loc-title` 改為「名 · 地區」（LOCS.area），desc 行刪走重複
  嘅地區前綴。實駕：🦁 獅子山製片 · 沙田／📺 星河電視台 · 九龍塘／🏢 何生事務所 · 中環 等。

## 四、網頁重量紓緩（盤點＋安全再壓縮）

主檔 **4,852,951 → 4,646,854 bytes（−206,097，−4.2%）**。全檔 data:image 共 69 張、
base64 約 2.92MB（佔 60%）。逐張試壓（PIL 同尺寸再編碼，慳唔到 8% 就保留原圖）：

| 圖 | 尺寸 | 原始（raw） | 結果 |
|---|---|---|---|
| PORTRAITS hero_awi（阿偉主圖） | 864×1152 | 191,434 | **q82 → 74,136（−61%）** 原圖明顯過編碼 |
| UI40_SCENE start_guide | 720×1280 | 201,839 | **q80 → 143,534（−29%）** |
| UI40_SCENE 其餘 5 張（cafe/agency/studio/startv/recording） | 800w | 94,628–158,000 | 保留：q80 再編碼反而大 11%（原圖係更靚 encoder 出品，PIL 追唔上） |
| MAP_IMG 大地圖 | 1080×1432 | 381,956 | 保留：q82 試壓 −0.1%（冇收益＋核心視覺唔冒險） |
| POSTER59 海報 ×10 | 340w WebP | 8,452–44,568 | 保留：v59 已 q60；本身已有 loading="lazy" |
| UI40_STAND 企立 ×10／NPC 頭像 ×7／頒獎 sprite | — | 細 | 保留：已係 WebP 高效編碼／體積細 |

- 再壓兩張已抽出嚟對圖檢查：平塗賽璐璐畫風喺 q80–82 冇可見劣化（線條、色塊乾淨）。
- 延遲載入：海報圖 v59 已有 loading="lazy"；場景／企立／頭像全部係 JS 按需先 assign
  src（唔開嗰版唔解碼），架構上已係懶載，冇再改。
- 載入體感：本地鏡像 loadEvent 中位 v67 524–594ms vs v68 567–590ms（loopback 桌面
  CPU 解析太快，**量唔到可信差異**，唔虛報）；減磅嘅實際得益喺真手機解析 4.6MB
  單檔同網絡傳輸嗰度。網頁版重量嘅根本限制仍然係單檔＋base64 膨脹（約 +33%），
  原生版資產獨立檔先根治——同 v67 NOTES 結論一致。

## 已知事項／跟進

- **台風訓練（train_stage）冇報名入口**：唔喺 TRAIN_BY_TYPE／COURSE_ENROLL_EXTRA／
  解鎖規則任何一處（增益表本身存在，進階台風解鎖又依賴佢堂數）——係 v68 之前已存在
  嘅接線缺口，唔喺本包範圍亂改數值／路徑；指南對佢老實標「未開放——暫未有報名入口」。
  建議另開小包定奪（例如電視台報名附帶開放台風）。
- organizer 每次 openLoc 重行一次（掣係每次新起，冇重複加工問題）；doScout 開通告欄
  嗰條路唔經 organizer（本來就唔係 sheet 選項清單）。
- 驗證證據喺 linji-work68/verify68/（driver68_log.txt＋截圖 9 張）；本地駕駛
  driver68.py（gate-on、槽 3、420px、零 pageerror 全程）。
