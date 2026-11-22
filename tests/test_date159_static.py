# v20a159 約會場次 B1 靜態測試：ROM159_DATES 37 場齊全＋價錢跟 Q7 帶＋無 vera 殘留。
# 只驗 DATES 數據表，唔驗機制（耗一日／每週上限／撞期係 Phase 1 已有，唔郁）。
# 用法：python3 tests/test_date159_static.py
import os
import re
import sys

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
idx = open(os.path.join(ROOT, "index.html"), encoding="utf8").read()
fails = []
total = [0]


def ok(name, cond):
    total[0] += 1
    if not cond:
        fails.append(name)


# --- 抽 ROM159_DATES 塊 ---
m = re.search(r"const ROM159_DATES = \{(.*?)\n\};", idx, re.S)
ok("ROM159_DATES 塊在場", bool(m))
block = m.group(1) if m else ""

# --- 預期表：key -> (who, locId, label, cost)（Q7 已拍板定值照寫） ---
EXPECTED = {
    "hiu_roof":     ("hiu", "tvb_longmen", "廠景天台", 4),
    "hiu_location": ("hiu", "film_lion", "獅子山外景", 4),
    "hiu_market":   ("hiu", "gift_shop", "廟街夜市", 20),
    "hiu_cafe":     ("hiu", "cafe_cha", "金龍茶餐廳", 20),
    "hiu_harbour":  ("hiu", "date_harbour", "尖沙咀海傍", 6),
    "hiu_beach":    ("hiu", "date_beach", "淺水灣沙灘", 6),
    "hiu_airport":  ("hiu", "date_airport", "啟德機場", 6),
    "choi_premiere": ("choi", "film_cotton", "紅棉首映", 30),
    "choi_radio":   ("choi", "tvb_harbour", "海港廣播", 4),
    "choi_cafe":    ("choi", "cafe_cha", "金龍茶餐廳", 20),
    "choi_lounge":  ("choi", "date_lounge", "酒廊唱歌", 25),
    "choi_cinema":  ("choi", "date_cinema", "旺角戲院", 30),
    "lan_studio":   ("lan", "tvb_longmen", "星河廠景", 4),
    "lan_ktv":      ("lan", "tvb_kowloon", "九龍電視台", 4),
    "lan_rec":      ("lan", "rec_hk", "香江唱片錄音室", 4),
    "lan_lounge":   ("lan", "date_lounge", "酒廊唱歌", 25),
    "lan_beach":    ("lan", "date_beach", "淺水灣沙灘", 6),
    "lan_cafe":     ("lan", "cafe_cha", "金龍茶餐廳", 20),
    "xu_central":   ("xu", "ad_central", "中環廣告", 4),
    "xu_adm":       ("xu", "ad_adm", "金鐘創意", 4),
    "xu_premiere":  ("xu", "film_cotton", "紅棉首映", 30),
    "xu_star":      ("xu", "rec_star", "天星商場活動", 6),
    "xu_peak":      ("xu", "date_peak", "山頂", 6),
    "xu_cinema":    ("xu", "date_cinema", "旺角戲院", 30),
    "xu_cafe":      ("xu", "cafe_cha", "金龍茶餐廳", 20),
    "yip_rec":      ("yip", "rec_hk", "香江唱片", 4),
    "yip_ktv":      ("yip", "tvb_kowloon", "九龍電視台", 4),
    "yip_peak":     ("yip", "date_peak", "山頂", 6),
    "yip_cinema":   ("yip", "date_cinema", "旺角戲院", 30),
    "yip_lounge":   ("yip", "date_lounge", "酒廊唱歌", 25),
    "yip_cafe":     ("yip", "cafe_cha", "金龍茶餐廳", 20),
    "so_rec":       ("so", "rec_wanchai", "灣仔唱片", 4),
    "so_central":   ("so", "ad_central", "中環廣告", 4),
    "so_harbour":   ("so", "date_harbour", "尖沙咀海傍", 6),
    "so_airport":   ("so", "date_airport", "啟德機場", 6),
    "so_beach":     ("so", "date_beach", "淺水灣沙灘", 6),
    "so_cafe":      ("so", "cafe_cha", "金龍茶餐廳", 20),
}
PER_PERSON = {"hiu": 7, "choi": 5, "lan": 6, "xu": 7, "yip": 6, "so": 6}

