# v20a358 支線複檢 (b) 潤飾＋欄位串層 5 項＋soft 層鄧麗萍清理

2026-11-21。基線 v357（main `478c428`，suite 398 PASS／9 FAIL）。複檢核實表：
`~/workspace/linji-story-review-side/verification.md`。本版處理餘下三部分；
4 項文風取捨、1 項部分證實（s7 A8）、2 項判斷唔修（s5 A3／s6 A8）留待用戶拍板，唔郁。

## 1. (b) 類待潤飾（qwen4-max 細批次＋程式閘門＋成批制）

流程跟 v346–v350 已驗證口徑：`bl text chat --model qwen4-max` 逐 node 細批次（20 批），
brief 帶語言硬規則＋敘述黑名單（引號內原話豁免），閘門＝數量對齊／半形標點退化／
長度比 0.45–2.0／N 層黑名單掃描／數字 token 保留；閘門 fail 成批保留原文。
20 批全過閘門（其中 3 批人手覆核後重跑：J10「指引／路線」用字唔啱、J11 xu_ending
「一隻錶有貴有賤」失「擋記者」回扣、E3 mak_patron_cold 主語調轉），共套用 59 處唯一文字改寫（另 s5 B1 beats[8] 一處，見 §2）：

- **rival_mentor JSON 27 處**（J1–J9）：ko 3、hakfan 4、gao 3（ending stay＋crisis synopsis＋push2 safe label）、
  tsijun 2、fong 5、tong 2、ho 3、lei 5。
  「心底有刺」×3（s1 B5＋s4 B5）統一改「暗裏仍存芥蒂／兩人之間自此有了隔閡」一類書面寫法。
  label 尾「。」按慣例剝走（ally／safe 兩 label）。
- **vera_hiu_choi JSON 1 處**（J10）：R_choi_push1 notes「獨家方向…談妥一條線」→「只給她一個獨家方向，
  沒有提供任何材料，兩人約定以不害人為界線」。
- **lan_xu JSON 7 處**（J11 xu 5＋J12 lan 2）：push1 synopsis／decline label+notes／push2 synopsis／
  ending HE notes；R_lan_push2 synopsis（「怎樣站」→「怎樣回應」）、R_lan_ending beats[4]
  （「笑容裏有些東西」→「笑容裏藏著的話」）。
- **WF2 覆寫同步 2 處**：R_lan_push2 synopsis、R_lan_ending beats[4]（同 JSON 一致）。
- **ENC 表 24 處**（E1–E8）：lan/ngai/ching openers 3、pang 2、chai 3、mak 2、hon 3、ngai_patron 1、
  ching_e4 1、yip 1、so 3（first lines[8]／wrap／heart choice）、chung 2、gu_loan 1、so label 1、
  chung_intel label 1（人手修正「他」→「她」＋「着」→「著」）。
- **swaps 同步**（ENC79_FIRST_ALT98 exact 配對）：pang first lines[1]（順手對齊 swap source 同 base
  嘅「和人／進出」vs「跟人／出入」不一致）、chai first lines[0]、lok first lines[1]（見 §2）。
  GRANT229_ENC79 key「講大話／指點」保留（chung_intel 新 label 留「指點」）。

唔改事實／年份字串／數值／旗標；source 年份冇手改 +2。

## 2. 欄位串層 5 項

旁白（N）層入咗「角色名：廣東話原話」裸引語嘅三處，加敘述框架＋引號（原話保留廣東話）；
阿偉（A）層第三人稱旁白式獨白兩處，改第一人稱內心獨白（保留 A 層，唔改結構）：

- **s9 B4** `ENC83_DLG_lok_gasing.first.lines[1]`：「高層：家聲，你嗰啲歌…」→
  「高層房裏傳出一把聲音：「家聲，你嗰啲歌，台度播唔播，我哋自有分數，你唔好咁大聲。」」；
  ENC79_FIRST_ALT98 lok swap 第二對 source／target 同步。
- **s13 B1** `ENC79_DLG_liu_bingxing.first.lines[4]`：「副導：喂，後生仔…」→
  「副導在旁邊開口：「喂，後生仔，企喺度做乜？唔好阻住大佬度橋啦。」」
- **s15 B3** `ENC83_DLG_gu_mingfai`：gu_foreshadow lines[1]（西裝男人壓低聲音說）、
  lines[3]（西裝男人嘆了口氣）、gu_patron lines[2]（昌哥笑著說），三句同法加框架＋引號。
- **s14 B6** `ENC84_DLG_ching_tinlok.beats.ching_patron_cold.lines[2]`（A 層）：
  「（阿偉望住佢個背影，明白佢唔係嬲…等你下次…）」→「（佢唔係嬲，係等緊——等我下次用把真聲，唔係用部機，同佢講嘢。）」
- **s16 B3** `ENC84_DLG_chung_choning`：first.choices[1].lines[0]「（阿偉點一點頭…）」→「（我點一點頭…）」；
  heart.lines[13]「（阿偉望住佢…）」→「（我望住佢…）」；同 beat heart.choices[0].lines[0]
  「（阿偉冇出聲…）」同型，一併改「（我冇出聲…）」（核實表未列，屬同型同 beat 順手修正）。

另 **s5 B1**（(b) 類）：R_lan_ending beats[8] speaker 藍若曦→旁白，text
「（佢笑住轉身收拾通告牌，嗰句說話留咗喺走廊，等佢接。）」→「她笑著轉身收拾通告牌。那句話留在走廊，等他接下去。」
（JSON＋WF2 覆寫同步；beat 數不變）。

