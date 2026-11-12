# -*- coding: utf-8 -*-
"""v138 drive resolver v2：將 batch138_final.json 嘅 57 句證據對白定位到：
  ENC：ENC(79|83|84)_DLG_<star> 區塊內嘅 section 路徑（first / openers.Tn /
       beats.<id> / heart / address.<kind>），連同 choice label（若喺 choice
       分支入面，label 必須喺 section 開始之後）同 beat 前置（beats 段嘅
       need/req/after 欄）。
  PACK/LIVE：index.html 入面最近嘅節點 key；PACK 行以 batch 嘅 node_hint 為準。
輸出 qa138/drive138_plan.json。"""
import json, re

s = open('index.html', encoding='utf-8').read()
batch = json.load(open('qa138/batch138_final.json', encoding='utf-8'))

# ---- ENC star blocks (79/83/84) ----
blocks = {}
for m in re.finditer(r'const ENC(?:79|83|84)_DLG_([a-z_]+) = \{', s):
    blocks[m.group(1)] = m.start()
stars = sorted(blocks, key=lambda k: blocks[k])
print('ENC DLG stars:', stars)
spans = {}
import re as _re
_next_const = [m.start() for m in _re.finditer(r'\nconst ', s)]
for i, st in enumerate(stars):
    a = blocks[st]
    later = [p for p in _next_const if p > a]
    end = min([blocks[stars[i + 1]]] if i + 1 < len(stars) else []) if False else (later[0] if later else len(s))
    spans[st] = (a, end)

SECTION_RE = re.compile(
    r'(?P<beats>beats\.(?P<bid>[A-Za-z0-9_]+): \{)'
    r'|(?P<openers>openers: \{)'
    r'|(?P<t>T[0-4]): \['
    r'|(?P<heart>heart: \{)'
    r'|(?P<first>first: \{)'
    r'|(?P<address>address: \{)'
    r'|(?P<akind>(?:extra|support|lead|king)): \[')

def enc_section(star, pos):
    a, _ = spans[star]
    seg = s[a:pos]
    marks = []
    for m in SECTION_RE.finditer(seg):
        if m.group('beats'):
            marks.append((m.start(), 'beats.' + m.group('bid')))
        elif m.group('openers'):
            marks.append((m.start(), 'openers'))
        elif m.group('t'):
            marks.append((m.start(), 'T.' + m.group('t')))
        elif m.group('heart'):
            marks.append((m.start(), 'heart'))
        elif m.group('first'):
            marks.append((m.start(), 'first'))
        elif m.group('address'):
            marks.append((m.start(), 'address'))
        elif m.group('akind'):
            marks.append((m.start(), 'addr.' + m.group('akind')))
    if not marks:
        return '?', None, None
    # section = 最後一個「段」標記；T 標記要跟隨 openers
    sec = None
    sec_start = None
    for off, name in marks:
        if name.startswith('T.'):
            if sec == 'openers':
                sec = 'openers.' + name[2:]
                sec_start = off
        else:
            sec = name
            sec_start = off
    # choice label：section 開始之後最近嘅 label
    tail = seg[sec_start:] if sec_start is not None else seg
    labels = re.findall(r'label: "([^"]{1,40})"', tail)
    choice = labels[-1] if labels else None
    # beat 前置：beats 段開頭 600 字內嘅 need/req/after
    prereq = None
    if sec and sec.startswith('beats.'):
        head = seg[sec_start:sec_start + 600]
        mm = re.search(r'(?:need|req|after|pre)\s*:\s*(\[[^\]]*\]|"[^"]*"|\{[^\}]*\})', head)
        if mm:
            prereq = mm.group(0)[:200]
    return sec, choice, prereq

def live_node(pos):
    seg = s[:pos]
    keys = re.findall(r'\n  ([A-Za-z][A-Za-z0-9_]*): \{', seg)
    return keys[-1] if keys else None

plan = []
unresolved = []
for it in batch:
    for e in it['evidence']:
        text = e['text']
        probe = text[:25]
        hits = [m.start() for m in re.finditer(re.escape(probe), s)]
        rec = {'stem': it['stem'], 'speaker': it['speaker'], 'expr': it['expr'],
               'src': e['src'], 'node_hint': e['node'], 'category': e['category'],
               'text': text, 'hits': len(hits)}
        if not hits:
            rec['where'] = None
            unresolved.append(rec)
            plan.append(rec)
            continue
        pos = hits[0]
        if e['src'] == 'ENC':
            star = None
            for st in stars:
                a, b = spans[st]
                if a <= pos < b:
                    star = st
                    break
            if star is None:
                rec['where'] = {'star': None, 'note': 'outside ENC DLG blocks'}
                unresolved.append(rec)
            else:
                sec, choice, prereq = enc_section(star, pos)
                rec['where'] = {'star': star, 'section': sec, 'choice': choice,
                                'prereq': prereq}
                if star != it['speaker']:
                    rec['star_mismatch'] = star
        else:
            node = live_node(pos)
            rec['where'] = {'node': node}
            if e['node'] and node != e['node']:
                rec['node_mismatch'] = (e['node'], node)
        plan.append(rec)

json.dump(plan, open('qa138/drive138_plan.json', 'w', encoding='utf-8'),
          ensure_ascii=False, indent=1)
print('lines:', len(plan), 'unresolved:', len(unresolved))
for r in unresolved:
    print('UNRESOLVED', r['stem'], r['text'][:30])
for r in plan:
    print(f"{r['stem']:28s} {r['src']:4s} {json.dumps(r.get('where'), ensure_ascii=False)}")
