# -*- coding: utf-8 -*-
"""v20a195 resync 套用：將 qa195/resync195.py difflib 映射到嘅新行號／總數寫入
受影響嘅靜態測試。只改期望數字＋加 v195 resync 註解，唔改任何斷言邏輯。
每項替換斷言出現次數，唔啱數即停。
用法：python3 qa195/apply_resync195.py
"""
import os, sys

ROOT = "/home/hatch/workspace/linji-work195"
CHANGES = []  # (file, old, new, count, note)

def rep(path, old, new, count=1, note=""):
    p = os.path.join(ROOT, path)
    s = open(p, encoding="utf-8").read()
    n = s.count(old)
    assert n == count, "%s: %r 出現 %d 次（預期 %d）" % (path, old[:60], n, count)
    open(p, "w", encoding="utf-8").write(s.replace(old, new))
    CHANGES.append((path, note or old[:40]))

def header(path, line):
    p = os.path.join(ROOT, path)
    s = open(p, encoding="utf-8").read()
    assert line not in s
    open(p, "w", encoding="utf-8").write(line + "\n" + s)
    CHANGES.append((path, "header: " + line[:50]))

# ---- 1. fullbody 總數 207 -> 209（加 2 張 angry 表情）----
rep("tests/test_dlg107_static.py",
    "148→170→207（v119 DLG119 加 10 張：男／女／老年影 base＋dim 6 張＋3 張 halo png＋老臨記 base；v123 加 12 張新表情；v126 加 6 張新表情；v20a131 B1 加 2 張企立圖；v127 加 22 張新表情；v138 加 37 張新表情；v111 boss_* 11 張／v116 v2/v2b 11 張見舊註）\", len([f for f in names if f.endswith((\".webp\", \".png\"))]) == 207",
    "148→170→207→209（v119 DLG119 加 10 張：男／女／老年影 base＋dim 6 張＋3 張 halo png＋老臨記 base；v123 加 12 張新表情；v126 加 6 張新表情；v20a131 B1 加 2 張企立圖；v127 加 22 張新表情；v138 加 37 張新表情；v195 加 2 張 angry 表情；v111 boss_* 11 張／v116 v2/v2b 11 張見舊註）\", len([f for f in names if f.endswith((\".webp\", \".png\"))]) == 209")
rep("tests/test_dlg119_static.py",
    "fullbody 總數 207（128＋v123 12 張新表情＋v126 6 張新表情＋v20a131 B1 2 張企立圖＋v127 22 張新表情＋v138 37 張新表情）",
    "fullbody 總數 209（128＋v123 12 張新表情＋v126 6 張新表情＋v20a131 B1 2 張企立圖＋v127 22 張新表情＋v138 37 張新表情＋v195 2 張 angry 表情）")
rep("tests/test_dlg119_static.py",
    "len([f for f in names if f.endswith((\".webp\", \".png\"))]) == 207",
    "len([f for f in names if f.endswith((\".webp\", \".png\"))]) == 209")
rep("tests/test_dlg123_static.py",
    "148→170→207（v119 後 128 張＋v123 12 張新表情＋v126 6 張新表情＋v20a131 B1 2 張企立圖＋v127 22 張新表情＋v138 37 張新表情）\", len([f for f in names if f.endswith((\".webp\", \".png\"))]) == 207",
    "148→170→207→209（v119 後 128 張＋v123 12 張新表情＋v126 6 張新表情＋v20a131 B1 2 張企立圖＋v127 22 張新表情＋v138 37 張新表情＋v195 2 張 angry 表情）\", len([f for f in names if f.endswith((\".webp\", \".png\"))]) == 209")
rep("tests/test_dlg126_static.py",
    "148→170→207（v123 後 140 張＋v126 6 張新表情＋v20a131 B1 2 張企立圖＋v127 22 張新表情＋v138 37 張新表情）\", len([f for f in names if f.endswith((\".webp\", \".png\"))]) == 207",
    "148→170→207→209（v123 後 140 張＋v126 6 張新表情＋v20a131 B1 2 張企立圖＋v127 22 張新表情＋v138 37 張新表情＋v195 2 張 angry 表情）\", len([f for f in names if f.endswith((\".webp\", \".png\"))]) == 209")
