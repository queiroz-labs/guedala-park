"""Confere ocupacao, posicoes e equilibrio da pre-selecao, sem capacidade fisica."""
from collections import defaultdict
import csv,hashlib,json,math
from pathlib import Path
from detalhar_ligacoes import ROOT,OUT,W,H,G
import numpy as np

def read(p):return json.loads(p.read_text(encoding='utf-8'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    d=read(OUT/'Selecao_ferragem.json')
    assert sha(ROOT/'ferramentas/aereos/selecionar_ferragem.py')==d['script_sha256']
    for r in d['source_pdfs']:assert sha(ROOT/r['path'])==r['sha256']
    for p,v in d['source_input_sha256'].items():assert sha(ROOT/p)==v
    release=read(ROOT/'ferramentas/site/current_release.json')
    assert sha(ROOT/release['cadPath'])==d['cad_sha256']
    assert abs(d['occupancy']['pair_bounding_boxes_liters']-2*49.5*37.8*16/1e6)<1e-12
    assert d['occupancy']['back_relocation_mm']==0 and d['occupancy']['storage_depth_proposed_mm']==312
    dims=d['preferred_candidate']['dimensions']
    assert dims['slot_end_center_from_outer_corner_mm']==49.5-9==40.5
    assert dims['small_rear_hole_from_outer_corner_mm']==32-22.5==1.5+8==9.5
    mount=d['mounting_assessment']
    assert mount['left_cabinet_translation_mm']==-(49.5-9-32)==-8.5
    assert mount['right_cabinet_translation_mm']==49.5-9-32==8.5
    assert mount['left_cabinet_translation_mm']!=mount['right_cabinet_translation_mm']
    assert not mount['common_translation_for_two_mirrored_keyholes_exists']
    assert len(d['mounts'])==6
    for m in d['mounts']:
        assert m['upper_z_mm']==H[m['code']]-58 and m['couple_h_mm']==H[m['code']]-148
        assert m['old_rear_Confirmat_vertical_separation_mm']==32
        assert m['wood_clear'] and not m['actual_product_clearance_verified']
    old=read(OUT/'Resultados.json')['cases']
    old += [r for r in read(ROOT/'04_Moveis/P04/Suspensao_P04_P15/Resultados.json')['cases'] if r['code']=='P15']
    cases={(r['code'],r.get('variant','current'),int(r['id'])):r for r in old}
    with (OUT/'Solicitacoes_suporte_L.csv').open(encoding='utf-8-sig',newline='') as f:rows=list(csv.DictReader(f,delimiter=';'))
    assert len(rows)==4176
    groups=defaultdict(list)
    for r in rows:groups[(r['code'],r['variant'],int(r['source_case_id']),float(r['traction_share_left']))].append(r)
    worst=0.
    for key,pair in groups.items():
        assert len(pair)==2 and {int(r['side']) for r in pair}=={0,1}
        old=cases[key[:3]];w,h=W[key[0]],H[key[0]]
        targetV=old['weight_N']+G
        targetM=old.get('wall_normal_moment_Nm',old.get('wall_normal_gravity_moment_Nm'))*1000+174*G
        targetS=old['lateral_first_moment_Nmm']+w/2*G
        residuals=[abs(sum(float(r['V_N']) for r in pair)-targetV),
            abs(sum(float(r['V_N'])*float(r['u_mm']) for r in pair)-targetS),
            abs(sum(float(r['T_N'])*(h-148) for r in pair)-targetM)]
        worst=max(worst,*residuals);assert max(residuals)<1e-7
        for r in pair:
            assert float(r['u_mm']) in [40.5,w-40.5] and float(r['upper_z_mm'])==h-58
            assert abs(math.hypot(float(r['V_N']),float(r['T_N']))-float(r['R_N']))<1e-9
            x=40.5 if int(r['side'])==0 else -40.5
            moment=np.cross([x,-18,0],[0,-float(r['T_N']),float(r['V_N'])])/1000
            assert max(abs(moment[i]-float(r[k])) for i,k in enumerate(['reference_corner_Mu_Nm','reference_corner_Mv_Nm','reference_corner_Mz_Nm']))<1e-9
    assert len(groups)==2088
    for critical in d['critical_groups']:
        relevant=[r for r in rows if (r['code'],r['variant'],float(r['payload_kg']))==(critical['code'],critical['variant'],critical['payload_kg'])]
        assert abs(max(float(r['R_N']) for r in relevant)-critical['R_N'])<1e-8
    with (OUT/'Requisitos_suporte_L.csv').open(encoding='utf-8-sig',newline='') as f:qualification=list(csv.DictReader(f,delimiter=';'))
    assert len(qualification)==d['qualification_case_count']
    for code,variant in [('P09','current'),('P11','current'),('P15','current'),('P15','wood_study')]:
        allrows=[r for r in rows if r['code']==code and r['variant']==variant and float(r['payload_kg'])==(20 if code=='P15' else 10)]
        selected=[r for r in qualification if r['code']==code and r['variant']==variant]
        for k in ['V_N','T_N','R_N']:assert max(float(r[k]) for r in selected)==max(float(r[k]) for r in allrows)
    for r in qualification:
        assert any(all(r[k]==v for k,v in orig.items()) for orig in rows)
    report=dict(candidate='Bigfer04.02.058',nominal_pair_envelope_ml=59.8752,vectors=4176,group_pairs=2088,
        independent_equilibrium_max_error=worst,source_hashes_checked=True,capacity_or_mounting_proven=False,
        slot_and_small_hole_datums_corrected=True,mirrored_single_translation_rejected=True,
        reference_local_moments_checked=True,
        qualification_case_count=len(qualification),V_T_R_controlling_cases_preserved=True,
        physical_tests=0,CAD_preserved=True)
    (OUT/'Verificacao_selecao.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(report))

if __name__=='__main__':main()
