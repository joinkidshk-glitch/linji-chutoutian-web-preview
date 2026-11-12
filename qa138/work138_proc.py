# -*- coding: utf-8 -*-
"""v20a138 cutout：37 張新表情圖去背（沿用 v127 work127_proc.py：fix2 連通體剪影＋
填洞＋收邊＋羽毛法；另加 v123 wedge 選擇性填洞掃描——下半身大純白底洞
（size>=1000、nearwhite>=0.8、ymin/H>0.5）唔填，還原做背景）。
輸入：linji-work138/gen138/{stem}-gen1.webp（生成圖，米白／白底）
輸出：linji-work138/assets138/{stem}.webp（去背 WebP q92，冇焗邊）
另出面部對照 qc138/face_{stem}.png（左＝基本款頭部、右＝新圖頭部，H=620）。
"""
import numpy as np, json, os
from PIL import Image
from scipy import ndimage

W = '/home/hatch/workspace/linji-work138/'
REPO_FB = '/home/hatch/workspace/linji-work138/assets/story/fullbody/'
JOBS = [
    ('chai_zanhoi_angry', 'chai_zanhoi_base.webp', None),
    ('chai_zanhoi_shy', 'chai_zanhoi_base.webp', None),
    ('chai_zanhoi_smile', 'chai_zanhoi_base.webp', None),
    ('chai_zanhoi_think', 'chai_zanhoi_base.webp', None),
    ('cheung_hakfan_serious', 'cheung_hakfan_base.webp', None),
    ('cheung_tsijun_sad', 'cheung_tsijun_base.webp', None),
    ('cheung_tsijun_think', 'cheung_tsijun_base.webp', 'cheung_tsijun_think-gen2.webp'),
    ('chung_choning_angry', 'chung_choning_base.webp', None),
    ('crew_laolinji_serious', 'crew_laolinji_base.webp', None),
    ('extra_ad_fen_sad', 'extra_ad_fen_base.webp', None),
    ('extra_ad_fen_serious', 'extra_ad_fen_base.webp', None),
    ('ho_sang_surprise', 'ho_sang_base.webp', None),
    ('ko_chunkit_shy', 'ko_chunkit_base.webp', None),
    ('ko_chunkit_think', 'ko_chunkit_base.webp', None),
    ('lin_hiu_serious', 'lin_hiu_base.webp', None),
    ('lin_hiu_smile', 'lin_hiu_base.webp', None),
    ('liu_bingxing_sad', 'liu_bingxing_base.webp', None),
    ('liu_bingxing_surprise', 'liu_bingxing_base.webp', None),
    ('liu_bingxing_think', 'liu_bingxing_base.webp', None),
    ('lok_gasing_angry', 'lok_gasing_base.webp', None),
    ('lok_gasing_shy', 'lok_gasing_base.webp', None),
    ('lok_gasing_smile', 'lok_gasing_base.webp', None),
    ('lok_gasing_surprise', 'lok_gasing_base.webp', None),
    ('lui_ging_serious', 'lui_ging_base.webp', 'lui_ging_serious-gen2.webp'),
    ('luk_baakyin_angry', 'luk_baakyin_base.webp', None),
    ('luk_baakyin_sad', 'luk_baakyin_base.webp', None),
    ('luk_baakyin_smile', 'luk_baakyin_base.webp', None),
    ('mak_zhendong_angry', 'mak_zhendong_base.webp', None),
    ('mak_zhendong_smile', 'mak_zhendong_base.webp', None),
    ('ngai_wingnaam_angry', 'ngai_wingnaam_base.webp', None),
    ('ngai_wingnaam_serious', 'ngai_wingnaam_base.webp', 'ngai_wingnaam_serious-gen2.webp'),
    ('ngai_wingnaam_smile', 'ngai_wingnaam_base.webp', None),
    ('ngai_wingnaam_surprise', 'ngai_wingnaam_base.webp', None),
    ('ngai_wingnaam_think', 'ngai_wingnaam_base.webp', None),
    ('so_jiyan_surprise', 'so_jiyan_base.webp', None),
    ('tsui_poushan_serious', 'tsui_poushan_base.webp', None),
    ('vera_serious', 'vera_base.webp', None),
]

def hard_mask(a):
    bg = np.median(a[:40, :40].reshape(-1, 3), axis=0)
    d = np.sqrt(((a.astype(int) - bg) ** 2).sum(axis=2))
    m = d > 26
    lab, n = ndimage.label(m)
    sizes = ndimage.sum(m, lab, range(1, n + 1))
    return ndimage.binary_fill_holes(lab == (np.argmax(sizes) + 1)), tuple(int(x) for x in bg)

