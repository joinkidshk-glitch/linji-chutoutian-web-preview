# NOTES V20A31 — Weave Phase 4-8：主幹收束 N12–N16（1990）＋感情 commit 機制＋半線素材準備

版本：v20a31（soft 預覽；SAVE key／softRev／?v= 不變）
範圍：三年版主幹 §2 嘅 1990 年五個收束節點（N12＝C15、N13＝C14、N14＝C12、N15＝C16、N16＝C13）內容上線＋C6 內容對齊 Qwen＋曉晴／采兒 commit 機制＋半線（Vera／藍／徐）狀態準備＋程天諾預熱＋債權補充兩張。
閘沿用 4-5 嘅 `STORY_GATE_3Y`（今步冇改任何門檻數字、冇改 tagAny 候選）；呈現行返 C1–C5 同一路徑。

## 逐節點對照（pack vs 主幹）——延續 4-6 定界結論

三方對照（pack `story_detail_c1_to_c17.json`、Qwen 原規劃、三年版主幹 §2）結論同 4-6 一致：pack C12–C16 係 soft 預覽自創嘅另一套線，同主幹大方向唔一致，逐節點以主幹為準用 index 側完整 node 覆寫（`STORY_SPINE_NODES_1990`＋`applyStorySpineOverrides48()`，掛 `refreshCopyPacksFromDisk` 賦值 `STORY_WIRE.romance.lanXu` 之後——嗰陣 main 同 lanXu 都賦值完）。**冇直接改 content pack JSON**（守 repo 慣例；原生移植時要連覆寫表一齊搬或回寫 pack）。

| N | C | pack 原內容（被取代） | 主幹版上線內容 | 場地／紅星 | 抉擇 → 旗／效果 |
|---|---|---|---|---|---|
| N12 | C15 | 藍若曦聯姻逼退圈（藍家宴會） | **高危替身**：麥震東拍跳樓戲扭傷，武指搵阿偉頂高危鏡頭 | film_harbour／麥震東 | 做替身 → flag_stunt_double／聲量+3／標籤「搏命」；拒接 → flag_stunt_refuse／信用+1／標籤「惜身」 |
| N13 | C14 | 徐寶珊尊重或包養（資本場宴會） | **站隊**：收視戰下齊鎮海約打波挖角，企電視台定電影公司 | tvb_longmen（場景寫電視台附近高爾夫球會所，跟 4-6 C9「locId=tvb_harbour＋酒廊」先例）／齊鎮海 | 站電視台 → flag_side_tv／信用+2；站電影公司 → flag_side_film／聲量+2 |
| N14 | C12 | 賀歲搶位 vs 關係危機（高文瀚／高俊傑） | **樂壇前哨**：陸柏言緋聞纏身，歌迷聚集唱片公司大堂聲援 | rec_star 天星音樂／陸柏言 | 幫粉絲應援 → flag_fans_support／聲量+2／標籤「親和力」；避開狂熱粉 → flag_fans_avoid／信用+1／標籤「高冷」 |
| N15 | C16 | 金九舊底片傳承（片場倉庫） | **偶像實力之爭**：程天諾俾實力派批評靠修音；監製拉阿偉試唱和音示範帶 | rec_star（舞蹈室）／程天諾 | 靠修音 → flag_vocal_polish／聲量+2／標籤「偶像派」；苦練唱功 → flag_vocal_train／信用+2／標籤「實力派」 |
| N16 | C13 | 緋聞公關真假（周刊草稿／關海媚） | **賀歲片**：廖炳星同導演為結局鬧翻停機，阿偉嗰兩句對白點落 | film_cotton 紅棉影業／廖炳星（era speakerId liu_bingxing） | 臨場爆肚 → flag_newyear_improv／聲量+2／標籤「執生」；死背劇本 → flag_newyear_script／信用+2 |

