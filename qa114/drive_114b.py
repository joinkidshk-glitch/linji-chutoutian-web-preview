# -*- coding: utf-8 -*-
"""v20a114 實駕補驗（drive_114.py run 3 嘅 8a／8b）：重用 drive_114.Drv，
修咗 advance_day 強制／soft 日 fallback 後再驗。另記低所有 HTTP >=400 回應 URL，
等 run 3 嗰 8 個 console 404 可以實名。
用法：/home/hatch/pwenv49/bin/python qa114/drive_114b.py
產出：qa114/shots/drive_114b_*.png ＋ qa114/drive_114b.json
"""
import sys, os, json, traceback
sys.path.insert(0, os.path.expanduser("~/workspace/linji-work114/qa114"))
import drive_114 as D
from playwright.sync_api import sync_playwright

HERE = os.path.join(os.path.expanduser("~/workspace/linji-work114"), "qa114")
SHOTS = os.path.join(HERE, "shots")
LOG = {"items": {}, "errors": [], "console_errors": [], "bad_responses": []}


def record(item, verdict, detail):
    LOG["items"][item] = {"verdict": verdict, "detail": detail}
    print(f"[{item}] {verdict}: {json.dumps(detail, ensure_ascii=False)[:1000]}")


def main():
    srv = D.serve()
    try:
        with sync_playwright() as pw:
            b = pw.chromium.launch(executable_path=D.EXE, args=["--no-sandbox"])
            pg = b.new_page(viewport={"width": 390, "height": 844}, device_scale_factor=2)
            pg.on("pageerror", lambda e: LOG["errors"].append(str(e)))
            pg.on("console", lambda m: LOG["console_errors"].append(m.text) if m.type == "error" else None)
            pg.on("response", lambda r: LOG["bad_responses"].append(
                {"status": r.status, "url": r.url.split("?")[0][-120:]}) if r.status >= 400 else None)
            d = D.Drv(pg)

            # ---- 9_404_probe: run 3 had 8 console 404s with no URL; reproduce with
            # response logging while driving two encounters (cafe_cha + rec_star). ----
            d.new_game_slot3("I_fresh")
            p1 = d.enter_loc("cafe_cha", "I1_cafe")
            d.back_to_map()
            p2 = d.enter_loc("rec_star", "I2_recstar")
            d.back_to_map()
            record("9_404_probe", "PASS" if not LOG["bad_responses"] else "INFO",
                   {"cafe": p1["outcome"], "rec_star": p2["outcome"],
                    "bad_responses": LOG["bad_responses"],
                    "console_errors": LOG["console_errors"][:5],
                    "pageerrors": LOG["errors"][:5]})

            # ---- 8a-redux: film_lion one loc, talk first then board (2 entries) ----
            d.new_game_slot3("G_fresh")
            r1 = d.enter_loc("film_lion", "G1_film")
            s1 = d.st()
            btns1 = [x["t"] for x in s1.get("sheetBtns", [])]
            talk_ok, talk_note = False, ""
            has_talk = any("傾談" in t for t in btns1)
            if s1.get("sheetOn") and has_talk:
                d.click_text(["傾談"], 1200)
                st = d.st()
                talk_ok = bool(st.get("modalBtns") or st.get("modalTitle") or st.get("hasStage"))
                talk_note = (f"modalTitle={st.get('modalTitle')} btns={st.get('modalBtns')} "
                             f"stage={st.get('hasStage')} e79={st.get('e79Meta')}")
                d.shot("G_talk_open")
                out, _ = d.drive_dialogue(max_steps=15)
                talk_note += f" | drive->{out}"
                s2 = d.st()
                if not s2.get("sheetOn") and "v-map" not in s2.get("view", []):
                    d.ensure_map()
            d.back_to_map()
            r2 = d.enter_loc("film_lion", "G2_film_again")
            s3 = d.st()
            btns2 = [x["t"] for x in s3.get("sheetBtns", [])]
            board_ok, board_note = False, ""
            has_board = any("通告欄" in t for t in btns2)
            if s3.get("sheetOn") and has_board:
                d.click_text(["通告欄"], 1200)
                sb = d.st()
                board_ok = bool(sb.get("modalBtns") or sb.get("modalTitle"))
                board_note = f"modalTitle={sb.get('modalTitle')} btns={sb.get('modalBtns')}"
                d.shot("G_board_open")
                d.modal_click(["關閉", "返回", "知道了", "好"])
                pg.wait_for_timeout(600)
                board_note += f" | sheet_after_close={d.st().get('sheetOn')}"
            ok8a = has_talk and talk_ok and has_board and board_ok
            record("8a_sheet_buttons", "PASS" if ok8a else "FAIL",
                   {"entry1": r1["outcome"], "btns1": btns1,
                    "entry2": r2["outcome"], "btns2": btns2,
                    "talk_btn": has_talk, "talk_ok": talk_ok, "talk_note": talk_note,
                    "board_btn": has_board, "board_ok": board_ok, "board_note": board_note,
                    "shot": "shots/drive_114_G_talk_open.png / drive_114_G_board_open.png"})

            # ---- 8b-redux: Mon->Fri, spend 1 quota Fri, run busking schedule ----
            d.new_game_slot3("H_fresh")
            adv_log = []
            adv_ok = True
            for step in range(4):
                a = d.advance_day(f"H_adv{step}")
                adv_log.append({"step": step, "ok": a["ok"],
                                "day": a["after"]["day"] if a.get("after") else None,
                                "error": a.get("error"),
                                "log_tail": [] if a["ok"] else a.get("log", [])[-8:]})
                if not a["ok"]:
                    adv_ok = False
                    break
            s_fri = d.st()
            fri_ok = adv_ok and s_fri.get("day") == 4
            exec_ok, exec_note, r_fri = False, "", None
            day5_snap, money0 = None, 0
            if fri_ok:
                r_fri = d.enter_loc("cafe_cha", "H_fri_cafe")
                s_f2 = d.st()
                used_fri = (s_f2.get("travel") or {}).get("used")
                d.back_to_map()
                s_f3 = d.st()
                exec_note += (f"fri hint={s_f3.get('hintTravel')} startToday={s_f3.get('startToday')} "
                              f"used={used_fri} enter={r_fri['outcome']}; ")
                money0, stress0 = s_f3.get("money"), s_f3.get("stress")
                clicked = None
                try:
                    pg.locator("#map-start-today").click(timeout=4000)
                    clicked = "map-start-today"
                except Exception:
                    clicked = d.modal_click(["開始今日行程"]) or d.any_click(["開始今日行程"])
                pg.wait_for_timeout(1500)
                day5_snap = None
                for i in range(40):
                    s = d.st()
                    if day5_snap is None and s.get("day") == 5:
                        day5_snap = {"day": 5, "money": s.get("money"), "stress": s.get("stress"),
                                     "travel": s.get("travel"), "modalBtns": s.get("modalBtns")}
                    if s.get("day") == 5 and "v-map" in s.get("view", []) \
                            and not s.get("modalBtns") and not s.get("hasStage"):
                        exec_ok = True
                        break
                    if s.get("hasStage") or s.get("modalBtns"):
                        if not d.modal_click(["返回地圖", "繼續", "知道了", "好", "確定", "明白",
                                             "下一句", "關閉"]):
                            d.any_click(["返回地圖", "繼續"])
                        pg.wait_for_timeout(500)
                        continue
                    pg.wait_for_timeout(500)
                s_sat = d.st()
                exec_note += (f"exec_click={clicked} day5_snap={day5_snap} "
                              f"final_day={s_sat.get('day')} "
                              f"money {money0}->{s_sat.get('money')} "
                              f"stress {stress0}->{s_sat.get('stress')} "
                              f"travel_sat={s_sat.get('travel')} hint_sat={s_sat.get('hintTravel')}")
                d.shot("H_sat_map")
            # Friday counts as executed if day 5 was reached with money gained vs Friday
            # start (busking pays); the game may then auto-run forced Sat/Sun via
            # goToMapForBrowse kickSchedule, so final day can be >5 — that is not a fail.
            ok8b = fri_ok and (exec_ok or (day5_snap is not None
                                            and (day5_snap.get("money") or 0) > (money0 or 0)))
            record("8b_schedule_exec", "PASS" if ok8b else "FAIL",
                   {"advances": adv_log, "fri_day": s_fri.get("day"),
                    "fri_entry": r_fri["outcome"] if r_fri else None,
                    "exec_ok": exec_ok, "note": exec_note,
                    "shot": "shots/drive_114_H_sat_map.png"})
            d.shot("H_final")
            print("pageerrors:", len(LOG["errors"]), LOG["errors"][:5])
            print("console errors:", len(LOG["console_errors"]))
            print("bad responses:", json.dumps(LOG["bad_responses"], ensure_ascii=False))
            b.close()
    finally:
        D.stop(srv)
    with open(os.path.join(HERE, "drive_114b.json"), "w", encoding="utf-8") as f:
        json.dump(LOG, f, ensure_ascii=False, indent=1)
    print("WROTE", os.path.join(HERE, "drive_114b.json"))


if __name__ == "__main__":
    try:
        main()
    except Exception:
        traceback.print_exc()
        with open(os.path.join(HERE, "drive_114b.json"), "w", encoding="utf-8") as f:
            json.dump(LOG, f, ensure_ascii=False, indent=1)
        raise
