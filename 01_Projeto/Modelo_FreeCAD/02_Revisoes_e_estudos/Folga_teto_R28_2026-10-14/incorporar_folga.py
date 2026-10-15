"""Save20mm top-gap proposal by lowering the cabinet, without reducing storage."""
from pathlib import Path
import json,hashlib,shutil
import FreeCAD as App
root=(Path(__file__).resolve().parent / '.').resolve();base=(Path(__file__).resolve().parent / '../..').resolve()
source=(Path(__file__).resolve().parent / '../Geometria_R27_2026-10-14/Guedala_Park_R27_Geometria_Oficial.FCStd').resolve()
target=(Path(__file__).resolve().parent / 'Guedala_Park_R28_Folga_Teto_Proposta.FCStd').resolve()
audit=json.loads(((Path(__file__).resolve().parent / 'Conferencia_folga_R28.json').resolve()).read_text(encoding='utf-8'))
assert audit['status']=='proposal_passed_scoped_lowering' and not audit['contacts'] and not audit['errors']
assert not target.exists()
sourcehash=hashlib.sha256(source.read_bytes()).hexdigest();assert sourcehash==audit['sha256_before']
shutil.copy2(source,target);d=App.openDocument(str(target))
def snapshot(o):
 return {'placement':list(o.Placement.toMatrix().A) if 'Placement' in o.PropertiesList else None,
         'expressions':list(o.ExpressionEngine) if 'ExpressionEngine' in o.PropertiesList else None,
         'parents':sorted(q.Name for q in o.InList if q.TypeId in ['App::Part','App::DocumentObjectGroup']),
         'visibility':o.ViewObject.Visibility,'linked':o.LinkedObject.Name if o.TypeId=='App::Link' else None}
before={o.Name:snapshot(o) for o in d.Objects};m=d.getObject('Modulo016')
volumes={r['name']:d.getObject(r['name']).Shape.Volume for r in audit['parts']}
dimensions={n:str(getattr(m,n)) for n in ['Altura','Comprimento','Profundidade','Chapa','Fundo','Frente','Junta']}
sheet=d.getObject('Dimensoes016');sheetbefore=sheet.Content
p=m.Placement;assert abs(p.Base.z-1920)<1e-8;p.Base.z=1900;m.Placement=p
m.addProperty('App::PropertyLength','FolgaTetoProposta','Instalação proposta R28')
m.FolgaTetoProposta=20;m.setEditorMode('FolgaTetoProposta',1)
m.addProperty('App::PropertyString','InstalacaoR28','Instalação proposta R28')
m.InstalacaoR28='Proposta: baixar o conjunto20mm; corpo2000x350x550 e vãos internos intactos. Base1900/topo2450, sob teto hipotético2470. Folga nominal20 sem mecanismo/tapa-fresta; conferir teto acabado/instalação/fixação antes de cortar ou furar.'
m.setEditorMode('InstalacaoR28',1)
d.recompute()
assert dimensions=={n:str(getattr(m,n)) for n in dimensions}
assert sheet.Content==sheetbefore
for n,v in volumes.items():assert abs(d.getObject(n).Shape.Volume-v)<1e-6
changes=[]
for n,s in before.items():
 keys=[k for k,v in snapshot(d.getObject(n)).items() if s[k]!=v]
 if keys:
  assert n==m.Name and keys==['placement'],(n,keys)
  changes.append({'name':n,'fields':keys})
assert len(changes)==1 and len(d.Objects)==len(before)
assert not [o.Name for o in d.Objects if 'Invalid' in o.State]
d.Label='Guedala Park — R28 — folga ao teto proposta'
d.save()
assert hashlib.sha256(source.read_bytes()).hexdigest()==sourcehash
report={'base':str(source),'file':str(target),'base_sha256_before':sourcehash,'base_sha256_after':sourcehash,
 'sha256':hashlib.sha256(target.read_bytes()).hexdigest(),'objects':len(d.Objects),'changes':changes,
 'module':m.Name,'dimensions_preserved':dimensions,'sheet_unchanged':True,'all_61_native_part_volumes_unchanged':True,
 'new_metadata':['FolgaTetoProposta','InstalacaoR28'],'base_before_after_mm':[1920,1900],'top_before_after_mm':[2470,2450],
 'proposed_ceiling_gap_mm':20,'invalid':[],'limits':'Installation position proposal only; no loss of internal storage, no new mechanisms or finishing strip, no physical ceiling measurement or fixation/fabrication release.'}
((Path(__file__).resolve().parent / 'Incorporacao_R28.json').resolve()).write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
App.setActiveDocument(d.Name)
result={'file':str(target),'base_mm':1900,'top_mm':2450,'proposed_gap_mm':20,'internal_storage_preserved':True,'invalid':[]}
