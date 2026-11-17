#!/usr/bin/env python3
"""v20a278 resync 應用：將 qa278/resync278.py difflib 對位出嚟嘅新行號寫入 7 個測試檔。
原則（AGENTS.md）：單次掃描 dict 查表，唔逐對 re.sub；逐個核實內容逐字相同先填。
映射來源：python3 qa278/resync278.py <錨點…>（全部「內容逐字相同」）。
淨 +527 行（舊 45503 → 新 46030；GRANT229 +57 行在先，其後 DLG／ChoiceFx／BuildScript／registry）。
"""
import re

ROOT = '/home/hatch/workspace/linji-work278/'

# ---- travel114 映射（只列有變嘅；+0 唔郁）----
COUNT_MAP = {28008: 28067, 43990: 44517, 44202: 44729, 44360: 44887, 44381: 44908}
FREE_MAP = {27817: 27876, 27850: 27909, 38917: 39433, 39036: 39552, 39111: 39627,
            39319: 39835, 39363: 39879, 39369: 39885, 39436: 39952, 39438: 39954,
            39441: 39957, 39468: 39984, 40601: 41128, 40648: 41175, 41018: 41545,
            41040: 41567, 41192: 41719, 41197: 41724, 42119: 42646, 43597: 44124,
            43867: 44394, 43868: 44395, 43912: 44439, 43913: 44440, 43938: 44465,
            44831: 45358}
ROM176_MAP = {39119: 39635, 39477: 39993, 40638: 41165, 40794: 41321}


def replace_block_numbers(text, start_marker, end_marker, mapping, label):
    """喺 start_marker…end_marker 區間內，單次掃描將行首數字按 mapping 查表換走。"""
    i = text.index(start_marker)
    j = text.index(end_marker, i)
    block = text[i:j]
    n = [0]

    def _sub(m):
        old = int(m.group(2))
        if old in mapping:
            n[0] += 1
            return m.group(1) + str(mapping[old]) + ','
        return m.group(0)

    new_block = re.sub(r'^(\s*)(\d+),', _sub, block, flags=re.M)
    assert n[0] == len(mapping), '%s：只換咗 %d／%d 個' % (label, n[0], len(mapping))
    return text[:i] + new_block + text[j:]


def one(text, old, new, label, count=1):
    assert text.count(old) == count, '%s：錨點出現 %d 次（預期 %d）：%s' % (label, text.count(old), count, old[:60])
    return text.replace(old, new)


# ---------- 1. travel114 ----------
p = ROOT + 'tests/test_travel114_static.py'
s = open(p).read()
if 'DEF_LINE = 41280' in s:
    print('travel114 已套用，跳過')
else:
    s = replace_block_numbers(s, 'COUNT_LINES = {', '}\n# v20a158', COUNT_MAP, 'travel114 COUNT')
    s = replace_block_numbers(s, 'FREE_LINES = {', '}\nFREE_FLAGS', FREE_MAP, 'travel114 FREE')
    s = one(s, 'DEF_LINE = 40753', 'DEF_LINE = 41280', 'travel114 DEF')
    s = one(s, 'WRAPPER_LINE = 28577', 'WRAPPER_LINE = 28636', 'travel114 WRAPPER')
    s = one(s, '# v20a268 resync：',
            '# v20a278 resync：index.html 淨 +527 行（GRANT229_ENC79 ＋57／DLG 新 beats＋冷版＋heartCold／ChoiceFx 12 分支／BuildScript 變體／registry；見 qa278/resync278.py difflib 對位核實，58 處錨點內容逐字相同，純漂移；COUNT／FREE／DEF／WRAPPER 按段重算：＜26739 唔郁、26739–36902 ＋59、36903–40599 ＋516、≥40600 ＋527；DEF 40753→41280、WRAPPER 28577→28636；openLoc( 呼叫點總數不變）。\n# v20a268 resync：', 'travel114 header')
    open(p, 'w').write(s)
    print('travel114 ok')

# ---------- 2. rom176 ----------
p = ROOT + 'tests/test_rom176_static.py'
s = open(p).read()
for old_n, new_n in ROM176_MAP.items():
    # 只改四個 ok() 釘行入面嘅 line(N)：逐行搵，唔郁註解（regex 會撞 'rom176TryIntercept(id)' 入面個括號）
    lines = s.split('\n')
    hit = 0
    for idx, ln in enumerate(lines):
        if ln.startswith("ok('釘：") and ('line(%d)' % old_n) in ln:
            lines[idx] = ln.replace('line(%d)' % old_n, 'line(%d)' % new_n)
            hit += 1
    assert hit == 1, 'rom176 line(%d)：改咗 %d 處' % (old_n, hit)
    s = '\n'.join(lines)
