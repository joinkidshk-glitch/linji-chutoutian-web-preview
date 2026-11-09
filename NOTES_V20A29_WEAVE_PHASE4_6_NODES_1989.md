# NOTES V20A29 — Weave Phase 4-6：主幹內容上線 N7–N11（1989 五節點）

版本：v20a29（soft 預覽；SAVE key／softRev／?v= 不變）
範圍：三年版主幹 §2 嘅 1989 年五個節點（N7＝C7、N8＝C11、N9＝C8、N10＝C9、N11＝C10）內容上線＋呈現接通。
閘沿用 4-5 嘅 `STORY_GATE_3Y`（除一項 registry 候選補齊，見下）；呈現行返 C1–C5 同一路徑（`StoryOC.listOpen` offer → 地點頁「播事態」→ `StoryPlay` → `applyChoice`）。

## 逐節點對照（pack vs 主幹）——重要定界發現

三方對照（pack `story_detail_c1_to_c17.json`、Qwen 原規劃 `PLAN_STORY_QWEN37_FULL_v1.md`、三年版主幹 §2）結論：

- **pack 只有 C1–C5 跟 Qwen 原案／主幹；pack 嘅 C6–C17 係 soft 預覽自創嘅另一套線，同主幹大方向都唔一致**，唔係細節出入：
  - pack C7＝「拒雷勁式苛刻合約」（雷勁）≠ 主幹暴雨外景（魏詠男）
  - pack C8＝「商業片 vs 文藝線」≠ 主幹茶餐廳度橋（廖炳星）
  - pack C9＝「藍若曦擋狗仔後」（成個節點係歌手向緋聞線）≠ 主幹年尾追數（顧明輝）
  - pack C10＝「台慶位 vs 陪伴」≠ 主幹戲路定型（彭兆基）
  - pack C11＝「曝光還是層次」，locId／playerOffer 都係 None（根本未接呈現）≠ 主幹選美後台（葉敏芝）
- Qwen 原規劃同主幹 §2 逐節點核實**完全對版**（C7 魏詠男避雨亭、C8 廖炳星茶餐廳度橋 loc=cafe_cha、C9 顧明輝老式酒廊追數、C10 彭兆基慈善秀後台、C11 葉敏芝選美後台＋攜帶特定禮物）。
- 處理：以主幹為準，喺 index 側新增 `STORY_SPINE_NODES_1989` 五個完整 node object（schema 跟 pack C5：beats／choices／effects／flags），載入後由 `applyStorySpineOverrides46()`（掛 `refreshCopyPacksFromDisk` 賦值 `STORY_WIRE.main` 之後）按 id 替換 pack node。**冇直接改 content pack JSON**（守 repo 慣例）。原生移植階段要注意：移植時要連覆寫表一齊搬，或者到時回寫 pack。

| N | C | 主幹內容（今次上線） | 場地 | 抉擇 → 旗／效果 |
|---|---|---|---|---|
| N7 | C7 | 暴雨救場：黑雨外景，魏詠男避雨亭 | film_harbour 維港電影 | 落手救場 → flag_rain_rescue／信用+2／標籤「識做」；躲雨保妝 → flag_rain_shelter／聲量+1 |
| N8 | C11 | 選美後台：掩護佳麗／爆料給記者，葉敏芝 | tvb_longmen 星河電視台 | 掩護 → flag_miss_cover／信用+1／標籤「守口如瓶」；爆料 → flag_miss_leak／聲量+1／wealth+1（+$500）／標籤「八卦」 |
| N9 | C8 | 茶餐廳度橋：廖炳星隔離枱改橋 | cafe_cha 金龍茶餐廳 | 主動度橋 → flag_bing_bridge／聲量+3；做背景 → flag_bing_background／信用+2 |
| N10 | C9 | 年尾追數：顧明輝老式酒廊，何生委託 | tvb_harbour 海港廣播（場景寫台附近酒廊） | 幫何生追數 → flag_chase_for_ho／何生好感+2；替劇組出頭 → flag_standup_crew／信用+2 |
| N11 | C10 | 戲路定型：彭兆基慈善秀後台＋梟雄片試鏡 | tvb_longmen 星河電視台 | 演黑幫 → flag_role_gangster／聲量+2；演警察 → flag_role_cop／信用+2 |

標籤說明：「識做／守口如瓶／八卦」唔喺 STUB_CASTING_TAGS registry，但 `applyCastingTags` 對未註冊 label 有 fallback（id=label 照存入 S.castingTags，淡印照顯示），照用；呢三隻係質地標籤，唔入任何閘 tagAny。

## 呈現接通

- 五節點經覆寫後有齊 locId＋playerOffer 字串，入地點自動 grant offer（openLoc 既有機制）、地點頁出「播事態」掣、`listOpen({player:true})` 列入 open。C6 亦已驗：4-5 新閘下經同一路徑開 offer（回歸測試覆蓋）。
- `STORY_LOC_SOFT` 更新：C7→film_harbour、C8→cafe_cha、C9→tvb_harbour、新增 C11→tvb_longmen（同覆寫 node locId 一致，只係後備表）。
- `STORY_TITLE_SOFT`：C7→「暴雨救場」、C8→「茶餐廳度橋」，新增 C9「年尾追數」、C10「戲路定型」、C11「選美後台」。
- `STORY_HINT_SOFT`：C7–C10 四個 entry 全部重寫成主幹版，新增 C11 entry（nextHint 只作 storyFaceLine 禁字過濾用，同 node playerHint 分開寫，冇撞字串）。
- 紅星出場：魏詠男／廖炳星／葉敏芝用返 era speakerId（ngai_wingnaam／liu_bingxing／yip_manji，有 bust 資產）；顧明輝／彭兆基未有 era 資產，用 speaker 顯示名（通用剪影＋名照出）。STAR_SIGHTINGS 遠觀表今次冇郁（彭兆基原本冇 sighting entry；節點出場已接返主幹地標）。

