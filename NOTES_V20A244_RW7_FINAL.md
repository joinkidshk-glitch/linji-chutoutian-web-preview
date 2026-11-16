# v20a244：RW-7 全本收尾（語言重寫最後一批）

- Base：main `076382f`（v243）。分支 rw7（統籌合併 rw7a／rw7b／rw7d）→ squash merge 落 main。
- Suite：**314／10**，FAIL 清單同基線已知 10 項完全一致（flash51／rumor49／slot50／soft_tip_111_restore／start53／weave43／weave44／weave49／wf5_87／wrap38），零回歸。inline script `vm.Script` 編譯 2/2；改動 JSON 逐檔 `python3 -m json.tool` 有效。

## 改咗咩

### A. TEXTFIX 層死碼刪除（工人 A，分支 rw7a）
- TEXTFIX55_EXACT 58 → **46**（刪 12：NP214 6 條 stub 舊字串＋鄧麗萍未載入檔 5 條＋DS filter 表 1 條）。
- TEXTFIX55_NOTE_EXACT 9 → **6**（刪 #1／#8／#9，未載入檔＋無釘死）。
- TEXTFIX57_EXACT 8 → **6**（刪 #2／#4；RW-5 話「4 條死映射」核實係 4 條 0-live，但 #1／#3 有測試釘死，實際可刪只得 2 條）。
- TEXTFIX55_PHRASES 14 → **6 對**（刪 8：連軸綵排／資本場合／資本場／粉絲／社交課／智商課／製作日／阿偉們之間；粉絲源頭 protagonist.json 經核實未載入）。
- 刪 `textfix55DropSents`／`textfix55GigField`／`textfix55GigRecord`＋`normalizeGigRecord` 呼叫點＋`TEXTFIX57_GIG_REQ` 13 條（gigs_new.json 逐項命中數全部 0）。
- 刪 `content/STUB_AWARDS_CEREMONY_v1.json` categories 區塊 80 行（v240 話「36 處」，實為 80 行；AWARDS188_CATEGORIES 本體唔郁）。
- index.html 44,453 → 44,384 行（淨 −69）。留低嘅全部有測試釘死（EXACT #1／#9／#10／#12／#14／#15／#57、NOTE #4–#7、57 #1／#3、57_PHRASES 3 條）或仲有 live 源頭；RUMORS 16 條／STAR_LOOKS 10 條一字未郁（注入用 live 語料，唔係死碼）。
- 偏差：EXACT #2 初版刪錯（只用全 key 搜 tests，漏咗 test_tang152 用 value＋key 片段釘死），第一輪 suite 309／15 捉到，已還原，之後逐條用片段＋value 再 grep 確認無同類漏網。
- 測試更新 7 檔＋resync 5 檔（difflib 對位 74 處釘行，內容逐字核實純漂移）。

### B. live 文字重寫（工人 B，分支 rw7b）
- N17 beats 揀格文案：指定 3 拍之外再掃到多 3 拍有揀格寫法，一併改埋（共 6 拍：3／6／9／13／14／15，1-indexed）；「六個意向／鎖一個／圈那一格／隔壁那格／由頭跳到尾」全文 0 命中；choices／flags／stats 一行未郁。beat 4 假設性忠告保留；beat 12 本身已係 v235 口徑。
- WF5 choi／hiu 變體（`WF5_VARIANT_OVERRIDES87`，R_hiu_meet＋R_choi_meet，34 句）：改 10 句（普通話殼旁白／敘述），保留 24 句（對白本身已係輕口語）；結構不變量（beat 數／speaker／行數／choices）唔郁；`test_wf5_87_logic` 52/0。
- N5 裸「采兒」24 處 →「周采兒」（title／synopsis／playerHint／lockedHint／beats／choices notes／resultBeats）；保留 2 處（阿偉內心獨白＋第一身手帳，佢自己嗌「采兒」）。
- cast_main.json 2 處簡體「周刊」→「週刊」（tests 無釘死；三檔測試加 `_v244_allowed` 豁免，按 v239／v241 舊例）。
- casting `labelToId` 3 鍵同步（跟場熟手／星味／動作好手，`content/STUB_CASTING_TAGS_v1.json`）；其餘 7 鍵核實同步唔郁。載入模擬 post-walk 鍵集合＝label 集合 10/10。
- 附註：舊存檔遷移 `ensureCastingTagsState` 仍將舊值轉做「身手好／耍大牌」（唔係任何 live label；該路徑已無內容寫入者，只影響極舊存檔顯示名）——邏輯層改動，超出今票範圍，未郁。

