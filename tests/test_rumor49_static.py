# v20a49 傳聞頁提示行對比靜態測試：.rumor-hint 作用域修復＋base 原樣＋紅線。
# 用法：python3 tests/test_rumor49_static.py [path-to-index.html]
import sys

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

# ---- 出事元素同根因標記 ----
base = seg('.rumor-hint{', '}')
ok('base rumor-hint rule present (dark text, no bg)', 'color:#6b4e2e' in base and 'background' not in base)
ok('rumor-hint rendered only in rumor pane paths', html.count('class="rumor-hint"') == 2)
ok('hint copy present', '點兩張剛聽聞，拉埋再確認。' in html)

# ---- v49 作用域修復 ----
v49 = seg('/* === v20a49 傳聞頁提示行對比', '/* === v20a49 完 === */')
rule = seg('#home-pane-rumor .rumor-hint{', '}', ) if '#home-pane-rumor .rumor-hint{' in v49 else ''
ok('scoped rule inside v49 segment', bool(rule))
ok('scoped solid paper bg', 'background:#fff8e8' in rule)
ok('scoped dark readable text', 'color:#3a2a18' in rule)
ok('scoped gold border matches pane-intro fix language', 'border:1px solid rgba(201,162,39,.65)' in rule)
ok('scoped padding/radius match pane-intro geometry', 'padding:6px 8px' in rule and 'border-radius:8px' in rule)

# ---- 作用域冇波及其他頁 ----
ok('scoped rule appears exactly once', html.count('#home-pane-rumor .rumor-hint') == 1)
ok('no debt-pane rumor-hint override', '#home-pane-debt .rumor-hint' not in html)
ok('no global rumor-hint recolor', html.count('.rumor-hint{') == 2)  # base 一條＋作用域一條，冇第三條
ok('weak-whisper untouched (different class, intentional faint flavor)', '.weak-whisper{' in html and '#home-pane-rumor .weak-whisper' not in html)
ok('v48 pane-intro fix still in place', '#home-pane-rumor .pane-intro' in html)

# ---- 紅線 ----
ok('SAVE key intact', html.count('starVolunteer_map_v19w') == 10)
ok('product ?v= intact', html.count('"v20a10"') == 7)
ok('softRev marker intact', 's110' in html)
style = html.split('<style', 1)[1].split('</style>', 1)[0]
ok('style braces balanced', style.count('{') == style.count('}'))

print('FAILURES: ' + ' | '.join(fails) if fails else 'ALL PASS')
sys.exit(1 if fails else 0)
