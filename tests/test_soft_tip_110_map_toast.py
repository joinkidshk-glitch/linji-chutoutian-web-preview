# Soft tip s110 — map filter toast names the mode AFTER one flip.
# Natural QA on s109: one press left the previous button label and the previous
# sentence, because a second click in the same gesture flipped the flag back.
# Polarity natural QA expects, from the post-toggle flag (not the button):
#   true  (show-all-locs, idle pins lit) → 「已顯示全部地點」
#   false (events-only)                  → 「只亮有事做嘅地點」
# Button label stays the next command. Soft≠PASS. SAVE and ?v= stay. toast-on-map stays.
import pathlib, re, subprocess, sys, textwrap
html = pathlib.Path(__file__).resolve().parents[1].joinpath("index.html").read_text(encoding="utf-8")
fails = []
def ok(name, cond):
    print(("OK  " if cond else "FAIL") + " " + name)
    if not cond: fails.append(name)

fn = re.search(r"function mapFilterToastText\(showAll\)\{(?P<body>.*?)\n\}", html, re.S)
ok("mapFilterToastText present", bool(fn))
body = fn.group("body") if fn else ""
ok("show-all arm is 已顯示全部地點", 'showAll ? "已顯示全部地點"' in body)
ok("events-only arm is 只亮有事做嘅地點", ': "只亮有事做嘅地點"' in body)
ok("not the inverted ternary", 'showAll ? "只亮有事做嘅地點"' not in body)

m = re.search(r"function wireMapShowAllLocs\(\)\{(?P<body>.*?)\}\)\(\);", html, re.S)
handler = m.group("body") if m else ""
ok("handler present", bool(handler))
guard = handler.find("(now - lastFlip) < 500) return;")
flip = handler.find("mapShowAllLocs = !mapShowAllLocs;")
snap = handler.find("const showAllNow = !!mapShowAllLocs;")
toast = handler.find("toast(mapFilterToastText(showAllNow)")
ok("echo guard returns before the flip", guard != -1 and flip != -1 and guard < flip)
ok("snapshot is the flag after the flip", flip != -1 and snap != -1 and flip < snap < toast)
ok("toast uses post-toggle flag, not its inverse", "mapFilterToastText(!showAllNow)" not in handler and "mapFilterToastText(!mapShowAllLocs)" not in handler)
ok("detail>1 is ignored", "ev.detail > 1" in handler)
ok("button stays the next command", 'on ? "只亮有事" : "全部地點"' in html)
ok("label apply is shared", "function applyMapShowAllLocs(showAll)" in html and "applyMapShowAllLocs(showAllNow)" in handler and "applyMapShowAllLocs(mapShowAllLocs)" in html)
ok("toast-on-map kept", "toast-on-map" in html)
ok("softRev s110", 'var SOFT_REV = "s110";' in html and "softRev=s110" in html)
ok("newspaper check s110", 'softRev:"s110"' in html)
ok("SAVE key unchanged", 'const SAVE = "starVolunteer_map_v19w"' in html or 'SAVE = "starVolunteer_map_v19w"' in html)
ok("product ?v= stays 20a10", "softRev=s110" in html and "?v=20a10" in html)
ok("no product v bump in soft rev script", 'q.set("v", "20a10")' in html)

if fn:
    probe = textwrap.dedent("""\
    """ + fn.group(0) + """
    const fails = [];
    if (mapFilterToastText(true) !== "已顯示全部地點") fails.push("true");
    if (mapFilterToastText(false) !== "只亮有事做嘅地點") fails.push("false");
    if (fails.length) { console.log(fails.join(",")); process.exit(1); }
    console.log("eval-ok");
    """)
    run = subprocess.run(["node", "-e", probe], capture_output=True, text=True)
    ok("node eval post-toggle flag → toast", run.returncode == 0 and "eval-ok" in run.stdout)
    if run.returncode != 0:
        print(run.stdout)
        print(run.stderr)
else:
    ok("node eval post-toggle flag → toast", False)

print("---")
print("FAILURES:", len(fails))
sys.exit(1 if fails else 0)
