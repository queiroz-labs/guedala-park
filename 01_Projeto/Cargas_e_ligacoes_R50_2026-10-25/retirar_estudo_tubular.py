"""R51: retira somente ramo oculto de alternativa cancelada; preserva R50.
Nao substitui os apoios reais da bancada por uma sustentacao nao calculada.
"""
from pathlib import Path
import json,hashlib,shutil,runpy
import FreeCAD as App
import FreeCADGui as Gui
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
source=ROOT/'01_Projeto/Otimizacao_FreeCAD_R50_2026-10-24/Guedala_Park_R50_Completo_Otimizado.FCStd'
expected='1eda9a56e7346f5e08d5b4a391a57b4407132f14a142efdef1e2e5699c4dfd69'
folder=ROOT/'01_Projeto/Revisao_sem_tubos_R51_2026-10-25'
folder.mkdir(exist_ok=True)
dest=folder/'Guedala_Park_R51_Sem_estudo_tubular.FCStd'
assert not dest.exists(), 'Nao sobrescrever revisao existente'
src=next(d for d in App.listDocuments().values() if Path(d.FileName).resolve()==source.resolve())
assert not Gui.getDocument(src.Name).Modified
assert hashlib.sha256(source.read_bytes()).hexdigest()==expected
root=src.getObject('R45_Ref_Bancada_Estrutura_R45_R02_ESTUDO')
remove=[root]+list(root.Group);names={o.Name for o in remove}
assert len(remove)==60 and all(not o.ViewObject.Visibility for o in remove)
for o in remove:
 assert not list(o.ExpressionEngine),o.Name
 for ref in o.InList:
  assert ref.Name in names or (o==root and ref.Name=='R45_Estudos'),(o.Name,ref.Name)

def snapshot(doc,excluded=set()):
 result={}
 for o in doc.Objects:
  if o.Name in excluded:continue
  r={'type':o.TypeId,'label':o.Label,'expressions':[(p,e) for p,e in o.ExpressionEngine],
     'visible':o.ViewObject.Visibility,'color':list(o.ViewObject.ShapeColor) if 'ShapeColor' in o.ViewObject.PropertiesList else None,
     'transparency':o.ViewObject.Transparency if 'Transparency' in o.ViewObject.PropertiesList else None}
  if 'Placement' in o.PropertiesList:r['placement']=list(o.Placement.toMatrix().A)
  if o.isDerivedFrom('Part::Feature') and not o.Shape.isNull():
   s=o.Shape;b=s.BoundBox
   r['geometry']=[s.Volume,s.Area,len(s.Faces),len(s.Edges),len(s.Vertexes),b.XMin,b.YMin,b.ZMin,b.XMax,b.YMax,b.ZMax]
  result[o.Name]=r
 return result
baseline=snapshot(src,names)
removed=[{'id':o.Name,'label':o.Label,'type':o.TypeId} for o in remove]
shutil.copy2(source,dest)
new=App.openDocument(str(dest))
for o in reversed(remove):new.removeObject(o.Name)
new.recompute()
new.Label='Guedala Park R51 - alternativa tubular cancelada retirada'
current=snapshot(new)
assert set(current)==set(baseline)
diff=[]
for name,r in baseline.items():
 s=current[name]
 for k,v in r.items():
  if k in ['geometry','placement']:
   if max((abs(a-b) for a,b in zip(v,s[k])),default=0)>1e-5:diff.append((name,k))
  elif v!=s[k]:diff.append((name,k))
assert not diff,diff[:30]
save=runpy.run_path(str(ROOT/'01_Projeto/Otimizacao_FreeCAD_R50_2026-10-24/serializacao_binaria.py'))['salvar_documento']
saved=save(new,dest)
assert hashlib.sha256(source.read_bytes()).hexdigest()==expected
expr=sum(len(o.ExpressionEngine) for o in new.Objects)
report=dict(source=str(source),source_sha256=expected,source_unchanged=True,
 source_objects=len(src.Objects),current_objects=len(new.Objects),removed_objects=removed,
 removed_group=root.Name,remaining_comparison_differences=diff,expressions_preserved=expr,
 nonnull_features=sum(o.isDerivedFrom('Part::Feature') and not o.Shape.isNull() for o in new.Objects),
 save=saved,meaning='Apenas estudo oculto cancelado removido. Geometria, placement, expressao, cor e visibilidade das pecas mantidas conferidas; apoios reais da bancada ainda por dimensionar. Nao e liberacao estrutural.')
(folder/'Verificacao_R51.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
Gui.activeDocument().activeView().viewAxonometric();Gui.activeDocument().activeView().fitAll()
print(json.dumps({'saved':saved,'objects':len(new.Objects),'expressions':expr,'remaining_differences':diff}))
