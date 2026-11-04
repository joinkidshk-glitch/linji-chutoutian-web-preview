> Soft≠PASS｜鄧線 Soft 計劃｜**Soft A 已鎖**｜經 qwen3.7-max｜唔 tip｜出圖 HOLD｜89–92 HOLD
>
> **Soft A 鎖（寫死）：** ①開線＝C5 完成＋`agency_ho` favorMin≥1（與 C4 favor∧loc 咬合）＋threshold｜②MVP Soft 可 Mock meet（只 meet；push1+ HOLD）｜③`rel_tang_threshold`**=2**

# PLAN_STORY_DENG_LINE_SOFT_v1.md（鄧麗萍可選攻略線 Soft 計劃）

## 1. 範圍與定位
- **定位**：可選攻略線（院線排片高層）。
- **平行原則**：不搶 MVP 曉晴＋采兒必經資源；可與雙女平行發展至結局（遵循 meet／rel／commit 節拍網精神，不強制互斥至結局前）。
- **實裝狀態**：本檔僅為 Soft／Mock 計劃文，不修改 LIVE JSON，不推 tip，不寫實裝引擎接線細節。

## 2. 角色與 ID 規範
- **玩家面角色名**：一律使用「鄧麗萍」。絕對禁止在玩家面例句或 UI 中出現真實藝名靈感（如陳淑芬、施南生等，僅限 DEV 內部參考）。
- **內部 ID 對齊**：
  - 角色 id：`tang_laiping`
  - 旗幟：`flag_tang_*`（如 `flag_tang_open`, `flag_tang_met`, `flag_tang_commit`）
  - 節點：`R_tang_*`（如 `R_tang_meet`, `R_tang_push1`）
  - 選項：`C_tang_*`（如 `C_tang_meet_data`）
- **關海媚重申**：維持週刊總編／曖昧 vignette 定位，絕對不升格為第六攻略或 commit 對象。鄧線為可選支線，不進入 C1–C5 必經節點。

## 3. 開線閘與前置條件（**Soft A 已鎖**）
- **開線閘（寫死 Soft A）**：`needDone: ['C5']` ＋ `favorMin: 1` @ `agency_ho`（何生事務所 favor／聲望閾；與行為閘 C4 `favor≥1`∧loc 咬合——C4 已要求 favorMin≥1，鄧線開線再要求 **C5 完成** 後仍維持／達到 favorMin≥1 @agency_ho）。
- **Meet**：排片上門談判；`R_tang_meet.openConditions=[]`（節拍本身可寫入 `flag_tang_open`）；一條 choice（`C_tang_meet_data`）必須寫入 `flag_tang_open`。
- **Push+ 觸發（雙條件）**：必須同時滿足 `flag_tang_open` 與 `rel_tang` ≥ **`rel_tang_threshold=2`**（Soft A 寫死）。
- **MVP Soft 範圍（Soft A）**：可 Mock **meet only**；`R_tang_push1`／`push2`／`crisis`／`ending` 正文 HOLD（push1+ 後做）。


## 4. Soft 節拍表（沿舊稿重鎖）
*註：年代已重鎖為「院線通用時空／1988 起步」，避開 89–92 深時代事件；synopsis 與 setting 已統一使用「阿偉」及規範書面語。*

| beatId | 類型 | when／setting（通用時空） | openConditions | choices（id＋效果旗） | 衝突一句 | synopsis（阿偉視角） |
|---|---|---|---|---|---|---|
| **R_tang_meet** | meet | 1988 後院線季節｜龍頭院線排片部會議室；牆上貼滿午夜場與周末場的報表，紅筆圈住每一格未達標的數字。 | `[]` (寫入 `flag_tang_open`) | `C_tang_meet_data` → `['flag_tang_open']`, `rel_tang: 1`<br>`C_tang_meet_wait` → `['flag_tang_met_wait']`, `rel_tang: 0` | 新片爭檔期 vs 院線數據門檻 | 阿偉帶着新片資料上門，想在龍頭院線爭一個正式檔期。鄧麗萍沒有同他寒暄，一開口就是上座率和午夜場數據；阿偉要在她的報表邏輯裏面，證明自己這套戲值得一個位。 |
| **R_tang_push1** | push | 院線通用時空（冬季）｜院線票房中控室，深夜十一點半，螢幕上跳動着各院即時入座數字，枱面有一疊未拆的午夜場報告。 | `['flag_tang_open', 'rel_tang_threshold']` | `C_tang_push1_exchange` → `['flag_tang_push1_exchange']`, `rel_tang: 1`<br>`C_tang_push1_prove` → `['flag_tang_push1_prove']`, `rel_tang: 1` | 冷門檔期風險 vs 數據回報 | 阿偉同鄧麗萍開始有來往，但她仍然句句帶百分比。雙方交換試映情報同冷門檔期資料，她第一次主動問阿偉這套戲在其他區的口碑走勢。 |
| **R_tang_push2** | push | 院線通用時空（春季）｜周六深夜午夜場散場後，戲院後巷茶餐廳，枱上攤着即日票房紙，隔壁枱還有人吃着宵夜。 | `['flag_tang_open', 'rel_tang_threshold']` | `C_tang_push2_business` → `['flag_tang_push2_business']`, `rel_tang: 1`<br>`C_tang_push2_private` → `['flag_tang_push2_private']`, `rel_tang: 1` | 純商業計算 vs 私人情感試探 | 黃金檔試水成績出爐，鄧麗萍約阿偉在午夜場後對數。她心情比平時鬆一點，講起自己以前排過一套文藝片，蝕到要寫報告。阿偉可以選擇繼續純商業，或者問她私人那一句。 |
| **R_tang_crisis** | crisis | 院線通用時空（秋季）｜院線總部會議室，對手片發行商剛剛離開，枱面留下兩份搶黃金檔的建議書，牆上排片表用紅筆畫到密密麻麻。 | `['flag_tang_open', 'rel_tang_threshold']` | `C_tang_crisis_data` → `['flag_tang_crisis_data']`, `rel_tang: 1`<br>`C_tang_crisis_favor` → `['flag_tang_crisis_favor']`, `rel_tang: 1`<br>`C_tang_crisis_middle` → `['flag_tang_crisis_middle']`, `rel_tang: 1` | 檔期數據 vs 人情 | 對手片用高價搶黃金檔，阿偉手上有一套帶人情和藝術傾向的片想排同一個位。鄧麗萍要阿偉在數據和人情之間揀，她自己亦被上頭壓住要交數。 |
| **R_tang_ending** | ending | 院線通用時空（年終檢討後）｜院線年終檢討會後，走廊燈光半暗，盡頭是一間未開場的空戲院，銀幕還未拉開。 | `['flag_tang_open', 'rel_tang_threshold']` | `C_tang_ending_he` → `['flag_tang_commit', 'flag_tang_he']`, `rel_tang: 3`, `standing: 1`<br>`C_tang_ending_be` → `['flag_tang_be']`, `rel_tang: -2` | 商業盟友 vs 感情原則 | 年終數字出爐，阿偉這套戲全年為院線帶來實質增長。鄧麗萍在走廊叫住他，講明她認可他的號召力；但她要阿偉揀，是做一個並肩的商業盟友，還是繼續用感情挑戰她這條線。 |

