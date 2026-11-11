# -*- coding: utf-8 -*-
"""v20a107 覆蓋重計：同 v106 口徑（handoff106/coverage_report.md）——
來源 linji-expression-inventory/work/lines_classified.json（2644 行）
× linji-fullbody-batch/manifest.json（96 條，已合併 fix2）。
分類→資產：happy→smile、neutral→base、serious→serious、sad→sad、
surprise→surprise、shy→shy、think→think、angry→angry。
「精確覆蓋」= 該角非 neutral 對白入面，類別有同名表情資產嘅句數。
預期：全局 403/593（68.0%）→ 439/593（74.0%）；
阿偉 s2/s3 階段 60/188（31.9%）→ 123/188（65.4%）。
數字對唔上即 exit 1，唔硬報。
用法：python3 qa107/coverage107.py
輸出：qa107/coverage107.json ＋ qa107/coverage_report107.md
"""
import json, os
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
LINES = "/home/hatch/workspace/linji-expression-inventory/work/lines_classified.json"
MANI = "/home/hatch/workspace/linji-fullbody-batch/manifest.json"
CAT2EXPR = {"happy": "smile", "neutral": "base", "serious": "serious",
            "sad": "sad", "surprise": "surprise", "shy": "shy",
            "think": "think", "angry": "angry"}

lines = json.load(open(LINES, encoding="utf-8"))
mani = json.load(open(MANI, encoding="utf-8"))
assets = defaultdict(set)   # speakerId -> {expr,...}
for m in mani:
    assets[m["speakerId"]].add(m["expr"])
print(f"lines={len(lines)} manifest={len(mani)} speakers_in_manifest={len(assets)}")

# 名冊：manifest 有嘅 speaker（awi 計 s1；awi_s2/s3 另計階段表）
roster = sorted(assets.keys())
nonneutral = [x for x in lines if x["category"] != "neutral" and x["char"] in roster]
# 注意：char='awi' 嘅行用 s1 資產計全局（同 v106）
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
               # 顯示用：剔走 s2_/s3_ 階段款（佢哋屬階段表，唔係 s1 資產）
               "have": sorted(e for e in assets[sp] - {"base"}
                              if not e.startswith(("s2_", "s3_")))}

# 阿偉分階段：同一 609 句池，唔同資產集。資產集按檔名派生（唔按
# manifest speakerId/expr——v106 嗰 6 條 s2/s3 記做 speakerId=awi、
# expr=s2_smile 式，fix2 8 條記做 speakerId=awi_s2、expr=think；
# 檔名先係對話解析器認圖嘅 ground truth，兩種記法都指向同一檔名）。
import re as _re
stage_assets = {}
for sid in ("awi", "awi_s2", "awi_s3"):
    s = set()
    for m in mani:
        fn = os.path.basename(m["file"])
        mm = _re.match(rf"^{sid}_(.+)\.webp$", fn)
        if mm:
            s.add(mm.group(1))
    stage_assets[sid] = s
print("stage assets:", {k: sorted(v) for k, v in stage_assets.items()})
awi_lines = [x for x in lines if x["char"] == "awi"]
awi_nn = [x for x in awi_lines if x["category"] != "neutral"]
stages = {}
for st, sid in (("s1", "awi"), ("s2", "awi_s2"), ("s3", "awi_s3")):
    cov = [x for x in awi_nn if CAT2EXPR[x["category"]] in stage_assets[sid]]
    miss = Counter(x["category"] for x in awi_nn if CAT2EXPR[x["category"]] not in stage_assets[sid])
    stages[st] = {"covered": len(cov), "of": len(awi_nn),
                  "pct": round(100 * len(cov) / len(awi_nn), 1), "missing": dict(miss)}

# 新圖 8 張各自對應句數（死圖檢查）
NEW = [("awi_s2", "think"), ("awi_s3", "think"), ("so_jiyan", "happy"),
       ("cheung_tsijun", "serious"), ("ho_sang", "sad"),
       ("gao_wenhan", "serious"), ("tang_laiping", "serious"),
       ("chow_choiyi", "think")]
new_counts = {}
for sid, cat in NEW:
    char = "awi" if sid.startswith("awi_") else sid
    n = sum(1 for x in lines if x["char"] == char and x["category"] == cat)
    new_counts[f"{sid}:{cat}"] = n
print("new asset lines:", new_counts)

# 殘留零覆蓋角
zero = [sp for sp in roster if per[sp]["nonneutral"] and per[sp]["covered"] == 0]
print("zero-coverage speakers:", zero)

out = {"global": {"covered": len(covered), "of": len(nonneutral)},
       "per_speaker": per, "awi_stages": stages,
       "new_asset_lines": new_counts, "zero_coverage": zero}
