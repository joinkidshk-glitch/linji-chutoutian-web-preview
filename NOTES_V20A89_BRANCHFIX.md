# NOTES V20A89 — 分支補完 S+M（BR89）

基底 v20a88（5,237,050 bytes）→ v20a89（5,288,711 bytes）。SAVE key／softRev／產品 `?v=` 全不變；
唔直改 pack JSON（新節點行注入、情報行註冊表 runtime push）；判定門檻（E1–E7／E5 閘／頒獎線）一概冇郁，
ending 相關只做呈現分版。關海媚冇入任何新回收。

## 逐項完成清單（對返 `linji-branch-audit.md` 編號）

### S 級接線
1. **WF1 第三抉擇三旗**：
   - `flag_rain_split`（C7_c 分工救場）→ 魏詠男巧遇「記憶前置」：再遇時佢會認返嗰次分工救場（一次性，真對白分版）。
   - `flag_mediate_gu_debt`（C9_c）→ 顧明輝借錢節拍 `gu_loan` 開頭分版對白（經 `enc87StoryFlag` 雙庫讀取）。
   - `flag_newyear_twotakes`（C13_c）→ 結局回望句（ECHO89）。
2. **C18/C19 四旗**（studio_dream／steady_craft／gamble_observe／gamble_quiet）→ 結局回望四句。
   冇入 E3 判定（紅線：唔郁門檻），喺報告註明。
3. **WF3/WF4 對白旗群**：
   - 何生提點（ho_steady／ho_asked）、方小龍傾談（fong_craft／bold／trust）→ 手帳人脈頁「對手・導師」段附加狀態句。
   - M27 表態（m27_stand／quiet）→ 結局回望句。
   - 芬姐相識（fen_tea／fen_help）→ 《啟德送芬姐》送別對白真分版（`wf4FenFarewellNode` 開頭按旗加拍）。
   - 芬姐送別（fen_redpacket／fen_quiet）→ 結局回望分版句。
4. **巧遇 grants 條件派發**：`liu_repay`／`mak_respect` 兩個 beat 移除無條件 `grants`，改經
   `enc79ChoiceFx`→`enc79RunChoiceFx` 按抉擇派：應承先派返原本嗰筆債權（id／debtor 逐字不變）；
   推辭改派風聲卡 `rumor_liu_priority_passed`；老實講會驚唔派（fav 數值原樣保留）。
5. **半線結局呈現 he/be 分版**：`endingRomanceScene410` Vera／藍／徐寶珊三線各三版
   （be＝親手放下新寫版、he＝原版＋留白句、冇去到嗰幕＝原版）；曉晴／采兒 almost 版同步分版；
   鄧麗萍唔入感情軸判定（既定定性），補結局回望 he/be 兩句。
6. **齊鎮海 C16 beat（chai_repay）**：v87 已用 `enc87StoryFlag` 雙庫讀取修好——本包核實在位，冇重做。

### M 級
7. **ripple 消費者**（`applyChoice`）：C1–C5 `effects.ripple` 逐欄機械兌現，只兌現文案有寫嘅：
   stressDelta→壓力、healthDelta→體能、creditDelta→業內信用（行既有 industryCreditDelta 路）、
   debtDelta>0→真入一筆何生人情債 `debt_c4_ho_ripple`（可還、入帳本、計結局人情）、
   tag→沉澱標籤。描述欄（mapTilt／statTilt／rivalAttitude／bondDepth／intelShare）唔入數：
   路線由 route 旗＋C6／C6F 承載、態度由 rival 旗承載、羈絆由 rel 承載。
8. **C1 route_film 對稱下游**：新節點 **C6F《片場跟班》**（獅子山製片、大製作固定跟班；
   同 C6 等量級：W15＋route_film 閘、接＝wealth 1／唔接＝零、注入器跟 WF1 慣例），
   註冊齊：STORY_GATE_3Y／STORY_LOC_SOFT／STORY_HINT_SOFT／STORY_TITLE_SOFT／進度頁 order71（第 20 幕、C6 正後）。
   playerHint 誤導：嗰句「影響後續地圖與數值傾斜」TEXTFIX55 已改寫做「會影響你之後多喺邊頭出現、識到咩人」——
   C6F 落地後陳述對兩條線都成真，冇再改字；C5 nextHint 改兩線並陳（唔再只提飯堂閒角）。
9. **對手／導師八線回收**：
   - 結局呈現：`endingInserts410` 加 ARC_END89——24 隻 ending 旗逐旗一句收科回顧。
   - 手帳狀態句：人脈頁加「對手・導師」段（八線齊：未開始唔出、進行中一句、收科按抉擇出句）。
   - **A_ho 線寫返 `S.npcs.agent`**：HO89 表逐幕細額（meet +1／push1 企硬 +2／push2 信任 +2／
     crisis 賭大 +3・行開 −3／ending +6・+3・−4），同 E5 閘咬合，唔取代日常事務所儲分路。
   - standing→popularity：冇順理成章嘅門檻讀取位，按指示冇硬造新貨幣，喺手帳狀態句呈現。
