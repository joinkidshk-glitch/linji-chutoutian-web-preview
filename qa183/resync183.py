# v20a183 resync：用 difflib 對位核實純漂移，更新釘行測試。
# 漂移來源（淨 +117 行）：C7 CSS +2（L3849）、prefKind +1（L30519）、TryIntercept +1（L53246）、
# PlayEncounter +2（L53279）、ROM183 block +107（L53549）、openGiftPick 確認 modal +3（L58500／58502）、
# goBit +1（L58684）。其餘 26 處取代全部原地改（行數不變）。
# 用法：python3 qa183/resync183.py — 先核實每粒釘行內容逐字相同先改數字，唔啱即停。
import io, re, subprocess, sys

def lines_of(p):
    return io.open(p, encoding='utf-8').read().split('\n')

old = lines_of('/tmp/pristine183/index.html')
new = lines_of('index.html')
assert len(new) - len(old) == 117, '行數差唔係 +117：%d' % (len(new) - len(old))

def map_line(old_n):
    """舊行號 → 新行號：舊行內容（去首尾空白）喺新檔預期位置 ±6 行內唯一出現。"""
    content = old[old_n - 1].strip()
    assert content, '舊行 %d 係空行' % old_n
    # 預期漂移：按插入點逐段計
    exp = old_n
    if old_n >= 3849: exp += 2
    if old_n >= 30519: exp += 1
    if old_n >= 53246: exp += 1
    if old_n >= 53279: exp += 2
    if old_n >= 53549: exp += 107
    if old_n >= 58500: exp += 3
    if old_n >= 58684: exp += 1
    hits = [i + 1 for i in range(max(0, exp - 7), min(len(new), exp + 6))
            if new[i].strip() == content]
    assert len(hits) == 1, '釘行 %d 對位失敗（預期 %d，命中 %s）：%s' % (old_n, exp, hits, content[:80])
    assert hits[0] == exp, '釘行 %d 對位 %d ≠ 預期 %d' % (old_n, hits[0], exp)
    return hits[0]

def patch_numbers(path, mapping, note):
    """mapping: {old: new}；只改 line(N)／lines()[N-1]／lines[N-1] 出現處，逐粒核實次數。"""
    src = io.open(path, encoding='utf-8').read()
    for o, n in sorted(mapping.items()):
        for pat, fmt in ((r'line\(%d\)' % o, 'line(%d)' % n),
                         (r'lines\(\)\[%d\]' % (o - 1), 'lines()[%d]' % (n - 1)),
                         (r'lines\[%d\]' % (o - 1), 'lines[%d]' % (n - 1))):
            c = len(re.findall(pat, src))
            if c:
                src = re.sub(pat, fmt, src)
                print('  %s: %s ×%d → %s' % (path, pat, c, fmt))
    src = src.replace('# v20a182 resync：', note + '\n# v20a182 resync：', 1) if '# v20a182 resync：' in src else src
    io.open(path, 'w', encoding='utf-8').write(src)

NOTE183 = '# v20a183 resync：v183 淨 ＋117 行（C7 CSS ＋2／prefKind ＋1／TryIntercept ＋1／PlayEncounter ＋2／ROM183 block ＋107／確認 modal ＋3／goBit ＋1；difflib 對位核實純漂移，見 qa183/resync183.py）。'

# ---- kwan151：25617／25958／25961／25962／25963／26006／26225／27171／27204（+2，C7 之後）；
#      30970／30978／30979／31021（+3，C7＋prefKind） ----
kwan = [25617, 25958, 25961, 25962, 25963, 26006, 26225, 27171, 27204, 30970, 30978, 30979, 31021]
patch_numbers('tests/test_kwan151_static.py', {o: map_line(o) for o in kwan}, NOTE183)

# ---- tang152：25777（+2）；31460／31604（+3） ----
patch_numbers('tests/test_tang152_static.py', {o: map_line(o) for o in [25777, 31460, 31604]}, NOTE183)

# ---- rom176：6030（唔郁）；31533（+1）；53050／53415（+3）；54447／54541（+113） ----
patch_numbers('tests/test_rom176_static.py', {o: map_line(o) for o in [31533, 53050, 53415, 54447, 54541]}, NOTE183)

# ---- travel114：DEF／WRAPPER＋COUNT／FREE 全表 ----
def parse_set(src, name):
    m = re.search(name + r' = \{(.*?)\n\}', src, re.S)
    assert m, name + ' 搵唔到'
    out = []
    for ln in m.group(1).split('\n'):
        mm = re.match(r'\s*(\d+),?\s*(#.*)?$', ln)
        if mm:
            out.append((int(mm.group(1)), (mm.group(2) or '').strip()))
    return out

