# NOTES · Freeplay v20a7 DESIGN — 定期頒獎禮（四媒介各自獎軌）

> **時間：** 2026-11-07（Asia/Hong_Kong）  
> **狀態：** 設計拍板；**已實裝 v20a7**（見 `NOTES_V20A7_AWARDS_CEREMONY.md`）；Soft≠PASS；**唔 tip LIVE**；**唔發明長 romance**；玩家面**禁真藝名／真獎項名**  
> **Repo：** `joinkidshk-glitch/linji-chutoutian-web-preview` · 實裝見 v20a7 NOTES  
> **SAVE：** 維持 `starVolunteer_map_v19w`（只加欄，唔抬 key）  
> **預覽：** `?v=20a7&softBehaviorGate=1`  
> **契約：** 實裝後再補 `docs/CONTENT_CONTRACT.md` §3.6；本檔係拍板依據  
> **修訂：** 用戶否決「只做電視／台慶」MVP → **唱片／電視／電影／廣告四條獨立獎軌**必須都有 Soft 體驗（可輕量，但唔能只留一軌）

---

## 0. 審計：規劃 vs 現況（缺咗咩）

| 來源 | 有咩 | 係咪「定期頒獎禮系統」 |
|---|---|---|
| `content/worldview.json` | 「文藝片搏獎」、台慶季嘉賓位 | 世界觀一句，**無引擎** |
| `STUB_FAVOR_DEBT_SEASON_v1.json` → `hook_autumn_award` | 季節鉤「台慶前後」＠`tvb_longmen` | **只係人情債氣氛**，無頒獎流程 |
| 主線 C5／C10、通告庫 | 台慶籌備／後台搶位 flavor | **劇情／通告**，唔係週期獎禮 |
| `gigs_1992.json` taboos | 禁「真實…獎項名」 | 必須用**虛構獎名** |
| v20a3–v20a6 殺青獎勵 | 報紙／新聞／街上 fans／**票房・收視・銷量・關注度** | **兄弟系統**；按 gig type 分 metrics，**唔係年度典禮** |
| 本輪草稿 | schema／stub 曾只偏 TV＋P1 影／街坊票 | **已改：四媒介各一典禮** |

**結論：** 「定期頒獎禮」未實裝。殺青獎勵已按四種通告類型分成績（電影→票房、劇／綜→收視、唱片→銷量、廣告→關注度）——獎禮設計**必須跟住四軌**，唔可以縮成單一電視台慶。

---

## 1. Goals / Non-goals / HOLD

### Goals（Soft）

1. **四媒介各自有年度獎軌**：唱片／音樂、電視（劇＋綜藝／台慶類）、電影、廣告——玩家做邊種通告，就感受到邊種「年底有人記」。  
2. **季節錯開**，一年內唔會四晚疊爆；每軌 1／曆年。  
3. 雙軌有意義：  
   - **幕前聲量 `stageVolume`** → 人氣／街坊／「最受歡迎」類  
   - **業內信用 `industryCredit`** → 評審／新人／「專業肯定」類  
4. 同殺青獎勵 `matchTypes`／`metrics.kindByGigType` **對齊**（見 §4.3）。  
5. Freeplay-ready：schema＋stub＋`S.*` log＋console self-check；內容 bot 只填短粵語／書面 punch。  
6. 同主線台慶事態、人情債季節鉤**並行唔吞**；短卡唔長弧。  
7. 缺席／落選都好玩；唔鎖地圖、唔鎖通告。

### Non-goals

- 完整紅地毯／投票小遊戲／直播時間軸  
- 真實金像／台慶獎／十大金曲／廣告獎真名、真實評審、真實報紙排版／SFX  
- 長對白樹、romance 綁獎、敵線完整「頒獎禮後台」重做  
- 靠頒獎禮清全主線 C9–C17  
- **單一 TV-only MVP**（已否決）

### HOLD

