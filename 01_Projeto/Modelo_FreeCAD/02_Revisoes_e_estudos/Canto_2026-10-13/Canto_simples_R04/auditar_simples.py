from pathlib import Path
import json
import FreeCAD as App
import FreeCADGui as Gui

root=(Path(__file__).resolve().parent / '.').resolve()
doc=next(d for d in App.listDocuments().values() if d.FileName and Path(d.FileName).name=='Guedala_Park_R04_Canto_Simples.FCStd')
s=next(o for o in doc.Objects if o.Name.startswith('ControleSimplesR04'))
old=next(o for o in doc.Objects if o.Name.startswith('ControleCanto'))
corner=next(o for o in doc.Objects if o.TypeId=='App::Part' and o.Label.startswith('Canto integrado em L'))
simple=next(o for o in corner.Group if o.Label.startswith('Canto R04 - portas independentes'))
A=next(o for o in doc.Objects if o.Label=='Porta A - canecos comuns')
B=next(o for o in doc.Objects if o.Label=='Porta B - canecos comuns')
N=next(o for o in doc.Objects if o.Name.startswith('VizinhaComCanecosR03'))
hardware=[o for o in doc.Objects if hasattr(o,'Shape') and o.Label.startswith(('71B3550 A - corpo','71B3550 B - corpo','173H7100 - calco da porta'))]
walls=[o for o in corner.Group+simple.Group if hasattr(o,'Shape') and o.TypeId in ['Part::Box','Part::Fuse'] and o.ViewObject.Visibility]
maleiro=next(o for o in doc.Objects if o.TypeId=='App::Part' and o.Label.startswith('Maleiro reto'))
near=[o for o in maleiro.Group if hasattr(o,'Shape') and o.ViewObject.Visibility]
def shape(o):
    r=o.Shape.copy();r.Placement=o.getGlobalPlacement();return r
def common(a,b):
    x,y=a.BoundBox,b.BoundBox
    if any(getattr(x,k+'Max')<=getattr(y,k+'Min')+1e-7 or getattr(y,k+'Max')<=getattr(x,k+'Min')+1e-7 for k in ['X','Y','Z']):return 0
    return a.common(b).Volume
cases=[('Fechado',0,0,0),('A_sozinha_1',1,0,0),('A_sozinha_15',15,0,0),('A_sozinha_45',45,0,0),('A_sozinha_86',86,0,0),
       ('B_sozinha_1',0,1,0),('B_sozinha_15',0,15,0),('B_sozinha_45',0,45,0),('B_sozinha_86',0,86,0),
       ('Ambas_15',15,15,0),('Ambas_30',30,30,0),('Critico_47_5',47.5,47.5,0),('Ambas_60',60,60,0),('Ambas_86',86,86,0),
       ('A15_B86',15,86,0),('A86_B15',86,15,0),('A45_B86',45,86,0),('A86_B45',86,45,0),
       ('Vizinha_simultanea',30,0,30),('Vizinha_e_B_abertas',86,86,86)]
rows=[]
for label,alpha,beta,gamma in cases:
    s.set('B2',str(alpha)+' deg');s.set('B3',str(beta)+' deg');old.set('B4',str(gamma)+' deg');doc.recompute()
    wood=[('A',shape(A)),('B',shape(B)),('vizinha',shape(N))]+[(o.Label,shape(o)) for o in walls+near]
    hits=[];gaps={}
    for i,(name,a) in enumerate(wood[:2]):
        for other,b in wood[i+1:]:
            vol=common(a,b)
            if vol>.1:hits.append({'pair':[name,other],'volume_mm3':vol})
            gaps[name+' / '+other]=a.distToShape(b)[0]
    fit=[]
    for o in hardware:
        h=shape(o)
        for name,w in wood:
            vol=common(h,w)
            if vol>.1:fit.append({'hardware':o.Label,'wood':name,'volume_mm3':vol})
    rows.append({'name':label,'angles_deg':[alpha,beta,gamma],'front_hits':hits,'hardware_hits':fit,'gaps_mm':gaps,'invalid':[o.Name for o in doc.Objects if 'Invalid' in o.State]})
    if label in ['Fechado','Ambas_86','Critico_47_5']:
        App.setActiveDocument(doc.Name);Gui.activeDocument().activeView().viewAxonometric();Gui.activeDocument().activeView().fitAll();Gui.updateGui()
        Gui.activeDocument().activeView().saveImage(str(root/(label+'.png')),1600,1000,'White')
s.set('B2','0 deg');s.set('B3','0 deg');old.set('B4','0 deg');doc.recompute();doc.save()
report={'hardware_count':len(hardware),'scope':'Geometria CAD nominal de proposta, sem regulagens extremas, tolerancias e carga. Interferencia reportada acima de 0.1 mm3. Suportes e dimensoes ainda propostas.','cases':rows}
((Path(__file__).resolve().parent / 'Auditoria_simples.json').resolve()).write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
result=json.dumps({'hardware_count':len(hardware),'cases':[{'name':r['name'],'front_hits':r['front_hits'],'hardware_hits':r['hardware_hits'],'invalid':r['invalid']} for r in rows]},ensure_ascii=False)
