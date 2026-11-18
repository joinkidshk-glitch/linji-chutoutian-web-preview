# qa294/resync294.py — v20a294 resync：index.html 淨 +17 行
#   Q7 曉晴 HE 鎖死三處改動：
#     (a) commit48Available CMT 閘 ＋2 行 @舊 L25060 之後
#     (b) rom159PrepareNode HE 換選擇 ＋14 行 @舊 L25906 之後
#     (c) enc158 危機改寫 1 行→2 行 ＋1 @舊 L27342（舊行本身內容變咗，唔係 pin）
#   漂移規則（舊行號 → 新行號）：＜25061 唔郁；25061–25906 ＋2；25907–27341 ＋16；≥27342 ＋17。
#   方法：先對 pristine main（常駐 clone）逐行核實純漂移（內容逐字相同），然後每檔單次掃描
#   dict 查表改 pin（唔用逐對 re.sub，唔會撞值／重複；歷史 resync 註解入面嘅舊行號唔郁）。
#   ok() 名入面嘅 L 號係歷史標籤，唔郁；每檔頂加一行 v294 resync 註解。
# 用法：python3 qa294/resync294.py [--check-only]
#   預設：pristine = ~/workspace/linji-repo/index.html；work = 同目錄上一層 index.html。
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
PRISTINE = os.environ.get("RESYNC294_PRISTINE", os.path.expanduser("~/workspace/linji-repo/index.html"))
WORK = os.environ.get("RESYNC294_WORK", os.path.join(ROOT, "index.html"))
CHECK_ONLY = "--check-only" in sys.argv


def shift(old):
    if old < 25061:
        return old
    if old <= 25906:
        return old + 2
    if old <= 27341:
        return old + 16
    return old + 17


# ---- (1) 行號 pin：(舊行, 錨點字串)；新行由 shift() 計，逐行核實 pristine 舊行內容 == work 新行內容 ----
LINE_PINS = {
    "tests/test_rom159_static.py": [
        (25117, "v20a159 ROM159 Phase 1"),
        (25951, "COMMIT48_NODES.CMT_lan_commit"),
        (25866, "function rom159SoMeetGate"),
        (25145, "全佳"),
    ],
    "tests/test_rom176_static.py": [
        (40173, "v20a176 ROM176"),
        (40531, "function rom176ApplyGiftOverrides()"),
        (41844, "function addLocTalkGiftActs(add, L, npcId)"),
        (42000, "rom176TryIntercept(id)"),
    ],
}

# ---- (2) travel114：COUNT／FREE／DEF／WRAPPER——set 內逐行 shift（只改行首數字，註解唔郁）----
TRAVEL114_PINS = [
    ("COUNT", 15398), ("COUNT", 18707), ("COUNT", 20908), ("COUNT", 22112),
    ("COUNT", 22552), ("COUNT", 22555), ("COUNT", 22586), ("COUNT", 28126),
    ("COUNT", 45198), ("COUNT", 45410), ("COUNT", 45568), ("COUNT", 45589),
    ("FREE", 6531), ("FREE", 6532), ("FREE", 8223), ("FREE", 14250), ("FREE", 14251),
    ("FREE", 14263), ("FREE", 14264), ("FREE", 14275), ("FREE", 14276), ("FREE", 14376),
    ("FREE", 24373), ("FREE", 25716), ("FREE", 25717), ("FREE", 25793), ("FREE", 27935),
    ("FREE", 27968), ("FREE", 39971), ("FREE", 40090), ("FREE", 40165), ("FREE", 40373),
    ("FREE", 40417), ("FREE", 40423), ("FREE", 40490), ("FREE", 40492), ("FREE", 40495),
    ("FREE", 40522), ("FREE", 41807), ("FREE", 41854), ("FREE", 42224), ("FREE", 42246),
    ("FREE", 42398), ("FREE", 42403), ("FREE", 43327), ("FREE", 44805), ("FREE", 45075),
    ("FREE", 45076), ("FREE", 45120), ("FREE", 45121), ("FREE", 45146), ("FREE", 46039),
    ("DEF", 41959), ("WRAPPER", 28695),
]

