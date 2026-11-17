# v20a270 檔尾碎片靜態測試：index.html 檔尾結構——單一 </html> 結尾、script 平衡、零 stray code。
# 背景：live index.html 檔尾有重複內容，第一個 </html> 之後仲有一段 stray 碎片
#   `1; } refreshCopyPacksFromDisk(); })(); </script> </body> </html>`，
# 瀏覽器將 </html> 之後嘅內容當可見文字 render，首頁最底見到一行 code。
# v270 刪走第一個 </html> 之後嘅全部 stray 內容（8 行），檔案以單一 </html> 結尾。
# 用法：python3 tests/test_tail270_static.py [path-to-index.html]
import os, re, subprocess, sys, tempfile

path = sys.argv[1] if len(sys.argv) > 1 else 'index.html'
ROOT = os.path.dirname(path) or '.'
html = open(path, encoding='utf-8').read()
fails = []
def ok(name, cond):
    print(('PASS ' if cond else 'FAIL ') + name)
    if not cond:
        fails.append(name)

# ---- (1) 單一 </html>，係檔案最後一個非空標記 ----
ok('</html> exactly once', html.count('</html>') == 1)
ok('</body> exactly once', html.count('</body>') == 1)
ok('file ends with </html> + newline', html.endswith('</html>\n'))
ok('nothing after </html> except newline', html.rstrip().endswith('</html>'))
ok('no stray fragment after first </html>', '</html>\n1;' not in html)
ok('stray code string absent', '})();\n\n</script>\n</body>\n</html>\n1;' not in html)

# ---- (2) script 平衡 ----
ok('<script count == </script> count', html.count('<script') == html.count('</script>'))
ok('two script blocks', html.count('<script') == 2)
ok('two </script>', html.count('</script>') == 2)
scripts = re.findall(r'<script>(.*?)</script>', html, re.S)
ok('two script blocks extractable', len(scripts) == 2)

# ---- (3) 合法檔尾完整在位 ----
tail = html[-400:]
ok('tail has return 1', 'return 1;' in tail)
ok('tail has refreshCopyPacksFromDisk();', 'refreshCopyPacksFromDisk();' in tail)
ok('tail ends refresh -> })(); -> </script> -> </body> -> </html>',
   re.search(r'refreshCopyPacksFromDisk\(\);\n\}\)\(\);\n\n</script>\n</body>\n</html>\n$', html) is not None)
ok('refreshCopyPacksFromDisk called exactly once', html.count('refreshCopyPacksFromDisk();') == 1)

# ---- (4) node --check 主 script（第二個 script block） ----
if len(scripts) >= 2:
    with tempfile.NamedTemporaryFile('w', suffix='.js', delete=False, encoding='utf-8') as tf:
        tf.write(scripts[1])
        tmp = tf.name
    try:
        r = subprocess.run(['node', '--check', tmp], capture_output=True, text=True)
        ok('node --check main script', r.returncode == 0)
        if r.returncode != 0:
            print(r.stderr[:500])
    finally:
        os.unlink(tmp)
else:
    ok('node --check main script', False)

# ---- (5) 紅線：SAVE key／softRev／產品 ?v= 不變 ----
ok('SAVE key starVolunteer_map_v19w present', 'starVolunteer_map_v19w' in html)
ok('softRev s107 present', 's107' in html)
ok('product ?v=v20a10 present', 'v20a10' in html)

print('FAILURES: ' + ' | '.join(fails) if fails else 'ALL PASS')
sys.exit(1 if fails else 0)
