# v20a125 TEXT125 靜態守門：StoryPlay 讀埋 `text` 單句 beats。
# 覆蓋：① currentLine／advance 有 text fallback（行號寫死，rebase 要人手重對）
#       ② applyFamilySafeToNode 處理 b.text
#       ③ 五個 text-beats 節點表普查（beats／resultBeats 句數＝任務書普查數）
#       ④ 節點數據零郁（五表入面零 `lines:`／`line:` 鍵——修法行播放器，唔郁數據）
#       ⑤ 全庫零 beat 同時有 lines／line＋text（fallback 次序唔會改任何現行 beat 行為）
#       ⑥ SAVE key／softRev／產品 ?v= 不變
# 反證：(a) 抽走 currentLine／advance 任一 fallback → checker 必須報錯；
#       (b) WF3 少一句 text → 普查必須報錯；(c) 成個測試對 pristine main 跑必須 FAIL。
# 用法：python3 tests/test_text125_static.py [path-to-index.html]
import re, sys, os

HERE = os.path.dirname(os.path.abspath(__file__))
IDX = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else os.path.join(HERE, "..", "index.html")
with open(IDX, encoding="utf-8") as f:
    src = f.read()
lines = src.split("\n")

fails = []
def ck(name, cond):
    print(("PASS " if cond else "FAIL ") + name)
    if not cond: fails.append(name)
def info(msg): print("INFO " + msg)

FALLBACK = '(typeof b.text === "string" && b.text ? [b.text] : [])'

def check(s):
    """回傳問題清單（空＝全過）。供反證餵變異輸入。"""
    probs = []
    ls = s.split("\n")
    # ① currentLine fallback（行號 27610，rebase 重對；v131 B2/B4 令行號由 27511 移位；v133 令行號由 27552 移位；v135 令行號由 27557 移位，CSS 淨 +1；v137 令行號由 27558 移位，CSS ＋23／地區名 HTML －10；v141 令行號由 27571 移位，淨 +60：CSS 段 ＋42／SVG defs ＋13／手帳 HTML 淨 ＋5；v143 令行號由 27631 移位，淨 +43：BOOK143 CSS 段；v136 rebase 上 v143，閘註解＋evalGate3Y 淨 +35；v142 ＋14：A2b CSS ＋4／A2a CSS ＋6／B1 註釋 ＋4；v145 ＋67：BOOK145 CSS 段；v146 rebase ＋10：MASK146 CSS 段 ＋8／modal 高帽註解 ＋2，B2 喺 40613 後唔影響呢行；v155 rebase ＋17：B1 註解 ＋6／B2 註解 ＋7／B3 ＋4；v161 rebase 上 bf612bc ＋14）
    if len(ls) < 27610 or FALLBACK not in ls[27609]:
        probs.append("currentLine 第 27610 行冇 text fallback")
    if not re.search(r"const lines = Array\.isArray\(b\.lines\) \? b\.lines : \(b\.line \? \[b\.line\] : "
                     + re.escape(FALLBACK) + r"\);", s):
        probs.append("currentLine fallback 唔係 lines＞line＞text 次序")
    # ① advance fallback（行號 27723，rebase 重對；v131 B2/B4 令行號由 27624 移位；v133 令行號由 27665 移位；v135 令行號由 27670 移位，CSS 淨 +1；v137 令行號由 27671 移位，CSS ＋23／地區名 HTML －10；v141 令行號由 27684 移位，淨 +60，同上；v143 令行號由 27744 移位，淨 +43，同上；v136 rebase 上 v143，淨 +35；v142 ＋14，同 currentLine 一樣；v145 ＋67，同上；v146 rebase ＋10，同 currentLine；v156 ＋15：EMPTY156 CSS 段（33516 嗰組再 ＋19 PICKER156；v155 rebase ＋17，同 currentLine；v161 rebase 上 bf612bc ＋14）
    if len(ls) < 27723 or FALLBACK not in ls[27722]:
        probs.append("advance 第 27723 行冇 text fallback")
    # ② applyFamilySafeToNode 處理 b.text（行號 33374–33583，rebase 重對；v131 B2/B4 令行號由 33222 移位；v133 令行號由 33263 移位；v135 令行號由 33268 移位，CSS 淨 +1；v137 令行號由 33269 移位，CSS ＋23／地區名 HTML －10；v141 令行號由 33282 移位，淨 +60，同上；v143 令行號由 33342 移位，淨 +43，同上；v136 rebase 上 v143，淨 +38，含 scrub 護欄 +3；v142 ＋16，實量；v145 ＋67，同上；v146 rebase ＋10，同 currentLine；v155 rebase ＋17，同 currentLine；v161 rebase 上 bf612bc ＋14）
    if len(ls) < 33376 or 'if(typeof b.text === "string" && b.text){' not in ls[33373]:
        probs.append("applyFamilySafeToNode 第 33374 行冇 b.text 分支")
    if 'b.text.replace(/臨時演員蹲在路邊抽煙/g' not in s:
        probs.append("applyFamilySafeToNode b.text 替換唔齊")
    # ③ 五表普查
    for name, got, want in census(s):
        if got != want:
            probs.append(f"{name} {got}≠{want}")
    # ④ 五表零 lines／line 鍵
    for tname, seg in table_segments(s):
        if re.search(r"\blines\s*:", seg) or re.search(r"\bline\s*:", seg):
            probs.append(f"{tname} 有 lines／line 鍵（數據郁咗）")
    # ⑤ 全庫零 beat 同時有 lines／line＋text（逐行：beat 係一行一個 object literal）
    for i, l in enumerate(ls, 1):
        if re.search(r"\blines\s*:", l) and re.search(r"\btext\s*:", l):
            probs.append(f"第 {i} 行同時有 lines＋text")
        if re.search(r"\bline\s*:", l) and re.search(r"\btext\s*:", l):
            probs.append(f"第 {i} 行同時有 line＋text")
    return probs

