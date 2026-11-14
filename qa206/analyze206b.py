# 。級成句（split on 。！？；）＋成個 out/label 全文
import re, sys, collections
path = sys.argv[1] if len(sys.argv)>1 else 'index.html'
src = open(path, encoding='utf-8').read()
arr = re.search(r'DAILY_EVENTS_WF4\s*=\s*\[(.*?)\n\];', src, re.S)
chunks = {}
for chunk in re.split(r'(?=\{\s*id:"wf4_ev_)', arr.group(1)):
    im = re.match(r'\{\s*id:"(wf4_ev_\w+)"', chunk)
    if im: chunks[im.group(1)] = chunk
def sents(chunk):
    ss = []
    for t in re.findall(r'(?:tx|label|out):"([^"]*)"', chunk):
        for s in re.split(r'[。！？；]', t):
            s = s.strip()
            if len(s) >= 6: ss.append(s)
        if len(t.strip()) >= 6: ss.append(t.strip())  # 全文
    return ss
by = collections.defaultdict(set)
for eid, ch in chunks.items():
    for s in set(sents(ch)): by[s].add(eid)
coll = {s: sorted(v) for s, v in by.items() if len(v) >= 2}
print('colliding 。-sentences:', len(coll))
for s, evs in sorted(coll.items(), key=lambda kv: kv[1][0]):
    print('  [%s] %s' % (' / '.join(evs), s))
