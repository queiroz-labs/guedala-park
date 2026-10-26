"""Proposta de envelopes, sem abrir ou modificar CAD; nao e lista de corte."""
from pathlib import Path
import csv,gzip,hashlib,json
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'04_Moveis/Inventario_dimensional/Gavetas'
def main():
    bp=ROOT/'02_Modelo_3D/Base_verificacao.json.gz'
    base=json.loads(gzip.decompress(bp.read_bytes())); obs=base['objetos']
    audit=json.loads((OUT/'Conferencia_P01_P06.json').read_text(encoding='utf-8'))
    release=json.loads((ROOT/'ferramentas/site/current_release.json').read_text(encoding='utf-8'))
    assert hashlib.sha256((ROOT/release['cadPath']).read_bytes()).hexdigest()==base['sha256']==audit['cad_sha256']
    assert hashlib.sha256(bp.read_bytes()).hexdigest()==audit['base_sha256']
    assert hashlib.sha256((ROOT/audit['archived_drawing']).read_bytes()).hexdigest()==audit['drawing_sha256']
    groups=[['GavetaComumR08']+[f'GavetaComumR{i:03}' for i in range(1,6)]]
    groups += [[f'GavetaComumR{i:03}' for i in range(s,s+6)] for s in [12,24,36,48]]
    groups += [[f'MontagemG2R{i:03}' for i in [17,18,19,16,21,20]]]
    groups += [[f'GavetaComumR{i:03}' for i in range(60,66)]]
    roles=['lateral_x_maior','lateral_x_menor','fundo','traseira','frente_interna','frente_decorativa']
    rows=[]; parts=[]
    for src,names in zip(audit['rows'],groups):
        before=[]; after=[]
        for i,(role,name) in enumerate(zip(roles,names)):
            assert obs[name]['pai']==src['drawer']
            b=obs[name]['caixa_global'][:]; p=b[:]
            if i<2:
                d=.5 if i==0 else -.5
                p[0]+=d; p[3]+=d; p[4]+=10
            elif i<5:
                p[0]-=.5; p[3]+=.5
                if i in [2,3]: p[4]+=10
                if i==3: p[1]+=10
            before.append(b); after.append(p)
            parts.append(dict(drawer=src['drawer'],module=src['module'],object=name,role=role,
                before_box_mm=b,proposed_box_mm=p,delta_box_mm=[round(y-x,6) for x,y in zip(b,p)],
                scope='Envelope only; no machining',
                exception='Imported bottom envelope 16.196, not panel thickness' if name=='MontagemG2R019' else None))
        r,l,bt,re,fr,de=after
        assert r[0]-l[3]==src['carcass_width_A_mm']-41
        assert r[4]-r[1]==l[4]-l[1]==500
        assert r[3]-r[0]==l[3]-l[0]==15
        assert bt[2]-l[2]==12
        assert l[3]-bt[0]==bt[3]-r[0]==5
        assert re[0]==fr[0]==l[3] and re[3]==fr[3]==r[0]
        assert re[4]==bt[4]==l[4]
        assert de==before[5] and all(b[2]==p[2] and b[5]==p[5] for b,p in zip(before,after))
        assert re[1]-fr[4]==469
        assert l[0]+r[3]==before[1][0]+before[0][3]
        rows.append(dict(drawer=src['drawer'],module=src['module'],inner_width_mm=r[0]-l[3],
            external_width_mm=r[3]-l[0],depth_mm=500,
            back_clearance_mm=src['carcass_back_y_mm']-r[4],
            centered_side_clearance_mm=(src['carcass_width_A_mm']-(r[3]-l[0]))/2,
            inner_length_before_mm=before[3][1]-before[4][4],inner_length_proposed_mm=re[1]-fr[4],
            bottom_underside_offset_mm=bt[2]-l[2],groove_overlap_each_side_mm=5,
            front_and_z_preserved=True))
    trays=[]
    g2={p['role']:p for p in parts if p['drawer']=='Gaveta005'}
    for name in ['BandejaG2R06','BandejaG2R001']:
        b=obs[name]['caixa_global']; gaps={}
        for state in ['before_box_mm','proposed_box_mm']:
            gaps[state]=dict(left=b[0]-g2['lateral_x_menor'][state][3],right=g2['lateral_x_maior'][state][0]-b[3],
                front=b[1]-g2['frente_interna'][state][4],back=g2['traseira'][state][1]-b[4])
        assert all(gaps['proposed_box_mm'][k]>=v for k,v in gaps['before_box_mm'].items())
        trays.append(dict(object=name,preserved_box_mm=b,horizontal_gaps_mm=gaps,
            existing_bottom_envelope_z_overlap_mm=round(g2['fundo']['before_box_mm'][5]-b[2],6),
            status='Actual shapes/support unresolved; vertical envelope overlap already exists'))
    result=dict(status='PROPOSTA_NAO_APLICADA',cad_sha256=base['sha256'],source_audit='Conferencia_P01_P06.json',
        cad_opened=False,cad_changed=False,physical_tests_executed=0,rows=rows,parts=parts,preserved_trays=trays,
        limits=['Global bounding boxes in mm, not cut list or CAD features.',
        'Groove overlap inferred from envelopes; actual grooves not verified.',
        'Hardware, fasteners, holes, vertical adjustment and removal unresolved.',
        'T51 excluded: never a FGVTN drilling template.',
        'No collision sweep, strength or capacity verification.'])
    (OUT/'Proposta_FGVTN_500.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    with (OUT/'Pecas_proposta_FGVTN_500.csv').open('w',encoding='utf-8',newline='') as f:
        w=csv.writer(f); w.writerow(['gaveta','modulo','objeto','funcao','caixa_atual_xyzXYZ_mm','caixa_proposta_xyzXYZ_mm','delta_xyzXYZ_mm','limite'])
        for p in parts: w.writerow([p['drawer'],p['module'],p['object'],p['role'],p['before_box_mm'],p['proposed_box_mm'],p['delta_box_mm'],p['exception'] or p['scope']])
    print('7 caixas; 42 pecas (35 envelopes propostos, 7 frentes preservadas); 2 bandejas preservadas. CAD intacto.')
if __name__=='__main__': main()