rep("tests/test_dlg127_static.py",
    "148→170→207（v131 後 148 張＋v127 22 張新表情＋v138 37 張新表情）\", len([f for f in names if f.endswith((\".webp\", \".png\"))]) == 207",
    "148→170→207→209（v131 後 148 張＋v127 22 張新表情＋v138 37 張新表情＋v195 2 張 angry 表情）\", len([f for f in names if f.endswith((\".webp\", \".png\"))]) == 209")
rep("tests/test_dlg138_static.py",
    "fullbody 總數 170→207（v127 後 170 張＋v138 37 張新表情）\", len([f for f in names if f.endswith((\".webp\", \".png\"))]) == 207",
    "fullbody 總數 170→207→209（v127 後 170 張＋v138 37 張新表情＋v195 2 張 angry 表情）\", len([f for f in names if f.endswith((\".webp\", \".png\"))]) == 209")
rep("tests/test_dlg138_static.py",
    "# 覆蓋：① 37 張新資產本地存在＋檔名一字唔差＋WebP 檔頭＋fullbody 總數 207",
    "# 覆蓋：① 37 張新資產本地存在＋檔名一字唔差＋WebP 檔頭＋fullbody 總數 209（v195：207＋2 張 angry 表情）")
# ---- 2. 真檔數目 182 -> 184 ----
rep("tests/test_dlg108_static.py",
    "真檔數目 182 張（v106 88 張＋v107 8 張新表情＋v119 DLG119 7 張 webp＋v123 12 張新表情＋v126 6 張新表情＋v20a131 B1 2 張企立圖＋v127 22 張新表情＋v138 37 張新表情；v111 boss_* 11 張另計，唔入對話重測；3 張 halo 係 png）\", len(files) == 182",
    "真檔數目 184 張（v106 88 張＋v107 8 張新表情＋v119 DLG119 7 張 webp＋v123 12 張新表情＋v126 6 張新表情＋v20a131 B1 2 張企立圖＋v127 22 張新表情＋v138 37 張新表情＋v195 2 張 angry 表情；v111 boss_* 11 張另計，唔入對話重測；3 張 halo 係 png）\", len(files) == 184")
rep("tests/test_dlg109_height_static.py",
    "真檔數目 182 張（109 唔加圖；96＋v119 DLG119 7 張 webp＋v123 12 張新表情＋v126 6 張新表情＋v20a131 B1 2 張企立圖＋v127 22 張新表情＋v138 37 張新表情；3 張 halo 係 png，唔入呢個數；v111 boss_* 11 張另計，唔入身高重測）\", len(files) == 182",
    "真檔數目 184 張（109 唔加圖；96＋v119 DLG119 7 張 webp＋v123 12 張新表情＋v126 6 張新表情＋v20a131 B1 2 張企立圖＋v127 22 張新表情＋v138 37 張新表情＋v195 2 張 angry 表情；3 張 halo 係 png，唔入呢個數；v111 boss_* 11 張另計，唔入身高重測）\", len(files) == 184")

# ---- 3. 總行數 60490 -> 60577（淨 +87）----
rep("tests/test_gift185_static.py",
    "ok('總行數 60143 不變（零淨行數改動，行號釘唔漂移）', html.count('\\n') == 60490)",
    "ok('總行數 60577（v195 淨 +87，行號釘見 resync195.py）', html.count('\\n') == 60577)")
for f in ("tests/test_tang171_static.py", "tests/test_tang173_static.py"):
    rep(f, "src.count('\\n') == 60490", "src.count('\\n') == 60577")
rep("tests/test_tang171_static.py",
    "ok('零行數漂移：總行數 59442（v170 59173＋v149 ＋97＋v153 ＋71＋v172 ＋15＋v175 ＋78＋v181 ＋8）'",
    "ok('零行數漂移：總行數 60577（v170 59173＋v149 ＋97＋v153 ＋71＋v172 ＋15＋v175 ＋78＋v181 ＋8＋v195 ＋87）'")