json.dump(out, open(os.path.join(HERE, "coverage107.json"), "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)

# 預期對數（v106 基線 → v107 預期），對唔上即 FAIL
EXP = {"global": (439, 593), "s2": (123, 188), "s3": (123, 188),
       "new": {"awi_s2:think": 63, "awi_s3:think": 63, "so_jiyan:happy": 12,
               "cheung_tsijun:serious": 6, "ho_sang:sad": 6,
               "gao_wenhan:serious": 4, "tang_laiping:serious": 4,
               "chow_choiyi:think": 4}}
fails = []
if (len(covered), len(nonneutral)) != EXP["global"]:
    fails.append(f"global {(len(covered), len(nonneutral))} != expected {EXP['global']}")
for st in ("s2", "s3"):
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

# 報告
L = []
L.append("# v20a107 情緒覆蓋率報告\n")
L.append("來源：`linji-expression-inventory/work/lines_classified.json`（2644 行）× "
         "`linji-fullbody-batch/manifest.json`（96 條，已合併 fix2 8 張）。\n"
         "口徑同 v106：精確覆蓋＝該角非 neutral 對白入面，類別有同名表情資產嘅句數。\n")
L.append("## 總覽\n")
L.append(f"- 名冊非 neutral 句精確覆蓋：**{len(covered)}/{len(nonneutral)} = "
         f"{100*len(covered)/len(nonneutral):.1f}%**（v106：403/593＝68.0%）\n")
L.append(f"- 阿偉 s1：{stages['s1']['covered']}/{stages['s1']['of']}＝{stages['s1']['pct']}%（不變）\n")
L.append(f"- 阿偉 s2：**{stages['s2']['covered']}/{stages['s2']['of']}＝{stages['s2']['pct']}%**"
         f"（v106：60/188＝31.9%）\n")
L.append(f"- 阿偉 s3：**{stages['s3']['covered']}/{stages['s3']['of']}＝{stages['s3']['pct']}%**"
         f"（v106：60/188＝31.9%）\n")
L.append("\n## 新圖 8 張各自對應句數（全部 >0，唔係死圖）\n")
L.append("| 新資產 | 對應分類句數 |")
L.append("|---|---|")
for (sid, cat) in NEW:
    L.append(f"| {sid}_{CAT2EXPR[cat]}.webp | {new_counts[f'{sid}:{cat}']} |")
L.append("\n## 逐角表（有變動嘅角）\n")
L.append("| 角 | 非neutral | 精確覆蓋 | 覆蓋率 | 有資產類別（除base） | 缺資產類別（句數） |")
L.append("|---|---|---|---|---|---|")
for sp in ("awi", "so_jiyan", "cheung_tsijun", "ho_sang", "gao_wenhan",
           "tang_laiping", "chow_choiyi"):
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
L.append("\n## 其他值得注意嘅殘留缺口（非零但未補）\n")
for sp in ("yip_manji", "pang_siuki", "gu_mingfai", "fong_siulung",
           "ngai_wingnaam", "lin_hiu", "chung_choning", "luk_baakyin"):
    p = per[sp]
    miss = "、".join(f"{k}({v})" for k, v in sorted(p["missing"].items()))
    L.append(f"- {sp}：{p['covered']}/{p['nonneutral']}（{100*p['covered']/p['nonneutral']:.1f}%）；缺 {miss}")
L.append("\n## 數據註\n")
L.append("- extra_ad_fen 嘅「sad」9 句經 v106 查證係旁白假陽性（同一句旁白重複），唔使補圖；"
         "本表沿用 v106 口徑，佢仍列零覆蓋。\n")
L.append("- 阿偉 s1/s2/s3 共用同一 609 句池；s2/s3 各補 think 63 句，"
         "故階段覆蓋各升 63 句，但全局 awi 只計 s1 一次，think 早已有圖，"
         "全局升幅只計其餘 6 張新圖對應嘅 36 句（12+6+6+4+4+4）。\n")
L.append("- manifest 記法分裂（老實註）：v106 嗰 6 條 s2/s3（base/smile/serious）"
         "記做 speakerId=awi、expr=s2_smile 式；fix2 8 條記做 speakerId=awi_s2/awi_s3、"
         "expr=think。本報告階段覆蓋按檔名派生資產集（檔名先係解析器 ground truth），"
         "唔依賴呢個分裂嘅記法；合併時冇改寫 v106 舊條目。\n")
open(os.path.join(HERE, "coverage_report107.md"), "w", encoding="utf-8").write("\n".join(L))
print("COVERAGE OK: global 439/593, awi s2/s3 123/188, new-asset lines all match")
