"""Nova comparacao de REGIOES com a montagemG2 arquivada, sem repetir curso."""
from pathlib import Path
import json,hashlib
import FreeCAD as App,FreeCADGui as Gui
HERE=Path(__file__).resolve().parent
d=json.loads((HERE/'Intersecoes_localizadas.json').read_text(encoding='utf8'))
s=next(o for o in App.listDocuments().values()if Path(o.FileName).resolve()==Path(d['source']).resolve())
assert not Gui.getDocument(s.Name).Modified
def world(o):
 sh=o.Shape.copy();sh.Placement=o.getGlobalPlacement().multiply(o.Placement.inverse()).multiply(sh.Placement);return sh
def bounds(sh):
 b=sh.optimalBoundingBox();return [b.XMin,b.YMin,b.ZMin,b.XMax,b.YMax,b.ZMax]
floor=world(s.getObject('MontagemG2R019'));rows=[]
for name in ['MontagemG2R007','MontagemG2R014']:
 guide=world(s.getObject(name));hit=floor.common(guide)
 parts=[dict(volume_mm3=x.Volume,box_mm=bounds(x),valid=x.isValid())for x in hit.Solids if x.Volume>1e-7]
 assert all(x['valid']for x in parts)
 total=sum(x['volume_mm3']for x in parts)
 rows.append(dict(guide=name,label=s.getObject(name).Label,floor='MontagemG2R019',floor_box_mm=bounds(floor),
  compound_volume_mm3=hit.Volume,sum_positive_solids_mm3=total,compound_vs_solids_delta_mm3=hit.Volume-total,
  top_level_shape_types=[x.ShapeType for x in hit.childShapes()],components=parts))
bores=[]
for name in ['GavetaComumR074','GavetaComumR086']:
 sh=world(s.getObject(name));b=bounds(sh);holes=[]
 for f in sh.Faces:
  sf=f.Surface
  if type(sf).__name__=='Cylinder' and abs(sf.Radius-3)<1e-6 and abs(abs(sf.Axis.y)-1)<1e-6:
   c=sf.Center;bb=bounds(f)
   holes.append(dict(radius_mm=sf.Radius,center_mm=[c.x,c.y,c.z],axis=[sf.Axis.x,sf.Axis.y,sf.Axis.z],box_mm=bb,
    distance_from_nearest_bottom_side_edge_mm=min(c.x-b[0],b[3]-c.x),height_above_bottom_underside_mm=c.z-b[2],bore_depth_mm=bb[4]-bb[1]))
 assert len(holes)==2
 assert all(abs(h['height_above_bottom_underside_mm']-11)<1e-6 and abs(h['bore_depth_mm']-10)<1e-6 and abs(h['distance_from_nearest_bottom_side_edge_mm']-12)<1e-6 for h in holes)
 bores.append(dict(floor=name,holes=holes))
assert hashlib.sha256(Path(s.FileName).read_bytes()).hexdigest()==d['source_sha256'] and not Gui.getDocument(s.Name).Modified
(HERE/'Referencia_G2_e_furos_P16.json').write_text(json.dumps(dict(reference_regions=rows,P16_bores=bores,source_unchanged=True,
 scope='Regioes comparadas com G2 proveniente da configuracao oficial, nao homologacao individualP16. Furos nominais confirmados; causa fisica/parametros de regulagem continuam por confirmar.'),indent=2,ensure_ascii=False)+'\n',encoding='utf8')
print(json.dumps(dict(G2_components=[len(r['components'])for r in rows],G2_volumes=[r['sum_positive_solids_mm3']for r in rows],P16_holes=4)))
