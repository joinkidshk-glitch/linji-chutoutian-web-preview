# SANDBOX_C1_FUSION_NOTE_v1｜C1 小說→遊戲試作對照

> **時間：** 2026-11-03（Asia/Hong_Kong）  
> **狀態：** **sandbox only** — `liveTouch:false`；**唔上 LIVE**；唔覆寫 `story_detail_*.json`／index。  
> **觸發：** 用戶 OK「試一試」`PLAN_NOVEL_GAME_FUSION_v1`；寫好即交 **@星途志願tester及manager** 手測。  
> **HOLD：** Soft≠PASS；出圖 HOLD；鄧 HOLD。  
> **草稿：** `/workspace/star-volunteer-web/content/SANDBOX_C1_FUSION_DRAFT_v1.json`

---

## 1. LIVE vs sandbox 對照

| 項 | LIVE C1 | sandbox v1 | 改動意圖 |
|---|---|---|---|
| title | 先練／先賺 | **先學做動作戲／先賺** | 對齊小說章題＋硬規則用詞 |
| setting | 廠景通告板旁，何生事務所 | **茶餐廳**（loc 暫掛 `tvb_longmen`） | 補小說開場窮／油煙場面；新針另票 |
| synopsis | 兩路＋練功班底腔 | 手頭緊＋何生平鋪＋電話留位；**學做動作戲** | 抽取母本情緒，少造新劇情 |
| beats 數 | **7** | **11** | 場面建立 2＋人情 1＋抉擇鏈；內心壓短（可略多於 LIVE） |
| 開場 | 何生直接兩條路 | **系統**短場面（收工／茶餐廳／月中錢） | 融合原則：場面建立 ≤1–2 beat |
| 人情 | 弱 | 何生「帶你因為準時／肯重拍」 | 早段可感知經理人 |
| 張子駿 | 電話三句 | 電話＋「唔會打第二次」語感（壓短） | 機會感，唔開導師大廳 |
| 兩邊都做 | 無 | 何生一句否決 | 小說有；抉擇前封死雙開幻想 |
| choice id | C1_a／C1_b | **保留** | 禁改 id |
| labels | 先練班底…／先賺錢… | **先跟班底學做動作戲…**／先賺錢… | 對齊小說選項 A 用詞 |
| effects flags／stats | route_tv craft+1；route_film wealth+1 | **同向同名** | 唔亂改 flag |
| effects.notes | 一句傾向說明 | 短後果＋小說動作（拿紙／填表） | 選後有人話，唔只數字 |
| resultBeats | 無 | 各選 **1–2 條 optional** | 引擎未讀則標 optional，靠 notes |
| playerHint | 廠景幕等你 | 茶餐廳兩路＋**無名臨記**自況 | 開局鎖定驗收 |
| lockedHint | 廠景通告欄 | 只推主線；**感情／大咖／送禮鎖** | §4 開局鎖呼應 |
| nextHint | C2 週4＋隔日 | 同上＋**月底何生再搵／通告板有人記得名** | 對齊小說共通段 |
| openConditions／pacing／locId／playerOffer | []／W1／tvb／true | **相容不變語義** | 可對照手感，唔合 LIVE |

**來源：** 手拆 `NOVEL_SCRIPT_MAIN_VOL1_C1C5_v1.md` 第1章；對照 LIVE 只讀；**未**呼叫 DeepSeek 新寫長對白。

---

## 2. 開局鎖定呼應（C1 前後世界仍窄）

- 出場只有：**阿偉、何生、張子駿（電話）**。  
- **唔引** Vera／采兒／鄧／高俊傑／林曉晴。  
- `playerOffer:true` 只推呢條主線；平行 meet 仍當 false（本 sandbox 唔改 meet JSON）。  
- lockedHint 明文：感情線／大咖牆／送禮先鎖。  
- 張子駿＝電話留位，唔係開局導師選單。

---

## 3. 播完回地圖餘波（hint 文案）

1. **結算：** `effects.notes`（必）＋ `resultBeats`（optional）。  
2. **nextHint：** 指向 C2（W4+、隔日）；提醒照常跑通告／訓練。  
3. **共通段落地：** 月底何生再搵；通告板開始有人記得名；兩條線並存、只先站穩一邊。  
4. **aftermathHint／journalCandidate：** 文案池候補（見 draft `meta.engineNotes`）；引擎無欄位可當 tester 讀感參考。

