# v20a81 — WF2：感情線廣東話化＋半線差一步收尾（＋彭少祺正名）

基底：v20a80（線上 4,854,789 bytes，tests 90/90）。SAVE key／softRev／產品 ?v= 不變；Save v 版不變（純內容覆寫＋一名稱正名，零機制改動）。

## 範圍（豐富化計劃 WF2）
1. 曉晴／采兒完整線主體對白廣東話化：盤點證實兩線主體係全書面語（廣東話標記 0），去到 commit 節點先轉廣東話，斷層嚴重。逐節點翻寫成自然廣東話，保留劇情事實、抉擇結構、數值後果。
2. 采兒職業升級（年代映射 M33）：新派週刊追訪記者——自己落場查證、唔抄通稿、主編催獨家；張力係「佢要料、阿偉要守（唔害人飯碗）」。唔寫成建制狗仔隊（1995 後先成形，排除清單）。
3. 四條半線（Vera／徐寶珊／藍若曦／鄧麗萍）專屬「差一步」收尾：原版 ending 得 99–142 字 3–5 行；逐條寫成場專屬收尾戲（450–557 字），場景、對白、差一步理由各自獨有，唔共用範本；其餘節點同步加厚到 200 字級＋廣東話化。
4. pack synopsis 名實修正：半線 ending 喺 pack 寫成「可以確定關係／建立平等伴侶關係」等，同結局專檔拍板（半線唔入 commit、只做差一步）不符——以覆寫改返差一步口徑。
5. 附帶：彭兆基 → 彭少祺正名（WF1 遺留核實項，見下）。

## 做法
- 新表 `ROMANCE_WF2_OVERRIDES`（30 節點）＋ `applyRomanceWf2Overrides81()`：欄位級 merge，只換 `beats`、`synopsis`，同（只限四條半線 ending）`choices[].label`／`choices[].effects.notes` 文字；WeakSet 冪等守衛。
- call 位：`refreshCopyPacksFromDisk` 內，`applyStorySpineOverrides48()`（藍 PA 覆寫）同 `applyStoryWf1Nodes80()` 之後、`textfix55StoryPack` 之前——藍線 merge 目標係 PA 版節點（PA 原句一字保留，只加厚）。
- choice id／flags／stats、openConditions、flags_written、playerOffer、commit 機制（`S.story.rel`、rel≥6、`flag_hiu_commit`／`flag_choi_commit` 互斥、COMMIT48 全部定義）逐字不動，測試以 v80 fixture 逐項比對。
- 唔直改 content pack JSON（原生移植時覆寫表一齊搬）。

## 自作判斷（如實記錄）
1. **半線 commit 旗保留唔改**：pack 四條半線 ending 嘅 HE choice 本來就寫 `flag_*_commit`，而 `endingRomance410()`／`endingRomanceState48()` 會讀嚟回報；原碼註解（近 35160 行）明言機制層如實回報、判定層（4-10）已定性半線只做差一步。今次只對齊呈現文本層（對白／synopsis／label／notes），旗同機制零改動——若將來要連旗改名，要連判定層一齊做，唔喺 WF2 範圍。
2. **鄧麗萍差一步理由係新創**：結局專檔原表冇鄧線（註「維持原規劃暫緩」）；按 parent 定案（鄧＝半線）同佢人設度身：數字上最親近嘅人，隔住一張排片表——紅筆圈住嗰格唔係數據最好嗰格，嗰句「呢格係我畀你嘅」最後改口做公事口吻。
3. **徐寶珊人設跟 pack LIVE**（廣告界女強人、離婚、生意為伴），唔跟結局專檔表格嘅「富豪千金」寫法；「世界唔同」質地照專檔設計（禮物扯平：名錶 ↔ 擋記者）。
4. **藍若曦以 LIVE PA 版為底本**加厚（唔係 pack 歌手版）；ending HE label 由「講明心意：嗰餐飯，唔使等第日」改成接住約定口徑，同其他半線一致。
5. **徐寶珊 push2 原句「生意就是我的伴侶」改寫**成「呢幾年陪住我嘅就得返盤生意」，意思不變，避開半線文本出現「伴侶」字眼造成名實混淆。
6. **采兒 crisis 加一句消息形態具體化**（「相係人哋追到交嚟嘅」）落 M33 追訪質地，冇改兩條路／前途／交稿期限等事實。
7. 寫作分五手並行（曉晴／采兒／Vera／徐／藍+鄧），統籌整合＋全量驗證；每節點 beats 字數、廣東話標記、書面語殘留都經程式核實。
8. 刊名跟 v57 術語：pack 原名《星訊周刊》嘅「周刊」係 v57 清理嘅 B6 禁字（玩家字串零周刊，speaker「周刊編輯」除外），覆寫表統一用《星訊週刊》；整合後 test_terms57_static 回歸 PASS。
9. 連帶原位改版嘅舊測試（有意行為變更，理由即本 NOTES）：test_poster59_logic／test_weave46_logic／test_weave46_static／test_awards63_logic 內「彭兆基」期望值改「彭少祺」；test_ux68_static 主檔總量上限 4,900,000 → 4,960,000（WF2 覆寫表有意增長）。

