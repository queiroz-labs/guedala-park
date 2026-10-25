"""Somente leitura das caixas atuais; sem recalcular/animar suas folhas."""
from pathlib import Path
import json,hashlib
import FreeCAD as App,FreeCADGui as Gui
HERE=Path(__file__).resolve().parent
src=App.getDocument('Guedala_Park_R51_Sem_estudo_tubular')
assert not Gui.getDocument(src.Name).Modified,'Conferir alteracoes nao salvas da fonte antes de extrair'
spec={
 'P09':dict(module='Modulo008',base='Peca318',back='Peca317',body=[f'Peca{i}' for i in range(315,321)]),
 'P11':dict(module='Modulo010',base='Peca337',back='Peca336',body=[f'Peca{i}' for i in range(334,340)]),
 'P12':dict(module='Modulo011',base='Peca345',back='Peca344',body=[f'Peca{i}' for i in range(342,348)]),
 'P17':dict(module='Modulo016',base='Peca387',back='Peca386',body=[f'Peca{i}' for i in range(384,389)]+['ApoioComumR11','ApoioComumR001','ApoioComumR002','ApoioOpostoR18'])}
inventory=json.loads((HERE.parent/'Cargas_e_ligacoes_R50_2026-10-25/Geometria_R50.json').read_text(encoding='utf8'))
snap=json.loads((HERE.parent/'Cinematica_offline_2026-10-25/Snapshot_R51.json').read_text(encoding='utf8'))
def shape(o):
 s=o.Shape.copy();s.Placement=o.getGlobalPlacement().multiply(o.Placement.inverse()).multiply(s.Placement);return s
def bbox(s):
 b=s.BoundBox;return [b.XMin,b.YMin,b.ZMin,b.XMax,b.YMax,b.ZMax]
modules={}
for code,sp in spec.items():
 m=src.getObject(sp['module']);inv=m.getGlobalPlacement().inverse();rows=[]
 for name in sp['body']:
  o=src.getObject(name);assert o.ViewObject.Visibility
  s=shape(o);s.Placement=inv.multiply(s.Placement)
  volume=sum(t.Volume for t in s.Solids);cg=sum((t.CenterOfMass*t.Volume for t in s.Solids),App.Vector())/volume
  rows.append(dict(name=name,label=o.Label,box_module_mm=bbox(s),center_module_mm=[cg.x,cg.y,cg.z],volume_mm3=volume))
 base=next(r for r in rows if r['name']==sp['base']);back=next(r for r in rows if r['name']==sp['back'])
 b=base['box_module_mm'];u0=b[0];rear=back['box_module_mm'][4];z0=min(r['box_module_mm'][2] for r in rows)
 width=b[3]-b[0];D=rear-b[1];H=max(r['box_module_mm'][5] for r in rows)-z0
 for r in rows:
  x,y,z=r['center_module_mm'];r['center_uvz_mm']=[x-u0,rear-y,z-z0]
 leaves=[]
 ids=set(inventory['modules'][code]['pieces'])
 for n,leaf in snap['leaves'].items():
  fronts=[f for f in leaf['fronts'] if f['name'] in ids and f['visible_effective']]
  if fronts:
   assert leaf['visible_effective'] and abs(src.getObject(n).Abertura.Value)<1e-8
   leaves.append(dict(leaf=n,fronts=[f['name'] for f in fronts]))
 assert leaves
 modules[code]=dict(label=m.Label,width_mm=width,body_depth_mm=D,height_mm=H,
  module_inverse_matrix=inv.toMatrix().A,canonical_origin=dict(u0_module_mm=u0,rear_module_mm=rear,z0_module_mm=z0),
  body=rows,leaves=leaves,base=sp['base'],back=sp['back'])
data=dict(cad=src.FileName,sha256=hashlib.sha256(Path(src.FileName).read_bytes()).hexdigest(),modules=modules,
 snapshot_sha256=hashlib.sha256((HERE.parent/'Cinematica_offline_2026-10-25/Snapshot_R51.json').read_bytes()).hexdigest(),
 scope='Geometria atual de quatro caixas. U cresce emX local;v e distancia normal da face traseira nominal. Sem massa real de ferragens/equipamentos, sem produto de suspensao ou ancoragem escolhidos.')
hood=shape(src.getObject('Peca139'));p09base=shape(src.getObject('Peca318'))
data['depurador_interface_nominal']=dict(hood_object='Peca139',hood_label=src.getObject('Peca139').Label,
 hood_global_box_mm=bbox(hood),cabinet_base_global_box_mm=bbox(p09base),
 vertical_gap_mm=p09base.BoundBox.ZMin-hood.BoundBox.ZMax,
 scope='Gabarito do produto; sem parafusos, abas, adaptadores ou ligacao real modelados. Nao resolve instalacao.')
(HERE/'Geometria_R51.json').write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n',encoding='utf8')
result={c:dict(width=m['width_mm'],depth=m['body_depth_mm'],height=m['height_mm'],wood=len(m['body']),doors=len(m['leaves'])) for c,m in modules.items()}
