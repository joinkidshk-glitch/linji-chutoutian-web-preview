# HANDOFF_C1_FUSION_LIVE_v1｜C1 fusion 已合 LIVE

> **時間：** 2026-11-03（Asia/Hong_Kong）  
> **來源批核：** 用戶 widget t152s782 — **合 LIVE，保留 11 beats**  
> **閘：** Soft≠PASS；**唔 publish Soft**；出圖 HOLD；鄧 HOLD；meet／送禮 unlock **未改**

---

## 改咗咩

| 項 | 內容 |
|---|---|
| LIVE C1 | `story_detail_c1_to_c17.json` **v1.2.5 → 1.2.6**：beats **7 → 11**（sandbox 全文） |
| 文案增量 | title／setting／synopsis／cast 口吻；playerHint／lockedHint／nextHint；choice **labels／notes**；可選 `resultBeats`＋`aftermathHint`／`journalCandidate` |
| 硬契約（不變） | choice id `C1_a`／`C1_b`；flags `route_tv`／`route_film`；stats craft+1／wealth+1；`openConditions: []`；pacing weekMin1／minDaysAfterPrev0；`locId: tvb_longmen`；`playerOffer: true`；`artId: story_c1`；conflict T1 |
| 鏡像 | `story_detail_phase1_c1c5.json` **3 → 3.1**；`phase1_to_c10` **1 → 1.1**；`phase1.json` **3 → 3.1**（薄檔：title／setting／synopsis／beats／choices／flags／art／conflict） |
| 同步 | `sv-phone-preview/content/story_detail_c1_to_c17.json` ＋ store-cbdfa* 同 SHA（見下） |
| 未改 | Soft 發佈、出圖、鄧節、romance／meet／送禮 unlock、C2+ |

**edits 註記：** `C1_FUSION_LIVE_v1` @ 2026-11-03 — sandbox merge C1 fusion；用戶批合 LIVE＋保留 11 beats。

**沙盒原文：** `SANDBOX_C1_FUSION_DRAFT_v1.json`（仍標 sandbox；LIVE 已吃入 node）

---

## Diff 摘要（C1）

- **場面：** 廠景事務所短對白 → 茶餐廳＋手頭緊＋何生人情＋伙計電話＋張子駿「不會打第二次」
- **用詞：** 「練功」腔 → 「學做動作戲／磨戲」
- **開局鎖文案：** lockedHint 寫明感情線／大咖／送禮先鎖；playerHint 無名臨記感
- **選項 notes：** 傾向說明 → 拿紙／填表短後果（id／flags／stats 不變）
- **beats：** 7 → **11**（用戶明示保留，唔壓）

---

## 路徑／版本／hash

| 檔 | version | SHA256 前綴 |
|---|---|---|
| `…/star-volunteer-web/content/story_detail_c1_to_c17.json` | **1.2.6** | `ec26240c44c21a04` |
| `…/sv-phone-preview/content/story_detail_c1_to_c17.json` | **1.2.6** | 同上（三地一致） |
| `store-cbdfa*/story_detail_c1_to_c17.json` | **1.2.6** | 同上 |
| `story_detail_phase1_c1c5.json`（web＝store） | **3.1** | `aeab619ace63cb1a` |
| `story_detail_phase1_to_c10.json` | **1.1** | `77ea333467ceb6a7` |
| `story_detail_phase1.json` | **3.1** | `defa4f61240457e7` |

---

## SAVE／預覽提示

1. **舊 SAVE：** 若已播過舊 C1（7 beats），重開／清進度再測 fusion 文案最穩；flags 機相容，但對白長度與 hints 已變。  
2. **預覽：** 用 `sv-phone-preview` 載入 content 後播 C1；確認 11 beats → C1_a／C1_b → notes（及若引擎有讀則 resultBeats）。  
3. **地圖：** 播完返地圖；`locId` 仍 `tvb_longmen`；開局唔應見 Vera／采兒／鄧牆。  
4. **引擎未知欄：** `resultBeats`／`aftermathHint`／`journalCandidate` 可忽略；靠 `effects.notes`＋hints 已夠。

---

## 請覆測（iOS ＋ tester）

**@明星志願 iOS developer**／**@星途志願tester及manager**

- [ ] C1 11 beats 可播完、無崩  
- [ ] C1_a → `route_tv`＋craft+1；C1_b → `route_film`＋wealth+1  
- [ ] 茶餐廳／手頭緊／何生人情／張子駿電話感在  
- [ ] 開局無 Vera／采兒／鄧；meet／送禮解鎖行為與合入前一致  
- [ ] Soft 未因本刀變 PASS／未誤 publish  
- [ ] 出圖／鄧仍 HOLD  

回報可寫短 QA 或直接答「LIVE C1 fusion PASS／nits」。

---

## 閘複述

**Soft≠PASS｜唔 publish Soft｜出圖 HOLD｜鄧 HOLD｜meet／送禮 unlock 本刀未動**