標籤說明：「搏命／惜身／親和力／高冷／偶像派／實力派／執生」跟 Qwen 原案標籤名；唔喺 STUB_CASTING_TAGS registry 嗰啲照 4-6 先例行 `applyCastingTags` fallback（id=label 照存），係質地／終局標籤，唔入任何閘 tagAny。紅星出場：麥震東／齊鎮海／陸柏言／程天諾未有 era speaker 資產，跟 4-6 顧明輝／彭兆基先例用 speaker 顯示名（通用剪影＋名照出）。同步對齊 `STORY_LOC_SOFT`（新增 C12–C16）、`STORY_TITLE_SOFT`（新增五個＋C6 改名）、`STORY_HINT_SOFT`（新增 C12–C16 五條）。

## C6 內容對齊決定：覆寫（Qwen 定義明確）

Qwen 原規劃對 C6 有明確定義：loc=電視城飯堂、route_tv＋Week 15+、可選可長期跳過、抉擇「熬日子 (Grind)／走人 (Quit)」、僅微量金錢與電視台資歷、無實質劇情推進。pack 現行係自創約會線（約 Vera／曉晴／采兒，date_* 旗＋rel+2），唔係定義含糊，所以按任務規則覆寫對齊：
- 新 C6「飯堂閒角」（`STORY_SPINE_NODES_C6`，同 apply48 一齊套用）：處境劇班底簽固定閒角（飯堂角落嗰枱，冇台詞冇近鏡，一簽一季）。熬日子 → flag_canteen_grind／wealth+1（+$500 微量金錢，資歷寫入 notes 語義）；走人 → flag_canteen_quit／零 stats。
- 閘不變（STORY_GATE_3Y.C6＝route_tv＋weekMin 15，同 Qwen 一致）；locId tvb_longmen（電視城飯堂語境）；`STORY_TITLE_SOFT.C6` 改「飯堂閒角」；`STORY_HINT_SOFT.C6` 重寫、C5 nextHint 同步改指「飯堂閒角」。
- **連帶影響（已處理）**：舊 C6 約會 choice 係 rel +2 嘅額外來源，移除後感情線 rel 天花板由 9 降到 7（淨鏈內）——commit 門檻就係按新經濟校準（見下），唔係按舊數。

## 感情 commit 機制（`COMMIT48_NODES`／`COMMIT48_DEFS`／`commit48Available`）

- **rel 套別（實查證據）**：遊戲有兩套關係值——`S.npcs`（0–100，傾談／送禮／好感階梯用）同 `S.story.rel`（細整數）。感情內容（`story_detail_romance_*.json` 全部 meet／push／crisis 節點）嘅 choice effects 一律寫 `stats.rel_*`，經 `StoryOC.applyChoice` 嘅 `bumpRel` 入 `S.story.rel`；主線節點同理（C5／C6／C9 嘅 rel_choi／rel_ho）。**commit 門檻只用 S.story.rel，唔混用 S.npcs。**
- **門檻校準**：每條線鏈內（meet→crisis，未計 ending）rel 來源逐格實查——meet 最佳 +1、push1 +2、push2 +2、crisis +2，理論最高 **7**；次佳揀法係 0／0／1 級，負值揀法有 −1（push1 自私）／−2（crisis 鬧翻）。門檻定 **rel ≥ 6**（`COMMIT48_REL_MIN`）：容許成條鏈一次次佳（例如 meet 揀疏離 0、其餘全取＝6），但任何負值揀法都會跌出門檻——係「認真行完條線」先有資格嘅高門檻，唔使完美 7/7。（任務原文建議嘅 80 係 0–100 尺度數字；按本遊戲實際 rel 經濟換算即係呢個 6。）
- **窗口**：1990 年秋起（`choice47SeasonReached(1990, "秋")`，即主幹 §6 嘅 N15–N17 收束期；過年唔鎖死），加前置**該線 crisis 節點已 done**（R_hiu_crisis／R_choi_crisis），確保唔會提早收束。
- **呈現**：跟 4-7 微節點 pattern——曉晴喺星河電視台（tvb_longmen，廠景天台）出 offer、采兒喺金龍茶餐廳（cafe_cha，茶餐廳老位，呼應結局專檔「茶餐廳收尾」）出 offer；openLoc 行動清單 `act-priority` 入口 → 真 `StoryPlay`（force）。
- **落旗**：玩家揀「行前一步」先經真 applyChoice 寫旗——`flag_hiu_commit`／`flag_choi_commit`（跟 pack 既有先例：鄧麗萍線 `flag_tang_commit`、且 pack R_hiu_ending／R_choi_ending 嘅 HE choice 本身都寫呢兩隻旗，兩條路徑同一個旗，4-10 讀取一致）。**互斥**：任一邊已落旗，另一邊唔再出 offer。
- **「再諗下」設計**：第二個 choice 零旗零 stats；applyChoice 照樣 markDone 微節點本身，但 `commit48Available` 唔查 done，所以 offer 會留到玩家真係確認為止（唔會撳錯一次就永遠冇咗 commit）。兩個微節點經真 `newspaperStoryResolve` 驗證回傳 null，唔會誤生報紙（邏輯測試覆蓋）。
- 結局呈現（頒獎禮後台／茶餐廳收尾點寫）係 4-10 嘅事，今步只落旗。

