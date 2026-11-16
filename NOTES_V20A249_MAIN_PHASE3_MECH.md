# v20a249 主線實裝：機制批（GRANT229 收窄＋E1 脊骨＋D8 開閘升格）

- 基底：main `c86e3af`（v248）；分支 `v20a249`；工作副本 `linji-work249`。
- 範圍：只做 v249 機制三項＋相關測試；37 張 NEW 通告、D11、D12 新 gig、D4、D9 搬遷全部留後批（見 §7）。
- 出貨方式：git 直接 squash merge 推 main，唔開 PR。

## 1. 改動總覽

### 1.1 GRANT229 收窄 wildcard（`index.html` GRANT229 表，L25611／L25615）

- `"N4:*"` → `"N4:N4_b"` → `gig_1990_film_114`《水塘夜戲》，reason 不變。
- `"N18:*"` → `"N18:N18_a"` → `gig_1990_tv_121`《電視城幕後》，reason 不變。
- `"N5:*"`（`gig_1990_tv_122`）唔郁；`N6:N6_a`（105）、`N6F:N6F_a`（110）不變。N6_b／N6F_b 唔加 entry（揀「唔接」固定位就唔派即派，抉擇要有真後果）。
- N4_a、N18_b、N5_a／N5_b／N5_c：v249 暫時無即派（NEW gig 留 v250 寫，嗰陣先加 entry）。見 §7 已知限制。

### 1.2 E1 full-spine 檢查——讀法甲（`index.html` L13012 起）

- 新增 `SPINE95_REQUIRED`（16 項：N1–N5、N7–N17；N6／N6F 唔在內）＋ `end95SpineDone(st)`（L13013，插在 `end95ChainsDone` 之後）。
- 脊骨定義（讀法甲）：17 個位置全部 done，N6／N6F 二揀一（任一 done 即計；N1 路線抉擇永久鎖定，AND 要求會令 E1 永遠無人攞到）。**N18／N19 唔計**（補幕）。
- `resolveEnding410`：`e1Qual95` 第三件由 `chains95.length >= 1` 改做 `spine95.done`；E1 reason「主線鏈 …」→「主線脊骨已走完」；SS reason「主線鏈 N」→「主線脊骨 已走完／尚欠 X、Y」。
- `end95BuildGaps`：舊 chains 句換做 spine 句（書面語）：「主線尚欠 … 未完成——天王那一格，要走完整條主線，單靠接工作是堆不出來的。」呼叫點加 `spine: spine95`；`ladder95` 同 `snapshot` 各加 `spine95: { done, missing }`。
- `chains95`／`end95ChainsDone` 保留做診斷（註解已更新，話明唔再係 E1 閘）。**唔好為讀法乙（加 N18／N19）預留結構**；只實裝甲，之後要轉乙，改一行清單就得。

### 1.3 D8 開閘升格（N1–N5 soft stub 由 dormant 升格做 live）

- `evalNode`（L7780 起）：保留原 soft 分支（DengLine held／push 守衛唔郁），加 `else if (coversNode(node))` live 分支（L7794）——stub 已載入即行 `evalTrigger_AND_softRumor`，唔查 `gatePath()`。保留原 `coversNode(node)) return BehaviorGate.evalTrigger_AND_softRumor` 字串（`test_weave45_static.py` 斷言 hook 在 soft dispatch 之前）。
- `liveWeekGateStillActive()`（L8351）改回 `false`，註解更新（v249 LIVE tip；stub file／slice 入面同名字段維持 true，`loadStub` 驗證用，唔郁）。`gatePath()` 註解更新（soft flag 只供測試用）。
- 連帶改咗三處運行時 `live_fn` 斷言（D8 tip 嘅直接後果，唔改 in-app self-check 會報錯）：
  - BehaviorGate `selfCheck` L9043 `live_fn` → 要求 `!==false`；L9047 `soft_retires_live` → 改名 `live_tipped`，要求 `!==false`。
  - `tutorialPhase2Steps56SelfCheck` L12214 同樣改做 `!==false`。
  - Phase3 `check()` L39578 同樣改做 `!==false`。
- JSON `content/story_detail_n1_to_n17.json`：N1–N5 `openConditionsNote` 各加「；live 閘以 soft stub trigger 為準（SANDBOX_BEHAVIOR_GATE_N1_N5_SOFT_STUB_v1.json），此欄只作對照」（只改文字，唔改值；JSON 驗證過有效，19 節點）。

