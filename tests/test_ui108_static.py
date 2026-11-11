# v20a108 UI108 視覺統一包（B 級）・靜態守門測試（工人 C 範圍：D-5＋S-1/2/4/5/7/8/9/11/18/20/27/29/33/34/36）。
# 用法：python3 tests/test_ui108_static.py [path-to-index.html]
# 反證意識：每項同時驗「新寫法在」＋「舊寫法不在」（舊寫法出現即 FAIL）。
# 注意 S-9 舊直角框規則保留喺檔（被 v108 規則後發覆蓋），故用「位置先後」驗覆蓋而非「舊字串消失」。
import os, sys

path = sys.argv[1] if len(sys.argv) > 1 else 'index.html'
html = open(path, encoding='utf-8').read()
fails = []

def ok(name, cond):
    print(('PASS ' if cond else 'FAIL ') + name)
    if not cond:
        fails.append(name)

def body_of(fname, span=3000):
    i = html.find(fname)
    return html[i:i + span] if i >= 0 else ''

# D-5 巧遇對話框改米紙框（JS 注入 CSS 字串）
ok('D-5 e79-box 米紙漸變', 'linear-gradient(168deg,#f8f0dd 0%,#f2e6cc 58%,#ebdfc1 100%)' in html)
ok('D-5 e79-box 冇舊深啡木框漸變', 'linear-gradient(180deg,#241a10,#1a120a)' not in html)
ok('D-5 e79-name 深金色', '#enc79-overlay .e79-name{font-weight:800;color:#8a5a00' in html)
ok('D-5 e79-name phone 紙底可讀藍', '#enc79-overlay .e79-name.phone{color:#2f6fed' in html)

# S-1 主頁規則字加半透明紙底
ok('S-1 tip 紙底規則', '#start-soft-tip{ background:rgba(243,231,200,.93)' in html)
ok('S-1 tip 深色字 !important 蓋過 .start p !important', 'color:#3a2e22 !important; text-shadow:none;' in html)
ok('S-1 tip 冇舊 opacity:.9 壓相', 'id="start-soft-tip" style="font-size:.78rem;margin-top:6px;opacity:.9"' not in html)

# S-2 冇存檔只留一粒細讀檔入口
ok('S-2 btn-load-mini 在', 'id="btn-load-mini"' in html)
ok('S-2 paintTitleSaveBtns 冇存檔隱藏大掣', 'bm.style.display = has ? "none" : "inline-block"' in html)
ok('S-2 mini 開讀檔 modal', '_btnLoadMini.onclick=()=>openSaveSlotsModal("load")' in html)

# S-4 導入 dim 只落內容／地圖區
b = body_of('function setTutMask', 1600)
ok('S-4 setTutMask 量度殼底', '--tut-shell-bottom' in b)
ok('S-4 tut-on 漸變 dim（殼底以上透明）', '#mask.tut-on{ background:linear-gradient(180deg, rgba(0,0,0,0) 0' in html)

# S-5 B01 導入圖換新場景＋新全身
ok('S-5 b01GuideHtml108 在', 'function b01GuideHtml108' in html)
ok('S-5 用新事務所場景圖', 'LOC_SHEET_BG.agency_ho' in body_of('function b01GuideHtml108', 900))
ok('S-5 用阿偉／何生新全身', 'fullbody/awi_base.webp?v=20a106' in html and 'fullbody/ho_sang_base.webp?v=20a106' in html)
ok('S-5 B01 呼叫新場景（舊圖只做退路）', 'b01GuideHtml108()' in body_of('function showB01HomeModal', 2600))

# S-7 地圖標籤微調＋光暈加厚
ok('S-7 鑽石山新位 38%/6.5%', 'left:38%;top:6.5%">鑽石山' in html)
ok('S-7 九龍城新位 58%/31.5%', 'left:58%;top:31.5%">九龍城' in html)
ok('S-7 紅磡新位 52%/38%', 'left:52%;top:38%">紅磡' in html)
ok('S-7 金禧新位 11%/44.5%', 'left:11%;top:44.5%">金禧大酒店' in html)
ok('S-7 薄扶林新位 41%/65%', 'left:41%;top:65%">薄扶林' in html)
ok('S-7 維港電影新位 80%', 'left:80%;top:calc(18% + 38px)">維港電影' in html)
ok('S-7 廟街禮品新位 44%', 'left:44%;top:calc(35% - 44px)">廟街禮品' in html)
ok('S-7 舊擠迫座標唔再出現', 'left:49%;top:8%">鑽石山' not in html and 'left:63%;top:29%">九龍城' not in html)
ok('S-7 地區名光暈加厚', '0 0 4px #f3e7c8, 0 0 4px #f3e7c8, 0 0 4px #f3e7c8' in html)

# S-8 頂欄進度 chip 只係徽章
ok('S-8 chip 係 span 唔係 button', '<span class="chip chip-story" id="chip-story"' in html)
ok('S-8 chip 冇 button 版', '<button type="button" class="chip chip-story" id="chip-story"' not in html)
ok('S-8 chip click 接線已刪', 'cs.addEventListener("click"' not in html)
ok('S-8 地圖 pill 唯一入口保留', 'id="map-progress-btn"' in html)
ok('S-8 chip 游標唔係 pointer', '#app #chip-story{ cursor:default; }' in html)

