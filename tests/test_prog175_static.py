# -*- coding: utf-8 -*-
# v20a175 靜態測試：v153 review C1＋C2。
# C1（文字紀律）：進度頁開放行「已開放」唔再講兩次——note 刪「已經開放——」，
#   變「返地圖嗰陣就會播出。（場景：…）」；tag 嗰粒「已開放」保留。
# C2（狀態可讀）：進度頁開頁嗰陣仲生效嘅全域 toast（B01「已用預設行程 · 到何生事務所
#   可播開局劇情」）唔再用 #toast 底部 overlay 蓋住第 14–15 幕——收容做 .prog71-wrap
#   頂部 in-flow banner（將 list 向下推），1.8 秒後平滑收起；toast() 喺進度頁開住
#   嗰陣觸發亦直接行 banner。字句本身唔變，toast 系統本身唔重寫。
# 反證：喺 pristine main（a618a5d／v174）index 上行，C1／C2 新斷言要乾淨 FAIL（唔 crash）；
#      基線斷言（SAVE／softRev／?v=／開放行場景文案）喺 pristine 一樣 PASS。
# 用法：python3 tests/test_prog175_static.py [path-to-index.html]
import re
import sys
from pathlib import Path

p = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent.parent / 'index.html'
src = p.read_text(encoding='utf-8')
fails = []


def ok(name, cond):
    print(('PASS ' if cond else 'FAIL ') + name)
    if not cond:
        fails.append(name)


def func_body(src_text, fname):
    """抽一段 function fname(...) { ... }（由宣告行起到下一個同級 function 為止）。"""
    m = re.search(r'function ' + re.escape(fname) + r'\b', src_text)
    if not m:
        return ''
    start = m.start()
    m2 = re.search(r'\nfunction ', src_text[start + 10:])
    return src_text[start:start + 10 + m2.start()] if m2 else src_text[start:]


def css_block(selector):
    """抽一段 CSS selector { ... }（首個閉括號為止）。"""
    m = re.search(re.escape(selector) + r'\s*\{', src)
    if not m:
        return ''
    end = src.find('}', m.start())
    return src[m.start():end] if end >= 0 else ''


# --- 基線不變 ---
ok('SAVE key／softRev／?v= 不變', 'starVolunteer_map_v19w' in src and 's107' in src and 'v20a10' in src)
ok('開放行場景文案仲喺度（返地圖嗰陣就會播出＋場景）',
   '返地圖嗰陣就會播出' in src and '（場景：' in src)
ok('B01 提示字句本身唔變（已用預設行程 · 到何生事務所可播開局劇情）',
   '已用預設行程 · 到' in src and '可播開局劇情' in src)

# --- C1：開放行 note 唔再講「已經開放」 ---
m = re.search(r'const openBody = .*?;', src)
open_body_line = m.group(0) if m else ''
ok('C1：openBody 抽到', bool(open_body_line))
ok('C1：note 冇咗「已經開放——」', '已經開放' not in open_body_line)
ok('C1：note 仲係「返地圖嗰陣就會播出。」', '返地圖嗰陣就會播出。' in open_body_line)
ok('C1：tag 嗰粒「已開放」保留',
   '<span class="prog71-tag open">已開放</span>' in src)
ok('C1：開放行得返一次「開放」狀態字（tag 嗰粒；note 唔再講）',
   open_body_line.count('開放') + src.count('<span class="prog71-tag open">已開放</span>') == 1)
ok('C1：全站開放行共用同一 code 位（得一個 openBody 定義）',
   src.count('const openBody = ') == 1)

# --- C2：in-flow 頂部 banner 收容 toast ---
ok('C2：prog175ShowBanner 定義咗', 'function prog175ShowBanner(msg)' in src)
ok('C2：prog175AdoptToast 定義咗', 'function prog175AdoptToast()' in src)
banner_css = css_block('.prog175-banner')
ok('C2：.prog175-banner CSS 在位', bool(banner_css))
ok('C2：banner 係 in-flow（position:static，唔係 fixed／absolute overlay）',
   'position:static' in banner_css and 'position:fixed' not in banner_css
   and 'position:absolute' not in banner_css)
ok('C2：banner 收起有過渡（唔會一下跳）',
   'transition:' in banner_css and 'max-height' in banner_css)
bye_css = css_block('.prog175-banner.bye')
ok('C2：收起態 .bye 在位（max-height:0＋opacity:0）',
   'max-height:0' in bye_css and 'opacity:0' in bye_css)
show_body = func_body(src, 'prog175ShowBanner')
ok('C2：banner 插喺 .prog71-wrap 最頂（firstChild，標題上面）',
   'wrap.insertBefore(b, wrap.firstChild)' in show_body)
ok('C2：banner 識字句原樣搬（textContent＝msg）', 'b.textContent = text' in show_body)
ok('C2：banner 1.8 秒後先收起', '}, 1800);' in show_body)
adopt_body = func_body(src, 'prog175AdoptToast')
ok('C2：adopt 只收仲生效嘅 overlay toast（#toast.on）',
   't.classList.contains("on")' in adopt_body)
ok('C2：adopt 收起 overlay（清計時＋除 on／has-stamp／has-sub＋清內容）',
   'clearTimeout(toast._t)' in adopt_body
   and 't.classList.remove("on","has-stamp","has-sub")' in adopt_body
   and 't.replaceChildren()' in adopt_body)
ok('C2：adopt 拎走 #app toast-up（唔留暗影 slab）',
   'app.classList.remove("toast-up","keep-sheet")' in adopt_body)
rp_body = func_body(src, 'renderProgressPane71')
ok('C2：renderProgressPane71 尾段有呼 prog175AdoptToast',
   'prog175AdoptToast()' in rp_body)
toast_body = func_body(src, 'toast')
ok('C2：toast() 喺進度頁開住嗰陣行 banner（唔行 overlay）',
   'prog175ShowBanner' in toast_body and 'home-pane-progress' in toast_body)
ok('C2：toast() 分流要手帳真係顯示緊（#v-home.on＋pane.on，唔係淨睇 pane）',
   'getElementById("v-home")' in toast_body
   and 'classList.contains("on")' in toast_body)
ok('C2：toast() banner 唔到就跌返 overlay（唔吞提示）',
   'if(prog175ShowBanner(_bm))' in toast_body)
ok('C2：#toast 本身定位唔郁（系統唔重寫：底部 absolute overlay 原封不動）',
   '#toast' in src and 'position:absolute' in src)

print('FAILURES: ' + ' | '.join(fails) if fails else 'ALL PASS')
sys.exit(1 if fails else 0)
