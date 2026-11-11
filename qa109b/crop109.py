# v20a109 B: crop head-and-shoulders busts from v106/v107 fullbody *_base.webp.
# Geometry (measured, see qa109b/measure109.json + crop_compare.png):
#   figure spans (nearly) the full canvas height in every base file;
#   head ~ top 0-13%, shoulders widen from ~20%.
#   Rule (uniform, no per-character exceptions):
#     Hc = 0.30 * fig_h ; Wc = Hc * 10/13 (display aspect 40:52)
#     top = max(0, fig_top - 0.01*fig_h)   (fig_top is ~0-4px, so effectively 0)
#     cx  = centroid-x of opaque pixels in the head band (y 2%-12% of canvas)
#     left = clamp(cx - Wc/2, 0, W - Wc)
#   Composite onto opaque cream #F2EBD8 (same studio bust background as the
#   era-star busts + the old JPEG PORTRAITS look), resize LANCZOS, save WebP.
import base64, hashlib, io, json, os
from PIL import Image
import numpy as np

CREAM = (244, 234, 210, 255)
FRAC = 0.30
OUT_W, OUT_H = 240, 312
QUALITY = 80

STEMS_PORTRAITS = {
  "hero_awi": "awi", "npc_cheung": "cheung_tsijun", "npc_chow": "chow_choiyi",
  "npc_ho": "ho_sang", "npc_ko": "ko_chunkit", "npc_lin": "lin_hiu", "npc_vera": "vera",
}
STEMS_EXTRA = ["awi_s2", "awi_s3",
  "luk_baakyin", "liu_bingxing", "ngai_wingnaam", "yip_manji", "mak_zhendong",
  "lok_gasing", "pang_siuki", "chung_choning", "gu_mingfai", "so_jiyan",
  "chai_zanhoi", "ching_tinlok"]

def head_cx(a, H, W):
    band = a[int(H*0.02):int(H*0.12), :]
    ys, xs = np.where(band > 200)
    return float(xs.mean()) if len(xs) else W / 2

def crop_bust(stem):
    src = f"assets/story/fullbody/{stem}_base.webp"
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
    out = bg.crop(box).convert("RGB").resize((OUT_W, OUT_H), Image.LANCZOS)
    buf = io.BytesIO()
    out.save(buf, "WEBP", quality=QUALITY, method=6)
    data = buf.getvalue()
    return data, dict(stem=stem, src=src, src_size=[W, H], fig_h=fh,
                      box=box, head_cx=round(cx, 1), out=[OUT_W, OUT_H],
                      webp_bytes=len(data), webp_sha256=hashlib.sha256(data).hexdigest(),
                      b64_len=len(base64.b64encode(data)))

if __name__ == "__main__":
    os.makedirs("qa109b/busts", exist_ok=True)
    report = {}
    total_b64 = 0
    for key, stem in STEMS_PORTRAITS.items():
        data, meta = crop_bust(stem)
        open(f"qa109b/busts/{stem}.webp", "wb").write(data)
        report[key] = meta; total_b64 += meta["b64_len"]
        print(f"{key:12s} <- {stem:16s} box={meta['box']} bytes={meta['webp_bytes']} b64={meta['b64_len']}")
    for stem in STEMS_EXTRA:
        data, meta = crop_bust(stem)
        open(f"qa109b/busts/{stem}.webp", "wb").write(data)
        report[stem] = meta; total_b64 += meta["b64_len"]
        print(f"{stem:12s} <- {stem:16s} box={meta['box']} bytes={meta['webp_bytes']} b64={meta['b64_len']}")
    json.dump(report, open("qa109b/crop109.json", "w"), indent=1, ensure_ascii=False)
    print(f"21 crops, total b64 chars {total_b64} (old PORTRAITS 7 = 235693; "
          f"new PORTRAITS 7 = {sum(report[k]['b64_len'] for k in STEMS_PORTRAITS)})")