## 閘修正一項（要 prominently 講明）

4-5 NOTES 已預告：`STORY_GATE_3Y` 嘅 tagAny 候選（「喜劇／comedy／動作／action」）對唔上 STUB_CASTING_TAGS registry 嘅真 id／label（tag_comedy／喜劇細胞／tag_action／動作演員），唔補嘅話玩家持有真標籤永遠唔中、C8／C15 永遠開唔到。今次補齊：C8 tagAny 加 `tag_comedy`、`喜劇細胞`、`tag_action`、`動作演員`；C15 tagAny 加 `tag_action`、`動作演員`。**門檻數字（信用>20／聲量>28／雙軌>70 等）一律冇改。** 邏輯測試用 registry 真形狀 {id:"tag_comedy", label:"喜劇細胞"} 驗證 C8 開到、冇標籤開唔到。

## 債權登記（favorLedger／mockCredits）

新增 `story46SettleTick()`（掛 advanceDay，喺 exodusFenTick 之後；冪等靠 mockCredits id＋ledger counted 雙重 check）：

- **credit_c7_rain「暴雨救場人情」**（債主：外景組副導演）——C7 揀「落手救場」後登記。任務說明只點名 N10，但 C7 救場結果同樣自然係「有人欠返玩家人情」，照 4-2 pattern 一併登記。
- **credit_c9_crew「年尾出頭人情」**（債主：劇組場務）——C9 揀「替劇組出頭」後登記。C9 揀「幫何生追數」嗰邊係何生好感+2，冇債權（幫老闆做嘢唔等於有人欠你），合理。
- 債權來源由 1 張（芬姐）增至 3 張，行近 E4（≥2 筆未用債權）／E5 門檻需要；E5 要債權合計≥6，仲差，留 4-8 内容補。

## C11「攜帶特定禮物」——內容層互動（取捨記錄）

主幹／Qwen C11 要求「攜帶特定禮物先做到某啲嘢」。今次做**內容層完成時互動**，唔做硬 offer 閘：玩家完成「掩護佳麗」嗰陣，`story46SettleTick` 檢查身上有冇**淡香氛樣品瓶（gift_perfume_sample，$650，items_gifts.json 既有禮物）**——有 → 扣 1 送畀葉敏芝、記 flag_miss_gift_prepared＋toast；冇 → 記 flag_miss_gift_missed，輕提示一次。節點 synopsis／playerHint／STORY_HINT_SOFT 都明文提示帶見面禮。
唔做硬閘嘅原因：引擎 offer 路徑冇 item token，落閘要焗改 4-5 閘層；而且 Qwen 原文「攜帶特定禮物」本身係抉擇輔助而唔係入場條件。日後若要升級做硬條件，flag 已齊（prepared／missed），改閘即可。

## 藍 PA 化處理結果

- pack C9 成個「藍若曦擋狗仔後」節點被主幹 C9 追數覆寫取代（運行時玩家永遠見唔到舊節點）。
- STORY_HINT_SOFT 舊 C8 nextHint「藍若曦擋狗仔後」、舊 C9 唱片／宣傳場提示已隨 C7–C10 提示重寫清走。
- 全檔逐處核實「藍若曦」出現處（去註解後）：只剩 3 處引擎基建——SP_SPEAKER_ALIAS 對照（名→speaker id）、SP_SPEAKER_LEGACY 註冊（顯示名）、送禮顯示名對照（lan:"藍若曦"）。全部只有個名，冇任何歌手向內容。另有 2 處係今次加嘅開發註解（記錄移除決定）。
- **掂唔到／唔喺今步範圍**：① content pack JSON 本身仍保留舊 C9 節點原文（慣例唔改 pack；運行時被覆寫蓋住）；② 感情線 pack `story_detail_romance_lan_xu.json`（藍嘅感情線）內容未審——藍 PA 版「差一步」屬 4-8 commit 工作，嗰陣一併審。

## 測試

- 新 `tests/test_weave46_logic.js`（43 項全過）：覆寫完整性／冪等；五節點逐個行真 listOpen offer 路徑（正確年份季節＋前置＋門檻開、未達唔開，含嚴格 > 邊界）；逐個 applyChoice 後 done＋抉擇旗＋數值；C7/C9 債權登記＋冪等；C11 禮物有／冇兩路；C1／C6 回歸。pack 用真副本 `tests/fixtures/story_detail_c1_to_c17.json`。
- 新 `tests/test_weave46_static.py`（全過）：覆寫表／掛點／tick 接線、閘候選、SOFT 表對齊、提示段歌手向清零、藍若曦出現處核實、真名掃描（兩組 QA 禁用表）、慣例不變。
- 既有全套測試（連新檔共 38 檔）全部通過；全檔 script `node --check` OK。

## 遺留

- C6 內容對齊：C6 閘已通、呈現已接，但 pack C6 內容（首次正式約會對象）同 Qwen 原案（C6 飯堂閒角）唔同——今步只驗接通，內容對齊未做（屬感情線／飯堂線範疇，建議跟 4-8 或另開票）。
- pack C12–C17 同主幹同樣對唔齊（已知 C16 係「金九舊底片傳承」vs 主幹樂壇線），4-8 預計照今次覆寫方法處理。
- C9「人情債觸發」：以何生委託＋年尾清貨期喺內容層呈現，冇入閘（閘表本身冇 debt 條件，同主幹一致）。
- 債權來源仲未夠 E5 門檻（≥6），4-8 補。
