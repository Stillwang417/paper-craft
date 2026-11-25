#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Scan Chinese manuscript text for the register problems of references/06_中文书面语.md.

It reports candidates only; every finding needs a human reading (advisory, never blocks).
What it checks (rule IDs of the skill):
  CN-02 explanatory brackets: any pair of full-width （…） or half-width (…) brackets, mixed pairs and pairs across a
        line break included, with a Chinese character inside (English names, numbers and symbols are not flagged)
  CN-14 an unbracketed '，即……' clause (candidate only: a definition or a naming is flagged too)
  CN-03 the pronoun 它 / 它们 (其它 is not flagged)
  CN-04 这一 + noun used for back-reference (not flagged: 这一问题, 这一现象)
  CN-05 colloquial or loose phrasings from the table in 06_中文书面语.md
  CN-06 engineering phrasings, CN-07 absolute requirements (fixed lists only)
  CN-08 a bare 转化为 (check that the reason is written)
  TERM-01 terms the paper profile forbids, and restricted terms outside their fixed names (only with --profile)
What it does NOT check: meaning, logic, whether a reason is good, wordiness, anything in English.
Profile lines it reads (see profiles/_template.md). A line may start with -, －, *, • or nothing; ':' or '：';
'|' or '｜'; words are separated by ， , 、 ； or ;  Placeholders such as <word> are skipped.
  - forbid: word1, word2
  - restrict: word | fixed name 1, fixed name 2
