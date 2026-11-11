# v20a109 B: apply bust replacement to index.html. All replacements assert count==1.
import base64, hashlib, json, re, sys

IDX = "index.html"
src = open(IDX, encoding="utf-8").read()
orig = src

def b64(stem):
    return base64.b64encode(open(f"qa109b/busts/{stem}.webp", "rb").read()).decode()

def replace_once(old, new, label):
    global src
    n = src.count(old)
    assert n == 1, f"{label}: count={n}"
    src = src.replace(old, new)

# ---------- 0. record old PORTRAITS values (for tests + NOTES) ----------
lines = src.split("\n")
old = {}
for i in range(5234, 5241):  # lines 5235..5241 (0-based)
    ln = lines[i]
    key = ln.strip().split('"')[1]
    val = ln.split('"')[3]
    old[key] = {"line": i + 1, "line_len": len(ln),
                "sha256_line": hashlib.sha256(ln.encode()).hexdigest(),
                "b64_len": len(val), "b64_prefix": val[:60],
                "mime": val.split(";")[0]}
    assert old[key]["mime"] == "data:image/jpeg", key
json.dump(old, open("qa109b/old_portraits.json", "w"), indent=1, ensure_ascii=False)
print("old PORTRAITS total b64:", sum(v["b64_len"] for v in old.values()))

# ---------- 1. PORTRAITS values -> new WebP crops (same 7 keys, same order) ----------
PORTRAITS_MAP = {"hero_awi": "awi", "npc_cheung": "cheung_tsijun", "npc_chow": "chow_choiyi",
                 "npc_ho": "ho_sang", "npc_ko": "ko_chunkit", "npc_lin": "lin_hiu",
                 "npc_vera": "vera"}
for i in range(5234, 5241):
    ln = lines[i]
    key = ln.strip().split('"')[1]
    stem = PORTRAITS_MAP[key]
    suffix = "," if ln.rstrip().endswith(",") else ""
    newln = f'  "{key}": "data:image/webp;base64,{b64(stem)}"{suffix}'
    replace_once(ln, newln, f"PORTRAITS {key}")
print("PORTRAITS replaced: 7 lines")

# ---------- 2. BUST109_EXTRA map after PORTRAITS block ----------
EXTRA_ORDER = ["awi_s2", "awi_s3",
    "luk_baakyin", "liu_bingxing", "ngai_wingnaam", "yip_manji", "mak_zhendong",
    "lok_gasing", "pang_siuki", "chung_choning", "gu_mingfai", "so_jiyan",
    "chai_zanhoi", "ching_tinlok"]
extra_lines = []
for j, stem in enumerate(EXTRA_ORDER):
    comma = "," if j < len(EXTRA_ORDER) - 1 else ""
    extra_lines.append(f'  "{stem}": "data:image/webp;base64,{b64(stem)}"{comma}')
extra_block = """/* v20a109 BUST109：新版頭肩縮圖（由 v106/v107 全身基本款裁出，唔係重新生成）。
   來源：assets/story/fullbody/{stem}_base.webp → qa109b/crop109.py（Hc＝0.30×全身高、
   闊＝Hc×10/13、頭頂對齊、頭帶中心 x、米白底 #F2EBD8、240×312 WebP q80）。
   點解繼續內嵌 base64 而唔行資產路徑：見 NOTES_V20A109_BUST.md §3——
   (1) spBustCandidates／spBustUrl 視 data: URI 為「必定存在、優先回傳」，
   資產路徑會跌落一串可能 404 嘅舊 bust 檔案後面；(2) 人情頁／傾談 modal／
   頁頭係最高頻畫面，零 fetch 零 404 面；(3) 21 張總共 280,192 字元，只係
   比舊 7 張多 44,499（舊 hero 一張已經 98,871）。
   PORTRAITS 7 鍵＝阿偉 s1＋6 位 NPCS 熟人（沿用舊 key，全部消費者零改動即換新圖）；
   BUST109_EXTRA 14 鍵＝PORTRAITS 覆蓋唔到嘅：阿偉 s2/s3（頁頭跟級數）＋12 紅星
   （人情頁紅星段首選，舊 era_stars 企立圖退做 onerror 後備）。 */
const BUST109_EXTRA = {
""" + "\n".join(extra_lines) + "\n};\n"
anchor = "};\n/* v20a97 MAP97"
replace_once(anchor, "};\n" + extra_block + "/* v20a97 MAP97", "BUST109_EXTRA insert")