# --- Q7 價錢帶（經濟重做 DESIGN.md §4.8；v377 第三輪 B7 減價後帶） ---
# 散步類＋海傍／山頂／淺水灣／啟德 $0–6；廟街 $10–30；茶記 $15–25；
# 戲院／首映 $25–35；酒廊 $20–30。
def q7_band(loc):
    if loc == "gift_shop":
        return (10, 30)
    if loc == "cafe_cha":
        return (15, 25)  # v377 B7 減價
    if loc in ("film_cotton", "date_cinema"):
        return (25, 35)  # v377 B7 減價
    if loc == "date_lounge":
        return (20, 30)  # v377 B7 減價
    return (0, 6)  # 散步類（廠景／外景／電台／錄音室／廣告場合／商場活動）
                   # ＋海傍／山頂／淺水灣／啟德


# --- 逐場抽頭行：key / who / locId / label / cost ---
ENTRY_RE = re.compile(
    r'^\s{2}(\w+):\s*\{\s*who:"(\w+)", locId:"([^"]+)", label:"([^"]+)", cost:(\d+),',
    re.M)
heads = list(ENTRY_RE.finditer(block))
entries = {}
for em in heads:
    key, who, loc, label, cost = em.groups()
    entries[key] = {"who": who, "locId": loc, "label": label, "cost": int(cost),
                    "start": em.start(), "end": None}
for i, em in enumerate(heads):
    key = em.group(1)
    entries[key]["end"] = heads[i + 1].start() if i + 1 < len(heads) else len(block)

# --- 場數齊全 ---
ok("DATES 共 37 場", len(entries) == 37)
ok("DATES key 同預期表一字不差", set(entries) == set(EXPECTED))
for who, n in sorted(PER_PERSON.items()):
    got = sum(1 for e in entries.values() if e["who"] == who)
    ok("每人場數 %s=%d" % (who, n), got == n)

# --- 逐場：who／locId／label／cost 定值＋intro／good／bad 齊全＋Q7 帶 ---
for key in sorted(EXPECTED):
    ewho, eloc, elabel, ecost = EXPECTED[key]
    e = entries.get(key)
    ok("場在場: " + key, e is not None)
    if not e:
        continue
    ok("who: " + key, e["who"] == ewho)
    ok("locId: " + key, e["locId"] == eloc)
    ok("label: " + key, e["label"] == elabel)
    ok("cost 定值: " + key, e["cost"] == ecost)
    lo, hi = q7_band(e["locId"])
    ok("cost 喺 Q7 帶 [%d,%d]: %s=$%d" % (lo, hi, key, e["cost"]), lo <= e["cost"] <= hi)
    ok("key 前綴同 who 一致: " + key, key.split("_")[0] == e["who"])
    body = block[e["start"]:e["end"]]
    im = re.search(r'intro:"([^"]+)"', body)
    ok("intro 非空: " + key, bool(im and im.group(1).strip()))
    gm = re.search(r'good:\{\s*label:"([^"]+)",\s*line:"([^"]+)"\s*\}', body)
    ok("good label+line 齊全: " + key, bool(gm and gm.group(1).strip() and gm.group(2).strip()))
    bm = re.search(r'bad:\{\s*label:"([^"]+)",\s*line:"([^"]+)"\s*\}', body)
    ok("bad label+line 齊全: " + key, bool(bm and bm.group(1).strip() and bm.group(2).strip()))
    # good／bad 唔可以係同一句（唔寫通用罐頭句）
    if gm and bm:
        ok("good/bad 唔同句: " + key, gm.group(2) != bm.group(2))

# --- 無 vera 殘留（DATES 塊內） ---
ok("DATES 塊無 vera_", "vera_" not in block)
ok("DATES 塊無 Vera", "Vera" not in block)

# --- locId 全部係已知地點或 date_* 新點（date_* 係 B2 工人加緊嘅 LOCS，呢度唔斷言佢哋已在 LOCS） ---
lm = re.search(r"const LOCS = \[(.*?)\n\];", idx, re.S)
locs_ids = set(re.findall(r'\{ id:"([^"]+)"', lm.group(1))) if lm else set()
ok("LOCS 塊抽得到（23 個：15 舊＋6 約會新點＋v265 2 新點）", len(locs_ids) == 23)  # v20a159 整合：B2 加 6 點；v265 加服裝店／屋企 2 點
for key in sorted(entries):
    loc = entries[key]["locId"]
    ok("locId 已知或 date_* 新點: %s=%s" % (key, loc),
       loc in locs_ids or loc.startswith("date_"))

# --- 玩家面文字唔寫數字承諾：intro／good／bad 入面唔出現「+1」「-1」「加分」 ---
for key in sorted(entries):
    body = block[entries[key]["start"]:entries[key]["end"]]
    ok("場面文字無數字承諾: " + key,
       "+1" not in body and "-1" not in body and "加分" not in body and "減分" not in body)

print("test_date159_static: %d checks, %d FAIL" % (total[0], len(fails)))
for f in fails:
    print("FAIL: " + f)
sys.exit(1 if fails else 0)