rep("tests/test_tang173_static.py",
    "ok('零行數漂移：總行數 59442（v181 ＋8）'",
    "ok('零行數漂移：總行數 60577（v181 ＋8＋v195 ＋87）'")

# ---- 4. openLoc DEF（tang171／173：實查 lines[54985]，即 L54986 -> L55070）----
for f in ("tests/test_tang171_static.py", "tests/test_tang173_static.py"):
    rep(f, "ok('零行數漂移：openLoc DEF 行 53961（v181 ＋8，travel114 釘行）',\n   len(lines) >= 54986 and 'function openLoc(id, opts){' in lines[54985])",
           "ok('零行數漂移：openLoc DEF 行 55070（v195 ＋84：54986→55070，travel114 釘行）',\n   len(lines) >= 55070 and 'function openLoc(id, opts){' in lines[55069])")

# ---- 5. tang152（0-based index；L31510->L31514、L31654->L31658）----
rep("tests/test_tang152_static.py",
    "ok('機制：normaliseTangStub152 函數在位（L31501）', lines()[31509].startswith('function normaliseTangStub152(pack){'))",
    "ok('機制：normaliseTangStub152 函數在位（L31514）', lines()[31513].startswith('function normaliseTangStub152(pack){'))")
rep("tests/test_tang152_static.py",
    "ok('機制：stub 正規化喺 TEXTFIX 之前行（L31645）', lines()[31653].strip().startswith('try{ normaliseTangStub152(rom2);'))",
    "ok('機制：stub 正規化喺 TEXTFIX 之前行（L31658）', lines()[31657].strip().startswith('try{ normaliseTangStub152(rom2);'))")

# ---- 6. rom176（1-based line(n)；31583->31587、53416->53500、53784->53868、54923->55007、55017->55101）----
rep("tests/test_rom176_static.py",
    "ok('釘：載入點 L31533（GIFT_REACT 賦值同行呼叫注入）',\n   'GIFT_REACT = giftReact' in line(31583) and 'rom176ApplyGiftOverrides()' in line(31583))",
    "ok('釘：載入點 L31587（GIFT_REACT 賦值同行呼叫注入）',\n   'GIFT_REACT = giftReact' in line(31587) and 'rom176ApplyGiftOverrides()' in line(31587))")
rep("tests/test_rom176_static.py",
    "ok('釘：ROM176 block 起點 L53050', line(53416).startswith('/* ===== v20a176 ROM176'))",
    "ok('釘：ROM176 block 起點 L53500', line(53500).startswith('/* ===== v20a176 ROM176'))")
rep("tests/test_rom176_static.py",
    "ok('釘：rom176ApplyGiftOverrides 定義 L53415', line(53784).startswith('function rom176ApplyGiftOverrides()'))",
    "ok('釘：rom176ApplyGiftOverrides 定義 L53868', line(53868).startswith('function rom176ApplyGiftOverrides()'))")
rep("tests/test_rom176_static.py",
    "ok('釘：addLocTalkGiftActs L54447', line(54923).startswith('function addLocTalkGiftActs(add, L, npcId)'))",
    "ok('釘：addLocTalkGiftActs L55007', line(55007).startswith('function addLocTalkGiftActs(add, L, npcId)'))")
rep("tests/test_rom176_static.py",
    "ok('釘：openLoc rom176 攔截 L54541', 'rom176TryIntercept(id)' in line(55017))",
    "ok('釘：openLoc rom176 攔截 L55101', 'rom176TryIntercept(id)' in line(55101))")

# ---- 7. kwan151（1-based line(n)；27213->27217、27246->27250、31020->31024、31028->31032、31029->31033、31071->31075）----
rep("tests/test_kwan151_static.py",
    "ok('B2 PHRASES 其餘配對唔郁', '[\"星河電視城\", \"星河電視台\"]' in line(31029) and '[\"送命題\", \"辣手問題\"]' in line(31029))",
    "ok('B2 PHRASES 其餘配對唔郁', '[\"星河電視城\", \"星河電視台\"]' in line(31033) and '[\"送命題\", \"辣手問題\"]' in line(31033))")
