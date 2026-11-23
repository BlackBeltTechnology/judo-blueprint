import json,collections,statistics as S,random,sys
smoke=open('runs2.txt').readline().split()[3]
REP={l.split()[3]:int(l.split()[2]) for l in open('runs2.txt')}
R=[json.loads(l) for l in open('metrics2.jsonl')]
for r in R: r['rep']=REP[r['id']]
R=[r for r in R if r['rep']<11]
R=[r for r in R if r['id']!=smoke]
G={}
for gf,kf in (('grades5a.jsonl','blind5-key.json'),('grades5b.jsonl','blind5-key.json')):
    try:
        key=json.load(open(kf))
        for l in open(gf): g=json.loads(l); G[key[g['key']]]=g
    except FileNotFoundError: pass
for r in R:
    g=G.get(r['id']); r['score']=g['score'] if g else None; r['wrong']=g['wrong'] if g else None
BASE_REPS=set(map(int,sys.argv[1].split(','))) if len(sys.argv)>1 else {1,2,3,4}
cell=collections.defaultdict(list)
for r in R:
    if r['variant']=='A-base' and r['rep'] not in BASE_REPS: continue
    cell[(r['variant'],r['task'])].append(r)
ts=['T1','T2','T3','T4']; vs=['A-base','V1-emoji','V2-bold','V3-generic','V4-hierarchy','V5-split','V6-bold-split','V7-bold-split-emoji','V8-adopted']
def ratio(v,k,boot=False):
    out=[]
    for t in ts:
        a=cell[(v,t)]; b=cell[('A-base',t)]
        if boot: a=[random.choice(a) for _ in a]; b=[random.choice(b) for _ in b]
        out.append(S.mean(x[k] for x in a)/max(S.mean(x[k] for x in b),1e-9))
    return S.mean(out)
random.seed(1); rows=[]
for v in vs:
    rs=[r for t in ts for r in cell[(v,t)]]
    bs=sorted(ratio(v,'kb_calls',True) for _ in range(2000))
    sc=[r['score'] for r in rs if r['score'] is not None]
    s13=[r['score'] for r in rs if r['score'] is not None and r['task']!='T4']; s4=[r['score'] for r in rs if r['score'] is not None and r['task']=='T4']
    wr=[r['wrong'] for r in rs if r['wrong'] is not None]
    rows.append(f"| {v} | {len(rs)} | {S.mean(r['kb_calls'] for r in rs):.2f} ({S.mean(r['kb_search'] for r in rs):.1f} + {S.mean(r['kb_get'] for r in rs):.1f}) | {ratio(v,'kb_calls'):.2f} [{bs[50]:.2f}, {bs[1949]:.2f}] | {sum(1 for t in ts if S.mean(r['kb_calls'] for r in cell[(v,t)])<S.mean(r['kb_calls'] for r in cell[('A-base',t)]))}/4 | {S.mean(r['kb_get_weak'] for r in rs):.2f} | {S.mean(r['kb_bytes'] for r in rs)/1000:.1f} | {ratio(v,'tokens'):.2f} | {S.mean(s13):.2f} / {S.mean(s4):.2f} | {S.mean(wr):.2f} |" if sc else f"| {v} | {len(rs)} | {S.mean(r['kb_calls'] for r in rs):.2f} | {ratio(v,'kb_calls'):.2f} [{bs[50]:.2f}, {bs[1949]:.2f}] | | {S.mean(r['kb_get_weak'] for r in rs):.2f} | | {ratio(v,'tokens'):.2f} | | |")
print("| Variant | runs | kb calls (search + get) | vs baseline [95% CI] | tasks fewer | weak kb_get | kb KB | tokens vs base | score T1-T3 / T4 | wrong |\n|---|---|---|---|---|---|---|---|---|---|"); print('\n'.join(rows))
print('per task kb_calls:')
for t in ts: print(t,' '.join(f"{v.split('-')[0]}={S.mean(r['kb_calls'] for r in cell[(v,t)]):.1f}" for v in vs))
b=[r for r in R if r['variant']=='A-base']
for reps in ({1,2,3,4},{5,6,7,8}): x=[r for r in b if r['rep'] in reps]; print('A-base reps',sorted(reps),'kb_calls',round(S.mean(r['kb_calls'] for r in x),2),'tokens',round(S.mean(r['tokens'] for r in x)/1000))
old=[json.loads(l) for l in open('metrics.jsonl') if json.loads(l)['variant'] in ('A-base','A2-base')]
print('old kb baselines (round 1, A+A2):',len(old),'kb_calls',round(S.mean(r['kb_calls'] for r in old),2),'weak',round(S.mean(r['kb_get_weak'] for r in old),2),'tokens',round(S.mean(r['tokens'] for r in old)/1000))
print('new kb baseline (all 32):','kb_calls',round(S.mean(r['kb_calls'] for r in b),2),'weak',round(S.mean(r['kb_get_weak'] for r in b),2),'tokens',round(S.mean(r['tokens'] for r in b)/1000))
