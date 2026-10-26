"""Conferencia independente de envelopes continuos e equilibrio P04."""
from pathlib import Path
from collections import defaultdict
import csv,json,math
import numpy as np
from fontes import sha,HASH_RULE
ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'04_Moveis/Aereos_suspensao'
def read(p):return json.loads(p.read_text(encoding='utf8'))
def overlap(a,b):return all(min(a[k+3],b[k+3])-max(a[k],b[k])>1e-7 for k in range(3))
def main():
    d=read(OUT/'P04_validacao.json');g=read(OUT/'Lote_B_geometria.json');detail=read(OUT/'Lote_B_detalhamento.json')
    assert d['hash_rule']==HASH_RULE and d['script_sha256']==sha(Path(__file__).with_name('validar_p04.py'))
    assert d['hash_helper_sha256']==sha(Path(__file__).with_name('fontes.py'))
    for path,digest in d['sources_sha256'].items():assert sha(ROOT/path)==digest,path
    release=read(ROOT/'ferramentas/site/current_release.json');assert sha(ROOT/release['cadPath'])==d['cad_sha256']
    assert not d['cad_opened'] and not d['cad_changed']
    module=next(m for m in g['modules'] if m['code']=='P04');chosen=next(v for v in module['variants'] if v['preferred_for_study'])
    obstacles={n:b for n,b in chosen['boxes_uvz_mm'].items()}
    assert d['source_tool']['key']['sku']=='05133154001' and d['source_tool']['key']['long_arm_mm']==80
    assert d['source_tool']['key']['short_arm_mm']==22 and d['source_tool']['key']['hex_mm']==4
    assert len(d['static_hardware'])==8
    obstacles.update({h['name']:h['box_uvz_mm'] for h in d['static_hardware']})
    assert overlap(d['old_corner_bracket']['box_uvz_mm'],obstacles['ApoioOpostoR002'])
    for b in d['proposed_brackets']:
        assert not any(overlap(b['envelope_uvz_mm'],x) for x in obstacles.values())
        obstacles['Bigfer_ESTUDO_'+str(b['side'])]=b['envelope_uvz_mm']
    # Limites analiticos,independentes da amostragem de segmentos do gerador.
    angular_guard=2*80*math.sin(math.pi/720);pad=5+angular_guard
    assert angular_guard<.699
    left_clear=34-pad-25;assert left_clear>3.3
    depth_clear=90-80*math.sin(math.radians(35))-15-angular_guard-18;assert depth_clear>10.4
    assert 230-(158+80*math.sin(math.radians(35))+15+angular_guard)>10.4
    assert 34-10-25<0 # O antigo diametro20 continua interferindo:controle negativo.
    left_calcos=[x for x in d['static_hardware'] if x['box_uvz_mm'][3]<40];assert len(left_calcos)==2
    for h in left_calcos:
        b=h['box_uvz_mm'];maxv=158+max(0,b[3]+pad-34)*math.tan(math.radians(35))
        assert maxv<b[1]-pad # Alavanca crescente emu passa longe do calco.
    assert all(h['box_uvz_mm'][0]>130 for h in d['static_hardware'] if h not in left_calcos)
    assert len(d['accesses'])==4
    generic_ids={r['id'] for r in detail['joints'] if r['code']=='P04' and not r['tool20_wood_clear']}
    assert {r['id'] for r in d['accesses']}==generic_ids
    for r in d['accesses']:
        assert len(r['rows'])==71 and r['sweep_deg']==[-35,35] and r['reindex_increment_deg']==60
        assert r['shaft_to_near_divider_mm']>3.3 and r['wood_and_fixed_calcos_clear']
        assert abs(r['continuous_angle_guard_mm']-angular_guard)<1e-12
        for bb in r['entry_swept_boxes_mm']:assert not any(overlap(bb,b) for b in obstacles.values())
        for row in r['rows']:
            assert not row['collisions'];assert not any(overlap(row['grip_swept_bbox_mm'],b) for b in obstacles.values())
    # Dois grupos superiores e duas faixas inferiores:equilibrio3D,nao capacidade.
    source={c['source_case_id']:c for c in detail['cases'] if c['code']=='P04'}
    assert len(source)==d['cases']==255 and len(d['vectors'])==1530
    groups=defaultdict(list);low=defaultdict(list)
    for r in d['vectors']:groups[r['case_id'],r['share_left']].append(r)
    for r in d['lower_reactions']:low[r['case_id'],r['share_left']].append(r)
    worst=0.
    for key,upper in groups.items():
        assert len(upper)==2 and len(low[key])==2;c=source[key[0]]
        F=np.array([0.,0.,-c['V_N']]);M=np.cross(c['center_uvz_mm'],F)
        for r in upper:
            assert r['h_mm']==160 and r['z_mm']==250 and r['u_mm']==[65.5,1723.5][r['side']]
            f=np.array([0.,-r['T_N'],r['V_N']]);at=np.array([r['u_mm'],0.,250.]);F+=f;M+=np.cross(at,f)
            corner=np.array([[25,18,250],[1764,18,250]][r['side']]);assert np.max(abs(np.cross(at-corner,f)-r['local_M_corner_Nmm']))<1e-8
            assert not r['capacity_selected'] and not r['hardware_mass_included']
        for r in low[key]:
            assert r['C_N']>0 and not r['actual_area_verified'];f=np.array([0.,r['C_N'],0.]);F+=f;M+=np.cross([r['u_mm'],0,90],f)
        err=max(max(abs(F)),max(abs(M)));worst=max(worst,float(err));assert err<1e-7
    assert len(d['qualification_cases'])==6
    for r in d['qualification_cases']:
        possible=[x for x in d['vectors'] if x['side']==r['side'] and x['payload_kg']==10]
        for control in r['controls']:assert abs(r[control]-max(x[control] for x in possible))<1e-8
    for name,key in [('P04_demandas_suspensao.csv','vectors'),('P04_reacoes_inferiores.csv','lower_reactions'),('P04_casos_qualificacao.csv','qualification_cases')]:
        with (OUT/name).open(encoding='utf-8-sig',newline='') as f:rows=list(csv.DictReader(f,delimiter=';'))
        assert len(rows)==len(d[key])
        for a,b in zip(rows,d[key]):assert all(a[k]==str(v) for k,v in b.items())
    report=dict(status='OK_NOMINAL_SEM_ENSAIO_FISICO',special_accesses_resolved=4,
        min_shaft_to_divider_clearance_mm=left_clear,continuous_guard_mm=angular_guard,
        old_generic_tool_and_left_corner_rejected=True,bracket_candidate_on_divider=True,
        equilibrium_cases=765,force_vectors=1530,qualification_cases=6,max_equilibrium_error=worst,
        CAD_preserved=True,physical_capacity_demonstrated=False,
        source_sha256=sha(OUT/'P04_validacao.json'),verifier_sha256=sha(Path(__file__)),hash_rule=HASH_RULE)
    (OUT/'P04_verificacao_validacao.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    print(json.dumps(report,ensure_ascii=True))

if __name__=='__main__':main()
