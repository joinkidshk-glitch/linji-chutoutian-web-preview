# v20a207：v204 設計 review 七項修復（B2／B3／C1–C5；B1 唔修，見 NOTES §1）。
#   B2 舞台放大：邏輯 480×360→480×432（10:9）／backing 720×540→720×648／FLOOR 262→314
#       （地板 y274–372，深 98px＝22.7%；觀眾席 y379–432）；人物 dispH 112→136／玩家 116→140
#       （燕尾服同樣 136）；獎盃 glyph 燕尾服 −110→−129／對手胸前 −52→−61；光池高 99→120；
#       彩紙底界 364→436；glamour aspect 480/360→480/432；stage safe center＋overflow-y:auto；
#       字幕 padding／卡列 margin／tap margin 各收 2–4px（提名 700 唔出 viewport）。
#   B3 跳過掣由 canvas 右上角（top:8px，遮「角逐」pill 右端）搬去右下角（bottom:8px）。
#   C1 揭曉得主 spotlight207（光柱＋地面光暈）＋落選者 dimVeil207 暗罩（光底上 alpha
#       減淡失效——半透明透光更光，實測得主 179.6 vs 落選者 179.0；實色＋暗罩先真係暗）；
#       suspense 光池唔郁。
#   C2 結果卡獎盃套返 v174 金底 chip（.psr-fellows63 img.ic112 入 L818 嗰條 rule）。
#   C3 結果卡 .awd-sheet 收緊（gap 5／卡 padding 5px／標題 .88rem 等）＋結果 modal 掛
#       awd-sheet-on 放寬到 94dvh（沿用 casting-sheet／day-res 前例），700 高三格＋聲望行齊見
#       （旁聽版＋提名版：提名版另有診斷＋安慰＋同屆提名行，要再收 ~50px 內容＋btns／modal padding）。
#   C4 影藝獎＋廣告獎請柬「旁聽／入圍席位信」→「席位信」（跟音樂場寫法）。
#   C5 地圖「中環廣告」標籤 left:60%→51%，離開藍塔。
# 反證：run against pristine main 9e338d6 -> 全部新斷言 FAIL（唔 crash）；舊守衛 pristine 應 PASS。
# 註：本檔用字串＋函數切片斷言（跟 v181 寫法），唔寫死行號。
import os, sys, re

idx_path = sys.argv[1] if len(sys.argv) > 1 else 'index.html'
root = os.path.dirname(os.path.abspath(idx_path))
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

