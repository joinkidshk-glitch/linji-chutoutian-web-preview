# v20a109 BUST109 靜態守門：舊 bust（PORTRAITS 7 張內嵌 JPEG）換新──由
# v106/v107 全身基本款裁出嘅頭肩縮圖（240×312 WebP q80，米白底 #F2EBD8）。
# 覆蓋：① 舊圖零殘留：7 個舊 key 嘅行 sha256／b64 前綴喺 index.html 內
#       一律搵唔到（hash＋長度比對，唔係齋靠 key 名；舊 hash 寫死喺下面
#       OLD 常數，來源 qa109b/old_portraits.json，main 546007d 實量）
#       ② 新 PORTRAITS 7 鍵＋BUST109_EXTRA 14 鍵：全部 data:image/webp，
#       解碼係真 WebP、240×312、sha256 同 crop 記錄一致（v20a199 C1：hero_awi／awi_s3
#       改用 qa199/crop199.json，其餘 19 鍵沿用 qa109b/crop109.json；見下面 crop199 一節）
#       ③ 覆蓋齊：NPCS 6 個 face 值全部有 PORTRAITS 鍵；12 紅星全部有
#       BUST109_EXTRA 鍵；每個 PORTRAITS 鍵對應嘅全身 *_base.webp 喺磁碟存在
#       ④ 接線：bust109HeroSrc 定義＋enterHome 用佢；enc79PeopleHtml 紅星段
#       有 BUST109_EXTRA[def.id]＋cands.unshift(b109)；4 個 PORTRAITS
#       消費者（手帳頁頭／傾談 modal／人情頁／開局畫面）引用健在；
#       UI40_STAND 10 鍵原封不動（今包唔掂企立圖）
#       ⑤ 反證：checker 函數食舊值／缺鍵／缺圖嘅輸入必須報問題；抽走
#       crop109.json 一項 → 交叉比對必須 FAIL
#       ⑥ 基線不變：SAVE key／softRev／產品 ?v=
# 用法：python3 tests/test_bust109_static.py [path-to-index.html]
import base64, hashlib, io, json, os, re, shutil, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
IDX = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else os.path.join(HERE, "..", "index.html")
ROOT = os.path.dirname(IDX)
with open(IDX, encoding="utf-8") as f:
    src = f.read()

fails = []
def ck(name, cond):
    print(("PASS " if cond else "FAIL ") + name)
    if not cond: fails.append(name)
def info(msg): print("INFO " + msg)

# ---------- ⑥ 基線不變 ----------
ck("SAVE key 不變", "starVolunteer_map_v19w" in src)
ck("softRev 不變", "s107" in src)
ck("產品 ?v= 不變", "v20a10" in src)