## 3. soft 層鄧麗萍清理（全段刪，live 路徑零讀者已核實）

鄧麗萍已刪除人物。清理前逐呼叫點核實（2026-11-21 實證）：DengLine 所有呼叫點都喺
`featureFlag_softBehaviorGatePreview()` soft 閘或 `typeof DengLine!=="undefined"` 守衛之後；
`tangFileThreshold()`／`resolveThreshold` 嘅 DengLine 分支回值同 fallback 同為 2，行為一致；
播放路徑同一個 if 包住 DualMeet（曉晴／采兒，唔係鄧麗萍）——改 guard 保留 DualMeet。
live 公事 stub 路徑（normaliseTangStub152、`flag_tang_open` 送禮入口、stub JSON、seed ID）
唔郁（屬 s7 A8 部分證實範圍，留待拍板）。SOFT_SEED_IDS 嘅 seed_deng_* ID 保留
（種子變 no-op，seed selfCheck 照過）。

刪走：
- `WF5_VARIANT_OVERRIDES87` 內 R_tang_meet／push1／push2／crisis 四條目（保留 R_hiu_meet／R_choi_meet
  ＋applyVariantWf5Overrides87，呼叫改 `applyVariantWf5Overrides87(dualMock)`）。
- DengLine IIFE 全段（約 294 行）＋`window.DengLine`／`window.__dengLine` 匯出。
- Mock 底稿 5 檔：`MOCK_STORY_DENG_LINE_MEET_SOFT_v1.json`／`v1.1.json`／`PUSH_SOFT_v1.json`
  ＋同名 .md（MEET v1.1.md、PUSH v1.md）；PLAN_*／NOTES_* 開發文件保留。
- Fetch 線（2 行 get＋destructure 名）＋下游 wiring（textfix55StoryPack、years66Walk 清單、
  loadMock／loadPushMock 塊）。
- 呼叫點：storyHintPack DengLine 塊、tangFileThreshold 簡化（return 2）、resolveThreshold rel_tang 分支、
  gatePath soft 守衛 3 處、播放路徑 DengLine 分支（保留 DualMeet）、鎖檢查條件 DengLine 部分、
  presentSoftSeed 兩 deng 種子分支、agency_ho 兩排片掣塊。
- 三處會誤導嘅註解改準確（L7862／L7944／L14397 一帶）；其餘註解提及保留作開發歷史。
- `debugUnlockTangPush` 保留（live 旗 debug 幫手，唔屬 soft 層）。

刪後核實：`DengLine.` 程式碼引用清零、`typeof DengLine` 清零；「鄧麗萍」只剩 live stub 路徑＋註解。
index.html 47440 → 46999 行（淨 −441）。

## 4. 測試手術（20 檔）

- **tang152**：§3「留線」改寫做「刪線」斷言；R_tang_ending 計數 1→0；刪 push mock 過濾斷言；
  §6 push mock 改「檔已刪」；釘行 normaliseTangStub152 14761→14348、stub 呼叫行 14888→14473。
- **kwan151**：§6 三 mock 改「檔已刪」；A0 關海媚 1→0（v151 註解喺 DengLine IIFE 入面一齊刪）；
  A2／A3／A6／A7／A8 改做「隨層刪」斷言。
- **delete268**：§7 檢查清單拎走兩個 MEET mock。
- **wf5_87_logic**：files 只剩 dualMock、applied 6→2、R_tang 斷言翻轉、禁詞改查 DualMeet。
- **wf5_87_static**：call site 字串更新（本身仍係 pre-existing FAIL，BASE 缺失）。
- **newspaper214**：X05 加 `_v358_allowed`（3 改＋5 刪）。
- **rom159**：6 釘行＋全佳行按內容重對；加 `_FIX358_KO`（3）＋`_FIX358`（24）兩層精確替代斷言。
- **gate136／contra98**：years66Walk 清單字串拎走 dengMock／dengPushMock。
- **text55／r297**：關海媚計數 1→0（同 kwan151 A0）。
- **gift185／tang171／tang173**：總行數 47440→46999；tang171/173 openLoc DEF 42660→42236。
- **r309**：pang_n17_cold 期望句「笑著說他想多了」→「笑著說對方想多了」。
- **r310**：ORIG_PLAYER 更新做 v358 潤飾句。
- **wf2_81**：HALF_END 對白標記門檻 10→9（R_lan_ending beats[8] 串層修正後實測 9）。
- **tang164／tang167**：R_tang_ending 計數 1→0；tang164 pushGate 斷言改「DengLine 已刪」。
- **travel114**：COUNT／FREE／DEF／WRAPPER 共 54 釘行 difflib 映射重寫（DEF 42660→42236、WRAPPER 29258→28834），內容逐行核實。
- **rom176**：5 釘行映射重寫（14834→14419、40887→40463、41237→40813、42540→42116、42701→42277）。
- **text125**：三錨點映射重寫（11304→10896、11446→11038、16403→15979）。

## 5. 驗證

- 全套 suite：見落地記錄（基線 398／9；九項 pre-existing 之外零新 FAIL）。
- Playwright 實駕（`~/workspace/linji-drive358/`）：開機正常、零 console error；
  served bytes 抽查 (b) 潤飾 8 處＋欄位串層 6 處＋soft 清理 3 處全中（19/19）。
- SAVE key（`starVolunteer_map_v19w`）／softRev 冇郁。

## 回滾

`git revert` 本版 squash commit 即還原（JSON／index.html／mock 檔／測試一併還原）。
