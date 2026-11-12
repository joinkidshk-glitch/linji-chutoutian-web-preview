# -*- coding: utf-8 -*-
"""v20a138 生死 verdict：reachable occurrence × runtime 分類 → 真需要嘅 (speaker, expr)。
生＝≥1 條 reachable 嘅線，真講者＝該角，runtime 分類＝該表情。
死＝其餘（並列出死因）。
輸出：qa138/verdict138.json ＋ 印表。
"""
import json, os, re
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(HERE, "..")
HTML = open(os.path.join(WORK, "index.html"), encoding="utf-8").read()

# GAZE keys（有全身圖先行表情候補鏈）
m = re.search(r"const DLG106_GAZE\s*=\s*\{", HTML)
seg = HTML[m.start():m.start() + 6000]
GAZE = set(re.findall(r'"?([a-z_0-9]+)"?\s*:\s*\{', seg))
SHADOW = {"shadow_male", "shadow_female", "shadow_elder", "generic_cinema_asst"}

FB = os.path.join(WORK, "assets", "story", "fullbody")
have = defaultdict(set)
for fn in os.listdir(FB):
    mm = re.match(r"^(.+)_(base|smile|serious|sad|surprise|shy|think|angry)\.webp$", fn)
    if mm:
        have[mm.group(1)].add(mm.group(2))

occ = json.load(open(os.path.join(HERE, "occ_index138.json"), encoding="utf-8"))
cls = json.load(open(os.path.join(HERE, "classify138.json"), encoding="utf-8"))
cls_map = {(r["text"], r["emotion"]): r for r in cls}

OVERRIDE = {"C6", "C7", "C8", "C9", "C10", "C11", "C12", "C13", "C14", "C15",
            "C16", "C17", "R_lan_meet", "R_lan_push1", "R_lan_push2",
            "R_lan_crisis", "R_lan_ending"}

def reachable(o):
    s = o["src"]
    if s == "LIVE":
        return (not o.get("in_resultBeats")), "LIVE-resultBeats" if o.get("in_resultBeats") else "LIVE"
    if s == "ENC":
        return True, "ENC"
    if s == "PACK":
        return (o["node"] not in OVERRIDE), ("PACK-overridden:" + str(o["node"])) if o["node"] in OVERRIDE else "PACK"
    if s == "CORE":
        return False, "CORE-talk-static-bust"
    if s == "TIER":
        return False, "TIER-talk-static-bust"
    if s == "CAST":
        return False, "CAST-never-loaded"
    if s == "GIFT":
        return False, "GIFT-text-only"
    return False, s

# live-needed: (speaker, expr) -> [evidence]
need = defaultdict(list)
dead_reasons = Counter()
for text, ocs in occ.items():
    for o in ocs:
        ok, why = reachable(o)
        if not ok:
            dead_reasons[(o["src"], why)] += 1
            continue
        c = cls_map.get((text, o.get("emotion")))
        if not c:
            continue
        expr = c["expr"]
        if expr == "base":
            continue
        sp = o["speaker"]
        if sp in SHADOW or sp.startswith("OTHER:") or sp == "extra_unknown":
            continue
        if sp not in GAZE:
            continue
        need[(sp, expr)].append({"text": text, "src": o["src"],
                                 "node": o.get("node"), "category": c["category"],
                                 "emotion_field": o.get("emotion")})

# batch = live-needed minus existing
batch = {}
for (sp, expr), ev in sorted(need.items()):
    if expr in have.get(sp, set()):
        continue
    if sp in ("awi", "awi_s2", "awi_s3"):
        continue  # 阿偉 s2/s3 angry 靠跨階段候補鏈，v127 已確立
    batch[f"{sp}_{expr}"] = {"speaker": sp, "expr": expr, "lines": len(ev), "evidence": ev}

print(f"live-needed (speaker,expr) total: {len(need)}")
print(f"already have: {sum(1 for (sp, e) in need if e in have.get(sp, set()))}")
print(f"BATCH (live + missing): {len(batch)} files")
for k, v in sorted(batch.items()):
    print(f"  {k}: {v['lines']} lines  e.g. {v['evidence'][0]['text'][:36]}… [{v['evidence'][0]['src']}]")

json.dump({"live_needed": {f"{sp}:{e}": len(ev) for (sp, e), ev in sorted(need.items())},
           "batch": batch},
          open(os.path.join(HERE, "verdict138.json"), "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)

# inventory 口徑增益：batch 每張覆蓋幾多條 inventory-missing 句
miss = json.load(open(os.path.join(HERE, "missing_detail138.json"), encoding="utf-8"))
CAT2EXPR = {"happy": "smile", "neutral": "base", "serious": "serious",
            "sad": "sad", "surprise": "surprise", "shy": "shy",
            "think": "think", "angry": "angry"}
gain = Counter()
for d in miss:
    k = f"{d['char']}_{CAT2EXPR[d['category']]}"
    if k in batch:
        gain[k] += 1
print(f"\ninventory-metric gain: +{sum(gain.values())} lines -> "
      f"515+{sum(gain.values())}/593")
for k, v in sorted(gain.items()):
    print(f"  {k}: +{v}")

# 死檔：inventory-missing 資產入面，唔入 batch 嘅
print("\nDEAD inventory-missing assets (not in batch):")
for d in miss:
    k = f"{d['char']}_{CAT2EXPR[d['category']]}"
    if k not in batch:
        pass
dead_assets = Counter()
for d in miss:
    k = f"{d['char']}_{CAT2EXPR[d['category']]}"
    if k not in batch:
        dead_assets[k] += 1
for k, v in sorted(dead_assets.items()):
    print(f"  {k}: {v} lines")
print("\ndead occurrence reasons (all sources):")
for (s, w), n in sorted(dead_reasons.items()):
    print(f"  {s} {w}: {n}")