## 5. 與主線／行為閘／人情／噂 輕咬合
本節僅作 Soft／Mock 規劃，引擎接線暫不實裝：
- **開線前提（Soft A 寫死）**：C5 完成後，且 `agency_ho` favorMin≥1（與 C4 咬合）；見 §3／§8。
- **情報／噂 (Rumor)**：玩家面僅於金龍茶餐廳（`cafe_cha`）或茶水間出現極低機率之「傳聞」級別 hint（例如：「聽講龍頭院線嗰個鄧小姐，睇數據好狠」），無實質互動，不強制觸發。
- **人情債**：`R_tang_crisis` 中的「人情片」可與主線人情債系統輕度掛鉤，但不影響主線核心數值。
- **競爭對手**：`rival_gao`（高仔）不混入鄧線，保持支線獨立性。

## 6. Out of Scope（不在此次計劃範圍）
- **89–92 深時代事件**：絕對不綁死特定年份的深時代政治或社會事件。
- **出圖 (Art)**：暫緩，artId 僅佔位，不生成實際圖像。
- **LIVE tip**：不推送任何 LIVE 環境的 tip 或實裝代碼。
- **關海媚升格**：維持曖昧 vignette，絕對不升格為第六攻略對象。
- **修改 LIVE JSON**：本檔僅為計劃文，不直接改動現有 LIVE 數據。
- **搶奪 MVP 資源**：不搶曉晴／采兒必經資源，不進入 C1–C5 必經節點。

## 7. 驗收清單（Acceptance Checklist）
- [ ] 頁眉格式正確，包含所有指定標籤。
- [ ] 玩家面角色名統一為「鄧麗萍」，無真實藝名靈感洩漏。
- [ ] 內部 ID（`tang_laiping`, `flag_tang_*`, `R_tang_*`, `C_tang_*`）完全對齊。
- [ ] 年代標籤已重鎖為「院線通用時空／1988 起步」，無 1991/1992 年終深時代字眼。
- [ ] Synopsis 與 Setting 已將「你」改為「阿偉」，並完成書面語輕潤（跳動、站得住、扛、懂分寸）。
- [ ] 節拍表齊全（meet/push1/push2/crisis/ending），且 openConditions 與 choices 邏輯正確。
- [ ] 關海媚不升格聲明已包含。
- [ ] Out of Scope 列表完整。
- [ ] Soft A 三項寫死（C5＋favorMin≥1@agency_ho；Mock meet only；rel_tang_threshold=2）。
- [ ] §8 標「已拍板 Soft A」，非「等統籌拍板」。

## 8. Soft A/B 決策（**已拍板 Soft A**）

> 統籌抽樣 PASS 後拍板；本節由「等拍板」改為「已鎖 Soft A」。唔再開 A/B。

### Soft A 寫死一覽
1. **開線門檻＝A（嚴格）**：C5 完成 ＋ `agency_ho` **favorMin≥1**（favor／聲望閾；與 C4 favor∧loc 咬合）＋ threshold 語意（見下）。
2. **MVP Soft 預覽＝A（可 Mock meet）**：可 Mock **只 meet**；push1+／crisis／ending **後做／唔入今次 Mock**。
3. **`rel_tang_threshold`＝A（=2）**：push1 起需 `flag_tang_open` ∧ `rel_tang≥2`。

### 對照（已否決之 B，僅存檔）
- B1 寬鬆（C3 後／threshold=1）— **否決**
- B2 唔預覽 Mock — **否決**
- B3 threshold=1 — **否決**

### 實作備註
- Mock 檔：`MOCK_STORY_DENG_LINE_MEET_SOFT_v1.json`（scope=meet only；Soft≠PASS）。
- 出圖／LIVE tip／89–92／關海媚升格／搶曉晴＋采兒必經：**仍禁**。

---
*DEV 標記：相關 JSON 節點未來實裝時加 `"dev_only": true`；MVP Soft Mock meet 另標 `"deng_line_soft_meet": true`。舊文稱謂統一「何生」；玩家面禁舊稱謂／真藝名。*
