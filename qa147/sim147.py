#!/usr/bin/env python3
"""v20a147 D4 贏線校準模擬 —— 唔用強制預覽／seed 存檔驗贏分支，模擬就係證據。

A. 真實檔案：全弧驗證第三輪（~/workspace/linji-fullarc3-report.md §2＋
   ~/workspace/fullarc3/arcN/gig_log.jsonl 138 單殺青＋days.jsonl 雙軌抽樣）。
   每單殺青 title 對照 content/gigs_*.json 取 roleScale／pay／stars，
   按 index.html awards62WorkQuality／awards62ScoreParts 原公式計 base：
     normPrimary = min(1, primary / (credit?60:45))
     wsum = q1 + .55*q2 + .35*q3 + .20*q4 + borrow(.55*.35*crossQ, 本桶有作品先借)
     worksScore = min(1, wsum/1.6)
     base = .40*normPrimary + .42*worksScore + tagBonus(0, MVP 類別冇 tagBonusAny)
            + repPower(.08*crossQ, 桶外>=2部且最佳q>=.5)
   每場取兩類別（聲望軌／信用軌）base 較大者（bestOutcome 係跨類別取最好）。
   桶年份＝殺青日曆法年（day 0 = 1990-01-01）；跨桶＝同年其他媒介殺青。
   雙軌用 ceremony 當日 days.jsonl 最近抽樣（<=當日）。
B. 前瞻檔案（註明 synthetic）：Y1 強／Y2 中／Y2 擔正／Y2 全弧風格（thin bucket）。
C. 贏率：taste ~ U(-0.05, +0.05)，P(win) = clamp((base+.05-L)/.10, 0, 1)。
用法：python3 qa147/sim147.py [--lines 0.82,0.80,0.78,0.76]
"""
import json, glob, sys, datetime, math
from collections import defaultdict

ROLE_Q = {
  'film_lead_big': 1.00, 'tv_lead_long': 1.00,
  'film_support_main': 0.78, 'tv_support_main': 0.78,
  'rec_album': 0.66,
  'film_support_small': 0.55, 'tv_cameo_short': 0.55,
  'mtv': 0.48, 'ad_av': 0.48, 'variety_special': 0.48,
  'ad_print': 0.40, 'variety_ep': 0.40, 'photobook': 0.40,
  'film_extra_day': 0.22, 'tv_extra_day': 0.22, 'ad_extra_day': 0.22,
  'rec_extra_day': 0.22, 'variety_extra_day': 0.22,
}
LEAD_SCALES = {'film_lead_big','tv_lead_long','tv_lead','film_second_lead',
               'tv_second_lead','music_lead','ad_lead','rec_album'}
EPOCH = datetime.date(1990, 1, 1)
WORK = '/home/hatch/workspace/linji-work147'
ARC = '/home/hatch/workspace/fullarc3/arcN'

def cal_year(day):
    return (EPOCH + datetime.timedelta(days=int(day))).year

def work_q(g):
    rs = g.get('roleScale') or ''
    if rs in ROLE_Q:
        q = ROLE_Q[rs]
    else:
        pay = g.get('payExact')
        if pay is None:
            pay = g.get('pay')
            pay = pay[1] if isinstance(pay, list) and len(pay) > 1 else (pay[0] if isinstance(pay, list) else pay)
        pay = float(pay or 0)
        q = 0.80 if pay >= 20000 else (0.62 if pay >= 8000 else (0.48 if pay >= 3000 else (0.36 if pay >= 1200 else 0.25)))
    st = g.get('stars')
    if st is not None:
        try:
            st = float(st)
            if st >= 5: q += 0.04
            elif st <= 1: q -= 0.04
        except (TypeError, ValueError):
            pass
    return min(1.0, max(0.05, q))

