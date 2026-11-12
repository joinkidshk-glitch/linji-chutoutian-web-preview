# NOTES_V20A118 — 地點面板重設計 Phase 2（全量 15 地點）

- 分支：`v118-locpanel`（基底 main `999c719`＝v110 已合併；途中由 `aeec7a5` rebase 上 `999c719`，乾淨無衝突）
- 性質：純呈現層。選項行為／數值／額度計數（v114：每日 2 次、每次入場都計、劇情地點都計）零改動；唔改 SAVE key／softRev／產品 `?v=`；唔直改 content pack JSON。
- 用戶拍板：2026-11-12 08:26「樣本 OK，開 Phase 2」；08:29 追加：廟街禮品＋仁康醫院場景圖會生成，齊就直接接入。

## 改咗咩

### index.html（＋233／−2 行，對 main `999c719`）
- `#loc-sheet` 加三元素：`#loc-quota118`（額度 pill）、`#loc-owner118`（負責人企位＋名牌 `#loc-owner-tag118`／圖 `#loc-owner-img118`）、`#loc-tagrow118`（無圖名牌列）。三者全部喺 `#loc-acts` 外面（ux68 重排唔掂佢哋）。
- CSS（v118 block）：banner 加高至 210px（矮屏 150/120px）；pill 絕對定位疊 banner 左上（兩粒點＋「今日出行：已用 N / 2 · 仲可以去 N 個地方」＋扣數嗰陣先出「✓ 已到埗，扣咗 1 次出行額度」）；負責人 `absolute right:8px width:120px`，腳部收 8px 入選項卡（遮腿，沿用對話舞台做法）；`#loc-acts` 變米紙卡實底；`.act-ic118`（26px，內圖 24px）＋`.act-txt118`。
- JS（`applyLocSheetBg` 之後）：
  - `locpanel118OwnerFor(locId)`：agency_ho 經 `gigIssuerFigure30v2` fallback 攞何生圖；11 間讀 `GIG_ISSUER_FIGURE_MAP30V2`（唔 hardcode 路徑，v116 換入後自動跟 v2/v2b）；cafe_cha → 霞姐名牌（無圖）；gift_shop → 老闆娘名牌（無圖）；hospital → null；未知 → null。**唔用何生頂替任何地點負責人。**
  - `locpanel118QuotaHtml`／`locpanel118ActIcon`（按掣類／標題揀 v112 手繪圖標，揀唔到回空字串，唔用 emoji）／`locpanel118Render`／`locpanel118AnchorOwner`（rAF＋resize）／`locpanel118Hide`（`closeSheet` 內呼叫）。
  - `locpanel118SpentVisit`（transient，唔入 save）＋`locpanel118ArrivedNow`：巧遇／WF4 攔截後嘅免費返嚟、同 modal 完嘅免費重開，pill 同扣數嗰次入場一模一樣。
  - `openLoc` 接線：額度閘之後、enc79 攔截之前計 `spent118`；`add()` 掣加圖標＋`act-txt118`；尾段 `ux68OrganizeLocSheet(L)` 之後呼叫 `locpanel118Render(L, spent118)`；render 包 try/catch。
- 場景圖接入（補充任務）：`~/workspace/linji-locpanel/scene_new/` 兩張齊晒，已驗圖（無字、無真人樣）——`assets/story/locs/bg_loc_gift_shop.jpg`（廟街夜市，720×1280，388,328 bytes，sha256 `022d39114c11…`）、`assets/story/locs/bg_loc_hospital.jpg`（醫院主樓＋落客亭，720×1280，255,879 bytes，sha256 `77d0837447fc…`）；`LOC_SHEET_BG` 加兩項（`?v=20a104` 照舊）；`MANIFEST.md` 加兩行。**15 地點場景圖齊晒，`locpanel118-nobg` 素底態留返做後備機制。**

### 實駕捉到、即場修好嘅兩個呈現 bug（唔係原計劃內）
1. **author `display` 蓋過 `[hidden]`**：三個新元素嘅 CSS 都有 author `display:flex`，蓋過 UA `[hidden]{display:none}`——hidden 咗都照顯示。無負責人地點（醫院／茶餐廳／禮品檔）喺入過有負責人地點之後，banner 右上會出破圖 icon＋殘留 alt 字「何生」（圖已 `removeAttribute("src")`，但 alt 仲喺度）。修法：CSS 加 `[hidden]` 明寫覆寫（`display:none !important`，三元素）；JS 清 src 嗰陣一併清 `alt=""`（render 兩分支＋`locpanel118Hide`）；`locpanel118Render`／`Hide` 收起嗰陣一併清走殘留名牌文字／圖 src／pill 內容（之前 hidden 元素留住上一地點舊文字）。靜態守門加咗對應斷言（見下）。
2. **實駕腳本可見判斷**：`offsetParent !== null` 對 `position:fixed` 容器（`#enc79-overlay` 巧遇全屏）入面嘅掣永遠係 null，誤判唔可見。改用 `getBoundingClientRect`＋computed display／visibility（只改 `drive_locpanel118.py`，唔入 repo）。

## 6 點未決 — 用咗邊個預設
1. 11 間機構老闆：老闆圖企側邊＋名牌「名 · 機構＋職位」（例「沈卓衡 · 星河電視台台長」），文案唔寫「佢今日喺度」／唔寫駐場。
2. 霞姐：唔補圖。茶餐廳只出名牌「霞姐 · 金龍茶餐廳老闆娘」，唔出人；名牌單獨出現無穿崩（實駕截圖確認）。
3. 禮品檔＋醫院場景圖：**已由 08:29 拍板取代——兩張圖已齊，直接接入，唔用素底**。
4. `cafe_cha`：**唔加 `residentNpc`**（唔改 LOCS 數據）。
5. 額度 pill：樣本嗰套文案；用盡態唔使處理（閘口擋咗，面板唔會出現）。
6. boss 圖版本：跟對照表行，現行路徑不變（v116 換入後面板自動跟 v2/v2b 新檔；邏輯測試讀真 map 證明跟表，實駕截圖目視確認 11 張老闆圖＋何生）。

