#!/bin/bash
# v20a193 第二次重驗：全套重跑（帶重試）。
# 背景：qa131/run_suite.sh 用 /tmp/suite_one.log 做每項測試嘅輸出，間歇性 EPERM
# 會令 redirect 失敗→測試未跑就計 FAIL（119/166 嗰種假失敗，OUT 寫入都一併 EPERM）。
# 呢支 wrapper：(1) 每項輸出改放 workspace（qa193/suite_one193.log），唔經 /tmp；
# (2) FAIL 數 >20 就當係 EPERM 風暴，重試最多 3 次；(3) 每次跑之前先 probe 寫入。
# 用法：bash qa193/run_suite193_retry.sh <repo-root> <outfile>
ROOT="$1"; OUT="$2"
cd "$ROOT" || exit 1
TMPLOG="$ROOT/qa193/suite_one193.log"
attempt=0
while [ $attempt -lt 3 ]; do
  attempt=$((attempt+1))
  if ! echo probe > "$TMPLOG" 2>/dev/null; then echo "attempt $attempt: probe write EPERM, sleep and retry"; sleep 20; continue; fi
  pass=0; fail=0; : > "$OUT"
  for f in tests/test_*.js; do
    if node "$f" > "$TMPLOG" 2>&1; then echo "PASS $f" >> "$OUT"; pass=$((pass+1)); else echo "FAIL $f" >> "$OUT"; fail=$((fail+1)); fi
  done
  for f in tests/test_*.py; do
    if python3 "$f" > "$TMPLOG" 2>&1; then echo "PASS $f" >> "$OUT"; pass=$((pass+1)); else echo "FAIL $f" >> "$OUT"; fail=$((fail+1)); fi
  done
  echo "TOTAL PASS $pass FAIL $fail" >> "$OUT"
  echo "attempt $attempt: TOTAL PASS $pass FAIL $fail"
  if [ "$fail" -le 20 ]; then exit 0; fi
  echo "attempt $attempt: FAIL $fail > 20，疑似 EPERM 風暴，20 秒後重試"
  sleep 20
done
echo "GAVE UP after 3 attempts"
exit 1
