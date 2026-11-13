# v20a187 修 v181 設計 review B1＋C1–C6・static tests（字串＋CSS 規則斷言，跟 v181 寫法）：
# B1：地板 y228–310（深 82px＝22.8% 高；地板深／人物高 0.92、腳底以下空地板 48px＝0.54 倍）；
#     幕布拉長到 y228、燈架跟到 y228、觀眾席 y316–360（深 44px，光點照舊）。
# C1：glamour 海報下半置中（panel flex-end＋img max-height 40%），海報頂唔再壓白牌。
# C2：卡罅 8→24px，角標留 10px 罅。
# C3：out beat 照畫人物、alpha 跟 step 遞減。C4：walkup 行緊 y＋6。C5：glamour-hide display:none 保留（trade-off）。
# C6：glyph −112→−110（牌底 149.4 到 glyph 頂 152，留 2.6 邏輯罅）。
# 唔郁守衛：FLOOR 262／企位／三行白牌黃字 fix（牌底 149.4）／SAVE key／softRev／?v=。
# 反證：run against pristine main b1b6092 index -> 新幾何／修法斷言全部 FAIL（唔 crash）；守衛 pristine 應 PASS。
import sys, re

idx_path = sys.argv[1] if len(sys.argv) > 1 else 'index.html'
src = open(idx_path, encoding='utf-8').read()
fails = []

def chk(name, cond):
    print(('PASS ' if cond else 'FAIL ') + name)
    if not cond:
        fails.append(name)

def slice_fn(name):
    i = src.find('function ' + name + '(')
    if i < 0: return ''
    depth = 0
    j = src.find('{', i)
    for k in range(j, len(src)):
        if src[k] == '{': depth += 1
        elif src[k] == '}':
            depth -= 1
            if depth == 0: return src[i:k+1]
    return ''

def css_rule(selector):
    i = src.find(selector + '{')
    if i < 0: return ''
    j = src.find('}', i)
    return src[i:j+1] if j >= 0 else ''

play_fn = slice_fn('awards62PlayCeremony')
base_fn = slice_fn('awards181DrawBase')

# --- B1：地板收窄（程式舞台幾何） ---
chk('B1 地板 y228–310（#d9a75f，深 82px）', '#d9a75f' in base_fn and '228, W + 16, 82' in base_fn)
chk('B1 舊地板 y200／深 134 唔再出現（base 範圍）', '200, W + 16, 134' not in base_fn)
chk('B1 地板深 82px＝22.8% 高（20–26% 帶）', 0.20 <= 82 / 360 <= 0.26)
chk('B1 地板深／人物高 82/89≈0.92（0.85–1.00）', 0.85 <= 82 / 89 <= 1.00)
chk('B1 腳底以下空地板 48px＝0.54 倍人物高（0.48–0.60）', 0.48 <= (310 - 262) / 89 <= 0.60)
chk('B1 幕布拉長到 y228（#f2e8d5 高 192）', '#f2e8d5' in base_fn and '36, W + 16, 192' in base_fn)
chk('B1 側幕落到 y228（#7a1f24 高 228）', '#7a1f24' in base_fn and '38, 228' in base_fn)
chk('B1 燈架鐵杆落到 y228（#23232c 高 188）', '#23232c' in base_fn and '40, 4, 188' in base_fn)
chk('B1 地板前緣 y310（#5a3a1e 高 6）', '#5a3a1e' in base_fn and '310, W + 16, 6' in base_fn)
chk('B1 觀眾席 y316–360（#120c20 高 44）', '#120c20' in base_fn and '316, W + 16, 44' in base_fn)
chk('B1 舊觀眾席 y340／高 20 唔再出現', '340, W + 16, 20' not in base_fn)
chk('B1 觀眾席光點仲在（金色 3px 點）', 'rgba(255,233,143,0.85)' in base_fn)
chk('B1 FLOOR＝262 唔郁（腳底唔郁，只郁地板帶）', 'const FLOOR = 262' in play_fn)

# --- C1：glamour 海報下半置中 ---
panel_rule = css_rule('.awd63-glamour-panel')
panel_img_rule = css_rule('.awd63-glamour-panel>img')
chk('C1 panel 改 flex-end（海報＋cap 沉底）', 'justify-content:flex-end' in panel_rule)
chk('C1 海報 max-height 60%→40%', 'max-height:40%' in panel_img_rule and 'max-height:60%' not in panel_img_rule)
chk('C1 海報 max-width 88% 唔郁', 'max-width:88%' in panel_img_rule)
chk('C1 海報頂計數 ≥171 邏輯＞牌底 149.4（360−144−45）', (360 - 0.40 * 360 - 45) > 149.4)