## 測試
- 新守門（全部 PASS；pristine main 跑新測試 FAIL，反證成立）：
  - `tests/test_locpanel118_static.py`：紀律（SAVE／softRev／?v=）、HTML 元素、15 地點負責人覆蓋、唔 hardcode boss 路徑、唔用何生頂替、pill 文案逐字、接線、圖標＋圖檔實存、場景圖 15/15、390px 尺寸上限、v114 零改動、**[hidden] 覆寫斷言（新增，捉上面 bug 1）**。
  - `tests/test_locpanel118_logic.js`（node 沙箱，讀真 map／真函數）：quota 數字／點數／已到埗行、`locpanel118ArrivedNow` 探訪記憶、15 地點負責人對照（11 老闆圖源逐字等於對照表）、16 個圖標案例＋揀唔到回空字串＋無 emoji 殘留。
- 因 v118 改動而要修嘅現成測試（全部再 PASS，唔係放寬）：`test_scene104_static.py`（LOC_SHEET_BG 13→15）、`test_enc105_logic.js`（計數 13→15＋hospital 有逐地點檔）、`test_weave47_logic.js`（沙箱加 `locpanel118ActIcon`）、`test_travel114_static.py`（行號漂移，`resync_travel114.py` 順序對齊 44 行 `openLoc(` 呼叫點，逐行內容逐字相同，確認純漂移；rebase 上 v110 後＋[hidden] 修復後各再對齊一次：COUNT 13 處／FREE 27 處／DEF_LINE 52457／WRAPPER_LINE 43311）。
- 全套回歸：新 main `999c719`（v110）基線 **158 PASS／12 FAIL**；工作版 **160 PASS／12 FAIL**（＋2 新守門檔），FAIL 清單逐字一致（flash51、giglib36、pacing35、poster59、rumor49、slot50、soft_tip_111_restore、start53、weave43、weave44、weave49、wrap38）。零回歸。

## 實駕（390×844，`?softPreview=1`，Playwright）
- 工作版全量 15 地點：**15/15 PASS，0 pageerror**。每間 pill「已用 1 / 2 · 仲可以去 1 個地方」＋「✓ 已到埗」，負責人啱（11 老闆＋何生＋霞姐／老闆娘名牌＋醫院無人），背景圖 15/15（禮品檔／醫院係新接入嗰兩張），幾何檢查零警告（唔出界、負責人腳收埋、pill 唔俾人物遮）。
- 重入計數：film_lion 連入兩次，pill 1→0（已用 1/2 → 已用 2/2）。免費返嚟：cafe_cha 打聽 modal 後重開，pill 完全唔變（已用 1/2）。
- A/B 對照（新 main `999c719` 同流程跑）：15/15 開到，選項逐項對——8 間逐字相同，其餘 7 間除咗 NPC 在場隨機掣（傾談／送禮，隨當日派位出沒）之外全部相同；v118 冇加減過任何選項。main 版禮品檔／醫院 bg=False（預期，未有圖）、pill／負責人梗係冇。
- 截圖（工作版最終跑）：`/tmp/drive118_work_final/`——agency_ho、cafe_cha、tvb_longmen、gift_shop、hospital 五張＋`results.json`（逐項 capture）。修正後複檢：`/tmp/drive118_fixcheck/`（醫院／茶餐廳 banner 右上乾淨晒）。
- 實駕腳本（唔入 repo）：`~/workspace/linji-work118/drive_locpanel118.py`。途中修好三個腳本問題：開局兩層 modal 鏈（教學 → intro，次序唔可以調轉）、WF4 事件「繼續」掣、巧遇全屏 overlay（`.e79-btn`／`.e79-skip`，加 `offsetParent` 誤判修復見上）。
- 途中撞到嘅非 v118 問題：廖炳星欠 `shy` 表情圖（`liu_bingxing_shy.webp/png` 兩次 console 404，fallback 正常行；v114 殘留，補圖另開一票）。
- 註：灰色「暫未能報」行無圖標（唔可撳，唔係可撳選項；可撳選項全部有 v112 圖標，`locpanel118ActIcon` 揀唔到回空字串係既定設計）。

## 殘留缺口
- 探訪記憶（`locpanel118SpentVisit`）罕見邊緣情況：早一日已付費入過某地點，之後同日經系統傳送（travelFree）去返同一地點，pill 會照出「已到埗」行（數字啱，行字輕微超前）。罕見，接受。
- 11 張老闆圖係 v2/v2b 新檔：邏輯測試讀真 map 證明跟表，實駕截圖目視確認。
- `/tmp` 滿咗（512M tmpfs 得約 105M 空）：新 main worktree 改放 `~/workspace/linji-main110wt`；舊 `/tmp/linji-main116`（aeec7a5）＋drive 輸出未清，遲啲要執。
- 實駕腳本／probe／resync 腳本留喺工作副本 `~/workspace/linji-work118/`，唔入 repo；`drive_explore118.py` 已 `git rm`（誤入 WIP commit）。

## 合併紀錄
- Squash 合併入 main：`2cdae13`（基底 `999c719`＝v110）。
- 本地 main index.html：5,137,219 bytes，sha256 `af6b43db0911b34a…`。
- 線上初檢（合併後即刻）：5,121,987 bytes，sha `d1c8fcea…`——舊版，Pages 部署滯後；推呢個 NOTES commit 重觸發部署，之後再核實。
