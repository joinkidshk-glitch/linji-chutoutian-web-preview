#!/usr/bin/env python3
"""v20a160 M9 時序驗證（drive160.py 補充）：won_932 再跑一次，但用單次原子 evaluate
同時讀 caption＋旗標＋performance.now()，消除兩次 evaluate 之間嘅 skew；
順便記低撳「出席」嗰刻嘅 performance.now() 做 beat 對照基線。
目標：證實 fanfare attempt 同 reveal caption 係同一個 advance() 入面發生（誤差 <500ms），
掌聲 attempt 係 fanfare 之後 900ms ± 容差。
用法：/home/hatch/pwenv49/bin/python qa160-m9/verify_timing.py
"""
import json, subprocess, sys, time, os
sys.path.insert(0, "/home/hatch/workspace/linji-work160-m9/qa160-m9")
import drive160 as d
from playwright.sync_api import sync_playwright

def atomic_poll(pg):
    return pg.evaluate("""() => {
      const cap = document.querySelector('.awd62-caption');
      const st = document.querySelector('.awd62-stage');
      return { present: !!st,
               caption: cap ? cap.textContent : '',
               flag: window.__awards160Audio ? { fanfare: window.__awards160Audio.fanfare, applause: window.__awards160Audio.applause } : null,
               now: Math.round(performance.now()) };
    }""")

def main():
    srv = subprocess.Popen(["python3", "-m", "http.server", str(d.PORT), "--bind", "127.0.0.1"],
                           cwd=d.ROOT, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(1.0)
    # 重試包裝：run_once 內含完整 browser session，失敗就成個重開（同 drive160.py 主迴圈一樣；
    # 「新遊戲」click 間歇性等 navigation 超時係環境波動，唔係 game code）
    out = {}
    last_err = None
    for attempt in range(3):
        try:
            out = run_once()
            break
        except Exception as e:
            last_err = e
            print(f"  verify attempt {attempt + 1} failed: {e!r}", flush=True)
            time.sleep(5)
    if not out:
        print("VERIFY ERROR", repr(last_err))
        sys.exit(2)
    try:
        json.dump(out, open(os.path.join(d.HERE, "verify_timing.json"), "w"), ensure_ascii=False, indent=1)
    except Exception as e:
        print("NOTE verify_timing.json write failed:", repr(e))
    print("VERDICT", out.get("verdict"))
    sys.exit(0 if out.get("verdict") == "PASS" else 1)

def run_once():
    srv = subprocess.Popen(["python3", "-m", "http.server", str(d.PORT), "--bind", "127.0.0.1"],
                           cwd=d.ROOT, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(1.0)
    out = {}
    try:
        d.check_served()  # 唔驗就可能靜默載咗兄弟工人嗰份（port 佔用教訓，見 drive160.py）
        with sync_playwright() as p:
            b = p.chromium.launch(executable_path=d.EXE)
            try:
                ctx = b.new_context(viewport={"width": 430, "height": 932})
                pg = ctx.new_page()
                errs = []
                pg.on("pageerror", lambda e: errs.append(str(e)))
                pg.on("requestfailed", lambda r: errs.append("REQFAIL " + r.url[:120]))
                assert d.new_game_to_map(pg), "no map"
                d.seed_strong(pg, d.day_index(1991, 10, 20))
                fw = d.force_won(pg, d.FILM)
                assert fw["pack"].get("bestOutcome") == "won", fw["pack"]
                assert d.click_vis_btn(pg, "出席")
                t0perf = pg.evaluate("() => Math.round(performance.now())")
                # 原子輪詢：每 ~120ms 一次，記 caption／flag 每次轉變＋performance.now()
                log = []
                last_cap, last_flag = None, "null"
                t_start = time.time()
                while time.time() - t_start < 16:
                    s = atomic_poll(pg)
                    if not s["present"]:
                        log.append({"perf": s["now"], "event": "stage_gone"})
                        break
                    if s["caption"] != last_cap:
                        log.append({"perf": s["now"], "event": "caption", "caption": s["caption"][:80]})
                        last_cap = s["caption"]
                    fk = json.dumps(s["flag"], sort_keys=True) if s["flag"] else "null"
                    if fk != last_flag:
                        log.append({"perf": s["now"], "event": "flag", "flag": s["flag"]})
                        last_flag = fk
                    pg.wait_for_timeout(120)
                out = {"clickPerf": t0perf, "log": log, "pageerrors": errs,
                       "finalFlag": d.audio_flag(pg), "resources": d.audio_resources(pg)}
                # 時序斷言（performance.now() 時間）
                def first(ev, pred):
                    for e in log:
                        if e["event"] == ev and pred(e):
                            return e["perf"]
                    return None
                t_reveal_cap = first("caption", lambda e: "得獎！" in (e.get("caption") or ""))
                t_fan = first("flag", lambda e: (e.get("flag") or {}).get("fanfare") in ("attempted", "playing", "blocked"))
                t_app = first("flag", lambda e: (e.get("flag") or {}).get("applause") in ("attempted", "playing", "blocked"))
                out["times"] = {"revealCaptionPerf": t_reveal_cap, "fanfarePerf": t_fan, "applausePerf": t_app}
                out["checks"] = {
                    "reveal_caption_seen": t_reveal_cap is not None,
                    "fanfare_attempted": t_fan is not None,
                    "applause_attempted": t_app is not None,
                    # fanfare attempt 同 reveal caption 同一輪詢／相鄰輪詢（<600ms），唔係早一個 beat
                    "fanfare_within_600ms_of_reveal": (t_reveal_cap is not None and t_fan is not None and abs(t_fan - t_reveal_cap) <= 600),
                    # 掌聲係 fanfare 之後 500–1400ms（規格 900ms；觀測係「首次見到」嘅輪詢時間，
                    # fanfare 嗰邊觀測可以遲一個輪詢（~120–300ms），所以下限放寬到 500ms——
                    # 同 drive160.py 嘅 applause_delay_ge_500ms 同一容差）
                    "applause_500_to_1400ms_after_fanfare": (t_fan is not None and t_app is not None and 500 <= (t_app - t_fan) <= 1400),
                    "no_pageerror": len(errs) == 0,
                    "fanfare_mp3_fetched": any(r.get("url") == "awards_fanfare.mp3" and (r.get("transferSize") or 0) > 0 for r in (out["resources"] or [])),
                    "applause_mp3_fetched": any(r.get("url") == "awards_applause.mp3" and (r.get("transferSize") or 0) > 0 for r in (out["resources"] or [])),
                }
                out["verdict"] = "PASS" if out["checks"] and all(out["checks"].values()) else "FAIL"
                print(json.dumps(out, ensure_ascii=False, indent=1))
                ctx.close()
            finally:
                b.close()
    finally:
        d.stop_server(srv)
    return out

if __name__ == "__main__":
    main()
