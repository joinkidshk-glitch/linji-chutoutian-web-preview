# 《臨記出頭天》WIRING_DRAFT_v1

> **版本：** v1  
> **時間：** 2026-11-02（Asia/Hong_Kong）  
> **對齊：** `PLOT_MASTER_PLAN_v1.4-DS.md`、`PLOT_DETAIL_UNLOCK_v1.md`、`SOFT_NITS_FIX_v1.md`  
> **性質：** 引擎／原型接線表（旗標・節點・條件・消費順序）；**不**產新對白、**不**做年庫、**不**出圖、**不** Soft 重寫。

---

## 1. 目的／範圍／非目標

### 目的

將已落地的 story JSON 與解鎖規劃，對齊為 Phase1 原型及後續引擎可直接掛載的 wiring 表：節點 id、出現條件、寫入旗標、主線／衝突掛鉤、缺口清單。

### 範圍

- 主線 `C1`–`C17`（`story_detail_c1_to_c17.json`）
- 感情線 Pack1／Pack2／鄧麗萍正式線（含 stub 相容）
- 對手／導師 Pack3（8 弧 × 5 節 = 40）
- `gigs_1988.json` 標註欄如何餵 Phase1 通告板
- 旗標註冊表、不一致項、建議消費順序

### 非目標

- 不寫新對白／synopsis；不改 Soft 已定稿文案本體
- 不做 1989–1992 年庫
- 不出圖；不 publish；Soft ≠ PASS
- 不發明 UNLOCK 未寫的數值門檻（凡方向性門檻標「方向性／playtest」）

---

## 2. ID 慣例

| 前綴／形態 | 用途 | 例子 |
|---|---|---|
| `C1`…`C17` | 主線節點 id | `C7` |
| `C_*`（choice） | 選擇支 id（感情／對手弧多用此前綴） | `C_vera_meet_warm`、`C_ko_meet_grab` |
| `C1_a` 等 | 主線選擇支（節點 id + 字母） | `C5_a` |
| `R_*` | 感情節點 id | `R_lan_crisis`、`R_tang_meet` |
| `A_*` | 對手／導師／友情／資本弧節點 | `A_ho_push1`、`A_lei_crisis` |
| `flag_*` | 布林／事件旗標（建議正規前綴） | `flag_anti_lei`、`flag_tang_open` |
| 裸前綴（歷史） | Pack1 曉晴／采兒部分 flags；見 `qa.flagAlias` | `hiu_meet_exchange` → 建議 `flag_hiu_meet_exchange` |
| `rel_*` | 關係數值 | `rel_vera`、`rel_tang` |
| `rel_tang_threshold` | **條件代幣**（不是布林旗）；檔頂值 = **2**（playtest 可調） | push1+ 雙閘之一 |
| `route_*` | 路線傾向 | `route_tv`、`route_indie` |
| `era_*` | 時代錨 tag | `era_1988_spring_grassroot` |
| `T1`…`T6` | 檔期衝突代號（UNLOCK §3） | `T2`＝台慶位 vs 陪伴 |
| `E01`…`E10` | 事業結局（名稱硬鎖） | E01 穩陣男演員 … E10 未出頭 |
| `B01`…`B10`／`Ch1`…`Ch4` | 現有原型教學／章節 beats（`story_beats_phase1.json`）；**尚未**等於 C 節點 | 過渡期雙軌 |
| loc id `tvb_longmen` | 地點 id（保留） | 顯示名＝**星河電視台** |

**Commit 規則摘要：** 感情 `ending` 寫 `flag_*_he`＋`flag_*_commit`（HE）或 `flag_*_be`（BE）；確定關係前 `parallelOk: true`；確定後其他線降友情／冷淡（規則文案在各 romance JSON `rule`；引擎尚未實作排他）。關海媚無 `flag_*_commit`、無專屬 HE 檔。

---

## 3. 主線 C1–C17 wiring 表

> JSON **無** `unlockConditions`／`openConditions` 欄；下表「UNLOCK 條件」取自 `PLOT_DETAIL_UNLOCK_v1.md`（方向性）。「JSON 寫入」取自 `flags_written`＋choices.effects。`nextHints` 為建議推進（非 JSON 欄）。

| id | phase | when | UNLOCK 出現條件 | JSON conflict | flags_written（節點級） | 選擇寫入摘要 | links／T* | nextHints | gaps vs UNLOCK |
|---|---|---|---|---|---|---|---|---|---|
| `C1` | P1 | 1988春 / W3-4 | 開局後首次重要通告選擇 | T1 | `route_tv, route_film` | C1_a→[route_tv]<br>C1_b→[route_film] | T1 | C2 | JSON 無 unlock／openConditions（靠 UNLOCK＋phase／when）；與 A_tsijun_meet（C1／T1）雙軌 |
| `C2` | P1 | 1988春 / W4-5 | C1 後；何生在場事件 | null | `flag_network_stay, flag_hustle_board` | C2_a→[flag_network_stay]<br>C2_b→[flag_hustle_board] | — | C3 | JSON 無 unlock／openConditions（靠 UNLOCK＋phase／when） |
| `C3` | P1 | 1988春 / W6-8 | 與高俊傑同場搶板 | null | `rival_gao_hard, rival_gao_endure` | C3_a→[rival_gao_hard]<br>C3_b→[rival_gao_endure] | —／連 A_ko | C4 | JSON 無 unlock／openConditions（靠 UNLOCK＋phase／when）；與 A_ko_meet 雙軌：需定 sync／互斥政策 |
| `C4` | P1 | 1988春 / W8-9 | 何生帶來可疑／苛刻通告 | null | `flag_refuse_gig_with_ho, flag_take_harsh_gig` | C4_a→[flag_refuse_gig_with_ho]<br>C4_b→[flag_take_harsh_gig] | —／連 A_ho | C5 | JSON 無 unlock／openConditions（靠 UNLOCK＋phase／when） |
| `C5` | P1 | 1988夏 / W9-10 | 周采兒好感達門檻或台慶籌備季（方向性／playtest） | null | `choi_honest, choi_spin, choi_dodge` | C5_a→[choi_honest]<br>C5_b→[choi_spin]<br>C5_c→[choi_dodge] | —／連 R_choi | C6 | JSON 無 unlock／openConditions（靠 UNLOCK＋phase／when） |
| `C6` | P1.5 | 1988秋 / W12-14 | 至少一條可攻略線達約會門檻；可平行未確定（方向性／playtest） | null | `date_vera_1, date_hiu_1, date_choi_1` | C6_a→[date_vera_1]<br>C6_b→[date_hiu_1]<br>C6_c→[date_choi_1] | — | C7 | JSON 無 unlock／openConditions（靠 UNLOCK＋phase／when） |
| `C7` | P1.5 | 1988秋冬 / W14-16 | P1.5 可提前；未觸則 P2 首交鋒；提前則拖字訣過渡 | null | `flag_anti_lei, flag_lei_delay, flag_lei_signed` | C7_a→[flag_anti_lei]<br>C7_b→[flag_lei_delay]<br>C7_c→[flag_lei_signed] | —／連 A_lei | C8 | JSON 無 unlock／openConditions（靠 UNLOCK＋phase／when）；UNLOCK／Pack3 連雷勁；JSON conflict=null（A_lei_crisis.linksMain=[C7]） |
| `C8` | P2 | 1989春 / W20-24 | 高文瀚機會＋張子駿邀約同時可見 | null | `route_commercial, route_indie` | C8_a→[route_commercial]<br>C8_b→[route_indie] | —／連 A_tsijun／A_gao | C9 | JSON 無 unlock／openConditions（靠 UNLOCK＋phase／when） |
| `C9` | P2 | 1989夏秋 / W28-32 | 藍若曦線已開芽＋狗仔事件（方向性／playtest） | null | `flag_public_romance, lan_blur, lan_confess, lan_cut` | C9_a→[flag_public_romance,lan_confess]<br>C9_b→[lan_cut]<br>C9_c→[lan_blur] | —／連 R_lan_push2 | C10 | JSON 無 unlock／openConditions（靠 UNLOCK＋phase／when）；連 R_lan_push2；無 T 碼 |
| `C10` | P2 | 1989冬 / W40-44 | 台慶季＋高俊傑競爭位 | T2 | `anni_mediate, anni_seize, anni_yield` | C10_a→[anni_seize]<br>C10_b→[anni_yield]<br>C10_c→[anni_mediate] | T2 | C11 | JSON 無 unlock／openConditions（靠 UNLOCK＋phase／when） |
| `C11` | P3 | 1990秋 / W60-64 | 張子駿線進行中＋影展／文藝檔 | T3 | `choose_exposure, choose_depth, route_indie` | C11_a→[choose_exposure]<br>C11_b→[choose_depth,route_indie] | T3 | C12 | JSON 無 unlock／openConditions（靠 UNLOCK＋phase／when） |
| `C12` | P4 | 1991夏 / W80-84 | 中高 tier＋已有確定或高好感線（方向性／playtest） | T4 | `anni91_seize, anni91_tend, love_crisis` | C12_a→[anni91_seize,love_crisis]<br>C12_b→[anni91_tend] | T4 | C13／C14／C15 | JSON 無 unlock／openConditions（靠 UNLOCK＋phase／when）；effects 用 rel_partner（抽象；引擎需映射當前約會線） |
| `C13` | P4 | 1991冬 / W92-96 | 周采兒或關海媚事件鏈＋fame 門檻（方向性／playtest） | null | `gossip_admit, gossip_deny, gossip_vague, flag_public_romance` | C13_a→[gossip_admit,flag_public_romance]<br>C13_b→[gossip_deny]<br>C13_c→[gossip_vague] | —／連 R_choi_crisis | C14／C15 | JSON 無 unlock／openConditions（靠 UNLOCK＋phase／when）；連 R_choi_crisis；關海媚無 commit |
| `C14` | P4 | 1991秋 / W88-90 | 徐寶珊線開芽＋金援邀請 | T6 | `flag_bao_respect, flag_bao_depend, flag_bao_refuse` | C14_a→[flag_bao_respect]<br>C14_b→[flag_bao_depend]<br>C14_c→[flag_bao_refuse] | T6／連 R_xu_crisis | C15／C16 | JSON 無 unlock／openConditions（靠 UNLOCK＋phase／when）；JSON conflict=T6（對齊 UNLOCK）；連 R_xu_crisis |
| `C15` | P4 | 1991春 / W72-76 | 藍若曦高好感＋家族壓事件 | null | `flag_family_help, flag_family_yield, flag_family_standby, flag_family_marriage` | C15_a→[flag_family_help,flag_family_marriage]<br>C15_b→[flag_family_yield,flag_family_marriage]<br>C15_c→[flag_family_standby,flag_family_marriage] | —／連 R_lan_crisis | C16 | JSON 無 unlock／openConditions（靠 UNLOCK＋phase／when）；連 R_lan_crisis；家族旗與 romance 雙寫 |
| `C16` | P5 | 1992夏 / W100-104 | 進入結局季；金九／傳承事件 | null | `flag_legacy_film, flag_legacy_refuse` | C16_a→[flag_legacy_film]<br>C16_b→[flag_legacy_refuse] | — | C17 | JSON 無 unlock／openConditions（靠 UNLOCK＋phase／when） |
| `C17` | P5 | 1992收束 / W105-108 | C16 後；事業數值＋旗標齊 | null | `ending_e01, ending_e02, ending_e03, ending_e04, ending_e05, ending_e06, ending_e07, ending_e08, ending_e09, ending_e10, career_lock` | C17_e01→[ending_e01,career_lock]<br>C17_e02→[ending_e02,career_lock]<br>C17_e03→[ending_e03,career_lock]<br>C17_e04→[ending_e04,career_lock]<br>C17_e05→[ending_e05,career_lock]<br>C17_e06→[ending_e06,career_lock]<br>C17_e07→[ending_e07,career_lock]<br>C17_e08→[ending_e08,career_lock]<br>C17_e09→[ending_e09,career_lock]<br>C17_e10→[ending_e10,career_lock] | — | 結局展示 | JSON 無 unlock／openConditions（靠 UNLOCK＋phase／when） |

