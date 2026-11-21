# NOTES v20a372 — 第二輪評估第二波七項

日期：2026-11-22。基線 v371（suite 400 PASS／9 FAIL）。本版 suite：**400 PASS／9 FAIL**（九項 pre-existing：flash51／slot50／soft_tip_111_restore／start53／weave43_static／weave44_static／weave49_static／wf5_87／wrap38），與基線一致。證據：`~/workspace/linji-drive372/`。

## 1. 作品牆海報兌現（實裝）
- GPT-6.2-sol 諮詢（原稿 `gpt_works_prompt.txt`／`gpt_works_reply.txt`）：採納「卡改 button＋詳情剪報 modal＋牆標題加部數」；不採納「作品牆搬上拍攝簿之前／刪已殺青履歷」（menu72 釘住＋既有「分段呈現唔合併」設計）。
- `work59IsNamed` 加 fallback：gig 回查唔到時用 wrapHistory 自帶 `category==="作品"`，令已殺青作品唔會因回查失敗變純文字。
- `workCard59Html` 改 `<button class="work-card59" data-work-gig>`＋「詳情 ›」；海報區沿用 v370 紙底四款 `work-csscard59`；`worksWallHtml59` 標題加「作品牆 · N 部」。
- 新 `openWorkDetail372(gigId)`：剪報式 modal（片名→媒介·年份→阿偉角色→陣容→簡介→日數／片酬／聲望／評價，缺項唔出空欄）；`renderWorksPane` 加點擊委派。
- 實駕驗證：5 張 button 卡、五媒介 css 海報齊、撳卡開詳情正確（`after_works.png`／`after_workdetail.png`）。

## 2. 蘇芷茵線休閒開唔到（實裝）
- 根因：`R_so_meet` 要 phase_P3（1992 年到），休閒 550 日只到 P2；設計 meet 係 1991 春。
- `content/story_detail_romance_yip_so.json`：R_so_meet phase P3→P2、openConditions phase_P3→phase_P2；R_so_push1 P3→P2；R_so_push2 P4→P3；crisis P4／ending P5 不變（鏡像葉線節奏）。index.html gate 變體 `R_so_meet_gate` 同步 phase_P2；`ROM159_WOMEN.so.phase` 3→2。
- tier 閘（配角以上）保留；HE/BE＋排他鎖不變。
- **觀察未改**：徐寶珊 meet 同樣係 P3，報告冇提，本版唔郁，留待拍板。

## 3. 故事跳轉「跳至選項」1/9（前提唔成立，冇改 code）
- 全節點掃描（`probe_skip_sweep.py`，91 個有 beats+choices 節點）：modal 層「跳至選項」掣全部存在、點擊後入 choices 模式，91/91（`skip_sweep.json`）。
- W1 driver 揀咗舞台內 `.sp-skip`（自 v19z24 起 `display:none`，真掣喺 #modal-btns），屬 driver artifact；W1 報告自己亦寫明「未能確認」。故唔改 code。

## 4. 通告欄短卡成功率（實裝）
- `gigBoardTeaserHtml`：ready 卡加 `<div class="gt-chance">試鏡成功率約 <b>X%</b></div>`，用同一支 `chance()`（v368 曲線不變），typeof 守衛＋try/catch；鎖定卡照出差額行。CSS `.gt-chance`。
- 實駕驗證：5 teasers／5 chances，樣本「試鏡成功率約 87%」（`after_board.png`）。

## 5. 脊骨次序倒轉（實裝）
- 根因：「冬」含 1–2 月，N10（1991 冬）／N16（1992 冬）年頭就開，搶先 N7/N9/N13。
- `STORY_GATE_3Y`：N10 加 `weekMin: 100`（1991-12-01＝day699＝week100）、N11 加 `weekMin: 100`、N16 加 `weekMin: 153`（1992-12-01＝day1065）。needDone 不變（N10/N16 刻意無鏈，屬恢復節點）。E1 脊骨讀法甲不變。

## 6. ad/host 供應 2→3（實裝）
- `content/gigs_new.json` 加 4 張（跟現有欄位規格，cast 用已知星 id）：`gig_1991_ad_111`《新春團圓》（廣告主角，春，高級）、`gig_1991_variety_107`《夏日繽紛夜》（主持，夏，高級）、`gig_1992_ad_112`《春風得意》（春，稀有）、`gig_1992_variety_107`《盛夏嘉年華》（夏，高級）。
- 計數：326→330（1990:130／1991:110／1992:90）；ad_lead／variety_host_lead 1991+1992 各 3 張/年（1990 維持 0，屬設計）。贏線 0.875 不變。

## 7. 感情送禮數值（實裝）
數表（感情線 `calcDelta`，週軟頂每人 +3/週）：
| 類別 | 首次 | 重複（floor/2） |
|---|---|---|
| 最愛 | +3（舊 +2） | +1 |
| 喜歡 | +2 | +1 |
| 普通 | +1 | 0 |
| 唔鍾意 | −1 | −1 |
- `calcDelta` 最愛獨立 +3、上限 3；`giveGift` 週軟頂 room 2→3（結構不變，令 +3 真正落到）。
- 星層（rom176StarDelta 最愛 +4／喜歡 +2）不變。

## 測試釘 resync（逐釘驗證內容相同先改）
- 計數：gig229 系列、r286/r299/r302/r304–r337、nat92、sideline158/274/280、p361、awei195、r307、r319、r5_284、press94（330／按年 130·110·90／司儀 9／真男主角 16/年／稀有 23／高級 26／作品 203／cast 258·138·65／named 194）。
- 閘表：gate136、v251_c、gate113_static、weave46、weave48（N10/N11 weekMin 100、N16 weekMin 153）。
- 感情：rom183、rom159_static、tang167（calcDelta 最愛 3）；rom159_yipso_static（so meet P2）。
- 行號：index.html 48212→48288（+76）；gift185／tang171／tang173 ledger＋openLoc DEF 43429→43505；rom159 六釘＋全佳行 26308；rom176 六釘；tang152 兩釘；travel114 COUNT/FREE/DEF/WRAPPER difflib 映射（`resync372_travel114.py`，內容逐字核實）；text125 三釘；tang173 L5109 註解平衡釘。
- suite 跑完已 `git checkout -- qa296/derive296.json` 還原。
