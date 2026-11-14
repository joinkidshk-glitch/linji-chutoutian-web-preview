# v20a216 resync 套用：按 qa216/resync216_map.json（difflib 對位核實純漂移）更新 8 個靜態測試嘅釘行／總行數。
# 全部用單次 re.sub mapping 查表，唔逐對 str.replace（有連鎖／歷史註解舊數，逐對改會誤寫）。
# 限範圍：travel114 只換 COUNT／FREE 集合內＋DEF／WRAPPER 字面；kwan151／rom176 只換 line(N) 呼叫；
# tang152 只換 lines()[N]；tang171／173／gift185 只換總行數／DEF／L4862 斷言行；text125 只換 ls[N]。
# 歷史註解入面嘅舊數（例如 kwan151 名入面嘅 L25608、tang173「L4862」標籤、resync 舊數）一律唔郁；
# 斷言名入面嘅歷史標籤（L6152／L31712／L25608…）係舊版標籤，今次唔改，淨換 code 數字。
# 用法：python3 qa216/apply_resync216.py（改完即印每個檔嘅替換數；任何一個錨點數目唔啱即 exit 1，唔寫檔）。
import json
import re
import sys

ROOT = '/home/hatch/workspace/linji-work216'
T = f'{ROOT}/tests'
m = json.load(open(f'{ROOT}/qa216/resync216_map.json'))
fails = []


def load(name):
    with open(f'{T}/{name}', encoding='utf-8') as f:
        return f.read()


def save(name, txt):
    with open(f'{T}/{name}', 'w', encoding='utf-8') as f:
        f.write(txt)


def sub_once(txt, pat, mapping, label):
    """單次掃描：pat 的第 1 組係整數，喺 mapping 入面先換，唔喺就原樣留返。回傳（新文字，換咗幾多）。"""
    n = [0]

    def fn(mm):
        v = int(mm.group(1))
        if v in mapping:
            n[0] += 1
            return mm.group(0).replace(str(v), str(mapping[v]), 1)
        return mm.group(0)
    return re.sub(pat, fn, txt), n[0]


def expect(cond, label):
    print(('PASS ' if cond else 'FAIL ') + label)
    if not cond:
        fails.append(label)


def resync_note_after(txt, anchor, note):
    lines = txt.split('\n')
    for i, ln in enumerate(lines):
        if anchor in ln:
            lines.insert(i + 1, note)
            return '\n'.join(lines)
    return txt


def count_matches(txt, pat, mapping):
    return sum(1 for mm in re.finditer(pat, txt) if int(mm.group(1)) in mapping)


OLD_TOTAL = '62492'
NEW_TOTAL = '62755'
TOTAL_SUFFIX = '＋v216 +263'
OLD_DEF = '56964'
NEW_DEF = '57227'

# --- travel114：COUNT／FREE 集合（只換集合內嘅釘行數字，註解數字唔郁）＋DEF／WRAPPER ---
txt = load('test_travel114_static.py')
if 'DEF_LINE = 57227' in txt and 'WRAPPER_LINE = 45430' in txt:
    print('SKIP travel114（已套用）')
else:
    count_map = {int(k): v for k, v in m['travel114 COUNT'].items()}
    free_map = {int(k): v for k, v in m['travel114 FREE'].items()}
    for var, mp in (('COUNT_LINES', count_map), ('FREE_LINES', free_map)):
        i = txt.index(var + ' = {')
        j = txt.index('\n}', i)
        seg, n = sub_once(txt[i:j], r'\b(\d+)\b', mp, var)
        expect(n == len(mp), f'travel114 {var} 換咗 {n}/{len(mp)} 個釘行')
        txt = txt[:i] + seg + txt[j:]
    txt = txt.replace('DEF_LINE = 56964', 'DEF_LINE = 57227')
    txt = txt.replace('WRAPPER_LINE = 45392', 'WRAPPER_LINE = 45430')
    expect('DEF_LINE = 57227' in txt and 'WRAPPER_LINE = 45430' in txt, 'travel114 DEF／WRAPPER 已更新')
    txt = resync_note_after(txt, '# v20a215 resync：',
        '# v20a216 resync：index.html 淨 +263 行（見 qa216/resync216.py difflib 對位核實純漂移），總行數 62492→62755；COUNT／FREE／DEF／WRAPPER 按映射重寫，DEF 56964→57227、WRAPPER 45392→45430。')
    if not fails:
        save('test_travel114_static.py', txt)

# --- kwan151：line(N) 呼叫（名入面嘅 L25608 等歷史標籤唔郁）---
txt = load('test_kwan151_static.py')
if 'line(25956)' in txt:
    print('SKIP kwan151（已套用）')
