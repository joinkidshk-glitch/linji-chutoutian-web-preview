# NOTES V20A55 — 文字修復（審計 176 條跟進）

基線：v20a54（4,247,738 bytes）→ 本版 4,303,107 bytes（+55,369）。
機制：**唔直接改 content pack JSON**（repo 慣例）。新增 `TEXTFIX55` 載入清洗層（index 內、packs 載入後即行）：
story／gift／freeplay／tutorial overlay／phase3 數據喺賦值後行清洗 walk；**所有通告**（pack＋內嵌 fallback＋衍生合成）經 `normalizeGigRecord` 統一清洗。另有一批 index 源碼字面直改（內嵌數據/UI 字串）。
冇改 SAVE key／softRev／?v=／任何邏輯同數值；只改字串。

## 一、出街修復（玩家會見到）

### 優先項
- **A1/A2 手帳 `[DEV]`**：空狀態改「暫時未有選角標籤。／接多啲唔同戲路嘅通告，行內人會開始用幾個字記住你。」；頁面 meta「[DEV] 選角標籤」→「選角標籤」。全檔 `[DEV]` 歸零。
- **A10 傳聞漏 ID**：「…傳聞 tvb_rules_gossip…」→「你啱啱聽完星河電視台嗰啲規矩傳聞，心入面有好多問號。」（精確表，main＋slots 兩包同句一併處理；`tvb_rules_gossip` 其餘出現全屬內部 id 定義/引用，合法保留）。
- **A6「試玩閘／softBehaviorGate」出街位全清**：開始畫面 li、教學 pack 三條 body/bodyAlt、內嵌 TUTORIAL、結算 dayNote ×2，全改「傾談／送禮唔計日子（茶錢另計）」口徑。`softBehaviorGate` 只剩 code 識別字（函數/旗標名，唔出街）。
- **A16/A17 結算 notes**：`effects.notes` 確認出街（`applyChoice` 收 notes → 選項掣面同結算名單經既有 `playerNotes()` 顯示）。五個 story pack 合計 200 條，清洗層改寫 **170 條**：精確對照 43 條＋規則鏈（刪「愛情結局另表並存／可與事業結局並存」、剝「連 X；」節點前綴、刪「寫入 flag_xxx／supersedes=」、rel_xxx 內部名映射做人名、屬性英文詞（standing/fame/wealth/craft/trust/music）映射做聲望/名氣/收入/手藝/信任、「觸發愛情危機」→「感情線嚟緊有風浪」、P2→日後、敵線→對手線、標點收尾）。結局 label 同步清洗（剝 `HE:/BE:` 前綴、「（連 T6）」尾巴）。
- **時代硬傷**：C20 1990「快閃」通告六欄成套換「商場推廣枱」寫法（連殺青/政策句一併）；C10 殺青卡「俾人截圖」→「俾人剪低」、人情債 toast「請截圖回報」→「請稍後再查一次」、通告 shootHint「上一集截圖」→「上一集劇照」；C11「送命題」→「辣手問題」（短語規則，連 C5 playerFaceLine 衍生副本）；C21「帶貨／喊麥」成句換走（連「不要現代叫賣口播腔」政策尾句刪除）。

### 其餘 (a)/(b)/(c) 出街條目（清洗層＋源碼直改）
- A3 內嵌遠觀描述 ×6 換正式描述；freeplay eraStars 10 位紅星「待補」剪影描述（陸柏言/廖炳星/魏詠男/葉敏芝/麥震東/駱家聲/彭少祺/鍾楚凝/顧明輝/蘇芷茵）由清洗層按 starId 補正式外形描述，phase3 sightings 同步。
- A4 傳聞兜底句換茶水間口吻；freeplay 傳聞碎片 16 條成批重寫（去晒「（傳聞）XXX 表示」速記式）。
- A5 送禮 fallback ×2 去「（佔位）她」；A7「對白池」×3→「傾談話題」；A9 網絡失敗/劇情未載入句改人話；介面鎖 modal 改人話。
- A8 故事提示覆寫表「雙軌總和夠數」×5＋「雙軌夠數先開」×1 →「聲望同信用（總和）夠數」（其餘「雙軌」出現係有定義嘅 HUD/教學語境，按唔好誤傷清單保留）；C11 提示物品名「淡香氛樣品瓶」×7 統一做「淡香水試用裝」（同物品庫一致）。
- 通告面：1991/1992 年池以外，1988–90 三年共 248 張有 **126 張**經清洗改動（五年全池 200/351）：「虛構」免責句/條款全刪（政策句）、「當紅主推／主推・」→「急招」、組製→劇組、口播→讀稿、粉絲→歌迷、上座率→入座率、練習生→學徒、簡體字（风/静/细）還原、B58 高/中 tier 角色名去「臨記」前綴（臨記男主→男主角等）、B63 非動作類通告誤植「吊威也意外」句刪除（動作類保留）、B64 synopsis 與 blurb 重複開頭去重、A47 模板句（「電影組。補位。」類）改寫；內嵌 softBridge「中環快閃檔」→「中環快拍檔」（經 normalize 清洗）。
- 劇情面短語規則：關海媚→當紅花旦（見下節）、星河電視城→星河電視台、電視城廠景→電視台廠景、上座率→入座率、粉絲→歌迷、社交課→魅力課、智商課→觀察課、製作日→拍攝日、互懟→駁火、連軸綵排→密密綵排、資本場→商界；synopsis 行首年份 1991/1992 → 1990（三年制對齊）、C17 notes「四年」→「三年」；B7 一句旁白誤掛對白改掛阿偉；**D1** rival pack 三節（A_lei_meet/push2/ending）誤掛「張克凡」名下嘅阿偉對白共 3 beats 改返阿偉（push1/crisis 嘅高俊傑 beat 經核實唔郁）。
- 內嵌數據直改：EVENTS（AUD_STRESS70/AUD_PASS 等）、STORY_BEATS（B03/B04/B09/B10）、TUTORIAL 五處、NPC_LINES 四句、人情債兜底「（文案待補）」→「人情一筆」、「本週最值得返看」×8→「本週焦點」、「試鏡表現未夠火候」×3 改自然句。
- gift 包：charFix（着→著、别→別）＋限定 lines 語體（沒有→冇、我們→我哋）＋喉咙→喉嚨。

