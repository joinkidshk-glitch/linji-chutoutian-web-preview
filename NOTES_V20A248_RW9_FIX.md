# NOTES_V20A248_RW9_FIX — TEXTFIX55_EXACT 逆向映射修復

- **落地**：v248（squash merge，唔開 PR）
- **問題**：RW-8 發現 `phase3CastCopy` live subLine 同 MOCK 版書面句有分歧，背後係 TEXTFIX55_EXACT 映射將書面洗返廣東話。審計（`~/workspace/linji-language-sample/TEXTFIX55_REVERSAL_AUDIT.md`）證實 EXACT 46 條入面 21 條逆向（書面旁白／標籤 → 廣東話），違反語言規則。
- **Suite**：314／10 零回歸（10 項全部係已知 pre-existing）

## 改咗咩

| 組 | 條目 | 做法 |
|---|---|---|
| A（純刪除） | #23、#25、#27、#29、#31、#33、#35、#43、#46 | 來源 key 本身已係書面語，直接刪映射。#43／#46 係恆等條目（key＝value），刪咗零影響。 |
| B（鄧麗萍排片線） | #20、#21、#22 | 來源重寫做書面語，保留正確地點「排片部夜班房」（唔還原「院線票房中控室」）＋電話報回數字／午夜場票房表；再刪映射。唯一 runtime 來源係 `content/MOCK_STORY_DENG_LINE_PUSH_SOFT_v1.json`（index.html 內無內嵌副本）。 |
| B（後果式標籤） | #24、#26、#28、#30、#32、#34、#36 | 來源 `playerFacingNote` 重寫做書面語嘅後果句（保留 value 意思，唔還原意圖句）；再刪映射。 |
| C | #9 N16 緋聞 synopsis | 來源重寫做書面語，保留 1990年冬＋「週刊」，關海媚提及保持原狀（v159 先處理）；`tests/test_kwan151_textfix.js` 同步改做 assert 新句原樣輸出，`test_kwan151_static.py` B3／B5 改做 assert 映射已刪。**發現：live 主線 pack（19 節點）嘅 N16 而家係「賀歲片」，舊緋聞 synopsis 只剩喺 EXACT key、測試 fixture 同 QA 舊檔——#9 映射喺 live play 早已係死映射。** |
| C | #37 周采兒 | 來源（`content/story_beats_phase1.json` N5 小訪）重寫書面語，保留「有啲印象」意思（唔還原「好感夠了」）；再刪映射。 |
| C | #44 phase3CastCopy | index.html 內嵌兩處（`phase3InlineMock` L39315＋`phase3CastCopy` L39392）廣東話 value 改返書面 key；MOCK 檔本身已係 key，唔使改；再刪映射。 |
| D（WF5 覆寫層） | 4 句抉擇標籤 | `applyVariantWf5Overrides87` 喺 walk 之後無條件寫入 `WF5_VARIANT_OVERRIDES87` 標籤，蓋過 EXACT 刪除嘅效果。4 句廣東話標籤（`C_tang_push1_prove`、`C_tang_crisis_data`、`C_tang_crisis_favor`、`C_tang_crisis_middle`）重寫做書面語；其餘 5 句已係書面語，留返。 |
| E（WF5 beats 行） | 2 句 | 同一覆寫層仲會換走 `R_tang_push1` beats[0]／beats[5] 嘅 lines，令 B 組 #21／#22 新句俾舊內容「票房中控室／螢幕」寫返入去，同 #20 setting 自相矛盾。兩句 WF5 行換做 B 組新句逐字照抄。 |

- **唔郁**：#13 Vera（v159 刪）、對白組 9 條（書面→廣東話，對白正確）、中性組 14 條、NOTE_EXACT 6 條、PHRASES 6 對、SAVE key、softRev、?v=。
- **EXACT 表**：46 → 24 條（剩低＝對白 9＋中性 14＋Vera 1）。
- **WF5 標籤寫法**：D 組新句無加句號，同表內其餘 5 句書面語標籤一致。

## 核實

- 中央刪表逐條斷言 key 喺表內恰好出現 1 次；刪後表同 A／B／C 三組工人各自嘅表做 key 集對照：合併結果＝三組交集，完全一致。
- 全載入模擬（真正載入順序 `textfix55StoryPack` → `applyVariantWf5Overrides87`，餵真正 MOCK JSON）：**38／38 PASS**——7 個 label＋7 個 playerFacingNote＋3 個 setting／lines 全部書面新句；22 條舊 key／21 條舊廣東話 value live 絕跡。
- `node --check`（抽兩個 `<script>` 塊，等效做法，`node --check index.html` 字面跑唔到）；改過嘅 4 個 JSON 全部 `JSON.parse` OK。
- kwan151 兩個測試 ALL PASS；wf5_87 logic PASS 52／0。`test_wf5_87_static.py` 跑唔起——佢寫死咗已刪除工作副本 `linji-work86` 嘅路徑，係已知 10 項 FAIL 之一，唔係本票整爛。
- drive*.py 無硬抄受影響句子，唔使同步（RW-8 要同步 drive157 嗰類情況今次無出現）。

## 殘留（另票／留返）

1. `R_tang_push1` beats[3] 仲有「螢幕」一句（「鄧麗萍的眼睛離開螢幕，望向阿偉…」）——B 組 MOCK 新版本身都有呢句，唔係舊內容殘留，留返；如要改，另開票。
2. 舊標籤／舊句殘留喺凍結歷史證據檔（`qa149/pristine_index.html`、`qa152/drive152.json`、`NOTES_V20A152.md`、舊 fixture `story_detail_romance_tang.json` 變體句），唔係 live code，留返。
3. DengLine 實機抽檢待瀏覽器恢復後做。
