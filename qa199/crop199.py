# -*- coding: utf-8 -*-
# v20a199 C1：s1／s3 bust 收緊裁切＋恤衫色對比（修 v195 review C1）。
# 基礎幾何跟 v20a109 crop109.py（頭肩裁切、米白底 #F2EBD8、240×312 WebP q80），
# 只改兩樣（淨係 hero_awi／awi_s3 兩鍵，awi_s2 唔郁）：
#   (1) FRAC 0.30 → 0.24（裁得貼啲：面＋領口喺框內大 ~25%，56px 細圖下領口／恤衫更易讀）；
#   (2) 恤衫色對比（淨係裁切後下半區 y≥55%，面部零誤觸——量度：兩款 mask 喺面部區
#       命中率 ≤0.02%）：s3 中性亮像素（色差 ≤10、min≥200＝白恤衫）向純白拉 60%；
#       s1 偏藍像素（B−R≥12、B≥150＝淺藍恤衫）加深（R×0.88、G×0.93、B×1.02）。
#       米白底（色差 34）同深藍褸（B＜150）唔中 mask，唔郁。
# 輸出：qa199/busts/{awi,awi_s3}.webp＋qa199/crop199.json（同 crop109.json 同 schema）。
# 入 index.html 嗰步由 qa199/bake199_bust.py 做（換兩個 data URI，逐字核實）。
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
    """arr：裁切後 RGB uint8（H×W×3）。只改 y≥55% 區，面部唔掂。回 (改咗像素數, 改前後 shirt 區平均色)。"""
    h = arr.shape[0]
    a = arr.astype(np.float32)
    y0 = int(h * 0.55)
    sub = a[y0:]
    before = sub.reshape(-1, 3).mean(axis=0)
    if stem == "awi_s3":
        mx = sub.max(axis=2); mn = sub.min(axis=2)
        mask = ((mx - mn) <= 10) & (mn >= 200)
        sub[mask] = sub[mask] + (255.0 - sub[mask]) * 0.6
    elif stem == "awi":
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
    old = json.load(open(os.path.join(ROOT, "qa109b", "crop109.json"), encoding="utf-8"))
    for key, stem in [("hero_awi", "awi"), ("awi_s3", "awi_s3")]:
        data, meta = crop_bust(stem)
        open(os.path.join(HERE, "busts", "%s.webp" % stem), "wb").write(data)
        meta["old_webp_sha256"] = old[key]["webp_sha256"]
        meta["old_b64_len"] = old[key]["b64_len"]
        report[key] = meta
        print("%s <- %s box=%s bytes=%d sha=%s.. tweak_px=%d" %
              (key, stem, meta["box"], meta["webp_bytes"], meta["webp_sha256"][:12], meta["tweak_pixels"]))
        print("   shirt zone mean %s -> %s (old sha %s..)" %
              (meta["shirt_zone_mean_before"], meta["shirt_zone_mean_after"], meta["old_webp_sha256"][:12]))
    json.dump(report, open(os.path.join(HERE, "crop199.json"), "w"), indent=1, ensure_ascii=False)
    print("wrote qa199/crop199.json (2 keys)")
