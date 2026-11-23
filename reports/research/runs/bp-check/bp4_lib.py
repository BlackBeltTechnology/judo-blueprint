import json, re, os

BATCH = 'target/bp-check/batches/bp4.json'
LEDGER = 'target/bp-check/ledger/bp4.jsonl'
b = json.load(open(BATCH))
ITEMS = {i['id']: i for i in b['items']}


def default_evidence(it):
    m = re.search(r'\bat ([^\s|]+:\S+)\s*$', it['text'])
    loc = m.group(1) if m else it['src']
    return loc


def emit(file, decisions, default_change=None):
    """decisions: {id: (status, change)} or {id: (status, change, evidence)}.
    Any item of this file not in decisions gets default 'not-relevant'."""
    items = [i for i in b['items'] if i['target'] == file]
    lines = []
    for it in items:
        d = decisions.get(it['id'])
        if d is None:
            status = 'not-relevant'
            change = default_change or 'file does not state this claim; no edit'
            ev = None
        else:
            status, change = d[0], d[1]
            ev = d[2] if len(d) > 2 else None
        sec = it['section']
        heading = sec.lstrip('#').strip() if sec else ''
        if d is not None and len(d) > 3:
            heading = d[3]
        evidence = (ev or default_evidence(it)) + ' | ' + file + '#' + heading
        lines.append({'id': it['id'], 'status': status, 'file': file,
                      'heading': heading, 'evidence': evidence, 'change': change})
    with open(LEDGER, 'a') as f:
        for l in lines:
            f.write(json.dumps(l, ensure_ascii=False) + '\n')
    return len(lines)
