# -*- coding: utf-8 -*-
"""v20a195 rebase 衝突解法：5 檔測試同 v192 main 衝突（兩邊都只係行號 resync）。
解法：以 HEAD（v192 版，b104f85 釘）做底，按 qa195/resync195_rebase.py
difflib 映射（BAD: 0，內容逐字核實）重算 v195 釘行；數字用單次掃描 dict 查表，
唔逐對 re.sub（v160 教訓）。
用法：python3 qa195/resolve_rebase195.py
"""
import re, sys

ROOT = "/home/hatch/workspace/linji-work195"

# HEAD（b104f85）釘 → rebase 後正確釘（1-based 行號）
NUMMAP = {
    60522: 60609,
    31583: 31587, 53448: 53532, 53816: 53900, 54955: 55039, 55049: 55133,
    32184: 32188, 35680: 35687, 37807: 37814, 38888: 38897, 39322: 39331,
    39325: 39334, 39356: 39365, 43911: 43920, 59078: 59162, 59256: 59340,
    59399: 59486, 59420: 59507,
    28228: 28232, 30851: 30855, 30852: 30856, 30864: 30868, 30865: 30869,
    30876: 30880, 30877: 30881, 30980: 30984, 40866: 40875, 43568: 43577,
    43591: 43600, 53271: 53355, 53390: 53474, 53440: 53524, 53663: 53747,
    53702: 53786, 53708: 53792, 53775: 53859, 53777: 53861, 53780: 53864,
    53807: 53891, 54918: 55002, 55292: 55376, 55314: 55398, 55465: 55549,
    57102: 57186, 58846: 58930, 58964: 59048, 58965: 59049, 59000: 59084,
    59001: 59085, 59026: 59110, 59870: 59957,
    55018: 55102, 44434: 44443,
}
NUM_RE = re.compile(r"\d+")

def map_numbers(text):
    return NUM_RE.sub(lambda m: str(NUMMAP.get(int(m.group(0)), m.group(0))), text)

BLOCK_RE = re.compile(r"<<<<<<< HEAD\n(.*?)\n=======\n.*?\n>>>>>>> [^\n]*\n", re.S)

def resolve_mapped(path, label_map=None):
    """將每個衝突塊換成 HEAD 側經 NUMMAP 映射後嘅文字（＋label 更新）。"""
    p = ROOT + "/" + path
    s = open(p, encoding="utf-8").read()
    blocks = BLOCK_RE.findall(s)
    assert blocks, path + ": 冇衝突塊"
    def repl(m):
        head = m.group(1)
        out = map_numbers(head)
        if label_map:
            for a, b in label_map.items():
                assert out.count(a) == 1, "%s: label %r 出現 %d 次" % (path, a, out.count(a))
                out = out.replace(a, b)
        return out + "\n"
    s2, n = BLOCK_RE.subn(repl, s)
    assert n == len(blocks), path
    open(p, "w", encoding="utf-8").write(s2)
    print("resolved %s: %d block(s) mapped" % (path, n))

def resolve_explicit(path, resolved_block):
    """將唯一衝突塊換成指定文字（gift185／tang171／173：成行重寫）。"""
    p = ROOT + "/" + path
    s = open(p, encoding="utf-8").read()
    blocks = BLOCK_RE.findall(s)
    assert len(blocks) == 1, path + ": 衝突塊 %d 個" % len(blocks)
    s2, n = BLOCK_RE.subn(resolved_block + "\n", s, count=1)
    assert n == 1
    open(p, "w", encoding="utf-8").write(s2)
    print("resolved %s: explicit block" % path)

def header_fix(path, pairs):
    p = ROOT + "/" + path
    s = open(p, encoding="utf-8").read()
    for a, b in pairs:
        assert s.count(a) == 1, "%s: %r 出現 %d 次" % (path, a, s.count(a))
        s = s.replace(a, b)
    open(p, "w", encoding="utf-8").write(s)
    print("header fixed %s" % path)

# ---- gift185：總行數一行 ----
resolve_explicit("tests/test_gift185_static.py",
    "ok('總行數 60609（v195 淨 +87，行號釘見 qa195/resync195_rebase.py）', html.count('\\\\n') == 60609)")
# ---- rom176：5 釘＋label 更新 ----
resolve_mapped("tests/test_rom176_static.py", {
    "L31533": "L31587", "L53050": "L53532", "L53415": "L53900",
    "L54447": "L55039", "L54541": "L55133",
})
# ---- tang171 ----
resolve_explicit("tests/test_tang171_static.py",
    "ok('零行數漂移：總行數 60609（v170 59173＋v149 ＋97＋v153 ＋71＋v172 ＋15＋v175 ＋78＋v181 ＋8＋v195 ＋87）', src.count('\\\\n') == 60609)\n"
    "ok('零行數漂移：openLoc DEF 行 55102（v195 ＋84：55018→55102，travel114 釘行）',\n"
    "   len(lines) >= 55102 and 'function openLoc(id, opts){' in lines[55101])")
# ---- tang173 ----
resolve_explicit("tests/test_tang173_static.py",
    "ok('零行數漂移：總行數 60609（v181 ＋8＋v195 ＋87）', src.count('\\\\n') == 60609)\n"
    "ok('零行數漂移：openLoc DEF 行 55102（v195 ＋84：55018→55102，travel114 釘行）',\n"
    "   len(lines) >= 55102 and 'function openLoc(id, opts){' in lines[55101])")
# ---- travel114：COUNT／FREE／DEF／WRAPPER 全部映射 ----
resolve_mapped("tests/test_travel114_static.py")

# ---- headers：總數 60490→60577 改做 60522→60609；DEF 54986→55070 改做 55018→55102 ----
for f in ("tests/test_gift185_static.py", "tests/test_tang171_static.py", "tests/test_tang173_static.py"):
    header_fix(f, [("總行數 60490→60577", "總行數 60522→60609")])
header_fix("tests/test_tang171_static.py", [("DEF 54986→55070", "DEF 55018→55102")])
header_fix("tests/test_tang173_static.py", [("DEF 54986→55070", "DEF 55018→55102")])
print("ALL RESOLVED")
