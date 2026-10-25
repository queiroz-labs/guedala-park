from pathlib import Path
import json,math
import FreeCAD as App
import FreeCADGui as Gui
import Part

root=(Path(__file__).resolve().parent / '.').resolve()
doc=next(d for d in App.listDocuments().values() if d.FileName and Path(d.FileName).name=='Guedala_Park_R03_Ferragens_Canto.FCStd')
inspection=App.getDocument('Blum_Inspecao_Articulacoes')
controls=next(o for o in doc.Objects if o.Name.startswith('ControleCanto'))
def baked(source,angle):
    s=source.Shape.transformGeometry(source.Shape.Placement.toMatrix())
    s.Placement=App.Placement()
    return s.transformGeometry(App.Rotation(App.Vector(1,0,0),angle).toMatrix())
for o in doc.Objects:
    source=None;angle=90
    if o.Label.startswith('71T7550 - corpo '):
        i=o.IndiceCorpo;source=inspection.getObject('Part__Feature'+('' if i==0 else str(i).zfill(3)))
    elif o.Label.startswith('79T8500 - corpo '):
        source=inspection.getObject('Part__Feature'+str(7+o.IndiceCorpo).zfill(3));angle=-90
    elif o.Name.startswith('CalcoPrincipalR03'):source=inspection.getObject('Part__Feature011')
    elif o.Name.startswith('CalcoUniaoR03'):source=inspection.getObject('Part__Feature011');angle=-90
    elif o.Name.startswith('LimitadorR03'):source=inspection.getObject('Part__Feature012')
    if source:
        o.Shape=baked(source,angle)
        o.Placement=App.Placement()
doc.recompute()
App.setActiveDocument(doc.Name)
def globalshape(o):
    s=o.Shape.copy();s.Placement=o.getGlobalPlacement();return s
front=next(o for o in doc.Objects if o.Name.startswith('FrenteAComCanecos'))
B=next(o for o in doc.Objects if o.Label.startswith('Frente articulada B'))
hardware=[o for o in doc.Objects if o.Name.startswith(('PrincipalCorpoR03','UniaoCorpoR03','CalcoPrincipalR03','CalcoUniaoR03','LimitadorR03'))]
wall=next(o for o in doc.Objects if o.Name.startswith('LateralApoioPrincipal'))
g=next(o for o in doc.Objects if o.Name.startswith('FaixaFixaEstudo'))
neighbour_group=next(o for o in doc.Objects if o.TypeId=='App::Part' and hasattr(o,'Abertura') and o.ExpressionEngine and any('Vizinha' in ex for prop,ex in o.ExpressionEngine))
neighbour=next(o for o in neighbour_group.Group if o.TypeId=='Part::Box')
maleiro=next(o for o in doc.Objects if o.Label.startswith('Maleiro reto') and o.TypeId=='App::Part')
maleirofronts=[o for o in maleiro.Group if hasattr(o,'Shape') and o.Label.startswith('Frente de correr')]
poses=[]
for label,a,b,n in [('Fechado',0,0,0),('Inicio',1,0,0),('Vizinha_critica',24.25,0,24),('Intermediario',45,30,45),('Principal_aberta',92,0,0),('Conjugado_aberto',92,60,90)]:
    controls.set('B2',str(a)+' deg');controls.set('B3',str(b)+' deg');controls.set('B4',str(n)+' deg');doc.recompute()
    Ashape=globalshape(front);Bshape=globalshape(B);wood=globalshape(wall)
    internal=[]
    for o in hardware:
        s=globalshape(o)
        for name,target in [('A',Ashape),('B',Bshape),('lateral',wood)]:
            volume=s.common(target).Volume
            if volume>1e-3:internal.append({'part':o.Label,'target':name,'volume_mm3':round(volume,5)})
    targets=[('vizinha',globalshape(neighbour)),('faixa',globalshape(g))]+[(o.Label,globalshape(o)) for o in maleirofronts]
    collisions=[];distances={}
    for name,s in targets:
        volume=Ashape.common(s).Volume+Bshape.common(s).Volume
        if volume>1e-3:collisions.append({'target':name,'volume_mm3':round(volume,5)})
        distances[name]=min(Ashape.distToShape(s)[0],Bshape.distToShape(s)[0])
    poses.append({'name':label,'requested_alpha_deg':a,'real_alpha_deg':float(controls.PrincipalReal),
                  'beta_deg':b,'neighbour_ideal_deg':n,'front_collisions':collisions,
                  'hardware_wood_collisions':internal,'distance_mm':distances,
                  'invalid':[o.Name for o in doc.Objects if 'Invalid' in o.State]})
    Gui.activeDocument().activeView().viewAxonometric();Gui.activeDocument().activeView().fitAll();Gui.updateGui()
    Gui.activeDocument().activeView().saveImage(str(root/(label+'_R03.png')),1600,1000,'White')
controls.set('B2','0 deg');controls.set('B3','0 deg');controls.set('B4','0 deg');doc.recompute();doc.save()
report={'poses':poses,'scope':'Principal multilink reconstruida. Uniao com ajuste travado. Vizinha ainda com giro ideal nesta etapa; nao certificar sua trajetória real.',
        'invalid':[o.Name for o in doc.Objects if 'Invalid' in o.State]}
((Path(__file__).resolve().parent / 'Conferencia_montagem.json').resolve()).write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
result=json.dumps(report,ensure_ascii=False)
