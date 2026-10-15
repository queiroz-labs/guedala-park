from pathlib import Path
from datetime import datetime
import shutil,json
import FreeCAD as App,Part

root=(Path(__file__).resolve().parent / '.').resolve()
src=(Path(__file__).resolve().parent / '../Montagem_R07_2026-10-14/Guedala_Park_R07_Montagem_G2.FCStd').resolve()
previous=next((d for d in App.listDocuments().values() if d.FileName and Path(d.FileName).resolve()==src),None)
if previous is None:previous=App.openDocument(str(src))
previous.save();dest=(Path(__file__).resolve().parent / 'Guedala_Park_R08_Gavetas_Comuns.FCStd').resolve()
if dest.exists():dest=dest.with_stem(dest.stem+'_'+datetime.now().strftime('%Y%m%d_%H%M%S'))
shutil.copy2(src,dest);doc=App.openDocument(str(dest));App.setActiveDocument(doc.Name)
doc.Label='Guedala Park - R08 - nove gavetas com montagem comum proposta'
rp=(Path(__file__).resolve().parent / '../Gavetas_R05_2026-10-13/Fontes_MOVENTO.FCStd').resolve()
raw=next((d for d in App.listDocuments().values() if d.FileName and Path(d.FileName).resolve()==rp),None)
if raw is None:raw=App.openDocument(str(rp))
template=[o for o in doc.Objects if hasattr(o,'Fonte') and o.Name.startswith('MontagemG2')]
locks=[o for o in template if o.Label.startswith(('46166126','43107713'))]
report=[];created=[]
def add(parent,label,shape,kind):
 o=doc.addObject('Part::Feature','GavetaComumR08');parent.addObject(o);o.Label=label+' - proposta R08';o.Shape=shape
 o.addProperty('App::PropertyString','CategoriaR08');o.CategoriaR08=kind
 o.addProperty('App::PropertyString','Status');o.Status='Proposta parametrizada a partir da montagem oficial G2 e STEP400/500; não é configuração individual homologada, não libera corte/compra.'
 o.ViewObject.ShapeColor=(.76,.71,.60) if kind=='wood' else (.95,.42,.08) if kind=='locking' else (.70,.72,.74)
 created.append(o);return o