### C. 試讀 17 句＋簡體漏網（工人 D，分支 rw7d；統籌合併嗰陣補 2 處）
- 簡體漏網 live 4 處：勉强→勉強（L35626）、以后→以後 ×2（L35107／35148）、看着→看著 ×2（L32266；L32274 同款一併改）。
- 試讀 17 句修復 16 項（N4／N17／N16／N5／N15 synopsis、LAN nodes[10] 刪開發備註句、VERA nodes[13]／[0]、報紙 wrap_success[8]／story_mixed[5]、stub 廣告賞 inviteDek、gigs[236]／[195]／[147]／[22]、events AUD_STRESS70）；再試讀 20／20 一次讀順。
- 統籌合併補漏：L6492（N3 playerHint）＋L12611（選角筆記）兩處「看着」→「看著」（同類漏網，行數中性）。「看着」全檔 0 殘留；「勉强」剩 L4936 開發註解一行（唔係玩家面）。
- 偏差：首次 suite 312／12（story157 index／pack 內容釘死），已 resync（期望值＋sha 重算；N6F 鏡像同步）；B15 舊句喺 gigs_new.json 出現 3 次，只精準改 gigs[22]，[43]／[62] 保留。

### D. DS filter 核實（工人 C，唯讀；唔刪，等拍板）
- 死碼確認：同一批 66 條存咗兩份（`DS_PLAYER_ZH_FILTER_TABLE_v1.json` 機表＋`_ds_filter_ui_corpus_v1.json` 語料，id 集合 66／66 相同）；index.html／tests 0 命中；34 個已載入 content JSON 入面無佢；唯一 live 痕跡係 `tutorial_zh_HK.json:4` 嘅 `source` 欄位（無程式讀取，唔顯示）。
- 刪走只需刪兩個檔（＋兩份文件可一併刪），index.html／tests／loader 一行唔使郁。風險：失去唯一一份 66 條 before→after 決策記錄；live 仲有 3 處「通告板」（index.html L23169／26333／26390）同表規則打架，要另定去留。
- DS filter 去留等用戶拍板，今票唔郁。

## 掃描殘留（工人 C，全本最後一掃；等拍板，今票唔郁）
- TEXTFIX 死映射：EXACT 死 13＋僅未載入 6（A 刪咗 12，留低嘅有測試釘死）、NOTE_EXACT 死 4（A 刪 3，#5／#6 釘死屬虛但家長明示留）、PHRASES 死 7（A 刪 8，連粉絲）、57_EXACT 死 4（A 刪 2，#1／#3 釘死）、57_GIG_REQ 全死 13（A 全刪）、57_PHRASES 實質死 3（測試釘死，留返）。
- 廣東話標記：content JSON 1,050 條命中，合法（對白／引號內／內心獨白／開發欄位）＋疑似漏網 18 條（MOCK_UI_PHASE3 silhouetteDesc／distanceLine／rumorTeaser ×12、SANDBOX redStarHook ×2、SCHEMA_AWARDS 類別 label ×1、LAN 括號舞台指示 ×3）；index.html 結局文案 188 句全廣東話旁白（最大簇，唔喺 RW 範圍）、頒獎 gallery 43 次、打聽／情報旁白部分。
- 簡體漏網：live 4 處已修（見 C）；「着」vs「著」：旁白／描述內「着」疑似漏網 52 次（等拍板）；L10666 speaker 對照表 dormant 簡體鍵「周刊編輯」留返（刪行會拖垮釘行測試，唔值得）。
- hiu setting「電視台廠景外的休息角」留返（mock pack sha 釘死；覆寫表加 setting 要 +1 行，會拖垮 5 檔釘行 resync，為一個詞唔值得）。

## 等拍板（RW-7 之外，另開票）
1. DS filter 刪唔刪（兩檔＋兩份文件）。
2. 結局文案 188 句全廣東話旁白：開票成段轉書面（RW-8 範圍）定接受結局用廣東話旁白做風格。
3. 旁白 52 處「着」轉唔轉「著」；描述類（STAR_LOOKS／silhouetteDesc／STAR_SIGHTINGS）用「着住／喺」係咪接受。
4. 描述類廣東話（MOCK_UI_PHASE3 12 條＋gallery 43 次＋情報旁白）：接受定一律書面。
5. 「通告板」3 處 live 殘留：跟 DS 表改「通告欄」定接受做實物名詞保留。
6. `ensureCastingTagsState` 舊存檔遷移「身手好／耍大牌」埋尾（邏輯層）。

## 驗收
- 統籌親跑全套 suite（合併後分支）：**314／10**，FAIL 清單同基線一致。
- 50 句試讀：初讀停低 17 句，修復後 20／20 一次讀順（17 句修復＋3 處簡體再讀）。
- Live 實駕押後（瀏覽器死）：N17 新 beats、藍若曦線、頒獎報紙畫面實玩確認未做。
