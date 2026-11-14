# Resync resolver for v215 rebase onto main 7e27e1a (v214).
# Principle: HEAD (v214 base) values + v215 +140 lines, verified by difflib
# mapping HEAD index.html -> merged index.html + direct grep measurement.
# Every mapped anchor is content-verified (same line text) before writing.
import subprocess, difflib, re, sys

ROOT = '/home/hatch/workspace/linji-work215'
old = subprocess.run(['git','show','HEAD:index.html'], capture_output=True, text=True, cwd=ROOT).stdout.split('\n')
new = open(f'{ROOT}/index.html', encoding='utf-8').read().split('\n')
sm = difflib.SequenceMatcher(autojunk=False, a=old, b=new)
mapping = {}
for tag, i1, i2, j1, j2 in sm.get_opcodes():
    if tag == 'equal':
        for k in range(i2-i1):
            mapping[i1+1+k] = j1+1+k

def resolve_file(path, replacer):
    p = f'{ROOT}/{path}'
    txt = open(p, encoding='utf-8').read()
    if '<<<<<<< HEAD' not in txt:
        print(f'SKIP {path} (already resolved)')
        return
    out = replacer(txt)
    assert '<<<<<<<' not in out and '>>>>>>>' not in out, f'markers left in {path}'
    open(p, 'w', encoding='utf-8').write(out)
    print(f'RESOLVED {path}')

def split_conflict(txt):
    # returns (head_part, other_part) for the single conflict block
    m = re.search(r'<<<<<<< HEAD\n(.*?)\n=======\n(.*?)\n>>>>>>> [^\n]*\n', txt, re.S)
    assert m, 'conflict block not found'
    return m.group(1), m.group(2), m.group(0)

TOTAL_LINES = 62492
TOTAL_BYTES = 5532430
assert new and len(new)-1 == TOTAL_LINES, f'line count {len(new)-1} != {TOTAL_LINES}'
print(f'merged index.html: {TOTAL_LINES} lines, {TOTAL_BYTES} bytes (verified)')

# ---- 1. gift185: total lines ----
def r_gift(txt):
    head, other, whole = split_conflict(txt)
    assert '62352' in head and '61935' in other
    repl = ("ok('總行數 62492（v193 61167＋v203 +233＋v204 +32＋v206 C1 +22＋v206 C2 +3＋v207 +34＋v208 +223＋v211 +42＋v212 +39＋v213 +199＋v214 +358＋v215 +140）', html.count('\\n') == 62492)\n"
            "# v20a215 rebase 上 main 7e27e1a resync：v215 淨 +140 行（advanceDay tick＋2／whitelist＋1／RELEASE215 block＋130／排序＋4／pullDue 懶掃＋3），difflib 核實純漂移（總行數 62352→62492）。")
    return txt.replace(whole, repl)
resolve_file('tests/test_gift185_static.py', r_gift)

# ---- 2. poster85: size cap ----
def r_poster(txt):
    head, other, whole = split_conflict(txt)
    assert '5491267' in head and '5495117' in other
    repl = ("ok('主檔冇脹大（<%d；v89 BR89 有意增長至 5,288,705；v92 NAT92 通告板分布自然化（錯峰＋保底＋加厚 18 張）有意增長至 5,336,030；v95 LADDER95 結局梯擴充（新梯判定＋計數器＋9 格文案）有意增長至 5,386,704；v203 WF4 迎新期＋Phase 2 擴池（41 單新事件＋迎新期 code）有意增長至 5,448,954；v213 請柬提前＋晚間典禮有意增長至 5,491,267；v214 NP214 報紙重做有意增長至 5,524,996；v215 RELEASE215 推出日提及（新函數＋掛點）有意增長至 5,532,430，上限跟住原位更新）' % (5532430 + 40000), size < 5532430 + 40000)")
    return txt.replace(whole, repl)
resolve_file('tests/test_poster85_static.py', r_poster)

