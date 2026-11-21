# v20a356 resync：index.html 淨 +20 行（支線複檢 (a) 類修復：WF2 B0＋1／rom159 葉 crisis 分流＋12／enc158 synopsis＋1／lost_role＋4／顧哼歌＋1／鍾追問者＋1）；釘行按段 shift，內容逐字核實純漂移。
# v159 感情線重排：葉敏芝／蘇芷茵 static 測試（新 pack 節點齊全、tier 閘、commit offer、
# WOMEN 六行、送禮分層、星層／感情層分流）。
# 用法：python3 tests/test_rom159_yipso_static.py
import json
import os
import re
import sys

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
idx = open(os.path.join(ROOT, "index.html"), encoding="utf8").read()
pack = json.load(open(os.path.join(ROOT, "content", "story_detail_romance_yip_so.json"), encoding="utf8"))
fails = []
total = [0]


def ok(name, cond):
    total[0] += 1
    if not cond:
        fails.append(name)


nodes = {n["id"]: n for n in pack.get("nodes", [])}

# ---- 1. 節點齊全 ----
want = ["R_yip_meet", "R_yip_push1", "R_yip_push2", "R_yip_crisis", "R_yip_ending",
        "R_so_meet", "R_so_push1", "R_so_push2", "R_so_crisis", "R_so_ending"]
ok("pack 10 節點", len(nodes) == 10)
for w in want:
    ok("節點在場: " + w, w in nodes)

# ---- 2. 結構＋rel 經濟＋HE／BE ----
REL = {"meet": (1, 0), "push1": (2, None), "push2": (2, 0), "crisis": (2, -1), "ending": (3, -2)}
for nid, n in nodes.items():
    arc = n.get("arcBeat")
    ok(nid + " 有 beats", isinstance(n.get("beats"), list) and len(n["beats"]) >= 2)
    ok(nid + " 有 2 個抉擇", isinstance(n.get("choices"), list) and len(n["choices"]) == 2)
    ok(nid + " playerOffer 非 false（v342：行 offer 機制）", n.get("playerOffer") is not False)
    ok(nid + " romanceLine 啱", n.get("romanceLine") in ("yip", "so"))
    written = set(n.get("flags_written") or [])
    got = set()
    for c in n["choices"]:
        got.update((c.get("effects") or {}).get("flags") or [])
    ok(nid + " flags_written＝抉擇寫旗", written == got)
    rels = sorted((c.get("effects") or {}).get("stats", {}).get("rel_yip" if nid.startswith("R_yip") else "rel_so")
                   for c in n["choices"])
    if arc == "push1" and nid.startswith("R_yip"):
        ok("R_yip_push1 rel＋2／−1（守口升、放料跌）", rels == [-1, 2])
    elif arc in REL and REL[arc][1] is not None:
        ok(nid + " rel 經濟 " + str(REL[arc]), rels == sorted(REL[arc]))
    if arc == "ending":
        _fl = lambda c: (c.get("effects") or {}).get("flags") or []
        _pfx = "yip" if nid.startswith("R_yip") else "so"
        he = [c for c in n["choices"] if ("flag_%s_he" % _pfx) in _fl(c)]
        be = [c for c in n["choices"] if ("flag_%s_be" % _pfx) in _fl(c)]
        ok(nid + " HE 寫 commit＋he", len(he) == 1 and ("flag_%s_commit" % _pfx) in _fl(he[0]))
        ok(nid + " BE 唔寫 commit", len(be) == 1 and ("flag_%s_commit" % _pfx) not in _fl(be[0]))

# ---- 3. 弧線鏈接（上一拍旗開下一拍） ----
def oca(nid):
    return (nodes[nid].get("openConditionsAny") or []) + (nodes[nid].get("openConditions") or [])
ok("yip push1 掛 meet 旗", any(f in oca("R_yip_push1") for f in ("flag_yip_met_warm", "flag_yip_met_cool")))
ok("yip push2 掛 push1 旗", any(f in oca("R_yip_push2") for f in ("flag_yip_kept_secret", "flag_yip_leaked")))
ok("yip crisis 掛 push2 旗", any(f in oca("R_yip_crisis") for f in ("flag_yip_stand", "flag_yip_quiet")))
ok("yip ending P5＋掛 crisis 旗", "phase_P5" in oca("R_yip_ending") and any(f in oca("R_yip_ending") for f in ("flag_yip_cleared", "flag_yip_be_route")))
ok("so push1 掛 meet 旗", any(f in oca("R_so_push1") for f in ("flag_so_met_warm", "flag_so_met_cool")))
ok("so push2 掛 push1 旗", any(f in oca("R_so_push2") for f in ("flag_so_confided", "flag_so_kept_distance")))
ok("so crisis 掛 push2 旗", any(f in oca("R_so_crisis") for f in ("flag_so_stayed", "flag_so_obeyed")))
ok("so ending P5＋掛 crisis 旗", "phase_P5" in oca("R_so_ending") and any(f in oca("R_so_ending") for f in ("flag_so_took_risk", "flag_so_played_safe")))

