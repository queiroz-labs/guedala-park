"""New static coverage between different imported furniture/equipment families."""
from pathlib import Path
import json, hashlib, time, traceback
import FreeCAD as App

root=(Path(__file__).resolve().parent / '.').resolve();start=time.monotonic()
manifest=json.loads(((Path(__file__).resolve().parent / '../Auditoria_implantacao_R23_2026-10-14/Manifesto_implantacao_R23.json').resolve()).read_text(encoding='utf-8'))
correction=json.loads(((Path(__file__).resolve().parent / '../Implantacao_R24_2026-10-14/Correcao_R24.json').resolve()).read_text(encoding='utf-8'))
base=json.loads(((Path(__file__).resolve().parent / '../../05_Ferramentas_e_registros/Base_interativa.json').resolve()).read_text(encoding='utf-8'))
source=Path(correction['file'])
skip={'wardrobe','bedcabinet','mirror','officecab','drawers','kitchenbase','sinkstorage','kitchenupper','laundrybase','laundrybasket','laundryupper','bathvanity','bathmirror','bench','lowdrawer','microwave'}
families={};number=0
for n in base['nodes']:
    if n['kind']=='wall':number+=2;continue
    if n['id'] in skip:continue
    name='Peca'+(f'{number:03d}' if number else '');number+=1
    if n['id']:families[name]=n['id']
newboxes={r['name']:r['after_bbox'] for r in correction['sofa']}
rows=[]
for original in manifest['items']:
    if original['name'] not in families or original['name'] in ['Peca127','Peca128']:
        continue
    r=dict(original,family=families[original['name']])
    if r['name'] in newboxes:r['bbox_source_mm']=newboxes[r['name']]
    rows.append(r)
report={'file':str(source),'status':'running','sha256_before':hashlib.sha256(source.read_bytes()).hexdigest(),
        'scope':'Static imported adopted furniture/equipment, distinct family IDs. Architecture, modules and internal assembly contacts excluded; their audits are separate.',
        'manifest':[{'name':r['name'],'family':r['family'],'label':r['label']} for r in rows],
        'stats':{'pairs':0,'bbox_separated':0,'candidates':0,'booleans':0},'contacts':[],'errors':[],'criterion_mm3':0.1}
def sep(a,b):return any(a[i+3]<=b[i]+1e-6 or b[i+3]<=a[i]+1e-6 for i in range(3))
def bb(s):
    b=s.BoundBox;return [b.XMin,b.YMin,b.ZMin,b.XMax,b.YMax,b.ZMax]
def desc(r):return {k:r[k] for k in ['name','label','family','bbox_source_mm']}
out=(Path(__file__).resolve().parent / 'Encontros_moveis_R24.json').resolve()
def dump():
    report['elapsed_s']=time.monotonic()-start
    out.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
d=None
try:
    assert report['sha256_before']==correction['sha256']
    pairs=[]
    for i,a in enumerate(rows):
        for b in rows[i+1:]:
            if a['family']==b['family']:continue
            report['stats']['pairs']+=1
            if sep(a['bbox_source_mm'],b['bbox_source_mm']):report['stats']['bbox_separated']+=1
            else:pairs.append((a,b))
    report['stats']['candidates']=len(pairs)
    report['candidate_manifest']=[[desc(a),desc(b)] for a,b in pairs];dump()
    d=App.openDocument(str(source));cache={}
    def shape(r):
        if r['name'] not in cache:
            o=d.getObject(r['name']);s=o.Shape.copy();s.Placement=o.getGlobalPlacement()
            assert max(abs(x-y) for x,y in zip(bb(s),r['bbox_source_mm']))<1e-5
            cache[r['name']]=s
        return cache[r['name']]
    for a,b in pairs:
        if time.monotonic()-start>180:raise TimeoutError('180s budget exceeded')
        report['stats']['booleans']+=1
        try:
            common=shape(a).common(shape(b))
            if common.Volume>.1:report['contacts'].append({'one':desc(a),'two':desc(b),'volume_mm3':common.Volume,'common_bbox_source_mm':bb(common),'classification':'requires_context_not_automatic_error'})
        except Exception:report['errors'].append({'objects':[a['name'],b['name']],'error':traceback.format_exc()})
        dump()
    report['status']='complete_static_imported_families_scope'
except Exception:report.update(status='failed',error=traceback.format_exc())
finally:
    if d is not None:App.closeDocument(d.Name)
    report['sha256_after']=hashlib.sha256(source.read_bytes()).hexdigest()
    report['source_unchanged']=report['sha256_before']==report['sha256_after']
    report['limits']='Simplified saved static volumes, selected imported families only; no physical product/material/cutout validation or continuous movements. No CAD changes/save/GUI.'
    dump();print('FURNITURE_RESULT',report['status'],len(rows),report['stats'],len(report['contacts']),len(report['errors']))
