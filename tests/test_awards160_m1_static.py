# v20a211 B1 resync：雙幾何（矮 480×432／高 480×540，HS211／HSC211＝×1.25）——短基準值不變，高 viewport 按比例換算；見 NOTES_V20A211。
# v20a181：M1 會場實景底圖退役 static tests（原 v20a160 M1 檔成份改寫）。
# v181 起舞台改做 canvas 程式繪製（awards181DrawBase：淺色幕布＋木地板＋燈架），M1 實景底圖
# assets/story/awards/bg_awards_ballroom.jpg＋AWARDS62_STAGE_BG 常數＋bgImg loader 一併撤走；
# 載入失敗唔再分叉——後備舞台就係同一個程式舞台。詳細新幾何見 tests/test_awards181_static.py。
# 反證：run against pristine main 91f264a -> 「已撤」斷言全部 FAIL（常數／檔案／loader 仲在），唔 crash；
#   backing／pixelated／硬規則守衛 pristine 應 PASS。
import os, sys

idx_path = sys.argv[1] if len(sys.argv) > 1 else 'index.html'
src = open(idx_path, encoding='utf-8').read()
root = os.path.dirname(os.path.abspath(idx_path))
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

BG_REL = 'assets/story/awards/bg_awards_ballroom.jpg'
BG_PATH = os.path.join(root, BG_REL)
play_fn = slice_fn('awards62PlayCeremony')
fb_fn = slice_fn('awards62FallbackStage')

# --- 1. M1 底圖退役 ---
chk('M1 常數已撤（AWARDS62_STAGE_BG 定義消失）', 'const AWARDS62_STAGE_BG' not in src)
chk('M1 底圖檔案已刪', not os.path.isfile(BG_PATH))
chk('M1 loader 已撤（唔再 preload bgImg）', 'im.src = AWARDS62_STAGE_BG;' not in play_fn and 'bgReady' not in play_fn)
chk('draw() 唔再畫 bgImg', 'drawImage(bgImg' not in play_fn)
chk('舊像素舞台 data URI 繼續唔存在（AWARDS62_STAGE_PX 全檔消失）', 'AWARDS62_STAGE_PX' not in src)

# --- 2. 程式舞台接替 ---
chk('程式舞台函數在場（awards181DrawBase）', 'function awards181DrawBase(ctx, W, H, off)' in src)
chk('降級舞台函數仲在（簽名唔變）', 'function awards62FallbackStage(ctx, W, H)' in src)
chk('降級舞台＝同一個程式舞台（唔再分叉）', 'awards181DrawBase(ctx, W, H, 0)' in fb_fn)
chk('canvas backing store 720×648（邏輯 480×432 ×1.5；v20a207 B2）', 'Math.round(HS211 * 1.5)' in src)
chk('canvas 像素呈現唔郁（pixelated）', 'image-rendering:pixelated' in src and 'awd62-canvas' in src)

# --- 3. 硬規則：SAVE key／softRev／?v= 冇郁 ---
chk('SAVE key 不變', 'starVolunteer_map_v19w' in src)
chk('softRev 不變（s107）', 'var SOFT_REV = "s107"' in src)
chk('產品 ?v= 不變（v20a10）', '?v=20a10' in src)

print('')
print('FAILED: %d' % len(fails) if fails else 'ALL PASS')
sys.exit(1 if fails else 0)
