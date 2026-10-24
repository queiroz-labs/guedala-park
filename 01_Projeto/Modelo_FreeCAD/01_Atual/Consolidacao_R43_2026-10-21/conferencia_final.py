import FreeCAD as A,FreeCADGui as G,pathlib,json,hashlib
P=pathlib.Path(__file__).resolve().parent;d=A.getDocument('Guedala_Park_R43_Consolidado')
reopen=json.loads((P/'Reabertura_R43.json').read_text(encoding='utf-8'))
assert reopen['reopened'] and not reopen['invalid_new_shapes']
assert len(reopen['berlin'])==15 and all(not x['null'] and x['valid'] for x in reopen['berlin'])
r={'bank_open_dimensions_mm':[],'new_living_vs_bathroom_bbox_hits':[]}
for i in [1,2]:
 setattr(d.BancoR43_Controle,'Abertura'+str(i),90);d.recompute();o=d.getObject('BancoR43_Painel'+str(i));s=o.Shape.copy();s.Placement=o.getGlobalPlacement();b=s.BoundBox
 r['bank_open_dimensions_mm'].append([b.XLength,b.YLength,b.ZLength]);assert abs(b.XLength-20)<.01 and abs(b.ZLength-448)<.01
 setattr(d.BancoR43_Controle,'Abertura'+str(i),0)
d.recompute()
for o in d.Objects:
 if hasattr(o,'Group') or not hasattr(o,'Shape') or o.Shape.isNull():continue
 if o.Name.startswith('Fechada_') or o.Name.startswith('BancoR43_'):
  a=o.Shape.copy();a.Placement=o.getGlobalPlacement()
  for q in d.Objects:
   if q.Name.startswith('BC43_') and not hasattr(q,'Group') and hasattr(q,'Shape') and not q.Shape.isNull() and q.ViewObject.Visibility:
    b=q.Shape.copy();b.Placement=q.getGlobalPlacement()
    if a.BoundBox.intersect(b.BoundBox):r['new_living_vs_bathroom_bbox_hits'].append([o.Name,q.Name])
 if o.Name.startswith(('Fechada_','Aberta_')):
  facecolors=o.ViewObject.DiffuseColor;mat=o.ViewObject.ShapeMaterial;mat.Shininess=0;o.ViewObject.ShapeMaterial=mat;o.ViewObject.DiffuseColor=facecolors
assert not r['new_living_vs_bathroom_bbox_hits']
d.save();r['r43_sha256']=hashlib.sha256(pathlib.Path(d.FileName).read_bytes()).hexdigest()
r['r42_sha256']=hashlib.sha256((P.parent/'Consolidacao_R42_2026-10-22/Guedala_Park_R42_Consolidado.FCStd').read_bytes()).hexdigest()
assert r['r42_sha256']=='b30ae9ab9c82620ecdab26b2cfae589037954356d515b483b5b6849f76e4bc26'
(P/'Conferencia_final.json').write_text(json.dumps(r,ensure_ascii=False,indent=2),encoding='utf-8');G.updateGui()