---

## 4. 風險／待引擎

| 項 | 說明 |
|---|---|
| `resultBeats` | **optional**；現 LIVE schema 無此欄。未讀＝忽略，唔壞播。 |
| `aftermathHint`／`journalCandidate` | 非正式欄；合 LIVE 前另案決定是否接入。 |
| beats 11 vs 7 | 手感可能偏長；tester 可標「可再壓」beat 編號。 |
| title／setting 用字 | sandbox 可改；合 LIVE 要用戶再批。 |
| locId 仍 soft 星河 | 茶餐廳場面靠文案；新 `cafe_*` 針【待用戶 OK】。 |

---

## 5. 建議下一步

1. **tester／manager 手測**（見 §6）— 讀 sandbox，唔上 LIVE。  
2. 用戶／tester OK 手感後，**另刀**先合 LIVE（仍要用戶再批；Soft≠PASS）。  
3. 同法再做 C2–C5 sandbox；VOL2–4 小說繼續用戶審。  
4. 送禮／meet／鄧／出圖：**唔喺本刀偷改**。

---

## 6. Tester 手測清單（交 @星途志願tester及manager）

**檔案路徑（只讀 sandbox，唔改 LIVE）**

| 檔 | 路徑 |
|---|---|
| 草稿 JSON | `/workspace/star-volunteer-web/content/SANDBOX_C1_FUSION_DRAFT_v1.json` |
| 本 NOTE | `/workspace/star-volunteer-web/content/SANDBOX_C1_FUSION_NOTE_v1.md` |
| 融合計劃 | `/workspace/star-volunteer-web/content/PLAN_NOVEL_GAME_FUSION_v1.md` |
| 鏡像（store） | `/cursor/stores/store-cbdfa415-74f6-4e12-8fbd-513ef31077be/SANDBOX_C1_FUSION_*.md|json` |
| 可選 preview 旁放 | `/workspace/sv-phone-preview/content/SANDBOX_C1_FUSION_DRAFT_v1.json`（**唔**覆寫 `story_detail_*.json`） |

**硬閘（測前確認）**

- [ ] **唔上 LIVE**：唔 merge、唔改 `story_detail_c1_to_c17.json`／index／既有 LIVE 預覽內容  
- [ ] **Soft≠PASS**；出圖 HOLD；鄧 HOLD  
- [ ] 對照 `PLAN_NOVEL_GAME_FUSION_v1` §3 融合原則＋§4 開局鎖定  

**讀感／內容（建議順序）**

1. [ ] 打開 draft → `meta.sandbox=true`、`liveTouch=false`  
2. [ ] 讀 11 條 beats：有無茶餐廳／手頭緊場面？何生人情（帶路原因）有無感覺？  
3. [ ] 張子駿是否只係**電話留位**（唔似開局導師牆）？  
4. [ ] 對白有無「學做動作戲」（唔應出現舊縮寫腔／自造黑話）？  
5. [ ] 選 C1_a／C1_b：id 不變；notes 是否一句人話後果？  
6. [ ] `resultBeats`：若預覽引擎唔顯示，是否仍可單靠 notes 明白後果？（標 optional OK）  
7. [ ] `playerHint`／`lockedHint`／`nextHint`：播完知唔知「返地圖跑通告／等週／月底何生」？  
8. [ ] 開局鎖：全文有無誤引 Vera／采兒／鄧／高俊傑／曉晴？  
9. [ ] 節奏：11 beats 會唔會太長？若要壓，標可刪 beat 編號  
10. [ ] **結論一句：** 可進入「另刀合 LIVE（仍要用戶批）」／要改 sandbox／暫擱  

**回報格式（請短答）**

- 手感：場面／人情／抉擇／餘波（各一句）  
- 要改：beat# 或 hint 原文建議  
- 閘：確認未碰 LIVE；Soft 仍非 PASS  

---

## 7. 路徑一覽

| 檔 | 位置 |
|---|---|
| Draft | `star-volunteer-web/content/SANDBOX_C1_FUSION_DRAFT_v1.json` |
| Note | `star-volunteer-web/content/SANDBOX_C1_FUSION_NOTE_v1.md` |
| Plan | `star-volunteer-web/content/PLAN_NOVEL_GAME_FUSION_v1.md` |

*仍未上 LIVE。*
