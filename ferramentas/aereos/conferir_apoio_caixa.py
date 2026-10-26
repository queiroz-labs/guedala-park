"""Certificados independentes de apoio,estatica3D e equilibrio do corpo de prova."""
from collections import defaultdict
from pathlib import Path
import csv,hashlib,json
import numpy as np
from detalhar_ligacoes import ROOT,OUT,W,H,profiles

def read(p):return json.loads(p.read_text(encoding='utf-8'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def csvrows(name):
    with (OUT/name).open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f,delimiter=';'))

def main():
    d=read(OUT/'Apoio_e_caixa.json');release=read(ROOT/'ferramentas/site/current_release.json')
    assert sha(ROOT/release['cadPath'])==d['cad_sha256']==release['cadSHA256']
    assert sha(ROOT/'ferramentas/aereos/analisar_apoio_caixa.py')==d['script_sha256']
    for p,v in d['input_sha256'].items():assert sha(ROOT/p)==v,p
    assert not d['cad_opened'] and not d['cad_changed']
    assert len(d['reference_lower_areas'])==8
    for a in d['reference_lower_areas']:
        b=profiles(a['code'],a['variant'])[a['piece']];band=a['reference_rear_face_uz_mm']
        assert (band[3]-band[0])*(band[5]-band[2])==1080==a['nominal_area_mm2']
        assert b[1]==0 and band[1]==band[4]==0
        assert b[0]<=band[0]<band[3]<=b[3] and b[2]<=60<120<=b[5]
        assert a['added_volume_mm3']==0 and not a['effective_contact_verified']
    upper=csvrows('Solicitacoes_suporte_L.csv');lower=csvrows('Reacoes_apoio_inferior.csv')
    def grouped(rows):
        out=defaultdict(list)
        for r in rows:out[(r['code'],r['variant'],r['source_case_id'],r['traction_share_left'])].append(r)
        return out
    up,lo=grouped(upper),grouped(lower);assert up.keys()==lo.keys() and len(lower)==4176
    worst=np.zeros(3);bad_copy_max=0.
    for key,pair in up.items():
        low=lo[key];assert len(pair)==len(low)==2
        T=sum(float(r['T_N']) for r in pair);moment=sum(float(r['T_N'])*float(r['u_mm']) for r in pair)
        errors=[abs(sum(float(r['C_N']) for r in low)-T),
            abs(sum(float(r['C_N'])*float(r['u_mm']) for r in low)-moment),
            abs(sum(float(r['C_N'])*float(r['z_mm']) for r in low)-90*T)]
        worst=np.maximum(worst,errors);assert max(errors)<1e-7
        for r in low:
            assert float(r['C_N'])>=0 and float(r['u_mm']) in [-9,W[r['code']]+9]
            assert abs(float(r['p_mean_nominal_MPa'])-float(r['C_N'])/1080)<1e-12
        # CopiarT paraC na lateral correspondente preservaria soma,mas falha guinada.
        wrong=sum(float(r['T_N'])*(-9 if int(r['side'])==0 else W[r['code']]+9) for r in pair)
        bad_copy_max=max(bad_copy_max,abs(wrong-moment))
    assert bad_copy_max>1000
    rows=csvrows('Corpos_prova_fundo_laterais.csv');assert len(rows)==48
    fixtures={str(f['id']):f for f in d['fixtures']};assert len(fixtures)==8 and d['fixture_configuration_count']==4
    assert len(d['specimens'])==4
    for s in d['specimens']:
        assert len(s['three_joint_z_from_side_bottom_mm'])==3
        assert all(abs(a+s['side_bottom_z_mm']-b-s['back_bottom_z_mm'])<1e-10 for a,b in zip(s['three_joint_z_from_side_bottom_mm'],s['three_joint_z_from_back_bottom_mm']))
        if s['variant']=='wood_study':assert s['side_bottom_z_mm']==s['back_bottom_z_mm']==-18
    worst_fixture=np.zeros(2)
    for fid,fx in fixtures.items():
        rr=[r for r in rows if r['fixture_id']==fid];assert len(rr)==6
        points=np.array([[float(r[k]) for k in ['u_mm','v_mm','z_mm']] for r in rr])
        reactions=np.array([[float(r[k]) for k in ['N_axis_u_N','Q_v_N','Q_z_N']] for r in rr])
        origin=np.array(fx['group_center_uvz_mm']);force=np.array(fx['applied_F_uvz_N']);at=np.array(fx['load_application_uvz_mm'])
        ef=float(np.max(np.abs(reactions.sum(axis=0)+force)))
        em=float(np.max(np.abs(sum((np.cross(p-origin,f) for p,f in zip(points,reactions)),np.zeros(3))+np.cross(at-origin,force))))
        worst_fixture=np.maximum(worst_fixture,[ef,em]);assert ef<1e-8 and em<1e-6
        lower_bound=np.linalg.norm(reactions)/np.sqrt(6)
        assert abs(lower_bound-fx['necessary_lower_bound_on_any_max_joint_resultant_N'])<1e-8
        assert max(np.linalg.norm(f) for f in reactions)>=lower_bound-1e-8
        # Uma coluna colinear nao geraMz por forcas pontuais na propria linha.
        for side in [0,1]:
            col=points[:3] if side==0 else points[3:];o=col.mean(axis=0)
            assert np.ptp(col[:,0])==np.ptp(col[:,1])==0
            assert all(np.cross(p-o,f)[2]==0 for p in col for f in np.eye(3))
            missing=np.cross(at-o,force)[2]/1000
            assert abs(missing-fx['one_column_checks'][side]['unbalanced_Mz_for_transfer_to_this_column_Nm'])<1e-10
        assert fx['matrix_rank']==6 and all(c['rank']==5 for c in fx['one_column_checks'])
    result=dict(lower_rows=4176,reference_contact_faces=8,nominal_area_per_face_mm2=1080,
        inferior_force_and_moment_max_errors_N_Nmm=worst.tolist(),wrong_side_copy_rejected=True,
        fixture_configurations=4,fixture_load_cases=8,fixture_joint_rows=48,
        independent_fixture_force_moment_errors_N_Nmm=worst_fixture.tolist(),single_point_column_torsion_rejected=True,
        specimen_datums_checked=True,contact_or_resistance_physically_proven=False,physical_tests=0,CAD_preserved=True)
    (OUT/'Verificacao_apoio_caixa.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(result))

if __name__=='__main__':main()
