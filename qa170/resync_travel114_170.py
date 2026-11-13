#!/usr/bin/env python3
"""v20a170 travel114 resync（rebase 上 main 56141a3 後版）：淨 +2 行（awards62FallbackStage 註解 2 行，插入點 L46098；
FLOOR 194→155 係原地改，行數不變）。行號 >=46098 者 +2，其前者唔郁；
DEF 53690→53692、WRAPPER 44172 唔郁（喺插入點之前）；COUNT 13／FREE 27 不變。
核實方法（同 v146／v147／v157）：pristine main 56141a3 vs 工作版 index.html——
  (a) 全部釘行內容逐行相同（舊行號取 pristine 內容，新行號取工作版內容，strip 後比對）；
  (b) 全部 openLoc( 呼叫點序列逐字一致（DEF 行除外）；
  (c) COUNT／FREE 集合大小不變。
用法：python3 qa170/resync_travel114_170.py [--apply]
"""
import re, subprocess, sys

ROOT = "/home/hatch/workspace/linji-work170"
OLD = subprocess.run(["git", "show", "56141a3:index.html"], cwd=ROOT,
                     capture_output=True, text=True).stdout.split("\n")
NEW = open(ROOT + "/index.html", encoding="utf-8").read().split("\n")
TEST = open(ROOT + "/tests/test_travel114_static.py", encoding="utf-8").read()

def parse_set(name):
    m = re.search(name + r" = \{([^}]*)\}", TEST, re.S)
    nums = [int(x) for x in re.findall(r"\d+", re.sub(r"#.*", "", m.group(1)))]
    return nums

COUNT = parse_set("COUNT_LINES")
FREE = parse_set("FREE_LINES")
DEF = int(re.search(r"DEF_LINE = (\d+)", TEST).group(1))
WRAP = int(re.search(r"WRAPPER_LINE = (\d+)", TEST).group(1))
INSERT_AT = 46098
SHIFT = 2

def new_ln(old):
    return old + SHIFT if old >= INSERT_AT else old

ok = True
for label, nums in (("COUNT", COUNT), ("FREE", FREE)):
    for old in nums:
        n = new_ln(old)
        same = OLD[old - 1].strip() == NEW[n - 1].strip()
        if not same:
            ok = False
            print(f"MISMATCH {label} {old}->{n}: old={OLD[old-1].strip()[:80]!r} new={NEW[n-1].strip()[:80]!r}")
print(f"COUNT {len(COUNT)} / FREE {len(FREE)} 釘行內容逐行相同：{'OK' if ok else 'FAIL'}")
for label, old, exp in (("DEF", DEF, 53692), ("WRAPPER", WRAP, 44172)):
    n = new_ln(old)
    same = OLD[old - 1].strip() == NEW[n - 1].strip()
    print(f"{label} {old}->{n}（預期 {exp}）：{'OK' if same and n == exp else 'FAIL'} {OLD[old-1].strip()[:70]!r}")
    ok = ok and same and n == exp

def call_sites(lines, def_ln):
    out = []
    for i, line in enumerate(lines, 1):
        if "openLoc(" in line and i != def_ln:
            out.append(line.strip())
    return out

old_calls = call_sites(OLD, DEF)
new_calls = call_sites(NEW, new_ln(DEF))
print(f"openLoc 呼叫點序列一致：{'OK' if old_calls == new_calls else 'FAIL'}（{len(old_calls)} vs {len(new_calls)}）")
ok = ok and old_calls == new_calls
print(f"COUNT 13／FREE 27：{'OK' if len(COUNT) == 13 and len(FREE) == 27 else 'FAIL'}")

if "--apply" in sys.argv and ok:
    def shift_set(name, nums):
        m = re.search(name + r" = \{([^}]*)\}", TEST, re.S)
        body = m.group(1)
        def repl(mo):
            v = int(mo.group(0))
            return str(new_ln(v)) if v in nums else mo.group(0)
        # 只改集合內數字：逐行處理，行首數字才換
        lines = body.split("\n")
        out_lines = []
        for ln in lines:
            code = ln.split("#", 1)[0]
            found = re.findall(r"\d+", code)
            if found and int(found[0]) in nums:
                ln = ln.replace(found[0], str(new_ln(int(found[0]))), 1)
            out_lines.append(ln)
        return TEST[:m.start(1)] + "\n".join(out_lines) + TEST[m.end(1):]
    new_test = shift_set("COUNT_LINES", COUNT)
    # shift_set 用舊 TEST 計 offset，FREE 要喺已改嘅 new_test 上面再做
    TEST2 = new_test
    m = re.search(r"FREE_LINES = \{([^}]*)\}", TEST2, re.S)
    body = m.group(1)
    out_lines = []
    for ln in body.split("\n"):
        code = ln.split("#", 1)[0]
        found = re.findall(r"\d+", code)
        if found and int(found[0]) in FREE:
            ln = ln.replace(found[0], str(new_ln(int(found[0]))), 1)
        out_lines.append(ln)
    new_test = TEST2[:m.start(1)] + "\n".join(out_lines) + TEST2[m.end(1):]
    new_test = new_test.replace(f"DEF_LINE = {DEF}", f"DEF_LINE = {new_ln(DEF)}", 1)
    hist = ("# v20a170 rebase 上 main 56141a3 resync：淨 +2 行（FallbackStage 註解 2 行，插入點 L46098；FLOOR 原地改）；\n"
            "# 行號 >=46098 者 +2，DEF 53690→53692、WRAPPER 44172 唔郁；COUNT 13／FREE 27 不變。\n")
    anchor = "# 計清單（玩家主動導航，預設計數，唔加旗）：13 處\n"
    new_test = new_test.replace(anchor, hist + anchor, 1)
    open(ROOT + "/tests/test_travel114_static.py", "w", encoding="utf-8").write(new_test)
    print("APPLIED：test_travel114_static.py 已 resync")
sys.exit(0 if ok else 1)
