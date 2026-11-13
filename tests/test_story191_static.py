# -*- coding: utf-8 -*-
# v20a191 靜態測試：C6F 幕號問題——A 進度頁唔再將插入幕排做第 20 幕＋B 場景頂加幕號。
# A：storyActLabel 係唯一幕號來源（C6／C6F 路線雙生、對稱後綴；C18／C19 時間錨番外）；
#    order71 顯示次序跟播次序 ORDER165，內部 n 保留供 far-merge／逐項揭曉邏輯用；
#    進度頁四行模板＋前置句＋地圖下一幕提示全部行共用 label。
# B：StoryPlay 開場 head 加幕號行（storyActLabel＋prog71Title），只限主線幕；
#    .sp-act191 樣式在位。
# 反證：喺 pristine main（v187）index 上行，A／B 新斷言要乾淨 FAIL（唔 crash）；
#      其餘基線斷言（SAVE／softRev／?v=／ORDER165 不變）喺 pristine 一樣 PASS。
# 用法：python3 tests/test_story191_static.py [path-to-index.html]
import re
import sys
from pathlib import Path

p = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent.parent / 'index.html'
src = p.read_text(encoding='utf-8')
root = p.parent
fails = []


def ok(name, cond):
    print(('PASS ' if cond else 'FAIL ') + name)
    if not cond:
        fails.append(name)


def func_body(src_text, fname):
    """抽一段 function fname(...) { ... }（由宣告行起到下一個同級 function 為止）。"""
    m = re.search(r'function ' + re.escape(fname) + r'\b', src_text)
    if not m:
        return ''
    start = m.start()
    m2 = re.search(r'\n  function ', src_text[start + 10:])
    return src_text[start:start + 10 + m2.start()] if m2 else src_text[start:]


def func_body_braces(src_text, fname):
    """抽一段頂層 function（大括號計數，唔受下一個 function 縮排影響）。"""
    m = re.search(r'function ' + re.escape(fname) + r'\b', src_text)
    if not m:
        return ''
    j = src_text.index('{', m.start())
    depth = 0
    for k in range(j, len(src_text)):
        if src_text[k] == '{':
            depth += 1
        elif src_text[k] == '}':
            depth -= 1
            if depth == 0:
                return src_text[m.start():k + 1]
    return ''


# --- 基線不變 ---
ok('SAVE key／softRev／?v= 不變', 'starVolunteer_map_v19w' in src and 's107' in src and 'v20a10' in src)
ok('ORDER165 播次序不變（C6、C6F、C18、C19、C7…；強制播候選唔郁）',
   'const ORDER165 = ["C1","C2","C3","C4","C5","C6","C6F","C18","C19","C7"' in src)
ok('開放條件／閘唔郁', 'C6F: { route: "route_film", weekMin: 15 }' in src
   and 'C18: { needDone: ["C5"], weekMin: 48, yearMin: 1990, seasonIn: ["冬"] }' in src
   and 'C19: { needDone: ["C18"], weekMin: 61, yearMin: 1991, seasonIn: ["春"] }' in src)

# --- A：共用幕號函數 ---
label_body = func_body_braces(src, 'storyActLabel')
ok('A：storyActLabel 定義（唯一幕號來源）', 'function storyActLabel(id){' in src)
ok('A：C6／C6F 路線雙生、對稱後綴', 'if(s==="C6") return "第 6 幕・電視線";' in label_body
   and 'if(s==="C6F") return "第 6 幕・電影線";' in label_body)
ok('A：C18／C19 時間錨番外（跟 CALIB60 whenLabel：1990 年冬／1991 年春）',
   'if(s==="C18") return "番外・1990 冬";' in label_body
   and 'if(s==="C19") return "番外・1991 春";' in label_body
   and 'C18: { year:1990, seasons:["冬"], whenLabel:"1990 年冬" }' in src
   and 'C19: { year:1991, seasons:["春"], whenLabel:"1991 年春" }' in src)
ok('A：主幹 C1–C17 用順序號、非主線回空字串', 'if(n>=1 && n<=17) return "第 "+n+" 幕";' in label_body
   and '\n  return "";' in label_body)
ok('A：storyActIsInsert 只認 C6F／C18／C19', 'function storyActIsInsert(id){' in src
   and 'return id==="C6F" || id==="C18" || id==="C19";' in src)

