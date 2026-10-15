from pathlib import Path
import math,json
import FreeCAD as App
import FreeCADGui as Gui
import Part

root=(Path(__file__).resolve().parent / '.').resolve()
doc=next(d for d in App.listDocuments().values() if d.FileName and Path(d.FileName).name=='Guedala_Park_R03_Ferragens_Canto.FCStd')
doc.save()  # Preserve the previous completed stage before extending it.
s=next(o for o in doc.Objects if o.Name.startswith('ControleCanto'));N=s.Name
inspection=App.getDocument('Blum_Inspecao_Articulacoes')
geometry=json.loads(((Path(__file__).resolve().parent / 'Geometria_vizinha.json').resolve()).read_text())
def shared(i,j,approx):
    rows=[]
    for c in geometry['parts'][i]['cylinders_Y']:
        p=[c['center'][0],c['center'][2]]
        for d in geometry['parts'][j]['cylinders_Y']:
            q=[d['center'][0],d['center'][2]]
            if math.dist(p,q)<.001:rows.append(p)
    return min(rows,key=lambda p:math.dist(p,approx))
a=shared(1,2,[-27.5,42.61]);b=shared(1,3,[-17.94,34.32])
c=shared(2,4,[-7.44,45.4]);d=shared(3,4,[-2.64,40.8])
def circle(A,B,r1,r2,sign):
    dx,dz=B[0]-A[0],B[1]-A[1];dist=math.hypot(dx,dz)
    ell=(r1*r1-r2*r2+dist*dist)/(2*dist);h=math.sqrt(r1*r1-ell*ell)
    return [A[0]+ell*dx/dist-sign*h*dz/dist,A[1]+ell*dz/dist+sign*h*dx/dist]
Q=[b[0]-d[0]+c[0],b[1]-d[1]+c[1]]
sign=min([-1,1],key=lambda z:math.dist(circle(a,Q,math.dist(a,c),math.dist(b,d),z),c))
row=80;cells={}
def cell(alias,label,value):
    global row
    address='B'+str(row);s.set('A'+str(row),label);s.set(address,str(value));s.setAlias(address,alias)
    cells[alias]=address;row+=1;return address
def expr(alias,label,f):return cell(alias,label,'='+f)
def v(alias):return cells[alias]
def wrap(f):return 'atan2(sin('+f+'),cos('+f+'))'
def angle(p,q):return math.degrees(math.atan2(q[1]-p[1],q[0]-p[0]))
for n,p in zip('abcd',[a,b,c,d]):
    cell('N'+n+'0x','Vizinha - eixo '+n+' x',p[0]);cell('N'+n+'0z','Vizinha - eixo '+n+' z',p[1])
