# -*- coding: utf-8 -*-
# v20a157 rebase resync（rebase 上 origin/main 60b0a8f，HEAD 171829a）：
#   用 difflib 將每條釘行由釘行基底對位去 rebase 後 index.html，逐行核實內容逐字相同＝純漂移先改行號。
#   單次掃描 dict 查表一次過換，唔逐對 re.sub（AGENTS.md v160 教訓：逐對 re.sub 會撞值丟失／重複）。
#   兩條基底：
#     A) d64887c（rebase 前 v157 樹，e08a070＋splice）——travel114／text125（rebase 衝突取咗 v157 版）
#     B) 60b0a8f（main）——kwan151／tang152（由 main 嚟，splice 令佢哋釘嘅行漂移）
# 用法：python3 qa131/resync_rebase157.py [--apply]
#   唔加 --apply：只印對位表＋核實結果，唔改檔。加 --apply：寫入四檔測試檔行號＋註解。
import difflib, subprocess, sys

ROOT = subprocess.run(['git', 'rev-parse', '--show-toplevel'], capture_output=True, text=True).stdout.strip()

def git_lines(ref):
    out = subprocess.run(['git', 'show', '%s:index.html' % ref], cwd=ROOT, capture_output=True, text=True)
    assert out.returncode == 0, ref
    return out.stdout.split('\n')

def head_lines():
    with open('%s/index.html' % ROOT, encoding='utf-8') as f:
        return f.read().split('\n')

def build_map(base, head):
    """回傳 dict：base 行號(1-based) -> head 行號(1-based)，只限 difflib 'equal' 段內逐行對應。"""
    sm = difflib.SequenceMatcher(None, base, head, autojunk=False)
    m = {}
    ops = []
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        ops.append((tag, i1, i2, j1, j2))
        if tag == 'equal':
            for k in range(i2 - i1):
                m[i1 + 1 + k] = j1 + 1 + k
    return m, ops

def op_summary(ops):
    ins = sum(j2 - j1 for t, i1, i2, j1, j2 in ops if t == 'insert')
    dele = sum(i2 - i1 for t, i1, i2, j1, j2 in ops if t == 'delete')
    rep_old = sum(i2 - i1 for t, i1, i2, j1, j2 in ops if t == 'replace')
    rep_new = sum(j2 - j1 for t, i1, i2, j1, j2 in ops if t == 'replace')
    nrep = sum(1 for t, *_ in ops if t == 'replace')
    return ins, dele, rep_old, rep_new, nrep

# 釘行表：檔 -> (基底 ref, [1-based 行號])
PINS = {
    'tests/test_travel114_static.py': ('d64887c', [
        32198, 35679, 37806, 38800, 39234, 39237, 39268, 43818, 57662, 57829, 57972, 57993, 58443,  # COUNT 13
        24796, 28291, 30919, 30920, 30932, 30933, 30944, 30945, 31048, 40773, 43475, 43498, 52507,
        52626, 53519, 53901, 53923, 54058, 55695, 57106, 57439, 57557, 57558, 57593, 57594, 57613, 57628,  # FREE 27
        53632, 44241]),  # DEF_LINE / WRAPPER_LINE
    'tests/test_text125_static.py': ('d64887c', [27824, 27937, 33582]),
    'tests/test_kwan151_static.py': ('60b0a8f', [
        25545, 25882, 25930, 26149, 25887, 25885, 25886, 30840, 30831, 30839, 27123, 30882, 27090]),
    'tests/test_tang152_static.py': ('60b0a8f', [25701, 31321, 31465]),
}

def main():
    apply = '--apply' in sys.argv
    head = head_lines()
    bases = {}
    maps = {}
    for ref in ('d64887c', '60b0a8f'):
        base = git_lines(ref)
        bases[ref] = base
        m, ops = build_map(base, head)
        maps[ref] = m
        ins, dele, ro, rn, nrep = op_summary(ops)
        print('基底 %s -> HEAD：%d 行 -> %d 行；insert +%d／delete -%d／replace %d 段（舊 %d 行→新 %d 行）；淨 %+d'
              % (ref, len(base), len(head), ins, dele, nrep, ro, rn, len(head) - len(base)))
    print()
    all_ok = True
    tables = {}
    for path, (ref, pins) in PINS.items():
        base = bases[ref]
        m = maps[ref]
        print('== %s（基底 %s）==' % (path, ref))
        tab = {}
        for old in sorted(set(pins)):
            new = m.get(old)
            if new is None:
                print('  !! %d 無對位（落喺 replace／delete 段，唔係純漂移）' % old)
                all_ok = False
                continue
            same = base[old - 1] == head[new - 1]
            flag = 'OK ' if same else '!! 內容唔同 '
            if not same:
                all_ok = False
            print('  %s%d -> %d（%+d）｜%s' % (flag, old, new, new - old, base[old - 1].strip()[:80]))
            tab[old] = new
        tables[path] = tab
        print()
    print('核實結論：%s' % ('全部釘行純漂移，內容逐字相同' if all_ok else '有問題，停低，唔 apply'))
    if not all_ok:
        sys.exit(1)
    if apply:
        do_apply(tables)
    return tables

