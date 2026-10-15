from pathlib import Path
from datetime import datetime
import json,math,shutil
import FreeCAD as App,Part
root=(Path(__file__).resolve().parent / '.').resolve()
base=(Path(__file__).resolve().parent / '../Portas_R09_2026-10-14/Guedala_Park_R09_Portas_Comuns.FCStd').resolve()
prev=next(v for v in App.listDocuments().values() if v.FileName and Path(v.FileName).resolve()==base)
prev.save();dest=(Path(__file__).resolve().parent / 'Guedala_Park_R10_Dobradicas_Comuns.FCStd').resolve()
if dest.exists():dest=dest.with_stem(dest.stem+'_'+datetime.now().strftime('%Y%m%d_%H%M%S'))
shutil.copy2(base,dest);doc=App.openDocument(str(dest));App.setActiveDocument(doc.Name)
doc.Label='Guedala Park - R10 - dobradiças comuns propostas, 6 pares'
sp=(Path(__file__).resolve().parent / '../Canto_2026-10-13/Canto_simples_R04/Fontes_STEP_Simples.FCStd').resolve()
source=next(v for v in App.listDocuments().values() if v.FileName and Path(v.FileName).resolve()==sp)
parts=[source.getObject('Part__Feature'+('%03d'%i if i else '')) for i in range(5)]
plate=source.getObject('Part__Feature005')
axes=json.loads(((Path(__file__).resolve().parent / 'Eixos_71B3550.json').resolve()).read_text(encoding='utf-8'));a,b,c,d=[axes[k] for k in ['a','b','c','d']]
def circle(A,B,r1,r2,sign):
 dx,dz=B[0]-A[0],B[1]-A[1];dist=math.hypot(dx,dz);ll=(r1*r1-r2*r2+dist*dist)/(2*dist);hh=math.sqrt(r1*r1-ll*ll)
 return [A[0]+ll*dx/dist-sign*hh*dz/dist,A[1]+ll*dz/dist+sign*hh*dx/dist]
Q=[b[0]-d[0]+c[0],b[1]-d[1]+c[1]]
sign=min([-1,1],key=lambda z:math.dist(circle(a,Q,math.dist(a,c),math.dist(b,d),z),c))
def angle(p,q):return math.degrees(math.atan2(q[1]-p[1],q[0]-p[0]))
sheet=doc.addObject('Spreadsheet::Sheet','CinematicaComumR10');sheet.Label='R10 - quatro barras dos pares comuns'
controls=doc.addObject('App::DocumentObjectGroup','ControlesPortasR10');controls.Label='R10 - abrir portas comuns (Abertura em graus)'
sheet.setColumnWidth('A',330);sheet.setColumnWidth('B',420);sheet.set('A1','MONTAGEM PROPOSTA - NÃO LIBERA CORTE/COMPRA');row=3
def add(alias,label,formula):
 global row
 addr='B'+str(row);sheet.set('A'+str(row),label);sheet.set(addr,'='+formula);sheet.setAlias(addr,alias);row+=1;return addr
