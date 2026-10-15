from pathlib import Path
import json,shutil
import FreeCAD as App, Part
root=(Path(__file__).resolve().parent / '.').resolve()
base=(Path(__file__).resolve().parent / '../Banheiro_R12_2026-10-14/Guedala_Park_R12_Banheiro_Simples.FCStd').resolve()
dest=(Path(__file__).resolve().parent / 'Guedala_Park_R13_Gaveta_Rodas.FCStd').resolve()
assert not dest.exists(),'Revisão existente: não reconstruir trabalho pronto'
prev=next(d for d in App.listDocuments().values() if d.FileName and Path(d.FileName).resolve()==base)
prev.save();shutil.copy2(base,dest);doc=App.openDocument(str(dest));App.setActiveDocument(doc.Name)
doc.Label='Guedala Park - R13 - gaveta baixa sobre rodas, proposta'
m=doc.getObject('Modulo007');g=doc.getObject('Gaveta007');g.Extensao=0
legacy=doc.addObject('App::Part','HistoricoCaixaBaixaR13');g.addObject(legacy);legacy.Label='Histórico oculto - caixa hipotética anterior'
original=[]
for o in list(g.Group):
 if o.TypeId=='Part::Box':
  original.append({'name':o.Name,'label':o.Label,'position_mm':list(o.Placement.Base),'dimensions_mm':[float(o.Length),float(o.Width),float(o.Height)]})
  g.removeObject(o);legacy.addObject(o);o.Visibility=False
legacy.Visibility=False
made=[];wood=[];program=[];wheels=[];fixed=[]
def feature(parent,label,shape,kind,color):
 o=doc.addObject('Part::Feature','PecaBaixaR13');parent.addObject(o);o.Label=label;o.Shape=shape
 o.addProperty('App::PropertyString','CategoriaR13');o.CategoriaR13=kind
 o.addProperty('App::PropertyString','Status');o.Status='Proposta/gabarito. Material, fixação, carga e medidas acabadas pendentes; não libera corte/compra.'
 o.ViewObject.ShapeColor=color;made.append(o);return o
def box(parent,label,x,y,z,w,d,h,kind='wood',color=(.76,.71,.60)):
 return feature(parent,label,Part.makeBox(w,d,h,App.Vector(x,y,z)),kind,color)
# Local g origin z39: same current front106/upper145. Board18 and wheel total39 from decision R02.
wood.append(box(g,'Frente baixa preservada1223x106 - recuo80',0,0,0,1223,18,106))
wood.append(box(g,'Fundo18 sobre rodas - proposta',0,18,0,1223,442,18))
for x in [0,1205]:wood.append(box(g,'Lateral18 baixa - proposta',x,36,18,18,406,88))
for y in [18,442]:wood.append(box(g,'Parede frente/trás18 baixa - proposta',0,y,18,1223,18,88))
# Simplified caster: source dimensions30/39/40x21/width13.5 and three mounting holes.
# Axle offset and bracket shape/thickness are conservative hypotheses, not exact manufacturer CAD.
for row,y in enumerate([58,398],1):
 for col,x in enumerate([50,611.5,1173],1):
  a=doc.addObject('App::Part','RodizioGabaritoR13');g.addObject(a);a.Label='Rodízio fixo30/altura39 - gabarito '+str(row)+'/'+str(col)
  a.Placement.Base=App.Vector(x,y,-39)
  plate=Part.makeBox(21,40,2,App.Vector(-10.5,0,37))
  for hy,radius in [(15,3.25),(23,2),(33,2)]:plate=plate.cut(Part.makeCylinder(radius,2,App.Vector(0,hy,37)))
  objects=[feature(a,'Chapa40x21 - furos de referência, espessura2 hipótese',plate,'wheel_bracket',(.65,.68,.72))]
  for fx in [-10.5,8.5]:
   fork=Part.makeBox(2,12,22,App.Vector(fx,-6,15)).cut(Part.makeCylinder(2,2,App.Vector(fx,0,15),App.Vector(1,0,0)))
   objects.append(feature(a,'Garfo simplificado - NÃO desenho executivo',fork,'wheel_bracket',(.65,.68,.72)))
  axle=Part.makeCylinder(2,25,App.Vector(-12.5,0,15),App.Vector(1,0,0))
  objects.append(feature(a,'Eixo simplificado - hipótese',axle,'wheel_axle',(.65,.68,.72)))
  wheel=Part.makeCylinder(15,13.5,App.Vector(-6.75,0,15),App.Vector(1,0,0)).cut(Part.makeCylinder(2,13.5,App.Vector(-6.75,0,15),App.Vector(1,0,0)))
  objects.append(feature(a,'Roda30 - material silicone exigido, NÃO confirmado',wheel,'wheel_tread',(.70,.84,.88)))
  wheels.append({'assembly':a.Name,'base_local_mm':list(a.Placement.Base),'parts':[o.Name for o in objects]})
