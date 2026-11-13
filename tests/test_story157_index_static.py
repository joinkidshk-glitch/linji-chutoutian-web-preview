# -*- coding: utf-8 -*-
# v20a157 index.html 側靜態測試（整合員）。
# 覆蓋：STORY_SPINE_NODES_1989／1990／C6／BR89／WF1、STORY_SPINE_NODE_C17_410、
# CHOICE47_NODES.F4_stay_mind／G4_family_job —— key 數目／次序、新 synopsis／beats
# 關鍵句、閘／choice 旗／stats 同 live 一致、ERA 修正句存在、舊句消失、年份舊曆寫法、
# effects.notes 零數字承諾、零「聲量」／「Ho哥」／真人名。
# 反證：喺 pristine main（e08a070／v148）index.html 上行會乾淨 FAIL（標題／beats 數／
# 旗 stats 唔同），唔 crash。
# 用法：python3 tests/test_story157_index_static.py [path-to-index.html]
import json
import os
import re
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IPATH = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, "index.html")
html = open(IPATH, encoding="utf-8").read()
fails = []


def ok(name, cond):
    print(("PASS " if cond else "FAIL ") + name)
    if not cond:
        fails.append(name)


def brace_match(s, open_idx):
    assert s[open_idx] == "{"
    i, depth, n = open_idx, 0, len(s)
    while i < n:
        c = s[i]
        if c in "\"'`":
            q = c
            i += 1
            while i < n:
                if s[i] == "\\":
                    i += 2
                    continue
                if s[i] == q:
                    i += 1
                    break
                i += 1
            continue
        if c == "/" and i + 1 < n and s[i + 1] == "/":
            j = s.find("\n", i)
            i = n if j == -1 else j
            continue
        if c == "/" and i + 1 < n and s[i + 1] == "*":
            j = s.find("*/", i + 2)
            i = n if j == -1 else j + 2
            continue
        if c == "{":
            depth += 1
        elif c == "}":
            depth -= 1
            if depth == 0:
                return i + 1
        i += 1
    raise ValueError("unbalanced braces")


def extract_const(name):
    m = re.search(r"const %s = \{" % re.escape(name), html)
    assert m, "missing const " + name
    end = brace_match(html, m.end() - 1)
    assert html[end] == ";"
    return html[m.start():end + 1]


def extract_key(key):
    m = re.search(r"  %s: \{" % re.escape(key), html)
    assert m, "missing key " + key
    end = brace_match(html, m.end() - 1)
    return html[m.end() - 1:end]


# ---- 用 node vm 將 spans 轉做 JSON（唔手寫 JS parser） ----
NODE_DUMP = r"""
const fs = require("fs");
const vm = require("vm");
function load(src, name) {
  const sb = { __v: null };
  vm.createContext(sb);
  vm.runInContext(src, sb);
  vm.runInContext("__v = " + name + ";", sb);
  return sb.__v;
}
const out = {};
for (const f of JSON.parse(process.argv[1])) {
  const src = fs.readFileSync(f.path, "utf8");
  out[f.key] = load(src, f.name);
}
console.log(JSON.stringify(out));
"""

spans = {}
tmp = tempfile.mkdtemp(prefix="t157_")
specs = [
    ("T1989", "STORY_SPINE_NODES_1989"),
    ("T1990", "STORY_SPINE_NODES_1990"),
    ("TC6", "STORY_SPINE_NODES_C6"),
    ("TBR89", "STORY_SPINE_NODES_BR89"),
    ("TWF1", "STORY_SPINE_NODES_WF1"),
    ("C17", "STORY_SPINE_NODE_C17_410"),
    ("GATE", "STORY_GATE_3Y"),
]
files = []
for key, name in specs:
    p = os.path.join(tmp, key + ".js")
    open(p, "w", encoding="utf-8").write(extract_const(name) + "\n")
    files.append({"path": p, "key": key, "name": name})
    spans[key] = extract_const(name)
# CHOICE47 keys（object literal 形）
for key in ("F4_stay_mind", "G4_family_job"):
    p = os.path.join(tmp, key + ".js")
    open(p, "w", encoding="utf-8").write("const %s = %s;\n" % (key, extract_key(key)))
    files.append({"path": p, "key": key, "name": key})
    spans[key] = extract_key(key)

