# WIRING_JSON_CONDITIONS_v1

> **時間：** 2026-11-02（Asia/Hong_Kong）  
> **依據：** `WIRING_DRAFT_v1.md`、`PLOT_DETAIL_UNLOCK_v1.md`、`SOFT_NITS_FIX_v1.md`  
> **目的：** 把解鎖／出現條件寫入 story detail JSON 節點級欄位，供引擎直接讀取。  
> **非目標：** 不改對白／synopsis；不改 `index.html`；不做 1989 年庫／出圖；Soft leftovers 原則 HOLD。

---

## 1. Schema 約定

| 欄位 | 型別 | 語義 |
|---|---|---|
| `openConditions` | `string[]` | **AND**：全部滿足才可開；`[]`＝無額外旗閘（仍受 `phase`／`when` 約束） |
| `openConditionsAny` | `string[]`（可選） | **OR**：若存在，須至少滿足一項，並與 `openConditions` 同時成立 |
| `openConditionsNote` | `string`（可選） | 方向性說明、雙軌政策、playtest 提示 |
| `thresholds` | `object`（可選） | `rel_*_threshold` 等；可 `null`＋ note＝playtest；Tang push+＝**2** |
| 檔級 `conditionSchema` | object | 本檔語義說明 |
| 檔級 `openConditions`（僅 Tang） | object | `meet`／`pushAndAfter`／`rel_tang_threshold`（既有，保留） |

**Token 慣例：** `C*`／`R_*`／`A_*`＝節點完成；`flag_*`／裸前綴／`route_*`＝旗標；`rel_*_threshold`／`fame_threshold`＝數值門檻（playtest）；`phase_P*`＝phase；`season_*`／`era_*`＝季節軟匹配。

與 Tang 陣列 AND schema 相容；Tang **不**使用 `openConditionsAny`。

---

## 2. 版本 bump

| 檔案 | 前 | 後 |
|---|---|---|
| `story_detail_c1_to_c17.json` | 1 | **1.1** |
| `story_detail_romance_vera_hiu_choi.json` | 1.1 | **1.2** |
| `story_detail_romance_lan_xu.json` | 2.1 | **2.2** |
| `story_detail_romance_tang.json` | 1.1 | **1.2** |
| `story_detail_rival_mentor.json` | 2.1 | **2.2** |

---

## 3. 主線 C1–C17 對照

