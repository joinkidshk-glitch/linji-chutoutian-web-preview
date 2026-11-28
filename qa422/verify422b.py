#!/usr/bin/env python3
"""v422 workflow B verification: seeded gate states + true-play flows."""
import asyncio, json, os, shutil, sys
sys.path.insert(0, "/home/hatch/workspace/linji-v422-verify")
from casual_lib import *

BASE = "/home/hatch/workspace/linji-work422/qa422"
SHOTDIR = os.path.join(BASE, "shots422b")
os.makedirs(SHOTDIR, exist_ok=True)
R = {}

async def shot2(page, name):
    try:
        await page.screenshot(path=os.path.join(SHOTDIR, name + ".png"))
        log(f" shot {name}")
    except Exception as e:
        log(f" shot fail {name}: {e}")

async def seed(page, cfg):
    return await page.evaluate("""(cfg) => {
      const key='starVolunteer_map_v19w';
      const s=JSON.parse(localStorage.getItem(key));
      s.dayIndex=cfg.day; s.money=cfg.money; s.stress=0;
      s.fame=cfg.fame; s.stage=cfg.stage; s.acting=cfg.acting; s.vocal=cfg.vocal; s.looks=cfg.looks; s.charm=cfg.charm; s.iq=cfg.iq; s.stamina=cfg.stamina;
      s.mapTips={}; s.travel114={day:cfg.day, used:0}; s.pendingAud=[]; s.booked=[]; s.shoots=[];
      s.intel381=null; s.tape383=null; s.ref422={};
      s.flags=s.flags||{}; delete s.flags.hoRef422Done; delete s.flags.dutyRef422Done; delete s.flags.pangRef422Done; delete s.flags.ho422Clue; delete s.flags.pang422Clue; delete s.flags.hoVisitDay;
      s.npcs=s.npcs||{}; s.npcs.agent=cfg.agent;
      s.stars=s.stars||{};
      s.stars.luk_baakyin=Object.assign({}, s.stars.luk_baakyin||{}, {fav:cfg.lukFav, met:true});
      s.stars.pang_siuki=Object.assign({}, s.stars.pang_siuki||{}, {fav:cfg.pangFav, met:true});
      s.enrolled=Object.assign({}, s.enrolled||{}, {train_stamina:true, train_acting:true});
      s.trainCount=Object.assign({}, s.trainCount||{}, {train_stamina:cfg.staminaLessons, train_acting:3});
      s.backstageDuties392=cfg.duties||[];
      s.story=s.story||{}; s.story.phase="P4"; s.story.done=Object.assign({}, s.story.done||{}, {N1:true,N2:true,N3:true,N4:true,N5:true,N6:true,N7:true,N8:true,N9:true,N10:true,N11:true,N12:true,N13:true,N14:true,N15:true,N16:true,N17:true,N18:true,N19:true});
      s.story.flags=Object.assign({}, s.story.flags||{}, {route_tv:true}); s.story.offers={};
      if(cfg.doneEmpty){ s.flags=s.flags||{}; (cfg.doneIds||[]).forEach(id=>{ s.flags["done_"+id]=true; }); }
      localStorage.setItem(key, JSON.stringify(s));
      return {day:s.dayIndex, agent:s.npcs.agent, luk:s.stars.luk_baakyin.fav, pang:s.stars.pang_siuki.fav};
    }""", cfg)

MID = {"day": 400, "money": 20000, "fame": 20, "stage": 30, "acting": 40, "vocal": 25, "looks": 30, "charm": 30, "iq": 25, "stamina": 80,
       "agent": 10, "lukFav": 30, "pangFav": 10, "staminaLessons": 5, "duties": []}

async def fresh(name, cfg):
    profile = os.path.join(BASE, f"profile422b_{name}")
    if os.path.exists(profile):
        shutil.rmtree(profile)
    pw, ctx, page = await launch(profile)
    set_log(os.path.join(BASE, f"verify422b_{name}.log"))
    await boot_fresh(page)
    sd = await seed(page, cfg)
    log(f"seeded {name}: {sd}")
    await boot_continue(page)
    for _ in range(40):
        f = await ui_flags(page)
        if f["choices"]:
            await page.evaluate("""() => { const b=document.querySelector('button.sp-choice'); if(b) b.click(); }""")
            await page.wait_for_timeout(500); continue
        if f["storyBtns"]:
            await click_contains(page, "下一句")
            await page.wait_for_timeout(400); continue
        break
    await handle_modals(page, f"boot-{name}")
    await back_to_map(page)
    await page.wait_for_timeout(800)
    return pw, ctx, page