## 二、出街／唔出街分清（冇郁但記錄在案）
- `effects.notes` = **出街**（已修，見上）。node 級 `notes` 欄（節點設計註記）= 唔出街，冇清。
- **A52** heroAngle/diasporaHook（210 條）：index 全文零引用，永不出街，冇清（回寫清單記低）。
- **A33** SOFT_PROGRESS_SEED titles、**A45** SCHEMA `rosterPlanned`、**A62** gigs `starHint.adjacency`：已驗證只供 QA/self-check/debug，唔渲染，冇郁。
- **A42** `{playerName}`：runtime 恒 resolve 做「阿偉」，混用屬源碼層面，非玩家問題。

## 三、關海媚（C1）處理
Pack 原文 7 處出名 **冇改 pack**。線上靠清洗層短語規則喺 story 顯示欄位（speaker/cast/synopsis/beats lines）一律換「當紅花旦」，功能測試驗證零漏（speaker＋lines 實測）。index 內其餘「關海媚」出現全屬合法內部：QA 禁用詞自檢名單、speaker 註冊表 dev display、清洗表 match pattern。原生移植時按回寫清單回寫 pack 原文。

## 四、A34 佔位對白出街面評估（今次唔修，寫作工程）
- STUB slots pack C6–C17 每節一句「（Cn 對白待補）」：`freeplaySlotHasPlayableBeats` 要求至少一句非佔位先採用 slot beats → **佔位句本身唔會出街**（守衞實證）。
- 真正出街嘅係 main pack C6–C17 對白本身：屬未廣東話化嘅書面語 register（B3/D9），玩家由 C6 起會明顯感到語體斷層——呢個係寫作工程範圍，唔係字串替換可以了結，留待另案。

## 五、內容包回寫清單（原生移植時回寫 pack，唔好再靠清洗層）
1. 關海媚出名 7 處（story_detail_c1_to_c17.json C13：synopsis 1、cast 1、beats speaker ×2 等）改稱號。
2. A34/B3：C6–C17 對白廣東話化（連 slot 佔位句補寫）；B2 Vera pack 旁白轉述 51 句改直接對白。
3. B15 招牌句重複、B22 npc_lines_core 全檔回爐（今次只修最差 4 句）、B53 欄位語體統一。
4. A57 roleHint 紅星鄰接模板 42 則逐則寫、A58 通告 limits 逐則化（今次只換罐頭短語）、C28 通用通告加香港錨點、C29 跨年通告去重。
5. D2 方小龍線輩分稱謂（高俊傑→高師傅向）、D3 藍若曦成線正本（線上靠 ROMANCE_LAN_PA_OVERRIDES；pack R_lan_meet 原 synopsis 已被覆寫取代，B16 exact 已撤）、D4 R_tang_meet_stub 節點隔離、D7 tang/deng、hiu/choi 雙版本指定正本。
6. C4 `when` 欄三年制重排（結構欄位，今次只修 synopsis 年份前綴同 C17「四年」字眼）。
7. gigs_1991/1992 附錄 L1–L11：今次只靠通用規則部分覆蓋（虛構/政策句、era 標籤、口播→讀稿經 normalize 一併生效），第三人稱 synopsis 未逐則重寫。
8. 其餘零星：node 級 notes 欄內部註記可保留；slots pack 散用「電視城」做地點簡稱（今次只修「星河電視城」全名）；A52 heroAngle/diasporaHook 若將來啟用要先改寫。

## 六、驗證
- Repo tests：**42/42 PASS**（基線 40 套＋新增 `test_text55_logic.js`、`test_text55_static.py`；兩套新測對 v20a54 index 均 FAIL，反證成立）。
- TEXTFIX55 功能測試：對真 packs 行清洗——story notes 170/200 改寫、gigs 三年 126/248 改動、關鍵字（DEV/試玩閘/快閃/截圖/送命題/帶貨/喊麥/虛構/電視城/關海媚）喺清洗後顯示欄位零命中。
- index 原文 grep 分類：`[DEV]` 0；「試玩閘」只剩清洗表 match pattern ×3；時代詞只剩清洗表 pattern、內嵌 gig 原始數據（runtime 經 normalize 清洗）同 1 條 v54 開發註解；`softBehaviorGate` 只剩 code 識別字。
- `node --check` 兩 script block PASS。
- ⚠️ 推送注意：本版 4,303,107 bytes —— 已知 snapshot push 上限實測區間係 4.19MB 過／5.23MB 413，4.30MB 未實測；如遇 413，可考慮將 TEXTFIX55 對照表壓縮（去空格序列化）或分段推。
