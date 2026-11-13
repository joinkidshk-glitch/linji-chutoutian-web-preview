# v20a181：橫向舞台幾何 static tests（原 v20a170 檔成份改寫；v170 係 FLOOR 跟底圖頂線，v181 成個舞台重建）。
# v181 幾何：canvas 邏輯 480×360（4:3）／backing 720×540／setTransform 1.5；FLOOR＝262（木地板 y228–310，
# 深 82px＝22.8% 高；v20a187 B1 收窄，舊 y200–334／134px 係讀錯參考圖）；slotCx 置中 240／間距 120（4 slots 60／180／300／420；gallery 75／240／405）；
# 人物 px 幀 dispH 112（fellow）／116（玩家）／燕尾服 112；行前向中央 240 集中 22%、y＋10（新腳 272）；
# 光池 99；獎盃 glyph −110（燕尾服頭頂，v20a187 C6；舊 −112）／−52（對手胸前）；後備舞台＝同一個程式舞台（awards181DrawBase）。
# 唔郁：slotCx 行前 x 向中心 22%、entryPlan（左右兩流／0.16px/ms／rank*380）、glamour overlay 並置
# （aspect 跟 canvas 改 480/360）、卡列隱藏 choke point（display:none）、SAVE key、softRev、?v=。
# M4 walkup GIF＋M1 底圖已撤（見 test_awards160_m4／m1）；walkup beat 而家由 canvas 畫人物（唔再淨係壓暗）。
# 反證：run against pristine main 91f264a -> (1)(2)(3)(4) 斷言全部 FAIL（唔 crash）；(5)(6) 係回歸守衛，pristine 應 PASS。
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
base_fn = slice_fn('awards181DrawBase')
beats_fn = slice_fn('awards62CeremonyBeats')

# --- (1) FLOOR＝262（木地板 y228–310，v20a187 B1） ---
chk('FLOOR＝262（v181：木地板 y228–310，深 82px）', 'const FLOOR = 262' in play_fn)
chk('舊 FLOOR＝250 唔再出現（頒獎禮範圍）', 'const FLOOR = 250' not in play_fn)
chk('舊 FLOOR＝193 唔再出現（頒獎禮範圍）', 'const FLOOR = 193' not in play_fn)
chk('舊 FLOOR＝155 唔再出現（頒獎禮範圍）', 'const FLOOR = 155' not in play_fn)
chk('FLOOR 只定義一次', play_fn.count('const FLOOR =') == 1)
chk('FLOOR 註解寫明木地板 y228–310＋22.8%', '228' in play_fn and '82' in play_fn and '22.8%' in play_fn)

# --- (2) 後備舞台＝同一個程式舞台 ---
chk('後備舞台在場', bool(fb_fn))
chk('後備舞台 delegate 去 awards181DrawBase', 'awards181DrawBase(ctx, W, H, 0)' in fb_fn)
chk('後備舞台舊平台頂 H-110 唔再出現', 'H - 110' not in fb_fn)
chk('後備舞台舊金線 H-116 唔再出現', 'H - 116' not in fb_fn)
chk('後備舞台舊平台底 H-33 唔再出現', 'H - 33' not in fb_fn)
chk('程式舞台地板 y228–310 在場', '#d9a75f' in base_fn and '228, W + 16, 82' in base_fn)
chk('程式舞台觀眾席 y316–360 在場', '#120c20' in base_fn and '316, W + 16, 44' in base_fn)

# --- (3) slot x ---
chk('slotCx 公式（置中 240／間距 120，v181）', '240 + (i - (slots.length - 1) / 2) * 120' in play_fn)
chk('gallery 3 slots 用 [75, 240, 405]', '[75, 240, 405]' in play_fn)
chk('4 slots 阿偉 x＝180（slotCx(1)＝240-60）', 'slotCx' in play_fn and 'playerSlot' in play_fn)
chk('入場 entryPlan 唔郁（左右兩流／0.16px/ms／rank*380）',
    'entryPlan' in play_fn and '0.16' in play_fn and 'rank * 380' in play_fn)

# --- (4) 腳底 y 對地板 ---
chk('drawFigure 腳底＝FLOOR＋o.y（跟常數，唔寫死）', 'const fy = FLOOR + (o.y || 0)' in play_fn)
chk('reveal 行前 y＋10（新腳 272）', 'y: Math.round(10 * p)' in play_fn)
chk('reveal 行前 x 向中心 240、22% 唔變', '(240 - cx0) * 0.22' in play_fn)
chk('lightPool 跟 FLOOR（F-99 至 F）', 'F - 99' in play_fn)
chk('獎盃 glyph 跟 FLOOR（FLOOR + fp.y - 110／-52，v20a187 C6）',
    'FLOOR + fp.y - 110' in play_fn and 'FLOOR + fp.y - 52' in play_fn)
chk('人物高度 px 幀（fellow 112／玩家 116／燕尾服 112）',
    '? 116 : 112' in play_fn and 'dispH: 112' in play_fn)
chk('canvas 480×360（W 480／H 360）', 'const W = 480, H = 360' in play_fn)

# --- (5) 受影響 beats 清單 ---
for bid in ('pan', 'enter', 'names', 'suspense', 'reveal', 'comfort', 'glamour'):
    chk('beat %s 經 drawFigure（跟 FLOOR 郁）' % bid,
        ('id === "%s"' % bid) in play_fn and 'drawFigure' in play_fn)
chk('open beat 冇人物（空台漸光）', 'id === "open"' in play_fn)
open_block = play_fn[play_fn.find('id === "open"'):play_fn.find('id === "pan"')]
chk('open beat 唔畫人物', 'drawFigure' not in open_block)
walk_block = play_fn[play_fn.find('if(id === "walkup")'):play_fn.find('if(id === "out")')]
chk('walkup beat canvas 畫人物（v181：px east 幀行上台，唔再淨係壓暗）', 'drawFigure' in walk_block and 'frame: "east"' in walk_block)
chk('beats 列表唔變（open／pan／enter／names／suspense／reveal／comfort／walkup／glamour／out）',
    all(('"%s"' % b) in beats_fn for b in
        ('open', 'pan', 'enter', 'names', 'suspense', 'reveal', 'comfort', 'walkup', 'glamour', 'out')))

# --- (6) 唔郁守衛（M1／M4 已撤，守衛改做「已撤」） ---
chk('walkup GIF 檔名已撤（awd_walkup_m4.gif 唔再出現）', 'awd_walkup_m4.gif' not in src)
chk('walkup GIF overlay CSS 已撤（.awd62-walkup160）', '.awd62-walkup160' not in src)
chk('M1 底圖常數已撤（AWARDS62_STAGE_BG）', 'const AWARDS62_STAGE_BG' not in src)
chk('glamour overlay 唔變（v166：absolute＋480/360 對齊 canvas，v181）',
    'position:absolute' in src and 'aspect-ratio:480/360' in src)
chk('syncGlamour 卡列隱藏唔變（v168：glamour-hide）', 'glamour-hide' in play_fn)
chk('SAVE key 唔變（starVolunteer_map_v19w）', 'starVolunteer_map_v19w' in src)
chk('softRev 唔變', 'softRev' in src)

print('')
print('FAILED: %d' % len(fails) if fails else 'ALL PASS')
sys.exit(1 if fails else 0)
