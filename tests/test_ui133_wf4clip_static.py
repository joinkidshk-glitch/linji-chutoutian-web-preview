# v20a133 WF4 事件舞台 viewport-aware・靜態守門測試。
# 用法：python3 tests/test_ui133_wf4clip_static.py [path-to-index.html]
# 反證意識：每項同時驗「新寫法在」＋「舊寫法不在」。
# 對 pristine main 行 → 固定 min-height:480px 仍在 → 乾淨 FAIL。
import re, sys

path = sys.argv[1] if len(sys.argv) > 1 else 'index.html'
html = open(path, encoding='utf-8').read()
fails = []

def ok(name, cond):
    print(('PASS ' if cond else 'FAIL ') + name)
    if not cond:
        fails.append(name)

m = re.search(r'#mask\.wf4-stage-on #modal-inner \.story-play \.sp-stage\{([^}]*)\}', html)
ok('WF4 舞台規則存在', m is not None)
rule = m.group(1) if m else ''
ok('WF4 舞台 min-height viewport-aware（min(480px,52dvh)）', 'min-height:min(480px,52dvh)' in rule)
ok('WF4 舞台唔再固定 min-height:480px（v128 回歸寫法）', 'min-height:480px' not in rule)
ok('WF4 舞台 480px 上限保留（高屏保 v128 觀感）', '480px' in rule)
ok('.story-play 58dvh 上限唔郁（唔影響全部 StoryPlay）', 'max-height:min(58dvh,480px);overflow:hidden;' in html)
ok('modal max-height 78dvh 唔郁', '#mask.story-play-on .modal{max-height:min(78dvh,720px);overflow:hidden}' in html)
ok('對話框定高 118px 唔郁（B4）', '.story-play .dlg106-plate{height:118px;min-height:118px;max-height:118px;flex:1}' in html)

print('TOTAL ' + ('PASS' if not fails else 'FAIL %d' % len(fails)))
sys.exit(1 if fails else 0)
