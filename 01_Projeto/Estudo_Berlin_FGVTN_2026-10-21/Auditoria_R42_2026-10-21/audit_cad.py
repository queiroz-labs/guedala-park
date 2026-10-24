import pathlib,zipfile,xml.etree.ElementTree as E,json,hashlib
import FreeCAD as A
root=pathlib.Path(__file__).resolve().parent;base=root.parents[1]
old=base/'Modelo_FreeCAD/01_Atual/Cesto_R41_2026-10-20/Guedala_Park_R41_Estudo_Frente500.FCStd'
new=base/'Modelo_FreeCAD/01_Atual/Consolidacao_R42_2026-10-22/Guedala_Park_R42_Consolidado.FCStd'
def load(p):
 with zipfile.ZipFile(p) as z:f={n:z.read(n) for n in z.namelist()}
 d=E.fromstring(f['Document.xml']);g=E.fromstring(f['GuiDocument.xml']);return f,d,g
of,od,og=load(old);nf,nd,ng=load(new)
def objects(d):return {o.get('name'):o for o in d.find('ObjectData')}
oo,no=objects(od),objects(nd)
def props(o):return {p.get('name'):E.tostring(p,encoding='unicode') for p in o.find('Properties') if p.tag=='Property'}
def val(o,p):
 n=o.find("Properties/Property[@name='%s']"%p)
 return n[0].attrib if n is not None and len(n) else None
def refs(d,names):
 result=[]
 for o in d.find('ObjectData'):
  for prop in o.find('Properties'):
   for n in prop.iter():
    if n.tag in ['Link','LinkSub','LinkSubList'] and n.get('value') and n.get('value') not in names:result.append([o.get('name'),prop.get('name'),n.tag,n.attrib])
 return result
changes={}
for name in oo.keys()&no.keys():
 a,b=props(oo[name]),props(no[name]);delta={k:[a.get(k),b.get(k)] for k in a.keys()|b.keys() if a.get(k)!=b.get(k)}
 if delta:changes[name]=delta
removedrefs=[]
for o in no.values():
 s=E.tostring(o,encoding='unicode')
 if 'Peca108' in s or 'Peca109' in s:removedrefs.append([o.get('name'),val(o,'Label'),s])
oldvis={};newvis={}
for name,o in no.items():
 if name in ['Peca%03d'%i for i in range(91,103)] or name.startswith(('CadeiraLina','Lina1_','Lina2_','Lina3_')):
  vp=ng.find("ViewProviderData/ViewProvider[@name='%s']"%name);oldvis[name]={'label':val(o,'Label'),'app':val(o,'Visibility'),'gui':val(vp,'Visibility') if vp is not None else None}
 if name.startswith(('Aberta_','Fechada_')):
  vp=ng.find("ViewProviderData/ViewProvider[@name='%s']"%name);newvis[name]={'label':val(o,'Label'),'app':val(o,'Visibility'),'gui':val(vp,'Visibility') if vp is not None else None,'group':val(o,'Group')}
control=[]
for name,o in no.items():
 p=props(o);s=' '.join(p.values()).lower()
 if any(t in s for t in ['peca091','peca092','peca093','peca094','peca095','mesa','folha central']):control.append({'name':name,'label':val(o,'Label'),'props':p})
missingfiles=[]
for tree in [nd,ng]:
 for n in tree.iter():
  f=n.get('file')
  if f and f not in nf:missingfiles.append(f)
print('XML audit done',flush=True)
d=A.openDocument(str(new));coords={}
for o in d.Objects:
 if o.Name.startswith(('Aberta_','Fechada_')) and hasattr(o,'Shape'):
  s=o.Shape;b=s.BoundBox;coords[o.Name]={'bbox':[b.XMin,b.YMin,b.ZMin,b.XMax,b.YMax,b.ZMax],'faces':len(s.Faces),'solids':len(s.Solids),'valid':s.isValid(),'null':s.isNull()}
report={'file':str(new),'sha256':hashlib.sha256(new.read_bytes()).hexdigest(),'object_count':len(d.Objects),'removed':sorted(oo.keys()-no.keys()),'added':sorted(no.keys()-oo.keys()),'changed_properties_retained_objects':changes,'dangling_before':refs(od,set(oo)),'dangling_after':refs(nd,set(no)),'removed_names_still_in_object_xml':removedrefs,'missing_archive_files':sorted(set(missingfiles)),'old_table_chair_visibility':oldvis,'berlin_visibility':newvis,'berlin_shapes':coords,'possible_old_table_controls':control,'brep_unchanged':all(nf.get(n)==v for n,v in of.items() if n.lower().endswith(('.brp','.brep'))),'gui_objects_without_document_object':[o.get('name') for o in ng.find('ViewProviderData') if o.get('name') not in no]}
(root/'Auditoria_CAD_R42.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({k:report[k] for k in ['object_count','removed','dangling_before','dangling_after','missing_archive_files','brep_unchanged','gui_objects_without_document_object']},ensure_ascii=False),flush=True)
print('old table adjacent',json.dumps({k:v for k,v in oldvis.items() if k.startswith('Peca')},ensure_ascii=False),flush=True)
print('controls',[(x['name'],x['label']) for x in control],flush=True)
