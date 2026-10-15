from pathlib import Path
import json,math
import FreeCAD as App
import FreeCADGui as Gui

root=(Path(__file__).resolve().parent / '.').resolve()
doc=next(d for d in App.listDocuments().values() if d.FileName and Path(d.FileName).name=='Guedala_Park_R03_Ferragens_Canto.FCStd')
s=next(o for o in doc.Objects if o.Name.startswith('ControleCanto'))
corner=next(o for o in doc.Objects if o.Label.startswith('Canto integrado em L') and o.TypeId=='App::Part')
maleiro=next(o for o in doc.Objects if o.Label.startswith('Maleiro reto') and o.TypeId=='App::Part')
aerial=next(o for o in doc.Objects if o.Label.startswith('Aéreo raso da cabeceira') and o.TypeId=='App::Part')
room=next(o for o in doc.Objects if o.Name.startswith('Ambiente_quarto'))
for o in room.Group:o.ViewObject.Visibility=o in [corner,maleiro,aerial]
A=next(o for o in doc.Objects if o.Name.startswith('FrenteAComCanecos'))
B=next(o for o in doc.Objects if o.Label.startswith('Frente articulada B'))
N=next(o for o in doc.Objects if o.Name.startswith('VizinhaComCanecosR03'))
walls=[o for o in doc.Objects if o.Name.startswith(('LateralApoioPrincipal','DivisorApoioVizinhaR03'))]
fixed=next(o for o in doc.Objects if o.Name.startswith('FaixaFixaEstudo'))
hardware=[o for o in doc.Objects if hasattr(o,'Shape') and o.Label.startswith(('71T7550 - corpo ','79T8500 - corpo ','71B3650 - corpo ','173H7100 - calco','70T7553.09 - montagem'))]
maleirofronts=[o for o in maleiro.Group if hasattr(o,'Shape') and o.Label.startswith('Frente de correr')]
mainj=json.loads(((Path(__file__).resolve().parent / 'Parametros_expressões.json').resolve()).read_text())['joints']
nearj=json.loads(((Path(__file__).resolve().parent / 'Vizinha_parametros.json').resolve()).read_text())
def shape(o):
    r=o.Shape.copy();r.Placement=o.getGlobalPlacement();return r
def common(a,b):
    x,y=a.BoundBox,b.BoundBox
    if any(getattr(x,k+'Max')<=getattr(y,k+'Min')+1e-7 or getattr(y,k+'Max')<=getattr(x,k+'Min')+1e-7 for k in ['X','Y','Z']):return 0
    return a.common(b).Volume
def joints():
    rows=[]
    for group in [o for o in doc.Objects if o.TypeId=='App::Part' and o.Label.startswith('71T7550 - bracos reconstruidos')]:
        parts={o.IndiceCorpo:o for o in group.Group if hasattr(o,'IndiceCorpo')}
        for i,j,p in [(1,4,'a'),(1,6,'b'),(4,5,'c'),(5,6,'d'),(6,3,'e'),(3,2,'f'),(5,2,'g')]:
            x,z=mainj[p];v=App.Vector(x,-z,0)
            error=(parts[i].getGlobalPlacement().multVec(v)-parts[j].getGlobalPlacement().multVec(v)).Length
            rows.append(error)
    for group in [o for o in doc.Objects if o.TypeId=='App::Part' and o.Label.startswith('71B3650 - quatro barras')]:
        parts={o.IndiceCorpo:o for o in group.Group if hasattr(o,'IndiceCorpo')}
        for i,j,p in [(1,2,'a'),(1,3,'b'),(2,4,'c'),(3,4,'d')]:
            x,z=nearj[p];v=App.Vector(z,-x,0)
            rows.append((parts[i].getGlobalPlacement().multVec(v)-parts[j].getGlobalPlacement().multVec(v)).Length)
    for group in [o for o in doc.Objects if o.TypeId=='App::Part' and o.Label.startswith('79T8500 - caneco na A')]:
        cup=next(o for o in group.Group if hasattr(o,'IndiceCorpo') and o.IndiceCorpo==3)
        armgroup=next(o for o in group.Group if o.TypeId=='App::Part')
        link=next(o for o in armgroup.Group if hasattr(o,'IndiceCorpo') and o.IndiceCorpo==2)
        v=App.Vector(27,49.5,0)
        rows.append((cup.getGlobalPlacement().multVec(v)-link.getGlobalPlacement().multVec(v)).Length)
    return max(rows)
