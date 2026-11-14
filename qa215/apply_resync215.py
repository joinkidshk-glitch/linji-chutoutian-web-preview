# v20a215 resync 套用：按 qa215/resync215_map.json（difflib 對位核實純漂移）更新 7 個靜態測試嘅釘行／上限。
# 全部用單次 re.sub mapping 查表，唔逐對 str.replace（有連鎖／歷史註解舊數，逐對改會誤寫）。
# 限範圍：travel114 只換 COUNT／FREE 集合內＋DEF／WRAPPER 字面；rom176 只換 L…', line(N)；
# tang171／173／gift185 只換總行數／DEF 斷言行；poster85／ux68 只換上限數字。
# 歷史註解入面嘅舊數（例如 rom176「54655→54697」、tang「DEF 56186→56225」）一律唔郁。
# 附帶修正：tang171／173 DEF 名公式漏咗 v211 +42（真 DEF 喺 56267 唔係 56225），呢次補返。
# 用法：python3 qa215/apply_resync215.py（改完即印每個檔嘅替換數；任何一個錨點數目唔啱即 exit 1，唔寫檔）。
import json
import re
import sys

ROOT = '/home/hatch/workspace/linji-work215'
T = f'{ROOT}/tests'
m = json.load(open(f'{ROOT}/qa215/resync215_map.json'))
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


# --- travel114：COUNT／FREE 集合（只換集合內嘅釘行數字，註解數字唔郁）＋DEF／WRAPPER ---
# （已套用過就跳過：DEF 已係新值嗰陣唔重跑）---
txt = load('test_travel114_static.py')
if 'DEF_LINE = 56407' in txt and 'WRAPPER_LINE = 45190' in txt:
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
    txt = txt.replace('DEF_LINE = 56267', 'DEF_LINE = 56407')
    txt = txt.replace('WRAPPER_LINE = 45188', 'WRAPPER_LINE = 45190')
    expect('DEF_LINE = 56407' in txt and 'WRAPPER_LINE = 45190' in txt, 'travel114 DEF／WRAPPER 已更新')
    txt = resync_note_after(txt, '# v20a212 resync：',
        '# v20a215 resync：index.html 淨 +140 行（見 qa215/resync215.py difflib 對位核實純漂移），總行數 61795→61935；COUNT／FREE／DEF／WRAPPER 按映射重寫，DEF 56267→56407、WRAPPER 45188→45190。')
    if not fails:
        save('test_travel114_static.py', txt)

# --- rom176：L…', line(N)（名＋呼叫一齊換；歷史註解「54655→54697」唔郁）---
# L56298 嗰行結構唔同（名後面唔係直接 line(，係 'rom176TryIntercept(id)' in line(），另做字面替換。---
txt = load('test_rom176_static.py')
mp = {int(k): v for k, v in m['rom176'].items()}
n_rom = [0]
def _rom_fn(mm):
    v = int(mm.group(2))
    if v in mp and int(mm.group(1)) == v:
        n_rom[0] += 1
        return f"L{mp[v]}', line({mp[v]})"
    return mm.group(0)
txt = re.sub(r"L(\d+)', line\((\d+)\)", _rom_fn, txt)
expect(n_rom[0] == 4, f'rom176 換咗 {n_rom[0]}/4 個 L…／line() 引用（6152 唔郁、31713 唔入呢式、56298 另處理）')
expect("ok('釘：openLoc rom176 攔截 L56298', 'rom176TryIntercept(id)' in line(56298))" in txt, 'rom176 56298 行在位')
txt = txt.replace("ok('釘：openLoc rom176 攔截 L56298', 'rom176TryIntercept(id)' in line(56298))",
                  "ok('釘：openLoc rom176 攔截 L56438', 'rom176TryIntercept(id)' in line(56438))")
expect("L56438', 'rom176TryIntercept(id)' in line(56438)" in txt, 'rom176 56298→56438 已更新')
txt = resync_note_after(txt, '# v20a212 rebase 上 main b1ca47a resync：',
    '# v20a215 resync：釘行按 difflib 映射重寫（54697→54837、55065→55205、56204→56344、56298→56438；6152／31713 唔郁），qa215/resync215.py 核實純漂移。')
if not fails:
    save('test_rom176_static.py', txt)

