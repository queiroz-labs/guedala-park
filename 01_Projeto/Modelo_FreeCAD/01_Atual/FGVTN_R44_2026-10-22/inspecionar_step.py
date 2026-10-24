import FreeCAD as A,Part,Import,pathlib,json,hashlib,re
p=pathlib.Path(__file__).resolve().parent;rows={}
def bb(s):
 b=s.BoundBox;return [b.XMin,b.YMin,b.ZMin,b.XMax,b.YMax,b.ZMax]
for label in ['FECHADA','ABERTA']:
 f=p/'Fontes'/('54FGOC12400TSX0_'+label+'.STEP');doc=A.newDocument('FGVTN400_'+label);Import.insert(str(f),doc.Name);doc.recompute()
 objs=[]
 for o in doc.Objects:
  r={'name':o.Name,'label':o.Label,'type':o.TypeId,'parents':[x.Name for x in o.InList],'children':[x.Name for x in o.OutList]}
  if hasattr(o,'Shape') and not o.Shape.isNull():
   s=o.Shape.copy()
   if hasattr(o,'getGlobalPlacement'):s.Placement=o.getGlobalPlacement()
   r.update({'bbox':bb(s),'solids':len(s.Solids),'volume':s.Volume,'valid':s.isValid()})
  objs.append(r)
 txt=f.read_text(encoding='latin1');products=re.findall(r"PRODUCT\s*\(\s*'([^']*)'",txt)
 rows[label]={'file':str(f),'sha256':hashlib.sha256(f.read_bytes()).hexdigest(),'products':products,'objects':objs}
 doc.saveAs(str(p/(label+'_400_IMPORTADO_INSPECAO.FCStd')))
 print(label, 'objects',len(objs),'products',products,flush=True)
 print(json.dumps([r for r in objs if 'bbox' in r],ensure_ascii=True),flush=True)
(p/'Inspecao_STEP_400.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
