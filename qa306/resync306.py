# qa306/resync306.py — v20a306 resync：index.html 淨 +10 行
#   Q19 齊 FRAME cap／wrap 各寫兩個版本：
#     (a) FRAME 新欄 cap_try／wrap_safe＋註解 ＋4 行 @舊 L37881 後（wrap 行之後；wrap 行本身加咗個逗號，內容其餘逐字相同）
#     (b) enc79BuildScript wrap 換句 ＋3 行 @舊 L40073 後（wrapEcho if 行之後）
#     (c) enc79BuildScript cap 換句 ＋3 行 @舊 L40247 後（capHit if 行之後）
#   漂移規則（舊行號 → 新行號，difflib 對位核實，見下 shift()）：
#     ≤37881 唔郁；37882–40073 ＋4；40074–40247 ＋7；≥40248 ＋10。
#   今次有釘行命中嘅全部喺 ≥40248 段，一律 ＋10；＋4／＋7 段無釘行。
#   方法：先對 pristine main（常駐 clone，v305）逐行核實純漂移（內容逐字相同），然後每檔單次掃描
#   dict 查表改 pin（唔用逐對 re.sub，唔會撞值／重複；歷史 resync 註解入面嘅舊行號唔郁）。
#   ok() 名入面嘅 L 號係歷史標籤，唔郁；每檔頂加一行 v306 resync 註解。
# 用法：python3 qa306/resync306.py [--check-only]
#   預設：pristine = ~/workspace/linji-repo/index.html；work = 同目錄上一層 index.html。
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
PRISTINE = os.environ.get("RESYNC306_PRISTINE", os.path.expanduser("~/workspace/linji-repo/index.html"))
WORK = os.environ.get("RESYNC306_WORK", os.path.join(ROOT, "index.html"))
CHECK_ONLY = "--check-only" in sys.argv


def shift(old):
    if old <= 37881:
        return old
    if old <= 40073:
        return old + 4
    if old <= 40247:
        return old + 7
    return old + 10


def new_line(old):
    return shift(old)


# ---- (1) 行號 pin：(舊行, 錨點字串)；新行由 new_line() 計，逐行核實 pristine 舊行內容 == work 新行內容 ----
LINE_PINS = {
    "tests/test_rom176_static.py": [
        (40670, "/* ===== v20a176 ROM176"),
        (41020, "function rom176ApplyGiftOverrides()"),
        (42323, "function addLocTalkGiftActs(add, L, npcId)"),
        (42479, "rom176TryIntercept(id)"),
    ],
}

# ---- (2) travel114：COUNT／FREE／DEF／WRAPPER（現行 v305 值）----
TRAVEL114_PINS = [
    ("COUNT", 15363), ("COUNT", 18672), ("COUNT", 20882), ("COUNT", 22085),
    ("COUNT", 22525), ("COUNT", 22528), ("COUNT", 22559), ("COUNT", 28534),
    ("COUNT", 45714), ("COUNT", 45922), ("COUNT", 46080), ("COUNT", 46101),
    ("FREE", 6525), ("FREE", 6526), ("FREE", 8217), ("FREE", 14215), ("FREE", 14216),
    ("FREE", 14228), ("FREE", 14229), ("FREE", 14240), ("FREE", 14241), ("FREE", 14341),
    ("FREE", 24721), ("FREE", 26065), ("FREE", 26066), ("FREE", 26142), ("FREE", 28342),
    ("FREE", 28375), ("FREE", 40468), ("FREE", 40587), ("FREE", 40662), ("FREE", 40862),
    ("FREE", 40906), ("FREE", 40912), ("FREE", 40979), ("FREE", 40981), ("FREE", 40984),
    ("FREE", 41011), ("FREE", 42286), ("FREE", 42333), ("FREE", 42703), ("FREE", 42725),
    ("FREE", 42877), ("FREE", 42882), ("FREE", 43807), ("FREE", 45284), ("FREE", 45591),
    ("FREE", 45592), ("FREE", 45636), ("FREE", 45637), ("FREE", 45662), ("FREE", 46551),
    ("DEF", 42438), ("WRAPPER", 29103),
]

