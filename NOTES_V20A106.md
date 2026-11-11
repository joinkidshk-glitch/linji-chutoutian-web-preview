# v20a106 對話呈現包：雙人全身企立＋表情＋視線（D-8 第二階段主體）

底本：用戶 2026-11-11 拍板嘅對話呈現規格（雙角色全身企立一左一右企喺場景圖前、下方對話框、講者全光／聽者變暗交替）＋全量全身圖重生批次（31 角＋芬姐＋阿偉三階段）。
紀律：SAVE key `starVolunteer_map_v19w`／softRev `s107`／產品 `?v=` `v20a10` 全冇郁（新資產用自己版本參數 `?v=20a106`）；content JSON 一律唔改，正規化只喺呈現層做。

## 逐項處置

- **雙人全身呈現規格（DLG106，主線劇情＋巧遇兩路接入）**：舞台 390×844 直向、場景圖底＋雙人全身企立（人物高＝舞台 50%）＋下方對話框；講者 brightness(1)、聽者 0.6、filter 過渡 250ms；旁白句兩人齊 0.6＋冇名牌；電話聲句兩人齊 0.8＋藍灰電話名牌（虛線框）。冇全身資產／雙表外 speaker 行返舊呈現（候補鏈：目標表情圖→同角 base 圖→舊 bust/剪影，載入失敗自動行後備鏈 `__dlg106Err`）。阿偉按成長級數（enc79PlayerTier）轉圖組 awi／awi_s2／awi_s3。呈現函數：主線 `spDlgCharsHtml`（dialogue／narration／phone 三態）、巧遇 `paintDlg106`。
- **表情解析次序＋覆蓋數字（工人 C 數據＋工人 B 接線）**：次序拍板＝beat 既有 emotion/expression 欄（舊詞彙正規化：worried→think、frown→serious 等）→ DLG106_EMOTION_MAP 查表（584 條，hash 查表，同 C 交付 `handoff106/emotion_map_embed.json` 逐條一致）→ 分類器（C classifier_runtime.js 原樣搬入）→ neutral。category→expr 八項：happy→smile、neutral→base、serious→serious、sad→sad、surprise→surprise、shy→shy、think→think、angry→angry。覆蓋（C 報告口徑，2,644 句對白）：名冊 32 角非 neutral 593 句，資產精確覆蓋 **403/593＝68.0%**，其餘按候補鏈退 base／相近款；阿偉 s1 精確覆蓋 184/188＝97.9%。JS 交叉驗證：hash 同 Python 生成器 2,644 句 100% 一致、lookup 還原 620 句非 neutral 分類 100%。
- **視線表 34 條＋企位原則（工人 C 實測表）**：DLG106_GAZE 內嵌全表（31 角＋extra_ad_fen＋awi_s2／awi_s3），分布 front 24／left 6／right 4、flipSafe=true 11 條；完整版喺 `handoff106/gaze_table.json`（同內嵌版逐條一致，測試守門）＋已內嵌 index.html DLG106_GAZE。企位原則：唔翻得嘅角優先按原生視線就位（望左→企右位面向對手、望右→企左位），翻得嘅角（包括阿偉）翻轉遷就，務求兩人互望；何生望左＋唔翻得、駱家聲望左＋唔翻得（以新全身圖實測為準，唔跟舊 bust 翻轉先例）、阿偉望右＋翻得。單角出場（同角／一邊表外）行獨角呈現，雙表外行舊呈現。
- **髮長修正 7 張（工人 A，像素級剪影手術，零生成重擲、面部逐像素 diff＝0）**：藍若曦 lan_ruoxi base/smile/sad 頭髮過膝→及腰（髮尾約 0.36H）；蘇芷茵 so_jiyan base/serious/sad/shy 頭髮近腳踝→腰／臀位（約 0.445H）。
- **改色 5 張（工人 A，HSV 色相旋轉，alpha 同面部鎖定）**：陸柏言 luk_baakyin base/serious 深藍西裝→深酒紅西裝；麥震東 mak_zhendong base/serious/sad 深藍恤衫→橄欖軍綠＋工作褲→深灰卡其去藍調。
- **焗邊 88 張（工人 A）**：米白光邊 RGB(243,233,210) 焗入圖本身（跟人物一齊變暗），剪影 alpha>128＋填洞、圓盤膨脹邊帶、高斯柔化，半徑按顯示高 422px 約 3 CSS px 換算（逐張 r 10–20）；全 88 張驗證 PASS（尺寸＝原圖+2r、邊帶命中 100%、內部大差異 ≤0.06%）。入庫 `assets/story/fullbody/`，清單見 `handoff106/assets_report.md`。
- **lin_hiu 碎片處理（工人 D 步驟一，已清理＋重焗）**：連通體分析確認 lin_hiu_sad／lin_hiu_shy 原批成品各有一粒獨立碎片（>50 連通體 119px／122px，bbox x65–88/y2315–2323 同 x66–89/y2309–2318，同主體剪影最短距離 4.12px，顏色＝腳下地面陰影色，係陰影尖端斷開嘅一小片，唔係身體部分）——alpha 清零後按 A 參數重焗（r=17）。驗證：邊帶外框像素數 7045／7305 同 A 原版 bake 紀錄完全相同、米白命中 100%、剪影深層核心（約 107 萬 px）大差異 0.0%、新版連通體剩 1（主體）。證據：`qa106/cleanup/`（CLEANUP_LOG.md＋分析／驗證 JSON＋diff 圖）。附帶觀察：sad 陰影區另有一粒 9px 細 speck，唔喺今期範圍冇掂。

