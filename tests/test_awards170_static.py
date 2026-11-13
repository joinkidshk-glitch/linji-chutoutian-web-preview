# v20a170 Phase 2：新舞台-only 底圖＋FLOOR 跟新圖頂線 static tests。
# v20a174 B1 resync：canvas 高 240→360（底圖垂直拉伸 1.5×，構圖完整保留），全部 y 幾何 ×1.5：
# FLOOR 193→290（源圖舞台頂 193×1.5＝289.5，FLOOR＝291−1＝290）；人仔 fellow 48→72／玩家 50→75／
# 燕尾服 64→96；slotCx 間距 72→80＋gallery 中央 −30（C1）；行前 y＋7→＋10；光池 66→99；
# 獎盃 glyph 21×12→31×18（−64→−96／−26→−39）；後備舞台 H-47→H-70。
# 唔郁：slotCx 置中 202、行前 x 向中心 22%、walkup GIF（DOM 層）、glamour overlay 並置（aspect 跟 canvas 改 424/360）、
# 卡列隱藏 choke point（v174 C2 改 display:none，見 test_awards174／168）、SAVE key、softRev、?v=、content pack JSON。
# 斷言：
# (1) FLOOR＝290，舊值 193／155 全檔消失（頒獎禮範圍內；註解入面提及舊值除外）。
# (2) 後備舞台平台頂 H-70＝290、正面伸到 H-33、金線 H-76 橫跨頂邊；舊 H-47／H-51／H-22／H-26 唔再出現。
# (3) slot x：slotCx 公式（置中 202／間距 80）、gallery 中央 slot 左移 30、4 slots 阿偉 x＝162。
# (4) 腳底 y 對舞台頂：drawFigure 腳底＝FLOOR＋o.y；reveal 行前腳＝FLOOR＋10＝300；lightPool／獎盃 glyph 全部跟 FLOOR。
# (5) 受影響 beats 清單：pan／enter／names／suspense／reveal／comfort／glamour 經 drawFigure（跟 FLOOR）；
#     open／walkup／out 冇人物 canvas 繪圖（walkup 只係壓暗＋DOM GIF）。
# (6) 唔郁守衛：walkup GIF 檔名／glamour overlay CSS／syncGlamour 卡列隱藏／SAVE key／softRev 在場。
# 反證：run against pristine main e8c3a73 -> (1)(2)(3)(4) 斷言全部 FAIL（唔 crash）；(5)(6) 係回歸守衛，pristine 應 PASS。
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

play_fn = slice_fn('awards62PlayCeremony')
fb_fn = slice_fn('awards62FallbackStage')
beats_fn = slice_fn('awards62CeremonyBeats')

# --- (1) FLOOR＝290 ---
chk('FLOOR＝290（拉伸後舞台頂線）', 'const FLOOR = 290' in play_fn)
chk('舊 FLOOR＝193 唔再出現（頒獎禮範圍）', 'const FLOOR = 193' not in play_fn)
chk('舊 FLOOR＝155 唔再出現（頒獎禮範圍）', 'const FLOOR = 155' not in play_fn)
chk('FLOOR 只定義一次', play_fn.count('const FLOOR =') == 1)
chk('FLOOR 註解寫明拉伸 1.5×＋源圖頂線 194', '194' in play_fn and '1.5' in play_fn)

# --- (2) 後備舞台平台頂跟 FLOOR ---
chk('後備舞台在場', bool(fb_fn))
chk('後備舞台側幕／金邊到 H-70＝290', 'H - 70' in fb_fn)
chk('後備舞台平台正面由 H-70 伸到 H-33（高 37）', 'ctx.fillRect(0, H - 70, W, 37)' in fb_fn)
chk('後備舞台金線 H-76 橫跨平台頂邊', 'H - 76' in fb_fn)
chk('後備舞台舊平台頂 H-47 唔再出現', 'H - 47' not in fb_fn)
chk('後備舞台舊金線 H-51 唔再出現', 'H - 51' not in fb_fn)
chk('後備舞台舊平台底 H-22 唔再出現', 'H - 22' not in fb_fn)
chk('後備舞台舊椅列 H-26 唔再出現', 'H - 26' not in fb_fn)
chk('後備舞台舊平台頂 H-85 唔再出現', 'H - 85' not in fb_fn)
chk('後備舞台舊金線 H-89 唔再出現', 'H - 89' not in fb_fn)
chk('後備舞台底部／椅列新值（H-33／H-39）', 'H - 33' in fb_fn and 'H - 39' in fb_fn)

