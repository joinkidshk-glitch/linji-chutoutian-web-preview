# -*- coding: utf-8 -*-
"""v20a123 覆蓋重計：同 v106/v107 口徑（精確覆蓋＝該角非 neutral 對白入面，
類別有同名表情資產嘅句數），但資產集改由 repo assets/story/fullbody/ 目錄
檔名直接派生（檔名先係對話解析器 ground truth，唔再經 batch manifest）。
來源 linji-expression-inventory/work/lines_classified.json（2644 行）。
預期：全局 439/593（74.0%）→ 458/593（77.2%）；
阿偉 s1 184/188 → 188/188（100%）；s2/s3 123/188（65.4%）→ 184/188（97.9%）。
數字對唔上即 exit 1，唔硬報。
用法：python3 qa123/coverage123.py
輸出：qa123/coverage123.json ＋ qa123/coverage_report123.md
"""
import json, os, re
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
LINES = "/home/hatch/workspace/linji-expression-inventory/work/lines_classified.json"
FB = os.path.join(HERE, "..", "assets", "story", "fullbody")
CAT2EXPR = {"happy": "smile", "neutral": "base", "serious": "serious",
            "sad": "sad", "surprise": "surprise", "shy": "shy",
            "think": "think", "angry": "angry"}

lines = json.load(open(LINES, encoding="utf-8"))
assets = defaultdict(set)
for fn in os.listdir(FB):
    m = re.match(r"^(.+)_(base|smile|serious|sad|surprise|shy|think|angry)\.webp$", fn)
    if m:
        assets[m.group(1)].add(m.group(2))
print(f"lines={len(lines)} fullbody_files={len(os.listdir(FB))} speakers_in_dir={len(assets)}")

roster = sorted(s for s in assets if not s.startswith("boss_"))
nonneutral = [x for x in lines if x["category"] != "neutral" and x["char"] in roster]
covered = [x for x in nonneutral if CAT2EXPR[x["category"]] in assets[x["char"]]]
print(f"global exact: {len(covered)}/{len(nonneutral)} = {len(covered)/len(nonneutral):.1%}")

per = {}
for sp in roster:
    sp_lines = [x for x in lines if x["char"] == sp]
    nn = [x for x in sp_lines if x["category"] != "neutral"]
    cov = [x for x in nn if CAT2EXPR[x["category"]] in assets[sp]]
    miss = Counter(x["category"] for x in nn if CAT2EXPR[x["category"]] not in assets[sp])
    per[sp] = {"total": len(sp_lines), "nonneutral": len(nn),
               "covered": len(cov), "missing": dict(miss),
               "have": sorted(e for e in assets[sp] - {"base"}
                              if not e.startswith(("s2_", "s3_")))}

awi_lines = [x for x in lines if x["char"] == "awi"]
awi_nn = [x for x in awi_lines if x["category"] != "neutral"]
stages = {}
for st, sid in (("s1", "awi"), ("s2", "awi_s2"), ("s3", "awi_s3")):
    cov = [x for x in awi_nn if CAT2EXPR[x["category"]] in assets[sid]]
    miss = Counter(x["category"] for x in awi_nn if CAT2EXPR[x["category"]] not in assets[sid])
    stages[st] = {"covered": len(cov), "of": len(awi_nn),
                  "pct": round(100 * len(cov) / len(awi_nn), 1), "missing": dict(miss)}

NEW = [("awi_s2", "surprise"), ("awi_s2", "sad"), ("awi_s2", "shy"),
       ("awi_s3", "surprise"), ("awi_s3", "sad"), ("awi_s3", "shy"),
       ("awi", "angry"), ("chung_choning", "think"), ("chung_choning", "happy"),
       ("ho_sang", "angry"), ("liu_bingxing", "shy"), ("pang_siuki", "surprise")]
new_counts = {}
for sid, cat in NEW:
    char = "awi" if sid.startswith("awi") else sid
    n = sum(1 for x in lines if x["char"] == char and x["category"] == cat)
    new_counts[f"{sid}:{cat}"] = n
print("new asset lines:", new_counts)
print("awi stages:", stages)

zero = [sp for sp in roster if per[sp]["nonneutral"] and per[sp]["covered"] == 0]
print("zero-coverage speakers:", zero)

out = {"global": {"covered": len(covered), "of": len(nonneutral)},
       "per_speaker": per, "awi_stages": stages,
       "new_asset_lines": new_counts, "zero_coverage": zero}
