# v20a139 FX139 其餘 6 條 fx 片換入・靜態測試：新片格式＋cache-buster＋紅線。
# 用法：python3 tests/test_fx139_static.py [path-to-index.html]
# 反證：pristine v159 index 冇 ?v=20a139、舊片 byte 數唔同 → 多項 FAIL。
# 成本：6 個 state（25 次／個，train_b 重試 1 次免費）＋6 次 animate（1 次／個）。
import hashlib, json, os, subprocess, sys

path = sys.argv[1] if len(sys.argv) > 1 else 'index.html'
root = os.path.dirname(os.path.abspath(path))
html = open(path, encoding='utf-8').read()
fails = []

def ok(name, cond):
    print(('PASS ' if cond else 'FAIL ') + name)
    if not cond:
        fails.append(name)

# 新片實體：PixelLab character-animation 版（阿偉 v2 49907fa9 起手），
# 場景用原版（用戶 2026-11-12 21:15 拍板，inpaint／重生都唔用）。
CLIPS = {
    'shoot_ext': ('fx_shoot_ext.mp4', 37264,
                  '30078ab6187b3d7b370ebf384d088e624daab1e1284307c51b0a50a49e6c840a'),
    'record':    ('fx_record.mp4', 42621,
                  '18eb80b8b1d93506dd5705435b40696b28f6248a91b11fbecead88a57634c0e9'),
    'audition':  ('fx_audition.mp4', 34668,
                  '0f8633f00a89d290e8beae0b7b46a5f81606993e3c2fd7ce759ee405dba5fee5'),
    'train_a':   ('fx_train_a.mp4', 32064,
                  'e52dc3c864456c4e796c6013782c69665215183f72774822deb6943f79f0c4e1'),
    'train_b':   ('fx_train_b.mp4', 47894,
                  'cc9cd2493f8f5fffa4e5a9d2e987f0163da1469cec8419eaa7d6ba736bc8ed23'),
    'train_c':   ('fx_train_c.mp4', 48129,
                  '071da765ed84fc77e05eff5f9bf10142f62b30b082c53cc4f3a4ffb84d46635e'),  # v20a264 機械修補版（舊 49172／e85a57b1…）
}
for kind, (fname, size, sha) in CLIPS.items():
    p = os.path.join(root, 'assets', 'fx', fname)
    ok(f'{kind} 新片存在', os.path.isfile(p))
    ok(f'{kind} 新片 byte 數 {size:,}',
       os.path.isfile(p) and os.path.getsize(p) == size)
    if os.path.isfile(p):
        got = hashlib.sha256(open(p, 'rb').read()).hexdigest()
        ok(f'{kind} 新片 sha256 {sha[:8]}…', got == sha)
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
        ok(f'{kind} ffprobe 讀到片', probe is not None)
        if probe is not None:
            ok(f'{kind} 闊 960', probe.get('width') == 960)
            ok(f'{kind} 高 540', probe.get('height') == 540)
            ok(f'{kind} 幀率 24fps', probe.get('r_frame_rate') == '24/1')
            ok(f'{kind} 時長 3.0 秒', abs(float(probe.get('duration', 0)) - 3.0) < 0.01)
            ok(f'{kind} 幀數 72', int(probe.get('nb_frames', 0)) == 72)
    else:
        ok(f'{kind} 新片 sha256 {sha[:8]}…', False)
        ok(f'{kind} ffprobe 讀到片', False)

# 接線：map 唔郁；6 條片各有 ?v=20a139 early return；共用行唔郁（淨係 fx_rest 行佢）
for kind, (fname, _s, _h) in CLIPS.items():
    key = {'shoot_ext': 'shootExt', 'record': 'record', 'audition': 'audition',
           'train_a': 'trainA', 'train_b': 'trainB', 'train_c': 'trainC'}[kind]
    ok(f'{kind} map 仲係 {fname}',
       f'{key}: "assets/fx/{fname}"' in html)
    ok(f'{kind} cache-buster ?v=20a139',
       f'kind==="{key}"' in html and '${src0}?v=20a139' in html)
ok('共用行 ?v=20a10 仲喺度（淨係 fx_rest 行佢）',
   'const src = src0 + "?v=20a10";' in html)
ok('休息片 ?v=20a129 冇郁（v129 接線）',
   '"v=20a129"' in html)
ok('拍攝片 ?v=20a130 冇郁（v130 接線）',
   'kind==="shoot"' in html and '${src0}?v=20a130' in html)

# 紅線：SAVE key／softRev／產品 ?v= 冇郁
ok('SAVE key 不變', 'starVolunteer_map_v19w' in html)
ok('softRev s107 不變', 'softRev=s107' in html)
ok('產品 ?v= v20a10 不變', 'Product ?v= stays 20a10' in html)
ok('Soft QA URL 不變',
   'Soft QA URL (required): ?v=20a10&softBehaviorGate=1&softRev=s107' in html)

print('FX139 static:', 'ALL PASS' if not fails else f'{len(fails)} FAIL')
sys.exit(1 if fails else 0)
