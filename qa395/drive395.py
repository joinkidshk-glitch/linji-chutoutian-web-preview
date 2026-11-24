# -*- coding: utf-8 -*-
"""v395 實駕 drive395：殺青「最後一 take」小遊戲 prototype。
用法：/home/hatch/pwenv49/bin/python qa395/drive395.py
工作副本 ~/workspace/linji-work395，port 8975，390x844 dsf 2，本地 HTTP（唔用 file://）。
A cue 直接入口：4 點完美＋拖放 2 個 X → 結果 4 完美＋走位 2/2。
B rhythm 直接入口：4 點＋長音按住 1400ms → 結果 5 完美＋長音完成。
C 跳過掣：開 cue 即撳跳過 → overlay 即刻消失。
D 失手：開 cue 唔撳 → 結果 4 失手。
E 殺青鉤子（播種）：新遊戲 → 寫入 1 日臨記電影通告 gig_1990_film_204 今日拍攝 →
  行程日結「拍攝日→殺青」撳繼續 → 彈 cue game → 玩完撳完成 → 獎勵頁照常 →
  下一日。同一播種再跑一次改撳跳過，兩局決定性數值必須一致
  （錢／人氣／次數；聲望差 ±1 係獎勵包隨機抽卡，壓力差係 R() 抖動，見 E-compare 註）。
"""
import sys, os, json, subprocess, time, signal, hashlib, urllib.request
from playwright.sync_api import sync_playwright

ROOT = "/home/hatch/workspace/linji-work395"
HERE = os.path.join(ROOT, "qa395")
SHOTS = os.path.join(HERE, "shots")
os.makedirs(SHOTS, exist_ok=True)
EXE = "/home/hatch/.cache/ms-playwright/chromium_headless_shell-1248/chrome-headless-shell-linux64/chrome-headless-shell"
PORT = 8975
BASE = f"http://127.0.0.1:{PORT}/index.html"
LOG = {"phases": {}, "errors": []}

def note(phase, msg, ok=True):
    LOG["phases"].setdefault(phase, []).append(msg)
    print(f"[{phase}] {'ok' if ok else 'FAIL'} {msg}", flush=True)

