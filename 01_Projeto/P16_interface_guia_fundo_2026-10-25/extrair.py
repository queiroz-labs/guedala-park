"""Localiza apenas componentes volumetricos das intersecoes, sem cortar madeira."""
from pathlib import Path
import json,hashlib
import FreeCAD as App,FreeCADGui as Gui
HERE=Path(__file__).resolve().parent
ref=json.loads((HERE.parent/'P16_gavetas_estabilidade_2026-10-25/Geometria_R51.json').read_text(encoding='utf8'))
cad=Path(ref['cad']);assert hashlib.sha256(cad.read_bytes()).hexdigest()==ref['sha256']
s=next(d for d in App.listDocuments().values()if Path(d.FileName).resolve()==cad.resolve())
assert not Gui.getDocument(s.Name).Modified
def world(o):
 sh=o.Shape.copy();sh.Placement=o.getGlobalPlacement().multiply(o.Placement.inverse()).multiply(sh.Placement);return sh
def bounds(sh):
 # Vertices nao incluem extremos internos de superficies curvas; registrar tambem caixa otima.
 b=sh.optimalBoundingBox();return [b.XMin,b.YMin,b.ZMin,b.XMax,b.YMax,b.ZMax]
rows=[]
for di in ref['drawers']:
 floor=next(o for o in di['wood']if 'Fundo comum' in o['label']);fo=s.getObject(floor['name']);wood=world(fo)
 guides=[o for o in s.Objects if o.Name.startswith('GavetaComum') and 'MOVENTO400' in o.Label and ('escritório 1' if di['name']=='Gaveta008' else 'escritório 2') in o.Label]
 assert len(guides)==4
 for o in guides:
  guide=world(o);hit=wood.common(guide);components=[]
  for solid in hit.Solids:
   if solid.Volume<1e-7:continue
   b=bounds(solid);c=solid.CenterOfMass
   components.append(dict(volume_mm3=solid.Volume,box_mm=b,size_mm=[b[i+3]-b[i]for i in range(3)],center_mm=[c.x,c.y,c.z],valid=solid.isValid(),
    face_surface_types=[type(f.Surface).__name__ for f in solid.Faces]))
  volume=sum(x['volume_mm3']for x in components)
  assert abs(volume-hit.Volume)<1e-4
  rows.append(dict(drawer=di['name'],floor=fo.Name,guide=o.Name,guide_label=o.Label,
   floor_box_mm=bounds(wood),guide_box_mm=bounds(guide),positive_intersection_volume_mm3=volume,components=components,
   guide_solid_count=len(guide.Solids),guide_valid=guide.isValid(),floor_valid=wood.isValid()))
assert hashlib.sha256(cad.read_bytes()).hexdigest()==ref['sha256'] and not Gui.getDocument(s.Name).Modified
out=dict(source_sha256=ref['sha256'],source=str(cad),pairs=rows,source_unchanged=True,
 scope='Somente localizacao das regioes com volume positivo na pose fechada. GuiasSTEP continuam inteiras/estaticas, sem regulagem/telescopio. Nenhuma usinagem/deslocamento corretivo foi aplicado.')
(HERE/'Intersecoes_localizadas.json').write_text(json.dumps(out,indent=2,ensure_ascii=False)+'\n',encoding='utf8')
print(json.dumps(rows,ensure_ascii=False))
