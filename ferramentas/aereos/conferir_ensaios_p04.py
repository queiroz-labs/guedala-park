"""Confere pacote de preparacao fisica. Nao transforma formulários em ensaios."""
from pathlib import Path
from collections import Counter
import csv,json,math
import numpy as np
from pypdf import PdfReader
from fontes import sha,HASH_RULE
ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'04_Moveis/Aereos_suspensao'
def read(p):return json.loads(p.read_text(encoding='utf8'))
def csvread(p):
    with p.open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f,delimiter=';'))
def main():
    d=read(OUT/'P04_preparacao_ensaios.json');v=read(OUT/'P04_validacao.json');g=read(OUT/'Lote_B_geometria.json')
    assert d['hash_rule']==HASH_RULE and d['generator_sha256']==sha(Path(__file__).with_name('preparar_ensaios_p04.py'))
    assert d['hash_helper_sha256']==sha(Path(__file__).with_name('fontes.py'))
    for path,expected in d['sources_sha256'].items():assert sha(ROOT/path)==expected,path
    release=read(ROOT/'ferramentas/site/current_release.json');assert sha(ROOT/release['cadPath'])==d['cad_sha256']==v['cad_sha256']
    assert not d['cad_changed'] and not d['cad_opened'] and d['physical_tests_executed']==0
    assert 'Preparar para marcenaria/laboratório' in d['authorization']
    assert d['T0_external_mm']==[218,230,308] and d['T0_internal_height_mm']==272 and d['T0_gap_side_divider_mm']==7
    module=next(m for m in g['modules'] if m['code']=='P04');full=next(x for x in module['variants'] if x['preferred_for_study'])['boxes_uvz_mm']
    assert len(d['T0_cut_list'])==5
    for r in d['T0_cut_list']:
        source=np.array(full[r['source_CAD']]);b=np.array(r['box_uvz_mm']);assert np.allclose(b[:3],source[:3])
        assert np.allclose(b[[4,5]],source[[4,5]]) and b[3]==min(200,source[3])
        dims=sorted(b[3:]-b[:3]);assert dims==[r['nominal_thickness_mm'],r['finished_B_mm'],r['finished_A_mm']]
        assert r['nominal_thickness_mm']==18 and r['qty']==1
    cuts={r['source_CAD']:r['box_uvz_mm'] for r in d['T0_cut_list']}
    assert cuts['ApoioOpostoR002'][0]-cuts['Peca267'][3]==7
    assert cuts['Peca270'][2]-cuts['Peca269'][5]==272
    assert len(d['T0_joints'])==8 and Counter(r['axis'] for r in d['T0_joints'])=={'u':4,'z':4}
    assert {r['id'] for r in v['accesses']}==set(d['T0_critical_access_ids'])
    for access in v['accesses']:
        for box in access['entry_swept_boxes_mm']:
            assert box[0]>25 and box[3]<200 and box[2]>=18 and box[5]<=290
        for pose in access['rows']:
            assert pose['grip_swept_bbox_mm'][3]<200
    assert len(d['T0_fixed_calcos'])==2 and all(r['box_uvz_mm'][3]<200 for r in d['T0_fixed_calcos'])
    assert [r['qty_T0'] for r in d['T0_bom']]==[8,8,2,1,1]
    assert d['qualification_cases']==v['qualification_cases']
    records=d['registration_template'];assert len(records)==15
    assert Counter(r['stage'].split('_')[0] for r in records)=={'T0':4,'T1':4,'T2':6,'T3':1}
    measured=['replica','specimen_lot','measured_thickness_mm','actual_hardware','actual_tool','process_pilot_torque',
        'applied_V_N','applied_T_N','relative_displacement_mm','device_displacement_mm','min_clearance_mm',
        'damage_or_contact','recovery_mm','time_temperature_humidity','evidence_file','laboratory_id','result']
    assert all(r['status']=='NAO_EXECUTADO' and all(r[k]=='' for k in measured) for r in records)
    for filename,rows in [('P04_retalhos_T0.csv',d['T0_cut_list']),('P04_registro_laboratorio.csv',records)]:
        saved=csvread(OUT/filename);assert len(saved)==len(rows)
        for a,b in zip(saved,rows):assert all(a[k]==str(value) for k,value in b.items())
    pdfpath=OUT/'P04_ensaios_laboratorio.pdf';reader=PdfReader(pdfpath);assert len(reader.pages)==4
    texts=[p.extract_text() for p in reader.pages];assert all(t.strip() for t in texts)
    assert 'Nenhum ensaio f\u00edsico executado' in texts[0] and 'NAO_EXECUTADO' in texts[3]
    assert all(not p.get('/Annots') or all(a.get_object().get('/Subtype')!='/Widget' for a in p['/Annots']) for p in reader.pages)
    assert not reader.get_fields() # Protocolo estatico com fichas para impressao,nao AcroForm.
    report=dict(status='OK_PACOTE_PREPARATORIO',pdf_pages=4,T0_parts=5,T0_MF=8,T0_critical_accesses=4,
        empty_record_templates=15,physical_tests_executed=0,CAD_preserved=True,
        sources_sha256={p.name:sha(p) for p in [OUT/'P04_preparacao_ensaios.json',pdfpath,OUT/'P04_retalhos_T0.csv',OUT/'P04_registro_laboratorio.csv']},
        verifier_sha256=sha(Path(__file__)),hash_rule=HASH_RULE)
    (OUT/'P04_verificacao_preparacao.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    print(json.dumps(report,ensure_ascii=True))

if __name__=='__main__':main()
