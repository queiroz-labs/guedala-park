from pathlib import Path
import json, math
from datetime import datetime
import Import
import FreeCAD as App
import FreeCADGui as Gui
import Part

root=(Path(__file__).resolve().parent / '.').resolve()
source=(Path(__file__).resolve().parent / '../Guedala_Park_R02_Canto.FCStd').resolve()
dest=(Path(__file__).resolve().parent / 'Guedala_Park_R03_Ferragens_Canto.FCStd').resolve()
if dest.exists():
    dest=dest.with_stem(dest.stem+'_'+datetime.now().strftime('%Y%m%d_%H%M%S_%f'))
doc=App.openDocument(str(source))
doc.Label='Guedala Park - R03 - canto com CAD Blum e articulacoes reconstruidas'
corner=next(o for o in doc.Objects if o.Label.startswith('Canto integrado em L') and o.TypeId=='App::Part')
room=next(o for o in doc.Objects if o.Name.startswith('Ambiente_quarto'))
A=next(o for o in corner.Group if o.Label.startswith('Frente articulada A'))
B=next(o for o in corner.Group if o.Label.startswith('Frente articulada B'))
controls=next(o for o in doc.Objects if o.Name.startswith('ControleCanto'))
controls.Label='Canto - abertura e articulacoes reconstruidas - R03'
controls.set('B2','0 deg');controls.set('B3','0 deg');controls.set('B4','0 deg')
controls.set('B5','150 mm');controls.set('B8','40 mm')
N=controls.Name
parameters=json.loads(((Path(__file__).resolve().parent / 'Parametros_expressões.json').resolve()).read_text())
j=parameters['joints'];coeff=parameters['drive_polynomial_coefficients']

row=12
cells={}
def cell(alias,label,value):
    global row
    address='B'+str(row)
    controls.set('A'+str(row),label)
    controls.set(address,str(value))
    controls.setAlias(address,alias);cells[alias]=address;row+=1
    return address
def expr(alias,label,formula): return cell(alias,label,'='+formula)
def v(alias): return cells[alias]
def wrap(formula): return 'atan2(sin('+formula+'),cos('+formula+'))'

cell('NotaR03','Geometria/cotas desta montagem são proposta de estudo','Reconstrucao dos eixos extraidos do STEP; sem liberacao de corte')
expr('Sdrive','Principal solicitada limitada a 0-92 graus','min(92,max(0,B2/(1 deg)))/92')
s=v('Sdrive')
poly=f'{coeff[-1]:.16g}'
for c in reversed(coeff[:-1]): poly=f'({c:.16g}+{s}*{poly})'
expr('DriveQ','Angulo da manivela inferido do curso principal',f'-({parameters["q_at_92_deg"]:.16g}*{s}+{s}*({s}-1)*{poly})*(1 deg)')
for point in 'abcdefg':
    cell(point+'0x','Eixo '+point+' - x original STEP',j[point][0])
    cell(point+'0z','Eixo '+point+' - z original STEP',j[point][1])
