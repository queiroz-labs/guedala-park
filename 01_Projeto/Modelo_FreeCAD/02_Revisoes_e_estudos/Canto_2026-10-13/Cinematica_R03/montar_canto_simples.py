from pathlib import Path
import json,math,shutil
from datetime import datetime
import FreeCAD as App
import FreeCADGui as Gui
import Part
import Import

root=(Path(__file__).resolve().parent / '.').resolve()
out=(Path(__file__).resolve().parent / '../Canto_simples_R04').resolve();out.mkdir(exist_ok=True)
original=next((d for d in App.listDocuments().values() if d.FileName and Path(d.FileName).name=='Guedala_Park_R03_Ferragens_Canto.FCStd'),None)
if original is None:original=App.openDocument(str((Path(__file__).resolve().parent / 'Guedala_Park_R03_Ferragens_Canto.FCStd').resolve()))
original.save()
dest=(Path(__file__).resolve().parent / '../Canto_simples_R04/Guedala_Park_R04_Canto_Simples.FCStd').resolve()
if dest.exists():dest=dest.with_stem(dest.stem+'_'+datetime.now().strftime('%Y%m%d_%H%M%S'))
shutil.copy2(original.FileName,dest)
doc=App.openDocument(str(dest));App.setActiveDocument(doc.Name)
doc.Label='Guedala Park - R04 - duas portas simples em sequencia'
corner=next(o for o in doc.Objects if o.TypeId=='App::Part' and o.Label.startswith('Canto integrado em L'))
old=next(o for o in doc.Objects if o.Name.startswith('ControleCanto'))
for cell in ['B2','B3','B4']:old.set(cell,'0 deg')
old.set('B5','25 mm')
doc.recompute()
for o in corner.Group:
    if o.Label.startswith(('Folha A - acompanha','Folha B - dobradica','71T7550 - bracos reconstruidos')):o.ViewObject.Visibility=False
simple=doc.addObject('App::Part','CantoSimplesR04');corner.addObject(simple)
simple.Label='Canto R04 - portas independentes - proposta simples'
s=doc.addObject('Spreadsheet::Sheet','ControleSimplesR04')
s.Label='R04 - abertura independente das duas portas'
s.set('A1','CANTO SIMPLES - PROPOSTA EM CONFERENCIA')
s.set('A2','Porta A (principal) - graus');s.set('B2','0 deg');s.setAlias('B2','AberturaA')
s.set('A3','Porta B (lateral) - graus');s.set('B3','0 deg');s.setAlias('B3','AberturaB')
s.set('A4','Funcionamento');s.set('B4','Portas independentes com faixa fixa na quina')
s.set('A5','Ferragem candidata');s.set('B5','Duas dobradicas comuns 71B3550 por porta; quantidade/carga a conferir')
s.set('A6','Cotas propostas');s.set('B6','A/B 271x306x18; faixa fixa 142/124; juntas 2 mm')
s.set('A7','Curso maximo de estudo');s.set('B7','86 deg');s.setAlias('B7','CursoEstudo')
s.set('A8','Limitador candidato');s.set('B8','70T3553 de encaixe, 110 para 86 graus; conferir montagem')
s.setColumnWidth('A',400);s.setColumnWidth('B',420)
source=App.listDocuments().get('Inspecao_Simples_R04')
library=(Path(__file__).resolve().parent / '../../../03_Recursos/Ferragens_STEP_2026-10-13/Referencias').resolve()
if source is None:
    source=App.newDocument('Inspecao_Simples_R04')
    Import.insert(str(next(((Path(__file__).resolve().parent / '../../../03_Recursos/Ferragens_STEP_2026-10-13/Referencias/CLIP_top_BLUMOTION').resolve()).glob('71B3550_*.step'))),source.Name)
    source.recompute()
parts=[o for o in source.Objects if o.TypeId=='Part::Feature' and len(o.Shape.Solids)==1]
parts=parts[:5]
before={o.Name for o in source.Objects}
Import.insert(str(next(((Path(__file__).resolve().parent / '../../../03_Recursos/Ferragens_STEP_2026-10-13/Referencias/CLIP_top').resolve()).glob('173H7100_*.step'))),source.Name);source.recompute()
plate=next(o for o in source.Objects if o.Name not in before and o.TypeId=='Part::Feature' and len(o.Shape.Solids)==1)
source.saveAs(str((Path(__file__).resolve().parent / '../Canto_simples_R04/Fontes_STEP_Simples.FCStd').resolve()))
App.setActiveDocument(doc.Name)
cyls=[]
for o in parts:
    cyls.append([{'p':[f.Surface.Center.x,f.Surface.Center.z],'area':f.Area}
        for f in o.Shape.Faces if isinstance(f.Surface,Part.Cylinder) and abs(f.Surface.Axis.y)>.99 and f.Surface.Radius<8])
