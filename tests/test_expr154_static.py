# v20a154 靜態守門：v138 review A1＋B1＋B2＋B3。
# A1：6 張重生表情讀實際圖檔 PIL 取樣對 base 色差（軀幹 L1 ≤19、鍾楚凝側髮 ≤140,000）
#     ＋ DLG154_CACHE 只覆蓋呢 6 個 stem（其餘 29 張唔郁、cache-buster 唔升）
# B1：plate 填滿到底（source 斷言：stage-inner 底留位清零、modal-inner 底留位清零、
#     dlg106-plate 高 170px＋底 pad 61px、掣列漸變透明；基底 118px 規則保留）
# B2：STORY_SCENE_OVERRIDE154（R_vera_meet→bg_loc_tvb_longmen 現成圖、
#     R_hiu_ending→bg_154_rooftop 新圖）＋ spBgClass 接受 bg_154_ ＋ 兩圖檔存在
# B3：舊行 if(stem119) bright = "1" 已刪，影聽者跟正常 bright 計算（source 斷言）
# 不變量：SAVE key／softRev／產品 ?v= 不變
# 量度方法（同 review／measure154_gen2.json）：
#   軀幹：y 0.30–0.45、x 0.30–0.70、alpha>128 像素平均 RGB，對 base 取 L1 距離
#   鍾楚凝：y 0.45–0.75、x 外側 25% opaque 像素數（base 約 105k，錯圖約 204k）
# 反證：對 pristine main（e08a070）跑必須乾淨 FAIL（A1 色差／B1／B2／B3 斷言全跌），唔 crash。
# 用法：python3 tests/test_expr154_static.py [path-to-index.html]
import os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
IDX = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else os.path.join(HERE, "..", "index.html")
ROOT = os.path.dirname(IDX)
with open(IDX, encoding="utf-8") as f:
    src = f.read()

fails, warns = [], []
def ck(name, cond):
    print(("PASS " if cond else "FAIL ") + name)
    if not cond: fails.append(name)
def info(msg): print("INFO " + msg)

# ---------- A1：PIL 色差 ----------
try:
    from PIL import Image
    def avg_rgb(path, y0, y1, x0=0.30, x1=0.70):
        im = Image.open(path).convert("RGBA"); w, h = im.size
        px = im.load(); rs = gs = bs = n = 0
        for y in range(int(h * y0), int(h * y1)):
            for x in range(int(w * x0), int(w * x1)):
                r, g, b, a = px[x, y]
                if a > 128: rs += r; gs += g; bs += b; n += 1
        return [round(rs / n), round(gs / n), round(bs / n)] if n else None
    def fringe_count(path):
        im = Image.open(path).convert("RGBA"); w, h = im.size; px = im.load(); n = 0
        for y in range(int(h * 0.45), int(h * 0.75)):
            for x in range(w):
                if (x < int(w * 0.25) or x >= int(w * 0.75)) and px[x, y][3] > 128:
                    n += 1
        return n
    def l1(a, b): return sum(abs(x - y) for x, y in zip(a, b))
    FB = os.path.join(ROOT, "assets", "story", "fullbody")
    for stem, base in [("luk_baakyin_angry", "luk_baakyin_base"),
                       ("luk_baakyin_sad", "luk_baakyin_base"),
                       ("luk_baakyin_smile", "luk_baakyin_base"),
                       ("mak_zhendong_angry", "mak_zhendong_base"),
                       ("mak_zhendong_smile", "mak_zhendong_base")]:
        nb = os.path.join(FB, stem + ".webp"); bb = os.path.join(FB, base + ".webp")
        d = l1(avg_rgb(bb, 0.30, 0.45), avg_rgb(nb, 0.30, 0.45))
        info("%s torso L1 vs base = %d (<=19)" % (stem, d))
        ck("A1 %s 軀幹色差 L1<=19（實量 %d）" % (stem, d), d <= 19)
    dn = l1(avg_rgb(os.path.join(FB, "luk_baakyin_base.webp"), 0.20, 0.30),
            avg_rgb(os.path.join(FB, "luk_baakyin_angry.webp"), 0.20, 0.30))
    info("luk_baakyin_angry neck V L1 = %d (<=19)" % dn)
    ck("A1 陸柏言 angry 頸 V 區色差 L1<=19（實量 %d）" % dn, dn <= 19)
    fb = fringe_count(os.path.join(FB, "chung_choning_base.webp"))
    fn = fringe_count(os.path.join(FB, "chung_choning_angry.webp"))
    info("chung_choning_angry fringe = %d (base %d, <=140000)" % (fn, fb))
    ck("A1 鍾楚凝 angry 側髮量落返 base 水平（實量 %d <= 140000）" % fn, fn <= 140000)
except ImportError:
    ck("A1 PIL 可用（取樣斷言要 PIL）", False)