def initial(p,k): return v(p+'0'+k)
q=v('DriveQ');ax=initial('a','x');az=initial('a','z');cx=initial('c','x');cz=initial('c','z')
expr('Cx','Eixo c - x movel',f'{ax}+cos({q})*({cx}-{ax})-sin({q})*({cz}-{az})')
expr('Cz','Eixo c - z movel',f'{az}+sin({q})*({cx}-{ax})+cos({q})*({cz}-{az})')
length=lambda p,r: math.dist(j[p],j[r])
expr('DistCb','Distancia entre C e eixo fixo b',f'sqrt(({initial("b","x")}-{v("Cx")})^2+({initial("b","z")}-{v("Cz")})^2)')
expr('Ld','Intersecao dos circulos C/b - projecao',f'({length("c","d")**2:.16g}-{length("b","d")**2:.16g}+{v("DistCb")}^2)/(2*{v("DistCb")})')
expr('Hd','Intersecao dos circulos C/b - altura',f'sqrt({length("c","d")**2:.16g}-{v("Ld")}^2)')
expr('Dx','Eixo d - x movel',f'{v("Cx")}+({v("Ld")}*({initial("b","x")}-{v("Cx")})-{v("Hd")}*({initial("b","z")}-{v("Cz")}))/{v("DistCb")}')
expr('Dz','Eixo d - z movel',f'{v("Cz")}+({v("Ld")}*({initial("b","z")}-{v("Cz")})+{v("Hd")}*({initial("b","x")}-{v("Cx")}))/{v("DistCb")}')
def initial_angle(p,r): return math.degrees(math.atan2(j[r][1]-j[p][1],j[r][0]-j[p][0]))
expr('Theta6','Braco 6 - angulo em XZ',wrap(f'atan2({v("Dz")}-{initial("b","z")},{v("Dx")}-{initial("b","x")})-({initial_angle("b","d"):.16g} deg)'))
expr('Theta5','Braco 5 - angulo em XZ',wrap(f'atan2({v("Dz")}-{v("Cz")},{v("Dx")}-{v("Cx")})-({initial_angle("c","d"):.16g} deg)'))
def moving(alias,p,origin,origin_moving,theta):
    ix=initial(p,'x');iz=initial(p,'z');ox=initial(origin,'x');oz=initial(origin,'z')
    nx=v(origin_moving+'x');nz=v(origin_moving+'z')
    expr(alias+'x',alias+' x',f'{nx}+cos({v(theta)})*({ix}-{ox})-sin({v(theta)})*({iz}-{oz})')
    expr(alias+'z',alias+' z',f'{nz}+sin({v(theta)})*({ix}-{ox})+cos({v(theta)})*({iz}-{oz})')
# Fixed b uses its original coordinates.
expr('Bfixedx','Eixo b fixo x',initial('b','x'));expr('Bfixedz','Eixo b fixo z',initial('b','z'))
moving('E','e','b','Bfixed','Theta6')
moving('G','g','c','C','Theta5')
expr('DistEg','Distancia entre E e G',f'sqrt(({v("Gx")}-{v("Ex")})^2+({v("Gz")}-{v("Ez")})^2)')
expr('Lf','Intersecao dos circulos E/G - projecao',f'({length("e","f")**2:.16g}-{length("g","f")**2:.16g}+{v("DistEg")}^2)/(2*{v("DistEg")})')
expr('Hf','Intersecao dos circulos E/G - altura',f'sqrt({length("e","f")**2:.16g}-{v("Lf")}^2)')
expr('Fx','Eixo f - x movel',f'{v("Ex")}+({v("Lf")}*({v("Gx")}-{v("Ex")})-{v("Hf")}*({v("Gz")}-{v("Ez")}))/{v("DistEg")}')
expr('Fz','Eixo f - z movel',f'{v("Ez")}+({v("Lf")}*({v("Gz")}-{v("Ez")})+{v("Hf")}*({v("Gx")}-{v("Ex")}))/{v("DistEg")}')
expr('Theta2','Caneco principal - angulo XZ',wrap(f'atan2({v("Fz")}-{v("Gz")},{v("Fx")}-{v("Gx")})-({initial_angle("g","f"):.16g} deg)'))
expr('Theta3','Braco 3 - angulo XZ',wrap(f'atan2({v("Fz")}-{v("Ez")},{v("Fx")}-{v("Ex")})-({initial_angle("e","f"):.16g} deg)'))
expr('PrincipalReal','Abertura calculada pela geometria dos bracos','-'+v('Theta2'))
for index,point,moving_name,theta in [(4,'a','a0','DriveQ'),(6,'b','Bfixed','Theta6'),(5,'c','C','Theta5'),(2,'g','G','Theta2'),(3,'e','E','Theta3')]:
    tx=initial(point,'x');tz=initial(point,'z');mx=v(moving_name+'x');mz=v(moving_name+'z');angle=v(theta)
    expr('T'+str(index)+'x','Translacao do corpo '+str(index)+' - x',f'{mx}-cos({angle})*{tx}+sin({angle})*{tz}')
    expr('T'+str(index)+'z','Translacao do corpo '+str(index)+' - z',f'{mz}-sin({angle})*{tx}-cos({angle})*{tz}')