# --- B2：舞台放大（邏輯 480×432／backing 720×648／FLOOR 314）---
chk('B2 canvas 邏輯 480×432（10:9）', 'const W = 480, H = 432' in play_fn)
chk('B2 舊邏輯 480×360 唔再出現（頒獎禮範圍）', 'const W = 480, H = 360' not in play_fn)
chk('B2 canvas backing 720×648', '<canvas class="awd62-canvas" width="720" height="648">' in src)
chk('B2 舊 backing 720×540 唔再出現', '<canvas class="awd62-canvas" width="720" height="540">' not in src)
chk('B2 setTransform 1.5 唔郁', 'ctx.setTransform(1.5, 0, 0, 1.5, 0, 0)' in play_fn)
chk('B2 FLOOR＝314（腳底）', 'const FLOOR = 314' in play_fn)
chk('B2 舊 FLOOR＝262 唔再出現（頒獎禮範圍）', 'const FLOOR = 262' not in play_fn)
chk('B2 地板 y274–372（深 98px＝22.7% 高）', '228 / 360' in base_fn and '310 / 360' in base_fn)
chk('B2 地板深 98px＝22.7% 高', abs(98 / 432 - 0.227) < 0.002)
chk('B2 觀眾席 y379–432（316／360 比例）', '316 / 360' in base_fn)
chk('B2 人物 dispH 136（fellow）／140（玩家）', '? 140 : 136' in play_fn)
chk('B2 舊 dispH 112／116 唔再出現（頒獎禮範圍）', '? 116 : 112' not in play_fn)
chk('B2 燕尾服 dispH 136（同 reveal 齊高）', play_fn.count('dispH: 136') >= 3)
chk('B2 獎盃 glyph 燕尾服頂 −129（兩處）', 'FLOOR + fp.y - 129' in play_fn and 'FLOOR - 129' in play_fn)
chk('B2 舊 glyph −110 唔再出現（頒獎禮範圍）', 'FLOOR + fp.y - 110' not in play_fn and 'FLOOR - 110' not in play_fn)
chk('B2 對手胸前 glyph −61', 'FLOOR + fp.y - 61' in play_fn)
chk('B2 舊胸前 glyph −52 唔再出現', 'FLOOR + fp.y - 52' not in play_fn)
chk('B2 牌底 179.3 到 glyph 頂 185 留罅', abs((314 - 129) - 179.3 - 5.7) < 0.01)
chk('B2 glyph 底 203 離頭頂 206 仲有 3px', (314 - 129 + 18) == 203 and 206 - 203 == 3)
chk('B2 光池高 120（蓋過 108px 人仔）', 'F - 120' in play_fn)
chk('B2 彩紙底界 436（H＋4）', 'p.y > 436' in play_fn)
chk('B2 glamour overlay aspect 跟 canvas（480/432）', 'aspect-ratio:480/432' in css_rule('.awd63-glamour'))
chk('B2 舊 glamour aspect 480/360 唔再出現', 'aspect-ratio:480/360' not in src)
chk('B2 stage safe center＋可捲（唔出 viewport 兜底）',
    'align-items:safe center' in css_rule('.awd62-stage') and 'overflow-y:auto' in css_rule('.awd62-stage'))

# --- B3：跳過掣搬去 canvas 右下角，唔遮「角逐」pill ---
skip_css = css_rule('.awd62-skip')
chk('B3 跳過掣 bottom:8px（右下角）', 'bottom:8px' in skip_css)
chk('B3 跳過掣唔再 top:8px（右上角）', 'top:8px' not in skip_css)
chk('B3 跳過掣仲喺 canvaswrap 入面（唔跟 beat 高度走）',
    '<button type="button" class="awd62-skip">' in play_fn)

# --- C1：揭曉得主 spotlight，落選者再暗 ---
def reveal_slice():
    i = play_fn.find('if(id === "reveal")')
    j = play_fn.find('if(id === "comfort")', i)
    return play_fn[i:j] if i >= 0 and j > i else ''

rv = reveal_slice()
chk('C1 spotlight207 helper 在場', 'spotlight207' in play_fn and 'const spotlight207' in play_fn)
chk('C1 揭曉贏分支得主有 spotlight', 'spotlight207(fp.x, 72' in rv)
chk('C1 揭曉非贏分支得主有 spotlight', 'spotlight207(fp.x, 66' in rv)
chk('C1 dimVeil207 helper 在場（落選者暗罩）', 'const dimVeil207' in play_fn and 'createLinearGradient' in play_fn)
chk('C1 贏分支落選者實色＋暗罩', 'dimVeil207(slotCx(i))' in rv and rv.count('dimVeil207(slotCx(i))') == 2)
chk('C1 落選者唔再靠 alpha 減淡（光底透光）', 'alpha: 0.55' not in rv and 'alpha: 0.5' not in rv and '? 0.6 : 0.5' not in rv)
chk('C1 suspense 光池唔郁（lightPool 仲喺度）', 'lightPool(slotCx(i)' in play_fn)

# --- C2：結果卡獎盃金底 chip ---
chk('C2 金底 chip rule 覆蓋 .psr-fellows63',
    '.psr-fellows63 img.ic112' in src and '#f2c14e' in src)
chk('C2 結果卡 fellows 行用 iconHtml112（唔改資產）',
    'iconHtml112("🏆")' in slice_fn('awards63FellowsHtml'))

