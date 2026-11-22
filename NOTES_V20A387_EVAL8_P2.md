# v387 第八輪評估 P2 收尾（2026-11-22）

對象：live v386（main `bdeb16a`）。第八輪報告 `~/workspace/linji-playtest-eval8-2026-11-22/REPORT.md` 共 12 項 P2（報告正文編號 1–12；簡報寫 11 項，第 10 項係觀察）。逐項對 live code 核實後處理如下。

## 已實裝（7 項）

1. **W2 P2-2 手帳子 tab 闊 30px**：根因——非 plan 組規則（`#home-subtabs .hsub-group:not([data-hsubgroup="plan"]) .home-tab`）寫死 `min-width:0`，蓋走 v373 嘅 44px；後置規則只補返 `min-height` 冇補闊。修法：`#home-subtabs .home-tab` 同 `#v-home .home-subtabs .home-tab` 兩處加 `min-width:44px !important`。紅圈視覺不變（GPT 規格：觸控區 44、視覺元素原比例）。
2. **W2 P2-3 人脈頁「去…行下」掣高 36px**：`.people-go` `min-height:36px→44px`＋inline-flex 置中。
3. **W2 P2-7 個別掣 38–39px**：晨報「第二版 →」（`.np214-switch`）、典禮「跳過 ⏩」（`.awd62-skip`）、地點面板「未達標／長遠目標」摺疊 summary（`.gig-locked108 summary` 改 flex＋min-height 44）、開始畫面「讀檔」mini 掣（`#btn-load-mini` 30→44）全部補到 44px。
4. **W2 P2-6 頒獎舞台只佔上半屏**：GPT 方案 C——frame 排版闊不變（96vw、頂釘死防跳位照舊），窄屏（≤480px）`transform:scale(1.06)` 視覺放大（origin 頂置中，beat 變高唔跳位）；舞台加 `overflow-x:hidden` 防放大出界；下半暗場加腳燈暖光漸層（第二層 radial），唔再死黑。
5. **W3 P2-1 壓力峰值預覽低估**：`stressDeltaForAct` 拍攝日預覽 +10→+12（實際 `shootDailyDelta` 係 8+R(2,6)＝10–14、平均 12）。低入口（10）＋5 日連拍預覽峰值由 60→76，觸發兩日休息門檻。只校準預覽口徑，唔改實際入水、唔改休息門檻（≥60 兩日／≥80 三日）。
6. **W4 P2-11 wrapHistory 封頂 90 vs careerStats95.total 110**：寫入點上限 90→240，同全史計數器口徑對齊（90 只冚一年，v147 校準；三年全弧實測 110 部，240 冚得晒單年上限 79×3≈237）。v147 讀取審計結論：窗口大咗只會更準，日期過濾嘅讀取不受影響。舊檔已截斷嘅歷史救唔返（同 v147 交代一致）。
7. **W4 P2-12 1992 電影／電視男主角只提名無差額提示**：核實後確認**機制已存在**——`buildAwardResultPack` 對所有 nominated 格（唔分媒介）都寫 `weakHint62 = awards62WeakHint + awards379GapBand`，結果報紙以 `.psr-weak62` 呈現，同 v379 音樂獎同口徑。實駕探針（`__awards.build` 電影典禮 nominee）證實「最佳男主角」nominated 格帶完整差額提示。唔使改 code；W4 觀察應係未開結果報紙嗰頁。

## 核實後不改（5 項，設計確認）

- **W2 P2-1 開始畫面立繪右緣出血 10px**：`right:-10px` 係 v52 全出血構圖有意設計，document 無橫捲。保留。
- **W2 P2-4 地點面板長通告名省略號截斷**：有意設計（詳情頁睇全名）。保留。
- **W2 P2-5 地圖容器 4px 亞像素溢出**：邊框／陰影亞像素，無橫捲無視覺出界，報告本身講唔使修。保留。
- **W3 P2-2 累積超額接單致 2 次取消**：B11 檔期風險提示＋B8 限期告急都有出聲，遊戲只提示唔硬擋——設計確認：接唔接由玩家決定，警告文案已寫明後果（逾期取消＋違約金＋聲望）。唔改。
- **W3 觀察 planner 入口 S.weekPlan 舊值**：探針 artifact，DOM／confirmed 正確。唔改。

## 唔郁

SAVE key／softRev／產品 `?v=`／贏線 0.875／floor 140／warnLine 180／E1 門檻 350／試鏡判定／頒獎計分／結局判定／實際壓力入水全部不變。

## 測試

- 新邏輯測試 `tests/test_eval8_387_logic.js` 全 PASS（峰值預覽、cap 240、六處 44px、舞台 scale、GapBand 三段＋WeakHint 接線）。
- Suite：第一跑 393/21，12 項新 FAIL 全部 resync（`qa387/resync387.py`，difflib 單次掃描；內容釘三處跟意圖更新：fix65 拍攝預覽 12、cap 240×2、buttons197 summary flex）。第二跑 **405 PASS／9 FAIL**（基線 404＋新測試 1，九項 pre-existing 不變）。
- Playwright 實駕（`~/workspace/linji-drive387/probe387.py`／`probe387b.py`）：六處觸控 min-height/min-width 實測 44px、舞台 transform matrix(1.06)＋overflow-x hidden、電影男主角 nominated 格 weakHint62 完整、零 page error。
- GPT-6.2-sol UI 規格原稿：`~/workspace/linji-drive387/gpt_ui387.txt`（brief 寫明終極目標原生 iOS app）。
