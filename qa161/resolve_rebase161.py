#!/usr/bin/env python3
# qa161/resolve_rebase161.py — 解 v20a161 rebase 上 origin/main (9346a8e) 嗰陣
# test_text125_static.py / test_travel114_static.py 兩個衝突。
# 兩個衝突都係純行號漂移：v161 喺舊行 4771 之後淨插入 14 行 CSS，
# 喺三個 text125 釘行（27815／27928／33550，HEAD 值）同全部 travel114 釘行之前，
# 所以正確合併值 = HEAD 值 + 14。index.html 本身 auto-merge 乾淨，證明修法冇重疊。
# 用法：python3 qa161/resolve_rebase161.py（在 ~/workspace/linji-work161 執行）
import re, sys

def split_hunks(path):
    """回傳 (前綴, [(head_side, v161_side)], 後綴)。假設每個衝突得一個 hunk。"""
    txt = open(path, encoding="utf-8").read()
    parts = re.split(r"^<<<<<<< HEAD\n", txt, flags=re.M)
    assert len(parts) == 2, path
    pre, rest = parts
    mid, post = re.split(r"^>>>>>>> a1de8b6.*\n", rest, flags=re.M)
    head_side, v161_side = re.split(r"^=======$\n", mid, flags=re.M)
    return pre, [(head_side, v161_side)], post

def resolve_text125():
    path = "tests/test_text125_static.py"
    pre, hunks, post = split_hunks(path)
    head = hunks[0][0]
    # 釘行：HEAD 值 + 14（27815→27829、27928→27942、33550→33564／33552→33566）
    out = head
    out = out.replace("行號 27815", "行號 27829")
    out = out.replace("len(ls) < 27815", "len(ls) < 27829")
    out = out.replace("ls[27814]", "ls[27828]")
    out = out.replace("第 27800 行", "第 27829 行")
    out = out.replace("行號 27928", "行號 27942")
    out = out.replace("len(ls) < 27928", "len(ls) < 27942")
    out = out.replace("ls[27927]", "ls[27941]")
    out = out.replace("第 27913 行", "第 27942 行")
    out = out.replace("行號 33550–33552", "行號 33564–33566")
    out = out.replace("len(ls) < 33552", "len(ls) < 33566")
    out = out.replace("ls[33549]", "ls[33563]")
    out = out.replace("第 33550 行", "第 33564 行")
    # 註解補 v161 記錄（每條釘行註解尾加一句）
    out = out.replace("B2 喺 40613 後唔影響呢行）",
                      "B2 喺 40613 後唔影響呢行；v161 rebase 上 9346a8e ＋14：START161 CSS 段）")
    out = out.replace("（33516 嗰組再 ＋19 PICKER156）",
                      "（33516 嗰組再 ＋19 PICKER156）；v161 rebase 上 9346a8e ＋14，同 currentLine）")
    out = out.replace("v146 rebase ＋10，同 currentLine）",
                      "v146 rebase ＋10，同 currentLine；v156 ＋34（EMPTY156 ＋15／PICKER156 ＋19）；v161 rebase 上 9346a8e ＋14）")
    assert "<<<<<<<" not in out and "=======" not in out, "markers left"
    # 驗算：三個新釘行喺新 index.html 嗰度內容要啱
    lines = open("index.html", encoding="utf-8").read().split("\n")
    assert 'typeof b.text === "string" && b.text ? [b.text] : []' in lines[27828], "currentLine anchor"
    assert 'typeof b.text === "string" && b.text ? [b.text] : []' in lines[27941], "advance anchor"
    assert 'if(typeof b.text === "string" && b.text){' in lines[33563], "applyFamilySafe anchor"
    open(path, "w", encoding="utf-8").write(pre + out + post)
    print("text125 resolved: 27829 / 27942 / 33564-33566, anchors verified in index.html")

def resolve_travel114():
    path = "tests/test_travel114_static.py"
    pre, hunks, post = split_hunks(path)
    head = hunks[0][0]
    lines = head.split("\n")
    out_lines = []
    in_count = in_free = False
    for l in lines:
        if l.startswith("COUNT_LINES = {"):
            in_count = True
        elif l.startswith("FREE_LINES = {"):
            in_free = True
        elif l.strip() == "}" and (in_count or in_free):
            in_count = in_free = False
        if (in_count or in_free) and re.match(r"\s*\d+,", l):
            l = re.sub(r"\d+", lambda m: str(int(m.group(0)) + 14), l, count=1)
        if l.startswith("DEF_LINE = "):
            l = re.sub(r"\d+", lambda m: str(int(m.group(0)) + 14), l, count=1)
        if l.startswith("WRAPPER_LINE = "):
            l = re.sub(r"\d+", lambda m: str(int(m.group(0)) + 14), l, count=1)
        out_lines.append(l)
    out = "\n".join(out_lines)
    # 註解補 v161 resync 記錄（放喺 v156 嗰行之後）
    v161_note = (
        "# v20a161 rebase 上 9346a8e resync：START161 淨 +14 行（舊行 4771 之後插入），\n"
        "# 行號 ≥4772 者 +14；qa161/resync161.py 方法核實純漂移（COUNT 13／FREE 27 不變，\n"
        "# DEF 53601→53615、WRAPPER 44205→44219）。"
    )
    anchor = "# v20a156 EMPTY156 resync："
    i = out.index(anchor)
    j = out.index("\n", i) + 1
    out = out[:j] + v161_note + "\n" + out[j:]
    assert "<<<<<<<" not in out and "=======" not in out, "markers left"
    # 驗算：DEF／WRAPPER 喺新 index.html 嗰度內容要啱
    idx = open("index.html", encoding="utf-8").read().split("\n")
    assert idx[53614].strip().startswith("function openLoc("), "DEF anchor: %r" % idx[53614][:80]
    assert "__phase2.openLoc" in idx[44218] or "openLoc" in idx[44218], "WRAPPER anchor: %r" % idx[44218][:80]
    open(path, "w", encoding="utf-8").write(pre + out + post)
    print("travel114 resolved: DEF 53615 / WRAPPER 44219, anchors verified in index.html")

resolve_text125()
resolve_travel114()
print("OK — both files resolved, no conflict markers")
