# qa335/resync335b.py — v20a335 第二次漂移 resync（地點掣金提示）
# 背景：resync335.py 嗰陣只得第一層 drift（板短卡 teaser，淨 +7，47256→47263）。
# 實駕覆驗發現 A1 檢查嗰層係地點面板 #loc-acts 嘅 button.act（addLocGigActs 渲染，
# 唔經 gigBoardTeaserHtml），要再補一層：add() 加 extraHtml 第 6 參數（註解＋2 行，
# 舊 L42636）＋addLocGigActs 內 favor158Gold 計算（＋5 行，舊 L42408 之後）
# ＋CSS #loc-sheet.sheet .act .gold（＋2 行，舊 L2089 之後）。第二層淨 +9，總計淨 +16，
# 47256→47272；difflib 對位核實純漂移（10 處 hunk：3 處第一層＋7 處第二層）。
# 錨點 shift（舊＝v334 HEAD 行號）：
#   ≤2089 唔郁、2090–2937 ＋2、2938–18031 ＋4、18032–18050 ＋8、
#   18051–42408 ＋9、42409–42636 ＋14、≥42637 ＋16。
# 已 resync 過嗰 5 檔（而家係 +7 座標）用第二層 shift（m＝+7 座標行號）：
#   m ≤2089 唔郁、2090–42415 ＋2、42416–42643 ＋7、≥42644 ＋9。
# 用法：python3 qa335/resync335b.py（喺工作副本根目錄行；只改 8 檔測試，唔郁 index.html）
import difflib
import re
import subprocess

NL = chr(10)
NEW = open('index.html', encoding='utf-8').read().splitlines()
OLD = subprocess.check_output(['git', 'show', 'HEAD:index.html'], text=True).splitlines()

# ---- 1. difflib 核實純漂移：淨 +16，只得 10 處非 equal hunk ----
assert len(OLD) == 47256 and len(NEW) == 47272, (len(OLD), len(NEW))
sm = difflib.SequenceMatcher(a=OLD, b=NEW, autojunk=False)
non_eq = [(tag, i1, i2, j1, j2) for tag, i1, i2, j1, j2 in sm.get_opcodes() if tag != 'equal']
expected = [
    ('insert', 2089, 2089, 2089, 2091),    # CSS .act .gold ＋2＠舊 L2089（#loc-sheet.sheet .act .h）之後
    ('insert', 2937, 2937, 2939, 2941),    # CSS .gig-teaser .gold ＋2＠舊 L2937 之後（第一層）
    ('insert', 18031, 18031, 18035, 18039),  # teaser 內 favor158Html 計算 ＋4＠舊 L18031 之後（第一層）
    ('insert', 18050, 18050, 18058, 18059),  # template 內插 ${favor158Html} ＋1＠舊 L18050 之後（第一層）
    ('insert', 42408, 42408, 42417, 42422),  # addLocGigActs 內 favor158Gold 計算 ＋5＠舊 L42408（const gate）之後
    ('replace', 42410, 42411, 42424, 42425),  # 鎖定掣傳 favor158Gold（1→1）
    ('replace', 42418, 42419, 42432, 42433),  # 試鏡入口掣傳 favor158Gold（1→1）
    ('replace', 42420, 42421, 42434, 42435),  # 接通告掣傳 favor158Gold（1→1）
    ('replace', 42635, 42636, 42649, 42652),  # add() 簽名＋註解（1→3，＋2）
    ('replace', 42661, 42662, 42677, 42678),  # add() innerHTML 插 ${extraHtml||""}（1→1）
]
assert non_eq == expected, non_eq
assert OLD[2088].strip() == '}', OLD[2088]
assert 'overflow: hidden !important;' in OLD[2087], OLD[2087]
assert NEW[2089].startswith('/* v20a335'), NEW[2089]
assert NEW[2090] == '#loc-sheet.sheet .act .gold{ color:#8a5a00; font-weight:700; font-size:.66rem; line-height:1.4; margin-top:2px; }', NEW[2090]
assert OLD[42407].strip() == 'const gate=canAudition(gig);', OLD[42407]
assert NEW[42417].strip().startswith('/* v20a335'), NEW[42417]
assert NEW[42420].strip() == 'let favor158Gold = "";', NEW[42420]
assert 'favor158ChannelForGig(gig)' in NEW[42421], NEW[42421]
assert OLD[42635].strip() == 'const add=(title,hint,cost,fn,cls)=>{', OLD[42635]
assert NEW[42649].strip() == 'const add=(title,hint,cost,fn,cls,extraHtml)=>{', NEW[42649]
assert '${extraHtml||""}' in NEW[42677], NEW[42677]
print('drift check OK: 10 hunks only (first layer +7, second layer +9), net +16')