async def click_contains(page, needle):
    return await page.evaluate("""(needle) => {
      const btns=Array.from(document.querySelectorAll('button')).filter(e=>e.offsetParent!==null || e.getClientRects().length>0);
      const b=btns.find(e=>(e.innerText||'').includes(needle));
      if(b){ b.click(); return (b.innerText||'').trim().slice(0,240); }
      return null;
    }""", needle)

async def modal_text(page):
    return await page.evaluate("""() => { const m=document.getElementById('modal-inner'); return m ? (m.innerText||'').slice(0,900) : ''; }""")


async def click_card_detail(page, marker):
    return await page.evaluate("""(marker) => {
      const els=[...document.querySelectorAll('*')].filter(e=>e.children.length===0 && (e.textContent||'').includes('查看詳情'));
      for(const el of els){ let n=el; for(let i=0;i<8&&n;i++){ const tx=n.textContent||''; if(tx.includes(marker) && tx.length<600){ el.click(); return 'card:'+marker; } n=n.parentElement; } }
      return null;
    }""", marker)


async def dismiss_story(page):
    for _ in range(40):
        f = await ui_flags(page)
        if f["choices"]:
            await page.evaluate("""() => { const b=document.querySelector('button.sp-choice'); if(b) b.click(); }""")
            await page.wait_for_timeout(500); continue
        if f["storyBtns"]:
            await click_contains(page, "下一句")
            await page.wait_for_timeout(400); continue
        break

async def click_gid(page, gid):
    return await page.evaluate("""(gid) => { const el=document.querySelector('.gig-teaser[data-gid="'+gid+'"]'); if(el){ el.click(); return 'gid:'+gid; } return null; }""", gid)

async def scenario_boundary():
    cfg = dict(MID); cfg.update({"acting":0,"stage":0,"vocal":0,"looks":0,"charm":0,"iq":0,"stamina":0,"fame":0,"doneEmpty":True,"doneIds":["gig_1990_ad_204", "gig_1990_ad_206", "gig_1990_film_201", "gig_1990_film_204", "gig_1990_film_205", "gig_1990_film_207", "gig_1990_film_208", "gig_1990_film_212", "gig_1990_film_301", "gig_1990_rec_202", "gig_1990_rec_203", "gig_1990_rec_204", "gig_1990_rec_205", "gig_1990_rec_210", "gig_1990_tv_201", "gig_1990_tv_202", "gig_1990_tv_204", "gig_1990_tv_206", "gig_1990_tv_207", "gig_1990_tv_208", "gig_1990_tv_209", "gig_1990_tv_210", "gig_1990_tv_211", "gig_1990_tv_212", "gig_1990_tv_213", "gig_1990_tv_214", "gig_1990_tv_215", "gig_1990_tv_217", "gig_1990_tv_218", "gig_1990_tv_301", "gig_1990_variety_203", "gig_1991_film_201", "gig_1991_film_202", "gig_1991_film_203", "gig_1991_film_204", "gig_1991_film_301", "gig_1991_rec_205", "gig_1991_tv_201", "gig_1991_tv_202", "gig_1991_tv_205", "gig_1991_tv_301", "gig_1992_film_301", "gig_1992_tv_301", "gig_1991_film_214", "gig_1990_film_305", "gig_1990_film_306"]})
    pw, ctx, page = await fresh("boundary", cfg)
    try:
        m0 = await page.evaluate("""() => S.money""")
        await enter_loc(page, "cafe_cha")
        await page.wait_for_timeout(600)
        c = await click_contains(page, "打聽補位消息")
        await page.wait_for_timeout(700)
        c2 = await click_contains(page, "確定")
        await page.wait_for_timeout(900)
        txt = await modal_text(page)
        body = await page.evaluate("""() => document.body.innerText.slice(0,3000)""")
        m1 = await page.evaluate("""() => S.money""")
        kept = await page.evaluate("""() => S.intel381""")
        R["boundary_low_buy"] = {"click": c, "confirm": c2, "modal": txt, "moneyBefore": m0, "moneyAfter": m1,
                                 "noCharge": m0 == m1, "explained": ("情報費不收" in body) or ("情報費不收" in txt),
                                 "keptGig": (kept or {}).get("gigId"),
                                 "ok": ((m0 == m1 and ("情報費不收" in body or "情報費不收" in txt)) or bool((kept or {}).get("gigId")))}
        await shot2(page, "boundary_low")
        log(f"boundary low buy: {R['boundary_low_buy']}")
    finally:
        await ctx.close(); await pw.stop()

