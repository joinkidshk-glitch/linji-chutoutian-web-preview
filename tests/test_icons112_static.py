# v20a112 ICONS112 圖標組・靜態測試：26 隻圖標入庫＋逐面換 emoji 做 <img>／CSS＋S-46 進度格＋紅線。
# 用法：python3 tests/test_icons112_static.py [path-to-index.html]
# 反證：對基線 546007d（未換版）跑，換圖斷言全部 FAIL（見 NOTES_V20A112_ICONS.md §5）。
import os, sys, json, re

path = sys.argv[1] if len(sys.argv) > 1 else 'index.html'
root = os.path.dirname(os.path.abspath(path))
html = open(path, encoding='utf-8').read()
fails = []
def ok(name, cond):
    print(('PASS ' if cond else 'FAIL ') + name)
    if not cond:
        fails.append(name)

# ---- 1. 中央對照＋helper 存在 ----
ok('helper EMOJI_ICON112 defined', 'const EMOJI_ICON112 = {' in html)
ok('helper iconHtml112 defined', 'function iconHtml112(v){' in html)
ok('helper favDots112 defined', 'function favDots112(n){' in html)
m = re.search(r'const EMOJI_ICON112 = \{([^}]*)\}', html)
ok('helper map parses', bool(m))
stems = set(re.findall(r'"([a-z_]+)"', m.group(1))) if m else set()
for stem in ['map','sleep','mic','tea','clapper','fitness','home','news','gift','hospital',
             'music','people','tv','radio','lion','briefcase','building','mask','book',
             'martial','broom','sick','phone','mood','star','sparkle',
             'trophy','gift_pineapple','gift_eggtart','gift_thermos','gift_hairclip',
             'gift_memopad','gift_cassette','gift_sweetbox','gift_perfume',
             'gift_pen','gift_calculator','gift_watch','gift_rose']:
    ok('map has stem ' + stem, stem in stems)
ok('map has 39 stems', len(stems) == 39)

# ---- 2. 39 隻圖標檔案齊（12 樣本＋14 新圖＋v128 A5 補 9：🏆＋禮物 8 隻＋v164 補 4：名筆／計數機／腕表／玫瑰） ----
for stem in sorted(stems):
    ok('file assets/icons/icon_' + stem + '.png', os.path.isfile(os.path.join(root, 'assets', 'icons', 'icon_' + stem + '.png')))

# ---- 3. CSS（圖尺寸＋CSS 勾＋S-46 進度格） ----
ok('css .ic112', '.ic112{' in html)
ok('css .ic-check112', '.ic-check112{' in html)
ok('css .fav-dots112', '.fav-dots112{' in html)

# ---- 4. 逐面換：新渲染點在場 ----
ok('render week day .ic', '<span class="ic">${iconHtml112(meta.icon)}</span>' in html)
ok('render act list .ai', '<span class="ai">${iconHtml112(it.icon)}</span>' in html)
ok('render cat tab .ci', '<span class="ci">${iconHtml112(c.icon)}</span>' in html)
ok('render day result body', '${iconHtml112(meta.icon||"")}' in html)
ok('render training guide card', 'iconHtml112(def.icon) + " "' in html)
ok('render all-locs list', '${iconHtml112(L.emoji||"")}' in html)
ok('render loc title innerHTML', 'document.getElementById("loc-title").innerHTML=iconHtml112(L.emoji||"")' in html)
ok('render psr kicker channel', '${iconHtml112(c.icon||"✨")}' in html)
ok('render psr kicker echo ✨', '${iconHtml112("✨")}' in html)
ok('render psr kicker press 📰 → 報紙 kicker（v214：結果卡改做報紙，psr-press 卡退役）', '${iconHtml112("📰")}' not in html and 'np214-kicker' in html and '"📰":"news"' in html)
ok('render psr kicker news 📻 → 報紙 kicker（v214：結果卡改做報紙，psr-news 卡退役）', '${iconHtml112("📻")}' not in html and 'np214-kicker' in html and '"📻":"radio"' in html)
ok('render jobs72 pending 📞', '${iconHtml112("📞")} ${rec.title}' in html)
ok('render jobs72 log ✅/📞', '${iconHtml112(en.ok?"✅":"📞")} ${en.title}' in html)
ok('render jobs72 shoot 🎥', '${iconHtml112("🎥")} ${sh.title}' in html)
ok('render jobs72 gig 🎬', '${iconHtml112("🎬")} ${b.title}' in html)
ok('render jobs72 wrap ✅', '${iconHtml112("✅")} ${h.title' in html)
ok('render gift shop', '${iconHtml112(it.emoji||"🎁")}' in html)
# v20a185 C1：give 行名入 .gift-pick-name span（icon 呼叫本身唔郁，淨係包多層 span 做 ellipsis）
ok('render gift give', '${iconHtml112(item.emoji||"🎁")} <span class="gift-pick-name">${item.name}</span>' in html)
ok('render gift inv', '${iconHtml112(item.emoji||"🎁")} <b>${item.name}' in html)