# --- A：進度頁次序＋行模板 ---
m = re.search(r'const order71 = \[(.*?)\];', src, re.S)
pairs = re.findall(r'\[\s*"([^"]+)"\s*,\s*(\d+)\s*\]', m.group(1)) if m else []
ok('A：order71 抽到 20 項', len(pairs) == 20)
ok('A：order71 顯示次序跟播次序（C6、C6F、C18、C19、C7–C17）',
   [i for i, _ in pairs] == ['C%d' % n for n in range(1, 7)] + ['C6F', 'C18', 'C19'] + ['C%d' % n for n in range(7, 18)])
ok('A：order71 內部 n 保留 1–20（供 far-merge／逐項邏輯用，唔係顯示幕號）',
   sorted(int(n) for _, n in pairs) == list(range(1, 21)))
ok('A：prog71Rows 行帶 label（storyActLabel 來源）', 'label:storyActLabel(id)' in src)
rp = func_body(src, 'renderProgressPane71')
ok('A：進度頁四行模板用 r.label（唔再寫死「第 "+r.n+" 幕」）',
   rp.count('r.label || ("第 "+r.n+" 幕")') == 4 and "'第 '+r.n+' 幕'" not in rp)
ok('A：鎖住未揭曉嘅插入幕唔觸發合併行（guard 在位）',
   'if(storyActIsInsert(r.id)) return;' in rp)
ok('A：遠幕合併 fallback 保留（farNs 空嗰陣跳過）', 'if(!farNs.length) return;' in rp)
ok('A：逐項揭曉閾值邏輯保留（lastDetailN71）',
   'lastDetailN71 >= (r.n|0) - 1' in rp and 'lastDetailN71' in rp)
ok('A：v153 B3 原意已處理（播呢幕掣 v165 已拎走，註解有交代）',
   'v20a191 supersedes v20a153 B3' in src and 'v165 拎走咗' in src)

# --- A：前置句＋地圖提示同一來源 ---
ok('A：前置句行共用幕號（prog71GateItems＋prog71StubItems）',
   func_body(src, 'prog71GateItems').count('storyActLabel(d)') >= 1
   and func_body(src, 'prog71StubItems').count('storyActLabel(d)') >= 1)
ok('A：前置句舊寫法「先完成第 "+dn+" 幕」已拎走',
   '"先完成第 "+dn+" 幕' not in src)
ok('A：地圖下一幕提示行共用幕號（storyMainProgressLine）',
   'storyActLabel(openMain.id)' in func_body(src, 'storyMainProgressLine')
   and 'storyActLabel(id)' in func_body(src, 'storyMainProgressLine'))
ok('A：地圖提示舊寫法已拎走', 'const actN = Number(id.replace(/^C/,""))||0;' not in src
   and '(`第 ${n} 幕〈${t}〉已經開咗`)' not in src)

# --- B：場景頂幕號 ---
sp = src[src.index('const StoryPlay = (()=>{'):src.index('const StoryPlay = (()=>{') + 120000] if 'const StoryPlay = (()=>{' in src else ''
ok('B：StoryPlay 開場 head 用 storyActLabel（同進度頁同一來源）',
   'storyActLabel(n.id)' in sp)
ok('B：StoryPlay 幕號行加埋進度頁標題（prog71Title，唔係淨拼數字落節點 title）',
   'prog71Title(n.id)' in sp and 'sp-act191' in sp)
ok('B：幕號行格式係「標籤：進度頁標題」', '${esc(actLabel191)}：${esc(actTitle191)}' in sp)
ok('B：.sp-act191 樣式在位（mask scope 淺色＋!important，跟 v20a46 meta／h3 做法）',
   '#mask.story-play-on .story-play .sp-head .sp-act191{' in src
   and 'color:rgba(245,234,210,.95) !important' in
       [l for l in src.splitlines() if '.sp-act191{' in l][0]
   and 'text-shadow:0 1px 2px rgba(0,0,0,.6)' in
       [l for l in src.splitlines() if '.sp-act191{' in l][0])
ok('B：.sp-act191 冇深色 base rule（深啡壓喺深色場景圖上睇唔清，實駕 A_film 截圖證實）',
   '.story-play .sp-act191{color:#4a2e10' not in src)
ok('B：抉擇屏唔加 head（v128 A3 原意保留——抉擇屏唔留 .sp-head）',
   '抉擇屏唔留 .sp-head' in src)

print('FAILURES: ' + ' | '.join(fails) if fails else 'ALL PASS')
sys.exit(1 if fails else 0)
