# v20a268 角色刪除靜態測試：Vera／鄧麗萍死檔／死條目／死引用零殘留；保留項在位；紅線。
# 刪咗嘅嘢：
#   (1) content/story_detail_romance_tang.json 成檔刪除（v152 已停載，v268 刪檔）；
#   (2) Vera 圖片 10 檔刪除（core bust 3＋silhouette 1＋fullbody 4＋npc_vera.jpg 2）；
#   (3) story_detail_romance_vera_hiu_choi.json 減 5 個 R_vera_* 節點（檔本身留返，hiu／choi 10 條在位）；
#   (4) index.html：WF2 覆寫表 Vera 5 條、STORY_MEET_SOFT R_vera_meet、SCENE_OVERRIDE154 R_vera_meet、
#       CONTRA98_WHEN_FIX R_vera_ending／R_vera_crisis 兩行＋R_tang_push2／R_tang_crisis 兩行（死項，見註）。
# 刻意保留（見 NOTES_V20A268）：WF2 表頭註解一句、tang_laiping 圖片、fixtures 凍結副本。
# v20a297 翻轉（見 NOTES_V20A297）：NPCS stylist／mei、gift_prefs vera、SP176 mei、kwan_hoimei 圖片、
#   結局／舊檔讀取位兩行全部已刪。
# 用法：python3 tests/test_delete268_static.py [path-to-index.html]
import json, os, re, subprocess, sys, tempfile

path = sys.argv[1] if len(sys.argv) > 1 else 'index.html'
ROOT = os.path.dirname(path) or '.'
html = open(path, encoding='utf-8').read()
fails = []
def ok(name, cond):
    print(('PASS ' if cond else 'FAIL ') + name)
    if not cond:
        fails.append(name)

def seg(start, end=None):
    try:
        i = html.index(start)
    except ValueError:
        return ''
    try:
        j = html.index(end, i) if end else len(html)
    except ValueError:
        j = min(len(html), i + 30000)
    return html[i:j]

# ---- (1) 刪檔唔存在 ----
for rel in ['content/story_detail_romance_tang.json',
            'assets/story/core/vera_bust_default.png',
            'assets/story/core/vera_bust_smile.png',
            'assets/story/core/vera_bust_frown.png',
            'assets/story/core/vera_silhouette_far.png',
            'assets/story/fullbody/vera_base.webp',
            'assets/story/fullbody/vera_smile.webp',
            'assets/story/fullbody/vera_serious.webp',
            'assets/story/fullbody/vera_angry.webp',
            'assets/npc_vera.jpg',
            'assets/dialog/npc_vera.jpg']:
    ok('gone file: ' + rel, not os.path.exists(os.path.join(ROOT, rel)))

# ---- (2) 檔名喺 index.html 零命中（npc_vera 係 PORTRAITS 鍵，唔係檔名——斷言完整檔名 npc_vera.jpg） ----
for fname in ['story_detail_romance_tang.json',
              'vera_bust_default.png', 'vera_bust_smile.png', 'vera_bust_frown.png',
              'vera_silhouette_far.png',
              'vera_base.webp', 'vera_smile.webp', 'vera_serious.webp', 'vera_angry.webp',
              'npc_vera.jpg']:
    ok('gone name in index: ' + fname, fname not in html)
ok('no loader call for tang pack', 'get("story_detail_romance_tang.json")' not in html)

# ---- (3) 已載入 pack：R_tang_* 節點只剩 live stub；R_vera_* 節點零個 ----
_loaded = ['content/story_detail_n1_to_n17.json', 'content/story_detail_romance_vera_hiu_choi.json',
           'content/story_detail_romance_lan_xu.json', 'content/story_detail_romance_yip_so.json',
           'content/story_detail_rival_mentor.json']
for rel in _loaded:
    d = json.load(open(os.path.join(ROOT, rel), encoding='utf-8'))
    ids = [n.get('id') for n in d.get('nodes', [])]
    ok('no R_vera_* node: ' + rel, not any(i and i.startswith('R_vera_') for i in ids))
    ok('R_tang_* only stub: ' + rel,
       [i for i in ids if i and i.startswith('R_tang_')] in ([], ['R_tang_meet_stub']))

# ---- (4) vera_hiu_choi.json：vera／Vera 零殘留＋nodes 10 條 hiu／choi ----
_vhc = json.load(open(os.path.join(ROOT, 'content', 'story_detail_romance_vera_hiu_choi.json'), encoding='utf-8'))
_vhc_ids = [n['id'] for n in _vhc.get('nodes', [])]
ok('vhc nodes 10 (hiu 5 + choi 5)', len(_vhc_ids) == 10
   and sorted(_vhc_ids) == sorted(['R_hiu_meet', 'R_hiu_push1', 'R_hiu_push2', 'R_hiu_crisis', 'R_hiu_ending',
                                    'R_choi_meet', 'R_choi_push1', 'R_choi_push2', 'R_choi_crisis', 'R_choi_ending']))
