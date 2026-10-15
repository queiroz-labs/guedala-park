from pathlib import Path
from datetime import datetime
import json,math,shutil
import FreeCAD as App,Part
root=(Path(__file__).resolve().parent / '.').resolve()
base=(Path(__file__).resolve().parent / '../Dobradicas_R10_2026-10-14/Guedala_Park_R10_Dobradicas_Comuns.FCStd').resolve()
prev=next(v for v in App.listDocuments().values() if v.FileName and Path(v.FileName).resolve()==base)
prev.save();dest=(Path(__file__).resolve().parent / 'Guedala_Park_R11_Apoios_Simples.FCStd').resolve()
if dest.exists():dest=dest.with_stem(dest.stem+'_'+datetime.now().strftime('%Y%m%d_%H%M%S'))
shutil.copy2(base,dest);doc=App.openDocument(str(dest));App.setActiveDocument(doc.Name)
doc.Label='Guedala Park - R11 - apoios simples escritório/cabeceira - proposta'
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
sheet=doc.addObject('Spreadsheet::Sheet','CinematicaComumR11');sheet.Label='R11 - quatro barras escritório/cabeceira'
controls=doc.addObject('App::DocumentObjectGroup','ControlesPortasR11');controls.Label='R11 - abrir portas comuns (Abertura em graus)'
sheet.setColumnWidth('A',330);sheet.setColumnWidth('B',420);sheet.set('A1','MONTAGEM PROPOSTA - NÃO LIBERA CORTE/COMPRA');row=3
def add(alias,label,formula):
 global row
 addr='B'+str(row);sheet.set('A'+str(row),label);sheet.set(addr,'='+formula);sheet.setAlias(addr,alias);row+=1;return addr
report=[];hardware=[];fronts=[]

supports=[]; configurations=[]; old_office=[]
def support(module,x,label):
 o=doc.addObject('Part::Box','ApoioComumR11');module.addObject(o);o.Label=label+' - proposta18'
 o.Length=18;o.Width=float(module.Profundidade)-38;o.Height=float(module.Altura)-36
 o.Placement.Base=App.Vector(x,20,18);o.ViewObject.ShapeColor=(.86,.86,.81)
 o.addProperty('App::PropertyString','Status');o.Status='Proposta: fixação, material/carga e tolerâncias pendentes'
 supports.append(o);return o
office=doc.getObject('Modulo016')
office.Condicoes='Envelope2000x350x550 preservado. Proposta R11 quatro portas comuns, três apoios18; quantidade/divisões/fixação/carga não liberadas.'
history=doc.addObject('App::Part','HistoricoFrentesEscritorioR11');office.addObject(history);history.Label='Histórico oculto - cinco folhas ilustrativas anteriores'
for g in list(office.Group):
 if hasattr(g,'Abertura'):
  g.setExpression('Abertura','0 deg');office.removeObject(g);history.addObject(g);g.Visibility=False;old_office.append(g.Name)
history.Visibility=False
for i in range(1,4):support(office,500*i,'Apoio interno escritório '+str(i))
for i in range(4):
 g=doc.addObject('App::Part','FolhaEscritorioR11');office.addObject(g);g.Label='Escritório porta '+str(i+1)+' - proposta'
 g.addProperty('App::PropertyAngle','Abertura');g.addProperty('App::PropertyAngle','CursoEstudo');g.CursoEstudo=86
 g.addProperty('App::PropertyString','Movimento');g.Placement.Base=App.Vector(2+i*500,0,1)
 p=doc.addObject('Part::Box','PainelEscritorioR11');g.addObject(p);p.Label='Frente escritório '+str(i+1)+' - proposta'
 p.Length=496;p.Width=18;p.Height=548;p.ViewObject.ShapeColor=(.86,.86,.81)
 configurations.append((office,g,2+i*500,496))