## 半線狀態清單（Vera／藍／徐寶珊）——狀態本身齊全，冇補寫入標記

三條半線嘅 pack 鏈（meet→push1→push2→crisis→ending）本身已經有齊持久狀態：meet 旗＋`S.story.rel`＋done 標記。新增唯讀讀取口 `endingRomanceState48()`（唔寫任何狀態）畀 4-10 直接用：

| 線 | 身份口徑 | 已相遇 | 關係程度 | 進度 | commit 旗現況 |
|---|---|---|---|---|---|
| Vera | **造型師（跟 LIVE，已拍板）** | `done R_vera_meet`／`flag_vera_met_warm·cold` | `S.story.rel.rel_vera`（鏈內 0–7） | R_vera_push1/push2/crisis done | `flag_vera_commit`（pack R_vera_ending HE 寫；專檔定性半線唔入 commit，4-10 判定處理） |
| 藍若曦 | **電視台 PA／場記（已拍板）** | `done R_lan_meet`／`flag_lan_met_warm·cool` | `S.story.rel.rel_lan`（鏈內 0–7） | R_lan_push1/push2/crisis done | `flag_lan_commit`（同上） |
| 徐寶珊 | 富豪千金（pack 同專檔一致） | `done R_xu_meet`／`flag_xu_met_polite·distance` | `S.story.rel.rel_xu`（鏈內 0–7） | R_xu_push1/push2/crisis done | `flag_xu_commit`（同上） |

- **Vera**：今步冇改佢任何內容、冇寫佢嘅專屬場景（按任務範圍）。實查 pack R_vera_* 本身就係造型師版（造型間初遇／形象會議／造型間收工）；pack 入面「公關」三處全屬采兒線嘅「公關切割」抉擇字眼，同 Vera 身份無關。佢嘅「差一步」場景之後按造型師身份寫（4-10）。
- **徐寶珊**：pack R_xu_*（春茗／商場活動／私人飯局／包廂條件）同專檔「富豪千金」一致、零歌手向內容，唔使覆寫（邏輯測試有斷言 R_xu_meet 冇被覆寫）。

## 藍 PA 化處理（逐處）

`ROMANCE_LAN_PA_OVERRIDES` 覆寫 lan_xu pack 全部五個 R_lan 節點嘅文字層，結構層（node id／phase／openConditions／openConditionsAny／artId／romanceLine／arcBeat／choice id／effects 嘅 flags＋stats／flags_written）同 pack 逐項一致（邏輯測試有 deep-compare 斷言）；**冇改 pack JSON**。

