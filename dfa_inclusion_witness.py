"""Prove finite DFA inclusion or emit a shortest token counterexample."""
import argparse, json, pathlib, sys

def need(ok, message):
    if not ok: raise ValueError(message)

def integer(n, low=0, high=10**9):
    need(type(n) is int and low <= n <= high, 'integer outside supported range')
    return n

def ident(s):
    need(type(s) is str and 0 < len(s) <= 80, 'invalid identifier')
    return s

def fields(obj, required, optional=()):
    need(type(obj) is dict and set(required) <= set(obj) <= set(required)|set(optional), 'missing or unknown fields')

def unique_pairs(pairs):
    out={}
    for k,v in pairs:
        need(k not in out, 'duplicate JSON key')
        out[k]=v
    return out

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('input',type=pathlib.Path);a=p.parse_args()
    try:
        with a.input.open('rb') as f: raw=f.read(1048577)
        need(len(raw) <= 1048576, 'input exceeds 1 MiB')
        doc=json.loads(raw.decode('utf-8'),object_pairs_hook=unique_pairs,parse_constant=lambda x: (_ for _ in ()).throw(ValueError('nonfinite JSON')))
        out=analyze(doc);print(json.dumps(out,ensure_ascii=True,sort_keys=True));return out.get('exit_code',0)
    except (ValueError,OSError,UnicodeError,RecursionError,OverflowError) as e:
        print(str(e),file=sys.stderr);return 2


from collections import deque

def machine(obj,alphabet):
    fields(obj,('states','start','accept','transitions'))
    need(type(obj['states']) is list and 1<=len(obj['states'])<=100,'expected 1..100 states')
    states=[ident(x) for x in obj['states']];need(len(set(states))==len(states),'duplicate state');states=set(states)
    need(type(obj['accept']) is list,'accept must be a list');accept=[ident(x) for x in obj['accept']]
    need(len(set(accept))==len(accept) and set(accept)<=states and ident(obj['start']) in states,'unknown or duplicate accepting/start state')
    need(type(obj['transitions']) is list and len(obj['transitions'])<=5000,'too many transitions')
    edges={}
    for e in obj['transitions']:
        fields(e,('from','symbol','to'));a,b,s=ident(e['from']),ident(e['to']),ident(e['symbol'])
        need(a in states and b in states and s in alphabet and (a,s) not in edges,'unknown or nondeterministic transition');edges[a,s]=b
    return obj['start'],set(accept),edges

def analyze(doc):
    fields(doc,('alphabet','left','right'))
    need(type(doc['alphabet']) is list and len(doc['alphabet'])<=32,'alphabet exceeds 32 tokens');alphabet=[ident(x) for x in doc['alphabet']]
    need(len(set(alphabet))==len(alphabet),'duplicate alphabet token');alphabet=sorted(alphabet)
    left=machine(doc['left'],alphabet);right=machine(doc['right'],alphabet);start=(left[0],right[0]);queue=deque([start]);parent={start:None};via={}
    while queue:
        pair=queue.popleft();a,b=pair
        if a in left[1] and b not in right[1]:
            path=[pair];tokens=[]
            while parent[pair] is not None:tokens.append(via[pair]);pair=parent[pair];path.append(pair)
            path.reverse();tokens.reverse()
            return {'included':False,'counterexample_tokens':tokens,'trace':[{'left':x,'right':y} for x,y in path],'discovered_pairs':len(parent),'exit_code':1}
        for s in alphabet:
            nxt=(left[2].get((a,s)),right[2].get((b,s)))
            if nxt not in parent:parent[nxt]=pair;via[nxt]=s;queue.append(nxt)
    return {'included':True,'reachable_pairs':len(parent),'counterexample_tokens':None,'exit_code':0}

if __name__ == '__main__':
    raise SystemExit(main())
