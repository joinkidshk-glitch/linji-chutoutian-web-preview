# NOTES_V20A246_CASTMIG — ensureCastingTagsState 舊存檔遷移清理

- 刪 `ensureCastingTagsState()` 入面舊存檔標籤改名遷移 loop（舊 L27840–27852，13 行）：動作演員→身手好／大牌→耍大牌（v20a57）＋識分寸→識做人（v20a217）。函數本身留返：初始化 `S.castingTags = []`＋回傳，6 個呼叫點全部唯讀使用。
- 死因核實（統籌親查）：registry `content/STUB_CASTING_TAGS_v1.json` 10 個標籤入面冇呢 6 個值任何一個（動作標籤係 `tag_action`／「動作好手」）；新庫 241 張通告 `tagOnComplete` 全空；舊存檔 v228 已定冇意義。舊值無任何 live 路徑寫入。
- 附帶發現（唔喺呢票，留返）：身手好／耍大牌喺 live 檢查入面仲有出現（N9／N12 tagAny、ENDING_NEG_TAGS410、WEAK_MARKS、L27511 regex），但永遠寫唔入，嗰啲檢查 dormant——留返唔郁。TEXTFIX57_EXACT 嘅「動作演員」→「身手好」／「大牌」→「耍大牌」＋TEXTFIX57_KEY_RENAME（L14395／14399）係另一層機制，同樣 0 命中，同樣留返唔郁，另開票先處理。
- 測試：terms57 釘死遷移行為嗰兩條已更新（`"身手好"` 計數期望 6→4；舊遷移檢查改為斷言已刪除；加多一條斷言 accessor 仲在位）。其餘 5 檔純行數漂移 resync（gift185／rom176／tang171／tang173／travel114，各 −13，內容逐行核實純漂移；travel114 段邊界用整行 `}`，單次掃描 dict 查表）。全套 suite 314／10 零回歸。
- 工作報告：`~/workspace/linji-language-sample/CASTMIG_WORKLOG.md`。