ok('vhc vera/Vera zero', 'vera' not in json.dumps(_vhc, ensure_ascii=False).lower())
ok('vhc version 1.3.2', _vhc.get('version') == '1.3.2')

# ---- (5) R_vera_ 喺四個區零殘留（WF2／SCENE_OVERRIDE／MEET_SOFT／CONTRA98） ----
_wf2 = seg('const ROMANCE_WF2_OVERRIDES = {', '\n};')
ok('WF2 region no R_vera_', 'R_vera_' not in _wf2 and '"R_lan_meet": {' in _wf2)
_sc = seg('const STORY_SCENE_OVERRIDE154 = {', '\n};')
ok('SCENE_OVERRIDE154 no R_vera_', 'R_vera_' not in _sc and '"R_hiu_ending":"bg_154_rooftop"' in _sc)
_ms = seg('const STORY_MEET_SOFT = {', '\n};')
ok('STORY_MEET_SOFT no R_vera_', 'R_vera_' not in _ms)
_c98 = seg('const CONTRA98_WHEN_FIX = {', '\n};')
ok('CONTRA98 no R_vera_', 'R_vera_' not in _c98)
ok('CONTRA98 no R_tang_push2/crisis (dead rows)', 'R_tang_push2' not in _c98 and 'R_tang_crisis' not in _c98
   and 'R_tang_meet_stub' in _c98)

# ---- (6) v297 翻轉：v268 刻意保留項已刪（WF2 表頭註解一句繼續留返） ----
ok('kept: WF2 header comment notes vera deletion', 'R_vera_* 5 條已刪' in html)
ok('gone: endingDual410/commit48 vera old-save reads (v297)',
   html.count('vera: line("R_vera_meet", "rel_vera", "R_vera_crisis", "flag_vera_commit")') == 0)
ok('gone: NPCS stylist + mei (v297)', '  stylist:{' not in html and '  mei:{' not in html)
ok('gone: rom176MeiUnlocked (v297)', 'rom176MeiUnlocked' not in html)
_gift = json.load(open(os.path.join(ROOT, 'content', 'gift_prefs.json'), encoding='utf-8'))
ok('gone: gift_prefs vera entry (v297)', 'vera' not in _gift.get('npcs', {}))
_sp176 = seg('const SP176 = {', '\n      };')
ok('gone: SP176 mei entry (v297)', 'mei:{' not in _sp176)
for rel in ['assets/story/core/tang_laiping_bust_default.png',
            'assets/story/fullbody/tang_laiping_base.webp']:
    ok('kept file: ' + rel, os.path.exists(os.path.join(ROOT, rel)))
for rel in ['assets/story/fullbody/kwan_hoimei_base.webp',
            'assets/story/fullbody/kwan_hoimei_serious.webp']:
    ok('gone file: ' + rel, not os.path.exists(os.path.join(ROOT, rel)))

# ---- (7) tang 檔名喺已載入 JSON 只剩 metadata 字串（唔係載入路徑） ----
# 容許嘅欄位：alignedWith／supersededByFile／notes_tang／oldRomanceRef／rule 敘述；其餘出現即 FAIL。
_tang_hits = []
# v20a358：兩個 MEET mock 已成檔刪除，唔再列入檢查清單（檔已刪，冇嘢好查）。
for rel in _loaded:
    txt = open(os.path.join(ROOT, rel), encoding='utf-8').read()
    for m in re.finditer(r'story_detail_romance_tang\.json', txt):
        ctx = txt[max(0, m.start() - 200):m.start()]
        if not re.search(r'"(alignedWith|supersededByFile|notes_tang|oldRomanceRef|rule)":\s*"[^"]*$', ctx):
            _tang_hits.append(rel + '@' + str(m.start()))
ok('tang filename in loaded JSON only in metadata strings', not _tang_hits)
if _tang_hits:
    print('   unexpected tang hits: ' + ' | '.join(_tang_hits))

# ---- 紅線 ----
ok('SAVE key intact', html.count('starVolunteer_map_v19w') == 10)
ok('product ?v= intact', html.count('"v20a10"') == 7)
ok('softRev marker intact (s107)', 's107' in html)
style = html.split('<style', 1)[1].split('</style>', 1)[0]
ok('style braces balanced', style.count('{') == style.count('}'))

# ---- node --check（抽第二個 script block） ----
scripts = re.findall(r'<script>(.*?)</script>', html, re.S)
ok('two script blocks found', len(scripts) >= 2)
if len(scripts) >= 2:
    with tempfile.NamedTemporaryFile('w', suffix='.js', delete=False, encoding='utf-8') as tf:
        tf.write(scripts[1])
        tmp = tf.name
    try:
        r = subprocess.run(['node', '--check', tmp], capture_output=True, text=True)
        ok('node --check main script', r.returncode == 0)
        if r.returncode != 0:
            print(r.stderr[:500])
    finally:
        os.unlink(tmp)

print('FAILURES: ' + ' | '.join(fails) if fails else 'ALL PASS')
sys.exit(1 if fails else 0)