def joint(i,j):
    pairs=[(a,b) for a in cyls[i] for b in cyls[j] if math.dist(a['p'],b['p'])<.001]
    return max(pairs,key=lambda p:p[0]['area']+p[1]['area'])[0]['p']
a,b,c,d=[joint(i,j) for i,j in [(1,2),(1,3),(2,4),(3,4)]]
def circle(A,B,r1,r2,sign):
    dx,dz=B[0]-A[0],B[1]-A[1];dist=math.hypot(dx,dz)
    ell=(r1*r1-r2*r2+dist*dist)/(2*dist);h=math.sqrt(r1*r1-ell*ell)
    return [A[0]+ell*dx/dist-sign*h*dz/dist,A[1]+ell*dz/dist+sign*h*dx/dist]
Q=[b[0]-d[0]+c[0],b[1]-d[1]+c[1]]
sign=min([-1,1],key=lambda z:math.dist(circle(a,Q,math.dist(a,c),math.dist(b,d),z),c))
row=12
def add(alias,label,val):
    global row
    addr='B'+str(row);s.set('A'+str(row),label);s.set(addr,str(val));s.setAlias(addr,alias);row+=1
    return addr
def angle(p,q):return math.degrees(math.atan2(q[1]-p[1],q[0]-p[0]))
def feature(parent,label,source,matrix):
    baked=source.Shape.transformGeometry(source.Shape.Placement.toMatrix());baked.Placement=App.Placement()
    o=doc.addObject('Part::Feature','FerragemSimplesR04');parent.addObject(o);o.Label=label;o.Shape=baked.transformGeometry(matrix)
    o.ViewObject.ShapeColor=(.65,.68,.72);return o
def box(parent,name,label,base,dims,color):
    o=doc.addObject('Part::Box',name);parent.addObject(o);o.Label=label
    o.Length,o.Width,o.Height=dims;o.Placement.Base=App.Vector(*base);o.ViewObject.ShapeColor=color;return o