expr('NThetaCup','Vizinha - abertura CAD 0-110 graus','-min(110 deg,max(0 deg,B4))')
t=v('NThetaCup');dcx=d[0]-c[0];dcz=d[1]-c[1]
expr('NQx','Vizinha - centro do segundo circulo x',f'{b[0]:.16g}-cos({t})*({dcx:.16g})+sin({t})*({dcz:.16g})')
expr('NQz','Vizinha - centro do segundo circulo z',f'{b[1]:.16g}-sin({t})*({dcx:.16g})-cos({t})*({dcz:.16g})')
expr('NDist','Vizinha - distancia entre centros',f'sqrt(({v("NQx")}-({a[0]:.16g}))^2+({v("NQz")}-({a[1]:.16g}))^2)')
expr('NL','Vizinha - projecao do circulo',f'({math.dist(a,c)**2:.16g}-{math.dist(b,d)**2:.16g}+{v("NDist")}^2)/(2*{v("NDist")})')
expr('NH','Vizinha - altura do circulo',f'sqrt({math.dist(a,c)**2:.16g}-{v("NL")}^2)')
expr('NCx','Vizinha - eixo C movel x',f'{a[0]:.16g}+({v("NL")}*({v("NQx")}-({a[0]:.16g}))-({sign})*{v("NH")}*({v("NQz")}-({a[1]:.16g})))/{v("NDist")}')
expr('NCz','Vizinha - eixo C movel z',f'{a[1]:.16g}+({v("NL")}*({v("NQz")}-({a[1]:.16g}))+({sign})*{v("NH")}*({v("NQx")}-({a[0]:.16g})))/{v("NDist")}')
expr('NDx','Vizinha - eixo D movel x',f'{v("NCx")}+cos({t})*({dcx:.16g})-sin({t})*({dcz:.16g})')
expr('NDz','Vizinha - eixo D movel z',f'{v("NCz")}+sin({t})*({dcx:.16g})+cos({t})*({dcz:.16g})')
expr('NTheta2','Vizinha - braco 2',wrap(f'atan2({v("NCz")}-({a[1]:.16g}),{v("NCx")}-({a[0]:.16g}))-({angle(a,c):.16g} deg)'))
expr('NTheta3','Vizinha - braco 3',wrap(f'atan2({v("NDz")}-({b[1]:.16g}),{v("NDx")}-({b[0]:.16g}))-({angle(b,d):.16g} deg)'))
for i,theta,point,mx,mz in [(2,'NTheta2',a,str(a[0]),str(a[1])),(3,'NTheta3',b,str(b[0]),str(b[1])),(4,'NThetaCup',c,v('NCx'),v('NCz'))]:
    expr('NT'+str(i)+'x','Vizinha - translacao '+str(i)+' x',f'{mx}-cos({v(theta)})*({point[0]:.16g})+sin({v(theta)})*({point[1]:.16g})')
    expr('NT'+str(i)+'z','Vizinha - translacao '+str(i)+' z',f'{mz}-sin({v(theta)})*({point[0]:.16g})-cos({v(theta)})*({point[1]:.16g})')
expr('NmountY','Vizinha - face interna do divisor','-1050-B5/(1 mm)-(1800-B5/(1 mm))/4+9')
expr('NDeltaX','Vizinha - translacao global x',f'193.5+{v("NT4z")}-193.5*cos({t})+{v("NmountY")}*sin({t})')
expr('NDeltaY','Vizinha - translacao global y',f'{v("NmountY")}-{v("NT4x")}-193.5*sin({t})-{v("NmountY")}*cos({t})')
doc.recompute()
ref=lambda alias:N+'.'+alias
corner=next(o for o in doc.Objects if o.Label.startswith('Canto integrado em L') and o.TypeId=='App::Part')
aerial=next(o for o in doc.Objects if o.Label.startswith('Aéreo raso da cabeceira') and o.TypeId=='App::Part')
old_group=next(o for o in aerial.Group if o.TypeId=='App::Part' and hasattr(o,'Abertura') and any('Vizinha' in ex for prop,ex in o.ExpressionEngine))
front=next(o for o in old_group.Group if o.TypeId=='Part::Box')
old_group.removeObject(front)
ga=doc.addObject('App::Part','VizinhaCADR03');corner.addObject(ga)
ga.Label='Vizinha - movimento 4 barras - 71B3650 candidata'
ga.setExpression('Placement.Base.x',ref('NDeltaX')+' * 1 mm')
ga.setExpression('Placement.Base.y',ref('NDeltaY')+' * 1 mm')
ga.setExpression('Placement.Rotation.Angle',ref('NThetaCup'))
ga.addObject(front)
front.Placement=App.Placement(App.Vector(250,-1611.5,1),App.Rotation(App.Vector(0,0,1),90))
front.setExpression('Placement.Base.y',ref('NmountY')+' * 1 mm - 8 mm')
front.setExpression('Length','(1800 mm - '+N+'.Faixa) / 4 - 2 mm')
front.Label='Vizinha - painel de estudo - furacao K 6.5 mm'
cutters=[]
for h in [51,255]:
    o=doc.addObject('Part::Cylinder','CanecoVizinhaR03');ga.addObject(o)
    o.Radius=17.5;o.Height=13
    o.Placement=App.Placement(App.Vector(232,-1587.5,h),App.Rotation(App.Vector(0,0,1),App.Vector(1,0,0)))
    o.setExpression('Placement.Base.y',ref('NmountY')+' * 1 mm + 16 mm');cutters.append(o)
