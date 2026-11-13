# v20a181：頒獎禮舞台按參考圖重建成橫向闊舞台＋人物換 PixelLab character。
# 設計（見 NOTES_V20A181.md §1–§2）：canvas 邏輯 480×360（4:3）／backing 720×540／setTransform 1.5；
#   (a) 橫向呈現：撐滿框冇黑帶（canvas width:100%＋height:auto，frame min(96vw,760px) 唔郁）。
#   (b) 佈局跟參考圖：頂部啡金橫額（DOM，典禮名）／左右兩格黃色數字條（DOM，聲望 S.fame／角逐
#       pack.categories 項數）／中央大白牌（DOM，焦點獎項名）＋牌下兩行黃字（代表作／會場名）／
#       淺色幕布＋平木地板 y200–334（深 134px＝37.2% 高）＋深木前緣＋暗觀眾席 y340–360／
#       左右簡化深色燈架／人物左／中／右分開企（4 slots 60／180／300／420，罅 78px；gallery 75／240／405）。
#   (c) 人物：PixelLab character 幀 px_<starId>_<dir>.png（south 企立／east／west 行入場跟方向；
#       12 人 × 3 向，全部腳底 y115 對齊 v180 錨；dispH 112，人物約 89px＝框高四分一；燕尾服同樣 112）。
#   (d) 舊 Q 版成批清走：AWARDS64_SPRITES（34 張 base64）＋loadSpr／drawSpr 路徑一併刪，唔留 fallback；
#       載唔到 px 圖畫中性剪影（PixelLab 比例頭＋身）。
#   (e) M1 實景底圖＋M4 walkup GIF 一併退役：舞台改程式繪製 awards181DrawBase（fallback 同一個）；
#       walkup beat 改由 canvas 畫（阿偉 px east 幀由台左行到中央，1400ms 行完，換燕尾服捧杯）。
# 唔郁守衛：6 beats＋walkup 2200ms＋彩紙 M5＋fanfare／掌聲＋跳過掣＋glamour 燕尾服＋卡列／字幕；
#   fellows 池（上限 3＋阿偉＝4 卡）／對手加權／贏線 0.875／comfort beat／報紙流程唔郁。
# 反證：run against pristine main 91f264a -> 新幾何／px／清走斷言全部 FAIL（唔 crash）；唔郁守衛 pristine 應 PASS。
# 註：本檔用字串＋函數切片斷言（跟 v177 寫法），唔寫死行號；rebase 漂移用 difflib 對位先改。
import os, sys, re
from PIL import Image

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
fb_fn = slice_fn('awards62FallbackStage')
base_fn = slice_fn('awards181DrawBase')
beats_fn = slice_fn('awards62CeremonyBeats')

WON = [60, 180, 300, 420]
GAL = [75, 240, 405]
FIG_W = 46          # px 人物顯示闊上限（dispH 112 × 最闊 48/128 ≈ 42，取 46 留鬆）
FLOOR = 262

# --- (a) 橫向呈現：480×360（4:3）／backing 720×540／setTransform 1.5 ---
chk('canvas 邏輯 480×360（4:3）', 'const W = 480, H = 360' in play_fn)
chk('舊邏輯 424×360 唔再出現（頒獎禮範圍）', 'const W = 424, H = 360' not in play_fn)
chk('canvas backing 720×540', '<canvas class="awd62-canvas" width="720" height="540">' in src)
chk('舊 backing 636×540 唔再出現', 'width="636" height="540"' not in src)
chk('setTransform 1.5 唔郁', 'ctx.setTransform(1.5, 0, 0, 1.5, 0, 0)' in play_fn)
chk('canvas 撐滿框冇黑帶（width:100%＋height:auto）', 'canvas.awd62-canvas{display:block;width:100%;height:auto' in src)
chk('glamour overlay aspect 跟 canvas（480/360）', 'aspect-ratio:480/360' in css_rule('.awd63-glamour'))

# --- (b) 佈局：橫額／數字條／白牌（DOM 層）＋程式舞台（canvas 層） ---
chk('橫額 DOM 在場（.awd181-banner）', 'awd181-banner' in play_fn and 'awd181-banner{' in src)
chk('橫額字＝典禮名（pack.displayName）', 'esc((pack && pack.displayName)' in play_fn)
chk('esc 係 playCeremony local alias（唔係裸用外層 esc，否則 ReferenceError 即死）',
    'const esc = (typeof esc59 === "function") ? esc59' in play_fn)
