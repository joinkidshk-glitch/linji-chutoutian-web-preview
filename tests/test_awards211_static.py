# v20a211：v207 設計 review 七項修復（A1＋B1＋B2＋C1–C3＋B7）。
#   A1 結果卡開出嗰刻收起 toast（hideToast211；開卡後唔再叫 toast()——嗰句就係遮住 700 提名版眉題嘅元兇）。
#   B1 高 viewport（≥850px，即 932）舞台加高 480×540（×1.25），矮 viewport（700）留返 480×432——
#       700 提名版 frame 已經 644px，canvas 再高會頂爆 viewport；FLOOR／人物／光池／glyph／閃粉全部按 HSC211 換算。
#   B2 won 版銷量卡點名得主＋作品（win211：won 類別攞玩家＋代表作，動態，唔寫死）。
#       v20a214 適配：結果卡改做《維港日報》報紙，第二版用 playerWinLine214／winLine214／metricHead214；
#       wonCat211／win211／「典禮後仍有人提起」stub 全部退役（見 B2 段）。
#   C1 won 版同屆提名加玩家一行「阿偉《代表作》🏆」＋圖例（金底 chip 同 v207 C2 一致）。
#       v20a214 適配：★統一＋全名，改做「★ 陳偉翔《代表作》」＋「★為得主」圖例（見 C1 段）。
#   C2 字幕框高度釘死 93px（3 行上限；基線 names 69／reveal 54–93 來回跳令 frame 跳 7–12px）。
#   C3 gallery 請柬席位去重（tierBit 唔出，留返 gate 行「今晚席位：觀禮。」；nominee 保留 tierBit）。
#   B7 揭曉 spotlight 改做由上射落嚟嘅梯形光柱（上窄下闊、y=0 到腳底、暖白漸變＋亮芯＋腳底光灘）；dimVeil207 不動。
# 反證：run against pristine main b7ddb37 -> 全部新斷言 FAIL（唔 crash）；舊守衛 pristine 應 PASS。
# 註：本檔用字串＋函數切片斷言（跟 v207 寫法），唔寫死行號。
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

def strip_comments(s):
    # v20a214 rebase 適配：斷言嗰陣先剝走 /* */ 註解——註解入面提到嘅舊字串（例如 stub「典禮後仍有人提起」）唔係 code，唔剝會誤判
    return re.sub(r'/\*[\s\S]*?\*/', '', s)

play_fn = slice_fn('awards62PlayCeremony')
res_fn = slice_fn('renderAwardResultHtml')
inv_fn = slice_fn('renderAwardInviteHtml')
fel_fn = slice_fn('awards63FellowsHtml')
toast_fn = slice_fn('toast')
pres_fn = slice_fn('presentAwardResult')

# --- A1：結果卡開出嗰刻收起 toast ---
chk('A1 hideToast211 在場（清計時＋class＋children＋aria）',
    'function hideToast211(' in src and 'clearTimeout(toast._t)' in slice_fn('hideToast211')
    and 'classList.remove("on","has-stamp","has-sub")' in slice_fn('hideToast211'))
chk('A1 presentAwardResult 開卡前收起 toast', 'hideToast211()' in pres_fn)
chk('A1 presentAwardResult 唔再開卡後叫 toast()', 'toast((pack.displayName' not in pres_fn)
chk('A1 toast() 本身唔郁（1.8s timer 仲在）', '},1800);' in toast_fn and 'toast._t=setTimeout' in toast_fn)
chk('A1 hideToast211 唔係靠縮 cap／加 padding（結果 modal 94dvh 唔郁）',
    'min(94dvh,94svh,720px)' in src)

# --- B1：高 viewport 舞台 480×540，矮 viewport 留 480×432 ---
chk('B1 HS211 門檻 innerHeight ≥850 → 540，否則 432',
    'window.innerHeight >= 850) ? 540 : 432' in play_fn)
