# v20a206 B1 基線分析：模板短語計數＋全池逐句碰撞（beats tx + choice label + out，≥6 字成句）
import re, sys, collections
path = sys.argv[1] if len(sys.argv)>1 else 'index.html'
src = open(path, encoding='utf-8').read()
arr = re.search(r'DAILY_EVENTS_WF4\s*=\s*\[(.*?)\n\];', src, re.S)
chunks = {}
for chunk in re.split(r'(?=\{\s*id:"wf4_ev_)', arr.group(1)):
    im = re.match(r'\{\s*id:"(wf4_ev_\w+)"', chunk)
    if im: chunks[im.group(1)] = chunk
new_ids = ['wf4_ev_day%02d'%d for d in range(17,29)] + ['wf4_ev_set%02d'%s for s in range(26,55)]
print('events total:', len(chunks), 'new41 present:', sum(1 for i in new_ids if i in chunks))
phrases = ['話佢識','成個人鬆晒','聽到入晒神','識食','識做人','眉飛色舞']
for scope, ids in [('new41', new_ids), ('whole113', list(chunks))]:
    txt = ''.join(chunks[i] for i in ids if i in chunks)
    print(scope, {p: txt.count(p) for p in phrases})
# sentence extraction
def sents(chunk):
    out = []
    for tx in re.findall(r'tx:"([^"]*)"', chunk): out.append(tx)
    for lb in re.findall(r'label:"([^"]*)"', chunk): out.append(lb)
    for o in re.findall(r'out:"([^"]*)"', chunk): out.append(o)
    ss = []
    for t in out:
        for s in re.split(r'[。，、；！？\n]', t):
            s = s.strip()
            if len(s) >= 6: ss.append(s)
    return ss
by = collections.defaultdict(set)
for eid, ch in chunks.items():
    for s in set(sents(ch)): by[s].add(eid)
coll = {s: sorted(v) for s, v in by.items() if len(v) >= 2}
print('colliding sentences:', len(coll))
for s, evs in sorted(coll.items(), key=lambda kv: kv[1][0]):
    print('  [%s] %s' % (' / '.join(evs), s))
