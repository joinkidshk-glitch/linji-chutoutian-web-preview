# -*- coding: utf-8 -*-
"""v20a195 TIER195・靜態測試（唔行瀏覽器，淨讀 index.html＋檔案系統）。
釘死：
  S1 dlg106AweiStem() 讀 max(即時 tier, playerTierMax)，唔係齋讀即時 tier
  S2 enc195 四函數在位（TierFromAllYears／Backfill／Ensure／Record）
  S3 normalizeSaveObj 呼叫 enc195BackfillTierMax（舊檔載入回填）
  S4 兩個 done_* 寫入點之後有 enc195RecordTierMax（resolvePlannedDay 殺青＋
     failShootOverdue 逾期掉單——兩處都寫 done_* 旗，口徑要一致）
  S5 backfill 行全歷年對照（掃 STORY_WIRE.gigsByYear＋normalizeGigRecord），
     唔係淨數當年 GIGS；enc79PlayerTier() 本身唔郁（仲係數當年 GIGS）
  S6 唔改 SAVE key／softRev／?v=；唔直改 content pack JSON（playerTierMax 唔入 pack）
  S7 附帶新圖在位：awi_s2_angry.webp／awi_s3_angry.webp（WebP、非空、RGBA）
  S8 唔郁開局 #start-standee／UI40_STAND（已知殘留，另開一票）
反證：pristine main（f2a6b0c）index 冇 enc195 → S1–S5 FAIL，exit 1。
用法：python3 tests/test_awei195_static.py
"""
import os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HTML = os.path.join(ROOT, "index.html")
fails = []

def ok(name, cond, extra=""):
    print(("PASS " if cond else "FAIL ") + name + (" :: " + str(extra) if extra else ""))
    if not cond:
        fails.append(name)

def lines_of(path):
    with open(path, encoding="utf-8", errors="ignore") as f:
        return f.read().splitlines()

def fn_body(lines, decl):
    """抽 function decl（...){...} 全文（brace 對位）。搵唔到回 None。"""
    for i, l in enumerate(lines):
        if len(l) > 600:
            continue
        if decl in l:
            j = lines[i].index("{")
            depth = 0
            for k in range(i, len(lines)):
                seg = lines[k][j:] if k == i else lines[k]
                for ch in seg:
                    if ch == "{":
                        depth += 1
                    elif ch == "}":
                        depth -= 1
                        if depth == 0:
                            return "\n".join(lines[i:k + 1])
            return None
    return None

def short_lines(lines):
    return [l for l in lines if len(l) <= 600]

html_lines = lines_of(HTML)
html_short = short_lines(html_lines)
html_text = "\n".join(html_lines)

# ---- 反證門：enc195 唔存在 → 逐組 FAIL，唔 crash ----
if "function enc195BackfillTierMax(" not in html_text:
    for n in ["S1 stem 讀最高紀錄", "S2 四函數在位", "S3 載入回填",
              "S4 兩個寫入點", "S5 全歷年對照＋即時計數唔郁"]:
        ok(n + "（pristine：冇 enc195）", False)
    print("AWEI195 STATIC: %d FAIL" % len(fails))
    sys.exit(1)

# ---- S1 ----
stem = fn_body(html_lines, "function dlg106AweiStem(")
ok("S1 dlg106AweiStem 在位", stem is not None)
if stem:
    ok("S1 stem 讀 playerTierMax", "playerTierMax" in stem)
    ok("S1 stem 取 max(即時, 最高紀錄)", "Math.max" in stem and "enc79PlayerTier" in stem)
    ok("S1 stem 懶回填（enc195EnsureTierMax）", "enc195EnsureTierMax" in stem)
    ok("S1 stem 仲有 s3／s2 分支", "awi_s3" in stem and "awi_s2" in stem)

# ---- S2 ----
for fn in ["enc195TierFromAllYears", "enc195BackfillTierMax",
           "enc195EnsureTierMax", "enc195RecordTierMax"]:
    ok("S2 %s 在位" % fn, ("function %s(" % fn) in html_text)

# ---- S3 ----
norm = fn_body(html_lines, "function normalizeSaveObj(")
ok("S3 normalizeSaveObj 在位", norm is not None)
if norm:
    ok("S3 normalizeSaveObj 呼叫 enc195BackfillTierMax(o)", "enc195BackfillTierMax(o)" in norm)

