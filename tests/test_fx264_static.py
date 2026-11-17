# v20a264 train_c 機械修補・靜態測試：cache-buster＋像素檢查。
# 用法：python3 tests/test_fx264_static.py [path-to-index.html]
# 背景：v139 換入嘅 fx_train_c.mp4 有兩個生成缺陷（樑上頭盔狀物件＋樁頂兩點
# 深色似眼），用戶 2026-11-17 拍板機械塗走，唔再生成。今次係 PIL 機械修補，
# 唔係 inpaint（9 次 inpaint 歷史留喺 NOTES_V20A139，唔好同今次混淆）。
# 像素檢查用 ffmpeg rawvideo＋numpy（系統 python3 有 numpy 1.26，唔依賴 PIL）。
import hashlib, os, re, subprocess, sys

path = sys.argv[1] if len(sys.argv) > 1 else 'index.html'
root = os.path.dirname(os.path.abspath(path))
html = open(path, encoding='utf-8').read()
fails = []

def ok(name, cond):
    print(('PASS ' if cond else 'FAIL ') + name)
    if not cond:
        fails.append(name)

# ---- cache-buster：淨係 trainC 升 20a264，其餘 5 條行 20a139
m = re.search(r'kind==="trainC".*?src="\$\{src0\}\?v=([0-9a-z]+)"', html)
ok('trainC cache-buster ?v=20a264', m is not None and m.group(1) == '20a264')
for key in ('shootExt', 'record', 'audition', 'trainA', 'trainB'):
    mm = re.search(r'kind==="%s".*?src="\$\{src0\}\?v=([0-9a-z]+)"' % key, html)
    ok(f'{key} cache-buster 仲係 ?v=20a139', mm is not None and mm.group(1) == '20a139')

# ---- 新片實體
p = os.path.join(root, 'assets', 'fx', 'fx_train_c.mp4')
ok('train_c 新片存在', os.path.isfile(p))
ok('train_c 新片 byte 數 48,129', os.path.isfile(p) and os.path.getsize(p) == 48129)
if os.path.isfile(p):
    got = hashlib.sha256(open(p, 'rb').read()).hexdigest()
    ok('train_c 新片 sha256 071da765…',
       got == '071da765ed84fc77e05eff5f9bf10142f62b30b082c53cc4f3a4ffb84d46635e')

# ---- 像素檢查：逐幀 rawvideo（numpy 計數；系統 python3 有 numpy 1.26）
import numpy as np

W, H = 960, 540
FRAME = W * H * 3
HELMET = (448, 48, 516, 110)     # x0, y0, x1, y1
DOT_L = (455, 188, 460, 192)     # x0, y0, x1, y1
DOT_R = (496, 192, 500, 201)


def is_tan(a):
    # a: (..., 3)，最後一軸係 RGB
    return (a[..., 0] > 170) & (a[..., 0] < 235) & \
           (a[..., 1] > 130) & (a[..., 1] < 200) & \
           (a[..., 2] > 80) & (a[..., 2] < 150)


proc = subprocess.run(['ffmpeg', '-v', 'error', '-i', p,
                       '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'],
                      capture_output=True, timeout=120)
raw = proc.stdout
nframes = len(raw) // FRAME
frames = np.frombuffer(raw[:nframes * FRAME], dtype=np.uint8) \
    .reshape(nframes, H, W, 3).astype(np.int16)
ok('抽到 72 幀', nframes == 72)
if nframes == 72:
    # 頭盔啡黃像素（修補區內應該零粒）
    x0, y0, x1, y1 = HELMET
    tan_left = int(is_tan(frames[:, y0:y1, x0:x1]).sum())
    ok('頭盔啡黃像素清零（修補區內）', tan_left == 0)
    # 樁頂兩點：修補區內最低亮度（原點約 51／37，修後木色約 86／58）
    lum_L = frames[:, DOT_L[1]:DOT_L[3], DOT_L[0]:DOT_L[2]].mean(axis=3).min()
    lum_R = frames[:, DOT_R[1]:DOT_R[3], DOT_R[0]:DOT_R[2]].mean(axis=3).min()
    ok('樁頂左點亮度已回復木色（最低 %.0f ≥ 70）' % lum_L, lum_L >= 70)
    ok('樁頂右點亮度已回復木色（最低 %.0f ≥ 50）' % lum_R, lum_R >= 50)
    # 背景靜態：y 260-447 以外，逐幀同第一幀嘅最大色差 ≤ 25（有損編碼噪聲水平；
    # 實測重建版 12，原片 10——修補本身係靜態，唔可以逐幀唔同）
    d = np.abs(frames[1:] - frames[0]).max(axis=3)
    d[:, 260:448] = 0
    worst = int(d.max())
    ok('背景逐幀靜態（y<260／y>447 最大色差 %d ≤ 25）' % worst, worst <= 25)
else:
    ok('頭盔啡黃像素清零（修補區內）', False)
    ok('樁頂左點亮度已回復木色', False)
    ok('樁頂右點亮度已回復木色', False)
    ok('背景逐幀靜態', False)

# ---- 紅線：SAVE key／softRev／產品 ?v= 冇郁
ok('SAVE key 不變', 'starVolunteer_map_v19w' in html)
ok('softRev s107 不變', 'softRev=s107' in html)
ok('產品 ?v= v20a10 不變', 'Product ?v= stays 20a10' in html)

print('FX264 static:', 'ALL PASS' if not fails else f'{len(fails)} FAIL')
sys.exit(1 if fails else 0)
