# v20a207 resync：index.html 淨 +34 行（見 qa207/resync207.py，73 錨點對位零 mismatch，純漂移）。
# -*- coding: utf-8 -*-
# v20a197 BUTTONS197 靜態測試：全站掣位 review B1–B7＋C1–C7＋刪 D1 印章掣
# （用戶 2026-11-13 21:11 拍板「一次過修晒」）。
# 反證：喺 pristine main（2760680）index 上行會 FAIL（冇 BUTTONS197 段）。
# 用法：python3 tests/test_buttons197_static.py [path-to-index.html]
import sys
from pathlib import Path
p = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent.parent / 'index.html'
src = p.read_text(encoding='utf-8')
fails = []
def ok(name, cond):
    print(('PASS ' if cond else 'FAIL ') + name)
    if not cond: fails.append(name)

# --- 基線不變 ---
ok('SAVE key／softRev／?v= 不變', 'starVolunteer_map_v19w' in src and 's107' in src and 'v20a10' in src)

# --- B1：巧遇「下一句」同主線同一粒掣 ---
ok('B1：巧遇「下一句」全寬深色掣 370×44 置中（唔再係右下角 88px 文字鏈）',
   '#enc79-overlay .e79-btn{flex:0 1 370px;width:370px;max-width:100%;margin:0 auto;min-height:44px;' in src
   and 'background:#2e2113;color:#f3e8d5' in src
   and '#enc79-overlay .e79-btn{flex:0 0 auto;margin-left:auto;' not in src)
ok('B1：巧遇選項掣同樣 370px 置中',
   '#enc79-overlay .e79-btn.e79-choice{flex:0 1 370px;width:370px;max-width:100%;margin:0 auto;' in src)
ok('B1：對話盒底 padding 收 9px（掣底同主線一樣離 viewport 底 9px）',
   'padding:12px 14px calc(9px + env(safe-area-inset-bottom));color:#2a2118;' in src)

# --- B2＋D1：手帳確認掣唔變形＋鎖定印章唔再係掣 ---
ok('B2：鎖定印章 flex:1 佔滿 bar、52px 高（同未確認掣同一幾何）',
   '#nb-actions #btn-confirm-plan.is-locked{ flex:1 1 auto; width:auto; height:52px;' in src
   and '#nb-actions #btn-confirm-plan.is-locked{ flex:0 0 auto; width:fit-content;' not in src)
ok('B2：印章視覺唔郁（24px、3px double 紅框、斜 -4.5°、.32em）',
   'font-size:24px' in src and 'border:3px double #c0452c !important' in src
   and 'rotate(-4.5deg)' in src and 'letter-spacing:.32em' in src)
ok('B2：「還原」鎖定態唔消失（永遠 inline-block＋disabled 灰態）',
   'resetBtn.style.display = "inline-block"' in src
   and '#nb-actions #btn-reset-plan:disabled{ opacity:.35; cursor:not-allowed; }' in src
   and 'resetBtn.style.display = editable ? "inline-block" : "none"' not in src)
ok('D1：鎖定態經 helper 換做 <span>（唔係掣），換返 button 嗰陣重綁 onclick=confirmPlan',
   'function syncConfirmPlanStamp197(locked){' in src
   and 'el = document.createElement(locked ? "span" : "button");' in src
   and 'if(!locked){ el.type = "button"; el.onclick = confirmPlan; }' in src)
ok('D1：三個呼叫點齊（renderNotebook／setUnderlyingInert／confirmPlan 鎖定分支）',
   src.count('syncConfirmPlanStamp197(') >= 4)  # 定義＋三個呼叫點

# --- B3：頒獎禮「跳過」釘死喺舞台固定位 ---
ok('B3：跳過掣搬入 canvaswrap（480×432 固定比例，v20a207 B2，唔跟 beat 高度走）',
   'awd62-skip">跳過 ⏩</button>\' + "</div>" + glamHtml' in src)
ok('B3：跳過掣 CSS 搬去底邊（v20a207 B3：absolute bottom:8 right:8，唔再壓框角「角度」pill）',
   '.awd62-skip{position:absolute;bottom:8px;right:8px' in src)

# --- B4：日結板 modal 固定高度＋底錨統一 ---
# 實駕揭露舊版 :not(.tut-on) 喺 tut-on 態下完全冇生效（兩板都係 tut-on，掣 y 差 70px
# 同 review 數字逐 px 相同），且兩板 anchor 唔同（拍攝板 tut-on 置中／休息板 v18a 貼底）。
# 所以高度規則唔再排除 tut-on，另加 anchor 統一做 flex-end 底錨。
ok('B4：日結板 modal 固定高度（78dvh，矮屏 92dvh；唔再排除 tut-on）',
   '#mask.day-res .modal{ height: min(78dvh,78svh,720px) !important; }' in src
   and '#mask.day-res:not(.tut-on) .modal{ height:' not in src
   and 'height: min(92dvh,92svh,720px) !important;' in src)
ok('B4：日結板 mask anchor 統一底錨（拍攝板置中 vs 休息板貼底係根因）',
   '#mask.day-res{ align-items: flex-end !important; }' in src)
ok('B4：日結板三條路徑一律掛 day-res（流程邏輯唔郁，只郁幾何）',
   src.count('classList.add("day-res")') >= 3)

# --- B5：「返回地圖」全局規格＝底部全寬 44px ---
ok('B5：地點 sheet「返回地圖」改全寬',
   '#loc-sheet.sheet .btnrow #loc-close,' in src
   and 'flex:1 1 100% !important; width:100% !important; min-height:44px !important;' in src)