| 節點 | pack 歌手版（被取代） | PA 版上線 |
|---|---|---|
| R_lan_meet | 唱片店外的傘（狗仔追訪、借傘掩護） | **通告牌下的人**：廠景門口撞散通告牌，幫手執牌撳牌 |
| R_lan_push1 | 錄音室的半首歌（台慶合唱綵排、教唱咬字） | **台慶嗰版通告牌**：台慶綵排幫佢對成版通告牌出場次序 |
| R_lan_push2 | 假戲與真話（公司要兩人認拍拖宣傳、緋聞） | **走廊的風聲**：茶水間傳佢「偏幫」阿偉排好位，企出嚟定劃清界線 |
| R_lan_crisis | 豪門側廳的條件（藍父聯姻、陳家公子） | **調組令**：外判公司高薪挖角＋屋企催轉穩陣文職，陪佢爭取留低定勸佢為前途行 |
| R_lan_ending | 晨光與登機證（推婚事、雪藏、離港） | **最後一版通告牌**：年尾大騷煞科，佢照舊幫阿偉撳牌＋「第日請返我食飯」約定（呼應專檔 PA 版差一步場景） |

- choice effects 嘅 `notes` 屬玩家可見文字，一併改寫（原「合唱推進」「假戲／狗仔後護航」「助抗聯姻」等）；flags／stats 數字原封不動。
- **遺留旗名說明**：`flag_lan_sang_together`（原「合唱」）同 `flag_family_marriage`（原「聯姻」）係 pack 既有狀態旗名，ocAny 鏈同舊存檔都引用緊，唔改名；PA 版入面佢哋只係鏈上標記，唔再代表唱歌／婚姻內容。`flag_family_help` 同理由保留。
- 玩家面歌手向掃描：五節點文字層（標題／場景／synopsis／beats／choice label／effects notes）零「唱片店／錄音室／合唱／狗仔／緋聞／聯姻／豪門／退圈／登機證／玉女／歌手」（邏輯＋靜態測試雙覆蓋）。

## 程天諾預熱（主幹 §5）

`PAPER_SIDE_ITEMS` 原有 1 則程天諾花邊（汽水廣告，fromYear 1990，Phase 1-1 已入池）。今步加 2 則（同樣 fromYear:1990、純氛圍、唔入 SIDE_PAPER_FRAGS 拼合）：「舞蹈室練到半夜」（埋舞蹈室＋苦練線）、「實力派前輩公開批評程天諾靠修音」（埋 C16 修音爭議）。1990 年花邊池入面程天諾共 3 則，N13–N14 期間（1990 夏–秋）報紙輪替自然會撞到，N15 出場前「未見其人先聞其名」。邏輯測試行真 `paperSideItemForDay`：1989 全年零程天諾、1990 全年出齊 3 則。

## 債權補充＋E5 帳面估算

新增 `story48SettleTick()`（掛 advanceDay，喺 story46SettleTick 之後；跟 4-2／4-6 pattern 雙重冪等）：
- **credit_c15_stunt「高危替身人情」**（債主：動作組武指）——C15 揀做替身後登記。（拒接嗰邊係惜身口碑，冇人欠你，唔登記。）
- **credit_c13_newyear「賀歲片頂場人情」**（債主：賀歲片場務組）——C13 揀臨場爆肚後登記。（死背劇本係交貨本份，唔登記。）
債權來源累計 5 張：芬姐（1989 夏轉絕響）＋C7＋C9＋C15＋C13；**未絕響持有上限 4**。

