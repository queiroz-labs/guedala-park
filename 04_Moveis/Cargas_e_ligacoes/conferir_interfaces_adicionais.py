"""BREP local das interfaces prioritarias fora da amostra146. Somente leitura."""
from pathlib import Path
import json,hashlib
import FreeCAD as App
import FreeCADGui as Gui
HERE=Path(__file__).resolve().parent
g=json.loads((HERE/'Geometria_R50.json').read_text(encoding='utf-8'))
cad=HERE.parents[1]/g['cad']
doc=next(d for d in App.listDocuments().values() if Path(d.FileName).resolve()==cad.resolve())
assert not Gui.getDocument(doc.Name).Modified
def bbox(s):
 b=s.BoundBox;return [b.XMin,b.YMin,b.ZMin,b.XMax,b.YMax,b.ZMax]
def world(n):
 o=doc.getObject(n);s=o.Shape.copy();s.Placement=o.getGlobalPlacement().multiply(o.Placement.inverse()).multiply(s.Placement);return s
pairs=[('Peca245','Peca242'),('Peca245','Peca241'),('Peca245','Peca206'),('Peca245','Peca208'),
       ('Peca246','Peca243'),('Peca246','Peca244'),('Peca246','Peca207')]
pairs += [(a,b) for a in ['PlacaL','PlacaL001'] for b in ['Peca255','Peca256','LateralApoioPrincipal']]
pairs += [('Peca255','Peca256')]
pairs += [(a,b) for a in ['BancoR43_Painel1','BancoR43_Painel2'] for b in ['Peca407','Peca408','PecaBancoR16','PecaBancoR003','PecaBancoR004','PecaBancoR005']]
rows=[];tol=1e-5
for a,b in pairs:
 sa,sb=world(a),world(b);ba,bb=bbox(sa),bbox(sb)
 overlap=[min(ba[i+3],bb[i+3])-max(ba[i],bb[i]) for i in range(3)]
 axes=[i for i in range(3) if abs(overlap[i])<tol and all(overlap[j]>tol for j in range(3) if j!=i)]
 area=0.
 for i in axes:
  plane=max(ba[i],bb[i])
  fa=[f for f in sa.Faces if abs(bbox(f)[i+3]-bbox(f)[i])<tol and abs(bbox(f)[i]-plane)<tol]
  fb=[f for f in sb.Faces if abs(bbox(f)[i+3]-bbox(f)[i])<tol and abs(bbox(f)[i]-plane)<tol]
  area+=sum(x.common(y).Area for x in fa for y in fb)
 distance=sa.distToShape(sb)[0]
 rows.append(dict(a=a,b=b,overlap_mm=overlap,common_face_area_mm2=area,distance_mm=distance,
  state='face' if area>tol else 'aresta/ponto' if distance<tol else 'separados',
  note='Contato geometrico nao comprova fixacao/capacidade; carga so percorre apoio com contato e direcao compativeis.'))
assert hashlib.sha256(cad.read_bytes()).hexdigest()==g['sha256']
(HERE/'Interfaces_adicionais_BREP.json').write_text(json.dumps(dict(cad_sha256=g['sha256'],pairs=rows,count=len(rows),CAD_unchanged=True),indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
print(json.dumps({'checked':len(rows),'faces':sum(r['state']=='face' for r in rows)}))
