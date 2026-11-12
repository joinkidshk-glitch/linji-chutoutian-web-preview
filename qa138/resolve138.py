# -*- coding: utf-8 -*-
"""v20a138 生死檔分類：先分生死，再排單。
口徑：
- 覆蓋率沿用 v106/v107（lines_classified.json × assets/story/fullbody/ 檔名）。
- 生死判定用「真實運行時」：真講者（spResolveSpeakerId 規則）＋真分類
  （dlg106ResolveCategory：beat emotion 欄 → 嵌入 map → 關鍵詞分類器，經 node 實跑），
  加來源可達性：
    LIVE beats（非 resultBeats）→ 生；ENC 巧遇 → 生；
    pack 節點未被 spine 覆寫（C6–C17 主幹＋R_lan_* 覆寫集之外）→ 生；
    NPC_LINES_CORE／NPC_TIER_LINES（傾談 modal 靜態 bust，唔行 dlg106 loader）→ 死；
    cast_main.json（index.html 出現 0 次，從未載入）→ 死；
    gift_react（reactionLine 只出純文字 <p>，冇圖）→ 死；
    resultBeats（applyChoice 只讀 effects）→ 死；
    括號舞台指示句：照計（v127 實駕見藍若曦 think 播到）。
用法：python3 qa138/resolve138.py
輸出：qa138/resolve138.json ＋ qa138/missing138.json ＋ 印出生死表。
分類器部分由 qa138/classify138.js（node，抽 index.html 真函數）另跑，
本檔先出 occurrences 檔 qa138/occ_for_classify.json。
"""
import json, os, re, sys
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(HERE, "..")
HTML = open(os.path.join(WORK, "index.html"), encoding="utf-8").read()
LINES = "/home/hatch/workspace/linji-expression-inventory/work/lines_classified.json"
FB = os.path.join(WORK, "assets", "story", "fullbody")
CAT2EXPR = {"happy": "smile", "neutral": "base", "serious": "serious",
            "sad": "sad", "surprise": "surprise", "shy": "shy",
            "think": "think", "angry": "angry"}
ROLE2ID = {"agent": "ho_sang", "stylist": "vera", "colleague": "lin_hiu",
           "director": "cheung_tsijun", "rival": "ko_chunkit", "reporter": "chow_choiyi"}
NAME2ID = {
    "陳偉翔": "awi", "阿偉": "awi", "何生": "ho_sang", "Vera": "vera",
    "林曉晴": "lin_hiu", "周采兒": "chow_choiyi", "高俊傑": "ko_chunkit",
    "張子駿": "cheung_tsijun", "高文瀚": "gao_wenhan", "藍若曦": "lan_ruoxi",
    "張克凡": "cheung_hakfan", "雷勁": "lui_ging", "關海媚": "kwan_hoimei",
    "鄭威廉": "cheng_william", "唐素雲": "tong_souwan", "方小龍": "fong_siulung",
    "徐寶珊": "tsui_poushan", "莫少輝": "mok_siufai", "金九": "uncle_kim",
    "鄧麗萍": "tang_laiping", "陸柏言": "luk_baakyin", "蘇芷茵": "so_jiyan",
    "麥震東": "mak_zhendong", "廖炳星": "liu_bingxing", "鍾楚凝": "chung_choning",
    "駱家聲": "lok_gasing", "齊鎮海": "chai_zanhoi", "魏詠男": "ngai_wingnaam",
    "顧明輝": "gu_mingfai", "葉敏芝": "yip_manji", "程天諾": "ching_tinlok",
    "彭少祺": "pang_siuki",
}
LEGACY = {}  # display name -> speaker id (SP_SPEAKER_LEGACY，StoryPlay spResolveSpeakerId 用)
_m = re.search(r"const SP_SPEAKER_LEGACY\s*=\s*\{(.*?)\n  \};", HTML, re.S)
for km in re.finditer(r'"([^"]+)":"([a-z_0-9]+)"', _m.group(1)):
    LEGACY[km.group(1)] = km.group(2)

