# NOTES_V20A215 — 推出日提及（細票）

分支 `v20a215`，基底 main `eed04dc`（v212）。hold 分支，唔落地、唔 push。
落地次序（最新 MEMORY）：v213 → v214 → v215（v209 已上線，index.html 唔郁，唔影響呢票）。

## 1. 做咗乜

玩家已殺青嘅**臨記級**通告，喺推出季首日朝早晨報出一則短訊（作品名＋播出資訊，唔點名玩家，fameDelta 0），併入現有晨報合併／排序／短訊機制，唔出獨立一份報。

新 code（`index.html`，淨 +140 行）：
- `release215ReleaseDay(year, season)`：季首日換算（春 3/1、夏 6/1、秋 9/1、冬 12/1），day 0＝1990-01-01，`Date.UTC` 差值計，閏年自動啱（1992 春＝790）。
- `release215LookupGig(gigId)`：先 `GIGS`，再 `STORY_WIRE.gigsByYear` 跨年搵（池換咗都搵到）。
- `release215CopyFor(entry, gig)`：文案（見 §3）。
- `release215EnqueueDue()`：掃 `wrapHistory`，合條件就 `enqueueNewspaperItem`（去重 key `release:<gigId>`）。
- `enqueueNewspaperItem`：source 正規化加 `"release"`（見 §4）。
- `buildNewspaperEdition`：排序加 release 排最後（見 §4）。
- 掛點二處（冪等，去重守住）：`advanceDay()` tick（跟 `news82Tick` 同位，live 主路徑）＋ `pullDueNewspaperEdition()` 開頭懶掃（載入／播種存檔直接跳到推出日嗰陣，`advanceDay` 未行過；喺計到期／分批之前行，保證入隊先過出報）。

## 2. 觸發規則

- 對象：`press94RoleClass == "base"`（臨記級）。配角級以上已有殺青報，唔入呢票。分類經 `press94IsBaseRole(gig, labelHint)`，labelHint＝`wrapHistory` 嘅 roleLabel＋title；gig 搵唔到嗰陣只靠 labelHint 判。
- 觸發日：`releaseDay ＝ gig 年＋季嘅首日`。gig 年份係**遊戲年**（載入嗰陣 `years66`＋2 已 remap：1988→1990；`wrapHistory` 存嘅就係遊戲年）。舊曆遺留值（1988／1989 未 remap）喺 `release215GameYear` 補 +2；1990–1994 照用。
- 條件：`wrappedDay < releaseDay`（推出日**之前**殺青；當日／之後先殺青唔補出）＋ `releaseDay <= 今日`（未到唔出；逾期載入照出，publishDay 照寫推出日，跟其他逾期報同一做法）。
- 去重：`newspaperEventSeen("release:<gigId>")`（queue／剪報／待出三處），一張通告永遠只提一次。`release:` key 唔行 `wrap:` 嗰套 per-gig 去重，exact key 已夠（同一 gigId 永遠同一 key）。
- 入隊慣例跟 award／wrap：`enqueuedDay = publishDay - 1`。呢點係 (e) 合併嘅關鍵：`pullDue` 只取最早 `enqueuedDay` 嗰批，同日到期嘅獎項報（典禮日入隊、翌日朝出）先至可以同一批合併。
- (e) 嘅準確語義：獎項報係**典禮翌日**朝出，推出短訊係**推出日**朝出。兩則併一份報嘅情況＝兩者**同一朝到期**（典禮日＝推出日−1，例如典禮 5/31、推出 6/1）。如果典禮日正正係推出日，兩份報分兩朝出（各朝一份，唔會同一朝出兩份）——機制上已經啱，實駕 (e) 驗嘅係同一朝到期嗰個情況。

## 3. 文案決定

