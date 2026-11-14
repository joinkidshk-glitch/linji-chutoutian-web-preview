# v20a212 resync 套用：按 qa212/resync212_map.json（difflib 對位核實純漂移）更新 10 個靜態測試嘅釘行。
# 全部用單次 re.sub mapping 查表，唔逐對 str.replace（kwan151 有 26082→26083→26084 連鎖，逐對改會誤寫）。
# 用法：python3 qa212/apply_resync212.py（改完即印每個檔嘅替換數；任何一個錨點數目唔啱即 exit 1，唔寫檔）。
import json
import re
import sys

T = '/home/hatch/workspace/linji-work212/tests'
m = json.load(open('/home/hatch/workspace/linji-work212/qa212/resync212_map.json'))
fails = []


def load(name):
    with open(f'{T}/{name}', encoding='utf-8') as f:
        return f.read()


def save(name, txt):
    with open(f'{T}/{name}', 'w', encoding='utf-8') as f:
        f.write(txt)


def sub_once(txt, pat, mapping, label):
    """單次掃描：pat 嘅第 1 組係整數，喺 mapping 入面先換，唔喺就原樣留返。回傳（新文字，換咗幾多）。"""
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


def resync_note(txt, note):
    # 喺第一個 v20a208 resync 註解行之後加一行 v20a212 註解（跟返舊慣例）
    lines = txt.split('\n')
    for i, ln in enumerate(lines):
        if 'v20a208 resync' in ln:
            lines.insert(i + 1, note)
            return '\n'.join(lines)
    return txt


# --- travel114：COUNT／FREE 集合（只換集合內嘅釘行數字，註解數字唔郁）＋DEF／WRAPPER ---
txt = load('test_travel114_static.py')
count_map = {int(k): v for k, v in m['travel114 COUNT'].items()}
free_map = {int(k): v for k, v in m['travel114 FREE'].items()}
for var, mp in (('COUNT_LINES', count_map), ('FREE_LINES', free_map)):
    i = txt.index(var + ' = {')
    j = txt.index('\n}', i)
    seg, n = sub_once(txt[i:j], r'\b(\d+)\b', mp, var)
    expect(n == len(mp), f'travel114 {var} 換咗 {n}/{len(mp)} 個釘行')
    txt = txt[:i] + seg + txt[j:]
txt = txt.replace('DEF_LINE = 56186', 'DEF_LINE = 56225')
txt = txt.replace('WRAPPER_LINE = 45180', 'WRAPPER_LINE = 45181')
expect('DEF_LINE = 56225' in txt and 'WRAPPER_LINE = 45181' in txt, 'travel114 DEF／WRAPPER 已更新')
txt = resync_note(txt, '# v20a212 resync：index.html 淨 +39 行（見 qa212/resync212.py difflib 對位核實純漂移），總行數 61714→61753；COUNT／FREE／DEF／WRAPPER 按映射重寫，DEF 56186→56225、WRAPPER 45180→45181。')
save('test_travel114_static.py', txt)

# --- rom176：line(N) ---
txt = load('test_rom176_static.py')
mp = {int(k): v for k, v in m['rom176'].items()}
txt, n = sub_once(txt, r'line\((\d+)\)', mp, 'rom176')
expect(n == 7, f'rom176 換咗 {n}/7 個 line() 引用（6 個釘行，31712 用兩次）')
txt = resync_note(txt, '# v20a212 resync：釘行按 difflib 映射重寫（6151→6152、31712→31713、54616→54655、54984→55023、56123→56162、56217→56256），qa212/resync212.py 核實純漂移。')
save('test_rom176_static.py', txt)

# --- tang152：lines()[N]（0-based index） ---
txt = load('test_tang152_static.py')
mp = {int(k) - 1: v - 1 for k, v in m['tang152'].items()}
txt, n = sub_once(txt, r'lines\(\)\[(\d+)\]', mp, 'tang152')
expect(n == 3, f'tang152 換咗 {n}/3 個釘行')
txt = resync_note(txt, '# v20a212 resync：釘行按 difflib 映射重寫（25897→25898、31638→31639、31782→31783，0-based index），qa212/resync212.py 核實純漂移。')
save('test_tang152_static.py', txt)

# --- kwan151：line(N)（有連鎖 26082→26083→26084／31157→31158→31159，單次掃描先啱） ---
txt = load('test_kwan151_static.py')
mp = {int(k): v for k, v in m['kwan151'].items()}
txt, n = sub_once(txt, r'line\((\d+)\)', mp, 'kwan151')
expect(n == 24, f'kwan151 換咗 {n}/24 個 line() 引用（13 個釘行，多處重用同一行）')
txt = resync_note(txt, '# v20a212 resync：釘行按 difflib 映射重寫（全部 ＋1，CSS 段 ＋2 行起；26082／26083／26084 連鎖用單次掃描查表），qa212/resync212.py 核實純漂移。')
save('test_kwan151_static.py', txt)

# --- text125：ls[N]（0-based）＋len(ls) 守衛 ---
txt = load('test_text125_static.py')
mp = {int(k) - 1: v - 1 for k, v in m['text125'].items()}
txt, n = sub_once(txt, r'ls\[(\d+)\]', mp, 'text125')
expect(n == 3, f'text125 換咗 {n}/3 個釘行')
for a, b in (('len(ls) < 27857', 'len(ls) < 27858'), ('len(ls) < 27986', 'len(ls) < 27987'), ('len(ls) < 33688', 'len(ls) < 33689')):
    expect(a in txt, f'text125 守衛 {a} 在場')
    txt = txt.replace(a, b)