rep("tests/test_kwan151_static.py",
    "ok('B3 EXACT C13 value 有關海媚', '關海媚提醒頭條係雙刃' in line(31020))",
    "ok('B3 EXACT C13 value 有關海媚', '關海媚提醒頭條係雙刃' in line(31024))")
rep("tests/test_kwan151_static.py",
    "ok('B4 EXACT C13 value 冇當紅花旦', '嗰位當紅花旦亦提過佢' not in line(31020))",
    "ok('B4 EXACT C13 value 冇當紅花旦', '嗰位當紅花旦亦提過佢' not in line(31024))")
rep("tests/test_kwan151_static.py",
    "'1990年冬，娛樂週刊已經寫好緋聞草稿' in line(31020)",
    "'1990年冬，娛樂週刊已經寫好緋聞草稿' in line(31024)")
rep("tests/test_kwan151_static.py",
    "ok('C1 speaker display 改真名', 'kwan_hoimei: { artId:\"char_kwan\", portraitsKey:null, display:\"關海媚\" }' in line(27246))",
    "ok('C1 speaker display 改真名', 'kwan_hoimei: { artId:\"char_kwan\", portraitsKey:null, display:\"關海媚\" }' in line(27250))")
rep("tests/test_kwan151_static.py",
    "ok('C3 relMap rel_mei 改真名', '[\"rel_mei\",\"關海媚\"]' in line(31071))",
    "ok('C3 relMap rel_mei 改真名', '[\"rel_mei\",\"關海媚\"]' in line(31075))")
rep("tests/test_kwan151_static.py",
    "ok('C4 NOTE_EXACT 兩句改真名', '采兒同關海媚嗰邊都近咗啲' in line(31028) and '但采兒同關海媚嗰邊，都冷淡咗' in line(31028))",
    "ok('C4 NOTE_EXACT 兩句改真名', '采兒同關海媚嗰邊都近咗啲' in line(31032) and '但采兒同關海媚嗰邊，都冷淡咗' in line(31032))")
rep("tests/test_kwan151_static.py",
    "ok('E1 speaker registry 留返', '\"關海媚\":\"kwan_hoimei\"' in line(27213))",
    "ok('E1 speaker registry 留返', '\"關海媚\":\"kwan_hoimei\"' in line(27217))")

# ---- 8. text125（0-based ls[i]；27738->27742、27867->27871、33568->33575）----
rep("tests/test_text125_static.py",
    'if len(ls) < 27738 or FALLBACK not in ls[27737]:',
    'if len(ls) < 27742 or FALLBACK not in ls[27741]:')
rep("tests/test_text125_static.py",
    'probs.append("currentLine 第 27738 行冇 text fallback")',
    'probs.append("currentLine 第 27742 行冇 text fallback")')
rep("tests/test_text125_static.py",
    'if len(ls) < 27867 or FALLBACK not in ls[27866]:',
    'if len(ls) < 27871 or FALLBACK not in ls[27870]:')
rep("tests/test_text125_static.py",
    'probs.append("advance 第 27867 行冇 text fallback")',
    'probs.append("advance 第 27871 行冇 text fallback")')
rep("tests/test_text125_static.py",
    'if len(ls) < 33568 or \'if(typeof b.text === "string" && b.text){\' not in ls[33567]:',
    'if len(ls) < 33575 or \'if(typeof b.text === "string" && b.text){\' not in ls[33574]:')
rep("tests/test_text125_static.py",
    'probs.append("applyFamilySafeToNode 第 33568 行冇 b.text 分支")',
    'probs.append("applyFamilySafeToNode 第 33575 行冇 b.text 分支")')