report=[];hardware=[];fronts=[]
for moduleName in ['Modulo004','Modulo008','Modulo009','Modulo010','Modulo011','Modulo014']:
 module=doc.getObject(moduleName);width,height=float(module.Comprimento),float(module.Altura)
 for index,g in enumerate([o for o in module.Group if hasattr(o,'Abertura')]):
  left=index==0;letter='D'+str(len(report)+1);aliases={}
  def ex(alias,f):aliases[alias]=add(letter+alias,g.Label+' '+alias,f);return aliases[alias]
  control=doc.addObject('App::FeaturePython','ControlePortaR10');controls.addObject(control);control.Label='Abrir '+module.Label+' · '+('esquerda' if left else 'direita')
  control.addProperty('App::PropertyAngle','Abertura');control.Abertura=0;control.addProperty('App::PropertyAngle','CursoEstudo');control.CursoEstudo=86
  control.addProperty('App::PropertyLength','JuntaExternaProposta');control.JuntaExternaProposta=2
  control.addProperty('App::PropertyLength','JuntaCentralProposta');control.JuntaCentralProposta=2
  g.setExpression('Abertura',control.Name+'.Abertura');g.setExpression('CursoEstudo',control.Name+'.CursoEstudo')
  theta=ex('Theta','-min('+control.Name+'.CursoEstudo,max(0 deg,'+control.Name+'.Abertura))')
  dcx,dcz=d[0]-c[0],d[1]-c[1]
  qx=ex('Qx',f'{b[0]:.16g}-cos({theta})*({dcx:.16g})+sin({theta})*({dcz:.16g})')
  qz=ex('Qz',f'{b[1]:.16g}-sin({theta})*({dcx:.16g})-cos({theta})*({dcz:.16g})')
  dist=ex('Dist',f'sqrt(({qx}-({a[0]:.16g}))^2+({qz}-({a[1]:.16g}))^2)')
  ll=ex('L',f'({math.dist(a,c)**2:.16g}-{math.dist(b,d)**2:.16g}+{dist}^2)/(2*{dist})')
  hh=ex('H',f'sqrt({math.dist(a,c)**2:.16g}-{ll}^2)')
  cx=ex('Cx',f'{a[0]:.16g}+({ll}*({qx}-({a[0]:.16g}))-({sign})*{hh}*({qz}-({a[1]:.16g})))/{dist}')
  cz=ex('Cz',f'{a[1]:.16g}+({ll}*({qz}-({a[1]:.16g}))+({sign})*{hh}*({qx}-({a[0]:.16g})))/{dist}')
  dx=ex('Dx',f'{cx}+cos({theta})*({dcx:.16g})-sin({theta})*({dcz:.16g})')
  dz=ex('Dz',f'{cz}+sin({theta})*({dcx:.16g})+cos({theta})*({dcz:.16g})')
  t2=ex('Theta2',f'atan2(sin(atan2({cz}-({a[1]:.16g}),{cx}-({a[0]:.16g}))-({angle(a,c):.16g} deg)),cos(atan2({cz}-({a[1]:.16g}),{cx}-({a[0]:.16g}))-({angle(a,c):.16g} deg)))')
  t3=ex('Theta3',f'atan2(sin(atan2({dz}-({b[1]:.16g}),{dx}-({b[0]:.16g}))-({angle(b,d):.16g} deg)),cos(atan2({dz}-({b[1]:.16g}),{dx}-({b[0]:.16g}))-({angle(b,d):.16g} deg)))')
  for i,t,p,xx,zz in [(2,t2,a,str(a[0]),str(a[1])),(3,t3,b,str(b[0]),str(b[1])),(4,theta,c,cx,cz)]:
   ex('T'+str(i)+'x',f'{xx}-cos({t})*({p[0]:.16g})+sin({t})*({p[1]:.16g})')
   ex('T'+str(i)+'z',f'{zz}-sin({t})*({p[0]:.16g})-cos({t})*({p[1]:.16g})')
  ref=lambda alias:sheet.Name+'.'+letter+alias
  mx=18 if left else width-18;myPlate=57;depthAdjustment=.5;myHinge=myPlate-depthAdjustment
  # Guia: calço37 a partir do apoio frontal20; ajuste comum0.5 dentro de -2/+3.
  # K5 + raio17.5 => centro a22.5 da borda. Calço0 e recobrimento16.
  initialX=2 if left else width-2;initialY=0
  phi=ref('Theta') if left else '-'+ref('Theta');tx=('-' if left else '')+ref('T4x');ty='-'+ref('T4z')
  g.setExpression('Placement.Base.x',f'({mx}+({tx})+({initialX-mx})*cos({phi})-({initialY-myHinge})*sin({phi}))*1 mm')
  g.setExpression('Placement.Base.y',f'({myHinge}+({ty})+({initialX-mx})*sin({phi})+({initialY-myHinge})*cos({phi}))*1 mm')
  g.setExpression('Placement.Rotation.Angle',phi)
  panel=next(o for o in g.Group if o.TypeId=='Part::Box');originalDims=[float(panel.Length),float(panel.Width),float(panel.Height)]
  panel.setExpression('Length',module.PlanilhaDimensoes.Name+'.Comprimento/2 - '+control.Name+'.JuntaCentralProposta/2 - '+control.Name+'.JuntaExternaProposta')
  tools=[];levels=[80,height-80]
  for level in levels:
   h=doc.addObject('Part::Cylinder','CanecoComumR10');g.addObject(h);h.Label='Caneco35x13 - proposta';h.Radius=17.5;h.Height=13
   h.Placement=App.Placement(App.Vector(22.5 if left else -22.5,18,level-1),App.Rotation(App.Vector(0,0,1),App.Vector(0,-1,0)));tools.append(h)
  fused=doc.addObject('Part::MultiFuse','FurosComunsR10');g.addObject(fused);fused.Shapes=tools
  front=doc.addObject('Part::Cut','FrenteComumR10');g.addObject(front);front.Base=panel;front.Tool=fused;front.Label='Frente com canecos comuns · '+g.Label;front.ViewObject.ShapeColor=panel.ViewObject.ShapeColor
  fronts.append(front)
  frame=App.Rotation(App.Vector(1,0,0),90)
  if left:frame=App.Rotation(App.Vector(0,1,0),180).multiply(frame)
  assemblies=[]
  for level in levels:
   assembly=doc.addObject('App::Part','DobradicaComumR10');module.addObject(assembly);assembly.Label='71B3550 · '+g.Label+' · z'+str(int(level));assembly.Placement=App.Placement(App.Vector(mx,myPlate,level),frame)
   adjusted=doc.addObject('App::Part','AjusteProfundidadeR10');assembly.addObject(adjusted);adjusted.Label='Regulagem comum de profundidade0.5 - proposta';adjusted.Placement.Base.z=depthAdjustment
   bodies=[]
   for i,original in enumerate(parts):
    driver=doc.addObject('App::Part','CorpoArticuladoR10');adjusted.addObject(driver);driver.Label='Corpo'+str(i)+' - '+g.Label
    if i in [2,3,4]:
     driver.Placement.Rotation.Axis=App.Vector(0,1,0);driver.setExpression('Placement.Rotation.Angle','-'+ref('Theta' if i==4 else 'Theta'+str(i)))
     driver.setExpression('Placement.Base.x',ref('T'+str(i)+'x')+'*1 mm');driver.setExpression('Placement.Base.z',ref('T'+str(i)+'z')+'*1 mm')
    obj=doc.addObject('Part::Feature','FerragemComumR10');driver.addObject(obj);obj.Label=original.Label+' · '+g.Label;obj.Shape=original.Shape.copy();obj.ViewObject.ShapeColor=(.65,.68,.72)
    obj.addProperty('App::PropertyInteger','IndiceCorpo');obj.IndiceCorpo=i;hardware.append(obj);bodies.append({'driver':driver.Name,'body':obj.Name,'index':i})
   obj=doc.addObject('Part::Feature','CalcoComumR10');assembly.addObject(obj);obj.Shape=plate.Shape.copy();obj.Label='173H7100 calço0 · '+g.Label;obj.ViewObject.ShapeColor=(.65,.68,.72);hardware.append(obj)
   assemblies.append({'group':assembly.Name,'adjustment':adjusted.Name,'bodies':bodies,'plate':obj.Name,'level':level})
  g.Movimento='Quatro barras71B3550; junta externa2, K5/calço0/recobrimento16 e regulagem comum0.5 propostos. Estudo86, batente70T3553/fixação/carga ainda a conferir.'
  report.append({'module':module.Name,'door':g.Name,'control':control.Name,'front':front.Name,'old_panel':panel.Name,'side':'left' if left else 'right','hinges':assemblies,'K_mm':5,'overlay_mm':16,'external_joint_mm':2,'plate_spacing_mm':0,'plate_hole_row_y':57,'depth_adjustment_proposed_mm':depthAdjustment,'original_panel_dimensions_R09_mm':originalDims,'front_source_dimensions':[originalDims[0]-1,originalDims[1],originalDims[2]]})
  doc.recompute()
  for o in tools+[panel,fused]:o.Visibility=False
  front.Visibility=True
doc.recompute();doc.save()
data={'file':str(dest),'doors':report,'hardware_count':len(hardware),'hinge_count':sum(len(r['hinges']) for r in report),
 'invalid_hardware':[o.Name for o in hardware if not o.Shape.isValid()],'invalid_fronts':[o.Name for o in fronts if not o.Shape.isValid()],
 'source_guide':'https://d2.blum.com/services/BEC003/clp0016-ma-679-bhk_ma_dok_bau_%24sml_%24aof_%24v2.pdf',
 'scope':'Montagem proposta com geometria oficial e quatro barras.24 dobradiças/12 folhas, fonte de quantidade C2 no cenário de referência. Regulações/fixação/peso real/batente não homologados. Não libera corte/compra.'}
((Path(__file__).resolve().parent / 'Montagem_R10.json').resolve()).write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
result=json.dumps({k:v for k,v in data.items() if k!='doors'},ensure_ascii=False)
