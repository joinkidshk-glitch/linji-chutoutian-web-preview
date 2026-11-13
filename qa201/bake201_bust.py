# -*- coding: utf-8 -*-
# v20a201 bust bake：將 qa201/crop201.py 出嘅新 hero_awi bust 寫入 index.html。
# 只換 PORTRAITS.hero_awi 一個 data URI 值（單行替換，行數不變）；逐字核實舊值出現
# 一次、新值解碼 240×312、sha 同 qa201/crop201.json 一致；其餘 20 個 bust
# （含 awi_s2／awi_s3）原封不動。
import base64, hashlib, io, json, os, re
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IDX = os.path.join(ROOT, "index.html")
REC = json.load(open(os.path.join(ROOT, "qa201", "crop201.json"), encoding="utf-8"))
src = open(IDX, encoding="utf-8").read()

def extract_map(text, name):
    a = text.index("const %s = {" % name)
    b = text.index("};", a) + 2
    return dict(re.findall(r'"([^"]+)":\s*"([^"]+)"', text[a:b]))

new_raw = open(os.path.join(ROOT, "qa201", "busts", "awi.webp"), "rb").read()
new_b64 = "data:image/webp;base64," + base64.b64encode(new_raw).decode()
assert hashlib.sha256(new_raw).hexdigest() == REC["hero_awi"]["webp_sha256"], "crop201.json sha mismatch"
assert len(base64.b64encode(new_raw)) == REC["hero_awi"]["b64_len"]
old_map = extract_map(src, "PORTRAITS")
old_extra = extract_map(src, "BUST109_EXTRA")
old_val = old_map["hero_awi"]
assert old_val != new_b64, "new == old"
assert src.count(old_val) == 1, "old value count != 1"
new_src = src.replace(old_val, new_b64)
print("baked PORTRAITS.hero_awi: old b64 %d -> new b64 %d" % (len(old_val), len(new_b64)))

# 驗證：新值解碼 240×312、sha 同 crop201 一致；其餘 bust 原封不動
m = extract_map(new_src, "PORTRAITS")
raw = base64.b64decode(m["hero_awi"].split(",", 1)[1])
im = Image.open(io.BytesIO(raw)); im.load()
assert im.format == "WEBP" and im.size == (240, 312)
assert hashlib.sha256(raw).hexdigest() == REC["hero_awi"]["webp_sha256"]
print("verified PORTRAITS.hero_awi 240x312 sha %s.." % REC["hero_awi"]["webp_sha256"][:12])
for k, v in old_map.items():
    if k != "hero_awi":
        assert m[k] == v, "PORTRAITS.%s changed!" % k
new_extra = extract_map(new_src, "BUST109_EXTRA")
assert new_extra == old_extra, "BUST109_EXTRA changed!"
print("verified 其餘 20 個 bust 原封不動")
assert new_src.count("\n") == src.count("\n"), "行數變咗"
open(IDX, "w", encoding="utf-8").write(new_src)
print("wrote", IDX)