def block(x,y,z,w,d,h):return Part.makeBox(w,d,h,App.Vector(x,y,z))
for g in [o for o in doc.Objects if hasattr(o,'Extensao') and o.Label not in ['Gaveta baixa','G2 · utensílios']]:
 module=next(o for o in g.InList if o.TypeId=='App::Part')
 oldwood=[o for o in g.Group if o.TypeId=='Part::Box']
 front=next(o for o in oldwood if o.Label.startswith('Frente'))
 side=next(o for o in oldwood if o.Label.startswith('Lateral'))
 fw,fh,ft=float(front.Length),float(front.Height),float(front.Width)
 lw=float(g.VaoInternoMedido);nl=float(g.NLProposto);height=float(side.Height);sb=side.Placement.Base.z
 left=(fw-lw)/2;inside=lw-42;ox=left+6;ix=left+21;depth=nl-10;fy=ft;fz=sb+12;top=fz+15;endheight=height-27
 if endheight<25.5+2.25:raise ValueError('Parede dianteira curta para a referência comum: '+g.Label)
 legacy=doc.addObject('App::Part','HistoricoGavetaR05');g.addObject(legacy);legacy.Label='Caixa anterior oculta - '+g.Label
 for o in oldwood:g.removeObject(o);legacy.addObject(o);o.Visibility=False
 legacy.Visibility=False
 fixed=doc.addObject('App::Part','GuiasComunsR08');module.addObject(fixed);fixed.Label='Guias estáticas comuns - '+g.Label
 fixed.Placement=App.Placement(App.Vector(g.Placement.Base.x,g.Placement.Base.y,g.Placement.Base.z),App.Rotation())
 fixed.addProperty('App::PropertyString','Status');fixed.Status='Perfis principais inteiros, estáticos. Não representam telescópio animável; furação executiva dos apoios pendente.'
 woods=[];movel=[];profiles=[]
 for right in [False,True]:
  x=ox+inside+15 if right else ox
  shape=block(x,fy,sb,15,depth,height)
  grooveX=x if right else x+10
  shape=shape.cut(block(grooveX,fy,fz,5,depth,15))
  woods.append(add(g,'Lateral comum '+('direita' if right else 'esquerda')+' · '+g.Label,shape,'wood'))
 floor=block(ix-5,fy,fz,inside+10,depth,15)
 for x in [ix+7,ix+inside-7]:floor=floor.cut(Part.makeCylinder(3,10,App.Vector(x,fy+depth-10,fz+11),App.Vector(0,1,0)))
 woods.append(add(g,'Fundo comum · '+g.Label,floor,'wood'))
 back=block(ix,fy+depth-15,top,inside,15,endheight)
 woods.append(add(g,'Traseira comum · '+g.Label,back,'wood'))
 head=block(ix,fy,top,inside,16,endheight)
 frontShape=block(0,0,0,fw,ft,fh)
 for x in [ix+52,ix+inside-52]:
  head=head.cut(Part.makeCylinder(2.25,16,App.Vector(x,fy,top+25.5),App.Vector(0,1,0)))
  frontShape=frontShape.cut(Part.makeCylinder(1.25,3,App.Vector(x,ft-3,top+25.5),App.Vector(0,1,0)))
 woods.append(add(g,'Dianteira comum16 · '+g.Label,head,'wood'))
 woods.append(add(g,'Frente preservada · '+g.Label,frontShape,'wood'))
 movel.extend(woods)
 for old in locks:
  s=old.Shape.copy();shift=left-17 if old.Label.startswith('46166126') else left+lw-600
  s.translate(App.Vector(shift,ft-18,sb-20));movel.append(add(g,'Trava T51.7600 · '+old.Label.split('[')[0]+' · '+g.Label,s,'locking'))
 for sideIndex in range(2):
  for partIndex in range(2):
   rawIndex=(0 if nl==400 else 4)+2*sideIndex+partIndex
   old=raw.getObject('Part__Feature'+('%03d'%rawIndex if rawIndex else ''))
   s=old.Shape.copy()
   place=App.Placement(App.Vector(left+lw*sideIndex,ft+37,sb+21.5),App.Rotation(App.Vector(1,0,0),90))
   obj=add(fixed,'MOVENTO'+str(int(nl))+' · '+old.Label+' · '+g.Label,s,'profile');obj.Placement=place.multiply(old.Shape.Placement)
   profiles.append(obj)
 for prop,ptype in [('MontagemR08','App::PropertyString'),('ProfundidadeInternaR08','App::PropertyLength')]:
  if prop not in g.PropertiesList:g.addProperty(ptype,prop,'Conferencia R08')
 g.MontagemR08='Caixa com rasgos comuns5, dianteira16, fundo15/recuo12, duas travas. Perfis oficiais400/500 estáticos; corte/carga/fixação pendentes.'
 g.ProfundidadeInternaR08=depth-31
 report.append({'drawer':g.Name,'label':g.Label,'module':module.Name,'LW':lw,'NL':nl,'front_preserved_mm':[fw,fh,ft],'box_mm':[inside+30,depth,height],
 'usable_floor_mm':[inside,depth-31],'sidebase_mm':sb,'floor_surface_mm':top,'inside_left_mm':ix,'body_front_mm':fy,'course_preserved_mm':float(g.CursoNominal),
 'wood_names':[o.Name for o in woods],'moving_names':[o.Name for o in movel],'profile_names':[o.Name for o in profiles],'fixed_part':fixed.Name,
 'notes':'Aplicação parametrizada com posição da referência oficial G2; sem escalar ferragens/furos. Parafusos dos apoios não replicados automaticamente. Configurador individual e tolerâncias pendentes.'})
doc.recompute();doc.save()
data={'file':str(dest),'changed_drawers':report,'invalid':[o.Name for o in created if not o.Shape.isValid()],
 'scope':'Oito caixas padronizadas; G2 R07 preservada. Novas caixas propostas pela referência comum, não STEP configurado individual. Frentes/cursos/implantações preservados.'}
((Path(__file__).resolve().parent / 'Padronizacao_R08.json').resolve()).write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
result=json.dumps({'file':str(dest),'drawers':[{k:v for k,v in r.items() if not k.endswith('names')} for r in report],'invalid':data['invalid']},ensure_ascii=False)
