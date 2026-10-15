"""Current adopted-result dimensions for review. Does not recompute or mutate CAD."""
import FreeCAD as App
from pathlib import Path
import json,hashlib,math,time
root=(Path(__file__).resolve().parent / '.').resolve();base=(Path(__file__).resolve().parent / '../..').resolve();d=App.ActiveDocument
file=(Path(__file__).resolve().parent / '../Folga_teto_R28_2026-10-14/Guedala_Park_R28_Folga_Teto_Proposta.FCStd').resolve()
assert Path(d.FileName).resolve()==(Path(__file__).resolve().parent / '../Folga_teto_R28_2026-10-14/Guedala_Park_R28_Folga_Teto_Proposta.FCStd').resolve()
t=time.monotonic();manifest=json.loads(((Path(__file__).resolve().parent / '../Auditoria_implantacao_R23_2026-10-14/Manifesto_implantacao_R23.json').resolve()).read_text(encoding='utf-8'))
selected={r['name']:r for r in manifest['items'] if r['adoption_scope']=='adopted_result'}
for n in ['Peca127','Peca128','Peca358','Peca107']:selected.pop(n,None)
for n in ['PainelCabeceiraR25','PainelCabeceiraR001']:selected[n]={'source_root':'CabeceiraDoisPaineisR25'}
rows=[];issues=[]
for n,r in selected.items():
    o=d.getObject(n);s=o.Shape.copy();s.Placement=o.getGlobalPlacement();b=s.BoundBox
    bounds=[7400-b.XMax,b.YMin,b.ZMin,7400-b.XMin,b.YMax,b.ZMax]
    dimensions=[b.XLength,b.YLength,b.ZLength]
    numeric={}
    for p in ['Length','Width','Height','Radius','Radius1','Radius2','Comprimento','Profundidade','Altura','Chapa','Fundo','Frente']:
        if p in o.PropertiesList and hasattr(getattr(o,p),'Value'):numeric[p]=getattr(o,p).Value
    if not all(math.isfinite(x) for x in bounds+dimensions) or min(dimensions)<=0:issues.append({'object':n,'kind':'nonfinite_or_nonpositive_bbox'})
    rows.append({'object':n,'label':o.Label,'root':r['source_root'],'type':o.TypeId,'native_dimensions_mm':numeric,'world_mirrored_bbox_mm':bounds,'world_bbox_size_mm':dimensions,'expressions':list(o.ExpressionEngine)})
inventory=json.loads(((Path(__file__).resolve().parent / '../Rotulos_R23_2026-10-14/Inventario_modulos_R23.json').resolve()).read_text(encoding='utf-8'))
modules=[]
for row in inventory['modules']:
    o=d.getObject(row['object']);props={p:float(getattr(o,p).Value) for p in row['cad_body_dimensions_mm']}
    if props!=row['cad_body_dimensions_mm']:issues.append({'object':o.Name,'kind':'inventory_dimension_difference','expected':row['cad_body_dimensions_mm'],'current':props})
    members=[r for r in rows if r['root']==o.Name]
    bbox=[min(r['world_mirrored_bbox_mm'][i] for r in members) for i in range(3)]+[max(r['world_mirrored_bbox_mm'][i] for r in members) for i in range(3,6)]
    expr=dict(o.ExpressionEngine);sheet_values={}
    for p in props:
        expression=expr.get(p,expr.get('.'+p,''))
        if expression.count('.')==1:
            sn,sp=expression.split('.');sheet=d.getObject(sn);value=getattr(sheet,sp);value=float(value.Value if hasattr(value,'Value') else value)
            sheet_values[p]=value
            if abs(value-props[p])>1e-7:issues.append({'object':o.Name,'kind':'spreadsheet_disagreement','property':p})
    modules.append({'object':o.Name,'label':o.Label,'body_dimensions_mm':props,'sheet_dimensions_mm':sheet_values,'adopted_solid_count':len(members),'closed_adopted_bbox_mirrored_mm':bbox,'placement_base_source_mm':list(o.Placement.Base),'limitations':'Body properties, not cut sizes; adopted envelope may include fronts/hardware/content or omit external accessories.'})
report={'file':str(file),'sha256':hashlib.sha256(file.read_bytes()).hexdigest(),'objects_in_document':len(d.Objects),'adopted_shapes':len(rows),'modules':modules,'items':rows,'issues':issues,'elapsed_seconds':time.monotonic()-t,'method':'Read current adopted shapes and native numeric dimensions, compare20module body properties to inventory and live spreadsheet aliases; common mirror X=7400-X. No movement, boolean, geometry validity rerun, recompute or save.'}
((Path(__file__).resolve().parent / 'Medidas_atual_R28.json').resolve()).write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
result={'adopted_shapes':len(rows),'modules':len(modules),'issues':issues,'seconds':report['elapsed_seconds'],'sha256':report['sha256']}
