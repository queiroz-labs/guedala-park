"""Preserve R25 and add one optional maintenance parking control, defaulting to home."""
from pathlib import Path
import json, hashlib, shutil
import FreeCAD as App

root=(Path(__file__).resolve().parent / '.').resolve()
base=(Path(__file__).resolve().parent / '../Programa_R25_2026-10-14/Guedala_Park_R25_Programa_Conferido.FCStd').resolve()
target=(Path(__file__).resolve().parent / 'Guedala_Park_R26_Manutencao_Simples.FCStd').resolve()
audit=json.loads(((Path(__file__).resolve().parent / 'Estacionamento_Loop_R26.json').resolve()).read_text(encoding='utf-8'))
assert audit['status']=='complete_scoped_proposal' and not audit['contacts'] and not audit['errors']
base_hash=hashlib.sha256(base.read_bytes()).hexdigest()
assert base_hash==audit['source_sha256_before']
assert not target.exists()
shutil.copy2(base,target)
d=App.openDocument(str(target))
def snapshot(o):
 return {'placement':list(o.Placement.toMatrix().A) if 'Placement' in o.PropertiesList else None,
         'expressions':list(o.ExpressionEngine) if 'ExpressionEngine' in o.PropertiesList else None,
         'geometric_parent':o.getParentGeoFeatureGroup().Name if hasattr(o,'getParentGeoFeatureGroup') and o.getParentGeoFeatureGroup() else None,
         'group':sorted(q.Name for q in o.Group) if o.TypeId in ['App::Part','App::DocumentObjectGroup'] else None,
         'visibility':o.ViewObject.Visibility,
         'linked':o.LinkedObject.Name if o.TypeId=='App::Link' else None}
before={o.Name:snapshot(o) for o in d.Objects}
control=d.addObject('App::FeaturePython','ControleLoopManutencaoR26')
control.Label='Loop 20 L — afastamento temporário para manutenção (proposta)'
control.addProperty('App::PropertyLength','Afastamento','Manutenção proposta','0: lugar habitual; 650: estacionamento temporário lateral. Somente esses estados e o trajeto 0–650 foram conferidos.')
control.Afastamento=0
control.addProperty('App::PropertyLength','DestinoEstudo','Manutenção proposta')
control.DestinoEstudo=650;control.setEditorMode('DestinoEstudo',1)
control.addProperty('App::PropertyString','Sequencia','Manutenção proposta')
control.Sequencia='Antes de abrir para manutenção: lixeira vazia/fechada, afastar650 mm lateralmente para o centro da cozinha no CAD espelhado. Só então saco fora e conjunto sustentado/retenções reais liberadas; painel200 e armação0–400 são estudos. Repor armação/painel, fechar cesto e devolver lixeira0 antes do uso diário. Sem intertravamento, manuseio/pega/peso/piso/ferragens físicos não validados.'
control.setEditorMode('Sequencia',1)
control.addProperty('App::PropertyString','Status','Manutenção proposta')
control.Status='Endereço e percurso CAD propostos; não é rodízio, trilho, mecanismo ou liberação de manutenção real. Lugar habitual e programa preservados.'
control.setEditorMode('Status',1)
control.ViewObject.Visibility=False
navigation=d.getObject('ControlesAmbienteR003')
navigation.addObject(control)
navigation.Label='Lavanderia — aéreo, cesto e manutenção da lixeira'
bin_names=['Peca147','Peca148','Peca149']
for n in bin_names:
 o=d.getObject(n)
 assert not o.ExpressionEngine and o.getParentGeoFeatureGroup() is None
 o.setExpression('Placement.Base.x',str(o.Placement.Base.x)+' mm + '+control.Name+'.Afastamento')
original_sequence=d.getObject('ControleCestoR15').Sequencia
d.getObject('ControleCestoR15').Sequencia='Uso diário: abrir55, retirar saco445, endireitar55. Manutenção: no lugar habitual a armação bate na Loop20L em300/400; proposta R26 afastar a lixeira650 usando ControleLoopManutencaoR26 antes de retirar. Endereço/percurso geométricos conferidos, manuseio/peso/pega/piso/ferragem/retenção reais pendentes. Voltar armação/painel e fechar cesto antes de devolver lixeira0. Controles independentes sem intertravamento físico ou de software.'
d.recompute()
changes=[]
for name,old in before.items():
 new=snapshot(d.getObject(name));keys=[k for k in old if new[k]!=old[k]]
 if keys:
  assert (name in bin_names and keys==['expressions']) or (name==navigation.Name and keys==['group']),(name,keys)
  changes.append({'name':name,'fields':keys})
assert len(changes)==4
assert not [o.Name for o in d.Objects if 'Invalid' in o.State]
assert len(d.Objects)==len(before)+1
d.Label='Guedala Park — R26 — manutenção simples proposta'
d.save()
assert hashlib.sha256(base.read_bytes()).hexdigest()==base_hash
report={'base':str(base),'file':str(target),'base_sha256_before':base_hash,'base_sha256_after':base_hash,
 'sha256':hashlib.sha256(target.read_bytes()).hexdigest(),'objects_before':len(before),'objects_after':len(d.Objects),
 'changes':changes,'new_control':control.Name,'group':navigation.Name,'bin_parts':bin_names,'default_mm':0,'temporary_mm':650,
 'cesto_sequence_before':original_sequence,'cesto_sequence_after':d.getObject('ControleCestoR15').Sequencia,
 'navigation_label':navigation.Label,'all_previous_placements_visibility_link_targets_geometric_parents_preserved':True,'invalid':[],
 'limits':'No geometry change in saved home state, no bin reparenting, no new hardware. 46 navigation accesses, including one independent new control. Parking remains a proposal with physical handling, retention, load and floor unknown.'}
((Path(__file__).resolve().parent / 'Incorporacao_R26.json').resolve()).write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
App.setActiveDocument(d.Name)
result={'file':str(target),'objects':len(d.Objects),'changes':changes,'control':control.Name,'invalid':[]}