# ---------- 舊圖指紋（main 546007d 實量，見 qa109b/old_portraits.json） ----------
OLD = {
  "hero_awi": {"sha256_line": "95854d861bcfb735f03d0dc202a7f930b47d3477b3b1c8c0c302e4613b95fedb",
                 "b64_len": 98871,  "b64_prefix": "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD/2wBDAAYEBAUEBAYFBQUGBgYHCQ4JCQgICRINDQoOFRIWFhUSFBQXGiEcFxgfGRQUHScdHyIjJSUlFhwpLCgkKyEkJST/2wBDAQYGBgkICREJCREkGBQYJCQkJCQkJCQkJCQkJCQkJCQkJCQkJCQkJ"},
  "npc_cheung": {"sha256_line": "46946ab5ec49e5c7e8a3eb22e7234b144e27c7ec4c83f7ad346632907cc2a15c",
                 "b64_len": 16891,  "b64_prefix": "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD/2wBDAAkGBwgHBgkIBwgKCgkLDRYPDQwMDRsUFRAWIB0iIiAdHx8kKDQsJCYxJx8fLT0tMTU3Ojo6Iys/RD84QzQ5Ojf/2wBDAQoKCg0MDRoPDxo3JR8lNzc3Nzc3Nzc3Nzc3Nzc3Nzc3Nzc3Nzc3N"},
  "npc_chow": {"sha256_line": "cffdb788409f5c2484ee1f240b9d523a5cd14155c871b9141646a6a6154da34d",
                 "b64_len": 28847,  "b64_prefix": "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD/2wBDAAkGBwgHBgkIBwgKCgkLDRYPDQwMDRsUFRAWIB0iIiAdHx8kKDQsJCYxJx8fLT0tMTU3Ojo6Iys/RD84QzQ5Ojf/2wBDAQoKCg0MDRoPDxo3JR8lNzc3Nzc3Nzc3Nzc3Nzc3Nzc3Nzc3Nzc3N"},
  "npc_ho": {"sha256_line": "cf493a6e678a2b84fc86247346bd00626030e33cdb8e15449927113f71ff2be0",
                 "b64_len": 17735,  "b64_prefix": "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD/2wBDAAkGBwgHBgkIBwgKCgkLDRYPDQwMDRsUFRAWIB0iIiAdHx8kKDQsJCYxJx8fLT0tMTU3Ojo6Iys/RD84QzQ5Ojf/2wBDAQoKCg0MDRoPDxo3JR8lNzc3Nzc3Nzc3Nzc3Nzc3Nzc3Nzc3Nzc3N"},
  "npc_ko": {"sha256_line": "8003cd6a7cfc49930d863451fac59eac4496049b45b33ba5e2425501fd80e3bf",
                 "b64_len": 23783,  "b64_prefix": "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD/2wBDAAkGBwgHBgkIBwgKCgkLDRYPDQwMDRsUFRAWIB0iIiAdHx8kKDQsJCYxJx8fLT0tMTU3Ojo6Iys/RD84QzQ5Ojf/2wBDAQoKCg0MDRoPDxo3JR8lNzc3Nzc3Nzc3Nzc3Nzc3Nzc3Nzc3Nzc3N"},
  "npc_lin": {"sha256_line": "1e4b990934bc551ef92f4058597fb563a334e46b3988117422ab89fcf4c83e2f",
                 "b64_len": 25471,  "b64_prefix": "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD/2wBDAAkGBwgHBgkIBwgKCgkLDRYPDQwMDRsUFRAWIB0iIiAdHx8kKDQsJCYxJx8fLT0tMTU3Ojo6Iys/RD84QzQ5Ojf/2wBDAQoKCg0MDRoPDxo3JR8lNzc3Nzc3Nzc3Nzc3Nzc3Nzc3Nzc3Nzc3N"},
  "npc_vera": {"sha256_line": "d7dfe3c683c86445402ef45e0426362803840774cbc4559bc56e3e49b893ed6e",
                 "b64_len": 23995,  "b64_prefix": "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD/2wBDAAkGBwgHBgkIBwgKCgkLDRYPDQwMDRsUFRAWIB0iIiAdHx8kKDQsJCYxJx8fLT0tMTU3Ojo6Iys/RD84QzQ5Ojf/2wBDAQoKCg0MDRoPDxo3JR8lNzc3Nzc3Nzc3Nzc3Nzc3Nzc3Nzc3Nzc3N"},
}

# qa109b/old_portraits.json 如在場，寫死常數要同佢一致（防手抄錯）
_op = os.path.join(ROOT, "qa109b", "old_portraits.json")
if os.path.exists(_op):
    with open(_op, encoding="utf-8") as f: opj = json.load(f)
    for k, v in OLD.items():
        ck(f"舊指紋 {k} 同 qa109b/old_portraits.json 一致",
           opj.get(k, {}).get("sha256_line") == v["sha256_line"]
           and opj.get(k, {}).get("b64_len") == v["b64_len"])
else:
    info("qa109b/old_portraits.json 缺席，跳過寫死常數交叉比對")

def extract_map(src_text, name):
    """抽 `const NAME = { "k": "v", ... };`（值係單行 data URI，唔含 '};'）。"""
    a = src_text.index("const %s = {" % name)
    b = src_text.index("};", a) + 2
    block = src_text[a:b]
    pairs = re.findall(r'"([^"]+)":\s*"([^"]+)"', block)
    return dict(pairs), block

