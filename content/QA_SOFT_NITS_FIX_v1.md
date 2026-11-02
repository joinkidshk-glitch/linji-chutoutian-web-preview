# QA｜Soft nits 補丁覆測 SOFT_NITS_FIX_v1（文件｜非 browser）

> **範圍：** `SOFT_NITS_FIX_v1.md` 聲稱改動：`story_detail_romance_tang.json` **v1.1**、`story_detail_romance_lan_xu.json` **v2.1**、`story_detail_rival_mentor.json` **v2.1**、`story_detail_romance_vera_hiu_choi.json` **v1.1**、`cast_main.json`、`npc_lines_core.json`（＋ gigs edits／parts 顯示名）。  
> **對照：** `QA_ROMANCE_TANG_v1.md`、`QA_ROMANCE_LAN_XU_v1.md`、`QA_RIVAL_MENTOR_v2.md`、`QA_ROMANCE_VERA_HIU_CHOI_v1.md`、`QA_GIGS_1988_FIX_v1.md`（npc／cast 龍門 nit）。  
> **Canon：** `PLOT_MASTER_PLAN_v1.4-DS.md`、`PLOT_DETAIL_UNLOCK_v1.md`、`COPY_STYLE_HK_LEXICON.md`。  
> **規則：** Soft≠PASS・唔 publish；書面語／現代港產詞；出圖暫緩；`tvb_longmen` id 可留、顯示名＝星河；保護欄勿誤改。  
> **本輪：** 只報告、**未改**任何 story content；**不出圖／不 browser**。  
> **時間：** 2026-11-02 23:42（Asia/Hong_Kong）

---

## Overall：**PASS with nits**

| 層 | 結果 |
|---|---|
| 重點 1–5（鄧 meet 空閘／push 雙閘／threshold=2／stub→`flag_tang_met`／龍門→星河顯示） | **PASS** |
| FIX 聲稱其餘 soft（Tang synopsis 阿偉、Pack3 title／setting／label、Choi `linksMain`＋`C_*`、hiu／choi 旁白、lan conflict 慣例、藍 meet 合唱鋪） | **PASS**（見 checklist） |
| 硬鎖回歸（禁詞／口語標記／星河／真人／政治／HE·BE＋commit／`C_*`／pcSilent 意圖／出圖暫緩） | **PASS**（無回歸弄壞先前 PASS 硬項） |
| Soft remaining（stub 元數據 `flags_written` 舊值；Vera 裸旗＋阿偉 speaker；Pack3 ending `parallelOk`；cast 徐 tier） | **NIT** |
| FYI：`index.html` `var_02.discoverNote` | **已與 JSON 對齊**（不擋本 verdict；FIX 未主打但現況 OK） |

**出圖仍暫緩。** Soft≠PASS → 本輪 **唔升純 PASS／唔 publish**。

---

## 1. 重點驗收 checklist

| # | 項 | 實際值（引用） | 結果 |
|---|---|---|---|
| 1 | 鄧 meet `openConditions=[]` | `R_tang_meet.openConditions=[]`；檔級 `openConditions.meet=[]`；`qa.meet_openConditions=[]` | **PASS**（雞生蛋打破） |
| 2 | push1+ 雙閘 | `R_tang_push1`／`push2`／`crisis`／`ending` 皆 `["flag_tang_open","rel_tang_threshold"]`；檔級 `pushAndAfter` 同 | **PASS** |
| 3 | `rel_tang_threshold=2` | 檔級 `openConditions.rel_tang_threshold=2`；`qa.rel_tang_threshold_value=2`；note「playtest 可調」 | **PASS** |
| 4 | stub→`flag_tang_met` | `C_tang_meet_keep_contact.effects.flags=["flag_tang_met"]`＋`rel_tang:1`；notes「正式開閘見 R_tang_meet」；**不再**寫 `flag_tang_open` | **PASS**（choice 實寫） |
| 5 | cast／npc「龍門」→「星河」；loc id 不變 | 玩家可見（除 `edits`）cast／npc **龍門=0**；例 cast `meetCondition`「星河電視台龍套組」、npc `colleague.greet`「星河電視台廠房」；`locPlaceholderMap.LOC_001=tvb_longmen`、homes 仍 `tvb_longmen`；`worldview.companies` `locId=tvb_longmen`／`name=星河電視台` | **PASS** |
| 6a | Tang synopsis「你」→「阿偉」 | synopsis 你=**0**／阿偉=**13**；`qa.synopsis_pov=阿偉` | **PASS** |
| 6b | Tang 跳住／企得住／孭／識做 | **body（nodes）0**；僅 `qa.oral_leftover_retarget` 留對照註 | **PASS**（與 FIX「body 清；qa 留」一致） |
| 6c | Pack3 title／setting 書面 | title oral **0／40**；setting oral **0／40**；抽樣 `A_hakfan_meet`「試鏡房門外的世家子弟」、`A_gao_crisis`「賀歲檔的賭注」 | **PASS** |
| 6d | Pack3 label 留低／企硬／學嘢 | **0**；`C_tong_push2_stay`＝「同唐老師講，想留下多學一點」 | **PASS** |
| 6e | Pack3 synopsis「你」→「阿偉」 | synopsis 你=**0**／阿偉=**117**（40 節） | **PASS** |
| 6f | Pack3 `parallelOk` | **未改**（ending 全 `true`；僅 `A_fong_crisis=false`）——FIX 標 ⏭ | **PASS（預期未改）** |
| 6g | Choi crisis `linksMain:[C13]` | `R_choi_crisis.linksMain=["C13"]`；`conflict=null` | **PASS** |
| 6h | Choi choice `R_choi_*`→`C_choi_*` | meet→ending 全 `C_choi_*`（8 ids） | **PASS** |
| 6i | hiu／choi speaker「我」→旁白 | speaker「我」=**0**；hiu／choi speakers＝林曉晴／周采兒／旁白／… | **PASS** |
| 6j | `qa.flagAlias` | 已加（hiu／choi 裸前綴→`flag_*` 對照表）；**未**破壞性改 flags 本體 | **PASS**（聲稱範圍） |
| 6k | Pack2 conflict：T→conflict；C→linksMain | `R_lan_push2` conflict=null／`linksMain:[C9]`；`R_lan_crisis`／`[C15]`；`R_xu_crisis` conflict=`T6`／`linksMain:[C14]` | **PASS** |
| 6l | 藍 meet synopsis 鋪合唱 | 末句「後來台慶合唱綵排的機會，要等到下一次再遇上她。」→指向 push1 | **PASS** |

