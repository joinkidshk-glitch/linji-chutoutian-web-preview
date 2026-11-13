# NOTES_V20A166 — 頒獎禮 glamour 並置＋空字幕框隱藏（v160 review B1／C1／C2）

- 分支 `v20a166`，基底 main `276ffa1`（v160 NOTES；遊戲 commit `109422b`）。
- 範圍：用戶 2026-11-13 09:48 拍板修 v160 review B1＋C1＋C2。v147 B1／B2（v149 處理中）、獎盃 glyph、掌聲 MP3、典禮其他 beats／贏全長／音頻觸發邏輯一律唔郁。
- `index.html` 淨改 7 行（＋7／−7），總行數 58884 不變——刻意零淨增，`test_kwan151_static.py`／`test_tang152_static.py`／`test_travel114_static.py` 釘行唔使 resync。

## B1 — glamour 海報縮細並置（修法：用戶揀嘅三揀一第 1 項）

### 問題（v160 review 實測）
glamour beat 燕尾服 canvas 繪製 14 次，但 `.awd63-glamour` overlay（`rgba(10,6,18,.93)` 全幅＋海報置中）冚住成個 frame；`elementFromPoint` 喺燕尾服位置命中海報 `<img>`。

### 佈局決定
- overlay 由 stage 全幅（`inset:0`）改做**只冚 canvas**：搬入 `.awd62-frame`（canvas 之後、skip 掣之前），`position:absolute;top:0;left:0;width:100%;aspect-ratio:424/240`，對齊 canvas。`z-index:2` 不變（skip 掣 z-index 3 照喺上面），`pointer-events:none`（撳掣／撳畫面快進／`elementFromPoint` 照通 canvas）。
- overlay 本身**唔再有暗底**，左邊透明（canvas 照見），右邊 44% 係暗 panel（`.awd63-glamour-panel`，`flex:0 0 44%`，暗底 `rgba(10,6,18,.93)` 搬咗入去——0.93 暗層係 glamour 造型一部分，留喺 panel，唔成個拎走）。panel 係 column：海報上、cap 下。
- 海報縮細：舊 `max-height:60vh／max-width:min(76vw,330px)` → 新 `max-width:88%／max-height:60%`（panel 內），金框＋光暈保留。
- 幾何安全邊際：燕尾服 4 slots 時 cx=166、dispH 64 → 右緣 (166+32)/424＝46.7%；3 slots 時 cx=202 → 右緣 55.2%；panel 左緣 56%——兩個情況都唔掂。海報 img 左緣實測 58% 之後（見下），再闊一截。
- reveal beat 唔郁（嗰邊燕尾服本身睇到）。walkup 層唔郁（仲喺 stage 尾段全幅）。

### 前後量度（實駕，viewport 430×932／430×700，frame 闊同為 406px）
| 項目 | 修前（v160 review） | 修後 v166（932／700 一致） |
|---|---|---|
| 燕尾服位置／尺寸（屏幕） | 框 x140–201、y378–440（932） | 同左（932）；700：x140–201、y262–324 |
| `elementFromPoint` 燕尾服中心 | `IMG`（海報） | `CANVAS`（5 點探針：中心＋上／下／左／右四分位全部 `CANVAS`） |
| 海報位置／尺寸（屏幕） | 全幅置中，~330px 闊 | x268–389、y248–374（932）；x268–389、y132–258（700）；121×126px，complete，600×627 |
| 海報—燕尾服重疊 | 全幅冚住 | 0 px²；panel—燕尾服重疊亦 0 px²；燕尾服右緣 x202 → panel 左緣 x239（37px 罅）→ 海報左緣 x268（66px 罅） |
| glamour overlay 框 | 全 viewport | 406×230，對齊 canvas 406×233——3px 差額只係 canvas 4px 底 border（overlay 冚晒 canvas 內容區） |
| glamour cap | 海報下金字 | 照見（「□ 得獎／影壇新面孔（臨記組）：《幻彩舞影》」；□ 係 headless 欠 emoji 字體，已知唔係問題） |
| 燕尾服繪製次數（glamour beat） | 14 | 14（932 兩次實駕：14／14；reveal 17，唔變） |

- 肉眼確認：`qa166/shots/won_932_beat_glamour.png`、`won_700_beat_glamour.png`——左邊會場＋燕尾服企紅地毯（黑燕尾服＋白恤衫，細但讀得清），右邊暗 panel 海報＋cap，兩樣並置，零重疊。

