# -*- coding: utf-8 -*-
"""v20a138 焗邊：37 張新表情圖，沿用 v106 同一方法（經 v127）（見
linji-work106/handoff106/assets_report.md；驗證記錄
linji-fullbody-batch/final106/bake_results.json）：
- 米白光邊 RGB(243,233,210) 焗入圖本身
- alpha 剪影（>128＋填洞）圓盤膨脹取「膨脹區−原剪影」邊帶、
  高斯柔化（sigma = 0.7*r/18）、畫布四邊各擴 r、原圖置中貼上
- 半徑 r = round(3 × 原生高 / 422)
- 存 WebP q92
驗證（逐張，同 v106 欄位）：尺寸＝原圖+2r、alpha 保留、邊帶像素
抽樣 ≥95% 係米白 ±12、人物內部大差異（>40）<1%、單一邊帶
（米白像素唔可以喺離剪影 >r+1 嘅地方出現，即唔准兩重邊）。
用法：python3 qa127/bake127.py
輸入：~/workspace/linji-work138/assets138/{37 張}
輸出：qa138/baked138/{37 張} ＋ qa138/bake_results138.json
"""
import json, os
import numpy as np
from PIL import Image
from scipy import ndimage

BATCH = "/home/hatch/workspace/linji-work138/assets138/"
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "baked138")
os.makedirs(OUT, exist_ok=True)

CREAM = np.array([243, 233, 210], dtype=np.int16)
FILES = [
    "chai_zanhoi_angry.webp",
    "chai_zanhoi_shy.webp",
    "chai_zanhoi_smile.webp",
    "chai_zanhoi_think.webp",
    "cheung_hakfan_serious.webp",
    "cheung_tsijun_sad.webp",
    "cheung_tsijun_think.webp",
    "chung_choning_angry.webp",
    "crew_laolinji_serious.webp",
    "extra_ad_fen_sad.webp",
    "extra_ad_fen_serious.webp",
    "ho_sang_surprise.webp",
    "ko_chunkit_shy.webp",
    "ko_chunkit_think.webp",
    "lin_hiu_serious.webp",
    "lin_hiu_smile.webp",
    "liu_bingxing_sad.webp",
    "liu_bingxing_surprise.webp",
    "liu_bingxing_think.webp",
    "lok_gasing_angry.webp",
    "lok_gasing_shy.webp",
    "lok_gasing_smile.webp",
    "lok_gasing_surprise.webp",
    "lui_ging_serious.webp",
    "luk_baakyin_angry.webp",
    "luk_baakyin_sad.webp",
    "luk_baakyin_smile.webp",
    "mak_zhendong_angry.webp",
    "mak_zhendong_smile.webp",
    "ngai_wingnaam_angry.webp",
    "ngai_wingnaam_serious.webp",
    "ngai_wingnaam_smile.webp",
    "ngai_wingnaam_surprise.webp",
    "ngai_wingnaam_think.webp",
    "so_jiyan_surprise.webp",
    "tsui_poushan_serious.webp",
    "vera_serious.webp",
]

def disk(r):
    y, x = np.ogrid[-r:r + 1, -r:r + 1]
    return (x * x + y * y) <= r * r

