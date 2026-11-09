# NOTES V20A33 — Weave Phase 4-10：結局系統（三軸總帳制）

版本：v20a33（soft 預覽；SAVE key／softRev／?v= 不變）
範圍：Phase 4 最後一步。結局設計專檔 `linji-endings-design.md` 全面落地：純函數判定 `resolveEnding410`（事業軸 §2 判定表）＋取代舊 C17 十檔任揀（覆寫做前夕場景）＋相鄰規則前夕抉擇（§3）＋呈現組裝（§5：場景→事業→感情→去留→個人化插入→手帳總結頁＋稱號卡＋差啲嗰條路）＋`S.ending410` 持久保存。判定閘沿用 4-5 嘅 `STORY_GATE_3Y.C17`（C13 done＋1990 冬，yearEq），**冇改**。

## 1. 判定表對照（resolveEnding410 vs 專檔 §2）

純函數、唯讀、無副作用（邏輯測試有 deep-equal 斷言）。上而下命中即停：

| 優先 | 專檔 | 實作 |
|---|---|---|
| E6 退圈 | 只限玩家主動入口 | 只認 `opts.quit`（"job"／"leave"）；旗（flag_family_job_accept 等）本身**唔會**令純函數入 E6（測試覆蓋）。版本：job→安穩、leave→遠走、原判定 E4＋job→心灰 |
| E1 天王接班 | 聲量≥60＋信用≥55＋雙軌≥125＋負標籤≤1 | 照表（`ENDING410_T`） |
| E4 泡沫偶像 | 聲量≥50＋信用<30；債權 ≥2 未用→沉唔死版 | 照表；variant=rescued／sunk（門檻照用戶拍板 ≥2，冇放寬） |
| E2 甘草王 | 信用≥42＋聲量≥35 | 照表 |
| E3 幕後之路 | 信用≥42＋（導演 rel 高 或 幕後標籤≥2） | 「導演 rel 高」定為 ≥60；幕後標籤關鍵字表同 4-9 `TRAJ49_TAG_SETS.backstage` 同表（`ENDING410_BACKSTAGE_KEYS`），逐標籤計 |
| E5 江湖撈家 | 已清債＋持有債權 ≥6＋何生 rel 高 | settled＋creditsHeld ≥6（`endingFavor410` 唯讀鏡像）；「何生 rel 高」定為 ≥60（好感階梯內幕級） |
| E0 浮沉未定 | 預設 | 照表 |

**判定唔用 `trajectoryOf49`**（嗰個係 4-9 呈現分類；靜態測試斷言 resolve 函數體內冇引用佢）。軌跡只用喺呈現銜接：個人化插入嘅「報紙最後稱呼」（`newspaperTrajRef49`）。

### 負標籤清單（`ENDING_NEG_TAGS410`，對照實際標籤集）

專檔原文「大牌／八卦／爛片類標籤」。逐一查實際可得標籤（registry `STUB_CASTING_TAGS_v1`＋全部節點／通告 `tags`／`tagOnComplete` 來源）後定清單＝精確命中（label 或 id 全等，唔用子串免誤傷）：

- **八卦**：C11 選美後台爆料抉擇嘅標籤（真實可得）。同源旗 `flag_miss_leak` 做兜底：標籤唔喺度嗰陣以旗計 1，唔雙計。
- **高冷**：C12 避開狂熱粉抉擇嘅標籤（真實可得；屬「大牌類」難親近形象印）。
- **大牌／爛片**：專檔原詞。現行內容未有同名標籤（「大牌」只喺 WEAK_MARKS 耳語池、唔入 castingTags），先入清單備用，日後內容加同名標籤即刻生效。

效果：現行內容入面負標籤實際上限係 2（八卦＋高冷），E1 嘅 ≤1 即係「兩樣唔可以齊犯」，同設計強度吻合。

### 讀數口（純函數嘅唯讀鏡像）

`favorLedgerCounts()` 經 `ensureFavorLedger()` 會做一次性 backfill **寫入**，唔可以直接喺純函數入面用。所以判定層用兩隻唯讀鏡像，來源同生產讀口逐項相同，邏輯測試有交叉對照斷言（同一狀態下數值一致）：