**密度核對：** P1–P1.5＝7；P2＝3；P3＝1；P4＝4；P5＝2；合計 **17**（`coverage.count=17`，`missing=[]`）。

**E01–E10 名稱硬鎖（C17.endings_catalog）：** 穩陣男演員／有名有實／評審眼熟／跨界紅人／動作班底／海外發展／金援靠山／有錢但空／淡出守住／未出頭。

---

## 4. 感情線 wiring（5＋鄧麗萍）

### 4.1 Pack1 — Vera／林曉晴／周采兒（`story_detail_romance_vera_hiu_choi.json` v1.1）

| beat id | line | arcBeat | phase | openConditions | flags_written | conflict | linksMain | 備註 |
|---|---|---|---|---|---|---|---|---|
| `R_vera_meet` | vera | meet | P1 | `<MISSING>` | `flag_vera_met_cold, flag_vera_met_warm` | — | — | — |
| `R_vera_push1` | vera | push | P1.5 | `<MISSING>` | `flag_vera_cooperate, flag_vera_perfunctory` | — | — | — |
| `R_vera_push2` | vera | push | P2 | `<MISSING>` | `flag_vera_honest, flag_vera_worktalk` | — | — | — |
| `R_vera_crisis` | vera | crisis | P4 | `<MISSING>` | `flag_vera_stay, flag_vera_workfirst` | T5 | — | T5 |
| `R_vera_ending` | vera | ending | P5 | `<MISSING>` | `flag_vera_be, flag_vera_commit, flag_vera_he` | — | — | parallelOk=false；HE/BE+commit |
| `R_hiu_meet` | hiu | meet | P1 | `<MISSING>` | `hiu_meet_distant, hiu_meet_exchange` | — | — | 裸前綴；見 qa.flagAlias |
| `R_hiu_push1` | hiu | push | P1.5 | `<MISSING>` | `hiu_push1_help, hiu_push1_self` | — | — | 裸前綴；見 qa.flagAlias |
| `R_hiu_push2` | hiu | push | P2 | `<MISSING>` | `hiu_push2_date, hiu_push2_friend` | — | — | 裸前綴；見 qa.flagAlias |
| `R_hiu_crisis` | hiu | crisis | P4 | `<MISSING>` | `hiu_crisis_fight, hiu_crisis_yield` | — | — | 裸前綴；見 qa.flagAlias |
| `R_hiu_ending` | hiu | ending | P5 | `<MISSING>` | `flag_hiu_be, flag_hiu_commit, flag_hiu_he` | — | — | parallelOk=false；HE/BE+commit |
| `R_choi_meet` | choi | meet | P1 | `<MISSING>` | `choi_meet_honest, choi_meet_official` | — | — | 裸前綴；見 qa.flagAlias |
| `R_choi_push1` | choi | push | P1.5 | `<MISSING>` | `choi_give_tip, choi_refuse_tip` | — | — | 裸前綴；見 qa.flagAlias |
| `R_choi_push2` | choi | push | P2 | `<MISSING>` | `choi_keep_professional, choi_real_date` | — | — | 裸前綴；見 qa.flagAlias |
| `R_choi_crisis` | choi | crisis | P4 | `<MISSING>` | `choi_deny_romance, flag_public_romance` | — | ['C13'] | Soft：linksMain=[C13]；choice ids 已 C_choi_* |
| `R_choi_ending` | choi | ending | P5 | `<MISSING>` | `flag_choi_be, flag_choi_commit, flag_choi_he` | — | — | parallelOk=false；HE/BE+commit |

**Commit：** `flag_vera_commit`／`flag_hiu_commit`／`flag_choi_commit` 僅 ending HE；確定前 `parallelOk=true`。

### 4.2 Pack2 — 藍若曦／徐寶珊＋鄧 stub（`story_detail_romance_lan_xu.json` v2.1）

> Soft 慣例：`T→conflict`；`C→linksMain`。

| beat id | line | arcBeat | phase | openConditions | flags_written | conflict | linksMain | 備註 |
|---|---|---|---|---|---|---|---|---|
| `R_lan_meet` | lan | meet | P2 | `<MISSING>` | `flag_lan_met_cool, flag_lan_met_warm` | — | — | — |
| `R_lan_push1` | lan | push | P2 | `<MISSING>` | `flag_lan_sang_together, flag_lan_work_only` | — | — | — |
| `R_lan_push2` | lan | push | P2 | `<MISSING>` | `flag_lan_colleague, flag_lan_protected` | — | ['C9'] | 連 C9 |
| `R_lan_crisis` | lan | crisis | P4 | `<MISSING>` | `flag_family_help, flag_family_marriage, flag_lan_help, flag_lan_stepback` | — | ['C15'] | 連 C15；雙寫 family 旗 |
| `R_lan_ending` | lan | ending | P5 | `<MISSING>` | `flag_lan_be, flag_lan_commit, flag_lan_he` | — | — | parallelOk=false；HE/BE+commit |
| `R_xu_meet` | xu | meet | P3 | `<MISSING>` | `flag_xu_met_distance, flag_xu_met_polite` | — | — | — |
| `R_xu_push1` | xu | push | P3 | `<MISSING>` | `flag_xu_coop_decline, flag_xu_coop_talk` | — | — | — |
| `R_xu_push2` | xu | push | P4 | `<MISSING>` | `flag_xu_business_only, flag_xu_personal_open` | — | — | — |
| `R_xu_crisis` | xu | crisis | P4 | `<MISSING>` | `flag_bao_depend, flag_bao_refuse, flag_bao_respect, flag_xu_depend, flag_xu_refuse, flag_xu_respect` | T6 | ['C14'] | T6＋連 C14；雙寫 flag_bao_* |
| `R_xu_ending` | xu | ending | P5 | `<MISSING>` | `flag_xu_be, flag_xu_commit, flag_xu_he` | — | — | parallelOk=false；HE/BE+commit |
| `R_tang_meet_stub` | tang | meet | P4 | `[]` | `flag_tang_open` | — | — | supersededBy R_tang_meet；**節點 flags_written 仍列 flag_tang_open，但 choice 只寫 flag_tang_met**（Soft leftover） |

### 4.3 鄧麗萍正式線（`story_detail_romance_tang.json` v1.1）

**檔級 openConditions：**

- `meet`: `[]`（可寫入 `flag_tang_open`）
- `pushAndAfter`: `[flag_tang_open, rel_tang_threshold]`
- `rel_tang_threshold`: **2**（方向性／playtest 可調）
- stubCompat：`R_tang_meet_stub` 保留；`supersededBy: R_tang_meet`；stub 只應寫 `flag_tang_met`＋`rel_tang`

