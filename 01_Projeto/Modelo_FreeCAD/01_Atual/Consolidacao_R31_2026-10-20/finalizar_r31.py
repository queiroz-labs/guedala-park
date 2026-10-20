"""Finaliza a apresentação e confere a revisão salva, sem redesenhar o banco."""
from pathlib import Path
import json, hashlib, traceback, runpy
import FreeCAD as App, FreeCADGui as Gui
here=Path(__file__).resolve().parent
status=here.parents[3]/'tmp/finalizacao_r31_status.json'
try:
 d=App.ActiveDocument
 assert Path(d.FileName).name=='Guedala_Park_R31_Consolidado.FCStd'
 hidden=[]
 for o in d.Objects:
  if o.Name.startswith('AcessoControle') and o.TypeId=='App::Link' and o.Visibility:
   o.Visibility=False;hidden.append(o.Name)
 # Esses vínculos servem para navegar na árvore. Exibi-los também desenha
 # cópias das gavetas na origem, fora do apartamento.
 d.recompute()
 current_roots={o.LinkedObject.Name for o in d.getObject('ApartamentoEspelhadoR20').OutListRecursive if o.TypeId=='App::Link' and o.LinkedObject and o.Visibility}
 def active(o):
  seen=set()
  while o is not None and o.Name not in seen:
   if o.Name in current_roots:return True
   seen.add(o.Name)
   if not o.Visibility:return False
   o=o.getParentGeoFeatureGroup() if hasattr(o,'getParentGeoFeatureGroup') else None
  return False
 native=[o for o in d.Objects if o.TypeId in ['Part::Box','Part::Feature','PartDesign::Feature'] and hasattr(o,'Shape') and not o.Shape.isNull() and active(o)]
 invalid=[o.Name for o in native if not o.Shape.isValid()]
 states=[o.Name for o in d.Objects if any(s in o.State for s in ['Invalid','Error'])]
 assert not invalid and not states,(invalid,states)
 assert d.getObject('AcessoFolhaR31').ExtracaoBandeja==0
 assert 'não gostou' in d.getObject('Modulo019').PreferenciaBanco20Out
 Gui.activeDocument().activeView().viewAxonometric()
 Gui.activeDocument().activeView().fitAll()
 d.save()
 Gui.activeDocument().activeView().saveImage(str(here/'Apartamento_R31.png'),1600,1100,'White')
 model=Path(d.FileName)
 reference=json.loads((here/'Consolidacao_R31.json').read_text(encoding='utf-8'))
 assert all(hashlib.sha256(Path(p).read_bytes()).hexdigest()==sha for p,sha in reference['reference_hashes_before'].items())
 report={'status':'PASSOU','date':'2026-10-20','objects':len(d.Objects),'native_shapes_checked':len(native),'invalid_native_shapes':invalid,'invalid_states':states,'navigation_links_hidden':hidden,'source_models_unchanged':True,'future_conventional_bank_reversal_applied':False,'bank_preference_recorded':True,'model_sha256':hashlib.sha256(model.read_bytes()).hexdigest()}
 (here/'Verificacao_final_R31.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
 runpy.run_path(str(here/'exportar_site.py'))
 status.write_text(json.dumps(report,ensure_ascii=False),encoding='utf-8')
except Exception:
 status.write_text(json.dumps({'status':'erro','trace':traceback.format_exc()}),encoding='utf-8');raise
