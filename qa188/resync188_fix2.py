# -*- coding: utf-8 -*-
"""v20a188 resync 第二輪（補 +29）：上一手 resync188.py 用 +225，但 index.html 其後
再加咗 +29 行（NP_WIN 覆寫＋load 呼叫＋gate 行＋debug 入口），總淨變 +254。
本腳本只改行號數字（逐對精確替換，出現唔係一次就停），內容已由
qa188/resync188_verify.py 用 difflib 對位核實全部純漂移。
用法：python3 qa188/resync188_fix2.py
"""
import re
import sys

ROOT = ''


def fix(path, pairs, comment_old=None, comment_new=None):
    s = open(path, encoding='utf-8').read()
    for old, new in pairs:
        n = s.count(old)
        assert n == 1, f"{path}: {old!r} 出現 {n} 次（預期 1）"
        s = s.replace(old, new)
    if comment_old:
        assert s.count(comment_old) == 1, f"{path}: comment 唔見"
        s = s.replace(comment_old, comment_new)
    open(path, 'w', encoding='utf-8').write(s)
    print(f"OK {path}（{len(pairs)} 處）")


C29 = ("# v20a188 resync：index.html 淨 +225 行（AWARDS188 覆寫表＋角色閘，插入點 L45380–46310）；"
       "其後釘行各 +225，之前唔郁；總行數 60155→60380。")
C29_NEW = ("# v20a188 resync：index.html 淨 +225 行（AWARDS188 覆寫表＋角色閘，插入點 L45380–46310）；"
           "其後釘行各 +225，之前唔郁；總行數 60155→60380。\n"
           "# v20a188 resync 補 +29：上一手 +225 計少咗其後再加嘅 NP_WIN 覆寫＋load 呼叫＋gate 行＋debug 入口"
           "（淨 +29）；總淨變 +254，總行數 60409；difflib 對位核實全部錨點純漂移，見 qa188/resync188_verify.py。")

# ---- travel114 ----
pairs114 = []
for a, b in [(58936, 58965), (59114, 59143), (59257, 59286), (59278, 59307),
             (53129, 53158), (53248, 53277), (53298, 53327), (53521, 53550),
             (53560, 53589), (53566, 53595), (53633, 53662), (53635, 53664),
             (53638, 53667), (53665, 53694), (54776, 54805), (55150, 55179),
             (55172, 55201), (55323, 55352), (56960, 56989), (58704, 58733),
             (58822, 58851), (58823, 58852), (58858, 58887), (58859, 58888),
             (58884, 58913), (59728, 59757)]:
    pairs114.append((f"    {a},", f"    {b},"))
pairs114.append(("DEF_LINE = 54876", "DEF_LINE = 54905"))
fix("tests/test_travel114_static.py", pairs114, C29, C29_NEW)

# ---- rom176 ----
fix("tests/test_rom176_static.py", [
    ("line(53306)", "line(53335)"),
    ("line(53674)", "line(53703)"),
    ("line(54813)", "line(54842)"),
    ("line(54907)", "line(54936)"),
], C29, C29_NEW)

# ---- tang171 / tang173 ----
for f in ("tests/test_tang171_static.py", "tests/test_tang173_static.py"):
    fix(f, [
        ("src.count('\\n') == 60380", "src.count('\\n') == 60409"),
        ("len(lines) >= 54876 and 'function openLoc(id, opts){' in lines[54875]",
         "len(lines) >= 54905 and 'function openLoc(id, opts){' in lines[54904]"),
    ], C29, C29_NEW)

# ---- gift185 ----
fix("tests/test_gift185_static.py", [
    ("html.count('\\n') == 60380", "html.count('\\n') == 60409"),
], C29, C29_NEW)

print("全部改完")