- `endingFavor410(st)`：settled／exodus 讀 `st.favorLedger`、creditsHeld 數 `st.mockCredits` 未絕響數、exodusNames 由 mockCredits 嘅 debtor 解名（fallback 表含 `credit_fen_rescue`→副導演芬姐）。
- `endingRomance410(st)`：鏡像 `endingRomanceState48()`（`S.story.done`／`rel`／flags）。半線（Vera／藍／徐）就算 pack R_*_ending 寫過 `flag_*_commit`，按專檔定性**唔入 commit**，只做差一步素材（判定層處理，同 4-8 NOTES 預告一致）。

## 2. 可達性審計（按 LIVE 信用公式，結論：全部可達，冇改任何門檻）

信用公式（`dualTrackNumbers`，4-9 已查實）：信用 ＝ round(0.5×聲量 ＋ 0.3×台風 ＋ 0.2×演技 − 壓力罰) ＋ industryCreditDelta。逐結局驗算：

- **E1**：雙軌 ≥125 令有效門檻係「聲量＋信用 ≥125」——同主幹 N15（C16）閘 `dualGt:125` 同一個數，即係設計本身預咗打通 C16 嗰班人就係 E1 候選。例：聲量 70＋台風 45＋演技 40＋delta 4 → 信用 61、雙軌 131 ✓；聲量 60 路線要台風／演技約 70（ dedicated 練功型）先到信用 65。最難但數學上成立，符合專檔「命中率 ≤10%」定位。
- **E4**：聲量 55＋台風／演技近 0 → 信用 28 <30 ✓（齋谷聲量唔練功型）。注意信用有 0.5×聲量托底，所以 E4 嘅存在本身就要求玩家幾乎唔練台風演技、唔揀信用向抉擇——係一條真實存在嘅玩法線，唔係死結局。
- **E2**：聲量 40＋台風 50＋演技 35 → 信用 42 ✓（中段穩陣型，專檔分佈目標主力）。
- **E3**：信用 ≥42 可由 E2 同一數段達到（例聲量 30＋台風 60＋演技 50 → 信用 43），分流靠導演 rel ≥60（傾談／劇情可累積）或幕後標籤——registry 暫無幕後標籤，現行實際入口係導演 rel 線，同 4-9 鏡像結論一致。
- **E5**：4-8 已估算 settled＋creditsHeld 中等投入＝6 啱啱達標、認真型 10–14；何生 rel ≥60 靠傾談／送禮／劇情累積 ✓。
- **E0**：預設，恆可達。**E6**：玩家主動，恆可達。

**校準：冇。** 專檔門檻係按「雙軌」概念寫，而 LIVE 信用公式（聲量托底）令各門檻嘅實際難度同專檔分佈目標（§7：E1 ≤10%、E2/E3 主力、E4 約 10–15%、E0 ≤25%）方向一致；唯一要留意係 E3 嘅標籤入口暫時係空嘅（靠導演 rel 單線），日後內容加幕後標籤嗰陣唔使改判定。

## 3. 舊 C17 處理（取代十檔任揀）

- `STORY_SPINE_NODE_C17_410`＋`applyStorySpineOverrides410()`（掛 `refreshCopyPacksFromDisk`，喺 apply48 之後）按 id 替換 pack C17。舊節點嘅 `endings_catalog`／十個 `C17_e*` choices（`endingId` E01–E10）玩家唔再到達得到（邏輯測試斷言覆寫後節點冇 `endingId`、冇 E01 字串）。冇改 content pack JSON。
- 同步對齊 `STORY_LOC_SOFT.C17="tvb_longmen"`、`STORY_TITLE_SOFT.C17="三年收科"`、`STORY_HINT_SOFT.C17`。
- **舊存檔相容**（邏輯測試覆蓋）：① C17 未 done（offer 狀態，含舊 pack C13 已 done）→ 新節點照樣經真閘開到、行到新流程；② C17 已 done（舊十檔揀過、`ending_e01`＋`career_lock` 旗在帳）→ 節點維持 done 唔重播，所有新函數唔 crash，總結頁出「未收科」保底版；③ 已入 1991+ 嘅舊五年節奏存檔過唔到 yearEq 1990 閘——嗰個係 4-5 三年版事件閘嘅既定設計，唔喺今步改動範圍。

## 4. 前夕場景＋相鄰選項生成規則（`endingEveOptions410`）

