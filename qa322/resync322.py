# v20a322 resync：index.html 淨 +4 行（lok_patron 引薦句變體：舊 L40194 一行
#   if(v278) ... → 新 5 行（v322 註解＋const v322＋stand push＋v278 push＋if(v322.length) ...）；
#   舊 L40194 之後全部 +4，之前唔郁。difflib 對位核實純漂移，見下。
# 用法：python3 qa322/resync322.py [old-index] [new-index]
import difflib, sys
old_path = sys.argv[1] if len(sys.argv) > 1 else '/home/hatch/workspace/linji-repo/index.html'
new_path = sys.argv[2] if len(sys.argv) > 2 else '/home/hatch/workspace/linji-work322/index.html'
old = open(old_path, encoding='utf-8').read().splitlines()
new = open(new_path, encoding='utf-8').read().splitlines()
print('old lines:', len(old), 'new lines:', len(new), 'delta:', len(new) - len(old))
assert len(new) - len(old) == 4, 'net delta must be +4'
sm = difflib.SequenceMatcher(a=old, b=new, autojunk=False)
hunks = [op for op in sm.get_opcodes() if op[0] != 'equal']
print('non-equal opcodes:', hunks)
assert len(hunks) == 1, 'must be exactly one hunk'
tag, i1, i2, j1, j2 = hunks[0]
assert tag == 'replace' and (i2 - i1) == 1 and (j2 - j1) == 5, 'hunk must be 1 old line -> 5 new lines'
print('replaced old line %d: %s' % (i1 + 1, old[i1][:100]))
assert old[i1].strip().startswith('if(v278) beatSeg100'), 'replaced line must be the v278 insert line'
for k in range(j1, j2):
    print('  new line %d: %s' % (k + 1, new[k][:100]))
assert 'v20a322' in new[j1] and 'lok_stand_original' in new[j1 + 2], 'new block must be the v322 insert'

# 釘行對位：舊行內容 == 新行（舊+4）內容，純漂移
def check(old_no, new_no=None):
    if new_no is None:
        new_no = old_no + 4
    a, b = old[old_no - 1], new[new_no - 1]
    ok = a == b
    print(('PASS' if ok else 'FAIL'), 'old L%d -> new L%d :: %s' % (old_no, new_no, a.strip()[:80]))
    return ok

fails = []
# travel114 COUNT（>40194 者 +4）
for n in (45771, 45979, 46137, 46158):
    fails += [] if check(n) else [n]
# travel114 FREE（>40194 者 +4）
for n in (40525, 40644, 40719, 40919, 40963, 40969, 41036, 41038, 41041, 41068,
          42343, 42390, 42760, 42782, 42934, 42939, 43864, 45341, 45648, 45649,
          45693, 45694, 45719, 46608):
    fails += [] if check(n) else [n]
# travel114 DEF +4；WRAPPER 唔郁（<40194）
fails += [] if check(42495) else [42495]
fails += [] if check(29108, 29108) else [29108]
# tang171/173 DEF
fails += [] if check(42495) else ['DEF']
# rom176 釘行（>40194 者 +4；6321／14781 唔郁）
for n in (40727, 41077, 42380, 42536):
    fails += [] if check(n) else [n]
fails += [] if check(6321, 6321) else [6321]
fails += [] if check(14781, 14781) else [14781]
print('ANCHOR FAILURES:', fails if fails else 'none')
sys.exit(1 if fails else 0)
