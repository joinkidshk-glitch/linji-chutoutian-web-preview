#!/bin/bash
# 逐個直接重跑 work-suite 多出嚟嘅 FAIL（避開 /tmp redirect，寫結果去 qa160-m1/rerun_out.txt）
cd /home/hatch/workspace/linji-work160-m1 || exit 1
OUT=qa160-m1/rerun_out.txt
: > "$OUT"
pass=0; fail=0
while read -r f; do
  if python3 "$f" > qa160-m1/rerun_one.log 2>&1; then echo "PASS $f" >> "$OUT"; pass=$((pass+1)); else echo "FAIL $f" >> "$OUT"; fail=$((fail+1)); fi
done < qa160-m1/rerun_list.txt
echo "RERUN TOTAL PASS $pass FAIL $fail" >> "$OUT"
echo "RERUN TOTAL PASS $pass FAIL $fail"