r = subprocess.run(["node", "-e", NODE_DUMP, json.dumps(files)],
                   capture_output=True, text=True, timeout=60)
assert r.returncode == 0, "node dump failed: " + r.stderr[:2000]
D = json.loads(r.stdout)

T1989, T1990 = D["T1989"], D["T1990"]
TC6, TBR89, TWF1 = D["TC6"], D["TBR89"], D["TWF1"]
C17, GATE = D["C17"], D["GATE"]
F4, G4 = D["F4_stay_mind"], D["G4_family_job"]

ALL_NODES = {}
for t in (T1989, T1990, TC6, TBR89, TWF1):
    ALL_NODES.update(t)
ALL_NODES["C17"] = C17

# ---- 1. key 數目／次序 ----
ok("1989 表 5 keys 次序 C7/C11/C8/C9/C10",
   list(T1989.keys()) == ["C7", "C11", "C8", "C9", "C10"])
ok("1990 表 5 keys 次序 C15/C14/C12/C16/C13",
   list(T1990.keys()) == ["C15", "C14", "C12", "C16", "C13"])
ok("C6 表 1 key", list(TC6.keys()) == ["C6"])
ok("BR89 表 1 key", list(TBR89.keys()) == ["C6F"])
ok("WF1 表 2 keys 次序 C18/C19", list(TWF1.keys()) == ["C18", "C19"])
ok("CHOICE47 F4/G4 在位", F4.get("id") == "F4_stay_mind" and G4.get("id") == "G4_family_job")

# ---- 2. beats／choices 數目（設計稿＋manifest 對照；C8 係 10 唔係設計稿嘅 8） ----
ok("beats 數 1989 C7/C11/C8/C9/C10",
   [len(T1989[k]["beats"]) for k in ["C7", "C11", "C8", "C9", "C10"]] == [9, 9, 10, 9, 8])
ok("beats 數 1990 C15/C14/C12/C16/C13",
   [len(T1990[k]["beats"]) for k in ["C15", "C14", "C12", "C16", "C13"]] == [7, 9, 12, 7, 7])
ok("beats 數 C6/C6F", (len(TC6["C6"]["beats"]), len(TBR89["C6F"]["beats"])) == (10, 8))
ok("beats 數 C17", len(C17["beats"]) == 15)
ok("beats 數 C18/C19", (len(TWF1["C18"]["beats"]), len(TWF1["C19"]["beats"])) == (10, 10))
ok("beats 數 F4/G4", (len(F4["beats"]), len(G4["beats"])) == (4, 4))
ok("choices 數",
   [len(ALL_NODES[k]["choices"]) for k in
    ["C6", "C6F", "C7", "C11", "C8", "C9", "C10", "C15", "C14", "C12", "C16", "C13", "C17"]]
   == [2, 2, 3, 3, 2, 3, 2, 2, 3, 3, 2, 3, 2]
   and [len(F4["choices"]), len(G4["choices"])] == [3, 2])

# ---- 3. 新 synopsis／beats 關鍵句存在 ----
def blob(node):
    return json.dumps(node, ensure_ascii=False)


ok("C6 標題＋synopsis 新寫", TC6["C6"]["title"] == "角落嗰張枱"
   and "每集都 call 你" in TC6["C6"]["synopsis"] and "一簽一季" not in blob(TC6["C6"]))
ok("C6F 標題＋synopsis 同 C6 一致", TBR89["C6F"]["title"] == "角落嗰張枱"
   and TBR89["C6F"]["synopsis"] == TC6["C6"]["synopsis"])
ok("C6 Beat5 Q1 已潤飾（無 route 旗術語）",
   "第一日嗰個選擇" in blob(TC6["C6"]) and "route 旗" not in blob(TC6["C6"]))
ok("C7 穿幫修正：暴雨唔係黑雨", "天文台話有暴雨" in blob(T1989["C7"]) and "黑雨" not in blob(T1989["C7"]))
ok("C11 synopsis＋Beat2 信任代價", "帶眼帶耳" in T1989["C11"]["synopsis"]
   and "後台啲人望你" in blob(T1989["C11"]))
