# v20a177：頒獎禮舞台加闊 static tests。
# 設計（見 NOTES_V20A177.md §1）：canvas 邏輯 424×360／backing 636×540／setTransform 1.5 全部唔郁；
#   (a) 地板加深：底圖重構（源圖幕布 0–193 壓到 0–166、地板 194–239 拉到 167–239，風格／內容唔變，
#       只係重採樣），源圖舞台頂線 y194→y167，×1.5 拉伸後 FLOOR 290→250，地板深 110px＝30.6% canvas 高
#       （對照參考圖：地板由幕布底到畫面底 316／1031＝30.7%）。
#   (b) 企位拉開：won／nominated 4 slots 間距 80→100、置中 202→212（62／162／262／362；
#       人仔闊 63px，罅 37px，兩邊各留 31px；講台 x194–229 啱啱落喺 slot 2／3 之間 193–231 條罅，
#       draw-rect 重疊 0）；gallery 3 slots 82／162／262（罅 80／100，唔再 −36 移位；
#       中央人右緣 193、右邊人左緣 231，同講台各留 1–2px；右邊空出 293–424＝131px 行走區，
#       對照參考圖右三分一留空）。
#   (c) 行走：enter beat 本身逐個由台側行到企位（entryPlan 0.16px/ms＋rank*380，唔郁）；
#       新幾何下最遠行距 92px（舊 132px 係因為舊 slot 貼邊；新 slot 企位本身闊咗，行走段仍然橫跨成個舞台）；
#       walkup beat 繼續用 M4 GIF（行上台領獎，2200ms 約兩圈）。
# 唔郁守衛（v174 五項）：獎盃金底 chip、舞台放大（424×360／636×540）、卡列預留（flex＋visibility）、
#   glamour frame 收短（display:none）、glamour 海報並置（44% panel＋燕尾服左邊留位）。
# 反證：run against pristine main 7801a72 -> 新幾何斷言全部 FAIL（唔 crash）；唔郁守衛 pristine 應 PASS。
import os, sys

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

WON = [62, 162, 262, 362]
GAL = [82, 162, 262]
FIG_W = 63          # 人仔闊（dispH 72，見 v174）
LECTERN = (194, 229)  # 講台正面 x（源圖 y196–214，v170／v174 已量度）

# --- (a) 地板加深：FLOOR 290→250 ---
chk('地板 FLOOR＝250（167×1.5＝250.5→250）', 'const FLOOR = 250' in play_fn)
chk('舊 FLOOR＝290 唔再出現（頒獎禮範圍）', 'const FLOOR = 290' not in play_fn)
chk('FLOOR 只定義一次', play_fn.count('const FLOOR =') == 1)
chk('地板深 110px（H 360 − FLOOR 250，佔 canvas 高 30.6%）',
    'const W = 424, H = 360' in play_fn and 'const FLOOR = 250' in play_fn)
chk('行前腳 260（FLOOR＋10）', 'y: Math.round(10 * p)' in play_fn)
chk('drawFigure 腳底跟 FLOOR（唔寫死）', 'const fy = FLOOR + (o.y || 0)' in play_fn)
chk('光池跟 FLOOR（F-99 至 F）', 'F - 99' in play_fn)
chk('獎盃 glyph 跟 FLOOR（−96／−39 唔變）',
    'FLOOR + fp.y - 96' in play_fn and 'FLOOR + fp.y - 39' in play_fn)
chk('後備舞台平台頂 H-110＝250', 'H - 110' in fb_fn)
chk('後備舞台平台正面由 H-110 伸 37（到 H-33）', 'ctx.fillRect(0, H - 110, W, 37)' in fb_fn)
chk('後備舞台金線 H-116 橫跨平台頂邊', 'H - 116' in fb_fn)
chk('後備舞台舊平台頂 H-70 唔再出現', 'H - 70' not in fb_fn)
chk('後備舞台舊金線 H-76 唔再出現', 'H - 76' not in fb_fn)
chk('後備舞台底部／椅列唔郁（H-33／H-39）', 'H - 33' in fb_fn and 'H - 39' in fb_fn)

# --- (b) 企位拉開：slotCx ---
chk('won／nominated slotCx 間距 100、置中 212',
    '212 + (i - (slots.length - 1) / 2) * 100' in play_fn)
chk('gallery 3 slots 用 [82, 162, 262]', '[82, 162, 262]' in play_fn)
chk('舊間距 80 唔再出現（slotCx 範圍）', '* 80' not in play_fn)
chk('舊 gallery 中央 −36 移位唔再出現', 'cx -= 36' not in play_fn)
chk('舊置中 202 唔再出現（slotCx 範圍）', '202 + (i -' not in play_fn)
chk('won 4 slots 罅 ≥70px（100−63＝37 邊罅；中心距 100）',
    all(WON[i+1] - WON[i] >= 70 for i in range(3)))
chk('gallery 3 slots 罅 ≥70px（中心距 80／100）',
    all(GAL[i+1] - GAL[i] >= 70 for i in range(2)))