# S-9 劇情高亮改柔光呼吸光暈（v108 規則喺舊規則之後，先覆蓋）
_i_old = html.find('.pin.has-story-tip{box-shadow:0 0 0 2px rgba(196,138,42,.85)')
_i_new = html.find('#app .map-pins .pin.has-story-tip{ background:radial-gradient')
ok('S-9 v108 柔光規則在舊規則之後', _i_old >= 0 and _i_new > _i_old)
ok('S-9 呼吸光暈 keyframes (box-shadow)', '@keyframes storyGlow108{ 0%,100%{ box-shadow:0 0 10px 1px rgba(232,200,120,.35); } 50%{ box-shadow:0 0 22px 5px rgba(232,200,120,.7); } }' in html)
ok('S-9 光暈用高特異性 + !important 蓋過 .pin !important', '#app .map-pins .pin.has-story-tip{ background:radial-gradient(ellipse at center, rgba(232,200,120,.55) 0%, rgba(232,200,120,.22) 55%, rgba(232,200,120,0) 78%) !important;' in html)
ok('S-9 柔光係圓形漸變', 'radial-gradient(ellipse at center, rgba(232,200,120,.55)' in html)

# S-11 HUD 壓力：數字加粗＋過 70 紅色脈動
ok('S-11 壓力數字加粗', '#app .hud-stress-val{ font-weight:900;' in html)
ok('S-11 hud danger 門檻 70', 'hsBox.classList.toggle("danger", hsVal>=70)' in html)
ok('S-11 stChip danger 門檻 70', 'stChip.classList.toggle("danger", stVal>=70)' in html)
ok('S-11 danger 脈動 keyframes', '@keyframes hudStressPulse108' in html)
ok('S-11 爆表文案門檻 90 保留（只改 HUD 顏色門檻）', 'if(stVal>=90) stMsg.textContent="爆表"' in html)

# S-18 複製掣加可見標籤
ok('S-18 ⧉ 加「複製」可見字', 'cp.textContent="⧉ 複製"' in html)

# S-20 編輯頁「返回地圖」改細掣
ok('S-20 返回地圖細掣規則', '#home-tab-exit #home-back-map-tabs{ flex:0 0 auto !important; width:auto !important;' in html)
ok('S-20 確定留主 CTA（flex:1）', '#nb-actions #btn-confirm-plan{ flex:1 1 auto; }' in html)

# S-27 卡面只留牌面一個數，區間收去詳情
ok('S-27 gigPayExactText 有 card 變體', 'if(opts && opts.card) return "$"+n.toLocaleString();' in html)
ok('S-27 兩張卡用 card 變體', html.count('gigPayExactText(g, {card:true})') == 2)
ok('S-27 詳情仍經 gigPayExactHtml（保留區間）', 'function gigPayExactHtml(g){\n  const t=gigPayExactText(g);' in html)

# S-29 可接置頂＋未達標預設摺疊
b = body_of('function doScout', 6000)
ok('S-29 板面分 ready/locked', 'ready108' in b and 'locked108' in b)
ok('S-29 未達標 details 預設摺疊', '<details class="gig-locked108">' in b)
ok('S-29 摺疊標題有張數', '未達標／長遠目標（${locked108.length} 張）' in b)

# S-33 簽約金行升摘要＋違約金有數先出
# 視窗 7000→11000：S-30v2 令 castingNoticeDetailHtml 由 ~6.9k 漲到 9750 字元
# （負責人英雄區＋要求格＋完成期限 consts），簽約金／違約金／toggle 行全部喺 8.5k 內。
b = body_of('function castingNoticeDetailHtml', 11000)
ok('S-33 摘要有簽約金行', '簽約金</span><span class="v">${signFee108}</span>' in b)
ok('S-33 簽約金寫「獲聘後即收」（v20a115：舊寫法「接通告後即收」同機制唔啱——簽約金只喺 aud91PresentOne 公佈獲聘嗰刻入帳，見「簽約金＝合約額三成，公佈嗰刻即付」；doAudition 接通告嗰刻唔入帳）', '（獲聘後即收）' in b and '（接通告後即收）' not in b)
ok('S-33 違約金有數先出', 'gigBreachFee(g)!=null' in b)
ok('S-33 違約金行只喺條件 helper 入面（模板改用 ${breachRow108}）', '${breachRow108}' in b and html.count('<div class="cn-sum-row"><span class="k">違約金</span><span class="v">${breachStr}</span></div>') == 1)
_i_sign = b.find('${signFee108}</span>')
_i_breach = b.find('${breachRow108}', _i_sign)
_i_toggle = b.find('cn-detail-toggle', _i_sign)
ok('S-33 違約金行升入摘要（唔使展開先見）', _i_sign > 0 and 0 < _i_breach < _i_toggle)

# S-34 「離開」改淺色文字掣
ok('S-34 btn_leave 透明淺色', 'button.btn_leave,\n#mask:not(.tut-on) #modal-btns button.g.btn_leave{\n  background:transparent !important; color:#7a6248 !important;' in html)
ok('S-34 舊鮮橙離開掣已蓋過', 'background:#e07020 !important; color:#fff !important; border:2px solid #a04810 !important;' in html and 'background:transparent !important; color:#7a6248 !important;' in html)

# S-36 地圖底部卡等試鏡回音行
ok('S-36 audLine108 在 paintBar', '等緊 ${_n} 張試鏡回音' in html)
ok('S-36 有先顯示（pendingAud 計數）', '(S.pendingAud||[]).length' in html)
ok('S-36 aud 行樣式', '.map-hint-aud108{ display:block;' in html)

# 紅線：SAVE key／softRev／產品 ?v= 冇郁
ok('紅線 SAVE key 不變', 'starVolunteer_map_v19w' in html)
ok('紅線 softRev s107', 's107' in html)
ok('紅線產品 ?v= v20a10', 'v=20a10' in html)

print()
if fails:
    print('FAILURES:', len(fails))
    sys.exit(1)
print('ALL PASS')
