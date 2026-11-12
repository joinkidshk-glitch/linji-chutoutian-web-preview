# v20a87 WF5 static 測試：紀律釘（SAVE/softRev/?v=、pack JSON 冇直改）＋修復標記在場。
import hashlib
import os
import sys

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
BASE = os.path.expanduser("~/workspace/linji-work86")
idx = open(os.path.join(ROOT, "index.html"), encoding="utf8").read()
fails = []


def ok(name, cond):
    if not cond:
        fails.append(name)


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


# 紀律：SAVE key / softRev / ?v= 不變
ok("SAVE key", "starVolunteer_map_v19w" in idx)
ok("softRev s107", '"s107"' in idx or "'s107'" in idx or "s107" in idx)
ok("?v= v20a10", "v20a10" in idx)

# F2 標記
ok("enc87StoryFlag 定義", "function enc87StoryFlag" in idx)
ok("ching_after_train 用新讀法", 'enc87StoryFlag("flag_vocal_train")' in idx)
ok("ching_after_polish 用新讀法", 'enc87StoryFlag("flag_vocal_polish")' in idx)
ok("舊死讀法已清除", "!!(S.flags||{}).flag_vocal_train" not in idx and "!!(S.flags||{}).flag_vocal_polish" not in idx)
ok("chai_repay 用新讀法", 'enc87StoryFlag("flag_side_film")' in idx)

# F1 標記
ok("getFlag alias 註記", "前綴 alias" in idx)

# F3 標記
ok("LIVE 補季節", "由同一來源字串補返季節" in idx)
ok("soft 年份跟 when", "年份跟節點 when" in idx)
ok("F3d 標籤短路只保留 C1", "標籤短路只保留 C1 本人" in idx)
ok("p3when 期望已更新", '"主線 · 1988秋"' in idx)

# 變體覆寫標記＋call site
ok("WF5 覆寫表", "const WF5_VARIANT_OVERRIDES87" in idx)
ok("WF5 apply", "function applyVariantWf5Overrides87" in idx)
ok("WF5 call site", "applyVariantWf5Overrides87(dengMock, dengPushMock, dualMock)" in idx)

# pack JSON 冇直改（同 v86 出貨副本逐檔 sha 對照）
packs = [
    "content/MOCK_STORY_DENG_LINE_MEET_SOFT_v1.1.json",
    "content/MOCK_STORY_DENG_LINE_PUSH_SOFT_v1.json",
    "content/MOCK_STORY_DUAL_MEET_THICKEN_SOFT_v1.json",
    "content/story_detail_c1_to_c17.json",
    "content/story_detail_romance_vera_hiu_choi.json",
    "content/story_detail_romance_lan_xu.json",
    "content/story_detail_romance_tang.json",
    "content/story_detail_rival_mentor.json",
]
# v151 例外：兩檔 DENG mock 准許刪走 guanHaimeiUpgradeForbidden 一行（名禁令退役）；
# 驗法：BASE 版刪走呢行之後要同現版逐字相同（唔係任意改）；其餘六檔照舊逐檔 sha 對照。
V151_FLAG_LINE = '    "guanHaimeiUpgradeForbidden": true,\n'
V151_PACKS = {
    "content/MOCK_STORY_DENG_LINE_MEET_SOFT_v1.1.json",
    "content/MOCK_STORY_DENG_LINE_PUSH_SOFT_v1.json",
}
for p in packs:
    if p in V151_PACKS:
        base_txt = open(os.path.join(BASE, p), encoding="utf8").read()
        cur_txt = open(os.path.join(ROOT, p), encoding="utf8").read()
        ok("pack v151 只刪禁令 flag: " + p, base_txt.replace(V151_FLAG_LINE, "") == cur_txt)
    else:
        ok("pack 冇直改: " + p, sha(os.path.join(ROOT, p)) == sha(os.path.join(BASE, p)))

# 審計腳本留底
ok("審計腳本存在", os.path.exists(os.path.join(ROOT, "tests", "audit_wf5.js")))

print("test_wf5_87_static: " + ("FAIL " + str(fails) if fails else "PASS"))
sys.exit(1 if fails else 0)
