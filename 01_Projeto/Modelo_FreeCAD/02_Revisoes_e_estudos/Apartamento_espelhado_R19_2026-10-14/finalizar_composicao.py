from pathlib import Path
import json,hashlib
import FreeCAD as App,FreeCADGui as Gui
root=(Path(__file__).resolve().parent / '.').resolve();base=(Path(__file__).resolve().parent / '../..').resolve();p=(Path(__file__).resolve().parent / 'Guedala_Park_R19_Apartamento_Espelhado.FCStd').resolve();src=(Path(__file__).resolve().parent / '../Portas_opostas_R18_2026-10-14/Guedala_Park_R18_Portas_Opostas.FCStd').resolve()
assert not ((Path(__file__).resolve().parent / 'Espelhamento_R19.json').resolve()).exists(),'Composição já finalizada'
d=next(x for x in App.listDocuments().values() if x.FileName and Path(x.FileName).resolve()==p);prev=next(x for x in App.listDocuments().values() if x.FileName and Path(x.FileName).resolve()==src)
source=d.getObject('FonteApartamentoR19');mirror=d.getObject('ApartamentoEspelhadoR19');assert source and mirror
probe=App.getDocument('TesteEspelhoR19').addObject('App::Feature','ProbeGlobal')
probe.addProperty('App::PropertyLinkGlobal','ParametroGlobal')
scope_fixes=[]
for o in d.Objects:
 for n in ['PlanilhaDimensoes','FonteControle']:
  if n in o.PropertiesList and o.getTypeIdOfProperty(n)=='App::PropertyLink':
   value=getattr(o,n);group=o.getGroupOfProperty(n);doc=o.getDocumentationOfProperty(n);mode=o.getEditorMode(n)
   assert o.removeProperty(n)
   o.addProperty('App::PropertyLinkGlobal',n,group,doc);setattr(o,n,value);o.setEditorMode(n,mode)
   scope_fixes.append({'object':o.Name,'property':n,'target':value.Name if value else None})
mapping=[]
for room in source.Group:
 title=room.Label.removesuffix(' - base paramétrica');old_parent=next((o for o in prev.Objects if o.TypeId=='App::DocumentObjectGroup' and o.Label==title),None)
 if old_parent and (old_parent.Name.startswith('Ambiente_') or old_parent.Name=='ParedesCortadas'):room.Visibility=True
 for o in room.Group:
  old=prev.getObject(o.Name)
  if old:o.Visibility=old.Visibility
  mapping.append({'object':o.Name,'room_part':room.Name,'source_parent':old_parent.Name if old_parent else 'Outros'})
for i in range(20):d.getObject('Modulo'+('%03d'%i if i else '')).Visibility=True
for o in d.Objects:
 if o.Name.startswith(('FrenteSimples','FerragemSimples','ApoioPortaB','FaixaQuina')) or o.Name in ['PlacaL','PlacaL001','Peca255','Peca256','LateralApoioPrincipal']:
  o.Visibility=True;parent=o.getParentGeoFeatureGroup()
  while parent and parent!=source:parent.Visibility=True;parent=parent.getParentGeoFeatureGroup()
for o in d.Objects:
 if o.Name.startswith('Historico'):o.Visibility=False
source.Visibility=False;mirror.Visibility=True;d.recompute()
def bounds(s):
 b=s.optimalBoundingBox();return [b.XMin,b.YMin,b.ZMin,b.XLength,b.YLength,b.ZLength]
samples=[]
r18=json.loads(((Path(__file__).resolve().parent / '../Portas_opostas_R18_2026-10-14/Montagem_R18.json').resolve()).read_text(encoding='utf-8'))
office_front=next(r['front'] for r in r18['doors'] if r['module']=='Modulo016')
for n in ['Peca351','Peca140','Peca138',office_front,'FrenteVizinhaR18']:
 o=d.getObject(n);parts=[];parent=o
 while parent and parent!=source:parts.append(parent.Name);parent=parent.getParentGeoFeatureGroup()
 path='.'.join(reversed(parts))+'.';s=o.Shape.copy();s.Placement=o.getGlobalPlacement();old=bounds(s)
 linked=mirror.getSubObject(path);assert linked is not None,(n,path)
 new=bounds(linked);expected=[7400-old[0]-old[3],old[1],old[2],old[3],old[4],old[5]];err=max(abs(x-y) for x,y in zip(new,expected));assert err<1e-6,(n,new,expected)
 samples.append({'object':n,'link_path':path,'source_bbox':old,'mirrored_bbox':new,'max_error_mm':err})
matrix_errors=[]
for r in mapping:
 old=prev.getObject(r['object']);o=d.getObject(r['object'])
 if old:matrix_errors.append(max(abs(x-y) for x,y in zip(old.getGlobalPlacement().Matrix.A,o.getGlobalPlacement().Matrix.A)))
assert max(matrix_errors)<1e-7
invalid=[o.Name for o in d.Objects if 'Invalid' in o.State];assert not invalid,str(invalid)
door_map=[]
for mn in ['Modulo016','Modulo003']:
 rr=[r for r in r18['doors'] if r['module']==mn]
 for i,r in enumerate(reversed(rr),1):door_map.append({'module':mn,'visual_number':i,'door':r['door'],'control':r['control'],'side_source':r['side'],'side_apartment':'left' if r['side']=='right' else 'right','front':r['front']})
for folder,fn in [('Dobradicas_R10_2026-10-14','Montagem_R10.json'),('Banheiro_R12_2026-10-14','Montagem_R12.json')]:
 for r in json.loads((base/'02_Revisoes_e_estudos'/folder/fn).read_text(encoding='utf-8'))['doors']:door_map.append({'module':r['module'],'door':r['door'],'control':r['control'],'side_source':r['side'],'side_apartment':'left' if r['side']=='right' else 'right','front':r['front']})
App.setActiveDocument(d.Name);Gui.getDocument(d.Name).activeView().viewAxonometric();Gui.getDocument(d.Name).activeView().fitAll();Gui.updateGui();d.save()
report={'file':str(p),'source':str(src),'source_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'reflection_constant_x_mm':7400,'mirror_plane_x_mm':3700,'source_group':source.Name,'mirror_link':mirror.Name,'geometric_roots_packed':len(mapping),'mapping':mapping,'linked_shape_checks':samples,'max_original_world_matrix_change':max(matrix_errors),'door_map':door_map,'invalid':invalid,'global_parameter_links':scope_fixes,'scope':'Composição integral nativa porApp::Link/ScaleVector(-1,1,1). Fonte paramétrica e controles no mesmo arquivo, fontesSTEP preservadas. Distâncias e encontros preservados por isometria quando a composição inteira acompanha o vínculo; não homologação física de ferragens ou fabricação.'}
((Path(__file__).resolve().parent / 'Espelhamento_R19.json').resolve()).write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
result={'file':str(p),'roots':len(mapping),'max_matrix_change':max(matrix_errors),'checks':samples,'invalid':invalid}
