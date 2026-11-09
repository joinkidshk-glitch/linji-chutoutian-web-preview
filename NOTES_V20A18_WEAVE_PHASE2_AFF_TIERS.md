# NOTES v20a18 — Weave Phase 2-3：好感階梯（何生＋采兒）

串聯規劃 §4「好感度做情報階梯」落地第二步：好感唔再只係解鎖通用對白池，指定 NPC 渠道按關係深淺畀唔同層次嘅情報。

## 研究結論（現有系統）

- 好感值：`S.npcs[id]`，0–100，`bumpNpc(id, d)` clamp 0–100；傾談每次 +3–7。
- 對白池：`NPC_LINES_CORE[id]` 有 greet／chat／advice／intel／pressure 五組；已有通用解鎖閘 `AFF_DIALOGUE_GATES`（寒暄 0／閒談 10／忠告 25／情報對白 40），`pickNpcLine()` 按已解鎖池加權抽線，未到閘嘅池唔會出。
- 傾談入口：`doTalk(npcId)`——有 tipGig 時用 intel 池出情報句＋具體通告提示；否則行 `pickNpcLine`。
- 何生 id = `agent`（事務所）；采兒 id = `reporter`（周采兒，遊戲內身份係娛樂記者）。
- 缺口：通用 intel 池 40 解鎖後就到頂，對白偏泛；無「越熟越多私料」嘅第二層。

## 今次改動（只綁何生＋采兒）

- 新增 `NPC_AFF_TIERS = { dailyAt: 25, insiderAt: 60 }` 同 `NPC_TIER_LINES`：
  - 中階「日常情報」（rel ≥ 25，同現有忠告閘對齊＝熟絡）：何生／采兒各 4 句——行內貼士、邊度有工開、點樣儲料，同現有系統（通告欄／手帳拼合／殺青留聯絡）咬合。
  - 高階「內幕情報」（rel ≥ 60＝自己人）：各 4 句——真情報提示，指去現有系統：陸柏言疑雲拼合→情報旗隱藏替工通告、麥震東通告卡情報行、人情到期要趁早還（何生）；陸柏言碎片拼合、私人儲料法、高俊傑競爭（采兒）。唔劇透主線爆點。
- `npcTierPool(npcId, aff)` 按階回傳已解鎖池；`pickNpcLine` 將階梯池入加權抽線（wantIntel 時權重更高）；未到階完全唔入池，低階對白保留。
- `npcIntelPool(npcId)`：傾談 tipGig 嘅情報池改為「原 intel 池＋已解鎖階梯池」，高好感傾談出嘅情報句會更深。
- `npcNextTierHint(npcId, aff)`：傾談結果頁好感行下面加一行「關係階梯：再加 X 點好感 → 解鎖『日常情報／內幕情報』（門檻 …）」，畀玩家知仲有下一層。
- 其他 NPC（曉晴／Vera／張子駿／高俊傑）行為完全不變，留待日後按同一模式擴充。

## 冇改

- SAVE key、softRev、`?v=`、`AFF_DIALOGUE_GATES` 本身、好感數值公式。

## 測試

- 新增 `tests/test_weave23_logic.js`（28 項：門檻／覆蓋範圍／階梯過濾／情報池擴充／pickNpcLine 統計抽樣／內幕指向現有系統／禁真藝名）全過。
- 新增 `tests/test_weave23_static.py`（13 項）全過。
- 舊測試全套回歸（P0、P0-3、Weave 1-1／1-2／1-3、2-1、2-2）無回歸；全檔 script `node --check` 通過。
