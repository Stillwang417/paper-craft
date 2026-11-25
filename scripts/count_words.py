#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Count an abstract the same way every time.

English: whitespace-separated tokens (a hyphenated word, a URL or "12.5%" counts as one).
Chinese: Han characters, and all characters without spaces.
--limit N compares the English word count with N; it is not applied to a text that contains Han characters
(the report says so).
Usage: python3 -I count_words.py FILE [FILE ...] [--limit N]
Status per file: CHECKED or NOT CHECKED. Exit 0 when every file is CHECKED (over the limit or not; advisory),
2 when a file cannot be read or the arguments are wrong.
"""
import io, re, sys

def count(text):
    return {
        'words': len(text.split()),
        'han': len(re.findall(r'[一-鿿]', text)),
        'chars_no_space': len(re.sub(r'\s', '', text)),
    }

def main(argv):
    limit, files = None, []
    i = 0
    while i < len(argv):
        if argv[i] == '--limit':
            if i + 1 >= len(argv) or not re.fullmatch(r'[0-9]+', argv[i + 1]):
                print('NOT CHECKED: wrong arguments (--limit needs a whole number)\n' + __doc__); return 2
            limit = int(argv[i + 1]); i += 2
        else:
            files.append(argv[i]); i += 1
    if not files:
        print('NOT CHECKED: wrong arguments (no file given)\n' + __doc__); return 2
    rc = 0
    for f in files:
        try:
            t = io.open(f, encoding='utf-8-sig').read()
        except Exception as e:
            print('NOT CHECKED %s: %s' % (f, e)); rc = 2; continue
        c = count(t)
        line = 'CHECKED %s | English words %d | Han characters %d | characters without spaces %d' % (f, c['words'], c['han'], c['chars_no_space'])
        if limit is not None:
            if c['han'] == 0:
                line += ' | limit %d: %s' % (limit, 'within' if c['words'] <= limit else 'OVER by %d' % (c['words'] - limit))
            else:
                line += ' | limit %d not applied: the text contains Han characters' % limit
        print(line)
    return rc

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
