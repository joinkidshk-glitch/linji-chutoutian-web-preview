# NOTES_V20A162_TITLES_TAGS — 手帳標籤頁開放＋稱號區

- 日期：2026-11-17；基底 main `4f79e7c`（v264）；分支 `v162`。
- 背景：手帳「標籤」頁俾 dev 閘閂住，正常玩睇唔到，但 `S.castingTags` 會影響結局軌跡呈現。用戶 2026-11-13 拍板開放標籤頁＋tag 卡＋同一頁稱號區；2026-11-17 15:56 拍板而家開工。

## 改動（index.html 淨 +118 行）

1. **tab 改名**：手帳 tab 掣「標籤」→「稱號」（內部 id `htab-tags`／`home-pane-tags`／`tags-list` 唔郁）。
2. **拎走 dev 閘**：刪 `freeplayDevTagsOn()` 定義（7 行）＋`syncDevTagsTabVisibility()` 定義（13 行）＋兩處呼叫（`ensureWeakSeals` 內 1 處、`loadFreeplayFramework` 內 1 處）；刪 `setHomeTab` tags→plan 彈回行（1 行）。弱印章留返。
3. **`renderCastingTagsPane` 重寫（TITLES162 block，161 行）**：頁頂現時稱號＋結局梯即時位置＋獎項數目＋跳轉連結；其下 tag 卡逐粒顯示 label／來源／軌跡組。來源解析對返 live 數據：`story-ripple:<id>`／`story:<id>`／`gig:<id>`（`StoryOC.findNodeRaw`／`work59GigLookup`）；舊存檔純字串條目有分支處理。
4. **進度頁頂**：插 `progTitleLine162` 行（現時稱號一行；注意現行 main 進度頁 intro 已經係書面語「逐幕列出開放條件與阿偉目前的進度：✓ 是已達標」，唔係舊版廣東話句）。

## 移植方法

- 工作副本入面有 v151 時代嘅未提交部分工作（已 commit 做 `a465cb7`「v20a162 WIP」留檔）。基底差約 110 版、主線內嵌表已刪，唔用 cherry-pick，改用 `/tmp/port162.py` 將舊 diff 嘅 TITLES162 區塊（161 行）逐字抽出再插上現行 main，全部編輯逐項 assert exact-match 計數。**區塊逐字節同舊版一致**。
- `S.castingTags` 條目形狀已核實：`{id, label, at, from}`。

## Resync（v162 淨 +118 行，全部純漂移）

- 頭一次全套 suite 324／15：5 檔釘行測試漂移（gift185／rom176／tang171／tang173／travel114）。用 difflib 舊 main→新檔對位，全部釘行內容逐字相同，零 mismatch：
  - gift185／tang171／tang173：總行數 46118→46236（標籤 46129→46247），鏈尾加 ＋v162 +118；openLoc DEF 41329→41447，guard 41335→41453、`lines[41328]`→`lines[41446]`；tang173 L4862 釘行 5204 喺改動點之前唔郁。
  - rom176：4 釘行各 ＋118（39679→39797、40054→40172、41214→41332、41362→41480）；6431／14875 唔郁。
  - travel114：COUNT／FREE／DEF／WRAPPER 按映射重寫（28292／28325／28654 各 −21、WRAPPER 29223→29204（−19）、其餘其後錨點各 ＋118；DEF 41329→41447）；共 33 處。
- Resync 用單次掃描 dict 查表，唔逐對 re.sub。期間捉到一個 single-scan 陷阱：pair 2（鏈尾＋`html.count`）食咗 pair 3 斷言嘅 `html.count` 前綴，令 `== 46118` 斷言漏改——已補修（`== 46118`→`== 46236`，三檔各一處），教訓：重疊 pair 要分開兩輪或錨點唔好重疊。

## 驗收

- 新測試 `tests/test_titles162_static.py` **48 項 ALL PASS**（閘清零、tab 改名、tag 卡、稱號區、梯位置、獎項、進度頁行、弱印章留返）。
- `test_book143_static.py`／`test_text55_static.py`（按新期望改）ALL PASS。
- 主 script 抽出 `node --check` 通過。
- **全套 suite：TOTAL PASS 329 FAIL 10**（基線 328＋新檔 1；十項全部係已知 pre-existing FAIL：flash51／rumor49／slot50／soft_tip_111_restore／start53／weave43／weave44／weave49／wf5_87／wrap38；`/tmp/qa162/suite162b.txt`）。
- 唔改 SAVE key（`starVolunteer_map_v19w`）、softRev（`s107`）、產品 `?v=`（`v20a10`）。

## 未做／押後

- **實機驗證押後（瀏覽器死）**：標籤頁實機顯示＋稱號區，等瀏覽器恢復再驗。
- 唔做：標籤／人情淨刪（另票）、新標籤設計（只顯示現有系統）。