real=v('PrincipalReal')
expr('DeltaAx','Deslocamento global A - x',f'632+{v("T2x")}-632*cos({real})+(-593.5)*sin({real})')
expr('DeltaAy','Deslocamento global A - y',f'-593.5-{v("T2z")}-632*sin({real})-(-593.5)*cos({real})')
expr('BetaReal','Articulacao B limitada ao dominio 0-60 graus','min(60 deg,max(0 deg,B3))')
beta=v('BetaReal')
expr('DeltaBx','Deslocamento global B - x',f'{v("DeltaAx")}+cos({real})*(259-259*cos({beta})+(-638.5)*sin({beta}))-sin({real})*(-638.5-259*sin({beta})-(-638.5)*cos({beta}))')
expr('DeltaBy','Deslocamento global B - y',f'{v("DeltaAy")}+sin({real})*(259-259*cos({beta})+(-638.5)*sin({beta}))+cos({real})*(-638.5-259*sin({beta})-(-638.5)*cos({beta}))')
controls.setColumnWidth('A',430);controls.setColumnWidth('B',160)
doc.recompute()

def reference(alias): return N+'.'+alias
def part(parent,name,label):
    o=doc.addObject('App::Part',name);parent.addObject(o);o.Label=label;return o
def delta_group(name,label,xalias,yalias,angle):
    o=part(corner,name,label)
    o.setExpression('Placement.Base.x',reference(xalias)+' * 1 mm')
    o.setExpression('Placement.Base.y',reference(yalias)+' * 1 mm')
    o.setExpression('Placement.Rotation.Angle',angle)
    return o
ga=delta_group('FolhaAReal','Folha A - acompanha caneco principal','DeltaAx','DeltaAy',reference('PrincipalReal'))
gb=delta_group('FolhaBReal','Folha B - dobradica de uniao com regulagem travada','DeltaBx','DeltaBy',reference('PrincipalReal')+' + '+reference('BetaReal'))
for o in [A,B]:
    for prop,expr_value in list(o.ExpressionEngine): o.setExpression(prop,None)
    corner.removeObject(o)
ga.addObject(A);gb.addObject(B)
A.Length=396;A.Width=18;A.Height=306
A.Placement=App.Placement(App.Vector(647,-632,1),App.Rotation(App.Vector(0,0,1),180))
B.Length=396;B.Width=18;B.Height=306
B.Placement=App.Placement(App.Vector(232,-651,1),App.Rotation(App.Vector(0,0,1),-90))
A.Corte='Variante CAD: 396x306x18, K principal 4 mm, caneco de uniao a 12.5 mm da borda. NAO e corte aprovado.'
B.Corte='Variante CAD: 396x306x18. Junta de estudo 1 mm na quina, sem regular a ferragem real. NAO e corte aprovado.'
cutters=[]
for h in [51,255]:
    for center,depth,label in [(625.5,13,'principal'),(263.5,11,'uniao - furo aberto na borda')]:
        o=doc.addObject('Part::Cylinder','FuroCanecoR03');ga.addObject(o)
        o.Label='Caneco '+label+' - referencia nao executiva'
        o.Radius=17.5;o.Height=depth
        o.Placement=App.Placement(App.Vector(center,-632,h),App.Rotation(App.Vector(0,0,1),App.Vector(0,-1,0)))
        cutters.append(o)