tool=doc.addObject('Part::MultiFuse','UsinagemVizinhaR03');ga.addObject(tool);tool.Shapes=cutters
cut=doc.addObject('Part::Cut','VizinhaComCanecosR03');ga.addObject(cut);cut.Base=front;cut.Tool=tool
cut.Label='Vizinha - canecos CAD, aplicacao de estudo';cut.ViewObject.ShapeColor=(.66,.26,.24)
wall=doc.addObject('Part::Box','DivisorApoioVizinhaR03');corner.addObject(wall)
wall.Label='Divisor 18 mm de apoio da vizinha - proposta'
wall.Length=212;wall.Width=18;wall.Height=272;wall.Placement.Base=App.Vector(18,-1621.5,18)
wall.setExpression('Placement.Base.y',ref('NmountY')+' * 1 mm - 18 mm')
wall.ViewObject.ShapeColor=(.75,.66,.48)
matrix=App.Matrix();matrix.A11=0;matrix.A12=0;matrix.A13=1
matrix.A21=-1;matrix.A22=0;matrix.A23=0;matrix.A31=0;matrix.A32=-1;matrix.A33=0
def newfeature(parent,name,label,source):
    shape=source.Shape.transformGeometry(source.Shape.Placement.toMatrix());shape.Placement=App.Placement()
    shape=shape.transformGeometry(matrix)
    o=doc.addObject('Part::Feature',name);parent.addObject(o);o.Label=label;o.Shape=shape
    o.ViewObject.ShapeColor=(.65,.68,.72);return o
for h in [51,255]:
    assembly=doc.addObject('App::Part','BlumVizinhaR03');corner.addObject(assembly)
    assembly.Label='71B3650 - quatro barras - nivel '+str(h)
    assembly.Placement.Base=App.Vector(193.5,-1603.5,h)
    assembly.setExpression('Placement.Base.y',ref('NmountY')+' * 1 mm')
    for i,p in enumerate(geometry['parts']):
        o=newfeature(assembly,'VizinhaCorpoR03','71B3650 - corpo '+str(i)+' - '+p['label'],inspection.getObject(p['name']))
        o.addProperty('App::PropertyInteger','IndiceCorpo');o.IndiceCorpo=i
        if i in [2,3,4]:
            angle='NThetaCup' if i==4 else 'NTheta'+str(i)
            o.setExpression('Placement.Base.x',ref('NT'+str(i)+'z')+' * 1 mm')
            o.setExpression('Placement.Base.y','-'+ref('NT'+str(i)+'x')+' * 1 mm')
            o.setExpression('Placement.Rotation.Angle',ref(angle))
    newfeature(assembly,'CalcoVizinhaR03','173H7100 - calco da vizinha - candidato',inspection.getObject('Part__Feature011'))
doc.recompute()
for o in cutters+[front,tool]:o.ViewObject.Visibility=False
cut.ViewObject.Visibility=True
report={'joint_source':geometry['source'],'a':a,'b':b,'c':c,'d':d,'circle_branch':sign,
    'native_four_bar':True,'hinge_count_study':2,'max_opening_deg':110,
    'bore_distance_study_mm':24,'K_study_mm':6.5,
    'scope':'Candidata 71B3650 com calco0, divisor18, sem homologacao de carga, fixacao e ajustes.'}
((Path(__file__).resolve().parent / 'Vizinha_parametros.json').resolve()).write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
doc.save()
result=json.dumps({'invalid':[o.Name for o in doc.Objects if 'Invalid' in o.State],'objects':len(doc.Objects),'neighbour_angle':str(s.NThetaCup)})
