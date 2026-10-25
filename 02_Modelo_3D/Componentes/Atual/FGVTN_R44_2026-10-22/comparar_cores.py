import pathlib,json,zipfile,xml.etree.ElementTree as E
p=pathlib.Path(__file__).parent;a=zipfile.ZipFile(p.parent/'Consolidacao_R43_2026-10-21/Guedala_Park_R43_Consolidado.FCStd');b=zipfile.ZipFile(p/'Guedala_Park_R44_Consolidado.FCStd')
aa={o.get('name'):o for o in E.fromstring(a.read('GuiDocument.xml')).iter('ViewProvider')};bb={o.get('name'):o for o in E.fromstring(b.read('GuiDocument.xml')).iter('ViewProvider')}
checks=[];bad=[]
for n,o in aa.items():
 for prop in o.findall('./Properties/Property'):
  if prop.get('name') not in ['ShapeAppearance','DiffuseColor','LineColorArray','PointColorArray']:continue
  q=bb[n].find('./Properties/Property[@name="'+prop.get('name')+'"]')
  for el in prop.iter():
   if 'file' not in el.attrib:continue
   other=q.find('.//'+el.tag);f=el.get('file');g=other.get('file');checks.append([n,prop.get('name'),f,g])
   if a.read(f)!=b.read(g):bad.append([n,prop.get('name'),f,g])
r=json.loads((p/'Comparacao_BREP_R43_R44.json').read_text());r['original_color_properties_checked']=len(checks);r['changed_color_properties']=bad;r.pop('original_color_files',None);r.pop('changed_color_files',None);(p/'Comparacao_BREP_R43_R44.json').write_text(json.dumps(r,indent=2));print('colors',len(checks),'bad',len(bad),bad[:5])
