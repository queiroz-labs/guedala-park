from pathlib import Path
import json
import hashlib
import Import

root = Path('C:\\Users\\Elias\\Documents\\PROJETOS\\Guedala park\\guedala-park\\02_Modelo_3D\\Componentes\\Estudos\\Canto_2026-10-13\\Blum_oficial')
name = 'Blum_Canto_CAD_Oficial'
if name in FreeCAD.listDocuments():
    FreeCAD.closeDocument(name)
doc = FreeCAD.newDocument(name)
report = {'origem': 'Blum E-SERVICES autenticado, produto unico 3D, STEP MEDIUM',
          'data_consulta_local': '2026-10-13',
          'escopo': 'Biblioteca estatica; sem juntas mecanicas nem validacao da trajetoria.',
          'produtos': []}
for index, code in enumerate(('71T7550', '79T8500')):
    source = next((root/code).glob('*.step'))
    before = {o.Name for o in doc.Objects}
    Import.insert(str(source), doc.Name)
    doc.recompute()
    new = [o for o in doc.Objects if o.Name not in before]
    group = doc.addObject('App::DocumentObjectGroup', 'Produto_'+code)
    group.Label = code + ' - CAD Blum oficial, estatico'
    for obj in new:
        if not obj.getParentGeoFeatureGroup():
            group.addObject(obj)
    shapes = [o for o in new if hasattr(o, 'Shape') and not o.Shape.isNull() and o.Shape.Solids]
    item = {'codigo': code, 'arquivo': str(source.relative_to(root)),
            'sha256': hashlib.sha256(source.read_bytes()).hexdigest(),
            'objetos_importados': len(new), 'formas': []}
    for obj in shapes:
        box = obj.Shape.BoundBox
        item['formas'].append({'nome': obj.Name, 'label': obj.Label,
            'solidos': len(obj.Shape.Solids), 'valida': obj.Shape.isValid(),
            'volume_mm3': obj.Shape.Volume,
            'caixa_mm': [box.XMin, box.YMin, box.ZMin, box.XMax, box.YMax, box.ZMax]})
    # Display the two products side by side, without changing their internal geometry.
    top = [o for o in new if hasattr(o, 'Placement') and not o.getParentGeoFeatureGroup()]
    for obj in top:
        pos = obj.Placement
        pos.Base.x += index * 160
        obj.Placement = pos
    report['produtos'].append(item)
doc.recompute()
report['objetos_invalidos'] = [o.Name for o in doc.Objects if 'Invalid' in o.State]
doc.saveAs(str(Path('C:\\Users\\Elias\\Documents\\PROJETOS\\Guedala park\\guedala-park\\02_Modelo_3D\\Componentes\\Estudos\\Canto_2026-10-13\\Blum_oficial\\Blum_Canto_CAD_Oficial.FCStd')))
FreeCADGui.activeDocument().activeView().viewAxonometric()
FreeCADGui.activeDocument().activeView().fitAll()
FreeCADGui.updateGui()
FreeCADGui.activeDocument().activeView().saveImage(str(Path('C:\\Users\\Elias\\Documents\\PROJETOS\\Guedala park\\guedala-park\\02_Modelo_3D\\Componentes\\Estudos\\Canto_2026-10-13\\Blum_oficial\\Blum_Canto_CAD_Oficial.png')), 1400, 900, 'White')
(Path('C:\\Users\\Elias\\Documents\\PROJETOS\\Guedala park\\guedala-park\\02_Modelo_3D\\Componentes\\Estudos\\Canto_2026-10-13\\Blum_oficial\\Inventario_importacao.json')).write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
result = json.dumps(report, ensure_ascii=False)