t114 = 'tests/test_travel114_static.py'
src = io.open(t114, encoding='utf-8').read()
count_old = parse_set(src, 'COUNT_LINES')
free_old = parse_set(src, 'FREE_LINES')
assert len(count_old) == 13 and len(free_old) == 33, 'COUNT/FREE 舊數唔啱：%d／%d' % (len(count_old), len(free_old))
count_new, free_new = [], []
for num, cm in count_old:
    if num == 59358:
        continue  # v183 C9：開局 intro 改行 travelFree，COUNT→FREE
    count_new.append((map_line(num), cm))
for num, cm in free_old:
    free_new.append((map_line(num), cm))
# C9 新 FREE 行：內容已改（openLoc(locId, {travelFree:true})），逐行核實
c9_new = 59358 + 117
assert 'openLoc(locId, {travelFree:true});' in new[c9_new - 1], 'C9 新行內容唔啱：%s' % new[c9_new - 1][:90]
free_new.append((c9_new, '# v183 C9 開局 intro「去睇劇情」掣（travelFree，唔計額度）'))
count_new.sort(); free_new.sort()
assert len(count_new) == 12 and len(free_new) == 34

def render_set(name, rows):
    body = '\n'.join('    %d,%s' % (n, ('  ' + c if c else '')) for n, c in rows)
    return '%s = {\n%s\n}' % (name, body)
src = re.sub(r'COUNT_LINES = \{.*?\n\}', render_set('COUNT_LINES', count_new), src, count=1, flags=re.S)
src = re.sub(r'FREE_LINES = \{.*?\n\}', render_set('FREE_LINES', free_new), src, count=1, flags=re.S)
src = src.replace('DEF_LINE = 54510      # function openLoc(id, opts){',
                  'DEF_LINE = %d      # function openLoc(id, opts){' % map_line(54510))
src = src.replace('WRAPPER_LINE = 44337  # window.__phase2.openLoc：轉發 opts',
                  'WRAPPER_LINE = %d  # window.__phase2.openLoc：轉發 opts' % map_line(44337))
src = src.replace('# 計清單（玩家主動導航，預設計數，唔加旗）：13 處',
                  '# 計清單（玩家主動導航，預設計數，唔加旗）：12 處（v183 C9：開局 intro 改行免費，59358→FREE）')
src = src.replace('# 免費清單（帶旗，唔計）：33 處（舊 27 減 2 條改行 back176 守衛，加 ROM176 新 8 處）',
                  '# 免費清單（帶旗，唔計）：34 處（舊 27 減 2 條改行 back176 守衛，加 ROM176 新 8 處＋v183 C9 intro 1 處）')
src = src.replace('# v20a176 第三輪 rebase 上 main c682cc2（v178）resync：',
                  NOTE183 + '\n# v20a176 第三輪 rebase 上 main c682cc2（v178）resync：', 1)
io.open(t114, 'w', encoding='utf-8').write(src)
print('  travel114: COUNT 13→12／FREE 33→34／DEF 54510→%d／WRAPPER 44337→%d／C9 59358→%d(FREE)'
      % (map_line(54510), map_line(44337), c9_new))

# ---- tang171／tang173：總行數 60010→60127、DEF 54510→新行；tang173 L4847→4849（C7 +2） ----
for f in ('tests/test_tang171_static.py', 'tests/test_tang173_static.py'):
    s = io.open(f, encoding='utf-8').read()
    assert "src.count('\\n') == 60010" in s, f + ' 總行數斷言搵唔到'
    s = s.replace("src.count('\\n') == 60010", "src.count('\\n') == 60127")
    s = s.replace("DEF 行 54510", "DEF 行 %d" % map_line(54510))
    s = s.replace("len(lines) >= 54510 and 'function openLoc(id, opts){' in lines[54509]",
                  "len(lines) >= %d and 'function openLoc(id, opts){' in lines[%d]" % (map_line(54510), map_line(54510) - 1))
    if 'tang173' in f:
        assert "lines[4846]" in s
        s = s.replace('L4847', 'L4849').replace('lines[4846]', 'lines[4848]')
    s = s.replace('# v20a182 resync：', NOTE183 + '\n# v20a182 resync：', 1) if '# v20a182 resync：' in s else s
    io.open(f, 'w', encoding='utf-8').write(s)
    print('  %s: 總行數→60127／DEF→%d' % (f, map_line(54510)))

print('resync 完成')
