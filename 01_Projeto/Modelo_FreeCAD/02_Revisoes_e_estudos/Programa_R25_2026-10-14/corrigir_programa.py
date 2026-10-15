"""Restore mirror centering and the approved two-panel headboard representation."""
from pathlib import Path
import hashlib, json, shutil
import FreeCAD as App

root=(Path(__file__).resolve().parent / '.').resolve()
base=(Path(__file__).resolve().parent / '../Implantacao_R24_2026-10-14/Guedala_Park_R24_Implantacao_Corrigida.FCStd').resolve()
target=(Path(__file__).resolve().parent / 'Guedala_Park_R25_Programa_Conferido.FCStd').resolve()
base_hash=hashlib.sha256(base.read_bytes()).hexdigest()
assert base_hash=='b2382d8a66045e430a3bd21e54c60e00406f9949c3ad47428449be4362dd04f9'
assert not target.exists()
shutil.copy2(base,target)
d=App.openDocument(str(target))

def bb(s):
    b=s.BoundBox;return [b.XMin,b.YMin,b.ZMin,b.XMax,b.YMax,b.ZMax]
def shape(o):
    s=o.Shape.copy();s.Placement=o.getGlobalPlacement();return s
def snapshot(o):
    return {'placement':list(o.Placement.toMatrix().A) if 'Placement' in o.PropertiesList else None,
            'expressions':list(o.ExpressionEngine) if 'ExpressionEngine' in o.PropertiesList else None,
            'parents':sorted(p.Name for p in o.InList if p.isDerivedFrom('App::DocumentObjectGroup') or p.TypeId=='App::Part'),
            'visibility':o.ViewObject.Visibility,'linked':o.LinkedObject.Name if o.TypeId=='App::Link' else None}
before={o.Name:snapshot(o) for o in d.Objects}
report={'base':str(base),'file':str(target),'base_sha256_before':base_hash,'changes':[]}

mirror=d.getObject('Peca275')
assert mirror.TypeId=='Part::Box' and not mirror.ExpressionEngine and mirror.getParentGeoFeatureGroup() is None
report['mirror_before_bbox']=bb(shape(mirror))
assert report['mirror_before_bbox']==[2010.0,3350.0,200.0,2015.0,3850.0,2000.0]
p=mirror.Placement;p.Base.y+=15;mirror.Placement=p
report['mirror_after_bbox']=bb(shape(mirror))
report['mirror_centering']='Lateral composed at mirror height: Peca207 + ApoioReferenciaCorrerR001, Y3290..3940; center3615, mirror500 wide at3365..3865, margins75/75. Nominal geometry, not installation certification.'

old=d.getObject('Peca107')
assert old.TypeId=='Part::Box' and not old.ExpressionEngine and old.getParentGeoFeatureGroup() is None
old_shape=shape(old);old_bounds=bb(old_shape);old_volume=old_shape.Volume
old.Label='Histórico oculto — cabeceira anterior em bloco único'
link=next(o for o in d.Objects if o.TypeId=='App::Link' and o.Name.startswith('EspelhoPecaR') and o.LinkedObject==old)
old_link_shape=link.Shape.copy();old_link_bounds=bb(old_link_shape)
parents=[p for p in old.InList if p.TypeId=='App::DocumentObjectGroup']
assert len(parents)==1
source_group=parents[0]
pieces=[]
for i in range(2):
    o=d.addObject('Part::Box','PainelCabeceiraR25')
    o.Label='Cabeceira estofada — painel '+('A' if i==0 else 'B')+' — envelope ilustrativo'
    o.Length=old.Length;o.Width=float(old.Width)/2;o.Height=old.Height
    o.Placement=old.Placement.multiply(App.Placement(App.Vector(0,i*float(old.Width)/2,0),App.Rotation()))
    source_group.addObject(o)
    o.addProperty('App::PropertyString','Status','Estudo R25')
    o.Status='Dois painéis aprovados; divisão central apenas ilustrativa, sem junta/furação/corte definidos. Dimensões do envelope anterior preservadas.'
    o.ViewObject.ShapeColor=old.ViewObject.ShapeColor
    o.ViewObject.LineColor=old.ViewObject.LineColor
    o.ViewObject.Visibility=False
    pieces.append(o)
combined=d.addObject('Part::Compound','CabeceiraDoisPaineisR25')
combined.Label='Cabeceira estofada — dois painéis aprovados / envelope de estudo'
combined.Links=pieces
source_group.addObject(combined)
combined.ViewObject.ShapeColor=old.ViewObject.ShapeColor
combined.ViewObject.LineColor=old.ViewObject.LineColor
combined.ViewObject.Visibility=False
link.LinkedObject=combined
link.Label='Cabeceira estofada — dois painéis / R25'
d.recompute()
assert max(abs(a-b) for a,b in zip(bb(shape(combined)),old_bounds))<1e-5
assert abs(combined.Shape.Volume-old_volume)<1e-5
assert max(abs(a-b) for a,b in zip(bb(link.Shape),old_link_bounds))<1e-5
assert combined.Shape.isValid()
assert not [o.Name for o in d.Objects if 'Invalid' in o.State]
for name,s in before.items():
    changed=[k for k in s if snapshot(d.getObject(name))[k]!=s[k]]
    if changed:
        assert (name=='Peca275' and changed==['placement']) or (name==link.Name and changed==['linked']), (name,changed)
        report['changes'].append({'name':name,'fields':changed})
assert len(report['changes'])==2
report.update(headboard_source=old.Name,headboard_link=link.Name,new_panels=[o.Name for o in pieces],compound=combined.Name,
              source_group=source_group.Name,source_group_added_members=[o.Name for o in pieces]+[combined.Name],
              headboard_bbox_source=old_bounds,headboard_bbox_mirrored=bb(link.Shape),headboard_volume_mm3=old_volume,
              objects_before=len(before),objects_after=len(d.Objects),invalid=[],
              limits='Nominal CAD centering/visual division only. No new physical dimensions, cutout, panel joint, fixings, adhesive, loads or fabrication release.')
d.Label='Guedala Park — R25 — programa conferido'
d.save()
report['base_sha256_after']=hashlib.sha256(base.read_bytes()).hexdigest()
assert report['base_sha256_after']==base_hash
report['sha256']=hashlib.sha256(target.read_bytes()).hexdigest()
((Path(__file__).resolve().parent / 'Correcao_R25.json').resolve()).write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
App.setActiveDocument(d.Name)