- 季節寫法，**唔逐字印 `releaseLabel`**：賀歲檔 label 話農曆新年 1–2 月，季首日係 3 月 1 號，逐字印會對撞。`release215CopyFor`／`release215EnqueueDue` 成段唔讀 `releaseLabel`（static 測試釘死）。
- 格式：headline `《作品》春季推出`（動詞按媒介：電影→上映、電視劇／綜藝→播出、其餘→推出）；dek 同句＋播出資訊尾句（電影「院線排片陸續公佈。」／電視「電視台黃金時段播出。」／廣告「廣告時段陸續出街。」／唱片「唱片舖陸續上架。」／其餘「檔期陸續公佈。」）。
- 書面語；唔點名玩家（headline／dek 零人名，全名規則唔觸發）；作品名經 `postShootDisplayTitle`（workTitle 優先）。
- `paperName "娛樂版"`，`clipLabel "娛樂版・推出"`（唔寫「殺青」，唔扮殺青報）；`rumorEcho ""`（短訊照舊經 `pushNewspaperRumor` 變「報紙都寫了」，同 wrap 短訊同一待遇，唔係新污染）。

## 4. source 決定

- 查過 `buildNewspaperEdition`／排序先定：加一個新 source `"release"`，唔用現有 source。原因：
  - 用 `"wrap"` 會扮殺青報（edition.source／clipLabel 語義撈亂，v214  cut 咗 base 殺青報之後更加唔啱）。
  - 用 `"award"`／`"story"`／`"world"` 會搶排序／觸發其他語義（world 有 paras／imgKey／頭版優先）。
- `enqueueNewspaperItem` 正規化白名單加 `"release"`；`buildNewspaperEdition` 排序加一級：release 永遠排最後（world → |fameDelta| → award → release）。淨係得佢嗰陣先做頭版（成份報得呢則，唔係搶頭條）。

## 5. wrapHistory 90 條上限核實（夠冚）

- 提及只可能喺殺青後約 90 日內：通告提早窗 60 日（`GIG_SEASON_LEAD88 = 60`，季首日前 60 日已上板）＋拍攝期（shootDaysHint 最大 29 日）＋接單延遲。殺青日同推出日必屬同一曆年（季首日喺 gig 嗰年內，殺青早過推出日），查 gig 嗰陣 `GIGS` 未換池。
- v20a147 D4 已核：arcN 單年最多 79 部、任何 365 日窗口最多 79 部；90 日窗口內最多約 20 部，遠低過 90 條上限。唔使搵 `isGigConsumed` 等更耐久紀錄。
- 局限（寫明）：v147 之前舊檔 wrapHistory 截到 30 條，被截走嘅歷史救唔返——嗰啲通告唔會有推出提及。新殺青先累積到 90。

## 6. 唔郁

v214 嘅 code（基底未落地，落地嗰陣先 rebase 對一次）、典禮流程、殺青報紙（`enqueueNewspaperFromWrap` 原封不動）、v213 改動、見報門檻、聲望幅度、剪報上限 40、SAVE key（`starVolunteer_map_v19w`）、softRev（`s107`）、產品 `?v=`、content pack JSON（零個新欄位；通告得 `year`＋`season`）。

**注意**：呢個基底 v214 未落地，base 級殺青報紙仲喺度。release 提及係另一則、另一日，唔同殺青報撈亂；v214 落地 cut 咗 base 殺青報之後，release 提及就係 base 通告唯一嘅報紙提及——code 唔依賴殺青報紙存在（只讀 `wrapHistory`＋gig 紀錄）。

## 7. 逐張準確推出日（留返以後）

呢票只用季首日（`year`＋`season`）。逐張準確推出日數據等劇本定稿＋通告重設計嗰陣一併加，嗰陣再將觸發日由季首日改做準確日（`release215ReleaseDay` 係單一換算點）。

## 8. 測試

- 新測試：`tests/test_release215_logic.js`（23 斷言）＋`tests/test_release215_static.py`（26 斷言），全部 ALL PASS。
- 反證（對 pristine `eed04dc`）：logic exit 1／23 FAIL、static exit 1／21 FAIL（static 其餘 5 項係「唔郁」不變量，pristine 照 PASS，係預期），乾淨 FAIL，唔 crash。
- 全套 `qa131/run_suite.sh`：pristine 基線（工作副本 `stash -u` 還原實測）296／13；工作版 298／13——FAIL 清單逐項相同（13 項穩定 pre-existing FAIL），＋2 係新測試，零回歸。
- 釘位 resync（`qa215/resync215.py`＋`qa215/apply_resync215.py`＋`qa215/resync215_map.json`）：呢票淨 +140 行，令 7 個靜態測試漂移——`test_gift185／test_poster85／test_rom176／test_tang171／test_tang173／test_travel114／test_ux68`。全部經 difflib 對位核實內容逐字相同（純漂移），按慣例更新（總行數 61795→61935、DEF 56267→56407、WRAPPER 45188→45190、主檔上限 5,488,954→5,495,117＋40,000／5,490,000→5,540,000）。附帶修正：tang171／173 DEF 名公式漏咗 v211 +42（真 DEF 喺 56267 唔係名寫嘅 56225），呢次補返。resync 後 7 檔逐個直接跑全部 PASS，全套重跑 298／13。