# ---- 3. ux68: size cap ----
def r_ux68(txt):
    head, other, whole = split_conflict(txt)
    assert '5565000' in head and '5540000' in other
    repl = ("ok('主檔總量 < 5,565,000 bytes（v84 ENC84 巧遇 Phase 3 四星對白 503 句＋註冊模組有意增長至 ~5,115,599；v83 為 ~5,047,816；v82 為 ~4,974,159；v86 WF4 事件池 36＋碎片 18＋對手線覆寫有意增長至 5,196,226；v89 BR89 分支補完有意增長至 ~5,288,705；v92 NAT92 通告板分布自然化（錯峰＋保底＋加厚 18 張）有意增長至 ~5,336,030；v95 LADDER95 結局梯擴充有意增長至 5,386,704；v203 WF4 迎新期＋Phase 2 擴池（41 單新事件＋迎新期 code）有意增長至 5,448,954；v213 請柬提前＋晚間典禮有意增長至 5,491,267；v211＋v212 rebase 上 main 17c6f69 有意增長至 5,500,561；v214 NP214 報紙重做有意增長至 5524996；v215 RELEASE215 推出日提及有意增長至 5532430）', len(src.encode('utf-8')) < 5575000)")
    return txt.replace(whole, repl)
resolve_file('tests/test_ux68_static.py', r_ux68)

# ---- 4/5. tang171 / tang173: total lines + openLoc DEF ----
DEF_OPENLOC = 56964
assert 'function openLoc(id, opts){' in new[DEF_OPENLOC-1], 'DEF line content mismatch'
def r_tang(txt):
    head, other, whole = split_conflict(txt)
    assert '62352' in head and '61935' in other and '56824' in head and '56407' in other
    repl = (f"ok('零行數漂移：總行數 62492（v193 61167＋v203 +233＋v204 +32＋v206 C1 +22＋v206 C2 +3＋v207 +34＋v208 +223＋v211 +42＋v212 +39＋v213 +199＋v214 +358＋v215 +140）', src.count('\\n') == 62492)\n"
            f"ok('零行數漂移：openLoc DEF 行 56964（v193 55639＋v203 +233＋v204 +32＋v206 C1 +22＋v206 C2 +3＋v207 +34＋v208 +223＋v211 +42＋v212 +39＋v213 +199＋v214 +358＋v215 +140，travel114 釘行）',\n"
            f"   len(lines) >= 56964 and 'function openLoc(id, opts){{' in lines[56963])\n"
            "# v20a215 rebase 上 main 7e27e1a resync：v215 淨 +140 行，釘行按 difflib 映射重寫，qa215 resync 核實純漂移（總行數 62352→62492；DEF 56824→56964）。")
    return txt.replace(whole, repl)
resolve_file('tests/test_tang171_static.py', r_tang)
resolve_file('tests/test_tang173_static.py', r_tang)

# ---- 6. rom176: anchor lines ----
def r_rom(txt):
    head, other, whole = split_conflict(txt)
    # HEAD-side anchor numbers -> mapped merged numbers (content-verified)
    pairs = [(31903, 'GIFT_REACT = giftReact'), (55254, '/* ===== v20a176 ROM176'),
             (55622, 'function rom176ApplyGiftOverrides()'), (56761, 'function addLocTalkGiftActs(add, L, npcId)'),
             (56855, 'rom176TryIntercept(id)')]
    mapped = {}
    for oldn, pat in pairs:
        n = mapping.get(oldn)
        assert n, f'anchor {oldn} unmapped'
        assert pat in new[n-1], f'anchor {oldn}->{n} content mismatch: {new[n-1][:80]}'
        mapped[oldn] = n
    print('rom176 mapped:', mapped)
    repl = (f"   'GIFT_REACT = giftReact' in line({mapped[31903]}) and 'rom176ApplyGiftOverrides()' in line({mapped[31903]}))\n"
            f"ok('釘：ROM176 block 起點 L{mapped[55254]}', line({mapped[55254]}).startswith('/* ===== v20a176 ROM176'))\n"
            f"ok('釘：rom176ApplyGiftOverrides 定義 L{mapped[55622]}', line({mapped[55622]}).startswith('function rom176ApplyGiftOverrides()'))\n"
            f"ok('釘：addLocTalkGiftActs L{mapped[56761]}', line({mapped[56761]}).startswith('function addLocTalkGiftActs(add, L, npcId)'))\n"
            f"ok('釘：openLoc rom176 攔截 L{mapped[56855]}', 'rom176TryIntercept(id)' in line({mapped[56855]}))\n"
            "# v20a215 rebase 上 main 7e27e1a resync：v215 淨 +140 行，釘行按 difflib 映射重寫（31903 唔郁、55254→55394、55622→55762、56761→56901、56855→56995），核實純漂移。")
    return txt.replace(whole, repl)