# ---- (3) 字串 pin：(檔, 舊片段, 新片段)——每段喺檔內唯一，先驗證 count == 1 ----
STR_PINS = {
    "tests/test_rom159_static.py": [
        ('line_has(25117, "v20a159 ROM159 Phase 1")', 'line_has(25119, "v20a159 ROM159 Phase 1")'),
        ('line_has(25951, "COMMIT48_NODES.CMT_lan_commit")', 'line_has(25967, "COMMIT48_NODES.CMT_lan_commit")'),
        ('line_has(25866, "function rom159SoMeetGate")', 'line_has(25868, "function rom159SoMeetGate")'),
        ("idx_lines[25145 - 1]", "idx_lines[25147 - 1]"),
    ],
    "tests/test_rom176_static.py": [
        ("line(40173).startswith('/* ===== v20a176 ROM176')", "line(40190).startswith('/* ===== v20a176 ROM176')"),
        ("line(40531).startswith('function rom176ApplyGiftOverrides()')", "line(40548).startswith('function rom176ApplyGiftOverrides()')"),
        ("line(41844).startswith('function addLocTalkGiftActs(add, L, npcId)')", "line(41861).startswith('function addLocTalkGiftActs(add, L, npcId)')"),
        ("'rom176TryIntercept(id)' in line(42000)", "'rom176TryIntercept(id)' in line(42017)"),
    ],
    "tests/test_gift185_static.py": [
        ("總行數 46717（v193 61167", "總行數 46734（v193 61167"),
        ("== 46717)", "== 46734)"),
        ("＋v290 +461）", "＋v290 +461＋v294 +17）"),
    ],
    "tests/test_tang171_static.py": [
        ("總行數 46717（v193 61167", "總行數 46734（v193 61167"),
        ("== 46717)", "== 46734)"),
        ("＋v290 +461）", "＋v290 +461＋v294 +17）"),
        ("openLoc DEF 行 41959（", "openLoc DEF 行 41976（"),
        ("＋v290 +461，travel114", "＋v290 +461＋v294 +17，travel114"),
        (">= 41965", ">= 41982"),
        ("lines[41958]", "lines[41975]"),
    ],
    "tests/test_tang173_static.py": [
        ("總行數 46717（v193 61167", "總行數 46734（v193 61167"),
        ("== 46717)", "== 46734)"),
        ("＋v290 +461）", "＋v290 +461＋v294 +17）"),
        ("openLoc DEF 行 41959（", "openLoc DEF 行 41976（"),
        ("＋v290 +461，travel114", "＋v290 +461＋v294 +17，travel114"),
        (">= 41965", ">= 41982"),
        ("lines[41958]", "lines[41975]"),
    ],
}

RESYNC_NOTE = {
    "tests/test_rom159_static.py": "# v20a294 resync：index.html 淨 +17 行（Q7：CMT 閘 ＋2 @舊 L25060 後／HE 換選擇 ＋14 @舊 L25906 後／危機改寫 ＋1 @舊 L27342）；釘行按段重算（25117→25119、25951→25967、25866→25868、全佳 25145→25147；內容逐字相同，純漂移；ok() 名入面嘅 L 號係歷史標籤，唔郁）。\n",
    "tests/test_rom176_static.py": "# v20a294 resync：index.html 淨 +17 行（Q7，插入點全部喺釘行之前）；釘行各 ＋17（40173→40190、40531→40548、41844→41861、42000→42017），內容逐字相同，純漂移；ok() 名入面嘅 L 號係歷史標籤，唔郁。\n",
    "tests/test_gift185_static.py": "# v20a294 resync：index.html 淨 +17 行；總行數 46717→46734（鏈尾加 ＋v294 +17）。\n",
    "tests/test_tang171_static.py": "# v20a294 resync：index.html 淨 +17 行；總行數 46717→46734、openLoc DEF 41959→41976（鏈尾加 ＋v294 +17；DEF guard 41965→41982、index 41958→41975）。\n",
    "tests/test_tang173_static.py": "# v20a294 resync：index.html 淨 +17 行；總行數 46717→46734、openLoc DEF 41959→41976（鏈尾加 ＋v294 +17；DEF guard 41965→41982、index 41958→41975）。\n",
    "tests/test_travel114_static.py": "# v20a294 resync：index.html 淨 +17 行（Q7：CMT 閘 ＋2 @舊 L25060 後／HE 換選擇 ＋14 @舊 L25906 後／危機改寫 ＋1 @舊 L27342）；COUNT／FREE／DEF／WRAPPER 按段重算（＜25061 唔郁、25061–25906 ＋2、25907–27341 ＋16、≥27342 ＋17；DEF 41959→41976、WRAPPER 28695→28712），內容逐行核實純漂移；openLoc( 呼叫點總數不變。\n",
}


