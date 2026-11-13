#!/usr/bin/env python3
"""v20a178 實駕輔助：數一張截圖入面有幾多粒高俊傑皮褸平塗色 (182,28,32)。
用系統 python3 跑（Playwright venv 冇 PIL，見 drive178.py）。
用法：/usr/bin/python3 qa178/ko_red.py <png> -> {"koRedPx": N, "bbox": {...}|null}
全場唯一用呢隻紅嘅係高俊傑件褸（舞台紅幕布／其他人衫色實測 0 粒完全相等）。"""
import json
import sys

from PIL import Image

path = sys.argv[1]
im = Image.open(path).convert("RGB")
w, h = im.size
pts = [(x, y) for y in range(h) for x in range(w)
       if im.getpixel((x, y)) == (182, 28, 32)]
if not pts:
    print(json.dumps({"koRedPx": 0, "bbox": None}))
    sys.exit(0)
xs = [p[0] for p in pts]
ys = [p[1] for p in pts]
print(json.dumps({"koRedPx": len(pts),
                  "bbox": {"x0": min(xs), "x1": max(xs), "y0": min(ys), "y1": max(ys)}}))