# ---- 5. 舊寫法已清（反證：基線呢批全部 FAIL） ----
ok('old week day .ic gone', '<span class="ic">${meta.icon}</span>' not in html)
ok('old act list .ai gone', '<span class="ai">${it.icon}</span>' not in html)
ok('old cat tab .ci gone', '<span class="ci">${c.icon}</span>' not in html)
ok('old day result body gone', '<p>${meta.icon||""}' not in html)
ok('old training icon-in-esc gone', 'ux68Esc((def.icon ? def.icon' not in html)
ok('old all-locs emoji gone', '${L.emoji||""} ${L.name}' not in html)
ok('old loc title textContent gone', 'document.getElementById("loc-title").textContent=' not in html)
ok('old psr kicker gone', '<span class="psr-icon">${c.icon||"✨"}</span>' not in html)
ok('old hearts enc79 gone', '"♥".repeat' not in html)
ok('old hearts people72 gone', '"♡".repeat' not in html)
ok('S-46 favDots112 wired x2', html.count('favDots112(Math.round(') == 2)

# ---- 6. 刻意留低嘅 emoji（審計 §4）：唔准靜靜消失，亦唔准擴散 ----
# v128 A5：🏆 已補圖（唔再係「冇圖留低」），映射入段一驗；v128 A4：🔒 換咗 CSS 畫鎖
# （.sp-lock-ico），emoji 本身清零——兩項都係刻意改動，唔係靜靜消失。
ok('🏆 awards 有圖（v128 A5：trophy 映射）', '"🏆":"trophy"' in html)
ok('🔒 已換 CSS 畫鎖（v128 A4：.sp-lock-ico，emoji 清零）', '🔒' not in html and '.sp-lock-ico' in html)
ok('kept 💡 intel mark', '💡' in html)
ok('kept 📋/👤 map fallbacks', '📋' in html and '👤' in html)
gifts_path = os.path.join(root, 'content', 'items_gifts.json')
try:
    gifts = json.load(open(gifts_path, encoding='utf-8'))
    items = gifts if isinstance(gifts, list) else gifts.get('items', [])
    emojis = sorted(set(it.get('emoji', '') for it in items if it.get('emoji')))
    ok('gift pictograms untouched (10 items)', len(emojis) == 10 and '🍍' in emojis and '🌸' in emojis)
except Exception as e:
    ok('gift pictograms untouched (10 items)', False)

# ---- 7. 紅線 ----
ok('redline SAVE key untouched', 'const SAVE = "starVolunteer_map_v19w"' in html)
ok('redline softRev s107 untouched', 'SOFT_REV = "s107"' in html)
ok('redline ?v= 20a10 untouched', '?v=20a10' in html)
ok('redline no new SAVE/softRev bump', html.count('SOFT_REV = ') == 1)

print('')
if fails:
    print('FAILED: ' + ' | '.join(fails))
    sys.exit(1)
print('ICONS112 STATIC: ALL PASS')
