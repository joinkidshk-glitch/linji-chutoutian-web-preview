# NOTES_V20A235 — 結局唔畀玩家揀（N17 前夕只問去留）

- 拍板：用戶 2026-11-16 07:47 — 結局由三年數值計出，N17 唔再問，結局直接播，N17 只係劇情；N17 淨留三個選項：留低（順其自然，照計出嚟的結局播）／收山（E6 安穩版）／走（E6 遠走版，限諗過走的人）。其餘臨尾選項一併拎走。
- Base：main b353034（v234）。分支 v235，兩 commit：aa3cf0c（實裝）＋c5839b2（行數 resync）。

## 改動（6 檔，+85/−62；另 resync 8 測試檔 +77/−69）

### index.html（淨 −24 行，總行數 45351→45327）
- `endingEveOptions410`：刪 `to_backstage`／`to_support`／`leave_follow` 三個生成分支；只留 natural（留低）／quit_job（收山）／quit_leave（走，限 `flag_leave_mind`）。函數頭頂註解重寫做新規則。附帶清走兩個變死嘅 local（`base`、`favor`）；`baseRes` 參數保留（`void baseRes`，兼容舊呼叫）。
- `ending410AfterEveChoice`：刪三個對應處理分支（`leave_follow` 的 `{exodus:"leave"}`、`to_backstage`／`to_support` 的 career 覆寫＋title 重算）及變死嘅 `const base`；保留 quit_job／quit_leave／natural。
- 註解同步：phase 4-10 頭註解、N17 節前註解、StoryPlay.start 的 N17 hook 註解——「相鄰規則」→「去留三則」。
- **`resolveEnding410` 一行未郁**（git diff 核實）。

### content/story_detail_n1_to_n17.json（N17 節點）
- `synopsis`：「六個意向裡面鎖一個」→「今晚只問一題：走，還是留」。
- `flags_written`：6→3，刪三支死旗（`flag_ending410_to_backstage`／`to_support`／`leave_follow`）。
- beats 15 個一字未郁；靜態 choices 兩則（natural／quit_job）未郁；其他節點未郁。

### 測試（只改斷言做新行為的正確期望，無放寬）
- `test_weave410_logic.js`／`test_weave410_static.py`：eve key 清單改做 present 三則／absent 三則；新增去留軸回歸測試（d2）＋CHOICE_IDS 映射斷言；`leave_follow` 全流程改做 `quit_leave` 全流程。
- `test_story157_pack_static.py`：nodes[5:] sha 重算 `1be6aa08…`→`7adfea57…`（先確認 diff 得返預期兩處先重算）。
- `test_wf1_80_logic.js`：N17 `flags_written ⊇ v136 fixture` 改做 N17 例外 exact 等於三則 live 旗（其餘節點維持 ⊇；刪旗係刻意設計，唔係意外）。

## 去留軸（重點，已逐行追）
- 修咗一個真缺陷：舊行為下，諗過走（`flag_leave_mind`）但揀留低的人會出 `exodus=undecided`（稱號「未說出口的人」），因為 `resolveEnding410` 得 `flag_stay_mind` 先兜底做 stay。修法：`ending410AfterEveChoice` 入面 natural 明確傳 `opts={exodus:"stay"}`（留低本身就係表態留低），`resolveEnding410` 本身唔郁。修復後前夕三條路全部有確定值（留低→stay、收山→stay、走→leave）。
- E7 強制收場刻意無修：玩家去唔到前夕，undecided 係誠實值；E7 呈現本身就係為呢個狀態而寫（`conseq61ExodusWord`、「未表態——留白」）。

## 全套 suite
- 初跑 304／18：8 項新 FAIL 全部係行數釘漂移（v235 淨 −24 行；喺 base b353034 8 項全部 PASS）。resync 8 檔（gift185／kwan151／rom176／tang152／tang171／tang173／text125／travel114）：只改釘值＋chain 註解（單次掃描 dict 查表換值；difflib 核實純漂移），無改斷言內容。
- 統籌親自再跑全套：**312／10**，FAIL 清單正正係基線 10 項已知 pre-existing（flash51／rumor49／slot50／soft_tip_111_restore／start53／weave43／weave44／weave49／wf5_87／wrap38），無新增、無遺漏。
- JS 語法：兩個 inline `<script>` 塊 `node --check` 2/2 PASS。

## 遺留（唔係呢票範圍，等拍板／另開票）
1. **reconfirm 機制根本唔存在**：全 repo grep `reconfirm` 零命中；StoryPlay 撳選項即刻落決定，中間無二次確認。2026-11-15「所有抉擇都要 reconfirm」係拍板，未有實裝票（規劃文件 M-1／G5）。v235 無加——全域機制唔係呢票範圍，N17 局部加會同其他抉擇行為唔一致。請決定係咪另開 reconfirm 實裝票。
2. **N17 beats 殘留舊揀格文案**：第 3 拍何生「繼續做演員、轉做幕後班底，或者兩邊兼顧」、第 13 拍「六個意向，鎖一個」「只能走到隔壁那格」、第 15 拍「等他親手圈那一格」——同新規則打架，但 brief 禁改 beats，留待語言／劇本票處理。
3. **E7 去留 undecided 保留**（見上）：如用戶認為 E7 結局頁都唔應該出「未表態」，要另行拍板點預設。
4. `endingBackstageClose410` pre-existing 死函數（v95 已無呼叫者，淨測試引用）；`ENDING410_CHOICE_IDS` d–f 未用但保留做命名空間——兩者刻意保留。
5. `tests/fixtures/` 兩個舊 snapshot（spine_c6_c17_v79／spine_n6_n17_v136）仲有舊 flags_written——版本快照，唔郁。

## 紀律
- SAVE key／softRev／`?v=` 零改動。`git push` 經 deploy key 直推 main，唔開 PR。
