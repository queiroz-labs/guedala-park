"""Read only; adopted link composition + saved child GUI visibility define scope."""
from pathlib import Path
import json,hashlib,zipfile,xml.etree.ElementTree as ET,time
import FreeCAD as App
root=(Path(__file__).resolve().parent / '.').resolve();started=time.monotonic()
source=Path(json.loads(((Path(__file__).resolve().parent / '../Rotulos_R23_2026-10-14/Rotulos_R23.json').resolve()).read_text(encoding='utf-8'))['file'])
mapping=json.loads(((Path(__file__).resolve().parent / '../Apartamento_espelhado_R20_2026-10-14/Espelhamento_R20.json').resolve()).read_text(encoding='utf-8'))['mapping']
with zipfile.ZipFile(source) as z:
 xml=ET.fromstring(z.read('GuiDocument.xml'))
vis={o.attrib['name']:(o.find("Properties/Property[@name='Visibility']/Bool").attrib['value']=='true') for o in xml.find('ViewProviderData') if o.find("Properties/Property[@name='Visibility']/Bool") is not None}
EXCLUDED={'FolhaAReal','FolhaBReal','PrincipalBlumR03','PrincipalBlumR001','DivisorApoioVizinhaR03','Peca251','Peca252','Peca253','Peca254'}
BOOLEAN_TYPES={'Part::Cut','Part::Fuse','Part::MultiFuse','Part::Common','Part::MultiCommon','Part::Compound'}
d=App.openDocument(str(source));selected=[];excluded=[];walls=[];architectural=[];seen=set();modules=[]
def row(o,context):
 s=o.Shape.copy();s.Placement=o.getGlobalPlacement();b=s.BoundBox
 return dict(context,name=o.Name,label=o.Label,type=o.TypeId,tipo_peca=getattr(o,'TipoPeca',None),bbox_source_mm=[b.XMin,b.YMin,b.ZMin,b.XMax,b.YMax,b.ZMax],volume_mm3=s.Volume,solid_count=len(s.Solids),matrix_source=o.getGlobalPlacement().Matrix.A,adoption_scope='historical_display_error' if o.Label.lower().startswith('hist') else 'adopted_result')
def walk(o,context,isroot=False):
 if o.Name in seen:return
 if o.Name.startswith('Historico') or o.Name in EXCLUDED:
  excluded.append(dict(context,name=o.Name,reason='explicit adopted exclusion R22/history'));return
 if any(p.TypeId in BOOLEAN_TYPES for p in o.InList):
  excluded.append(dict(context,name=o.Name,reason='boolean operand, final result selected'));return
 if not isroot and not vis.get(o.Name,False):
  excluded.append(dict(context,name=o.Name,reason='saved child visibility false'));return
 if o.TypeId in ['App::Part','App::DocumentObjectGroup']:
  for c in o.Group:walk(c,context)
 elif 'Shape' in o.PropertiesList:
  seen.add(o.Name);selected.append(row(o,context))
 else:excluded.append(dict(context,name=o.Name,reason='not a solid result'))
for r in mapping:
 link=d.getObject(r['link']);src=link.LinkedObject
 context={'link':r['link'],'source_root':src.Name,'source_group':r['source_group']}
 assert r['source_roots']==[src.Name]
 if not vis.get(link.Name,False):
  excluded.append(dict(context,name=src.Name,reason='saved mirror link not displayed'));continue
 if r['source_group']=='ParedesInteiras':walls.append(row(src,context));continue
 if r['source_group']=='ParedesCortadas':excluded.append(dict(context,name=src.Name,reason='cut wall duplicate'));continue
 if src.Name.startswith('Modulo'):modules.append({'name':src.Name,'label':src.Label,'link':link.Name})
 walk(src,context,True)
for r in list(selected):
 text=r['label'].lower()
 if r['tipo_peca']=='Arquitetura de estudo' and (text.startswith('floor') or text.startswith('piso') or text.startswith('ceiling') or text.startswith('teto')):
  r['architectural_class']='floor' if text.startswith('floor') or text.startswith('piso') else 'ceiling'
  architectural.append(r);selected.remove(r)
 elif r['solid_count']==0 or r['volume_mm3']<=0:
  excluded.append(dict(r,reason='non-volumetric reference geometry, no solid'));selected.remove(r)
for r in walls:r['architectural_class']='wall';architectural.append(r)
report={'file':str(source),'sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'gui_up':bool(App.GuiUp),
 'selection':'Actual App::Link composition as saved in R23; saved GuiDocument child visibility with explicit R22 final results/retired exclusions. Root source visibility overridden by active mirror link. Base source coordinate frame preserved; shared mirror isometry.',
 'modules':modules,'architecture':architectural,'items':selected,'excluded':excluded,'retired_visible_roots':[x for x in selected if x['adoption_scope']=='historical_display_error'],
 'counts':{'modules':len(modules),'architecture':len(architectural),'walls':sum(x['architectural_class']=='wall' for x in architectural),'floors':sum(x['architectural_class']=='floor' for x in architectural),'ceilings':sum(x['architectural_class']=='ceiling' for x in architectural),'item_results':len(selected),'item_roots':len({x['source_root'] for x in selected}),'adopted_item_results':sum(x['adoption_scope']=='adopted_result' for x in selected),'historical_display_errors':sum(x['adoption_scope']=='historical_display_error' for x in selected)},
 'elapsed_s':time.monotonic()-started}
App.closeDocument(d.Name)
((Path(__file__).resolve().parent / 'Manifesto_implantacao_R23.json').resolve()).write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print('INVENTORY',report['counts'],report['elapsed_s'])
