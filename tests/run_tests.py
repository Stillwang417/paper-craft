#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tests of the skill's scripts: each rule has a case it must flag and a case it must not flag.
All example sentences are invented (an imaginary paper on battery remaining-useful-life prediction).
Usage: python3 -I tests/run_tests.py   (from the skill folder, or any folder)
Prints "tests: N failed"; exit 0 when all pass, 1 otherwise.
"""
import io, os, sys, tempfile, zipfile, subprocess
HERE = os.path.dirname(os.path.abspath(__file__))
SCR = os.path.join(HERE, '..', 'scripts')
sys.path.insert(0, SCR)
import register_scan as R, count_words as C, number_parity as N, extract_marks as E

fails = []
def check(name, cond):
    if not cond: fails.append(name)

def ids(text, **kw):
    return [f[0] for f in R.scan(text, **kw)]

def run(script, *args):
    r = subprocess.run([sys.executable, '-I', '-B', os.path.join(SCR, script)] + list(args), capture_output=True, text=True)
    return r.returncode, r.stdout

def write(d, name, text, bom=False):
    p = os.path.join(d, name)
    io.open(p, 'w', encoding='utf-8-sig' if bom else 'utf-8').write(text)
    return p

RESTRICT = {'失效': ['失效阈值']}

# register_scan: must flag
check('CN-02 gloss', 'CN-02' in ids('在留出集（即训练时没有用过的电池）上评估。'))
check('CN-02 half-width gloss', 'CN-02' in ids('在留出集(即训练时没有用过的电池)上评估。'))
check('CN-02 mixed pair', 'CN-02' in ids('在留出集(即训练时没有用过的电池）上评估。'))
check('CN-02 across a line break', 'CN-02' in ids('在留出集（即训练时\n没有用过的电池）上评估。'))
check('CN-02 name note', 'CN-02' in ids('在温度恒定的条件下（下称恒温条件），'))
check('CN-03 ta', 'CN-03' in ids('它是一个标量，可以直接比较。'))
check('CN-04 zheyi', 'CN-04' in ids('这一分布只在温度恒定时成立。'))
check('CN-05 yue', 'CN-05' in ids('温度越高，寿命越短。'))
check('CN-05 jiushi', 'CN-05' in ids('预测就是把容量曲线往后外推。'))
check('CN-05 budai', 'CN-05' in ids('参考电池的读数不带测量误差。'))
check('CN-05 dedao', 'CN-05' in ids('只靠一个温度工况，得不到两个参数。'))
check('CN-06 add loss', 'CN-06' in ids('将两项损失直接相加，作为总损失。'))
check('CN-06 concat', 'CN-06' in ids('把两组特征拼接后送入网络。'))
check('CN-07 require', 'CN-07' in ids('要求估计的活化能必须非负。'))
check('CN-08 bare', 'CN-08' in ids('参数的估计由此转化为线性回归。'))
check('CN-14 restatement', 'CN-14' in ids('该指标为预测寿命与真实寿命之差的平方的均值，即预测偏离真实的程度。'))
check('TERM forbid', 'TERM-01' in ids('老化速度在高温下加快。', forbid=['老化速度', '寿命网络']))
check('TERM restrict', 'TERM-01' in ids('电池在高温下更早失效。', restrict=RESTRICT))
# register_scan: must NOT flag
check('no CN-02 for English full name', 'CN-02' not in ids('剩余寿命（remaining useful life，RUL）。'))
check('no CN-02 for numbers and symbols', 'CN-02' not in ids('扩散系数（σ² = 0.04），误差降低（12.5%）。'))
check('no CN-02 for English in half-width brackets', 'CN-02' not in ids('剩余寿命 (RUL) 的分布，见式 (3)。'))
check('no CN-03 for 其它', 'CN-03' not in ids('其它方法均未考虑温度。'))
check('no CN-05 for 越来越', 'CN-05' not in ids('储能系统的规模越来越大。'))
check('no CN-04 for 这一问题', 'CN-04' not in ids('针对这一问题，我们建立衰减模型。'))
check('no CN-14 for 即使 / 即可', 'CN-14' not in ids('即使是同一型号的电池，衰减速率也不同；有两个温度工况的数据，即可估计两个参数。'))
check('no TERM for fixed names', 'TERM-01' not in ids('容量降至失效阈值时，剩余寿命为零。', restrict=RESTRICT))
check('no finding in a clean formal sentence', ids('在温度恒定的条件下，平均剩余寿命与漂移系数成反比。') == [])
check('LaTeX comment lines skipped', ids('% 它就是这样（即注释）\n正文句子。') == [])
# register_scan: profile lines in several notations, and the status lines
with tempfile.TemporaryDirectory() as d:
    p = write(d, 'profile.md', '- forbid: 老化速度, 寿命网络\n－ forbid：剩余时长；衰减快慢。\n* restrict：失效｜失效阈值\n')
    fb, rs = R.load_profile(p)
    empty = write(d, 'empty.md', '# 本篇论文的设定\n\n没有用词表。\n')
    nopipe = write(d, 'nopipe.md', '- forbid: 老化速度\n- restrict: 失效\n')
    tmpl = os.path.join(HERE, '..', 'profiles', '_template.md')
    t = write(d, 'text.txt', '它是一个标量。\n', bom=True)
    rc_ok, out_ok = run('register_scan.py', t, '--profile', p)
    rc_empty, out_empty = run('register_scan.py', t, '--profile', empty)
    rc_nopipe, out_nopipe = run('register_scan.py', t, '--profile', nopipe)
    rc_tmpl, out_tmpl = run('register_scan.py', t, '--profile', tmpl)
    rc_bad, out_bad = run('register_scan.py', t, '--profile', os.path.join(d, 'missing.md'))
    rc_arg, out_arg = run('register_scan.py', t, '--profile')
    rc_blank, out_blank = run('register_scan.py', t, '--profile', '')
check('profile forbid in several notations', fb == ['老化速度', '寿命网络', '剩余时长', '衰减快慢'])
check('profile restrict (full-width punctuation)', rs == RESTRICT)
check('scan with profile: CHECKED, exit 0, BOM ignored', rc_ok == 0 and 'CHECKED' in out_ok and 'PARTIAL' not in out_ok and 'CN-03' in out_ok)
check('profile without entries: PARTIAL, exit 2', rc_empty == 2 and 'PARTIAL' in out_empty)
check('restrict line without a bar: PARTIAL, exit 2', rc_nopipe == 2 and 'PARTIAL' in out_nopipe)
check('template placeholders are not terms', rc_tmpl == 2 and 'forbid 0 | restrict 0' in out_tmpl)
check('unreadable profile: PARTIAL, exit 2', rc_bad == 2 and 'PARTIAL' in out_bad and 'CHECKED' not in out_bad)
check('register_scan wrong arguments: NOT CHECKED, exit 2', rc_arg == 2 and out_arg.startswith('NOT CHECKED'))
check('register_scan empty --profile: NOT CHECKED, exit 2', rc_blank == 2 and out_blank.startswith('NOT CHECKED'))
# count_words
check('count words', C.count('Battery packs age faster in hot climates than the usual linear extrapolation suggests.')['words'] == 13)
check('count han', C.count('剩余寿命预测')['han'] == 6)
with tempfile.TemporaryDirectory() as d:
    en, zh = write(d, 'en.txt', 'one two three four five'), write(d, 'zh.txt', '剩余寿命预测', bom=True)
    rc1, out1 = run('count_words.py', en, '--limit', '4')
    rc2, out2 = run('count_words.py', zh, '--limit', '4')
    rc3, out3 = run('count_words.py', en, '--limit', 'abc')
    rc4, out4 = run('count_words.py', en, '--limit', '²')
check('count_words CHECKED and over limit', rc1 == 0 and out1.startswith('CHECKED') and 'OVER by 1' in out1)
check('count_words: limit not applied to Chinese, BOM not counted', rc2 == 0 and 'not applied' in out2 and 'characters without spaces 6' in out2)
check('count_words bad --limit: exit 2', rc3 == 2 and out3.startswith('NOT CHECKED'))
check('count_words superscript digit: exit 2', rc4 == 2 and out4.startswith('NOT CHECKED'))
# number_parity
na, nb = N.numbers('error reduced by 12.5% (baseline: 3.0%), 480 cells'), N.numbers('误差降低12.5%，基线为3.0%，共480节电池')
check('parity equal, numbers right after Han characters', (na - nb) == {} and (nb - na) == {} and sum(nb.values()) == 3)
check('parity mismatch', dict(N.numbers('12.5%') - N.numbers('12.6%')) == {'12.5%': 1})
check('parity full-width', dict(N.numbers('１２.５%')) == {'12.5%': 1})
check('parity thousands separator after Han', dict(N.numbers('共1,200节')) == {'1200': 1})
check('parity Chinese list comma does not join numbers', dict(N.numbers('在200，300，400次循环时')) == {'200': 1, '300': 1, '400': 1})
check('parity table number then count', dict(N.numbers('见表2，120节电池')) == {'2': 1, '120': 1})
check('parity space before percent', dict(N.numbers('降低 12.5 %')) == {'12.5%': 1})
check('parity number after a full stop', dict(N.numbers('see Fig.3')) == {'3': 1})
check('parity skips identifiers', dict(N.numbers('model v2 and x1')) == {})
with tempfile.TemporaryDirectory() as d:
    rc5, out5 = run('number_parity.py', write(d, 'a.txt', '1'))
    rc6, out6 = run('number_parity.py', write(d, 'b.txt', '共480节', bom=True), write(d, 'c.txt', '480 cells'))
check('number_parity wrong arguments: NOT CHECKED, exit 2', rc5 == 2 and out5.startswith('NOT CHECKED'))
check('number_parity with a BOM', rc6 == 0 and 'only in first: none | only in second: none' in out6)
# extract_marks on a synthetic docx
NS = ('xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" '
      'xmlns:v="urn:schemas-microsoft-com:vml" '
      'xmlns:mc="http://schemas.openxmlformats.org/markup-compatibility/2006"')
doc = ('<?xml version="1.0" encoding="UTF-8"?><w:document ' + NS + '><w:body>'
       '<w:p><w:r><w:t>保留</w:t></w:r><w:r><w:rPr><w:strike/></w:rPr><w:t>删去的话</w:t></w:r>'
       '<w:r><w:rPr><w:color w:val="EE0000"/></w:rPr><w:t>【批注】</w:t></w:r></w:p>'
       '<w:p><w:r><w:rPr><w:color w:val="ff0000"/></w:rPr><w:tab/><w:t xml:space="preserve">带制表符的红字</w:t></w:r>'
       '<w:r><w:rPr><w:color w:val="00B050"/></w:rPr><w:t>绿字</w:t></w:r>'
       '<w:r><w:rPr><w:color w:val="123456"/></w:rPr><w:t>别的颜色</w:t></w:r>'
       '<w:r><w:rPr><w:color w:val="000000"/></w:rPr><w:t>黑字</w:t></w:r>'
       '<w:r><w:rPr><w:dstrike/></w:rPr><w:t>双删除线</w:t></w:r>'
       '<w:r><w:rPr><w:strike w:val="off"/></w:rPr><w:t>不是删除线</w:t></w:r></w:p>'
       '<w:p><w:r><w:t>文本框前</w:t></w:r>'
       '<w:r><mc:AlternateContent><mc:Choice Requires="wps"><w:drawing><w:txbxContent><w:p><w:r>'
       '<w:rPr><w:color w:val="0070C0"/></w:rPr><w:t>框里蓝字</w:t></w:r></w:p></w:txbxContent></w:drawing></mc:Choice>'
       '<mc:Fallback><w:pict><v:shape><v:textbox><w:txbxContent><w:p><w:r><w:rPr><w:color w:val="0070C0"/></w:rPr>'
       '<w:t>框里蓝字</w:t></w:r></w:p></w:txbxContent></v:textbox></v:shape></w:pict></mc:Fallback>'
       '</mc:AlternateContent></w:r>'
       '<w:r><w:rPr><w:color w:val="00B050"/></w:rPr><w:t>框后绿字</w:t></w:r></w:p>'
       '<w:p><w:ins w:id="1" w:author="a"><w:r><w:t>插入的字</w:t></w:r></w:ins>'
       '<w:del w:id="2" w:author="a"><w:r><w:delText>删去的字</w:delText></w:r></w:del></w:p>'
       '<w:p/>'
       '<w:p><w:r><w:rPr><w:highlight w:val="yellow"/></w:rPr><w:t>高亮&#x2014;破折号</w:t><w:br/><w:t>下一行</w:t></w:r></w:p>'
       '<w:p><w:r><w:t>没有标记的段落</w:t></w:r></w:p></w:body></w:document>')
foot = ('<?xml version="1.0" encoding="UTF-8"?><w:footnotes ' + NS + '><w:footnote w:id="1"><w:p><w:r>'
        '<w:rPr><w:color w:val="FF0000"/></w:rPr><w:t>脚注红字</w:t></w:r></w:p></w:footnote></w:footnotes>')
header = ('<?xml version="1.0" encoding="UTF-8"?><w:hdr ' + NS + '><w:p><w:ins w:id="3" w:author="a"><w:r>'
          '<w:t>页眉插入</w:t></w:r></w:ins></w:p></w:hdr>')
comm = ('<?xml version="1.0" encoding="UTF-8"?><w:comments ' + NS + '><w:comment w:id="0" w:author="导师">'
        '<w:p><w:r><w:t>这句要改</w:t></w:r></w:p></w:comment></w:comments>')
rows, n = E.marks(doc)
joined = '\n'.join(rows)
check('marks spans in the main part', n == 11)
check('marks strike', '⟦删:删去的话⟧' in joined)
check('marks red', '⟦红:【批注】⟧' in joined)
check('marks tab without raw XML', '⟦红:\t带制表符的红字⟧' in joined and '<w:' not in joined)
check('marks green and other colours', '⟦绿:绿字⟧' in joined and '⟦色123456:别的颜色⟧' in joined)
check('marks black is not a mark', '黑字' in joined and '000000' not in joined and ':黑字⟧' not in joined)
check('marks double strike', '⟦删:双删除线⟧' in joined)
check('marks strike val=off is not a mark', '不是删除线' in joined and ':不是删除线⟧' not in joined)
check('marks text box read once, and the text after it', joined.count('⟦蓝:框里蓝字⟧') == 1
      and any(r.startswith('T') and '⟦蓝:框里蓝字⟧' in r for r in rows) and '⟦绿:框后绿字⟧' in joined)
check('marks tracked changes', '⟦插:插入的字⟧' in joined and '⟦删(修订):删去的字⟧' in joined)
check('marks entity and line break', '⟦亮:高亮—破折号↵下一行⟧' in joined)
check('marks unmarked paragraph hidden', '没有标记的段落' not in joined)
with tempfile.TemporaryDirectory() as d:
    p = os.path.join(d, 't.docx')
    with zipfile.ZipFile(p, 'w') as z:
        z.writestr('word/document.xml', doc)
        z.writestr('word/footnotes.xml', foot)
        z.writestr('word/header1.xml', header)
        z.writestr('word/comments.xml', comm)
    rc_m, out_m = run('extract_marks.py', p)
    rc_x, out_x = run('extract_marks.py', os.path.join(d, 'missing.docx'))
    rc_a, out_a = run('extract_marks.py', p, p)
check('extract_marks CHECKED with footnotes, header and comments', rc_m == 0 and out_m.startswith('CHECKED')
      and 'marked spans 13' in out_m and '⟦红:脚注红字⟧' in out_m and '⟦插:页眉插入⟧' in out_m
      and 'tracked insertions 2, deletions 1' in out_m and 'comments 1' in out_m and 'C001 导师: 这句要改' in out_m)
check('extract_marks missing file: NOT CHECKED, exit 2', rc_x == 2 and 'NOT CHECKED' in out_x)
check('extract_marks wrong arguments: NOT CHECKED, exit 2', rc_a == 2 and out_a.startswith('NOT CHECKED'))
# a script that cannot read its input says NOT CHECKED and exits 2
rc, out = run('register_scan.py', '/nonexistent/file.txt')
check('not checked exit 2', rc == 2 and 'NOT CHECKED' in out)

print('tests: %d failed' % len(fails) + ('' if not fails else ' -> ' + ', '.join(fails)))
sys.exit(1 if fails else 0)