def table_segments(s):
    """五個 text-beats 節點表嘅原文段（marker 定位，唔靠行號）。"""
    def seg(start, end):
        a = s.find(start)
        b = s.find(end, a) if a >= 0 else -1
        return s[a:b] if a >= 0 and b > a else ""
    return [
        ("CHOICE47_NODES", seg("const CHOICE47_NODES = {", "const CHOICE47_DEFS")),
        ("WF3_TALK_NODES", seg("const WF3_TALK_NODES = {", "const WF3_TALK_DEFS")),
        ("COMMIT48_NODES", seg("const COMMIT48_NODES = {", "const COMMIT48_DEFS")),
        ("WF4_FEN_INTRO_NODE", seg("const WF4_FEN_INTRO_NODE = {", "function wf4FenIntroDone")),
        ("wf4FenFarewellNode", seg("function wf4FenFarewellNode(arm){", "\nfunction wf4PresentFenFarewell")),
    ]

def count_text(seg, kind):
    """kind: 'beats'＝beats:[ 到下一 choices:[ 之間嘅 text: 數；
       'result'＝其餘 text: 數（resultBeats 內）。"""
    beats = len(re.findall(r"\btext\s*:", seg))
    m = re.search(r"\bbeats\s*:\s*\[", seg)
    c = re.search(r"\bchoices\s*:\s*\[", seg)
    bcount = 0
    if m and c and c.start() > m.start():
        bcount = len(re.findall(r"\btext\s*:", seg[m.start():c.start()]))
    return bcount if kind == "beats" else beats - bcount

def census(s):
    """(名，實數，預期數)。farewell 係動態建 beats：literal 4＋push 8＝12 行 code，
       運行時 8–11 句（conditional 0–2＋variant 1＋trailing 3）。"""
    out = []
    segs = dict(table_segments(s))
    for tname, want_b, want_r in [
            ("CHOICE47_NODES", 8, 11), ("WF3_TALK_NODES", 43, 24),
            ("COMMIT48_NODES", 8, 8), ("WF4_FEN_INTRO_NODE", 6, 4)]:
        seg = segs[tname]
        # 逐節點計（beats 之後先至係 choices；全表第一個 beats:[ 到第一個 choices:[ 只覆蓋首節點）
        total_b, total_r = 0, 0
        for chunk in re.split(r"\n  \w+: \{", seg):
            if "beats" not in chunk: continue
            total_b += count_text(chunk, "beats")
            total_r += count_text(chunk, "result")
        out.append((tname + " beats", total_b, want_b))
        out.append((tname + " resultBeats", total_r, want_r))
    fw = segs["wf4FenFarewellNode"]
    lit = fw.split("beats.push")[0]
    out.append(("wf4Farewell literal beats", len(re.findall(r"\btext\s*:", lit)), 4))
    out.append(("wf4Farewell beats.push", sum(1 for l in fw.split("\n")
               if "beats.push" in l and re.search(r"\btext\s*:", l)), 8))
    out.append(("wf4Farewell resultBeats", len(re.findall(r"\btext\s*:", fw))
               - len(re.findall(r"\btext\s*:", lit))
               - sum(1 for l in fw.split("\n") if "beats.push" in l and re.search(r"\btext\s*:", l)), 3))
    return out

# ---------- 正本檢查 ----------
probs = check(src)
ck("TEXT125 靜態檢查全過（fallback＋普查＋數據零郁＋零並存）", not probs)
if probs: info("問題：" + "；".join(probs[:12]))
for name, got, want in census(src):
    ck(f"普查 {name}＝{want}", got == want)

# ---------- ⑥ 基線不變 ----------
ck("SAVE key 不變", "starVolunteer_map_v19w" in src)
ck("softRev 不變", "s107" in src)
ck("產品 ?v= 不變", "v20a10" in src)
ck("修法只郁播放器 3 處（TEXT125 標記恰好 3 個：currentLine／advance／familySafe）",
   src.count("TEXT125") == 3)

# ---------- 反證（in-memory 變異） ----------
mut = src.replace(
    'const lines = Array.isArray(b.lines) ? b.lines : (b.line ? [b.line] : (typeof b.text === "string" && b.text ? [b.text] : []));',
    'const lines = Array.isArray(b.lines) ? b.lines : (b.line ? [b.line] : []);', 1)
ck("反證：抽走 currentLine fallback → checker 必須報錯",
   len(check(mut)) >= 1 and any("currentLine" in p for p in check(mut)))
mut_adv = src.replace(
    '      const lines = Array.isArray(b.lines) ? b.lines : (b.line ? [b.line] : (typeof b.text === "string" && b.text ? [b.text] : []));',
    '      const lines = Array.isArray(b.lines) ? b.lines : [];', 1)
ck("反證：抽走 advance fallback → checker 必須報錯",
   len(check(mut_adv)) >= 1 and any("advance" in p for p in check(mut_adv)))
# WF3 少一句 text（刪 W3_lu_pa 第一句）→ 普查報錯
mut3 = src.replace(
    '{ speakerId:"", speaker:"場務姐姐", kind:"npc", text:"咦——你咪係……嗰晚嗰個？嗰晚係你頂嗰？" },\n', '', 1)
p3 = check(mut3)
ck("反證：WF3 少一句 text → 普查必須報錯",
   len(p3) >= 1 and any("WF3" in p for p in p3))

print("RESULT " + ("FAIL (" + str(len(fails)) + ")" if fails else "PASS"))
sys.exit(1 if fails else 0)
