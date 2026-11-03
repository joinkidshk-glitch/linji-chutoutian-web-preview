# ART BRIEF｜通告 Detail＝《明星志願》招募單 layout＋切圖方向 v1

> **日期：** 2026-11-03（Asia/Hong_Kong）  
> **觸發：** tester 轉用戶——通告 detail 跟《明星志願》招募單；參考 `/workspace/ref-mv-casting-notice.png`。  
> **對齊：** `PLAN_GIG_CASTING_NOTICE_DETAIL_v1.md`（劇本字段／派生／禁詞）、`UI_PHYSICAL_CANON.md`（紙 `#E6D2A8`、印章、Noto／禁止 AI CJK）、`PLAN_GIG_CARD_PLAYER_COPY_v1`、`HANDOFF_DS_PLAYER_ZH_FILTER_v1`。  
> **閘門：** **出圖 HOLD** — 本票只交 **layout／wire／9-slice 方向**；**禁止** Krea／GenerateImage／最終彩繪資產。線框／標註 PNG wire／ASCII／SVG **OK**。  
> **Soft≠PASS**  
> **交：** GD（版式＋切片表）／iOS（stub `?v=18v` 對齊本 brief；本機 modal 內 scroll）／Tester（A＋B 上板後對十一欄）

---

## 0. Goal

玩家點開通告 Detail，要見到**一張真・招募單**（非列表短卡），字段與 MV 參考圖右欄對齊，紙質跟現有 `notice_paper`／色票加深票根感。左立繪／海報牆 **phone 可收合或置頂 optional**；**phone 優先 sheet-first stacked**。

本 brief **唔產成圖**；等用戶／tester **開閘** 先入階段 D 美術。

---

## 1. Phone constraints（iOS stub）

| Token | 值 | 備註 |
|---|---|---|
| Device safe | ~390×844 | iPhone 邏輯；`safe_pad` 頂 54／底 34 pt（canon） |
| Modal | 全寬或 inset ~12–16；`max-height` ~78dvh | 內層 `#modal-inner` **豎滾**；底 `#modal-btns` sticky |
| Sheet width | content ≈ 358–366 pt | 左右紙邊／9-slice cap 外 |
| Bust／poster | optional | phone：**預設收合**；可「展開立繪」；landscape／iPad 可左欄 |
| `.sp-*` 無關 | — | 本頁係 **gig casting sheet**，唔套 StoryPlay bust layout |

現網頁已用 `notice_paper` 做 modal 紙底；本 brief 係 **full casting sheet** 結構（header／tabs／條件格／星／簡介框），唔止一張紙底。

---

## 2. Zone map — sheet-first stacked（phone portrait）

優先序上→下（跟 `PLAN_GIG_CASTING_NOTICE_DETAIL_v1` §4，並改為直向 stack）：

```
┌─ modal（paper #E6D2A8／notice_sheet_frame）─────────────┐
│ [optional] notice_poster_wall／立繪條（可收合）            │
│ ┌ notice_header_orange ──────────────────────────────┐ │
│ │ 作品名 workTitle（大白字）          導演 slot        │ │
│ └────────────────────────────────────────────────────┘ │
│ [notice_tag_type]  [notice_tag_recruiting 紅]            │
│ ┌ notice_period_bar ─────────────────────────────────┐ │
│ │ 通告期間：…，共 N 週                                  │ │
│ └────────────────────────────────────────────────────┘ │
│ [notice_tab_on] [notice_tab_off…]   ← MVP 可單 tab     │
│ ┌ conditions grid（notice_table_*）──────────────────┐ │
│ │ 條件（左）     │ 難易度 ★★★★☆（notice_star_*）     │ │
│ │ req 合／未合   │ 每週 N 天／總天 M／片酬／簽約—／特殊— │ │
│ └────────────────────────────────────────────────────┘ │
│ ┌ notice_synopsis_frame ─────────────────────────────┐ │
│ │ 劇情簡介（synopsis；可選上排「角色：roleHint」）      │ │
│ └────────────────────────────────────────────────────┘ │
│              [btn_leave 離開]  [約試鏡／報名]             │
└─────────────────────────────────────────────────────────┘
```

**PC／寬屏 optional：** 左 `notice_poster_wall`（海報牆＋立繪）｜右上表 sheet（跟參考圖）。Phone **唔強制**左欄。

詳細 ASCII／標註見：`assets/ui-physical/notice/CASTING_DETAIL_WIRE.md`。

---

## 3. MV classic zones → 我方字段

對齊 `PLAN_GIG_CASTING_NOTICE_DETAIL_v1.md` §1（十一欄）：

