#!/bin/bash
# 跑全套 tests：每個檔 PASS/FAIL 一行，尾行 TOTAL。用法：run_suite.sh <repo-root> <outfile>
ROOT="$1"; OUT="$2"
cd "$ROOT" || exit 1
pass=0; fail=0; : > "$OUT"
for f in tests/test_*.js; do
  if node "$f" > /tmp/suite_one.log 2>&1; then echo "PASS $f" >> "$OUT"; pass=$((pass+1)); else echo "FAIL $f" >> "$OUT"; fail=$((fail+1)); fi
done
for f in tests/test_*.py; do
  if python3 "$f" > /tmp/suite_one.log 2>&1; then echo "PASS $f" >> "$OUT"; pass=$((pass+1)); else echo "FAIL $f" >> "$OUT"; fail=$((fail+1)); fi
done
echo "TOTAL PASS $pass FAIL $fail" >> "$OUT"
echo "TOTAL PASS $pass FAIL $fail"
