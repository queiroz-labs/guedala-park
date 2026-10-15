from pathlib import Path
import json
import FreeCAD as App

root=(Path(__file__).resolve().parent / '.').resolve()
doc=next(d for d in App.listDocuments().values() if d.FileName and Path(d.FileName).name=='Guedala_Park_R03_Ferragens_Canto.FCStd')
s=next(o for o in doc.Objects if o.Name.startswith('ControleCanto'))
N=next(o for o in doc.Objects if o.Name.startswith('VizinhaComCanecosR03'))
ng=next(o for o in doc.Objects if o.TypeId=='App::Part' and o.Label.startswith('71B3650 - quatro barras'))
arms=[o for o in ng.Group if hasattr(o,'IndiceCorpo') and o.IndiceCorpo in [2,3]]
mg=next(o for o in doc.Objects if o.TypeId=='App::Part' and o.Label.startswith('71T7550 - bracos reconstruidos'))
stop=next(o for o in mg.Group if o.Label.startswith('70T7553.09 - montagem'))
mb=[o for o in mg.Group if hasattr(o,'IndiceCorpo') and o.IndiceCorpo not in [0,1,6]]

def world(o):
    v=o.Shape.copy();v.Placement=o.getGlobalPlacement();return v
def overlaps(a,b):
    x,y=a.BoundBox,b.BoundBox
    if any(getattr(x,k+'Max')<=getattr(y,k+'Min')+1e-7 or getattr(y,k+'Max')<=getattr(x,k+'Min')+1e-7 for k in ['X','Y','Z']):return 0
    return a.common(b).Volume
def evaluate(mode,angle):
    s.set('B2',str(angle if mode=='principal' else 0)+' deg')
    s.set('B4',str(angle if mode=='vizinha' else 0)+' deg')
    doc.recompute()
    a=world(stop if mode=='principal' else N)
    bodies=mb if mode=='principal' else arms
    return {'angle_deg':angle,'volume_mm3':sum(overlaps(a,world(b)) for b in bodies),
            'min_gap_mm':min(a.distToShape(world(b))[0] for b in bodies)}
def threshold(mode,lo,hi,volume):
    for unused in range(18):
        mid=(lo+hi)/2
        if evaluate(mode,mid)['volume_mm3']>volume:hi=mid
        else:lo=mid
    return {'threshold_volume_mm3':volume,'last_below_deg':lo,'first_above_deg':hi}

s.set('B3','0 deg');s.set('B5','150 mm');s.set('B130','6.5 mm');doc.recompute()
report={'scope':'Uma das duas dobradiças em cada sistema; montagens simétricas. Curso nominal do modelo; regulagens travadas. Limitador montado por inferência.',
        'vizinha':[evaluate('vizinha',a) for a in [0,60,80,86,90,95,100,105,110]],
        'principal':[evaluate('principal',a) for a in [0,60,80,86,90,91,92]],
        'thresholds':{'vizinha':[threshold('vizinha',90,110,v) for v in [0.001,0.1]],
                      'principal':[threshold('principal',80,92,v) for v in [0.001,0.1]]}}
s.set('B2','0 deg');s.set('B3','0 deg');s.set('B4','0 deg');doc.recompute();doc.save()
((Path(__file__).resolve().parent / 'Primeiro_contato.json').resolve()).write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
result=json.dumps(report,ensure_ascii=False)