def shift(n):
    """舊行號（v334 HEAD）-> 最終行號。"""
    if n <= 2089:
        return n
    if n <= 2937:
        return n + 2
    if n <= 18031:
        return n + 4
    if n <= 18050:
        return n + 8
    if n <= 42408:
        return n + 9
    if n <= 42636:
        return n + 14
    return n + 16


def shift2(m):
    """+7 座標行號（resync335.py 之後）-> 最終行號。"""
    if m <= 2089:
        return m
    if m <= 42415:
        return m + 2
    if m <= 42643:
        return m + 7
    return m + 9


def resync_pairs(path, pairs, header):
    """pairs：(old, new, expected_count)；一次過用 combined regex 掃描，逐對斷言次數。"""
    text = open(path, encoding='utf-8').read()
    pats = sorted(((o, n, c) for o, n, c in pairs), key=lambda t: -len(t[0]))
    rx = re.compile('|'.join(re.escape(o) for o, _, _ in pats))
    counts = {o: 0 for o, _, _ in pats}
    mapping = {o: n for o, n, _ in pats}

    def repl(m):
        counts[m.group(0)] += 1
        return mapping[m.group(0)]
    out = rx.sub(repl, text)
    for o, n, c in pats:
        assert counts[o] == c, (path, o, counts[o], c)
    open(path, 'w', encoding='utf-8').write(header + NL + out)
    print('resynced %s (%d pairs)' % (path, len(pats)))


HDR = '# v20a335 resync335b：第二層 drift（地點掣金提示：CSS ＋2＠舊 L2089 後＋favor158Gold 計算 ＋5＠舊 L42408 後＋add() 簽名註解 ＋2＠舊 L42636；總計淨 +16，47256→47272；錨點按段 shift，內容逐行核實純漂移，見 qa335/resync335b.py）。'
HDR2 = '# v20a335 resync335b：第二層 drift（+7 座標→最終：≤2089 唔郁、2090–42415 ＋2、42416–42643 ＋7、≥42644 ＋9；總計淨 +16，47256→47272；內容逐行核實純漂移，見 qa335/resync335b.py）。'

# ---- A. 未 resync 嗰 3 檔（舊＝v334 座標）----
# rom159：6 個釘行＋全佳行按段 shift（8241 ＋4；10699／14774 ＋4；25424／26173／26272／25452 ＋9）；
# ok() 名入面嘅 L 號係歷史標籤，唔郁。內容逐字核實。
resync_pairs('tests/test_rom159_static.py', [
    ('line_has(25424,', 'line_has(25433,', 1),
    ('line_has(8241,', 'line_has(8245,', 1),
    ('line_has(26272,', 'line_has(26281,', 1),
    ('line_has(10699,', 'line_has(10703,', 1),
    ('line_has(14774,', 'line_has(14778,', 1),
    ('line_has(26173,', 'line_has(26182,', 1),
    ('idx_lines[25452 - 1]', 'idx_lines[25461 - 1]', 1),
], HDR)
assert 'v20a159 ROM159 Phase 1' in NEW[25432], NEW[25432]
assert 'rom159GainAllowed(k)' in NEW[8244], NEW[8244]
assert 'COMMIT48_NODES.CMT_lan_commit' in NEW[26280], NEW[26280]
assert 'rom159PrepareNode(node)' in NEW[10702], NEW[10702]
assert 'rom159ApplyGiftOverrides()' in NEW[14777], NEW[14777]
assert 'function rom159SoMeetGate' in NEW[26181], NEW[26181]
assert '查實' in NEW[25460], NEW[25460]
print('rom159 content check OK: 7 anchors')