| # | MV 區 | 我方顯示 | 綁定／派生（建議 field） |
|---|---|---|---|
| 1 | 橙頭作品名 | **作品名** | `workTitle` → 否則 `title`《》內文 → 否則整段 `title` |
| 2 | 類型 pill | **類型** | `genreLabel` → 否則 `type`（電影／電視劇／廣告／唱片通告／綜藝） |
| 3 | 紅標招募中 | **招募中**／已截止／製作中／已殺青／已取消 | **引擎派生**（唔入 JSON）；見 PLAN §3.3 |
| 4 | 導演章／slot | **導演** | `director`；缺 →「組製未公開」 |
| 5 | 通告期間橙條 | **通告期間** | `castWindow.{startHint,endHint,weeks}` 或 season+year+shootDeadlineDays+shootDaysHint 派生 |
| 6 | 角色分頁 | **角色** tabs | `roles[]`；MVP **單 tab**＝現可報位（`roleHint`／label） |
| 7 | 條件表 | **條件** | 既有 `req`（+聲望地板）；**預設合／未合**，`SHOW_REQ_THRESHOLD=false` |
| 8 | 難易度星 | **難易度** 1–5★ | 由 `tier`／`hard`／`roleScale` 映射（PLAN §3.6） |
| 9 | 工作時間／天數 | **每週**／**總天** | `shootWeekdays.length`；`shootDaysHint`（唱片用語見 PLAN） |
| 10 | 酬勞 | **片酬**；簽約／特殊 MVP「—」 | `pay[0]–pay[1]` |
| 11 | 徵求簡介 | **劇情簡介** | `synopsis`；可選 `roleHint` 作角色小節 |
| — | 離開 | **離開** | `btn_leave`；另主 CTA「約試鏡／報名」 |

禁詞（顯示面）：有板／看板／硬鎖／唔能試／差 N／你 X／睇板／薄本 —— 見 PLAN §5＋DS filter。

---

## 4. Wireframe + 9-slice（明確區段）

### 4.1 結構元素（上→下）必須可對切圖

| UI 元素 | artId（建議） | 切法 | 行為 |
|---|---|---|---|
| 整張招募單外框／紙 | `notice_sheet_frame` | **9-slice** | 鋪滿 modal 內容區；沿用／加深 `notice_paper` 亦可，另出 sheet 框若要灰bevel |
| 橙頭標題條 | `notice_header_orange` | **9-slice** 或左右 cap + stretch | 左作品名 live 字；右可嵌導演 slot |
| 類型 pill | `notice_tag_type` | **9-slice**／stretch pill | 內 live 類型字；色可跟 type token（sky／rose／jade／violet） |
| 紅「招募中」 | `notice_tag_recruiting` | stretch／cap | 狀態派生；截止／殺青可另 `notice_tag_status_*` 或同底換字色 |
| 導演 slot | （header 內區 or `notice_director_slot`） | stretch／icon+框 | 小導演剪影 icon 可選；名 live |
| 通告期間條 | `notice_period_bar` | **9-slice** 橫條 | 橙 stripe；文案 live |
| 角色 tab 開／關 | `notice_tab_on`／`notice_tab_off` | stretch／cap | MVP 單 on；多角色後切 |
| 條件格／表 | `notice_table_cell`（+ optional `notice_table_frame`） | 9-slice cell／frame | 左條件列、右難易度／天／酬 |
| 難易度星 | `notice_star_on`／`notice_star_off` | **icon** | 1–5；唔燒數字 |
| 每週／總天／片酬 | （table 右欄 live） | — | 無獨立圖亦可；可要 `notice_meta_row` 底 |
| 劇情簡介框 | `notice_synopsis_frame` | **9-slice** | 可選直書「劇情簡介」裝飾（**Noto 燒錄**，禁 AI CJK） |
| 左海報牆／立繪 | `notice_poster_wall` | stretch／full | phone optional／收合；PC 左欄 |
| 離開掣 | `btn_leave` | 9-slice／hud 掣風格 | 對齊 physical HUD 膠掣感；可 reuse `btn_primary` 變體 |
| 印章 | 既有 `seal_junior|mid|senior|urgent` | **seal** 單層 | 列表／角標沿用；Detail 可用 tier→seal 角 |

### 4.2 9-slice 建議（@3x 邏輯 pt → 資產 px ≈ ×3）