# ---------- A1：cache-buster 只覆蓋 6 個 stem ----------
m = re.search(r"const DLG154_CACHE = \{([^}]*)\}", src, re.S)
keys = sorted(re.findall(r'"([a-z_]+)":"20a154"', m.group(1))) if m else []
ck("A1 DLG154_CACHE 存在且恰好 6 個 stem",
   keys == ["chung_choning_angry", "luk_baakyin_angry", "luk_baakyin_sad",
            "luk_baakyin_smile", "mak_zhendong_angry", "mak_zhendong_smile"])
ck("A1 其餘表情 cache-buster 唔郁（addStem 預設仍係 20a106）",
   '"20a106"' in src and '|| "20a106"' in src)
ck("A1 新圖沿用同一路徑（addStem 按 stem＋expr 拼路徑）",
   'push("assets/story/fullbody/"+st+"_"+ex+".webp?v="+v);' in src)

# ---------- B1：plate 填滿到底 ----------
ck("B1 (1) 對白／旁白模式 .sp-stage-inner padding-bottom 清零（safe-area）",
   "#mask.story-play-on:has(.sp-mode-dialogue) .story-play .sp-stage-inner" in src
   and "padding-bottom:env(safe-area-inset-bottom,0px);" in src)
ck("B1 (2) 故事播放 #modal-inner padding-bottom:0（:not(.tut-on) 拼滿 (2,2,0) 贏 L3506）",
   "#mask.story-play-on:not(.tut-on) #modal-inner{" in src
   and re.search(r"#mask\.story-play-on:not\(\.tut-on\) #modal-inner\{\s*padding-bottom:0;", src) is not None)
ck("B1 (3) .dlg106-plate 高 118→170px（對白／旁白限定）",
   "#mask.story-play-on:has(.sp-mode-dialogue) .story-play .dlg106-plate" in src
   and "height:170px;" in src)
ck("B1 (3) plate 底 pad 61px 避掣列（calc(61px + safe-area)）",
   "padding-bottom:calc(61px + env(safe-area-inset-bottom,0px));" in src)
ck("B1 (3) 舊 bust 路徑 .sp-plate 同樣加底 pad 61px",
   "#mask.story-play-on:has(.sp-mode-dialogue) .story-play .sp-stage-inner .sp-plate" in src)
ck("B1 (4) 對白／旁白模式 #modal-btns 漸變→transparent",
   re.search(r"#mask\.story-play-on:has\(\.sp-mode-dialogue\) #modal-btns,\s*#mask\.story-play-on:has\(\.sp-mode-narration\) #modal-btns\{\s*background:transparent;", src) is not None)
ck("B1 基底 118px 規則保留（覆寫係限定範圍，唔係刪基底）",
   "height:118px" in src)

# ---------- B2：單人舞台場景圖 ----------
ck("B2 STORY_SCENE_OVERRIDE154 有 R_vera_meet→bg_loc_tvb_longmen（重用現成圖）",
   '"R_vera_meet":"bg_loc_tvb_longmen"' in src)
ck("B2 STORY_SCENE_OVERRIDE154 有 R_hiu_ending→bg_154_rooftop（新圖）",
   '"R_hiu_ending":"bg_154_rooftop"' in src)
ck("B2 spResolveBgKey 查覆寫表優先（node id）",
   "STORY_SCENE_OVERRIDE154[nid154]" in src)
ck("B2 spBgClass 接受 bg_154_ 前綴",
   '/^bg_154_/.test(key)' in src)
ck("B2 新圖檔存在：assets/story/locs/bg_154_rooftop.jpg",
   os.path.isfile(os.path.join(ROOT, "assets", "story", "locs", "bg_154_rooftop.jpg")))
ck("B2 重用圖檔存在：assets/story/locs/bg_loc_tvb_longmen.jpg",
   os.path.isfile(os.path.join(ROOT, "assets", "story", "locs", "bg_loc_tvb_longmen.jpg")))

# ---------- B3：剪影聽者變暗 ----------
ck("B3 舊行 if(stem119) bright = \"1\" 已刪",
   'if(stem119) bright = "1";' not in src)
ck("B3 正常 bright 計算保留（預設 0.6／電話 0.8／講者 1）",
   'let bright = "0.6", z = 3;' in src
   and 'if(mode106==="phone"){ bright = "0.8"; z = 3; }' in src
   and 'else if(mode106!=="narration" && isActive){ bright = "1"; z = 4; }' in src)
ck("B3 影聽者繼續用 _dim 資產（dlg119Candidates 講者 base／聽者 _dim）",
   "cands = dlg119Candidates(stem119, !isActive);" in src)
ck("B3 v20a154 B3 註釋有寫明實效約 0.47（誠實交代）",
   "0.78" in src and "0.47" in src)

# ---------- 不變量 ----------
ck("SAVE key 不變 starVolunteer_map_v19w", "starVolunteer_map_v19w" in src)
ck("softRev 不變 s107", '"s107"' in src or "s107" in src)
ck("產品 ?v= 不變 v20a10", "?v=v20a10" in src or "v20a10" in src)

print("RESULT " + ("FAIL (" + str(len(fails)) + ")" if fails else "PASS"))
sys.exit(1 if fails else 0)