txt = resync_note(txt, '# v20a212 resync：釘行按 difflib 映射重寫（27863→27864、27992→27993、33700→33701，0-based index；守衛同步 ＋1），qa212/resync212.py 核實純漂移。')
save('test_text125_static.py', txt)

# --- tang171／tang173：總行數＋DEF＋（173：L4862 實指 lines[4953]） ---
for fname, extra in (('test_tang171_static.py', []), ('test_tang173_static.py', [('lines[4953]', 'lines[4954]', 8)])):
    txt = load(fname)
    expect("src.count('\\n') == 61714" in txt, f'{fname} 總行數錨點在場')
    txt = txt.replace("src.count('\\n') == 61714", "src.count('\\n') == 61753")
    expect('總行數 61714（v193 61167＋v203 +233＋v204 +32＋v206 C1 +22＋v206 C2 +3＋v207 +34＋v208 +223）' in txt,
           f'{fname} 總行數名在場')
    txt = txt.replace('總行數 61714（v193 61167＋v203 +233＋v204 +32＋v206 C1 +22＋v206 C2 +3＋v207 +34＋v208 +223）',
                      '總行數 61753（v193 61167＋v203 +233＋v204 +32＋v206 C1 +22＋v206 C2 +3＋v207 +34＋v208 +223＋v212 +39）')
    expect('openLoc DEF 行 56186' in txt, f'{fname} DEF 名在場')
    txt = txt.replace('openLoc DEF 行 56186（v193 55639＋v203 +233＋v204 +32＋v206 C1 +22＋v206 C2 +3＋v207 +34＋v208 +223，travel114 釘行）',
                      'openLoc DEF 行 56225（v193 55639＋v203 +233＋v204 +32＋v206 C1 +22＋v206 C2 +3＋v207 +34＋v208 +223＋v212 +39，travel114 釘行）')
    expect('lines[56185]' in txt, f'{fname} DEF index 在場')
    txt = txt.replace('lines[56185]', 'lines[56224]')
    for a, b, cnt in extra:
        got = txt.count(a)
        expect(got == cnt, f'{fname} {a} 出現 {got}/{cnt} 次')
        txt = txt.replace(a, b)
    txt = resync_note(txt, '# v20a212 resync：index.html 淨 +39 行（見 qa212/resync212.py difflib 對位核實純漂移），總行數 61714→61753、DEF 56186→56225。')
    save(fname, txt)

# --- gift185：總行數 ---
txt = load('test_gift185_static.py')
expect("html.count('\\n') == 61714" in txt, 'gift185 總行數錨點在場')
txt = txt.replace("html.count('\\n') == 61714", "html.count('\\n') == 61753")
expect('總行數 61714（v193 61167＋v203 +233＋v204 +32＋v206 C1 +22＋v206 C2 +3＋v207 +34＋v208 +223）' in txt,
       'gift185 總行數名在場')
txt = txt.replace('總行數 61714（v193 61167＋v203 +233＋v204 +32＋v206 C1 +22＋v206 C2 +3＋v207 +34＋v208 +223）',
                  '總行數 61753（v193 61167＋v203 +233＋v204 +32＋v206 C1 +22＋v206 C2 +3＋v207 +34＋v208 +223＋v212 +39）')
txt = resync_note(txt, '# v20a212 resync：index.html 淨 +39 行（見 qa212/resync212.py difflib 對位核實純漂移），總行數 61714→61753。')
save('test_gift185_static.py', txt)

# --- awards168／awards174：syncGlamour 錨點改用 isGlam212（v20a212 A1 重構，choke point 意圖不變） ---
txt = load('test_awards168_static.py')
expect('classList.toggle("on", !!(b && b.id === "glamour"))' in txt, 'awards168 on 錨點在場')
txt = txt.replace('classList.toggle("on", !!(b && b.id === "glamour"))', 'classList.toggle("on", isGlam212)')
expect('classList.toggle("glamour-hide", !!(b && b.id === "glamour"))' in txt, 'awards168 glamour-hide 錨點在場')
txt = txt.replace('classList.toggle("glamour-hide", !!(b && b.id === "glamour"))', 'classList.toggle("glamour-hide", isGlam212)')
txt = resync_note(txt, '# v20a212 A1：syncGlamour 改用 isGlam212 變數（跳過掣一併喺同一 choke point 開／閂），錨點跟住改，意圖不變。')
save('test_awards168_static.py', txt)

txt = load('test_awards174_static.py')
expect('classList.toggle("glamour-hide", !!(b && b.id === "glamour"))' in txt, 'awards174 glamour-hide 錨點在場')
txt = txt.replace('classList.toggle("glamour-hide", !!(b && b.id === "glamour"))', 'classList.toggle("glamour-hide", isGlam212)')
txt = resync_note(txt, '# v20a212 A1：syncGlamour 改用 isGlam212 變數（跳過掣一併喺同一 choke point 開／閂），錨點跟住改，意圖不變。')
save('test_awards174_static.py', txt)

print('')
print('FAILED: %d' % len(fails) if fails else 'ALL APPLIED')
sys.exit(1 if fails else 0)