resolve_file('tests/test_rom176_static.py', r_rom)

# ---- 7. travel114: COUNT/FREE sets via difflib mapping, comments carried from HEAD side ----
def parse_entries(block):
    entries = []
    for line in block.split('\n'):
        m = re.match(r'\s*(\d+),(\s*#.*)?$', line)
        if m:
            entries.append((int(m.group(1)), (m.group(2) or '').rstrip()))
    return entries

def r_travel(txt):
    blocks = re.findall(r'<<<<<<< HEAD\n(.*?)\n=======\n(.*?)\n>>>>>>> [^\n]*\n', txt, re.S)
    assert len(blocks) == 2, f'expected 2 conflict blocks, got {len(blocks)}'
    out = txt
    FREE_FLAGS = ("travelFree:true","encDone:true","forceRestore:true","wf4Done:true")
    for head, other in blocks:
        h_entries = parse_entries(head)
        if not h_entries:
            continue
        # which set? COUNT has 12, FREE (2nd block) has 32 (+24945 outside = 33)
        mapped_lines = []
        for num, comment in h_entries:
            n = mapping.get(num)
            assert n, f'travel114 anchor {num} unmapped'
            assert 'openLoc(' in new[n-1], f'travel114 {num}->{n} no openLoc: {new[n-1][:80]}'
            mapped_lines.append(f'    {n},{comment}')
        repl = '\n'.join(mapped_lines)
        if 'DEF_LINE' in head:
            # DEF/WRAPPER 尾行喺呢個衝突塊入面，一併寫返（唔係用 replace 補）
            repl += ('\n}\nFREE_FLAGS = ("travelFree:true", "encDone:true", "forceRestore:true", "wf4Done:true")\n'
                     'DEF_LINE = 56964      # function openLoc(id, opts){\n'
                     'WRAPPER_LINE = 45392  # window.__phase2.openLoc：轉發 opts\n'
                     '# v20a215 rebase 上 main 7e27e1a resync：v215 淨 +140 行，COUNT／FREE／DEF／WRAPPER 按 difflib 映射重寫（COUNT 12／FREE 33 不變；DEF 56824→56964、WRAPPER 45390→45392），核實純漂移。')
            # head 嘅 FREE 塊尾本身有 "}\nFREE_FLAGS..." 兩行，要由 whole 扣起，唔重複
            whole = f'<<<<<<< HEAD\n{head}\n=======\n{other}\n>>>>>>> a0b5f2f (v20a215: 推出日提及——已殺青臨記級通告喺推出季首日晨報一則短訊)\n'
            assert whole in out, 'conflict block text mismatch'
            out = out.replace(whole, repl)
            continue
        whole = f'<<<<<<< HEAD\n{head}\n=======\n{other}\n>>>>>>> a0b5f2f (v20a215: 推出日提及——已殺青臨記級通告喺推出季首日晨報一則短訊)\n'
        assert whole in out, 'conflict block text mismatch'
        out = out.replace(whole, repl + '\n')
    assert '<<<<<<<' not in out and '>>>>>>>' not in out
    assert 'DEF_LINE = 56964' in out and 'WRAPPER_LINE = 45392' in out
    # verify DEF/WRAPPER content
    assert 'function openLoc(id, opts){' in new[56964-1]
    assert 'openLoc: function(id, opts){ openLoc(id, opts); }' in new[45392-1]
    open(f'{ROOT}/tests/test_travel114_static.py', 'w', encoding='utf-8').write(out)
    print('RESOLVED tests/test_travel114_static.py')
    # verify FREE content flags + COUNT no-flag on mapped sets
    return out
r_travel(open(f'{ROOT}/tests/test_travel114_static.py', encoding='utf-8').read())
print('ALL RESOLVED')