| beat id | arcBeat | phase | openConditions | flags_written | conflict（現況＝自由字串） | 備註 |
|---|---|---|---|---|---|---|
| `R_tang_meet` | meet | P3 | `[]` | `flag_tang_met_wait, flag_tang_open` | 新片爭檔期 vs 院線數據門檻 | 本節可寫入 flag_tang_open；不要求雙閘 |
| `R_tang_push1` | push | P3 | `['flag_tang_open', 'rel_tang_threshold']` | `flag_tang_push1_exchange, flag_tang_push1_prove` | 冷門檔期風險 vs 數據回報 | 正式推進需雙條件已滿足。數據互助、試映／冷門檔交換情報。鄧仍冷酷但開始留意你號召力。 |
| `R_tang_push2` | push | P4 | `['flag_tang_open', 'rel_tang_threshold']` | `flag_tang_push2_business, flag_tang_push2_private` | 純商業計算 vs 私人情感試探 | 可略露 secret（藝術片虧損）但不完全打開。玩家選：繼續純商業 vs 問私人。 |
| `R_tang_crisis` | crisis | P4 | `['flag_tang_open', 'rel_tang_threshold']` | `flag_tang_crisis_data, flag_tang_crisis_favor, flag_tang_crisis_middle` | 檔期數據vs人情 | 危機主題明確：檔期數據 vs 人情／藝術。三支 choice：堅持數據／為人情破例／折衷。連院線排片、票房、午夜場（虛構）。 |
| `R_tang_ending` | ending | P5 | `['flag_tang_open', 'rel_tang_threshold']` | `flag_tang_be, flag_tang_commit, flag_tang_he` | 商業盟友 vs 感情原則 | HE 含 flag_tang_he＋flag_tang_commit；BE 含 flag_tang_be。鄧麗萍認可號召力；感情線與事業結局並存。 |

**Commit：** HE＝`flag_tang_he`＋`flag_tang_commit`；BE＝`flag_tang_be`；`parallelOk=false` at ending。

---

## 5. 對手／導師 Pack3 wiring（8 弧）

來源：`story_detail_rival_mentor.json` v2.1。每弧 5 節：meet → push1 → push2 → crisis → ending。

### 5.1 弧總表

| arcLine | 人物 | kind | nodePrefix | arcs.linksMain | nodeIds |
|---|---|---|---|---|---|
| `ko` | 高俊傑 | rival | `A_ko_` | ['C3', 'C10', 'C12', 'T2'] | `A_ko_meet`, `A_ko_push1`, `A_ko_push2`, `A_ko_crisis`, `A_ko_ending` |
| `hakfan` | 張克凡 | rival | `A_hakfan_` | ['P2–P4資源場'] | `A_hakfan_meet`, `A_hakfan_push1`, `A_hakfan_push2`, `A_hakfan_crisis`, `A_hakfan_ending` |
| `tsijun` | 張子駿 | mentor | `A_tsijun_` | ['C8', 'C11', 'C17', 'E03', 'T3'] | `A_tsijun_meet`, `A_tsijun_push1`, `A_tsijun_push2`, `A_tsijun_crisis`, `A_tsijun_ending` |
| `fong` | 方小龍 | friend | `A_fong_` | ['P3替身危機', 'E05'] | `A_fong_meet`, `A_fong_push1`, `A_fong_push2`, `A_fong_crisis`, `A_fong_ending` |
| `tong` | 唐素雲 | mentor | `A_tong_` | ['P2去留', 'E09'] | `A_tong_meet`, `A_tong_push1`, `A_tong_push2`, `A_tong_crisis`, `A_tong_ending` |
| `ho` | 何生 | mentor | `A_ho_` | ['C2', 'C4', 'E01'] | `A_ho_meet`, `A_ho_push1`, `A_ho_push2`, `A_ho_crisis`, `A_ho_ending` |
| `gao` | 高文瀚 | mentor | `A_gao_` | ['C8', 'C12', 'E02', 'T4'] | `A_gao_meet`, `A_gao_push1`, `A_gao_push2`, `A_gao_crisis`, `A_gao_ending` |
| `lei` | 雷勁 | capital | `A_lei_` | ['C7', 'flag_anti_lei'] | `A_lei_meet`, `A_lei_push1`, `A_lei_push2`, `A_lei_crisis`, `A_lei_ending` |

### 5.2 節點表（精簡）

| beat id | arc | arcBeat | phase | flags_written（節點） | conflict | linksMain | parallelOk |
|---|---|---|---|---|---|---|---|
| `A_ko_meet` | ko | meet | P1 | `flag_ko_met_grab, flag_ko_met_yield` | C3 | ['C3'] | True |
| `A_ko_push1` | ko | push | P1 | `flag_ko_push1_counter, flag_ko_push1_observe` | 排練場上互較執生同搶鏡位 | — | True |
| `A_ko_push2` | ko | push | P2 | `flag_ko_push2_ally, flag_ko_push2_confront, flag_ko_push2_ignore` | 台慶排位同放風比較，爭企中間嘅機會 | ['C10', 'T2'] | True |
| `A_ko_crisis` | ko | crisis | P2 | `flag_ko_crisis_deal, flag_ko_crisis_fight, flag_ko_crisis_stepback` | C10／T2 | ['C10', 'T2'] | True |
| `A_ko_ending` | ko | ending | P4 | `flag_ko_cold_war, flag_ko_mentor_complete, flag_ko_rival_respect` | C12 | ['C12'] | True |
| `A_hakfan_meet` | hakfan | meet | P2 | `flag_hakfan_avoided, flag_hakfan_met, flag_hakfan_probed, flag_hakfan_stand_ground` | P2資源場 | ['P2資源場'] | True |
| `A_hakfan_push1` | hakfan | push | P2 | `flag_hakfan_negotiated, flag_hakfan_rejected_support, flag_hakfan_took_support` | 張克凡靠飯局人脈搶走主角，你只剩配角位；連 P2資源場，接 A_hakfan_p… | — | True |
| `A_hakfan_push2` | hakfan | push | P3 | `flag_hakfan_deferred, flag_hakfan_faced_off, flag_hakfan_own_style` | 同場對戲，張克凡用世家訓練壓你節奏，你用地道演法頂返；連 A_hakfan_cr… | — | True |
| `A_hakfan_crisis` | hakfan | crisis | P4 | `flag_hakfan_allied, flag_hakfan_leaked, flag_hakfan_solo` | P2–P4資源場 | ['P2', 'P3', 'P4'] | True |
| `A_hakfan_ending` | hakfan | ending | P5 | `flag_hakfan_cold_war, flag_hakfan_mentor_complete, flag_hakfan_rival_respect` | 台慶後台最後對望，張克凡放下家世語氣講演技，你決定敵線收於尊重抑或繼續死敵；連 … | — | True |
| `A_tsijun_meet` | tsijun | meet | P1 | `flag_tsijun_met_leave, flag_tsijun_met_stay` | C1／T1 | ['C1', 'T1'] | True |
| `A_tsijun_push1` | tsijun | push | P1.5 | `flag_tsijun_push1_grind, flag_tsijun_push1_side` | 收視話題同演出層次拉扯；張子駿守住班底，高俊傑要廠方交代。 | — | True |
| `A_tsijun_push2` | tsijun | push | P2 | `flag_tsijun_push2_film, flag_tsijun_push2_variety` | C8 | ['C8'] | True |
| `A_tsijun_crisis` | tsijun | crisis | P3 | `flag_tsijun_crisis_cut, flag_tsijun_crisis_hold, flag_tsijun_crisis_silent` | C11／T3 | ['C11', 'T3'] | True |
| `A_tsijun_ending` | tsijun | ending | P5 | `flag_tsijun_ending_cold, flag_tsijun_ending_complete, flag_tsijun_ending_respect` | C17／E03 | ['C17', 'E03'] | True |
| `A_fong_meet` | fong | meet | P1 | `flag_fong_intro_sent, flag_fong_met, flag_fong_warned` | 你對入行嘅猶豫 vs 小龍嘅熱心拉攏；高俊傑對臨記嘅冷淡 | — | True |
| `A_fong_push1` | fong | push | P2 | `flag_fong_push1_learn, flag_fong_push1_let, flag_fong_push1_watch` | 張克凡嘅嚴要求 vs 小龍嘅死頂；你喺棚入面嘅位置 | — | True |
| `A_fong_push2` | fong | push | P3 | `flag_fong_push2_leave, flag_fong_push2_rest, flag_fong_push2_train` | 密集通告下嘅練功壓力 vs 班底規矩；你同小龍嘅投入程度 | — | True |
| `A_fong_crisis` | fong | crisis | P3 | `flag_fong_crisis_call, flag_fong_crisis_freeze, flag_fong_crisis_rescue, flag_fong_saved_once` | P3替身危機 | ['P3替身危機'] | False |
| `A_fong_ending` | fong | ending | P5 | `flag_cold_war, flag_fong_ending_cold, flag_fong_ending_respect, flag_fong_ending_save, flag_friend_saved, flag_rival_respect` | E05 | ['E05'] | True |
| `A_tong_meet` | tong | meet | P2 | `flag_tong_met_step_in, flag_tong_met_watch` | 唐素雲賞識 vs 高俊傑輕視；玩家要決定是否踏出第一步。 | ['P2去留'] | True |
| `A_tong_push1` | tong | push | P2 | `flag_tong_push1_accept, flag_tong_push1_argue` | 唐素雲的嚴格要求 vs 你對自己演法的堅持。 | ['P2去留'] | True |
| `A_tong_push2` | tong | push | P2 | `flag_tong_push2_doubt, flag_tong_push2_stay` | P2去留 | ['P2去留'] | True |
| `A_tong_crisis` | tong | crisis | P3 | `flag_tong_crisis_confess, flag_tong_crisis_leave, flag_tong_crisis_stay` | E09氣氛 | ['E09'] | True |
| `A_tong_ending` | tong | ending | P5 | `flag_tong_ending_cold, flag_tong_ending_mentor, flag_tong_ending_respect` | E09 | ['E09'] | True |
| `A_ho_meet` | ho | meet | P1 | `flag_ho_asked_why, flag_ho_intro_round, flag_ho_met` | C2 | ['C2'] | True |
| `A_ho_push1` | ho | push | P1 | `flag_ho_refused_deal, flag_ho_took_deal, flag_ho_trust_up` | C4 | ['C4'] | True |
| `A_ho_push2` | ho | push | P2 | `flag_ho_quality_trust, flag_ho_self_select` | 通告量同品質拉鋸；何生要你唔好做蝕底嘅工 | — | True |
| `A_ho_crisis` | ho | crisis | P4 | `flag_ho_big_bet, flag_ho_crisis_ask, flag_ho_crisis_leave, flag_ho_crisis_stay` | 忠誠同利益對撞；何生押上身家；連 E01 | ['E01'] | True |
| `A_ho_ending` | ho | ending | P5 | `flag_ho_cold_war, flag_ho_mentor_complete, flag_ho_rival_respect` | E01 | ['E01'] | True |
| `A_gao_meet` | gao | meet | P2 | `flag_gao_curious, flag_gao_honest, flag_gao_met` | C8 | ['C8'] | True |
| `A_gao_push1` | gao | push | P2 | `flag_gao_push_ask, flag_gao_push_grab, flag_gao_push_wait` | 爭位嘅野心 vs 唔想顯得咄咄逼人；高文瀚要睇你係唔係真係餓 | — | True |
| `A_gao_push2` | gao | push | P3 | `flag_gao_push2_deliver, flag_gao_push2_help, flag_gao_push2_safe` | 一次過嘅壓力 vs 廠內等你出錯嘅目光；高文瀚要睇你係唔係佢可以推出去嘅人 | — | True |
| `A_gao_crisis` | gao | crisis | P4 | `flag_gao_crisis_commit, flag_gao_crisis_honest, flag_gao_crisis_stepback` | C12／T4 | ['C12', 'T4'] | True |
| `A_gao_ending` | gao | ending | P5 | `flag_gao_ending_break, flag_gao_ending_respect, flag_gao_ending_stay` | E02 | ['E02'] | True |
| `A_lei_meet` | lei | meet | P1.5 | `flag_lei_bluff, flag_lei_contract_read, flag_lei_met` | 雷勁想收你入旗下，你想保住自主；合約條款苛刻，簽與唔簽都係壓力。 | — | True |
| `A_lei_push1` | lei | push | P1.5 | `flag_ko_ally, flag_lei_defiant, flag_lei_push1` | 雷勁用通告同人脈施壓，你想守住立場又唔想斷咗條路。 | — | True |
| `A_lei_push2` | lei | push | P2 | `flag_lei_contract_read, flag_lei_deal, flag_lei_push2, flag_lei_refuse_film` | 雷勁用電影機會換你接受苛刻條件，你想上位又唔想俾人食住。 | — | True |
| `A_lei_crisis` | lei | crisis | P1.5 | `flag_anti_lei, flag_lei_bound, flag_lei_crisis, flag_lei_negotiated` | C7 | ['C7'] | True |
| `A_lei_ending` | lei | ending | P5 | `flag_ally_danger, flag_anti_lei, flag_lei_ally, flag_lei_cold_war, flag_lei_rival_respect` | flag_anti_lei | ['flag_anti_lei'] | True |

