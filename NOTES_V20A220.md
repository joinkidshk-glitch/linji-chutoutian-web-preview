# NOTES_V20A220 — 書面語改寫 P1：v217 越界還原（PHASE1＋EVENTS）

- 日期：2026-11-15
- 基線：main `5580f8d`（v218）
- 範圍：書面語改寫票 P1（遊戲邊）。AUDIT2 §2.4＋RECOUNT-REPORT：P1 係 v217 diff 還原工 29 處（PHASE1 28＋EVENTS 1），唔用 recount 數（live 17）做分母。

## §1 改動內容

### 1.1 PHASE1 章節旁白 17 句（純轉寫還原，inline＋JSON 兩邊一齊改）
Ch1–Ch4 title／open／close 全部還原 v217 前書面語版（例：「記數簿同名片冊」→「記數簿與名片冊」；「佢學識睇通告欄，亦學識等。」→「他學會看通告欄，也學會等。」）。locale `zh-Hant-HK` 保留（v217 §4 第 5 項已定，唔還原）。

### 1.2 PHASE1 系統 beats 12 句（speaker=系統 lines）
- B02：36 句本身 0 標記唔郁；37／38 句內容重寫過，要新書面語版（「先看鎖區和日期，再記下地點。」／「約試鏡日要準時；即場看排隊。」——與 JSON 舊文一致）。
- B04：48／49 句本身 0 標記唔郁；50 句還原（「要不要報名，由你決定。」）。
- B07：3 句純轉寫還原（Vera 嗰句保留原名，刪除收尾歸 v159，唔喺呢票改）。
- B09：79／80 純還原；78 句舊文 v217 前已係廣東話，用新書面語版（「周采兒在場邊多看了兩眼，好感夠了。」）。

### 1.3 EVENTS 4 句（inline＋JSON 兩邊一齊改）
- WEEK_OK（v217 句）：留臨記、去咗——「數一數，臨記也做了幾場。」
- WEEK_IDLE ×2、WEEK_TRAIN_HEAVY ×1：預存旁白（JSON live 嗰 5 個標記入面除 WEEK_OK 之外嗰 4 個），順手重寫書面語。

### 1.4 inline EVENTS 分叉句 10 句（inline-only，JSON 嗰邊已有書面語版／無對應 key）
AUD_PASS ×3、AUD_STRESS70 ×2、TRAIN_RESULT_stamina ×2、UNLOCK_CHARM／IQ／STAMINA 各 1，inline 就地重寫（唔郁 JSON；兩邊分叉本身係 pre-existing，P0-2 已記錄，呢票只清語體，唔做全量 resync）。

### 1.5 唔郁嘅嘢
- PHASE1 對白（B01／B03／B05／B06／B08／B10 lines，speaker 何生／阿偉）全部保留廣東話——v217 粵語化正確。
- B02-36／B04-48／49：v217 新寫內容本身已係書面語（0 標記），唔郁。
- 其餘 EVENTS inline／JSON 分叉（13 個 key 內容唔同）唔喺呢票處理；live 係 JSON。

## §2 驗收

- recount.py（遊戲邊）：P1 live 17 → **0**（index PHASE1 12→0、EVENTS inline 21→0；content phase1 12→0、events 5→0）。P2／P3 池數字零變動（只係 P1 池變咗）。
- PHASE1 inline vs JSON：87 句字串完全一致（multiset 0 差異），兩邊同步。
- JSON 合法：兩 pack `json.load` 通過。
- `node --check`：index.html 兩塊 inline script 全部通過。
- 全套 suite A／B：**A 309／13 vs B 309／13，FAIL 清單一模一樣（13 項穩定 pre-existing FAIL），零回歸**。A＝pristine main `5580f8d`，B＝工作副本 `linji-work220`。
- 對白核實：git diff 只改旁白／系統句，對白行零郁動（B01／B03／B05／B06／B08／B10 全數保留）。

## §3 落地

- 分支 `v20a220` → squash merge → main HEAD `09e7774`；線上核實 5,569,800 bytes、sha `1d3bfeae709c1d5d9e4d9475a9f1ad34417b85d1`，同 main HEAD index.html 完全一致。
- 工作副本 `linji-work220` 落地後刪除；pristine 對照 `linji-pristine220` 已刪除；分支 `v20a220` 已刪。

## §4 殘留／跟進

- EVENTS inline／JSON 13 個 key 內容分叉（P0-2 已記錄）：呢票只清咗有標記嘅句，全量 resync 未做。
- P2（主線旁白 2,411）→ v221；P3（隨機事件等 2,535＋G1／G9／G10）→ v222。