# tang152：3 個 0-based 錨（9282／14699／14826，各 ＋4 → 9286／14703／14830）
resync_pairs('tests/test_tang152_static.py', [
    ('lines()[9282]', 'lines()[9286]', 1),
    ('lines()[14699]', 'lines()[14703]', 1),
    ('lines()[14826]', 'lines()[14830]', 1),
], HDR)
assert NEW[9286].startswith('  const HELD = ["R_tang_push1","R_tang_push2","R_tang_crisis"];'), NEW[9286]
assert NEW[14703].startswith('function normaliseTangStub152(pack){'), NEW[14703]
assert NEW[14830].strip().startswith('try{ normaliseTangStub152(rom2);'), NEW[14830]
print('tang152 content check OK: 3 anchors')

# text125：3 個錨點各 ＋4（currentLine 11279→11283、advance 11421→11425、applyFamilySafe 16341→16345）；
# 報錯字串行號一併更新。
resync_pairs('tests/test_text125_static.py', [
    ('len(ls) < 11279', 'len(ls) < 11283', 1),
    ('ls[11278]', 'ls[11282]', 1),
    ('currentLine 第 11279 行', 'currentLine 第 11283 行', 1),
    ('len(ls) < 11421', 'len(ls) < 11425', 1),
    ('ls[11420]', 'ls[11424]', 1),
    ('advance 第 11421 行', 'advance 第 11425 行', 1),
    ('len(ls) < 16341', 'len(ls) < 16345', 1),
    ('ls[16340]', 'ls[16344]', 1),
    ('applyFamilySafeToNode 第 16341 行', 'applyFamilySafeToNode 第 16345 行', 1),
], HDR)
FALLBACK = '(typeof b.text === "string" && b.text ? [b.text] : [])'
assert FALLBACK in NEW[11282], NEW[11282]
assert FALLBACK in NEW[11424], NEW[11424]
assert 'if(typeof b.text === "string" && b.text){' in NEW[16344], NEW[16344]
print('text125 content check OK: 3 anchors')

# ---- B. 已 resync 過嗰 5 檔（+7 座標 → 最終）----
# gift185：總行數 47263→47272（名＋值）
resync_pairs('tests/test_gift185_static.py', [
    ('總行數 47263（', '總行數 47272（', 1),
    ('＋v333 +7＋v335 +7）', '＋v333 +7＋v335 +7＋v335b +9）', 1),
    ('== 47263', '== 47272', 1),
], HDR2)

# tang171／tang173：總行數＋openLoc DEF 42485→42492（42485 喺 42416–42643 段，＋7）
for f in ('tests/test_tang171_static.py', 'tests/test_tang173_static.py'):
    resync_pairs(f, [
        ('總行數 47263（', '總行數 47272（', 1),
        ('＋v333 +7＋v335 +7）', '＋v333 +7＋v335 +7＋v335b +9）', 1),
        ('== 47263', '== 47272', 1),
        ('openLoc DEF 行 42485（', 'openLoc DEF 行 42492（', 1),
        ('＋v333 +7＋v335 +7，travel114 釘行）', '＋v333 +7＋v335 +7＋v335b +9，travel114 釘行）', 1),
        ('len(lines) >= 42485', 'len(lines) >= 42492', 1),
        ('lines[42484]', 'lines[42491]', 1),
    ], HDR2)

# tang173：L5089 錨（實查 lines[5089]，+7 座標 L5090 → 最終 L5092，＋2）
resync_pairs('tests/test_tang173_static.py', [
    ('lines[5089]', 'lines[5091]', 8),
    ('len(lines) >= 5090', 'len(lines) >= 5092', 1),
], HDR2)

