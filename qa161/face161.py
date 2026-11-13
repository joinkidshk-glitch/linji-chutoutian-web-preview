#!/usr/bin/env python3
"""v20a161: locate the face (skin-tone bbox) inside a standee element screenshot,
then map it to page coords using probe JSON geometry.
Usage: face161.py [probe_json] [shots_dir] [tag]
Face = skin pixels in the top 35% of the standee shot (hair dark, suit dark blue,
hands are at hip level ~85% down, so the top band isolates the face+neck).
Skin test: R>170, G>105, B>60, R>G+18, R>B+35, G>=B.
Prints face box in shot coords, in page coords per viewport, and overlap vs intro
(element box + glyph union).
"""
import json, sys
from pathlib import Path
from PIL import Image

probe_path = Path(sys.argv[1]); shots = Path(sys.argv[2]); tag = sys.argv[3]
probe = json.loads(probe_path.read_text(encoding="utf-8"))

def skin_bbox(img):
    w, h = img.size
    px = img.convert("RGB").load()
    top = int(h * 0.35)
    xs, ys = [], []
    for y in range(top):
        for x in range(w):
            r, g, b = px[x, y]
            if r > 170 and g > 105 and b > 60 and r > g + 18 and r > b + 35 and g >= b:
                xs.append(x); ys.append(y)
    if not xs:
        return None
    return {"x": min(xs), "y": min(ys), "right": max(xs), "bottom": max(ys),
            "w": max(xs) - min(xs), "h": max(ys) - min(ys), "n": len(xs)}

def overlap(a, b):
    ox = max(0, min(a["right"], b["right"]) - max(a["x"], b["x"]))
    oy = max(0, min(a["bottom"], b["bottom"]) - max(a["y"], b["y"]))
    return {"ox": round(ox, 1), "oy": round(oy, 1), "area": round(ox * oy, 1)}

out = []
for rec in probe:
    w, h = rec["viewport"]
    shot = shots / f"standee_{w}x{h}_{tag}.png"
    img = Image.open(shot)
    fb = skin_bbox(img)
    g = rec["geom"]
    st = g["standee"]
    # element screenshot is the img box itself (devicePixelRatio 1 in headless shell);
    # scale shot coords -> page coords
    sx = st["w"] / img.size[0]
    sy = st["h"] / img.size[1]
    face_page = None
    if fb:
        face_page = {"x": round(st["x"] + fb["x"] * sx, 1), "y": round(st["y"] + fb["y"] * sy, 1),
                     "right": round(st["x"] + fb["right"] * sx, 1), "bottom": round(st["y"] + fb["bottom"] * sy, 1),
                     "w": round(fb["w"] * sx, 1), "h": round(fb["h"] * sy, 1)}
    intro = g["intro"]
    glyphs = g["introText"]
    gx = {"x": min(r["x"] for r in glyphs), "y": min(r["y"] for r in glyphs),
          "right": max(r["right"] for r in glyphs), "bottom": max(r["bottom"] for r in glyphs)}
    res = {"viewport": [w, h], "shotSize": list(img.size),
           "faceShot": fb, "facePage": face_page,
           "introBox": intro, "glyphUnion": gx,
           "overlapIntroBoxFace": overlap(intro, face_page) if face_page else None,
           "overlapGlyphsFace": overlap(gx, face_page) if face_page else None}
    out.append(res)
    print(json.dumps(res, ensure_ascii=False))
Path(f"qa161/face_{tag}.json").write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