async def scenario_intel():
    pw, ctx, page = await fresh("intel", MID)
    try:
        await enter_loc(page, "cafe_cha")
        await page.wait_for_timeout(600)
        who = await page.evaluate("""() => (document.getElementById('loc-who')||{}).textContent||''""")
        acts = await loc_acts(page)
        R["intel_cafe"] = {"who": who, "acts": [a["txt"][:160] for a in acts]}
        await shot2(page, "intel_cafe")
        c = await click_contains(page, "打聽補位消息")
        log(f"intel click: {c}")
        await page.wait_for_timeout(700)
        R["intel_confirm"] = await modal_text(page)
        await shot2(page, "intel_confirm")
        c2 = await click_contains(page, "確定")
        await page.wait_for_timeout(900)
        R["intel_after_buy_modal"] = await modal_text(page)
        await handle_modals(page, "intel-buy")
        await back_to_map(page)
        # home -> notebook intel book
        await enter_loc(page, "home")
        await page.wait_for_timeout(800)
        c3 = await page.evaluate("""() => { const b=document.getElementById('btn-intel381'); if(b){ b.click(); return 'clicked'; } return null; }""")
        await page.wait_for_timeout(700)
        R["intel_book"] = {"click": c3, "text": await modal_text(page)}
        await shot2(page, "intel_book")
        c4 = await click_contains(page, "覆電保留資格")
        await page.wait_for_timeout(700)
        st = await page.evaluate("""() => ({intel:S.intel381, money:S.money})""")
        R["intel_kept"] = {"reply": c4, "state": st}
        await handle_modals(page, "intel-reply")
        # go to gig loc board, open detail, audition
        loc = (st.get("intel") or {}).get("locId")
        await goto_map(page); await back_to_map(page)
        await enter_loc(page, loc)
        await page.wait_for_timeout(600)
        await click_contains(page, "通告欄")
        await page.wait_for_timeout(1200)
        board_txt = await page.evaluate("""() => document.body.innerText.slice(0,4000)""")
        R["intel_board_has_label"] = ("補位" in board_txt)
        await shot2(page, "intel_board")
        # click teaser containing gig title
        title = (st.get("intel") or {}).get("title", "")
        c5 = await click_gid(page, (st.get("intel") or {}).get("gigId",""))
        await page.wait_for_timeout(1000)
        detail = await page.evaluate("""() => document.body.innerText.slice(0,5000)""")
        R["intel_detail"] = {"click": c5, "hasDeadline": ("補位試鏡" in detail), "hasReady": ("條件已達標" in detail)}
        await shot2(page, "intel_detail")
        c6 = await click_contains(page, "接通告")
        await page.wait_for_timeout(1200)
        await click_contains(page, "確定")
        await page.wait_for_timeout(1500)
        await handle_modals(page, "intel-aud")
        pend = await page.evaluate("""() => (S.pendingAud||[]).map(p=>({gig:p.gigId, src:p.src422, ok:p.ok}))""")
        R["intel_audition"] = {"click": c6, "pending": pend, "modal": await modal_text(page)}
        await shot2(page, "intel_audition")
    finally:
        await ctx.close(); await pw.stop()

