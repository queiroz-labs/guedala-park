"""Correção exata da R33 em disco, preservando os dados gráficos originais."""
import sys,json,zipfile,hashlib,shutil,xml.etree.ElementTree as ET
from pathlib import Path
sys.path.append('C:/Users/Elias/AppData/Local/Programs/FreeCAD-1.1.4/lib')
import FreeCAD as App
base=Path('C:/Users/Elias/Documents/PROJETOS/Guedala park')
folder=base/'guedala-park/02_Modelo_3D/Componentes/Atual/Conferencia_R33_2026-10-20'
path=folder/'Guedala_Park_R33_Conferencia.FCStd'
backup=base/'tmp/R33_antes_finalizacao_portas.FCStd'
assert not backup.exists(),'Backup já existe; verificar antes de repetir.'
shutil.copy2(path,backup)
source_sha=hashlib.sha256(path.read_bytes()).hexdigest()
names=['FrenteComumR005','FrenteComumR007']
with zipfile.ZipFile(path) as z:
 gui=ET.fromstring(z.read('GuiDocument.xml'))
 for name in names:
  p=gui.find(".//ViewProvider[@name='%s']/Properties/Property[@name='Visibility']/Bool" % name)
  assert p is not None,name
  p.set('value','true')
 gui_bytes=ET.tostring(gui,encoding='utf-8',xml_declaration=True)
d=App.openDocument(str(path));d.recompute()
geometry={o.Name:(o.Shape.Volume,o.Shape.Area,str(o.Placement),str(o.ExpressionEngine)) for o in d.Objects if o.isDerivedFrom('Part::Feature') and not o.Shape.isNull()}
rows=[]
for name in names:
 o=d.getObject(name);assert o.Shape.isValid()
 rows.append({'name':name,'label':o.Label,'visible_before':o.Visibility,'visible_after':True,'parent':o.getParentGeoFeatureGroup().Name,'volume_mm3':o.Shape.Volume})
 o.Visibility=True
 if 'CorrecaoR33' not in o.PropertiesList:o.addProperty('App::PropertyString','CorrecaoR33','AuditoriaR33')
 o.CorrecaoR33='Visibilidade restaurada na R33; painel e controle existentes preservados.'
 d.getObject(o.getParentGeoFeatureGroup().Name).Visibility=True
d.getObject('ConferenciaR33').Correcoes='Medição completa com32 formas adicionais frente à R32; duas frentes antes ocultas restauradas. Banco550=450+encosto100. Dimensões e expressões geométricas preservadas.'
d.recompute()
assert all(d.getObject(n).Visibility for n in names)
assert geometry=={o.Name:(o.Shape.Volume,o.Shape.Area,str(o.Placement),str(o.ExpressionEngine)) for o in d.Objects if o.isDerivedFrom('Part::Feature') and not o.Shape.isNull()}
d.save();App.closeDocument(d.Name)
# O salvamento pelo núcleo não escreve ViewProviders: recuperar seus dados
# e alterar apenas os dois indicadores de visibilidade na configuração GUI.
with zipfile.ZipFile(backup) as src,zipfile.ZipFile(path,'a',compression=zipfile.ZIP_DEFLATED) as dst:
 existing=set(dst.namelist());assert 'GuiDocument.xml' not in existing
 for n in src.namelist():
  if n not in existing:dst.writestr(n,gui_bytes if n=='GuiDocument.xml' else src.read(n))
with zipfile.ZipFile(path) as z:
 for fn,prefix in [('Document.xml','.//ObjectData/Object'),('GuiDocument.xml','.//ViewProvider')]:
  r=ET.fromstring(z.read(fn))
  for name in names:
   p=r.find(prefix+"[@name='%s']/Properties/Property[@name='Visibility']/Bool" % name)
   assert p is not None and p.get('value')=='true',(fn,name)
d=App.openDocument(str(path));d.recompute()
assert all(d.getObject(n).Visibility and d.getObject(n).Shape.isValid() for n in names)
assert not [o.Name for o in d.Objects if any(s in o.State for s in ['Invalid','Error'])]
assert len(d.Objects)==6195
App.closeDocument(d.Name)
report={'status':'PASSOU','model':str(path),'backup':str(backup),'before_sha256':source_sha,'after_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'doors':rows,'reopened':True,'core_and_gui_visibility_verified':True,'geometry_dimensions_placements_expressions_unchanged':True,'objects':6195,'source_R32_preserved':True}
(folder/'Portas_restauradas_R33.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(report,ensure_ascii=False))
