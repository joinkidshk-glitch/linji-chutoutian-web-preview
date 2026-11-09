# NOTES v20a13 — Weave Phase 1-1：報紙「花邊短訊」（鏈 D 上半）

日期：2026-11-09
性質：soft 預覽功能增量（規劃實作 Phase 1 第 1 步）。Soft≠PASS。SAVE key 不變（`starVolunteer_map_v19w`）、softRev 不變（s107）、`?v=` 不變（v20a10）。
分支基礎：疊喺 `fix/p03-rumor-filter-consistency`（PR #109）之上；#109 合併後本 PR 改 base 去 main。

## 背景

按《系統串聯規劃》§6 落地分期 Phase 1（數據先行、零新機制）：
鏈 D 要求報紙除咗寫玩家，仲要有「唔關你事嘅娛樂圈花邊」——報紙先似一份真報紙，
花邊碎片日後（Phase 3）會入返傳聞池做跨系統拼合。Phase 1 先做顯示面。

## 改動（只改 index.html）

1. **新增 `PAPER_SIDE_ITEMS` 靜態池（16 則）**：虛構紅星花邊＋真地名＋日常質地
   （清水灣片場、廟街、跑馬地、重慶大廈、電視城飯堂、大排檔…），跟串聯規劃 §4.5 碎片庫。
   部分條目有年份閘：卡拉 OK／移民講座／散席飯（1989 起）、程天諾廣告／啟德送機（1990 起）——
   1988 年嘅報紙唔會出現未發生嘅時代話題，移民潮味道跟年份慢慢滲入。
2. **新增 `paperSideItemForDay(day)`**：按遊戲年份過濾池、按日序輪替揀一則，
   包成同現有 shorts 一樣嘅結構（`source:"side"`、`fameDelta:0`）。
3. **`buildNewspaperEdition`**：每份 edition 尾加一則花邊短訊。唔計聲望、唔佔頭條同玩家短訊位。
4. **`pushNewspaperRumor`**：`source==="side"` 同 `"summary"` 一樣跳過——Phase 1 花邊唔入傳聞池（入池留 Phase 3）。

無改：SAVE 結構（花邊只存在於 edition／clippings 既有 `shorts` 陣列入面，舊檔照讀）、
報紙去重、聲望結算、顯示過濾。

## 測試

- 新增 `tests/test_weave1_logic.js`（本地）：抽真函數跑——edition 恰好一則 side、按日輪替、
  1988 池唔漏 1989+ 條目、1989 解鎖移民類、1990 解鎖啟德類、聲望總數不受影響。12/12 PASS。
- 新增 `tests/test_weave1_static.py`（本地）：接入點、花邊池無真藝名、SAVE key／softRev 未變。14/14 PASS。
- 回歸：P0 邏輯／靜態、P0-3 過濾／靜態全部照過；全檔 script `node --check` OK。

## 待覆檢（合併＋部署後）

- 新存檔玩到第一份報紙：版面底部應有一則「花邊短訊」，內容唔關阿偉事；
  連續兩日報紙花邊應唔同；手帳傳聞唔應多咗花邊條目。