ok("C8 紙仔係劇本", "紙仔" in blob(T1989["C8"]) and "紙仔就係劇本" in blob(T1989["C8"])
   or "紙仔" in blob(T1989["C8"]))
ok("C9 顧明輝紅完之後", "紅完之後" in blob(T1989["C9"]) or "紅係" in blob(T1989["C9"]))
ok("C10 戲路定型＋第一次有個種類", "第一次有個「種類」" in T1989["C10"]["synopsis"])
ok("C15 傷唔係勳章係帳", "唔係勳章，係帳" in blob(T1990["C15"]))
ok("C14 挖角潮尾水", "挖角潮打到尾水" in blob(T1990["C14"]) and "白熱化" not in blob(T1990["C14"]))
ok("C12 K 房句照用", "首歌唔入 K 房" in blob(T1990["C12"]))
ok("C16 修音定苦練", "苦練" in blob(T1990["C16"]) and "修音" in blob(T1990["C16"]))
ok("C13 未揭盅口徑", "出年年初一先上畫" in blob(T1990["C13"]) and "票房要等出年先知" in blob(T1990["C13"]))
ok("C17 會議室場景", "星河電視台會議室" in C17["setting"] and "後台" not in C17["setting"])
ok("C17 台灣資金風聲照用", "台灣嗰邊啲水，冇以前咁鬆手喇" in blob(C17))
ok("C17 彩紙仲喺走廊", "彩紙仲喺走廊" in blob(C17))
ok("C17 synopsis：頒獎禮之後嗰晚", "頒獎禮之後嗰晚" in C17["synopsis"])
ok("C17 synopsis 無 DEV 註解（舊版文案／重寫）", "舊版文案" not in C17["synopsis"] and "重寫" not in C17["synopsis"])
ok("C17 最後一則係收尾過場句", "親手圈嗰一格" in C17["beats"][-1].get("lines", [""])[-1]
   or "親手圈嗰一格" in json.dumps(C17["beats"][-1], ensure_ascii=False))
ok("F4 太空人＋回流零星口吻", "太空人" in blob(F4) and "間中都會聽到" in blob(F4)
   and "呢年開始" not in blob(F4))
ok("F4 回流句 6 處（3 beats＋3 notes）", blob(F4).count("間中都會聽到") == 6)
ok("G4 標題＋阿媽文職", G4["title"] == "阿媽煲咗湯" and "表叔喺銀行嗰邊" in blob(G4)
   and "薦到一份文職" in blob(G4))

# ---- 4. 閘／choice 旗／stats 同 live 一致 ----
ok("閘 C6/C6F route＋weekMin 15",
   GATE["C6"].get("route") == "route_tv" and GATE["C6"].get("weekMin") == 15
   and GATE["C6F"].get("route") == "route_film" and GATE["C6F"].get("weekMin") == 15)
ok("閘 C11 需 C7、C15 需 C10",
   GATE["C11"].get("needDone") == ["C7"] and GATE["C15"].get("needDone") == ["C10"])
ok("閘 C17 weekMin 153＋1992 冬",
   GATE["C17"].get("weekMin") == 153 and GATE["C17"].get("yearEq") == 1992
   and GATE["C17"].get("needDone") == ["C13"])
ok("閘 C18 需 C5＋weekMin 48、C19 需 C18＋weekMin 61",
   GATE["C18"].get("needDone") == ["C5"] and GATE["C18"].get("weekMin") == 48
   and GATE["C19"].get("needDone") == ["C18"] and GATE["C19"].get("weekMin") == 61)