# ---- 4. 葉 push1 守口／放料雙軌 ----
_push1 = nodes["R_yip_push1"]
_keep = [c for c in _push1["choices"] if "flag_yip_kept_secret" in str(c.get("effects", {}).get("flags"))]
_leak = [c for c in _push1["choices"] if "flag_yip_leaked" in str(c.get("effects", {}).get("flags"))]
ok("yip push1 守口 rel＋2", len(_keep) == 1 and _keep[0]["effects"]["stats"].get("rel_yip") == 2)
ok("yip push1 放料 rel−1＋「把口唔穩」標籤", len(_leak) == 1 and _leak[0]["effects"]["stats"].get("rel_yip") == -1
   and (_leak[0]["effects"].get("ripple") or {}).get("tag") == "把口唔穩")
ok("yip push1 守口 notes 係玩家面文字（v20a355 清走製作備忘：冇 ENC79／fx 術語）",
   "ENC79" not in str(_keep[0]["effects"].get("notes", ""))
   and "fx" not in str(_keep[0]["effects"].get("notes", ""))
   and "以後會還" in str(_keep[0]["effects"].get("notes", "")))

# ---- 5. 年份／phase（source 年，YEARS66＋2 之後＝顯示年） ----
ok("yip meet 1989夏（顯示 1991夏）", nodes["R_yip_meet"].get("when") == "1989夏" and nodes["R_yip_meet"].get("phase") == "P2")
ok("so meet 1989春（顯示 1991春）", nodes["R_so_meet"].get("when") == "1989春" and nodes["R_so_meet"].get("phase") == "P2")  # v372：P3→P2（休閒打法 550 日只到 P2，P3 開唔到）
ok("yip ending 1990秋（顯示 1992秋）", nodes["R_yip_ending"].get("when") == "1990秋" and nodes["R_yip_ending"].get("phase") == "P5")
ok("so ending 1990冬（顯示 1992冬）", nodes["R_so_ending"].get("when") == "1990冬" and nodes["R_so_ending"].get("phase") == "P5")
ok("yip meet 掛 N8", nodes["R_yip_meet"].get("linksMain") == ["N8"])
ok("旁白唔寫阿偉「我」", all("我" not in ln for n in nodes.values() for b in n["beats"]
                             if b.get("speaker") == "旁白" for ln in b.get("lines", [])))

# ---- 6. Loader 接線 ----
ok("loader 載 rom3", 'get("story_detail_romance_yip_so.json")' in idx)
ok("loader destructure 有 rom3", "rom1, rom2, rom3, rival" in idx)
ok("STORY_WIRE.romance.yipSo", "STORY_WIRE.romance.yipSo = rom3" in idx)
ok("iterNodes 有 romance_yip_so", 'push("romance_yip_so"' in idx)
ok("未載入 error 有 yip/so", 'romance yip/so 未載入' in idx)
ok("textfix55 有 rom3", "textfix55StoryPack(rom3)" in idx)
ok("years66 有 rom3", "[main, rom1, rom2, rom3, rival" in idx)

# ---- 7. 蘇層級閘 ----
ok("rom159SoMeetGate 定義", "function rom159SoMeetGate()" in idx)
ok("閘數字係 tier>=1", "enc79PlayerTier())>=1" in idx)
ok("rom176BeatOpen 查閘", 'if(key==="so" && typeof rom159SoMeetGate==="function"' in idx)
ok("rom159PrepareNode 有 R_so_meet gate 變體", "R_so_meet_gate" in idx and 'node.id==="R_so_meet"' in idx)
ok("gate 變體有暗示句", "你而家仲係臨記，我唔會同你講呢啲" in idx)
ok("gate 寫 flag_so_gate_seen", "flag_so_gate_seen" in idx)
ok("葉唔使閘（無 yip gate）", "rom159YipMeetGate" not in idx and "R_yip_meet_gate" not in idx)