# --- tang171／tang173：總行數＋DEF（名公式補返 v211 +42；歷史註解行 7 唔郁，另加註解行）---
for fname in ('test_tang171_static.py', 'test_tang173_static.py'):
    txt = load(fname)
    old_total = "總行數 61795（v193 61167＋v203 +233＋v204 +32＋v206 C1 +22＋v206 C2 +3＋v207 +34＋v208 +223＋v211 +42＋v212 +39）"
    new_total = "總行數 61935（v193 61167＋v203 +233＋v204 +32＋v206 C1 +22＋v206 C2 +3＋v207 +34＋v208 +223＋v211 +42＋v212 +39＋v215 +140）"
    expect(old_total in txt, f'{fname} 總行數名在位')
    txt = txt.replace(old_total, new_total)
    expect("src.count('\\n') == 61795" in txt, f'{fname} 總行數比較在位')
    txt = txt.replace("src.count('\\n') == 61795", "src.count('\\n') == 61935")
    old_def = "openLoc DEF 行 56225（v193 55639＋v203 +233＋v204 +32＋v206 C1 +22＋v206 C2 +3＋v207 +34＋v208 +223＋v212 +39，travel114 釘行）"
    new_def = "openLoc DEF 行 56407（v193 55639＋v203 +233＋v204 +32＋v206 C1 +22＋v206 C2 +3＋v207 +34＋v208 +223＋v211 +42＋v212 +39＋v215 +140，travel114 釘行）"
    expect(old_def in txt, f'{fname} DEF 名在位')
    txt = txt.replace(old_def, new_def)
    expect("len(lines) >= 56267 and 'function openLoc(id, opts){' in lines[56266]" in txt, f'{fname} DEF 檢查在位')
    txt = txt.replace("len(lines) >= 56267 and 'function openLoc(id, opts){' in lines[56266]",
                      "len(lines) >= 56407 and 'function openLoc(id, opts){' in lines[56406]")
    txt = resync_note_after(txt, '# v20a212 resync：',
        '# v20a215 resync：index.html 淨 +140 行（見 qa215/resync215.py difflib 對位核實純漂移），總行數 61795→61935、DEF 56267→56407（名公式補返漏咗嘅 v211 +42；真 DEF 喺 56267 唔係 56225）。')
    if not fails:
        save(fname, txt)

# --- gift185：總行數 ---
txt = load('test_gift185_static.py')
old_total = "總行數 61795（v193 61167＋v203 +233＋v204 +32＋v206 C1 +22＋v206 C2 +3＋v207 +34＋v208 +223＋v211 +42＋v212 +39）"
new_total = "總行數 61935（v193 61167＋v203 +233＋v204 +32＋v206 C1 +22＋v206 C2 +3＋v207 +34＋v208 +223＋v211 +42＋v212 +39＋v215 +140）"
expect(old_total in txt, 'gift185 總行數名在位')
txt = txt.replace(old_total, new_total)
expect("html.count('\\n') == 61795" in txt, 'gift185 總行數比較在位')
txt = txt.replace("html.count('\\n') == 61795", "html.count('\\n') == 61935")
expect('v211 +42＋v212 +39，qa212/resync212_rebase.py' in txt, 'gift185 註解在位')
txt = txt.replace('v211 +42＋v212 +39，qa212/resync212_rebase.py',
                  'v211 +42＋v212 +39＋v215 +140，qa215/resync215.py')
if not fails:
    save('test_gift185_static.py', txt)

# --- poster85：主檔上限 5448954＋40000 → 5495117＋40000（現 5,495,117）---
txt = load('test_poster85_static.py')
expect(txt.count('5448954') == 2, f'poster85 上限基數出現 {txt.count("5448954")}/2 次')
txt = txt.replace('5448954', '5495117')
expect('有意增長至 5,448,954，上限跟住原位更新' in txt, 'poster85 訊息在位')
txt = txt.replace('有意增長至 5,448,954，上限跟住原位更新',
                  '有意增長至 5,448,954；v215 RELEASE215 推出日提及（新函數＋掛點）有意增長至 5,495,117，上限跟住原位更新')
if not fails:
    save('test_poster85_static.py', txt)

# --- ux68：主檔上限 5,490,000 → 5,540,000（現 5,495,117）---
txt = load('test_ux68_static.py')
expect("len(src.encode('utf-8')) < 5490000" in txt, 'ux68 上限在位')
txt = txt.replace("len(src.encode('utf-8')) < 5490000", "len(src.encode('utf-8')) < 5540000")
expect('有意增長至 5,448,954）' in txt, 'ux68 訊息在位')
txt = txt.replace('有意增長至 5,448,954）', '有意增長至 5,448,954；v215 RELEASE215 推出日提及有意增長至 5,495,117）')
if not fails:
    save('test_ux68_static.py', txt)

print()
if fails:
    print('FAILED: ' + ' | '.join(fails))
    print('有數目唔啱——未寫檔，停低檢查。')
    sys.exit(1)
print('ALL RESYNC APPLIED')