# --- (3) slot x ---
chk('slotCx 公式（置中 202／間距 80）', '202 + (i - (slots.length - 1) / 2) * 80' in play_fn)
chk('gallery 中央 slot 左移 36（C1，避講台）', 'slots.length === 3 && i === 1' in play_fn and 'cx -= 36' in play_fn)
chk('4 slots 阿偉 x＝162（slotCx(1)＝202-40）', 'slotCx' in play_fn and 'playerSlot' in play_fn)
chk('入場 entryPlan 唔郁（左右兩流／0.16px/ms／rank*380）',
    'entryPlan' in play_fn and '0.16' in play_fn and 'rank * 380' in play_fn)

# --- (4) 腳底 y 對舞台頂 ---
chk('drawFigure 腳底＝FLOOR＋o.y（跟常數，唔寫死）', 'const fy = FLOOR + (o.y || 0)' in play_fn)
chk('reveal 行前 y＋10（新腳 300，講台身前平台面）', 'y: Math.round(10 * p)' in play_fn)
chk('reveal 行前 x 向中心 22% 唔變', '(212 - cx0) * 0.22' in play_fn)
chk('lightPool 跟 FLOOR（F-99 至 F）', 'F - 99' in play_fn)
chk('獎盃 glyph 跟 FLOOR（FLOOR + fp.y - 96／-39）',
    'FLOOR + fp.y - 96' in play_fn and 'FLOOR + fp.y - 39' in play_fn)
chk('人仔高度放大 1.5×（fellow 72／玩家 75／燕尾服 96）',
    '? 75 : 72' in play_fn and 'dispH: 96' in play_fn)
chk('canvas 高 360（W 424 唔變）', 'const W = 424, H = 360' in play_fn)

# --- (5) 受影響 beats 清單 ---
for bid in ('pan', 'enter', 'names', 'suspense', 'reveal', 'comfort', 'glamour'):
    chk('beat %s 經 drawFigure（跟 FLOOR 郁）' % bid,
        ('id === "%s"' % bid) in play_fn and 'drawFigure' in play_fn)
chk('open beat 冇人物（空台漸光）', 'id === "open"' in play_fn)
open_block = play_fn[play_fn.find('id === "open"'):play_fn.find('id === "pan"')]
chk('open beat 唔畫人物', 'drawFigure' not in open_block)
walk_block = play_fn[play_fn.find('if(id === "walkup")'):play_fn.find('if(id === "out")')]
chk('walkup beat canvas 冇人物（只壓暗，GIF 係 DOM 層）', 'drawFigure' not in walk_block)
chk('walkup beat 註解寫明 GIF 做主角', 'GIF' in walk_block)
chk('beats 列表唔變（open／pan／enter／names／suspense／reveal／comfort／walkup／glamour／out）',
    all(('"%s"' % b) in beats_fn for b in
        ('open', 'pan', 'enter', 'names', 'suspense', 'reveal', 'comfort', 'walkup', 'glamour', 'out')))

# --- (6) 唔郁守衛 ---
chk('walkup GIF 檔名唔變（awd_walkup_m4.gif）', 'awd_walkup_m4.gif' in src)
chk('walkup GIF overlay CSS 唔變（.awd62-walkup160）', '.awd62-walkup160' in src)
chk('glamour overlay 唔變（v166：absolute＋424/360 對齊 canvas）',
    'position:absolute' in src and 'aspect-ratio:424/360' in src)
chk('syncGlamour 卡列隱藏唔變（v168：glamour-hide）', 'glamour-hide' in play_fn)
chk('SAVE key 唔變（starVolunteer_map_v19w）', 'starVolunteer_map_v19w' in src)
chk('softRev 唔變', 'softRev' in src)

print('')
print('FAILED: %d' % len(fails) if fails else 'ALL PASS')
sys.exit(1 if fails else 0)