def load_gigs():
    """title -> gig；同 title 多年版，取 pack 年最貼近殺青日曆年嗰個（pack 年 +2 = 遊戲年）。
    來源二合一：content/gigs_*.json ＋ index.html 內嵌 gig object（softBridgeGig／gig36 等，
    用 brace-match 抽 object literal 再 regex 取欄位，唔 eval）。"""
    by_title = defaultdict(list)
    for f in sorted(glob.glob(WORK + '/content/gigs_19*.json')):
        try:
            d = json.load(open(f))
        except Exception:
            continue
        for g in d.get('gigs', []):
            if g.get('title'):
                by_title[g['title']].append(g)
    src = open(WORK + '/index.html', encoding='utf-8').read()
    import re
    n_inline = 0
    for m in re.finditer(r'title\s*:\s*"《', src):
        # 向後搵包住呢個 title 嘅 object 開括號
        depth = 0
        start = -1
        i = m.start()
        # 先向後掃：由 title 位置倒數，搵 depth 回到 0 嘅 '{'
        j = i
        bal = 0
        while j >= 0:
            ch = src[j]
            if ch == '}':
                bal += 1
            elif ch == '{':
                if bal == 0:
                    start = j
                    break
                bal -= 1
            j -= 1
        if start < 0:
            continue
        depth = 0
        k = start
        in_str = False
        esc = False
        end = -1
        while k < len(src):
            ch = src[k]
            if in_str:
                if esc:
                    esc = False
                elif ch == '\\':
                    esc = True
                elif ch == '"':
                    in_str = False
            else:
                if ch == '"':
                    in_str = True
                elif ch == '{':
                    depth += 1
                elif ch == '}':
                    depth -= 1
                    if depth == 0:
                        end = k
                        break
            k += 1
        if end < 0:
            continue
        obj = src[start:end + 1]
        def fld(pat):
            mm = re.search(pat, obj)
            return mm.group(1) if mm else None
        title = fld(r'title\s*:\s*"([^"]+)"')
        rs = fld(r'roleScale\s*:\s*"([^"]+)"')
        if not title or not rs:
            continue
        g = {'title': title, 'roleScale': rs,
             'id': fld(r'\bid\s*:\s*"([^"]+)"'),
             'type': fld(r'\btype\s*:\s*"([^"]+)"'),
             'roleLabel': fld(r'roleLabel\s*:\s*"([^"]+)"'),
             'payExact': fld(r'payExact\s*:\s*(\d+)'),
             'stars': fld(r'\bstars\s*:\s*(\d+)'),
             'year': fld(r'\byear\s*:\s*(\d+)')}
        by_title[title].append(g)
        n_inline += 1
    print('  （gig 庫：content JSON＋index 內嵌 %d 隻）' % n_inline, file=sys.stderr)
    return by_title

def score_base(fame, credit, bucket_qs, cross_qs, primary_track):
    primary = credit if primary_track == 'industryCredit' else fame
    norm = min(1.0, max(0.0, primary / (60 if primary_track == 'industryCredit' else 45)))
    qs = sorted(bucket_qs, reverse=True)
    cross_q = max(cross_qs) if cross_qs else 0.0
    cross_n = len(cross_qs)
    borrow = 0.55 * 0.35 * cross_q if qs else 0.0
    wsum = sum([qs[0] if len(qs) > 0 else 0, 0.55 * (qs[1] if len(qs) > 1 else 0),
                0.35 * (qs[2] if len(qs) > 2 else 0), 0.20 * (qs[3] if len(qs) > 3 else 0)]) + borrow
    ws = min(1.0, wsum / 1.6)
    rep_power = 0.08 * cross_q if (cross_n >= 2 and cross_q >= 0.5) else 0.0
    return 0.40 * norm + 0.42 * ws + rep_power, {
        'normPrimary': round(norm, 3), 'worksScore': round(ws, 3),
        'borrow': round(borrow, 3), 'repPower': round(rep_power, 3),
        'crossQ': cross_q, 'crossN': cross_n, 'nWorks': len(qs),
        'topQ': qs[0] if qs else 0.0}

def win_prob(base, line):
    return min(1.0, max(0.0, (base + 0.05 - line) / 0.10))

