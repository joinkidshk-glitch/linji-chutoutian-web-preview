# v20a129 FX129 休息片換入・靜態測試：新片格式＋cache-buster＋紅線。
# 用法：python3 tests/test_fx129_static.py [path-to-index.html]
# 反證：pristine v126 index 冇 ?v=20a129、舊片 14,606 bytes → 多項 FAIL。
import json, os, subprocess, sys

path = sys.argv[1] if len(sys.argv) > 1 else 'index.html'
root = os.path.dirname(os.path.abspath(path))
html = open(path, encoding='utf-8').read()
fails = []

def ok(name, cond):
    print(('PASS ' if cond else 'FAIL ') + name)
    if not cond:
        fails.append(name)

# 新片實體：PixelLab v3，36,212 bytes（舊片 14,606 bytes 唔可以再出現）
p = os.path.join(root, 'assets', 'fx', 'fx_rest.mp4')
ok('新片存在', os.path.isfile(p))
ok('新片 byte 數 36,212（v3）', os.path.isfile(p) and os.path.getsize(p) == 36212)
ok('舊片 byte 數 14,606 已唔係', not (os.path.isfile(p) and os.path.getsize(p) == 14606))

# 新片格式：960x540、24fps、3.0 秒、72 幀（ffprobe）
probe = None
try:
    r = subprocess.run(['ffprobe', '-v', 'error', '-show_entries',
                        'stream=width,height,r_frame_rate,duration,nb_frames',
                        '-of', 'json', p],
                       capture_output=True, text=True, timeout=30)
    probe = json.loads(r.stdout)['streams'][0] if r.returncode == 0 else None
except Exception as e:
    print('ffprobe error: ' + str(e))
ok('ffprobe 讀到片', probe is not None)
if probe is not None:
    ok('闊 960', probe.get('width') == 960)
    ok('高 540', probe.get('height') == 540)
    ok('幀率 24fps', probe.get('r_frame_rate') == '24/1')
    ok('時長 3.0 秒', abs(float(probe.get('duration', 0)) - 3.0) < 0.01)
    ok('幀數 72', int(probe.get('nb_frames', 0)) == 72)

# 接線：休息片 src 仲係 fx_rest.mp4，cache-buster 升做 ?v=20a129
ok('REST src 仲係 fx_rest.mp4',
   'const REST_SLEEP_FX_SRC = "assets/fx/fx_rest.mp4"' in html)
ok('休息片 cache-buster ?v=20a129',
   '"v=20a129"' in html and
   'REST_SLEEP_FX_SRC)?"&":"?") + "v=20a129"' in html)
ok('其餘 7 條 fx 片仲係 ?v=20a10',
   'const src = src0 + "?v=20a10";' in html)

# 紅線：SAVE key／softRev／產品 ?v= 冇郁
ok('SAVE key 不變', 'starVolunteer_map_v19w' in html)
ok('softRev s107 不變', 'softRev=s107' in html)
ok('產品 ?v= v20a10 不變', 'Product ?v= stays 20a10' in html)
ok('Soft QA URL 不變',
   'Soft QA URL (required): ?v=20a10&softBehaviorGate=1&softRev=s107' in html)

print('FX129 static:', 'ALL PASS' if not fails else f'{len(fails)} FAIL')
sys.exit(1 if fails else 0)
