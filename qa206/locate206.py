import re, sys
src = open('index.html', encoding='utf-8').read()
arr = re.search(r'DAILY_EVENTS_WF4\s*=\s*\[(.*?)\n\];', src, re.S)
chunks = {}
for chunk in re.split(r'(?=\{\s*id:"wf4_ev_)', arr.group(1)):
    im = re.match(r'\{\s*id:"(wf4_ev_\w+)"', chunk)
    if im: chunks[im.group(1)] = chunk
new_ids = ['wf4_ev_day%02d'%d for d in range(17,29)] + ['wf4_ev_set%02d'%s for s in range(26,55)]
for p in ['話佢識','成個人鬆晒','聽到入晒神','識食','識做人','眉飛色舞']:
    print('=== %s ===' % p)
    for eid in new_ids:
        ch = chunks[eid]
        for m in re.finditer(re.escape(p), ch):
            s = max(0, m.start()-28); e = min(len(ch), m.end()+28)
            print('  %s: ...%s...' % (eid, ch[s:e].replace('\n',' ')))