## 2. N5 carve-out 決定：唔用 carve-out，照 stub 原文升格

工人 B 寫定案嗰陣 D10 未決，所以話升格嗰陣跳過 N5 嘅 `seasonAny`＋`rumorSoftPriority` 兩步、拍板後刪 carve-out。而家 D10 已決（N5＝秋、約第 36 週，P-01，用戶 2026-11-15 決定），開工嗰陣逐項核對過 stub file（`content/SANDBOX_BEHAVIOR_GATE_N1_N5_SOFT_STUB_v1.json`，`stubRev: v1.3.0-full-literal-or`）：

- N5 `seasonAny:[autumn,winter]`、`rumorAny:[choi_recent_news, hau_ching_recent_news]`、`rumorSoftPriority:true`、`rumorSeedsRequired:true`。
- `seasonAny` 同 P-01 一致（JSON `openConditionsAny` 亦秋｜冬）；傳聞要求同 P-01 無矛盾（P-01 只定季節／週次）。
- 唯一矛盾係 stub `weekMin: 9` vs P-01 約 36 週，但 `seasonAny` 秋／冬之下 weekMin 9 永遠非 binding（秋天開始已係第 36 週），升格後 N5 實際最早開閘仍係秋天，符合 P-01 實質。
- **決定：唔用 carve-out。**weekMin 9→36 的數值修正留 v250（連同 JSON 一併改，stub 亦要同步）。

## 3. 風險：D8 升格舊檔短暫被鎖（寫入實機抽檢清單 §8）

舊檔升格後即時受新閘約束，唔清 `done`：N2 未聽傳聞會鎖、N3 聲望未夠 16 會鎖。玩家只要去聽傳聞／升聲望就開得返，係短暫被鎖，唔係死檔。

## 4. 測試

### 4.1 新／改測試（邏輯批）

- `test_guidance34_logic.js` §b：改讀真 stub file（之前係 inline 手寫 N2 trigger）；加 live-path 斷言 b7–b16。全部 PASS。
- `test_story_gate113_static.py`：加 v249 四組斷言（evalNode live 路徑、Deng 守衛留喺 soft 分支、sentinel false、GRANT229 收窄、E1 spine 在位＋snapshot／ladder95 有 spine95）。ALL PASS。
- `test_ladder95_logic.js`：`end95SpineDone`／`SPINE95_REQUIRED` 加入 FN／CONST 清單；加 `SPINE95_DONE` fixture；弧2 同 E1 邊界 fixture 加全脊骨 story.done；弧1／弧2／rNoChain 斷言改做脊骨版；加 `end95SpineDone` 單元（全齊／電影線得 N6F／漏 N9／N6＋N6F 皆無／乜都冇／清單 16 項、N18／N19 唔計）。45 passed, 0 failed。
- `test_gig229_counts.js`／`test_qa101_logic.js`／`test_conseq61_logic.js`／`test_weave410_logic.js`：spine 兩項加入提取清單／fixture。全部 PASS（qa101：24 pass / 0 fail；conseq61：82 / 0；weave410：64 passed, 0 failed）。
- `test_gig229_grant.js`：T1 由 wildcard 改做按選項（N4_b→114、N4_a 唔派、N18_a→121、N18_b 唔派）；T3／T4／T9／T10 探針由 N4_a 改 N4_b；頭註更新。ALL PASS。

### 4.2 行數 resync（8 檔，index.html 淨 +21 行：44371→44392）

改動令 index.html 淨 +21 行（`git diff` +47／−26；插入點舊 L7780／7794／8336／8345／8362／9036／9040／12207／12985／12999／13027／13057／13063／13066／13072／13129／13136／13141／25590／25594／39557）。8 份行數釘位測試按 difflib 映射重寫釘行，每個釘行逐字核實內容相同（純漂移），鏈尾加 ＋v249 +21：