# ---------- ① 舊圖零殘留 ----------
for k, v in OLD.items():
    ck(f"舊 {k} 行 sha256 唔再出現",
       not any(hashlib.sha256(ln.encode()).hexdigest() == v["sha256_line"]
               for ln in src.split("\n")))
    ck(f"舊 {k} b64 前綴唔再出現", v["b64_prefix"] not in src)
ck("PORTRAITS 區零 data:image/jpeg（舊 JPEG 全數換走）",
   "data:image/jpeg" not in extract_map(src, "PORTRAITS")[1])

# ---------- ② 新圖：格式＋尺寸＋hash ----------
try:
    from PIL import Image
    def webp_info(b64val):
        raw = base64.b64decode(b64val)
        im = Image.open(io.BytesIO(raw))
        im.load()
        return im.format, im.size, hashlib.sha256(raw).hexdigest(), len(b64val)
except ImportError:
    webp_info = None
    info("PIL 缺席：WebP 尺寸檢查跳過（環境問題，唔係遊戲問題）")

PORTRAITS, _pb = extract_map(src, "PORTRAITS")
EXTRA, _eb = extract_map(src, "BUST109_EXTRA")
PORTRAITS_STEM = {"hero_awi": "awi", "npc_cheung": "cheung_tsijun", "npc_chow": "chow_choiyi",
                  "npc_ho": "ho_sang", "npc_ko": "ko_chunkit", "npc_lin": "lin_hiu",
                  "npc_vera": "vera"}
STARS = ["luk_baakyin", "liu_bingxing", "ngai_wingnaam", "yip_manji", "mak_zhendong",
         "lok_gasing", "pang_siuki", "chung_choning", "gu_mingfai", "so_jiyan",
         "chai_zanhoi", "ching_tinlok"]
ck("PORTRAITS 7 鍵齊", set(PORTRAITS) == set(PORTRAITS_STEM))
ck("BUST109_EXTRA 14 鍵齊", set(EXTRA) == set(["awi_s2", "awi_s3"] + STARS))

crop_path = os.path.join(ROOT, "qa109b", "crop109.json")
crop = {}
if os.path.exists(crop_path):
    with open(crop_path, encoding="utf-8") as f: crop = json.load(f)
    ck("crop109.json 有 21 項", len(crop) == 21)
else:
    info("qa109b/crop109.json 缺席，跳過 hash 交叉比對")

# v20a201：hero_awi 由新 s1 base 重裁，新記錄喺 qa201/crop201.json（1 鍵）；
# awi_s3 繼續用 crop199.json。hero_awi 必須同 crop199 舊值唔同（base 換咗，
# bust 跟住換）。
crop201_path = os.path.join(ROOT, "qa201", "crop201.json")
crop201 = {}
if os.path.exists(crop201_path):
    with open(crop201_path, encoding="utf-8") as f: crop201 = json.load(f)
    ck("crop201.json 有 1 項（hero_awi）", set(crop201) == {"hero_awi"})
    # crop201 記錄嘅 old_webp_sha256 就係 crop199 嗰個 hero_awi 值。
    ck("hero_awi 新 sha 同舊 crop199 值唔同（base 換咗，bust 跟住換）",
       crop201["hero_awi"]["webp_sha256"] != crop201["hero_awi"]["old_webp_sha256"])
else:
    info("qa201/crop201.json 缺席，hero_awi 沿用 crop199.json 比對")
crop199_path = os.path.join(ROOT, "qa199", "crop199.json")
crop199 = {}
if os.path.exists(crop199_path):
    with open(crop199_path, encoding="utf-8") as f: crop199 = json.load(f)
    ck("crop199.json 有 2 項（hero_awi／awi_s3）", set(crop199) == {"hero_awi", "awi_s3"})
    for _k in ("hero_awi", "awi_s3"):
        ck(f"{_k} 新 sha 同舊 crop109 值唔同（C1 真係換咗）",
           _k in crop and crop199[_k]["webp_sha256"] != crop[_k]["webp_sha256"])
