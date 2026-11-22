# v380：第五輪評估修正（P1 兩項＋P2 七項）

基線：v379（`7e2c1da`，suite 400/9）。第五輪報告：`~/workspace/linji-playtest-eval5-2026-11-22/REPORT.md`。逐項對 live code 核實後實裝，suite 返 400 PASS／9 FAIL（九項 pre-existing 不變）。index.html 淨 +33 行。

## P1

1. **蘇芷茵 crisis BE 旗入 CMT 閘**：`commit48Available` 補 `flag_so_played_safe` 檢查，同葉 `flag_yip_be_route` 對稱。BE 後唔再出 commit offer，唔可繞道 commit。
2. **葉／蘇感情層送禮＋傾談入口**：跟 v176 藍／徐同一套 plumbing——NPCS 補 yip／so 條目（homes 跟 meet 地點：葉星河電視台、蘇灣仔唱片／中環廣告）、ROM159_WOMEN npcId 補返、ROM176_WOMEN 補兩位巧遇（主場葉 tvb_longmen、蘇 rec_wanchai）＋GREET／TEA 風聲句、NL176 補傾談對白（greet/chat/advice/intel/pressure 各 2 句，廣東話對白）、PORTRAITS 補 npc_yip／npc_so（fullbody base 圖）。送禮偏好 rom159ApplyGiftOverrides 已有（最愛卡帶＋咖啡豆／拍紙簿），巧遇設 gift_met 旗開閘，rel 靠送禮＋約會＋劇情。

## P2

3. **meet 閘**：葉 `R_yip_meet` openConditions 補 `N8`（設計明文掛 N8 選美後台）。徐／蘇核實後保留 phase_P2：v372／v373 刻意降 P2（休閒打法 550 日只到 P2，P3 閘令成條線開唔到），`when` 係顯示文字唔係硬閘，唔加 weekMin 倒退。
4. **dev 用語清掃**：葉 crisis 兩選項、葉／蘇 ending HE/BE 選項、蘇 crisis 兩選項、藍／徐 ending HE 選項嘅 `notes`（玩家面副文案）改寫做玩家面書面語，刪「HE 路線／BE 路線／flag_…／rom159PrepareNode／push1」等開發字眼；蘇層級閘變體 notes 改「她還沒有把你放在眼內……」。
5. **巧遇「約佢出街」掣**：舊版只 call `rom159DateGate` 丟棄結果，改 `rom159OpenDatePicker`（內含閘檢查＋原因 toast）。
6. **桌面側欄＋標題 tip 舊文案**：「傾談／送禮不計日子」→「耗用一日」；開始畫面 tip 同步改準；紅星送禮結果 modal 改動態跟 `softSocialCostsDay()`（live 耗一日）。
7. **壓力休息被拍攝填位蓋過**：`lockShootsIntoDraft` 跳過 `rest` 位，預設計劃壓力休息唔再被拍攝填走（拍攝順延，限期壓力照舊）。
8. **E1 場景對比**（GPT-6.2-sol 先諮詢，原稿 `~/workspace/linji-drive380/gpt_e1_contrast.txt`）：結局頭兩頁（正常＋強制收場兩路）內容包入 `.ending410-scene` 實色米紙底（#f2ebd8／深墨 #33241C／金邊 #a88443，對比約 12.5:1），唔改轉頁流程；原生版對應 Color Assets。
9. **靜態 pack N17_410_b notes**：同步 v379 動態版「此選擇不可逆轉，結局會按退圈計算。」；wf1_80 fixture 同步一處（v354 先例）。

## Resync

行號釘 difflib 映射（`qa380/resync380.py`）：rom159（6 釘＋全佳行＋npcId 斷言更新）、rom176（6 釘）、tang152（2 釘）、tang171／tang173／gift185（總行數 48823→48856、openLoc 43985→44018、tang173 lines[5207]→[5212]）、travel114（清單＋DEF/WRAPPER，含 4 位數條目）、text125（三錨 ls 索引）、text55（A6 文案）、story157（nodes[5:] sha 重算——git diff 核實只 N17_410_b notes 一行變）、r342（種子補 N8 done，意圖不變）。

## 未郁

SAVE key／softRev／產品 `?v=`／贏線 0.875／floor 140／warnLine 180／E1 門檻 350 全部不變。冇改 MEMORY.md。
