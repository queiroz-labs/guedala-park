import FreeCAD as A,FreeCADGui as G,pathlib,json,hashlib
ROOT=pathlib.Path(__file__).resolve().parent
d=A.getDocument('Guedala_Park_R42_Consolidado');c=d.getObject('ControlePortaR018');a=c.Abertura.Value;limit=c.CursoEstudo.Value
def shape(o):
 q=o.Shape.copy();q.Placement=o.getGlobalPlacement();return q
front=d.getObject('FrenteComumR018');obstacle=d.getObject('Peca075');fixed=shape(obstacle);rows=[]
pose=str(front.getGlobalPlacement());sha=hashlib.sha256(pathlib.Path(d.FileName).read_bytes()).hexdigest()
def children(o):
 out=[]
 for ch in getattr(o,'Group',[]):out.append(ch);out+=children(ch)
 return out
d.openTransaction('Diagnóstico temporário banheiro')
try:
 for angle in range(40,87,2):
  c.Abertura=angle;d.recompute();q=shape(front);rows.append({'angle_deg':angle,'intersection_mm3':q.common(fixed).Volume})
 c.Abertura=60;d.recompute()
 objs=[o for o in children(d.getObject('Modulo017')) if not hasattr(o,'Group') and hasattr(o,'Shape') and not o.Shape.isNull() and o.Shape.Solids and o.Shape.Volume>300000]
 snapshots=[(o.Name,o.Label,shape(o)) for o in objs+[obstacle]]
finally:
 c.Abertura=a;c.CursoEstudo=limit;d.recompute();d.abortTransaction();d.recompute()
assert str(front.getGlobalPlacement())==pose and hashlib.sha256(pathlib.Path(d.FileName).read_bytes()).hexdigest()==sha
evidence=A.newDocument('R42_Encontro_Banheiro_ESTUDO');evidence.Label='R42 — encontro gabinete/porta; diagnóstico, não solução'
for name,label,q in snapshots:
 o=evidence.addObject('PartDesign::Feature',name);o.Label=label;o.Shape=q;o.Visibility=True
 o.ViewObject.ShapeColor=(.85,.48,.2) if name==obstacle.Name else ((.82,.15,.12) if name==front.Name else (.55,.7,.6))
 if name!=front.Name:o.ViewObject.Transparency=55
note=evidence.addObject('App::FeaturePython','Escopo');note.addProperty('App::PropertyString','Limites');note.Limites='Gabinete aberto60 graus; porta de entrada na pose salva da R42. Porta e medidas reais desconhecidas. Diagnóstico, não solução liberada.'
evidence.recompute();evidence.saveAs(str(ROOT/'R42_Encontro_Banheiro_ESTUDO.FCStd'))
(ROOT/'Banheiro_amostragem_2graus.json').write_text(json.dumps({'samples':rows,'source_unchanged':True,'pose_restored':True,'limit':'Porta de entrada fixa na pose salva, não cotada em campo. Amostragem2graus, não limite exato nem trajetória simultânea.'},indent=2,ensure_ascii=False),encoding='utf-8')
A.setActiveDocument(evidence.Name);G.activeDocument().activeView().viewTop();G.activeDocument().activeView().fitAll();G.updateGui()
