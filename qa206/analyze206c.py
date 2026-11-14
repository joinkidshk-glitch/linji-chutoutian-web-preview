# 子串碰撞：任兩單之間共享 ≥N 字子串（beats tx + label + out），報最長者
import re, sys, collections, itertools
path = sys.argv[1] if len(sys.argv)>1 else 'index.html'
src = open(path, encoding='utf-8').read()
arr = re.search(r'DAILY_EVENTS_WF4\s*=\s*\[(.*?)\n\];', src, re.S)
chunks = {}
for chunk in re.split(r'(?=\{\s*id:"wf4_ev_)', arr.group(1)):
    im = re.match(r'\{\s*id:"(wf4_ev_\w+)"', chunk)
    if im: chunks[im.group(1)] = chunk
def texts(chunk):
    return re.findall(r'(?:tx|label|out):"([^"]*)"', chunk)
N = int(sys.argv[2]) if len(sys.argv)>2 else 10
ids = sorted(chunks)
found = []
for a, b in itertools.combinations(ids, 2):
    ta = ' | '.join(texts(chunks[a])); tb = ' | '.join(texts(chunks[b]))
    # longest common substring via DP on chars, cap: find all common substrings len>=N, keep maximal
    best = ''
    # simple approach: for each start in ta, extend while in tb
    for i in range(len(ta)):
        if ta[i] in ' |': continue
        j = 0
        while i+j < len(ta) and ta[i+j] in tb and ta[i+j] not in ' |':
            j += 1
        if j >= N and j > len(best):
            best = ta[i:i+j]
    if best:
        found.append((a, b, best))
print('pairs sharing >=%d-char substring: %d' % (N, len(found)))
for a, b, s in found:
    print('  [%s / %s] len=%d %s' % (a, b, len(s), s))
