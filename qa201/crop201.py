# -*- coding: utf-8 -*-
# v20a201：hero_awi bust 由新 s1 base 重裁（修 v199 review C1 嘅跟手——awi_base
# 換咗新圖，舊 bust 係由舊 base 裁出嚟，源頭唔同要跟住換；awi_s3 唔郁）。
# 幾何／tweak 同 v199 crop199.py 一字不改（FRAC 0.24、頭肩裁切、米白底 #F2EBD8、
# 240×312 WebP q80、s1 淺藍恤衫加深 R×0.88／G×0.93／B×1.02，下半區 y≥55%）。
# 舊記錄由 qa199/crop199.json 讀（hero_awi 舊 sha／舊 b64_len）。
# 輸出：qa201/busts/awi.webp＋qa201/crop201.json（1 鍵 hero_awi）。
# 入 index.html 嗰步由 qa201/bake201_bust.py 做。
import base64, hashlib, io, json, os
import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
CREAM = (244, 234, 210, 255)
FRAC = 0.24
OUT_W, OUT_H = 240, 312
QUALITY = 80

def head_cx(a, H, W):
    band = a[int(H*0.02):int(H*0.12), :]
    ys, xs = np.where(band > 200)
    return float(xs.mean()) if len(xs) else W / 2

def tweak_shirt(arr, stem):
    h = arr.shape[0]
    a = arr.astype(np.float32)
    y0 = int(h * 0.55)
    sub = a[y0:]
    before = sub.reshape(-1, 3).mean(axis=0)
    if stem == "awi":
        mask = ((sub[:, :, 2] - sub[:, :, 0] >= 12) & (sub[:, :, 2] >= 150))
        sub[mask, 0] *= 0.88
        sub[mask, 1] *= 0.93
        sub[mask, 2] *= 1.02
    else:
        mask = np.zeros(sub.shape[:2], dtype=bool)
    a[y0:] = sub
    after = a[y0:].reshape(-1, 3).mean(axis=0)
    return np.clip(a, 0, 255).astype(np.uint8), int(mask.sum()), before.round(1).tolist(), after.round(1).tolist()

def crop_bust(stem):
    src = os.path.join(ROOT, "assets", "story", "fullbody", "%s_base.webp" % stem)
    im = Image.open(src).convert("RGBA")
    W, H = im.size
    a = np.array(im)[:, :, 3]
    ys = np.where((a > 200).any(axis=1))[0]
    y0, y1 = int(ys.min()), int(ys.max())
    fh = y1 - y0 + 1
    Hc = int(round(FRAC * fh)); Wc = int(round(Hc * 10 / 13))
    top = max(0, y0 - int(round(0.01 * fh))); top = min(top, H - Hc)
    cx = head_cx(a, H, W)
    left = int(round(cx - Wc / 2)); left = max(0, min(left, W - Wc))
    box = [left, top, left + Wc, top + Hc]
    bg = Image.new("RGBA", im.size, CREAM)
    bg.alpha_composite(im)
    cropped = np.array(bg.crop(box).convert("RGB"))
    tweaked, n_tweaked, before, after = tweak_shirt(cropped, stem)
    out = Image.fromarray(tweaked).resize((OUT_W, OUT_H), Image.LANCZOS)
    buf = io.BytesIO()
    out.save(buf, "WEBP", quality=QUALITY, method=6)
    data = buf.getvalue()
    return data, dict(stem=stem, src="assets/story/fullbody/%s_base.webp" % stem,
                      src_size=[W, H], fig_h=fh, box=box, head_cx=round(cx, 1),
                      frac=FRAC, out=[OUT_W, OUT_H], webp_bytes=len(data),
                      webp_sha256=hashlib.sha256(data).hexdigest(),
                      b64_len=len(base64.b64encode(data)),
                      tweak_pixels=n_tweaked, shirt_zone_mean_before=before,
                      shirt_zone_mean_after=after)

if __name__ == "__main__":
    os.makedirs(os.path.join(HERE, "busts"), exist_ok=True)
    report = {}
    old = json.load(open(os.path.join(ROOT, "qa199", "crop199.json"), encoding="utf-8"))
    data, meta = crop_bust("awi")
    open(os.path.join(HERE, "busts", "awi.webp"), "wb").write(data)
    meta["old_webp_sha256"] = old["hero_awi"]["webp_sha256"]
    meta["old_b64_len"] = old["hero_awi"]["b64_len"]
    report["hero_awi"] = meta
    print("hero_awi <- awi box=%s bytes=%d sha=%s.. tweak_px=%d" %
          (meta["box"], meta["webp_bytes"], meta["webp_sha256"][:12], meta["tweak_pixels"]))
    print("   shirt zone mean %s -> %s (old sha %s..)" %
          (meta["shirt_zone_mean_before"], meta["shirt_zone_mean_after"], meta["old_webp_sha256"][:12]))
    json.dump(report, open(os.path.join(HERE, "crop201.json"), "w"), indent=1, ensure_ascii=False)
    print("wrote qa201/crop201.json (1 key)")