else:
    mp = {int(k): v for k, v in m['kwan151'].items()}
    exp = count_matches(txt, r'\bline\((\d+)\)', mp)
    txt, n = sub_once(txt, r'\bline\((\d+)\)', mp, 'kwan151')
    expect(n == exp == 24, f'kwan151 換咗 {n}/{exp} 個 line() 引用')
    txt = resync_note_after(txt, '# v20a214 rebase 上 main d1239d4 resync：',
        '# v20a216 resync：index.html 淨 +263 行（見 qa216/resync216.py difflib 對位核實純漂移），13 個釘行按映射重寫（＋38，名入面嘅 L25608 等歷史標籤唔郁）。')
    if not fails:
        save('test_kwan151_static.py', txt)

# --- rom176：名＝code 嘅 L…', line(N) 一齊換；L6152／L31712 名唔郁，淨換 line(N) ---
txt = load('test_rom176_static.py')
if 'line(55657)' in txt:
    print('SKIP rom176（已套用）')
else:
    mp = {int(k): v for k, v in m['rom176'].items()}
    n_rom = [0]

    def _rom_fn(mm):
        v = int(mm.group(2))
        if v in mp and int(mm.group(1)) == v:
            n_rom[0] += 1
            return f"L{mp[v]}', line({mp[v]})"
        return mm.group(0)
    txt = re.sub(r"L(\d+)', line\((\d+)\)", _rom_fn, txt)
    expect(n_rom[0] == 3, f'rom176 換咗 {n_rom[0]}/3 個 L…／line() 引用（55394／55762／56901）')
    rest = {k: v for k, v in mp.items() if k not in (55394, 55762, 56901)}
    exp = count_matches(txt, r'\bline\((\d+)\)', rest)
    txt, n = sub_once(txt, r'\bline\((\d+)\)', rest, 'rom176-rest')
    expect(n == exp == 4, f'rom176 換咗 {n}/{exp} 個其餘 line() 引用（6322／31903×2／56995）')
    txt = resync_note_after(txt, '# v20a215 rebase 上 main 7e27e1a resync：',
        '# v20a216 resync：釘行按 difflib 映射重寫（6322→6360、31903→31941、55394→55657、55762→56025、56901→57164、56995→57258；L6152／L31712 名唔郁），qa216/resync216.py 核實純漂移。')
    if not fails:
        save('test_rom176_static.py', txt)

# --- tang152：lines()[N]（0-based 索引）---
txt = load('test_tang152_static.py')
if 'lines()[26115]' in txt:
    print('SKIP tang152（已套用）')
else:
    mp = {k - 1: v - 1 for k, v in ((int(k), v) for k, v in m['tang152'].items())}
    exp = count_matches(txt, r'lines\(\)\[(\d+)\]', mp)
    txt, n = sub_once(txt, r'lines\(\)\[(\d+)\]', mp, 'tang152')
    expect(n == exp == 3, f'tang152 換咗 {n}/{exp} 個 lines()[N] 引用')
    txt = resync_note_after(txt, '# v20a214 rebase 上 main d1239d4 resync：',
        '# v20a216 resync：index.html 淨 +263 行（見 qa216/resync216.py difflib 對位核實純漂移），3 個釘行按映射重寫（＋38）。')
    if not fails:
        save('test_tang152_static.py', txt)

