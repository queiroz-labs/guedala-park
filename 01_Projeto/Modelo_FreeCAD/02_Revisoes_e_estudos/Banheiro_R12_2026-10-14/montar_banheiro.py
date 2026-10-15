from pathlib import Path
from datetime import datetime
import json,math,shutil
import FreeCAD as App,Part
root=(Path(__file__).resolve().parent / '.').resolve()
base=(Path(__file__).resolve().parent / '../Apoios_R11_2026-10-14/Guedala_Park_R11_Apoios_Simples.FCStd').resolve()
prev=next(v for v in App.listDocuments().values() if v.FileName and Path(v.FileName).resolve()==base)
prev.save();dest=(Path(__file__).resolve().parent / 'Guedala_Park_R12_Banheiro_Simples.FCStd').resolve()
assert not dest.exists(),'A revisão já existe: preservar e iniciar nova pasta/revisão, sem reexecutar gerador pronto.'
shutil.copy2(base,dest);doc=App.openDocument(str(dest));App.setActiveDocument(doc.Name)
doc.Label='Guedala Park - R12 - banheiro portas comuns - proposta'
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
sheet=doc.addObject('Spreadsheet::Sheet','CinematicaComumR12');sheet.Label='R12 - quatro barras dos pares comuns'
controls=doc.addObject('App::DocumentObjectGroup','ControlesPortasR12');controls.Label='R12 - abrir portas comuns (Abertura em graus)'
sheet.setColumnWidth('A',330);sheet.setColumnWidth('B',420);sheet.set('A1','MONTAGEM PROPOSTA - NÃO LIBERA CORTE/COMPRA');row=3
def add(alias,label,formula):
 global row
 addr='B'+str(row);sheet.set('A'+str(row),label);sheet.set(addr,'='+formula);sheet.setAlias(addr,alias);row+=1;return addr
report=[];hardware=[];fronts=[]

