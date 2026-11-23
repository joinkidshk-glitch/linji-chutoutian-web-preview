# v20a267 傳聞系統刪除靜態測試：傳聞頁／拼合／情報旗／舊注入路全部消失；新閘就位；紅線。
# 用法：python3 tests/test_rumor267_static.py [path-to-index.html]
import os, re, subprocess, sys, tempfile

path = sys.argv[1] if len(sys.argv) > 1 else 'index.html'
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

# ---- 傳聞系統消失（零殘留） ----
for ident in ['#home-pane-rumor', '#htab-rumor', 'renderRumorPane', 'mockRumors',
              'MERGE_PAIRS', 'INTEL_FLAGS', 'mergeIntelGigs', 'INTEL_HIDDEN_GIGS',
              'hasIntelFlag', 'ensureIntelFlags', 'hasMergedIntel', 'enc79GrantFrag',
              'enc79GrantRumorCard', 'wf3GrantRumor', 'mergeWf3Gigs', 'rumorStateLabel',
              'displayRumor', 'pushNewspaperRumor', 'SIDE_PAPER_FRAGS', 'EXODUS_RUMOR_SEEDS',
              'wf4SeedFrags', 'intelLineForGig', 'intelSightLineFor', 'rumor_gu_money_heard',
              'mockIntelHits', 'grantsRumorId', 'MERGE_FRAGS', 'MERGE_FLOW', 'INTEL_USE_POINTS',
              'INTEL_CARD_USE_POINTS89', 'br89HoldsCard', 'stepRumor', 'liveRumors',
              'rumorAny', 'rumorSoftPriority', 'rumorSeedsRequired', 'rumorHearHint',
              'rumorPlayerTitle', 'evalTrigger_AND_softRumor', 'STUB_RUMOR', 'rumorFrags',
              'MOCK_RUMOR_SEEDS', 'mockJournalSeeded']:
    ok('gone: ' + ident, ident not in html)

# ---- 傳聞頁 CSS／HTML 一併清走 ----
ok('no .rumor-hint rule', '.rumor-hint' not in html)
ok('no .rumor-card rule', '.rumor-card' not in html)
ok('no rumor tab group entry', 'rumor:"news"' not in html and 'news:"rumor"' not in html)

# ---- 情報站就位 ----
ok('intelAsked record exists', 'intelAsked' in html)
ok('MOCK_ASK carries intelText (v389 dedupe: 4)', html.count('intelText:"') >= 4)
ok('ask-result modal title', '打聽到情報' in html)
ok('whisper state kept', 'S.starWhispers' in html and 'enc79GrantWhisper' in html)
ok('paper whisper wiring', 'enc79PaperWhisper' in html and 'side_lu_concert' in html)

# ---- W3_ho_liao：改閘做廖炳星 enc79 tier ≥1（星好感，唔係 S.npcs） ----
w3 = seg('W3_ho_liao: { loc:"agency_ho"', 'W3_ho_m27')
ok('W3_ho_liao avail reads liu_bingxing star fav',
   'enc79StarState("liu_bingxing")' in w3 and 'enc79TierOf' in w3)
ok('W3_ho_liao when rewritten', 'when:"識咗廖炳星之後"' in html)
ok('W3_ho_liao no intel flag', 'hasIntelFlag' not in w3 and 'intel_liao_money' not in w3)
ok('W3_ho_liao GRANT229 mapping kept',
   '"W3_ho_liao:W3_ho_liao_a"' in html and 'gig_1990_tv_209' in html)

# ---- N8_d：無條件出現 ----
prep = seg('function wf3PrepareNode82(node){', 'function wf3SettleTick()')
ok('N8_d unconditional (no intel gate)', 'intel_yip_truth' not in prep and 'N8_d' in prep)
ok('N8_d dedupe kept', 'c.id==="N8_d"' in prep)
ok('yip echo reads flag_yip_warned82', 'flag_yip_warned82' in html)

# ---- 星夜迷離：通用 trigger（rel／luk_baakyin／25）＋trigger 讀星好感 ----
gigs = open(os.path.join(os.path.dirname(path) or '.', 'content', 'gigs_new.json'), encoding='utf-8').read()
ok('gig_1991_tv_203 trigger rel/luk/25',
   '"gig_1991_tv_203"' in gigs and '"kind": "rel"' in gigs and '"npcId": "luk_baakyin"' in gigs and '"relMin": 25' in gigs)
trig = seg('function triggerGigOn(g){', 'function triggerGigLabel229(g){')
ok('triggerGigOn rel reads star fav', 'enc79StarState' in trig and 'S.stars' in trig)

# ---- Q6：忠告改記旗 ----
ok('Q6 chung advice flag', 'chungAdviceHeld229' in html)
ok('Q6 no rumor card id', 'rumor_chung_advice' not in html)

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
