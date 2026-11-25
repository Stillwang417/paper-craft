#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Compare the numbers in two texts, e.g. an English abstract and its Chinese version, or two rounds of one text.

Numbers are normalised: thousands separators (an ASCII comma followed by exactly three digits) are removed, full-width
digits are folded, a Chinese list comma "，" never joins two numbers, and "12.5 %" is read as "12.5%". A number counts
wherever it stands, also right after a Chinese character ("降低12.5%") or a full stop ("Fig.3"), but not inside a
word or an identifier ("v2", "x1"); a leading ".5" is read as 5. Reports numbers present in one text and missing in
the other.
Advisory; it cannot tell whether a number is right.
Usage: python3 -I number_parity.py FILE_A FILE_B
Status: CHECKED or NOT CHECKED. Exit 0 when both files were read; exit 2 otherwise (also for wrong arguments).
"""
import collections, io, re, sys, unicodedata

def numbers(text):
    t = re.sub(r'(?<=\d),(?=\d{3}(?![0-9０-９]))', '', text)   # thousands separators: ASCII comma only
    t = t.replace('，', '、')                                    # a Chinese list comma is not a separator
    t = unicodedata.normalize('NFKC', t)
    t = re.sub(r'(?<=\d)\s+%', '%', t)
    toks = re.findall(r'(?<![A-Za-z0-9_])(?<!\d\.)\d+(?:\.\d+)?%?', t)
    return collections.Counter(toks)

def main(argv):
    if len(argv) != 2:
        print('NOT CHECKED: wrong arguments (two files needed)\n' + __doc__); return 2
    try:
        a, b = (io.open(f, encoding='utf-8-sig').read() for f in argv)
    except Exception as e:
        print('NOT CHECKED: %s' % e); return 2
    na, nb = numbers(a), numbers(b)
    only_a, only_b = na - nb, nb - na
    print('CHECKED %s vs %s | numbers %d vs %d | only in first: %s | only in second: %s'
          % (argv[0], argv[1], sum(na.values()), sum(nb.values()),
             dict(only_a) or 'none', dict(only_b) or 'none'))
    return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
