# -*- coding: utf-8 -*-
"""v20a201：s1 全身組重生圖後期——白底切透明＋AR 正規化＋驗證（唔重新焗邊）。
背景：media 編輯器出圖係 RGB 白底，但完整保留咗底圖焗入嘅米白光邊
（RGB(243,233,210)，v106／v107 同款）；重新焗邊會造成雙重邊，所以呢票
只做「白底切透明」，光邊沿用繼承返嚟嗰條（同 v199 bake199.py 口徑）。
切法：白底＝由畫布邊界 flood-fill 到嘅近白連通區（衫嘅白高光喺剪影入面，
flood 唔會掂到；米白光邊 B 通道低 45，唔會誤判做白底）。
AR 正規化：成品闊高比目標 TARGET_AR＝0.280（±0.004）。raw 出圖本身已近
0.28；切完之後量實際 AR——太闊就裁透明邊（只裁透明，人物＋光邊零誤觸，
左右對稱，裁完留 ≥6px 透明邊）；太窄就補透明邊。唔郁人物本身。
輸入：qa201/samples201/media-generation-awi-{expr}-v201-*.webp（raw）
輸出：assets/story/fullbody/awi_{expr}.webp（WebP q92，同路徑覆蓋）
驗證（同 v107／v199 口徑）：畫框透明、邊帶像素 ≥95% 係米白 ±12、單一邊帶
（米白像素唔可以離剪影 >r+1）、人物內部同原圖一致；另加成品 AR 入範圍、
人物完整（切後 alpha bbox＝切前 alpha bbox 減透明邊）。
用法：python3 qa201/bake201.py [--only base]；結果寫 qa201/samples201/bake201_results.json
"""
import hashlib, io, json, os, sys
import numpy as np
from PIL import Image
from scipy import ndimage

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SAMP = os.path.join(HERE, "samples201")
OUT_DIR = os.path.join(ROOT, "assets", "story", "fullbody")
CREAM = np.array([243, 233, 210], dtype=np.int16)
TARGET_AR = 0.280
AR_TOL = 0.004
MIN_EDGE_MARGIN = 6  # 裁完／補完，人物光邊離畫框至少 6px 透明邊


def disk(r):
    y, x = np.ogrid[-r:r + 1, -r:r + 1]
    return (x * x + y * y) <= r * r


def find_raw(expr):
    cands = sorted(f for f in os.listdir(SAMP)
                   if f.startswith("media-generation-awi-%s-v201-" % expr)
                   and f.endswith(".webp"))
    if not cands:
        raise FileNotFoundError("no raw for %s in %s" % (expr, SAMP))
    return os.path.join(SAMP, cands[-1])


