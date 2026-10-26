"""Conferencia independente de premissas,contatos,acessos e demandas do loteB."""
from pathlib import Path
from collections import Counter
import csv,json,math,hashlib
import numpy as np
from fontes import sha,HASH_RULE
ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'04_Moveis/Aereos_suspensao';G=9.80665
def read(p):return json.loads(p.read_text(encoding='utf8'))
def csvread(p):
    with p.open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f,delimiter=';'))
def inside(point,box):return np.all(point>=box[:3]-1e-6) and np.all(point<=box[3:]+1e-6)
def overlaps(a,b):return np.all(np.minimum(a[3:],b[3:])-np.maximum(a[:3],b[:3])>1e-6)
def face(a,b,point,axis):
    delta=np.minimum(a[3:],b[3:])-np.maximum(a[:3],b[:3]);k='uvz'.index(axis)
    return abs(delta[k])<1e-6 and all(delta[j]>1e-6 for j in range(3) if j!=k) and inside(point,a) and inside(point,b)

def main():
    geom=read(OUT/'Lote_B_geometria.json');d=read(OUT/'Lote_B_detalhamento.json');p=read(OUT/'Lote_B_premissas.json')
    for data,script in [(geom,'reconciliar_lote_b.py'),(d,'detalhar_lote_b.py')]:
        assert data['hash_rule']==HASH_RULE and data['hash_helper_sha256']==sha(Path(__file__).with_name('fontes.py'))
        assert data['script_sha256']==sha(Path(__file__).with_name(script))
        for path,expected in data['sources_sha256'].items():assert sha(ROOT/path)==expected,path
        assert data['cad_changed'] is False
    release=read(ROOT/'ferramentas/site/current_release.json');assert sha(ROOT/release['cadPath'])==d['cad_sha256']==geom['cad_sha256']
    assert p['payload_targets_kg']==geom['chosen_payloads_kg']=={'P17':20,'P04':10,'P12':10}
    assert p['full_back_preferred_for_study']==['P17','P04'] and p['CAD_adoption_authorized'] is False
    assert p['P04_filler7_adopted'] is False and geom['chosen_hardware'] is None
    assert p['back_edge_finish']=={'P04':'Fita Arenza na borda inferior','P17':'Fita off-white na borda inferior'}
    assert geom['historical_map_rows']==47 and geom['current_mapped_contacts_all_positive']
    for recon in geom['reconciliation']:
        specs={}
        for r in csvread(ROOT/recon['dimension_csv']):
            for name in r['IDs CAD'].split(' | '):specs[name]=sorted(float(r[k]) for k in ['C nominal mm','L nominal mm','Esp. envelope mm'])
        assert hashlib.sha256(json.dumps(specs,sort_keys=True,separators=(',',':')).encode()).hexdigest()==recon['dimension_projection_sha256']
    assert geom['underside_positions_proposed']=={'P17':8,'P04':8}
    modules={m['code']:m for m in geom['modules']};boxes={};delta={}
    for code,m in modules.items():
        selected=next(v for v in m['variants'] if v['preferred_for_study']);assert selected['adopted'] is False
        boxes[code]={n:np.array(b) for n,b in selected['boxes_uvz_mm'].items()}
        old=m['variants'][0]['volume_mm3'];delta[code]=selected['volume_mm3']-old
        assert abs(delta[code]-m['full_back_additional_volume_mm3'])<1e-6
        for variant in m['variants']:
            a=list(variant['boxes_uvz_mm'].values())
            assert all(not overlaps(np.array(x),np.array(y)) for i,x in enumerate(a) for y in a[i+1:])
        assert m['external_and_useful_dimensions_change_mm']==0
    assert delta=={'P17':1272672.,'P04':1143072.,'P12':0.}
    assert len(d['joints'])==60
    counts=Counter(r['code'] for r in d['joints']);assert counts=={'P17':24,'P04':24,'P12':12}
    expected=Counter()
    for r in csvread(ROOT/'04_Moveis/Mapa_conectores/Mapa_conectores_R00.csv'):
        if r['Módulo'] in modules and r['Conector']=='Minifix 15':expected[(r['Módulo'],tuple(sorted([r['Peça A'],r['Peça B']])))] += int(r['Qtd conector'])
    actual=Counter((r['code'],tuple(sorted([r['a'],r['b']]))) for r in d['joints']);assert actual==expected
    blocked=[]
    for r in d['joints']:
        b=boxes[r['code']];point=np.array(r['interface_uvz_mm']);assert face(b[r['a']],b[r['b']],point,r['axis'])
        cam=np.array(r['cam_access_uvz_mm']);direction=np.array(r['drill_inward']);center=cam+9*direction
        vector=center-point;assert abs(np.linalg.norm(vector)-34)<1e-6
        pin_end=point-vector/34*8
        pin_part=r['b'] if r['cam_part']==r['a'] else r['a'];assert inside(pin_end,b[pin_part])
        bore=np.array(r['blind_bore_bbox_mm']);host=b[r['cam_part']]
        assert inside(bore[:3],host) and inside(bore[3:],host)
        hits=[n for n,bx in b.items() if overlaps(np.array(r['tool_corridor_bbox_mm']),bx)]
        assert hits==r['tool20_interferences'] and (not hits)==r['tool20_wood_clear']
        if hits:
            assert r['code']=='P04' and r['a']=='Peca267' and hits==['ApoioOpostoR002']
            assert r['local_straight_tool_diameter_limit_mm']==18;blocked.append(r['id'])
        if r['cam_part'] in ['Peca387','Peca269','Peca345']:assert bore[2]>=4-1e-6
        assert r['underside_face_unbroken'] and not r['hardware_clearance_verified'] and not r['purchase_quantity']
    assert len(blocked)==4
    assert len(d['rear_joints'])==48 and Counter(r['code'] for r in d['rear_joints'])=={'P17':24,'P04':24}
    for r in d['rear_joints']:
        b=boxes[r['code']];point=np.array(r['interface_uvz_mm']);assert face(b[r['a']],b[r['b']],point,'v')
        assert np.allclose(point[1],18) and r['nominal_length_beyond_back_mm']==32
        entry=np.array(r['rear_entry_uvz_mm']);tip=np.array(r['nominal_tip_uvz_mm'])
        assert abs(np.linalg.norm(tip-entry)-50)<1e-6 and entry[1]==0 and tip[1]==50
        assert inside(entry,b[r['a']]) and inside(tip,b[r['b']])
        if point[2]==9:assert r['nominal_wood_to_base_underside_mm']==5.5
        assert not r['head_pilot_or_capacity_selected'] and not r['purchase_quantity']
    # Controle negativo: uma coordenada deslocada para fora da face deve falhar.
    r=d['joints'][0];b=boxes[r['code']];bad=np.array(r['interface_uvz_mm'])+np.array([9999,0,0])
    assert not face(b[r['a']],b[r['b']],bad,r['axis'])
    historical=read(OUT/'Resultados.json')['cases']+read(ROOT/'04_Moveis/P04/Suspensao_P04_P15/Resultados.json')['cases']
    old={(c['code'],c['id']):c for c in historical if c['code'] in modules and c.get('variant','current')=='current'}
    assert len(d['cases'])==585;assert len(set((r['code'],r['source_case_id']) for r in d['cases']))==585
    max_error=0.
    for r in d['cases']:
        c=old[r['code'],r['source_case_id']];m=modules[r['code']];rho=r['rho_kg_m3'];extra=delta[r['code']]*rho/1e9*18.3/18
        oldmass=c.get('wood_plus_content_kg',c.get('total_wood_plus_content_kg'));expected_mass=oldmass+extra
        expected_M=c.get('wall_normal_moment_Nm',c.get('wall_normal_gravity_moment_Nm'))+extra*G*.009
        expected_S=c['lateral_first_moment_Nmm']+extra*G*m['width_internal_mm']/2
        errors=[abs(r['mass_wood_contents_kg']-expected_mass),abs(r['V_N']-G*expected_mass),abs(r['M_Nm']-expected_M),abs(r['S_Nmm']-expected_S)]
        max_error=max(max_error,*errors);assert max(errors)<1e-5
        assert r['payload_kg'] in [0,p['payload_targets_kg'][r['code']]] and not r['accessory_mass_included']
        assert abs(r['M_Nm']-r['V_N']*r['center_uvz_mm'][1]/1000)<1e-8
    for name,rows in [('Lote_B_ligacoes_internas.csv',d['joints']),('Lote_B_ligacoes_traseiras.csv',d['rear_joints']),('Lote_B_demandas.csv',d['cases'])]:
        saved=csvread(OUT/name);assert len(saved)==len(rows)
        for a,b in zip(saved,rows):assert all(a[k]==('' if v is None else str(v)) for k,v in b.items())
    result=dict(status='OK_COM_RESTRICOES',geometry_variants=5,positive_historical_contacts=47,
        current_underside_positions_to_replace=16,internal_MF_positions=60,rear_CF_positions=48,wood_only_tool20_clear=56,
        P04_left_accesses_requiring_actual_tool=blocked,load_cases=585,max_independent_load_error=max_error,
        CAD_preserved=True,no_capacity_demonstrated=True,
        source_sha256={n:sha(OUT/n) for n in ['Lote_B_geometria.json','Lote_B_detalhamento.json','Lote_B_premissas.json']},
        verifier_sha256=sha(Path(__file__)),hash_rule=HASH_RULE)
    (OUT/'Lote_B_verificacao.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    print(json.dumps(result,ensure_ascii=True))

if __name__=='__main__':main()