## 彭少祺正名核實（WF1 遺留）
- 全 index 共 34 處「彭兆基」，pack JSON 0 處。玩家可見面包括：C10 主線節點（cast／synopsis／beats speaker／redStarHook，金牌司儀顯示名）＋ LEADSTAR59 通告主演對照表（通告卡「主演：」顯示）；內部鍵有 speaker→sprite 對照以顯示名做 key 一處；其餘係 DEV 註解。
- 結論：玩家可見，要正名。index 內全量取代「彭兆基」→「彭少祺」（index 係源碼，唔受「唔直改 pack」紀律限制），對照 key 同步改名；測試斷言全檔計數 = 0。

## 內容量（beats 字數，lines 字元合計）
- 曉晴 5 節點：303–321（原 269–294）；采兒 5 節點：314–329（原 220–296）；合計原約 2,689 → 新 3,160。
- Vera：212–236＋ending 557（原 99–160）；徐寶珊：218–224＋ending 480（原 91–112）；藍（PA 底本）：204–223＋ending 491（原約 108–130）；鄧麗萍：217–240＋ending 540（原 124–181，數字 token 全數保留）。
- 四條收尾差一步理由：Vera＝手停喺領口嘅清醒（唔攞專業同對方前途嚟賭）；徐＝世界唔同，禮物扯平、心照唔講「一齊」；藍＝太熟唔敢＋唔想坐實「偏幫」閒話，嗰餐飯係約定唔係關係；鄧＝唔肯改嗰把尺（改咗就唔再係鄧麗萍），紅圈嗰句改口做公事口吻。

## 驗證
- 新增測試 2 份：`tests/test_wf2_81_logic.js`（121 項：語體密度／M33／收尾互異 Jaccard／merge 機制零改動 fixture 比對／commit 回歸／紅線）＋ `tests/test_wf2_81_static.py`，連 fixture `tests/fixtures/romance_wf2_v80.json`。反證：兩份新測試喺 v20a80 index 行均 FAIL。全套 tests（根目錄跑法）92/92 PASS。
- 真 UI 實駕（本地鏡像＋槽 3，`~/workspace/linji-work81/verify81/`，pageerror 0）：
  - 曉晴線 R_hiu_push1 真 UI 開播，渲染 WF2 新廣東話（截圖：林曉晴「我聽講下星期有個試鏡喎…」），播完入 done；R_hiu_meet 喺註冊表（StoryOC.findNode）核實第一拍已係 WF2 新文本。
  - 半線收尾 Vera ending 真 UI 開播（9 拍，「手停喺領口」場面＋新 HE label「留低嗰句心照，帶住餘溫行出去」渲染、播完入 done）；鄧麗萍 ending 喺註冊表核實 beats＋HE label 已更新。
- **實駕發現（既有架構，唔喺 WF2 範圍，留俾後續工作包定奪）**：soft 行為閘模式下，曉晴／采兒 meet 由 DualMeet 雙人 meet 層換版播放（C3 後開閘）、成條鄧麗萍線由 DengLine 層換版播放（isPush/pushNode）——兩層各有自己一套 beats（部分仍係書面語），唔經 pack 節點。WF2 覆寫嘅 pack 節點係非 soft 路徑同原生移植嘅正文；soft 層變體文本要唔要同步廣東話化／差一步對齊，建議列入 WF5 觸達審計一併盤點。