> Soft outstanding：全部 ending 仍 `parallelOk: true`（與感情 ending 慣例不一致；本輪 wiring **不**改 JSON）。

---

## 6. gigs_1988 標註 wiring

來源：`gigs_1988.json` **v2.1.1**（30 則）；標註說明見 `GIGS_1988_ANNOTATION_v1.md`。

### 6.1 欄位 → Phase1 通告板

| 欄位 | 覆蓋 | 引擎建議用途 |
|---|---|---|
| `eraTag` | 30/30 | 與當前季／週氛圍過濾或加權；詞表見標註 md |
| `boardPriority` | 30/30（`high`14／`normal`11／`low`5） | 通告板排序／置頂；high 應優先露出 |
| `seasonWeight` | 30/30（僅 1.0 或 0.6） | 與當季匹配時加權；high 多配 1.0 |
| `boardNote` | 30/30 | 板面短註（非 synopsis） |
| `discoverNote` | 30/30 | 「點樣發現呢張通告」敘事鉤 |
| `loc` | 30/30 | 地點 id；**顯示名**由原型 locs 表映射 |
| `synopsis`／pay／id 等 | — | **鐵律：標註輪不改**；wiring 只讀 |

**高覆蓋期望：** 春 high≥4、夏≥4、秋≥2、冬≥3 — 標註自檢已 PASS（春4／夏4／秋2／冬4）。

### 6.2 星河 vs loc id

| 層 | 值 |
|---|---|
| loc id（資料） | `tvb_longmen`（gigs 內出現 7 次；**保留**） |
| 顯示名（原型 `index.html` locs） | `name:"星河電視台"` |
| 玩家可見正文 | Soft 後「龍門」＝0；edits 審計註記可保留 |

### 6.3 與現有原型落差（重要）

- `index.html` 內嵌 `const GIGS = [...]`（約 30 則 `gig_1988_*`），**未** `fetch("content/gigs_1988.json")`。
- 內嵌 GIGS **無** `boardPriority`／`seasonWeight`／`eraTag` 欄（搜尋 `boardPriority` in html = 0）。
- Phase1 接線建議：**改為讀 `gigs_1988.json`**（或 build 時同步內嵌），先按 `boardPriority`＋當季 `seasonWeight` 排序，再套現有 hard-gate／育成鎖。

---

## 7. 旗標註冊表

> 由各 story JSON 之 `flags_written`＋`choices.effects.flags`＋`openConditions` 抽出。`rel_tang_threshold` 為條件代幣（無 writer）。統計類 `rel_*`／`craft` 等見下「數值」。

**Unique flag／條件代幣數：** 241（含 `rel_tang_threshold`）