# ---- (3) 字串 pin：(檔, 舊片段, 新片段)——每段喺檔內唯一，先驗證 count == 1 ----
STR_PINS = {
    "tests/test_rom176_static.py": [
        ("line(40670).startswith('/* ===== v20a176 ROM176')", "line(40680).startswith('/* ===== v20a176 ROM176')"),
        ("line(41020).startswith('function rom176ApplyGiftOverrides()')", "line(41030).startswith('function rom176ApplyGiftOverrides()')"),
        ("line(42323).startswith('function addLocTalkGiftActs(add, L, npcId)')", "line(42333).startswith('function addLocTalkGiftActs(add, L, npcId)')"),
        ("'rom176TryIntercept(id)' in line(42479)", "'rom176TryIntercept(id)' in line(42489)"),
    ],
    "tests/test_gift185_static.py": [
        ("總行數 47229（v193 61167", "總行數 47239（v193 61167"),
        ("== 47229)", "== 47239)"),
        ("＋v304 +38＋v305 +35）", "＋v304 +38＋v305 +35＋v306 +10）"),
    ],
    "tests/test_tang171_static.py": [
        ("總行數 47229（v193 61167", "總行數 47239（v193 61167"),
        ("== 47229)", "== 47239)"),
        ("＋v304 +38＋v305 +35）", "＋v304 +38＋v305 +35＋v306 +10）"),
        ("openLoc DEF 行 42438（", "openLoc DEF 行 42448（"),
        ("＋v304 +38＋v305 +35，travel114", "＋v304 +38＋v305 +35＋v306 +10，travel114"),
        (">= 42444", ">= 42454"),
        ("lines[42437]", "lines[42447]"),
    ],
    "tests/test_tang173_static.py": [
        ("總行數 47229（v193 61167", "總行數 47239（v193 61167"),
        ("== 47229)", "== 47239)"),
        ("＋v304 +38＋v305 +35）", "＋v304 +38＋v305 +35＋v306 +10）"),
        ("openLoc DEF 行 42438（", "openLoc DEF 行 42448（"),
        ("＋v304 +38＋v305 +35，travel114", "＋v304 +38＋v305 +35＋v306 +10，travel114"),
        (">= 42444", ">= 42454"),
        ("lines[42437]", "lines[42447]"),
    ],
}

RESYNC_NOTE = {
    "tests/test_rom176_static.py": "# v20a306 resync：index.html 淨 +10 行（Q19：FRAME cap_try／wrap_safe ＋4／wrap 換句 ＋3／cap 換句 ＋3，插入點全部喺釘行之前）；釘行各 ＋10（40670→40680、41020→41030、42323→42333、42479→42489），內容逐字相同，純漂移；ok() 名入面嘅 L 號係歷史標籤，唔郁。\n",
    "tests/test_gift185_static.py": "# v20a306 resync：index.html 淨 +10 行；總行數 47229→47239（鏈尾加 ＋v306 +10）。\n",
    "tests/test_tang171_static.py": "# v20a306 resync：index.html 淨 +10 行；總行數 47229→47239、openLoc DEF 42438→42448（鏈尾加 ＋v306 +10；DEF guard 42444→42454、index 42437→42447）。\n",
    "tests/test_tang173_static.py": "# v20a306 resync：index.html 淨 +10 行；總行數 47229→47239、openLoc DEF 42438→42448（鏈尾加 ＋v306 +10；DEF guard 42444→42454、index 42437→42447）。\n",
    "tests/test_travel114_static.py": "# v20a306 resync：index.html 淨 +10 行（Q19，插入點見 qa306/resync306.py）；COUNT／FREE／DEF／WRAPPER 按段重算（≤37881 唔郁、37882–40073 ＋4、40074–40247 ＋7、≥40248 ＋10；命中嘅全部喺 ≥40248 段，一律 ＋10；DEF 42438→42448、WRAPPER 29103 唔郁），內容逐行核實純漂移；openLoc( 呼叫點總數不變。\n",
}