def fill_holes_selective(main, gen_int):
    """fill_holes，但剔走下半身大純白底洞（腿間口袋，v123 教訓）。"""
    H = main.shape[0]
    filled = ndimage.binary_fill_holes(main)
    holes = filled & ~main
    hlab, hn = ndimage.label(holes)
    dropped = []
    if hn:
        hs = ndimage.sum(holes, hlab, range(1, hn + 1))
        for i, s in enumerate(hs, 1):
            if s < 1000:
                continue
            ys, xs = np.where(hlab == i)
            px = gen_int[hlab == i]
            nearwhite = float((np.sqrt(((px - np.array([255, 255, 255])) ** 2).sum(axis=1)) < 12).mean())
            if nearwhite >= 0.8 and ys.min() / H > 0.5:
                filled[hlab == i] = False
                dropped.append((int(s), round(float(ys.min() / H), 2), round(nearwhite, 2)))
    return filled, dropped

def bbox(m):
    ys, xs = np.where(m)
    return xs.min(), ys.min(), xs.max(), ys.max()

def head_crop(im_rgb, mask):
    x0, y0, x1, y1 = bbox(mask)
    h = int((y1 - y0) * 0.20)
    return im_rgb.crop((max(0, x0 - 20), y0, min(im_rgb.size[0], x1 + 20), y0 + h))

out = {}
for stem, base_fn, gen_override in JOBS:
    gen_rel = gen_override if gen_override else f'{stem}-gen1.webp'
    fin_rel = f'assets138/{stem}.webp'
    gen = Image.open(W + 'gen138/' + gen_rel).convert('RGB')
    ga = np.array(gen)
    gm, bg = hard_mask(ga)
    gm, dropped = fill_holes_selective(gm, ga.astype(int))
    gm_e = ndimage.binary_erosion(gm, iterations=1)
    af = np.clip(ndimage.gaussian_filter(gm_e.astype(np.float32), 0.9), 0, 1)
    x0, y0, x1, y1 = bbox(gm)
    rgba = np.dstack([ga, (af * 255).astype(np.uint8)])
    crop = rgba[y0:y1 + 1, x0:x1 + 1]
    Image.fromarray(crop, 'RGBA').save(W + fin_rel, quality=92)
    ratio = crop.shape[1] / crop.shape[0]
    base = Image.open(REPO_FB + base_fn).convert('RGBA')
    ba = np.array(base.convert('RGB'))
    bratio = base.size[0] / base.size[1]
    alpha = af[y0:y1 + 1, x0:x1 + 1]
    trans_frac = float((alpha < 0.05).mean())
    lab2, n2 = ndimage.label(gm)
    sizes2 = ndimage.sum(gm, lab2, range(1, n2 + 1))
    order = np.argsort(sizes2)[::-1]
    frags = [int(sizes2[i]) for i in order[1:]] if n2 > 1 else []
    out[fin_rel] = dict(gen='gen138/' + gen_rel, cutout=f'{crop.shape[1]}x{crop.shape[0]}',
                        ratio=round(float(ratio), 3), base_ratio=round(float(bratio), 3),
                        ratio_diff=round(float(ratio - bratio), 3), bg=bg,
                        transparent_frac=round(trans_frac, 3),
                        components=int(n2), frag_px=frags[:5], wedge_dropped=dropped)
    print(fin_rel, crop.shape[1], 'x', crop.shape[0], 'ratio', round(ratio, 3),
          'base', round(bratio, 3), 'diff', round(ratio - bratio, 3),
          'bg', bg, 'transparent', round(trans_frac, 3),
          'components', n2, 'frags', frags[:5], 'wedge_dropped', dropped, flush=True)
    bm, _ = hard_mask(ba)
    oc = head_crop(base.convert('RGB'), bm)
    gc = head_crop(gen, gm)
    H = 620
    oc = oc.resize((int(oc.size[0] * H / oc.size[1]), H), Image.LANCZOS)
    gc = gc.resize((int(gc.size[0] * H / gc.size[1]), H), Image.LANCZOS)
    pair = Image.new('RGB', (oc.size[0] + gc.size[0] + 16, H), (30, 30, 30))
    pair.paste(oc, (0, 0))
    pair.paste(gc, (oc.size[0] + 16, 0))
    pair.save(W + f'qc138/face_{stem}.png')
    print('  face pair', W + f'qc138/face_{stem}.png', pair.size, flush=True)

json.dump(out, open(W + 'qa138/work138_metrics.json', 'w'), indent=1, ensure_ascii=False)
print('DONE')