| HOLD | 原因 |
|---|---|
| tip LIVE／抬 `SAVE` | Soft≠PASS |
| 真藝名／真獎項名／真台名 | worldview taboos |
| 89–92 深時代獎季改寫 | 年庫未開深 |
| 紅星長互動／齊鎮海上地圖 | 遠觀契約 |
| 出圖／LOOKS 新立繪 | 出圖 HOLD |
| 改 BehaviorGate parsers／C* weekMin | 另票 |
| 發明長篇傳媒／頒獎劇情弧 | 只准短卡＋短 beat |

---

## 2. 四軌虛構品牌（玩家面）

| id | 媒介 | 玩家面名稱 | locHint | 感覺 | 主軌偏重 | Soft 相位 |
|---|---|---|---|---|---|---|
| `award_harbour_ad` | **廣告** | **維港街招・年度廣告賞** | `ad_central` | 廣告／品牌年賞氣味（禁真廣告獎名） | 聲量＋關注度 wrap | **MVP 輕** |
| `award_golddisc_music` | **唱片／音樂** | **星河金碟夜** | `rec_star` | 唱片公司／電台氣味嘅年度金碟頒獎（禁真音樂獎名） | 聲量＋銷量 wrap | **MVP 輕** |
| `award_harbour_film` | **電影** | **維港影藝獎** | `film_harbour` | 虛構影圈年獎（禁「金像」等） | 信用＋票房 wrap | **MVP 輕** |
| `award_singho_tv` | **電視**（劇／綜／台慶類） | **星河台慶・年度頒獎夜** | `tvb_longmen` | 電視台台慶夜內頒獎環節 | 雙軌；偏收視 wrap | **MVP 輕** |

**已降級／可選 P2：** 舊稿 `award_street_poll`「街坊人氣票」——跨媒介人氣可做各軌內 `cat_*_popular` 欄，唔再獨立第五典禮（避免一年五彈）。若日後要商場票選 flavor，另開 P2。

內容 bot 可改 `displayName`，**唔改 id**。DEV 靈感只可 `devOnly`。

---

## 3. Cadence（季節錯開）

遊戲開局 `START = 1988-03-07`；季節用既有 `calendarSeason()`（Soft 可 `softCalendarSeason`）。

| 典禮 | 媒介 | 季節窗 | Soft 建議觸發 | 每年 |
|---|---|---|---|---|
| 維港街招・年度廣告賞 | 廣告 | **春**（3–5） | `weekNumNow() ≥ 6` 且該年 `廣告` wrap ≥1；若未達門 → **gallery 邀請仍可出**（見 §4） | 1／曆年 |
| 星河金碟夜 | 唱片 | **夏**（6–8） | `week ≥ 16`；該年 `唱片通告` wrap 加權 | 1／曆年 |
| 維港影藝獎 | 電影 | **秋**（9–11） | `week ≥ 28`；該年 `電影` wrap 加權 | 1／曆年 |
| 星河台慶・年度頒獎夜 | 電視 | **冬**（12–2） | `week ≥ 40`；該年 `電視劇`／`綜藝` wrap 加權 | 1／曆年 |

**第一年 Soft 節奏（開局 3 月）：**

1. **1988 春** → 廣告賞（最早體驗；早期廣告通告多，易達 gallery）  
2. **1988 夏** → 金碟夜  
3. **1988 秋** → 影藝獎  
4. **1988 冬** → 台慶頒獎夜（可同 C10 冬窗並行）

**同主線關係：**

- C5「台慶籌備」＝夏／秋氣氛＋小訪，**≠** 冬頒獎夜。  
- C10＠W40＝後台搶位事態；**只影響電視軌**防疊：若 C10 進行中，`award_singho_tv` invite 可延 1 個工作日或標「台慶週・改日再睇信」。其他三軌**唔**跟 C10 鎖。  
- `hook_autumn_award` 人情債鉤保留；唔吞、唔合併 id。

