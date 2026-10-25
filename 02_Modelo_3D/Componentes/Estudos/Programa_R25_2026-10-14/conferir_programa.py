from pathlib import Path
import hashlib,json,time,traceback
import FreeCAD as App
root=(Path(__file__).resolve().parent / '.').resolve();start=time.monotonic()
r=json.loads(((Path(__file__).resolve().parent / 'Correcao_R25.json').resolve()).read_text(encoding='utf-8'))
manifest=json.loads(((Path(__file__).resolve().parent / '../Auditoria_implantacao_R23_2026-10-14/Manifesto_implantacao_R23.json').resolve()).read_text(encoding='utf-8'))
correction=json.loads(((Path(__file__).resolve().parent / '../Implantacao_R24_2026-10-14/Correcao_R24.json').resolve()).read_text(encoding='utf-8'))
source=Path(r['file'])
report={'file':str(source),'status':'running','sha256_before':hashlib.sha256(source.read_bytes()).hexdigest(),
        'scope':'Only saved mirror centering and equal-envelope two-panel headboard representation; unaffected motions not repeated',
        'mirror_pairs':0,'mirror_bbox_separated':0,'mirror_booleans':0,'contacts':[],'errors':[]}
def bb(s):
    b=s.BoundBox;return [b.XMin,b.YMin,b.ZMin,b.XMax,b.YMax,b.ZMax]
def shape(o):
    s=o.Shape.copy();s.Placement=o.getGlobalPlacement();return s
def sep(a,b):return any(a[i+3]<=b[i]+1e-6 or b[i+3]<=a[i]+1e-6 for i in range(3))
d=None
try:
    d=App.openDocument(str(source));report['objects']=len(d.Objects)
    report['invalid']=[o.Name for o in d.Objects if 'Invalid' in o.State]
    assert not report['invalid']
    comp=d.getObject(r['compound']);old=d.getObject('Peca107');link=d.getObject(r['headboard_link'])
    assert link.LinkedObject==comp and link.LinkTransform
    report['panel_count']=len(comp.Links)
    assert report['panel_count']==2
    s=shape(comp);o=shape(old)
    report['headboard_bbox_source']=bb(s);report['headboard_bbox_mirrored']=bb(link.Shape)
    assert max(abs(a-b) for a,b in zip(bb(s),r['headboard_bbox_source']))<1e-5
    assert max(abs(a-b) for a,b in zip(bb(link.Shape),r['headboard_bbox_mirrored']))<1e-5
    report['headboard_added_volume_mm3']=s.cut(o).Volume
    report['headboard_removed_volume_mm3']=o.cut(s).Volume
    assert report['headboard_added_volume_mm3']<1e-5 and report['headboard_removed_volume_mm3']<1e-5
    mirror=shape(d.getObject('Peca275'));assert bb(mirror)==r['mirror_after_bbox']
    assert abs((mirror.BoundBox.YMin+mirror.BoundBox.YMax)/2-3615)<1e-6
    report['mirror_bbox_source']=bb(mirror)
    newboxes={x['name']:x['after_bbox'] for x in correction['sofa']}
    for item in manifest['architecture']+manifest['items']:
        if item['name'] in ['Peca275','Peca127','Peca128','Peca358']:continue
        bounds=newboxes.get(item['name'],item['bbox_source_mm'])
        report['mirror_pairs']+=1
        if sep(bb(mirror),bounds):report['mirror_bbox_separated']+=1;continue
        report['mirror_booleans']+=1
        try:
            common=mirror.common(shape(d.getObject(item['name'])))
            if common.Volume>.1:report['contacts'].append({'mirror':'Peca275','target':item['name'],'volume_mm3':common.Volume,'bbox_source':bb(common)})
        except Exception:report['errors'].append({'target':item['name'],'error':traceback.format_exc()})
    report['status']='complete_changed_program_scope'
except Exception:report.update(status='failed',error=traceback.format_exc())
finally:
    if d is not None:App.closeDocument(d.Name)
    report['sha256_after']=hashlib.sha256(source.read_bytes()).hexdigest()
    report['source_unchanged']=report['sha256_before']==report['sha256_after']
    report['elapsed_s']=time.monotonic()-start
    report['limits']='Nominal geometry/representation only; panel seam and dimensions remain proposals. No adhesive/fixation/capacity certification. No CAD save or unrelated tests.'
    ((Path(__file__).resolve().parent / 'Conferencia_R25.json').resolve()).write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    print('PROGRAM_CHECK',report['status'],report['mirror_pairs'],len(report['contacts']),len(report['errors']))
