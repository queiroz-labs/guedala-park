from pathlib import Path
import json
import FreeCAD as App
root=(Path(__file__).resolve().parent / '.').resolve()
doc=globals().get('document') or next(d for d in App.listDocuments().values() if d.FileName and Path(d.FileName).name=='Guedala_Park_R05_Caixas_Gavetas.FCStd')
data=json.loads(((Path(__file__).resolve().parent / 'Caixas_dimensoes_R05.json').resolve()).read_text(encoding='utf-8'))
drawers=[o for o in doc.Objects if hasattr(o,'NLProposto')]
def overlaps(a0,a1,b0,b1):return min(a1,b1)>max(a0,b0)+1e-6
rows=[]
for g in drawers:
    m=next(p for p in g.InList if p.TypeId=='App::Part')
    floor=next(o for o in g.Group if o.Label.startswith('Fundo da caixa'))
    side=next(o for o in g.Group if o.Label.startswith('Lateral da caixa'))
    x=g.Placement.Base.x+floor.Placement.Base.x;y=g.Placement.Base.y+floor.Placement.Base.y
    xf=x+float(floor.Length);yf=y+float(floor.Width);top=g.Placement.Base.z+floor.Placement.Base.z+float(floor.Height)
    obstacles=[]
    for o in m.Group:
        if o.TypeId!='Part::Box' or float(o.Height)>30:continue
        ox,oy,oz=o.Placement.Base.x,o.Placement.Base.y,o.Placement.Base.z
        if oz>top and overlaps(x,xf,ox,ox+float(o.Length)) and overlaps(y,yf,oy,oy+float(o.Width)):
            obstacles.append({'name':o.Label,'underside_z_module_mm':oz,'type':'Madeira do modulo'})
    for other in m.Group:
        if other==g or not hasattr(other,'NLProposto'):continue
        of=next(o for o in other.Group if o.Label.startswith('Fundo da caixa'))
        ox=other.Placement.Base.x+of.Placement.Base.x;oy=other.Placement.Base.y+of.Placement.Base.y
        if overlaps(x,xf,ox,ox+float(of.Length)) and overlaps(y,yf,oy,oy+float(of.Width)):
            lower=other.Placement.Base.z+of.Placement.Base.z-28.5
            if lower>top:obstacles.append({'name':'Planejamento sob '+other.Label,'underside_z_module_mm':lower,'type':'Estimativa baseada no requisito28.5 mm; conferir corrediça superior real e regulagens'})
    if 'Gaveteiro G1' in m.Label:obstacles.append({'name':'Bancada no topo720 do modulo','underside_z_module_mm':720,'type':'Hipotese geometrica da bancada existente'})
    first=min(obstacles,key=lambda o:o['underside_z_module_mm'])
    clearance=first['underside_z_module_mm']-top
    walltop=g.Placement.Base.z+side.Placement.Base.z+float(side.Height)
    for name in ['AlturaParedeSobreFundo','VaoVerticalEstimado']:
        if name not in g.PropertiesList:g.addProperty('App::PropertyLength',name,'Conferencia R05')
    g.AlturaParedeSobreFundo=walltop-top;g.VaoVerticalEstimado=clearance;g.AlturaUtilProposta=clearance
    if 'VaoVerticalConservadorProposto' in g.PropertiesList:g.removeProperty('VaoVerticalConservadorProposto')
    row={'drawer':g.Label,'floor_top_z_module_mm':top,'wall_above_floor_mm':walltop-top,'estimated_clearance_to_first_obstacle_mm':clearance,'first_obstacle':first,
         'scope':'Altura acima das paredes da caixa pode ser utilizada; o limite e o primeiro obstaculo. Corrediça superior ainda representada por requisito minimo28.5 mm, nao STEP montado.'}
    if g.Label.startswith('G2'):
        row['content_height_requirement_mm']=111;row['estimated_margin_to_requirement_mm']=clearance-111
        row['organizer_depth_mm']={'existing_proposal':460,'floor_available':float(floor.Width),'status':'Coincidencia nominal sem folga; encurtar bandejas removiveis como proposta, conferir gabaritos.'}
    rows.append(row)
    record=next(r for r in data['drawers'] if r['name']==g.Name)
    record['candidate']['wall_above_floor_mm']=walltop-top
    record['candidate'].pop('usable_height_mm',None)
    record['candidate']['estimated_vertical_clearance_mm']=clearance
data['height_scope']='Alturas livres estimadas ate madeira ou envoltoria minima de corrediça superior; confirmar com montagem STEP e regulagens. Nao confundir parede da caixa com limite de armazenamento.'
doc.recompute();doc.save()
((Path(__file__).resolve().parent / 'Caixas_dimensoes_R05.json').resolve()).write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
((Path(__file__).resolve().parent / 'Alturas_R05.json').resolve()).write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
result=json.dumps(rows,ensure_ascii=False)
