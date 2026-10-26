"""Conferencia independente: equacoes vetoriais, fontes e controles geometricos."""
from pathlib import Path
from collections import defaultdict
import argparse,csv,gzip,json,math
import numpy as np
from fontes import sha,HASH_RULE
ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'04_Moveis/Aereos_suspensao'

def read(p):return json.loads(p.read_text(encoding='utf-8'))
def hit(a,b):return all(min(a[i+3],b[i+3])-max(a[i],b[i])>1e-7 for i in range(3))

def main(code):
    d=read(OUT/f'{code}_suspensao.json');geo=read(OUT/'Lote_B_geometria.json');detail=read(OUT/'Lote_B_detalhamento.json')
    assert d['hash_rule']==HASH_RULE and d['script_sha256']==sha(Path(__file__).with_name('suspender_lote_b.py'))
    assert d['hash_helper_sha256']==sha(Path(__file__).with_name('fontes.py'))
    for p,s in d['sources_sha256'].items():assert sha(ROOT/p)==s,p
    release=read(ROOT/'ferramentas/site/current_release.json')
    assert sha(ROOT/release['cadPath'])==d['cad_sha256'] and not d['cad_opened'] and not d['cad_changed']
    module=next(m for m in geo['modules'] if m['code']==code)
    variant=next(v for v in module['variants'] if v['preferred_for_study'])
    assert variant['variant']==d['variant'] and not variant['adopted']
    wood=variant['boxes_uvz_mm'];base=json.loads(gzip.decompress((ROOT/'02_Modelo_3D/Base_verificacao.json.gz').read_bytes()))['objetos']
    for c in d['static_calcos']:
        b=base[c['name']]['caixa_global']
        if code=='P17':expected=[2882-b[4],4850-b[3],b[2]-1900,2882-b[1],4850-b[0],b[5]-1900]
        else:expected=[b[0]-868,7000-b[4],b[2]-1966,b[3]-868,7000-b[1],b[5]-1966]
        assert np.max(abs(np.array(expected)-c['box_uvz_mm']))<1e-8
    assert len(d['static_calcos'])==(8 if code=='P17' else 4)
    obstacles={**wood,**{c['name']:c['box_uvz_mm'] for c in d['static_calcos']}}
    w=d['width_internal_mm'];h=d['height_mm'];zu=h-36;zl=90;arm=h-126
    assert d['mounting']['couple_mm']==arm and d['mounting']['top_metal_gap_mm']==10
    assert not d['mounting']['single_translation_mirrored_keyholes'] and d['mounting']['bracket_count_hypothesis']==2
    for m in d['mounts']:
        side=m['side'];box=m['envelope_uvz_mm']
        assert box==[0 if side==0 else w-49.5,18,zu-8,49.5 if side==0 else w,55.8,zu+8]
        assert not any(hit(box,b) for b in obstacles.values())
        assert h-18-box[5]==10 and not m['product_mounting_confirmed']
    for r in d['rejected_old_height']:
        assert r['old_upper_z_mm']==h-58
        assert [n for n,b in obstacles.items() if n.startswith('Calco') and hit(r['auxiliary12_bbox_mm'],b)]==r['calco_interferences']
        assert len(r['calco_interferences'])==1
    assert len(d['accesses'])==8
    for r in d['accesses']:
        expected=[n for n,b in obstacles.items() if hit(r['generic20_bbox_mm'],b)]
        assert expected==r['generic20_interferences']
        assert not any(hit(r['candidate_bbox_mm'],b) for b in obstacles.values())
        assert not r['actual_bit_head_grip_verified']
        if r['role']=='rear_auxiliary':
            assert r['candidate_diameter_mm']==12 and len(expected)==1
            assert abs(9.5-20/2)==.5 and 9.5-12/2==3.5
        else:assert r['candidate_diameter_mm']==20 and not expected
    cams=[j for j in detail['joints'] if j['code']==code]
    assert len(cams)==d['cam_accesses_checked']==(24 if code=='P17' else 12)
    for j in cams:
        assert not any(hit(j['tool_corridor_bbox_mm'],b) for b in obstacles.values())
        assert not any(hit(j['tool_corridor_bbox_mm'],m['envelope_uvz_mm']) for m in d['mounts'])
    sources={c['source_case_id']:c for c in detail['cases'] if c['code']==code}
    upper=defaultdict(list);lower=defaultdict(list)
    for r in d['vectors']:upper[r['case_id'],r['share_left']].append(r)
    for r in d['lower_reactions']:lower[r['case_id'],r['share_left']].append(r)
    worst=0.;solution_error=0.
    for key,rows in upper.items():
        rows=sorted(rows,key=lambda r:r['side']);bottom=sorted(lower[key],key=lambda r:r['side']);c=sources[key[0]];share=key[1]
        assert len(rows)==len(bottom)==2
        # Resolver6incognitas por5equilibrios3D nao triviais e uma partilhaT.
        locations=[[40.5,0,zu],[w-40.5,0,zu],[-9,0,zl],[w+9,0,zl]]
        basis=[(locations[0],[0,0,1]),(locations[1],[0,0,1]),
               (locations[0],[0,-1,0]),(locations[1],[0,-1,0]),
               (locations[2],[0,1,0]),(locations[3],[0,1,0])]
        matrix=[]
        for at,f in basis:
            moment=np.cross(at,f);matrix.append([f[1],f[2],*moment])
        matrix=np.vstack([np.array(matrix).T,[0,0,1-share,-share,0,0]])
        gravity=np.array([0.,0.,-c['V_N']]);gm=np.cross(c['center_uvz_mm'],gravity)
        target=np.r_[-gravity[1],-gravity[2],-gm,0.]
        solved=np.linalg.solve(matrix,target)
        actual=np.array([rows[0]['V_N'],rows[1]['V_N'],rows[0]['T_N'],rows[1]['T_N'],bottom[0]['C_N'],bottom[1]['C_N']])
        solution_error=max(solution_error,float(max(abs(solved-actual))))
        assert max(abs(solved-actual))<1e-8
        error=max(abs(matrix@actual-target));worst=max(worst,float(error));assert error<1e-7
        for row in rows:
            s=row['side'];u=[40.5,w-40.5][s]
            assert row['u_mm']==u and row['z_mm']==zu and row['h_mm']==arm
            assert not row['capacity_demonstrated'] and not row['hardware_mass_included']
            assert row['V_N']>0 and row['T_N']>=0
            assert abs(row['R_N']-math.hypot(row['V_N'],row['T_N']))<1e-9
            local=np.cross([u-[0,w][s],-18,0],[0,-row['T_N'],row['V_N']])
            assert max(abs(local-row['local_M_corner_Nmm']))<1e-8
        for r in bottom:
            assert r['C_N']>0 and r['reference_area_mm2']==1080 and not r['actual_contact_measured']
            assert abs(r['mean_pressure_reference_MPa']-r['C_N']/1080)<1e-12
    assert len(upper)==len(sources)*3 and len(d['vectors'])==len(sources)*6
    assert len(d['certificates'])==len(upper)
    target=[r for r in d['vectors'] if r['payload_kg']==d['payload_target_kg']]
    for field in ['V_N','T_N','R_N']:
        assert max(r[field] for r in target)==d['target_separate_maxima'][field]
        for side in [0,1]:
            selected=[r for r in d['qualification_cases'] if r['side']==side]
            assert max(r[field] for r in selected)==max(r[field] for r in target if r['side']==side)
    for r in d['qualification_cases']:
        assert r['payload_kg']==d['payload_target_kg']
        assert any(all(r[k]==v for k,v in orig.items()) for orig in target)
    for suffix,key in [('demandas_suspensao','vectors'),('reacoes_inferiores','lower_reactions'),('qualificacao_suspensao','qualification_cases')]:
        with (OUT/f'{code}_{suffix}.csv').open(encoding='utf-8-sig',newline='') as f:rows=list(csv.DictReader(f,delimiter=';'))
        assert len(rows)==len(d[key])
        for a,b in zip(rows,d[key]):assert all(a[k]==str(v) for k,v in b.items())
    report=dict(code=code,status='OK_NOMINAL_SEM_ENSAIO',equilibria=len(upper),force_vectors=len(d['vectors']),
        qualification_cases=len(d['qualification_cases']),linear_solve_max_difference_N=solution_error,max_equilibrium_residual=worst,
        fixed_calcos_checked=len(d['static_calcos']),old_height_auxiliary_collisions=2,generic20_auxiliary_collisions=2,
        candidate12_corridors_clear=True,capacity_or_actual_tool_demonstrated=False,physical_tests=0,CAD_preserved=True,
        source_sha256=sha(OUT/f'{code}_suspensao.json'),verifier_sha256=sha(Path(__file__)),hash_rule=HASH_RULE)
    (OUT/f'{code}_verificacao_suspensao.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(report))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--movel',choices=['P17','P12'],required=True);main(p.parse_args().movel)
