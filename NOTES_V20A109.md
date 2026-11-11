# NOTES_V20A109 — 角色身高比＋舊 bust 換新（統籌總交代）

- main：`bea5272`（A `a490934`＋B `0bb85b2`＋NOTES `c7f8832`＋實駕證據 `bea5272`）；線上 index.html 5,075,443 bytes、sha256 `758fb7a390a95eb9194ae71dadc0720304a33eaf082a46056e9950cf0d9ad2ab`，同本地逐 byte 一致。
- 來源：用戶 2026-11-12 06:39 兩則實機反饋——①彭少祺應該較矮，對話舞台將每人縮放到同一高度（60%），身高差唔見晒 ②人情頁見到嘅舊 bust（林曉晴／張子駿／Vera／高俊傑／周采兒）係 v106 之前嘅舊圖。
- 唔改 SAVE key／softRev／`?v=`。基線 142 PASS／12 FAIL（12 個 static 檔係環境性 FAIL）。

## A 線：對話舞台 per-character 身高比（`DLG109_HEIGHT_SCALE`，阿偉＝1.00）
- 實作：渲染高＝DLG108 fitted 基礎高 × 身高比，`dlg108FitApply` 逐張落 inline height；腳底 `bottom:10%` 唔郁，遮腿不變；CSS 一字唔郁。
- 身高表實數（覆蓋 `DLG106_GAZE` 全部 34 個 id，數值 0.80–1.10）：
  - 矮 0.85：`pang_siuki` — brief「身型偏胖但靈活、面型圓潤」＋矮個司儀靈感對照；全身圖 AR 0.376，比阿偉 0.343 闊 9%。
  - 高 1.05：`gu_mingfai`、`ching_tinlok` — AR 全庫最瘦兩名（0.232／0.267），圖中腿長身窄＋brief 修長線索。
  - 中 1.00：其餘 31 個 id（含 `awi`／`awi_s2`／`awi_s3`；brief 無身高線索者一律唔估，唔准逐個估 cm）。
- 量度表（實駕 390×844）：阿偉×彭少祺 506.4／506.4 → 506.4／**430.4px**，彭生頭頂低 **76.0px**，淨空 13.6 → 39.1px；阿偉×顧明輝高 25.3px，淨空 83.4 → 77.5px；C1 阿偉×何生、阿偉×鍾楚凝不變；最闊配對方小龍＋Vera fitted 55.4% 自動收細照觸發（只有計數值，兩人唔係可觸發巧遇嘅星，冇可玩配對）。
- 對照：`qa109a/shots/pre_enc_pang.png` → `post_enc_pang.png`（同一句「哎，收工啦收工啦，各位辛苦晒，聽日準時呀！」）；顧明輝／鍾楚凝／C1 對照同目錄。
- 詳見 `NOTES_V20A109_HEIGHT.md`。分支 `v109-height`（`a3e2ca8`）。