**Skip：** 每軌每年可推辞一次；`skipped:true` 唔重發；下年再計。唔鎖地圖／通告。

**防疊：** 同時最多 **1** 個獎禮 pending；下一季節窗到而仍有 pending → 排隊（FIFO），唔一次彈四張。

---

## 4. Entry conditions（邊個請到你）

### 4.1 資格階（共用；門檻可按軌微調）

| tier | 玩家面 | Soft 條件（建議；實裝可微調） | 結果池 |
|---|---|---|---|
| `gallery` | 旁聽席 | **該媒介** year wrap ≥1 **或**（總 `gigCount ≥ 2` 且雙軌達低門） | 觀禮短卡；小幅聲量 |
| `nominee` | 入圍／提名 | 該媒介 year wrap ≥2（廣告／唱片可 ≥1 放寬）且（聲量≥10 **或** 信用≥12） | 1 個提名欄 |
| `contender` | 熱門 | nominee ＋對應軌較高／相關 tag | 較高勝率（P1） |
| `presenter` | 頒獎／助演上鏡 | P2；信用高＋ tag | 短上鏡卡 |

**MVP 實裝 `gallery` + `nominee`。** 第一年 Soft **以觀禮／入圍為主**，得獎係驚喜。

**無該媒介 wrap：** 仍可收 **gallery** 請柬（「行內旁聽」），唔好令未拍過電影嘅玩家完全無感——但 **nominee 必須有該媒介 wrap**。

### 4.2 Soft 閘注意

- 通告 Soft 閘獨立；獎禮唔替代 `canAudition`。  
- BehaviorGate／C* **唔因獎禮改數字**。  
- 逾期人情債：可開已 pending 獎禮 sheet；「去現場」可提示先清債。

### 4.3 同殺青獎勵對齊（核心）

殺青 `SCHEMA_POST_SHOOT_REWARD_v1.json` → `metrics.kindByGigType`：

| gig `type` | 殺青 metric | **對應獎軌** | 計提名／yearRelevantWraps |
|---|---|---|---|
| `電影` | `boxOffice`（票房） | `award_harbour_film` | 電影 wrap |
| `電視劇` | `ratings`（收視） | `award_singho_tv` | 劇／綜 wrap |
| `綜藝` | `ratings`（收視） | `award_singho_tv` | 同上 |
| `唱片通告` | `sales`（銷量） | `award_golddisc_music` | 唱片 wrap |
| `廣告` | `attention`（關注度） | `award_harbour_ad` | 廣告 wrap |
| `_fallback` | `attention` | 唔計入任何軌提名（可只加總 gig 觀禮） | — |

引擎聚合：`S.postShootRewards` log（按 type／metricKind）＋ `gigCount`／雙軌／`castingTags`。  
**MVP 唔要玩家手動報名。** P1 可加何生「代報」一鍵。

結果傳媒卡可呼應殺青頻道氣味（press／news／streetFans），但用 **awards 專屬 templates**，pending queue **分開**（唔同一次殺青包攪埋）。得獎卡 `metrics` 行可顯示：

- 電影軌 → 「票房話題」一句  
- 電視軌 → 「收視餘溫」一句  
- 唱片軌 → 「銷量／碟市」一句  
- 廣告軌 → 「街外關注度」一句  

（數值可用 stub `valueLine` 風格，唔做真榜單。）

---

## 5. Flow UX（每軌同一骨架）

```
[該軌季節窗到達]
    ↓
① 邀請卡（信）—— modal 或手帳行程置頂
    ↓ 出席 / 推辞 / 稍後
②（可選 P1）紅地毯 1～2 句 —— MVP 跳過
    ↓
③ 提名一行（可縮入結果頁頂）—— 該軌 1～2 個 category
    ↓
④ 結果 sheet —— 得獎／入圍／觀禮；雙軌 delta
    ↓
⑤ 傳媒短卡 —— press／news（＋可選 metrics 餘韻）
    ↓
⑥ 手帳留底 —— S.awardsLog；記數小計（P1）
```

