# v20a102 FX102 行程動畫・靜態測試：接線標記／資產／紅線。
# 用法：python3 tests/test_fx102_static.py [path-to-index.html]
# 反證：v101 index 冇 FX102 標記、REST src 仲指住舊片 → 多項 FAIL。
import os, sys

path = sys.argv[1] if len(sys.argv) > 1 else 'index.html'
root = os.path.dirname(os.path.abspath(path))
html = open(path, encoding='utf-8').read()
fails = []

def ok(name, cond):
    print(('PASS ' if cond else 'FAIL ') + name)
    if not cond:
        fails.append(name)

# 映射表＋函數齊全
for probe in ['const ACT_FX102 = {', 'function actFx102KindForShoot',
              'function actFx102KindForTrain', 'function actFx102Html',
              'function armActFx102', 'function stopActFx102',
              'function actFx102Check', 'window.__fx102']:
    ok('標記 ' + probe, probe in html)

# 八條資產路徑＋實體檔齊全（新片入庫、舊瞓覺片保留唔刪）
for f in ['fx_shoot.mp4', 'fx_shoot_ext.mp4', 'fx_record.mp4',
          'fx_audition.mp4', 'fx_train_a.mp4', 'fx_train_b.mp4',
          'fx_train_c.mp4', 'fx_rest.mp4']:
    ok('index 引用 assets/fx/' + f, ('assets/fx/' + f) in html)
    p = os.path.join(root, 'assets', 'fx', f)
    ok('實體檔存在且 >5KB ' + f, os.path.isfile(p) and os.path.getsize(p) > 5000)
ok('舊瞓覺片保留', os.path.isfile(os.path.join(root, 'assets', 'fx',
                                               'awei-rest-sleep.mp4')))

# 接線點：三個分支 set kind、兩處呈現、closeModal 停片
ok('拍攝分支 set kind', 'fx102Kind=actFx102KindForShoot(sh)' in html)
ok('試鏡分支 set kind', 'fx102Kind="audition"' in html)
ok('訓練分支 set kind', 'fx102Kind=actFx102KindForTrain(id)' in html)
ok('地點訓練傳 kind', 'actFx102KindForTrain(tr.courseId)' in html)
ok('actFx102Html 呼叫點 x2（resolvePlannedDay＋afterDayModal）',
   html.count('actFx102Html(') == 3)  # 定義 1＋呼叫 2
ok('armActFx102 呼叫點 x2', html.count('armActFx102()') >= 3)  # 定義+自檢引用+2 呼叫
ok('closeModal 停片', 'stopActFx102(); }catch(_e){} /* v20a102' in html)

# 休息片改指新版（有意改變行為，NOTES 有記）
ok('REST src → fx_rest.mp4',
   'const REST_SLEEP_FX_SRC = "assets/fx/fx_rest.mp4"' in html)
ok('restSleepFxCheck 斷言已跟改版',
   'indexOf("fx_rest.mp4")' in html)

# 紅線：SAVE key／softRev／產品 ?v= 冇郁
ok('SAVE key 不變', 'starVolunteer_map_v19w' in html)
ok('CSS 類 .act-fx102 video', '.act-fx102 video' in html)

print('FX102 static:', 'ALL PASS' if not fails else f'{len(fails)} FAIL')
sys.exit(1 if fails else 0)
