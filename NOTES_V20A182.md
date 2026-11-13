# NOTES_V20A182 — 修 v178 設計 review B1＋C1＋C2（未落地，分支 `v20a182`）

狀態：**未落地。分支 `v20a182`，HEAD `f60f6ee`（rebase 上 main `ece1fac` 之後；基底原本 `4475564`，做嘢期間 main 郁咗一個 v176 NOTES commit `ece1fac`，已 rebase，零衝突）。等統籌 squash merge 落 main。**

任務：用戶 2026-11-13 15:58 親自拍板「一次過修」v178 設計 review（`~/workspace/linji-design-review-v178/REVIEW.md`）嘅 B1＋C1＋C2。實作＋驗證＋NOTES＋commit＋push 分支；唔落地（唔 squash merge、唔 push main、唔做設計 review）。

## 1. B1 — 獎項頁「同屆提名」行被裁切（已修）

- 根源：`renderAwardsPane62()` 提名行同日期行共用 `.awd62-when`（`white-space:nowrap`，v62 舊規則）。三 fellow 長名單（名＋書名號作品名 ×3＋得主標記）伸出卡邊被切。
- 修法（只改顯示，數據層唔郁）：提名行獨立 class `.awd62-fellows`（`flex-basis:100%` 另起一行＋`white-space:normal` 准換行＋`line-height:1.5`）；日期行繼續用 `.awd62-when`（nowrap）唔郁。唔縮字、唔截斷。
- 數字（實駕 932／700 一致）：
  - 修前（pristine）：提名行 scrollW 494 vs 卡 clientW 340（溢出 154px，成行 31% 唔見）；item scrollW 504 vs clientW 340。「高俊傑」只見一半，「《潮汐家庭》（🏆葉敏芝）」全唔見。
  - 修後：提名行 scrollW 320 ＝ clientW 320；item 340 ＝ 340；全句「同屆提名：葉敏芝《渡輪燈火》、鍾楚凝《星光夜》、高俊傑《潮汐家庭》（🏆葉敏芝）」換兩行齊晒（目視 `qa182/shots/fu4_awards_page_430x932.png`）。日期行維持 144＝144，唔郁。

## 2. C1 — 提名卡列三張卡一模一樣（已修）

- 方案（NOTES 寫明揀咗邊個同點解）：揀咗 **CSS 卡面 fellow 專屬化**，唔揀 fullbody 頭像——葉敏芝／鍾楚凝有 fullbody 圖，但高俊傑唔係紅星、冇 fullbody（佢嘅 Q 版 sprite 已按用戶 15:11 方向剝走），用頭像只會 2/3 有圖、1/3 跌返，唔一致；亦唔改卡片數據結構／判定，只改呈現。
- 改動：
  - 卡面（冇 poster 嗰陣）：大字首字（30px，如 葉／鍾／高）＋全名（12px）＋媒介細行（電視／電影／唱片／廣告，淨文字）；唔再三張都印同一典禮名（`medName149`／`.awd63-cssname`／`.awd63-cssicon` 已撤，死 CSS 一併清走）。
  - 底色按卡位 index 揀 tint（`AWDS63_TINTS182` 6 色盤，每場最多 4 張卡，保證唔撞）；得主 🏆 角標／玩家 「你」 金框唔郁；海報卡（有 poster）唔郁。
  - 星名跟隔籬 `.s` 行一樣直接印（內部數據，唔經 esc——見 §6 教訓）。
- 數字（實駕 1991 星河台慶，3 張全係 CSS 卡）：三張 face 文字各不相同（`葉葉敏芝電視`／`鍾鍾楚凝電視`／`高高俊傑電視`），底色 tint 各不相同（紫 `#3a2a4a`／綠 `#274a3a`／酒紅 `#4a2a2e`）；目視 `qa182/shots/ko_cards_430x932.png` 一眼分得開。
- 揀 tint 機制嘅教訓：第一版用星名 hash（charCodeAt 之和 ％ 6），實駕撞色——葉敏芝同高俊傑都係 `#2a3a4a`（心算碼點錯咗）。改做卡位 index，保證同場唔撞。代價：同一粒星唔同場次 tint 未必相同（tint 係同場區分色，唔係身份色），見 §8。

