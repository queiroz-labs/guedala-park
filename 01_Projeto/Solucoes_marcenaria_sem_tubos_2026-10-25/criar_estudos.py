"""Estudos parciais separados P15/P04. Sem tubos, sem editar R51.
Marcadores sao pontos de interface; nao representam furo ou ferragem liberados.
"""
from pathlib import Path
import json,hashlib,csv
import FreeCAD as App,FreeCADGui as Gui,Part
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
cad=ROOT/'01_Projeto/Revisao_sem_tubos_R51_2026-10-25/Guedala_Park_R51_Sem_estudo_tubular.FCStd'
expected='ab5323bb12f8eca40b25bdfe4eadc8a3221c82b0646f354cd1f2832acfb27c16'
assert hashlib.sha256(cad.read_bytes()).hexdigest()==expected
assert 'Marcenaria_sem_tubos_P15_P04' not in App.listDocuments()
doc=App.newDocument('Marcenaria_sem_tubos_P15_P04')
doc.Label='P15 e P04 - estudos de marcenaria sem tubos, condicionais'
wood=(.72,.69,.61);green=(.25,.62,.51);gold=(.88,.68,.30)
rows=[];checks=[]

def box(group,name,label,dim,pos,color=wood,alpha=35):
 o=doc.addObject('PartDesign::Feature',name);o.Label=label;o.Shape=Part.makeBox(*dim,App.Vector(*pos));group.addObject(o)
 o.ViewObject.ShapeColor=color;o.ViewObject.Transparency=alpha
 o.addProperty('App::PropertyString','Situacao').Situacao='ESTUDO nominal; materiais, juntas, composicao e fabricacao condicionados'
 return o
def mark(group,code,piece,kind,point,direction,role):
 o=doc.addObject('PartDesign::Feature',code);o.Label=code+' - eixo/interface nominal, nao CNC'
 o.Shape=Part.makeSphere(2.,App.Vector(*point));group.addObject(o);o.ViewObject.ShapeColor=(.8,.16,.12)
 rows.append(dict(id=code,piece=piece,family_proposed=kind,X_mm=point[0],Y_mm=point[1],Z_mm=point[2],
  axis=direction,role=role,datum='Coordenadas do estudo: P15 datum na frente/esquerda da base original; P04 normalizado e deslocado+1200 emX para exibicao; nao sao coordenadas globais R51',status='Ponto nominal no estudo, nao centro completo de operacao. Confirmar broca, cabeca, acesso e produto. Nao somar aos mapas anteriores sem reconciliar.'))
def contact(a,b,axis,plane,expected_area):
 def faces(s):
  out=[]
  for f in s.Faces:
   bb=f.BoundBox;lo=[bb.XMin,bb.YMin,bb.ZMin];hi=[bb.XMax,bb.YMax,bb.ZMax]
   if abs(hi[axis]-lo[axis])<1e-6 and abs(lo[axis]-plane)<1e-6:out.append(f)
  return out
 area=sum(f.common(g).Area for f in faces(a.Shape) for g in faces(b.Shape))
 assert abs(area-expected_area)<1e-4,(a.Name,b.Name,area)
 checks.append(dict(a=a.Name,b=b.Name,area_mm2=area,normal_axis=axis))

# P15 normalizado: datum na frente/esquerda da base original, Z0 inferior original.
p15=doc.addObject('App::DocumentObjectGroup','P15');p15.Label='P15 estudo - base composta36, lado inferior18 abaixo do atual'
markers=doc.addObject('App::DocumentObjectGroup','P15_Eixos');p15.addObject(markers)
s1=box(p15,'P15_lateral_E','Peca360: lateral18, altura598 proposta',(18,330,598),(-18,0,-18))
s2=box(p15,'P15_lateral_D','Peca359: lateral18, altura598 proposta',(18,330,598),(799,0,-18))
upper=box(p15,'P15_base_superior','Peca362: camada superior18, topoZ18 preservado',(799,312,18),(0,0,0),green,0)
lower=box(p15,'P15_base_inferior','Camada18 adicional: acao composta exige processo/ensaio',(799,312,18),(0,0,-18),(.18,.45,.37),0)
back=box(p15,'P15_fundo','Peca361: fundo18 com altura598 proposta',(799,18,598),(0,312,-18),gold,30)
top=box(p15,'P15_tampo','Peca363: tampo original18',(799,312,18),(0,0,562))
contact(upper,back,1,312,799*18);contact(lower,back,1,312,799*18);contact(top,back,1,312,799*18)
contact(upper,lower,2,0,799*312)
for k,x in enumerate([72,203,334,465,596,727],1):
 for label,z in [('base',9),('tampo',571)]:mark(markers,f'P15_R_{label}_{k}','base/fundo' if label=='base' else 'tampo/fundo','Confirmat7x50 proposto',(x,321,z),'Y','ligacao traseira com face positiva')
