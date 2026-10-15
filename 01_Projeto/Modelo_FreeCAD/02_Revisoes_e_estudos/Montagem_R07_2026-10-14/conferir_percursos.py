from pathlib import Path
import json
import FreeCAD as App
import Part
root=(Path(__file__).resolve().parent / '.').resolve()
doc=next(d for d in App.listDocuments().values() if d.FileName and Path(d.FileName).name=='Guedala_Park_R07_Montagem_G2.FCStd')
g=next(o for o in doc.Objects if o.Label=='G2 · utensílios' and hasattr(o,'Extensao'))
module=next(o for o in g.InList if o.TypeId=='App::Part')
room=next(o for o in module.InList if o.Name.startswith('Ambiente_'))
trays=[o for o in g.Group if o.Label.startswith('Bandeja removivel')]
bases={o.Name:App.Vector(o.Placement.Base) for o in trays}
def shape(o):
    r=o.Shape.copy();r.Placement=o.getGlobalPlacement();return r
def common(a,b):
    x,y=a.BoundBox,b.BoundBox
    if any(getattr(x,k+'Max')<=getattr(y,k+'Min')+1e-7 or getattr(y,k+'Max')<=getattr(x,k+'Min')+1e-7 for k in ['X','Y','Z']):return 0
    return a.common(b).Volume
def swept(shape,delta):
    # Exact for the axis aligned boxes used here and one-axis translation.
    b=shape.BoundBox
    lo=[b.XMin+min(0,delta.x),b.YMin+min(0,delta.y),b.ZMin+min(0,delta.z)]
    size=[b.XLength+abs(delta.x),b.YLength+abs(delta.y),b.ZLength+abs(delta.z)]
    return Part.makeBox(*size,App.Vector(*lo))
static=[o for o in module.Group if o.TypeId=='Part::Box']
static += [o for sibling in module.Group if sibling.TypeId=='App::Part' and sibling!=g for o in sibling.Group if o.TypeId=='Part::Box']
static += [o for o in room.Group if o.TypeId=='Part::Box' and o.Label.startswith('Bancada cozinha')]
contents=[o for t in trays for o in t.Group if o.TypeId=='Part::Box']
g.Extensao=0;doc.recompute()
opening=[]
for o in contents:
    s=swept(shape(o),App.Vector(0,-500,0))
    for p in static:
        vol=common(s,shape(p))
        if vol>.1:opening.append({'moving':o.Label,'obstacle':p.Label,'volume_swept_mm3':vol})
g.Extensao=500;doc.recompute()
operations=[]
for t in trays:
    obstacles=static+[o for o in g.Group if hasattr(o,'Fonte') and '[3B0R-' in o.Label]+[o for other in trays if other!=t for o in other.Group if o.TypeId=='Part::Box']
    segments=[]
    for label,delta in [('elevar120',App.Vector(0,0,120)),('avancar40',App.Vector(0,-40,0)),('elevarmais100',App.Vector(0,0,100))]:
        hits=[]
        for o in t.Group:
            if o.TypeId!='Part::Box':continue
            s=swept(shape(o),delta)
            for p in obstacles:
                vol=common(s,shape(p))
                if vol>.1:hits.append({'moving':o.Label,'obstacle':p.Label,'volume_swept_mm3':vol})
        segments.append({'segment':label,'delta_mm':[delta.x,delta.y,delta.z],'hits':hits})
        t.Placement.Base=t.Placement.Base+delta;doc.recompute()
    operations.append({'tray':t.Label,'segments':segments})
    t.Placement.Base=bases[t.Name];doc.recompute()
g.Extensao=0;doc.recompute();doc.save()
report={'opening500_continuous_swept_envelope_hits':opening,'removal_loaded':operations,
    'method':'Envoltorias varridas ao longo de cada translacao axial. Para os gabaritos retangulares alinhados, abrangem todo segmento, nao apenas amostras.',
    'scope':'Geometria rigida nominal; nao inclui mãos, pega, peso, flexão, regulagem de corrediças ou objetos reais. Retirada pressupõe gaveta totalmente aberta. Caminho ilustrativo reversivel, nao validacao ergonômica.'}
((Path(__file__).resolve().parent / 'Percursos_G2_R07.json').resolve()).write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
result=json.dumps(report,ensure_ascii=False)
