# v20a195 resync：index.html 淨 +87 行（見 qa195/resync195.py difflib 對位核實純漂移），三錨點 +4／+4／+7 重算。
# v20a125 TEXT125 靜態守門：StoryPlay 讀埋 `text` 單句 beats。
# v20a191 resync：index.html 淨 +47 行，三錨點 +2／+2／+9（currentLine 27711→27713、advance 27840→27842、familySafe 33534→33543），內容逐字核實純漂移。
# v20a191 rebase 上 main b3db32f resync：v189 淨 +34 行＋v191 淨 +47 行，三錨點 +2／+2／+9（currentLine 27736→27738、advance 27865→27867、familySafe 33559→33568），內容逐字核實純漂移。
# 覆蓋：① currentLine／advance 有 text fallback（行號寫死，rebase 要人手重對）
#       ② applyFamilySafeToNode 處理 b.text
#       ③ 五個 text-beats 節點表普查（beats／resultBeats 句數＝任務書普查數）
#       ④ 節點數據零郁（五表入面零 `lines:`／`line:` 鍵——修法行播放器，唔郁數據）
#       ⑤ 全庫零 beat 同時有 lines／line＋text（fallback 次序唔會改任何現行 beat 行為）
#       ⑥ SAVE key／softRev／產品 ?v= 不變
# 反證：(a) 抽走 currentLine／advance 任一 fallback → checker 必須報錯；
#       (b) WF3 少一句 text → 普查必須報錯；(c) 成個測試對 pristine main 跑必須 FAIL。
# v20a157 rebase 上 main 60b0a8f resync：main 淨刪行令三錨點漂移（currentLine 27826→27639、advance 27937→27752、familySafe 33582→33445；qa131/resync_rebase157.py difflib 對位核實內容逐字相同，純漂移；報錯字串行號一併更新）。
# v20a153 第三輪 rebase 上 main a500536（v149）resync：錨點 difflib 對位核實純漂移，行號按映射重寫（見 qa153/resync_rebase153c.py）。
# v20a172 rebase 上 main a500536（v149）resync：v149 淨 ＋97，三錨點一律 ＋13（currentLine 27657、advance 27770、familySafe 33463；qa172/resync172b.py difflib 對位核實）。
# v20a172 rebase 上 main e2add29（v174）resync：三錨點一律 ＋5（qa172/resync172c.py difflib 對位核實純漂移）。
# v20a175 rebase 上 main f09fa1b（v177）resync：index.html 淨 ＋78，三錨點一律 ＋10（currentLine 27677→27687、advance 27806→27816、familySafe 33499→33509；錨點逐行核實內容逐字相同，純漂移；報錯字串行號一併更新）。
# v20a181 resync：index.html 淨 ＋8，三錨點一律 ＋13（currentLine 27687→27700、advance 27816→27829、familySafe 33509→33522；difflib 對位核實內容逐字相同，純漂移；報錯字串行號一併更新）。
# v20a181 rebase 上 main 9640c6f（v183）resync：三錨點 ＋11／＋12（currentLine 27700→27711、advance 27829→27840、familySafe 33522→33534；difflib 對位核實內容逐字相同，純漂移；報錯字串行號一併更新）。
# 用法：python3 tests/test_text125_static.py [path-to-index.html]
# v20a182 resync：v182 淨 ＋17 行全部喺錨點之前，三錨點一律 ＋2（qa182/resync182.py difflib 對位核實內容逐字相同，純漂移；報錯字串行號一併更新）。
# v20a176 resync：NPCS ＋7 行（插入點 L6017 之後），三錨點一律 ＋7（qa176/resync176.py 逐行核實內容逐字相同，純漂移）。
# v20a189 resync：index.html 淨 ＋34 行（accel-link CSS ＋15 @~1831／day-res 92dvh media ＋10 @~3235／hint 刪除 −10 @37990／soft map 掣 ＋3／accel link push ＋12／day-res class ＋4；difflib 對位核實純漂移，見 qa189/resync189.py）。
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
    # v20a183 resync：C7 CSS ＋2／prefKind ＋1：27696→27698、27825→27827、33518→33521。
    # ① currentLine fallback（行號 27805，rebase 重對；v131 B2/B4 令行號由 27511 移位；v133 令行號由 27552 移位；v135 令行號由 27557 移位，CSS 淨 +1；v137 令行號由 27558 移位，CSS ＋23／地區名 HTML －10；v141 令行號由 27571 移位，淨 +60：CSS 段 ＋42／SVG defs ＋13／手帳 HTML 淨 ＋5；v143 令行號由 27631 移位，淨 +43：BOOK143 CSS 段；v136 rebase 上 v143，閘註解＋evalGate3Y 淨 +35；v142 ＋14：A2b CSS ＋4／A2a CSS ＋6／B1 註釋 ＋4；v145 ＋67：BOOK145 CSS 段；v146 rebase ＋10：MASK146 CSS 段 ＋8／modal 高帽註解 ＋2，B2 喺 40613 後唔影響呢行）
    if len(ls) < 27742 or FALLBACK not in ls[27741]:
        probs.append("currentLine 第 27742 行冇 text fallback")  # v157 resync：27805→27824（splice ＋24）；v149 rebase ＋13：27639→27652
    if not re.search(r"const lines = Array\.isArray\(b\.lines\) \? b\.lines : \(b\.line \? \[b\.line\] : "
                     + re.escape(FALLBACK) + r"\);", s):
        probs.append("currentLine fallback 唔係 lines＞line＞text 次序")
    # ① advance fallback（行號 27913，rebase 重對；v131 B2/B4 令行號由 27624 移位；v133 令行號由 27665 移位；v135 令行號由 27670 移位，CSS 淨 +1；v137 令行號由 27676 移位，CSS ＋23／地區名 HTML －10；v141 令行號由 27684 移位，淨 +60，同上；v143 令行號由 27744 移位，淨 +43，同上；v136 rebase 上 v143，淨 +35；v142 ＋14，同 currentLine 一樣；v145 ＋67，同上；v146 rebase ＋10，同 currentLine）
    if len(ls) < 27871 or FALLBACK not in ls[27870]:
        probs.append("advance 第 27871 行冇 text fallback")  # v157 resync：27913→27937（splice ＋24）；v149 rebase ＋13：27752→27765
    # ② applyFamilySafeToNode 處理 b.text（行號 33516–33518，rebase 重對；v131 B2/B4 令行號由 33222 移位；v133 令行號由 33263 移位；v135 令行號由 33268 移位，CSS 淨 +1；v137 令行號由 33269 移位，CSS ＋23／地區名 HTML －10；v141 令行號由 33282 移位，淨 +60，同上；v143 令行號由 33342 移位，淨 +43，同上；v136 rebase 上 v143，淨 +38，含 scrub 護欄 +3；v142 ＋16，實量；v145 ＋67，同上；v146 rebase ＋10，同 currentLine）
    if len(ls) < 33575 or 'if(typeof b.text === "string" && b.text){' not in ls[33574]:
        probs.append("applyFamilySafeToNode 第 33575 行冇 b.text 分支")  # v157 resync：33516→33582（splice ＋66）；v149 rebase ＋13：33445→33458
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
            ("CHOICE47_NODES", 8, 15), ("WF3_TALK_NODES", 43, 24),  # v157：CHOICE47 resultBeats 11→15（F4 3×3=9＋G4 2+4=6；beats 8 不變）
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