## 3. C2 — 請柬 modal 下方大片黑空（已修）

- 根源（實駕量度證實，唔係估）：請柬 present 嗰陣 `#mask` 仲帶 `story-play-on`（N1 開場故事 modal 仲開緊——新遊戲第一次入地圖會播 N1，drive 強制 `__awards.present()` 嗰陣故事未行完），`#mask.story-play-on .modal{height:100%; max-height:none; background:#0a0705}` 令 modal 變全屏黑。實量：modal 高 932px、maxHeight none、底色 `rgb(10,7,5)`；內容文字得 ~200px，掣貼底，黑空約 640px。結果卡唔受影響（出席掣 `closeModal()` 會清走 story-play-on，結果卡本身係正常 compact 底紙，已目視核實）。
- 修法（兩部分，唔改請柬邏輯）：
  1. `presentAwardInvite()` 開請柬前落返 `story-play-on`＋`setStoryPlayLock(false)`（只係呈現層；故事本身之後經 StoryPlay 重入嗰陣會再加返；`modal()` 本身唔郁，StoryPlay 唔受影響）。呢個就係「收緊 modal 高度」——modal 返返正常 bottom-sheet。
  2. `renderAwardInviteHtml()` 加一行「今晚獎項：{categories labels}」（pack.categories 真實數據；寫「獎項」唔寫「角逐」，旁聽者唔係參賽者）。請柬接線唔郁（細海報＋同屆提名＋門檻行全部留返）。
- 數字（實駕 932／700）：
  - 932：modal 932px → **381px**（maxHeight 720px，底色變返米紙 `rgb(242,235,216)`，`maskClasses: "mask on"`）；文字高 258px，內容下黑空 28px（修前約 640px）。
  - 700：modal 385px，黑空同樣 28px。請柬有「今晚獎項：最佳電視新人（臨記組）、最受歡迎螢幕面孔」一行。
  - 目視 `qa182/shots/ko_invite_430x932.png`：compact 米紙底紙貼喺手帳上面，掣緊貼內容。
- 誠實附註：真實晨鏈流程（朝早報紙／請柬鏈）本身唔會撞到故事播放中，請柬一向係正常底紙；今次修嘅係「請柬喺任何 modal 狀態下 present 都唔會繼承 story 全屏模式」呢個呈現 robustness，review 嗰張全黑截圖係強制 drive 路徑先會出現。修法喺真實流程係 no-op，喺強制流程先見效。

## 4. v181 衝突位（開工前已睇，唔郁嗰邊任何嘢）

- v181（橫向舞台重建）工作副本 `~/workspace/linji-work181/`，基底 `91f264a`，未 commit 改動：`index.html` ＋332／−332 行、多份 awards 測試、刪 `assets/fx/awd_walkup_m4.gif`／`assets/story/awards/bg_awards_ballroom.jpg`、新 px sprite 33 張、`qa181/`＋`tests/test_awards181_logic.js`。
- 查核：v181 嘅 diff 入面 **零行 `+/-` 掂到 `.awd63-cards`／`.awd63-card`／`.awd63-csscard`／請柬**（`git diff index.html | grep -E "^[+-].*awd63-card"` 零結果）。佢郁嘅係：`.awd62-frame` 加 `container-type`、canvas 636×540→720×540（邏輯 480×360）、walkup GIF 層刪除、`.awd63-glamour` aspect 424/360→480/360、以及 `awards62PlayCeremony` 內 walkup／beats 邏輯。
- 對本票嘅影響：
  - **B1／C2 零交集**：B1 係獎項頁 CSS＋`renderAwardsPane62`；C2 係 `presentAwardInvite`／`renderAwardInviteHtml`；v181 兩個函數都冇郁。
  - **C1 交界但唔撞**：v181 嘅 `awards62PlayCeremony` hunk 由 glamHtml 行起（`@@ -46453,26`，佢 base 行號），C1 改嘅 `cardsHtml`／`media` 行喺嗰個 hunk 之上 2–6 行，v181 冇改過嗰幾行；rebase 嗰陣我嘅 patch context（`let glamHtml` 行）喺 v181 嗰邊係 context、無改動，預期乾淨合併。唯一要留意：v181 改咗多份 static 測試嘅行號（resync），我新加嘅 `tests/test_awards182_static.py` 係新檔，唔會撞；但 v181 落地後 main 行號會再郁，**下一輪釘行測試要再 resync**（同 §6 一樣嘅流程）。
  - v181 刪咗 `bg_awards_ballroom.jpg` 同 walkup GIF——本票完全唔掂呢啲資產，唔受影響。

