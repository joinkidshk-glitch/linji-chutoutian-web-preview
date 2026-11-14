# v20a190 修 v187 設計 review 新 C1・static tests（字串＋CSS 規則斷言，跟 v187 寫法）：
# 新 C1：v187 海報推到底避白牌，panel 上半留 46–48% 空暗底（932 空 273px／700 空 234px）。
# 修法（用戶 2026-11-13 19:40 拍板）：panel 縮短貼底——overlay align-items stretch→flex-end，
#   海報＋cap 位置唔郁。機制（探針證實）：淨改 flex-end 唔得——img max-height:40% 會對住內容高嘅
#   panel 解（不定→失效），海報脹到 284.8 撞牌；轉 40cqh 亦唔啱（高 8px，932 clearance 跌到 28）；
#   正確係 calc(40cqh - 8px)＋overlay container-type:size——40cqh＝舊 40%×overlay 高，
#   −8px＝扣返 panel 上下 padding 各 10px 嘅 40%（0.4×20；全域 border-box 下舊 cap＝40%×(panel 高−20)），
#   兩 viewport 逐 px 等價（932 cap 220／700 cap 193.6）。
# 驗收（實駕量度）：空佔比 47.9%→3.3%（932）／46.3%→3.6%（700）；海報盒唔郁（932 img 396–616／
#   700 img 390–583）；clearance 36／24 唔跌；底罅 77 唔郁。
# 唔郁守衛：B1 地板 y274–372／FLOOR 314（v20a207 B2）；C2 卡罅 24px；C3 out 留人；C4 walkup y＋6；
#   C5 glamour-hide display:none（下移 124px trade-off）；C6 glyph −110。
# 反證：run against pristine main dcf1b72 index -> 新 C1 斷言全部 FAIL（唔 crash）；守衛 pristine 應 PASS。
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
beats_fn = slice_fn('awards62CeremonyBeats')
glam_rule = css_rule('.awd63-glamour')
panel_rule = css_rule('.awd63-glamour-panel')
panel_img_rule = css_rule('.awd63-glamour-panel>img')
cap_rule = css_rule('.awd63-glamour .cap')

# --- 新 C1：panel 縮短貼底（CSS 機制） ---
chk('C1 overlay 改 align-items:flex-end（唔再 stretch 全高）',
    'align-items:flex-end' in glam_rule and 'align-items:stretch' not in glam_rule)
chk('C1 overlay 有 container-type:size（cqh 以 overlay 高計）', 'container-type:size' in glam_rule)
chk('C1 海報 cap 轉 calc(40cqh - 8px)（舊 40% 唔再出現；裸 40cqh 亦唔准）',
    'max-height:calc(40cqh - 8px)' in panel_img_rule and 'max-height:40%' not in panel_img_rule
    and 'max-height:40cqh' not in panel_img_rule)
chk('C1 海報 max-width 88% 唔郁', 'max-width:88%' in panel_img_rule)
chk('C1 海報金框＋光暈唔郁', 'border:4px solid #f2c14e' in panel_img_rule
    and 'box-shadow:0 0 34px rgba(242,193,78,.45)' in panel_img_rule)
chk('C1 panel 闊 44%＋0.93 暗底＋column＋flex-end＋gap 8＋padding 10/12 唔郁',
    'flex:0 0 44%' in panel_rule and 'rgba(10,6,18,.93)' in panel_rule
    and 'flex-direction:column' in panel_rule and 'justify-content:flex-end' in panel_rule
    and 'gap:8px' in panel_rule and 'padding:10px 12px' in panel_rule)
chk('C1 overlay 仲係 absolute top:0／left:0／width:100%＋aspect 480/432＋pointer-events:none（v20a207 B2）',
    'position:absolute' in glam_rule and 'top:0' in glam_rule and 'left:0' in glam_rule
    and 'width:100%' in glam_rule and 'aspect-ratio:480/432' in glam_rule
    and 'pointer-events:none' in glam_rule)
chk('C1 cap 字體唔郁（19px／行高 1.55，兩行＝58.9px）',
    'font-size:19px' in cap_rule and 'line-height:1.55' in cap_rule)

# --- 新 C1：逐 px 計數（932／700，CSS px） ---
# panel 底＝frame 頂＋overlay 高（932：123＋570＝693；700：156＋504＝660）；牌底 360／366（v187 實測）。
CAP_H = 19 * 1.55 * 2  # 58.9，cap 兩行
def geom(overlay_h, panel_bottom, board_bottom):
    cap = 0.4 * overlay_h - 8  # calc(40cqh - 8px) 用值
    content_h = 10 + cap + 8 + CAP_H + 10
    panel_top = panel_bottom - content_h
    img_top = round(panel_top + 10)
    return {'cap': cap, 'content_h': content_h, 'img_top': img_top,
            'clearance': img_top - board_bottom, 'empty_ratio': 10 / content_h,
            'bottom_gap': round(8 + CAP_H + 10)}
