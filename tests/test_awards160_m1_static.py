# v20a160 M1 會場場景圖做典禮底圖 static tests：
# 會場實景底圖檔案在位（424×240 JPG，等比放大、冇拉變形）、典禮 code 引用佢、
# 舊像素舞台 data URI 已撤、降級舞台同 canvas 幾何唔郁、硬規則（SAVE key／softRev／?v=）冇郁。
# 反證：對 pristine main（e08a070）index.html 跑——舊像素底圖在位、新常數／新檔案全部缺失 → 乾淨 FAIL，唔 crash。
import os, re, struct, sys

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

def jpeg_size(path):
    """唔靠 PIL 讀 JPEG 尺寸（SOF0/SOF2）；讀唔到返 (0, 0)。"""
    try:
        with open(path, 'rb') as fh:
            data = fh.read(2)
            if data != b'\xff\xd8': return (0, 0)
            while True:
                hdr = fh.read(4)
                if len(hdr) < 4: return (0, 0)
                if hdr[0] != 0xFF: return (0, 0)
                marker = hdr[1]
                seglen = struct.unpack('>H', hdr[2:4])[0]
                if marker in (0xC0, 0xC1, 0xC2):
                    sof = fh.read(5)
                    if len(sof) < 5: return (0, 0)
                    h, w = struct.unpack('>HH', sof[1:5])
                    return (w, h)
                fh.seek(seglen - 2, 1)
    except Exception:
        return (0, 0)

BG_REL = 'assets/story/awards/bg_awards_ballroom.jpg'
BG_PATH = os.path.join(root, BG_REL)

# --- 1. 新底圖常數＋檔案 ---
chk('會場底圖常數在位（AWARDS62_STAGE_BG＝檔案路徑）',
    'const AWARDS62_STAGE_BG = "assets/story/awards/bg_awards_ballroom.jpg";' in src)
chk('舊像素舞台 data URI 已撤（AWARDS62_STAGE_PX 全檔消失）', 'AWARDS62_STAGE_PX' not in src)
chk('底圖只得一個共享引用點（常數定義＋loader 各一次，唔分場／唔分分支）',
    src.count('const AWARDS62_STAGE_BG = ') == 1 and src.count('im.src = AWARDS62_STAGE_BG;') == 1)
chk('底圖檔案在位（新檔名，唔撞舊快取）', os.path.isfile(BG_PATH))
magic_ok = False
size_ok = False
dims = (0, 0)
if os.path.isfile(BG_PATH):
    with open(BG_PATH, 'rb') as fh:
        magic_ok = fh.read(2) == b'\xff\xd8'
    size_ok = 10 * 1024 <= os.path.getsize(BG_PATH) <= 200 * 1024
    dims = jpeg_size(BG_PATH)
chk('底圖係 JPEG（magic FF D8）', magic_ok)
chk('底圖檔案大小合理（10–200KB）', size_ok)
chk('底圖尺寸 424×240（配合 canvas backing store 1:1）', dims == (424, 240))
chk('底圖比例 ≈424/240（等比放大，冇拉變形）',
    dims[0] and abs(dims[0] / dims[1] - 424 / 240) < 0.01)

# --- 2. 典禮 code 引用佢 ---
play_fn = slice_fn('awards62PlayCeremony')
chk('loader 用新常數', 'im.src = AWARDS62_STAGE_BG;' in play_fn)
chk('loader 失敗照舊降級（onerror → bgReady=false）', 'im.onerror' in play_fn and 'bgReady = false' in play_fn)
chk('draw() 畫底圖 1:1（424×240）', 'ctx.drawImage(bgImg, 0, 0, W, H)' in play_fn)
chk('pan beat 保持橫移畫法（440 闊）', 'ctx.drawImage(bgImg, -8 + off, 0, 440, H)' in play_fn)
chk('降級舞台函數仲在（載入失敗兜底）', 'function awards62FallbackStage(ctx, W, H)' in src)
chk('canvas backing store 仲係 424×240', '<canvas class="awd62-canvas" width="424" height="240">' in src)
chk('canvas 像素呈現唔郁（pixelated）', 'image-rendering:pixelated' in src and 'awd62-canvas' in src)

# --- 3. 硬規則：SAVE key／softRev／?v= 冇郁 ---
chk('SAVE key 不變', 'starVolunteer_map_v19w' in src)
chk('softRev 不變（s107）', 'var SOFT_REV = "s107"' in src)
chk('產品 ?v= 不變（v20a10）', '?v=20a10' in src)
chk('底圖路徑唔帶 ?v=（新檔名本身避快取）', '?v=' not in BG_REL)

print('')
print('FAILED: %d' % len(fails) if fails else 'ALL PASS')
sys.exit(1 if fails else 0)
