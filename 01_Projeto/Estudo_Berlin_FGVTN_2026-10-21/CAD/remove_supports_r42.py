import FreeCAD as A, pathlib, hashlib, json, zipfile, xml.etree.ElementTree as E
base=pathlib.Path(__file__).resolve().parents[2]
src=base/'Modelo_FreeCAD/01_Atual/Cesto_R41_2026-10-20/Guedala_Park_R41_Estudo_Frente500.FCStd'
dest=base/'Modelo_FreeCAD/01_Atual/Sem_suportes_R42_2026-10-22'
dest.mkdir(exist_ok=True)
out=dest/'Guedala_Park_R42_Sem_Suportes.FCStd'
assert not out.exists()
h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
before=h(src);d=A.openDocument(str(src));remove={'Peca108','Peca109'}
def snap(doc):
 r={}
 for o in doc.Objects:
  if o.Name in remove:continue
  props={}
  for p in o.PropertiesList:
   if p in ['Shape','Group'] or p.startswith('_'):continue
   try:props[p]=str(getattr(o,p))
   except:pass
  if 'Group' in o.PropertiesList:props['Group']=[x.Name for x in o.Group if x.Name not in remove]
  if hasattr(o,'Shape') and not o.Shape.isNull():
   s=o.Shape;b=s.BoundBox
   props['_shape']=[b.XMin,b.YMin,b.ZMin,b.XMax,b.YMax,b.ZMax,len(s.Faces),len(s.Edges)]
  r[o.Name]=props
 return r
initial=snap(d);removed=[]
for n in sorted(remove):
 o=d.getObject(n)
 assert o and 'celular' in o.Label.lower() and len(o.OutList)==0
 assert [x.Name for x in o.InList]==['Ambiente_quarto']
 removed.append({'nome':n,'label':o.Label,'tipo':o.TypeId,'pai':'Ambiente_quarto','placement':str(o.Placement),'dimensoes_mm':[o.Length.Value,o.Width.Value,o.Height.Value]})
 d.removeObject(n)
# no global recompute: preserve all existing parametric states
after=snap(d)
changes=[n for n in initial if any(after.get(n,{}).get(p)!=v for p,v in initial[n].items())]
assert not changes,[(n,[(p,initial[n][p],after[n].get(p)) for p in initial[n] if initial[n][p]!=after[n].get(p)]) for n in changes[:2]]
d.saveAs(str(out));A.closeDocument(d.Name)
# Preserve the original GUI presentation for every remaining object, removing only the two view providers.
with zipfile.ZipFile(src) as zin:
 gui=E.fromstring(zin.read('GuiDocument.xml'))
 vp=gui.find('ViewProviderData')
 for child in list(vp):
  if child.get('name') in remove:vp.remove(child)
 vp.set('Count',str(len(vp)))
 gui_bytes=E.tostring(gui,encoding='utf-8',xml_declaration=True)
 gui_assets={n:zin.read(n) for n in zin.namelist() if n.endswith('.col')}
with zipfile.ZipFile(out) as z:entries={n:z.read(n) for n in z.namelist() if n!='GuiDocument.xml' and not n.startswith('thumbnails/')}
entries.update(gui_assets);entries['GuiDocument.xml']=gui_bytes
with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED) as z:
 for n,data in entries.items():z.writestr(n,data)
c=A.openDocument(str(out));reopened=snap(c)
differences=[n for n in initial if any(reopened.get(n,{}).get(p)!=v for p,v in initial[n].items())]
assert not differences,differences
assert len(c.Objects)==5496 and all(c.getObject(n) is None for n in remove)
assert h(src)==before
report={'fonte':str(src),'saida':str(out),'sha256_original_antes':before,'sha256_original_depois':h(src),'sha256_r42':h(out),'removidos':removed,'objetos_antes':5498,'objetos_depois':len(c.Objects),'propriedades_ou_geometria_restantes_alteradas':differences,'viewproviders_preservados':len(vp),'thumbnail_antigo':'omitido para nao apresentar imagem desatualizada','nota':'Somente apoios de celular/oculos removidos. Berlin e ferragens nao incorporadas. Nenhuma medida fisica ou aprovacao de fabricacao.'}
(dest/'Verificacao_R42.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(report,ensure_ascii=False))