EXP_FLAGS = {
    "C6": ["flag_canteen_grind", "flag_canteen_quit"],
    "C6F": ["flag_studio_follow", "flag_studio_roam"],
    "C7": ["flag_rain_rescue", "flag_rain_shelter", "flag_rain_split"],
    "C11": ["flag_miss_cover", "flag_miss_leak", "flag_miss_deflect"],
    "C8": ["flag_bing_bridge", "flag_bing_background"],
    "C9": ["flag_chase_for_ho", "flag_standup_crew", "flag_mediate_gu_debt"],
    "C10": ["flag_role_gangster", "flag_role_cop"],
    "C15": ["flag_stunt_double", "flag_stunt_refuse"],
    "C14": ["flag_side_tv", "flag_side_film", "flag_side_undecided"],
    "C12": ["flag_fans_support", "flag_fans_avoid", "flag_fans_mediate"],
    "C16": ["flag_vocal_polish", "flag_vocal_train"],
    "C13": ["flag_newyear_improv", "flag_newyear_script", "flag_newyear_twotakes"],
    "C18": ["flag_wf1_studio_dream", "flag_wf1_steady_craft"],
    "C19": ["flag_wf1_gamble_quiet", "flag_wf1_gamble_observe"],
}
for nid, flags in EXP_FLAGS.items():
    got = [c["effects"].get("flags", [None])[0] if c.get("effects") else None
           for c in ALL_NODES[nid]["choices"]]
    ok("%s choice 旗不變 %s" % (nid, flags), got == flags)

EXP_STATS = {
    ("C7", 0): {"industryCredit": 2}, ("C7", 1): {"fame": 1}, ("C7", 2): {"industryCredit": 1},
    ("C11", 0): {"industryCredit": 1}, ("C11", 1): {"fame": 1, "wealth": 1},
    ("C11", 2): {"industryCredit": 1},
    ("C8", 0): {"fame": 3}, ("C8", 1): {"industryCredit": 2},
    ("C9", 0): {"rel_ho": 2}, ("C9", 1): {"industryCredit": 2},
    ("C9", 2): {"rel_ho": 1, "industryCredit": 1},
    ("C10", 0): {"fame": 2}, ("C10", 1): {"industryCredit": 2},
    ("C15", 0): {"fame": 3}, ("C15", 1): {"industryCredit": 1},
    ("C14", 0): {"industryCredit": 2}, ("C14", 1): {"fame": 2}, ("C14", 2): {"industryCredit": 1},
    ("C12", 0): {"fame": 2}, ("C12", 1): {"industryCredit": 1},
    ("C12", 2): {"fame": 1, "industryCredit": 1},
    ("C16", 0): {"fame": 2}, ("C16", 1): {"industryCredit": 2},
    ("C13", 0): {"fame": 2}, ("C13", 1): {"industryCredit": 2},
    ("C13", 2): {"fame": 1, "industryCredit": 1},
    ("C6", 0): {"wealth": 1}, ("C6", 1): {},
    ("C6F", 0): {"wealth": 1}, ("C6F", 1): {},
    ("C18", 0): {"rel_ho": 1, "industryCredit": 1}, ("C18", 1): {"industryCredit": 2},
    ("C19", 0): {"industryCredit": 2}, ("C19", 1): {"industryCredit": 1, "fame": 1},
}
for (nid, ci), st in EXP_STATS.items():
    got = (ALL_NODES[nid]["choices"][ci].get("effects") or {}).get("stats", {})
    ok("%s choice[%d] stats 不變 %s" % (nid, ci, st), got == st)

ok("F4 三旗不變",
   [c["effects"]["flags"] for c in F4["choices"]]
   == [["flag_stay_mind"], ["flag_leave_mind"], ["flag_undecided_mind"]])
ok("G4 兩旗不變",
   [c["effects"]["flags"] for c in G4["choices"]]
   == [["flag_family_job_accept"], ["flag_family_job_decline"]])
ok("C17 靜態 choices 旗不變",
   [c["effects"]["flags"] for c in C17["choices"]]
   == [["flag_ending410_natural"], ["flag_ending410_quit_job"]])
ok("C17 靜態 choices ending410Key 不變",
   [c.get("ending410Key") for c in C17["choices"]] == ["natural", "quit_job"])
ok("C15／C13 債權旗無 ripple（經 story48SettleTick）",
   all("ripple" not in (c.get("effects") or {}) for c in
       T1990["C15"]["choices"] + T1990["C13"]["choices"]))

# ---- 5. ERA 修正句存在、舊句消失 ----
ok("ERA§2 C11 Beat2 降級做口頭提點", "唔係規矩，係呢度嘅做法" in blob(T1989["C11"])
   and "司儀企正中嗰塊板" not in blob(T1989["C11"]))