| flag／token | first-writer（節點或 choice） | 其他 writers（節選） | consumers |
|---|---|---|---|
| `anni91_seize` | `C:C12` | `C:C12/C12_a` | — |
| `anni91_tend` | `C:C12` | `C:C12/C12_b` | — |
| `anni_mediate` | `C:C10` | `C:C10/C10_c` | — |
| `anni_seize` | `C:C10` | `C:C10/C10_a` | — |
| `anni_yield` | `C:C10` | `C:C10/C10_b` | — |
| `career_lock` | `C:C17` | `C:C17/C17_e01`, `C:C17/C17_e02`, `C:C17/C17_e03` …(+7) | — |
| `choi_deny_romance` | `R1:R_choi_crisis` | `R1:R_choi_crisis/C_choi_crisis_b` | — |
| `choi_dodge` | `C:C5` | `C:C5/C5_c` | — |
| `choi_give_tip` | `R1:R_choi_push1` | `R1:R_choi_push1/C_choi_push1_a` | — |
| `choi_honest` | `C:C5` | `C:C5/C5_a` | — |
| `choi_keep_professional` | `R1:R_choi_push2` | `R1:R_choi_push2/C_choi_push2_b` | — |
| `choi_meet_honest` | `R1:R_choi_meet` | `R1:R_choi_meet/C_choi_meet_a` | — |
| `choi_meet_official` | `R1:R_choi_meet` | `R1:R_choi_meet/C_choi_meet_b` | — |
| `choi_real_date` | `R1:R_choi_push2` | `R1:R_choi_push2/C_choi_push2_a` | — |
| `choi_refuse_tip` | `R1:R_choi_push1` | `R1:R_choi_push1/C_choi_push1_b` | — |
| `choi_spin` | `C:C5` | `C:C5/C5_b` | — |
| `choose_depth` | `C:C11` | `C:C11/C11_b` | — |
| `choose_exposure` | `C:C11` | `C:C11/C11_a` | — |
| `date_choi_1` | `C:C6` | `C:C6/C6_c` | — |
| `date_hiu_1` | `C:C6` | `C:C6/C6_b` | — |
| `date_vera_1` | `C:C6` | `C:C6/C6_a` | — |
| `ending_e01` | `C:C17` | `C:C17/C17_e01` | — |
| `ending_e02` | `C:C17` | `C:C17/C17_e02` | — |
| `ending_e03` | `C:C17` | `C:C17/C17_e03` | — |
| `ending_e04` | `C:C17` | `C:C17/C17_e04` | — |
| `ending_e05` | `C:C17` | `C:C17/C17_e05` | — |
| `ending_e06` | `C:C17` | `C:C17/C17_e06` | — |
| `ending_e07` | `C:C17` | `C:C17/C17_e07` | — |
| `ending_e08` | `C:C17` | `C:C17/C17_e08` | — |
| `ending_e09` | `C:C17` | `C:C17/C17_e09` | — |
| `ending_e10` | `C:C17` | `C:C17/C17_e10` | — |
| `flag_ally_danger` | `A:A_lei_ending` | `A:A_lei_ending/C_lei_ending_ally` | — |
| `flag_anti_lei` | `C:C7` | `C:C7/C7_a`, `A:A_lei_crisis`, `A:A_lei_crisis/C_lei_crisis_refuse` …(+2) | `A:A_lei_ending:linksMain` |
| `flag_bao_depend` | `C:C14` | `C:C14/C14_b`, `R2:R_xu_crisis`, `R2:R_xu_crisis/C_xu_crisis_depend` | — |
| `flag_bao_refuse` | `C:C14` | `C:C14/C14_c`, `R2:R_xu_crisis`, `R2:R_xu_crisis/C_xu_crisis_refuse` | — |
| `flag_bao_respect` | `C:C14` | `C:C14/C14_a`, `R2:R_xu_crisis`, `R2:R_xu_crisis/C_xu_crisis_respect` | — |
| `flag_choi_be` | `R1:R_choi_ending` | `R1:R_choi_ending/C_choi_ending_be` | — |
| `flag_choi_commit` | `R1:R_choi_ending` | `R1:R_choi_ending/C_choi_ending_he` | — |
| `flag_choi_he` | `R1:R_choi_ending` | `R1:R_choi_ending/C_choi_ending_he` | — |
| `flag_cold_war` | `A:A_fong_ending` | `A:A_fong_ending/C_fong_ending_cold` | — |
| `flag_family_help` | `C:C15` | `C:C15/C15_a`, `R2:R_lan_crisis`, `R2:R_lan_crisis/C_lan_crisis_help` | — |
| `flag_family_marriage` | `C:C15` | `C:C15/C15_a`, `C:C15/C15_b`, `C:C15/C15_c` …(+3) | — |
| `flag_family_standby` | `C:C15` | `C:C15/C15_c` | — |
| `flag_family_yield` | `C:C15` | `C:C15/C15_b` | — |
| `flag_fong_crisis_call` | `A:A_fong_crisis` | `A:A_fong_crisis/C_fong_crisis_call` | — |
| `flag_fong_crisis_freeze` | `A:A_fong_crisis` | `A:A_fong_crisis/C_fong_crisis_freeze` | — |
| `flag_fong_crisis_rescue` | `A:A_fong_crisis` | `A:A_fong_crisis/C_fong_crisis_rescue` | — |
| `flag_fong_ending_cold` | `A:A_fong_ending` | `A:A_fong_ending/C_fong_ending_cold` | — |
| `flag_fong_ending_respect` | `A:A_fong_ending` | `A:A_fong_ending/C_fong_ending_respect` | — |
| `flag_fong_ending_save` | `A:A_fong_ending` | `A:A_fong_ending/C_fong_ending_save` | — |
| `flag_fong_intro_sent` | `A:A_fong_meet` | `A:A_fong_meet/C_fong_meet_take` | — |
| `flag_fong_met` | `A:A_fong_meet` | `A:A_fong_meet/C_fong_meet_take`, `A:A_fong_meet/C_fong_meet_ask` | — |
| `flag_fong_push1_learn` | `A:A_fong_push1` | `A:A_fong_push1/C_fong_push1_learn` | — |
| `flag_fong_push1_let` | `A:A_fong_push1` | `A:A_fong_push1/C_fong_push1_let` | — |
| `flag_fong_push1_watch` | `A:A_fong_push1` | `A:A_fong_push1/C_fong_push1_watch` | — |
| `flag_fong_push2_leave` | `A:A_fong_push2` | `A:A_fong_push2/C_fong_push2_leave` | — |
| `flag_fong_push2_rest` | `A:A_fong_push2` | `A:A_fong_push2/C_fong_push2_rest` | — |
| `flag_fong_push2_train` | `A:A_fong_push2` | `A:A_fong_push2/C_fong_push2_train` | — |
| `flag_fong_saved_once` | `A:A_fong_crisis` | `A:A_fong_crisis/C_fong_crisis_rescue` | — |
| `flag_fong_warned` | `A:A_fong_meet` | `A:A_fong_meet/C_fong_meet_ask` | — |
| `flag_friend_saved` | `A:A_fong_ending` | `A:A_fong_ending/C_fong_ending_save` | — |
| `flag_gao_crisis_commit` | `A:A_gao_crisis` | `A:A_gao_crisis/C_gao_crisis_commit` | — |
| `flag_gao_crisis_honest` | `A:A_gao_crisis` | `A:A_gao_crisis/C_gao_crisis_honest` | — |
| `flag_gao_crisis_stepback` | `A:A_gao_crisis` | `A:A_gao_crisis/C_gao_crisis_stepback` | — |
| `flag_gao_curious` | `A:A_gao_meet` | `A:A_gao_meet/C_gao_meet_ask` | — |
| `flag_gao_ending_break` | `A:A_gao_ending` | `A:A_gao_ending/C_gao_ending_break` | — |
| `flag_gao_ending_respect` | `A:A_gao_ending` | `A:A_gao_ending/C_gao_ending_respect` | — |
| `flag_gao_ending_stay` | `A:A_gao_ending` | `A:A_gao_ending/C_gao_ending_stay` | — |
| `flag_gao_honest` | `A:A_gao_meet` | `A:A_gao_meet/C_gao_meet_answer` | — |
| `flag_gao_met` | `A:A_gao_meet` | `A:A_gao_meet/C_gao_meet_answer`, `A:A_gao_meet/C_gao_meet_safe`, `A:A_gao_meet/C_gao_meet_ask` | — |
| `flag_gao_push2_deliver` | `A:A_gao_push2` | `A:A_gao_push2/C_gao_push2_deliver` | — |
| `flag_gao_push2_help` | `A:A_gao_push2` | `A:A_gao_push2/C_gao_push2_help` | — |
| `flag_gao_push2_safe` | `A:A_gao_push2` | `A:A_gao_push2/C_gao_push2_safe` | — |
| `flag_gao_push_ask` | `A:A_gao_push1` | `A:A_gao_push1/C_gao_push1_ask` | — |
| `flag_gao_push_grab` | `A:A_gao_push1` | `A:A_gao_push1/C_gao_push1_grab` | — |
| `flag_gao_push_wait` | `A:A_gao_push1` | `A:A_gao_push1/C_gao_push1_wait` | — |
| `flag_hakfan_allied` | `A:A_hakfan_crisis` | `A:A_hakfan_crisis/C_hakfan_crisis_ally` | — |
| `flag_hakfan_avoided` | `A:A_hakfan_meet` | `A:A_hakfan_meet/C_hakfan_meet_walk` | — |
| `flag_hakfan_cold_war` | `A:A_hakfan_ending` | `A:A_hakfan_ending/C_hakfan_ending_cold` | — |
| `flag_hakfan_deferred` | `A:A_hakfan_push2` | `A:A_hakfan_push2/C_hakfan_push2_defer` | — |
| `flag_hakfan_faced_off` | `A:A_hakfan_push2` | `A:A_hakfan_push2/C_hakfan_push2_match` | — |
| `flag_hakfan_leaked` | `A:A_hakfan_crisis` | `A:A_hakfan_crisis/C_hakfan_crisis_leak` | — |
| `flag_hakfan_mentor_complete` | `A:A_hakfan_ending` | `A:A_hakfan_ending/C_hakfan_ending_mentor` | — |
| `flag_hakfan_met` | `A:A_hakfan_meet` | `A:A_hakfan_meet/C_hakfan_meet_hold`, `A:A_hakfan_meet/C_hakfan_meet_probe`, `A:A_hakfan_meet/C_hakfan_meet_walk` | — |
| `flag_hakfan_negotiated` | `A:A_hakfan_push1` | `A:A_hakfan_push1/C_hakfan_push1_negotiate` | — |
| `flag_hakfan_own_style` | `A:A_hakfan_push2` | `A:A_hakfan_push2/C_hakfan_push2_own` | — |
| `flag_hakfan_probed` | `A:A_hakfan_meet` | `A:A_hakfan_meet/C_hakfan_meet_probe` | — |
| `flag_hakfan_rejected_support` | `A:A_hakfan_push1` | `A:A_hakfan_push1/C_hakfan_push1_reject` | — |
| `flag_hakfan_rival_respect` | `A:A_hakfan_ending` | `A:A_hakfan_ending/C_hakfan_ending_respect` | — |
| `flag_hakfan_solo` | `A:A_hakfan_crisis` | `A:A_hakfan_crisis/C_hakfan_crisis_solo` | — |
| `flag_hakfan_stand_ground` | `A:A_hakfan_meet` | `A:A_hakfan_meet/C_hakfan_meet_hold` | — |
| `flag_hakfan_took_support` | `A:A_hakfan_push1` | `A:A_hakfan_push1/C_hakfan_push1_take` | — |
| `flag_hiu_be` | `R1:R_hiu_ending` | `R1:R_hiu_ending/C_hiu_ending_be` | — |
| `flag_hiu_commit` | `R1:R_hiu_ending` | `R1:R_hiu_ending/C_hiu_ending_he` | — |
| `flag_hiu_he` | `R1:R_hiu_ending` | `R1:R_hiu_ending/C_hiu_ending_he` | — |
| `flag_ho_asked_why` | `A:A_ho_meet` | `A:A_ho_meet/C_ho_meet_ask` | — |
| `flag_ho_big_bet` | `A:A_ho_crisis` | `A:A_ho_crisis/C_ho_crisis_stay` | — |
| `flag_ho_cold_war` | `A:A_ho_ending` | `A:A_ho_ending/C_ho_ending_cold` | — |
| `flag_ho_crisis_ask` | `A:A_ho_crisis` | `A:A_ho_crisis/C_ho_crisis_ask` | — |
| `flag_ho_crisis_leave` | `A:A_ho_crisis` | `A:A_ho_crisis/C_ho_crisis_leave` | — |
| `flag_ho_crisis_stay` | `A:A_ho_crisis` | `A:A_ho_crisis/C_ho_crisis_stay` | — |
| `flag_ho_intro_round` | `A:A_ho_meet` | `A:A_ho_meet/C_ho_meet_follow` | — |
| `flag_ho_mentor_complete` | `A:A_ho_ending` | `A:A_ho_ending/C_ho_ending_complete` | — |
| `flag_ho_met` | `A:A_ho_meet` | `A:A_ho_meet/C_ho_meet_follow`, `A:A_ho_meet/C_ho_meet_ask` | — |
| `flag_ho_quality_trust` | `A:A_ho_push2` | `A:A_ho_push2/C_ho_push2_trust` | — |
| `flag_ho_refused_deal` | `A:A_ho_push1` | `A:A_ho_push1/C_ho_push1_refuse` | — |
| `flag_ho_rival_respect` | `A:A_ho_ending` | `A:A_ho_ending/C_ho_ending_respect` | — |
| `flag_ho_self_select` | `A:A_ho_push2` | `A:A_ho_push2/C_ho_push2_self` | — |
| `flag_ho_took_deal` | `A:A_ho_push1` | `A:A_ho_push1/C_ho_push1_take` | — |
| `flag_ho_trust_up` | `A:A_ho_push1` | `A:A_ho_push1/C_ho_push1_refuse` | — |
| `flag_hustle_board` | `C:C2` | `C:C2/C2_b` | — |
| `flag_ko_ally` | `A:A_lei_push1` | `A:A_lei_push1/C_lei_push1_seek_help` | — |
| `flag_ko_cold_war` | `A:A_ko_ending` | `A:A_ko_ending/C_ko_ending_cold` | — |
| `flag_ko_crisis_deal` | `A:A_ko_crisis` | `A:A_ko_crisis/C_ko_crisis_deal` | — |
| `flag_ko_crisis_fight` | `A:A_ko_crisis` | `A:A_ko_crisis/C_ko_crisis_fight` | — |
| `flag_ko_crisis_stepback` | `A:A_ko_crisis` | `A:A_ko_crisis/C_ko_crisis_stepback` | — |
| `flag_ko_mentor_complete` | `A:A_ko_ending` | `A:A_ko_ending/C_ko_ending_mentor` | — |
| `flag_ko_met_grab` | `A:A_ko_meet` | `A:A_ko_meet/C_ko_meet_grab` | — |
| `flag_ko_met_yield` | `A:A_ko_meet` | `A:A_ko_meet/C_ko_meet_yield` | — |
| `flag_ko_push1_counter` | `A:A_ko_push1` | `A:A_ko_push1/C_ko_push1_counter` | — |
| `flag_ko_push1_observe` | `A:A_ko_push1` | `A:A_ko_push1/C_ko_push1_observe` | — |
| `flag_ko_push2_ally` | `A:A_ko_push2` | `A:A_ko_push2/C_ko_push2_ally` | — |
| `flag_ko_push2_confront` | `A:A_ko_push2` | `A:A_ko_push2/C_ko_push2_confront` | — |
| `flag_ko_push2_ignore` | `A:A_ko_push2` | `A:A_ko_push2/C_ko_push2_ignore` | — |
| `flag_ko_rival_respect` | `A:A_ko_ending` | `A:A_ko_ending/C_ko_ending_respect` | — |
| `flag_lan_be` | `R2:R_lan_ending` | `R2:R_lan_ending/C_lan_ending_be` | — |
| `flag_lan_colleague` | `R2:R_lan_push2` | `R2:R_lan_push2/C_lan_push2_distance` | — |
| `flag_lan_commit` | `R2:R_lan_ending` | `R2:R_lan_ending/C_lan_ending_he` | — |
| `flag_lan_he` | `R2:R_lan_ending` | `R2:R_lan_ending/C_lan_ending_he` | — |
| `flag_lan_help` | `R2:R_lan_crisis` | `R2:R_lan_crisis/C_lan_crisis_help` | — |
| `flag_lan_met_cool` | `R2:R_lan_meet` | `R2:R_lan_meet/C_lan_meet_cool` | — |
| `flag_lan_met_warm` | `R2:R_lan_meet` | `R2:R_lan_meet/C_lan_meet_warm` | — |
| `flag_lan_protected` | `R2:R_lan_push2` | `R2:R_lan_push2/C_lan_push2_protect` | — |
| `flag_lan_sang_together` | `R2:R_lan_push1` | `R2:R_lan_push1/C_lan_push1_serious` | — |
| `flag_lan_stepback` | `R2:R_lan_crisis` | `R2:R_lan_crisis/C_lan_crisis_stepback` | — |
| `flag_lan_work_only` | `R2:R_lan_push1` | `R2:R_lan_push1/C_lan_push1_work` | — |
| `flag_legacy_film` | `C:C16` | `C:C16/C16_a` | — |
| `flag_legacy_refuse` | `C:C16` | `C:C16/C16_b` | — |
| `flag_lei_ally` | `A:A_lei_ending` | `A:A_lei_ending/C_lei_ending_ally` | — |
| `flag_lei_bluff` | `A:A_lei_meet` | `A:A_lei_meet/C_lei_meet_bluff` | — |
| `flag_lei_bound` | `A:A_lei_crisis` | `A:A_lei_crisis/C_lei_crisis_sign` | — |
| `flag_lei_cold_war` | `A:A_lei_ending` | `A:A_lei_ending/C_lei_ending_cold` | — |
| `flag_lei_contract_read` | `A:A_lei_meet` | `A:A_lei_meet/C_lei_meet_read`, `A:A_lei_push2`, `A:A_lei_push2/C_lei_push2_probe` | — |
| `flag_lei_crisis` | `A:A_lei_crisis` | `A:A_lei_crisis/C_lei_crisis_refuse`, `A:A_lei_crisis/C_lei_crisis_negotiate`, `A:A_lei_crisis/C_lei_crisis_sign` | — |
| `flag_lei_deal` | `A:A_lei_push2` | `A:A_lei_push2/C_lei_push2_join` | — |
| `flag_lei_defiant` | `A:A_lei_push1` | `A:A_lei_push1/C_lei_push1_stand` | — |
| `flag_lei_delay` | `C:C7` | `C:C7/C7_b` | — |
| `flag_lei_met` | `A:A_lei_meet` | `A:A_lei_meet/C_lei_meet_read`, `A:A_lei_meet/C_lei_meet_polite`, `A:A_lei_meet/C_lei_meet_bluff` | — |
| `flag_lei_negotiated` | `A:A_lei_crisis` | `A:A_lei_crisis/C_lei_crisis_negotiate` | — |
| `flag_lei_push1` | `A:A_lei_push1` | `A:A_lei_push1/C_lei_push1_stand`, `A:A_lei_push1/C_lei_push1_soften`, `A:A_lei_push1/C_lei_push1_seek_help` | — |
| `flag_lei_push2` | `A:A_lei_push2` | `A:A_lei_push2/C_lei_push2_join`, `A:A_lei_push2/C_lei_push2_refuse`, `A:A_lei_push2/C_lei_push2_probe` | — |
| `flag_lei_refuse_film` | `A:A_lei_push2` | `A:A_lei_push2/C_lei_push2_refuse` | — |
| `flag_lei_rival_respect` | `A:A_lei_ending` | `A:A_lei_ending/C_lei_ending_respect` | — |
| `flag_lei_signed` | `C:C7` | `C:C7/C7_c` | — |
| `flag_network_stay` | `C:C2` | `C:C2/C2_a` | — |
| `flag_public_romance` | `C:C9` | `C:C9/C9_a`, `C:C13`, `C:C13/C13_a` …(+2) | — |
| `flag_refuse_gig_with_ho` | `C:C4` | `C:C4/C4_a` | — |
| `flag_rival_respect` | `A:A_fong_ending` | `A:A_fong_ending/C_fong_ending_respect` | — |
| `flag_take_harsh_gig` | `C:C4` | `C:C4/C4_b` | — |
| `flag_tang_be` | `RT:R_tang_ending` | `RT:R_tang_ending/C_tang_ending_be` | — |
| `flag_tang_commit` | `RT:R_tang_ending` | `RT:R_tang_ending/C_tang_ending_he` | — |
| `flag_tang_crisis_data` | `RT:R_tang_crisis` | `RT:R_tang_crisis/C_tang_crisis_data` | — |
| `flag_tang_crisis_favor` | `RT:R_tang_crisis` | `RT:R_tang_crisis/C_tang_crisis_favor` | — |
| `flag_tang_crisis_middle` | `RT:R_tang_crisis` | `RT:R_tang_crisis/C_tang_crisis_middle` | — |
| `flag_tang_he` | `RT:R_tang_ending` | `RT:R_tang_ending/C_tang_ending_he` | — |
| `flag_tang_met` | `R2:R_tang_meet_stub/C_tang_meet_keep_contact` | — | — |
| `flag_tang_met_wait` | `RT:R_tang_meet` | `RT:R_tang_meet/C_tang_meet_wait` | — |
| `flag_tang_open` | `R2:R_tang_meet_stub` | `RT:R_tang_meet`, `RT:R_tang_meet/C_tang_meet_data` | `RT:R_tang_push1`, `RT:R_tang_push2`, `RT:R_tang_crisis`, `RT:R_tang_ending`, `RT:FILE:pushAndAfter` |
| `flag_tang_push1_exchange` | `RT:R_tang_push1` | `RT:R_tang_push1/C_tang_push1_exchange` | — |
| `flag_tang_push1_prove` | `RT:R_tang_push1` | `RT:R_tang_push1/C_tang_push1_prove` | — |
| `flag_tang_push2_business` | `RT:R_tang_push2` | `RT:R_tang_push2/C_tang_push2_business` | — |
| `flag_tang_push2_private` | `RT:R_tang_push2` | `RT:R_tang_push2/C_tang_push2_private` | — |
| `flag_tong_crisis_confess` | `A:A_tong_crisis` | `A:A_tong_crisis/C_tong_crisis_confess` | — |
| `flag_tong_crisis_leave` | `A:A_tong_crisis` | `A:A_tong_crisis/C_tong_crisis_leave` | — |
| `flag_tong_crisis_stay` | `A:A_tong_crisis` | `A:A_tong_crisis/C_tong_crisis_stay` | — |
| `flag_tong_ending_cold` | `A:A_tong_ending` | `A:A_tong_ending/C_tong_ending_cold` | — |
| `flag_tong_ending_mentor` | `A:A_tong_ending` | `A:A_tong_ending/C_tong_ending_mentor` | — |
| `flag_tong_ending_respect` | `A:A_tong_ending` | `A:A_tong_ending/C_tong_ending_respect` | — |
| `flag_tong_met_step_in` | `A:A_tong_meet` | `A:A_tong_meet/C_tong_meet_step_in` | — |
| `flag_tong_met_watch` | `A:A_tong_meet` | `A:A_tong_meet/C_tong_meet_watch` | — |
| `flag_tong_push1_accept` | `A:A_tong_push1` | `A:A_tong_push1/C_tong_push1_accept` | — |
| `flag_tong_push1_argue` | `A:A_tong_push1` | `A:A_tong_push1/C_tong_push1_argue` | — |
| `flag_tong_push2_doubt` | `A:A_tong_push2` | `A:A_tong_push2/C_tong_push2_doubt` | — |
| `flag_tong_push2_stay` | `A:A_tong_push2` | `A:A_tong_push2/C_tong_push2_stay` | — |
| `flag_tsijun_crisis_cut` | `A:A_tsijun_crisis` | `A:A_tsijun_crisis/C_tsijun_crisis_cut` | — |
| `flag_tsijun_crisis_hold` | `A:A_tsijun_crisis` | `A:A_tsijun_crisis/C_tsijun_crisis_hold` | — |
| `flag_tsijun_crisis_silent` | `A:A_tsijun_crisis` | `A:A_tsijun_crisis/C_tsijun_crisis_silent` | — |
| `flag_tsijun_ending_cold` | `A:A_tsijun_ending` | `A:A_tsijun_ending/C_tsijun_ending_cold` | — |
| `flag_tsijun_ending_complete` | `A:A_tsijun_ending` | `A:A_tsijun_ending/C_tsijun_ending_complete` | — |
| `flag_tsijun_ending_respect` | `A:A_tsijun_ending` | `A:A_tsijun_ending/C_tsijun_ending_respect` | — |
| `flag_tsijun_met_leave` | `A:A_tsijun_meet` | `A:A_tsijun_meet/C_tsijun_meet_leave` | — |
| `flag_tsijun_met_stay` | `A:A_tsijun_meet` | `A:A_tsijun_meet/C_tsijun_meet_stay` | — |
| `flag_tsijun_push1_grind` | `A:A_tsijun_push1` | `A:A_tsijun_push1/C_tsijun_push1_grind` | — |
| `flag_tsijun_push1_side` | `A:A_tsijun_push1` | `A:A_tsijun_push1/C_tsijun_push1_side` | — |
| `flag_tsijun_push2_film` | `A:A_tsijun_push2` | `A:A_tsijun_push2/C_tsijun_push2_film` | — |
| `flag_tsijun_push2_variety` | `A:A_tsijun_push2` | `A:A_tsijun_push2/C_tsijun_push2_variety` | — |
| `flag_vera_be` | `R1:R_vera_ending` | `R1:R_vera_ending/C_vera_ending_be` | — |
| `flag_vera_commit` | `R1:R_vera_ending` | `R1:R_vera_ending/C_vera_ending_he` | — |
| `flag_vera_cooperate` | `R1:R_vera_push1` | `R1:R_vera_push1/C_vera_push1_cooperate` | — |
| `flag_vera_he` | `R1:R_vera_ending` | `R1:R_vera_ending/C_vera_ending_he` | — |
| `flag_vera_honest` | `R1:R_vera_push2` | `R1:R_vera_push2/C_vera_push2_honest` | — |
| `flag_vera_met_cold` | `R1:R_vera_meet` | `R1:R_vera_meet/C_vera_meet_cold` | — |
| `flag_vera_met_warm` | `R1:R_vera_meet` | `R1:R_vera_meet/C_vera_meet_warm` | — |
| `flag_vera_perfunctory` | `R1:R_vera_push1` | `R1:R_vera_push1/C_vera_push1_perfunctory` | — |
| `flag_vera_stay` | `R1:R_vera_crisis` | `R1:R_vera_crisis/C_vera_crisis_stay` | — |
| `flag_vera_workfirst` | `R1:R_vera_crisis` | `R1:R_vera_crisis/C_vera_crisis_work` | — |
| `flag_vera_worktalk` | `R1:R_vera_push2` | `R1:R_vera_push2/C_vera_push2_work` | — |
| `flag_xu_be` | `R2:R_xu_ending` | `R2:R_xu_ending/C_xu_ending_be` | — |
| `flag_xu_business_only` | `R2:R_xu_push2` | `R2:R_xu_push2/C_xu_push2_business` | — |
| `flag_xu_commit` | `R2:R_xu_ending` | `R2:R_xu_ending/C_xu_ending_he` | — |
| `flag_xu_coop_decline` | `R2:R_xu_push1` | `R2:R_xu_push1/C_xu_push1_decline` | — |
| `flag_xu_coop_talk` | `R2:R_xu_push1` | `R2:R_xu_push1/C_xu_push1_accept` | — |
| `flag_xu_depend` | `R2:R_xu_crisis` | `R2:R_xu_crisis/C_xu_crisis_depend` | — |
| `flag_xu_he` | `R2:R_xu_ending` | `R2:R_xu_ending/C_xu_ending_he` | — |
| `flag_xu_met_distance` | `R2:R_xu_meet` | `R2:R_xu_meet/C_xu_meet_distance` | — |
| `flag_xu_met_polite` | `R2:R_xu_meet` | `R2:R_xu_meet/C_xu_meet_polite` | — |
| `flag_xu_personal_open` | `R2:R_xu_push2` | `R2:R_xu_push2/C_xu_push2_open` | — |
| `flag_xu_refuse` | `R2:R_xu_crisis` | `R2:R_xu_crisis/C_xu_crisis_refuse` | — |
| `flag_xu_respect` | `R2:R_xu_crisis` | `R2:R_xu_crisis/C_xu_crisis_respect` | — |
| `gossip_admit` | `C:C13` | `C:C13/C13_a` | — |
| `gossip_deny` | `C:C13` | `C:C13/C13_b` | — |
| `gossip_vague` | `C:C13` | `C:C13/C13_c` | — |
| `hiu_crisis_fight` | `R1:R_hiu_crisis` | `R1:R_hiu_crisis/C_hiu_crisis_b` | — |
| `hiu_crisis_yield` | `R1:R_hiu_crisis` | `R1:R_hiu_crisis/C_hiu_crisis_a` | — |
| `hiu_meet_distant` | `R1:R_hiu_meet` | `R1:R_hiu_meet/C_hiu_meet_b` | — |
| `hiu_meet_exchange` | `R1:R_hiu_meet` | `R1:R_hiu_meet/C_hiu_meet_a` | — |
| `hiu_push1_help` | `R1:R_hiu_push1` | `R1:R_hiu_push1/C_hiu_push1_a` | — |
| `hiu_push1_self` | `R1:R_hiu_push1` | `R1:R_hiu_push1/C_hiu_push1_b` | — |
| `hiu_push2_date` | `R1:R_hiu_push2` | `R1:R_hiu_push2/C_hiu_push2_a` | — |
| `hiu_push2_friend` | `R1:R_hiu_push2` | `R1:R_hiu_push2/C_hiu_push2_b` | — |
| `lan_blur` | `C:C9` | `C:C9/C9_c` | — |
| `lan_confess` | `C:C9` | `C:C9/C9_a` | — |
| `lan_cut` | `C:C9` | `C:C9/C9_b` | — |
| `love_crisis` | `C:C12` | `C:C12/C12_a` | — |
| `rel_tang_threshold` | `—（無 writer；條件代幣或僅消費）` | — | `RT:R_tang_push1`, `RT:R_tang_push2`, `RT:R_tang_crisis`, `RT:R_tang_ending`, `RT:FILE:pushAndAfter` |
| `rival_gao_endure` | `C:C3` | `C:C3/C3_b` | — |
| `rival_gao_hard` | `C:C3` | `C:C3/C3_a` | — |
| `route_commercial` | `C:C8` | `C:C8/C8_a` | — |
| `route_film` | `C:C1` | `C:C1/C1_b` | — |
| `route_indie` | `C:C8` | `C:C8/C8_b`, `C:C11`, `C:C11/C11_b` | — |
| `route_tv` | `C:C1` | `C:C1/C1_a` | — |

