# -*- coding: utf-8 -*-
"""v20a199：s2／s3 angry 原圖後期——白底切透明＋驗證（唔重新焗邊）。
背景：media 編輯器出圖係 RGB 白底，但完整保留咗底圖焗入嘅米白光邊
（RGB(243,233,210)，v106／v107 同款）；重新焗邊會造成雙重邊，所以呢票
只做「白底切透明」，光邊沿用繼承返嚟嗰條。
切法：白底＝由畫布邊界 flood-fill 到嘅近白連通區（衫嘅白高光喺剪影入面，
flood 唔會掂到；米白光邊 B 通道低 45，唔會誤判做白底）。
驗證（同 v107 口徑）：畫框透明、邊帶像素 ≥95% 係米白 ±12、單一邊帶
（米白像素唔可以離剪影 >r+1）、人物內部同原圖一致。
輸入：qa199/samples199/media-generation-awi-{s2,s3}-angry-v2-*.webp
輸出：assets/story/fullbody/awi_{s2,s3}_angry.webp（WebP q92）
"""
import json, os
import numpy as np
from PIL import Image
from scipy import ndimage

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # repo root (script lives in qa199/)
SRC = {
    "awi_s2_angry.webp": os.path.join(HERE, "qa199", "samples199",
        "media-generation-awi-s2-angry-v2-0-02b83207-cd16-482b-b0f2-03ab869da54a.webp"),
    "awi_s3_angry.webp": os.path.join(HERE, "qa199", "samples199",
        "media-generation-awi-s3-angry-v2-0-bcf60366-454f-4cf4-b206-a7e12a7c879f.webp"),
}
OUT_DIR = os.path.join(HERE, "assets", "story", "fullbody")
CREAM = np.array([243, 233, 210], dtype=np.int16)
results = []

def disk(r):
    y, x = np.ogrid[-r:r + 1, -r:r + 1]
    return (x * x + y * y) <= r * r

for fn, src in SRC.items():
    im = Image.open(src).convert("RGB")
    # 原圖人物光邊掂到左畫框（編輯器裁得比底圖貼），flood-fill 會斷；
    # 先墊 32px 白邊再切（效果同 v107 焗邊擴畫布一樣，成品留透明邊距）。
    PAD = 32
    im = Image.new("RGB", (im.size[0] + 2 * PAD, im.size[1] + 2 * PAD), (255, 255, 255))
    im.paste(Image.open(src).convert("RGB"), (PAD, PAD))
    a = np.array(im).astype(np.int16)
    h, w = a.shape[0], a.shape[1]
    r = round(3 * h / 422)
    # 近白底：三通道 ≥240 且色差 ≤15（米白光邊 max-min=33，唔會中）
    mx = a.max(axis=2); mn = a.min(axis=2)
    bg_like = (mn >= 240) & ((mx - mn) <= 15)
    # 只保留掂到畫框嗰個連通區（衫內白高光唔會掂框，唔會俾切走）
    lab, n = ndimage.label(bg_like)
    border_ids = set(np.unique(np.concatenate(
        [lab[0, :], lab[-1, :], lab[:, 0], lab[:, -1]]))) - {0}
    flood = np.isin(lab, list(border_ids))
    # 羽化 1px：alpha 由 flood 邊界做高斯柔化（唔好硬切出鋸齒）
    alpha_f = ndimage.gaussian_filter((~flood).astype(np.float32), 0.8)
    alpha = np.clip(alpha_f * 255, 0, 255).astype(np.uint8)
    out = np.dstack([np.array(im), alpha])
    out_path = os.path.join(OUT_DIR, fn)
    Image.fromarray(out, "RGBA").save(out_path, quality=92)

    # ---------- 驗證（v107 口徑，改為「光邊喺剪影入面」版） ----------
    # 繼承返嚟嘅光邊係不透明剪影嘅一部分，所以人物本體＝不透明且唔係米白；
    # 光邊帶＝本體膨脹 r 減本體（v107 焗邊同一幾何，方向調轉）。
    b = np.array(Image.open(out_path).convert("RGBA"))
    bh, bw = b.shape[0], b.shape[1]
    opaque = b[:, :, 3] > 128
    is_cream = np.abs(b[:, :, :3].astype(np.int16) - CREAM).max(axis=2) <= 12
    figure = opaque & ~is_cream
    figure = ndimage.binary_fill_holes(figure)
    dil = ndimage.binary_dilation(figure, structure=disk(r))
    ring = dil & ~figure
    edge_px = int(ring.sum())
    edge_sel = ring & (b[:, :, 3] > 200)
    edge_cream = edge_sel & is_cream
    edge_color_frac = float(edge_cream.sum() / max(1, edge_sel.sum()))
    # 單一邊帶：米白不透明像素離人物本體唔可以超過 r+1
    dist_b = ndimage.distance_transform_edt(~figure)
    cream_opaque = (b[:, :, 3] > 200) & is_cream
    far_cream_px = int((cream_opaque & (dist_b > r + 1)).sum())
    # 畫框透明
    frame = np.concatenate([b[0, :, 3], b[-1, :, 3], b[:, 0, 3], b[:, -1, 3]])
    frame_transp = float((frame == 0).mean())
    # 人物內部：同原圖 RGB 一致（alpha>200 嗰啲像素，唔計羽化邊）
    inner = figure & (b[:, :, 3] > 200)
    raw_rgb = np.array(Image.open(src).convert("RGB")).astype(np.int16)
    pad_rgb = np.full((bh, bw, 3), 255, dtype=np.int16)
    pad_rgb[PAD:PAD + raw_rgb.shape[0], PAD:PAD + raw_rgb.shape[1]] = raw_rgb
    interior_diff = float(np.abs(b[:, :, :3].astype(np.int16)[inner] - pad_rgb[inner]).max(axis=1).mean()) if inner.sum() else 999
    has_alpha = bool((b[:, :, 3] < 255).any() and (b[:, :, 3] > 0).any())
    ok = bool(edge_color_frac >= 0.95 and far_cream_px == 0 and frame_transp >= 0.99
              and has_alpha and interior_diff < 1.0)
    res = {"file": fn, "size": [bw, bh], "r": r, "edge_px": edge_px,
           "edge_color_frac": round(edge_color_frac, 4), "far_cream_px": far_cream_px,
           "frame_transparent_frac": round(frame_transp, 4),
           "interior_mean_maxdiff": round(interior_diff, 3),
           "has_alpha": has_alpha, "ok": ok}
    results.append(res)
    print(("PASS " if ok else "FAIL ") + fn, json.dumps(res, ensure_ascii=False))

with open(os.path.join(HERE, "qa199", "samples199", "bake199_results.json"), "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=1)
print("ALL OK" if all(x["ok"] for x in results) else "HAS FAIL")
raise SystemExit(0 if all(x["ok"] for x in results) else 1)
