from pathlib import Path
from datetime import datetime
import json,shutil
import FreeCAD as App
import Part

root=(Path(__file__).resolve().parent / '.').resolve();root.mkdir(exist_ok=True)
src=(Path(__file__).resolve().parent / '../Gavetas_R05_2026-10-13/Guedala_Park_R05_Caixas_Gavetas.FCStd').resolve()
original=next((d for d in App.listDocuments().values() if d.FileName and Path(d.FileName).resolve()==(Path(__file__).resolve().parent / '../Gavetas_R05_2026-10-13/Guedala_Park_R05_Caixas_Gavetas.FCStd').resolve()),None)
if original is None:original=App.openDocument(str(src))
original.save();dest=(Path(__file__).resolve().parent / 'Guedala_Park_R06_G2_Simples.FCStd').resolve()
if dest.exists():dest=dest.with_stem(dest.stem+'_'+datetime.now().strftime('%Y%m%d_%H%M%S'))
shutil.copy2(src,dest);doc=App.openDocument(str(dest));App.setActiveDocument(doc.Name)
doc.Label='Guedala Park - R06 - bandejas removiveis simples de G2'
g=next(o for o in doc.Objects if o.Label=='G2 · utensílios' and hasattr(o,'Extensao'))
floor=next(o for o in g.Group if o.Label.startswith('Fundo da caixa'))
program=json.loads(((Path(__file__).resolve().parent / '../../../Compatibilizacao_2026-10-03/Resultados_tampas_g2.json').resolve()).read_text(encoding='utf-8'))['g2']
trays=[];contents=[];wood=[];rows=[]
labels={'long':['Concha','Escumadeira','Espátula lisa','Espátula vazada','Peneira pequena'],
        'wide':['Frigideira Turim20 - candidata','Espremedor de alho - limite','Espremedor de cítricos - limite','Ralador plano - limite']}
def box(parent,label,base,size,color):
    o=doc.addObject('Part::Box','OrganizadorG2R06');parent.addObject(o);o.Label=label;o.Placement.Base=App.Vector(*base)
    o.Length,o.Width,o.Height=size;o.ViewObject.ShapeColor=color;return o
for kind,x,w in [('long',5,200),('wide',210,312)]:
    tray=doc.addObject('App::Part','BandejaG2R06');g.addObject(tray)
    tray.Label='Bandeja removivel '+('utensílios longos' if kind=='long' else 'frigideira e acessórios')+' - proposta455'
    tray.Placement.Base=App.Vector(floor.Placement.Base.x+x,floor.Placement.Base.y+2.5,floor.Placement.Base.z+float(floor.Height))
    tray.addProperty('App::PropertyString','Status');tray.Status='Bandeja455 mm, paredes/fundo4 como hipótese; pega, rigidez e materiais pendentes.'
    trays.append(tray)
    wood.extend([box(tray,'Fundo bandeja '+kind,(0,0,0),(w,455,4),(.76,.69,.55)),
        box(tray,'Parede esquerda bandeja '+kind,(0,0,4),(4,455,35),(.76,.69,.55)),
        box(tray,'Parede direita bandeja '+kind,(w-4,0,4),(4,455,35),(.76,.69,.55)),
        box(tray,'Parede frontal bandeja '+kind,(4,0,4),(w-8,4,35),(.76,.69,.55)),
        box(tray,'Parede posterior bandeja '+kind,(4,451,4),(w-8,4,35),(.76,.69,.55))])
    for index,item in enumerate(program[kind]):
        px,py,pz=[item[k]*10 for k in ['x','y','z']]
        if kind=='wide' and index==3:py=370 # 2 mm forward, retaining the same item and size
        if kind=='wide':pz+=4
        size=[item[k]*10 for k in ['w','d','h']]
        o=box(tray,labels[kind][index],(px+4,py+4,pz),size,(.43,.65,.63) if kind=='long' else (.72,.48,.33))
        o.addProperty('App::PropertyString','Status');o.Status='Gabarito do programa: não é produto medido nem geometria do utensílio real.'
        contents.append(o)
        margins=[px,w-8-px-size[0],py,447-py-size[1]]
        rows.append({'item':o.Label,'source_name':item['name'],'tray':kind,'size_mm':size,'position_inside_mm':[px,py,pz],
            'planar_margins_mm':margins,'rear_position_shift_mm':-2 if kind=='wide' and index==3 else 0,
            'estimated_vertical_margin_with10mm_allowance':116.5-pz-size[2]-10})
doc.recompute()
def shape(o):
    r=o.Shape.copy();r.Placement=o.getGlobalPlacement();return r
def common(a,b):
    x,y=a.BoundBox,b.BoundBox
    if any(getattr(x,k+'Max')<=getattr(y,k+'Min')+1e-7 or getattr(y,k+'Max')<=getattr(x,k+'Min')+1e-7 for k in ['X','Y','Z']):return 0
    return a.common(b).Volume
hits=[]
for o in contents:
    for w in wood:
        vol=common(shape(o),shape(w))
        if vol>.1:hits.append({'item':o.Label,'wood':w.Label,'volume_mm3':vol})
for i,o in enumerate(contents):
    for p in contents[i+1:]:
        vol=common(shape(o),shape(p))
        if vol>.1:hits.append({'pair':[o.Label,p.Label],'volume_mm3':vol})
report={'file':str(dest),'floor_mm':[float(floor.Length),float(floor.Width)],'tray_outer_mm':[[200,455],[312,455]],
    'tray_inner_mm':[[192,447],[304,447]],'front_rear_gap_each_mm':2.5,'side_gaps_mm':[5,5,19],
    'items':rows,'item_count':len(contents),'collisions':hits,'invalid_shapes':[o.Name for o in wood+contents if not o.Shape.isValid()],
    'scope':'Nove gabaritos, oito utensílios e frigideira candidata. Cotas propostas, não lista de corte. Altura116.5 e planejamento; corrediça superior real ainda nao montada.'}
doc.save();((Path(__file__).resolve().parent / 'Bandejas_G2_R06.json').resolve()).write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
result=json.dumps(report,ensure_ascii=False)
