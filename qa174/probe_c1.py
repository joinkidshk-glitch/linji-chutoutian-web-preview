#!/usr/bin/env python3
"""v174 C1 探針：gallery reveal 中央人 vs 講台，邊個像素贏？
做法：gallery 實駕到 reveal beat，讀 canvas toDataURL，同底圖原圖同座標像素對比。
overlap 區 (x196-226, y184-192) 若 == 底圖像素 -> 講台喺上面（真遮）；若 != -> 人物喺上面（review C1 假設錯）。"""
import base64, io, json, os, subprocess, sys, time
sys.path.insert(0, "/home/hatch/workspace/linji-design-review-v170")
sys.path.insert(0, "/home/hatch/workspace/linji-work170/qa170")
sys.path.insert(0, "/home/hatch/workspace/linji-design-review-v168")
sys.path.insert(0, "/home/hatch/workspace/linji-design-review-v160")
import drive170_p2 as W
import drive168r as D168
import drive160r as D

HERE = "/home/hatch/workspace/linji-work174/qa174"
ROOT = "/home/hatch/workspace/linji-work174"
PORT = 8994
D168.ROOT = ROOT; D168.SHOTS = HERE; D168.PORT = PORT
D.ROOT = ROOT; D.SHOTS = HERE; D.PORT = PORT
W.SHOTS = HERE; W.PORT = PORT

def main():
    srv = subprocess.Popen(["python3", "-m", "http.server", str(PORT), "--bind", "127.0.0.1"],
                           cwd=ROOT, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        D.check_served()
        from playwright.sync_api import sync_playwright
        with sync_playwright() as pw:
            pg = pw.chromium.launch(executable_path=D.EXE, args=["--no-sandbox"]).new_page(viewport={"width": 430, "height": 932})
            errs = []
            pg.on("pageerror", lambda e: errs.append(str(e)))
            assert D.new_game_to_map(pg), "去唔到地圖"
            D.install_draw_patch(pg)
            W.install_fig_patch(pg)
            day = D.day_index(1991, 10, 20)
            D.seed_plain(pg, day)
            fa = D.force_award(pg, "award_harbour_film", "gallery", want_won=False)
            assert fa["pack"].get("bestOutcome") == "gallery", fa["pack"]
            assert D.attend(pg), "請柬出席撳唔到"
            # poll 到 reveal beat
            data_url = None
            for _ in range(100):
                st = D168.stage_state168(pg)
                if W.seg_of(st) == "reveal":
                    pg.wait_for_timeout(300)
                    data_url = pg.evaluate("""() => {
                      const cv = document.querySelector('.awd62-stage canvas');
                      return cv ? cv.toDataURL('image/png') : null; }""")
                    break
                pg.wait_for_timeout(150)
            assert data_url, "等唔到 reveal"
            open(os.path.join(HERE, "c1_live.png"), "wb").write(base64.b64decode(data_url.split(",", 1)[1]))
            print("saved c1_live.png")
            print("saved; analyse with system python3")
            print("pageerrors:", errs)
            pg.close()
    finally:
        D.stop_server(srv)

if __name__ == "__main__":
    main()