chk('B1 HSC211＝HS211/432 換算比在場', 'const HSC211 = HS211 / 432' in play_fn)
chk('B1 draw() H 跟 HS211', 'const W = 480, H = HS211' in play_fn)
chk('B1 canvas backing 高動態（432→648／540→810）', 'Math.round(HS211 * 1.5)' in play_fn)
chk('B1 舊 backing 720×648 寫死唔再出現', '<canvas class="awd62-canvas" width="720" height="648">' not in src)
chk('B1 FLOOR 按 HSC211 換算（314→393）', 'const FLOOR = Math.round(314 * HSC211)' in play_fn)
chk('B1 人物 dispH 按 HSC211 換算（136／140→170／175）',
    'Math.round(140 * HSC211)' in play_fn and 'Math.round(136 * HSC211)' in play_fn)
chk('B1 燕尾服 dispH 全部按 HSC211 換算（5 處）', play_fn.count('dispH: Math.round(136 * HSC211)') >= 5)
chk('B1 glyph 頂按 HSC211 換算（-129／-61）',
    'FLOOR + fp.y - Math.round(129 * HSC211)' in play_fn and 'FLOOR + fp.y - Math.round(61 * HSC211)' in play_fn
    and 'FLOOR - Math.round(129 * HSC211)' in play_fn)
chk('B1 光池高按 HSC211 換算（120→150）', 'F - Math.round(120 * HSC211)' in play_fn)
chk('B1 彩紙底界跟 HS211（H＋4）', 'p.y > HS211 + 4' in play_fn)
chk('B1 glamour overlay aspect 跟 HS211（CSS 480/432 留做短 viewport 後備）',
    "aspect-ratio:480/' + HS211" in play_fn and 'aspect-ratio:480/432' in css_rule('.awd63-glamour'))
chk('B1 闊度唔郁（W 480／slotCx 間距 120／setTransform 1.5）',
    'const W = 480' in play_fn and '* 120' in play_fn and 'ctx.setTransform(1.5, 0, 0, 1.5, 0, 0)' in play_fn)
chk('B1 地板比例唔郁（drawBase 仍按 H/360 換算，地板深 22.7%）',
    'H * 228 / 360' in slice_fn('awards181DrawBase') and 'H * 310 / 360' in slice_fn('awards181DrawBase'))
chk('B1 觀眾暗帶唔加唔減（drawBase 316/360 仲在，冇新觀眾席／剪影帶）',
    '316 / 360' in slice_fn('awards181DrawBase') and '觀眾席' not in play_fn.replace('暗觀眾席', ''))

# --- B2：won 版銷量卡點名得主＋作品（v20a214 適配：結果卡改做報紙，第二版用真得主數據） ---
chk('B2 won 版第二版點名玩家＋代表作（動態，唔寫死作品名）',
    'playerWinLine214' in res_fn and '陳偉翔憑《' in res_fn
    and 'rep214' in res_fn and 'wonCat211' not in res_fn)
chk('B2 第二版用真得主數據（metricHead214＝winLine214 || playerWinLine214）',
    'metricHead214' in res_fn and 'winLine214 || playerWinLine214' in res_fn)
chk('B2 winLine214 跌返 win149（gallery／提名版對手得主唔郁）',
    'const winLine214' in res_fn and 'awardWinLine149(win149)' in res_fn)
chk('B2 冇得主先跌返散場句，stub「典禮後仍有人提起」唔再出現（註解先剝走，唔係誤判）',
    '典禮後仍有人提起' not in strip_comments(res_fn) and '散場' in strip_comments(res_fn))
chk('B2 awardWinner149 本身唔郁（won 回 null 係既定規則）',
    'if(f.outcome === "won") return null;' in slice_fn('awardWinner149'))

# --- C1：won 版同屆提名加玩家一行（v20a214 適配：★＋全名陳偉翔） ---
chk('C1 won 版加玩家一行（★ 陳偉翔＋代表作，排第一）',
    'isWon211' in fel_fn and 'parts.unshift("★ 陳偉翔"' in fel_fn
    and 'c.repWorkTitle' in fel_fn)
