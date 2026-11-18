# v20a289 Q1 劣評分支靜態測試：表現判定函數在位、舊制 fame<=1 已退役、測試覆蓋在位。
import pathlib
ROOT = pathlib.Path(__file__).resolve().parent.parent
src = (ROOT / 'index.html').read_text(encoding='utf-8')
fails = []
def ok(name, cond):
    print(('PASS ' if cond else 'FAIL ') + name)
    if not cond:
        fails.append(name)

ok('表現判定函數 enc79WrapPerf 在位', 'function enc79WrapPerf(sh, g)' in src)
ok('enc79OnWrap 呼叫表現判定', 'enc79WrapPerf(sh, g)' in src)
ok('舊制判句已刪：const bad = ((Number(sh.fame)||0) <= 1)', 'const bad = ((Number(sh.fame)||0) <= 1)' not in src)
ok('註解記低舊制退役原因（fame roll 最低 5）', 'fame roll 全庫最低 5' in src)
ok('判定讀底圍（衫加成唔計）', '衫加成唔計' in src)
ok('判定讀壓力（危險線 85）', '85 係遊戲本身' in src)
ok('殺青掛點未郁：resolvePlannedDay 入面 enc79OnWrap', 'enc79OnWrap(sh)' in src)
ok('邏輯測試檔在位', (ROOT / 'tests' / 'test_r289_wrap_perf_logic.js').exists())
ok('NOTES 在位', (ROOT / 'NOTES_V20A289_BAD_REVIEW.md').exists())

if fails:
    print('FAILURES: ' + ' | '.join(fails))
    raise SystemExit(1)
print('ALL PASS')