head=doc.getObject('Modulo003')
head.Condicoes='Envelope1800x250x308 preservado. Três folhas comuns R11 com dois apoios18; vizinha/canto R04 e faixa25 recuada40 preservados. Proposta, sem fabricação.'
corner=doc.getObject('Modulo001');corner.Label='Canto integrado em L - R04 simples - proposta'
corner.Condicoes='Proposta R04: duas portas independentes271x306, faixas fixas142/124, vizinha e faixa25 recuada40. Fixação/carga/batente/cotas executivas pendentes.'
for i,n in enumerate(['Folha','Folha001','Folha002']):
 g=doc.getObject(n);g.setExpression('Abertura',None);g.Abertura=0
 x=2+i*443.75
 if i:support(head,x-2,'Apoio interno cabeceira '+str(i))
 configurations.append((head,g,x,440.75))
doc.recompute()
for module,g,initialX,frontWidth in configurations:
 width,height=float(module.Comprimento),float(module.Altura)
 left=True;letter='D'+str(len(report)+1);aliases={}
 def ex(alias,f):aliases[alias]=add(letter+alias,g.Label+' '+alias,f);return aliases[alias]
 control=doc.addObject('App::FeaturePython','ControlePortaR11');controls.addObject(control);control.Label='Abrir '+module.Label+' · '+g.Label
 control.addProperty('App::PropertyAngle','Abertura');control.Abertura=0;control.addProperty('App::PropertyAngle','CursoEstudo');control.CursoEstudo=86
 leftGap=2 if len(report) in [0,4] else (4 if module.Name=='Modulo016' else 3)
 rightGap=2 if len(report) in [3,6] else (4 if module.Name=='Modulo016' else 3)
 for name,value in [('JuntaEsquerdaProposta',leftGap),('JuntaDireitaProposta',rightGap)]:
  control.addProperty('App::PropertyLength',name);setattr(control,name,value);control.setEditorMode(name,1)

 if 'CursoEstudo' not in g.PropertiesList:g.addProperty('App::PropertyAngle','CursoEstudo')
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
 mx=initialX+16;myPlate=57;depthAdjustment=.5;myHinge=myPlate-depthAdjustment
 # Guia: calço37 a partir do apoio frontal20; ajuste comum0.5 dentro de -2/+3.
 # K5 + raio17.5 => centro a22.5 da borda. Calço0 e recobrimento16.
 initialY=0
 phi=ref('Theta') if left else '-'+ref('Theta');tx=('-' if left else '')+ref('T4x');ty='-'+ref('T4z')
 g.setExpression('Placement.Base.x',f'({mx}+({tx})+({initialX-mx})*cos({phi})-({initialY-myHinge})*sin({phi}))*1 mm')
 g.setExpression('Placement.Base.y',f'({myHinge}+({ty})+({initialX-mx})*sin({phi})+({initialY-myHinge})*cos({phi}))*1 mm')
 g.setExpression('Placement.Rotation.Angle',phi)
 panel=next(o for o in g.Group if o.TypeId=='Part::Box');originalDims=[float(panel.Length),float(panel.Width),float(panel.Height)]
 panel.setExpression('Length',None);panel.Length=frontWidth
 tools=[];levels=[80,height-80]
 for level in levels:
  h=doc.addObject('Part::Cylinder','CanecoComumR11');g.addObject(h);h.Label='Caneco35x13 - proposta';h.Radius=17.5;h.Height=13
  h.Placement=App.Placement(App.Vector(22.5 if left else -22.5,18,level-1),App.Rotation(App.Vector(0,0,1),App.Vector(0,-1,0)));tools.append(h)
 fused=doc.addObject('Part::MultiFuse','FurosComunsR11');g.addObject(fused);fused.Shapes=tools
 front=doc.addObject('Part::Cut','FrenteComumR11');g.addObject(front);front.Base=panel;front.Tool=fused;front.Label='Frente com canecos comuns · '+g.Label;front.ViewObject.ShapeColor=panel.ViewObject.ShapeColor
 fronts.append(front)
 frame=App.Rotation(App.Vector(1,0,0),90)
 if left:frame=App.Rotation(App.Vector(0,1,0),180).multiply(frame)
 assemblies=[]
 for level in levels:
  assembly=doc.addObject('App::Part','DobradicaComumR11');module.addObject(assembly);assembly.Label='71B3550 · '+g.Label+' · z'+str(int(level));assembly.Placement=App.Placement(App.Vector(mx,myPlate,level),frame)
  adjusted=doc.addObject('App::Part','AjusteProfundidadeR11');assembly.addObject(adjusted);adjusted.Label='Regulagem comum de profundidade0.5 - proposta';adjusted.Placement.Base.z=depthAdjustment
  bodies=[]
  for i,original in enumerate(parts):
   driver=doc.addObject('App::Part','CorpoArticuladoR11');adjusted.addObject(driver);driver.Label='Corpo'+str(i)+' - '+g.Label
   if i in [2,3,4]:
    driver.Placement.Rotation.Axis=App.Vector(0,1,0);driver.setExpression('Placement.Rotation.Angle','-'+ref('Theta' if i==4 else 'Theta'+str(i)))
    driver.setExpression('Placement.Base.x',ref('T'+str(i)+'x')+'*1 mm');driver.setExpression('Placement.Base.z',ref('T'+str(i)+'z')+'*1 mm')
   obj=doc.addObject('Part::Feature','FerragemComumR11');driver.addObject(obj);obj.Label=original.Label+' · '+g.Label;obj.Shape=original.Shape.copy();obj.ViewObject.ShapeColor=(.65,.68,.72)
   obj.addProperty('App::PropertyInteger','IndiceCorpo');obj.IndiceCorpo=i;hardware.append(obj);bodies.append({'driver':driver.Name,'body':obj.Name,'index':i})
  obj=doc.addObject('Part::Feature','CalcoComumR11');assembly.addObject(obj);obj.Shape=plate.Shape.copy();obj.Label='173H7100 calço0 · '+g.Label;obj.ViewObject.ShapeColor=(.65,.68,.72);hardware.append(obj)
  assemblies.append({'group':assembly.Name,'adjustment':adjusted.Name,'bodies':bodies,'plate':obj.Name,'level':level})
 g.Movimento='Proposta R11: 71B3550/calço0/K5/recobrimento16; regulagem0.5; limites86 não comprovam batente. Após mudar dimensões, revisar apoios/canecos e montagem.'
 report.append({'module':module.Name,'door':g.Name,'control':control.Name,'front':front.Name,'old_panel':panel.Name,'side':'left' if left else 'right','hinges':assemblies,'K_mm':5,'overlay_mm':16,'left_joint_mm':leftGap,'right_joint_mm':rightGap,'plate_spacing_mm':0,'plate_hole_row_y':57,'depth_adjustment_proposed_mm':depthAdjustment,'panel_dimensions_before_canecos_mm':originalDims,'front_source_dimensions':[frontWidth,originalDims[1],originalDims[2]],'hinge_support_inner_x_mm':mx,'closed_x_mm':initialX})
 doc.recompute()
 for o in tools+[panel,fused]:o.Visibility=False
 front.Visibility=True
doc.recompute()
history.Visibility=False
doc.save()
data={'file':str(dest),'doors':report,'hardware_count':len(hardware),'hinge_count':sum(len(r['hinges']) for r in report),
 'supports':[{'name':o.Name,'label':o.Label,'dimensions_mm':[float(o.Length),float(o.Width),float(o.Height)],'position_mm':list(o.Placement.Base)} for o in supports],
 'historical_office_leaves':old_office,
 'invalid_hardware':[o.Name for o in hardware if not o.Shape.isValid()],'invalid_fronts':[o.Name for o in fronts if not o.Shape.isValid()],
 'scope':'R11 proposta: quatro folhas escritório, três cabeceira existentes com apoios, vizinha/canto R04 preservados. Mesma dobradiça comum. Não libera fabricação/carga/fixação.'}
((Path(__file__).resolve().parent / 'Montagem_R11.json').resolve()).write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
result=json.dumps({k:v for k,v in data.items() if k!='doors'},ensure_ascii=False)