# rom176：6 個釘行（6323／14774／40717／41067／42370 ＋2；42526 ＋7）
resync_pairs('tests/test_rom176_static.py', [
    ('line(6323)', 'line(6325)', 1),
    ('line(14774)', 'line(14776)', 2),
    ('line(40717)', 'line(40719)', 1),
    ('line(41067)', 'line(41069)', 1),
    ('line(42370)', 'line(42372)', 1),
    ('line(42526)', 'line(42533)', 1),
], HDR2)
assert NEW[6324].startswith('  lan:{ id:"lan", name:"藍若曦"'), NEW[6324]
assert 'GIFT_REACT = giftReact' in NEW[14775] and 'rom176ApplyGiftOverrides()' in NEW[14775], NEW[14775]
assert NEW[40718].startswith('/* ===== v20a176 ROM176'), NEW[40718]
assert NEW[41068].startswith('function rom176ApplyGiftOverrides()'), NEW[41068]
assert NEW[42371].startswith('function addLocTalkGiftActs(add, L, npcId)'), NEW[42371]
assert 'rom176TryIntercept(id)' in NEW[42532], NEW[42532]
print('rom176 content check OK: 6 anchors')


# travel114：COUNT／FREE 集合按第二層 shift＋DEF_LINE 42485→42492＋WRAPPER_LINE 29090→29092
def resync_travel114():
    path = 'tests/test_travel114_static.py'
    lines = open(path, encoding='utf-8').read().splitlines()
    in_set = None
    changed = 0
    count_n = 0
    free_n = 0
    new_count = []
    new_free = []
    for i, ln in enumerate(lines):
        if ln.startswith('COUNT_LINES = {'):
            in_set = 'COUNT'
            continue
        if ln.startswith('FREE_LINES = {'):
            in_set = 'FREE'
            continue
        if in_set and ln == '}':
            in_set = None
            continue
        if in_set:
            m = re.match(r'^(    )([0-9]+)(,.*)$', ln)
            if m:
                old_n = int(m.group(2))
                new_n = shift2(old_n)
                if new_n != old_n:
                    lines[i] = m.group(1) + str(new_n) + m.group(3)
                    changed += 1
                    if in_set == 'COUNT':
                        count_n += 1
                    else:
                        free_n += 1
                if in_set == 'COUNT':
                    new_count.append(new_n)
                else:
                    new_free.append(new_n)
    def_hit = [i for i, ln in enumerate(lines) if ln.startswith('DEF_LINE = 42485')]
    assert len(def_hit) == 1, def_hit
    lines[def_hit[0]] = 'DEF_LINE = 42492      # function openLoc(id, opts){'
    wr_hit = [i for i, ln in enumerate(lines) if ln.startswith('WRAPPER_LINE = 29090')]
    assert len(wr_hit) == 1, wr_hit
    lines[wr_hit[0]] = 'WRAPPER_LINE = 29092  # window.__phase2.openLoc：轉發 opts'
    # 預期：第二層 shift 郁到嘅錨點（≤2089 者唔郁；其餘 ＋2，DEF 嗰個 ＋7 唔喺集合入面）
    for n in new_count:
        assert 'openLoc(' in NEW[n - 1], (n, NEW[n - 1])
        assert not any(f in NEW[n - 1] for f in ('travelFree:true', 'encDone:true', 'forceRestore:true', 'wf4Done:true')), (n, NEW[n - 1])
    for n in new_free:
        assert 'openLoc(' in NEW[n - 1], (n, NEW[n - 1])
        assert any(f in NEW[n - 1] for f in ('travelFree:true', 'encDone:true', 'forceRestore:true', 'wf4Done:true')), (n, NEW[n - 1])
    assert NEW[42491] == 'function openLoc(id, opts){', NEW[42491]
    assert 'openLoc: function(id, opts){ openLoc(id, opts); }' in NEW[29091], NEW[29091]
    open(path, 'w', encoding='utf-8').write(
        '# v20a335 resync335b：第二層 drift（+7 座標→最終：≤2089 唔郁、2090–42415 ＋2、42416–42643 ＋7、≥42644 ＋9；總計淨 +16，47256→47272；DEF 42485→42492＋WRAPPER 29090→29092，內容逐行核實純漂移，見 qa335/resync335b.py）。' + NL + NL.join(lines) + NL)
    print('resynced tests/test_travel114_static.py (%d set shifts)' % changed)


resync_travel114()
print('ALL RESYNC DONE')
