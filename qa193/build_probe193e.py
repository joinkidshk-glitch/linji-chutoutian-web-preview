# -*- coding: utf-8 -*-
"""Build instrumented copy of index.html for Case C tracing (probe only, NEVER commit).
Copies index.html to /tmp/wf4probe193/, symlinks assets/content/favicon, and injects
entry-log statements (window.__probe193) into morning-chain / WF4 functions.
Insertion: right after the opening brace of each target function body.
"""
import os, re, shutil, sys

SRC = "/home/hatch/workspace/linji-work193/index.html"
DSTDIR = "/tmp/wf4probe193"
DST = os.path.join(DSTDIR, "index.html")

LOG = "try{window.__probe193=window.__probe193||[];window.__probe193.push(%s);}catch(_e){}"

def snap(extra):
    return "'{' + '\"fn\":\"' + '%s' + '\",\"day\":' + ((typeof S!=='undefined'&&S)?(S.dayIndex|0):null) + %s + '}'" % ("", "")

def js_str(s):
    return "'" + s.replace("\\", "\\\\").replace("'", "\\'") + "'"

# (fn name, extra JS expression appended inside the pushed object literal, as raw JS)
TARGETS = [
    ("contFromSlot",
     "log('contFromSlot')"),
    ("runScheduleFromToday",
     "log('runScheduleFromToday', {plan: (typeof todayPlanId==='function')?String(todayPlanId()):null})"),
    ("resolvePlannedDay",
     "log('resolvePlannedDay', {id: String(id)})"),
    ("goToMapForBrowse",
     "log('goToMapForBrowse')"),
    ("presentPendingPostShootReward",
     "log('presentPendingPostShootReward')"),
    ("presentPendingAward",
     "log('presentPendingAward', {hasPack: !!(typeof FREEPLAY_FW!=='undefined' && FREEPLAY_FW._pendingAward)})"),
    ("presentDueMorningPaper",
     "log('presentDueMorningPaper')"),
    ("aud91PresentDue",
     "log('aud91PresentDue')"),
    ("wf4PresentPending",
     "log('wf4PresentPending-enter', {pending:(S&&S.wf4)?S.wf4.pending:null, lastDay:(S&&S.wf4)?S.wf4.lastDay:null, seenPend:(S&&S.wf4&&S.wf4.pending)?(S.wf4.seen[S.wf4.pending]||0):null, baseOk:(typeof wf4BaseOk==='function')?wf4BaseOk():null, newsDay:(typeof wf4NewsDay==='function'&&S)?wf4NewsDay(S.dayIndex|0):null, forced:(typeof todayIsForcedDay==='function')?todayIsForcedDay():null, sick:(typeof conseq61IsSickToday==='function')?conseq61IsSickToday():null, ending:(typeof ending78Locked==='function')?ending78Locked():null})"),
    ("wf4PresentFenFarewell",
     "log('wf4PresentFenFarewell')"),
    ("wf4BaseOk",
     "log('wf4BaseOk')"),
    ("wf4DailyTick",
     "log('wf4DailyTick', {pending:(S&&S.wf4)?S.wf4.pending:null, pendingDay:(S&&S.wf4)?S.wf4.pendingDay:null})"),
    ("wf4TryLocEvent",
     "log('wf4TryLocEvent', {loc:String(locId), pending:(S&&S.wf4)?S.wf4.pending:null})"),
    ("story165TryForcedPlay",
     "log('story165TryForcedPlay')"),
    ("conseq61ResolveSickDay",
     "log('conseq61ResolveSickDay')"),
    ("presentAwardInvite",
     "log('presentAwardInvite', {ceremony:(pack&&pack.ceremonyId)||null})"),
]

HELPER = """
;try{window.__probe193log=function(fn,ex){try{window.__probe193=window.__probe193||[];var o={fn:fn,t:Date.now(),day:(typeof S!=='undefined'&&S)?(S.dayIndex|0):null,pending:(S&&S.wf4)?S.wf4.pending:null};if(ex){for(var k in ex)o[k]=ex[k];}window.__probe193.push(o);}catch(_e){}};}catch(_e){}
"""

def main():
    os.makedirs(DSTDIR, exist_ok=True)
    for name in ("assets", "content", "favicon.ico"):
        link = os.path.join(DSTDIR, name)
        if not os.path.lexists(link):
            os.symlink(os.path.join("/home/hatch/workspace/linji-work193", name), link)
    src = open(SRC, encoding="utf-8").read()
    # inject helper right after the main <script> tag (line 5907)
    tag = "<script>\n"
    i = src.find(tag, src.find("</head>"))
    assert i >= 0
    src = src[:i + len(tag)] + "var __probe193log;\n" + HELPER + src[i + len(tag):]
    # the helper defines window.__probe193log; `log` alias used in snippets:
    # snippets call log(...) -> define local alias via a var in scope is not possible
    # across functions; instead snippets call window.__probe193log directly.
    # Rewrite snippet calls: log( -> window.__probe193log(
    fixed_targets = []
    for name, snippet in TARGETS:
        fixed_targets.append((name, snippet.replace("log(", "window.__probe193log(")))
    for name, snippet in fixed_targets:
        pat = "function " + name + "("
        j = src.find(pat)
        assert j >= 0, "fn not found: " + name
        brace = src.find("{", j)
        assert brace >= 0
        inject = " " + snippet + ";"
        src = src[:brace + 1] + inject + src[brace + 1:]
        print("injected", name, "at", src[:brace + 1].count("\n") + 1)
    # marker: guard line reached inside wf4PresentPending (proves baseOk passed)
    guard = "if((st.seen[st.pending]||0) > 0){ st.pending = null; return false; }"
    gi = src.find(guard)
    assert gi >= 0
    src = src[:gi] + "window.__probe193log('wf4PresentPending-guard-reached');" + src[gi:]
    # marker: event lookup reached (guard passed, pending unseen)
    lookup = "const ev = DAILY_EVENTS_WF4.find(e=>e && e.id===st.pending);"
    li = src.find(lookup)
    assert li >= 0
    src = src[:li] + "window.__probe193log('wf4PresentPending-lookup-reached');" + src[li:]
    open(DST, "w", encoding="utf-8").write(src)
    print("wrote", DST, len(src))

if __name__ == "__main__":
    main()