---

## 2. 回歸（先前硬 PASS 不可弄壞）

| 項 | 結果 | 證據 |
|---|---|---|
| 版本 bump | **PASS** | tang **1.1**／lan_xu **2.1**／rival **2.1**／vera **1.1** |
| 禁詞 body（薄本／趕板／苛約／拖字訣） | **PASS** | 四包 nodes **0** |
| 口語標記（beats／synopsis／label／notes） | **PASS** | tang 0／44；lan 0／94；rival 0／450；vera 0／181（同前輪方法） |
| TVB／無線顯示名；星河 | **PASS** | romance／rival 顯示「星河」；loc id `tvb_longmen` 保留於 cast map／homes／worldview／gigs `loc` |
| 真人藝名／政治 | **PASS** | 抽樣 周星馳／六四／民運等 **0**（本輪掃 nodes） |
| HE／BE＋commit | **PASS** | tang／lan／xu／vera／hiu／choi 旗齊 |
| Choice id `C_*` | **PASS** | 本輪改動包非 `C_`＝**0**（Choi 已統一） |
| 鄧／藍徐／Pack3 節數 | **PASS** | tang 5；lan_xu 11；rival 40；vera 15 |
| 出圖 | **PASS（暫緩）** | 仍佔位；本輪未出圖 |
| gigs 保護欄意圖 | **PASS／INFO** | FIX 僅 edits／parts 顯示名；canonical `gigs_1988.json` version **2.1.1**（季節口吻既有 v2.1 基礎上）——未見本輪誤改 pay／id 之硬傷 |

---

## 3. Soft remaining（不升 FAIL）

1. **`R_tang_meet_stub.flags_written` 仍為 `["flag_tang_open"]`**，與 choice 實寫 `flag_tang_met` **不一致**。notes／`openConditionsNote` 已正確。Wiring 若讀 `flags_written` 元數據會誤判——建議下一刀改成 `["flag_tang_met"]` 或刪該欄。  
2. **Vera 裸旗標仍在 effects**（`hiu_*`／`choi_*` 無 `flag_` 前綴，約 15 處）；本輪僅加 `qa.flagAlias`——符合 FIX「不破壞性 rename」，**wiring 須讀 alias**。  
3. **Vera 線 speaker「阿偉」仍在**（FIX outstanding）——非「我」；hiu／choi 已旁白化。  
4. **Pack3 ending `parallelOk=true`**（FIX ⏭ 未改）——延續 v1／v2 soft。  
5. **`cast_main` 徐寶珊 `tier=阻力`**——前輪 Pack2 soft，本 FIX 未聲稱；不擋。  
6. **（資訊）** stub synopsis 仍敘述「正式開線需 flag_tang_open＋rel_tang」——語意正確，非錯寫。

---

## 4. 額外抽查｜index `var_02.discoverNote`

| 源 | discoverNote |
|---|---|
| `content/gigs_1988.json` `gig_1988_var_02` | 「星河台慶籌備季的黃金時段曝光」 |
| `index.html` 內嵌同 id | **相同** |

→ 前輪 `QA_GIGS_1988_FIX_v1` soft（index 未跟）**現已對齊**。FIX 未把此项列為本輪主修復；**不擋／不抬升** Soft nits 主 verdict。Wiring 仍建議以 `content/` 為準。

---

## 5. 建議下一步

1. 小修 stub `flags_written` → `flag_tang_met`（或移除）後可再極短覆核。  
2. Wiring 草案：鄧線用 meet 空閘＋push 雙閘＋`rel_tang>=2`；stub 只加 rel／met。  
3. Vera wiring 讀 `qa.flagAlias`；可另開破壞性 rename 票。  
4. **出圖仍暫緩**；唔 publish（Soft≠PASS）。  
5. Pack3 `parallelOk`／徐 cast tier 可另票。

---

## 6. 一句給用戶／劇本 manager

**Soft nits FIX：PASS with nits**（`QA_SOFT_NITS_FIX_v1.md`）。重點 1–5 全達標；其餘 FIX 聲稱項達標；回歸硬鎖未壞。Soft remaining：stub `flags_written` 舊值、Vera 裸旗／阿偉 speaker、Pack3 ending `parallelOk`、徐 tier。**出圖仍暫緩。**
