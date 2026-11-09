# Soft tip s109 — map filter toast names the mode AFTER the toggle.
# show-all (mapShowAllLocs true) → 「已顯示全部地點」
# events-only (false) → 「只亮有事做嘅地點」
# Button label stays the next command, so it reads the other phrase.
# Soft≠PASS. SAVE and product ?v= stay put. toast-on-map from s108 stays.
import pathlib, re, sys
html = pathlib.Path(__file__).resolve().parents[1].joinpath("index.html").read_text(encoding="utf-8")
fails = []
def ok(name, cond):
    print(("OK  " if cond else "FAIL") + " " + name)
    if not cond: fails.append(name)

m = re.search(r"function wireMapShowAllLocs\(\)\{(?P<body>.*?)\}\)\(\);", html, re.S)
body = m.group("body") if m else ""
ok("handler present", bool(body))
flip = body.find("mapShowAllLocs = !mapShowAllLocs;")
snap = body.find("const showAllNow = !!mapShowAllLocs;")
draw = body.find("drawMap();")
toast = body.find('toast(showAllNow ? "已顯示全部地點" : "只亮有事做嘅地點"')
ok("flip then snapshot then redraw then toast", flip != -1 and flip < snap < draw < toast)
ok("show-all copy is 已顯示全部地點", 'showAllNow ? "已顯示全部地點"' in body)
ok("events-only copy is 只亮有事做嘅地點", ': "只亮有事做嘅地點"' in body)
ok("not the inverted ternary", 'showAllNow ? "只亮有事做嘅地點"' not in body)
ok("drawMap throw cannot skip toast", "try{ drawMap(); }catch(_e){}" in body)
ok("toast-on-map kept", "toast-on-map" in html)
ok("softRev s109", 'var SOFT_REV = "s109";' in html and "softRev=s109" in html)
ok("newspaper check s109", 'softRev:"s109"' in html)
ok("SAVE key unchanged", 'const SAVE = "starVolunteer_map_v19w"' in html or 'SAVE = "starVolunteer_map_v19w"' in html)
ok("product ?v= stays 20a10", "softRev=s109" in html and "?v=20a10" in html)
ok("no product v bump in soft rev script", 'q.set("v", "20a10")' in html)
print("---")
print("FAILURES:", len(fails))
sys.exit(1 if fails else 0)
