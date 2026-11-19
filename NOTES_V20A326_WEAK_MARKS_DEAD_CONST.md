# NOTES_V20A326_WEAK_MARKS_DEAD_CONST — 刪 WEAK_MARKS 死常數

> Base：main `a87b9dd`（v325，通告庫 322 張）。票源：`NOTES_V20A323_TEXTFIX57_DEAD_MAPPINGS.md:12,38` 明文列 WEAK_MARKS 為死常數另開票。
> 偵察 brief：`~/workspace/linji-brief-weak-marks-v326.md`（2026-11-19，唯讀核實，全部前提喺工作副本再對一次先動手）。

## 一、改動（index.html 兩處，淨 −1 行：47281 → 47280）

| 檔案 | 改動 |
|---|---|
| `index.html` L27959（刪整行） | `const WEAK_MARKS = ["捱得","識做","耍大牌","爛仔","守口如瓶","搏出位"];`——零讀者死常數。讀者死於 v20a1（`a8d6149`）：`ensureWeakSeals()` 改寫做讀 `castingTagsEarnedLabels()`，`WEAK_MARKS.map` 一行被換走，常數留低無人清。鄰行 L27958 `};`（DEBT_FUZZY 結尾）／新 L27958 `function debtStatusLabel(status){`，結構不變。 |
| `index.html` L12541（註解改一行） | `   -「大牌」「爛片」：專檔原詞，現行內容未有同名標籤（大牌只喺 WEAK_MARKS 耳語池），先入清單，` → `   -「大牌」「爛片」：專檔原詞，現行內容未有同名標籤，先入清單，`（刪括號一句；括號本身雙重過時——值早已唔係「大牌」而係「耍大牌」，刪常數後「耳語池」亦唔存在）。L12541 喺刪除點之前，行號唔郁。 |

## 二、測試同步（5 檔，全部 −1 漂移，difflib 核實純漂移）

- `qa326/resync326.py`（仿 qa323 寫法，單次掃描 dict 查表＋精確錨點＋次數斷言）：difflib 核實 index.html 只有兩處非 equal hunk——舊 L12541 replace（1 行換 1 行）＋舊 L27959 delete；總行數 47281→47280；`WEAK_MARKS` 已不在新檔。同步 `tests/test_gift185_static.py`（總行數）、`tests/test_tang171_static.py`／`tests/test_tang173_static.py`（總行數＋openLoc DEF 42490→42489、guard 42496→42495、`lines[42489]`→`lines[42488]`）；ok() 名歷史鏈加 `＋v326 −1`；每檔檔頭加 resync 註解行。
- `qa326/resync326b.py`（suite 兜底，見 §三）：同步 `tests/test_rom176_static.py`（4 個釘行各 −1：40722→40721、41072→41071、42375→42374、42531→42530；6321／14772 喺刪除點之前唔郁；ok() 名入面嘅 L55647 等歷史標籤唔郁）＋`tests/test_travel114_static.py`（FREE／COUNT 區塊單次掃描 dict 查表：COUNT 5 處＋FREE 26 處各 −1，之前唔郁；DEF 42490→42489、WRAPPER 29099→29098；逐個錨點內容核實：FREE 40 行帶免費旗、COUNT 12 行唔帶）。
- **brief 更正**：brief 寫 `test_tang173_static.py:168` 有兩處斷言，實際喺副本核實係總行數 L166、openLoc L167–168（差 2 行）；已按實際行號改，唔跟 brief 舊數。
- 五檔測試檔頭 resync 註解行刻意唔寫 `WEAK_MARKS` 字串（寫「刪死常數舊 L27959」），等驗收 grep 喺 tests/ 保持 0 命中（見 §四）。

## 三、測試

- 五檔逐個直接跑：gift185 ALL PASS、tang171 22／22、tang173 22／22、rom176 ALL PASS、travel114 RESULT PASS。
- 全套 suite 第一跑：`bash qa131/run_suite.sh` → **TOTAL PASS 383 FAIL 11**——基線 9 項之外多出 rom176＋travel114，兩檔經 difflib 核實係純 −1 漂移，按同一慣例 resync（qa326/resync326b.py），唔係非漂移 FAIL。
- 全套 suite 第二跑：**TOTAL PASS 385 FAIL 9**＝基線；9 項 FAIL 全部係已知 pre-existing（flash51／slot50／soft_tip_111_restore／start53／weave43_static／weave44_static／weave49_static／wf5_87／wrap38），逐項同基線一致，零回歸。跑完已喺工作副本還原 `qa296/derive296.json`（衍生檔，唔入版）。

## 四、驗收

- `grep -rn "WEAK_MARKS" index.html tests/ content/` ＝ **0 命中**。
- `ensureWeakSeals()`（L28065–28080）＋ 4 個呼叫點（L28422／28664／29180／35358）＋自檢 `weak_seals_tags`（L35446）、`castingTagsEarnedLabels()`（L28048）、`ENDING_NEG_TAGS410`（L12543）、`.weak-seals` CSS（L3416–3426）、SAVE key `starVolunteer_map_v19w`／softRev `s107`／`?v=20a10` 全部原封不動——`git diff index.html` 嘅 `+`／`−` 行 0 命中上述 token，diff 只有 §一 兩個 hunk（1 增 2 刪）。
- 刻意保留（唔郁）：`qa149/pristine_index.html` 凍結快照（L42897 定義＋L29184 註解）；NOTES 歷史提及（`NOTES_V20A33`／`V20A57`／`V20A79`／`V20A246`／`V20A323`）；個別值字串獨立出現（`爛仔` TRAJ49 表、`守口如瓶` support 表／通告 tag／對白、`捱得`／`識做` 對白／標籤）唔係引用；「身手好／耍大牌」dormant 檢查另一層機制，唔係本票範圍。

## 五、合併＋部署（待填）

- 工作副本：`linji-work326`，分支 `v326-weak-marks`；內容 commit `82aace7`。
- main HEAD `7a8493a`；Pages md5 `fe48880b5ae8db427e0e514901586844`／4,701,053 bytes，curl 核實 byte-identical；工作副本已刪。
