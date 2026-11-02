# Soft nits 補齊｜SOFT_NITS_FIX_v1

> **時間：** 2026-11-02（Asia/Hong_Kong）  
> **範圍：** 既有 QA Soft nits；**不**開新包、**不**出圖、**不**做 1989 年庫／引擎 wiring／週≥2 high 模擬。  
> **風格：** 書面語＋`COPY_STYLE_HK_LEXICON.md`；禁薄本／趕板／苛約。

---

## 勾選清單

| # | 項 | 前後 | 狀態 |
|---|---|---|---|
| 1 | 專名「龍門」→「星河」（cast／npc／gigs edits／parts；loc id 不變） | 玩家可見 龍門：cast+npc 共 4 → **0**（僅 edits 註記殘） | ✅ |
| 2a | 鄧 `R_tang_meet` openConditions 清空；meet 可寫 `flag_tang_open` | 前：meet 亦 AND 雙閘（雞生蛋）；後：`[]` | ✅ |
| 2b | push1+ 雙閘＋`rel_tang_threshold=2`（playtest 可調） | 前：僅 token；後：檔頂／rule／qa 寫死 2 | ✅ |
| 2c | Tang synopsis／setting「你」→「阿偉」 | synopsis 你 14→**0**；阿偉 0→13+ | ✅ |
| 2d | 輕潤 跳住／企得住／孭／識做 | body 清；qa 留 retarget 註 | ✅ |
| 2e | Pack2 stub 勿寫 `flag_tang_open`→`flag_tang_met`＋`rel_tang` | keep_contact flags 已改；notes 指向 `R_tang_meet` | ✅ |
| 3a | Pack3 title／setting 書面（v2.1） | title 口語 8→0；setting 21→0 | ✅ |
| 3b | Pack3 label「留低／企硬／學嘢」 | 清 | ✅ |
| 3c | Pack3 synopsis「你」→「阿偉」 | 40／40 | ✅ |
| 3d | parallelOk | **未改**（依 brief） | ⏭ |
| 4a | Pack1 Choi crisis `linksMain:[C13]` | 已補 | ✅ |
| 4b | Choi choice `R_choi_*`→`C_choi_*` | 8 ids rename | ✅ |
| 4c | hiu／choi speaker「我」→旁白＋pcSilent | 玩家 beats 已轉第三人稱敘 | ✅ |
| 4d | `qa.flagAlias`（不破壞性 rename flags） | 已加 | ✅ |
| 5a | Pack2 conflict：T→conflict；C→linksMain | 藍 C9／C15；徐 T6＋C14 | ✅ |
| 5b | 藍 meet synopsis 鋪合唱 | 加一句指向 push1 | ✅ |
| 6 | 本 md＋bump version＋cp store | 見下 | ✅ |

## 鄧閘前後

| 節 | 前 openConditions | 後 |
|---|---|---|
| 檔級 | `['flag_tang_open','rel_tang_threshold']` | `{meet:[], pushAndAfter:[…], rel_tang_threshold:2}` |
| `R_tang_meet` | 雙閘（死鎖風險） | `[]`（可寫入 open） |
| push1／push2／crisis／ending | 雙閘 | 雙閘＋threshold=2 |
| stub `C_tang_meet_keep_contact` | `flag_tang_open` | `flag_tang_met`＋`rel_tang` |

## 龍門剩餘

- **玩家可見 content（cast／npc／story／gigs body）：0**
- **edits 審計註記**（「龍門→星河」說明句）：cast_main／npc_lines 各 1 —— 可接受
- **backup／QA／舊 bak**：不改
- **loc id `tvb_longmen`：** 保留

## Pack3 title 抽樣（v2.1）

1. `A_hakfan_meet`：「試鏡房門外的世家子弟」
2. `A_tong_push2`：（原書面 title 保留）「去留一句鉤」；label「同唐老師講，想留下多學一點」
3. `A_gao_crisis`：「賀歲檔的賭注」

## 改動檔列表

- `content/cast_main.json`
- `content/npc_lines_core.json`
- `content/gigs_1988.json`（edits 註記）
- `content/_gigs_1988_parts/tv.json`、`var.json`
- `content/story_detail_romance_tang.json`（v1.1）
- `content/story_detail_romance_lan_xu.json`（v2.1）
- `content/story_detail_rival_mentor.json`（v2.1）
- `content/story_detail_romance_vera_hiu_choi.json`（v1.1）
- `content/PLOT_DETAIL_ROMANCE_TANG_v1.md`
- `content/PLOT_DETAIL_ROMANCE_LAN_XU_v1.md`
- `content/PLOT_DETAIL_RIVAL_MENTOR_v1.md`
- `content/PLOT_DETAIL_ROMANCE_V1.md`
- `content/SOFT_NITS_FIX_v1.md`（本檔）
- store 同步：上述 JSON／本 md

## 仍 outstanding（本輪不做）

- 出圖；1989–1992 年庫；引擎 wiring
- 週≥2 high 通告板模擬
- Vera 線仍保留 speaker「阿偉」對白（非「我」；本輪只清 hiu／choi）
- Pack3 ending `parallelOk` 慣例（未改）
