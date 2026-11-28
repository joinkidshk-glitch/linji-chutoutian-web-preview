# -*- coding: utf-8 -*-
"""v424 枱沿錨點量度：bg_loc_agency_ho 長水平邊緣（枱面前緣）偵測。
逐 y 計全闊水平邊緣強度（上 4px 平均亮度 − 下 4px 平均亮度，正值累計），
峰值 y 即枱面前緣；同 SP_FG424_ANCHOR 0.915 對照，換算三視口 CSS px 偏差。"""
from PIL import Image

im = Image.open('assets/story/locs/bg_loc_agency_ho.jpg').convert('L')
W, H = im.size
px = im.load()
scores = []
for y in range(int(H * 0.84), int(H * 0.97)):
    s = 0.0
    for x in range(10, W - 10, 4):
        above = sum(px[x, y - d] for d in range(1, 5)) / 4
        below = sum(px[x, y + d] for d in range(1, 5)) / 4
        g = above - below
        if g > 12:
            s += g
    scores.append((s, y))
scores.sort(reverse=True)
peak_y = scores[0][1]
print('img', W, H, 'edge peak y', peak_y, 'frac', round(peak_y / H, 4))
for s, y in scores[:5]:
    print(' y', y, 'frac', round(y / H, 4), 'score', round(s))
anchor = 0.915
# 三視口 dispH（measure_after fg bgSize 實測）：390x844=756、430x707=693.33、430x932=844
for vp, dispH in [('390x844', 756.0), ('430x707', 693.33), ('430x932', 844.0)]:
    dev = abs(anchor - peak_y / H) * dispH
    print(vp, 'deviation vs anchor (CSS px)', round(dev, 2))