### 數值（stats）鍵（非 flag，供引擎狀態機）

`craft`／`fame`／`music`／`wealth`／`standing`／`trust`／`rel_vera`／`rel_hiu`／`rel_choi`／`rel_lan`／`rel_xu`／`rel_tang`／`rel_mei`／`rel_cheung`／`rel_partner`

> `rel_partner`：C12 抽象鍵；引擎需解析為當前高好感或已 commit 線。`rel_mei`：關海媚暧昧，無 commit。

### qa.flagAlias（Pack1；非破壞性 rename）

| 舊裸前綴 | 建議 flag_* |
|---|---|
| `hiu_meet_exchange` | `flag_hiu_meet_exchange` |
| `hiu_meet_distant` | `flag_hiu_meet_distant` |
| `hiu_push1_help` | `flag_hiu_push1_help` |
| `hiu_push1_self` | `flag_hiu_push1_self` |
| `hiu_push2_date` | `flag_hiu_push2_date` |
| `hiu_push2_friend` | `flag_hiu_push2_friend` |
| `hiu_crisis_fight` | `flag_hiu_crisis_fight` |
| `hiu_crisis_yield` | `flag_hiu_crisis_yield` |
| `choi_meet_honest` | `flag_choi_meet_honest` |
| `choi_meet_official` | `flag_choi_meet_official` |
| `choi_give_tip` | `flag_choi_give_tip` |
| `choi_refuse_tip` | `flag_choi_refuse_tip` |
| `choi_real_date` | `flag_choi_real_date` |
| `choi_keep_professional` | `flag_choi_keep_professional` |
| `choi_deny_romance` | `flag_choi_deny_romance` |