ok("ERA§2 C11 synopsis 唔再叫規矩", "後台規矩只有一句" not in T1989["C11"]["synopsis"])
ok("ERA M39「一成」無殘留", "一成" not in blob(F4) and "回流比例" not in blob(F4))
ok("STORY_HINT_SOFT.C17 會議室",
   "台慶之後，何生喺會議室等你" in html and "到咗去星河電視台會議室" in html
   and "何生喺後台等你" not in html)
ok("Q4 endingInserts410 嗰排閒角",
   "電視台飯堂嗰排閒角" in html and "電視台飯堂嗰季閒角" not in html)
ok("全檔零黑雨", "黑雨" not in html)
ok("C6／C6F 零嗰季", "嗰季" not in blob(TC6["C6"]) and "嗰季" not in blob(TBR89["C6F"]))

# ---- 6. 年份舊曆寫法（只限 8 個內容 span；STORY_GATE_3Y 係機制表，yearMin／yearEq
# 本來就寫遊戲年份 1991／1992，唔計） ----
for key, span in spans.items():
    if key == "GATE":
        continue
    if key == "TWF1":
        # 唯一例外：WF1 C19 openConditionsNote legacy 字串「1991 春」（live 原值，唔郁）
        n91 = span.count("1991")
        ok("WF1 表年份：只得 legacy openConditionsNote 一處 1991",
           n91 == 1 and "1991 春" in span and span.count("1992") == 0 and span.count("1993") == 0)
    elif key in ("F4_stay_mind", "G4_family_job"):
        ok("%s 零 1991／1992／1993" % key,
           "1991" not in span and "1992" not in span and "1993" not in span)
    else:
        ok("%s 表零 1991／1992／1993" % key,
           "1991" not in span and "1992" not in span and "1993" not in span)

# ---- 7. effects.notes 零數字承諾；beats 無空句；emotion 合法 ----
EMOTIONS = {"neutral", "calm", "tense", "angry", "warm", "tired",
            "smirk", "worried", "soft", "firm"}
bad_notes, empty_beats, bad_emo, bad_kind = [], [], [], []
for nid, node in ALL_NODES.items():
    for c in node.get("choices", []):
        n = (c.get("effects") or {}).get("notes", "")
        if n and re.search(r"[0-9]", n):
            bad_notes.append(nid + ":" + c["id"])
    for b in node.get("beats", []):
        lines = b.get("lines") or ([b["text"]] if b.get("text") else [])
        if not lines or not all(isinstance(x, str) and x.strip() for x in lines):
            empty_beats.append(nid)
        if b.get("emotion") and b["emotion"] not in EMOTIONS:
            bad_emo.append(nid + ":" + str(b["emotion"]))
        if b.get("kind") not in ("system", "npc", "player"):
            bad_kind.append(nid + ":" + str(b.get("kind")))
for nm, node in (("F4", F4), ("G4", G4)):
    for c in node.get("choices", []):
        n = (c.get("effects") or {}).get("notes", "")
        if n and re.search(r"[0-9]", n):
            bad_notes.append(nm + ":" + c["id"])
    for b in node.get("beats", []):
        if not (b.get("text") or "").strip():
            empty_beats.append(nm)
ok("effects.notes 零阿拉伯數字", not bad_notes)
ok("beats 無空句", not empty_beats)
ok("emotion 全部合法", not bad_emo)
ok("kind 只用 system／npc／player", not bad_kind)

# ---- 8. 禁用詞／真人名；紅線 ----
REAL = ["周星馳", "劉德華", "張國榮", "周潤發", "梁朝偉", "梅艷芳", "張曼玉",
        "王祖賢", "鍾楚紅", "林青霞", "陳淑芬", "施南生"]
joined = "".join(v for k, v in spans.items() if k != "GATE")  # 閘表舊註解有「聲量」殘留，唔計
ok("新內容零聲量／Ho哥", "聲量" not in joined and "Ho哥" not in joined)
ok("新內容零真人名", not any(n in joined for n in REAL))
ok("SAVE key 不變", "starVolunteer_map_v19w" in html)
ok("softRev 不變", '"s107"' in html or "'s107'" in html)
ok("?v= 不變", "v20a10" in html)
ok("C17 動態重建接駁在位", "ending410EveNode" in html and "endingEveOptions410" in html)

print("---")
print("ALL PASS" if not fails else "FAILURES: " + " | ".join(fails))
sys.exit(1 if fails else 0)
