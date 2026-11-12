#!/bin/bash
# Pipe-based suite runner: 不寫 /tmp/suite_one.log，逐個測試經 command substitution
# 攞 stdout（pipe，唔受檔案寫入攔截影響），只憑 exit code 計 PASS/FAIL。
# 用法：bash qa147/run_suite_pipe.sh [ROOT] — 印 TOTAL 同 FAIL 清單去 stdout。
ROOT="${1:-/home/hatch/workspace/linji-work147}"
cd "$ROOT" || exit 2
pass=0; fail=0; failed=""
for f in tests/test_*.js tests/test_*.py; do
  if [[ "$f" == *.py ]]; then out=$(python3 "$f" 2>&1); ec=$?
  else out=$(node "$f" 2>&1); ec=$?
  fi
  if [ $ec -eq 0 ]; then pass=$((pass+1)); else fail=$((fail+1)); failed="$failed
$f"; fi
done
echo "TOTAL PASS $pass FAIL $fail"
echo "FAILED:$failed"