10. **情報卡 13 張全接下游**：
    - 新拼合 2 對：駱家聲（grudge＋music→`rumor_lok_highlevel_truth`／`intel_lok_truth`）、
      鍾楚凝（canada＋advice→`rumor_chung_farewell_truth`／`intel_chung_leave`），連情報旗＋使用點。
    - 單卡使用點 6 張（pang_show／so_ad／chai_tv／chung_director／ching_rehearse／gu_comeback）：
      持卡即喺通告卡出情報行、巧遇出提示行（`INTEL_CARD_USE_POINTS89`）。
    - `rumor_ngai_stunt_tip`→情報通告《鐵血柔情》替身缺位（持卡先上板）。
    - `rumor_gu_money_heard`→`gu_loan` 前置旁白（知佢撲水先借）。
11. **提攜具名兌現＋人情債中段兌現位 ×4**：陸柏言／彭少祺／程天諾 patron 債＋廖炳星 priority 債，
    持有期間各開一張引薦通告（`BR89_GIGS`，持債先上板）；殺青標記兌現（`redeemedBy`＋line 交代，
    **status 唔郁**——`endingFavor410` 計數口徑原封不動）；結局頁點名邊位提攜過你。
12. **附帶清埋**（lint 揭出、審計範圍外）：主幹態度旗 14 隻（C6–C15：role_cop／gangster、fans 三旗、
    bing 兩旗、chase_for_ho、miss_deflect、stunt_refuse、canteen 兩旗、rain_shelter、newyear_script）
    入結局回望 ECHO89（上限 3 段）；`flag_family_job_decline` 入屋企段分版；C6F 兩旗同法回收。

### dead-flag lint（流程防再犯）
- `tests/test_br89_deadflag_lint.js`：掃 pack＋index 全部抉擇寫入旗（257 隻），冇 gameplay 讀取位
  又唔喺白名單（`tests/br89_flag_whitelist.json`，逐條註明理由）即 FAIL。
- 反證：對 v88 基線行 → **83 隻死旗**（審計點名嗰批全中）；v89 → **全綠**（238 有讀取／19 白名單）。

## 覆核評級（審計三級口徑，只計受影響範圍 ~66 個抉擇）
| 組 | 數 | 變化 |
|---|---|---|
| C1_b 電影支 | 1 | C → **A**（專屬節點＋閘＋進度頁，同 TV 支等量） |
| ripple 組（C2–C5，C5_b 除外） | 7 | B → B（承諾由假變真；C4_a 升 B+：真債入帳本） |
| WF1 第三抉擇（rain／mediate） | 2 | C → B（後續內容分版） |
| 八線 ending 抉擇 | 24 | C → B（結局呈現＋手帳狀態；A_ho ending 3 個 B+：兼入 E5 閘輸入） |
| 半線 ending 抉擇（vera／lan／xu／tang／hiu／choi） | 12 | C → B（結局呈現分版） |
| 芬姐相識抉擇 | 2 | C → B（送別真對白分版） |
| 巧遇 grants 抉擇（liu／mak） | 4 | B(假) → B(真) |
| 呈現型（newyear／C18・C19／WF3／芬姐送別） | 14 | C → C+（結局回望／狀態句） |
受影響範圍新分佈：**A 1／B 51／C+ 14／C 0**。全遊戲總分佈要全量重審先有，冇喺度估。

## 驗證
- 邏輯測試 `test_br89_logic.js` 47 斷言全 PASS；對 v88 行 20 FAIL（反證）。
- 全套 tests A/B：基線（v88）95 PASS／12 FAIL（環境性）；v89 **98 PASS／12 FAIL**（同一批環境名單，零回歸）。
  有意改版斷言原位註明：ux68／poster85 檔量守衛（有意增長）、weave48 C5 nextHint、wf1_80 進度次序。
- 真 UI 實駕（槽 3，證據 `verify89/`）：四條路全 PASS、pageerror 0——
  R1 C4 拒單→債入帳＋信用 10→9；R2 進度頁有《片場跟班》、獅子山播到＋落旗＋done；
  R3 人脈頁「對手・導師」段出高俊傑收科句；R4 持提攜債→維港電影通告欄有引薦試鏡卡（data-gid 核實）。

## 自作判斷清單
- C18/C19 旗唔入 E3 判定（守紅線），改接呈現下游。
- 提攜兌現唔改 credit status（守 E4/E5 計數），用 redeemedBy＋line 文字。
- healthDelta 映射體能（遊戲冇 health 欄）；debtDelta 只做正數（文案冇負債承諾）。
- A_ho npcs 數額細額自訂，方向跟各幕文本；唔取代日常儲分。
- he 版只加留白句、唔斷言劇情冇講過嘅事；be 版按 WF2 各線專屬理由寫。
- 白名單 19 條：孖旗（主旗已讀）／meet 態度副旗（主旗已讀）／結局流程內部標記，逐條有理由。