| id | openConditions (AND) | openConditionsAny (OR) | thresholds | Note 摘要 |
|---|---|---|---|---|
| `C1` | `[]` | — | — | 開局／教學後首次重要通告選擇時觸發（方向性）。phase=P1；衝突 T1。引擎亦可掛首次重要通告事件。 |
| `C2` | `["C1"]` | — | — | C1 完成後；何生在場事件（方向性）。 |
| `C3` | `["C2"]` | — | — | C2 後與高俊傑同場搶板（方向性）。可與 A_ko_meet 雙軌（sync／互斥政策另定）。 |
| `C4` | `["C3"]` | — | — | 何生帶來可疑／苛刻通告（方向性）。可與 A_ho_push1 雙軌。 |
| `C5` | `["C4"]` | `["rel_choi_threshold", "season_1988_summer_anni_prep"]` | 有 | 方向性／playtest：C4 後，且（rel_choi 達門檻 OR 1988 夏台慶籌備季）。門檻數值未鎖死。 |
| `C6` | `["C5"]` | `["rel_vera_threshold", "rel_hiu_threshold", "rel_choi_threshold"]` | 有 | 方向性／playtest：至少一條可攻略線達約會門檻；可平行未確定。門檻數值 playtest。 |
| `C7` | `["C6"]` | — | — | P1.5 可提前；若玩家未觸，引擎可於進入 P2 且尚未寫 flag_anti_lei／flag_lei_delay／flag_lei_si |
| `C8` | `["C7"]` | — | — | 進入 1989／P2；高文瀚機會與張子駿邀約同時可見（方向性）。可與 A_gao_meet／A_tsijun_push2 雙軌。 |
| `C9` | `["C8"]` | `["flag_lan_met_warm", "flag_lan_met_cool"]` | — | 方向性／playtest：藍若曦線已開芽（meet 任一旗）＋狗仔事件。可與 R_lan_push2 連動。 |
| `C10` | `["C9"]` | — | — | 台慶季＋高俊傑競爭位（方向性）；衝突 T2。可與 A_ko_crisis／A_ko_push2 雙軌。 |
| `C11` | `["C10"]` | `["route_indie", "flag_tsijun_met_stay", "flag_tsijun_push1_grind", "flag_tsijun_push2_film"]` | — | 張子駿線進行中（任一導師推進旗或 route_indie）＋影展／文藝檔（方向性）；衝突 T3。可與 A_tsijun_crisis 雙軌。 |
| `C12` | `["C11"]` | — | — | 方向性／playtest：中高 tier＋已有確定或高好感線（引擎映射 rel_partner／commit）。衝突 T4。可與 C15／C |
| `C13` | `["C11"]` | `["rel_choi_threshold", "rel_mei_threshold", "fame_threshold", "R_choi_crisis"]` | 有 | 方向性／playtest：周采兒或關海媚事件鏈＋fame 門檻；可與 R_choi_crisis 連動。關海媚無 commit。P4 內不強 |
| `C14` | `["C11"]` | `["flag_xu_met_polite", "flag_xu_met_distance", "flag_xu_coop_talk", "R_xu_crisis"]` | — | 徐寶珊線開芽＋金援邀請（方向性）；衝突 T6。可與 R_xu_crisis 連動。 |
| `C15` | `["C11"]` | `["flag_lan_sang_together", "flag_lan_protected", "flag_lan_met_warm", "rel_lan_threshold", "R_lan_crisis"]` | 有 | 方向性／playtest：藍若曦高好感／推進後＋家族壓事件。可與 R_lan_crisis 連動。when＝1991春，可早於 C12。 |
| `C16` | `["phase_P5"]` | — | — | 進入 1992 結局季；金九／傳承事件（方向性）。建議 P4 至少完成關鍵節之一，精確集合 playtest。 |
| `C17` | `["C16"]` | — | — | C16 後；事業數值＋旗標齊（方向性）。結算優先序：玩家最終選擇＞旗標＞數值（UNLOCK §6）。 |

**前：** 全無。**後：** 17／17。

---

## 4. 感情線對照

### Pack1（15）— 前 0 → 後 15

| id | AND | ANY |
|---|---|---|
| `R_vera_meet` | `[]` | `—` |
| `R_vera_push1` | `[]` | `["flag_vera_met_warm", "flag_vera_met_cold"]` |
| `R_vera_push2` | `[]` | `["flag_vera_cooperate", "flag_vera_perfunctory"]` |
| `R_vera_crisis` | `[]` | `["flag_vera_honest", "flag_vera_worktalk"]` |
| `R_vera_ending` | `["phase_P5"]` | `["flag_vera_stay", "flag_vera_workfirst", "flag_vera_honest", "flag_vera_worktalk"]` |
| `R_hiu_meet` | `[]` | `—` |
| `R_hiu_push1` | `[]` | `["hiu_meet_exchange", "hiu_meet_distant"]` |
| `R_hiu_push2` | `[]` | `["hiu_push1_help", "hiu_push1_self"]` |
| `R_hiu_crisis` | `[]` | `["hiu_push2_date", "hiu_push2_friend"]` |
| `R_hiu_ending` | `["phase_P5"]` | `["hiu_crisis_fight", "hiu_crisis_yield", "hiu_push2_date", "hiu_push2_friend"]` |
| `R_choi_meet` | `[]` | `—` |
| `R_choi_push1` | `[]` | `["choi_meet_honest", "choi_meet_official", "choi_honest", "choi_spin", "choi_dodge"]` |
| `R_choi_push2` | `[]` | `["choi_give_tip", "choi_refuse_tip"]` |
| `R_choi_crisis` | `[]` | `["choi_real_date", "choi_keep_professional"]` |
| `R_choi_ending` | `["phase_P5"]` | `["flag_public_romance", "choi_deny_romance", "choi_real_date", "choi_keep_professional"]` |