# ---------- 1) 覆蓋重計（v127 口徑） ----------
lines = json.load(open(LINES, encoding="utf-8"))
assets = defaultdict(set)
for fn in os.listdir(FB):
    m = re.match(r"^(.+)_(base|smile|serious|sad|surprise|shy|think|angry)\.webp$", fn)
    if m:
        assets[m.group(1)].add(m.group(2))
roster = sorted(s for s in assets if not s.startswith("boss_"))
nonneutral = [x for x in lines if x["category"] != "neutral" and x["char"] in roster]
covered = [x for x in nonneutral if CAT2EXPR[x["category"]] in assets[x["char"]]]
print(f"coverage: {len(covered)}/{len(nonneutral)} = {len(covered)/len(nonneutral):.1%}")
assert (len(covered), len(nonneutral)) == (515, 593), "baseline coverage drifted!"
missing = [x for x in nonneutral if CAT2EXPR[x["category"]] not in assets[x["char"]]]
print(f"missing lines: {len(missing)}")
miss_assets = Counter()
for x in missing:
    miss_assets[(x["char"], CAT2EXPR[x["category"]])] += 1
json.dump({"global": [len(covered), len(nonneutral)],
           "missing_lines": missing,
           "missing_assets": {f"{k[0]}:{k[1]}": v for k, v in sorted(miss_assets.items())}},
          open(os.path.join(HERE, "missing138.json"), "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)

# ---------- 2) 來源索引 ----------
def extract_const_block(name):
    m = re.search(r"const\s+" + re.escape(name) + r"\s*=\s*", HTML)
    if not m:
        return None
    i = m.end()
    start = i
    depth = 0
    instr = None
    while i < len(HTML):
        c = HTML[i]
        if instr:
            if c == "\\":
                i += 2
                continue
            if c == instr:
                instr = None
        elif c in "\"'":
            instr = c
        elif c in "{[":
            depth += 1
        elif c in "}]":
            depth -= 1
            if depth == 0:
                return HTML[start:i + 1]
        i += 1
    return None

def top_level_keys(obj_src):
    """回傳 JS 物件字面量第一層嘅 key（depth-aware）。"""
    keys = []
    depth = 0
    instr = None
    i = 0
    n = len(obj_src)
    while i < n:
        c = obj_src[i]
        if instr:
            if c == "\\":
                i += 2
                continue
            if c == instr:
                instr = None
        elif c in "\"'":
            instr = c
        elif c in "{[":
            depth += 1
        elif c in "}]":
            depth -= 1
        elif c == ":" and depth == 1:
            # look back for key token
            j = i - 1
            while j >= 0 and obj_src[j] in " \t\r\n":
                j -= 1
            if j >= 0 and obj_src[j] in "\"'":
                q = obj_src[j]
                k = j - 1
                while k >= 0 and obj_src[k] != q:
                    k -= 1
                keys.append(obj_src[k + 1:j])
            else:
                k = j
                while k >= 0 and (obj_src[k].isalnum() or obj_src[k] == "_"):
                    k -= 1
                keys.append(obj_src[k + 1:j + 1])
        i += 1
    return keys

OVERRIDE = set()
for const_name in ["STORY_SPINE_NODES_1989", "STORY_SPINE_NODES_1990",
                   "STORY_SPINE_NODES_C6", "ROMANCE_LAN_PA_OVERRIDES"]:
    blk = extract_const_block(const_name)
    ks = top_level_keys(blk)
    OVERRIDE |= set(ks)
    print(f"override {const_name}: {sorted(ks)}")
OVERRIDE.add("C17")
print("OVERRIDE set:", sorted(OVERRIDE))

# text -> list of occurrence dicts
occ = defaultdict(list)

def add_occ(text, d):
    text = (text or "").strip()
    if text:
        occ[text].append(d)

# 2a) NPC_LINES_CORE
blk = extract_const_block("NPC_LINES_CORE")
core = json.loads(blk)
for role, pack in core.items():
    if role not in ROLE2ID:
        continue
    for k, arr in pack.items():
        if isinstance(arr, list):
            for v in arr:
                add_occ(v, {"src": "CORE", "role": role, "speaker": ROLE2ID[role]})

# 2b) NPC_TIER_LINES（逐 role balanced-brace 解析，唔好成段攞到尾）
blk = extract_const_block("NPC_TIER_LINES")
for role in ROLE2ID:
    km = re.search(r"(?<![A-Za-z0-9_])" + re.escape(role) + r"\s*:\s*\{", blk)
    if not km:
        continue
    # balanced brace from the opening {
    start = km.end() - 1
    depth = 0
    instr = None
    i = start
    seg = None
    while i < len(blk):
        c = blk[i]
        if instr:
            if c == "\\":
                i += 2
                continue
            if c == instr:
                instr = None
        elif c in "\"'":
            instr = c
        elif c == "{":
            depth += 1
        elif c == "}":
            depth -= 1
            if depth == 0:
                seg = blk[start:i + 1]
                break
        i += 1
    if seg is None:
        print(f"WARN: TIER role {role} block not closed")
        continue
    for txt in re.findall(r'"((?:[^"\\]|\\.){8,})"', seg):
        t = re.sub(r"\\u([0-9a-fA-F]{4})", lambda m: chr(int(m.group(1), 16)), txt)
        t = t.replace('\\"', '"').replace("\\\\", "\\").replace("\\n", "\n").replace("\\t", "\t")
        add_occ(t, {"src": "TIER", "role": role, "speaker": ROLE2ID[role]})

# 2c) cast_main.json
cm = json.load(open(os.path.join(WORK, "content", "cast_main.json"), encoding="utf-8"))
for npc in cm["npcs"]:
    for k, arr in (npc.get("lines") or {}).items():
        if isinstance(arr, list):
            for v in arr:
                add_occ(v, {"src": "CAST", "npc": npc["id"], "speaker": npc["id"]})

# 2d) pack files（連 node id；beats＋choices.beats；唔包 resultBeats）
PACK_FILES = ["story_detail_c1_to_c17.json", "story_detail_rival_mentor.json",
              "story_detail_romance_lan_xu.json", "story_detail_romance_tang.json",
              "story_detail_romance_vera_hiu_choi.json"]
pack_nodes = {}
for f in PACK_FILES:
    d = json.load(open(os.path.join(WORK, "content", f), encoding="utf-8"))
    for node in d.get("nodes", []):
        nid = node.get("id")
        pack_nodes.setdefault(nid, f)

        def walk_beats(node_, in_choice=False):
            for b in node_.get("beats", []) or []:
                name = b.get("speaker", "")
                if b.get("kind") == "system" or name in ("系統", "旁白", ""):
                    continue
                sid = b.get("speakerId") or NAME2ID.get(name) or LEGACY.get(name) or ("OTHER:" + name)
                for v in b.get("lines", []) or []:
                    add_occ(v, {"src": "PACK", "file": f, "node": nid,
                                "speaker": sid, "emotion": b.get("emotion"),
                                "in_choice": in_choice})
            for ch in (node_.get("choices") or []):
                for b in ch.get("beats", []) or []:
                    name = b.get("speaker", "")
                    if b.get("kind") == "system" or name in ("系統", "旁白", ""):
                        continue
                    sid = b.get("speakerId") or NAME2ID.get(name) or LEGACY.get(name) or ("OTHER:" + name)
                    for v in b.get("lines", []) or []:
                        add_occ(v, {"src": "PACK", "file": f, "node": nid,
                                    "speaker": sid, "emotion": b.get("emotion"),
                                    "in_choice": True})
        walk_beats(node)
print("pack nodes:", len(pack_nodes), "overridden pack nodes:",
      sorted(n for n in pack_nodes if n in OVERRIDE))

# 2e) LIVE beats（regex，同 inventory 抽法；另記 emotion 欄＋係咪 resultBeats 入面）
def parse_js_string(s, i):
    """s[i] is opening quote. Return (value, next_index) — inventory 同款轉義處理
    （\\n→換行、\\t、\\r、其他 \\X→X；唔用 unicode_escape，會整爛中文）。"""
    q = s[i]
    assert q in "\"'"
    i += 1
    out = []
    while i < len(s):
        c = s[i]
        if c == "\\":
            n = s[i + 1] if i + 1 < len(s) else ""
            out.append({"n": "\n", "t": "\t", "r": "\r"}.get(n, n))
            i += 2
            continue
        if c == q:
            return "".join(out), i + 1
        out.append(c)
        i += 1
    return "".join(out), i

def parse_lines_array(s, i):
    assert s[i] == "["
    i += 1
    vals = []
    while i < len(s):
        c = s[i]
        if c in "\"'":
            v, i = parse_js_string(s, i)
            vals.append(v)
        elif c == "]":
            return vals, i + 1
        else:
            i += 1
    return vals, i

beat_re = re.compile(r"speaker:\s*\"([^\"]*)\"")
n_live = 0
n_live_text = 0
for m in beat_re.finditer(HTML):
    seg = HTML[m.start():m.start() + 1200]
    lm = re.search(r"lines:\s*\[", seg)
    tm = re.search(r"text:\s*\"", seg)
    use_lines = lm and (not tm or lm.start() < tm.start())
    use_text = tm and (not lm or tm.start() < lm.start())
    if not use_lines and not use_text:
        continue
    # 同 beat 守則：speaker: 同 lines:/text: 之間唔可以有另一個 speaker: 或 }，
    # 否則個 lines:/text: 屬於下一個 beat（舊版 4500 字窗誤歸，例：wf4FenFarewellNode
    # 13 個 text:-beat 誤將 A_ko_meet 旁白句歸畀芬姐／阿偉）。
    head = seg[: (lm.start() if use_lines else tm.start())]
    head_rest = head[len(m.group(0)):]
    if "speaker:" in head_rest or "}" in head_rest:
        continue
    sid_m = re.search(r"speakerId:\s*\"([^\"]+)\"", head)
    emo_m = re.search(r"emotion:\s*\"([^\"]+)\"", head)
    kind_m = re.search(r"kind:\s*\"([^\"]+)\"", head)
    kind = kind_m.group(1) if kind_m else ""
    name = m.group(1)
    if kind == "system" or name in ("系統", "旁白", ""):
        continue
    # resultBeats 判定：最近嘅 resultBeats: 係咪近過最近嘅 beats:
    back = HTML[max(0, m.start() - 3000):m.start()]
    rb = back.rfind("resultBeats")
    bb = back.rfind("beats:")
    in_result = rb > bb
    if sid_m:
        sid = sid_m.group(1)
        if sid == "agent":
            sid = "ho_sang"
        elif sid == "player":
            sid = "awi"
    else:
        sid = NAME2ID.get(name) or LEGACY.get(name) or ("OTHER:" + name)
    emo = emo_m.group(1) if emo_m else None
    if use_lines:
        arr_start = m.start() + lm.end() - 1
        vals, _ = parse_lines_array(HTML, arr_start)
        if not vals:
            continue
        n_live += 1
        for v in vals:
            add_occ(v, {"src": "LIVE", "speaker": sid, "emotion": emo,
                        "in_resultBeats": in_result, "beat_speaker": name})
    else:
        txt, _ = parse_js_string(HTML, m.start() + tm.end() - 1)
        if not txt:
            continue
        n_live_text += 1
        add_occ(txt, {"src": "LIVE", "speaker": sid, "emotion": emo,
                      "in_resultBeats": in_result, "beat_speaker": name})
print(f"LIVE beats parsed: {n_live} (lines) + {n_live_text} (text)")


# 2f) ENC 巧遇
pair_re = re.compile(r"\[\s*\"([SAN])\"\s*,\s*\"")
for name in re.findall(r"const (ENC\d+_(?:DLG|FRAME)_[a-z_]+)", HTML):
    star = re.match(r"ENC\d+_(?:DLG|FRAME)_(.+)$", name).group(1)
    star = {"yip_manzi": "yip_manji"}.get(star, star)
    if star not in set(NAME2ID.values()):
        continue
    block = extract_const_block(name)
    if not block:
        continue
    for pm in pair_re.finditer(block):
        v, _ = parse_js_string(block, pm.end() - 1)
        if pm.group(1) == "S":
            add_occ(v, {"src": "ENC", "speaker": star})
        elif pm.group(1) == "A":
            add_occ(v, {"src": "ENC", "speaker": "awi"})
for const_name, _ in [("ENC79_STAGEUP", None), ("ENC79_CAP_LINES", None), ("ENC79_WRAP_ECHO", None)]:
    block = extract_const_block(const_name)
    if not block:
        continue
    for sid in ["luk_baakyin", "liu_bingxing", "mak_zhendong", "yip_manji"]:
        km = re.search(re.escape(sid) + r":", block)
        if not km:
            continue
        seg = block[km.start():]
        nxt = re.search(r",\n  \w+:", seg)
        if nxt:
            seg = seg[:nxt.start()]
        for pm in pair_re.finditer(seg):
            v, _ = parse_js_string(seg, pm.end() - 1)
            if pm.group(1) == "S":
                add_occ(v, {"src": "ENC", "speaker": sid})
            elif pm.group(1) == "A":
                add_occ(v, {"src": "ENC", "speaker": "awi"})

# 2g) GIFT
gr = json.load(open(os.path.join(WORK, "content", "gift_react_copy.json"), encoding="utf-8"))
for e in gr.get("entries", []):
    nk = e.get("npcKey", "")
    cid = ROLE2ID.get(nk) or (nk if nk in set(NAME2ID.values()) else None)
    if not cid:
        continue
    for v in e.get("lines", []):
        t = re.sub(r"^[^：]*：", "", v).strip("「」")
        add_occ(t, {"src": "GIFT", "speaker": cid})

print(f"occurrence index: {len(occ)} distinct texts")

# ---------- 3) 每條 missing line 嘅 occurrences ＋ 分類器輸入 ----------
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

occ_for_classify = []
seen_cls = set()
detail = []
for x in missing:
    t = x["text"]
    ocs = occ.get(t, [])
    recs = []
    for o in ocs:
        ok, why = reachable(o)
        recs.append({**o, "reachable": ok, "reach_why": why})
        key = (t, o.get("emotion"))
        if key not in seen_cls:
            seen_cls.add(key)
            occ_for_classify.append({"text": t, "emotion": o.get("emotion")})
    detail.append({"char": x["char"], "category": x["category"],
                   "expr": CAT2EXPR[x["category"]], "source_bucket": x["source"],
                   "text": t, "occurrences": recs})
json.dump(detail, open(os.path.join(HERE, "missing_detail138.json"), "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)
json.dump(occ_for_classify, open(os.path.join(HERE, "occ_for_classify.json"), "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)
print(f"missing lines with occurrences: {sum(1 for d in detail if d['occurrences'])}/{len(detail)}")
print(f"missing lines with NO occurrence in index: {sum(1 for d in detail if not d['occurrences'])}")
for d in detail:
    if not d["occurrences"]:
        print("  NO-OCC:", d["char"], d["category"], d["source_bucket"], d["text"][:50])
print(f"classifier inputs (missing only): {len(occ_for_classify)} distinct (text, emotion)")

# ---------- 4) 全量分類器輸入：所有 occurrence 嘅 (text, emotion) ----------
# 用途：真實運行時需要嘅 (speaker, expr) 全集＝reachable occurrence × runtime 分類。
# 咁先捉到 inventory 口徑漏咗嘅（例如 beat emotion 欄指定 surprise，但 inventory
# 關鍵詞分類話 neutral；又如 yip_manji_serious／lin_hiu_surprise 呢啲 v119 404 檔）。
all_pairs = set()
for t, ocs in occ.items():
    for o in ocs:
        all_pairs.add((t, o.get("emotion")))
all_in = [{"text": t, "emotion": e} for (t, e) in sorted(all_pairs)]
json.dump(all_in, open(os.path.join(HERE, "occ_all_for_classify.json"), "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)
# 另存完整 occurrence index（供 verdict 用）
json.dump({t: ocs for t, ocs in occ.items()},
          open(os.path.join(HERE, "occ_index138.json"), "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)
print(f"classifier inputs (all): {len(all_in)} distinct (text, emotion)")
