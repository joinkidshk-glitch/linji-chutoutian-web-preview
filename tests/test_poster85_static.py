# v20a85 POSTER85 靜態測試（B3 重寫做刪除契約）：v20a85 POSTER85 模組已刪——
# POSTER85_IDS／poster85File／POSTER59_DATA 一律唔再存在，poster59Path 係 stub（一律回空字串），
# 新庫 posterBrief 出圖另開批（D-12）。留返：NOTES 歷史檔在位、assets/posters/*.webp 檔在磁碟
# （檔名帶舊 id，D-12 先處理）、SAVE/softRev/?v= 冇變、主檔冇脹大。
import io, os, sys
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
ipath = os.path.join(ROOT, 'index.html')
html = io.open(ipath, encoding='utf-8').read()
fails = []
def ok(name, cond):
    print(('PASS ' if cond else 'FAIL ') + name)
    if not cond: fails.append(name)

ok('SAVE key 冇變', 'starVolunteer_map_v19w' in html)
ok('softRev 冇變', '"s107"' in html or "'s107'" in html)
ok('產品 ?v= 冇變', 'v20a10' in html)
ok('NOTES_V20A85 文件在位（歷史留檔）', os.path.exists(os.path.join(ROOT, 'NOTES_V20A85_POSTER.md')))
ok('B3 POSTER85 模組標記已刪', 'v20a85 POSTER85' not in html)
ok('B3 POSTER85_IDS 已刪', 'const POSTER85_IDS' not in html)
ok('B3 poster85File 已刪', 'function poster85File(gigId)' not in html)
ok('B3 檔案參照查表已刪', '"assets/posters/" + poster85File(gigId)' not in html)
ok('B3 POSTER59_DATA 已刪', 'const POSTER59_DATA' not in html)
ok('B3 poster59Path 係 stub（一律回空字串）', 'function poster59Path(gigId)' in html and 'return "";' in html)
ok('B3 assets/posters 圖檔留喺磁碟（D-12 先處理）', os.path.isdir(os.path.join(ROOT, 'assets', 'posters')) and len(os.listdir(os.path.join(ROOT, 'assets', 'posters'))) > 0)
size = os.path.getsize(ipath)
ok('主檔冇脹大（B3 刪庫後應細過舊上限 5,626,915）', size < 5586915 + 40000)

if fails:
    print('FAILURES:', ' | '.join(fails)); sys.exit(1)
print('ALL PASS')
