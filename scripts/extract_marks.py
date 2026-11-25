#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Extract the marks in a Word file: coloured, highlighted and struck-through text, tracked changes, and the
comments of Word's comment pane.

Reads the main text, text boxes, footnotes, endnotes, headers, footers and comments with an XML parser (standard
library only). When Word stores a drawing twice (a modern copy and a fallback copy), only the modern copy is read.
Output: one line per paragraph that carries a mark, labelled P (main text), T (text box), F (footnote),
E (endnote) or H (header or footer) with a running number; then one line per comment, labelled C, as
"C001 author: text". Marked text is shown as ⟦tag:text⟧, combined as ⟦红+删:…⟧:
  红 red, 蓝 blue, 紫 purple, 绿 green, 橙 orange, 黄 yellow, 色XXXXXX any other font colour (hex code);
  亮 highlight; 删 single or double strike-through; 插 tracked insertion; 删(修订) tracked deletion.
Black and automatic font colours are not marks. A tab is shown as a tab and a line break as ↵.
Not shown: which passage of the text a comment refers to. Read-only.
Usage: python3 -I extract_marks.py FILE.docx [--all]      (--all prints unmarked paragraphs too)
Status: CHECKED or NOT CHECKED. Exit 0 when the file was read; exit 2 when it is not a readable .docx
or the arguments are wrong.
"""
import re, sys, zipfile
import xml.etree.ElementTree as ET

W = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
MC_FALLBACK = '{http://schemas.openxmlformats.org/markup-compatibility/2006}Fallback'
COL = {'EE0000': '红', 'FF0000': '红', 'C00000': '红', '7030A0': '紫', '00B0F0': '蓝', '0070C0': '蓝', '0000FF': '蓝',
       '00B050': '绿', '92D050': '绿', '00FF00': '绿', 'FFC000': '橙', 'ED7D31': '橙', 'FFFF00': '黄'}
NOT_A_MARK = {'000000', 'AUTO'}
OFF = {'0', 'false', 'off'}
REVISION = {W + 'ins': '插', W + 'moveTo': '插', W + 'del': '删(修订)', W + 'moveFrom': '删(修订)'}

def _val(el):
    return None if el is None else el.get(W + 'val')

def run_tags(r):
    rpr = r.find(W + 'rPr')
    tags = []
    if rpr is None:
        return tags
    v = _val(rpr.find(W + 'color'))
    if v and v.upper() not in NOT_A_MARK:
        tags.append(COL.get(v.upper(), '色' + v.upper()))
    hl = rpr.find(W + 'highlight')
    if hl is not None and (_val(hl) or '').lower() != 'none':
        tags.append('亮')
    for name in ('strike', 'dstrike'):
        st = rpr.find(W + name)
        if st is not None and (_val(st) or 'true').lower() not in OFF:
            tags.append('删'); break
    return tags

def run_text(r):
    parts = []
    for ch in r:
        if ch.tag in (W + 't', W + 'delText'):
            parts.append(ch.text or '')
        elif ch.tag == W + 'tab':
            parts.append('\t')
        elif ch.tag in (W + 'br', W + 'cr'):
            parts.append('↵')
        elif ch.tag == W + 'noBreakHyphen':
            parts.append('-')
    return ''.join(parts)

def paragraph_runs(p):
    """Runs of this paragraph in order, with the revision they sit in; nested paragraphs (text boxes) excluded."""
    out = []
    def walk(el, rev):
        for ch in el:
            if ch.tag == W + 'p':
                continue
            if ch.tag == W + 'r':
                out.append((ch, rev))
                continue
            walk(ch, REVISION.get(ch.tag, rev))
    walk(p, None)
    return out

def drop_fallbacks(root):
    """Word may store a drawing twice; keep the modern copy and drop the fallback copy."""
    for parent in list(root.iter()):
        for ch in list(parent):
            if ch.tag == MC_FALLBACK:
                parent.remove(ch)

def parse(xml):
    root = ET.fromstring(xml.encode('utf-8') if isinstance(xml, str) else xml)
    drop_fallbacks(root)
    return root

def marks(xml, show_all=False, label='P', counts=None):
    """Marked paragraphs of one WordprocessingML part and the number of marked spans.
    counts, if given, is a dict that collects the numbers of inserted and deleted runs with text."""
    root = parse(xml)
    in_box = set()
    for box in root.iter(W + 'txbxContent'):
        in_box.update(box.iter(W + 'p'))
    rows, n_spans = [], 0
    for i, p in enumerate(root.iter(W + 'p')):
        s, has = '', False
        for r, rev in paragraph_runs(p):
            txt = run_text(r)
            if not txt:
                continue
            if counts is not None and rev:
                key = 'ins' if rev == '插' else 'del'
                counts[key] = counts.get(key, 0) + 1
            tags = run_tags(r) + ([rev] if rev else [])
            if tags:
                s += '⟦%s:%s⟧' % ('+'.join(tags), txt); has = True; n_spans += 1
            else:
                s += txt
        if s.strip() and (has or show_all):
            rows.append('%s%03d %s' % ('T' if p in in_box else label, i, s))
    return rows, n_spans

def comments(xml):
    """Comments of the comment pane as 'C001 author: text'."""
    root = parse(xml)
    rows = []
    for i, c in enumerate(root.iter(W + 'comment'), 1):
        author = c.get(W + 'author') or '?'
        paras = []
        for p in c.iter(W + 'p'):
            paras.append(''.join(run_text(r) for r, _ in paragraph_runs(p)))
        rows.append('C%03d %s: %s' % (i, author, ' ↵ '.join(t for t in paras if t)))
    return rows

def main(argv):
    files = [a for a in argv if a != '--all']
    if len(files) != 1:
        print('NOT CHECKED: wrong arguments (one .docx file needed)\n' + __doc__); return 2
    path, show_all = files[0], '--all' in argv
    try:
        z = zipfile.ZipFile(path)
        names = z.namelist()
        parts = [('P', z.read('word/document.xml'))]
        for name in sorted(names):
            if name in ('word/footnotes.xml', 'word/endnotes.xml'):
                parts.append(('F' if 'foot' in name else 'E', z.read(name)))
            elif re.fullmatch(r'word/(header|footer)\d*\.xml', name):
                parts.append(('H', z.read(name)))
        rows, n, counts = [], 0, {}
        for label, data in parts:
            r, k = marks(data, show_all, label, counts)
            rows += r; n += k
        crows = comments(z.read('word/comments.xml')) if 'word/comments.xml' in names else []
    except Exception as e:
        print('NOT CHECKED %s: %s' % (path, e)); return 2
    print('CHECKED %s | marked spans %d | tracked insertions %d, deletions %d (runs with text) | comments %d'
          % (path, n, counts.get('ins', 0), counts.get('del', 0), len(crows)))
    for r in rows + crows:
        print(r)
    return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
