import copy,itertools,json,pathlib,random,sqlite3,subprocess,sys,tempfile,unittest
from dfa_inclusion_witness import analyze
ROOT=pathlib.Path(__file__).absolute().parent
def example():return json.loads((ROOT/'example.json').read_text())
class Contract(unittest.TestCase):
    def test_strict_cli_failures(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=pathlib.Path(tmp)/'bad.json'
            for raw in ('{', '{"x":1,"x":2}', '{"x":NaN}', '{}', ' '*1048577):
                p.write_text(raw);r=subprocess.run([sys.executable,str(ROOT/'dfa_inclusion_witness.py'),str(p)],text=True,capture_output=True,timeout=5)
                self.assertEqual(r.returncode,2);self.assertTrue(r.stderr);self.assertFalse(r.stdout)
    def test_input_unchanged(self):
        x=example();saved=copy.deepcopy(x);analyze(x);self.assertEqual(x,saved)

    def test_shortest_token_witness(self):
        r=analyze(example());self.assertFalse(r['included']);self.assertEqual(r['counterexample_tokens'],['a','b']);self.assertEqual(r['trace'][-1],{'left':'ok','right':None})
    def test_empty_word(self):
        d=example();d['left']['accept'].append('s');self.assertEqual(analyze(d)['counterexample_tokens'],[])
    def test_partial_sink_and_inclusion(self):
        d=example();d['right']=copy.deepcopy(d['left']);self.assertTrue(analyze(d)['included'])
        d['alphabet']=[];d['left']['transitions']=[];d['right']['transitions']=[];self.assertTrue(analyze(d)['included'])
    def test_nondeterminism_and_unknown(self):
        d=example();d['left']['transitions']*=2
        with self.assertRaises(ValueError):analyze(d)
        d=example();d['right']['start']='missing'
        with self.assertRaises(ValueError):analyze(d)
    def test_small_complete_dfa_enumeration(self):
        def machine(bits):
            return {'states':['0','1'],'start':'0','accept':[str(i) for i in range(2) if bits>>i&1],'transitions':[{'from':str(i),'symbol':s,'to':str((bits>>(2+2*i+j))&1)} for i in range(2) for j,s in enumerate('ab')]}
        def accept(m,word):
            state=m['start']
            for s in word:state=next(t['to'] for t in m['transitions'] if t['from']==state and t['symbol']==s)
            return state in m['accept']
        words=[list(w) for n in range(4) for w in itertools.product('ab',repeat=n)]
        for a in range(64):
            for b in range(0,64,7):
                l,r=machine(a),machine(b);want=next((w for w in words if accept(l,w) and not accept(r,w)),None);out=analyze({'alphabet':['b','a'],'left':l,'right':r})
                self.assertEqual(out['included'],want is None);self.assertEqual(out['counterexample_tokens'],want)

if __name__ == '__main__':unittest.main()