### Pack2（11）— 前僅 stub 有 `[]` → 後 11

| id | AND | ANY | Soft |
|---|---|---|---|
| `R_lan_meet` | `["phase_P2"]` | `—` | — |
| `R_lan_push1` | `[]` | `["flag_lan_met_warm", "flag_lan_met_cool"]` | — |
| `R_lan_push2` | `[]` | `["flag_lan_sang_together", "flag_lan_work_only"]` | — |
| `R_lan_crisis` | `[]` | `["flag_lan_protected", "flag_lan_colleague", "flag_lan_sang_together"]` | — |
| `R_lan_ending` | `["phase_P5"]` | `["flag_lan_help", "flag_lan_stepback", "flag_family_help", "flag_family_yield", "flag_family_standby", "flag_lan_protected"]` | — |
| `R_xu_meet` | `["phase_P3"]` | `—` | — |
| `R_xu_push1` | `[]` | `["flag_xu_met_polite", "flag_xu_met_distance"]` | — |
| `R_xu_push2` | `[]` | `["flag_xu_coop_talk", "flag_xu_coop_decline"]` | — |
| `R_xu_crisis` | `[]` | `["flag_xu_personal_open", "flag_xu_business_only", "flag_xu_coop_talk"]` | — |
| `R_xu_ending` | `["phase_P5"]` | `["flag_xu_respect", "flag_xu_depend", "flag_xu_refuse", "flag_bao_respect", "flag_bao_depend", "flag_bao_refuse"]` | — |
| `R_tang_meet_stub` | `[]` | `—` | HOLD：flags_written 仍列 flag_tang_open |

### Tang（5）— 條件維持；push+ 補 thresholds=2

| id | openConditions | thresholds |
|---|---|---|
| `R_tang_meet` | `[]` | — |
| `R_tang_push1` | `["flag_tang_open", "rel_tang_threshold"]` | {"rel_tang_threshold": 2, "rel_tang_threshold_note": "playtest 可調；與檔級 openConditions.rel_tang_threshold 一致"} |
| `R_tang_push2` | `["flag_tang_open", "rel_tang_threshold"]` | {"rel_tang_threshold": 2, "rel_tang_threshold_note": "playtest 可調；與檔級 openConditions.rel_tang_threshold 一致"} |
| `R_tang_crisis` | `["flag_tang_open", "rel_tang_threshold"]` | {"rel_tang_threshold": 2, "rel_tang_threshold_note": "playtest 可調；與檔級 openConditions.rel_tang_threshold 一致"} |
| `R_tang_ending` | `["flag_tang_open", "rel_tang_threshold"]` | {"rel_tang_threshold": 2, "rel_tang_threshold_note": "playtest 可調；與檔級 openConditions.rel_tang_threshold 一致"} |

檔級：`meet=[]`；`pushAndAfter=[flag_tang_open, rel_tang_threshold]`；`rel_tang_threshold=2`。

---

## 5. Pack3 對手／導師（40）— 前 0 → 後 40

