# NOTES_V20A179 — v172 review 唯一新項 C1：鎖行「（場景：X）」改標籤式

- **來源**：v172 設計 review（`~/workspace/linji-design-review-v172/REVIEW.md`，A 0／B 0／C 1）唯一新項 C1；用戶已拍板修法：鎖行改做「場景：X」標籤式。
- **問題**：進度頁鎖行嘅「（場景：X）」係一句無動詞嘅孤兒括號，隔籬四項全部係條件句（「先完成…」「到第 N 週…」「聽到傳聞…」「聲望要多於…」），初睇要諗一諗佢即係咩。唔係 bug。
- **修法**：拎走括號，改做標籤式「場景：X」，同條件句分返開，一眼睇得出佢唔係條件。已開放行完整句式「已經開放——返地圖嗰陣就會播出。（場景：X）」唔郁。

## 1. 改動位置（`index.html`，只改鎖行渲染 `prog71StubItems`）

| 位置 | 改前 | 改後 | 覆蓋 |
|---|---|---|---|
| L44097（`lm` 分支，`s.match(/^到(.+)播$/)`） | `text:"（場景："+lm[1]+"）"` | `text:"場景："+lm[1]` | C3 單地點鎖行「場景：星河電視台」；C5 多地點鎖行「場景：金龍茶餐廳或星河電視台」（同一分支，raw 係「到 A 或 B 播」） |
| L44104（OR 分支，`s.indexOf("或到")`） | `"或（場景：$1）"` | `"或場景：$1"` | C4 OR 行「以下任一達標：人情債 0／1／何生人情 0／1／或場景：何生事務所」 |

- 註解同步更新（L44091–44096、L44101–44103），記低 v172 括號寫法由 v179 取代。
- **唔郁**：已開放行 L44177「已經開放——返地圖嗰陣就會播出。（場景：X）」原封不動；`progressToward` 原料（「或到何生事務所」等）唔郁，攔截繼續喺渲染層；傳聞提示「（去金龍茶餐廳打聽）」刻意保留（講點滿足條件，唔係觸發句）；SAVE key（`starVolunteer_map_v19w`）、softRev、產品 `?v=` 唔變；content pack JSON 唔郁。

## 2. 測試

### 新測試
- `tests/test_story179_logic.js`（9 項）：抽取真 `prog71StubItems`，stub `BehaviorGate.progressToward` 餵三種 remain 原料——C3 單地點／C4 OR／C5 多地點全部係標籤式、冇「（場景：」；其餘條件句（前置／週數／聲望／傳聞）唔變。**9/9 PASS**。
- `tests/test_story179_static.py`（11 項）：靜態斷言鎖行括號寫法清零、全檔只剩已開放行一處「（場景：」（code 字面計）、已開放行唔變、NOTES 在位、SAVE key／softRev／`?v=` 不變。**11/11 PASS**。

### 反證（pristine main `7801a72`）
- 新測試兩檔喺 pristine 上乾淨 FAIL（鎖行仲係括號寫法），唔 crash：logic **6 FAIL**（3 條新寫法斷言＋3 條冇括號斷言；守衛項照 PASS）／static **4 FAIL**（exit 1）。NOTES 斷言喺 pristine 照 PASS——test 讀嘅係自己 repo root 嘅 NOTES，同 v172 測試同一設計。
- （附：v172 靜態測試 `test_story172_static.py` 兩條 C1 斷言寫死咗舊括號寫法，隨 v179 更新為標籤式斷言並註明取代——斷言意圖不變，只係預期值跟新寫法。更新後 **ALL PASS**。）

### 全套 `qa131/run_suite.sh` A/B
- Pristine 基線（`7801a72`）：**PASS 235／FAIL 12**（12 項 pre-existing FAIL：`qa179_suite_pristineA.txt`）。
- 工作版第一輪：PASS 234／FAIL 15——多出 3 項（`test_tang171_static`／`test_tang173_static`／`test_travel114_static`），根因係初版改動淨 +4 行，撞咗「零行數漂移」釘行測試（總行數／openLoc DEF 行釘死）。修法：將兩段註解壓返原本行數，成個改動淨行數 0（`index.html` 7+/7−，總行數兩邊都係 59356 行）。
- 工作版第二輪（`qa179_suite_workB.txt`）：**PASS 237／FAIL 12**——FAIL 清單同 pristine 基線逐項相同（只差 TOTAL 行 235→237，即兩檔新測試），12 項 pre-existing FAIL 以外零回歸。相關測試逐個直接覆驗：tang171／tang173／travel114／story179 logic／story179 static／story172 static 全部 PASS。

## 3. 實駕（932／700，本地鏡像＋`python3 -m http.server`，`qa179/drive179.py`）

- **A（932，S1：day 21、C1 done）PASS**：C2 已開放行「已經開放——返地圖嗰陣就會播出。（場景：星河電視台）」不變、無播幕掣；C3 鎖行「○ 場景：星河電視台」（標籤式、冇括號），傳聞提示保留。
- **B（932，S2：C1–C3 done＋favor 歸零）PASS**：`progressToward(C4).remain` 原料照舊「或到何生事務所」，渲染出嚟係「○ 以下任一達標：人情債 0／1／何生人情 0／1／或場景：何生事務所」；C5 鎖行「○ 場景：金龍茶餐廳或星河電視台」。兩行都冇「（場景：」、冇「或到」。
- **C（700，S1）PASS**：同 A 逐字相同（C2 已開放行唔變＋C3「場景：星河電視台」）。
- **3/3 PASS，0 pageerror**。截圖 `qa179/shots/`（3 張），結果 `qa179/drive179.json`。

## 4. 殘留問題

- 無。C1 係文案打磨，唔係 bug；修法只係拎走括號，唔改任何判定／數據／流程。
## 5. 落地紀錄（統籌，2026-11-13）

- 分支 `v20a179`（工人 HEAD `03def42`，基底 `7801a72`）rebase 上當時最新 main `1fe7fc2`（v177 已落地）：第一次 rebase 誤報「local changes to tests/test_story172_static.py」（`git diff` 空、實質零改動，假陽性），`git rebase --abort` 後 `git update-index --refresh` 再 rebase 即成功，無衝突；新 HEAD `021e300`。
- Rebase 後重驗：新測試 logic 9/9＋static 11/11 全 PASS；全套 `238／12`，FAIL 清單同 pristine 12 項逐項相同，零回歸（PASS 由工人嗰輪 237→238 係 suite 波動，見 AGENTS.md v151 教訓）。
- Squash merge 落 main：遊戲 commit `4106b2f`；`git fsck` 乾淨（只得 dangling 物件，無錯誤）。
- Push main：第一次斷線（Broken pipe／remote hung up，egress proxy reset，已知間歇問題），重試一次成功（`1fe7fc2..4106b2f`）。
- 線上核實：第一次 curl 仲係舊版（Pages 滯後），等 90 秒後重 curl——**5,271,638 bytes、sha256 `c428f3d18eb1bfa49ff2047230a8ddccf2aa460500265065cfe85b246a84c643`**，同 repo `HEAD:index.html` 完全一致。v179 已上線。