呈現路径：地點（星河電視台）→ listOpen 真 offer →「播事態：三年收科」→ `StoryPlay.start` 內 C17 hook（跟 C1 `softCanonC1Face` 先例）用 `ending410EveNode()` 按當下狀態重建節點：beats 用覆寫骨架，**原判定係 E4 嗰陣插入形象危機拍**；choices 由選項生成函數即場砌（每個 choice 帶 `ending410Key`）。揀完 `StoryOC.applyChoice` 真寫旗＋markDone，跟住 `pickChoice` 內 C17 hook 將流程交畀 `ending410AfterEveChoice` 組裝呈現，唔行通用結算 modal。eve 旗（`flag_ending410_*`）經真 `newspaperStoryResolve` 驗證全數回 null，唔生報紙。

選項集合（按狀態生成，唔寫死）：

| 選項 | 出現條件 | 效果 |
|---|---|---|
| natural 順其自然 | 永遠 | 照原判定 |
| quit_job 接穩陣工 | 永遠（有 `flag_family_job_accept` 嗰陣改標籤做「嗰份工仲等緊你」） | E6（安穩／心灰版）——文案明文寫「揀咗就唔再係呢行嘅人」 |
| quit_leave 移民離場 | `flag_leave_mind` | E6 遠走版 |
| to_backstage 轉幕後 | (E4＋債權<2＋幕後差少少：標籤 ≥1 或導演 rel ≥40) 或 (E2＋合 E3 資格) | career 改 E3，variant 記低來源（由泡沫轉幕後／前夕轉幕後） |
| to_support 爭男配 | E3＋合 E2 資格 | career 改 E2，variant「前夕爭男配」 |
| leave_follow 跟住去 | `flag_leave_mind`＋原判定 E0／E2 | 事業不變，exodus 轉 leave |

相鄰紀律：除 quit（專檔明文嘅主動離場，任何結局可入）之外，選項只准將事業結局搬去圖上相鄰一格（E4→E3 係任務／專檔 §3「被拉返起身只可去 E2 方向」嘅幕後變體——唔上幕前、只入幕後，喺 NOTES 明文申報呢個取捨：E4 沉底嗰陣畀嘅唔係翻身做甘草王，而係轉幕後重新嚟過，格數仍然係一格）；E1／E5／E6 向嘅跳格選項永遠唔生成（邏輯測試逐態驗證）。

## 5. 呈現組裝（專檔 §5 順序）

`ending410AfterEveChoice` 計最終結局（base＋前夕覆寫）→ 寫 `S.ending410` → modal 逐頁：

1. **事業場景**（`endingCareerScene410`）：E0–E6 各一段專屬場景（約 150–280 字）；E4 兩版分開寫（沉唔死＝債權人逐個企返出嚟；真沉＝靜到冇電話＋留 1991 懸念句唔寫死）；E6 三版（安穩茶餐廳／遠走執行李／心灰）；場景主場跟 `route_film`／`flag_side_film` 切電影／電視頒獎禮；E1／E2 加高俊傑回收句（`rival_gao_hard` 對台舉杯／`rival_gao_endure` 和解）；**關海媚只喺 E1／E0 場景角落以「嗰位當紅花旦」稱號遠觀回收，冇出名、唔係感情對象**（ QA 禁用掃描覆蓋成個新 block）。
2. **感情收尾**（`endingRomanceScene410`）：commit 曉晴＝頒獎禮後台（文案按事業高低分兩句）、commit 采兒＝金龍茶餐廳老位首尾呼應；差一步三段專屬、唔共用範本——Vera 造型師版（後台整理領口妝髮、手停喺領口，跟專檔現行文字）、藍 PA 版（收尾加班戲撳通告牌＋「請返我食飯」約定）、徐寶珊版（送買唔起嘅禮物／回擋記者嗰次，扯平但門不當戶不對）；未 commit 嘅曉晴／采兒各有自己嘅差一步短段；全低＝孤身獨白（唔寫慘）。差一步觸發＝已相遇＋rel ≥4（滿 7），同分按完整線優先序取最高 rel 嗰條。
3. **去留收尾**（`endingExodusScene410`）：留＝1991 第一張通告（畫面感、唔出字）；走＝茶餐廳最後一餐＋啟德；未表態＝留白；玩家留低＋有人絕響嗰陣加送機段（送芬姐）。
4. **個人化插入**（`endingInserts410`，五項有先寫）：最高關係 NPC 一句回收（`S.npcs` 最高嗰位點名）、人情帳最大筆（未清債點名邊個／冇債就點名最大持有債權）、芬姐絕響回收（exodus 含芬姐先出）、屋企回收（接穩陣工→阿媽嗰句／有剪報回音→電話簿字條／否則煲湯）、報紙最後稱呼（軌跡稱呼／點名級別）。
5. **手帳總結頁**（`endingSummaryHtml410`）：稱號卡（事業名・去留詞，如「甘草王・留下來的人」）、事業結局名＋版本、雙軌最終數、人情總帳（已清／持有／絕響數）、「邊啲人走咗」名單（exodus 解名清單）、感情一行、去留一行、**差啲嗰條路**（`ENDING410_ADJ_RUMOR` 按結局一句傳聞口吻，二週目餌，只喺總結頁出）。總結頁喺手帳**剪報頁**頂部有常駐卡（`renderClippingsPane` 注入＋重睇掣 `showEndingSummary410`），收科後隨時重睇。