| id | AND | ANY（節選） | linksMain（既有） |
|---|---|---|---|
| `A_ko_meet` | `[]` | `[]` | ['C3'] |
| `A_ko_push1` | `[]` | `["flag_ko_met_grab", "flag_ko_met_yield"]` | — |
| `A_ko_push2` | `[]` | `["flag_ko_push1_counter", "flag_ko_push1_observe"]` | ['C10', 'T2'] |
| `A_ko_crisis` | `[]` | `["flag_ko_push2_ally", "flag_ko_push2_confront", "flag_ko_push2_ignore", "flag_ko_push1_counter"]…` | ['C10', 'T2'] |
| `A_ko_ending` | `["phase_P4"]` | `["flag_ko_crisis_deal", "flag_ko_crisis_fight", "flag_ko_crisis_stepback", "flag_ko_push2_ally"]…` | ['C12'] |
| `A_hakfan_meet` | `["phase_P2"]` | `[]` | ['P2資源場'] |
| `A_hakfan_push1` | `[]` | `["flag_hakfan_met"]` | — |
| `A_hakfan_push2` | `[]` | `["flag_hakfan_negotiated", "flag_hakfan_rejected_support", "flag_hakfan_took_support"]` | — |
| `A_hakfan_crisis` | `[]` | `["flag_hakfan_deferred", "flag_hakfan_faced_off", "flag_hakfan_own_style"]` | ['P2', 'P3', 'P4'] |
| `A_hakfan_ending` | `["phase_P5"]` | `["flag_hakfan_allied", "flag_hakfan_leaked", "flag_hakfan_solo"]` | — |
| `A_tsijun_meet` | `[]` | `[]` | ['C1', 'T1'] |
| `A_tsijun_push1` | `[]` | `["flag_tsijun_met_leave", "flag_tsijun_met_stay"]` | — |
| `A_tsijun_push2` | `[]` | `["flag_tsijun_push1_grind", "flag_tsijun_push1_side"]` | ['C8'] |
| `A_tsijun_crisis` | `[]` | `["flag_tsijun_push2_film", "flag_tsijun_push2_variety", "route_indie", "C8"]` | ['C11', 'T3'] |
| `A_tsijun_ending` | `["phase_P5"]` | `["flag_tsijun_crisis_cut", "flag_tsijun_crisis_hold", "flag_tsijun_crisis_silent", "C17"]…` | ['C17', 'E03'] |
| `A_fong_meet` | `[]` | `[]` | — |
| `A_fong_push1` | `[]` | `["flag_fong_met"]` | — |
| `A_fong_push2` | `[]` | `["flag_fong_push1_learn", "flag_fong_push1_let", "flag_fong_push1_watch"]` | — |
| `A_fong_crisis` | `["phase_P3"]` | `["flag_fong_push2_leave", "flag_fong_push2_rest", "flag_fong_push2_train"]` | ['P3替身危機'] |
| `A_fong_ending` | `["phase_P5"]` | `["flag_fong_crisis_call", "flag_fong_crisis_freeze", "flag_fong_crisis_rescue", "flag_fong_saved_once"]…` | ['E05'] |
| `A_tong_meet` | `["phase_P2"]` | `[]` | ['P2去留'] |
| `A_tong_push1` | `[]` | `["flag_tong_met_step_in", "flag_tong_met_watch"]` | ['P2去留'] |
| `A_tong_push2` | `[]` | `["flag_tong_push1_accept", "flag_tong_push1_argue"]` | ['P2去留'] |
| `A_tong_crisis` | `[]` | `["flag_tong_push2_doubt", "flag_tong_push2_stay"]` | ['E09'] |
| `A_tong_ending` | `["phase_P5"]` | `["flag_tong_crisis_confess", "flag_tong_crisis_leave", "flag_tong_crisis_stay"]` | ['E09'] |
| `A_ho_meet` | `[]` | `[]` | ['C2'] |
| `A_ho_push1` | `[]` | `["flag_ho_met"]` | ['C4'] |
| `A_ho_push2` | `[]` | `["flag_ho_refused_deal", "flag_ho_took_deal", "flag_ho_trust_up"]` | — |
| `A_ho_crisis` | `["phase_P4"]` | `["flag_ho_quality_trust", "flag_ho_self_select"]` | ['E01'] |
| `A_ho_ending` | `["phase_P5"]` | `["flag_ho_big_bet", "flag_ho_crisis_ask", "flag_ho_crisis_leave", "flag_ho_crisis_stay"]` | ['E01'] |
| `A_gao_meet` | `["phase_P2"]` | `[]` | ['C8'] |
| `A_gao_push1` | `[]` | `["flag_gao_met"]` | — |
| `A_gao_push2` | `[]` | `["flag_gao_push_ask", "flag_gao_push_grab", "flag_gao_push_wait"]` | — |
| `A_gao_crisis` | `[]` | `["flag_gao_push2_deliver", "flag_gao_push2_help", "flag_gao_push2_safe", "C12"]` | ['C12', 'T4'] |
| `A_gao_ending` | `["phase_P5"]` | `["flag_gao_crisis_commit", "flag_gao_crisis_honest", "flag_gao_crisis_stepback"]` | ['E02'] |
| `A_lei_meet` | `["phase_P1_5"]` | `[]` | — |
| `A_lei_push1` | `[]` | `["flag_lei_met"]` | — |
| `A_lei_push2` | `[]` | `["flag_ko_ally", "flag_lei_defiant", "flag_lei_push1", "phase_P2"]` | — |
| `A_lei_crisis` | `[]` | `["flag_lei_bluff", "flag_lei_contract_read", "flag_lei_met", "flag_ko_ally"]…` | ['C7'] |
| `A_lei_ending` | `["phase_P5"]` | `["flag_anti_lei", "flag_lei_bound", "flag_lei_negotiated", "flag_lei_crisis"]…` | ['flag_anti_lei'] |