tool=doc.addObject('Part::MultiFuse','UsinagemEstudoA');ga.addObject(tool);tool.Shapes=cutters
front=doc.addObject('Part::Cut','FrenteAComCanecos');ga.addObject(front)
front.Label='Frente A - furos de caneco em estudo';front.Base=A;front.Tool=tool
front.ViewObject.ShapeColor=(.17,.47,.57);B.ViewObject.ShapeColor=(.81,.55,.25)
wall=doc.addObject('Part::Box','LateralApoioPrincipal');corner.addObject(wall)
wall.Label='Lateral 18 mm de apoio da principal - proposta R03'
wall.Length=18;wall.Width=612;wall.Height=272;wall.Placement.Base=App.Vector(632,-630,18)
wall.ViewObject.ShapeColor=(.75,.66,.48)
wall.addProperty('App::PropertyString','Status');wall.Status='Suporte necessario a montagem; nova proposta, sem aprovacao executiva.'

cache=(Path(__file__).resolve().parent / '../../../03_Recursos/Ferragens_STEP_2026-10-13/Referencias/CLIP_top').resolve()
def read_shapes(path):
    name='FonteSTEP_R03'
    if name in App.listDocuments(): App.closeDocument(name)
    temp=App.newDocument(name);Import.insert(str(path),temp.Name);temp.recompute()
    shapes=[(o.Shape.copy(),o.Label) for o in temp.Objects if o.TypeId=='Part::Feature' and len(o.Shape.Solids)==1]
    App.closeDocument(temp.Name);App.setActiveDocument(doc.Name)
    return shapes
main=read_shapes(next(((Path(__file__).resolve().parent / '../Blum_oficial/71T7550').resolve()).glob('*.step')))
fold=read_shapes(next(((Path(__file__).resolve().parent / '../Blum_oficial/79T8500').resolve()).glob('*.step')))
plate=read_shapes((Path(__file__).resolve().parent / '../../../03_Recursos/Ferragens_STEP_2026-10-13/Referencias/CLIP_top/173H7100_42501451.step').resolve())[0]
stop=read_shapes((Path(__file__).resolve().parent / '../../../03_Recursos/Ferragens_STEP_2026-10-13/Referencias/CLIP_top/70T7553.09_41054330.step').resolve())[0]
def feature(parent,name,label,shape,rotation):
    copy=shape.transformGeometry(shape.Placement.toMatrix())
    copy.Placement=App.Placement()
    copy=copy.transformGeometry(rotation.toMatrix())
    o=doc.addObject('Part::Feature',name);parent.addObject(o);o.Label=label;o.Shape=copy
    o.ViewObject.ShapeColor=(.68,.70,.72);return o