# Overall1269 = posts36 + guides/gaps10 + outer box1223. Posts are geometric reserves, not a calculated supporting frame.
for x in [-23,1228]:fixed.append(box(m,'Reserva apoio lateral18 dos gabinetes - estrutura NÃO calculada',x,0,0,18,530,180,'structure_reserve',(.82,.68,.43)))
for x in [-5,1225]:fixed.append(box(m,'Guia lateral simples3 + corrida2 - proposta sem apoio vertical',x,36,85,3,406,30,'guide_proposal',(.55,.61,.56)))
# Program from accepted detached-head arrangement: immutable length1125, no telescopic or cut sticks.
for name,x,y,w,d,h in [('Cabo fixo1 - referência1125',31,30,1125,21,21),('Cabo fixo2 - referência1125',31,65,1125,21,21),('Cabeça vassoura retirada - referência315x190x65',50,140,315,190,65),('Cabeça rodo retirada - referência325x95x35',430,170,325,95,35)]:
 program.append(box(g,name,18+x,36+y,18,w,d,h,'program_reference',(.43,.61,.42)))
m.PlanilhaDimensoes.set('B3','460 mm') # rolling assembly incl applied front18 + body442; former box reached467 despite declared442.
m.Label='Gaveta baixa de limpeza - rodas R13 - proposta'
m.Condicoes='R13 preserva rodas de silicone/cabos fixos/cabeças retiradas, recuo80/base180. Caixa externa1223x442, interna1187x406x88, fundo18 e gabarito roda39. Trecho total1269. Estrutura independente/material/carga/guia/batente/retirada pendentes.'
for name,typ,value in [('NLProposto','App::PropertyString','Não se aplica a caixa sobre rodas; não usar400/442 como NL de corrediça'),('AlturaUtilR13','App::PropertyLength',88),('LarguraUtilR13','App::PropertyLength',1187),('ProfundidadeUtilR13','App::PropertyLength',406),('ExtracaoCompletaEstudo','App::PropertyLength',530),('MontagemR13','App::PropertyString','Rodas fixas em gabarito, sem corrediça vertical. CursoNominal400 herdado é somente posição de estudo; retirável para limpeza, guia/batente físico pendentes.')]:
 if name not in g.PropertiesList:g.addProperty(typ,name,'Conferência R13')
 setattr(g,name,value)
g.addProperty('App::PropertyString','StatusR13');g.StatusR13='Translação ideal das peças, não rolagem física/piso/carga certificada. Não liberar corte ou rodízios sem confirmar silicone/carga.'
doc.recompute();legacy.Visibility=False;doc.save()
report={'file':str(dest),'drawer':g.Name,'module':m.Name,'original_box':original,
 'front_preserved_mm':[1223,18,106],'body_outer_mm':[1223,442,106],'usable_mm':[1187,406,88],
 'floor_bottom_global_z_mm':39,'floor_surface_global_z_mm':57,'rim_global_z_mm':145,'upper_cabinet_start_global_z_mm':180,
 'foot_recess_from_main_front_mm':80,'rear_margin_to_reference_wall_mm':70,'wheels':wheels,
 'wood_names':[o.Name for o in wood],'program_names':[o.Name for o in program],'fixed_names':[o.Name for o in fixed],
 'moving_names':[o.Name for o in wood+program]+[n for r in wheels for n in r['parts']],
 'rolling_assembly_depth_mm':460,'course_nominal_preserved_mm':float(g.CursoNominal),'complete_withdrawal_study_mm':530,
 'invalid_individuals':[o.Name for o in made if not o.Shape.isValid()],
 'scope':'R13 caixa sobre rodas aprovada como função, cotas/gabaritos propostos pela R02. Caster bracket/axle offset/thickness not manufacturer STEP;39/30/40/21/13.5 and mounting holes from drawing. Silicone/capacity not primary-confirmed. Guides/posts are proposals, structure not calculated.'}
((Path(__file__).resolve().parent / 'Montagem_R13.json').resolve()).write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
result=json.dumps({k:v for k,v in report.items() if k not in ['original_box','wheels','wood_names','program_names','fixed_names','moving_names']},ensure_ascii=False)
