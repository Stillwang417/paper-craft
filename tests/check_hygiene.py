#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Repository hygiene: no personal home paths, e-mail addresses, access tokens or paper profiles
(other than the template and the invented example) in the files of this repository.

Inside a git checkout it reads every file git would commit: tracked files plus new files that are not ignored.
Outside git it reads every file under the skill folder.
Usage: python3 -I tests/check_hygiene.py
Status: CHECKED or NOT CHECKED. Exit 0: nothing found; 1: findings; 2: NOT CHECKED (no files, or a file unreadable).
"""
import os, re, subprocess, sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
SELF = os.path.relpath(os.path.abspath(__file__), ROOT).replace(os.sep, '/')
ALLOWED_PROFILES = {'profiles/_template.md', 'profiles/示例_电池寿命.md'}
SKIP_DIRS = {'.git', '__pycache__'}
PATTERNS = [
    ('home path', re.compile(r'(?:/Users/|/home/)[^/\s\'"`]+|[A-Za-z]:\\Users\\[^\\\s]+|~/(?:Desktop|Documents|Downloads)/')),
    ('e-mail address', re.compile(r'[A-Za-z0-9._%+-]+@[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)*\.[A-Za-z]{2,}')),
    ('access token', re.compile(r'gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,}|hf_[A-Za-z0-9]{20,}|sk-[A-Za-z0-9]{20,}|AKIA[0-9A-Z]{16}')),
]

def file_list():
    try:
        r = subprocess.run(['git', '-C', ROOT, 'ls-files', '-co', '--exclude-standard', '-z'], capture_output=True)
    except OSError:
        r = None  # git is not installed: read the folder instead
    if r is not None and r.returncode == 0:
        return 'git', [p for p in r.stdout.decode('utf-8').split('\0') if p]
    out = []
    for d, dirs, files in os.walk(ROOT):
        dirs[:] = [x for x in dirs if x not in SKIP_DIRS]
        for f in files:
            out.append(os.path.relpath(os.path.join(d, f), ROOT).replace(os.sep, '/'))
    return 'folder', sorted(out)

def main():
    mode, files = file_list()
    if not files:
        print('NOT CHECKED: no files found under %s' % ROOT); return 2
    findings, unread = [], []
    for rel in files:
        if rel.startswith('profiles/') and rel not in ALLOWED_PROFILES:
            findings.append((rel, 0, 'paper profile', rel))
        if rel == SELF:
            continue  # this file holds the patterns themselves
        try:
            text = open(os.path.join(ROOT, rel), 'rb').read().decode('utf-8')
        except UnicodeDecodeError:
            continue  # binary file: nothing to read as text
        except OSError as e:
            unread.append('%s (%s)' % (rel, e)); continue
        for ln, line in enumerate(text.split('\n'), 1):
            for label, pat in PATTERNS:
                for m in pat.finditer(line):
                    findings.append((rel, ln, label, m.group(0)))
    status = 'NOT CHECKED' if unread else 'CHECKED'
    print('%s %d files (%s) | findings %d%s' % (status, len(files), mode, len(findings),
          '' if not unread else ' | unread: ' + ', '.join(unread)))
    for rel, ln, label, text in findings:
        print('  %s:%d  %s  %s' % (rel, ln, label, text))
    if unread:
        return 2
    return 1 if findings else 0

if __name__ == '__main__':
    sys.exit(main())
