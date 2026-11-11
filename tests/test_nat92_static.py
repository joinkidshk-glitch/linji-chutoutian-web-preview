#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""v20a92 NAT92 靜態測試：通告板分布自然化——
(A) 錯峰決定性：nat92Hash 用 FNV-1a/Math.imul；NAT92 實作碼冇 Math.random( / Date.now(（存檔/重載穩定）。
(B) 接線：gigsForLocSeasonBoard 有 posted 判準＋mergeNat92Gigs＋保底；openLoc 清 board 有 posted 判準；tipGig 有 posted 判準。
(C) 守衛常量：SPREAD 40、PULL_MAX 24、PULL_OPEN_MAX 30；年初開窗豁免；入門/常駐豁免。
(D) 紅線：SAVE key / softRev / ?v= 不變；mergeNat92Gigs 走 normalizeGigRecord；NOTES_V20A92 存在；
    NAT92_GIGS 玩家面文案冇禁用詞（真藝名/「聲量」）。
(E) 入門補位：紅棉/灣仔兩張 NAT92 入門 gig 字面存在（entryTier + boardPriority high）。
用法：python3 tests/test_nat92_static.py [path-to-index.html]
"""
import re
import sys
import pathlib

base = pathlib.Path(__file__).resolve().parent.parent
idx = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else base / "index.html"
src = idx.read_text(encoding="utf-8")
fails = []


def ok(name, cond):
    print(("PASS " if cond else "FAIL ") + name)
    if not cond:
        fails.append(name)


def extract_fn(name):
    i = src.find("function " + name + "(")
    if i < 0:
        return ""
    j = src.find("{", i)
    depth = 0
    for k in range(j, len(src)):
        if src[k] == "{":
            depth += 1
        elif src[k] == "}":
            depth -= 1
            if depth == 0:
                return src[i:k + 1]
    return ""


m = re.search(r"/\* =+ v20a92[^\n]*\n(.*?)\nfunction mergeNat92Gigs", src, re.S)
ok("A0 NAT92 區塊存在", bool(m))
blk = m.group(1) if m else ""
# 只睇實作碼：剝走 /* */ 註解先檢查隨機源
blk_code = re.sub(r"/\*.*?\*/", "", blk, flags=re.S)
ok("A1 nat92Hash 行 FNV-1a（Math.imul）", "Math.imul" in blk and "function nat92Hash" in blk)
ok("A2 NAT92 實作碼冇 Math.random(", "Math.random(" not in blk_code)
ok("A3 NAT92 實作碼冇 Date.now(", "Date.now(" not in blk_code)
ok("A4 gigBoardPosted92 存在", "function gigBoardPosted92" in blk)
ok("A5 錯峰資格只限 pack 年編碼/g36 前綴", "gig_\\d{4}_" in blk and "g36_" in blk)

btxt = extract_fn("gigsForLocSeasonBoard")
ok("B1 gigsForLocSeasonBoard 調 mergeNat92Gigs", "mergeNat92Gigs()" in btxt)
ok("B2 board pool 有 posted 判準（gigBoardPosted92）", "gigBoardPosted92" in btxt)
ok("B3 board 保底存在（best92）", "best92" in btxt)
ok("B4 openLoc 清 S.board 有 posted 判準", "gigBoardPosted92" in extract_fn("openLoc"))
ok("B5 tipGig 有 posted 判準", "gigBoardPosted92" in extract_fn("tipGig"))

ok("C1 SPREAD=40", "const NAT92_SPREAD = 40;" in blk)
ok("C2 PULL_MAX=24", "const NAT92_PULL_MAX = 24;" in blk)
ok("C3 PULL_OPEN_MAX=30", "const NAT92_PULL_OPEN_MAX = 30;" in blk)
ok("C4 年初開窗豁免（iv[0] <= yearStart）", "iv[0] <= yearStart" in blk)
ok("C5 入門/常駐豁免（entryTier/softBridge）", "g.entryTier" in blk and "g.softBridge" in blk)

ok("D1 SAVE key 不變", "starVolunteer_map_v19w" in src)
ok("D2 softRev 不變", '"s107"' in src or "'s107'" in src)
ok("D3 ?v= 不變", "v20a10" in src)
mg = extract_fn("mergeNat92Gigs")
ok("D4 mergeNat92Gigs 經 normalizeGigRecord 入池", "normalizeGigRecord(JSON.parse(JSON.stringify(raw)))" in mg)
notes = list(base.glob("NOTES_V20A92_*.md"))
ok("D5 NOTES_V20A92 存在", len(notes) >= 1)
nat92_txt = re.search(r"const NAT92_GIGS = \[(.*?)\n\];", src, re.S)
ntxt = nat92_txt.group(1) if nat92_txt else ""
for banned in ["成龍", "周潤發", "劉德華", "張國榮", "梅艷芳", "林青霞", "王祖賢", "周星馳", "聲量"]:
    ok("D6 NAT92 文案冇禁用詞「" + banned + "」", banned not in ntxt)

ok("E1 紅棉入門 gig 存在", "gig_1988_nat92_cotton_entry" in src and '"film_cotton"' in ntxt)
ok("E2 灣仔入門 gig 存在", "gig_1988_nat92_wanchai_entry" in src and '"rec_wanchai"' in ntxt)
ok("E3 入門 gig 帶 entryTier + boardPriority high", ntxt.count("entryTier:true") >= 2 and ntxt.count('boardPriority:"high"') >= 2)

print("FAILURES: " + " | ".join(fails) if fails else "ALL PASS")
sys.exit(1 if fails else 0)
