# NOTES_V20A241 — RW-5：事件／NPC／教學／禮物／UI 逐句重寫＋覆寫表刪除

- Base：main `f5c4488`（v240）。分支 `v241`（工作副本 `linji-work241`；工人副本 `-a`／`-b`）。
- 落地：squash merge → main，push main。工作報告 `~/workspace/linji-language-sample/RW5_WORKLOG.md`（工人改寫清單逐條見 `RW5A_DRAFT.md`／`RW5B_DRAFT.md`，統籌已對住 patch 逐條核實）。

## 改咗乜

RW-5 逐句重寫（輕口語對白＋香港式書面語旁白；報紙正式書面語）：

| 組 | 改寫 |
|---|---|
| A 重做：JSON packs（events／npc／tutorial／beats／gift_react／gift_prefs／items／freeplay／favor／casting／era／dualMock／dualSeed／sandbox／WF5） | 169 處 |
| B：index.html 內嵌 UI | 202 對／236 處 |
| 合併層：10 句 gift_react 普通話對白補漏 | 10 句（17 處替換） |
| 合併層：教學句還原 v108 定稿 | 30 句 |
| 采兒更名＋周刊補漏 | 11＋1 處 |
| **合計** | **457 處** |

其他改動（同一票）：

- **4 個內嵌 fallback 表全部刪除**（NPC_LINES_CORE／EVENTS_ZH_HK／STORY_BEATS_PHASE1／TUTORIAL_ZH_HK；JSON 做唯一來源）。`events_zh_HK.json` 補 `UNLOCK_STAMINA`（25→26 keys）。
- **覆寫表刪除**（用戶 2026-11-16 拍板，類比 v234）：WF4 表全刪（20／20 一致）；WF2 刪 15 條、剩 10 條（R_vera_* 5 條唔一致＋R_lan_* 5 條分層生效，保留）；LAN 表 0／5 一致，成張保留。載入模擬證明：生效版 66 節點 diffs 0。
- **TEXTFIX55_EXACT** 134→64（A）→58（合併層刪 6 條教學死映射）；**TEXTFIX57_EXACT** 9→8（刪 1 條死教學映射）。NOTE_EXACT 9 條全部保留。
- **TEXTFIX57「點擊→撳」裁定：KEEP**（唯一活玩家源頭係 MOCK 教學檔 1 處；刪映射會令「點擊都得」原樣見玩家；測試 A4 釘死）。
- **DS filter 定位：已死碼**（無呼叫碼、無 loader、無 runtime 讀取點；只剩 metadata 痕跡＋兩個未載入 content 檔，共 66 句）。去留等拍板，今票唔刪。
- **采兒更名**：報紙／頒獎面「采兒」→「周采兒」（STUB 故事報紙 11 處；裸「采兒」0 殘留）。對白／引話／凍結覆寫表／「采兒小訪題」標題唔郁。

## 統籌訂正（工人稿入面冇，合併層親手做）

- A 第一稿將已係輕口語嘅對白逐詞換成普通話，成批打回重做（還原 219 處、真正重寫 28 處）。重做後再漏 10 句 gift_react 普通話對白，合併層補改（見上）。
- B 將教學 JSON 新句自行改寫，偏離 v108 定稿；30 句已按已刪 EXACT 值還原。B 嘅 suite 314／10 聲稱唔成立——喺 B commit 上面 text108（6 項 FAIL）＋guidance34（2 項 FAIL）已經 FAIL，呢兩檔係合併層修返。
- LAN 表同 RW-3 報告唔一致：RW-3「JSON vs 生效版差異 220→0」只係文字層；LAN 嘅 beats 結構／choices／when 等欄位從來冇對齊。LAN 同步等下一票（先定邊版係準）。

## 測試

- 全套 suite **314 pass／10 項已知 pre-existing FAIL**（flash51／rumor49／slot50／soft_tip_111_restore／start53／weave43／weave44／weave49／wf5_87／wrap38），同基線一致。
- 測試更新 15 檔：覆寫表刪除 4 檔（wf4_86／wf2_81 logic＋static）、text108／guidance34（改查 JSON）、tang167（期望值同步）、8 檔釘行 resync（覆寫表刪除令 index.html 淨 −859 行；74 錨點 difflib 核實純漂移；腳本 `qa241/resync241.js`）。
- `vm.Script`：index.html 兩段 inline script 全部編譯通過。

## 跟進（唔喺今票）

WF5 choi／hiu 變體成套重寫；LAN 表同步 JSON；casting `labelToId` 鍵同新 label 唔同步；TEXTFIX55 NP214 死映射＋stub 36 處頒獎類別行死 fallback；DS filter 去留；TEXTFIX57_EXACT 4 條死映射；N5 synopsis／playerHint 裸「采兒」；`cast_main.json` 2 處簡體「周刊」。
