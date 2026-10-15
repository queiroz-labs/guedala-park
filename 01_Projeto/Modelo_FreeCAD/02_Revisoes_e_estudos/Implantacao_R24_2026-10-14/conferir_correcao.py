"""Read the saved R24 and check only the changed sofa/current display scope."""
from pathlib import Path
import hashlib, json, time, traceback, zipfile
import xml.etree.ElementTree as ET
import FreeCAD as App

root=(Path(__file__).resolve().parent / '.').resolve()
correction=json.loads(((Path(__file__).resolve().parent / 'Correcao_R24.json').resolve()).read_text(encoding='utf-8'))
manifest=json.loads(((Path(__file__).resolve().parent / '../Auditoria_implantacao_R23_2026-10-14/Manifesto_implantacao_R23.json').resolve()).read_text(encoding='utf-8'))
source=Path(correction['file']);start=time.monotonic()
report={'file':str(source),'sha256_before':hashlib.sha256(source.read_bytes()).hexdigest(),
        'status':'running','pairs':0,'bbox_separated':0,'booleans':0,'contacts':[],'errors':[],
        'scope':'Only five current sofa primitives after correction against architecture and other displayed adopted solids; saved correction persistence',
        'criterion_mm3':0.1}
def bb(s):
    b=s.BoundBox;return [b.XMin,b.YMin,b.ZMin,b.XMax,b.YMax,b.ZMax]
def sep(a,b):return any(a[i+3]<=b[i]+1e-6 or b[i+3]<=a[i]+1e-6 for i in range(3))
def shape(o):
    s=o.Shape.copy();s.Placement=o.getGlobalPlacement();return s
d=None
try:
    d=App.openDocument(str(source))
    report['objects']=len(d.Objects)
    report['invalid']=[o.Name for o in d.Objects if 'Invalid' in o.State]
    assert not report['invalid']
    with zipfile.ZipFile(source) as z:
        gui=ET.fromstring(z.read('GuiDocument.xml'))
    visibility={}
    for p in gui.iter('ViewProvider'):
        for prop in p.iter('Property'):
            if prop.get('name')=='Visibility':visibility[p.get('name')]=prop.find('Bool').get('value')
    report['hidden_links']={name:visibility.get(name) for name in correction['hidden_links']}
    assert set(report['hidden_links'].values())=={'false'}
    sofa=[]
    for row in correction['sofa']:
        o=d.getObject(row['name']);s=shape(o)
        assert max(abs(a-b) for a,b in zip(o.Placement.toMatrix().A,row['after_matrix']))<1e-9
        assert max(abs(a-b) for a,b in zip(bb(s),row['after_bbox']))<1e-5
        assert abs(s.Volume-row['volume_mm3'])<1e-5 and s.isValid()
        if row['name'] not in ['Peca127','Peca128']:sofa.append((row['name'],s))
    all_sofa={row['name'] for row in correction['sofa']}
    targets=[r for r in manifest['architecture']+manifest['items'] if r['name'] not in all_sofa and r['name']!='Peca358']
    cache={}
    report['current_sofa']=[n for n,s in sofa]
    report['targets']=len(targets)
    for name,s in sofa:
        a=bb(s)
        for r in targets:
            report['pairs']+=1
            if sep(a,r['bbox_source_mm']):report['bbox_separated']+=1;continue
            report['booleans']+=1
            try:
                if r['name'] not in cache:cache[r['name']]=shape(d.getObject(r['name']))
                common=s.common(cache[r['name']])
                if common.Volume>.1:report['contacts'].append({'sofa':name,'target':r['name'],'target_label':r['label'],'volume_mm3':common.Volume,'common_bbox_source_mm':bb(common)})
            except Exception:report['errors'].append({'sofa':name,'target':r['name'],'error':traceback.format_exc()})
    report['status']='complete_changed_sofa_scope'
except Exception:report.update(status='failed',error=traceback.format_exc())
finally:
    if d is not None:App.closeDocument(d.Name)
    report['elapsed_s']=time.monotonic()-start
    report['sha256_after']=hashlib.sha256(source.read_bytes()).hexdigest()
    report['source_unchanged']=report['sha256_before']==report['sha256_after']
    report['limits']='Saved daily pose, selected modeled targets only. No guest conversion/intermediate mechanism, physical dimensions, people, load/fixation or fabrication release. Ceiling absent. Earlier unaffected tests not repeated.'
    ((Path(__file__).resolve().parent / 'Conferencia_correcao_R24.json').resolve()).write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    print('CORRECTION_CHECK',report['status'],report['pairs'],len(report['contacts']),len(report['errors']))
