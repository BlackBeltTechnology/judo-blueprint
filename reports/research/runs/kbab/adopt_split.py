#!/usr/bin/env python3
"""Adopt the V5 split in the repo: split agent-docs over 40 KB into an index + parts, keep each old H2 as a
part alias, and rewrite links into moved sections (resolved relative to the linking file)."""
import re, sys, json, pathlib, os
sys.path.insert(0, os.path.dirname(__file__))
import variants as V

ROOT = pathlib.Path('/Users/bmiller/Projects/judo-blueprint')
CAT = ROOT / 'catalog'


def slug(h):  # GitHub anchor
    h = re.sub(r'[`*_~]', '', h).strip().lower()
    h = re.sub(r'[^\w\- ]', '', h)
    return h.replace(' ', '-')


targets = [p for p in CAT.rglob('*.md') if 'agent-docs' in str(p) and not p.name.endswith('.agent.md')
           and p.name != 'AGENTS.md' and p.stat().st_size > 40000]
# anchor map from the ORIGINAL files: anchor -> (part file name, anchor inside part or '')
amap = {}
for p in targets:
    front, body = V.split_front(p.read_text())
    fence, part_i, cur, seen = False, 0, None, {}
    m_ = {}
    for l in body.split('\n'):
        if l.lstrip().startswith('```'):
            fence = not fence
        m = None if fence else V.HEAD.match(l)
        if not m:
            continue
        lv, h = len(m.group(1)), m.group(2)
        a = slug(h); n = seen.get(a, 0); seen[a] = n + 1; a = a if n == 0 else f'{a}-{n}'
        if lv == 2:
            part_i += 1
            cur = f'{p.stem}-{part_i:02d}-' + re.sub(r'[^a-z0-9]+', '-', re.sub(r'[`*_]', '', h).lower()).strip('-')[:50] + '.md'
            m_[a] = (cur, '')
        elif lv >= 3 and cur:
            m_[a] = (cur, a)
    amap[p.resolve()] = m_

n = V.split_large(CAT)
print('split files', n)

# aliases: old H2 into each part's frontmatter
for p in targets:
    for part in p.parent.glob(f'{p.stem}-[0-9][0-9]-*.md'):
        t = part.read_text(); front, body = V.split_front(t)
        h1 = re.search(r'^# (.*)$', body, re.M).group(1)
        old = h1.split(': ', 1)[1] if ': ' in h1 else h1
        part.write_text(V.add_aliases(front, [old]) + body)

# link rewrite
LINK = re.compile(r'\]\(([^)\s#]*?\.md)#([^)\s]+)\)')
changed = 0
for f in list(CAT.rglob('*.md')) + list((ROOT / 'skills').rglob('*.md')):
    t = f.read_text(); new = t
    def rep(m):
        tgt = (f.parent / m.group(1)).resolve()
        if tgt not in amap or m.group(2) not in amap[tgt]:
            return m.group(0)
        part, a = amap[tgt][m.group(2)]
        rel = os.path.relpath(tgt.parent / part, f.parent)
        return f']({rel}' + (f'#{a}' if a else '') + ')'
    new = LINK.sub(rep, t)
    if new != t:
        f.write_text(new); changed += 1
print('files with rewritten links', changed)
unresolved = []
for f in list(CAT.rglob('*.md')):
    for m in LINK.finditer(f.read_text()):
        tgt = (f.parent / m.group(1)).resolve()
        if tgt in amap:
            unresolved.append(f'{f.relative_to(ROOT)} -> {m.group(1)}#{m.group(2)}')
print('anchored links still into split index files:', len(unresolved)); print('\n'.join(unresolved[:20]))