json.dump(out, open(os.path.join(HERE, "coverage123.json"), "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)

EXP = {"global": (458, 593), "s1": (188, 188), "s2": (184, 188), "s3": (184, 188),
       "new": {"awi_s2:surprise": 27, "awi_s2:sad": 20, "awi_s2:shy": 14,
               "awi_s3:surprise": 27, "awi_s3:sad": 20, "awi_s3:shy": 14,
               "awi:angry": 4, "chung_choning:think": 4, "chung_choning:happy": 3,
               "ho_sang:angry": 4, "liu_bingxing:shy": 2, "pang_siuki:surprise": 2}}
fails = []
if (len(covered), len(nonneutral)) != EXP["global"]:
    fails.append(f"global {(len(covered), len(nonneutral))} != expected {EXP['global']}")
for st in ("s1", "s2", "s3"):
    if (stages[st]["covered"], stages[st]["of"]) != EXP[st]:
        fails.append(f"awi {st} {(stages[st]['covered'], stages[st]['of'])} != expected {EXP[st]}")
for k, v in EXP["new"].items():
    if new_counts.get(k) != v:
        fails.append(f"new {k}={new_counts.get(k)} != expected {v}")
if fails:
    print("COVERAGE MISMATCH:")
    for f in fails:
        print("  FAIL " + f)
    raise SystemExit(1)

L = []
L.append("# v20a123 情緒覆蓋率報告\n")
L.append("來源：`linji-expression-inventory/work/lines_classified.json`（2644 行）× "
         "`assets/story/fullbody/` 目錄檔名（130 張，含新 12 張）。\n"
         "口徑同 v106/v107：精確覆蓋＝該角非 neutral 對白入面，類別有同名表情資產嘅句數。\n")
L.append("## 總覽\n")
L.append(f"- 名冊非 neutral 句精確覆蓋：**{len(covered)}/{len(nonneutral)} = "
         f"{100*len(covered)/len(nonneutral):.1f}%**（v107：439/593＝74.0%）\n")
L.append(f"- 阿偉 s1：**{stages['s1']['covered']}/{stages['s1']['of']}＝{stages['s1']['pct']}%**（v107：184/188＝97.9%）\n")
L.append(f"- 阿偉 s2：**{stages['s2']['covered']}/{stages['s2']['of']}＝{stages['s2']['pct']}%**"
         f"（v107：123/188＝65.4%）\n")
L.append(f"- 阿偉 s3：**{stages['s3']['covered']}/{stages['s3']['of']}＝{stages['s3']['pct']}%**"
         f"（v107：123/188＝65.4%）\n")
L.append("\n## 新圖 12 張各自對應句數（全部 >0，唔係死圖）\n")
L.append("| 新資產 | 對應分類句數 |")
L.append("|---|---:|")
for (sid, cat) in NEW:
    L.append(f"| {sid}_{CAT2EXPR[cat]}.webp | {new_counts[f'{sid}:{cat}']} |")
L.append("\n## 逐角表（有變動嘅角）\n")
L.append("| 角 | 非neutral | 精確覆蓋 | 覆蓋率 | 有資產類別（除base） | 缺資產類別（句數） |")
L.append("|---|---|---|---|---|---|")
for sp in ("awi", "chung_choning", "ho_sang", "liu_bingxing", "pang_siuki"):
    p = per[sp]
    miss = "、".join(f"{k}({v})" for k, v in sorted(p["missing"].items())) or "—"
    L.append(f"| {sp} | {p['nonneutral']} | {p['covered']} | "
             f"{100*p['covered']/p['nonneutral']:.1f}% | {', '.join(p['have'])} | {miss} |")
L.append("\n## 殘留缺口（零精確覆蓋嘅角）\n")
for sp in zero:
    p = per[sp]
    miss = "、".join(f"{k}({v})" for k, v in sorted(p["missing"].items()))
    L.append(f"- **{sp}**：{p['covered']}/{p['nonneutral']}；缺 {miss}；"
             f"有資產 {', '.join(p['have']) or '（只有 base）'}")
L.append("\n## 其他值得注意嘅殘留缺口（非零但未補；最大單項 ≤5 句）\n")
for sp in ("fong_siulung", "pang_siuki", "gu_mingfai", "yip_manji",
           "lan_ruoxi", "ching_tinlok", "chow_choiyi", "ko_chunkit"):
    p = per[sp]
    miss = "、".join(f"{k}({v})" for k, v in sorted(p["missing"].items()))
    L.append(f"- {sp}：{p['covered']}/{p['nonneutral']}（{100*p['covered']/p['nonneutral']:.1f}%）；缺 {miss}")
L.append("\n## 數據註\n")
L.append("- 阿偉 s2/s3 精確覆蓋剩 angry 4 句——但 runtime 候補鏈（dlg106Candidates）"
         "s2/s3 angry 會經跨階段後備攞到新出嘅 `awi_angry.webp`，實際顯示 100%，"
         "唔會退 base。\n")
L.append("- extra_ad_fen 嘅「sad」9 句經 v106 查證係旁白假陽性（同一句旁白重複），唔使補圖；"
         "本表沿用 v106 口徑，佢仍列零覆蓋。\n")
L.append("- 全局升幅 +19 句（439→458）：awi_angry 4、chung think 4＋happy 3、ho angry 4、"
         "liu shy 2、pang surprise 2；s2/s3 六張唔計入全局（s1 早已有 surprise／sad／shy）。\n")
open(os.path.join(HERE, "coverage_report123.md"), "w", encoding="utf-8").write("\n".join(L))
print("COVERAGE OK: global 458/593, awi s1 188/188, s2/s3 184/188, new-asset lines all match")