`S.ending410` 結構：`{ career, careerVariant, romanceLine, romanceKind, exodus, title, eveKey, day, fame, credit, dual, settled, creditsHeld, exodusNames[] }`。結局後唔鎖檔：C17 done 之後唔再 offer、流程唔重彈（`ending410AfterEveChoice` 有冪等守衛：已有 `S.ending410` 只重開總結頁）；玩家照常 freeplay。

## 6. 測試

- 新 `tests/test_weave410_logic.js`（56 項全過）：判定矩陣（E1／負標籤擋 E1／E4 兩版／E2／E3 兩入口／E5／E0／E6 三版＋旗唔自觸發／純函數 deep-equal）；讀口交叉對照（favor／romance 鏡像 vs 生產函數）；覆寫完整性＋冪等；閘矩陣（1989／C13 未 done／齊備）；相鄰選項矩陣（差少少邊界 39 vs 40、債權 2 唔出、leave_follow 只限 E0/E2 等）；全流程真呈現（真 listOpen→真 eve 節點→真 applyChoice→組裝三頁齊＋落檔＋冪等＋done 後唔再開）；E4 危機 beats＋行一格落 E3；leave_follow 事業不變；舊存檔 A／B 相容。
- 新 `tests/test_weave410_static.py`（全過）：判定表數字、負標籤清單、hooks 接駁、相鄰條件字串、呈現函數齊全、S.ending410 落檔＋冪等守衛、剪報頁重睇卡、4-10 新 block 真名＋QA 禁用掃描（關海媚／陳淑芬／施南生／Ho哥）、三段差一步專屬字串、慣例不變。
- **舊測試更新兩處（申報）**：① `test_weave46_static.py` 藍若曦出現處斷言放寬包含 4-10 結局 PA 版差一步場景嗰句（以「撳住個通告牌」標誌句識別；「零歌手向」嗰半保留不變）；② `test_weave49_static.py` 「no ending resolver」斷言由全檔收窄到 4-9 區塊內（4-10 已按規劃喺自己區塊落地 resolver；預兆≠判定嘅邊界語義保留）。兩處改動處都有 v20a33 註解。
- 既有全套連新檔共 **46 檔全過**；全檔 script `node --check` OK；index.html 2,315,391 → 2,357,880 bytes。

## 7. 遺留／取捨

- E4→E3 前夕選項同專檔 §3 圖「E4 只可去 E2 方向」嘅對照：今次按任務定義行「轉幕後」變體（唔翻身做幕前甘草、只入幕後班底），格數守一格；如果日後要嚴格跟圖，可將呢格改做「債權人拉你去做甘草配角」E2 變體，判定同呈現位都已預留（variant 欄）。
- 感情軸「送人走」（專檔 §4.2）以絕響送機段呈現（芬姐），感情線人物移民未有獨立事件，冇硬造。
- 舊五年節奏存檔（已過 1990）入唔返 C17 事件閘，屬 4-5 既定設計；嗰類存檔唔 crash、其他系統照行。
- 原生移植提醒：`STORY_SPINE_NODE_C17_410` 同判定／呈現成組函數（resolveEnding410 等）要一齊搬；`S.ending410` 係新增存檔欄位（可選、舊檔冇都行）。