chk('左數字條 DOM 在場（.awd181-strip.l）', 'awd181-strip l' in play_fn)
chk('左數字條＝聲望（S.fame 即時值）', 'Number(S.fame)' in play_fn and '聲望' in play_fn)
chk('右數字條 DOM 在場（.awd181-strip.r）', 'awd181-strip r' in play_fn)
chk('右數字條＝角逐（pack.categories 項數）', 'pack.categories' in play_fn and '角逐' in play_fn and 'awd181Noms' in play_fn)
chk('數字條唔抄參考圖字（Hype／Popular 唔出現）', 'Hype' not in play_fn and 'Popular' not in play_fn)
chk('白牌 DOM 在場（.awd181-board）', 'awd181-board' in play_fn)
chk('白牌字＝焦點獎項名（focus.label）', 'focus && focus.label' in play_fn)
chk('白牌唔抄參考圖字（Star Venture 唔出現）', 'Star Venture' not in src)
chk('白牌內細字兩行（代表作／會場名，搬入白牌）', 'awd181-sub' in play_fn and 'awd181Line1' in play_fn and 'awd181Line2' in play_fn)
chk('白牌細字唔抄 First appearance', 'First appearance' not in src)
chk('文字層全部 pointer-events:none（撳畫面快進照通）', 'pointer-events:none' in css_rule('.awd181-banner') and 'pointer-events:none' in css_rule('.awd181-sub'))

# --- (b1) 黃字 fix：兩行字搬入白牌，唔再獨立放 43.5% 人頭高度 ---
# 實測根因（2026-11-13 探針，932 won names）：sub 框 y239–327（顯示 px）vs 人頭頂 y265
#   （canvas 頂 −10＋173 邏輯×572/360）；舊 top:43.5% 係對 canvaswrap 高 572 計（唔係成個 frame 865），
#   但就算對 canvas 計，兩行字 156.6–212.6 邏輯都同頭頂 173 邏輯重疊 40 邏輯——位置本身就係人頭高度。
# 修法：白牌改三行牌（獎項名＋代表作＋會場名），白牌底唔郁（149.4 邏輯＜glyph 頂 150＜頭頂 173）。
def _pct(rule, prop):
    m = re.search(prop + r':\s*([\d.]+)%', rule)
    return float(m.group(1)) if m else None
board_rule = css_rule('.awd181-board')
board_top = _pct(board_rule, 'top'); board_h = _pct(board_rule, 'height')
chk('黃字 fix：舊 top:43.5% 獨立字行已撤（CSS 唔再有 top:43.5%）', 'top:43.5%' not in src)
chk('黃字 fix：細字係白牌入面嘅 span（board div 包住 awd181-t＋awd181-sub 先閂）',
    '<span class="awd181-t">' in play_fn and '<span class="awd181-sub">' in play_fn
    and play_fn.find('awd181-board') < play_fn.find('awd181-sub')
    and '</span></div>' in play_fn[play_fn.find('awd181-sub'):])
chk('黃字 fix：白牌底唔過獎盃 glyph 頂（top＋height＝41.5%→149.4 邏輯＜150）',
    board_top is not None and board_h is not None and round((board_top + board_h) * 3.6, 1) == 149.4)
chk('黃字 fix：白牌底唔過人頭頂（149.4 邏輯＜173）',
    board_top is not None and board_h is not None and (board_top + board_h) * 3.6 < 173)
chk('黃字 fix：白牌頂唔撞數字條（top 21%→75.6 邏輯＞數字條底 20%＝72）',
    board_top is not None and board_top * 3.6 > 72)
# 三行內容塞得入白牌（邏輯 px 計：1cqw＝4.78 邏輯；標題 5.4cqw×lh1.15＋細字 3.0cqw×lh1.3×2 行＋margin .3cqw ≤ 牌高 73.8）
def _cqw(rule, prop):
    m = re.search(prop + r':[^;]*?([\d.]+)cqw', rule)
    return float(m.group(1)) if m else None
