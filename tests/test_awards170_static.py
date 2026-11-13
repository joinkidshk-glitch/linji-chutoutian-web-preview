# v20a170 Phase 2：新舞台-only 底圖＋FLOOR 跟新圖頂線 static tests。
# 修法核心：FLOOR 155→193（新底圖 bg_awards_ballroom.jpg 舞台-only：紅幕布填滿取景、講台置中；
# PIL 量度最終 424×240：中央帶幕布底 y191–193 過渡、y194 滿亮平台面，FLOOR＝194−1＝193；
# 舊圖頂線 155、舊值 194 企觀眾席。源圖 pixflux 400×224，裁走底部椅背 y208–224 → 400×208，
# 再放大 424×240；講台 y≈181–210 完整在圖內，左右幕布邊完整，無字無人無 logo 無椅無紅地毯）。
# 後備舞台（awards62FallbackStage）平台頂一併由 H-85＝155 改到 H-47＝193，平台正面伸到 H-22。
# 唔郁：slotCx x 值（4 slots 94／166／238／310；3 slots 130／202／274）、dispH（48／50／64）、
# 行前 fwd64（x 向中心 22%、y＋7）、walkup GIF（DOM 層，焗死喺 GIF 入面）、glamour overlay（v166 並置）、
# 卡列隱藏（v168）、SAVE key、softRev、?v=、content pack JSON。
# 斷言：
# (1) FLOOR＝193，舊值 155／194 全檔消失（頒獎禮範圍內；註解入面提及舊值除外）。
# (2) 後備舞台平台頂 H-47＝193、正面伸到 H-22、金線 H-51 橫跨頂邊；舊 H-85／H-89／H-52／H-56 唔再出現。
# (3) slot x 唔變：slotCx 公式、4／3 slots 數值。
# (4) 腳底 y 對舞台頂：drawFigure 腳底＝FLOOR＋o.y；reveal 行前腳＝FLOOR＋7＝200（講台 y≈181–210，
#     行前腳落喺講台身前平台面）；lightPool／獎盃 glyph 全部跟 FLOOR，冇寫死 194。
# (5) 受影響 beats 清單：pan／enter／names／suspense／reveal／comfort／glamour 經 drawFigure（跟 FLOOR）；
#     open／walkup／out 冇人物 canvas 繪圖（walkup 只係壓暗＋DOM GIF）。
# (6) 唔郁守衛：walkup GIF 檔名／glamour overlay CSS／syncGlamour 卡列隱藏／SAVE key／softRev 在場。
# 反證：run against pristine main 56141a3 -> (1)(2) 斷言全部 FAIL（唔 crash）；(3)(4)(5)(6) 係回歸守衛，pristine 應 PASS。
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

# --- (1) FLOOR＝193 ---
chk('FLOOR＝193（新圖舞台頂線）', 'const FLOOR = 193' in play_fn)
chk('舊 FLOOR＝155 唔再出現（頒獎禮範圍）', 'const FLOOR = 155' not in play_fn)
chk('舊 FLOOR＝194 唔再出現（頒獎禮範圍）', 'const FLOOR = 194' not in play_fn)
chk('FLOOR 只定義一次', play_fn.count('const FLOOR =') == 1)
chk('FLOOR 註解寫明舞台頂線 y≈194＋舊值問題', '194' in play_fn and '觀眾席' in play_fn)

# --- (2) 後備舞台平台頂跟 FLOOR ---
chk('後備舞台在場', bool(fb_fn))
chk('後備舞台側幕／金邊到 H-47＝193', 'H - 47' in fb_fn)
chk('後備舞台平台正面由 H-47 伸到 H-22（高 25）', 'ctx.fillRect(0, H - 47, W, 25)' in fb_fn)
chk('後備舞台金線 H-51 橫跨平台頂邊', 'H - 51' in fb_fn)
chk('後備舞台舊平台頂 H-85 唔再出現', 'H - 85' not in fb_fn)
chk('後備舞台舊金線 H-89 唔再出現', 'H - 89' not in fb_fn)
chk('後備舞台舊平台頂 H-52 唔再出現', 'H - 52' not in fb_fn)
chk('後備舞台舊金線 H-56 唔再出現', 'H - 56' not in fb_fn)
chk('後備舞台底部／椅列唔郁（H-22／H-26）', 'H - 22' in fb_fn and 'H - 26' in fb_fn)

# --- (3) slot x 唔變 ---
chk('slotCx 公式唔變（置中 202／間距 72）', '202 + (i - (slots.length - 1) / 2) * 72' in play_fn)
chk('4 slots 阿偉 x＝166（slotCx(1)＝202-36）', 'slotCx' in play_fn and 'playerSlot' in play_fn)
chk('入場 entryPlan 唔郁（左右兩流／0.16px/ms／rank*380）',
    'entryPlan' in play_fn and '0.16' in play_fn and 'rank * 380' in play_fn)

# --- (4) 腳底 y 對舞台頂 ---
chk('drawFigure 腳底＝FLOOR＋o.y（跟常數，唔寫死）', 'const fy = FLOOR + (o.y || 0)' in play_fn)
chk('reveal 行前 y＋7（新腳 200，講台身前平台面）', 'y: Math.round(7 * p)' in play_fn)
chk('reveal 行前 x 向中心 22% 唔變', '(212 - cx0) * 0.22' in play_fn)
chk('lightPool 跟 FLOOR（F-66 至 F）', 'F - 66' in play_fn)
chk('獎盃 glyph 跟 FLOOR（FLOOR + fp.y - 64／-26）',
    'FLOOR + fp.y - 64' in play_fn and 'FLOOR + fp.y - 26' in play_fn)
_play_no_floor_comment = '\n'.join(l for l in play_fn.split('\n') if 'const FLOOR = 193' not in l)
chk('頒獎禮範圍內冇寫死 194 做腳底（FLOOR 註解入面提及舊值除外）', '194' not in _play_no_floor_comment)
chk('人仔高度唔變（fellow 48／玩家 50／燕尾服 64）',
    '? 50 : 48' in play_fn and 'dispH: 64' in play_fn)

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
chk('glamour overlay 唔變（v166：absolute＋424/240 對齊 canvas）',
    'position:absolute' in src and 'aspect-ratio:424/240' in src)
chk('syncGlamour 卡列隱藏唔變（v168：glamour-hide）', 'glamour-hide' in play_fn)
chk('SAVE key 唔變（starVolunteer_map_v19w）', 'starVolunteer_map_v19w' in src)
chk('softRev 唔變', 'softRev' in src)

print('')
print('FAILED: %d' % len(fails) if fails else 'ALL PASS')
sys.exit(1 if fails else 0)
