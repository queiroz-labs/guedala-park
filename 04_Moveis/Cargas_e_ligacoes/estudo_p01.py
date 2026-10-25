"""Estudo separado: duas prateleiras723 cobrindo as divisorias existentes.
R50 somente lida; nenhuma alteracao em portas, gavetas, cursos ou fonte.
"""
from pathlib import Path
import json,hashlib
import FreeCAD as App
import FreeCADGui as Gui
import Part
HERE=Path(__file__).resolve().parent
g=json.loads((HERE/'Geometria_R50.json').read_text(encoding='utf-8'))
cad=HERE.parents[1]/g['cad']
src=next(d for d in App.listDocuments().values() if Path(d.FileName).resolve()==cad.resolve())
assert not Gui.getDocument(src.Name).Modified
assert hashlib.sha256(cad.read_bytes()).hexdigest()==g['sha256']
assert 'Estudo_P01_apoios_723' not in App.listDocuments(), 'Estudo ja aberto: preservar antes de recriar'
camera=Gui.getDocument(src.Name).activeView().getCameraOrientation()
study=App.newDocument('Estudo_P01_apoios_723')
study.Label='P01 estudo de apoios 723 mm - condicionado'
changes=[]
try:
 for name in ['Peca206','Peca207','Peca208','Peca209','Peca210','Peca241','Peca242','Peca243','Peca244']:
  original=src.getObject(name);sh=original.Shape.copy()
  sh.Placement=original.getGlobalPlacement().multiply(original.Placement.inverse()).multiply(sh.Placement)
  o=study.addObject('PartDesign::Feature','Base_'+name);o.Label=original.Label;o.Shape=sh
  o.ViewObject.ShapeColor=(.80,.79,.74);o.ViewObject.Transparency=55
  o.addProperty('App::PropertyString','Origem').Origem=name+' na R50, geometria preservada'
 for name in ['Peca245','Peca246']:
  old=g['parts'][name];bb=old['bbox_global_mm'];newbb=list(bb)
  if name=='Peca245':newbb[0]-=18
  else:newbb[3]+=18
  o=study.addObject('PartDesign::Feature','Proposta_'+name)
  o.Label=name+' - prateleira proposta 723 x 550 x 18'
  o.Shape=Part.makeBox(723,550,18,App.Vector(*newbb[:3]))
  o.ViewObject.ShapeColor=(.24,.60,.51)
  o.addProperty('App::PropertyString','Situacao').Situacao='Proposta nominal separada, sem carga liberada; juntas/fundo por comprovar'
  o.addProperty('App::PropertyString','Diferenca').Diferenca='705 -> 723: cobre18mm da divisoria que ja existia, sem mudarZ/profundidade/vano util'
  changes.append(dict(source_id=name,old_mm=bb,new_mm=newbb,length_before_mm=705,length_after_mm=723,
   thickness_unchanged_mm=18,depth_unchanged_mm=550,top_unchanged_mm=bb[5],
   extra_volume_mm3=18*550*18,nominal_mass_increment_kg_at_rho800=18*550*18*800/1e9))
 # Face horizontal real: nao aceitar simplesmente distancia zero.
 checks=[]
 for shelf,divider in [('Peca245','Peca242'),('Peca245','Peca241'),('Peca246','Peca243'),('Peca246','Peca244')]:
  a=study.getObject('Proposta_'+shelf).Shape;b=study.getObject('Base_'+divider).Shape
  za=g['parts'][shelf]['bbox_global_mm'][2]
  fs=lambda s:[f for f in s.Faces if abs(f.BoundBox.ZMin-za)<1e-6 and abs(f.BoundBox.ZMax-za)<1e-6]
  area=sum(f.common(h).Area for f in fs(a) for h in fs(b))
  assert abs(area-9900)<1e-5,(shelf,divider,area)
  checks.append(dict(shelf=shelf,divider=divider,horizontal_bearing_area_mm2=area))
 study.recompute()
 Gui.activeDocument().activeView().viewAxonometric();Gui.activeDocument().activeView().fitAll()
 Gui.activeDocument().activeView().saveImage(str(HERE/'P01_estudo_apoios_723.png'),1280,960,'White')
 study.saveAs(str(HERE/'P01_estudo_apoios_723.FCStd'))
 assert hashlib.sha256(cad.read_bytes()).hexdigest()==g['sha256']
 (HERE/'P01_estudo_diferencas.json').write_text(json.dumps(dict(changes=changes,bearing_checks=checks,source_sha256=g['sha256'],source_unchanged=True,
   scope='Estudo parcial da caixa. Portas/gavetas/ferragens omitidas somente deste estudo; integralmente preservadas na fonte R50. Furo/conector resistente nao modelados.'),indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
finally:
 App.setActiveDocument(src.Name)
 Gui.getDocument(src.Name).activeView().setCameraOrientation(camera.Q)
print(json.dumps({'study':study.FileName,'source_unchanged':True,'checks':checks}))
