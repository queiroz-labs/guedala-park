"""Read saved R26, check only the new control and reflected bin tracking, never save."""
from pathlib import Path
import json,hashlib,traceback
import FreeCAD as App
root=(Path(__file__).resolve().parent / '.').resolve()
source=(Path(__file__).resolve().parent / 'Guedala_Park_R26_Manutencao_Simples.FCStd').resolve()
report={'file':str(source),'sha256_before':hashlib.sha256(source.read_bytes()).hexdigest(),'states':[],'errors':[]}
def bb(s):
 b=s.BoundBox;return [b.XMin,b.YMin,b.ZMin,b.XMax,b.YMax,b.ZMax]
d=None
try:
 assert not App.GuiUp
 d=App.openDocument(str(source));c=d.getObject('ControleLoopManutencaoR26')
 assert float(c.Afastamento)==0
 parts=['Peca147','Peca148','Peca149']
 links={n:next(o for o in d.Objects if o.TypeId=='App::Link' and o.Name.startswith('EspelhoPecaR') and o.LinkedObject==d.getObject(n)) for n in parts}
 expected={r['name']:r for r in json.loads(((Path(__file__).resolve().parent / 'Estacionamento_Loop_R26.json').resolve()).read_text(encoding='utf-8'))['bin_parts']}
 for distance in [0,650,0]:
  c.Afastamento=distance;d.recompute();case={'control_mm':distance,'parts':[]}
  for n in parts:
   o=d.getObject(n);s=o.Shape.copy();s.Placement=o.getGlobalPlacement();b=bb(s)
   exp=expected[n]['before_source_mm' if distance==0 else 'parked_source_mm']
   assert max(abs(x-y) for x,y in zip(b,exp))<1e-6
   mirrored=bb(links[n].Shape)
   transformed=[7400-b[3],b[1],b[2],7400-b[0],b[4],b[5]]
   assert max(abs(x-y) for x,y in zip(mirrored,transformed))<1e-6
   assert o.getParentGeoFeatureGroup() is None and s.isValid() and links[n].Shape.isValid()
   case['parts'].append({'name':n,'link':links[n].Name,'bbox_source_mm':b,'bbox_current_mm':mirrored})
  report['states'].append(case)
 report['invalid']=[o.Name for o in d.Objects if 'Invalid' in o.State]
 assert not report['invalid']
 assert all(abs(float(getattr(d.getObject('ControleCestoR15'),k).Value))<1e-9 for k in ['Abertura','RetiradaSaco','EndireitarSaco','RetiradaPainelSuperior','RetiradaConjunto'])
 report['status']='saved_control_and_reflection_verified';report['objects']=len(d.Objects)
except Exception:
 report['status']='failed';report['errors'].append(traceback.format_exc())
finally:
 if d is not None:App.closeDocument(d.Name)
 report['sha256_after']=hashlib.sha256(source.read_bytes()).hexdigest()
 report['source_unchanged']=report['sha256_before']==report['sha256_after']
 ((Path(__file__).resolve().parent / 'Verificacao_controle_R26.json').resolve()).write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
 print('CONTROL_RESULT',report['status'],len(report['errors']),report['source_unchanged'])
