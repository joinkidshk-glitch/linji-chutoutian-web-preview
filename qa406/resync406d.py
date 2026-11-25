#!/usr/bin/env python3
"""v406 resync D：手帳/膠紙 CSS +12 行（插入點 L7464）後釘行重對；內容逐行核實。"""
import os, re
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IDX = open(os.path.join(ROOT,"index.html"),encoding="utf-8").read().split("\n")
def ln(n): return IDX[n-1]
def patch(path, pairs, header):
    p=os.path.join(ROOT,path); s=open(p,encoding="utf-8").read()
    for a,b in pairs:
        assert a in s, (path,a); s=s.replace(a,b)
    lines=s.split("\n"); lines.insert(0,header)
    open(p,"w",encoding="utf-8").write("\n".join(lines)); print("ok",path)

# content checks first
assert ln(8045).startswith('  lan:{ id:"lan", name:"藍若曦"'), ln(8045)
assert 'GIFT_REACT = giftReact' in ln(16760)
assert ln(45070).startswith('/* ===== v20a176 ROM176'), ln(45070)
assert ln(45429).startswith('function rom176ApplyGiftOverrides()')
assert ln(46995).startswith('function addLocTalkGiftActs(add, L, npcId)')
assert 'rom176TryIntercept(id)' in ln(47183)
assert 'typeof b.text === "string"' in ln(12706) and 'typeof b.text === "string"' in ln(12848)
assert 'if(typeof b.text === "string" && b.text){' in ln(18562)
assert 'function openLoc(id, opts){' in ln(47142), ln(47142)
assert 'openLoc: function(id, opts){ openLoc(id, opts); }' in ln(33208), ln(33208)
assert '查實' in IDX[29354], IDX[29354]

patch("tests/test_rom176_static.py",[
 ("line(8033)","line(8045)"),("line(16748)","line(16760)"),("line(45058)","line(45070)"),
 ("line(45417)","line(45429)"),("line(46983)","line(46995)"),("line(47171)","line(47183)")],
 "# v406 resync D：手帳/膠紙 CSS +12 行（L7464），6 釘行各 +12，內容逐行核實。")

patch("tests/test_menu72_static.py",[
 ("ms == ['back', 'settings', 'wire', 'slots']","ms == ['settings', 'wire', 'slots']")],
 "# v406：選單刪「返回」列（有意圖改動），data-m 清單去 back。")

patch("tests/test_gift185_static.py",[
 ("總行數 52227（","總行數 52373（"),("＋v405 +142）","＋v405 +142＋v406 +146）"),
 ("html.count('\\n') == 52227","html.count('\\n') == 52373")],
 "# v406 resync D：總行數 52227→52373（v406 +146）。")

patch("tests/test_text125_static.py",[
 ("12694","12706"),("ls[12693]","ls[12705]"),("12836","12848"),("ls[12835]","ls[12847]"),
 ("18550","18562"),("ls[18549]","ls[18561]"),("len(ls) < 18562","len(ls) < 18562")],
 "# v406 resync D：三錨點各 +12（12706/12848/18562），內容核實。")

patch("tests/test_rom159_static.py",[
 ("25499","25511"),("8020","8032"),("26333","26345"),("10553","10565"),
 ("14877","14889"),("26248","26260"),("idx_lines[29342]","idx_lines[29354]")],
 "# v406 resync D：6 釘行＋全佳行各 +12。")

# tang171/173、tang152、travel114 由 resync406d 附帶 inline 步驟處理（見 NOTES）。
