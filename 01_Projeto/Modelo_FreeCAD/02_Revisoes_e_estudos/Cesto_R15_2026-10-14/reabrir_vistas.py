from pathlib import Path
import json
import FreeCAD as App,FreeCADGui as Gui
root=(Path(__file__).resolve().parent / '.').resolve();data=json.loads(((Path(__file__).resolve().parent / 'Montagem_R15.json').resolve()).read_text(encoding='utf-8'));p=(Path(__file__).resolve().parent / 'Guedala_Park_R15_Cesto_Simples.FCStd').resolve()
d=next(d for d in App.listDocuments().values() if d.FileName and Path(d.FileName).resolve()==p)
for n in ['Peca352','Peca353','Peca354']:d.getObject(n).Visibility=True
d.getObject('Ambiente_lavanderia').Visibility=True
meta=d.getObject('Documentacao');meta.Revisao='R15 - cesto55/saco removível; correr R14 e apartamento anterior incorporados';meta.Cinematica='Cesto55 por pivô ideal, armação e pinos-gabarito. Retirada diária e manutenção são trajetos geométricos; retenção/carga/apoios/hidráulica reais pendentes. Correr R14 e rodas R13 são gabaritos; MOVENTO estático; portas R10-12 pelos eixos STEP.'
d.recompute();d.save();assert d.isSaved() and p.exists() and p.stat().st_size>100000
App.closeDocument(d.Name);d=App.openDocument(str(p));c=d.getObject(data['control']);checks=[]
c.Abertura=55;c.RetiradaSaco=445;c.EndireitarSaco=55;d.recompute()
for n in [data['driver'],data['bag_driver'],data['front'],data['bag']]:
 o=d.getObject(n);checks.append({'name':n,'placement':str(o.getGlobalPlacement()),'state':list(o.State),'valid':o.Shape.isValid() if 'Shape' in o.PropertiesList else None})
driver=d.getObject(data['driver']);bag=d.getObject(data['bag']);s=bag.Shape.copy();s.Placement=bag.getGlobalPlacement();bb=s.BoundBox
proof={'checks':checks,'driver_axis':list(driver.Placement.Rotation.Axis),'driver_angle_deg':driver.Placement.Rotation.Angle*180/3.141592653589793,'upright_bag_bbox_world_mm':[bb.XMin,bb.XMax,bb.YMin,bb.YMax,bb.ZMin,bb.ZMax]}
for field in ['Abertura','RetiradaSaco','EndireitarSaco','RetiradaPainelSuperior','RetiradaConjunto']:setattr(c,field,0)
d.recompute();d.save();proof['final_controls']={f:float(getattr(c,f)) for f in ['Abertura','RetiradaSaco','EndireitarSaco','RetiradaPainelSuperior','RetiradaConjunto']}
((Path(__file__).resolve().parent / 'Reabertura_R15.json').resolve()).write_text(json.dumps(proof,ensure_ascii=False,indent=2),encoding='utf-8')
records=[];m=d.getObject(data['module']);room=next(o for o in m.InList if o.Name=='Ambiente_lavanderia')
stone=next(o for o in room.Group if o.Label.startswith('Bancada lavanderia'))
for label,params in [('Aberto55',[55,0,0]),('SacoFora',[55,445,55])]:
 c.Abertura,c.RetiradaSaco,c.EndireitarSaco=params;d.recompute();preview=App.newDocument('Cesto'+label+'R15');preview.Label='Cesto R15 '+label+' - gabaritos, não montagem executiva'
 objects=[d.getObject(n) for n in data['moving']+data['fixed']+data['hydraulic']+[data['bag']]]+[d.getObject(n) for n in ['Peca352','Peca353','Peca354']]+[stone]
 for o in objects:
  s=o.Shape.copy();s.Placement=App.Placement(-m.Placement.Base,App.Rotation()).multiply(o.getGlobalPlacement());copy=preview.addObject('Part::Feature','PecaVistaCesto');copy.Label=o.Label;copy.Shape=s;copy.ViewObject.ShapeColor=o.ViewObject.ShapeColor
  kind=o.CategoriaR15 if 'CategoriaR15' in o.PropertiesList else ''
  if o==stone or o.Name in ['Peca352','Peca353','Peca354']:copy.ViewObject.Transparency=80
  elif kind in ['hidraulica_limite','saco_gabarito']:copy.ViewObject.Transparency=85 if kind=='hidraulica_limite' else 65
 preview.recompute();preview.saveAs(str(root/(label+'_Detalhe_R15.FCStd')));records.append({'label':label,'document':preview.Name,'file':preview.FileName})
 App.setActiveDocument(preview.Name);Gui.getDocument(preview.Name).activeView().viewAxonometric();Gui.updateGui()
for field in ['Abertura','RetiradaSaco','EndireitarSaco','RetiradaPainelSuperior','RetiradaConjunto']:setattr(c,field,0)
d.recompute();d.save();((Path(__file__).resolve().parent / 'Vistas_R15.json').resolve()).write_text(json.dumps(records,ensure_ascii=False,indent=2),encoding='utf-8');result={'reopen':proof,'views':records}