for x,side in [(0,'E'),(799,'D')]:
 for k,z in enumerate([54,281,508],1):mark(markers,f'P15_FL_{side}_{k}','fundo/lateral','Confirmat7x50 proposto',(x,321,z),'X','grupo completo exige rigidez/resistencia propria')
 for k,y in enumerate([60,252],1):mark(markers,f'P15_MF_{side}_{k}','base/lateral','Minifix existente, reconciliar',(x,y,9),'X','quatro conjuntos da base dentro dos oito da caixa; acesso pela face superior a compatibilizar')
markers.ViewObject.Visibility=False
doc.recompute();Gui.activeDocument().activeView().viewAxonometric();Gui.activeDocument().activeView().fitAll()
Gui.activeDocument().activeView().saveImage(str(HERE/'P15_estudo_sem_tubos.png'),1280,960,'White')

# P04 isolado no mesmo documento, deslocado1200 apenas para comparar visualmente.
dx=1200.;p15.ViewObject.Visibility=False
p04=doc.addObject('App::DocumentObjectGroup','P04');p04.Label='P04 estudo - fundo inteiro e unioes positivas das divisorias'
pm=doc.addObject('App::DocumentObjectGroup','P04_Eixos');p04.addObject(pm)
ba=box(p04,'P04_base','Peca269: base18 preservada',(1764,212,18),(dx,0,0),green,0)
to=box(p04,'P04_tampo','Peca270: tampo18 preservado',(1764,212,18),(dx,0,290))
fu=box(p04,'P04_fundo','Peca268: fundo18 com altura308 proposta',(1764,18,308),(dx,212,0),gold,30)
box(p04,'P04_lateral_E','Lateral esquerda18 preservada',(18,230,308),(dx-18,0,0))
box(p04,'P04_lateral_D','Lateral direita18 preservada',(18,230,308),(dx+1764,0,0))
for j,x in enumerate([16,885.5,903.5,1329.25],1):
 di=box(p04,f'P04_divisoria_{j}','Divisoria18 existente preservada',(18,212,272),(dx+x-9,0,18))
 contact(di,ba,2,18,18*212);contact(di,fu,1,212,18*272)
 for k,y in enumerate([72,140],1):
  for level,z in [('base',0),('tampo',308)]:mark(pm,f'P04_D{j}_{level}_{k}','base/divisoria' if level=='base' else 'tampo/divisoria','Confirmat7x50 proposto',(dx+x,y,z),'Z+ / Z- conforme face','grupo em tracao; acesso inferior/superior. Cabeça e acabamento por conferir')
 for k,z in enumerate([88,154,220],1):mark(pm,f'P04_D{j}_fundo_{k}','divisoria/fundo','Confirmat7x50 proposto',(dx+x,221,z),'Y','entrada na aresta da divisoria, extremidades a70mm dos cantos')
for k in range(12):
 x=72+k*(1764-144)/11
 for label,z in [('base',9),('tampo',299)]:mark(pm,f'P04_R_{label}_{k+1}','base/fundo' if label=='base' else 'tampo/fundo','Confirmat7x50 proposto',(dx+x,221,z),'Y','face positiva; malha nominal sob estudo')
contact(ba,fu,1,212,1764*18);contact(to,fu,1,212,1764*18)
pm.ViewObject.Visibility=False
doc.recompute();Gui.activeDocument().activeView().viewAxonometric();Gui.activeDocument().activeView().fitAll()
Gui.activeDocument().activeView().saveImage(str(HERE/'P04_estudo_sem_tubos.png'),1280,960,'White')
p15.ViewObject.Visibility=True
Gui.activeDocument().activeView().fitAll()
doc.saveAs(str(HERE/'P15_P04_estudos_sem_tubos.FCStd'))
with (HERE/'Eixos_ligacoes_estudo.csv').open('w',newline='',encoding='utf-8-sig') as f:
 w=csv.DictWriter(f,list(rows[0]),delimiter=';');w.writeheader();w.writerows(rows)
assert hashlib.sha256(cad.read_bytes()).hexdigest()==expected
(HERE/'Conferencia_geometrica.json').write_text(json.dumps(dict(checks=checks,nominal_joint_points=len(rows),source_R51_unchanged=True,
 scope='Estudos parciais normalizados, sem portas/ferragens. Contato nominal nao comprova ligacao. P15 baixa18 externo e requer base composta; P04 preserva dimensoes externas e internas.'),indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
App.setActiveDocument(next(d.Name for d in App.listDocuments().values() if Path(d.FileName).resolve()==cad.resolve()))
print(json.dumps({'study':doc.FileName,'contacts':len(checks),'nominal_axes':len(rows),'source_unchanged':True}))
