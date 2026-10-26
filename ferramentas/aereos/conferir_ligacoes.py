"""Conferencia independente: contato real, reconciliacao e equilibrio do loteA."""
from collections import Counter,defaultdict
import csv,hashlib,json,math
from pathlib import Path
import numpy as np
from detalhar_ligacoes import profiles,W,H,ROOT,OUT,G

def read(p):return json.loads(p.read_text(encoding='utf-8'))
def main():
    d=read(OUT/'Detalhamento_P09_P11_P15.json')
    assert hashlib.sha256((ROOT/'ferramentas/aereos/detalhar_ligacoes.py').read_bytes()).hexdigest()==d['generator_sha256']
    assert hashlib.sha256((ROOT/'02_Modelo_3D/Guedala_Park_R52_Corrigido.FCStd').read_bytes()).hexdigest()==d['cad_sha256']
    for name,expected in d['source_sha256'].items():assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==expected,name
    assert d['cad_changed'] is False and d['cad_opened'] is False
    def face_joint(row):
        p=profiles(row['code'],row['variant']);a,b=p[row['a']],p[row['b']]
        delta=np.minimum(a[3:],b[3:])-np.maximum(a[:3],b[:3]);axis='uvz'.index(row['axis'])
        point=np.array([row[k] for k in ['u_mm','v_mm','z_mm']])
        return (abs(delta[axis])<1e-7 and all(delta[i]>1e-7 for i in range(3) if i!=axis)
                and all(np.all(point>=x[:3]-1e-7) and np.all(point<=x[3:]+1e-7) for x in [a,b]))
    assert len(d['axes_nominal'])==96 and all(face_joint(r) for r in d['axes_nominal'])
    with (OUT/'Mapa_ligacoes_P09_P11_P15.csv').open(encoding='utf-8-sig',newline='') as f:axis_csv=list(csv.DictReader(f,delimiter=';'))
    assert len(axis_csv)==96
    for saved,row in zip(d['axes_nominal'],axis_csv):
        assert all(row[k]==str(value) for k,value in saved.items())
    assert not face_joint(dict(code='P09',variant='current',a='Peca317',b='Peca318',axis='v',u_mm=72,v_mm=18,z_mm=18))
    expected={('P09','current'):(20,0,11),('P11','current'):(10,12,3),('P15','current'):(6,8,0),('P15','wood_study'):(18,8,0)}
    totals=[]
    for (code,variant),numbers in expected.items():
        rows=[r for r in d['axes_nominal'] if r['code']==code and r['variant']==variant]
        cf=sum(r['family'].startswith('Confirmat') for r in rows);mf=sum(r['existing'] for r in rows);cv=sum(r['family'].startswith('Cavilha') for r in rows)
        assert (cf,mf,cv)==numbers
        totals.append(dict(code=code,variant=variant,Confirmat_candidate=cf,Minifix_existing=mf,dowels_position_only=cv,purchase_quantity=False))
    old=read(OUT/'Resultados.json')['cases']
    old += [r for r in read(ROOT/'04_Moveis/P04/Suspensao_P04_P15/Resultados.json')['cases'] if r['code']=='P15']
    source={(r['code'],r.get('variant','current'),r['id']):r for r in old}
    with (OUT/'Solicitacoes_fixacao_direta.csv').open(encoding='utf-8-sig',newline='') as f:rows=list(csv.DictReader(f,delimiter=';'))
    assert len(rows)==4176
    groups=defaultdict(list)
    for r in rows:groups[(r['code'],r['variant'],int(r['source_case_id']),float(r['traction_share_left']))].append(r)
    maxerr=np.zeros(3)
    for key,pair in groups.items():
        assert len(pair)==2 and {int(r['side']) for r in pair}=={0,1}
        r=source[key[:3]];code=key[0]
        # Calcula pela resultante antiga mais1kg: independente da recomposicao
        # por volumes/centros e do motorR52 usados no gerador.
        V=r['weight_N']+G
        M=r.get('wall_normal_moment_Nm',r.get('wall_normal_gravity_moment_Nm'))*1000+G*174
        S=r['lateral_first_moment_Nmm']+G*W[code]/2
        errors=[abs(sum(float(p['V_N']) for p in pair)-V),
                abs(sum(float(p['T_N'])*float(p['couple_h_mm']) for p in pair)-M),
                abs(sum(float(p['V_N'])*float(p['u_mm']) for p in pair)-S)]
        maxerr=np.maximum(maxerr,errors);assert max(errors)<1e-7
        for p in pair:assert abs(math.hypot(float(p['V_N']),float(p['T_N']))-float(p['R_N']))<1e-10
    assert len(groups)==696*3
    for c in d['critical_groups']:
        subset=[r for r in rows if r['code']==c['code'] and r['variant']==c['variant'] and float(r['payload_kg'])==c['payload_kg']]
        assert abs(max(float(r['R_N']) for r in subset)-c['R_N'])<1e-8
    for a in d['alternative_rear_reserve']:
        assert a['internal_depth_old_mm']-a['internal_depth_new_mm']==16
        assert a['outside_depth_change_mm']==0
    assert d['depurador_geometric_reach']['unreached_gap_mm']==42-30==12
    assert d['P15_new_side_pin_base_height_mm']==9-(-18)==27
    report=dict(cases=696,group_rows=4176,group_equilibria=len(groups),joint_interface_points=96,
        all_joint_points_on_positive_contact_faces=True,edge_only_mutation_rejected=True,
        hardware_variant_counts=totals,independent_equilibrium_max_error_N_Nmm=maxerr.tolist(),
        critical_vectors_keep_same_case=True,wood_access_zones=12,hardware_tool_real_clearance=False,
        geometry_and_R52_source_preserved=True,manufacturer_load_discrepancy_unresolved=True,
        tests_physical=0,gate='Implantacao nominal e solicitacoes;nao CNC/produto/ancoragem/capacidade liberados.')
    (OUT/'Verificacao_ligacoes_P09_P11_P15.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(report,ensure_ascii=True))

if __name__=='__main__':main()