### 5.1 MVP 畫面（四軌共用殼）

1. **邀請 sheet**（標題＋dek＋出席／推辞／稍後）  
2. **結果＋傳媒合併 sheet**（標題跟典禮名，例如「金碟夜・結果」）  
3. **跳過**紅地毯同獨立提名頁  

一殼四軌：只換 `ceremonyId`／文案／category 池／matchTypes。

### 5.2 各軌虛構獎項欄（MVP 每軌 2 欄；每次抽 1～2）

#### A. 唱片／音樂 · `award_golddisc_music`

| categoryId | 玩家面 | 傾向 |
|---|---|---|
| `cat_newcomer_disc` | 年度新人碟緣（臨記組） | 信用＋唱片 wrap |
| `cat_popular_voice` | 最受歡迎出鏡嗓／面孔 | 聲量＋銷量餘韻 |

#### B. 電視 · `award_singho_tv`

| categoryId | 玩家面 | 傾向 |
|---|---|---|
| `cat_newcomer_tv` | 最佳電視新人（臨記組） | 信用＋劇／綜 wrap |
| `cat_popular_face` | 最受歡迎螢幕面孔 | 聲量＋收視餘韻 |
| `cat_variety_spark` | 綜藝閃光綠葉 | 綜藝 wrap＋聲量（P1 抽池） |
| `cat_ensemble` | 最佳班底／群戲 | 信用＋tag（P1） |

MVP 電視軌先用 **newcomer + popular**；variety／ensemble 留 schema 抽池。

#### C. 電影 · `award_harbour_film`

| categoryId | 玩家面 | 傾向 |
|---|---|---|
| `cat_newcomer_film` | 影壇新面孔（臨記組） | 信用＋電影 wrap |
| `cat_box_talk` | 年度票房話題綠葉 | 聲量＋票房 metric 餘韻 |

#### D. 廣告 · `award_harbour_ad`

| categoryId | 玩家面 | 傾向 |
|---|---|---|
| `cat_newcomer_ad` | 年度廣告新面孔 | 信用＋廣告 wrap |
| `cat_street_recall` | 街外最記得住嘅一鏡 | 聲量＋關注度餘韻 |

背景 NPC／紅星遠觀名可短寫「某某獲獎」，無長互動。

### 5.3 結果公式（Soft 可解釋）

```
score = w1*normalize(primaryTrack) + w2*yearMediumWrapWeight + w3*tagBonus + rng(0..ε)
```

- `gallery`：觀禮卡；`stageVolume +0～1`  
- `nominee`：score ≥ 門 → 得獎；否則入圍（微加，細過得獎）  
- **禁止**保證年年贏；第一年以入圍／觀禮為主  

**媒介權重：** 無該媒介 wrap → 唔入 nominee；有 wrap 但雙軌低 → gallery。

---

## 6. Data model

### 6.1 Save 欄（唔改 SAVE key）

```js
S.awardsLog = [  // max ~24（四年×四軌夠用）
  {
    id: "aw_1988_golddisc",          // `${year}_${ceremonyId短碼}`
    ceremonyId: "award_golddisc_music",
    medium: "music",                 // music|tv|film|ad
    year: 1988,
    season: "夏",
    week: 18,
    tier: "nominee",
    categories: [{ id:"cat_newcomer_disc", outcome:"nominated"|"won"|"lost"|"gallery" }],
    rewardsApplied: { stageVolume:1, industryCredit:2, money:0, tags:[] },
    metricEcho: "sales",             // 對齊殺青 metricKind；可選
    skipped: false,
    dayIndex: 120
  }
];
S.awardsFlags = {
  // `${year}:${ceremonyId}` → "invited"|"pending"|"done"|"skipped"
};
// FREEPLAY_FW._pendingAward（單一 pending；多軌排隊）
```

### 6.2 Schema／Stub

