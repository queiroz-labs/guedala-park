"""Verifica equilibrio por momentos diretos e viabilidade por envoltoria convexa."""
from pathlib import Path
import hashlib,json,math
ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'04_Moveis/P08'
def cross(o,a,b):return (a[0]-o[0])*(b[1]-o[1])-(a[1]-o[1])*(b[0]-o[0])
def hull(points):
    points=sorted(set(tuple(p) for p in points));lo=[];hi=[]
    for seq,out in [(points,lo),(points[::-1],hi)]:
        for p in seq:
            while len(out)>=2 and cross(out[-2],out[-1],p)<=0:out.pop()
            out.append(p)
    return lo[:-1]+hi[:-1]
def main():
    d=json.loads((OUT/'Apoios.json').read_text(encoding='utf-8'));wheels=d['wheels'];max_error=0;vertices=0
    for path,expected in d['inputs'].items():
        p=ROOT/path;data=p.read_bytes()
        if p.suffix in {'.py','.json','.md','.csv'}:data=data.replace(b'\r\n',b'\n')
        assert hashlib.sha256(data).hexdigest()==expected
    for c in d['cases']:
        cg=c['center_XY_mm'];W=c['total_weight_N']
        polygon=hull([w['contact_XY_mm'] for w in wheels if w['id']!=c['removed_contact']])
        inside=all(cross(p,polygon[(i+1)%len(polygon)],cg)>=-1e-6 for i,p in enumerate(polygon))
        assert inside==c['feasible_nonnegative_equilibrium'],c['id']
        for v in c['vertices_N']:
            vertices+=1;assert min(v)>=0
            error=abs(sum(v)-W)
            for axis in [0,1]:
                error=max(error,abs(sum(n*(w['contact_XY_mm'][axis]-cg[axis])/1000 for n,w in zip(v,wheels))))
            max_error=max(max_error,error);assert error<1e-7
            if c['removed_contact']:assert v[next(i for i,w in enumerate(wheels) if w['id']==c['removed_contact'])]==0
            # Total de cada fileira independe da divisao entre suas tres rodas.
            expected_back=W*(cg[1]-6528)/340
            assert abs(sum(v[3:])-expected_back)<1e-7
        if inside:
            for i in range(6):
                assert abs(min(v[i] for v in c['vertices_N'])-c['min_reaction_N'][i])<1e-8
                assert abs(max(v[i] for v in c['vertices_N'])-c['max_reaction_N'][i])<1e-8
    six=[c for c in d['cases'] if c['removed_contact'] is None]
    assert len(six)==48 and all(c['feasible_nonnegative_equilibrium'] for c in six)
    result={'status':'OK_LIMITES_NOMINAIS_P08','cases':len(d['cases']),'vertices_checked':vertices,
        'hull_classifications_checked':len(d['cases']),'maximum_force_or_moment_error':max_error,
        'six_contacts_cases':len(six),'infeasible_after_one_contact_removed':sum(not c['feasible_nonnegative_equilibrium'] for c in d['cases']),
        'physical_tests_executed':0,'capacity_demonstrated':False}
    (OUT/'Verificacao.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8');print(result)
if __name__=='__main__':main()
