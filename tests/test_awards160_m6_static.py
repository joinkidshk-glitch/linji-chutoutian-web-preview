# v20a160 M6「燕尾服阿偉」static tests:
# (1) 資產在場：assets/story/awards/awei_tuxedo.png，PNG 128x128（Pixellab state 7577440c… south 原圖）。
# (2) 常量接線：AWARDS160_TUXEDO_AWEI 指向該資產；awards62PlayCeremony 預載（tuxRec）。
# (3) 渲染：drawTuxedo 腳底對齊 floorY（115/128）；drawFigure 經 o.tuxedo 分流，載唔到跌返 Q 版 drawSpr。
# (4) 贏分支先著：reveal won 區（行前＋企定）同 glamour 區有 tuxedo: true；全 play 內 tuxedo: true 共 4 處
#     （v20a181：walkup beat 行完換燕尾服捧杯，加多一處）。
# (5) 輸分支唔著：comfort 區、nominated reveal else 區、awards62CeremonyBeats 全部無 tuxedo。
# 反證：run against pristine main (e08a070) -> 資產＋常量＋接線全部缺 -> FAIL（唔 crash）。
import os, struct, sys

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

def slice_brace(text, open_idx):
    """由 open_idx（一個 '{' 嘅位置）起搵返配對嘅 '}'，回傳成段（含首尾括號）。"""
    depth = 0
    for k in range(open_idx, len(text)):
        if text[k] == '{': depth += 1
        elif text[k] == '}':
            depth -= 1
            if depth == 0: return text[open_idx:k+1]
    return ''

# --- (1) 資產 ---
asset_rel = 'assets/story/awards/awei_tuxedo.png'
asset = os.path.join(root, asset_rel)
chk('燕尾服資產在場 assets/story/awards/awei_tuxedo.png', os.path.isfile(asset))
is_png = False
w = h = 0
try:
    with open(asset, 'rb') as fh:
        d = fh.read(32)
    is_png = d[:8] == b'\x89PNG\r\n\x1a\n'
    if is_png:
        w, h = struct.unpack('>II', d[16:24])
except Exception:
    pass
chk('資產係 PNG', is_png)
chk('資產原生 128x128（唔係放大假高清）', (w, h) == (128, 128))

# --- (2) 常量＋預載 ---
chk('常量 AWARDS160_TUXEDO_AWEI 指向資產', 'const AWARDS160_TUXEDO_AWEI = "assets/story/awards/awei_tuxedo.png"' in src)
play_fn = slice_fn('awards62PlayCeremony')
chk('play 預載燕尾服（tuxRec）', 'tuxRec' in play_fn and 'AWARDS160_TUXEDO_AWEI' in play_fn)

# --- (3) 渲染 ---
chk('drawTuxedo helper 在場', 'const drawTuxedo' in play_fn)
chk('燕尾服腳底對齊 floorY（115/128）', 'dispH * 115 / 128' in play_fn)
chk('drawFigure 經 o.tuxedo 分流', 'o.tuxedo' in play_fn)
chk('載唔到跌返 px south 幀（drawPx 剪影降級）', 'drawTuxedo(cx' in play_fn and 'drawPx(starId, dir, cx' in play_fn)

# --- (4) 贏分支先著 ---
# v20a181：M4 walkup GIF 區已撤，play 內只剩 reveal 一個 if(best === "won"){（行前＋企定）。
# v20a208：揭曉分支條件由 pack best 改做而家呢格 outcome（curOutcome208）——多格之夜每格 outcome
# 唔同，pack best 會令非玩家格揭曉誤行燕尾服分支；「贏分支先著」意圖不變，錨點跟住改名。
_won_cands = []
_start = 0
while True:
    _wi = play_fn.find('if(curOutcome208 === "won"){', _start)
    if _wi < 0:
        break
    _won_cands.append((_wi, slice_brace(play_fn, play_fn.find('{', _wi))))
    _start = _wi + 1
chk('reveal won 區搵到（一個 won 區，帶 tuxedo: true）', sum(1 for _, b in _won_cands if 'tuxedo: true' in b) == 1)
_won_hit = [(i, b) for i, b in _won_cands if 'tuxedo: true' in b]
won_i, won_block = _won_hit[0] if _won_hit else (-1, '')
chk('reveal won 區有 tuxedo: true', 'tuxedo: true' in won_block)
chk('reveal won 企定加獎盃 glyph', 'drawTrophyGlyph' in won_block)
glam_i = play_fn.find('if(id === "glamour"){')
glam_block = slice_brace(play_fn, play_fn.find('{', glam_i)) if glam_i >= 0 else ''
chk('glamour 區有 tuxedo: true', 'tuxedo: true' in glam_block)
chk('全 play 內 tuxedo: true 共 5 處（reveal 行前＋企定＋walkup＋glamour＋out，v20a187 C3）', play_fn.count('tuxedo: true') == 5)

# --- (5) 輸分支唔著 ---
comf_i = play_fn.find('if(id === "comfort"){')
comf_block = slice_brace(play_fn, play_fn.find('{', comf_i)) if comf_i >= 0 else ''
chk('comfort 區無 tuxedo', 'tuxedo' not in comf_block)
nom_region = play_fn[play_fn.find('} else {', won_i):play_fn.find('if(id === "comfort"){')] if won_i >= 0 else ''
chk('nominated reveal else 區無 tuxedo: true', 'tuxedo: true' not in nom_region)
beats_fn = slice_fn('awards62CeremonyBeats')
chk('beats 定義無 tuxedo（門檻唔喺 beats 層）', 'tuxedo' not in beats_fn)

print('')
print('FAILED: %d' % len(fails) if fails else 'ALL PASS')
sys.exit(1 if fails else 0)
