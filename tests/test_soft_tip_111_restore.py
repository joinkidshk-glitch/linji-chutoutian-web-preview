# Soft tip s111 — restore s108–s110 after LIVE tips overwrote index.html.
# Map filter toast names the mode AFTER one flip, sits on the map (toast-on-map),
# and far-view copy skips 文案待補 / flavor duplicates.
#   true  (show-all-locs, idle pins lit) → 「已顯示全部地點」
#   false (events-only)                  → 「只亮有事做嘅地點」
# Button label stays the next command. Soft≠PASS. SAVE and ?v= stay.
import pathlib, re, subprocess, sys, textwrap
html = pathlib.Path(__file__).resolve().parents[1].joinpath("index.html").read_text(encoding="utf-8")
fails = []
def ok(name, cond):
    print(("OK  " if cond else "FAIL") + " " + name)
    if not cond: fails.append(name)

def grab(name):
    i = html.find("function " + name + "(")
    if i < 0:
        return ""
    j = html.find("{", i)
    depth = 0
    k = j
    while k < len(html):
        ch = html[k]
        if ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                return html[i:k + 1]
        k += 1
    return ""

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

toast_fn = re.search(r"function toast\(m, opts\)\{(?P<body>.*?)\n\}", html, re.S)
toast_body = toast_fn.group("body") if toast_fn else ""
ok("toast toggles toast-on-map when map has no sheet", 'app.classList.toggle("toast-on-map", !keepSheet && mapOn)' in toast_body)
ok("toast clears toast-on-map", 'app.classList.remove("toast-up","keep-sheet","toast-on-map")' in toast_body)
ok("toast-on-map css lifts the ticket", "#app.toast-up.toast-on-map .toast{" in html and "top: 64px !important;" in html and "z-index: 520 !important;" in html)
ok("old :has rule kept", "#app.toast-up:has(#v-map.view.on)::after" in html)

sight = re.search(r"function eraSightIsPlaceholder\(s\)\{(?P<body>.*?)\n\}", html, re.S)
paras = re.search(r"function eraSightParagraphs\(star\)\{(?P<body>.*?)\n\}", html, re.S)
ok("eraSightIsPlaceholder present", bool(sight) and "/待補|文案待補|選項待補/" in (sight.group(0) if sight else ""))
ok("eraSightIsPlaceholder uses freeplay helper", "freeplayIsPlaceholderLine" in (sight.group(0) if sight else ""))
ok("eraSightParagraphs skips placeholders and flavor dupes", bool(paras) and "eraSightIsPlaceholder(t)" in paras.group(0) and "t===flavor" in paras.group(0))
phase3 = re.search(r"function phase3Stars\(\)\{(?P<body>.*?)\n\}", html, re.S)
phase3_body = phase3.group("body") if phase3 else ""
ok("phase3Stars drops placeholder silhouetteDesc", "eraSightIsPlaceholder(silDesc)" in phase3_body and "distanceLook: distanceLook" in phase3_body)
ok("farview flavor drops placeholder", "eraSightIsPlaceholder(flavorPick)" in html)

ok("softRev s111", 'var SOFT_REV = "s111";' in html and "softRev=s111" in html)
ok("newspaper check s111", 'softRev:"s111"' in html)
ok("soft rev attr check s111", '!=="s111") bad("soft_rev_attr")' in html)
ok("SAVE key unchanged", 'const SAVE = "starVolunteer_map_v19w"' in html)
ok("product ?v= stays 20a10", "softRev=s111" in html and "?v=20a10" in html)
ok("no product v bump in soft rev script", 'q.set("v", "20a10")' in html)
ok("awards poster consequence and chibi still present", "v20a63 AWARDS63" in html and "loadPx" in html and "const POSTER59_DATA" in html and "v20a61 CONSEQ61" in html)  # v20a181：Q 版池 AWARDS64_SPRITES 已撤，改 PixelLab 幀 loadPx

sight_fn = grab("eraSightIsPlaceholder")
paras_fn = grab("eraSightParagraphs")
toast_text_fn = grab("mapFilterToastText")
if toast_text_fn and sight_fn and paras_fn:
    probe = textwrap.dedent("""\
    function journalText(s){ return String(s==null?"":s); }
    function freeplayIsPlaceholderLine(s){
      const t = String(s||"").trim();
      if(!t) return true;
      return /待補|文案待補|選項待補/.test(t);
    }
    """ + sight_fn + "\n" + paras_fn + "\n" + toast_text_fn + """
    const fails = [];
    if (mapFilterToastText(true) !== "已顯示全部地點") fails.push("true");
    if (mapFilterToastText(false) !== "只亮有事做嘅地點") fails.push("false");
    const sheet = eraSightParagraphs({
      distanceLook: "文案待補",
      distanceLine: "只能遠望，時機未到唔好行埋。",
      rumorTeaser: "選項待補",
      locHint: "灣仔",
    });
    if (sheet.indexOf("文案待補") >= 0 || sheet.indexOf("選項待補") >= 0 || sheet.indexOf("待補") >= 0) fails.push("placeholder");
    if (sheet.indexOf("只能遠望") >= 0) fails.push("flavor-dupe");
    if (sheet.indexOf("灣仔") < 0) fails.push("kept");
    const both = eraSightParagraphs({
      distanceLook: "遠處一個短髮身影。",
      distanceLine: "只能遠望，時機未到唔好行埋。",
      rumorTeaser: "",
      locHint: "",
    });
    if (both.indexOf("短髮") < 0) fails.push("look-kept");
    if (both.indexOf("只能遠望") >= 0) fails.push("line-is-flavor");
    if (fails.length) { console.log(fails.join(",")); process.exit(1); }
    console.log("eval-ok");
    """)
    run = subprocess.run(["node", "-e", probe], capture_output=True, text=True)
    ok("node eval toast + farview filter", run.returncode == 0 and "eval-ok" in run.stdout)
    if run.returncode != 0:
        print(run.stdout)
        print(run.stderr)
else:
    ok("node eval toast + farview filter", False)

print("---")
print("FAILURES:", len(fails))
sys.exit(1 if fails else 0)