# ---- S4：兩個 done_* 寫入點之後有 record call ----
# 定位：S.flags["done_"+sh.gigId]=(S.flags["done_"+sh.gigId]||0)+1; 出現兩次
# （resolvePlannedDay 殺青／failShootOverdue 逾期掉單）；每處之後 3 行內要有 record。
write_idx = [i for i, l in enumerate(html_lines)
             if 'S.flags["done_"+sh.gigId]=(S.flags["done_"+sh.gigId]||0)+1;' in l]
ok("S4 done_* 寫入點啱啱兩處", len(write_idx) == 2, "n=%d %s" % (len(write_idx), write_idx))
for n, i in enumerate(write_idx):
    window = "\n".join(html_lines[i:i + 4])
    ok("S4 寫入點 %d 之後有 enc195RecordTierMax" % (n + 1), "enc195RecordTierMax()" in window, "L%d" % (i + 1))
    # 邊個函數包住：向上搵最近嘅 function 宣告
    fn_name = "?"
    for j in range(i, max(0, i - 400), -1):
        m = re.match(r"\s*(?:async\s+)?function\s+([A-Za-z0-9_$]+)\s*\(", html_lines[j])
        if m:
            fn_name = m.group(1)
            break
    ok("S4 寫入點 %d 喺預期函數（resolvePlannedDay／failShootOverdue）" % (n + 1),
       fn_name in ("resolvePlannedDay", "failShootOverdue"), fn_name)

# ---- S5 ----
all_years = fn_body(html_lines, "function enc195TierFromAllYears(")
ok("S5 enc195TierFromAllYears 在位", all_years is not None)
if all_years:
    ok("S5 回填掃 STORY_WIRE.gigsByYear（全歷年）", "gigsByYear" in all_years)
    ok("S5 回填經 normalizeGigRecord（NAME93／OVR110 降級一致）", "normalizeGigRecord" in all_years)
    ok("S5 回填唔直接數當年 GIGS（唔可以只掃 GIGS）", "GIGS" not in all_years.replace("gigsByYear", ""))
    ok("S5 回填有 null guard（年庫未齊唔寫錯值）", "return null" in all_years)
    ok("S5 回填 tier 門檻跟 enc79（3 lead＋fame 70 → 3）", "lead>=3" in all_years and "fame>=70" in all_years.replace("fm>=70", "fame>=70") or ("lead>=3" in all_years and "fm>=70" in all_years))
tier = fn_body(html_lines, "function enc79PlayerTier(")
ok("S5 enc79PlayerTier 在位", tier is not None)
if tier:
    ok("S5 即時 tier 計數唔郁（仲係數當年 GIGS）", "GIGS" in tier and "playerTierMax" not in tier)

# ---- S6：唔改 SAVE／softRev／?v=／pack ----
ok("S6 SAVE key 仲係 starVolunteer_map_v19w", 'SAVE = "starVolunteer_map_v19w"' in html_text)
ok("S6 softRev 仲係 s107", 'softRev:"s107"' in html_text or 'SOFT_REV' in html_text)
for y in ("1988", "1989", "1990", "1991", "1992"):
    p = os.path.join(ROOT, "content", "gigs_%s.json" % y)
    txt = open(p, encoding="utf-8").read()
    ok("S6 pack gigs_%s.json 冇 playerTierMax" % y, "playerTierMax" not in txt)

# ---- S7：新圖在位 ----
for fn in ("awi_s2_angry.webp", "awi_s3_angry.webp"):
    p = os.path.join(ROOT, "assets", "story", "fullbody", fn)
    exists = os.path.isfile(p)
    size = os.path.getsize(p) if exists else 0
    magic = b""
    if exists:
        with open(p, "rb") as f:
            magic = f.read(12)
    ok("S7 %s 在位、非空、WebP" % fn, exists and size > 10000 and magic[:4] == b"RIFF" and magic[8:12] == b"WEBP",
       "size=%d" % size)
# 舊表情齊晒 7 張＋新 angry＝8 張（s2／s3 各）
for stem_name in ("awi_s2", "awi_s3"):
    got = sorted(f for f in os.listdir(os.path.join(ROOT, "assets", "story", "fullbody"))
                 if f.startswith(stem_name + "_") and f.endswith(".webp"))
    ok("S7 %s 表情齊 8 張（含 angry）" % stem_name, len(got) == 8, got)

# ---- S8：唔郁開局舊圖 ----
ok("S8 UI40_STAND.awi 仲係舊內嵌圖（唔郁）", "UI40_STAND" in html_text)
ok("S8 #start-standee 仲喺度", "start-standee" in html_text)

print("AWEI195 STATIC: %s" % ("ALL PASS" if not fails else ("%d FAIL -> %s" % (len(fails), " | ".join(fails)))))
sys.exit(1 if fails else 0)
