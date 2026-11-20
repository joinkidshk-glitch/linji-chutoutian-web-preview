#!/usr/bin/env python3
# v342: remove playerOffer:false from R_ nodes + fix crisis/push2 when 1991->1990 (display 1993->1992)
import json, re, sys

FILES = [
    "content/story_detail_romance_lan_xu.json",
    "content/story_detail_romance_vera_hiu_choi.json",
    "content/story_detail_romance_yip_so.json",
]
WHEN_FIX = {"R_lan_crisis", "R_xu_push2", "R_xu_crisis", "R_hiu_crisis", "R_choi_crisis"}

for path in FILES:
    lines = open(path, encoding="utf8").read().split("\n")
    out = []
    cur_id = None
    removed = 0
    when_fixed = []
    for line in lines:
        m = re.search(r'"id":\s*"([^"]+)"', line)
        if m:
            cur_id = m.group(1)
        # playerOffer removal
        if re.match(r'^\s*"playerOffer": false,\s*$', line):
            removed += 1
            continue
        if re.match(r'^\s*"playerOffer": false\s*$', line):
            # last property: strip trailing comma from previous emitted line
            for j in range(len(out) - 1, -1, -1):
                if out[j].strip():
                    if out[j].rstrip().endswith(","):
                        out[j] = out[j].rstrip()[:-1]
                    break
            removed += 1
            continue
        # when fix for target nodes
        if cur_id in WHEN_FIX and '"when":' in line and "1991" in line:
            new = line.replace("1991", "1990", 1)
            when_fixed.append((cur_id, line.strip(), new.strip()))
            out.append(new)
            continue
        out.append(line)
    text = "\n".join(out)
    # validate JSON
    d = json.loads(text)
    open(path, "w", encoding="utf8").write(text)
    print(path, "removed playerOffer:", removed, "when fixed:", when_fixed, "nodes:", len(d.get("nodes", [])))
print("OK")