## 9. 實駕（`qa215/drive215.py`，本地鏡像，live 模式，0 pageerror，4/4 PASS）

播種：`new_game` 後直接寫 localStorage（slot 1，prefs 指去 1），reload → 撳「繼續」→ 晨鏈。播種標 C1 已完成（真玩家到推出日一早做完開局）＋頒獎旗全 done（唔畀請柬搶晨鏈）。

- **(a) `a_release_spring` PASS（12/12）**：臨記廣告 `gig_1988_entry_ad_passerby`（《便利店短片》，春），wrappedDay 30 → 1990/3/1 朝早晨報即出：報頭「娛樂版」、日期 1990/3/1、欄目「娛樂版・推出」、頭條《便利店短片》春季推出、dek「《便利店短片》春季推出，廣告時段陸續出街。」、聲望未有變動；收報後聲望仲係 5、剪報 1 張（eventKeys 有 `release:gig_1988_entry_ad_passerby`）、queue 清空。截圖目視確認係完整報紙實物（`qa215/shots215/a_release_spring_paper.png`）。
- **(b) `b_named_no` PASS（6/6）**：配角級 `gig_1988_rec_02`（《海傍情話》男主角，夏），wrappedDay 100 → 151 日朝早冇晨報（queue 空、剪報 0 張）。
- **(c) `c_wrapped_on_day` PASS（6/6）**：同一臨記廣告，wrappedDay 59（＝推出日當日）→ 59 日朝早冇晨報（queue 空、剪報 0 張）。
- **(d) 接 (a) PASS**：過一日（day 60）再睇，冇第二份報（queue 空、剪報仲係 1 張）。
- **(e) `e_merge_award` PASS（12/12）**：臨記電影 `gig_1988_film_02`（《孤劍破陣》，夏，wrappedDay 100）＋獎項報同一朝到期（enqueuedDay 150、publishDay 151）→ **併一份報**：頭條「頒獎見報」（娛樂快報・頒獎夜），短訊《孤劍破陣》夏季上映（dek「《孤劍破陣》夏季上映，院線排片陸續公佈。」），聲望 +2（5→7，淨計獎項），剪報只得 1 張（eventKeys 兩則齊），queue 清空。
- 判定說明：(b)(c)(d) 嗰陣晨鏈行完報紙環（無嘢出）之後去到強制播 C2（「第 2 幕：留人脈／趕通告」），係播種存檔主線落後嘅正常行為，唔係報紙；所以「冇報紙」用「有冇『收下這份剪報』掣」＋queue／剪報數字判，唔係用「有冇任何 modal」判。
- 證據：`qa215/drive215.json`（逐場 checks＋state）、截圖 5 張（`qa215/shots215/`）。

## 10. rebase 上 v214 嘅預期衝突區（落地嗰陣對）

- `buildNewspaperEdition`：v214 報紙升級版式（v11）好可能重構 shorts／head 段，我加嘅 release 排序級要保留喺新排序尾。
- `enqueueNewspaperItem`：v214 可能加欄位／改 source 處理，我加嘅 `"release"` 白名單要保留。
- `pullDueNewspaperEdition`／`enqueueNewspaperFromAward` 附近：v214 改頒獎結果卡做報紙公佈＋cut base 殺青報；我嘅 release block 錨喺 `enqueueNewspaperFromAward` 之後，`pullDue` 懶掃行要保留。
- `advanceDay`：v214 唔預期掂呢度（冇衝突預期）。
- 測試釘位：v214 落地自帶 resync 會再移行號／上限，我嘅 resync 數字係對 `eed04dc`，rebase 後要按新基底重跑 `qa215/resync215.py` 核實。
- `tests/test_press94_static.py` 等 press94 測試：v214 改殺青報邏輯可能郁到，我嘅 release 測試唔依賴殺青報，但要重跑確認。