async def scenario_tape_ho():
    cfg = dict(MID); cfg["agent"] = 62
    pw, ctx, page = await fresh("tapeho", cfg)
    try:
        await enter_loc(page, "agency_ho")
        await page.wait_for_timeout(600)
        who = await page.evaluate("""() => (document.getElementById('loc-who')||{}).textContent||''""")
        acts = await loc_acts(page)
        R["ho_panel"] = {"who": who, "acts": [a["txt"][:200] for a in acts]}
        await shot2(page, "ho_panel")
        c = await click_contains(page, "自費拍攝試鏡帶")
        await page.wait_for_timeout(800)
        R["tape_picker"] = {"click": c, "text": await modal_text(page)}
        await shot2(page, "tape_picker")
        c2 = await click_contains(page, "可試鏡")
        await page.wait_for_timeout(800)
        R["tape_confirm"] = {"click": c2, "text": await modal_text(page)}
        await shot2(page, "tape_confirm")
        c3 = await click_contains(page, "確定")
        await page.wait_for_timeout(1000)
        st = await page.evaluate("""() => ({tape:S.tape383, money:S.money})""")
        R["tape_kept"] = {"confirm": c3, "state": st, "modal": await modal_text(page)}
        await handle_modals(page, "tape-done")
        # advance a day to fire ho tick (rel 62 seeded; visit +2 already applied)
        await back_to_map(page)
        await advance_day(page)
        await page.wait_for_timeout(1500)
        await handle_modals(page, "ho-advance")
        await back_to_map(page)
        ho = await page.evaluate("""() => ({agent:S.npcs.agent, ref:S.ref422, day:S.dayIndex})""")
        R["ho_ref"] = ho
        log(f"ho ref: {ho}")
        loc = ((ho.get("ref") or {}).get("ho") or {}).get("locId")
        if loc:
            await enter_loc(page, loc)
            await page.wait_for_timeout(500)
            await click_contains(page, "通告欄")
            await page.wait_for_timeout(1200)
            bt = await page.evaluate("""() => document.body.innerText.slice(0,4000)""")
            R["ho_board_label"] = ("何生引薦" in bt)
            await shot2(page, "ho_board")
    finally:
        await ctx.close(); await pw.stop()

async def scenario_duty_pang_stamina():
    cfg = dict(MID); cfg["pangFav"] = 72; cfg["day"] = 100
    cfg.update({"acting":99,"stage":99,"vocal":99,"looks":99,"charm":99,"iq":99,"stamina":99,"fame":60})
    cfg["duties"] = [{"kind": "場記", "production": "廟街夜話", "gigId": "duty392_clapper_a", "day": 10}]
    pw, ctx, page = await fresh("dutypang", cfg)
    try:
        # stamina progress + duty progress text evidence
        ev = await page.evaluate("""() => ({trainCount:S.trainCount, duties:S.backstageDuties392})""")
        R["stamina_duty_text"] = ev
        # duty gig detail screenshot: open board at film_harbour, click duty teaser
        await enter_loc(page, "film_harbour")
        await page.wait_for_timeout(600)
        await dismiss_story(page)
        await handle_modals(page, "duty-enc")
        await click_contains(page, "通告欄")
        await page.wait_for_timeout(1200)
        c = await click_gid(page, "duty392_editor_b")
        await page.wait_for_timeout(1000)
        detail = await page.evaluate("""() => document.body.innerText.slice(0,5000)""")
        R["duty_detail"] = {"click": c, "hasProgress": ("幕後履歷" in detail)}
        await shot2(page, "duty_detail")
        # audition the duty gig (req {} so always auditionable), then advance days to wrap
        R["duty_audition"] = {"attempts": []}
        for att in range(4):
            c2 = await click_contains(page, "接通告")
            await page.wait_for_timeout(1200)
            await click_contains(page, "確定")
            await page.wait_for_timeout(1500)
            pend = await page.evaluate("""() => (S.pendingAud||[]).map(p=>({gig:p.gigId, ok:p.ok}))""")
            R["duty_audition"]["attempts"].append({"click": c2, "pending": pend})
            await handle_modals(page, "duty-aud")
            if pend and pend[0].get("ok"):
                break
            await back_to_map(page); await advance_day(page); await page.wait_for_timeout(1000)
            await handle_modals(page, "duty-retry")
            await enter_loc(page, "film_harbour"); await page.wait_for_timeout(600)
            await dismiss_story(page); await handle_modals(page, "duty-retry-enc")
            await click_contains(page, "通告欄"); await page.wait_for_timeout(1000)
            await click_gid(page, "duty392_editor_b")
            await page.wait_for_timeout(1000)
        for i in range(24):
            st = await page.evaluate("""() => ({day:S.dayIndex, duties:S.backstageDuties392, ref:S.ref422, shoots:(S.shoots||[]).map(s=>s.gigId), pending:(S.pendingAud||[]).length})""")
            log(f"duty loop {i}: {st}")
            if (st.get("ref") or {}).get("duty"):
                R["duty_ref"] = st
                break
            await back_to_map(page)
            await advance_day(page)
            await page.wait_for_timeout(1200)
            await handle_modals(page, f"duty-day{i}")
            # confirm shoot placement if modal asks
            await click_contains(page, "確定")
            await page.wait_for_timeout(600)
            await handle_modals(page, f"duty-day{i}b")
        else:
            R["duty_ref"] = await page.evaluate("""() => ({duties:S.backstageDuties392, ref:S.ref422, day:S.dayIndex})""")
        # pang: tick should have fired during advances
        R["pang_ref"] = await page.evaluate("""() => ({pang:(S.stars.pang_siuki||{}).fav, ref:S.ref422, day:S.dayIndex})""")
        await shot2(page, "duty_pang_end")
        # negative tag pane evidence: grant a neg tag via applyCastingTags then open tags pane text
        await page.evaluate("""() => { S.castingTags=[{label:'八卦',from:'story:N8'}]; const b=document.getElementById('book389-handle'); if(b) b.click(); }""")
        await page.wait_for_timeout(800)
        await click_contains(page, "事業")
        await page.wait_for_timeout(600)
        await click_contains(page, "作品")
        await page.wait_for_timeout(600)
        await page.evaluate("""() => { const sm=document.querySelector('.tags389-fold summary'); if(sm) sm.click(); const d=document.querySelector('.tags389-fold'); if(d) d.scrollIntoView(); }""")
        await page.wait_for_timeout(800)
        neg = await page.evaluate("""() => { const el=document.getElementById('tags-list'); return {pane:(el?el.innerText:'').slice(0,1500)}; }""")
        await shot2(page, "neg_pane")
        R["neg_pane"] = neg
    finally:
        await ctx.close(); await pw.stop()


