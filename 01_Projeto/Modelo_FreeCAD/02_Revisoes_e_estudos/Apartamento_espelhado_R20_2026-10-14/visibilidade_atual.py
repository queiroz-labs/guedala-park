from pathlib import Path
import json
import FreeCAD as App, FreeCADGui as Gui
root=(Path(__file__).resolve().parent / '.').resolve()
p=(Path(__file__).resolve().parent / 'Guedala_Park_R20_Apartamento_Espelhado.FCStd').resolve()
d=next(x for x in App.listDocuments().values() if x.FileName and Path(x.FileName).resolve()==p)
report=json.loads(((Path(__file__).resolve().parent / 'Espelhamento_R20.json').resolve()).read_text(encoding='utf-8'))
collection=d.getObject(report['collection'])
# Links to document groups override child visibility. Link each existing geometric
# root instead; keep every source hierarchy, placement and parameter type intact.
old_mapping=report['mapping'];new=[]
for row in old_mapping:
    if row['source_group'] in ['ReferenciasFerragens']:
        continue
    group=d.addObject('App::DocumentObjectGroup','VistaAmbienteR20')
    collection.addObject(group)
    group.Label=(d.getObject(row['source_group']).Label if row['source_group'] else 'Referências de equipamentos')+' — espelhado'
    for name in row['source_roots']:
        source=d.getObject(name)
        link=d.addObject('App::Link','EspelhoPecaR20')
        group.addObject(link);link.setLink(source);link.LinkTransform=True
        link.ScaleVector=App.Vector(-1,1,1);link.Placement.Base=App.Vector(7400,0,0)
        link.Label=source.Label
        visible=row['source_group'] not in ['ParedesCortadas',None]
        link.Visibility=visible
        new.append({'link':link.Name,'source_group':row['source_group'],'source_roots':[name],'visible':visible})
        source.Visibility=False
for name in ['FolhaAReal','FolhaBReal','PrincipalBlumR03','PrincipalBlumR001']:
    d.getObject(name).Visibility=False
for o in d.Objects:
    if o.Name.startswith('Historico'):o.Visibility=False
for row in old_mapping:
    d.removeObject(row['link'])
if d.getObject('TesteModuloAtualR20'):d.removeObject('TesteModuloAtualR20')
d.recompute()
for sample in report['samples']:
    o=d.getObject(sample['object']);chain=[];q=o
    while q:chain.append(q.Name);q=q.getParentGeoFeatureGroup()
    row=next(r for r in new if chain[-1] in r['source_roots'])
    sample['link']=row['link'];sample['path']='.'.join(reversed(chain[:-1]))+('.' if len(chain)>1 else '')
    s=d.getObject(row['link']).getSubObject(sample['path']);b=s.optimalBoundingBox()
    actual=[b.XMin,b.YMin,b.ZMin,b.XLength,b.YLength,b.ZLength]
    assert max(abs(x-y) for x,y in zip(actual,sample['mirrored_bbox']))<1e-6
assert not [o.Name for o in d.Objects if 'Invalid' in o.State]
report['mapping']=new
report['display_strategy']='Native links to individual existing geometric roots, organized in new non-geometric room groups; whole walls visible, cut walls and reference sources hidden. R03 articulated corner and adopted histories hidden. No geometry reparenting or parameter type conversion.'
((Path(__file__).resolve().parent / 'Espelhamento_R20.json').resolve()).write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
Gui.activeDocument().activeView().viewAxonometric();Gui.activeDocument().activeView().fitAll();Gui.updateGui();d.save()
result={'links':len(new),'saved':str(p),'invalid':[]}