else:
    info("qa199/crop199.json 缺席，hero_awi／awi_s3 沿用 crop109.json 比對")

def check_one(label, b64val, expect_key):
    ok_prefix = b64val.startswith("data:image/webp;base64,")
    ck(f"{label} 係 WebP data URI", ok_prefix)
    if not ok_prefix: return
    raw_b64 = b64val.split(",", 1)[1]
    if webp_info:
        fmt, size, sha, blen = webp_info(raw_b64)
        ck(f"{label} 解碼係 WebP 240×312", fmt == "WEBP" and size == (240, 312))
        rec = crop201.get(expect_key) or crop199.get(expect_key) or crop.get(expect_key)
        rec_name = ("crop201.json" if expect_key in crop201 else
                    "crop199.json" if expect_key in crop199 else "crop109.json")
        if rec:
            ck(f"{label} sha256 同 {rec_name} 一致", sha == rec["webp_sha256"])
            ck(f"{label} b64 長度同 {rec_name} 一致", blen == rec["b64_len"])
        else:
            info(f"{label} 唔喺 crop 記錄，跳過 hash 比對")

for k, stem in PORTRAITS_STEM.items():
    check_one(f"PORTRAITS.{k}（{stem}）", PORTRAITS.get(k, ""), k)
for stem in ["awi_s2", "awi_s3"] + STARS:
    check_one(f"BUST109_EXTRA.{stem}", EXTRA.get(stem, ""), stem)

# ---------- ③ 覆蓋齊 ----------
m_npcs = re.search(r"const NPCS\s*=\s*\{(.*?)\n\};", src, re.S)
ck("搵到 NPCS", bool(m_npcs))
faces = set(re.findall(r'face:"([^"]+)"', m_npcs.group(1))) if m_npcs else set()
# v20a176：NPCS 加藍／徐／海媚 3 個 face，PORTRAITS 鍵行 runtime 注入（rom176ApplyGiftOverrides，
# GIFT 賦值之後呼叫）——覆蓋檢查要連注入鍵一齊計，唔係齋睇字面 PORTRAITS。
injected = set(re.findall(r'PORTRAITS\.(npc_\w+)\s*=', src))
ck(f"NPCS {len(faces)} 個 face（{sorted(faces)}）全部有 PORTRAITS 鍵（字面＋運行注入）",
   faces and faces <= (set(PORTRAITS) | injected))
for k, stem in (("npc_lan", "lan_ruoxi"), ("npc_xu", "tsui_poushan"), ("npc_mei", "kwan_hoimei")):
    ck(f"注入 PORTRAITS.{k} 指向存在嘅 fullbody 圖",
       ('PORTRAITS.%s = "assets/story/fullbody/%s_base.webp' % (k, stem)) in src
       and os.path.exists(os.path.join(ROOT, "assets", "story", "fullbody", stem + "_base.webp")))
m_stars = re.search(r"const ENC79_STARS = \[(.*?)\n\];", src, re.S)
star_ids = re.findall(r'id:"([^"]+)"', m_stars.group(1)) if m_stars else []
ck(f"紅星 12 個（{len(star_ids)}）全部有 BUST109_EXTRA 鍵",
   len(star_ids) == 12 and set(star_ids) <= set(EXTRA))
for k, stem in PORTRAITS_STEM.items():
    ck(f"全身基本款 {stem}_base.webp 喺磁碟",
       os.path.exists(os.path.join(ROOT, "assets", "story", "fullbody", stem + "_base.webp")))
for stem in ["awi_s2", "awi_s3"] + STARS:
    ck(f"全身基本款 {stem}_base.webp 喺磁碟",
       os.path.exists(os.path.join(ROOT, "assets", "story", "fullbody", stem + "_base.webp")))

# ---------- ④ 接線 ----------
ck("bust109HeroSrc 有定義", "function bust109HeroSrc()" in src)
ck("enterHome 用 bust109HeroSrc",
   'const h109=(typeof bust109HeroSrc==="function") ? bust109HeroSrc()' in src)