---

## 6. 未改項（HOLD／下一輪）

| 項 | 狀態 |
|---|---|
| `index.html` 掛載 story_detail／gigs_1988 | **未改**（下一輪） |
| 1989 年庫／出圖／週≥2 high 模擬 | **未做** |
| `R_tang_meet_stub.flags_written` 含 `flag_tang_open` | Soft **HOLD**（choice 仍寫 `flag_tang_met`；Note 已標明） |
| Pack1 裸前綴 flags／`qa.flagAlias` rename | Soft **HOLD**（openConditions 引用現存裸名） |
| Pack3 ending `parallelOk: true` | Soft **HOLD** |
| 徐寶珊 tier 數值 | Soft **HOLD**（meet 僅 `phase_P3`） |
| 對白／synopsis 正文 | **未改** |
| phase 分冊 JSON（`story_detail_phase*.json`） | **未同步**（權威＝`c1_to_c17` merge；分冊另任務） |
| C↔A／R 雙軌 sync 政策 | 僅 Note 標明；引擎政策另定 |

---

## 7. 仍存 gaps（接線後）

1. 原型尚未 fetch 本批 JSON（硬接線仍在 index 輪）。
2. playtest 門檻（`rel_*_threshold`／`fame_threshold`）多為 `null`，待數值校準。
3. 節點完成 token（`C1`、`R_vera_meet`）需引擎進度表；JSON 不自動寫 `*_done`。
4. P4 主線 `C12`–`C15` 以 `C11` 為共同前置、彼此不強制串鏈（對齊 when 春夏秋冬）；引擎須按曆排序。
5. Soft stub／裸旗／parallelOk／徐 tier 仍 HOLD。

---

## 8. 驗收清單

- [x] C1–C17 皆有 `openConditions`
- [x] Pack1 15 節皆有 `openConditions`
- [x] Pack2 lan／xu／stub 皆有；stub 維持可開 `[]`
- [x] Tang meet=`[]`；push1+＝雙閘＋ threshold 2
- [x] Pack3 40 節皆有 `openConditions`
- [x] 對白／synopsis 未改（僅 meta／edits／version／qa）
- [x] index／1989／出圖未動
- [x] Soft leftovers 未主動大修
- [x] 本 md＋JSON 已 sync store

---

## 9. 檔案清單

- `content/story_detail_c1_to_c17.json`
- `content/story_detail_romance_vera_hiu_choi.json`
- `content/story_detail_romance_lan_xu.json`
- `content/story_detail_romance_tang.json`
- `content/story_detail_rival_mentor.json`
- `content/WIRING_JSON_CONDITIONS_v1.md`（本檔）
- store 根目錄：同上檔名複本

- 本輪補／對齊：主線 17 + Pack1 15 + Pack2 11 + Pack3 40＝**83** 節寫入／對齊 OC；Tang 5 節條件確認，其中 4 節補 `thresholds`

*完 — WIRING_JSON_CONDITIONS_v1*