def do_apply(tables):
    import re
    # --- travel114：只喺 COUNT_LINES／FREE_LINES 集合區＋DEF／WRAPPER 賦值行內換數（註解歷史唔郁）---
    p = '%s/tests/test_travel114_static.py' % ROOT
    tab = tables[p.split(ROOT + '/')[1]]
    src = open(p, encoding='utf-8').read()
    # 搵出四個 live 區嘅 span
    spans = []
    for pat in (r'COUNT_LINES\s*=\s*\{', r'FREE_LINES\s*=\s*\{'):
        m = re.search(pat, src)
        j = src.find('}', m.end())
        spans.append((m.start(), j + 1))
    for pat in (r'DEF_LINE\s*=\s*\d+', r'WRAPPER_LINE\s*=\s*\d+'):
        m = re.search(pat, src)
        spans.append((m.start(), m.end()))
    num_re = re.compile(r'\b\d{5}\b')
    def repl(mo):
        v = int(mo.group(0))
        return str(tab[v]) if v in tab else mo.group(0)
    out = []
    pos = 0
    for a, b in sorted(spans):
        out.append(src[pos:a])
        out.append(num_re.sub(repl, src[a:b]))
        pos = b
    out.append(src[pos:])
    new = ''.join(out)
    open(p, 'w', encoding='utf-8').write(new)
    print('travel114：已寫入（COUNT＋FREE＋DEF／WRAPPER，單次掃描 dict 查表）')

    # --- text125：只喺 `len(ls) < N`／`ls[N]` 呢兩個 pattern 換數（行尾 # v157 resync 註解唔郁）---
    p = '%s/tests/test_text125_static.py' % ROOT
    tab = tables[p.split(ROOT + '/')[1]]
    src = open(p, encoding='utf-8').read()
    # len bound：27824→new（＝行號本身），27937→new，33584→new+2（原 +2 slack 保留）
    len_map = {27824: tab[27824], 27937: tab[27937], 33584: tab[33582] + 2}
    idx_map = {27823: tab[27824] - 1, 27936: tab[27937] - 1, 33581: tab[33582] - 1}
    new, n = re.subn(r'len\(ls\) < (\d+)', lambda mo: 'len(ls) < %d' % len_map[int(mo.group(1))], src)
    new, n2 = re.subn(r'ls\[(\d+)\]', lambda mo: 'ls[%d]' % idx_map[int(mo.group(1))], new)
    open(p, 'w', encoding='utf-8').write(new)
    print('text125：已寫入（len bound %d 處＋ls 索引 %d 處）' % (n, n2))

    # --- kwan151：`line(N)`＋`LNNNNN` 標籤（code 行＋header 註解入面跟 live 錨點嗰兩個 L 號），單次掃描 dict 查表 ---
    p = '%s/tests/test_kwan151_static.py' % ROOT
    tab = tables[p.split(ROOT + '/')[1]]
    src = open(p, encoding='utf-8').read()
    pat = re.compile(r'line\((\d+)\)|L(\d{5})')
    def repl151(mo):
        if mo.group(1) is not None:
            v = int(mo.group(1))
            return 'line(%d)' % tab[v] if v in tab else mo.group(0)
        v = int(mo.group(2))
        return 'L%d' % tab[v] if v in tab else mo.group(0)
    new, n = pat.subn(repl151, src)
    open(p, 'w', encoding='utf-8').write(new)
    print('kwan151：已寫入（%d 處 line()／L 標籤）' % n)

    # --- tang152：`lines()[N]`＋ok() 名 `(LNNNNN)`，單次掃描 dict 查表；header 裸數行另外成行改寫 ---
    p = '%s/tests/test_tang152_static.py' % ROOT
    tab = tables[p.split(ROOT + '/')[1]]
    src = open(p, encoding='utf-8').read()
    # 注意：ok() 名標籤用全形括號（L25701），唔係半形 (L25701)。
    pat = re.compile(r'lines\(\)\[(\d+)\]|（L(\d{5})）')
    def repl152(mo):
        if mo.group(1) is not None:
            v = int(mo.group(1))
            return 'lines()[%d]' % (tab[v + 1] - 1) if (v + 1) in tab else mo.group(0)
        v = int(mo.group(2))
        return '（L%d）' % tab[v] if v in tab else mo.group(0)
    new, n = pat.subn(repl152, src)
    # header 裸數行：HELD 25701／normaliser 31321／loader 31465 → 新數（成行寫死，唔經 re.sub 鏈）
    old_hdr = '# 行號寫死（HELD 25701／normaliser 31321／loader 31465（v152 rebase 上 main 8409178：v155＋v161 令行號再移位） 等），rebase 要人手 resync。'
    new_hdr = '# 行號寫死（HELD %d／normaliser %d／loader %d（v152 rebase 上 main 8409178：v155＋v161 令行號再移位） 等），rebase 要人手 resync。' % (
        tab[25701], tab[31321], tab[31465])
    assert old_hdr in new, 'tang152 header 行搵唔到'
    new = new.replace(old_hdr, new_hdr)
    open(p, 'w', encoding='utf-8').write(new)
    print('tang152：已寫入（%d 處 lines()／L 標籤＋header 裸數行）' % n)

if __name__ == '__main__':
    main()
