# v20a131 B3 殺青反響第三卡藍底 → 統一米色・靜態守門測試。
# 用法：python3 tests/test_ui131b3_static.py [path-to-index.html]
# 對 pristine main 行 → 藍色值仍在 → 乾淨 FAIL（唔 crash）。
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

# 取出 .psr-card.psr-news 規則本體
m = re.search(r'\.psr-card\.psr-news\{[^}]*\}', html)
rule = m.group(0) if m else ''
ok('psr-news 規則存在', bool(m))

# 藍色唔見：淺藍漸變兩值＋藍邊全部清零
ok('psr-news 無淺藍漸變上值 rgba(235,244,255', '235,244,255' not in rule)
ok('psr-news 無淺藍漸變下值 rgba(220,234,250', '220,234,250' not in rule)
ok('psr-news 無藍邊 rgba(60,100,140', '60,100,140' not in rule)

# 統一米色：跟返 .psr-press 同款邊色，背景繼承 .psr-card 預設米色漸變
ok('psr-news 邊色跟 press 同款米啡 rgba(120,90,40,.4)', 'border-color:rgba(120,90,40,.4)' in rule)
ok('psr-news 無獨立 background 覆寫（繼承 .psr-card 米色）', 'background:' not in rule)
ok('.psr-card 預設米色漸變不變',
   'background:linear-gradient(180deg,rgba(255,248,230,.92),rgba(255,240,210,.78))' in html)

# 唔郁範圍：粉卡 psr-streetFans 照舊
ok('psr-streetFans 粉色不變（唔喺 B3 範圍）',
   '.psr-card.psr-streetFans{ border-color:rgba(160,60,80,.35); background:linear-gradient(180deg,rgba(255,236,240,.92),rgba(255,224,230,.78)); }' in html)

# 反證：喺規則入面加返藍漸變，藍色斷言必須轉 False
def news_has_no_blue(s):
    mm = re.search(r'\.psr-card\.psr-news\{[^}]*\}', s)
    r = mm.group(0) if mm else ''
    return ('235,244,255' not in r) and ('220,234,250' not in r) and ('60,100,140' not in r)
ok('反證：加返藍漸變後 news_has_no_blue 必須轉 False',
   news_has_no_blue(html) and not news_has_no_blue(
       html.replace('.psr-card.psr-news{ border-color:rgba(120,90,40,.4); }',
                    '.psr-card.psr-news{ border-color:rgba(60,100,140,.35); background:linear-gradient(180deg,rgba(235,244,255,.9),rgba(220,234,250,.75)); }')))

print('TOTAL %s' % ('PASS' if not fails else 'FAIL: ' + ', '.join(fails)))
sys.exit(1 if fails else 0)