palette=[(.7,.72,.74),(.3,.5,.7),(.3,.7,.4),(.9,.66,.2),(.64,.33,.8),(.15,.7,.7),(.8,.45,.25)]
theta={4:'DriveQ',6:'Theta6',5:'Theta5',2:'Theta2',3:'Theta3'}
hardware=[]
for h in [51,255]:
    assembly=part(corner,'PrincipalBlumR03','71T7550 - bracos reconstruidos - nivel '+str(h))
    assembly.Placement.Base=App.Vector(632,-593.5,h)
    for i,(shape,label) in enumerate(main):
        o=feature(assembly,'PrincipalCorpoR03','71T7550 - corpo '+str(i)+' - '+label,shape,App.Rotation(App.Vector(1,0,0),90))
        o.addProperty('App::PropertyInteger','IndiceCorpo');o.IndiceCorpo=i
        o.ViewObject.ShapeColor=palette[i]
        if i in theta:
            o.setExpression('Placement.Base.x',reference('T'+str(i)+'x')+' * 1 mm')
            o.setExpression('Placement.Base.y','-'+reference('T'+str(i)+'z')+' * 1 mm')
            o.setExpression('Placement.Rotation.Angle','-'+reference(theta[i]))
        hardware.append(o)
    feature(assembly,'CalcoPrincipalR03','173H7100 - calco 0 mm - candidato',plate[0],App.Rotation(App.Vector(1,0,0),90))
    limiter=feature(assembly,'LimitadorR03','70T7553.09 - montagem inferida no corpo 6',stop[0],App.Rotation(App.Vector(1,0,0),90))
    limiter.ViewObject.ShapeColor=(.25,.27,.28)
    limiter.setExpression('Placement.Base.x',reference('T6x')+' * 1 mm')
    limiter.setExpression('Placement.Base.y','-'+reference('T6z')+' * 1 mm')
    limiter.setExpression('Placement.Rotation.Angle','-'+reference('Theta6'))
    secondary=part(ga,'UniaoBlumR03','79T8500 - caneco na A - nivel '+str(h))
    secondary.Placement.Base=App.Vector(232,-688,h)
    base=part(secondary,'BracoUniaoMovel','79T8500 - braco/base ligados a B; regulagem travada')
    base.setExpression('Placement.Base.x','27 mm - 27 mm*cos('+reference('BetaReal')+') + 49.5 mm*sin('+reference('BetaReal')+')')
    base.setExpression('Placement.Base.y','49.5 mm - 27 mm*sin('+reference('BetaReal')+') - 49.5 mm*cos('+reference('BetaReal')+')')
    base.setExpression('Placement.Rotation.Angle',reference('BetaReal'))
    for i,(shape,label) in enumerate(fold):
        parent=secondary if i==3 else base
        o=feature(parent,'UniaoCorpoR03','79T8500 - corpo '+str(i)+' - '+label,shape,App.Rotation(App.Vector(1,0,0),-90))
        o.addProperty('App::PropertyInteger','IndiceCorpo');o.IndiceCorpo=i
        hardware.append(o)
    feature(base,'CalcoUniaoR03','173H7100 - calco sobre B - candidato',plate[0],App.Rotation(App.Vector(1,0,0),-90))

corner.ModeloDeMovimento='Principal: seis corpos rigidos/sete eixos reconstruidos do STEP. Uniao: pivô CAD, regulagem travada. Nao e lei cinematica homologada pela Blum.'
corner.addProperty('App::PropertyString','EstadoR03','Conferencia')
corner.EstadoR03='Cotas e apoios desta variante nao aprovados. Furo de borda, ajustes, quantidade e carga exigem conferência executiva.'
for o in doc.Objects:
    if o.Name.startswith('ReferenciasFerragens'): o.ViewObject.Visibility=False
    if o.Name.startswith('Ambiente_'): o.ViewObject.Visibility=o==room
    if o.Name in ['ParedesInteiras','ParedesCortadas']: o.ViewObject.Visibility=False
doc.recompute()
for o in cutters+[A,tool]:o.ViewObject.Visibility=False
front.ViewObject.Visibility=True
App.setActiveDocument(doc.Name)
Gui.activeDocument().activeView().viewAxonometric();Gui.activeDocument().activeView().fitAll();Gui.updateGui()
invalid=[o.Name for o in doc.Objects if 'Invalid' in o.State]
invalid_shapes=[o.Name for o in doc.Objects if hasattr(o,'Shape') and not o.Shape.isNull() and not o.Shape.isValid()]
report={'file':str(dest),'invalid_objects':invalid,'invalid_shapes':invalid_shapes,
    'principal_real_deg':float(controls.PrincipalReal),'native_motion_expressions':True,
    'principal_joints':7,'main_links':6,'fold_adjustment_locked':True,
    'fronts_study_mm':{'A':[396,306,18],'B':[396,306,18]},
    'new_support':{'right_wall_mm':18,'status':'proposta'},
    'kinematics_scope':'Reconstrucao de geometria CAD, sem tolerancias e sem carga. Ajuste neutral do STEP da uniao.'}
doc.saveAs(str(dest))
((Path(__file__).resolve().parent / 'Montagem_R03.json').resolve()).write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
result=json.dumps(report,ensure_ascii=False)
