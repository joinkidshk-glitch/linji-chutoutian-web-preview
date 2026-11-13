# -*- coding: utf-8 -*-
# v20a199 C1 bake：將 qa199/crop199.py 出嘅兩個新 bust（hero_awi／awi_s3）寫入 index.html。
# 只換兩個 data URI 值（單行替換，行數不變）；逐字核實舊值出現一次、新值解碼 240×312、
# sha 同 qa199/crop199.json 一致；awi_s2 同其餘 19 個 bust 原封不動。
import base64, hashlib, io, json, os, re, sys
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IDX = os.path.join(ROOT, "index.html")
REC = json.load(open(os.path.join(ROOT, "qa199", "crop199.json"), encoding="utf-8"))
src = open(IDX, encoding="utf-8").read()

def extract_map(text, name):
    a = text.index("const %s = {" % name)
    b = text.index("};", a) + 2
    return dict(re.findall(r'"([^"]+)":\s*"([^"]+)"', text[a:b]))

def bake(map_name, key, stem):
    new_raw = open(os.path.join(ROOT, "qa199", "busts", "%s.webp" % stem), "rb").read()
    new_b64 = "data:image/webp;base64," + base64.b64encode(new_raw).decode()
    assert hashlib.sha256(new_raw).hexdigest() == REC[key]["webp_sha256"], "crop199.json sha mismatch " + key
    assert len(base64.b64encode(new_raw)) == REC[key]["b64_len"]
    old_map = extract_map(src, map_name)
    old_val = old_map[key]
    assert old_val != new_b64, "new == old for " + key
    assert src.count(old_val) == 1, "old value count != 1 for " + key
    return old_val, new_b64

jobs = [("PORTRAITS", "hero_awi", "awi"), ("BUST109_EXTRA", "awi_s3", "awi_s3")]
new_src = src
for map_name, key, stem in jobs:
    old_val, new_b64 = bake(map_name, key, stem)
    new_src = new_src.replace(old_val, new_b64)
    print("baked %s.%s: old b64 %d -> new b64 %d" % (map_name, key, len(old_val), len(new_b64)))

# 驗證：新值解碼 240×312、sha 同 crop199 一致；awi_s2 原封不動
for map_name, key, stem in jobs:
    m = extract_map(new_src, map_name)
    raw = base64.b64decode(m[key].split(",", 1)[1])
    im = Image.open(io.BytesIO(raw)); im.load()
    assert im.format == "WEBP" and im.size == (240, 312), key
    assert hashlib.sha256(raw).hexdigest() == REC[key]["webp_sha256"], key
    print("verified %s.%s 240x312 sha %s.." % (map_name, key, REC[key]["webp_sha256"][:12]))
old_extra = extract_map(src, "BUST109_EXTRA")
new_extra = extract_map(new_src, "BUST109_EXTRA")
assert old_extra["awi_s2"] == new_extra["awi_s2"], "awi_s2 must be untouched"
print("verified awi_s2 untouched")
open(IDX, "w", encoding="utf-8").write(new_src)
print("wrote", IDX)
