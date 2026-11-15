# -*- coding: utf-8 -*-
"""v20a218 D-v209：藍若曦 6 張全身圖重焗——B1／B2／C1／C2 一併修。

成因（review 實測）：原圖塵點俾 16–17px 光邊圓盤放大（B1 sad 腰側 592px 半圓、
C1 think 鞋邊 1408px 圓點、C2 shy／think 各 25px 塵點）；6 張頭頂光邊俾畫布裁平
（髮頂離畫布頂 11–12px，細過光邊闊；腳底同理貼邊）。

修法（review B2 方案 b＋B1／C1 建議嘅 component 篩法）：
  1. 身體＝不透明且唔係米白 CREAM(243,233,210)±12 嘅像素（v195 口徑）；
     只留最大連通 component（人物主體），其餘細 component（塵點／邊緣碎屑）全部丟棄
     ——B1 半圓／C1 圓點本身係米白，根本唔入身體；C2 塵點係分離細 component，一併清走。
  2. 人物縮細 2%（0.98，LANCZOS），置中貼返原尺寸畫布——畫布尺寸不變
     （lan209 測試釘死尺寸），頭頂／腳底各多 ~23px 空位，光邊唔再掂畫布邊。
  3. 重焗光邊：身體膨脹 r=17（實量光邊闊；v107 公式 round(3*h/422) 同值）減身體，
     填 CREAM；alpha 成層 gaussian σ0.8 羽化（跟 v195 白底切同一口徑），外緣柔和。
  4. 透明區 RGB 填 CREAM（唔係黑），重採樣唔會洩黑邊。

覆驗（同 review 口徑）：6 張 top／bottom／left／right 行不透明像素＝0；
身體 1 個 component；遠處米白像素（離身體 >r+1）＝0；v107 ring 米白 ≥0.95；
四角 alpha 皆 0；尺寸不變；檔案 sha 同 v205 舊版唔同。
用法：python3 qa218_bake209.py（原檔先備份去 ~/workspace/linji-work218-bake209-backup/）。
"""
import hashlib
import os
import shutil

import numpy as np
from PIL import Image
from scipy import ndimage

ROOT = os.path.dirname(os.path.abspath(__file__))
FULLBODY = os.path.join(ROOT, "assets", "story", "fullbody")
BACKUP = os.path.expanduser("~/workspace/linji-work218-bake209-backup")
CREAM = np.array([243, 233, 210], dtype=np.int16)
CREAM_U8 = np.array([243, 233, 210], dtype=np.uint8)
SHRINK = 0.98
R = 17


def disk(r):
    y, x = np.ogrid[-r:r + 1, -r:r + 1]
    return (x * x + y * y) <= r * r


