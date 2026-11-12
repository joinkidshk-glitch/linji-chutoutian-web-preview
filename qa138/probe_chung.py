"""probe13: chung day 368 — click rec_star pin (retry x2), dump overlay + mapTips + StoryOC."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'drive138.py'), encoding='utf-8').read()
cut = src.find('srv = serve(ROOT)')
ns = {'__file__': os.path.join(os.path.dirname(os.path.abspath(__file__)), 'drive138.py')}
exec(compile(src[:cut], 'drive138_lib', 'exec'), ns)
new_game, suppress_wf4, isolate_star, back_to_map, seed_star = ns['new_game'], ns['suppress_wf4'], ns['isolate_star'], ns['back_to_map'], ns['seed_star']
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
        seed_star(pg, "chung_choning", True, 50, 3, beats_done=["chung_review","chung_intel","chung_f_clue","chung_patron"], heart_done=False)
        pg.evaluate("(d) => { S.dayIndex = d; }", 368)
        suppress_wf4(pg); isolate_star(pg, "chung_choning"); back_to_map(pg)
        pre = pg.evaluate("""() => ({
          presence: (S.starDay && S.starDay.presence) || {},
          mapTipRec: (S.mapTips && S.mapTips["rec_star"]) || null,
          mapTipAdm: (S.mapTips && S.mapTips["ad_adm"]) || null,
          storyOC: (typeof StoryOC !== 'undefined') ? 'object' : 'undef',
          chung: (S.stars && S.stars.chung_choning) || null })""")
        print("PRE:", pre)
        for attempt in (1, 2):
            pg.evaluate("() => { const p = document.querySelector('button[data-loc=\"rec_star\"].pin'); if (p) p.click(); return !!p; }")
            pg.wait_for_timeout(1200)
            st = pg.evaluate("""() => {
              const ov = document.getElementById('enc79-overlay');
              const sheet = document.getElementById('loc-sheet');
              return { overlay: !!ov, overlayName: ov ? ((ov.querySelector('.e79-name')||{}).textContent||'').trim() : null,
                       sheetOn: sheet ? sheet.className.includes(' on') : false,
                       title: (document.getElementById('loc-title')||{}).textContent.trim(),
                       triggered: (S.starDay && S.starDay.triggered) || 0 };
            }""")
            print(f"attempt{attempt}:", st)
            if st["overlay"]:
                break
            back_to_map(pg); pg.wait_for_timeout(500)
        # StoryOC listOpen check (if accessible)
        oc = pg.evaluate("""() => {
          try {
            if (typeof StoryOC === 'undefined' || !StoryOC.listOpen) return 'StoryOC n/a';
            const oc = StoryOC.listOpen({ checkNodePhase:true, player:true, ignoreSheetLoc:true }) || {};
            const open = (oc.open||[]).map(r=>r.id);
            return { openCount: open.length, open: open.slice(0, 20) };
          } catch(e){ return 'err:' + e.message; }
        }""")
        print("LISTOPEN:", oc)
        b.close()
finally:
    import signal
    try:
        srv.send_signal(signal.SIGTERM); srv.wait(timeout=5)
    except Exception:
        try: srv.kill()
        except Exception: pass
print("PROBE13 DONE")
