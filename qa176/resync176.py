#!/usr/bin/env python3
"""v20a176 resync 核實：對照 pristine (a618a5d) 同工作版 index.html，
逐個舊釘行驗證內容逐字相同（純漂移），印出新行號對照表。
漂移（pristine 行號 → 工作版行號）：
  L<=6016: +0；6017-52895: +7；52896-52899: +19；52900-53018: +520；
  53019-53041: +528；53042-53785: +532；53786-53802: 取代區（addLocTalkGiftActs）；
  53803-53887: +519；53888-57855: +524；57856-57869: +527；57870-58028: +528；>=58029: +538。
用法：python3 qa176/resync176.py"""
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PRIS = "/home/hatch/workspace/linji-work176-pristine/index.html"
WORK = os.path.join(ROOT, "index.html")
pris = open(PRIS, encoding="utf-8").read().split("\n")
work = open(WORK, encoding="utf-8").read().split("\n")

def drift(L):
    if L <= 6016: return 0
    if L <= 52895: return 7
    if L <= 52899: return 19
    if L <= 53018: return 520
    if L <= 53041: return 528
    if L <= 53785: return 532
    if L <= 53802: return None
    if L <= 53887: return 519
    if L <= 57855: return 524
    if L <= 57869: return 527
    if L <= 58028: return 528
    return 538

def check(label, old):
    d = drift(old)
    if d is None:
        print(f"SKIP {label}: L{old} 在取代區"); return None
    new = old + d
    same = pris[old - 1] == work[new - 1]
    print(f"{'OK  ' if same else 'DIFF'} {label}: L{old} -> L{new} (d={d}) :: {pris[old-1][:70]!r}")
    if not same:
        print(f"      work L{new}: {work[new-1][:70]!r}")
    return new if same else False

print("== kwan151 (+7) ==")
for L in [25598, 25939, 25987, 26206, 25944, 25942, 25943, 30955, 30946, 27180, 30997, 30954, 27147]:
    check(f"kwan151 L{L}", L)
print("== tang152 (+7) ==")
for L in [25758, 31436, 31580]:
    check(f"tang152 L{L}", L)
print("== text125 (+7) ==")
for L in [27672, 27801, 33494]:
    check(f"text125 L{L}", L)
print("== travel114 COUNT ==")
for L in [32110, 35591, 37718, 38784, 39218, 39221, 39252, 43806, 57908, 58075, 58218, 58239, 58689]:
    check(f"travel114 COUNT L{L}", L)
print("== travel114 FREE (57350/57872 除外：內容改咗行 back176) ==")
for L in [24625, 28155, 30777, 30778, 30790, 30791, 30802, 30803, 30906, 40761, 43463, 43486,
          52735, 52854, 53747, 54129, 54151, 54302, 55939, 57683, 57801, 57802, 57837, 57838, 57857]:
    check(f"travel114 FREE L{L}", L)
print("== tang171/173 DEF ==")
check("travel114 DEF L53860", 53860)
print("== totals ==")
print(f"pristine lines: {len(pris)}, work lines: {len(work)}, delta: {len(work)-len(pris)}")
print("== 新 FREE 行（ROM176 新增 8 處 openLoc encDone）==")
for i, ln in enumerate(work, 1):
    if "openLoc(" in ln and ("{ encDone:true }" in ln or "{encDone:true}" in ln):
        if i > 52890:
            print(f"  L{i}: {ln.strip()[:100]}")