def rebake(fn):
    p = os.path.join(FULLBODY, fn)
    im = Image.open(p).convert("RGBA")
    w, h = im.size
    a = np.array(im)
    opaque = a[:, :, 3] > 0
    is_cream = np.abs(a[:, :, :3].astype(np.int16) - CREAM).max(axis=2) <= 12
    body_raw = opaque & (~is_cream)
    lab, n = ndimage.label(body_raw)
    sizes = ndimage.sum_labels(body_raw, lab, range(1, n + 1))
    main_id = int(np.argmax(sizes)) + 1
    body_main = lab == main_id
    dropped = int(n - 1)
    # 穩健 bbox（身體腐蝕 2px 去羽化噪點）→ 置中平移量：縮細之後將身體中心移返畫布中心
    # （think 身體偏右 25px，淨縮細唔夠，右邊光邊照掂邊；其餘幾張都有幾 px 偏置）
    er = ndimage.binary_erosion(body_main, iterations=2)
    ys, xs = np.where(er)
    # bbox 幾何中心（唔係像素平均——人物上半身實、下半身疏，平均會偏上 ~180px，成個人移落底邊）
    cx = (float(xs.min()) + float(xs.max())) / 2
    cy = (float(ys.min()) + float(ys.max())) / 2
    dx = int(round((w / 2 - cx) * SHRINK))
    dy = int(round((h / 2 - cy) * SHRINK))
    # 乾淨身體層：RGB＝原圖（身體處）／CREAM（其餘）；A＝255／0
    rgb = np.where(body_main[:, :, None], a[:, :, :3], CREAM_U8)
    al = np.where(body_main, 255, 0).astype(np.uint8)
    fig = Image.fromarray(np.dstack([rgb, al]), "RGBA")
    # 縮細 2%，置中＋平移貼返原尺寸畫布
    nw, nh = max(1, round(w * SHRINK)), max(1, round(h * SHRINK))
    small = fig.resize((nw, nh), Image.LANCZOS)
    canvas = Image.new("RGBA", (w, h), (243, 233, 210, 0))
    canvas.paste(small, ((w - nw) // 2 + dx, (h - nh) // 2 + dy))
    s = np.array(canvas)
    body_s = s[:, :, 3] > 128
    dil = ndimage.binary_dilation(body_s, structure=disk(R))
    halo = dil & (~body_s)
    # RGB：身體（含邊緣羽化 RGB）用原色，其餘（光邊＋透明區）填 CREAM
    out_rgb = np.where(s[:, :, 3:4] > 0, s[:, :, :3], CREAM_U8)
    out_a = np.clip(ndimage.gaussian_filter(dil.astype(np.float32), 0.8) * 255, 0, 255).astype(np.uint8)
    out = np.dstack([out_rgb, out_a])
    Image.fromarray(out, "RGBA").save(p, quality=92)
    return {"file": fn, "size": (w, h), "body_px": int(body_main.sum()),
            "dropped_comps": dropped, "halo_px": int(halo.sum()),
            "shift": (dx, dy)}


def verify(fn):
    """review 口徑覆驗，返 dict。"""
    p = os.path.join(FULLBODY, fn)
    im = Image.open(p).convert("RGBA")
    a = np.array(im)
    h, w = a.shape[0], a.shape[1]
    opaque = a[:, :, 3] > 0
    is_cream = np.abs(a[:, :, :3].astype(np.int16) - CREAM).max(axis=2) <= 12
    # 邊行
    top = int(opaque[0, :].sum()); bot = int(opaque[-1, :].sum())
    left = int(opaque[:, 0].sum()); right = int(opaque[:, -1].sum())
    # 身體 component 數（review 口徑：不透明 component 應為 1 個——主體＋光邊連埋；
    # 唔用「非米白」計法：WebP 壓縮令羽化邊緣像素 RGB 偏離 CREAM >12，碎成幾百個 1–2px 假 component）
    lab_o, n_o = ndimage.label(opaque)
    lab_s, n_s = ndimage.label(a[:, :, 3] > 128)
    # v107 ring：ring 米白比＋遠處米白像素
    body = opaque & (~is_cream)
    figure = ndimage.binary_fill_holes(body)
    r = round(3 * h / 422)
    ring = ndimage.binary_dilation(figure, structure=disk(r)) & (~figure)
    edge_sel = ring & (a[:, :, 3] > 200)
    frac = float((edge_sel & is_cream).sum() / max(1, edge_sel.sum()))
    dist_b = ndimage.distance_transform_edt(~figure)
    far = int((((a[:, :, 3] > 200) & is_cream) & (dist_b > r + 1)).sum())
    corners = (int(a[0, 0, 3]), int(a[0, -1, 3]), int(a[-1, 0, 3]), int(a[-1, -1, 3]))
    sha = hashlib.sha256(open(p, "rb").read()).hexdigest()[:12]
    return {"file": fn, "size": (w, h), "top": top, "bot": bot, "left": left,
            "right": right, "opaque_comps": int(n_o), "solid_comps": int(n_s),
            "ring_cream": round(frac, 4),
            "far_cream": far, "corners": corners, "sha12": sha}


if __name__ == "__main__":
    files = ["lan_ruoxi_%s.webp" % e for e in
             ["base", "sad", "serious", "shy", "smile", "think"]]
    os.makedirs(BACKUP, exist_ok=True)
    for fn in files:
        src = os.path.join(FULLBODY, fn)
        shutil.copy2(src, os.path.join(BACKUP, fn))
    print("backup -> " + BACKUP)
    for fn in files:
        print("bake", rebake(fn))
    print("--- verify (review 口徑) ---")
    ok = True
    for fn in files:
        v = verify(fn)
        good = (v["top"] == 0 and v["bot"] == 0 and v["left"] == 0 and v["right"] == 0
                and v["opaque_comps"] == 1 and v["solid_comps"] == 1 and v["far_cream"] == 0
                and v["ring_cream"] >= 0.95 and all(c == 0 for c in v["corners"]))
        ok = ok and good
        print(("PASS " if good else "FAIL ") + str(v))
    print("ALL PASS" if ok else "FAILED")
