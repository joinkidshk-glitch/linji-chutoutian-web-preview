#!/bin/bash
# v20a107 全套測試 A/B runner：逐檔跑 tests/*.py（python3）＋*.js（node），
# 每檔一行 PASS/FAIL（同 qa106/suite_*.txt 格式）。
# 用法：bash qa107/run_suite.sh <repo-root> <output-txt>
set -u
ROOT="$1"; OUT="$2"
cd "$ROOT" || exit 1
: > "$OUT"
for f in tests/test_*.py; do
  if python3 "$f" > /dev/null 2>&1; then echo "PASS $f" >> "$OUT"; else echo "FAIL $f" >> "$OUT"; fi
done
for f in tests/test_*.js; do
  if node "$f" > /dev/null 2>&1; then echo "PASS $f" >> "$OUT"; else echo "FAIL $f" >> "$OUT"; fi
done
echo "PASS $(grep -c '^PASS' "$OUT") / FAIL $(grep -c '^FAIL' "$OUT")"