Usage: python3 -I register_scan.py FILE [FILE ...] [--profile profiles/<paper>.md]
Status per file: CHECKED; PARTIAL when --profile was given but could not be read, held no forbid or restrict entry,
or held a line that could not be parsed (term checks skipped or incomplete); NOT CHECKED when the file could not
be read or the arguments are wrong. Exit 0 when every file is CHECKED, 2 otherwise.
"""
import io, re, sys

ALLOWED_ZHEYI = ('这一问题', '这一现象')
HAN = r'[一-鿿]'
COLLOQ = [
    ('CN-05', r'也就是|就是', '就是／也就是 → 即'),
    ('CN-05', r'能够[^，。；]{0,20}的，是', '能够……的，是…… → 直接陈述'),
    ('CN-05', r'所要实现的是', '所要实现的是 → 直接陈述'),
    ('CN-05', r'越(?!来越)[^。；越]{1,15}越', '越……越…… → 随……而……（“越来越”不算）'),
    ('CN-05', r'改变不了|满足不了|学不会|得不到', '……不了、得不到 → 无法……'),
    ('CN-05', r'不带[^，。；]{0,6}(?:误差|偏差|噪声)', '不带…… → ……为零'),
    ('CN-05', r'合起来', '合起来 → 共同／总'),
    ('CN-05', r'紧跟', '紧跟 → 紧随'),
    ('CN-05', r'只用', '只用 → 仅用／仅以'),
    ('CN-05', r'读到', '读到 → 读取'),
]
ENGINEERING = [
    ('CN-06', r'损失[^，。；]{0,6}相加', '工程腔：写成方法做什么、得到什么'),
    ('CN-06', r'拼接后送入', '工程腔：写成方法做什么、得到什么'),
    ('CN-07', r'要求(?:模型|输出|网络|预测|估计)|必须使|模型必须', '绝对化：写成方法做什么、促使什么（确是硬约束的照实写约束）'),
]
BULLET = r'\s*[-－*•·]?\s*'
SEP = r'[，,、；;]'

def _words(s):
    out = []
    for w in re.split(SEP, s):
        w = w.strip().rstrip('。.').strip()
        if w and not re.fullmatch(r'<[^<>]*>', w):
            out.append(w)
    return out

def load_profile(path, problems=None):
    """Read the forbid and restrict lines of a paper profile; lines that cannot be parsed go to problems."""
    forbid, restrict = [], {}
    problems = [] if problems is None else problems
    for n, line in enumerate(io.open(path, encoding='utf-8-sig'), 1):
        m = re.match(BULLET + r'forbid\s*[:：]\s*(.*)', line)
        if m:
            words = _words(m.group(1))
            if not words and not re.search(r'<[^<>]*>', m.group(1)):
                problems.append('line %d: forbid without words' % n)
            forbid += words
            continue
        m = re.match(BULLET + r'restrict\s*[:：]\s*(.*)', line)
        if m:
            parts = re.split(r'[|｜]', m.group(1), maxsplit=1)
            term = parts[0].strip()
            if re.fullmatch(r'<[^<>]*>', term):
                continue  # a template placeholder
            if len(parts) < 2 or not term:
                problems.append("line %d: restrict needs 'word | fixed names'" % n)
                continue
            restrict.setdefault(term, []).extend(_words(parts[1]))
    return forbid, restrict

def _comment_lines(text):
    return {i for i, l in enumerate(text.split('\n'), 1) if l.lstrip().startswith('%')}

def scan(text, forbid=(), restrict=None):
    restrict = restrict or {}
    out = []
    skip = _comment_lines(text)
    # brackets: on the whole text, so that a pair may span a line break or mix full and half width
    for m in re.finditer(r'[（(]([^（）()]{0,300})[）)]', text):
        ln = text.count('\n', 0, m.start()) + 1
        if ln in skip or not re.search(HAN, m.group(1)):
            continue  # English names, numbers and symbols in brackets are allowed
        out.append(('CN-02', ln, m.group(0).replace('\n', ' '), '括号里的解释：写进句子或删去'))
    for ln, line in enumerate(text.split('\n'), 1):
        if ln in skip:
            continue  # LaTeX comment lines are not part of the text
        for m in re.finditer(r'[，,]即(?![使可为指便将刻时由是])', line):
            out.append(('CN-14', ln, line[max(0, m.start() - 8):m.end() + 12], '不带括号的“即……”：定义之后的宽泛重述删去；定义、命名本身保留'))
        for m in re.finditer(r'(?<!其)它们?', line):
            out.append(('CN-03', ln, line[max(0, m.start() - 6):m.end() + 6], '“它”：写出所指名词'))
        for m in re.finditer(r'这一[一-鿿]{1,4}', line):
            if not any(line[m.start():].startswith(a) for a in ALLOWED_ZHEYI):
                out.append(('CN-04', ln, m.group(0), '回指用“该……”'))
        for rid, pat, hint in COLLOQ + ENGINEERING:
            for m in re.finditer(pat, line):
                out.append((rid, ln, line[max(0, m.start() - 6):m.end() + 6], hint))
        for m in re.finditer(r'转化为', line):
            out.append(('CN-08', ln, line[max(0, m.start() - 10):m.end() + 10], '核对理由是否写出'))
        for w in forbid:
            for m in re.finditer(re.escape(w), line):
                out.append(('TERM-01', ln, w, '本篇用词表不用此词'))
        for term, names in restrict.items():
            masked = line
            for a in sorted(names, key=len, reverse=True):
                masked = masked.replace(a, '＃' * len(a))
            for m in re.finditer(re.escape(term), masked):
                out.append(('TERM-01', ln, line[max(0, m.start() - 6):m.end() + 6], '“%s”只用于固定名称' % term))
    return sorted(out, key=lambda f: f[1])

def main(argv):
    prof, files = None, []
    i = 0
    while i < len(argv):
        if argv[i] == '--profile':
            if i + 1 >= len(argv) or not argv[i + 1].strip():
                print('NOT CHECKED: wrong arguments (--profile needs a file)\n' + __doc__); return 2
            prof = argv[i + 1]; i += 2
        else:
            files.append(argv[i]); i += 1
    if not files:
        print('NOT CHECKED: wrong arguments (no file given)\n' + __doc__); return 2
    forbid, restrict, profile_note = [], {}, ''
    if prof:
        problems = []
        try:
            forbid, restrict = load_profile(prof, problems)
            print('profile %s | forbid %d | restrict %d' % (prof, len(forbid), len(restrict)))
            if problems:
                profile_note = 'term checks incomplete: ' + '; '.join(problems)
            elif not forbid and not restrict:
                profile_note = 'term checks skipped: no forbid or restrict entry read from the profile'
        except Exception as e:
            profile_note = 'term checks skipped: profile not read (%s)' % e
    rc = 0
    for f in files:
        try:
            t = io.open(f, encoding='utf-8-sig').read()
        except Exception as e:
            print('NOT CHECKED %s: %s' % (f, e)); rc = 2; continue
        found = scan(t, forbid, restrict)
        status = 'PARTIAL' if profile_note else 'CHECKED'
        print('%s %s | candidates %d | scope: Chinese register patterns only (see docstring)%s'
              % (status, f, len(found), ' | ' + profile_note if profile_note else ''))
        if profile_note:
            rc = 2
        for rid, ln, ex, hint in found:
            print('  %-7s line %-4d %s   — %s' % (rid, ln, ex.replace('\n', ' '), hint))
    return rc

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
