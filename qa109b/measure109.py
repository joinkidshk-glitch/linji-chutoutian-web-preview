# v20a109 B: measure alpha bbox of every fullbody *_base.webp needed for bust crops.
# Stems: 7 PORTRAITS (awi + 6 NPCS) + 14 EXTRA (awi_s2/s3 + 12 red stars) = 21.
import json, os
from PIL import Image
import numpy as np

STEMS_PORTRAITS = {  # PORTRAITS key -> fullbody stem
  "hero_awi": "awi", "npc_cheung": "cheung_tsijun", "npc_chow": "chow_choiyi",
  "npc_ho": "ho_sang", "npc_ko": "ko_chunkit", "npc_lin": "lin_hiu", "npc_vera": "vera",
}
STEMS_EXTRA = ["awi_s2", "awi_s3",
  "luk_baakyin", "liu_bingxing", "ngai_wingnaam", "yip_manji", "mak_zhendong",
  "lok_gasing", "pang_siuki", "chung_choning", "gu_mingfai", "so_jiyan",
  "chai_zanhoi", "ching_tinlok"]

rows = {}
for stem in sorted(set(list(STEMS_PORTRAITS.values()) + STEMS_EXTRA)):
    p = f"assets/story/fullbody/{stem}_base.webp"
    im = Image.open(p)
    a = np.array(im.convert("RGBA"))[:, :, 3]
    ys, xs = np.where(a > 16)
    x0, x1, y0, y1 = int(xs.min()), int(xs.max()), int(ys.min()), int(ys.max())
    W, H = im.size
    rows[stem] = dict(file=os.path.basename(p), W=W, H=H, mode=im.mode,
        bbox=[x0, y0, x1, y1], fig_w=x1 - x0 + 1, fig_h=y1 - y0 + 1,
        fig_top_frac=round(y0 / H, 4), fig_h_frac=round((y1 - y0 + 1) / H, 4),
        fig_cx_frac=round(((x0 + x1) / 2) / W, 4),
        fig_w_frac=round((x1 - x0 + 1) / W, 4))
    print(f"{stem:16s} {W}x{H} mode={im.mode} bbox x[{x0},{x1}] y[{y0},{y1}] "
          f"fig {x1-x0+1}x{y1-y0+1} top_frac={y0/H:.3f} h_frac={(y1-y0+1)/H:.3f} cx_frac={((x0+x1)/2)/W:.3f} w_frac={(x1-x0+1)/W:.3f}")
json.dump({"portraits": STEMS_PORTRAITS, "extra": STEMS_EXTRA, "measure": rows},
          open("qa109b/measure109.json", "w"), indent=1, ensure_ascii=False)
print("stems:", len(rows))