## 測試證據
- 新增守門：`tests/test_dlg106_logic.js`（視線表逐條對 handoff、企位解析＋整爛視線表反證、解析次序欄→map→分類器、刪 map 條目反證、候補鏈＋阿偉階段、覆蓋統計）＋`tests/test_dlg106_static.py`（基線字串、接線、內嵌表同 C 交付逐條對照、資產存在）——全 PASS。
- 舊測試按新規格更新（檔案內註明）：`test_map54_static.py`「last skin」斷言——DLG106 皮膚段合法追加後 v54 完結標記被推出舊 2500 字尾窗，改驗「v54 後只有已知後繼段（v20a76＋v20a106）先到 </style>」；反證齊（基線 index 跑更新後測試 FAIL、塞未知皮膚段 FAIL），v54 本體內容檢查全冇改。
- 全套 A/B：work106 **134 PASS／12 FAIL**，pristine 基線（linji-repo main）**132 PASS／12 FAIL**，FAIL 清單逐字相同（12 個全屬已知環境性 static FAIL），**零新增 FAIL**；差額 +2 PASS 就係新增 dlg106 兩檔。證據：`qa106/suite_work106.txt`／`qa106/suite_baseline.txt`。
- 主 script 抽出 `node --check` OK；git diff grep 存證：SAVE key／softRev／產品 ?v= 冇刪除或改動行（只有 DLG106 註解提及）。

## 實駕證據索引（合併後線上鏡像實駕，工人 D）
- 主線 C1：`qa106/shots/c1_speaker.png`（講者句全身雙人＋表情）、`qa106/shots/c1_narration.png`（旁白句兩人齊暗＋冇名牌）、`qa106/shots/c1_phone.png`（電話聲句 0.8＋藍灰電話牌）。
- 巧遇表情切換：`qa106/shots/enc_expr_a.png`／`qa106/shots/enc_expr_b.png`（同角前後兩句唔同表情＋明暗交替）。
- 舊檔相容：存檔→重載→狀態還原（見 qa106 駕駛紀錄）。

## 未達標位（老實申報）
- **阿偉 s2／s3 表情缺口**：s2/s3 只有 base/smile/serious 三款，非 neutral 精確覆蓋得 60/188＝31.9%；think（63 句，阿偉最大類別）／surprise／sad／shy 喺主角／天王期一律退 base。要補圖以 think 優先。
- **so_jiyan happy 冇 smile 圖**：蘇芷茵非 neutral 比例全場最高（42.6%），最大類別 happy 12 句冇專屬圖（得 shy 圖近似頂），屬單角單類別最大缺口。
- **隨機事件 WF4 未套新呈現**：D-8 第二階段未及——WF4 隨機事件對話維持 v105 第一階段（場景底＋舊呈現），留下一包。
- **零精確覆蓋 9 角屬資產缺口**：cheung_tsijun、fong_siulung、gao_wenhan、tang_laiping、extra_ad_fen、uncle_kim、kwan_hoimei、cheng_william、mok_siufai——有非 neutral 對白但嗰啲類別冇表情圖，runtime 退 base（逐角原因見 C 覆蓋報告；extra_ad_fen 嘅「sad」9 句經查係旁白假陽性，唔使補圖）。
- 名冊外功能 NPC（generic_*／extra_* 等 10 個 speaker）冇全身資產，行舊呈現，屬規格內豁免。

## 部署核實＋實駕結果
（合併後補記，見跟進 commit。）