ok('B5：手帳頁頂吊牌高改 44px（保留頁頂右位置＋吊牌形）',
   '#home-tab-exit #home-back-map-tabs{ flex:0 0 auto; width:102px !important; min-height:44px; height:44px;' in src)
ok('B5：日結 modal 嗰粒已經係全寬（唔郁）',
   'label:"回家結算"' in src or 'label: "回家結算"' in src or 'btns.push({label: ended?"回家結算":"返回地圖"' in src)

# --- B6：地圖「過一日」開 sheet 唔走位 ---
ok('B6：舊 v18a compact HUD 拎走（top:42px／max-width:280px／細字／收起 help 行）',
   'top:42px; left:8px; right:auto;' not in src
   and 'max-width:min(72%,280px)' not in src
   and '.map-wrap.sheet-open .map-hint .map-hint-help,' not in src)
ok('B6：sheet-open 嗰陣 hint sticky 釘喺 scrollport 底、幾何同乾淨態一致',
   '.map-wrap.sheet-open .map-hint{' in src
   and 'position:sticky !important; bottom:12px !important;' in src
   and 'max-width:none; max-height:none; overflow:visible;' in src)

# --- B7：手帳分類掣初 paint 見晒撳到 ---
ok('B7：#notebook 內容尾加 bar 高度 padding（932：84px；700：61px）',
   '.notebook{' in src and 'padding-bottom:84px;' in src
   and '.notebook{ padding-bottom:61px; }' in src)
ok('B7：入 plan pane 嗰陣初 paint 分類掣俾 bar 冚住就捲返出嚟（只喺 scrollTop===0）',
   'function revealCatTabs197(){' in src
   and 'if(nb.scrollTop!==0) return;' in src
   and 'revealCatTabs197()' in src)

# --- C1：主分頁使用中嗰格唔改大細 ---
ok('C1：選中格 32px（同其餘四格同一條 y，用色／底線區分）',
   '#home-tabs .home-tab.on{ height:32px;' in src
   and '#home-tabs .home-tab.on{ height:38px;' not in src)

# --- C2：地圖底部主掣用色區分兩個身份 ---
ok('C2：「過一日」改紙色＋啡框（「開始今日行程」留返金色實色）',
   '#v-map .map-hint #map-end-day{' in src
   and 'background:#fffdf6 !important; color:#3a2e22 !important;' in src
   and 'border:2px solid #8a6f4d !important; box-shadow:none !important;' in src)

# --- C3：地點 sheet 行動掣齊高 ---
ok('C3：行動掣固定 60px 高，標題／描述單行截短',
   'height: 60px !important;' in src
   and 'white-space: nowrap !important;' in src
   and '-webkit-line-clamp: 1 !important;' in src)

# --- C4：肯定／主動作永遠在上 ---
ok('C4：tut-on 嗰陣非教學 modal 掣一律 order:1（次序跟 DOM；肯定行永遠在上）',
   '#mask.tut-on #modal-btns button{ order:1 !important; }' in src)
ok('C4：教學掣次序唔郁（.p order:1／.tut-skip order:2／.tut-replay-step order:3）',
   '#mask.tut-on #modal-btns button.tut-skip,' in src
   and 'order: 2 !important;' in src
   and '#mask.tut-on #modal-btns button.tut-replay-step{' in src
   and 'order: 3 !important;' in src)
ok('C4：全部 modal DOM 次序本身已經係肯定行先（出席→推辭、確定→取消）',
   '{ label: "出席", role: "p", on: attend },' in src
   and '{ label: "推辭", role: "g", on: skip }' in src
   and '{ label:"確定過一日", role:"d", on:()=>endBrowseDayGoHome() },' in src)

# --- C5：抉擇卡齊高 ---
ok('C5：抉擇卡最小 64px、短句置中',
   '.story-play .sp-choice{' in src and 'min-height:64px;' in src
   and 'display:flex;flex-direction:column;justify-content:center;' in src)

# --- C6：通告板 54px 罅＝分組頭 ---
ok('C6：未達標分組頭做返明顯標題（唔再係無解釋嘅空位）',
   '.gig-locked108{ margin-top:12px; border-top:2px solid #cbb98d; padding-top:0; }' in src
   and '.gig-locked108 summary{ display:block;' in src
   and 'background:#efe6cf; border-bottom:1px solid #cbb98d;' in src)
ok('C6：開合提示由 CSS ::after 出（▸ 點開睇／▾ 點開收起），唔寫死喺字串',
   '.gig-locked108 summary::after{ content:"  ▸ 點開睇";' in src
   and '.gig-locked108[open] summary::after{ content:"  ▾ 點開收起"; }' in src
   and '——點開睇</summary>`' not in src)

# --- C7：手帳分頁撞名 ---
ok('C7：sub-tab「行程」改名「本週安排」（主分頁「行程」唔郁）',
   'id="htab-plan" role="tab" aria-selected="false" data-htab="plan">本週安排</button>' in src
   and 'id="hgroup-plan" role="tab" aria-selected="true" data-hgroup="plan" data-htab="plan">行程</button>' in src)

# --- 唔做嘅嘢 ---
ok('D3 唔刪：地圖「進度」chip 保留', '進度' in src)
ok('D2 唔喺呢票：日結板「返回地圖」掣仲喺度', '返回地圖' in src)

print('RESULT ' + ('FAIL (%d)' % len(fails) if fails else 'PASS'))
sys.exit(1 if fails else 0)
