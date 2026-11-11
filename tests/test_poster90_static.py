#!/usr/bin/env python3
"""v20a90 POSTER90 靜態守門：作品圖／主演顯示時機。
- 完成前場合（接通告詳情 openCastingNoticeDetail、通告卡 gigCardHtml）唔准渲染
  成品作品圖／主演行。
- 完成後場合保留：wrapPoster59Html（殺青）、worksWallEntries59（作品牆）照用 poster59Path。
- SAVE key／softRev／?v= 不變。
對 v20a89/v20a90-未修 index 必須 FAIL（反證）。
"""
import os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
html = open(os.path.join(ROOT, "index.html"), encoding="utf-8").read()
fails = []

def seg(start_marker, end_marker=None):
    i = html.index(start_marker)
    j = html.index(end_marker, i) if end_marker else len(html)
    return html[i:j]

def seg_fn(start_marker):
    i = html.index(start_marker)
    j = html.index("\nfunction ", i + 100)
    return html[i:j]

# 1. 詳情頁模板（castingNoticeDetailHtml；openCastingNoticeDetail 係開啟器，
#    其 hired/shooting/wrapped 狀態分支共用同一模板或狀態 body）：唔再渲染海報/主演行
detail = seg_fn("function castingNoticeDetailHtml")
for bad in ["${poster59fig}", "${leadRow59}", "cn-poster59", '<span class="k">主演</span>']:
    if bad in detail:
        fails.append(f"詳情頁仍渲染 {bad}")
if "POSTER90" not in detail:
    fails.append("詳情頁缺 POSTER90 標記註")
opener = seg_fn("function openCastingNoticeDetail")
for bad in ["${poster59fig}", "${leadRow59}", "poster59Path", "leadStar59Of"]:
    if bad in opener:
        fails.append(f"openCastingNoticeDetail 狀態分支仍渲染 {bad}")

# 2. 通告卡：唔出主演行
card = seg_fn("function gigCardHtml")
if "${leadStar}" in card or "lead-star" in card:
    fails.append("gigCardHtml 仍渲染主演行")
if "POSTER90" not in card:
    fails.append("gigCardHtml 缺 POSTER90 標記註")

# 3. 完成後場合保留
wrap = seg_fn("function wrapPoster59Html")
if "poster59Path" not in wrap or "主演" not in wrap:
    fails.append("wrapPoster59Html 被誤傷（殺青海報/主演應保留）")
wall = seg_fn("function worksWallEntries59")
if "poster59Path" not in wall or "leadStar59Of" not in wall:
    fails.append("worksWallEntries59 被誤傷（作品牆應保留）")
if html.count("wrapPoster59Html(") < 2:
    fails.append("wrapPoster59Html 調用點消失（殺青流程應照用）")
# leadStar 數據層保留（選角回填＋殺青好感邏輯照讀）
if "leadStar59Apply" not in html or "leadStar59Of" not in html:
    fails.append("leadStar 數據層被誤傷")

# 4. 紀律
if "starVolunteer_map_v19w" not in html: fails.append("SAVE key 變咗")
if '"s107"' not in html and "softRev=s107" not in html: fails.append("softRev 變咗")
if "?v=20a10" not in html: fails.append("?v= 變咗")

if fails:
    print("POSTER90 STATIC FAIL:")
    for f in fails: print(" -", f)
    sys.exit(1)
print("POSTER90 STATIC PASS: 詳情/通告卡冇成品圖冇主演行；殺青/作品牆保留；數據層冇郁")