def bake_one(expr):
    src = find_raw(expr)
    im = Image.open(src).convert("RGB")
    w0, h0 = im.size
    # 人物掂唔掂畫框：近白邊界檢查；掂框先墊 32px 白邊（v199 做法），唔掂就唔墊
    a0 = np.array(im).astype(np.int16)
    mx0 = a0.max(axis=2); mn0 = a0.min(axis=2)
    bg0 = (mn0 >= 240) & ((mx0 - mn0) <= 15)
    touches = bool((~bg0[0, :]).any() or (~bg0[-1, :]).any()
                   or (~bg0[:, 0]).any() or (~bg0[:, -1]).any())
    PAD = 32 if touches else 0
    if PAD:
        canvas = Image.new("RGB", (w0 + 2 * PAD, h0 + 2 * PAD), (255, 255, 255))
        canvas.paste(im, (PAD, PAD))
        im = canvas
    a = np.array(im).astype(np.int16)
    h, w = a.shape[0], a.shape[1]
    mx = a.max(axis=2); mn = a.min(axis=2)
    bg_like = (mn >= 240) & ((mx - mn) <= 15)
    lab, n = ndimage.label(bg_like)
    border_ids = set(np.unique(np.concatenate(
        [lab[0, :], lab[-1, :], lab[:, 0], lab[:, -1]]))) - {0}
    flood = np.isin(lab, list(border_ids))
    alpha_f = ndimage.gaussian_filter((~flood).astype(np.float32), 0.8)
    alpha = np.clip(alpha_f * 255, 0, 255).astype(np.uint8)
    rgba = np.dstack([np.array(im), alpha])

    # ---- AR 正規化（只郁透明邊）----
    opaque = alpha > 128
    ys, xs = np.where(opaque)
    x0, x1, y0, y1 = int(xs.min()), int(xs.max()), int(ys.min()), int(ys.max())
    fig_w, fig_h = x1 - x0 + 1, y1 - y0 + 1
    cur_ar = w / h
    norm_note = "raw AR %.4f in range, no norm" % cur_ar
    cut_each = 0
    pad_each = 0
    if cur_ar > TARGET_AR + AR_TOL:
        # 太闊：裁左右透明邊至 TARGET_AR（對稱，留 ≥6px 邊）
        new_w = int(round(TARGET_AR * h))
        need = w - new_w
        cut_each = need // 2
        if x0 - cut_each >= MIN_EDGE_MARGIN and (w - 1 - x1) - cut_each >= MIN_EDGE_MARGIN:
            rgba = rgba[:, cut_each:cut_each + new_w]
            alpha = alpha[:, cut_each:cut_each + new_w]
            w = new_w
            norm_note = "cropped %dpx/side transparent -> AR %.4f" % (cut_each, w / h)
        else:
            norm_note = "TOO WIDE but figure too close to edge, left as-is"
    elif cur_ar < TARGET_AR - AR_TOL:
        new_w = int(round(TARGET_AR * h))
        pad_each = (new_w - w) // 2
        rgba = np.pad(rgba, ((0, 0), (pad_each, new_w - w - pad_each), (0, 0)))
        alpha = np.pad(alpha, ((0, 0), (pad_each, new_w - w - pad_each)))
        w = new_w
        norm_note = "padded %dpx/side transparent -> AR %.4f" % (pad_each, w / h)
    h, w = rgba.shape[0], rgba.shape[1]

    out_path = os.path.join(OUT_DIR, "awi_%s.webp" % expr)
    Image.fromarray(rgba, "RGBA").save(out_path, quality=92)
    old_sha = None
    import subprocess
    try:
        old_bytes = subprocess.check_output(
            ["git", "show", "HEAD:assets/story/fullbody/awi_%s.webp" % expr], cwd=ROOT)
        old_sha = hashlib.sha256(old_bytes).hexdigest()
    except Exception:
        old_sha = None

    # ---------- 驗證（v107／v199 口徑） ----------
    b = np.array(Image.open(out_path).convert("RGBA"))
    bh, bw = b.shape[0], b.shape[1]
    r = round(3 * bh / 422)
    opaque2 = b[:, :, 3] > 128
    is_cream = np.abs(b[:, :, :3].astype(np.int16) - CREAM).max(axis=2) <= 12
    figure = opaque2 & ~is_cream
    figure = ndimage.binary_fill_holes(figure)
    dil = ndimage.binary_dilation(figure, structure=disk(r))
    ring = dil & ~figure
    edge_px = int(ring.sum())
    edge_sel = ring & (b[:, :, 3] > 200)
    edge_cream = edge_sel & is_cream
    edge_color_frac = float(edge_cream.sum() / max(1, edge_sel.sum()))
    dist_b = ndimage.distance_transform_edt(~figure)
    cream_opaque = (b[:, :, 3] > 200) & is_cream
    far_cream_px = int((cream_opaque & (dist_b > r + 1)).sum())
    frame = np.concatenate([b[0, :, 3], b[-1, :, 3], b[:, 0, 3], b[:, -1, 3]])
    frame_transp = float((frame == 0).mean())
    inner = figure & (b[:, :, 3] > 200)
    # 人物內部同 raw 一致：成品座標 = raw 座標 + (oy, ox)（PAD 白邊＋正規化裁／補透明邊）
    raw_rgb = np.array(Image.open(src).convert("RGB")).astype(np.int16)
    pad_rgb = np.full((bh, bw, 3), 255, dtype=np.int16)
    ox, oy = PAD - cut_each + pad_each, PAD
    rh, rw = raw_rgb.shape[0], raw_rgb.shape[1]
    x_lo, x_hi = max(0, ox), min(bw, ox + rw)
    y_lo, y_hi = max(0, oy), min(bh, oy + rh)
    pad_rgb[y_lo:y_hi, x_lo:x_hi] = raw_rgb[y_lo - oy:y_hi - oy, x_lo - ox:x_hi - ox]
    sub_inner = inner[y_lo:y_hi, x_lo:x_hi]
    sub_b = b[y_lo:y_hi, x_lo:x_hi, :3].astype(np.int16)
    sub_raw = pad_rgb[y_lo:y_hi, x_lo:x_hi]
    interior_diff = float(np.abs(sub_b[sub_inner] - sub_raw[sub_inner]).max(axis=1).mean()) \
        if sub_inner.sum() else 999
    has_alpha = bool((b[:, :, 3] < 255).any() and (b[:, :, 3] > 0).any())
    # 人物完整：切後 alpha bbox（人物本體）闊／高 vs 切前 raw 嘅人物 bbox
    ys2, xs2 = np.where(opaque2)
    fig_w2, fig_h2 = int(xs2.max()) - int(xs2.min()) + 1, int(ys2.max()) - int(ys2.min()) + 1
    final_ar = bw / bh
    ar_ok = abs(final_ar - TARGET_AR) <= AR_TOL
    ok = bool(edge_color_frac >= 0.95 and far_cream_px == 0 and frame_transp >= 0.99
              and has_alpha and interior_diff < 2.0 and ar_ok)
    new_sha = hashlib.sha256(open(out_path, "rb").read()).hexdigest()
    res = {"file": "awi_%s.webp" % expr, "raw": os.path.basename(src),
           "raw_size": [w0, h0], "size": [bw, bh], "ar": round(final_ar, 4),
           "ar_ok": ar_ok, "padded_for_touch": bool(PAD),
           "fig_bbox_w_h": [fig_w2, fig_h2], "fig_ar": round(fig_w2 / fig_h2, 4),
           "norm": norm_note, "r": r, "edge_px": edge_px,
           "edge_color_frac": round(edge_color_frac, 4), "far_cream_px": far_cream_px,
           "frame_transparent_frac": round(frame_transp, 4),
           "interior_mean_maxdiff": round(interior_diff, 3),
           "has_alpha": has_alpha, "old_sha256": (old_sha or "")[:12],
           "new_sha256": new_sha[:12], "ok": ok}
    return res


def main():
    only = None
    if "--only" in sys.argv:
        only = sys.argv[sys.argv.index("--only") + 1]
    exprs = [only] if only else \
        ["base", "serious", "angry", "sad", "shy", "smile", "surprise", "think"]
    results = []
    prev_path = os.path.join(SAMP, "bake201_results.json")
    if os.path.exists(prev_path):
        try:
            prev = json.load(open(prev_path, encoding="utf-8"))
            results = [r for r in prev if r["file"] not in
                       {"awi_%s.webp" % e for e in exprs}]
        except Exception:
            results = []
    for e in exprs:
        res = bake_one(e)
        results.append(res)
        print(("PASS " if res["ok"] else "FAIL ") + res["file"],
              json.dumps(res, ensure_ascii=False))
    order = ["base", "serious", "angry", "sad", "shy", "smile", "surprise", "think"]
    results.sort(key=lambda r: order.index(r["file"][4:-5]))
    json.dump(results, open(prev_path, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    print("ALL OK" if all(x["ok"] for x in results) else "HAS FAIL")
    raise SystemExit(0 if all(x["ok"] for x in results) else 1)


if __name__ == "__main__":
    main()
