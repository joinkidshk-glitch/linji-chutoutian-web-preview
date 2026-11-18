# NOTES_V20A313 — Q26 高俊傑同場兩段死 code 刪除

- 版本：v20a313（Q26）
- 基線：main `bec7a84`（v312，suite 375／9）
- 結果：suite 376／9（基線 375／9；+1 係新測試 test_r313_ko_rival_dead.js；9 項 pre-existing FAIL 不變：flash51／slot50／soft_tip_111_restore／start53／weave43_static／weave44_static／weave49_static／wf5_87／wrap38）；Pages md5 `a5dbc7c0e79b915d7b7682a77fd12730`／4,697,273 bytes（見 §5）
- 新測試：`tests/test_r313_ko_rival_dead.js`（18 項，ALL PASS）

## 1. 刪咗乜（index.html 淨 −19 行，47285→47266）

兩段都讀 fellows 有冇高俊傑，永遠唔觸發，係死 code。死因：D-v2-2 刪咗高俊傑名額＋池抽兜底；全庫得 `gig_1991_film_102`《霓虹夜影》提過佢（blurb／boardNote／synopsis 文字，cast leadM 係 null）；`awards63Fellows` 只讀 cast／singer／host，fellows 永遠唔會有高俊傑。

| # | 位置（舊行號） | 內容 |
|---|---|---|
| ① | L31295–31308（14 行） | 結果卡 R4 同場對照：註解＋`rivalHeadBit` IIFE——搵 outcome won／nominated 且 fellows63 有 star「高俊傑」嗰格，贏就出「今屆同高俊傑同場提名，你贏咗呢一場。」、輸就出「今屆同高俊傑同場提名，獎落Ｘ手，下年再鬥。」 |
| ② | L32169–32173（5 行） | 典禮揭曉前對決 beat：註解＋`koF208` 兩行——有高俊傑同場嗰陣 push 一格 rival beat（「同場有高俊傑《Ｘ》——今晚呢個獎，係你哋兩個嘅對決。」） |

跟手改動：`rivalHeadBit` 喺 L31389 模板有用（`${catsHtml}${felBit186}${rivalHeadBit}`），一併清埋插值，模板而家係 `${catsHtml}${felBit186}`，唔留死變數。`koF208` 只喺嗰兩行用，無其他引用。

## 2. 守住晒

- 結果卡其他行、典禮 beats 其餘格（nominee／suspense／reveal）唔郁；刪除接駁位逐行核實（felBit186 → v20a214 註解；nominee beats → suspense beat）。
- 高俊傑其他 live 用法一行都唔郁：對手 NPC（`rival:{ id:"rival", name:"高俊傑", face:"npc_ko" }`）、結局旗（rival_gao_hard／rival_gao_endure）、師父旗（flag_ko_mentor_complete／flag_ko_rival_respect／flag_ko_cold_war）、競爭線（weave／通告競爭情報／N3 交鋒）、film_102 文字提及、rivalry trigger（film_102 rivalScoreMin 3）。全檔「高俊傑」仲有 56 命中。
- 舊檔唔 crash（新測試覆蓋靜態；刪除淨係刪 code，唔改數據形狀）。

## 3. 測試

- 新 `tests/test_r313_ko_rival_dead.js` 18 項 ALL PASS：
  - (A) 靜態：rivalHeadBit／koF208／兩段輸出句（「今屆同高俊傑同場提名」「你贏咗呢一場」「下年再鬥」「同場有高俊傑」「係你哋兩個嘅對決」）／R4 註解全檔 0 命中；模板淨係留 catsHtml＋felBit186；典禮 beats 唔再 push id:"rival" 格（NPC 定義 `rival:{ id:"rival" }` 唔計）；suspense／reveal 仲喺度。
  - (B) 守住：高俊傑 live 用法（見 §2）全部在位。
  - (C) gigs_new.json 仍係 306 張。
- 舊測試 mock 檢查：全 tests 目錄無一處引用已刪輸出句；`test_awards178_logic.js`／`test_awards178_static.py`／`test_awards204_logic.js`／`test_awards204_static.py`／`test_awards63_logic.js` 係退役測試，斷言 fellows 永遠唔含 ko／高俊傑（fellows 函數層面），唔受今次刪除影響；`test_awards186_logic.js` 用 mock fellows（含 ko_chunkit）測 C1 重複行規則，測嘅係 felBit186 嗰行，唔郁；四個含 "rival" 嘅測試（test_gig229_trigger／test_r285_rival_cfg／test_r297_remove_vera_mei／test_wf3_82_logic）全部係對手系統（trigger／CFG／NPC），唔掂典禮 beats／結果卡。**無測試要改斷言。**
- 第一輪 suite 371／14——多出嘅 5 項 FAIL 全部係釘行漂移（gift185／rom176／tang171／tang173／travel114），唔係功能回歸。`qa313/resync313.py` 用 difflib opcodes 核實唯一差異係兩段 19 行＋模板插值 1 行，逐個錨點核實純漂移後重寫 5 檔（gift185 1 行、tang171／173 各 3 行、rom176 4 行、travel114 29 行：DEF／COUNT 4 處／FREE 24 處）。重跑後 5 檔全 PASS，第二輪全套 376／9。
- resync 段邊界：＜31295 唔郁；31309–32168 −14（本票 5 檔無釘行喺呢段）；≥32174 −19。教訓：difflib 會將刪除區入面嘅 `}` 行對位去附近相同內容行，`not in mapping` 斷言太嚴——改用 opcodes 核實刪除區。

## 4. 殘留

- 無。Q26 結案；Q1–Q26＋B1 全部落地／結案（Q5 已解決唔開票、Q16 核實結案唔落地、Q21 唔開票）。

## 5. 落地

- main HEAD：`8f8a41f`（內容）＋＿＿＿（NOTES §5 補填）
- Pages：index.html md5 `a5dbc7c0e79b915d7b7682a77fd12730`／4,697,273 bytes（byte-identical）
- 工作副本 `linji-work313` 已刪；`qa296/derive296.json` suite 重跑再生，已還原，唔入版。
