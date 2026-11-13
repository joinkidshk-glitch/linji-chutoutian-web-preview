#!/usr/bin/env python3
"""v20a184 實駕輔助：ko_cards 截圖入面每張 csscard 上／下 20% 帶平均色。
用法：/usr/bin/python3 qa184/card_px.py <png> '<rects-json>' -> {"cards": [{"top": [r,g,b], "bottom": [r,g,b]}]}
rects 為 [{x, y, w, h}] CSS px；截圖 1:1（viewport 430，deviceScaleFactor 1）。
"""
import json
import sys

from PIL import Image

path = sys.argv[1]
rects = json.loads(sys.argv[2])
im = Image.open(path).convert("RGB")
w, h = im.size
out = []
for r in rects:
    x0 = max(0, int(r["x"]))
    y0 = max(0, int(r["y"]))
    x1 = min(w, int(r["x"] + r["w"]))
    y1 = min(h, int(r["y"] + r["h"]))
    ch = y1 - y0
    top_n = max(1, int(ch * 0.2))
    bot_n = max(1, int(ch * 0.2))
    def mean(y_a, y_b):
        pts = [(x, y) for y in range(y_a, y_b) for x in range(x0, x1)]
        if not pts:
            return [0, 0, 0]
        rs = gs = bs = 0
        for (x, y) in pts:
            pr, pg, pb = im.getpixel((x, y))
            rs += pr
            gs += pg
            bs += pb
        n = len(pts)
        return [round(rs / n), round(gs / n), round(bs / n)]
    out.append({"top": mean(y0, y0 + top_n), "bottom": mean(y1 - bot_n, y1)})
print(json.dumps({"cards": out}))