fronts=[]
for letter,inp,mount,frame in [('A','B2',(632,-593.5),'A'),('B','B3',(193.5,-1032),'B')]:
    aliases={}
    def ex(alias,f):
        aliases[alias]=add(letter+alias,letter+' - '+alias,'='+f);return aliases[alias]
    theta=ex('Theta','-min(B7,max(0 deg,'+inp+'))')
    dcx,dcz=d[0]-c[0],d[1]-c[1]
    qx=ex('Qx',f'{b[0]:.16g}-cos({theta})*({dcx:.16g})+sin({theta})*({dcz:.16g})')
    qz=ex('Qz',f'{b[1]:.16g}-sin({theta})*({dcx:.16g})-cos({theta})*({dcz:.16g})')
    dist=ex('Dist',f'sqrt(({qx}-({a[0]:.16g}))^2+({qz}-({a[1]:.16g}))^2)')
    ell=ex('L',f'({math.dist(a,c)**2:.16g}-{math.dist(b,d)**2:.16g}+{dist}^2)/(2*{dist})')
    h=ex('H',f'sqrt({math.dist(a,c)**2:.16g}-{ell}^2)')
    cx=ex('Cx',f'{a[0]:.16g}+({ell}*({qx}-({a[0]:.16g}))-({sign})*{h}*({qz}-({a[1]:.16g})))/{dist}')
    cz=ex('Cz',f'{a[1]:.16g}+({ell}*({qz}-({a[1]:.16g}))+({sign})*{h}*({qx}-({a[0]:.16g})))/{dist}')
    dx=ex('Dx',f'{cx}+cos({theta})*({dcx:.16g})-sin({theta})*({dcz:.16g})')
    dz=ex('Dz',f'{cz}+sin({theta})*({dcx:.16g})+cos({theta})*({dcz:.16g})')
    t2=ex('Theta2',f'atan2(sin(atan2({cz}-({a[1]:.16g}),{cx}-({a[0]:.16g}))-({angle(a,c):.16g} deg)),cos(atan2({cz}-({a[1]:.16g}),{cx}-({a[0]:.16g}))-({angle(a,c):.16g} deg)))')
    t3=ex('Theta3',f'atan2(sin(atan2({dz}-({b[1]:.16g}),{dx}-({b[0]:.16g}))-({angle(b,d):.16g} deg)),cos(atan2({dz}-({b[1]:.16g}),{dx}-({b[0]:.16g}))-({angle(b,d):.16g} deg)))')
    for i,t,p,xx,zz in [(2,t2,a,str(a[0]),str(a[1])),(3,t3,b,str(b[0]),str(b[1])),(4,theta,c,cx,cz)]:
        ex('T'+str(i)+'x',f'{xx}-cos({t})*({p[0]:.16g})+sin({t})*({p[1]:.16g})')
        ex('T'+str(i)+'z',f'{zz}-sin({t})*({p[0]:.16g})-cos({t})*({p[1]:.16g})')
    ref=lambda alias:s.Name+'.'+letter+alias
    worldang=ref('Theta') if frame=='B' else '-'+ref('Theta')
    tx=ref('T4z') if frame=='B' else ref('T4x')
    ty='-'+ref('T4x') if frame=='B' else '-'+ref('T4z')
    mx,my=mount
    moving=doc.addObject('App::Part','PortaIndependenteR04');simple.addObject(moving);moving.Label='Porta '+letter+' - dobradicas independentes'
    moving.setExpression('Placement.Base.x',f'({mx}+({tx})-{mx}*cos({worldang})+({my})*sin({worldang}))*1 mm')
    moving.setExpression('Placement.Base.y',f'({my}+({ty})-{mx}*sin({worldang})-({my})*cos({worldang}))*1 mm')
    moving.setExpression('Placement.Rotation.Angle',worldang)
    if frame=='A':base=(376,-650,1);dims=(271,18,306);color=(.17,.47,.57)
    else:base=(232,-1047,1);dims=(18,271,306);color=(.81,.55,.25)
    board=box(moving,'PainelSimplesR04','Porta '+letter+' - painel proposto',base,dims,color)
    cutters=[]
    for level in [51,255]:
        hole=doc.addObject('Part::Cylinder','FuroSimplesR04');moving.addObject(hole);hole.Radius=17.5;hole.Height=13
        center=(625.5,-632,level) if frame=='A' else (232,-1025.5,level)
        axis=App.Vector(0,-1,0) if frame=='A' else App.Vector(1,0,0)
        hole.Placement=App.Placement(App.Vector(*center),App.Rotation(App.Vector(0,0,1),axis));cutters.append(hole)
    tool=doc.addObject('Part::MultiFuse','UsinagemSimplesR04');moving.addObject(tool);tool.Shapes=cutters
    front=doc.addObject('Part::Cut','FrenteSimplesR04');moving.addObject(front);front.Base=board;front.Tool=tool;front.Label='Porta '+letter+' - canecos comuns';front.ViewObject.ShapeColor=color;fronts.append(front)
    if frame=='A':matrix=App.Rotation(App.Vector(1,0,0),90).toMatrix()
    else:
        matrix=App.Matrix();matrix.A11=0;matrix.A12=0;matrix.A13=1;matrix.A21=-1;matrix.A22=0;matrix.A23=0;matrix.A31=0;matrix.A32=-1;matrix.A33=0
    for level in [51,255]:
        assembly=doc.addObject('App::Part','DobradicaSimplesR04');simple.addObject(assembly)
        assembly.Label='71B3550 - porta '+letter+' - nivel '+str(level);assembly.Placement.Base=App.Vector(mx,my,level)
        for i,source_part in enumerate(parts):
            o=feature(assembly,'71B3550 '+letter+' - corpo '+str(i),source_part,matrix);o.addProperty('App::PropertyInteger','IndiceCorpo');o.IndiceCorpo=i
            if i in [2,3,4]:
                t='Theta' if i==4 else 'Theta'+str(i)
                o.setExpression('Placement.Base.x',(ref('T'+str(i)+'z') if frame=='B' else ref('T'+str(i)+'x'))+' *1 mm')
                o.setExpression('Placement.Base.y','-'+ref('T'+str(i)+('x' if frame=='B' else 'z'))+' *1 mm')
                o.setExpression('Placement.Rotation.Angle',ref(t) if frame=='B' else '-'+ref(t))
        feature(assembly,'173H7100 - calco da porta '+letter,plate,matrix)
    doc.recompute()
    for o in cutters+[board,tool]:o.ViewObject.Visibility=False
    front.ViewObject.Visibility=True
box(simple,'ApoioPortaBR04','Lateral 18 mm de apoio da porta B - proposta',(18,-1050,18),(212,18,272),(.75,.66,.48))
box(simple,'FaixaQuinaAR04','Faixa fixa A 142 mm - proposta',(232,-650,1),(142,18,306),(.75,.66,.48))
box(simple,'FaixaQuinaBR04','Faixa fixa B 124 mm - proposta',(232,-774,1),(18,124,306),(.75,.66,.48))
corner.ModeloDeMovimento='R04: duas portas independentes com dobradicas comuns e faixa fixa na quina; curso de estudo86 com limitador candidato70T3553.'
doc.recompute();doc.save()
Gui.activeDocument().activeView().viewAxonometric();Gui.activeDocument().activeView().fitAll();Gui.updateGui()
report={'file':str(dest),'joints':{'a':a,'b':b,'c':c,'d':d},'branch':sign,'new_fronts_mm':{'A':[271,306,18],'B':[271,306,18]},'fixed_corner_mm':[142,124],'adjacent_strip_mm':25,'objects':len(doc.Objects),'invalid':[o.Name for o in doc.Objects if 'Invalid' in o.State],'status':'Proposta simples ainda em conferencia; sem liberacao de corte.'}
((Path(__file__).resolve().parent / '../Canto_simples_R04/Montagem_simples.json').resolve()).write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
result=json.dumps(report,ensure_ascii=False)