chk('C1 won 版行首有圖例（為得主）', '(win || isWon211)' in fel_fn)
chk('C1 gallery／提名版 fellows 邏輯唔郁（winner63／fellows[0] fallback 仲在）',
    'c.winner63 || ((c.outcome === "gallery" && fl[0]) ? fl[0] : null)' in fel_fn)

# --- C2：字幕框高度釘死 93px ---
cap_css = css_rule('.awd62-caption')
chk('C2 字幕框高度釘死 93px', 'height:93px' in cap_css)
chk('C2 舊 min-height:54px 唔再出現（字幕框）', 'min-height:54px' not in cap_css)
chk('C2 空字幕 beat display:none 維持（walkup／glamour 跳位係 v174 已接受 trade-off）',
    'capEl.style.display' in play_fn)
chk('C2 卡列留位唔郁（visibility:hidden＋glamour-hide display:none 仲在）',
    '.awd63-cards{display:flex' in src and 'glamour-hide' in play_fn)

# --- C3：gallery 請柬席位去重 ---
chk('C3 gallery 唔出 tierBit（留返 gate 行）', '(pack.tier === "gallery") ? ""' in inv_fn)
chk('C3 nominee 保留 tierBit（席位：入圍／提名）', '席位：${pack.tierLabel}' in inv_fn)
chk('C3 gate 行「今晚席位：觀禮。」仲在', '今晚席位：觀禮。' in slice_fn('awards62GateLineHtml'))
chk('C3 請柬其餘行唔郁（席位信／獎項行／代表作行）',
    '席位信' in src and '今晚獎項' in inv_fn and 'awards63InviteBitHtml(pack)' in inv_fn)

# --- B7：揭曉光柱改做梯形（上窄下闊、框頂到腳底） ---
def spot_slice():
    i = play_fn.find('const spotlight207')
    j = play_fn.find('const dimVeil207', i)
    return play_fn[i:j] if i >= 0 and j > i else ''
sp = spot_slice()
chk('B7 spotlight207 仲在（簽名唔郁，呼叫點唔使改）', 'const spotlight207 = (cx, w, fy)' in play_fn)
chk('B7 梯形光柱：上窄（topW＝w×0.5）下闊（botW＝w＋44）',
    'topW211' in sp and 'Math.round(w * 0.5)' in sp and 'botW211 = w + 44' in sp)
chk('B7 光柱由框頂 y=0 起（moveTo y=0）', 'moveTo(cx - topW211 / 2, 0)' in sp and 'lineTo(cx + topW211 / 2, 0)' in sp)
chk('B7 光柱到底 F（腳底）', 'lineTo(cx + botW211 / 2, F)' in sp and 'lineTo(cx - botW211 / 2, F)' in sp)
chk('B7 暖白縱向漸變（createLinearGradient 0→F）',
    'createLinearGradient(0, 0, 0, F)' in sp and 'rgba(255,244,200,0.42)' in sp)
chk('B7 中央亮芯梯形（方向感）', 'g211b' in sp and 'topW211 * 0.28' in sp)
chk('B7 腳底光灘仲在（光池＋地面光暈）',
    'F - Math.round(120 * HSC211)' in sp and 'rgba(255,217,104,0.45)' in sp)
chk('B7 舊直身光柱唔再出現', 'fillRect(cx - w / 2 - 14, 40, w + 28, F - 40)' not in play_fn)
chk('B7 呼叫點唔郁（won 72／非贏 66，跟 fp.x）',
    'spotlight207(fp.x, 72' in play_fn and 'spotlight207(fp.x, 66' in play_fn)
chk('B7 dimVeil207 落選者暗罩一字唔郁（0.45 中段＋漸隱邊）',
    'const dimVeil207' in play_fn and 'rgba(10,6,20,0.45)' in play_fn)
chk('B7 suspense 照舊 lightPool（唔用光柱）', 'lightPool(slotCx(i)' in play_fn)

print('---')
print('TOTAL FAIL %d' % len(fails))
for f in fails:
    print('FAIL ' + f)
sys.exit(1 if fails else 0)