## B 線：舊 bust 換新（列表縮圖）
- 消費者審計（grep 實證）：PORTRAITS 7 鍵——手帳頁頭阿偉像（`enterHome`）、傾談 modal `.dlg-portrait`、人情頁 `.people-row`（40×52px）、開局 `#start-hero`（hidden）、開局導入後備（恆不觸發）、舊 story-play bust 後備鏈尾；`n.face` 6 個（林曉晴／張子駿／Vera／高俊傑／周采兒／何生）全部有鍵零缺圖；人情頁紅星段 12 星原本行舊 era_stars 企立圖（864×1152），今包 `BUST109_EXTRA` 首選、舊圖退做 `onerror` 後備；未見紅星維持剪影（刻意「未揭面」）。
- 技術取捨：**繼續內嵌 base64，唔行資產路徑**——(1) 後備鏈語義視 `data:` URI 為必定存在、優先回傳，資產路徑會跌落一串可能 404 嘅舊 bust 檔後面；(2) 人情頁／傾談／頁頭係最高頻畫面，內嵌零 fetch、零 404、離線都得；(3) 體積唔係問題——21 張新圖 b64 共 280,192 字元，只比舊 7 張多 44,599 字元，`index.html` +0.95%（5,023,304→5,070,946 bytes；合併 A 線後 5,075,443 bytes）。
- 新縮圖清單（21 張，全部由 `assets/story/fullbody/*_base.webp` 裁出，240×312 WebP q80，米白底 `#F2EBD8`）：PORTRAITS 7 鍵沿用（hero_awi←阿偉 s1、npc_lin、npc_cheung、npc_vera、npc_ko、npc_chow、npc_ho）；新增 `BUST109_EXTRA` 14 鍵（`awi_s2`、`awi_s3`＋12 紅星）。裁切幾何：`Hc=0.30×fig_h`、`Wc=Hc×10/13`、頭帶 centroid 置中、頂部唔裁；0.28／0.32／0.36 對照後選 0.30；21 張逐張目檢 PASS。
- 阿偉 tier：跟 `dlg106AweiStem()` 同一規則——tier 0／1→s1、2→s2、3→s3（`bust109HeroSrc()`，讀唔到 tier／缺圖退 s1）；開局 `#start-hero` 留 s1（boot 時 tier 必然係 0）。
- UI40_STAND 10 張舊企立 WebP：**仲用緊，但今包唔掂**——只喺深層後備鏈／開局畫面 `#start-standee`（可見舊圖）出現；換開局企立要成張全身圖唔係頭肩裁圖，留畀統籌開包。守門測試釘死 10 鍵原封不動。
- 詳見 `NOTES_V20A109_BUST.md`。分支 `v109-bust`（`d2f59f4`＋清理 `b3bfab9`）。

## 合併後驗收（合併版 HEAD `0bb85b2`）
- 全套測試：**146 PASS／12 FAIL**，FAIL 清單同基線逐字相同，零新增回歸（＋4＝四隻新測試檔：`test_dlg109_height_logic/static`、`test_bust109_logic/static`）。附帶修咗 `test_ux68_static.py` 一處（JPEG-only regex 抽唔到新 WebP hero；改收 jpeg|webp，上限 100,000 不變，新 hero 8,016 bytes；pristine 仍 PASS，冇放寬）。
- 合併版實駕（`qa109/`）：B 線 `drive109.py` 10/10（人情頁 18 行全 WebP 240×312，未見蘇芷茵維持剪影；hero 三級 sha match；舊檔相容原樣還原；0 pageerror）；A 線 `drive109a.py` 數值同 post 分支逐項相同（彭生 topDiff 76.0、顧生 −25.3、C1 不變；0 pageerror）；額外合併檢查 `drive_merge109.py` 10/10——同一 save 先後行 B 再入 A，hero tier 2（s2 灰西裝）頁頭＋C1 對話同框一致，阿偉 s2 渲染高 487.2、inlineH 60%、ratio 1.000，B 線 tier 切換零干擾 A 線身高比。
- 截圖：`qa109/shots/merge_people_full.png`＋分段 seg1–3、彭少祺 `merged_enc_pang.png`、hero tier 2 `merge_hero_t2.png`、同框 `merge_c1_awixho_t2.png`。
- `node --check`：index.html 兩個 script 塊抽出驗 PASS。

## 殘留缺口（留待跟進）
- `ho_sang_angry.webp`／`.png` 缺檔（舊問題，唔係 109 引起）：庫內何生得 base／sad／serious／smile／think，欠 angry；對白 loader 先試 `.webp` 再試 `.png`，兩個都 404 先退回；pre／post／merged 三跑同數 8 個。留待另開表情細包補。
- 開局 `#start-standee` 舊企立＋UI40_STAND 其餘 9 張未換（見 B 線）；換開局企立要成張全身圖，另開一票。
- WF4 舞台未套 DLG108／DLG109（D-8 二期範圍外）；方小龍＋Vera 身高配對只有計數值，冇可玩實駕值。
- 駕駛腳本次序敏感：`enc79PlayEncounter` 等函數唔係全域，要用玩法入場逐日重骰；顧明輝要排第一個（day 0 即撞），排最後 18 日都撞唔到，原因未深究——`qa109a/drive109a.py` 現行顧→彭→鍾次序穩定，唔好亂調。
