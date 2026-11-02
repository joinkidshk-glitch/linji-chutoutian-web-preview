# QA_GIGS_1988_FIX_v1

> 《臨記出頭天》gigs_1988 **v2.1** 季節口吻＋星河顯示名修好｜文件 QA（**不改正文**）
>
> 對照：`gigs_1988.json` v2.1、`gigs_1988_pre_fix_v21_backup.json`、`GIGS_1988_FIX_v1.md`、`worldview.json`、`index.html`、前次 `QA_GIGS_1988_ANNOTATION_v1.md`；季節規劃：台慶≈11月、賀歲≈1–2月、春勿賀歲
>
> QA 時間：2026-11-02（Asia/Hong_Kong）

## Overall

**PASS with nits**

- Canonical **`content/gigs_1988.json` v2.1** 季節口吻硬核全過；保護欄對 pre_fix backup **0 diff**；high 春4夏4秋2冬4 且 high＝當季主詞。
- **`tvb_longmen` id 不變**；`worldview.json` companies＋`index.html` LOCS **display name＝星河電視台**。
- 可作 Phase1 wiring（以 `content/gigs_1988.json`＋worldview 為準）。
- **出圖仍暫緩**。

---

## 1. Hard — 保護欄 vs `gigs_1988_pre_fix_v21_backup.json`

| 檢查 | 結果 |
|---|---|
| id 集合 30＝30 | PASS |
| `pay`／`fame`／`req`／`hard`／`tier`／`id`／`loc`／`boardPriority`／`eraTag`／`seasonWeight` | **PASS 0 diff** |
| 改動範圍僅 claimed 4 則 | PASS（其餘 26 則深比全等） |
| claimed 改動欄 | `var_01`：title／blurb／synopsis／boardNote／discoverNote／roleHint／diasporaHook（7）；`var_05`：title／blurb／synopsis／boardNote／discoverNote／heroAngle／diasporaHook（7）；`var_02`：blurb／boardNote／discoverNote（3）；`tv_07`：blurb／boardNote／discoverNote（3） |

註：相對 annotation 鐵律（synopsis／title／blurb 不動）——本輪**刻意**改寫上述 title／blurb／synopsis（用戶季節口吻修好）；屬預期，不記 FAIL。

---

## 2. Hard — 季節口吻（canonical JSON）

| 規則 | 結果 | 抽核 |
|---|---|---|
| `var_01` 春：無「賀歲／過年／龍年」 | **PASS** | title→《今宵同樂》茶樓夥計烏龍短劇；blurb／synopsis／notes 皆日常／草根 |
| `var_05`／`tv_07`：無「台慶」；賀歲檔口吻 | **PASS** | `var_05` title《歲月星輝賀歲夜》；`tv_07` blurb「跨年賀歲檔大劇」；兩則全文無「台慶」 |
| `var_02` 夏：允許「台慶」**僅作籌備季** | **PASS** | blurb／boardNote／discoverNote 皆「台慶籌備」；無「台慶晚會／壓軸」誤植 |
| 全庫掃描其餘「賀歲／台慶／龍年」 | INFO | `ad_02` 春「龍年大婚」、`rec_04`「龍年金曲」等**未改**（非本輪 scope，且非春賀歲違規）；冬線賀歲落在 `var_05`／`tv_07`／`film_05`／`film_06`／`ad_07`（否定句）——合理 |

---

## 3. Hard — high／eraTag 主詞

| 季 | high | 目標 | high.eraTag ∈ 當季主集合 |
|---|---|---|---|
| 春 | 4 | 4 | PASS（含 `var_01`→`era_1988_spring_grassroot`） |
| 夏 | 4 | 4 | PASS（含 `var_02`→`era_1988_summer_variety`） |
| 秋 | 2 | 2 | PASS |
| 冬 | 4 | 4 | PASS（含 `var_05`／`tv_07`→`era_1988_winter_festive`） |

`boardPriority`／`eraTag`／`seasonWeight` 對 backup **未改**（與 FIX 自稱一致）。

---

## 4. Hard — 禁詞／專名

| 檢查 | 結果 |
|---|---|
| `gigs_1988.json` 正文（除 `loc` id）無「龍門／無線／TVB」 | **PASS**（0 hit） |
| `worldview.json` `companies[]` 中 `locId=tvb_longmen` 且 `name=星河電視台` | **PASS**（id 欄為 `locId`，非改 id） |
| `index.html` LOCS：`{ id:"tvb_longmen", name:"星河電視台", area:"九龍塘", ...}` | **PASS** |
| `index.html` 內嵌 GIGS 字串無「龍門／無線／TVB」 | **PASS** |

---

## 5. Soft / nits（不擋 wiring）

1. **`index.html` 內嵌 GIGS 未完全跟 v2.1**  
   - claimed 四則：`title`／`blurb`／`synopsis`／（除下）多數口吻欄已對齊。  
   - **`gig_1988_var_02.discoverNote` 仍為舊句**（「監製高文瀚為手下新人爭取的黃金時段大型節目曝光名額。」），缺「星河台慶籌備季…」——若 runtime 讀 index 內嵌而非 `content/gigs_1988.json`，夏檔 discover 口吻會偏舊（blurb 已有籌備季，硬核仍勉強可過）。  
   - 內嵌 GIGS **仍缺** `boardNote`／`boardPriority`／`seasonWeight`；`eraTag` 仍為舊 array 標籤——屬 annotation 起已有之 sync 債，非本輪引入，但 FIX 自稱「內嵌 GIGS 對應口吻」未 100% 達標。

2. **`sv-phone-preview/content/` 路徑不存在**  
   - `GIGS_1988_FIX_v1.md` 列已同步 preview；本機 workspace **無**該目錄 → soft miss／文件自檢偏樂觀。

3. **npc／cast 仍「龍門」**（本輪 scope 外，只報告）  
   - `npc_lines_core.json`：如「今天在龍門電視廠…」「龍門電視那邊缺班底…」  
   - `cast_main.json`：如「喺龍門電視龍套組…」「平日龍門審本…」  
   - 另：`content/_gigs_1988_parts/*`、部分 raw prompt 備份仍舊稱——非正式 canonical。

4. **Annotation 鐵律刻意打破**（預期）  
   - 相對 `gigs_1988_pre_annotation_backup.json`：`var_01`／`var_05` 的 title＋blurb＋synopsis、`var_02`／`tv_07` 的 blurb 已變——用戶季節修好優先；不記 FAIL。

5. **index／json 既有 drift（非本輪）**  
   - 例：`gig_1988_tv_01` JSON `discoverNote`＝「片場人情爭取的龍套開工」；index 內嵌仍「阿偉在星河電視台片場…」——說明雙軌內容源，wiring 應 **只認 `content/`**。

---

## 6. Wiring／出圖

| 項 | 判定 |
|---|---|
| Phase1 wiring（通告板季節＋星河顯示名） | **OK**（以 `content/gigs_1988.json` v2.1＋`worldview.json` 為 canonical） |
| 出圖 | **仍暫緩** |
| 建議後續（非 blocker） | 補齊 index 內嵌 `var_02.discoverNote`；統一 runtime 單一內容源；另開票清 npc／cast「龍門」→「星河」 |

---

## 7. 對 Manager 一句

`gigs_1988` v2.1 季節口吻＋星河 display：**PASS with nits**；保護欄／四季硬核／專名 OK；出圖仍暫緩。Nits：index 內嵌 `var_02.discoverNote` 未跟、preview 路徑缺失、npc／cast 仍龍門（scope 外）。
