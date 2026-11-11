# v20a108 D-8（二期）靜態守門：WF4 接入 v106 對話組件——接線齊全／
# 盤點表（36 事件／8 新／28 舊）同 index.html 事件數據一致／
# 分工護欄（WF4 唔掂組件 CSS／幾何／渲染函數）／紀律（SAVE key／softRev／?v= 不變）／
# 阿偉全身資產齊全／事件內容零改動（傳 baseline 路徑先對照）。
# 用法：python3 tests/test_dlg108_static.py [path-to-index.html] [path-to-baseline-index.html]
import json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
IDX = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else os.path.join(HERE, "..", "index.html")
ROOT = os.path.dirname(IDX)
with open(IDX, encoding="utf-8") as f:
    src = f.read()

fails = []
def ck(name, cond):
    print(("PASS " if cond else "FAIL ") + name)
    if not cond: fails.append(name)
def info(msg): print("INFO " + msg)

# ---------- 紀律：三個不變 ----------
ck("SAVE key 不變", "starVolunteer_map_v19w" in src)
ck("softRev 不變", "s107" in src)
ck("產品 ?v= 不變", "v20a10" in src)

# ---------- 接線：WF4 呼叫現成 DLG106 入口 ----------
def wiring_ok(s):
    return all(x in s for x in [
        "function wf4SpeakerId108(", "function wf4OnTableIds108(",
        "function wf4DlgCharsHtml108(", "function wf4BeatStageHtml108(",
        "dlg106ResolveSides", "dlg106Candidates", "dlg106ResolveCategory",
        "dlg106HasFullbody", "wf4DlgExtraCands108", "__dlg106Err",
        "data-dlg-fallbacks", "dlg106-on", "dlg106-plate",
    ])
ck("WF4 接線齊全（新函數＋現成 DLG106 入口＋後備鏈）", wiring_ok(src))
ck("反證：整爛接線（dlg106ResolveSides 改名）後 wiring_ok 必須轉 False",
   not wiring_ok(src.replace("dlg106ResolveSides", "dlg106ResolveSideX")))
ck("wf4PlayEvent 逐句經 beatHtml 分流（新／舊兩路）",
   "wf4BeatStageHtml108(ev, b, scene105)" in src and "onTable108" in src)
ck("抉擇／結算屏維持舊文字（headDlg108 只喺 beatHtml 出現兩次：定義＋使用）",
   src.count("headDlg108") == 2)

# ---------- 分工護欄：唔掂組件 CSS／幾何／渲染函數 ----------
ck("分工：WF4 冇專屬 CSS class（wf4-play 零出現）", "wf4-play" not in src)
ck("分工：DLG106 模組標記原封不動", src.count("/* ===== v20a106 DLG106") == 1
   and "/* ===== DLG106 模組完 ===== */" in src)
ck("分工：冇改 spDlgCharsHtml／paintDlg106（只出現原有定義＋原有呼叫）",
   src.count("function spDlgCharsHtml") == 1 and src.count("const paintDlg106") == 1)
ck("分工：WF4 舞台只用組件原有 class（sp-stage／dlg106-on／dlg106-plate／sp-plate-narration105）",
   all(x in src for x in ["sp-stage sp-mode-", "dlg106-on", "sp-plate-narration105"]))
i = src.find("/* === v20a106 DLG106 對話呈現層")
seg = src[i:i + 1400] if i >= 0 else ""
ck("分工：DLG106 CSS 原規則在場（人物高 50%＋250ms 過渡）",
   "height:50%" in seg and "250ms" in seg)

