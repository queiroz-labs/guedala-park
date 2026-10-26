"""P20: equilibrio por formulas de alavanca, energia e acao/reacao."""
from pathlib import Path
import json, math
import numpy as np
from fontes import sha,HASH_RULE
ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'04_Moveis/P20/Assento_fechado'


def main():
    d=json.loads((OUT/'Montagem_aberta.json').read_text(encoding='utf-8'))
    g=json.loads((OUT/'Geometria_R51.json').read_text(encoding='utf-8'))
    assert d['generator_sha256']==sha(Path(__file__).with_name('detalhar_banco_aberto.py'))
    for p,h in d['sources_sha256'].items():assert sha(ROOT/p)==h,p
    assert not d['cad_changed'] and not d['cad_opened'] and d['physical_tests_executed']==0
    errors=[]
    for r in d['load_cases']:
        lid=next(x for x in g['lids'] if x['name']==r['lid']);b=lid['box'];L=b[4]-b[1]
        origin=np.array(r['origin_mm']);cg=np.array(r['cg_open_mm'])-origin
        mobile=np.array(r['mobile_terminal_mm']);fixed=np.array(r['fixed_terminal_mm'])
        v=mobile-fixed;v/=np.linalg.norm(v);p=mobile-origin
        W=lid['volume_mm3']*r['rho_kg_m3']/1e9*9.80665
        arm=p[0]*v[2]-p[2]*v[0]
        C=W*cg[0]/arm;F=C*v;s=mobile[1]-b[1]
        right=np.array([-F[0]*s/L,0,(W*L/2-F[2]*s)/L]);left=np.array([-F[0],0,W-F[2]])-right
        assert C>0 and abs(C-r['compression_N'])<1e-9 and r['tension_positive_N']<0
        assert np.allclose(F,r['force_articulator_on_lid_N'])
        assert np.allclose([left,right],r['hinge_forces_on_lid_N'])
        body=sum(np.array(r['hinge_forces_on_body_N']))+r['fixed_terminal_receives_N']
        assert np.allclose(body,[0,0,-W])
        residual=F+left+right+[0,0,-W];errors.append(float(max(abs(residual))))
        # Somatorio de momentos pelo ponto fixo: verifica reducao de forcas
        # sem reutilizar a matriz do gerador.
        moments=np.cross(mobile-origin,F)+np.cross(cg,[0,0,-W])
        for point,force in zip(r['hinge_equivalent_points_mm'],[left,right]):moments+=np.cross(np.array(point)-origin,force)
        assert max(abs(moments))<1e-7
    for r in d['operation']:
        lid=next(x for x in g['lids'] if x['name']==r['lid']);b=lid['box'];x=(b[0]+b[3])/2-100;z=(b[2]+b[5])/2-423.1
        W=lid['volume_mm3']*r['rho_kg_m3']/1e9*9.80665;t=math.radians(r['angle_deg'])
        expected=W*(x*math.sin(t)+z*(math.cos(t)-1))/1000
        assert abs(expected-r['energy_above_closed_J'])<1e-9
        assert r['articulator_axial_force_during_folded_motion'] is None
    assert len(d['load_cases'])==6 and len(d['operation'])==42 and len(d['lock_sensitivity'])==10
    for lid in [x['name'] for x in g['lids']]:
        rows=[r for r in d['lock_sensitivity'] if r['lid']==lid]
        assert all(a['angle_deg']<b['angle_deg'] for a,b in zip(rows,rows[1:]))
        assert abs(rows[-1]['angle_deg']-90)<1e-7
    assert d['known_piano']['remainder_min_before_saw_and_end_trimming_mm']==194
    assert all(x['physical_result'] is None for x in d['interfaces'])
    report=dict(status='OK_ESTATICA_NOMINAL_P20',cases=6,operation_poses=42,lock_sensitivities=10,
        max_force_error_N=max(errors),physical_tests_executed=0,capacity_demonstrated=False,
        result_sha256=sha(OUT/'Montagem_aberta.json'),verifier_sha256=sha(Path(__file__)),hash_rule=HASH_RULE)
    (OUT/'Verificacao_montagem_aberta.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(report))


if __name__=='__main__':main()
