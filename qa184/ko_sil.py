#!/usr/bin/env python3
"""v20a178-strip 實駕輔助：數一張截圖入面有幾多粒剪影降級色 (29,24,50)（#1d1832）。
drawSpr 載唔到 sprite 就畫兩格 #1d1832 剪影（闊方頭＋短身，Q 版比例），企位唔郁。
v20a178-strip 之後高俊傑冇 Q 版 sprite，唱名嗰刻佢嗰位應該係剪影（預期中間狀態，
v180 先換做 PixelLab character 直接用）。舊 ko_names 截圖（有紅褸嗰陣）實測 silPx = 0，
呢隻色喺舞台截圖入面只屬於降級剪影，係乾淨嘅分辨器。
用系統 python3 跑（Playwright venv 冇 PIL，見 drive178.py）。
用法：/usr/bin/python3 qa178/ko_sil.py <png> -> {"silPx": N, "bbox": {...}|null}"""
import json
import sys

from PIL import Image

path = sys.argv[1]
im = Image.open(path).convert("RGB")
w, h = im.size
pts = [(x, y) for y in range(h) for x in range(w)
       if im.getpixel((x, y)) == (29, 24, 50)]
if not pts:
    print(json.dumps({"silPx": 0, "bbox": None}))
    sys.exit(0)
xs = [p[0] for p in pts]
ys = [p[1] for p in pts]
print(json.dumps({"silPx": len(pts),
                  "bbox": {"x0": min(xs), "x1": max(xs), "y0": min(ys), "y1": max(ys)}}))
