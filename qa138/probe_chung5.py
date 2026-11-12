"""probe17: on day 368, replicate enc79StoryPendingAt('rec_star') via exposed StoryOC + storyNodeLocId."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'drive138.py'), encoding='utf-8').read()
cut = src.find('srv = serve(ROOT)')
ns = {'__file__': os.path.join(os.path.dirname(os.path.abspath(__file__)), 'drive138.py')}
exec(compile(src[:cut], 'drive138_lib', 'exec'), ns)
new_game = ns['new_game']
serve, ROOT, EXE, HERE = ns['serve'], ns['ROOT'], ns['EXE'], ns['HERE']
from playwright.sync_api import sync_playwright
srv = serve(ROOT)
try:
    with sync_playwright() as pw:
        b = pw.chromium.launch(executable_path=EXE, args=["--no-sandbox"])
        ctx = b.new_context(viewport={"width": 390, "height": 844}, device_scale_factor=2)
        pg = ctx.new_page()
        pg.on("pageerror", lambda e: print("PAGEERROR:", e))
        new_game(pg)
        pg.evaluate("(d) => { S.dayIndex = d; }", 368)
        pg.wait_for_timeout(800)
        res = pg.evaluate("""() => {
          const out = { storyNodeLocId: typeof storyNodeLocId, listOpen: typeof StoryOC.listOpen, findNodeRaw: typeof StoryOC.findNodeRaw };
          try {
            const oc = StoryOC.listOpen({ checkNodePhase:true, player:true, ignoreSheetLoc:true }) || {};
            out.open = (oc.open||[]).map(r => {
              let loc = null, err = null;
              try { const n = StoryOC.findNodeRaw(r.id); loc = (typeof storyNodeLocId==='function') ? storyNodeLocId(n) : 'no-fn'; } catch(e){ err = String(e).slice(0,60); }
              return { id: r.id, loc, err };
            });
            out.mapTipRec = (S.mapTips && S.mapTips["rec_star"]) || null;
          } catch(e){ out.err = String(e).slice(0,120); }
          return out;
        }""")
        print("DAY368 story-pending check:", res)
        b.close()
finally:
    import signal
    try:
        srv.send_signal(signal.SIGTERM); srv.wait(timeout=5)
    except Exception:
        try: srv.kill()
        except Exception: pass
print("PROBE17 DONE")
