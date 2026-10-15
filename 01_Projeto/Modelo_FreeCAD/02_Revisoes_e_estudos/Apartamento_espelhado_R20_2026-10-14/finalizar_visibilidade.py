from pathlib import Path
import json
import FreeCAD as App,FreeCADGui as Gui
root=(Path(__file__).resolve().parent / '.').resolve();p=(Path(__file__).resolve().parent / 'Guedala_Park_R20_Apartamento_Espelhado.FCStd').resolve()
d=next(x for x in App.listDocuments().values() if x.FileName and Path(x.FileName).resolve()==p)
a=json.loads(((Path(__file__).resolve().parent / 'Espelhamento_R20.json').resolve()).read_text(encoding='utf-8'));new=[]
for l in [o for o in d.Objects if o.Name.startswith('EspelhoPecaR')]:
 l.LinkTransform=True
 old=next(r for r in a['mapping'] if l.LinkedObject.Name in r['source_roots'])
 new.append({'link':l.Name,'source_group':old['source_group'],'source_roots':[l.LinkedObject.Name],'visible':l.Visibility})
d.recompute()
for s in a['samples']:
 o=d.getObject(s['object']);chain=[]
 while o:chain.append(o.Name);o=o.getParentGeoFeatureGroup()
 row=next(r for r in new if chain[-1] in r['source_roots']);l=d.getObject(row['link'])
 path='.'.join(reversed(chain[:-1]))+('.' if len(chain)>1 else '')
 q=l.getSubObject(path);b=q.optimalBoundingBox();actual=[b.XMin,b.YMin,b.ZMin,b.XLength,b.YLength,b.ZLength]
 err=max(abs(x-y) for x,y in zip(actual,s['mirrored_bbox']));assert err<1e-6,(s['object'],actual,s['mirrored_bbox'])
 s.update(link=l.Name,path=path,max_error_mm=err)
a['mapping']=new;a['display_strategy']='Native links to existing individual geometric roots, LinkTransform=True; new non-geometric room groups. Whole walls visible, cut walls/references hidden. R03 articulated corner and histories hidden. No geometry reparenting or parameter type conversion.'
assert not [o.Name for o in d.Objects if 'Invalid' in o.State]
((Path(__file__).resolve().parent / 'Espelhamento_R20.json').resolve()).write_text(json.dumps(a,ensure_ascii=False,indent=2),encoding='utf-8')
Gui.activeDocument().activeView().viewAxonometric();Gui.activeDocument().activeView().fitAll();Gui.updateGui();d.save()
result={'links':len(new),'samples':a['samples'],'saved':str(p)}