## 5. 新測試＋反證

- 新檔 `tests/test_awards182_static.py`：**27 項，ALL PASS**（B1 6 項／C1 11 項／C2 7 項／硬規則 SAVE／softRev／?v= 3 項）。
- 反證（pristine main `4475564` index）：**15 FAIL／12 PASS，exit 1，無 crash**。12 項 PASS 係「唔郁」守衛（日期行 nowrap、卡片通用 builder、請柬接線／邏輯等），pristine 本來就啱；15 項 FAIL 全部係 B1／C1／C2 新修法。
- 實駕 drive：`qa182/drive182.py`（改編自 `qa178/drive178.py`，加 B1／C1／C2 量度＋斷言），**2/2 PASS（932＋700，各 24/24 checks，0 pageerror）**。證據 `qa182/drive182.json`＋`qa182/shots/`（10 張）。
  - 唱名 caption：葉敏芝 t≈1893ms → 鍾楚凝 t≈2781ms → 高俊傑 t≈3445ms（932）；典禮全長 ~11.0s；舞台剪影 4056 粒（x323–387／y318–385，932；700：y202–269），紅褸 0 粒——同 v178 review 數字吻合，無倒退。

## 6. 全套 A/B＋resync（7 檔釘行測試）

- Pristine（`ece1fac`，`~/workspace/linji-pristine182` 抽出嚟跑，已刪）：**243 PASS／12 FAIL**（同 v176 基線一致）。
- 工作版初跑：**237／19**——12 項穩定 FAIL 兩邊共有，新增 7 項全部係釘行測試（kwan151／tang152／tang171／tang173／text125／travel114／rom176），原因係 v182 index.html 淨 ＋17 行令行號漂移，唔係回歸。
- Resync（`qa182/resync182.py`，跟 resync178 方法：difflib 單次掃描 dict 查表＋逐粒釘行內容逐字核實純漂移；只改測試檔釘行數字＋每檔一行 resync 註解，唔郁遊戲檔）：
  - 漂移段：CSS ＋2（B1＋1／C1 淨＋1）→ 請柬 ＋4 → presentAwardInvite ＋6 → C1 JS ＋5；總淨 ＋17，總行數 59993→60010，openLoc DEF 54493→54510。
  - 7 檔全部 resync：kwan151（13 粒）、tang152（3 粒）、tang171（總行數＋DEF）、tang173（總行數＋DEF＋CSS 同行 4845→4847）、text125（3 粒，精確字串替換——行內歷史註解同釘數字同行，唔行 dict）、travel114（COUNT 13＋FREE 33＋DEF／WRAPPER）、rom176（6 粒）。
  - **教訓（寫低免重犯）**：第一輪只憑 `head -6` 睇 FAIL，kwan151 漏咗 7 粒隱藏釘（A8／B2–B5／C1／C3／C4／E1 用嘅 `line(n)`）；補核實後一併更新，NOTES 同 script 已更正。另：resync 腳本第一版 NUM regex 只食 5 位數，漏咗 4 位釘（rom176 L6028、tang173 L4845），已放寬到 4–5 位；travel114 歷史註解 L206 有 DEF／WRAPPER 舊數，要 SKIP（193–206）。
