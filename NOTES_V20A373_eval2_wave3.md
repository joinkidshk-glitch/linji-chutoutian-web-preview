# v20a373 — 第二輪評估第三波修正

對象：第二輪評估報告（`~/workspace/linji-playtest-eval2-2026-11-22/REPORT.md`，對象 v370）。
結論先行：第一輪阻斷級問題全部修好、冇 P0；第三波五項全部落地，suite 400 PASS／9 FAIL（基線，九項 pre-existing 不變）。

## 1. 結局門檻（resolveEnding410）

| 項 | 舊 | 新 | 理由 |
|---|---|---|---|
| E4 救回門檻 `e4RescueCredits` | 2 | **5** | 全脊骨被動故事債權恒 4 筆（endingFavor410 數 mockCredits 未 redeem 者），舊門檻 2 令全脊骨恒 rescued、真沉變體不可達。新門檻：被動 4 筆→真沉；真經營人情網 5+→沉唔死，兩變體皆可達。 |
| ID 信用窗上限 `idCreditHi` | 54 | **60** | 信用隨殺青上漂，W4 播種 50→55 穿上限落 E2。試過 65 會搶 E2 平衡 profile（weave410 三案 fame70/credit61 落 ID 而非 E2），收返 60。 |
| E3/E5 守門 | `credit>fame` | **`credit>=fame-10`** | 信用≈聲望嘅幕後／人情路線唔使刻意壓聲望。E3 另有 credit≥42＋幕後標籤／導演 rel 閘、E5 另有人情總量≥6＋何生 rel≥60 閘，唔會變免費結局。 |

唔郁：贏線 0.875、1992 年終評核 floor 140／warnLine 180、E1 雙軌門檻 350。

## 2. 成長曲線（CALIB60 遞減帶收緊上段）

方向：跟 GPT（技能衰減、門檻不變）；**唔採用** Claude 抬 E1 門檻 350→420 嘅方向——門檻係玩家可見目標，抬門檻等於拉長三年度嘅前段，衰減只壓後段膨脹，開局節奏不變。

| 帶 | 舊 | 新 |
|---|---|---|
| FAME | `[[15,1],[28,0.30],[50,0.22],[85,0.17],[140,0.14],[230,0.12],[∞,0.10]]` | `[[15,1],[28,0.30],[50,0.22],[85,0.15],[140,0.11],[230,0.09],[∞,0.07]]` |
| ATTR | `[[28,1],[55,0.36],[110,0.25],[190,0.19],[∞,0.14]]` | `[[28,1],[55,0.36],[110,0.20],[190,0.13],[∞,0.08]]` |

開局帶（FAME <50、ATTR <55）不變，只壓後段。test_calib60_logic 已 resync（含雙軌回放模擬段）ALL PASS。

## 3. 黑剪影過渡卡

五位新星（胡美琳、韓秀婷等）冇美術，巧遇候補鏈跌到黑橢圓＋梯形 SVG。新增 `enc373CardSrc(sid)`：藝員資料卡 SVG data URI（米紙 #F3E8D0、墨 #342D26、框 #786A57、空相框＋四角相片角貼、姓名 32px），用 `starName252Of`，無名回 ""。`enc79StandCandidates` 喺黑剪影兜底之前 push 卡（候補最尾仍係 ENC105_STAND_FALLBACK）；`__dlg106Err` 非影角色候補走盡改出卡（dataset.enc373card 守衛）唔再隱藏。實物截圖：`~/workspace/linji-drive373/03_card_wu.png`。美術票仍排隊，卡係過渡。

## 4. 地圖標籤／觸控（先諮詢 GPT-6.2-sol，原稿 `~/workspace/linji-drive373/gpt_ui_reply.txt`）

- 「可打聽」由 pin 浮動徽章（`.plab-ask369`，壓住星河電視台標籤）改入紙標籤第二行：金龍茶餐廳／何生事務所兩個 `.mn68` div 加 `mn68-ask373` class，CSS `::after` 出「可打聽」（block、10.5px、墨綠 #36564B）。標籤文字保持純地名（textContent 唔污染，deCollide 照常）。
- 約會層冇玩家標記：`mapMe363` 喺 pinPos 冇 atLoc 時改出頂部紙頁眉 `.map-here373`「目前所在：X」（像素人 24px 行首、min-height 44px、pointer-events none）。
- 觸控：`#home-subtabs .home-tab` min-height 36→44＋min-width 44px；plan 組手寫 tab 加 min 44×44＋inline-flex 置中；`.debt-repay-btn` min-height 36→44；`.pane-go72` 加 min-height 44px。

實駕驗證（drive373）：片場層 17 pin／17 標籤／重疊 0；約會層 8 標籤／重疊 0＋頁眉「目前所在：阿偉屋企」高 44px；手帳子 tab 實測 55×44／44×44。約會層頁眉左緣輕壓「廟街禮品」標籤右邊，文字仍可讀，屬已知小重疊。

## 5. 徐寶珊 meet P3→P2

`content/story_detail_romance_lan_xu.json`：R_xu_meet P3→P2（openConditions phase_P3→phase_P2）、R_xu_push1 P3→P2、R_xu_push2 P4→P3；crisis P4／ending P5 不變，同蘇芷茵線（v372）同等鏡像。HE/BE＋排他鎖不變。

## 測試釘 resync

- 行號釘：`qa373/resync373.py`（difflib 單次掃描 dict 查表、逐行核實內容逐字相同＝純漂移先改，base c381a4b，index.html 48288→48355 行）。
- mn68 標籤 regex 容許額外 class：costume265／map97／ui137／ux68／ui142；awards207 count 改前綴。
- calib60/weave410/sideline280/p361 數值釘跟新門檻 resync。
- 佔位卡函數驗證：`~/workspace/linji-drive373/card373_check.js` ALL PASS（11 項）。