async def scenario_pang_board():
    cfg = dict(MID); cfg["pangFav"] = 72; cfg["day"] = 100
    pw, ctx, page = await fresh("pangboard", cfg)
    try:
        await advance_day(page); await page.wait_for_timeout(1200)
        await page.evaluate("""() => { const b=[...document.querySelectorAll('button')].find(x=>(x.textContent||'').includes('休息並過日')); if(b) b.click(); }"""); await page.wait_for_timeout(1500)
        await handle_modals(page, "pangboard-day")
        st = await page.evaluate("""() => ({ref:S.ref422, day:S.dayIndex})""")
        R["pang_grant"] = st
        slot = (st.get("ref") or {}).get("pang") or {}
        loc = slot.get("locId"); gid = slot.get("gigId")
        await back_to_map(page); await enter_loc(page, loc); await page.wait_for_timeout(600)
        await dismiss_story(page)
        await page.evaluate("""() => { const b=[...document.querySelectorAll('button')].find(x=>(x.textContent||'').trim()==='行開'); if(b) b.click(); }""")
        await page.wait_for_timeout(800)
        await dismiss_story(page)
        await click_contains(page, "通告欄"); await page.wait_for_timeout(1200)
        card = await page.evaluate("""(gid) => { const el=document.querySelector('.gig-teaser[data-gid="'+gid+'"]'); return el ? el.textContent.slice(0,300) : null; }""", gid)
        bt = await page.evaluate("""() => document.body.innerText.slice(0,4000)""")
        R["pang_board"] = {"loc": loc, "gid": gid, "card": card, "hasLabel": ("彭少祺引薦" in bt)}
        await shot2(page, "pang_board")
        if card:
            await click_gid(page, gid); await page.wait_for_timeout(1000)
            detail = await page.evaluate("""() => document.body.innerText.slice(0,5000)""")
            R["pang_detail"] = {"hasLabel": ("彭少祺引薦" in detail)}
            await shot2(page, "pang_detail")
    finally:
        await ctx.close(); await pw.stop()

async def main():
    import os
    only = os.environ.get("ONLY","")
    await scenario_boundary() if (not only or only=='scenario_boundary') else None
    await scenario_intel() if (not only or only=='scenario_intel') else None
    await scenario_tape_ho() if (not only or only=='scenario_tape_ho') else None
    await scenario_duty_pang_stamina() if (not only or only=='scenario_duty_pang_stamina') else None
    await scenario_pang_board() if (not only or only=='scenario_pang_board') else None
    with open(os.path.join(BASE, "verify422b_results.json"), "w", encoding="utf-8") as f:
        json.dump(R, f, ensure_ascii=False, indent=2)
    print(json.dumps(R, ensure_ascii=False, indent=2)[:8000])

asyncio.run(main())