# --- tang171／tang173：總行數＋DEF（＋tang173 L4862）---
for fname in ('test_tang171_static.py', 'test_tang173_static.py'):
    txt = load(fname)
    if f"== {NEW_TOTAL}" in txt:
        print(f'SKIP {fname}（已套用）')
        continue
    old_total = ("總行數 62492（v193 61167＋v203 +233＋v204 +32＋v206 C1 +22＋v206 C2 +3＋v207 +34＋v208 +223"
                 "＋v211 +42＋v212 +39＋v213 +199＋v214 +358＋v215 +140）")
    new_total = ("總行數 62755（v193 61167＋v203 +233＋v204 +32＋v206 C1 +22＋v206 C2 +3＋v207 +34＋v208 +223"
                 "＋v211 +42＋v212 +39＋v213 +199＋v214 +358＋v215 +140＋v216 +263）")
    expect(old_total in txt, f'{fname} 總行數名在位')
    txt = txt.replace(old_total, new_total)
    expect("src.count('\\n') == 62492" in txt, f'{fname} 總行數比較在位')
    txt = txt.replace("src.count('\\n') == 62492", "src.count('\\n') == 62755")
    old_def = ("openLoc DEF 行 56964（v193 55639＋v203 +233＋v204 +32＋v206 C1 +22＋v206 C2 +3＋v207 +34＋v208 +223"
               "＋v211 +42＋v212 +39＋v213 +199＋v214 +358＋v215 +140，travel114 釘行）")
    new_def = ("openLoc DEF 行 57227（v193 55639＋v203 +233＋v204 +32＋v206 C1 +22＋v206 C2 +3＋v207 +34＋v208 +223"
               "＋v211 +42＋v212 +39＋v213 +199＋v214 +358＋v215 +140＋v216 +263，travel114 釘行）")
    expect(old_def in txt, f'{fname} DEF 名在位')
    txt = txt.replace(old_def, new_def)
    expect("len(lines) >= 56964 and 'function openLoc(id, opts){' in lines[56963]" in txt, f'{fname} DEF 檢查在位')
    txt = txt.replace("len(lines) >= 56964 and 'function openLoc(id, opts){' in lines[56963]",
                      "len(lines) >= 57227 and 'function openLoc(id, opts){' in lines[57226]")
    if fname == 'test_tang173_static.py':
        expect("len(lines) >= 5125 and 'loc-acts-more171::after' in lines[5124]" in txt,
               'tang173 L4862 len 檢查在位（換前）')
        mp = {5124: 5162}
        exp = count_matches(txt, r'lines\[(\d+)\]', mp)
        txt, n = sub_once(txt, r'lines\[(\d+)\]', mp, 'tang173-L4862')
        expect(n == exp == 8, f'tang173 L4862 換咗 {n}/{exp} 個 lines[5124] 引用')
        txt = txt.replace('len(lines) >= 5125', 'len(lines) >= 5163')
    txt = resync_note_after(txt, '# v20a215 resync：',
        '# v20a216 resync：index.html 淨 +263 行（見 qa216/resync216.py difflib 對位核實純漂移），總行數 62492→62755、DEF 56964→57227'
        + ('、L4862 5125→5163。' if fname == 'test_tang173_static.py' else '。'))
    if not fails:
        save(fname, txt)

# --- gift185：總行數 ---
txt = load('test_gift185_static.py')
if f"== {NEW_TOTAL}" in txt:
    print('SKIP gift185（已套用）')
else:
    old_total = ("總行數 62492（v193 61167＋v203 +233＋v204 +32＋v206 C1 +22＋v206 C2 +3＋v207 +34＋v208 +223"
                 "＋v211 +42＋v212 +39＋v213 +199＋v214 +358＋v215 +140）")
    new_total = ("總行數 62755（v193 61167＋v203 +233＋v204 +32＋v206 C1 +22＋v206 C2 +3＋v207 +34＋v208 +223"
                 "＋v211 +42＋v212 +39＋v213 +199＋v214 +358＋v215 +140＋v216 +263）")
    expect(old_total in txt, 'gift185 總行數名在位')
    txt = txt.replace(old_total, new_total)
    expect("html.count('\\n') == 62492" in txt, 'gift185 總行數比較在位')
    txt = txt.replace("html.count('\\n') == 62492", "html.count('\\n') == 62755")
    txt = resync_note_after(txt, '# v20a214 rebase 上 main d1239d4 resync：',
        '# v20a216 resync：index.html 淨 +263 行（見 qa216/resync216.py difflib 對位核實純漂移），總行數 62492→62755。')
    if not fails:
        save('test_gift185_static.py', txt)

# --- text125：ls[N]（0-based 索引）---
txt = load('test_text125_static.py')
if 'ls[28081]' in txt:
    print('SKIP text125（已套用）')
else:
    mp = {k - 1: v - 1 for k, v in ((int(k), v) for k, v in m['text125'].items())}
    exp = count_matches(txt, r'\bls\[(\d+)\]', mp)
    txt, n = sub_once(txt, r'\bls\[(\d+)\]', mp, 'text125')
    expect(n == exp == 3, f'text125 換咗 {n}/{exp} 個 ls[N] 引用')
    txt = resync_note_after(txt, '# v20a214 rebase 上 main d1239d4 resync：',
        '# v20a216 resync：index.html 淨 +263 行（見 qa216/resync216.py difflib 對位核實純漂移），3 個釘行按映射重寫（＋38）。')
    if not fails:
        save('test_text125_static.py', txt)

print()
if fails:
    print('FAILED: ' + ' | '.join(fails))
    print('有數目唔啱——未寫檔，停低檢查。')
    sys.exit(1)
print('ALL RESYNC APPLIED')
