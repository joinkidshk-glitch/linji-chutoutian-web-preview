# v20a160-m4 上台領獎 GIF static tests：修好版 GIF 入庫＋贏分支揭曉後播 walkup beat。
# 反證：run against pristine main (e08a070) -> GIF 唔存在、walkup beat 冇、引用冇 -> FAIL（唔 crash）。
# 殘影回歸防線：PIL 逐幀驗入庫 GIF 係全幅幀 (tile box 0,0,144,144) ＋ disposal=2。
# 原版係差分幀（幀 1-8 tile 得細格）＋ disposal=0，播起嚟疊殘影——所以原版唔准入庫。
import sys, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
idx_path = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, 'index.html')
src = open(idx_path, encoding='utf-8').read()
fails = []

def chk(name, cond):
    print(('PASS ' if cond else 'FAIL ') + name)
    if not cond:
        fails.append(name)

GIF_REL = 'assets/fx/awd_walkup_m4.gif'
GIF_PATH = os.path.join(ROOT, GIF_REL)
ORIG_REL = 'assets/fx/m4_walkup.gif'

# --- 資產入庫 ---
chk('修好版 GIF 入咗 repo（assets/fx/awd_walkup_m4.gif）', os.path.isfile(GIF_PATH))
chk('原版 GIF 冇入 repo（assets/fx/m4_walkup.gif 唔存在）', not os.path.isfile(os.path.join(ROOT, ORIG_REL)))
chk('原版檔名唔喺 assets 入面任何檔案', not any(
    fn == 'm4_walkup.gif'
    for _, _, files in os.walk(os.path.join(ROOT, 'assets')) for fn in files))
chk('修好版 GIF 非空', os.path.isfile(GIF_PATH) and os.path.getsize(GIF_PATH) > 1000)

# --- PIL：全幅幀＋disposal=2（殘影回歸防線）---
try:
    from PIL import Image
    im = Image.open(GIF_PATH)
    n = getattr(im, 'n_frames', 1)
    chk('GIF 有 9 幀', n == 9)
    chk('GIF 邏輯尺寸 144x144', im.size == (144, 144))
    all_full, all_disp2, all_120 = True, True, True
    for i in range(n):
        im.seek(i)
        box = im.tile[0][1] if im.tile else None
        if box != (0, 0, 144, 144):
            all_full = False
        if getattr(im, 'disposal_method', None) != 2:
            all_disp2 = False
        if im.info.get('duration') != 120:
            all_120 = False
    chk('逐幀全幅（tile box 全部 0,0,144,144，唔係差分幀）', all_full)
    chk('逐幀 disposal=2（播完清畫布，唔留殘影）', all_disp2)
    chk('逐幀 120ms（一圈 1080ms）', all_120)
except Exception as e:
    chk('PIL 讀到 GIF（' + str(e) + '）', False)

# --- 典禮贏分支引用修好版 ---
chk('index.html 引用修好版 GIF', GIF_REL in src)
chk('index.html 冇引用原版檔名', 'm4_walkup.gif' not in src)
chk('walkupHtml 掛修好版 <img>', 'awd62-walkup160' in src and '<img src="assets/fx/awd_walkup_m4.gif"' in src)

# --- beats：walkup 只限 won，reveal 之後 ---
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

beats_fn = slice_fn('awards62CeremonyBeats')
chk('beats：walkup 2200ms', 'id: "walkup", ms: 2200' in beats_fn)
chk('beats：walkup 只限 won 分支', 'if(best === "won")' in beats_fn and beats_fn.find('id: "walkup"') > beats_fn.find('if(best === "won")'))
chk('beats：walkup 喺 reveal 之後', beats_fn.find('id: "walkup"') > beats_fn.find('id: "reveal"'))
chk('beats：walkup beat caption 係空（跟 glamour 同款，文案喺 overlay cap）', 'id: "walkup", ms: 2200, caption: ""' in beats_fn)
chk('beats：gallery／nominated 唔行 walkup（walkup 喺 won guard 入面）',
    beats_fn.count('id: "walkup"') == 1)

# --- PlayCeremony 接線 ---
play_fn = slice_fn('awards62PlayCeremony')
chk('play：walkup overlay 淨係 won 先起', 'if(best === "won")' in play_fn and 'awd62-walkup160' in play_fn)
chk('play：walkup overlay cap 有行上台文案（唔喺 beat caption，免同台下字幕重複）', '阿偉行上台，接過獎盃，高高舉起。' in play_fn)
chk('play：syncWalkup 定義齊', 'const syncWalkup' in play_fn and '"walkup"' in play_fn)
chk('play：advance 嗰陣 syncWalkup', play_fn.count('syncWalkup(') >= 2)
chk('play：draw 有 walkup case（壓暗 canvas）', 'id === "walkup"' in play_fn)

# --- CSS ---
chk('CSS：.awd62-walkup160 層齊（display:none，.on 先 show）',
    '.awd62-walkup160{position:absolute' in src and '.awd62-walkup160.on{display:flex}' in src)
chk('CSS：GIF 像素渲染（image-rendering:pixelated）', '.awd62-walkup160 img' in src and 'image-rendering:pixelated' in src)
chk('CSS：overlay 唔擋撳掣（pointer-events:none）', '.awd62-walkup160{' in src and 'pointer-events:none' in src)

# --- 硬規則冇郁 ---
chk('SAVE key 冇郁', 'starVolunteer_map_v19w' in src)
chk('softRev 冇郁', 's107' in src)

if fails:
    print('FAILURES: %d' % len(fails))
    sys.exit(1)
print('ALL PASS')
