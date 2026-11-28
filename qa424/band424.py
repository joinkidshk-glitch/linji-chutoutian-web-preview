# -*- coding: utf-8 -*-
"""v424 N1 輪廓亮帶量度（GPT 法）：每位立繪揀 >=5 段固定輪廓，沿法線（水平）取樣，
亮帶峰值（輪廓外側 0-3px 帶內最高亮度）同緊貼人物內側亮度中位數（內側 4-10px）之差。
輪廓位置由素材 alpha 遮罩映射到截圖座標（object-fit:contain, object-position:bottom center）。
同時量臉部／衣服實色中位數，排除靠壓暗人物取得改善。
用法: python3 qa424/band424.py [before|after]"""
import json, os, sys, statistics
from PIL import Image

ROOT = '/home/hatch/workspace/linji-work424'
OUT = ROOT + '/qa424/out'
TAG = sys.argv[1] if len(sys.argv) > 1 else 'after'

def lum(p):
    return 0.2126 * p[0] + 0.7152 * p[1] + 0.0722 * p[2]

def measure(tag_vp, m):
    png = os.path.join(OUT, 'shots', f'{TAG}_n1_5of16_{tag_vp}.png')
    if not os.path.exists(png):
        return {'error': 'no png'}
    im = Image.open(png).convert('RGB')
    W, H = im.size
    sx, sy = W / float(m['vw']), H / float(m['vh'])
    chars = []
    for img in (m.get('imgs') or []):
        src = img['src'].split('?')[0]
        apath = os.path.join(ROOT, src)
        asset = Image.open(apath).convert('RGBA')
        aw, ah = asset.size
        alpha = asset.getchannel('A')
        r = img['r']
        # object-fit contain + bottom center：內容矩形
        scale = min(r['w'] / aw, r['h'] / ah)
        cw, ch = aw * scale, ah * scale
        cx0 = r['left'] + (r['w'] - cw) / 2
        cy0 = r['bottom'] - ch
        flip = img.get('flip')
        segs = []
        # 固定輪廓段：資產高 12%/25%/38%/52%/66% 處左右邊
        for frac in [0.12, 0.25, 0.38, 0.52, 0.66]:
            ay = int(ah * frac)
            row = [alpha.getpixel((x, ay)) for x in range(aw)]
            xs = [x for x, a in enumerate(row) if a > 128]
            if not xs:
                continue
            for side, ax in [('L', min(xs)), ('R', max(xs))]:
                # 映射到截圖 CSS 座標
                fx = (aw - 1 - ax) if flip else ax
                css_x = cx0 + fx * scale
                css_y = cy0 + ay * scale
                px, py = int(css_x * sx), int(css_y * sy)
                if not (8 < px < W - 8 and 0 <= py < H):
                    continue
                # 法線取樣：向外 0..3 CSS px（峰值）、向內 4..10 CSS px（中位）
                out_dir = -1 if side == 'L' else 1
                outer, inner = [], []
                for d in range(0, 4):
                    x = px + out_dir * int(d * sx)
                    if 0 <= x < W:
                        outer.append(lum(im.getpixel((x, py))))
                for d in range(4, 11):
                    x = px - out_dir * int(d * sx)
                    if 0 <= x < W:
                        inner.append(lum(im.getpixel((x, py))))
                if outer and inner:
                    peak = max(outer)
                    med = statistics.median(inner)
                    segs.append({'frac': frac, 'side': side, 'peak': round(peak, 1),
                                 'innerMed': round(med, 1), 'diff': round(peak - med, 1)})
        diffs = [s['diff'] for s in segs]
        # 實色對照：頭部區（臉）同軀幹區中位亮度
        def region_med(fx0, fy0, fx1, fy1):
            x0 = int((cx0 + cw * fx0) * sx); x1 = int((cx0 + cw * fx1) * sx)
            y0 = int((cy0 + ch * fy0) * sy); y1 = int((cy0 + ch * fy1) * sy)
            vals = []
            for y in range(max(0, y0), min(H, y1), 3):
                for x in range(max(0, x0), min(W, x1), 3):
                    vals.append(lum(im.getpixel((x, y))))
            return round(statistics.median(vals), 1) if vals else None
        chars.append({
            'src': src, 'nSeg': len(segs),
            'medianDiff': round(statistics.median(diffs), 1) if diffs else None,
            'segs': segs,
            'faceMed': region_med(0.35, 0.05, 0.65, 0.14),
            'clothMed': region_med(0.3, 0.3, 0.7, 0.5),
        })
    all_diffs = [s['diff'] for c in chars for s in c['segs']]
    return {'chars': chars, 'overallMedianDiff': round(statistics.median(all_diffs), 1) if all_diffs else None,
            'nSegTotal': len(all_diffs)}

meas = json.load(open(os.path.join(OUT, f'measure_{TAG}.json'), encoding='utf-8'))
out = {}
for tag_vp in ['390x844', '430x707', '430x932']:
    m = meas.get(f'n1_{tag_vp}')
    if m:
        out[tag_vp] = measure(tag_vp, m)
        print(tag_vp, 'overallMedianDiff', out[tag_vp].get('overallMedianDiff'), 'nSeg', out[tag_vp].get('nSegTotal'),
              [(c['src'].split('/')[-1], c['medianDiff'], c['faceMed'], c['clothMed']) for c in out[tag_vp]['chars']], flush=True)
json.dump(out, open(os.path.join(OUT, f'band_{TAG}.json'), 'w'), ensure_ascii=False, indent=1)
print('saved band_' + TAG)
