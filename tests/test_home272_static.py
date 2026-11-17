# v20a272 手帳 tab 死掣靜態測試：setHomeTab 殘留裸呼叫令成個手帳面板死晒。
# 背景：v267 刪傳聞系統嗰陣，刪走咗傳聞教學函數 applyPhase2Steps56TabLabel
#   嘅定義（佢只係幫已刪 #htab-rumor 設 label），但漏咗 setHomeTab 入面
#   嗰行裸呼叫。之後每次 setHomeTab 都掟 ReferenceError：頭三行就死，
#   tab 切換＋pane 渲染全部唔行；enterHome 喺 setHomeTab 之後先呼叫
#   renderNotebook，入屋流程喺嗰度斷埋——行程空白、瞓覺／衣櫃無接線、
#   saveQ 都唔行。返回地圖唔經 setHomeTab，所以獨善其身。
#   新存檔舊存檔一樣死（個函數根本唔存在，唔關存檔事）。
# 修復：刪走 setHomeTab 嗰行殘留呼叫；enterHome 嘅 setHomeTab 加 try/catch，
#   tab 失敗唔可以再拖死成個入屋流程。
# 用法：python3 tests/test_home272_static.py [path-to-index.html]
import os, re, subprocess, sys, tempfile

path = sys.argv[1] if len(sys.argv) > 1 else 'index.html'
ROOT = os.path.dirname(path) or '.'
html = open(path, encoding='utf-8').read()
fails = []
def ok(name, cond):
    print(('PASS ' if cond else 'FAIL ') + name)
    if not cond:
        fails.append(name)

def func_body(name):
    # 抽出 function NAME(...) {...} 全文（brace matching，唔靠 regex 尾）
    m = re.search(r'function\s+' + re.escape(name) + r'\s*\([^)]*\)\s*\{', html)
    if not m:
        return None
    i = m.end() - 1
    depth = 0
    for j in range(i, len(html)):
        c = html[j]
        if c == '{':
            depth += 1
        elif c == '}':
            depth -= 1
            if depth == 0:
                return html[m.start():j + 1]
    return None

# ---- (1) 殘留裸呼叫已清 ----
ok('no bare call applyPhase2Steps56TabLabel(', re.search(r'applyPhase2Steps56TabLabel\s*\(', html) is None)
ok('no bare call line with indent', '  applyPhase2Steps56TabLabel();' not in html)

# ---- (2) setHomeTab 本體完整在位 ----
st = func_body('setHomeTab')
ok('setHomeTab defined', st is not None)
if st is not None:
    ok('setHomeTab calls book70SyncTabGroups', 'book70SyncTabGroups(tab)' in st)
    ok('setHomeTab toggles panes', 'home-pane-' in st and 'classList.toggle("on"' in st)
    ok('setHomeTab covers all 11 panes', all(p in st for p in
       ['"plan"','"ledger"','"clippings"','"debt"','"people"','"tags"','"inv"','"works"','"awards"','"memory"','"progress"']))
    ok('setHomeTab syncs exit', 'syncHomeTabExit(tab)' in st)
    ok('setHomeTab renders ledger pane', 'renderLedgerPane()' in st)
    ok('setHomeTab renders works pane', 'renderWorksPane()' in st)

# ---- (3) 失敗類別回歸：setHomeTab 呼叫嘅每個頂層函數都要有定義 ----
# v272 教訓：一個未定義函數嘅裸呼叫可以靜默殺死成個 handler。呢度逐個核對。
BUILTINS = {'if','for','while','switch','catch','return','typeof','function','new','in','of',
            'parseInt','parseFloat','isNaN','isFinite','encodeURIComponent','decodeURIComponent',
            'setTimeout','setInterval','clearTimeout','clearInterval','console','Math','JSON',
            'Object','Array','String','Number','Boolean','Date','RegExp','Promise','Symbol',
            'require','module','exports','alert','confirm','prompt'}
def is_defined(name):
    if re.search(r'function\s+' + re.escape(name) + r'\s*\(', html):
        return True
    if re.search(r'(?:const|let|var)\s+' + re.escape(name) + r'\s*=', html):
        return True
    if re.search(re.escape(name) + r'\s*=\s*(?:async\s+)?function', html):
        return True
    if re.search(re.escape(name) + r'\s*=\s*\(', html):
        return True
    if re.search(r'window\.' + re.escape(name) + r'\s*=', html):
        return True
    return False
if st is not None:
    calls = set(re.findall(r'(?<![\w$.\"\'`])\b([A-Za-z_$][\w$]*)\s*\(', st))
    calls -= BUILTINS
    missing = sorted(c for c in calls if not is_defined(c))
    ok('setHomeTab calls all resolve to definitions (missing: %s)' % (','.join(missing) or 'none'),
       not missing)

# ---- (4) enterHome 嘅 setHomeTab 有防禦，唔可以再拖死入屋流程 ----
eh = func_body('enterHome')
ok('enterHome defined', eh is not None)
if eh is not None:
    ok('enterHome guards setHomeTab', re.search(r'try\s*\{\s*setHomeTab\(_homeTab\);\s*\}\s*catch', eh) is not None)
    ok('enterHome still calls renderNotebook after setHomeTab',
       eh.index('setHomeTab') < eh.index('renderNotebook()'))

# ---- (5) 瞓覺／衣櫃接線路徑完整在位 ----
ok('sleep button id present', 'id="btn-sleep265"' in html)
ok('wardrobe button id present', 'id="btn-wardrobe265"' in html)
ok('wireHome265 defined', func_body('wireHome265') is not None)
ok('renderNotebook calls wireHome265', 'wireHome265();' in html)
ok('costume265Sleep defined', func_body('costume265Sleep') is not None)
ok('costume265SleepAvailable defined', func_body('costume265SleepAvailable') is not None)

# ---- (6) node --check 主 script（第二個 script block） ----
scripts = re.findall(r'<script>(.*?)</script>', html, re.S)
ok('two script blocks extractable', len(scripts) == 2)
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
else:
    ok('node --check main script', False)

# ---- (7) 紅線：SAVE key／softRev／產品 ?v= 不變 ----
ok('SAVE key starVolunteer_map_v19w present', 'starVolunteer_map_v19w' in html)
ok('softRev s107 present', 's107' in html)
ok('product ?v=v20a10 present', 'v20a10' in html)

print('FAILURES: ' + ' | '.join(fails) if fails else 'ALL PASS')
sys.exit(1 if fails else 0)
