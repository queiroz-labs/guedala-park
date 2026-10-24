import FreeCAD as A, Part, pathlib, json
ROOT=pathlib.Path('C:/Users/Elias/Documents/PROJETOS/Guedala park')
P=ROOT/'guedala-park/01_Projeto'
OUT=ROOT/'outputs/estudo-dimensional-2026-10-23'
main=A.getDocument('Guedala_Park_R44_Consolidado')
def world(o):
 q=o.Shape.copy();q.Placement=o.getGlobalPlacement();return q
def bb(q):
 b=q.BoundBox;return [b.XMin,b.YMin,b.ZMin,b.XMax,b.YMax,b.ZMax]
def visible(o,seen=None):
 seen=set() if seen is None else seen
 if o.Name in seen:return True
 seen.add(o.Name)
 return o.ViewObject.Visibility and all(visible(p,seen) for p in o.InList if hasattr(p,'Group') and o in p.Group)
bank=[]
region=Part.makeBox(650,1900,1000,A.Vector(0,3700,0)).BoundBox
for o in main.Objects:
 if hasattr(o,'Group') or not hasattr(o,'Shape') or not hasattr(o,'getGlobalPlacement') or o.Shape.isNull() or not o.Shape.Solids or not visible(o):continue
 q=world(o)
 if q.BoundBox.intersect(region):bank.append({'name':o.Name,'label':o.Label,'bbox':bb(q),'volume':q.Volume})
(OUT/'banco_visivel.json').write_text(json.dumps(bank,ensure_ascii=False,indent=2),encoding='utf8')
result={'objects':len(bank),'names':[x['name'] for x in bank]}
