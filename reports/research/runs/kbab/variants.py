#!/usr/bin/env python3
"""Structure-only catalog transforms for kb A/B tests. Usage: variants.py <catalog-dir> <variant>[,<variant>...]
Variants: base, emoji, bold, generic, hierarchy. Operates in place on a COPY of catalog/."""
import re, sys, pathlib

EMO = re.compile('[\U0001F300-\U0001FAFF\u2600-\u27BF\u2B50\u2B06\u2194-\u21FF]\uFE0F?|\uFE0F')
GENERIC = {'overview', 'notes', 'note', 'example', 'examples', 'usage', 'solution', 'solutions', 'best practices',
           'troubleshooting', 'related documentation', 'see also', 'key points', 'summary', 'introduction',
           'configuration', 'common issues', 'common pitfalls', 'quick reference', 'quick start', 'key concepts',
           'purpose', 'description', 'details', 'workaround', 'implementation', 'testing', 'pattern', 'patterns'}
HEAD = re.compile(r'^(#{1,6}) (.*?)\s*$')


def split_front(t):
    if t.startswith('---\n'):
        e = t.find('\n---\n', 4)
        if e > 0:
            return t[:e + 5], t[e + 5:]
    return '', t


def add_aliases(front, olds):
    if not olds or not front:
        return front
    olds = [o.replace('"', "'") for o in olds]
    m = re.search(r'^aliases:\s*\[(.*?)\]\s*$', front, re.M)
    if m:
        cur = m.group(1).strip()
        add = ', '.join(f'"{o}"' for o in olds)
        return front[:m.start(1)] + (cur + ', ' if cur else '') + add + front[m.end(1):]
    return front.replace('\n---\n', '\naliases: [' + ', '.join(f'"{o}"' for o in olds) + ']\n---\n', 1) if front.endswith('\n---\n') else front


def lines_outside_fences(body):
    fence = False
    for i, l in enumerate(body.split('\n')):
        if l.lstrip().startswith('```'):
            fence = not fence
            yield i, l, True
            continue
        yield i, l, fence


def emoji(t):
    front, body = split_front(t)
    out = []
    for i, l, fence in lines_outside_fences(body):
        if fence:
            out.append(l); continue
        if l.lstrip().startswith('|'):
            cells = l.split('|')
            cells = [(' Yes ' if c.strip() in ('✅', '✔️', '✔') else ' No ' if c.strip() in ('❌', '✖️') else c) for c in cells]
            l = '|'.join(cells)
        l = re.sub(r'⚠️\s*(\S*)', lambda m: (m.group(1) if re.match(r'(?i)(important|critical|warning)', m.group(1)) else 'Warning: ' + m.group(1)), l)
        l = EMO.sub('', l)
        l = re.sub(r'(^#{1,6}) +', r'\1 ', l)
        l = re.sub(r'^(\s*[-*]) {2,}', r'\1 ', l)
        l = re.sub(r'\*\*\s+(?=\w)', '**', l, count=1) if re.match(r'^\s*(?:[-*]\s+|\d+\.\s+)?\*\*\s+\w', l) else l
        out.append(l.rstrip() if l.strip() == '' else l)
    return front + '\n'.join(out)


def bold(t):
    front, body = split_front(t)
    out, level = [], 1
    for i, l, fence in lines_outside_fences(body):
        if not fence:
            m = HEAD.match(l)
            if m:
                level = len(m.group(1))
            b = re.match(r'^\*\*([^*]{3,80}?)\*\*:?\s*$', l)
            if b:
                lv = min(level + 1, 6)
                out.append('#' * lv + ' ' + b.group(1).rstrip(':').strip())
                continue
        out.append(l)
    return front + '\n'.join(out)


