# -*- coding: utf-8 -*-
"""v424 全覆蓋 scan（after）：pixel sanity + sidecar geometry，同基線 scan424.json 對照。"""
import os, json
from PIL import Image

BASE = "/home/hatch/workspace/linji-work424/qa424/out/scan_after"
shots = sorted(p[:-4] for p in os.listdir(os.path.join(BASE, "shots")) if p.endswith(".png"))
out = {"pixel": {}, "geometry": {}, "clickables": {}, "counts": {}}
full, crop = [], []
for name in shots:
    png = os.path.join(BASE, "shots", name + ".png")
    im = Image.open(png).convert("RGB")
    W, H = im.size
    scp = os.path.join(BASE, "sidecars", name + ".json")
    vp = {"width": 390, "height": 844}
    sc = {}
    if os.path.exists(scp):
        try:
            sc = json.load(open(scp, encoding="utf-8"))
            vp = sc.get("viewport") or vp
        except Exception:
            sc = {}
    vw, vh = float(vp.get("width", 390)), float(vp.get("height", 844))
    is_full = abs(W / H - vw / vh) <= 0.02 and W >= vw
    (full if is_full else crop).append(name)
    small = im.resize((min(im.width, 195), min(im.height, 422)))
    px = list(small.getdata())
    n = len(px)
    mean = sum(0.2126 * p[0] + 0.7152 * p[1] + 0.0722 * p[2] for p in px) / n
    black = sum(1 for p in px if p[0] < 12 and p[1] < 12 and p[2] < 12) / n
    uniq = len(set(px))
    out["pixel"][name] = {"size": [W, H], "viewport": [vw, vh], "meanLum": round(mean, 1),
                          "blackShare": round(black, 3), "uniq": uniq,
                          "blank": mean > 250 and uniq < 40, "dark": mean < 25}
    texts = [t for t in ((sc.get("data") or {}).get("texts") or []) if t.get("hit") is True]
    clipped = [t["text"][:24] for t in texts if t["x"] < -1 or t["y"] < -1 or t["x"] + t["w"] > vw + 1 or t["y"] + t["h"] > vh + 1]
    coll = []
    for i in range(len(texts)):
        for j in range(i + 1, len(texts)):
            a, b = texts[i], texts[j]
            ox = min(a["x"] + a["w"], b["x"] + b["w"]) - max(a["x"], b["x"])
            oy = min(a["y"] + a["h"], b["y"] + b["h"]) - max(a["y"], b["y"])
            if ox > 2 and oy > 2:
                inter = ox * oy
                smaller = min(a["w"] * a["h"], b["w"] * b["h"])
                if smaller > 0 and inter / smaller > 0.35:
                    coll.append([a["text"][:16], b["text"][:16], round(inter / smaller, 2)])
    out["geometry"][name] = {"clipped": clipped[:8], "collisions": coll[:8], "nHit": len(texts)}
    out["clickables"][name] = (sc.get("data") or {}).get("clickables")
out["counts"] = {"shots": len(shots), "full": len(full), "crop": len(crop)}
json.dump(out, open(os.path.join(BASE, "scan_after.json"), "w"), ensure_ascii=False, indent=1)

base = json.load(open("/home/hatch/workspace/linji-ui-audit-2026-11-24y/scan424.json", encoding="utf-8"))
common = sorted(set(out["pixel"]) & set(base["pixel"]))
def flags(d):
    return [k for k, v in d["pixel"].items() if v["blank"] or v["dark"]]
def clips(d):
    return {k: v["clipped"] for k, v in d["geometry"].items() if v["clipped"]}
def colls(d):
    return {k: v["collisions"] for k, v in d["geometry"].items() if v["collisions"]}
print("shots", len(shots), "full", len(full), "crop", len(crop), "commonWithBaseline", len(common))
print("pixel flags after:", flags(out))
print("pixel flags baseline(common):", [k for k in flags(base) if k in common])
ca, cb = clips(out), clips(base)
print("clipped after:", len(ca), list(ca)[:20])
print("clipped baseline(common):", len([k for k in cb if k in common]), [k for k in cb if k in common][:20])
print("new clipped:", [k for k in ca if k in common and k not in cb])
oa, ob = colls(out), colls(base)
print("collisions after:", len(oa), list(oa)[:20])
print("collisions baseline(common):", len([k for k in ob if k in common]), [k for k in ob if k in common][:20])
print("new collisions:", [k for k in oa if k in common and k not in ob])
