# ART BRIEF｜C1 劇情界面最小可測集 v1

> 2026-11-03｜**用戶開閘測 chapter**（經 GD／tester）→ 本票 **允許出圖**（只限下列最小集）。全量 G0／Soft 仍 ≠PASS；鄧 HOLD。  
> Schema：`PLAN_STORY_UI_BEAT_SCHEMA_v1.md`（speakerId／emotion／expression／`bg_loc_*`）。  
> 章節：主線 **C1**《先學做動作戲／先賺》（LIVE 1.2.7；11 beats）。

---

## 1. 地點底圖（loc／bg）

| key | 用途 | 畫面（1988 港感；禁真實商標） |
|---|---|---|
| `bg_loc_tvb_longmen` | C1 預設環境（node.`locId`） | 星河電視台外圍／後巷：貨車、廠門、臨時演員蹲路邊；午後 |
| `bg_c1_tea_restaurant`（建議加；soft） | 系統 beat 茶餐廳＋對白場 | 舊式茶餐廳卡座：凍奶茶、油煙、不夠冷氣；可與後巷同色溫 |

引擎優先：beat.`bg` → beat.`locId` → node.`locId`＝`tvb_longmen` → `bg_loc_tvb_longmen`。

**最小：** 至少交 **`bg_loc_tvb_longmen` 1 張**；有餘力再交茶餐廳 1 張。

---

## 2. 半身 bust（多表情）

| speakerId | 顯示名 | artId | **本測要表情**（expression；對齊 schema v1） | 備註 |
|---|---|---|---|---|
| `awi` | 阿偉 | `char_hero` | `default` · `eyes_down` · `frown` · `raise_brow` | 主角；袖口可帶佈景灰感 |
| `ho_sang` | 何生 | `char_ho` | `default` · `raise_brow` · `frown` · `serious`→用 `frown` | 經理人；茶餐廳卡座對面 |
| `cheung_tsijun` | 張子駿 | `char_cheung` | `default` · `firm` 臉→`frown` 或 `raise_brow` | **電話戲**；可半身＋聽筒／側光；1–2 表情即可 |

> expression 枚舉 v1：`default|smile|frown|raise_brow|eyes_down|look_aside`（唔自造）。  
> emotion 係 JSON 語氣槽（iOS tint）；出圖以 **expression 檔**為主，檔名建議：`{artId}_bust_{expression}.png`。

**可攻略（可選、非本測阻塞）：** 若同一批想睇可攻略半身，另加 `lan_ruoxi`／`char_lan`：`default`＋`soft` 臉（`smile`／`worried`→`eyes_down`）各 1；loc soft `rec_star` 或雨景另議。**最小可測唔強制。**

---

## 3. C1 對白情緒對照（劇本建議；尚未寫入 LIVE JSON）

| beat | kind | speakerId | emotion | expression | bg 建議 |
|---|---|---|---|---|---|
| 0 | system | — | — | — | `bg_loc_tvb_longmen`（後巷） |
| 1 | system | — | — | — | `bg_c1_tea_restaurant` 或同 loc |
| 2 | dialogue | `ho_sang` | `firm` | `default` | 茶餐廳 |
| 3 | dialogue | `ho_sang` | `firm` | `raise_brow` | 茶餐廳 |
| 4 | dialogue | `awi` | `worried` | `eyes_down` | 茶餐廳 |
| 5 | dialogue | `ho_sang` | `firm` | `frown` | 茶餐廳 |
| 6 | system | — | — | — | 茶餐廳（電話打斷） |
| 7 | dialogue | `cheung_tsijun` | `firm` | `default` | 茶餐廳（電話；可暗一檔） |
| 8 | dialogue | `awi` | `tense` | `default` | 茶餐廳 |
| 9 | dialogue | `ho_sang` | `firm` | `frown` | 茶餐廳 |
| 10 | dialogue | `awi` | `firm` | `raise_brow` | 茶餐廳 |

系統線：**無 bust**；文案置中＋環境底。

---

## 4. 交付清單（GD 勾）

- [ ] `bg_loc_tvb_longmen`
- [ ] （可選）`bg_c1_tea_restaurant`
- [ ] `char_hero_bust_{default,eyes_down,frown,raise_brow}`
- [ ] `char_ho_bust_{default,raise_brow,frown}`
- [ ] `char_cheung_bust_{default,raise_brow}`（電話可）
- [ ] （可選）`char_lan` 1–2 表情

交檔後 @iOS 掛佔位路徑；@劇本 下一刀先 C1 sandbox 寫入 kind／speakerId／emotion／expression（LIVE 另批）。Soft≠PASS。
