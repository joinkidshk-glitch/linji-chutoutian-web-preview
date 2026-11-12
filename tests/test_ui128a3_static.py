# v20a128 A3 對話舞台收尾包・靜態守門測試（N5／N4／D-7／D-1／N16／WF4）。
# 用法：python3 tests/test_ui128a3_static.py [path-to-index.html]
# 反證意識：每項同時驗「新寫法在」＋「舊寫法不在」（舊寫法出現即 FAIL）。
# 對 pristine main（v129 前）行 → 全部新寫法缺席 → 乾淨 FAIL。
import os, sys

path = sys.argv[1] if len(sys.argv) > 1 else 'index.html'
html = open(path, encoding='utf-8').read()
fails = []

def ok(name, cond):
    print(('PASS ' if cond else 'FAIL ') + name)
    if not cond:
        fails.append(name)

# N5：故事播放器開嗰陣收起底層 HUD 頂欄，唔再畀金 pill 穿透 mask 露出半粒
ok('N5 story-play-lock 收起 #map-bar', '#app.story-play-lock #map-bar{ visibility:hidden !important; }' in html)
ok('N5 唔係收起成個 #app（範圍收窄到 story-play-lock）', '#app.story-play-lock #map-bar' in html and '#app.mask-up #map-bar' not in html)

# N4：抉擇屏留紙卡，刪重複金掣；紙卡恢復可撳
ok('N4 抉擇模式唔再將選項推入 modalBtns（舊 label: lab 金掣消失）', 'label: lab, role:"p"' not in html)
ok('N4 .sp-choices 隱藏 block 已刪（紙卡恢復可撳）', 'root.querySelectorAll(".sp-choices")' not in html)
ok('N4 抉擇屏底部只留「先返回」註釋', 'v20a128 A3 N4' in html)
ok('N4 強制劇情空 #modal-btns 收起', '#mask.story-play-on #modal-btns:empty{ display:none !important; }' in html)
ok('N4 .sp-actions 隱藏保留（beats 模式唯一主 CTA 仍喺 #modal-btns）', 'root.querySelectorAll(".sp-actions")' in html)

# D-7：頂部 meta 欄只喺開場第一句閃現，抉擇屏唔再重出 .sp-head
# （錨點用 JS 模板 sp-cinematic sp-choices-layout，唔用 sp-choices-layout——
#  嗰個字串第一次出現喺 CSS，CSS 入面有 .sp-head 規則，會誤判。）
i = html.find('sp-cinematic sp-choices-layout')
choices_tpl = html[i:i + 700] if i >= 0 else ''
ok('D-7 抉擇屏模板冇 .sp-head', 'sp-head' not in choices_tpl and 'sp-choices-layout' in choices_tpl)
ok('D-7 抉擇屏模板仲有舞台＋紙卡', 'sp-mode-choices' in choices_tpl and 'sp-choices' in choices_tpl)
ok('D-7 開場第一句 .sp-head 保留（isOpening105）', 'sp-head-opening' in html)

# D-1：開場單人步補阿偉左企位
ok('D-1 pair 單人＋阿偉有對白就補 awi', 'pair.unshift("awi")' in html)
ok('D-1 只補有對白嘅節（hasAwi 檢查）', 'spResolveSpeakerId(b)==="awi"' in html)

# N16：巧遇第三方講者（副導／導演／場務／伙記）中間影格
ok('N16 第三方偵測 helper 在', 'function enc79ThirdParty128(step)' in html)
ok('N16 第三方影映射在（副導／導演／場務／伙記）', '"副導":"shadow_male"' in html and '"伙記":"shadow_male"' in html)
ok('N16 中間影格 HTML 在', 'e79-char3' in html and 'e79-char3-halo' in html)
ok('N16 中間影格唔用 .e79-char class（唔入 __dlg108Fit 自動收細）', 'class="e79-char3-halo"' in html and 'class="e79-char3"' in html)
ok('N16 名牌出職銜＋文案去前綴', 'tpName128' in html and 'tpName128.text' in html and 'tpName128.name' in html)

# WF4：事件 modal 舞台加高，人物唔再 34×100
# v20a133：固定 480px 改 viewport-aware（修 v128 回歸：短 viewport 對話框被切）
ok('WF4 舞台加高 CSS 在', '#mask.wf4-stage-on #modal-inner .story-play .sp-stage{ min-height:min(480px,52dvh); }' in html)
ok('WF4 舞台唔再固定 min-height:480px（v128 回歸寫法）', '#mask.wf4-stage-on #modal-inner .story-play .sp-stage{ min-height:480px; }' not in html)
ok('WF4 開場加 class、finish() 清走', 'classList.add("wf4-stage-on")' in html and 'classList.remove("wf4-stage-on")' in html)

print('TOTAL %s' % ('PASS' if not fails else 'FAIL: ' + ', '.join(fails)))
sys.exit(1 if fails else 0)