def _lh(rule):
    m = re.search(r'line-height:\s*([\d.]+)', rule)
    return float(m.group(1)) if m else None
t_rule = src[src.find('.awd181-board .awd181-t{'):src.find('}', src.find('.awd181-board .awd181-t{')) + 1]
s_rule = css_rule('.awd181-sub')
CQW_LOGIC = 4.78
stack = (_cqw(t_rule, 'font-size') or 0) * CQW_LOGIC * (_lh(t_rule) or 1) \
    + 2 * (_cqw(s_rule, 'font-size') or 0) * CQW_LOGIC * (_lh(s_rule) or 1) \
    + 0.3 * CQW_LOGIC
chk('黃字 fix：牌內三行總高 ≤ 白牌高（%.1f ≤ %.1f 邏輯）' % (stack, (board_h or 0) * 3.6),
    board_h is not None and stack <= board_h * 3.6)
# 細字喺白牌底色上面要夠對比（深啡 #7c4f22 vs 米白 #fdfbf5，WCAG 對比 ≥4.5）
def _lum(hexs):
    r, g, b = (int(hexs[i:i + 2], 16) / 255 for i in (0, 2, 4))
    f = lambda c: c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = f(r), f(g), f(b)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b
_m = re.search(r'\.awd181-sub\{[^}]*color:\s*#([0-9a-fA-F]{6})', src)
_sub_lum = _lum(_m.group(1)) if _m else 0
_contrast = (_lum('fdfbf5') + 0.05) / (_sub_lum + 0.05) if _m else 0
chk('黃字 fix：牌內細字夠對比（#7c4f22 on #fdfbf5，對比 %.1f ≥ 4.5）' % _contrast, _contrast >= 4.5)
chk('黃字 fix：細字唔再係黃色（#ffe14d 唔喺 .awd181-sub）', '#ffe14d' not in s_rule)
chk('黃字 fix：.long 條件覆蓋長細字行（細字行 ＞10 字都縮）',
    'awd181Line1).length > 10' in play_fn and 'awd181Line2).length > 10' in play_fn)
chk('程式舞台函數在場', 'function awards181DrawBase(ctx, W, H, off)' in src)
chk('地板 y200–334（#d9a75f）', '#d9a75f' in base_fn and '200, W + 16, 134' in base_fn)
chk('地板深 134px＝37.2% 高（下半約四成）', 'const FLOOR = 262' in play_fn and 'const W = 480, H = 360' in play_fn)
chk('地板前緣深木邊 y334（#5a3a1e）', '#5a3a1e' in base_fn and '334, W + 16, 6' in base_fn)
chk('暗觀眾席 y340–360（#120c20）', '#120c20' in base_fn and '340, W + 16, 20' in base_fn)
chk('淺色幕布（#f2e8d5）', '#f2e8d5' in base_fn)
chk('幕布唔抄淺綠格仔花紋（#f2e8d5 淺米，唔係綠格）', '#f2e8d5' in base_fn)
chk('燈架深色鐵架左右（#23232c，x12／452）', '#23232c' in base_fn)
chk('後備舞台＝同一個程式舞台', 'awards181DrawBase(ctx, W, H, 0)' in fb_fn)
chk('draw() 畫程式舞台（唔再畫 bgImg）', 'awards181DrawBase(ctx, W, H,' in play_fn and 'drawImage(bgImg' not in play_fn)
chk('pan beat 橫移程式舞台（±6）', 'Math.round(Math.sin(tick * 0.45) * 6)' in play_fn)

