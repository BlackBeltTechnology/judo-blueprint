#!/usr/bin/env python3
"""dump.py START END [--out FILE]: compact text of the webshop build session lines START..END
(user prompts, assistant text, tool calls with args, tool results truncated to 1500 chars)."""
import json,sys
F='/Users/bmiller/.pi/agent/sessions/--Users-bmiller-Projects-webshop-test--/2026-11-11T14-06-20-342Z_01a1caee-58b6-724e-ae62-d32987dbcd2d.jsonl'
s,e=int(sys.argv[1]),int(sys.argv[2]); out=open(sys.argv[4],'w') if len(sys.argv)>4 else sys.stdout
for i,l in enumerate(open(F)):
    if i<s: continue
    if i>e: break
    d=json.loads(l)
    if d.get('type')!='message': continue
    m=d['message']; r=m.get('role'); c=m.get('content')
    if isinstance(c,str): c=[{'type':'text','text':c}]
    for b in c or []:
        if not isinstance(b,dict): continue
        t=b.get('type')
        if t=='text' and b['text'].strip(): print(f"[{i}] {r.upper()}: {b['text'][:4000] if r!='toolResult' else b['text'][:1500]}",file=out)
        elif t=='toolCall': print(f"[{i}] CALL {b.get('name')}: {json.dumps(b.get('arguments'))[:1200]}",file=out)
