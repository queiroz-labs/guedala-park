"""Read current navigation and bank/sofa dependencies; no mutations or recompute."""
from pathlib import Path
import FreeCAD as App
import json, hashlib

root=(Path(__file__).resolve().parent / '.').resolve()
base=(Path(__file__).resolve().parent / '../..').resolve()
file=(Path(__file__).resolve().parent / '../Folga_teto_R28_2026-10-14/Guedala_Park_R28_Folga_Teto_Proposta.FCStd').resolve()
d=App.ActiveDocument
assert d is not None and Path(d.FileName).resolve()==(Path(__file__).resolve().parent / '../Folga_teto_R28_2026-10-14/Guedala_Park_R28_Folga_Teto_Proposta.FCStd').resolve()
catalog=json.loads(((Path(__file__).resolve().parent / '../Rotulos_R23_2026-10-14/Controles_R23.json').resolve()).read_text(encoding='utf-8'))['catalog']
catalog=catalog+[{'control':'ControleLoopManutencaoR26','fields':['Afastamento'],'label':d.getObject('ControleLoopManutencaoR26').Label}]
bank=json.loads(((Path(__file__).resolve().parent / '../Banco_R16_2026-10-14/Montagem_R16.json').resolve()).read_text(encoding='utf-8'))
report={'file':str(file),'sha256':hashlib.sha256(file.read_bytes()).hexdigest(),'navigation':[], 'catalog':[], 'bank':{},'sofa':[],'method':'Read only, no recompute, save, movement, boolean or reopening.'}
nav=d.getObject('ControlesAtuaisR21')
for room in nav.Group:
    for entry in room.Group:
        original=entry.LinkedObject if entry.TypeId=='App::Link' else entry
        report['navigation'].append({'room':room.Label,'entry':entry.Name,'original':original.Name if original else None,'entry_label':entry.Label,'entry_type':entry.TypeId})
for row in catalog:
    o=d.getObject(row['control']); fields=[]
    for p in row['fields']:
        if o.TypeId=='Spreadsheet::Sheet':
            try: value=o.getContents(p); mode='spreadsheet cell'
            except Exception as exc: value=str(exc);mode='unresolved'
        elif p in o.PropertiesList:
            value=str(getattr(o,p));mode=o.getEditorMode(p)
        else: value=None;mode='missing'
        fields.append({'field':p,'value':value,'editor_mode':mode})
    report['catalog'].append({'control':o.Name,'label':o.Label,'fields':fields,'expressions':list(o.ExpressionEngine),'parents':[q.Name for q in o.InList],'bindings':[{'object':q.Name,'path':p,'expression':e} for q in o.InList if 'ExpressionEngine' in q.PropertiesList for p,e in q.ExpressionEngine if o.Name+'.' in e]})
def bbox(o):
    s=o.Shape.copy();s.Placement=o.getGlobalPlacement();b=s.BoundBox
    return [b.XMin,b.YMin,b.ZMin,b.XMax,b.YMax,b.ZMax]
m=d.getObject(bank['module'])
axis=m.getGlobalPlacement().Rotation.multVec(App.Vector(1,0,0))
report['bank']['module']=m.Name
report['bank']['placement_matrix']=list(m.getGlobalPlacement().toMatrix().A)
report['bank']['longitudinal_world_axis']=list(axis)
report['bank']['lids']=[]
for row in bank['lids']:
    driver=d.getObject(row['driver']);pad=d.getObject(row['cushion'])
    report['bank']['lids'].append({'sector':row['id'],'control':row['control'],'driver':driver.Name,'driver_axis':list(driver.Placement.Rotation.Axis),'driver_expressions':list(driver.ExpressionEngine),'lid':row['lid'],'lid_bbox':bbox(d.getObject(row['lid'])),'cushion':pad.Name,'cushion_bbox':bbox(pad),'cushion_placement_matrix':list(pad.Placement.toMatrix().A),'cushion_expressions':list(pad.ExpressionEngine),'pad_length_mm':float(pad.Length.Value),'separate':row['separate_cushion']})
report['bank']['content']=[{'object':n,'bbox':bbox(d.getObject(n))} for n in bank['content']+bank['panels']+[bank['leaf']]]
for n in ['Peca122','Peca123','Peca124','Peca125','Peca126']:
    report['sofa'].append({'object':n,'bbox':bbox(d.getObject(n))})
report['bank']['leaf']=bank['leaf']
report['control_instructions']={n:d.getObject(n).Sequencia for n in ['ControleCestoR15','ControleLoopManutencaoR26','ControleBancoR16','ControleBancoR001','ControleBancoR002','ControleBancoR003']}
report['sha256_after']=hashlib.sha256(file.read_bytes()).hexdigest()
assert report['sha256']==report['sha256_after']
((Path(__file__).resolve().parent / 'Leitura_controles_R28.json').resolve()).write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
result={'navigation':len(report['navigation']),'catalog':len(report['catalog']),'bank_axis':report['bank']['longitudinal_world_axis'],'file_unchanged':True}
