#!/usr/bin/env python3
"""v405 P1-3: E4 must not intercept GH-qualified states; E4 non-variety path stays reachable.
Constants copied from live ENDING95_T / ENDING410_T (verified 2026-11-26)."""
T95 = dict(e1Fame=70, e1Credit=65, e1Dual=350, e1NegMax=1, ssDual=300, ssFame=60, ssCredit=55, ssNegMax=1,
           fkDual=200, fkFilmShare=0.5, fkFilmLeads=2, tkDual=200, tkTvShare=0.5, tkTvLongLeads=1,
           skDual=200, skMusicShare=0.5, ghDual=180, ghHostShare=0.5, ghVarietyMin=8,
           e4ExposureMin=6, e4ExposureMonths=3)
T410 = dict(e4Fame=50, e4NetCreditBelow=45, e4RescueCredits=5)

def resolve(c, guard=True):
    fame, credit = c["fame"], c["credit"]
    dual = fame + credit
    sel_share = c["selVariety"] / c["selTotal"] if c["selTotal"] else 0
    gh_qualified = dual >= T95["ghDual"] and sel_share >= T95["ghHostShare"] and c["selVariety"] >= T95["ghVarietyMin"] and c["pangProgress"]
    e4 = fame >= T410["e4Fame"] and (credit - 0.5 * fame) < T410["e4NetCreditBelow"] and c["exposureCount"] >= T95["e4ExposureMin"] and c["exposureMonths"] >= T95["e4ExposureMonths"]
    if e4 and not (guard and gh_qualified):
        return "E4"
    if gh_qualified:
        return "GH"
    if dual >= T95["ssDual"] and fame >= T95["ssFame"] and credit >= T95["ssCredit"]:
        return "SS"
    return "OTHER"

gh_state = dict(fame=120, credit=90, selVariety=8, selTotal=16, pangProgress=True, exposureCount=8, exposureMonths=4)
e4_state = dict(fame=120, credit=90, selVariety=0, selTotal=14, pangProgress=False, exposureCount=7, exposureMonths=4)
gh_no_pang = dict(gh_state, pangProgress=False)

r = {
  "gh_state_prefix": resolve(gh_state, guard=False),
  "gh_state_postfix": resolve(gh_state, guard=True),
  "e4_state_postfix": resolve(e4_state, guard=True),
  "gh_no_pang_postfix": resolve(gh_no_pang, guard=True),
}
print(r)
ok = r["gh_state_prefix"] == "E4" and r["gh_state_postfix"] == "GH" and r["e4_state_postfix"] == "E4" and r["gh_no_pang_postfix"] == "E4"
print("P13 PASS" if ok else "P13 FAIL")
raise SystemExit(0 if ok else 1)