引擎建議：讀檔時正規化；存檔可雙寫過渡。

---

## 8. 不一致／Soft leftovers／可行動缺口

（**本輪不自動再跑 Soft**；除非標成硬 blockers。以下僅列表。）

| # | 嚴重度 | 項 | 說明 | 建議 |
|---|---|---|---|---|
| 1 | **硬接線** | C／多數 R／A 無 `openConditions` | 只有 Tang push+ 同 stub／meet 有欄；主線靠 UNLOCK 文件 | 引擎實作 UNLOCK 方向條件；或後補 JSON 欄（另任務） |
| 2 | **硬接線** | 原型未載入 story_detail_* | `index.html` 只 fetch `story_beats_phase1`／npc／events／tutorial | Phase1 消費順序見 §9：先掛 C1–C7 |
| 3 | **硬接線** | 通告板未用標註欄 | 內嵌 GIGS 無 boardPriority／eraTag／seasonWeight | 改讀 `gigs_1988.json` 或同步 build |
| 4 | Soft leftover | `R_tang_meet_stub.flags_written` 仍含 `flag_tang_open` | Soft 已改 choice→`flag_tang_met`；節點級陣列未對齊；notes／openConditionsNote 正確 | 下輪 Soft：節點 flags_written 改 `[flag_tang_met]` 或不列 open |
| 5 | Soft leftover | Pack1 裸前綴 flags | `qa.flagAlias` 已備；flags_written 未 rename | 引擎 alias；或非破壞性雙寫 |
| 6 | Soft leftover | Pack3 ending `parallelOk: true` | Soft outstanding；感情 ending 為 false | 定 rival ending 是否允許並行再改 |
| 7 | 慣例 | Tang `conflict` 自由字串 | Pack2 慣例 T→conflict；Tang 無 T 碼 | 接線可忽略或後補敘事 conflict id |
| 8 | 雙軌 | C3↔A_ko、C1↔A_tsijun、C4↔A_ho、C7↔A_lei、C8↔A_gao／A_tsijun、C10↔A_ko_crisis、C11↔A_tsijun_crisis、C12↔A_gao_crisis／A_ko_ending、C14↔R_xu、C15↔R_lan、C9↔R_lan_push2、C13↔R_choi | 主線節點與弧節點內容重疊 | 定「主線為準／弧為加戲」或合併觸發政策 |
| 9 | 抽象鍵 | `rel_partner` | 僅 C12 | 引擎映射表 |
| 10 | 教學雙軌 | `B01`–`B10` vs `C1`–`C7` | 原型章節文案仍係舊 beats | Phase1 可先並存：B 做週報／教學，C 做重大抉擇 UI |
| 11 | 消費稀疏 | 大多數 flag 無 JSON 內 consumer | openConditions 極少；結局鎖靠 C17 選擇＋文件優先序 | 結局引擎讀 MASTER／UNLOCK §6；不宜只靠 flag 自動推導 |
| 12 | 非 blockers | Vera 線仍有 speaker「阿偉」；Pack3 parallelOk；出圖；1989 年庫；週≥2 high 模擬 | Soft §仍 outstanding | 另排程 |

