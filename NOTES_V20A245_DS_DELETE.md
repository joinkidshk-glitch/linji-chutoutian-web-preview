# NOTES_V20A245_DS_DELETE

- 版本：v20a245（DS filter 刪除）
- 拍板：用戶 2026-11-16 15:02，刪走 DS filter 兩檔。
- 刪走：
  - `content/DS_PLAYER_ZH_FILTER_TABLE_v1.json`（66 項，declared count 66，66 個唯一 id）
  - `content/_ds_filter_ui_corpus_v1.json`（66 項，66 個唯一 id）
- 核實（統籌親數，非齋信舊報告）：
  - 兩檔 id 集合完全一致，逐 id `old` 值一致；TABLE 多 `new`／`reason` 欄，CORPUS 多 `source`／`ctx` 欄——同一批 66 條存咗兩份，屬實。
  - 檔名引用：index.html 0、tests/ 0、其餘 content JSON 0；泛查 `DS_PLAYER`／`ds_filter` 於 index.html／tests 亦 0。
  - 兩檔無 loader、無 runtime 讀取點，從未載入。
- 唔郁：
  - `content/HANDOFF_DS_PLAYER_ZH_FILTER_v1.md`、`content/NOTES_V18U_DS_PLAYER_ZH_FILTER.md`、`content/PLAN_MAP_BOARD_DECISIONS_v1.md` 等文件檔（決策記錄留返）。
  - `content/tutorial_zh_HK.json:4` `source` 欄 metadata 痕跡（無程式讀取，留做殘留）。
  - live 3 處「通告板」（index.html L23169／26333／26390，另一條待拍板問題，今票唔郁）。
- 驗收：vm.Script 編譯 inline script block 2/2；全套 suite 314／10（FAIL 清單同基線已知 10 項一致），零回歸；Pages 線上 index.html sha1 同 main 逐 byte 一致。
- 工作副本 linji-work-dsdel＋分支 dsdel 已刪。