s = one(s, '# v20a268 resync：',
        '# v20a278 resync：index.html 淨 +527 行；4 個釘行按 difflib 映射重算（39119→39635、39477→39993、40638→41165、40794→41321；內容逐字核實純漂移，見 qa278/resync278.py）。\n# v20a268 resync：', 'rom176 header')
open(p, 'w').write(s)
print('rom176 ok')

# ---------- 3/4. tang171 / tang173 ----------
for fname in ('tests/test_tang171_static.py', 'tests/test_tang173_static.py'):
    p = ROOT + fname
    s = open(p).read()
    # 總行數
    s = one(s, '總行數 45503（', '總行數 46030（', fname + ' total name')
    s = one(s, '＋v276 +1）\', src.count', '＋v276 +1＋v278 +527）\', src.count', fname + ' total chain')
    s = one(s, "src.count('\\n') == 45503", "src.count('\\n') == 46030", fname + ' total assert')
    # openLoc DEF
    s = one(s, 'openLoc DEF 行 40753（', 'openLoc DEF 行 41280（', fname + ' def name')
    s = one(s, '＋v276 +1，travel114 釘行）', '＋v276 +1＋v278 +527，travel114 釘行）', fname + ' def chain')
    s = one(s, 'len(lines) >= 40759', 'len(lines) >= 41286', fname + ' def guard')
    s = one(s, 'lines[40752]', 'lines[41279]', fname + ' def line')
    s = one(s, '# v20a267 resync：',
            '# v20a278 resync：index.html 淨 +527 行；總行數 45503→46030、openLoc DEF 40753→41280（鏈尾加 ＋v278 +527；標籤＋lines[] guard 一併更新），difflib 對位核實純漂移（見 qa278/resync278.py）。\n# v20a267 resync：', fname + ' header')
    open(p, 'w').write(s)
    print(fname + ' ok')

# ---------- 5. gift185 ----------
p = ROOT + 'tests/test_gift185_static.py'
s = open(p).read()
s = one(s, '總行數 45503（', '總行數 46030（', 'gift185 total name')
s = one(s, '＋v276 +1）\', html.count', '＋v276 +1＋v278 +527）\', html.count', 'gift185 total chain')
s = one(s, "html.count('\\n') == 45503", "html.count('\\n') == 46030", 'gift185 total assert')
open(p, 'w').write(s)
print('gift185 ok')

# ---------- 6. enc83_static ----------
p = ROOT + 'tests/test_enc83_static.py'
s = open(p).read()
old = "ok('提攜：八星 patron 節拍＋引薦債權齊', all(('credit_enc83_' + k + '_patron') in mod for k in ['luk','liu','mak','yip','ngai','gu','lok','chai']))"
new = ("# v20a278：魏提攜債權改行抉擇 fx——ngai_patron grants() 已拆，揀「照實講」先授（ngai_vouch handler 喺 RunChoiceFx，唔喺 ENC83 模組段內）；其餘七星照舊經 grants()，喺 mod 入面。\n"
       "ok('提攜：八星 patron 節拍＋引薦債權齊', all(('credit_enc83_' + k + '_patron') in mod for k in ['luk','liu','mak','yip','gu','lok','chai']) and 'if(fx===\"ngai_vouch\")' in src and 'enc79GrantCredit({ id:\"credit_enc83_ngai_patron\"' in src)")
s = one(s, old, new, 'enc83_static patron')
open(p, 'w').write(s)
print('enc83_static ok')

# ---------- 7. sideline158 T7 ----------
p = ROOT + 'tests/test_sideline158_logic.js'
s = open(p).read()
s = one(s, "ok('T7 全表 17 行（原 9＋新 8）', GRANT229_ENC79.length===17, 'n='+GRANT229_ENC79.length);",
        "ok('T7 全表 74 行（原 17＋v20a278 六線 57）', GRANT229_ENC79.length===74, 'n='+GRANT229_ENC79.length);", 'sideline158 T7 count')
s = one(s, 'GRANT229_ENC79.slice(9).every(r=>{ const g=gigById(r.gigId); return g && r.reason.indexOf(g.title)>=0; })',
        'GRANT229_ENC79.slice(9, 17).every(r=>{ const g=gigById(r.gigId); return g && r.reason.indexOf(g.title)>=0; })', 'sideline158 T7 reason slice')
open(p, 'w').write(s)
print('sideline158 ok')
print('ALL RESYNC APPLIED')