---

## 9. 建議引擎消費順序（Phase1 原型）

目標：C1–C7 + 1988 通告板 + 早期感情 meet；**仍不出圖、不做 1989 年庫**。

1. **資料載入**
   - 讀 `gigs_1988.json`（取代或同步內嵌 GIGS）；locs 顯示：`tvb_longmen`→星河電視台
   - 讀 `story_detail_c1_to_c17.json`（至少 C1–C7）
   - 讀 Pack1 romance（Vera／hiu／choi 的 meet；C5／C6 相關）
   - 可選：Pack3 之 `A_ho_meet`／`A_ko_meet`／`A_tsijun_meet`／`A_lei_*`（與 C2–C4／C7 雙軌政策先定）
   - 保留現有 `story_beats_phase1.json` 作教學／週章節，直至 C 節點 UI 接上
2. **通告板**
   - 過濾當季 → 以 `boardPriority`（high>normal>low）排序 → 乘 `seasonWeight` → 套現有育成 hard-gate
   - 期望：每季有足夠 high 露出（標註已達覆蓋）
3. **主線觸發（方向性／playtest）**
   - C1：首個重要通告後（T1）
   - C2：C1 後何生事件
   - C3：同場高俊傑搶板
   - C4：可疑通告／何生拒單
   - C5：采兒門檻或夏台慶籌備（playtest）
   - C6：至少一 rel 達約會門檻（playtest）；選 Vera／曉晴／采兒之一
   - C7：秋冬雷勁苛約；寫 `flag_anti_lei` 等
4. **早期感情**
   - `R_vera_meet`／`R_hiu_meet`／`R_choi_meet`：P1 與通告／C5 交錯
   - 鄧／藍／徐：**不**入 Phase1 強制路徑（藍 P2、徐 P3、鄧 meet P3）
5. **旗標寫入**
   - 只寫 choices.effects；讀 node.flags_written 作枚舉／QA
   - Pack1 經 `qa.flagAlias` 正規化
6. **暫緩**
   - C8+、Tang 雙閘、Pack3 ending、藝術資源、1989 gigs

---

## 10. 版本腳註＋檔案清單

| 項 | 值 |
|---|---|
| 本檔 | `content/WIRING_DRAFT_v1.md`（v1） |
| 權威計劃 | `PLOT_MASTER_PLAN_v1.4-DS.md`、`PLOT_DETAIL_UNLOCK_v1.md` |
| Soft | `SOFT_NITS_FIX_v1.md`（已套；本輪不重跑） |
| 主線 JSON | `story_detail_c1_to_c17.json` v1 |
| 感情 JSON | `story_detail_romance_vera_hiu_choi.json` v1.1；`…_lan_xu.json` v2.1；`…_tang.json` v1.1 |
| 對手 JSON | `story_detail_rival_mentor.json` v2.1 |
| 通告 | `gigs_1988.json` v2.1.1 |
| 原型 | `index.html`（現消費 story_beats／內嵌 GIGS；尚未接 story_detail） |
| store 同步 | 本 md → bot store 根目錄（同 Soft 慣例） |

### 本輪觸碰檔

- `content/WIRING_DRAFT_v1.md`（新建）
- store：`WIRING_DRAFT_v1.md`（複製）
- **未改**任何 story JSON／gigs／index.html

### 計數摘要

- 主線 C 節點：**17**
- 感情節點（含 stub）：**31**（Pack1 15 + Pack2 11 + Tang 5）
- 對手／導師節點：**40**（8 弧）
- Unique flags／條件代幣：**241**
- gigs_1988：**30** 則；標註欄 30/30

*完 — WIRING_DRAFT_v1*
