from pathlib import Path
import json
import FreeCAD as App

root=(Path(__file__).resolve().parent / '.').resolve()
doc=next(d for d in App.listDocuments().values() if d.FileName and Path(d.FileName).name=='Guedala_Park_R05_Caixas_Gavetas.FCStd')
def shape(o):
    r=o.Shape.copy();r.Placement=o.getGlobalPlacement();return r
def common(a,b):
    x,y=a.BoundBox,b.BoundBox
    if any(getattr(x,k+'Max')<=getattr(y,k+'Min')+1e-7 or getattr(y,k+'Max')<=getattr(x,k+'Min')+1e-7 for k in ['X','Y','Z']):return 0
    return a.common(b).Volume
office=next(o for o in doc.Objects if o.TypeId=='App::Part' and o.Label=='Gaveteiro do escritório')
office.Placement=App.Placement(App.Vector(3100,700,480),App.Rotation(App.Vector(0,0,1),180))
if 'CorrecaoOrientacaoR05' not in office.PropertiesList:office.addProperty('App::PropertyString','CorrecaoOrientacaoR05','Conferencia R05')
office.CorrecaoOrientacaoR05='Mesmo envelope fechado; abertura para centro do quarto conforme R10. A antiga orientacao abriu para parede.'
drawers=[o for o in doc.Objects if hasattr(o,'NLProposto')]
ward=next(o for o in doc.Objects if o.TypeId=='App::Part' and o.Label.startswith('Guarda-roupa'))
right=next(o for o in ward.Group if o.Label=='Porta de correr inferior 2')
right.setExpression('Placement.Base.x','985 mm - Deslocamento')
for o in drawers:o.Extensao=0
doc.recompute()
rows=[]
walls=[o for o in doc.Objects if o.Label.startswith('Parede ·') and o.TypeId=='Part::Box']
for g in drawers:
    module=next(o for o in g.InList if o.TypeId=='App::Part')
    own=[o for o in g.Group if o.TypeId=='Part::Box']
    structure=[o for o in module.Group if o.TypeId=='Part::Box']
    others=[o for sibling in module.Group if sibling.TypeId=='App::Part' and sibling!=g for o in sibling.Group if o.TypeId=='Part::Box']
    sliding=[o for o in module.Group if hasattr(o,'Deslocamento')]
    for o in sliding:o.Deslocamento=0
    if sliding:
        if g.Placement.Base.x<1000:sliding[0].Deslocamento=985
        else:sliding[1].Deslocamento=985
    room=next((o for o in module.InList if o.Name.startswith('Ambiente_')),None)
    furniture=[o for o in room.Group if o.TypeId=='Part::Box' and o.Label.startswith(('Cama','Sofá','Bancada de trabalho'))] if room else []
    paths=[]
    travel=int(float(g.NLProposto))
    for amount in sorted(set(list(range(0,travel+1,25))+[int(float(g.CursoNominal))])):
        g.Extensao=amount;doc.recompute()
        obstacles=[(o.Label,shape(o)) for o in structure+others+walls+furniture]
        hits=[]
        for o in own:
            a=shape(o)
            for label,b in obstacles:
                vol=common(a,b)
                if vol>.1:hits.append({'moving':o.Label,'obstacle':label,'volume_mm3':vol})
        front=next(o for o in own if o.Label.startswith('Frente'));f=shape(front)
        paths.append({'extension_mm':amount,'hits':hits,'front_global_Y_mm':[f.BoundBox.YMin,f.BoundBox.YMax]})
    internal=[]
    for i,o in enumerate(own):
        for p in own[i+1:]:
            vol=common(shape(o),shape(p))
            if vol>.1:internal.append({'pair':[o.Label,p.Label],'volume_mm3':vol})
    rows.append({'name':g.Name,'drawer':g.Label,'virtual_sliding_door_opened':bool(sliding),'internal_box_hits':internal,'paths':paths,
                 'invalid_individual_pieces':[o.Name for o in own if not o.Shape.isValid()]})
    g.Extensao=0
    for o in sliding:o.Deslocamento=0
    doc.recompute()
doc.save()
report={'scope':'Translacao rigida de caixas e frentes em passos25 mm. Corrediças reais ainda nao montadas. Portas de correr do roupeiro abertas por deslocamento ideal, ferragem real pendente. Sofa diario simplificado; nao valida cama preparada, uso ou carga.',
    'office_orientation_fix':{'closed_footprint_mm':[2700,3100,250,700],'front_Y_closed_mm':700,'front_Y_open400_mm':1100,'prior_wall_intersection_at300_mm3':845352,'guest_bed_reference_starts_Y_mm':1100,'guest_scope':'Coincidencia em planta, nao margem de uso. Altura/roupa de cama nao verificadas.'},
    'drawers':rows}
((Path(__file__).resolve().parent / 'Conferencia_caixas_R05.json').resolve()).write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
result=json.dumps({'drawers':[{'name':r['drawer'],'tested_poses':len(r['paths']),'poses_with_hits':sum(bool(p['hits']) for p in r['paths']),'box_hits':r['internal_box_hits'],'invalid':r['invalid_individual_pieces']} for r in rows],'office':report['office_orientation_fix']},ensure_ascii=False)