- `content/SCHEMA_AWARDS_CEREMONY_v1.json` — 引擎擁有（本輪已改四軌草稿）  
- `content/STUB_AWARDS_CEREMONY_v1.json` — 內容 bot 文案（本輪已改四軌草稿）  
- **仍 `implemented: false`**；唔當 LIVE

### 6.3 Stub 分界

| 欄 | 誰填 |
|---|---|
| `ceremonies[].id`／`season`／`cadence`／`medium`／`matchTypes` | **引擎** |
| `displayName`／`inviteTitle`／`inviteDek` | 內容 bot |
| `categories[].id`／weights／`matchTypes`／`metricEcho` | **引擎** |
| `categories[].label`／`winLine`／`loseLine`／`galleryLine` | 內容 bot |
| `tiers[].id`／thresholds | **引擎**（改要 re-board） |
| `tiers[].label` | 內容 bot |
| `pressTemplates`／`newsTemplates`（可按 medium 分） | 內容 bot |
| `redCarpet.*` | 內容 bot（P1） |
| `nextHint` | **必須 ""** |

空字／「待補」→ fallback；遊戲唔崩。

---

## 7. Integration points

| 現有件 | 點接 |
|---|---|
| `__reward`／殺青獎勵 | **sibling**：共用 press-like builder 氣味；**分 pending**；計分讀 `S.postShootRewards` 嘅 type／metricKind |
| Freeplay loader | meta 加 `awardsCeremony`；`__freeplay.check()` 報四軌 id |
| BehaviorGate | 只讀 season／week／flags |
| 雙軌 | 得獎／入圍經 `stageVolume`／`industryCredit` |
| 手帳 | 行程置頂該軌事件；記數「入圍×N／得獎×N」按媒介小計（P1） |
| 遠觀紅星 | 結果背景短名 |
| `hook_autumn_award` | 保留；唔合併 |
| Soft CTA／mask | sheet 關後還原地點 CTA（v20a4 教訓） |
| SAVE | `starVolunteer_map_v19w`；hydrate `awardsLog:[]`／`awardsFlags:{}` |

---

## 8. Soft vs 未來 LIVE

| | Soft（而家） | LIVE（日後 tip 另票） |
|---|---|---|
| 開關 | `softBehaviorGate=1` 先跑四軌排程 | 預設關或獨立 flag |
| 文案 | stub＋fallback | 過審長文／過場 |
| 門檻 | 偏鬆；保證每年每軌至少有「觀禮」機會（達低門） | 可收緊 |
| C10 | **只**電視軌防疊 | 可硬節拍 |
| 音效／紅地毯 | 無／極簡 | 可加 |
| 年庫 89–92 | HOLD | 另開獎季表 |

**唔 tip LIVE** 直至用戶明示。

---

## 9. Phased build（仍要四媒介，唔係 TV-only）

### Phase MVP（建議 v20a7 實裝 · **四軌輕量同年交貨**）

- [x] Schema＋Stub 四軌殼＋`S.awardsLog` hydrate  
- [x] **四個** `ceremonyId` 全開排程（春廣／夏碟／秋影／冬視）  
- [x] 共用邀請＋結果／傳媒合併 sheet（無紅地毯）  
- [x] 每軌 MVP **2** 個 category（見 §5.2）；電視 extra 欄可進抽池但唔強制  
- [x] tier：`gallery`｜`nominee`；按媒介 wrap 計  
- [x] 讀殺青 log 做 yearRelevantWraps；結果可帶 `metricEcho`  
- [x] 雙軌小 delta＋`__awards.check()`／`__awards.preview({ceremonyId})`  
- [x] pending 單槽＋季節排隊；Soft CTA 還原  
- [x] CONTENT_CONTRACT §3.6＋NOTES verify  
- [x] 用戶確認：獎項名之後再落實（placeholder OK）

**MVP「輕」嘅意思：** UX 殼單一、無紅地毯、每軌少欄、第一年難得出獎——**唔係**只做一軌。