# --- (b2) 企位：左／中／右分開企，中間大段空地板 ---
chk('FLOOR＝262（腳底）', 'const FLOOR = 262' in play_fn)
chk('舊 FLOOR＝250 唔再出現（頒獎禮範圍）', 'const FLOOR = 250' not in play_fn)
chk('FLOOR 只定義一次', play_fn.count('const FLOOR =') == 1)
chk('4 slots 60／180／300／420（間距 120，置中 240）', '240 + (i - (slots.length - 1) / 2) * 120' in play_fn)
chk('gallery 3 slots 75／240／405', '[75, 240, 405]' in play_fn)
chk('4 slots 唔出 canvas 界', WON[0] - FIG_W // 2 >= 0 and WON[-1] + FIG_W // 2 <= 480)
chk('gallery 唔出 canvas 界', GAL[0] - FIG_W // 2 >= 0 and GAL[-1] + FIG_W // 2 <= 480)
chk('4 slots 相鄰罅 ≥70px（大段空地板）', all(WON[i+1] - WON[i] - FIG_W >= 70 for i in range(3)))
chk('gallery 相鄰罅 ≥100px', all(GAL[i+1] - GAL[i] - FIG_W >= 100 for i in range(2)))
chk('入場由台側行入（from -40／520，界外起步）', 'p.from = side < 0 ? -40 : 520' in play_fn)
chk('入場分流界＝240（中央）', 'slotCx(i) <= 240 ? -1 : 1' in play_fn)
chk('行前向中央 240 集中（舊 212 唔再出現）', '(240 - cx0) * 0.22' in play_fn and '(212 - cx0)' not in play_fn)
chk('行前腳 FLOOR＋10＝272', 'y: Math.round(10 * p)' in play_fn)
chk('drawFigure 腳底跟 FLOOR（唔寫死）', 'const fy = FLOOR + (o.y || 0)' in play_fn)

# --- (c) 人物：PixelLab character 幀 ---
chk('px 預載函數在場（loadPx）', 'const loadPx = (starId, dir)' in play_fn)
chk('px 路徑格式 px_<starId>_<dir>.png', '"assets/story/awards/px_" + starId + "_" + dir + ".png"' in play_fn)
chk('企立預載 south／行預載 east／west', '["south", "east", "west"].forEach(d=> loadPx("awei", d))' in play_fn)
chk('對手三向齊預載（starId 有先載）', 'if(f.starId) ["south", "east", "west"].forEach(d=> loadPx(f.starId, d))' in play_fn)
chk('drawPx 在場（腳底 115/128）', 'const drawPx = (starId, dir, cx, floorY, dispH)' in play_fn and 'floorY - dispH * 115 / 128' in play_fn)
chk('企立用 south 幀（預設 dir south）', '? o.frame : "south"' in play_fn or 'o.frame : "south"' in play_fn)
chk('行幀跟方向（east／west，唔再 walkA／walkB）', '"east"' in play_fn and '"west"' in play_fn and 'frame: (tick % 2)' not in play_fn)
chk('入場行幀跟 side（左入 east／右入 west）', 'frame: (p.side < 0) ? "east" : "west"' in play_fn)
chk('人物 dispH 112（fellow）／116（玩家）', '? 116 : 112' in play_fn)
chk('人物高約 89px＝框高四分一（112×102/128）', 88 <= round(112 * 102 / 128) <= 90)
chk('燕尾服 dispH 112（同 reveal 齊高）', play_fn.count('dispH: 112') >= 3)
chk('燕尾服腳底 115/128 唔郁', 'dispH * 115 / 128' in play_fn)
chk('獎盃 glyph 燕尾服頂 −112', 'FLOOR + fp.y - 112' in play_fn)
chk('獎盃 glyph 對手胸前 −52', 'FLOOR + fp.y - 52' in play_fn)
chk('舊 glyph −96／−39 唔再出現', 'FLOOR + fp.y - 96' not in play_fn and 'FLOOR + fp.y - 39' not in play_fn)

# --- (c2) px 資產：36 檔齊，128×128，腳底 y115 ---
PX_DIR = os.path.join(root, 'assets', 'story', 'awards')
IDS = ['awei', 'luk_baakyin', 'liu_bingxing', 'chai_zanhoi', 'mak_zhendong', 'lok_gasing',
       'chung_choning', 'so_jiyan', 'ngai_wingnaam', 'gu_mingfai', 'yip_manji', 'ko_chunkit']
missing = []
bad_geo = []
for sid in IDS:
    for d in ('south', 'east', 'west'):
        p = os.path.join(PX_DIR, 'px_%s_%s.png' % (sid, d))
        if not os.path.isfile(p):
            missing.append(p)
            continue
        im = Image.open(p).convert('RGBA')
        bb = im.getchannel('A').getbbox()
        h = bb[3] - bb[1] if bb else 0
        if im.size != (128, 128) or not bb or bb[3] != 115 or not (99 <= h <= 103):
            bad_geo.append((os.path.basename(p), im.size, bb, h))
chk('px 36 檔齊（12 人 × 3 向）', not missing)
chk('px 全部 128×128、腳底 y115、高 99–103px', not bad_geo)
if missing:
    print('  missing:', missing[:5])
if bad_geo:
    print('  bad_geo:', bad_geo[:5])

# --- (d) 舊 Q 版成批清走 ---
chk('AWARDS64_SPRITES 常數已撤', 'const AWARDS64_SPRITES' not in src)
chk('Q 版 base64 池已撤（play 內冇 data:image/png）', 'data:image/png;base64' not in play_fn)
chk('loadSpr／drawSpr／sprImgs 已撤', 'loadSpr' not in play_fn and 'drawSpr' not in play_fn and 'sprImgs' not in play_fn)
chk('舊 walkA／walkB 幀值已撤（剩低只係「作廢」註解）', '"walkA"' not in play_fn and '"walkB"' not in play_fn)
chk('awei_hold 幀已撤', 'awei_hold' not in play_fn)
chk('剪影降級仲在（中性剪影，PixelLab 比例，唔係 Q 版方頭）', '中性剪影' in play_fn and 'ctx.ellipse' in play_fn)
chk('剪影唔再講 Q 版比例', 'Q 版比例' not in play_fn)

# --- (e) M1／M4 退役 ---
chk('M1 常數已撤（AWARDS62_STAGE_BG 定義消失）', 'const AWARDS62_STAGE_BG' not in src)
chk('M1 底圖檔案已刪', not os.path.isfile(os.path.join(PX_DIR, 'bg_awards_ballroom.jpg')))
chk('M4 GIF 檔案已刪', not os.path.isfile(os.path.join(root, 'assets', 'fx', 'awd_walkup_m4.gif')))
chk('M4 GIF 引用已撤（檔名唔再出現）', 'awd_walkup_m4.gif' not in src)
chk('walkup GIF overlay CSS 已撤', '.awd62-walkup160' not in src)
chk('walkup GIF overlay HTML 已撤（walkupHtml／syncWalkup 消失）', 'walkupHtml' not in play_fn and 'syncWalkup' not in play_fn)
chk('walkup beat 改由 canvas 畫（east 幀＋1400ms＋燕尾服捧杯）', 'id === "walkup"' in play_fn and 'frame: "east"' in play_fn and 'beatElapsed / 1400' in play_fn)
chk('walkup 文案經 setCaption（阿偉行上台…）', 'setCaption("阿偉行上台，接過獎盃，高高舉起。")' in play_fn)
chk('walkup beat 本身仲在（2200ms，caption ""）', 'id: "walkup", ms: 2200, caption: ""' in beats_fn)

# --- 唔郁守衛 ---
chk('WIN_LINE 0.875 唔郁', 'const AWARDS62_WIN_LINE = 0.875' in src)
chk('fellows 上限 3（slice(0, 3)）', 'focus.fellows63.slice(0, 3)' in play_fn)
chk('卡列／字幕／跳過掣仲在', 'awd63-cards' in play_fn and 'awd62-caption' in play_fn and 'awd62-skip' in play_fn)
chk('彩紙 M5 仲在（reveal／comfort／out）', 'awd_confetti_m5.gif' in play_fn and 'syncConfetti149' in play_fn)
chk('fanfare＋掌聲仲在（揭曉觸發）', 'awards160PlayWinAudio()' in play_fn and 'AWARDS160_FANFARE_SRC' in src)
chk('glamour 燕尾服仲在（tuxedo: true ≥4 處：reveal 行前＋企定＋walkup＋glamour）', play_fn.count('tuxedo: true') == 4)
chk('comfort beat 仲在（draw 分支）', 'id === "comfort"' in play_fn)
chk('燕尾服資產仲在', os.path.isfile(os.path.join(PX_DIR, 'awei_tuxedo.png')))
chk('SAVE key 不變', 'starVolunteer_map_v19w' in src)
chk('softRev 不變（s107）', 'var SOFT_REV = "s107"' in src)
chk('產品 ?v= 不變（v20a10）', '?v=20a10' in src)

print()
if fails:
    print('FAILED: %d' % len(fails))
    for f in fails:
        print(' - ' + f)
    sys.exit(1)
print('ALL PASS')