poses=[]
cases=[('Fechado',0,0,0,150),('Inicio',1,0,0,150),('Critico_simultaneo',24.25,0,25,150),
       ('Meio_curso',45,30,45,150),('Principal_aberta',92,0,90,150),('Abertura_completa',92,60,110,150),
       ('Alternativa_faixa200',25,0,25,200),('R01_sem_faixa',24.25,0,25,0)]
for label,alpha,beta,near,filler in cases:
    s.set('B2',str(alpha)+' deg');s.set('B3',str(beta)+' deg');s.set('B4',str(near)+' deg');s.set('B5',str(filler)+' mm');doc.recompute()
    fixed.ViewObject.Visibility=filler>0
    wood=[('A',shape(A)),('B',shape(B)),('vizinha',shape(N))]+[(o.Label,shape(o)) for o in walls]
    obstacles=[('faixa',shape(fixed))] if filler else []
    obstacles +=[(o.Label,shape(o)) for o in maleirofronts]
    collisions=[];gaps={}
    for i,(name,a) in enumerate(wood[:3]):
        for other,b in wood[i+1:]+obstacles:
            vol=common(a,b)
            if vol>1e-3:collisions.append({'pair':[name,other],'volume_mm3':round(vol,5)})
            gaps[name+' / '+other]=a.distToShape(b)[0]
    hardware_hits=[]
    for o in hardware:
        h=shape(o)
        for name,w in wood+obstacles:
            vol=common(h,w)
            if vol>1e-3:hardware_hits.append({'hardware':o.Label,'wood':name,'volume_mm3':round(vol,5)})
    stops=[]
    for group in [o for o in doc.Objects if o.TypeId=='App::Part' and o.Label.startswith('71T7550 - bracos reconstruidos')]:
        stop=next(o for o in group.Group if o.Label.startswith('70T7553.09 - montagem'))
        bodies=[o for o in group.Group if hasattr(o,'IndiceCorpo') and o.IndiceCorpo not in [0,1,6]]
        stops.append({'min_gap_mm':min(shape(stop).distToShape(shape(o))[0] for o in bodies),
                      'overlap_mm3':sum(common(shape(stop),shape(o)) for o in bodies)})
    record={'name':label,'alpha_requested_deg':alpha,'alpha_actual_deg':float(s.PrincipalReal),
        'beta_deg':beta,'near_deg':near,'filler_mm':filler,'front_collisions':collisions,
        'hardware_wood_collisions':hardware_hits,'max_joint_error_mm':joints(),
        'gaps_mm':gaps,'stop_attachment_inferred_body6':stops,
        'invalid':[o.Name for o in doc.Objects if 'Invalid' in o.State]}
    poses.append(record)
    Gui.activeDocument().activeView().viewAxonometric();Gui.activeDocument().activeView().fitAll();Gui.updateGui()
    Gui.activeDocument().activeView().saveImage(str(root/(label+'_CAD.png')),1600,1000,'White')
s.set('B2','0 deg');s.set('B3','0 deg');s.set('B4','0 deg');s.set('B5','150 mm');fixed.ViewObject.Visibility=True;doc.recompute();doc.save()
report={'poses':poses,'hardware_objects_checked':len(hardware),'mechanisms':{'main':'6 links / 7 axes inferred from STEP','fold':'CAD pivot with adjustment locked','neighbour':'4 links / 4 axes inferred from STEP'},
    'scope':'Sólidos CAD e mecanismos reconstruidos. Nao inclui extremos de regulagem, carga, tolerancias ou homologacao da Blum.',
    'new_geometry':'A/B396, caneco uniao12.5, suporte principal18, divisor vizinha18; variantes propostas.'}
((Path(__file__).resolve().parent / 'Auditoria_final_CAD.json').resolve()).write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
result=json.dumps({'poses':[{'name':p['name'],'front_hits':p['front_collisions'],'hardware_hits':p['hardware_wood_collisions'],'max_joint_error_mm':p['max_joint_error_mm'],'stop':p['stop_attachment_inferred_body6'],'invalid':p['invalid']} for p in poses]},ensure_ascii=False)