## C1 — caption 為空嗰陣隱藏字幕框

- 機制：`setCaption` 單一 choke point（`awards62PlayCeremony` 內，全部 beats 經 `applyBeatCaption` → `setCaption`）。改做 `capEl.innerHTML = html` 之後按 `textContent.trim()` 切換 `style.display`：空 → `none`，有字 → `""`。一行改，行數不變。
- 空 caption beats（實測 display＝`none`）：`walkup`、`glamour`、won／nominated `out`（`out` 500ms，poll 判唔到 beat id，log 喺 `?`，display 亦係 `none`）。
- 有字 beats（實測 display＝`block`）：`open`、`enter`、`names`（`lines` 填字，唔係空 caption）、`suspense`、`reveal`、`comfort`；gallery `out` 有字（「掌聲響起——今晚完滿落幕。」）照顯示——gallery 分支唔行 won-out，唔受影響。
- 肉眼確認：walkup／glamour 截圖 canvas 下直接係卡片列＋「撳畫面可以快進」，中間冇空框（舊版 v160 截圖嗰度有一個空框）。

## C2 — NOTES_V20A160.md 贏全長數字更正（文件問題）

- **改咗邊個檔案：常駐 clone `~/workspace/linji-repo/NOTES_V20A160.md` 第 20 行**（唔係工作副本入面嗰份；工作副本嗰份係 v160 快照，刻意唔郁）。
- 改動：`贏全長 9350→11550ms` → `贏全長 11150→13350ms`，加註「v166 更正：舊數 9350→11550 兩邊都漏咗 glamour beat 1800ms——beats62 總和 13350ms，實駕 13594／13605ms」。
- 狀態：**已改，未 commit**——留喺常駐 clone 工作區（`git status` 淨係 `M NOTES_V20A160.md`，`index.html` 冇掂）。統籌落地嗰陣同 v166 squash merge 分開 commit（唔好撈埋入 v166 squash commit）。
- 點解唔郁 `NOTES_V20A160_M4.md`：嗰份第 12 行「贏分支全長 9350 → 11550ms（冇海報；有海報 13350ms）」數字本身啱——9350 係加 walkup 之前、冇海報（冇 glamour）嘅總和（1200＋1750＋2400＋1400＋2100＋500），11550＝9350＋2200（walkup），13350＝11550＋1800（glamour）。錯嘅只係主 NOTES 第 20 行冇寫「冇海報」限定，令人以為贏全長係 11550。

## 測試

- 新 `tests/test_awards166_static.py`：**33/33 PASS**（B1：overlay 只冚 canvas／pointer-events／panel 44%＋0.93 暗底／海報縮細／glamHtml 包 panel＋搬入 frame／walkup 唔郁／燕尾服 3 處唔郁；C1：setCaption 切換 display／walkup＋glamour＋won-out 空 caption／open＋reveal＋comfort 有字／names 經 lines 填字）。
- 反證（pristine `276ffa1`，`/tmp/pristine166.html`）：**21 FAIL，唔 crash**——FAIL 嘅正正係 21 項修復斷言；PASS 嘅 12 項係本來就真嘅事實（overlay 在場、glamHtml 有海報＋cap、燕尾服 3 處、setCaption 在場、空／有字 beats 本來就係咁）。
- 全套 `qa131/run_suite.sh`：**工作版 222 PASS／12 FAIL**；基線 pristine 221／12——＋1 正正係新測試。12 項 FAIL 逐個對 pristine `276ffa1` 直接覆驗，全部同樣 FAIL（pre-existing 穩定集：flash51、giglib36、pacing35、poster59、rumor49、slot50、soft_tip_111_restore、start53、weave43、weave44、weave49、wrap38）。**零回歸。**
- 行數紀律：`index.html` ＋7／−7，總行數 58884 不變；kwan151／tang152／travel114 釘行唔使 resync（L802 附近 CSS 註解併入同一行、`+ glamHtml` 併入 canvas 行）。

## 實駕（`qa166/drive166.py`，沿用 `drive160r.py` 模式＋v166 量度）