- `test_travel114_static.py`：COUNT 12 處＋FREE 35 處＋DEF 39772→39793＋WRAPPER 27795→27816（47 處錨點全數核實）。
- `test_kwan151_static.py`：A 系 7 釘（9052→9059、9393→9400、9441→9448、9660→9667、9396→9403、9397→9404、9398→9405）＋ B2 14382→14403、N1 10694→10701、N3 14417→14438、N4／N5 14381→14402、E1 10661→10668、B3／B4／B5 14372→14393。注意：B3／B4／B5／N5 係否定檢查，錯行都會假 PASS，更加要改啱；已逐個核實。
- `test_tang152_static.py`：9212→9219、14704→14725、14826→14847（`lines()` 0-based 索引 9211→9218、14703→14724、14825→14846）。
- `test_rom176_static.py`：14775→14796、38192→38213、38565→38586、39703→39724、39803→39824；6360 唔郁。
- `test_text125_static.py`：11186→11193、11323→11330、16421→16442（`ls[]` 索引 11185→11192、11322→11329、16420→16441）；報錯字串行號一併更新。
- `test_gift185_static.py`／`test_tang171_static.py`／`test_tang173_static.py`：總行數斷言 44371→44392（標籤 44382→44403）；tang171／173 另有 openLoc DEF 39772→39793（`lines[39771]`→`lines[39792]`，guard 39778→39799）。
- 測試名入面嘅 Lxxxxx 歷史標籤一律唔郁，只改 `line()`／`lines[]`／`ls[]` 索引。

### 4.3 全套 suite

`bash qa131/run_suite.sh . /tmp/v249_suite2.txt`：**TOTAL PASS 314 FAIL 10**，同基線 314／10 形態一致。FAIL 清單逐項吻合已知 10 項 pre-existing FAIL：flash51／rumor49／slot50／soft_tip_111_restore／start53／weave43／weave44／weave49／wf5_87／wrap38。8 檔 resync 後逐個直接覆驗全部 PASS。

## 5. 載入模擬核實（`/tmp/v249_sim.js`，一次性）

- GRANT229 鍵正確（N4:N4_b→114、N18:N18_a→121、N5:*→122 不動、無 N4:*／N18:*）。
- 全脊骨存檔 → E1，`snapshot.spine95:{done:true,missing:[]}`；漏 N12 → SS，gap 句正確。
- stub 載入 ok（n=5）；`liveWeekGateStillActive()` false；flag-off 下 N2 stub 評估 true；`BehaviorGate.selfCheck()` `{ok:true,fails:[]}`。
- `node --check`：兩個 inline `<script>` 塊抽出嚟各自 PASS。

## 6. SPEC 修正（workspace 文件，唔入 repo）

`~/workspace/linji-gig-redesign/SPEC.md` L104：舊句「N5 是春（第 9 週），不可寫秋」→「N5 是秋（約第 36 週），不可寫春」。grep 核實：0 處殘留「N5 是春」。

## 7. 已知限制（留後批，唔係漏做）

- N4_a、N18_b、N5_a／N5_b／N5_c 暫無即派，等 v250（NEW gig 寫好嗰陣先加 entry）。
- 37 張 NEW gig 留 v250／v251，v249 一張都冇寫；庫規模仍係 241 張。
- D11（N17 意向表重寫，按 v235）：v252。D12：G3 新 gig `gig_1992_rec_114`（要求演技 85／歌藝 55／台風 65、陸柏言 `luk_baakyin`）留 v252 寫；**季節修正：工人 C 報告寫 1992秋係錯，正確係 1992春**（N14 春末，D5 已定）——v252 跟春。
- D4：closeup39 獨立節點（weekMin 39）留 v251。D9：N6F 搬入 JSON 留 v250；F4／G4 留喺 `CHOICE47_NODES`，唔搬。
- `gig_1990_tv_122`《記者會現場》：v249 唔改唔刪，去留留 v250。
- N5 stub `weekMin: 9`→36 數值修正留 v250（見 §2）。
- E1 用讀法甲（N18／N19 唔計）；讀法乙未拍板，唔預留結構。

## 8. 待實機抽檢清單（瀏覽器已死，自 2026-11-15 起；live 實機驗證全部押後，唔好當驗過）

- D8 升格：N2 未聽傳聞鎖／N3 聲望 15 鎖 16 開／N4 OR 三路；舊檔短暫被鎖係咪如預期（§3）。
- E1 脊骨檢查：要正常實玩先判到，唔好用 forced preview／seeded save 當證明。
- GRANT229 收窄：N4_b／N18_a 即派實機。
