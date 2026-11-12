# v20a131 B2 事業 tab 深藍底 → 統一做筆記紙・靜態守門測試。
# 用法：python3 tests/test_ui131b2_static.py [path-to-index.html]
# 對 pristine main 行 → 筆記紙規則缺席 → 乾淨 FAIL（唔 crash）。
import os, re, sys

path = sys.argv[1] if len(sys.argv) > 1 else 'index.html'
html = open(path, encoding='utf-8').read()
fails = []

def ok(name, cond):
    print(('PASS ' if cond else 'FAIL ') + name)
    if not cond:
        fails.append(name)

# 基線不變
ok('SAVE key 不變', 'starVolunteer_map_v19w' in html)
ok('softRev 不變', 's107' in html)
ok('產品 ?v= 不變', 'v20a10' in html)

# (1) 三頁 .journal-scroll 改米紙（同 .notebook 同一套：#f3e6c8＋金邊 #c4a574）
for pane in ['#home-pane-works', '#home-pane-awards', '#home-pane-memory']:
    ok('筆記紙規則覆蓋 %s .journal-scroll' % pane, (pane + ' .journal-scroll') in html)
ok('筆記紙底色 #f3e6c8', 'background:#f3e6c8; color:#2a2118;' in html)
ok('筆記紙金邊 #c4a574', 'border:2px solid #c4a574; border-bottom:0;' in html)

# (2) 拍攝簿 .req 列由深藍盒改紙卡（只命中 #works-list 直出嘅列，唔掂 .gig-card 內嘅 .req）
m = re.search(r'#home-pane-works #works-list > \.req\{[^}]*\}', html)
req_rule = m.group(0) if m else ''
ok('拍攝簿 .req 紙卡規則存在', bool(m))
ok('.req 紙卡淺米漸變', 'background:linear-gradient(180deg,#fbf2da,#f3e5c3)' in req_rule)
ok('.req 紙卡金邊 #d9c491', 'border:1px solid #d9c491' in req_rule)
ok('.req 紙卡無深藍底 #0d1828', '#0d1828' not in req_rule)
ok('.req 紙卡墨色字 #2a2118', 'color:#2a2118' in req_rule)
ok('.req 行內淺金字 #b3a284 改深墨 #6b4e2e',
   '#home-pane-works #works-list > .req div{ color:#6b4e2e !important; }' in html)
ok('.req 內 .gold #C9A227 改深金 #8a5a20', '#home-pane-works .gold{ color:#8a5a20; }' in html)

# (3) v76 深底淺字覆寫喺事業頁範圍內還原返紙面墨色
ok('jobs72-h 事業頁還原紙面墨色 #43301c', '#home-pane-works .jobs72-h{ color:#43301c; }' in html)
ok('works-empty59 h3 還原 --navy', '#home-pane-works .works-empty59 h3{ color:var(--navy); }' in html)
ok('mem-empty60／mem-head60 h3 還原 --navy',
   '#home-pane-memory .mem-empty60 h3, #home-pane-memory .mem-head60 h3{ color:var(--navy); }' in html)

# 唔郁範圍
ok('base .req 規則保留深藍盒（其他場合唔郁）',
   '.req{font-size:.78rem;background:#0d1828;' in html)
ok('.work-csscard59 海報代用卡深藍漸變不變（海報畫面本身，唔係頁底色）',
   '.work-csscard59{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;padding:12px;background:linear-gradient(160deg,#33355e,#1c1e38 70%)}' in html)
ok('副 tab 結構不變（作品／獎項／回憶）',
   'id="htab-works"' in html and 'id="htab-awards"' in html and 'id="htab-memory"' in html)
ok('拍攝簿渲染函數 jobs72SectionHtml 不變', 'function jobs72SectionHtml(){' in html)
ok('作品牆渲染函數 worksWallHtml59 不變', 'function worksWallHtml59(){' in html)

# 反證：紙底改返深藍，筆記紙斷言必須轉 False
def paper_ok(s):
    return ('#home-pane-works .journal-scroll' in s) and ('background:#f3e6c8; color:#2a2118;' in s)
ok('反證：紙底改返深藍後 paper_ok 必須轉 False',
   paper_ok(html) and not paper_ok(html.replace('background:#f3e6c8; color:#2a2118;', 'background:#0a1424; color:#ecdfc2;')))

print('TOTAL %s' % ('PASS' if not fails else 'FAIL: ' + ', '.join(fails)))
sys.exit(1 if fails else 0)