E5 條件＝`favorLedgerCounts()` 嘅 settled＋creditsHeld ≥ 6 ＋何生 rel 高。settled 來源盤點：教學債 debt_ho_tutorial（+1）、芬姐債勾銷（+1）、SEASON_COLLECT 季節卡 8 張（id 固定、跨年唔重複計，全清 +8）、其他事件債還清（唔入保守估算）。估算（去到 1990 冬結局時）：
- 人情線認真型玩家：settled ≈ 7–10（教學＋芬姐＋季節卡 5–8）＋ held 3–4 ＝ **10–14 ✓ 餘裕達標**
- 中等投入：settled ≈ 4（教學＋芬姐＋季節卡 2）＋ held 2 ＝ **6 ✓ 啱啱達標**
- 唔碰人情系統：settled ≈ 2 ＋ held 0–1 ＝ 2–3 ✗（設計上正確：E5 係人情網專屬結局，唔應該白送）
結論：加完兩張之後 E5 對目標玩家群可達而且唔濫，**唔需要再補**；4-10 判定嗰陣照 `favorLedgerCounts()` 讀即可。E4 救回條件 creditsHeld ≥ 2 由 C7（1989 夏）起已可累積，節奏合理。

## 測試

- 新 `tests/test_weave48_logic.js`（66 項全過）：覆寫完整性／冪等；藍 PA 結構層 deep-compare＋文字層零歌手向＋徐線無被動；五節點逐個行真 listOpen（條件齊開、抽走關鍵條件唔開，含 C14 信用=42／C12 聲量=50／C16 雙軌=125 嚴格邊界）＋真 applyChoice 旗／數值／標籤；C15／C13 債權 tick＋冪等；C6 真路徑（route_tv＋W15 開、C6_a 微量金錢、C6_b 旗）；預熱真 picker 年份閘；commit 全矩陣（窗口外／未入秋／rel 5／rel 6 邊界／crisis 未做／互斥／確認落旗／再諗下唔落旗兼 offer 留返／真 newspaperStoryResolve 回 null／endingRomanceState48 讀取）；C1／C7 回歸。fixtures 新增 romance 兩包真副本。
- 新 `tests/test_weave48_static.py`（134 項全過）：覆寫表／掛點次序／SOFT 表對齊／閘數字不變／commit 把關欄位／藍 PA 掃描／真名雙表掃描／慣例不變。
- **舊測試更新兩處（申報）**：① `test_weave32_logic.js` 花邊池大小斷言 18 → 20（訊息同步註明 v20a31 預熱×2；呢條斷言歷來隨池增長逐次更新）；② `test_weave46_static.py` 兩處藍斷言按新現實調整——STORY_HINT_SOFT「C7–C11 段」範圍收窄到 C15 entry 之前（C12／C16 提示正當引用「唱片公司」場地，唔關藍事），同「藍若曦出現處」放寬到「引擎基建＋PA 覆寫表」（藍感情線已上線，個名正當出現喺 PA 內容），兩處語義（C7–C11 零歌手向殘留／藍若曦零歌手向 framing）保留不變，改動處有註解。
- 既有全套連新檔共 **42 檔全過**；全檔 script `node --check` OK；index.html 2,250,926 → 2,305,418 bytes。

## 遺留／取捨

- C14 場地：遊戲冇高爾夫球場 loc，locId 用 tvb_longmen＋setting 寫明會所外約（同 4-6 C9 酒廊先例）；齊鎮海係電視台一哥，喺電視台出 offer 合理。
- pack R_*_ending 五個節點（含 flag_*_commit 寫入）維持原狀冇郁：佢哋嘅 phase_P5 閘喺三年版係 1990 冬可達，HE 路徑寫入嘅 commit 旗同本機制同名一致，唔會打架；半線三條嘅 ending 旗語義（專檔定性唔入 commit）留畀 4-10 判定層處理。
- C17（N17）內容同結局系統係 4-10；C6 舊約會線嘅 date_* 旗由今步起唔再有新寫入（舊存檔已有嘅旗唔清除、冇系統再讀佢哋做閘）。
- 原生移植提醒：`STORY_SPINE_NODES_1990`、`STORY_SPINE_NODES_C6`、`ROMANCE_LAN_PA_OVERRIDES` 三張覆寫表要連同 4-6 嗰張一齊搬，或者到時回寫 content pack。