# ---------- 3. bust109HeroSrc() after dlg106AweiStem (inside DLG106 module) ----------
hero_fn = """function bust109HeroSrc(){
  /* v20a109 BUST109：頁頭阿偉像跟成長級數（同 dlg106AweiStem 一條規則：tier 2→s2、3→s3，
     其餘／判定唔到→s1＝PORTRAITS.hero_awi）。BUST109_EXTRA／PORTRAITS 缺失嗰陣退返
     另一邊，兩邊都冇先回 ""，唔出破圖。 */
  try{
    const stem = (typeof dlg106AweiStem==="function") ? dlg106AweiStem() : "awi";
    if(stem!=="awi" && typeof BUST109_EXTRA!=="undefined" && BUST109_EXTRA && BUST109_EXTRA[stem]) return BUST109_EXTRA[stem];
  }catch(_e){}
  try{ if(typeof PORTRAITS!=="undefined" && PORTRAITS && PORTRAITS.hero_awi) return PORTRAITS.hero_awi; }catch(_e){}
  return "";
}
"""
anchor3 = """  return "awi";
}
function dlg106StemFor(speakerId){"""
replace_once(anchor3, """  return "awi";
}
""" + hero_fn + """function dlg106StemFor(speakerId){""", "bust109HeroSrc insert")

# ---------- 4. enterHome: tier-aware hero ----------
old_home = """  const img=document.getElementById("home-awi");
  if(PORTRAITS.hero_awi) img.src=PORTRAITS.hero_awi;"""
new_home = """  const img=document.getElementById("home-awi");
  if(img){ const h109=(typeof bust109HeroSrc==="function") ? bust109HeroSrc() : ((typeof PORTRAITS!=="undefined" && PORTRAITS) ? PORTRAITS.hero_awi : ""); if(h109) img.src=h109; }"""
replace_once(old_home, new_home, "enterHome hero")

# ---------- 5. enc79PeopleHtml: red-star met rows prefer BUST109_EXTRA ----------
old_cands = """      const cands = enc79StandCandidates(def.id);
      const img = cands.length ?"""
new_cands = """      const cands = enc79StandCandidates(def.id);
      /* v20a109 BUST109：已見紅星縮圖改用新版全身基本款裁出嘅頭肩圖（BUST109_EXTRA），
         舊 era_stars 企立圖退做後備（cands[1]，onerror 嗰陣接住）；未見過嗰啲維持
         剪影（上面分支），唔揭面。 */
      try{ const b109=(typeof BUST109_EXTRA!=="undefined" && BUST109_EXTRA) ? BUST109_EXTRA[def.id] : ""; if(b109) cands.unshift(b109); }catch(_e){}
      const img = cands.length ?"""
replace_once(old_cands, new_cands, "enc79PeopleHtml unshift")

# ---------- guards: nothing else touched ----------
assert "starVolunteer_map_v19w" in src, "SAVE key lost"
assert src.count("BUST109_EXTRA") >= 5
assert src.count("bust109HeroSrc") == 3, src.count("bust109HeroSrc")  # def + enterHome + comment? count below
open(IDX, "w", encoding="utf-8").write(src)
print("written. bytes:", len(orig), "->", len(src), "delta:", len(src) - len(orig))
print("new PORTRAITS total b64:", sum(len(b64(s)) for s in PORTRAITS_MAP.values()))
print("BUST109_EXTRA occurrences:", src.count("BUST109_EXTRA"))
print("bust109HeroSrc occurrences:", src.count("bust109HeroSrc"))