# ---------- 盤點表：由 index.html 事件數據獨立計出，再對預期集合 ----------
def extract_events(s):
    j = s.find("const DAILY_EVENTS_WF4 = [")
    k = s.find("[", j)
    depth, end = 0, k
    in_str = False
    esc = False
    for n in range(k, len(s)):
        ch = s[n]
        if in_str:
            if esc: esc = False
            elif ch == "\\": esc = True
            elif ch == '"': in_str = False
        else:
            if ch == '"': in_str = True
            elif ch == "[": depth += 1
            elif ch == "]":
                depth -= 1
                if depth == 0:
                    end = n + 1
                    break
    raw = s[k:end]
    # JS 字面量→JSON：補無引號鍵名、清尾逗號（事件文案本身全雙引號字串）
    js = re.sub(r'([{,]\s*)([A-Za-z_][A-Za-z0-9_]*)\s*:', r'\1"\2":', raw)
    js = re.sub(r',(\s*[\]}])', r'\1', js)
    return json.loads(js)

evs = extract_events(src)
NEW108 = {"wf4_ev_cha02", "wf4_ev_home01", "wf4_ev_st01", "wf4_ev_st03",
          "wf4_ev_boss01", "wf4_ev_boss02", "wf4_ev_boss03", "wf4_ev_day02"}
with_awi = {e["id"] for e in evs if any(b.get("sp") == "阿偉" for b in e["beats"])}
ck("事件總數 36", len(evs) == 36)
ck("有阿偉講者嘅事件＝預期 8 單（盤點表同數據一致）", with_awi == NEW108)
ck("其餘 28 單冇阿偉（舊路徑）", len(evs) - len(with_awi) == 28)
named_no_asset = set()
for e in evs:
    for b in e["beats"]:
        sp = b.get("sp")
        if sp and sp not in ("旁白", "阿偉"):
            named_no_asset.add(sp)
ck("表外講者清單有阿媽／霞姐／阿成／昌叔／表姨媽（具名但冇資產）",
   {"阿媽", "霞姐", "阿成", "昌叔", "表姨媽"} <= named_no_asset)
info("表外講者（%d）：%s" % (len(named_no_asset), "、".join(sorted(named_no_asset))))

# ---------- 阿偉全身資產齊全（s1 七款＋s2/s3 各三款） ----------
FB = os.path.join(ROOT, "assets", "story", "fullbody")
if os.path.isdir(FB):
    have = set(os.listdir(FB))
    need_s1 = {"awi_%s.webp" % x for x in ["base", "smile", "serious", "sad", "surprise", "shy", "think"]}
    need_s23 = {"awi_s2_%s.webp" % x for x in ["base", "smile", "serious"]} | \
               {"awi_s3_%s.webp" % x for x in ["base", "smile", "serious"]}
    ck("阿偉 s1 七款全身圖齊全", need_s1 <= have)
    ck("阿偉 s2/s3 各三款全身圖齊全", need_s23 <= have)
    ck("候補鏈尾段資產在場（bust＋剪影）",
       os.path.exists(os.path.join(ROOT, "assets", "story", "c1", "char_hero_bust_default.png"))
       and os.path.exists(os.path.join(ROOT, "assets", "story", "era_stars", "enc105_stand_silhouette.png")))
else:
    ck("assets/story/fullbody/ 存在", False)

# ---------- 事件內容零改動（有 baseline 先對照） ----------
if len(sys.argv) > 2:
    with open(os.path.abspath(sys.argv[2]), encoding="utf-8") as f:
        base = f.read()
    base_evs = extract_events(base)
    ck("事件內容零改動（DAILY_EVENTS_WF4 同 baseline 逐字一致）",
       json.dumps(evs, ensure_ascii=False, sort_keys=True)
       == json.dumps(base_evs, ensure_ascii=False, sort_keys=True))
    i108 = src.find("function wf4SpeakerId108(")
    ck("反證：baseline 冇 wf4SpeakerId108", "function wf4SpeakerId108(" not in base)
else:
    info("事件內容對照跳過（未傳 baseline 路徑；跑全套 A/B 時對照）")

print("RESULT " + ("FAIL (%d)" % len(fails) if fails else "PASS"))
sys.exit(1 if fails else 0)