chk('won 企位唔出 canvas 界（左右各留 31px）',
    WON[0] - FIG_W // 2 >= 0 and WON[-1] + FIG_W // 2 <= 424)
chk('gallery 企位唔出 canvas 界', GAL[0] - FIG_W // 2 >= 0 and GAL[-1] + FIG_W // 2 <= 424)
chk('won 講台落喺 slot 2／3 之間（slot2 右緣 193 ≤194、slot3 左緣 231 ≥229，重疊 0）',
    WON[1] + FIG_W // 2 <= LECTERN[0] - 1 and WON[2] - FIG_W // 2 >= LECTERN[1] + 2)
chk('gallery 中央人唔掂講台（右緣 193 ≤194）', GAL[1] + FIG_W // 2 <= LECTERN[0] - 1)
chk('gallery 右邊人唔掂講台（左緣 231 ≥229）', GAL[2] - FIG_W // 2 >= LECTERN[1] + 2)
chk('gallery 右邊留出行走區（293–424＝131px）', 424 - (GAL[-1] + FIG_W // 2) >= 100)
chk('玩家 slot 仍然係 1（won 4 slots，阿偉 x＝162 唔變）',
    'slots.splice(Math.min(1, slots.length), 0, { kind: "player" })' in play_fn)
chk('glamour 燕尾服右緣 210／424＝49.5%（<56%，海報 panel 唔重疊）',
    162 + 96 // 2 < 424 * 0.56)

# --- (c) 行走接線唔郁 ---
chk('入場 entryPlan 唔郁（左右兩流／0.16px/ms／rank*380）',
    'entryPlan' in play_fn and '0.16' in play_fn and 'rank * 380' in play_fn)
chk('入場由台側行入（from −30／454）', 'p.from = side < 0 ? -30 : 454' in play_fn)
chk('enter beat 用 walk 幀行入', 'id === "enter"' in play_fn and 'frame: (tick % 2)' in play_fn)
chk('reveal 得獎者行前（fwd64，向 212 行 22%）',
    'fwd64' in play_fn and '(212 - cx0) * 0.22' in play_fn)
chk('walkup beat 繼續用 M4 GIF（2200ms，行上台領獎）',
    'id: "walkup", ms: 2200' in slice_fn('awards62CeremonyBeats')
    and 'awd_walkup_m4.gif' in play_fn)

# --- 底圖重構（PIL 量度）---
BG_REL = 'assets/story/awards/bg_awards_ballroom.jpg'
BG_PATH = os.path.join(root, BG_REL)
try:
    from PIL import Image
    bg = Image.open(BG_PATH).convert('RGB')
    def row_br(y, x0, x1):
        row = [bg.getpixel((x, y)) for x in range(x0, x1)]
        return sum(sum(p) / 3 for p in row) / len(row)
    chk('底圖尺寸仲係 424×240（重構只係重採樣，唔換尺寸／唔換風格）', bg.size == (424, 240))
    chk('底圖新舞台頂邊：y160–164 仲係幕布紅（中央帶 mean < 110）',
        row_br(160, 244, 297) < 110 and row_br(164, 244, 297) < 110)
    chk('底圖新舞台頂邊：y170–172 已係平台面（中央帶 mean > 180）',
        row_br(170, 244, 297) > 180 and row_br(172, 244, 297) > 180)
    gold = sum(1 for y in range(170, 201) for x in range(195, 231)
               if (lambda p: p[0] > 170 and p[1] > 140 and p[2] < 210 and p[0] - p[2] > 30)(bg.getpixel((x, y))))
    chk('底圖講台仲在位（y170–200 中央有金色講台像素）', gold > 0)
    chk('底圖檔案大小合理（10–200KB）', 10 * 1024 <= os.path.getsize(BG_PATH) <= 200 * 1024)
except Exception as e:
    chk('PIL 讀到底圖（' + str(e) + '）', False)

# --- v174 五項唔郁守衛 ---
chk('v174 A1：海報裱框收窄到直屬 img（>）', bool(css_rule('.awd63-glamour-panel>img')))
chk('v174 A1：獎盃金底 chip 規則在場（#f2c14e／22px）',
    'background:#f2c14e' in css_rule('.awd63-glamour .cap img.ic112,.awd62-caption img.ic112')
    and 'width:22px' in css_rule('.awd63-glamour .cap img.ic112,.awd62-caption img.ic112'))
chk('v174 B1：canvas 邏輯 424×360／backing 636×540／setTransform 1.5 唔郁',
    'const W = 424, H = 360' in play_fn
    and '<canvas class="awd62-canvas" width="636" height="540">' in src
    and 'ctx.setTransform(1.5, 0, 0, 1.5, 0, 0);' in play_fn)
chk('v174 B1：人仔 72／75／96 唔郁', '? 75 : 72' in play_fn and 'dispH: 96' in play_fn)
chk('v174 B1：glamour overlay aspect 424/360 唔郁', 'aspect-ratio:424/360' in src)
chk('v174 B2：卡列常駐 flex＋visibility 隱藏（預留高度）',
    'display:flex' in css_rule('.awd63-cards') and 'visibility:hidden' in css_rule('.awd63-cards'))
chk('v174 B2：stagger 60＋i*180 唔郁', 'elapsed > 60 + i * 180' in play_fn)
chk('v174 C2：glamour-hide display:none（frame 收短）',
    'display:none' in css_rule('.awd63-cards.glamour-hide'))
chk('v174 C2：syncGlamour 單一 choke point 仲在',
    'classList.toggle("glamour-hide", !!(b && b.id === "glamour"))' in play_fn)

# --- 紀律守衛 ---
chk('SAVE key 唔變（starVolunteer_map_v19w）', 'starVolunteer_map_v19w' in src)
chk('softRev 唔變', 'softRev' in src)
chk('掌聲 MP3 唔喺呢票（M9 觸發點仲在）', 'awards160PlayWinAudio' in play_fn)
chk('提名卡唔掂（cardsData／cardsHtml 仲在）', 'cardsData' in play_fn and 'cardsHtml' in play_fn)
chk('彩紙底界 364 唔郁（H 唔變）', 'p.y > 364' in play_fn)

print('')
print('FAILED: %d' % len(fails) if fails else 'ALL PASS')
sys.exit(1 if fails else 0)
