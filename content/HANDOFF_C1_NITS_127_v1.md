# HANDOFF — C1 nits → JSON **1.2.7**（v18e 公開站 PASS with nits 修復）

**日期：** 2026-11-03（Asia/Hong_Kong）  
**契約：** 唔改 Soft／出圖／鄧／meet／送禮 unlock；手頭緊 beat **skip**（對白已夠）

## 改咗咩

1. **setting 露玩家**  
   C1.`setting`：`星河電視台附近茶餐廳；片場後巷感（locId 暫掛 tvb_longmen）` → **`星河電視台附近茶餐廳；片場後巷感`**  
   `locId` 欄位仍係 `tvb_longmen`（只删 setting 括號 debug）  
   已同步：
   - `story_detail_c1_to_c17.json`（web／sv-phone-preview／store-cbdfa*）
   - `story_detail_phase1_c1c5.json`、`phase1_to_c10.json`、`phase1.json`（web＋store；sv-phone-preview 無呢三份 phase 鏡像）
   - `SANDBOX_C1_FUSION_DRAFT_v1.json`（web／sv-phone-preview／store）

2. **舊 title「先練／先賺」玩家可見殘留**  
   `/workspace/star-volunteer-web/index.html` 同 `/workspace/sv-phone-preview/index.html`：
   - `STORY_TITLES`／fallback：`C1: "先學做動作戲／先賺"`
   - playerHint／nextHint：「先學做動作戲定先賺」／「先學做動作戲／先賺」
   - B01／週結教學金句：同上  
   註解可留「先練／先賺」；`rg` 玩家可見已清乾淨。

3. **Version**  
   - `story_detail_c1_to_c17.json`：**1.2.6 → 1.2.7**  
   - edits：`C1_NITS_127_v1` — `nits: strip locId from setting + title fallback 學做動作戲`  
   - phase 鏡像 edits 已註記同 note  
   - **SHA16（全檔 SHA256 前綴）：`ed1f006c2267cfe8`**

## 叫 iOS

1. 推公開預覽 **`?v=18f`**（SAVE／cache-bust 跟你們慣例；本地 SAVE 暫仍 `starVolunteer_map_v18e`，註解已標 pending 18f）  
2. 確認遠端 JSON **1.2.7**／SHA16 **`ed1f006c2267cfe8`**／C1.setting **無**「暫掛／locId」  
3. Soft≠PASS／出圖 HOLD／鄧 HOLD／meet·送禮 **唔動**

## Tester 覆測清單

- [ ] 公開／本機：C1 每拍 setting 只見「星河電視台附近茶餐廳；片場後巷感」（無 locId／暫掛）
- [ ] 手帳／B01／事態標題／fallback：**「先學做動作戲／先賺」**，唔見「先練／先賺」
- [ ] version 欄／curl JSON = **1.2.7**，SHA16 = **`ed1f006c2267cfe8`**
- [ ] 11 beats／C1_a／C1_b／開局鎖／契約回歸仍 PASS
- [ ] Soft≠PASS／出圖 HOLD／鄧 HOLD

## 路徑摘要

| 檔 | version | SHA16 |
|---|---|---|
| `/workspace/star-volunteer-web/content/story_detail_c1_to_c17.json` | **1.2.7** | `ed1f006c2267cfe8` |
| `/workspace/sv-phone-preview/content/story_detail_c1_to_c17.json` | **1.2.7** | 同上 |
| `/cursor/stores/store-cbdfa415-74f6-4e12-8fbd-513ef31077be/story_detail_c1_to_c17.json` | **1.2.7** | 同上 |
| `…/index.html`（web＋sv-phone-preview） | title fallback 已改 | — |
| 本手冊 | — | `content/HANDOFF_C1_NITS_127_v1.md` |