| artId | type | 建議邏輯尺寸 | @3x 約 | capInsets 起步（pt） | notes |
|---|---|---|---|---|---|
| `notice_sheet_frame` | 9-slice | 366×640+ scroll | 1098×1920+ | t28 l36 b36 r28 | 可對齊現 `slices.json`→`notice_paper`；加深紙 `#E6D2A8` |
| `notice_header_orange` | 9-slice | 340×44 | 1020×132 | t8 l16 b8 r16 | 白字作品名 live；右留導演 88–110 pt |
| `notice_tag_type` | stretch／9-slice pill | h28；w content+24 | h84 | l14 r14 t6 b6 | 藍／類型色底 |
| `notice_tag_recruiting` | stretch／pill | h28 | h84 | 同上 | **紅**；文案「招募中」live 或 Noto 短燒 |
| `notice_period_bar` | 9-slice | 340×32 | 1020×96 | t6 l12 b6 r12 | 橙條；期間字 live 12–13 pt |
| `notice_tab_on` | stretch／cap | h36；min-w 88 | h108 | l12 r12 | 選中藍／實心 |
| `notice_tab_off` | stretch／cap | h36 | h108 | 同上 | 未選白／淡粉邊 |
| `notice_table_frame` | 9-slice | 340×160+ | 1020×480+ | t12 l12 b12 r12 | 淺藍格感（實體紙印，唔似 CSS table） |
| `notice_table_cell` | 9-slice | 可变 | — | t8 l8 b8 r8 | 條件／右欄共用 |
| `notice_star_on` | icon | 18×18 | 54×54 | — | 實心星（金／藍擇一；跟 canon gold `#C9A227` 優先） |
| `notice_star_off` | icon | 18×18 | 54×54 | — | 空心／淡 |
| `notice_synopsis_frame` | 9-slice | 340×120+ | 1020×360+ | t16 l16 b16 r16 | 內 padding 給長 synopsis |
| `notice_poster_wall` | stretch | phone 頂 120–180 高；PC 左 ~160 w | ×3 | — | 海報牆感；**無**真實商標 |
| `btn_leave` | 9-slice | h44；min-w 96 | h132 | l20 r20 t10 b10 | 橙圓角；跟參考「離開」 |
| `seal_*` | seal | 既有 | — | — | **reuse**；唔重畫除非 QC |

開閘後把上表寫入 `assets/ui-physical/slices.json`（新 key）；**而家唔改資產檔**。

### 4.3 Typography（硬規則）

- App live：**PingFang HK／系統中文**（canon 字級：H1 22–24／H2 17–18／正文 15–16／輔助 12–13）。  
- 燒錄短標（pill／直書「劇情簡介」／印章）：**本機 Noto／Source Han TC only**。  
- **禁止 AI 生成漢字**（任何最終或半最終彩圖）。

---

## 5. Data binding notes（iOS）

建議 ViewModel／render 對照（派生邏輯以 PLAN §3 為準）：

```text
workTitleDisplay     ← workTitle | extract《》from title | title
genreLabelDisplay    ← genreLabel | map(type, roleScale)
recruitStatusLabel   ← engine: 招募中|製作中|已殺青|已取消|已截止
directorDisplay      ← director || "組製未公開"
periodDisplay        ← castWindow format | year+season+deadline+daysHint
roles[] / activeRole ← roles[] (playerSlot) | synthetic single from roleHint
conditionsRows[]     ← req keys → "演技：合組製要求" | "未合組製要求"（SHOW_REQ_THRESHOLD=false）
difficultyStars      ← 1..5 from tier/hard/roleScale
workDaysPerWeek      ← unique(shootWeekdays).length
totalDays            ← shootDaysHint
payDisplay           ← pay[0]–pay[1]
contractDisplay      ← "—"（MVP）
specialDisplay       ← "—"（MVP）
synopsisText         ← synopsis
roleBlurb            ← roleHint（optional 小節）
```

保留既有 gig 欄：`id type title loc season tier req pay synopsis roleHint roleScale shootDaysHint shootWeekdays shootDeadlineDays hard fame…`。新欄增量唔破舊客戶（PLAN §2）。

CTA：離開 dismiss；主按鈕「約試鏡」／「報名」跟現引擎，**文案禁**睇板／跑板。

---

## 6. What NOT to produce until gate opens

- ❌ 最終彩繪 `notice_*` PNG／JPG（Krea、GenerateImage、手繪 finals）  
- ❌ AI CJK 標題／簡介字燒進圖  
- ❌ 左欄全套角色立繪牆（可攻略／雜角）— 另票；C1 劇情 bust **唔入**本 notice 包  
- ❌ 改 Soft＝PASS；唔宣佈 G0 通告美術完成  
- ❌ 真商標／真人導演名  

**允許（本票）：** 本 md、ASCII／SVG wire、標註框線 PNG wire、切片表、iOS stub 用 CSS／現 `notice_paper` 搭骨架。

---

## 7. Phased handoff

| 階段 | 誰 | 內容 |
|---|---|---|
| **A** | iOS＋GD | Detail 跟本 zone map；字段全用 PLAN §3 派生；無新 JSON 亦可出板 |
| **B** | iOS | 合／未合條件；DS 禁詞；version bump stub |
| **C** | 劇本 | 補 `workTitle`／`genreLabel`／`director`；（可選）`castWindow`；多 `roles` 暫緩 |
| **D** | GD | **開閘後** 按 §4 出 9-slice／pill／星／tab／synopsis 框；poster_wall optional |

Wire 檔：`assets/ui-physical/notice/CASTING_DETAIL_WIRE.md`  
Canon：`assets/ui-physical/UI_PHYSICAL_CANON.md`  
劇本 PLAN：`content/PLAN_GIG_CASTING_NOTICE_DETAIL_v1.md`

Soft≠PASS · **出圖 HOLD**。
