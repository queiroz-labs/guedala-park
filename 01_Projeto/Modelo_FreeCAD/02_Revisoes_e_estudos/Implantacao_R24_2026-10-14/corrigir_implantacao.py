"""Restore the original Daiane work layout; hide three confirmed stale references."""
from pathlib import Path
import hashlib, json, shutil
import FreeCAD as App

root = (Path(__file__).resolve().parent / '.').resolve()
base = (Path(__file__).resolve().parent / '../Rotulos_R23_2026-10-14/Guedala_Park_R23_Rotulos_Consistentes.FCStd').resolve()
target = (Path(__file__).resolve().parent / 'Guedala_Park_R24_Implantacao_Corrigida.FCStd').resolve()
expected_sha = 'cf515686f48057c3b9e025bee28f3ddac735ea73608e401133e5fc842a972eea'
assert hashlib.sha256(base.read_bytes()).hexdigest() == expected_sha
assert not target.exists(), 'Preserve existing revision; do not run correction twice'
shutil.copy2(base, target)
d = App.openDocument(str(target))

def parents(o):
    return sorted(p.Name for p in o.InList if p.isDerivedFrom('App::DocumentObjectGroup') or p.TypeId == 'App::Part')

def state(o):
    return {'placement': list(o.Placement.toMatrix().A) if 'Placement' in o.PropertiesList else None,
            'expressions': list(o.ExpressionEngine) if 'ExpressionEngine' in o.PropertiesList else None,
            'parents': parents(o), 'visibility': o.ViewObject.Visibility}

before = {o.Name: state(o) for o in d.Objects}
sofa_names = ['Peca'+str(n) for n in range(122,129)]
hide = ['EspelhoPecaR041', 'EspelhoPecaR042', 'EspelhoPecaR123']
rot = App.Rotation(App.Vector(0,0,1), 180)
pivot = App.Vector(2570,2220,0)
change = App.Placement(pivot-rot.multVec(pivot),rot)
report = {'base': str(base), 'file': str(target), 'base_sha256_before': expected_sha,
          'reason': 'Importer used +yaw while original JS uses -yaw in CAD XY. Restore seven Daiane primitives to approved daily envelope. Hide original guest-only pads and retired tank reference.',
          'source_documents': ['Escritorio/Ajuste_sofa_e_UltraComfort_R07.md', 'Escritorio/README.md', 'Estudo_interativo/src/app.js:249', 'Modelo_FreeCAD/gerar_modelo.py:215', 'Modelo_FreeCAD/Cesto_R15_2026-10-14/montar_cesto.py:73'],
          'sofa': [], 'hidden_links': hide}
for name in sofa_names:
    o = d.getObject(name)
    assert o is not None and 'Daiane' in o.Label
    assert o.getParentGeoFeatureGroup() is None
    assert not o.ExpressionEngine
    bb = o.Shape.BoundBox
    original_volume = o.Shape.Volume
    o.Placement = change.multiply(o.Placement)
    report['sofa'].append({'name':name, 'before_matrix':before[name]['placement'],
                          'before_bbox':[bb.XMin,bb.YMin,bb.ZMin,bb.XMax,bb.YMax,bb.ZMax],
                          'volume_mm3':original_volume})
for name in hide:
    o = d.getObject(name)
    assert o is not None and o.TypeId == 'App::Link'
    o.ViewObject.Visibility = False
d.recompute()
for row in report['sofa']:
    o=d.getObject(row['name']);bb=o.Shape.BoundBox
    row['after_matrix']=list(o.Placement.toMatrix().A)
    row['after_bbox']=[bb.XMin,bb.YMin,bb.ZMin,bb.XMax,bb.YMax,bb.ZMax]
    assert abs(o.Shape.Volume-row['volume_mm3']) < 1e-5
body=d.getObject('Peca122').Shape.BoundBox
assert abs(body.XMin-2570)<1e-5 and abs(body.XMax-3470)<1e-5
assert abs(body.YMin-1520)<1e-5 and abs(body.YMax-2920)<1e-5
after={o.Name:state(o) for o in d.Objects}
assert before.keys()==after.keys()
differences=[]
for name in before:
    changed=[k for k in before[name] if before[name][k]!=after[name][k]]
    if changed:
        assert (name in sofa_names and changed==['placement']) or (name in hide and changed==['visibility']), (name,changed)
        differences.append({'name':name,'fields':changed})
assert len(differences)==10
assert not [o.Name for o in d.Objects if 'Invalid' in o.State]
report['changes']=differences
report['objects_compared']=len(before)
report['invalid']=[]
d.Label='Guedala Park — R24 — implantação corrigida'
d.save()
report['base_sha256_after']=hashlib.sha256(base.read_bytes()).hexdigest()
assert report['base_sha256_after']==expected_sha
report['sha256']=hashlib.sha256(target.read_bytes()).hexdigest()
((Path(__file__).resolve().parent / 'Correcao_R24.json').resolve()).write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
App.setActiveDocument(d.Name)