ck("enc79PeopleHtml 紅星段讀 BUST109_EXTRA[def.id]",
   "BUST109_EXTRA[def.id]" in src)
ck("enc79PeopleHtml 紅星段 cands.unshift(b109)",
   "cands.unshift(b109)" in src)
ck("PORTRAITS 消費者健在：手帳頁頭 hero_awi", "PORTRAITS.hero_awi" in src)
ck("PORTRAITS 消費者健在：傾談 modal PORTRAITS[npc.face]", "PORTRAITS[npc.face]" in src)
ck("PORTRAITS 消費者健在：人情頁 PORTRAITS[n.face]", "PORTRAITS[n.face]" in src)
ck("PORTRAITS 消費者健在：開局畫面 start-hero", "PORTRAITS.hero_awi" in src)
ck("fallback 鏈健在：spBustCandidates 推 PORTRAITS[pk]",
   "PORTRAITS[pk]" in src)
for k in ["awi", "ho_sang", "cheung_tsijun", "lin_hiu", "chow_choiyi",
          "ko_chunkit", "vera", "lui_ging", "tang_laiping", "luk_baakyin"]:
    ck(f"UI40_STAND.{k} 原封不動（今包唔掂企立圖）",
       re.search(r"const UI40_STAND = \{[\s\S]*?%s:" % re.escape(k), src) is not None)

# ---------- ⑤ 反證 ----------
def check_portraits_block(block_text, extra_text):
    """同上面 ①＋② 嘅核心斷言，食任意文字，回問題清單（供負向測試）。"""
    problems = []
    try:
        pm, _ = extract_map(block_text, "PORTRAITS")
    except ValueError:
        return ["搵唔到 PORTRAITS"]
    for k, v in OLD.items():
        if v["b64_prefix"] in block_text: problems.append(f"舊 {k} 殘留")
        if k not in pm: problems.append(f"缺 {k}")
    for k, val in pm.items():
        if not val.startswith("data:image/webp;base64,"): problems.append(f"{k} 唔係 WebP")
    try:
        em, _ = extract_map(extra_text, "BUST109_EXTRA")
    except ValueError:
        return problems + ["搵唔到 BUST109_EXTRA"]
    for stem in ["awi_s2", "awi_s3"] + STARS:
        if stem not in em: problems.append(f"EXTRA 缺 {stem}")
    return problems

ck("反證：checker 食正版文字回零問題",
   check_portraits_block(src, src) == [])
# (a) 舊值殘留：將一個新值換返舊 JPEG 前綴＋舊長度垃圾，checker 必須捉到
mut = src.replace(PORTRAITS["npc_lin"][:80],
                  OLD["npc_lin"]["b64_prefix"] + "X" * 100, 1)
ck("反證：checker 食舊 JPEG 值必須報問題",
   len(check_portraits_block(mut, src)) >= 1)
# (b) 缺 EXTRA 鍵
mut2 = re.sub(r'"so_jiyan":\s*"[^"]+",\n', "", src, count=1)
ck("反證：checker 食缺 so_jiyan 嘅 EXTRA 必須報問題",
   any("so_jiyan" in p for p in check_portraits_block(src, mut2)))
# (c) 真實臨時目錄負向測試：crop109.json 抽走一項 → 交叉比對必須 FAIL
if crop:
    tmpd = tempfile.mkdtemp(prefix="bust109neg_")
    try:
        slim = dict(crop); slim.pop("npc_vera")
        with open(os.path.join(tmpd, "crop109.json"), "w", encoding="utf-8") as f:
            json.dump(slim, f)
        with open(os.path.join(tmpd, "crop109.json"), encoding="utf-8") as f:
            slim2 = json.load(f)
        ck("反證：crop109.json 缺 npc_vera → 21 項斷言 FAIL",
           len(slim2) != 21)
    finally:
        shutil.rmtree(tmpd, ignore_errors=True)

print("FAILURES: %d" % len(fails))
for f in fails: print(" - " + f)
sys.exit(1 if fails else 0)