def main():
    with open(PRISTINE, encoding="utf-8") as f:
        pris = f.read().split("\n")
    with open(WORK, encoding="utf-8") as f:
        work = f.read().split("\n")
    print("pristine %s：%d 行；work %s：%d 行；淨 %s%d 行"
          % (PRISTINE, len(pris) - 1, WORK, len(work) - 1,
             "+" if len(work) >= len(pris) else "", len(work) - len(pris)))
    assert len(work) - len(pris) == 10, "淨行數唔係 +10，停低檢查"
    fails = []

    # ---- (1) LINE_PINS：逐行核實 pristine 舊行內容 == work 新行內容 ----
    for fname, pins in LINE_PINS.items():
        for old, anchor in pins:
            new = new_line(old)
            p = pris[old - 1] if 0 < old <= len(pris) else ""
            w = work[new - 1] if 0 < new <= len(work) else ""
            if p != w or anchor not in w:
                fails.append("%s：pin %d→%d 內容唔同／錨點唔見（pristine=%r work=%r）" % (fname, old, new, p[:80], w[:80]))
            else:
                print("  pin ok %s %d→%d（%s）" % (fname, old, new, anchor[:40]))

    # ---- (2) travel114 pins：逐行核實純漂移 ----
    for kind, old in TRAVEL114_PINS:
        new = new_line(old)
        p = pris[old - 1] if 0 < old <= len(pris) else ""
        w = work[new - 1] if 0 < new <= len(work) else ""
        if p != w:
            fails.append("travel114 %s pin %d→%d 內容唔同（pristine=%r work=%r）" % (kind, old, new, p[:80], w[:80]))
    print("  travel114 pins 核實完：%d 處" % len(TRAVEL114_PINS))
    if fails:
        print("FAILURES:\n" + "\n".join(fails))
        sys.exit(1)
    if CHECK_ONLY:
        print("CHECK-ONLY PASS：全部釘行純漂移核實通過，未寫檔")
        return

    # ---- (3) travel114：set 內逐行 shift（單次掃描，只改行首數字）----
    tpath = os.path.join(ROOT, "tests/test_travel114_static.py")
    with open(tpath, encoding="utf-8") as f:
        tlines = f.read().split("\n")
    pmap = {old: new_line(old) for _, old in TRAVEL114_PINS}
    # 只喺 COUNT_LINES／FREE_LINES set 區內改行首數字；DEF／WRAPPER 用整行匹配
    in_set = None
    changed = 0
    for i, ln in enumerate(tlines):
        if ln.startswith("COUNT_LINES = {"):
            in_set = "COUNT"
            continue
        if ln.startswith("FREE_LINES = {"):
            in_set = "FREE"
            continue
        if in_set and ln.strip() == "}":
            in_set = None
            continue
        if in_set:
            m = re.match(r"^(\s*)(\d+)(,.*)$", ln)
            if m:
                old = int(m.group(2))
                if old in pmap and pmap[old] != old:
                    tlines[i] = m.group(1) + str(pmap[old]) + m.group(3)
                    changed += 1
                elif old not in pmap:
                    print("  警告：travel114 %s 區有未列入 pmap 嘅行號 %d（%s），唔郁" % (in_set, old, ln.strip()[:60]))
        elif ln.startswith("DEF_LINE = "):
            m = re.match(r"^DEF_LINE = (\d+)(.*)$", ln)
            if m and int(m.group(1)) in pmap and pmap[int(m.group(1))] != int(m.group(1)):
                tlines[i] = "DEF_LINE = " + str(pmap[int(m.group(1))]) + m.group(2)
                changed += 1
    print("  travel114 改咗 %d 處（預期 29：COUNT 4＋FREE 24＋DEF 1）" % changed)
    assert changed == 29, "travel114 改動數唔啱"
    with open(tpath, "w", encoding="utf-8") as f:
        f.write("\n".join(tlines))

    # ---- (4) STR_PINS：每段檔內唯一，先驗證 count == 1 再換 ----
    for fname, pairs in STR_PINS.items():
        fpath = os.path.join(ROOT, fname)
        with open(fpath, encoding="utf-8") as f:
            txt = f.read()
        for old, new in pairs:
            c = txt.count(old)
            if c != 1:
                print("FAILURES：%s 舊片段出現 %d 次（預期 1）：%r" % (fname, c, old[:70]))
                sys.exit(1)
            txt = txt.replace(old, new)
            print("  str ok %s：%r → %r" % (fname, old[:50], new[:50]))
        with open(fpath, "w", encoding="utf-8") as f:
            f.write(txt)

    # ---- (5) 每檔頂加 v306 resync 註解 ----
    for fname, note in RESYNC_NOTE.items():
        fpath = os.path.join(ROOT, fname)
        with open(fpath, encoding="utf-8") as f:
            txt = f.read()
        assert "v20a306 resync" not in txt, "%s 已經有 v306 註解，唔重加" % fname
        with open(fpath, "w", encoding="utf-8") as f:
            f.write(note + txt)
        print("  note ok %s" % fname)

    print("RESYNC306 DONE")


if __name__ == "__main__":
    main()