- 本地鏡像（工作副本本身，port 8987）＋`?softPreview=1`；force won（film 海報 gig 種子）。
- **won_932 PASS、won_700 PASS，0 pageerror**（每 case 21 項 checks 全 PASS）。關鍵量度見上表 B1 一節。
- 贏全長：932 實測 13284ms、700 實測 12986ms（期望 beats 總和 13350ms；700 低少少係 poll 粒度，各 beat 實測時長全部貼近規格：open ~770／enter ~1800／names ~2370／suspense ~1440／reveal ~2080／walkup ~2240／glamour ~2400 含 out 500＋poll 滯後——同 v160 review 嘅 glamour＋out 合併量度同一 artifact）。
- Beats 全部見齊：open／enter／names／suspense／reveal／walkup／glamour；結果卡照出「得獎」；舞台播完拆走。
- 實駕輸出：`qa166/drive166.json`、截圖 `qa166/shots/`（每 beat＋invite＋result，won_932／won_700 各一套）。

## 殘留

- glamour 燕尾服偏細（屏幕 61×62px，同 reveal 一致，dispH 64 canvas px）——按規格，唔係新問題；並置之後肉眼讀得清，唔建議喺呢票放大（郁 draw 尺寸會牽連 reveal）。
- glamour panel 內容偏逼：cap 3 行（88px）＋海報 126px＋gap／padding，panel 高 230px——實測海報頂 y248（panel 頂 244＋4）、cap 底 y470（panel 底 474−4），啱啱塞得入，無溢出；再長嘅獎項名會再逼，下一票郁 glamour 文案嗰陣要重驗。
- v149 未落地（頒獎禮 B1 舞台放大＋B2 報紙賽果＋comfort beat）：今次改動只限 glamour overlay／caption 顯示，冇掂舞台幾何／報紙／comfort，唔會同 v149 打架；但 v149 落地後舞台幾何變，glamour 並置要重驗一次（overlay 係 aspect-ratio 對齊 canvas，理論上跟住郁）。
- 掌聲 MP3 仍然未經人耳試聽（v160 已知，唔係今票範圍）。

## 落地紀錄（統籌）
- main 落地前係 `13e2594`（v164 NOTES；遊戲 commit `3973d4a`）。分支 `v20a166` 兩輪 rebase：先上 `3973d4a`（v164 遊戲），再上 `13e2594`（v164 NOTES，淨 4 行 NOTES，零衝突）；最終分支 HEAD `e56b223`。第一次 push 俾常駐 clone 拒絕（non-fast-forward——rebase 改寫歷史），用 `--force-with-lease` 更新分支後，核實常駐 clone `v20a166` HEAD＝`e56b223` 先 merge（v160 教訓）。
- C2 修正**分開 commit**：`433b62a`（淨改 `NOTES_V20A160.md` 1 行），唔撈入 v166 squash。
- Squash commit：`da05b32`——「v20a166: 頒獎禮 glamour 海報縮細並置＋空字幕框隱藏（v160 review B1／C1；C2 另 commit 433b62a；新測試 33 項＋實駕 won_932／won_700 全 PASS；全套 223／12 零回歸）」。`qa166/` 實駕腳本＋截圖留喺工作副本，唔入 main（18 張圖約 3.5MB）。
- 線上核實：push 後約 135 秒 curl，HTTP 200，**5,219,490 bytes、sha256 `bdd92378…`**，同 repo HEAD index.html 完全一致（第一次 45 秒嗰陣仲係舊版 5,218,568／`fe149f34…`，Pages 部署有 lag）。
- 驗證（rebase 後最終樹）：新測試 33/33 PASS＋反證 pristine 21 FAIL（唔 crash）；全套 pristine 222／12 vs 工作版 **223／12**，FAIL 清單逐項相同（12 項穩定 pre-existing），零回歸；kwan151／tang152／travel114 全部 PASS；主 JS `node --check` SYNTAX-OK；合併後樹重驗新測試 ALL PASS；`git fsck --strict` 只有 dangling objects（預期），零 error。
- 殘留：glamour 燕尾服偏細（61×62px，同 reveal 一致，按規格）；glamour panel 內容偏逼（cap 3 行 88px＋海報 126px，panel 高 230px，啱啱塞入無溢出；再長嘅獎項名要重驗）；v149 未落地，佢落地後舞台幾何變，glamour 並置要重驗一次；掌聲 MP3 仍然未經人耳試聽。