## 11. Rebase 上 v214（`7e27e1a`）紀錄（落地統籌，2026-11-14）

- 分支 rebase 後 HEAD `d575f28`（實作 `5abb7c9`＋實駕 `9615958`＋S16 更新 `d575f28`）。
- `git rebase origin/main` 第一轉停咗（todo 重複 pick，v153 教訓：直接 `--continue`）；第二轉 7 個內容衝突，**全部係靜態測試行數 resync**，`index.html` 自動合併零衝突。
- difflib 對位（HEAD `7e27e1a` → 合併版）：v215 插入點 tick＋2／whitelist＋1／RELEASE215 block＋130／排序＋4／pullDue 懶掃＋3＝＋140 行；總行數 62,352→**62,492**，體積 5,524,996→**5,532,430** bytes。
- 合併版語義核實（逐段睇過）：whitelist v214 `world`＋v215 `release` 兩邊齊；排序 award 優先之後 release 排最後；pullDue 懶掃喺函數開頭、計到期之前；advanceDay tick 緊貼 `news82Tick` 之後；`renderMorningPaperHtml`／`np214ShowPage` 等 v214 渲染器原封不動（19 命中）。
- Resync 腳本 `qa215/resolve_rebase215.py`：difflib 映射＋每個錨點逐行內容核實（rom176 31903 唔郁、55254→55394、55622→55762、56761→56901、56855→56995；travel114 COUNT 12／FREE 33 全數映射＋內容核實；DEF 56824→56964、WRAPPER 45390→45392）。附帶修咗腳本一隻 bug：replacement 漏咗尾換行，黏住咗三檔下一行（poster85／ux68／tang173 語法錯），補返換行後三檔重跑全綠。
- **S16（`tests/test_newspaper214_wrap_static.py`）**：v214 測試釘死「無 release 機制」（`source: "release"`／`releaseDay` 唔准出現），v215 正正落地呢個機制——第一輪全套 A/B 唯一差異就係 S16 FAIL。唔係回歸：已更新 S16 改釘 v215 規格（`source: "release"`＋`release215ReleaseDay`＋`release215EnqueueDue`＋`"release:"+String(entry.gigId)` 四樣齊），工作版 PASS。
- 新測試：logic 25＋static 28 全綠。反證（pristine `7e27e1a`，新測試抄過去跑）：logic 23 FAIL、static 19 FAIL，乾淨 FAIL 唔 crash；static 其餘 9 項 PASS 係「唔郁」不變量／空真（季節詞表、唔讀 releaseLabel、季首日對照表）。
- 全套 A/B（乾淨 pristine）：**305／13 vs 307／13，FAIL 清單完全相同**（13 項穩定 pre-existing FAIL），＋2 係新測試，零回歸。注意：第一輪 A/B pristine 嗰邊混入咗反證嗰陣抄過去嘅兩檔新測試（305／15 vs 306／14），基線唔乾淨，已清走重跑。
- 實駕重跑（rebase 後，`qa215/drive215.py`）：**4/4 PASS，0 pageerror**。初跑 (e) 兩項 FAIL（`headline_present`、`head_is_award`）——唔係機制錯：合併本身啱（一份剪報、兩則 key 齊、聲望 +2）；係 v214 分頁報紙將短訊放第二版（`SECTION.np214-page`，`display:none`），`modal_info` 嘅 innerText 只見第一版。Probe（`qa215/probe_e.py`）核實短訊喺全版 HTML 入面、第二版可見；drive 已更新（headline 睇埋全版 textContent＋記低邊一版＋短訊喺第二版嗰陣撳過去核實可見＋截圖），重跑 4/4 PASS（(e) `headline_page: 2`、`headline_visible_p2: true`）。第二版截圖目視確認：同版短訊頭條就係《孤劍破陣》夏季上映。