results = []
for fn in FILES:
    src = os.path.join(BATCH, fn)
    im = Image.open(src).convert("RGBA")
    a = np.array(im)
    w, h = im.size
    r = round(3 * h / 422)
    alpha = a[:, :, 3]
    mask = ndimage.binary_fill_holes(alpha > 128)
    dil = ndimage.binary_dilation(mask, structure=disk(r))
    ring = dil & ~mask
    sigma = 0.7 * r / 18.0
    ring_f = ndimage.gaussian_filter(ring.astype(np.float32), sigma)
    ring_f = np.clip(ring_f, 0, 1)
    # 新畫布：米白邊層（alpha＝柔化後邊帶，平移 r 對齊擴大後畫布）＋原圖置中
    canvas = np.zeros((h + 2 * r, w + 2 * r, 4), dtype=np.uint8)
    edge_alpha = np.zeros((h + 2 * r, w + 2 * r), dtype=np.uint8)
    edge_alpha[r:r + h, r:r + w] = (ring_f * 255).astype(np.uint8)
    canvas[:, :, 0] = CREAM[0]
    canvas[:, :, 1] = CREAM[1]
    canvas[:, :, 2] = CREAM[2]
    canvas[:, :, 3] = edge_alpha
    # 原圖置中貼上（v106「貼上」＝原樣覆蓋，唔係同邊層混色：原圖 alpha>0
    # 嘅像素 RGBA 原封不動，內部先至唔會被米白邊染到；半透明羽化邊
    # 保持原色，渲染時先同底下邊層合成）
    region = canvas[r:r + h, r:r + w, :]
    keep = a[:, :, 3] > 0
    region[keep] = a[keep]
    canvas[r:r + h, r:r + w, :] = region
    out_path = os.path.join(OUT, fn)
    Image.fromarray(canvas, "RGBA").save(out_path, quality=92)

    # ---------- 驗證（同 v106 口徑） ----------
    b = np.array(Image.open(out_path).convert("RGBA"))
    bh, bw = b.shape[0], b.shape[1]
    size_ok = (bw, bh) == (w + 2 * r, h + 2 * r)
    has_alpha = bool((b[:, :, 3] < 255).any() and (b[:, :, 3] > 0).any())
    ring_b = np.zeros((bh, bw), dtype=bool)
    ring_b[r:r + h, r:r + w] = ring
    edge_px = int(ring_b.sum())
    edge_sel = ring_b & (b[:, :, 3] > 200)
    if edge_sel.sum():
        d = np.abs(b[:, :, :3].astype(np.int16) - CREAM).max(axis=2)
        edge_color_frac = float((d[edge_sel] <= 12).mean())
    else:
        edge_color_frac = 0.0
    # 內部：原剪影區（平移 r）同原圖比較，大差異（>40）佔比
    d2 = np.abs(b[r:r + h, r:r + w, :3].astype(np.int16) - a[:, :, :3].astype(np.int16))
    # 只比較原圖不透明像素（透明區原圖 RGB 無意義）
    inner_opaque = mask & (alpha > 128)
    interior_bigdiff_frac = float((d2.max(axis=2)[inner_opaque] > 40).mean()) if inner_opaque.sum() else 0.0
    # alpha 保留：同原圖（padding 區 alpha=0）逐像素相同嘅比例
    padded_a = np.zeros((bh, bw), dtype=np.uint8)
    padded_a[r:r + h, r:r + w] = alpha
    alpha_preserved_frac = float((b[:, :, 3] == padded_a).mean())
    # 單一邊帶：米白不透明像素唔可以離剪影超過 r+1（兩重邊／光暈即現形）
    dist = ndimage.distance_transform_edt(~mask)
    dist_b = np.zeros((bh, bw), dtype=np.float32)
    dist_b[r:r + h, r:r + w] = dist
    cream_opaque = (b[:, :, 3] > 200) & (np.abs(b[:, :, :3].astype(np.int16) - CREAM).max(axis=2) <= 12)
    far_cream_px = int((cream_opaque & (dist_b > r + 1)).sum())
    # 輸入預檢：外框 1px 全透明（即輸入本身冇預焗邊頂住畫布邊）
    frame = np.concatenate([alpha[0, :], alpha[-1, :], alpha[:, 0], alpha[:, -1]])
    frame_transparent_frac = float((frame == 0).mean())
    ok = bool(size_ok and has_alpha and edge_color_frac >= 0.95
              and interior_bigdiff_frac < 0.01 and far_cream_px == 0)
    rec = {
        "file": fn, "r": r, "orig_size": [w, h], "baked_size": [bw, bh],
        "orig_bytes": os.path.getsize(src), "bytes": os.path.getsize(out_path),
        "size_ok": bool(size_ok), "has_alpha": bool(has_alpha),
        "edge_px": edge_px, "edge_color_frac": edge_color_frac,
        "interior_bigdiff_frac": interior_bigdiff_frac,
        "alpha_preserved_frac": alpha_preserved_frac,
        "far_cream_px": far_cream_px, "single_edge_ok": far_cream_px == 0,
        "frame_transparent_frac": frame_transparent_frac,
        "pass": ok,
    }
    results.append(rec)
    print(f"{fn}: r={r} {w}x{h}->{bw}x{bh} edge={edge_color_frac:.4f} "
          f"bigdiff={interior_bigdiff_frac:.5f} alpha_pres={alpha_preserved_frac:.4f} "
          f"far_cream={far_cream_px} frame_transp={frame_transparent_frac:.3f} "
          f"{'PASS' if ok else 'FAIL'}")

with open(os.path.join(HERE, "bake_results138.json"), "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=1)
print("RESULT", "PASS" if all(x["pass"] for x in results) else "FAIL",
      f"{sum(x['pass'] for x in results)}/{len(results)}")
