# NOTES_V20A247_RW8_FINAL — 語言重寫 RW-8：結局文案轉書面語（補記）

> 本檔為 v247 落地後補記：統籌回報話版本筆記已入 repo，但核實發現 v247 commit 入面漏咗呢個檔（新檔要用 `git add <path>` 明確加，`git add -u` 會靜默忽略——v146 教訓）。內容按 `~/workspace/linji-language-sample/RW8_WORKLOG.md` ＋統籌落地回報重建，數字全部來自嗰兩份記錄。

- **落地**：v247，main HEAD `ebbc2f0`（squash merge，唔開 PR）
- **Pages**：線上 index.html sha1 `5a717227f0e1ac3a50bf8ac7b50e67d03b3580b3`，同 main 逐 byte 一致；HTTP 200，4,515,541 bytes
- **Suite**：314／10 零回歸（10 項全部係已知 pre-existing）

## 改咗咩（統籌自數）

| 簇 | 盤點 | 實改 | 留低 |
|---|---|---|---|
| 結局文案 | RW-7 話 188 句；逐句抽取實數 292 句含廣東話標記 | **297 句**（A 155：gaps／eve／career／summary；B 142：romance／exodus／inserts，捉多 5 句標記集漏咗嘅） | 重掃剩 28 句，全部係「」引述入面人物原話（G5 原則留廣東話） |
| 旁白「着」→「著」 | RW-7 話 52 處；實數 48 處旁白要改 | **48 處**（U+7740 → U+8457） | 35 處留返：對白／引述／程式鍵名／死檔 |
| 描述類 | STAR_SIGHTINGS 30 欄改 24 欄；INTEL gig／sightLine 26／26 全改；頒獎 win／lose／galleryLine 45 行核實 0 句要改；MOCK_UI_PHASE3 檔同步 | 見左欄 | — |
| 「通告板」→「通告欄」 | live 3 處（情報文／toast／引述），每處只改一詞 | **3 處** | N1 章標題「通告板」唔郁（用戶親自揀） |

- 「」引述人物原話一字未郁；ADJ_RUMOR 17 行本身已書面。
- 統籌合併補改 5 處：gaps「聲望／信用仲差」→「還差」×2、MERGE_PAIRS 拼合情報正文 2 段轉書面語（鍾楚凝段「」引述留廣東話）、E6 阿媽句加「」明示引述。
- 合併衝突 3 處（test_weave410／test_cleanup100／TEXTFIX55_STAR_LOOKS）全部對 live 核實手動合併。
- `qa131/drive157.py` 硬抄 ECHO89 表已同步新版（連帶修咗佢本身已漂移嘅一行：寫「收科」但 live 係「埋單」）。
- 驗收重掃：結局區含標記句 292→28（全部引述原話）、着 83→28（全部屬保留類別）、STAR／INTEL 含標記 0、通告板 live 0。
- 試讀 10 句全部一次讀順；vm.Script 編譯 2/2。

## Parent 獨立核實（v247 落地後）

- main HEAD `ebbc2f0`＝`git ls-remote origin main`；Pages sha1 同 main 一致；TEXTFIX55_EXACT 維持 46；工作副本＋分支已刪。
- Parent 親跑全套 suite：**314／10**，FAIL 清單同基線已知 10 項完全一致。
- Parent 逐處核實殘留「着」：index.html 剩 14 處，全部屬保留類別（對白／引述／程式碼／註解）；content JSON 剩低嘅「着」除咗對白之外，只喺未載入嘅 `story_detail_romance_tang.json`（v20a152 已停載，鄧麗萍感情線取消）——dormant，唔係 live 漏網。
- 殘留「通告板」10 處全部係 code 註解／美術 brief，唔係玩家面文字；live 0 命中屬實。

## 新發現（另票，唔喺 RW-8 範圍）

1. `phase3CastCopy` live subLine「火候未夠。先跟班睇多幾場，練好再嚟報。」同 MOCK 版書面句有分歧，背後係 TEXTFIX55_EXACT 映射將書面洗返廣東話——要另開票查。
2. MOCK 檔 meta／devAppendix／toasts.rumorHint／hooks 何生行殘留廣東話（DEV 註，未定性）。
3. 結局「聲望／信用」系統名外洩（術語問題，另票）。
4. 結局第二人稱「你」保留（聲道問題，唔喺語言票範圍）。

## 語言重寫收科

RW-0…RW-8 全部完成。TEXTFIX55_EXACT 殘留 46 條（全部測試釘死或仲有 live 源頭）。