def serve():
    p = subprocess.Popen(["python3", "-m", "http.server", str(PORT)], cwd=ROOT,
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(1.2)
    with urllib.request.urlopen(f"http://127.0.0.1:{PORT}/minigame395.js", timeout=5) as r:
        assert r.status == 200
    print("serve ok", flush=True)
    return p

def stop(p):
    try:
        p.send_signal(signal.SIGTERM); p.wait(timeout=5)
    except Exception:
        try: p.kill()
        except Exception: pass

def visible_buttons(pg):
    return pg.evaluate("""() => [...document.querySelectorAll('button')].filter(b => {
      const r = b.getBoundingClientRect(); return r.width > 0 && r.height > 0 && b.offsetParent !== null;
    }).map(b => (b.innerText || '').trim()).filter(t => t).slice(0, 30)""")

def click_text(pg, texts, wait=900):
    for t in texts:
        try:
            ok = pg.evaluate("""(t) => {
              const els = [...document.querySelectorAll('button')].filter(e => {
                const r = e.getBoundingClientRect();
                return r.width > 0 && r.height > 0 && (e.innerText || '').trim() === t; });
              if (!els.length) return false; els[0].click(); return true; }""", t)
            if ok:
                pg.wait_for_timeout(wait); return t
        except Exception:
            pass
    return None

def click_substr(pg, texts, wait=900):
    """子字串撳掣（標題掣帶副標題，精確比對唔到；跟 drive131 click_first）。"""
    for t in texts:
        try:
            loc = pg.locator(f"button:has-text('{t}')")
            for i in range(loc.count()):
                el = loc.nth(i)
                try:
                    if el.is_visible() and el.is_enabled():
                        el.click(timeout=900); pg.wait_for_timeout(wait); return t
                except Exception:
                    pass
        except Exception:
            pass
    return None

def overlay_present(pg):
    return pg.evaluate("() => !!document.getElementById('mg395-overlay')")

def wait_overlay(pg, timeout=8000):
    try:
        pg.wait_for_selector("#mg395-overlay", timeout=timeout); return True
    except Exception:
        return False

def wait_result(pg, timeout=15000):
    try:
        pg.wait_for_selector("#mg395-result", timeout=timeout); return True
    except Exception:
        return False

def result_counts(pg):
    return pg.evaluate("""() => {
      const r = document.getElementById('mg395-result');
      if (!r) return null;
      const grades = [...r.querySelectorAll('.mg395-grade')].map(g => ({
        label: (g.querySelector('.mg395-glabel') || {}).innerText || '',
        count: (g.querySelector('.mg395-gcount') || {}).innerText || '' }));
      const extra = [...r.querySelectorAll('.mg395-rextra')].map(e => e.innerText);
      return { grades, extra, text: r.innerText.slice(0, 400) }; }""")

# --- 精準撳點：在頁內用 performance.now() 對齊 __mg395.t0 dispatch pointerdown ---
def cue_perfect_taps(pg):
    pg.evaluate("""() => {
      const st = window.__mg395; if (!st) return;
      st.cues.forEach((t, i) => {
        const delay = Math.max(0, st.t0 + t - performance.now());
        setTimeout(() => {
          const tr = document.querySelectorAll('.mg395-track')[i];
          if (tr) tr.dispatchEvent(new PointerEvent('pointerdown', { bubbles: true, cancelable: true, pointerId: 1 }));
        }, delay);
      });
    }""")

def rhythm_perfect_taps(pg):
    pg.evaluate("""() => {
      const st = window.__mg395; if (!st) return;
      const tap = document.getElementById('mg395-tap');
      if (!tap) return;
      st.notes.forEach((t, i) => {
        const delay = Math.max(0, st.t0 + t - performance.now());
        if (i < st.notes.length - 1) {
          setTimeout(() => tap.dispatchEvent(new PointerEvent('pointerdown', { bubbles: true, cancelable: true, pointerId: 1 })), delay);
        } else {
          setTimeout(() => tap.dispatchEvent(new PointerEvent('pointerdown', { bubbles: true, cancelable: true, pointerId: 1 })), delay);
          setTimeout(() => tap.dispatchEvent(new PointerEvent('pointerup', { bubbles: true, cancelable: true, pointerId: 1 })), delay + 1400);
        }
      });
    }""")

def drag_token_to_x(pg, x_index=0):
    try:
        token = pg.locator("#mg395-awei").bounding_box()
        xs = pg.locator(".mg395-x").nth(x_index).bounding_box()
        if not token or not xs: return False
        cx, cy = token["x"] + token["width"] / 2, token["y"] + token["height"] / 2
        tx, ty = xs["x"] + xs["width"] / 2, xs["y"] + xs["height"] / 2
        pg.mouse.move(cx, cy); pg.mouse.down()
        for s in range(1, 11):
            pg.mouse.move(cx + (tx - cx) * s / 10, cy + (ty - cy) * s / 10)
            pg.wait_for_timeout(30)
        pg.mouse.up(); pg.wait_for_timeout(400)
        return pg.evaluate("(i) => document.querySelectorAll('.mg395-x')[i].classList.contains('done')", x_index)
    except Exception as e:
        LOG["errors"].append(f"drag: {e}"); return False

def main():
    srv = serve()
    try:
        with sync_playwright() as pw:
            br = pw.chromium.launch(executable_path=EXE, args=[
                "--no-sandbox", "--proxy-server=http://127.0.0.1:18081",
                "--ignore-certificate-errors"])
            ctx = br.new_context(viewport={"width": 390, "height": 844},
                                 device_scale_factor=2, is_mobile=True, has_touch=True)
            pg = ctx.new_page()
            pg.on("pageerror", lambda e: LOG["errors"].append(f"pageerror: {e}"))
            pg.on("console", lambda m: LOG["errors"].append(f"console.{m.type}: {m.text}") if m.type == "error" else None)

            # ---------- A: cue 直接入口（先排撳點計時，再拖放，唔好等 Cue 過期） ----------
            pg.goto(BASE + "?minigame=cue")
            assert wait_overlay(pg), "A overlay 未出"
            st = pg.evaluate("() => window.__mg395 && { kind: window.__mg395.kind, cues: window.__mg395.cues }")
            note("A-cue", f"overlay 出，kind={st['kind']} cues={st['cues']}")
            cue_perfect_taps(pg)
            d1 = drag_token_to_x(pg, 0); d2 = drag_token_to_x(pg, 1)
            note("A-cue", f"拖放 X1={d1} X2={d2}")
            assert wait_result(pg), "A 結果未出"
            rc = result_counts(pg)
            note("A-cue", f"結果 grades={rc['grades']} extra={rc['extra']}")
            pg.screenshot(path=os.path.join(SHOTS, "395A_cue_result.png"))
            assert rc["grades"][0]["count"] == "4", "A 完美唔係 4"
            assert "2 / 2" in str(rc["extra"]), "A 走位唔係 2/2"
            pg.click("#mg395-done"); pg.wait_for_timeout(600)
            assert not overlay_present(pg), "A 完成後 overlay 未消失"
            note("A-cue", "撳完成 → overlay 消失，PASS")

            # ---------- B: rhythm 直接入口（即排撳點，唔等） ----------
            pg.goto(BASE + "?minigame=rhythm")
            assert wait_overlay(pg), "B overlay 未出"
            st = pg.evaluate("() => window.__mg395 && { kind: window.__mg395.kind, notes: window.__mg395.notes }")
            note("B-rhythm", f"overlay 出，kind={st['kind']} notes={st['notes']}")
            rhythm_perfect_taps(pg)
            assert wait_result(pg), "B 結果未出"
            rc = result_counts(pg)
            note("B-rhythm", f"結果 grades={rc['grades']} extra={rc['extra']}")
            pg.screenshot(path=os.path.join(SHOTS, "395B_rhythm_result.png"))
            assert rc["grades"][0]["count"] == "5", "B 完美唔係 5"
            assert "完成" in str(rc["extra"]), "B 長音唔係完成"
            pg.click("#mg395-done"); pg.wait_for_timeout(600)
            assert not overlay_present(pg), "B 完成後 overlay 未消失"
            note("B-rhythm", "撳完成 → overlay 消失，PASS")

            # ---------- C: 跳過掣 ----------
            pg.goto(BASE + "?minigame=cue")
            assert wait_overlay(pg), "C overlay 未出"
            pg.click("#mg395-skip"); pg.wait_for_timeout(500)
            assert not overlay_present(pg), "C 跳過後 overlay 未消失"
            note("C-skip", "跳過掣 → 即刻消失，PASS")

            # ---------- D: 失手（唔撳） ----------
            pg.goto(BASE + "?minigame=cue")
            assert wait_overlay(pg), "D overlay 未出"
            assert wait_result(pg, timeout=20000), "D 結果未出"
            rc = result_counts(pg)
            note("D-miss", f"結果 grades={rc['grades']}")
            pg.screenshot(path=os.path.join(SHOTS, "395D_cue_miss.png"))
            assert rc["grades"][3]["count"] == "4", "D 失手唔係 4"
            note("D-miss", "唔撳 → 4 失手，PASS")
            pg.click("#mg395-done"); pg.wait_for_timeout(400)

            # ---------- E: 殺青鉤子（播種） ----------
            # 流程（probe395b 已驗）：新遊戲（直入，存檔 slot 1）→ 播種 1 日 204 通告今日拍攝
            # → reload → 繼續 → 確定本週行程 → N1 故事 16 句 → 抉擇 → 拍攝日結「殺青」
            # → 撳繼續 → 彈小遊戲 → 玩／跳過 → 獎勵頁 → 下一日。
            # 對照：錢／聲望／人氣／weekGigsDone／gigCount／done204 必須兩局一致
            # （決定性數值）；壓力／演技／台風／智商有 R() 抖動，只記錄唔斷言。
            for run, mode in [(1, "play"), (2, "skip")]:
                # 每局清存檔先開新遊戲，否則 run 2 會載入 run 1 嘅舊 save（行程已定、dayIndex 1）。
                pg.goto(BASE); pg.wait_for_timeout(1200)
                pg.evaluate("() => localStorage.clear()")
                pg.goto(BASE); pg.wait_for_timeout(2500)
                click_substr(pg, ["新遊戲"], 1200)
                pg.wait_for_timeout(800)
                click_substr(pg, ["覆蓋", "確定", "確認"], 900)
                click_substr(pg, ["跳過教學"], 1200)
                click_substr(pg, ["開始寫手帳"], 1400)
                # 播種：讀 slot 1 存檔（開局後已寫入，見 probe395），寫入 1 日 204 通告今日拍攝。
                # 必須喺第一次「確定本週行程」之前寫入，否則 S 已入記憶體，localStorage 改動無用。
                seed = pg.evaluate("""() => {
                  const KEY = 'starVolunteer_map_v19w';
                  const raw = localStorage.getItem(KEY);
                  if (!raw) return { err: 'no save slot1' };
                  const S = JSON.parse(raw);
                  const wd = ((S.dayIndex % 7) + 7) % 7;
                  const shoot = { id: 'mg395wrap1', gigId: 'gig_1990_film_204', title: '戲院散場路人',
                    workTitle: '', roleLabel: '路人', type: '電影', tier: '臨記', roleScale: 'tv_cameo_short',
                    daysLeft: 1, totalDays: 1, pay: 42, fame: 7, popularity: 5, locId: 'film_studio',
                    doneDays: 0, shootWeekdays: [0,1,2,3,4,5,6], hiredAtDay: S.dayIndex | 0,
                    deadlineDays: 14, deadlineDay: (S.dayIndex | 0) + 14, overdueConsumed: false, breachFee: null };
                  S.shoots = [shoot];
                  const wp = (S.weekPlan || ['scout_all','scout_all','scout_all','scout_all','scout_all','scout_all','scout_all']).slice(0, 7);
                  while (wp.length < 7) wp.push('scout_all');
                  wp[wd] = 'shoot:mg395wrap1';
                  S.weekPlan = wp;
                  localStorage.setItem(KEY, JSON.stringify(S));
                  return { dayIndex: S.dayIndex, wd, weekPlan: wp,
                    before: { money: S.money, fame: S.fame, popularity: S.popularity, stress: S.stress } };
                }""")
                if "err" in seed:
                    note(f"E{run}", f"播種失敗：{seed}", ok=False)
                    raise AssertionError(f"E{run} 播種失敗：{seed}")
                note(f"E{run}", f"播種 ok dayIndex={seed['dayIndex']} wd={seed['wd']} weekPlan={seed['weekPlan']} before={seed['before']}")
                pg.goto(BASE); pg.wait_for_timeout(2500)
                # 「繼續」載入 active slot（slot 1）
                if not click_substr(pg, ["繼續"], 1200):
                    note(f"E{run}", f"無「繼續」掣，title btns={visible_buttons(pg)}", ok=False)
                    raise AssertionError(f"E{run} 讀檔失敗")
                pg.wait_for_timeout(1200)
                # 行今日行程
                try:
                    pg.locator("#btn-confirm-plan").click(timeout=3000); pg.wait_for_timeout(1200)
                except Exception as e:
                    note(f"E{run}", f"讀檔後 confirm-plan 撳唔到：{e}", ok=False)
                    raise AssertionError(f"E{run} 讀檔後行程掣失敗")
                # 穿過 N1 故事（16 句）＋抉擇 → 日結殺青板
                reached_dayend = False
                for step in range(40):
                    pg.wait_for_timeout(700)
                    if overlay_present(pg):
                        break
                    modal = pg.evaluate("() => (document.getElementById('modal-inner')||{}).innerText || ''")
                    if "殺青" in modal and "戲院散場路人" in modal:
                        reached_dayend = True
                        note(f"E{run}", f"step {step} 日結板：殺青：戲院散場路人")
                        break
                    c = click_text(pg, ["下一句", "繼續", "知道了", "好", "確定", "確認", "關閉"], 600)
                    if not c:
                        c = click_substr(pg, ["繼續跑今日行程", "關閉"], 600)
                    if not c:
                        c = click_substr(pg, ["接電影散工賺快錢", "跟張子駿班底學動作戲", "下一句"], 600)
                    if not c:
                        note(f"E{run}", f"step {step} 無掣可撳，modal={modal[:120]!r} btns={visible_buttons(pg)[:8]}", ok=False)
                        break
                pg.screenshot(path=os.path.join(SHOTS, f"395E{run}_dayend.png"))
                assert reached_dayend or overlay_present(pg), f"E{run} 未到殺青日結板"
                # 日結板撳繼續 → 應該彈小遊戲
                got_game = overlay_present(pg)
                if not got_game:
                    clicked = click_text(pg, ["開始今日行程", "返回地圖", "開始並結算當日", "繼續", "回家結算"], 1200)
                    pg.wait_for_timeout(1200)
                    got_game = wait_overlay(pg, timeout=5000)
                    note(f"E{run}", f"日結繼續撳咗 {clicked}，game 出={got_game}")
                assert got_game, f"E{run} 殺青後無彈小遊戲"
                st = pg.evaluate("() => window.__mg395 && window.__mg395.kind")
                note(f"E{run}", f"殺青彈出 game kind={st}")
                pg.screenshot(path=os.path.join(SHOTS, f"395E{run}_minigame.png"))
                if mode == "play":
                    cue_perfect_taps(pg) if st == "cue" else rhythm_perfect_taps(pg)
                    assert wait_result(pg), f"E{run} 結果未出"
                    rc = result_counts(pg)
                    note(f"E{run}", f"玩完結果 grades={rc['grades']}")
                    pg.click("#mg395-done"); pg.wait_for_timeout(1200)
                else:
                    pg.click("#mg395-skip"); pg.wait_for_timeout(1200)
                    note(f"E{run}", "撳跳過")
                assert not overlay_present(pg), f"E{run} game 完成後 overlay 未消失"
                # 獎勵頁照常（傳媒／票房／成績反響，敘事 only）
                reward_txt = pg.evaluate("() => (document.getElementById('modal-inner')||{}).innerText || ''")
                note(f"E{run}", f"game 後畫面：{reward_txt[:160]!r}")
                pg.screenshot(path=os.path.join(SHOTS, f"395E{run}_after_game.png"))
                # 穿過獎勵頁返地圖／下一日
                for _ in range(6):
                    if not click_text(pg, ["收下這份反響", "繼續", "知道了", "好", "返回地圖", "開始今日行程"], 1000):
                        break
                    pg.wait_for_timeout(600)
                after = pg.evaluate("""() => {
                  const raw = localStorage.getItem('starVolunteer_map_v19w');
                  if (!raw) return null; const S = JSON.parse(raw);
                  return { dayIndex: S.dayIndex, money: S.money, fame: S.fame,
                    popularity: S.popularity, stress: S.stress, acting: S.acting,
                    weekGigsDone: S.weekGigsDone,
                    gigCount: S.story && S.story.gigCount, shootsLeft: (S.shoots || []).length,
                    done204: S.flags && S.flags.done_gig_1990_film_204 }; }""")
                note(f"E{run}", f"跑完存檔：{after}")
                LOG["phases"][f"E{run}-final"] = after
                pg.screenshot(path=os.path.join(SHOTS, f"395E{run}_final.png"))

            f1, f2 = LOG["phases"].get("E1-final"), LOG["phases"].get("E2-final")
            if f1 and f2:
                # 決定性字段：錢／人氣／weekGigsDone／gigCount／shootsLeft／done204。
                # 聲望唔入斷言：applyPostShootRewardDual 派聲望＝calib60FameGain(1＋Σ隨機抽卡
                # stageVolumeDelta)，pack 喺殺青嗰刻（queuePostShootRewardOnWrap，日結板之前）
                # 已經建好兼即派——小遊戲喺撳繼續先至開，掂唔到；兩局抽卡唔同，聲望差 ±1 係
                # 原獎勵系統隨機，唔係小遊戲造成。壓力／演技同理（shootDailyDelta 用 R()）。
                det = ["money", "popularity", "weekGigsDone", "gigCount", "shootsLeft", "done204"]
                same = all(f1.get(k) == f2.get(k) for k in det)
                note("E-compare", f"玩 vs 跳過決定性數值一致={same} 玩={f1} 跳={f2}（聲望 {f1.get('fame')} vs {f2.get('fame')} 差隨機抽卡，壓力 {f1.get('stress')} vs {f2.get('stress')} 差 R() 抖動）", ok=same)
                assert same, "玩 vs 跳過數值唔一致"
            br.close()
    finally:
        stop(srv)
    print("DRIVE395 ALL PASS", json.dumps(LOG, ensure_ascii=False)[:3000], flush=True)

if __name__ == "__main__":
    main()
