import FreeCAD as A,Part,pathlib,json
p=pathlib.Path(__file__).parent
s=A.openDocument(str(p.parents[2]/'Avanco_pendencias_2026-10-21/Gavetas/Fixacao_simples_R04/Escritorio_fixacao_simples_R04_ESTUDO.FCStd'))
rot=A.Rotation(A.Vector(1,1,1),-120)
r={'method':'HIPOTESE NAO VALIDADA: source Y0 na parede X4318; base frontal Z148.5 alinhada Y676 (4mm atras carcaça680); topo perfil movel X30.6 apoiado no fundo inferior Z521/629. Sem engates. Nao autoriza recortes ou fabricacao.','cases':[]}
for st in ['FECHADA','ABERTA']:
 d=A.openDocument(str(p/(st+'_400_GUI_INSPECAO.FCStd')))
 for drawer,floor in [('Gaveta008',521),('Gaveta009',629)]:
  travel=374.3 if st=='ABERTA' else 0
  parts=list(s.getObject('Carcaca_470x248').Group)+list(s.getObject('Caixa_'+drawer).Group)
  solids=[];hits=[]
  for o in d.Objects:
   if o.TypeId!='Part::Feature':continue
   q=o.Shape.copy();q.Placement=A.Placement(A.Vector(4318,527.5,floor-30.6),rot).multiply(o.getGlobalPlacement());solids.append(q)
   for w in parts:
    t=w.Shape.copy();t.Placement=w.getGlobalPlacement()
    if w in s.getObject('Caixa_'+drawer).Group:t.translate(A.Vector(0,travel,0))
    if q.BoundBox.intersect(t.BoundBox):
     v=q.common(t).Volume
     if v>0.01:hits.append({'rail':o.Label,'wood':w.Name,'intersection_mm3':round(v,3)})
  compound=Part.makeCompound(solids);b=compound.BoundBox
  r['cases'].append({'state':st,'drawer':drawer,'bbox':[b.XMin,b.YMin,b.ZMin,b.XMax,b.YMax,b.ZMax],'interferences':hits})
(p/'Ensaio_datum_HIPOTESE.json').write_text(json.dumps(r,indent=2,ensure_ascii=False),encoding='utf8')
print(json.dumps(r,ensure_ascii=True))

