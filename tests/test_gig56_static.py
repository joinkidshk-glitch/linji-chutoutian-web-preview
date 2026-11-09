# v20a56 散工修復 static tests: 冷卻/變體/改名區塊在位、接線齊、撞名已拆、
# 變體字串守 v20a55 時代詞彙標準、硬規則（SAVE key/softRev/經濟）冇郁。
# 反證: run against a pre-v56 index -> BRIDGE56 block missing -> FAIL.
import sys, re

src = open(sys.argv[1] if len(sys.argv) > 1 else 'index.html', encoding='utf-8').read()
fails = []

def chk(name, cond):
    print(('PASS ' if cond else 'FAIL ') + name)
    if not cond:
        fails.append(name)

# --- 區塊與接線 ---
a = src.find('/* ===== v20a56 散工修復')
b = src.find('function takeSoftBridgePay')
chk('BRIDGE56 block present', 0 <= a < b)
block = src[a:b] if 0 <= a < b else ''
chk('variants table present', 'const BRIDGE56_VARIANTS = {' in src)
chk('crossyear rename table present', 'const BRIDGE56_CROSSYEAR_RENAME = {' in src)
chk('cooldown const = 2 weeks', 'const BRIDGE56_COOLDOWN_WEEKS = 2;' in src)
chk('normalize hook wired', 'bridge56NormalizeGig(o)' in src and 'function normalizeGigRecord' in src)
chk('renew uses bcool', 'S.flags["bcool_"+g.id]' in src)
chk('renew bumps bvar on release', 'S.flags["bvar_"+g.id]' in src)
chk('starvation valve present', 'function bridge56StarvationValve()' in src)
chk('settleWeek still calls renew', 'try{ renewSoftBridgeGigs(); }catch(_rb){}' in src)

# --- 明碼化 ---
chk('card label: bridge-tag rendered', 'class="bridge-tag">常駐散工</span>' in src)
chk('card label: weekly note', '常駐散工 · 每週有工開' in src)
chk('card label css', '.gig-card .bridge-tag{' in src and '.gig-card .bridge-note{' in src)
chk('wrap copy: bridge wrap note', '常駐散工收工：呢單糧已入帳' in src)
chk('wrap copy: bridge title', '散工收工：${sh.title}' in src)

# --- 拆同名複本（1988 bridge base 改名） ---
chk('dup: 暑期跟組 only harbour', src.count('workTitle:"暑期跟組"') == 1 and 'title:"《暑期跟組》場務助手"' in src)
chk('dup: kowloon renamed 棚景組', 'workTitle:"暑期棚景組"' in src and 'title:"《暑期棚景組》場務助手"' in src)
chk('dup: adm renamed 暑期招牌', 'workTitle:"暑期招牌"' in src and 'title:"《暑期招牌》背景路人"' in src)
chk('dup: autumn central renamed 中環秋日招', 'workTitle:"中環秋日招"' in src and 'title:"《中環秋日招》廣告路人"' in src)
chk('dup: no second 暑期街招 workTitle', src.count('workTitle:"暑期街招"') == 1)
chk('dup: no second 秋日街招 workTitle', src.count('workTitle:"秋日街招"') == 1)

# --- 變體表完整性（30 張 bridge 卡 × 2）＋時代詞彙 ---
m = re.search(r'const BRIDGE56_VARIANTS = \{(.*?)\n\};', src, re.S)
vt = m.group(1) if m else ''
ids = re.findall(r'"(gig_1988_soft_bridge_[a-z_]+|g36_\d\d_brg_[a-z_]+)":', vt)
chk('variants: 30 bridge ids covered', len(ids) == 30)
pairs = re.findall(r'\["([^"]+)","([^"]+)"\]', vt)
chk('variants: 60 variant pairs', len(pairs) == 60)
banned = ['快閃', '截圖', '送命題', '帶貨', '喊麥', '粉絲', '上座率', '口播', '練習生', '街拍', '虛構', '電視城']
chk('variants: no anachronism words', not any(w in vt for w in banned))
titles = [t for _, t in pairs]
chk('variants: all titles unique', len(set(titles)) == len(titles))
chk('variants: titles wrapped in 《》', all(t.startswith('《') and '》' in t for t in titles))

# --- 跨年改名表 ---
for gid, frag in [('gig_1990_film_13', '霧港夜航'), ('gig_1990_rec_06', '起錨'), ('gig_1990_rec_07', '涼風'),
                  ('gig_1990_rec_08', '夏日口白試音'), ('gig_1990_rec_10', '年終合唱收聲'),
                  ('gig_1990_rec_11', '灣仔錄音室'), ('g36_90_brg_spr_wanchai', '灣仔和音新班'),
                  ('g36_90_brg_win_recstar', '賀歲歌錄音班')]:
    chk('xYear rename: ' + gid, gid in src and frag in src)

# --- 硬規則 ---
chk('SAVE key unchanged', 'starVolunteer_map_v19w' in src)
chk('economy: stipend $800 intact', 'return { pay:800, stipend:true };' in src)
chk('economy: bridge pay range intact', 'pay: [3400, 4000]' in src)
chk('no SAVE/softRev tampering markers', 'softRev' not in block)

if fails:
    print('FAILURES:', ' | '.join(fails))
    sys.exit(1)
print('ALL PASS')