# ---- 8. Commit offer ----
for who, loc, crisis in (("lan", "rec_hk", "R_lan_crisis"), ("xu", "ad_central", "R_xu_crisis"),
                         ("yip", "tvb_kowloon", "R_yip_crisis"), ("so", "rec_wanchai", "R_so_crisis")):
    ok("CMT_%s NODES 在場" % who, ("COMMIT48_NODES.CMT_%s_commit = {" % who) in idx)
    _m = re.search(r"COMMIT48_DEFS\.CMT_%s_commit = \{([^}]*)\}" % who, idx)
    ok("CMT_%s DEFS 在場" % who, bool(_m))
    if _m:
        _d = _m.group(1)
        ok("CMT_%s loc %s" % (who, loc), ('loc:"%s"' % loc) in _d)
        ok("CMT_%s crisis %s" % (who, crisis), ('crisis:"%s"' % crisis) in _d)
        ok("CMT_%s relKey rel_%s" % (who, who), ('relKey:"rel_%s"' % who) in _d)
        ok("CMT_%s flag flag_%s_commit" % (who, who), ('flag:"flag_%s_commit"' % who) in _d)
        ok("CMT_%s otherFlag null" % who, "otherFlag:null" in _d)
ok("CMT_vera 已刪", "COMMIT48_NODES.CMT_vera_commit" not in idx and "COMMIT48_DEFS.CMT_vera_commit" not in idx)
ok("ending commit 分支有 yip／so", "rom.yip.committed" in idx and "rom.so.committed" in idx)
ok("endingRomance410 有 yip／so 行", 'line("R_yip_meet"' in idx and 'line("R_so_meet"' in idx)

# ---- 9. WOMEN 六行＋37 場（自足覆核） ----
_m = re.search(r"const ROM159_WOMEN = \{(.*?)\n\};", idx, re.S)
_women = _m.group(1) if _m else ""
_keys = re.findall(r"^\s*(\w+):\s*\{", _women, re.M)
ok("WOMEN 六人", _keys == ["hiu", "choi", "lan", "xu", "yip", "so"])
_spots = re.findall(r"spots:\[([^\]]*)\]", _women)
_tot = sum(len([s for s in grp.split(",") if s.strip()]) for grp in _spots)
ok("WOMEN spots 總數 37", _tot == 37)

# ---- 10. 送禮分層＋星層／感情層分流 ----
_g = re.search(r"const ROM159_GIFT_OVERRIDES = \{(.*?)\n\};", idx, re.S)
_gb = _g.group(1) if _g else ""
ok("覆寫有 yip 最愛卡帶＋咖啡豆", "yip:[\"gift_cassette_indie\",\"gift_coffee_beans\"]" in _gb)
ok("覆寫有 so 最愛卡帶＋拍紙簿", "so:[\"gift_cassette_indie\",\"gift_memo_pad\"]" in _gb)
ok("覆寫有 lan 最愛甜品盒＋卡帶", "lan:[\"gift_handmade_sweet\",\"gift_cassette_indie\"]" in _gb)
ok("覆寫有 xu 最愛保溫瓶＋卡帶", "xu:[\"gift_thermos\",\"gift_cassette_indie\"]" in _gb)
ok("覆寫無 vera", "vera:" not in _gb)
ok("覆寫 yip／so dislike 有香水＋雜誌",
   "yip:[\"gift_perfume_sample\",\"gift_fashion_mag\"]" in _gb and "so:[\"gift_perfume_sample\",\"gift_fashion_mag\"]" in _gb)
ok("覆寫 react 葉香水 dislike 講花瓶", "花瓶" in _gb)
ok("覆寫 react 蘇香水 dislike 講玉女海報", "玉女海報" in _gb)
ok("星層葉最愛仍係香水＋雜誌（分流對照）", "yip_manji:{ fav:[\"gift_perfume_sample\",\"gift_fashion_mag\"]" in idx)
ok("星層蘇最愛仍係香水＋髮夾（分流對照）", "so_jiyan:{ fav:[\"gift_perfume_sample\",\"gift_hair_clip_set\"]" in idx)
ok("感情層葉／蘇香水係唔鍾意（分流對照）",
   "yip:[\"gift_perfume_sample\",\"gift_fashion_mag\"]" in _gb and "so:[\"gift_perfume_sample\",\"gift_fashion_mag\"]" in _gb)

# ---- 11. 鏈 D 留返（星層四拍在場，yip_choice 有 guard） ----
ok("ENC79 yip_choice 在場", '"yip_choice"' in idx or "id:\"yip_choice\"" in idx)
ok("yip_choice 有 R_yip_push1 guard", 'StoryOC.isDone("R_yip_push1")' in idx)
ok("ENC79 yip_stand 在場", '"yip_stand"' in idx or "id:\"yip_stand\"" in idx)
ok("鏈 D 人情 credit 讀取在場", "credit_enc79_yip_manager" in idx)

print("ROM159 yip/so static: %d checks, %d FAIL" % (total[0], len(fails)))
if fails:
    for f in fails:
        print("FAIL: " + f)
    sys.exit(1)
print("PASS")