def generic(t):
    front, body = split_front(t)
    stack, out, olds = {}, [], []
    title = None
    for i, l, fence in lines_outside_fences(body):
        if not fence:
            m = HEAD.match(l)
            if m:
                lv, h = len(m.group(1)), m.group(2)
                plain = re.sub(r'[`*_]', '', EMO.sub('', h)).strip().rstrip(':')
                if lv == 1 and title is None:
                    title = plain
                if plain.lower() in GENERIC or re.match(r'^(step \d+|\d+\.)\s*$', plain.lower()):
                    parent = next((stack[k] for k in range(lv - 1, 0, -1) if k in stack), title)
                    if parent and parent.lower() != plain.lower():
                        new = f'{parent}: {plain}'
                        olds.append(h)
                        l = m.group(1) + ' ' + new
                        plain_new = new
                    else:
                        plain_new = plain
                else:
                    plain_new = plain
                stack[lv] = plain_new
                for k in [k for k in stack if k > lv]:
                    del stack[k]
        out.append(l)
    return add_aliases(front, olds) + '\n'.join(out)


def hierarchy(t):
    front, body = split_front(t)
    out, seen_h1, prev = [], False, 0
    for i, l, fence in lines_outside_fences(body):
        if not fence:
            m = HEAD.match(l)
            if m:
                lv = len(m.group(1))
                if lv == 1:
                    if seen_h1:
                        lv = 2
                    seen_h1 = True
                if prev and lv > prev + 1:
                    lv = prev + 1
                prev = lv
                l = '#' * lv + ' ' + m.group(2)
        out.append(l)
    return front + '\n'.join(out)


T = {'base': lambda t: t, 'emoji': emoji, 'bold': bold, 'generic': generic, 'hierarchy': hierarchy}

if __name__ == '__main__':
    root, names = pathlib.Path(sys.argv[1]), sys.argv[2].split(',')
    changed = 0
    for p in root.rglob('*.md'):
        if p.name == 'AGENTS.md':
            continue
        t = p.read_text()
        n = t
        for v in names:
            if v in T: n = T[v](n)
        if n != t:
            p.write_text(n); changed += 1
    print(f'{",".join(names)}: {changed} files changed')


def split_large(root, limit=40000):
    """File structure: split agent-docs over `limit` bytes into an index file + one part per H2 (names keep the prefix)."""
    n = 0
    for p in list(root.rglob('*.md')):
        if p.name.endswith('.agent.md') or p.name == 'AGENTS.md' or 'agent-docs' not in str(p) or p.stat().st_size <= limit:
            continue
        front, body = split_front(p.read_text())
        parts, cur, title, intro = [], None, p.stem, []
        fence = False
        for l in body.split('\n'):
            if l.lstrip().startswith('```'):
                fence = not fence
            m = None if fence else HEAD.match(l)
            if m and len(m.group(1)) == 1 and title == p.stem:
                title = m.group(2); intro.append(l); continue
            if m and len(m.group(1)) == 2:
                cur = [m.group(2), []]; parts.append(cur); continue
            (cur[1] if cur else intro).append(l)
        if len(parts) < 2:
            continue
        idx = [*intro, '', '## Parts', '']
        for i, (h, ls) in enumerate(parts, 1):
            slug = re.sub(r'[^a-z0-9]+', '-', re.sub(r'[`*_]', '', h).lower()).strip('-')[:50]
            name = f'{p.stem}-{i:02d}-{slug}.md'
            d = (title + ': ' + re.sub(r'[`*_"]', '', h) + ' (part of ' + p.name + ')').replace('"', "'")
            pf = re.sub(r'^description:.*$', lambda _m: f'description: "{d}"', front, count=1, flags=re.M) if re.search(r'^description:', front, re.M) else front
            (p.parent / name).write_text(pf + f'# {title}: {h}\n' + '\n'.join(ls).rstrip() + '\n')
            idx.append(f'- [{h}]({name})')
        p.write_text(front + '\n'.join(idx) + '\n'); n += 1
    return n


if __name__ == '__main__' and 'split' in sys.argv[2].split(','):
    print('split files:', split_large(pathlib.Path(sys.argv[1])))
