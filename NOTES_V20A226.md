# NOTES_V20A226 — 書面語改寫：522 池外旁白＋ADJ_RUMOR＋DualMeet

- 基底：main `724ab04`（v225 對手線強化）；分支 `v20a226`；工作副本 `linji-work226`。
- 範圍：約 591 句玩家可見旁白從來冇入 recount 池——ENC83／84、LAN_PA、WF5 三組＋耦合 FIRST_ALT98 91，收三組做 recount 新池（P4）；另加 ADJ_RUMOR 89（結局頁耳語）＋DualMeet mock（曉晴／采兒預覽句）。
- 用戶拍板：ADJ_RUMOR 入 v226（2026-11-15 18:42）；DualMeet 入 v226（同日 18:43）；采兒 DualMeet 8 句一併落地（同日 18:59「落地，連采兒一齊」）。
- 設計／審核：`~/workspace/linji-language-audit-v2/`（recount.py v4.1、fixlist `work/fixlist_v226.json`）。

## §1 改動

- **227 fix / 14 leave**（241 項；fixlist：fix markers 833／fix core 713；leave markers 45／38）。
- 分池：ENC83_GU 24、WF5 tang 23、LAN_PA 20、FIRST_ALT98 20、ENC83_NGAI 17、ENC84_SO 17、ADJ_RUMOR 17、ENC84_CHUNG 16、ENC83_LOK 14、ENC84_PANG 14、ENC84_CHING 13、ENC83_CHAI 9、DUALMEET_CHOI 8、DUALMEET_HIU 7、8 個 FRAME 池各 1。
- Commits（工作分支）：
  - `e8f5b85` — 主批 522（195 fix / 13 leave），rebase 上 724ab04，零衝突。
  - `a5b16f9` — ADJ_RUMOR＋DualMeet（32 fix / 1 leave）。
  - `0dde817` — 落地前統一「亮着燈」→「亮著燈」（ALT98 `ching_tinlok` swap 兩處，跟 primary fix 用「著」；香港書面語用「著」，唔用簡化嘅「着」）。

## §2 recount 前後（統籌獨立重跑 `recount_v226b.py` 核實）

| 批 | 改前 | 改後 |
|---|---|---|
| P4（ENC83/84、LAN_PA、WF5、FIRST_ALT98） | 789 / 687 | **44 / 29** |
| ADJ（ENDING410_ADJ_RUMOR） | 89 / 64 | **1 / 0** |
| 舊池（P1＋P2＋P3＋P3*） | 100 / 42 | **100 / 42（不變）** |
| **GRAND** | 978 / 793 | **145 / 71** |

- ADJ 殘留 1／0 係有意保留嘅固定習語「講義氣」（E5，core-0「講」標記）。
- P4 殘留 44／29＝既有 ENC83/84＋LAN_PA＋ALT98（39／28：D4 leave 4／0、FIRST_ALT98 對白 leave 26／24、LAN_PA 新文本內 9／4）＋R_tang_* 5／1（範圍外，唔郁）。
- G1 echo 不變（1 項，5 標記）；G10 簡體 0。
- 備註：fixlist fix_core 合計（713）比 recount 淨 core 減幅（722）少 9，統籌推斷係 4 個 FIRST_ALT98 重複項經 primary 改寫但記做 leave——未逐行核實，量度後數字（上表）先係準。

## §3 驗證

- `node --check` PASS（兩個 inline script 塊），每個 commit 之後都驗過。
- Grep：主批 195／195 舊＝0／新＝1 in-span；ADJ＋DualMeet 32／32 舊＝0／新＝1 in-span。
- Suite A／B：**311／13 → 311／13，FAIL 清單一模一樣（13 項穩定 FAIL）——零回歸**，驗過兩次。
- Test pins（10 項逐項驗）：`test_cleanup100_enc.js` B06 pin、8 個 `lanPa` fixture label（`romance_wf2_v80.json`）、`test_weave410_logic.js` L409 `sum.includes('聽講')` → `sum.includes('聽說')`（57 passed／0 failed，原本 56／1）。
- `test_wf5_87_static.py` 喺乾淨樹上面一樣 FAIL（hardcoded 唔見咗嘅 `~/workspace/linji-work86` 路徑）——pre-existing。
- R_tang 係 LIVE：23 句 WF5 fix 全部在位（`applyVariantWf5Overrides87` 載入＋`DengLine.meetAvailable/pushAvailable`）；v159 鄧麗萍刪除未做。
- 重複項：7 個 FIRST_ALT98 leave——4 個經 primary `text_new` 解決，3 個唔郁（primary 係對白）；5 句同時有 primary fix＋ALT98 fix，各自喺自己 span 入面改咗。
- Live drive：未跑——瀏覽器死，等恢復後補跑。

## §4 備註

- `dualMock` 喺主載入路徑有 fetch＋`DualMeet.loadMock` 會跑，「preview-only」未經 code 確認，即係呢啲 beat 可能玩家見得到。WF5 overrides 係 v20a87 特登寫做廣東話，今票按用戶拍板改做書面語。
- 未評估漏網候選（即刻、嗌、㗎、攞、擡、「話」殘留 6）冇加入標記表，留下一輪。
- 落地：squash merge 入 main → push main → curl 核實線上同 main HEAD:index.html 逐 byte 相同 → 刪工作副本。