def main():
    lines = [0.82, 0.80, 0.78, 0.76]
    if len(sys.argv) > 1 and sys.argv[1].startswith('--lines'):
        lines = [float(x) for x in sys.argv[1].split('=', 1)[1].split(',')]
    by_title = load_gigs()
    # ---- A. 全弧三輪真實殺青 ----
    wraps = []  # (day, year, medium, q, title, is_lead)
    unmatched = []
    for ln in open(ARC + '/gig_log.jsonl'):
        r = json.loads(ln)
        if r.get('kind') != 'gig_shoot_end':
            continue
        day, title = int(r['day']), r['title']
        cands = by_title.get(title, [])
        if not cands:
            unmatched.append((day, title))
            continue
        y = cal_year(day)
        # pack 年 +2 = 遊戲年，揀最貼近
        cands.sort(key=lambda g: abs((int(g.get('year') or 0) + 2) - y))
        g = cands[0]
        mtype = g.get('type') or ''
        medium = ('film' if '電影' in mtype else 'tv' if ('電視' in mtype or '綜藝' in mtype)
                  else 'music' if '唱片' in mtype else 'ad' if '廣告' in mtype else '?')
        rs = g.get('roleScale') or ''
        rl = str(g.get('roleLabel') or '')
        is_lead = rs in LEAD_SCALES or any(k in rl for k in ('男主角', '女主角', '主角', '主演', '擔正', '領銜')) \
            or any(k in title for k in ('男主角', '女主角'))
        wraps.append({'day': day, 'year': y, 'medium': medium, 'q': work_q(g),
                      'title': title, 'is_lead': is_lead, 'gigId': g.get('id')})
    days = {}
    for ln in open(ARC + '/days.jsonl'):
        r = json.loads(ln)
        days[int(r['dayIndex'])] = (r['fame'], r['credit'])
    def dual_at(day):
        d = day
        while d >= 0 and d not in days:
            d -= 1
        return days.get(d, (0, 0))
    # 9 場（報告 §2 日子＋結果）
    ceremonies = [
        (59,  'award_harbour_ad',   'ad',    'gallery'),
        (151, 'award_golddisc_music','music','nominated'),
        (245, 'award_harbour_film', 'film',  'nominated'),
        (364, 'award_singho_tv',    'tv',    'nominated'),
        (365, 'award_singho_tv',    'tv',    'gallery'),
        (427, 'award_harbour_ad',   'ad',    'nominated'),
        (518, 'award_golddisc_music','music','nominated'),
        (609, 'award_harbour_film', 'film',  'nominated'),
        (742, 'award_singho_tv',    'tv',    'gallery'),
    ]
    print('=== A. 全弧三輪真實檔案（arcN，138 單殺青，%d 單對唔到 gig 庫）===' % len(unmatched))
    if unmatched:
        print('  未對照（唔計入桶，列出嚟交代）：%s' % (unmatched[:12],))
    print('  殺青分布（年／媒介）：%s' % (dict(sorted(
        ((f'{w["year"]}/{w["medium"]}', sum(1 for x in wraps if x['year'] == w['year'] and x['medium'] == w['medium']))
         for w in wraps), key=lambda kv: kv[0])),))
    print('  擔正作品數：%d（全弧 138 單）' % sum(1 for w in wraps if w['is_lead']))
    print()
    hdr = 'day  ceremony              year med  result    fame credit bucket_qs                    cross  base_sv base_ic baseMAX'
    print(hdr)
    real_rows = []
    for day, cid, med, res in ceremonies:
        y = cal_year(day)
        fame, credit = dual_at(day)
        bucket = [w['q'] for w in wraps if w['year'] == y and w['medium'] == med and w['day'] <= day]
        cross = [w['q'] for w in wraps if w['year'] == y and w['medium'] != med and w['day'] <= day]
        b_sv, d_sv = score_base(fame, credit, bucket, cross, 'stageVolume')
        b_ic, _ = score_base(fame, credit, bucket, cross, 'industryCredit')
        bmax = max(b_sv, b_ic)
        real_rows.append((day, cid, y, med, res, fame, credit, bmax, bucket, d_sv))
        print(f'{day:<4} {cid:<22} {y} {med:<6} {res:<9} {fame:<4} {credit:<6} '
              f'{str([round(q,2) for q in sorted(bucket, reverse=True)])[:28]:<28} '
              f'q{d_sv["crossQ"]:.2f}/n{d_sv["crossN"]}  {b_sv:.3f}  {b_ic:.3f}  {bmax:.3f}')
    print()
    print('  baseMAX 分布（6 場入圍）：%s' % [round(r[7], 3) for r in real_rows if r[4] == 'nominated'])
    print('  最高 base：%.3f（day %d %s）' % (max(r[7] for r in real_rows), max(real_rows, key=lambda r: r[7])[0], max(real_rows, key=lambda r: r[7])[1]))
    print()
    # ---- B. 前瞻檔案 ----
    synth = [
        ('Y1 正常 (wk26)', 43, 52, [0.55, 0.48], [0.48], 'Y1'),
        ('Y1 強 (wk39)', 64, 71, [0.78, 0.55, 0.48], [0.55, 0.48], 'Y1'),
        ('Y2 中 (wk52)', 81, 87, [0.78, 0.55, 0.48, 0.40], [0.55, 0.55, 0.48], 'Y2'),
        ('Y2 全弧風格 thin', 149, 162, [0.55, 0.48, 0.40, 0.36], [0.55, 0.55, 0.48, 0.40], 'Y2'),
        ('Y2 擔正 (wk65)', 118, 124, [1.00, 0.78, 0.55], [0.66, 0.55], 'Y2'),
        ('Y3 擔正 (wk104)', 176, 200, [1.00, 0.78, 0.55, 0.48], [0.78, 0.66], 'Y3'),
    ]
    print('=== B. 前瞻檔案（synthetic；雙軌取全弧週快照，桶向量見標註）===')
    synth_rows = []
    for name, fame, credit, bq, cq, tag in synth:
        b_sv, _ = score_base(fame, credit, bq, cq, 'stageVolume')
        b_ic, _ = score_base(fame, credit, bq, cq, 'industryCredit')
        bmax = max(b_sv, b_ic)
        synth_rows.append((name, tag, bmax))
        print(f'  {name:<18} fame {fame:<4} credit {credit:<4} bucket {bq} cross {cq} -> base {bmax:.3f}')
    print()
    # ---- C. 贏率表 ----
    print('=== C. 贏率 P(win) = clamp((base+.05-L)/.10) ===')
    print('  檔案                              base   ' + '  '.join('L=%.2f' % L for L in lines))
    for day, cid, y, med, res, fame, credit, bmax, bucket, d in real_rows:
        label = f'{day} {cid[6:]} {y} {res}'
        print(f'  {label:<32} {bmax:.3f}  ' + '  '.join('%.0f%%' % (100 * win_prob(bmax, L)) for L in lines))
    for name, tag, bmax in synth_rows:
        print(f'  {name:<32} {bmax:.3f}  ' + '  '.join('%.0f%%' % (100 * win_prob(bmax, L)) for L in lines))
    print()
    # 匯總：強勢入圍年份 = Y2 中；第一年 = Y1 正常＋Y1 強；弱玩 = 假設 base<=0.30
    print('=== D. 匯總（判據：強勢入圍年 25-40%；第一年 ~0%；弱玩 0%）===')
    for L in lines:
        y1 = max(win_prob(b, L) for n, t, b in synth_rows if t == 'Y1')
        y2mid = win_prob([b for n, t, b in synth_rows if n.startswith('Y2 中')][0], L)
        y2thin = win_prob([b for n, t, b in synth_rows if 'thin' in n][0], L)
        y2lead = win_prob([b for n, t, b in synth_rows if n.startswith('Y2 擔正')][0], L)
        real_best = max(r[7] for r in real_rows)
        print(f'  L={L:.2f}: Y1最強 {y1:.0%} | Y2中 {y2mid:.0%} | Y2全弧風格 {y2thin:.0%} | '
              f'Y2擔正 {y2lead:.0%} | 全弧實測最高base {real_best:.3f} -> {win_prob(real_best, L):.0%}')

if __name__ == '__main__':
    main()