# ---- 9. travel114（COUNT／FREE 集＋DEF 54986->55070＋WRAPPER 44434->44443）----
TRAVEL_COUNT = {
    32184: 32188, 35680: 35687, 37807: 37814, 38888: 38897, 39322: 39331,
    39325: 39334, 39356: 39365, 43911: 43920, 59046: 59130, 59224: 59308,
    59367: 59454, 59388: 59475,
}
TRAVEL_FREE = {
    24686: 24686, 28228: 28232, 30851: 30855, 30852: 30856, 30864: 30868,
    30865: 30869, 30876: 30880, 30877: 30881, 30980: 30984, 40866: 40875,
    43568: 43577, 43591: 43600, 53239: 53323, 53358: 53442, 53408: 53492,
    53631: 53715, 53670: 53754, 53676: 53760, 53743: 53827, 53745: 53829,
    53748: 53832, 53775: 53859, 54886: 54970, 55260: 55344, 55282: 55366,
    55433: 55517, 57070: 57154, 58814: 58898, 58932: 59016, 58933: 59017,
    58968: 59052, 58969: 59053, 58994: 59078, 59838: 59925,
}
p = os.path.join(ROOT, "tests/test_travel114_static.py")
s = open(p, encoding="utf-8").read()
for old_ln, new_ln in list(TRAVEL_COUNT.items()) + list(TRAVEL_FREE.items()):
    if old_ln == new_ln:
        continue
    old_s = "    %d," % old_ln
    new_s = "    %d," % new_ln
    n = s.count(old_s)
    assert n == 1, "travel114: %r 出現 %d 次" % (old_s, n)
    s = s.replace(old_s, new_s)
open(p, "w", encoding="utf-8").write(s)
CHANGES.append(("tests/test_travel114_static.py", "COUNT/FREE 46 行重映射"))
rep("tests/test_travel114_static.py",
    "DEF_LINE = 54986      # function openLoc(id, opts){",
    "DEF_LINE = 55070      # function openLoc(id, opts){")
rep("tests/test_travel114_static.py",
    "WRAPPER_LINE = 44434  # window.__phase2.openLoc：轉發 opts",
    "WRAPPER_LINE = 44443  # window.__phase2.openLoc：轉發 opts")

# ---- 10. 各檔加 v195 resync 註解 ----
header("tests/test_gift185_static.py",
         "# v20a195 resync：index.html 淨 +87 行（見 qa195/resync195.py difflib 對位核實純漂移），總行數 60490→60577。")
header("tests/test_tang171_static.py",
         "# v20a195 resync：index.html 淨 +87 行（見 qa195/resync195.py difflib 對位核實純漂移），總行數 60490→60577、DEF 54986→55070。")
header("tests/test_tang173_static.py",
         "# v20a195 resync：index.html 淨 +87 行（見 qa195/resync195.py difflib 對位核實純漂移），總行數 60490→60577、DEF 54986→55070；L4862 錨點 4889 唔郁（喺插入點之前）。")
header("tests/test_tang152_static.py",
         "# v20a195 resync：index.html 淨 +87 行（見 qa195/resync195.py difflib 對位核實純漂移），normaliser／loader 錨點各 +4；HELD 唔郁（喺插入點之前）。")
header("tests/test_rom176_static.py",
         "# v20a195 resync：index.html 淨 +87 行（見 qa195/resync195.py difflib 對位核實純漂移），6 個釘行按段 +0／+4／+84 重算。")
header("tests/test_kwan151_static.py",
         "# v20a195 resync：index.html 淨 +87 行（見 qa195/resync195.py difflib 對位核實純漂移），釘行按段 +4／+10 重算。")
header("tests/test_text125_static.py",
         "# v20a195 resync：index.html 淨 +87 行（見 qa195/resync195.py difflib 對位核實純漂移），三錨點 +4／+4／+7 重算。")
header("tests/test_travel114_static.py",
         "# v20a195 resync：index.html 淨 +87 行（見 qa195/resync195.py difflib 對位核實純漂移），COUNT／FREE／DEF／WRAPPER 按段重算，總數不變。")
for f in ("tests/test_dlg107_static.py", "tests/test_dlg119_static.py", "tests/test_dlg123_static.py",
          "tests/test_dlg126_static.py", "tests/test_dlg127_static.py", "tests/test_dlg138_static.py",
          "tests/test_dlg108_static.py", "tests/test_dlg109_height_static.py"):
    header(f, "# v20a195 resync：加 2 張 angry 表情（awi_s2／s3_angry），fullbody 總數 207→209、真檔 182→184。")

print("APPLIED %d changes" % len(CHANGES))
for c in CHANGES:
    print(" -", c[0], "::", c[1])