- 工作版重跑（resync 後）：**244 PASS／12 FAIL，FAIL 清單同 pristine 一字不差**（244＝243＋1 新測試）。零回歸。
- 途中捉到兩個真 bug，已即場修好（見 §7）。

## 7. 途中捉到嘅兩個真 bug（已修，唔係 resync）

1. **`esc()` 唔喺 play 作用域（C1 第一版）**：C1 卡面用 `esc(c.star)`，但 `esc` 只係局部 helper（L27052 嵌套、L46197 `renderAwardsPane62` 內），`awards62PlayCeremony` 入面冇佢 → `ReferenceError` → `attend()` 嘅 try/catch 跌返結果卡，**成個典禮舞台靜默跳過**（stage_appears false、唱名／卡列全無，但結果卡照出、0 pageerror——極易漏網）。修法：跟隔籬 `.s` 行一樣直接印星名（內部數據）。之後 drive 2/2 PASS 證實舞台返嚟。
2. **星名 hash 撞 tint（C1 第一版）**：`charCodeAt` 之和 ％ 6，葉敏芝同高俊傑撞同一色 `#2a3a4a`（心算碼點錯咗）。改做卡位 index 揀 tint（見 §2）。

## 8. 殘留／交接

- **唔落地**：等統籌 squash merge。落地的話 main HEAD 係 `ece1fac`＋本分支（`f60f6ee`）；NOTES 呢份未入 main。
- **v181 落地嗰陣**：佢改咗多份 static 測試行號＋`awards62PlayCeremony` 附近代碼；如果 v181 先落地，下一票要按 §6 流程再 resync 一次（尤其 kwan151／tang152／travel114／tang171／tang173／text125／rom176 呢 7 檔）。C1 改動本身預期乾淨合併（見 §4）。
- **C1 tint 係同場區分色，唔係身份色**：同一粒星唔同場次 tint 未必相同（按卡位 index）。如果之後想每粒星固定色，要改做 starId→色板映射（要處理新星／撞色），另開票。
- **C2 真實流程**：晨鏈請柬本身唔會撞故事播放，今次修法喺真實流程係 no-op（見 §3 附註）；唔使擔心改壞晨鏈——出席／推辭／dismiss 邏輯全部唔郁，static＋drive 已覆驗。
- **`/tmp` 爆滿教訓**：`/tmp` 係 512M tmpfs，`git archive` 抽 pristine（445M）嗰陣爆滿，令一次 suite 輸出爛咗；之後改去 `~/workspace/linji-pristine182` 跑，跑完已刪。之後對照 pristine 用 workspace 唔好用 `/tmp`。
- **Commit**：`f60f6ee`（v20a182，index.html＋新測試＋qa182 全套＋resync 腳本）；resync 7 檔＋NOTES 呢份喺第二個 commit（見 git log）。已 `git push origin v20a182`（只去常駐 clone，唔上 GitHub）。

## 9. Diff 摘要

- `index.html`：＋26／−9（B1 CSS＋1／JS 換 class 1 行；C1 CSS 淨＋1、新卡面 class 4 則、刪 cssicon／cssname 2 則、JS medLabel＋tint＋卡面模板；C2 presentAwardInvite＋6、renderAwardInviteHtml＋3 含今晚獎項行）。
- `tests/test_awards182_static.py`：新檔，27 項。
- `tests/` resync 7 檔：淨釘行數字＋resync 註解（`git diff --stat tests/`：101 insertions／94 deletions，大部分係行號數字）。
- `qa182/`：`drive182.py`、`ko_red.py`、`ko_sil.py`、`resync182.py`、`drive182.json`、`shots/` 10 張、`suite_pristine182.txt`、`suite_work182.txt`、`suite_work182b.txt`（最終 244／12）。