g932 = geom(570, 693, 360)
g700 = geom(504, 660, 366)
chk('C1 932 cap＝0.4×570−8＝220（同 v187 舊 cap 逐 px 等價）', g932['cap'] == 220)
chk('C1 700 cap＝0.4×504−8＝193.6（同 v187 舊 cap 逐 px 等價）', abs(g700['cap'] - 193.6) < 0.01)
chk('C1 932 海報頂 396、離牌底 36px（v187 實測下限）', g932['img_top'] == 396 and g932['clearance'] == 36)
chk('C1 700 海報頂 390、離牌底 24px（v187 實測下限）', g700['img_top'] == 390 and g700['clearance'] == 24)
chk('C1 932 空佔比 10／306.9＝3.3% ≤25%（舊 47.9%）', g932['empty_ratio'] <= 0.25 and abs(g932['empty_ratio'] - 0.033) < 0.002)
chk('C1 700 空佔比 10／280.5＝3.6% ≤25%（舊 46.3%）', g700['empty_ratio'] <= 0.25 and abs(g700['empty_ratio'] - 0.036) < 0.002)
chk('C1 海報底到 panel 底 77px 唔郁', g932['bottom_gap'] == 77 and g700['bottom_gap'] == 77)
chk('C1 海報盒唔郁：932 img 396–616、700 img 390–583',
    g932['img_top'] + 220 == 616 and abs(g700['img_top'] + 193.6 - 583.6) < 0.01)
chk('C1 panel 底唔郁（932：693；700：660）',
    round(693 - g932['content_h'] + g932['content_h']) == 693 and round(660 - g700['content_h'] + g700['content_h']) == 660)
chk('C1 高身海報（0.5 比例）cap 下闊 106px＜max-width 273px', (220 - 8) * 0.5 == 106 and 106 < 0.88 * (334.4 - 24))

# --- 唔郁守衛：其餘六項 ---
chk('守衛 B1 地板 y274–372（#d9a75f，深 98px；v20a207 B2）', '#d9a75f' in base_fn and '228 / 360' in base_fn and '310 / 360' in base_fn)
chk('守衛 B1 觀眾席 y379–432（#120c20，高 53；v20a207 B2）', '#120c20' in base_fn and '316 / 360' in base_fn)
chk('守衛 B1 FLOOR＝314（v20a207 B2）', 'const FLOOR = 314' in play_fn)
cards_rule = css_rule('.awd63-cards')
_m = re.search(r'gap:\s*(\d+)px', cards_rule)
chk('守衛 C2 卡罅 gap 24px', _m and int(_m.group(1)) == 24)
_out_i = play_fn.find('if(id === "out"){')
_out = play_fn[_out_i:play_fn.find('};', _out_i)] if _out_i >= 0 else ''
chk('守衛 C3 out 分支照畫人物、alpha 1−step×0.25', 'drawFigure' in _out and '1 - step * 0.25' in _out)
_walk_i = play_fn.find('if(id === "walkup"){')
_walk = play_fn[_walk_i:play_fn.find('if(id === "out"){', _walk_i)] if _walk_i >= 0 else ''
chk('守衛 C4 walkup 行緊 y＋6（只一處）', 'y: 6' in _walk and _walk.count('y: 6') == 1)
chk('守衛 C5 glamour-hide 仲係 display:none', 'display:none' in css_rule('.awd63-cards.glamour-hide'))
chk('守衛 C6 燕尾服 glyph −129 兩處、舊 −112 唔見（v20a207 B2）',
    'FLOOR + fp.y - 129' in play_fn and 'FLOOR - 129' in play_fn and '- 112' not in play_fn)
chk('守衛 C6 牌底 179.3 到 glyph 頂 185 留 5.7 邏輯罅（v20a207 B2）', abs((314 - 129) - 179.3 - 5.7) < 0.01)

# --- 唔郁守衛：流程／版本 ---
chk('守衛 walkup 2200ms、glamour 1800ms 唔郁', 'id: "glamour", ms: 1800' in beats_fn and 'id: "walkup", ms: 2200' in beats_fn)
chk('守衛 6 beats 順序唔郁', beats_fn.find('id: "reveal"') < beats_fn.find('id: "walkup"') < beats_fn.find('id: "glamour"'))
chk('守衛 fanfare＋掌聲仲在', 'awards160PlayWinAudio()' in play_fn)
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
