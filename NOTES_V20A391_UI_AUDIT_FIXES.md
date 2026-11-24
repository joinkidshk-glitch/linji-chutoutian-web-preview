# NOTES_V20A391_UI_AUDIT_FIXES.md

v391：第二輪全畫面 UI 再檢視（2026-11-24，`~/workspace/linji-ui-audit-2026-11-24/REPORT.md`，GPT B68／C3、Gemini B53／C18，冇一屏 A）頭五項必修實裝。用戶 2026-11-24 14:04 批准開工。只改呈現層 CSS，數值／邏輯／文案零改動。

## 1. 確認 modal 可讀性＋深色 modal token 統一（雙 C）
- 修法：reconfirm 喺 story-play 入面改置中米紙卡（底 #F2EBD8）。
- 實測（`~/workspace/linji-drive391/verify/measurements.json`）：標題對比 1.18:1 → **15.33:1**；內文 1.52:1 → **11.07:1**；選單維持 10.19:1。
- ⚠️「確定」掣唔郁：實色金漸變底配深棕字，經 Gemini 專項＋裁切放大圖雙重證實無問題；量度嘅 1.15:1 係未合成透明底數值，唔好誤修。新測試有守門（確定掣背景規則仲喺度）。

## 2. 地圖標籤層（專項 C，主畫面核心）
- 修法：deCollide 改方向精確推距（向上 D=標籤底−障礙頂+8，向下 D=障礙底−標籤頂+8，揀細嗰邊＋越界否決）；障礙物改 marker＋「我喺呢度」tag 聯集；pair pass 推上面嗰個上去避開標記區；定型後三輪覆核（400／800／1200ms）；屋企唔出 tag；當前地金底＋有提示淺金＋閒置淡化；手帳拉柄改 in-flow。
- 實測：標籤互撞 **0**、minGap **8px**；玩家標記重疊 0（屋企＋電視台，修前撞 219px²／15.8%）；手帳掣 844／682 高都喺畫面入面（修前 682 高遮灣仔唱片 59.3%）；約會層 minGap 18.9px。

## 3. 稱號段跌出紙面（GPT C，v389 摺疊新斷裂）
- 修法：包入米紙卡、刪重複標頭、「當紅小生阿偉」朱紅印章、獎／擔正／主線對齊短列。
- 實測：內文對比 **11.48:1**；印章 #9E2F2F 對比 **5.74:1**；稱號段喺紙卡入面（x10／w370／bottom 882.7）。

## 4. 劇情對話層疊漏＋「下一句」防呆（23 Gemini C／23b B）
- 修法：tut-on 漸變＋78dvh 封頂唔再壓贏 story-play（全屏、底 #0a0705、頁眉零漏入）；「下一句」改 static 底欄，三粒掣同一 y、右邊距 16px；闊字體重測一樣。
- 實測：homeTop 不可見（w/h 0）；三掣同一 y=792，右邊距 **16px**（修前僅 12px、唔對齊），全部 44px 高；「下一句」right=374／viewport 390。

## 5. 彈窗清單去網頁化（先修 08b 地點面板＋35 頒獎禮系列）
- 修法：返回地圖改頁角吊牌、標題單行、在場文字唔撞立繪；請柬票根＋結果卡報紙式，掣改啞面紙籤。
- 實測：休息列完整可見（5 列都 fit，restVsCloseOv 0、restBottom 距 sheet 底 82.3px）；結果卡全部對比 ≥11.49:1。

## 測試
- Suite：`bash qa131/run_suite.sh <work391> ~/workspace/suite391_out.txt` → **TOTAL PASS 407 FAIL 9**；9 FAIL 全部係已知 pre-existing（flash51／slot50／soft_tip_111_restore／start53／weave43_static／weave44_static／weave49_static／wf5_87／wrap38），新 FAIL 0。
- 新增 `tests/test_v391_ui_static.py`（28 項靜態守門：五項關鍵標記在位＋對比度守門＋「確定」金掣未被改），獨立跑 PASS。
- Resync：8 項漂移全部係行號釘（travel114／rom159／rom176／tang152／tang171／tang173／text125／gift185），difflib 映射零移除、內容逐字核實；另補 rom159 漏咗嘅「全佳」釘 26982→27225。`qa391/resync391.py`。
- 實駕：`~/workspace/linji-drive391/`（drive391.py verify 1 2 3 5 4 全套 pass，verify13；截圖＋measurements.json 喺 verify/）。
- 跑完 suite 已還原 `qa296/derive296.json`。

## 出貨
- SAVE key／softRev／產品 `?v=` 不變。index.html 淨 +243 行（v391 區塊只含 CSS，無 JS 邏輯改動混入）。