def main():
    with open(PRISTINE, encoding="utf-8") as f:
        pris = f.read().split("\n")
    with open(WORK, encoding="utf-8") as f:
        work = f.read().split("\n")
    print("pristine %s：%d 行；work %s：%d 行；淨 %s%d 行"
          % (PRISTINE, len(pris) - 1, WORK, len(work) - 1,
             "+" if len(work) >= len(pris) else "", len(work) - len(pris)))
    assert len(work) - len(pris) == 17, "淨行數唔係 +17，停低唔做"

    fails = []

    # ---- 核實 (1)：行號 pin 純漂移 ----
    for fname, pins in LINE_PINS.items():
        for old, anchor in pins:
            new = shift(old)
            a = pris[old - 1] if 0 < old <= len(pris) else None
            b = work[new - 1] if 0 < new <= len(work) else None
            ok = (a is not None and anchor in a and a == b)
            print(("PASS " if ok else "FAIL ") + "%s：%d→%d %s" % (fname, old, new, anchor[:40]))
            if not ok:
                fails.append("%s pin %d" % (fname, old))

    # ---- 核實 (2)：travel114 全部錨點純漂移 ----
    for kind, old in TRAVEL114_PINS:
        new = shift(old)
        a = pris[old - 1] if 0 < old <= len(pris) else None
        b = work[new - 1] if 0 < new <= len(work) else None
        ok = (a is not None and a == b)
        if not ok:
            print("FAIL travel114 %s：%d→%d 內容唔同：%r vs %r" % (kind, old, new, a, b))
            fails.append("travel114 %s %d" % (kind, old))
    print("travel114：%d 處錨點核實 %s" % (len(TRAVEL114_PINS), "全過" if not fails else "有 FAIL"))

    # ---- 核實 (3)：字串 pin 唯一 ----
    for fname, pairs in STR_PINS.items():
        with open(os.path.join(ROOT, fname), encoding="utf-8") as f:
            txt = f.read()
        for old_frag, _new_frag in pairs:
            n = txt.count(old_frag)
            if n != 1:
                print("FAIL %s：片段出現 %d 次（要 1 次）：%r" % (fname, n, old_frag[:60]))
                fails.append("%s frag %r" % (fname, old_frag[:40]))

    if fails:
        print("\nFAILURES: %d 處，停低唔改" % len(fails))
        return 1
    if CHECK_ONLY:
        print("\nCHECK-ONLY：全部核實通過，冇改檔")
        return 0

    # ---- 改檔：每檔單次掃描 dict 查表（regex alternation，最長先）----
    for fname, pairs in STR_PINS.items():
        path = os.path.join(ROOT, fname)
        with open(path, encoding="utf-8") as f:
            txt = f.read()
        table = dict(pairs)
        pat = re.compile("|".join(re.escape(k) for k in sorted(table, key=len, reverse=True)))
        txt2, n = pat.subn(lambda m: table[m.group(0)], txt)
        assert n == len(pairs), "%s：換咗 %d 處，預期 %d" % (fname, n, len(pairs))
        txt2 = RESYNC_NOTE[fname] + txt2
        with open(path, "w", encoding="utf-8") as f:
            f.write(txt2)
        print("改 %s：%d 處字串 pin＋頂加 resync 註解" % (fname, n))

    # ---- travel114：set 內逐行 shift（只改行首數字）----
    path = os.path.join(ROOT, "tests/test_travel114_static.py")
    with open(path, encoding="utf-8") as f:
        tlines = f.read().split("\n")
    mapping = {}
    for kind, old in TRAVEL114_PINS:
        mapping[old] = shift(old)
    # 搵 COUNT_LINES／FREE_LINES 兩個 set 嘅範圍＋DEF／WRAPPER 賦值行
    changed = 0
    in_set = None
    for i, ln in enumerate(tlines):
        s = ln.strip()
        if s.startswith("COUNT_LINES = {"):
            in_set = "COUNT"
            continue
        if s.startswith("FREE_LINES = {"):
            in_set = "FREE"
            continue
        if s == "}":
            in_set = None
            continue
        if in_set:
            m = re.match(r"^(\s*)(\d+),", ln)
            if m and int(m.group(2)) in mapping:
                old = int(m.group(2))
                tlines[i] = m.group(1) + str(mapping[old]) + ln[m.end(2):]
                changed += 1
            continue
        m = re.match(r"^DEF_LINE = (\d+)", ln)
        if m and int(m.group(1)) in mapping:
            tlines[i] = ln.replace(m.group(1), str(mapping[int(m.group(1))]), 1)
            changed += 1
            continue
        m = re.match(r"^WRAPPER_LINE = (\d+)", ln)
        if m and int(m.group(1)) in mapping:
            tlines[i] = ln.replace(m.group(1), str(mapping[int(m.group(1))]), 1)
            changed += 1
    assert changed == len(TRAVEL114_PINS), "travel114：改咗 %d 處，預期 %d" % (changed, len(TRAVEL114_PINS))
    with open(path, "w", encoding="utf-8") as f:
        f.write(RESYNC_NOTE["tests/test_travel114_static.py"] + "\n".join(tlines))
    print("改 tests/test_travel114_static.py：%d 處錨點 shift＋頂加 resync 註解" % changed)
    print("\nALL DONE")
    return 0


if __name__ == "__main__":
    sys.exit(main())
