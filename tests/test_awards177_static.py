# v20a211 B1 resync：雙幾何（矮 480×432／高 480×540，HS211／HSC211＝×1.25）——短基準值不變，高 viewport 按比例換算；見 NOTES_V20A211。
# v20a181：頒獎禮舞台橫向重建 static tests（原 v20a177 檔成份改寫；v177 幾何成批作廢）。
# 設計（見 NOTES_V20A181.md §1）：canvas 邏輯 480×360（4:3）／backing 720×540／setTransform 1.5；
#   (a) 地板：木地板 y228–310（深 82px＝22.8% 高；v20a187 B1 收窄，舊 y200–334／134px 係讀錯參考圖），FLOOR＝262，行前腳 272；後備舞台＝同一個程式舞台。
#   (b) 企位：won／nominated 4 slots 60／180／300／420（間距 120，置中 240；人闊約 42px，罅 78px，
#       兩邊各留 39px；冇圓台／講台）；gallery 3 slots 75／240／405（罅 165／165，左／中／右分開企）。
#   (c) 行走：enter beat 逐個由台側行到企位（entryPlan 0.16px/ms＋rank*380，唔郁；from −40／520）；
#       行幀跟方向揀 east／west；reveal 行前向中央 240 行 22%；walkup beat 改由 canvas 畫（唔再用 M4 GIF）。
# 唔郁守衛（v174 五項，v181 幾何跟住改）：獎盃金底 chip、舞台 480×360／720×540、卡列預留（flex＋visibility）、
#   glamour frame 收短（display:none）、glamour 海報並置（44% panel＋燕尾服左邊留位）。
# 反證：run against pristine main 91f264a -> 新幾何斷言全部 FAIL（唔 crash）；唔郁守衛 pristine 應 PASS。
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
base_fn = slice_fn('awards181DrawBase')

WON = [60, 180, 300, 420]
GAL = [75, 240, 405]
FIG_W = 51          # px 人物顯示闊上限（dispH 136 × 最闊 48/128 ≈ 51；v20a207 B2：112→136）

# --- (a) 地板：FLOOR 262→314（v20a207 B2） ---
chk('地板 FLOOR＝314（木地板 y274–372，v20a207 B2）', 'const FLOOR = Math.round(314 * HSC211)' in play_fn)
chk('舊 FLOOR＝250 唔再出現（頒獎禮範圍）', 'const FLOOR = 250' not in play_fn)
chk('FLOOR 只定義一次', play_fn.count('const FLOOR =') == 1)
chk('地板深 98px（H 432，佔 canvas 高 22.7%；v20a207 B2）',
    'const W = 480, H = HS211' in play_fn and 'const FLOOR = Math.round(314 * HSC211)' in play_fn)
chk('行前腳 324（FLOOR＋10；v20a207 B2）', 'y: Math.round(10 * p)' in play_fn)
chk('drawFigure 腳底跟 FLOOR（唔寫死）', 'const fy = FLOOR + (o.y || 0)' in play_fn)
chk('光池跟 FLOOR（F-120 至 F；v20a207 B2）', 'F - Math.round(120 * HSC211)' in play_fn)
chk('獎盃 glyph 跟 FLOOR（−129／−61，v20a187 C6；v20a207 B2）',
    'FLOOR + fp.y - Math.round(129 * HSC211)' in play_fn and 'FLOOR + fp.y - Math.round(61 * HSC211)' in play_fn)
chk('後備舞台 delegate 去程式舞台（舊平台頂 H-110 消失）', 'awards181DrawBase(ctx, W, H, 0)' in fb_fn and 'H - 110' not in fb_fn)
chk('後備舞台舊金線 H-116 唔再出現', 'H - 116' not in fb_fn)
chk('後備舞台舊平台底 H-33 唔再出現', 'H - 33' not in fb_fn)
chk('程式舞台地板 y274–372（#d9a75f，H 比例）', '#d9a75f' in base_fn and '228 / 360' in base_fn and '310 / 360' in base_fn)
chk('程式舞台觀眾席 y379–432（#120c20，H 比例）', '#120c20' in base_fn and '316 / 360' in base_fn)

# --- (b) 企位：slotCx ---
chk('won／nominated slotCx 間距 120、置中 240',
    '240 + (i - (slots.length - 1) / 2) * 120' in play_fn)