### Phase P1

- 每軌加第 3～4 category；獨立提名頁；紅地毯 1 選項  
- 手帳記數按媒介小計；何生「代報」  
- 電視軌同 C10 防疊打磨  
- 可選跨媒介「街坊人氣票」輕量結果卡（唔另開長流程）

### Phase P2

- `presenter`；敵線／采兒短 hook  
- 動畫／音效；89–92 年表  

---

## 10. Acceptance／console（實裝後）

```js
await __freeplay.load();
__freeplay.check();     // ok:true；awardsCeremony:true；四軌 id 齊
__awards.check();       // ok:true；stub＋queue＋SAVE hydrate
__awards.preview({ ceremonyId:"award_harbour_ad", year:1988, forceTier:"gallery" });
__awards.preview({ ceremonyId:"award_golddisc_music", year:1988, forceTier:"nominee" });
__awards.preview({ ceremonyId:"award_harbour_film", year:1988, forceTier:"nominee" });
__awards.preview({ ceremonyId:"award_singho_tv", year:1988, forceTier:"nominee" });
// 各回傳 pack：invite／categories／result／pressCards／deltas／metricEcho

__awards.debugForceSeasonWindow("award_harbour_ad");
// 出席 → 結果 sheet → 關後地圖 CTA 仍可開
// 同年同 ceremonyId 唔重複；四季可先後各一次
```

**玩測清單**

1. 新局春開 → 未達窗：**無**逼弹。  
2. DEV 跳春＋有／無廣告 wrap → gallery 或 nominee 行為正確。  
3. 夏／秋／冬三軌同樣驗一次（至少 gallery）。  
4. 殺青電影後秋窗 → 影藝獎提名權重有感覺；唱片→金碟；劇／綜→台慶；廣告→街招。  
5. 四軌 pending 唔疊爆 mask；推辞後同年唔再出。  
6. 玩家面無真獎名、無 nextHint、無 stub tip。

---

## 11. 內容 bot 預備（批核後）

填 `STUB_AWARDS_CEREMONY_v1.json`：

- 四軌 `displayName`／`inviteTitle`／`inviteDek`  
- 各 category `label`／`winLine`／`loseLine`／`galleryLine`  
- 按 `medium` 分嘅 press／news 短模板（禁真藝名）  

**唔改** id、cadence、matchTypes、threshold、SAVE、BehaviorGate。  
文風：典禮夜儀式感；可同殺青 punch 呼應，但唔共用「殺青」語氣。

---

## 12. 拍板問題（已吸收用戶意見）

| # | 問題 | 現況假設（可改） |
|---|---|---|
| 1 | 四媒介各自獎項 | **已定：要**（本修訂） |
| 2 | MVP 是否四軌同年輕量 | **建議：要**（唔再 TV-only） |
| 3 | 季節：春廣／夏碟／秋影／冬視 | 建議；可調 |
| 4 | 第一年難度 | **觀禮／入圍為主** |
| 5 | 同 C10 | **只電視軌**並行＋防疊 |
| 6 | 紅地毯 | MVP 全跳過 |
| 7 | 街坊人氣票獨立典禮 | **降 P2**（併入各軌人氣欄） |

若季節次序或虛構名要改，批核時講聲即可——**唔改四軌必須齊**呢條。

---

## 13. 一句總結

> Soft 定期頒獎禮＝**四條獨立虛構獎軌**（星河金碟夜／星河台慶頒獎夜／維港影藝獎／維港街招廣告賞），按**春廣·夏碟·秋影·冬視**錯開；資格同結果跟殺青四類 metrics（銷量／收視／票房／關注度）同雙軌；MVP 用同一短卡殼輕量交齊四媒介，唔再縮成單一電視台慶；真名／LIVE／長弧／抬 SAVE 一律 HOLD。

**已拍板並實裝 v20a7（placeholder 獎名；內容 bot 之後改 displayName）。**
