# v395：殺青「最後一 take」小遊戲 prototype — 靜態測試（釘字串／接線／禁區守門）。
# 用法：python3 tests/test_v395_static.py [repo-root]
import json
import os
import sys

root = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(__file__), "..")
src = open(os.path.join(root, "index.html"), encoding="utf-8").read()
js = open(os.path.join(root, "minigame395.js"), encoding="utf-8").read()
gigs = {g["id"]: g for g in json.load(open(os.path.join(root, "content/gigs_new.json"), encoding="utf-8"))["gigs"]}
fails = []


def ok(msg, cond):
    if cond:
        print("PASS " + msg)
    else:
        fails.append(msg)
        print("FAIL " + msg)


# ---- (1) 載入：檔尾 script 標籤，主 script 之後，index.html 淨增 1 行 ----
ok("v395 index.html 載入 minigame395.js", '<script src="minigame395.js"></script>' in src)
ok("v395 script 標籤喺主 script 之後（檔尾）",
   src.index('<script src="minigame395.js"></script>') > src.rindex("</script>", 0, src.index('<script src="minigame395.js"></script>')))

# ---- (2) 殺青鉤子：afterDayRes 攔截，玩完／跳過先行原獎勵鏈 ----
ok("v395 afterDayRes 有 minigame395Eligible 檢查",
   "minigame395Eligible(wrapGigId395)" in src)
ok("v395 afterDayRes 開 game 用輪換 kind",
   "openMinigame395(minigame395PickKind(wrapGigId395)" in src)
ok("v395 afterDayRes 完成後行原獎勵鏈（afterGame395）",
   "onDone: afterGame395" in src and "afterGame395();" in src)
ok("v395 殺青分支記低 gigId／title",
   "wrapGigId395=sh.gigId" in src and 'wrapTitle395=sh.title||""' in src)
ok("v395 同一單同一日只彈一次（去重 key）",
   'window.mg395DoneKey395!==String(wrapGigId395)+"|"+(S.dayIndex|0)' in src)
ok("v395 唔經週加速（accel cont 到 afterDayRes 之間無開 game）",
   "openMinigame395" not in src[src.index("flushWeekAccelSummary"):src.index("const afterDayRes")])
ok("v395 獎勵包喺 game 開之前已經建好兼派好（queuePostShootRewardOnWrap 行先）",
   src.index("queuePostShootRewardOnWrap(sh)") < src.index("openMinigame395(minigame395PickKind"))

# ---- (3) 唔郁嘅嘢：SAVE／softRev／?v=／頒獎贏線 ----
ok("v395 SAVE key 不變 starVolunteer_map_v19w", "starVolunteer_map_v19w" in src)
ok("v395 softRev 不變 s107", 'SOFT_REV = "s107"' in src)
ok("v395 產品 ?v= 不變 20a10", '"20a10"' in src)
ok("v395 頒獎贏線 0.875 不變", "AWARDS62_WIN_LINE = 0.875" in src)

# ---- (4) allowlist：3 張 1990 臨記級電影，開局接得到 ----
for gid in ["gig_1990_film_204", "gig_1990_film_205", "gig_1990_film_206"]:
    g = gigs.get(gid)
    ok("v395 allowlist %s 喺庫內" % gid, g is not None)
    if g:
        ok("v395 allowlist %s 係 1990 電影臨記" % gid,
           g.get("year") == 1990 and g.get("type") == "電影" and g.get("tier") == "臨記")
ok("v395 allowlist 204／205 無 req（開局即接）",
   gigs["gig_1990_film_204"].get("req") == {} and gigs["gig_1990_film_205"].get("req") == {})
ok("v395 allowlist 206 req stamina 55 ≤ 開局體能 75",
   gigs["gig_1990_film_206"].get("req", {}).get("stamina") == 55)
ok("v395 allowlist 唔包主線 gig_1991_tv_203",
   "gig_1991_tv_203" not in js.split("MINIGAME395_ALLOWLIST")[1].split("]")[0])

# ---- (5) 判定窗／長音閾值／四級雙碼 ----
ok("v395 判定窗 80／250／500 齊全",
   "a <= 80" in js and "a <= 250" in js and "a <= 500" in js)
ok("v395 長音閾值 0.8", "0.8 * t" in js)
ok("v395 四級顏色金／藍／灰／紅齊全",
   all(c in js for c in ["#FFD700", "#4A9EFF", "#A0A0A0", "#FF4444"]))
ok("v395 四級形狀星／圈／半圓／叉齊全",
   all(c in js for c in ["★", "●", "◐", "✕"]))
ok("v395 結果畫面講明唔寫入數值",
   "唔會寫入聲望、信用、片酬或好感" in js)

# ---- (6) 觸控目標：Cue 圈／阿偉 ≥60px、跳過掣 60×44px ----
ok("v395 跳過掣 60×44", "width:60px;min-height:44px" in js.replace(" ", ""))
ok("v395 阿偉拖放圈 60px", ".mg395-awei{position:absolute;width:60px;height:60px" in js)
ok("v395 撳掣 ≥64px 高", "min-height:64px" in js)
ok("v395 完成掣 ≥48px 高", "min-height:48px" in js)

# ---- (7) 獎勵零寫入守門：prototype 檔唔可以掂獎勵／狀態／存檔 ----
FORBIDDEN = [
    "applyGain60", "applyCalib60", "applyCastingTags", "bumpNpc",
    "enc79OnWrap", "br89OnGigComplete", "genericCreditOnGigComplete283",
    "end95AddWrap", "end229AddWrap", "contractCredit361OnWrap",
    "grant229GigById", "duty392GigById",
    "S.fame", "S.money", "S.credit", "S.popularity", "S.stress", "S.flags",
    "saveQ", "localStorage", "sessionStorage",
]
for tok in FORBIDDEN:
    ok("v395 零寫入守門：無 %s" % tok, tok not in js)

# ---- (8) 直接試玩入口 ----
ok("v395 ?minigame 參數解析", "minigame395ParamFromSearch" in js)
ok("v395 load 後自啟直接入口", "minigame395BootDirect()" in js)
ok("v395 兩機制 kind 齊全", '"cue"' in js and '"rhythm"' in js)

print("v395 static: %d failed" % len(fails))
if fails:
    sys.exit(1)