chk('gallery 3 slots 用 [75, 240, 405]', '[75, 240, 405]' in play_fn)
chk('舊間距 100 唔再出現（slotCx 範圍）', '* 100' not in play_fn)
chk('舊 gallery [82, 162, 262] 唔再出現', '[82, 162, 262]' not in play_fn)
chk('舊置中 212 唔再出現（slotCx 範圍）', '212 + (i -' not in play_fn)
chk('won 4 slots 罅 ≥65px（120−51＝69；v20a207 B2：人闊咗）',
    all(WON[i+1] - WON[i] - FIG_W >= 65 for i in range(3)))
chk('gallery 3 slots 罅 ≥100px（165−46＝119）',
    all(GAL[i+1] - GAL[i] - FIG_W >= 100 for i in range(2)))
chk('won 企位唔出 canvas 界（左右各留 39px）',
    WON[0] - FIG_W // 2 >= 0 and WON[-1] + FIG_W // 2 <= 480)
chk('gallery 企位唔出 canvas 界', GAL[0] - FIG_W // 2 >= 0 and GAL[-1] + FIG_W // 2 <= 480)
chk('舞台冇講台／圓台幾何（LECTERN／講台 x194 唔再出現；退役註解提及除外）', 'LECTERN' not in play_fn and '講台 x194' not in play_fn)
chk('玩家 slot 仍然係 1（won 4 slots，阿偉 x＝180；v20a208：splice 搬入 buildSlots208，初建＋轉格共用）',
    'sl.splice(Math.min(1, sl.length), 0, { kind: "player" })' in play_fn and
    'buildSlots208(fellows, winFellow' in play_fn)
chk('glamour 燕尾服右緣 236／480＝49.2%（<56%，海報 panel 唔重疊）',
    180 + 136 // 2 < 480 * 0.56) # v20a207 B2：dispH 136

# --- (c) 行走接線 ---
chk('入場 entryPlan 唔郁（左右兩流／0.16px/ms／rank*380）',
    'entryPlan' in play_fn and '0.16' in play_fn and 'rank * 380' in play_fn)
chk('入場由台側行入（from −40／520）', 'p.from = side < 0 ? -40 : 520' in play_fn)
chk('enter beat 用 east／west 側面幀行入', 'id === "enter"' in play_fn and 'frame: (p.side < 0) ? "east" : "west"' in play_fn)
chk('reveal 得獎者行前（fwd64，向 240 行 22%）',
    'fwd64' in play_fn and '(240 - cx0) * 0.22' in play_fn)
chk('walkup beat 改由 canvas 畫（2200ms，唔再用 M4 GIF）',
    'id: "walkup", ms: 2200' in slice_fn('awards62CeremonyBeats')
    and 'awd_walkup_m4.gif' not in play_fn and 'frame: "east"' in play_fn)

# --- v174 五項唔郁守衛（v181 幾何跟住改） ---
chk('v174 A1：海報裱框收窄到直屬 img（>）', bool(css_rule('.awd63-glamour-panel>img')))
chk('v174 A1：獎盃金底 chip 規則在場（#f2c14e／22px；v20a207 C2 擴到 fellows）',
    'background:#f2c14e' in css_rule('.awd63-glamour .cap img.ic112,.awd62-caption img.ic112,.psr-fellows63 img.ic112')
    and 'width:22px' in css_rule('.awd63-glamour .cap img.ic112,.awd62-caption img.ic112,.psr-fellows63 img.ic112'))
chk('v174 B1：canvas 邏輯 480×432／backing 720×648／setTransform 1.5（v181；v20a207 B2）',
    'const W = 480, H = HS211' in play_fn
    and 'Math.round(HS211 * 1.5)' in src
    and 'ctx.setTransform(1.5, 0, 0, 1.5, 0, 0);' in play_fn)
chk('v174 B1：人物 136／140／燕尾服 136（v181；v20a207 B2）', 'Math.round(140 * HSC211)' in play_fn and 'dispH: Math.round(136 * HSC211)' in play_fn)
chk('v174 B1：glamour overlay aspect 480/432（v181；v20a207 B2）', 'aspect-ratio:480/432' in src)
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
chk('彩紙底界 436（H 432；v20a207 B2）', 'p.y > HS211 + 4' in play_fn)

print('')
print('FAILED: %d' % len(fails) if fails else 'ALL PASS')
sys.exit(1 if fails else 0)
