#!/bin/bash
cd ~/workspace/linji-work138
echo "===== SUITE work @ $(date +%H:%M:%S) ====="
bash qa138/run_suite.sh ~/workspace/linji-work138 ~/workspace/linji-work138/qa138/suite_work138.txt
tail -1 qa138/suite_work138.txt
echo "===== SUITE pristine(632e371) @ $(date +%H:%M:%S) ====="
bash qa138/run_suite.sh ~/workspace/linji-pristine138 ~/workspace/linji-work138/qa138/suite_pristine138.txt
tail -1 qa138/suite_pristine138.txt
echo "===== DIFF FAIL lists ====="
grep '^FAIL' qa138/suite_work138.txt | sort > /tmp/fail_work.txt
grep '^FAIL' qa138/suite_pristine138.txt | sort > /tmp/fail_pris.txt
diff /tmp/fail_work.txt /tmp/fail_pris.txt && echo "FAIL LISTS IDENTICAL (zero regression)"
echo "----- done @ $(date +%H:%M:%S) -----"