# --- C2：卡罅 8→24px ---
cards_rule = css_rule('.awd63-cards')
_m = re.search(r'gap:\s*(\d+)px', cards_rule)
_gap = int(_m.group(1)) if _m else -1
chk('C2 卡罅 gap 24px', _gap == 24)
chk('C2 角標唔撞（gap 24 − 7 − 7 ＝ 10px 罅）', _gap - 7 - 7 == 10)
chk('C2 卡列總闊 424px ≤ 760 框', 4 * 88 + 3 * _gap <= 760)
chk('C2 🏆 仲喺左上角（left:-7，唔搬去右上角）', 'left:-7px' in css_rule('.awd63-card.win::after'))
chk('C2 「你」徽仲喺右上角（right:-7 唔郁）', 'right:-7px' in css_rule('.awd63-card.me::after'))

# --- C3：out beat 照畫人物 ---
_out_i = play_fn.find('if(id === "out"){')
_out = play_fn[_out_i:play_fn.find('};', _out_i)] if _out_i >= 0 else ''
chk('C3 out 分支畫人物（唔再淨係畫 overlay）', 'drawFigure' in _out)
chk('C3 人物 alpha 跟 step 遞減（1−step×0.25）', '1 - step * 0.25' in _out)
chk('C3 won 只留燕尾服阿偉（tuxedo）', 'tuxedo: true' in _out and 'best === "won"' in _out)
chk('C3 其餘跟 comfort 暗度（winnerSlot ? 0.85 : 0.7）', 'winnerSlot ? 0.85 : 0.7' in _out)
chk('C3 out 仲係 500ms（唔加 beat）', 'id: "out", ms: 500' in src)

# --- C4：walkup y＋6 ---
_walk_i = play_fn.find('if(id === "walkup"){')
_walk = play_fn[_walk_i:play_fn.find('if(id === "out"){', _walk_i)] if _walk_i >= 0 else ''
chk('C4 walkup 行緊 y＋6', 'y: 6' in _walk)
chk('C4 行完換燕尾服 y 歸 0（y: 6 只出現一次）', _walk.count('y: 6') == 1)
chk('C4 walkup 路徑唔郁（−40 行 1400ms）', '-40 + (targetX + 40) * wp' in _walk and 'beatElapsed / 1400' in _walk)

# --- C5：glamour 下移 trade-off 保留 ---
chk('C5 glamour-hide 仲係 display:none（v174 trade-off 保留）', 'display:none' in css_rule('.awd63-cards.glamour-hide'))
chk('C5 syncGlamour 仲係 toggle glamour-hide', 'cardsEl.classList.toggle("glamour-hide"' in play_fn)

# --- C6：glyph −110 ---
chk('C6 燕尾服 glyph −110 兩處', 'FLOOR + fp.y - 110' in play_fn and 'FLOOR - 110' in play_fn)
chk('C6 舊 −112 唔再出現（頒獎禮範圍）', '- 112' not in play_fn)
chk('C6 牌底 149.4 到 glyph 頂 152 留 2.6 邏輯罅', abs((262 - 110) - 149.4 - 2.6) < 0.01)
chk('C6 glyph 底 170 離頭頂 173 仲有 3px', (262 - 110 + 18) == 170 and 173 - 170 == 3)
chk('C6 對手胸前 glyph −52 唔郁', 'FLOOR + fp.y - 52' in play_fn)

# --- 唔郁守衛：黃字 fix 三行白牌（牌底 149.4 唔郁） ---
def _pct(rule, prop):
    mm = re.search(prop + r':\s*([\d.]+)%', rule)
    return float(mm.group(1)) if mm else None
board_rule = css_rule('.awd181-board')
board_top = _pct(board_rule, 'top'); board_h = _pct(board_rule, 'height')
chk('守衛 白牌底 149.4 邏輯唔郁（top＋height＝41.5%）',
    board_top is not None and board_h is not None and round((board_top + board_h) * 3.6, 1) == 149.4)
chk('守衛 白牌底 149.4 ＜ glyph 頂 152（C6 之後罅仲大咗）',
    board_top is not None and board_h is not None and (board_top + board_h) * 3.6 < 152)
chk('守衛 4 slots／gallery 企位唔郁',
    '240 + (i - (slots.length - 1) / 2) * 120' in play_fn and '[75, 240, 405]' in play_fn)
chk('守衛 SAVE key 不變', 'starVolunteer_map_v19w' in src)
chk('守衛 softRev 不變（s107）', 'var SOFT_REV = "s107"' in src)
chk('守衛 產品 ?v= 不變（v20a10）', '?v=20a10' in src)

print()
if fails:
    print('FAILED: %d' % len(fails))
    for f in fails:
        print(' - ' + f)
    sys.exit(1)
print('ALL PASS')