historical=[]
for moduleName in ['Modulo017','Modulo018']:
 module=doc.getObject(moduleName);width,height=float(module.Comprimento),float(module.Altura)
 isMirror=moduleName=='Modulo018';backingOffset=4 if isMirror else 0
 old=doc.getObject('Peca405' if isMirror else 'Peca398')
 history=doc.addObject('App::Part','HistoricoFrenteBanheiroR12');module.addObject(history);history.Label='Histórico oculto - frente volumétrica anterior'
 module.removeObject(old);history.addObject(old);old.Visibility=False;history.Visibility=False;historical.append(history)
 if isMirror:
  for name in ['Peca400','Peca401','Peca403','Peca404']:
   o=doc.getObject(name);o.setExpression('Placement.Base.y','24 mm')
   o.setExpression('Width',module.PlanilhaDimensoes.Name+'.Profundidade - '+('24 mm' if name in ['Peca400','Peca401'] else '24 mm - '+module.PlanilhaDimensoes.Name+'.Fundo'))
 module.Condicoes=('R12 proposta: duas folhas MDF18 + espelho4, frente22 dentro de profundidade150; vidro/fixação/carga/torneira/tubulação pendentes.' if isMirror else 'R12 proposta: duas portas comuns, sem divisória central; sifão/pontos/fundo e fixação/carga ainda pendentes. Envelope600x420x545 preservado.')
 leaves=[]
 for i in range(2):
  g=doc.addObject('App::Part','FolhaBanheiroR12');module.addObject(g);g.Label=('Espelhado' if isMirror else 'Gabinete')+' · '+('esquerda' if i==0 else 'direita')+' - proposta'
  g.addProperty('App::PropertyAngle','Abertura');g.addProperty('App::PropertyAngle','CursoEstudo');g.CursoEstudo=86
  g.addProperty('App::PropertyString','Movimento');g.Placement.Base=App.Vector(2 if i==0 else width-2,0,1)
  panel=doc.addObject('Part::Box','PainelBanheiroR12');g.addObject(panel);panel.Label='Painel18 comum · '+g.Label
  panel.Length=width/2-3;panel.Width=18;panel.Height=height-2
  panel.Placement.Base=App.Vector(0 if i==0 else -float(panel.Length),backingOffset,0)
  panel.ViewObject.ShapeColor=(.77,.64,.46) if isMirror else old.ViewObject.ShapeColor
  panel.addProperty('App::PropertyString','Status');panel.Status='Proposta, sem liberação de corte/furação/compra'
  leaves.append(g)
 for index,g in enumerate(leaves):
  left=index==0;letter='D'+str(len(report)+1);aliases={}
  def ex(alias,f):aliases[alias]=add(letter+alias,g.Label+' '+alias,f);return aliases[alias]
  control=doc.addObject('App::FeaturePython','ControlePortaR12');controls.addObject(control);control.Label='Abrir '+module.Label+' · '+('esquerda' if left else 'direita')
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
  mx=18 if left else width-18;myPlate=57+backingOffset;depthAdjustment=.5;myHinge=myPlate-depthAdjustment
  # Guia: calço37 a partir do apoio frontal20; ajuste comum0.5 dentro de -2/+3.
  # K5 + raio17.5 => centro a22.5 da borda. Calço0 e recobrimento16.
  initialX=2 if left else width-2;initialY=0
  phi=ref('Theta') if left else '-'+ref('Theta');tx=('-' if left else '')+ref('T4x');ty='-'+ref('T4z')
  g.setExpression('Placement.Base.x',f'({mx}+({tx})+({initialX-mx})*cos({phi})-({initialY-myHinge})*sin({phi}))*1 mm')
  g.setExpression('Placement.Base.y',f'({myHinge}+({ty})+({initialX-mx})*sin({phi})+({initialY-myHinge})*cos({phi}))*1 mm')
  g.setExpression('Placement.Rotation.Angle',phi)
  panel=next(o for o in g.Group if o.TypeId=='Part::Box');originalDims=[float(panel.Length),float(panel.Width),float(panel.Height)]
  panel.setExpression('Length',module.PlanilhaDimensoes.Name+'.Comprimento/2 - '+control.Name+'.JuntaCentralProposta/2 - '+control.Name+'.JuntaExternaProposta')
  tools=[];levels=([80,height/2,height-80] if isMirror else [80,height-80]) # Scenario of composite mirrored front requires three common hinges.
  for level in levels:
   h=doc.addObject('Part::Cylinder','CanecoComumR12');g.addObject(h);h.Label='Caneco35x13 - proposta';h.Radius=17.5;h.Height=13
   h.Placement=App.Placement(App.Vector(22.5 if left else -22.5,18+backingOffset,level-1),App.Rotation(App.Vector(0,0,1),App.Vector(0,-1,0)));tools.append(h)
  fused=doc.addObject('Part::MultiFuse','FurosComunsR12');g.addObject(fused);fused.Shapes=tools
  front=doc.addObject('Part::Cut','FrenteComumR12');g.addObject(front);front.Base=panel;front.Tool=fused;front.Label='Frente com canecos comuns · '+g.Label;front.ViewObject.ShapeColor=panel.ViewObject.ShapeColor
  fronts.append(front)
  frame=App.Rotation(App.Vector(1,0,0),90)
  if left:frame=App.Rotation(App.Vector(0,1,0),180).multiply(frame)
  assemblies=[]
  for level in levels:
   assembly=doc.addObject('App::Part','DobradicaComumR12');module.addObject(assembly);assembly.Label='71B3550 · '+g.Label+' · z'+str(int(level));assembly.Placement=App.Placement(App.Vector(mx,myPlate,level),frame)
   adjusted=doc.addObject('App::Part','AjusteProfundidadeR12');assembly.addObject(adjusted);adjusted.Label='Regulagem comum de profundidade0.5 - proposta';adjusted.Placement.Base.z=depthAdjustment
   bodies=[]
   for i,original in enumerate(parts):
    driver=doc.addObject('App::Part','CorpoArticuladoR12');adjusted.addObject(driver);driver.Label='Corpo'+str(i)+' - '+g.Label
    if i in [2,3,4]:
     driver.Placement.Rotation.Axis=App.Vector(0,1,0);driver.setExpression('Placement.Rotation.Angle','-'+ref('Theta' if i==4 else 'Theta'+str(i)))
     driver.setExpression('Placement.Base.x',ref('T'+str(i)+'x')+'*1 mm');driver.setExpression('Placement.Base.z',ref('T'+str(i)+'z')+'*1 mm')
    obj=doc.addObject('Part::Feature','FerragemComumR12');driver.addObject(obj);obj.Label=original.Label+' · '+g.Label;obj.Shape=original.Shape.copy();obj.ViewObject.ShapeColor=(.65,.68,.72)
    obj.addProperty('App::PropertyInteger','IndiceCorpo');obj.IndiceCorpo=i;hardware.append(obj);bodies.append({'driver':driver.Name,'body':obj.Name,'index':i})
   obj=doc.addObject('Part::Feature','CalcoComumR12');assembly.addObject(obj);obj.Shape=plate.Shape.copy();obj.Label='173H7100 calço0 · '+g.Label;obj.ViewObject.ShapeColor=(.65,.68,.72);hardware.append(obj)
   assemblies.append({'group':assembly.Name,'adjustment':adjusted.Name,'bodies':bodies,'plate':obj.Name,'level':level})
  g.Movimento='R12 proposta: quatro barras71B3550/K5/calço0; estudo86 não é batente físico. Peso/material/fixação/hidráulica pendentes.'
  report.append({'module':module.Name,'door':g.Name,'control':control.Name,'front':front.Name,'old_panel':panel.Name,'side':'left' if left else 'right','hinges':assemblies,'K_mm':5,'overlay_mm':16,'external_joint_mm':2,'plate_spacing_mm':0,'plate_hole_row_y':myPlate,'depth_adjustment_proposed_mm':depthAdjustment,'panel_dimensions_before_canecos_mm':originalDims,'front_source_dimensions':[width/2-3,18,height-2],'backing_front_offset_mm':backingOffset})
  if isMirror:
   mirror=doc.addObject('Part::Box','EspelhoAplicadoR12');g.addObject(mirror);mirror.Label='Espelho4 sobre painel comum - proposta'
   mirror.Length=width/2-3;mirror.Width=4;mirror.Height=height-2;mirror.Placement.Base.x=0 if left else -float(mirror.Length)
   mirror.ViewObject.ShapeColor=(.72,.83,.86);report[-1]['mirror']=mirror.Name;mirror.addProperty('App::PropertyString','Status');mirror.Status='Proposta: vidro/adesivo/retenção/arestas/carga devem ser definidos com fornecedor'
  doc.recompute()
  for o in tools+[panel,fused]:o.Visibility=False
  front.Visibility=True

doc.recompute()
for o in historical:o.Visibility=False
doc.save()
data={'file':str(dest),'doors':report,'hardware_count':len(hardware),'hinge_count':sum(len(r['hinges']) for r in report),
 'invalid_hardware':[o.Name for o in hardware if not o.Shape.isValid()],'invalid_fronts':[o.Name for o in fronts if not o.Shape.isValid()],
 'scope':'R12 proposta: gabinete duas portas comuns, espelhado duas folhas madeira18 + espelho4 dentro de150. Não libera corte/vidro/adesivo/carga/fixação.'}
((Path(__file__).resolve().parent / 'Montagem_R12.json').resolve()).write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
result=json.dumps({k:v for k,v in data.items() if k!='doors'},ensure_ascii=False)