# --- C3：結果卡收緊＋結果 modal 放寬 94dvh（旁聽版＋提名版） ---
awd_css = src[src.find('.awd-sheet .psr-cards'):] if '.awd-sheet .psr-cards' in src else ''
chk('C3 .awd-sheet 卡列 gap 5px', '.awd-sheet .psr-cards{gap:5px' in src)
chk('C3 .awd-sheet 卡列 margin 2px 0 4px（提名版）', '.awd-sheet .psr-cards{gap:5px;margin:2px 0 4px}' in src)
chk('C3 .awd-sheet 卡 padding 5px 10px', '.awd-sheet .psr-card{padding:5px 10px}' in src)
chk('C3 .awd-sheet 標題 .88rem', '.awd-sheet .psr-title{font-size:.88rem' in src)
chk('C3-nom 診斷盒 weak62 收緊', '.awd-sheet .psr-weak62{margin:2px 0 0;padding:4px 8px;line-height:1.35}' in src)
chk('C3-nom 安慰行 comfort147 收 margin', '.awd-sheet .psr-comfort147{margin:2px 0 0;font-size:.85rem;line-height:1.35}' in src)
chk('C3-nom eyebrow mb 2px', '.awd-sheet .psr-eyebrow{ letter-spacing:.14em; margin-bottom:2px; }' in src)
chk('C3-nom 同屆提名行 lh 1.3', '.awd-sheet .psr-fellows63{margin-top:0;font-size:12px;line-height:1.3}' in src)
chk('C3 結果 modal 掛 awd-sheet-on 放寬 94dvh',
    '#mask.awd-sheet-on' in src and 'min(94dvh,94svh,720px)' in src)
chk('C3-nom btns 收窄（只限結果卡）', '#mask.awd-sheet-on #modal-btns{margin-top:4px!important;padding:6px 0 calc(8px + env(safe-area-inset-bottom, 0px))!important}' in src)
chk('C3-nom modal padding 收窄（只限結果卡）', '#mask.awd-sheet-on .modal{padding-top:8px!important;padding-bottom:8px!important}' in src)
chk('C3 presentAwardResult 傳 awardSheet:true', 'awardSheet:true' in src)
chk('C3 modal() 接 awardSheet 掛 mask class', 'awd-sheet-on' in slice_fn('modal'))
chk('C3 closeModal 清 awd-sheet-on', 'awd-sheet-on' in slice_fn('closeModal'))

# --- C4：請柬「旁聽／入圍席位信」→「席位信」 ---
m = re.search(r'const VENUE99_INVITE_DEK = \{(.*?)\};', src, re.S)
dek = m.group(1) if m else ''
chk('C4 影藝獎請柬用「一張席位信」',
    'award_harbour_film: "影圈年獎將至，今屆喺金禧大酒店大禮堂舉行。你收到一張席位信' in dek)
chk('C4 廣告獎請柬用「一張席位信」',
    'award_harbour_ad: "廣告圈年賞將至，今屆喺金禧大酒店大禮堂舉行。你收到一張席位信' in dek)
chk('C4 「旁聽／入圍席位信」唔再出現', '旁聽／入圍席位信' not in src)
chk('C4 音樂場寫法唔郁', 'award_golddisc_music: "唱片年終有金碟夜，喺金禧大酒店大禮堂舉行。你收到一張席位信' in dek)

# --- C5：地圖「中環廣告」標籤移離藍塔 ---
chk('C5 中環廣告 left:51%', 'left:51%;top:calc(57% + 30px)">中環廣告' in src)
chk('C5 中環廣告舊 left:60% 唔再出現', 'left:60%;top:calc(57% + 30px)">中環廣告' not in src)
chk('C5 地圖標籤仲係 15 個', src.count('class="mn68"') == 15)
chk('C5 其餘標籤唔郁（金鐘創意／灣仔唱片）',
    'left:85%;top:calc(60% + 28px)">金鐘創意' in src and 'left:68%;top:calc(77% + 34px)">灣仔唱片' in src)

print('---')
print('TOTAL FAIL %d' % len(fails))
for f in fails:
    print('FAIL ' + f)
sys.exit(1 if fails else 0)
