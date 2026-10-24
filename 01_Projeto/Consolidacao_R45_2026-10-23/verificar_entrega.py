from pathlib import Path
import json,zipfile,xml.etree.ElementTree as ET,re,hashlib,datetime
p=Path(__file__).parent
f=p/'Guedala_Park_R45_Consolidado.FCStd'
with zipfile.ZipFile(f) as z:
 bad=z.testzip();xml=ET.fromstring(z.read('Document.xml'))
 objects=xml.find('Objects');names=[o.attrib['name'] for o in objects if 'name' in o.attrib]
 assert bad is None
 assert len(names)==5840
 assert 'R45_Auditoria' in names and 'R45_Estudos' in names
missing=[]
for html in p.rglob('*.html'):
 if 'Fontes' in html.parts:continue
 for ref in re.findall(r'(?:href|src)=["\']([^"\']+)',html.read_text(encoding='utf8')):
  if re.match(r'^(https?:|data:|mailto:|#)',ref):continue
  target=html.parent/ref.split('#')[0]
  if not target.exists() and target.name!='Verificacao_entrega.json':missing.append({'arquivo':str(html.relative_to(p)),'referencia':ref})
src=p.parent/'Modelo_FreeCAD/01_Atual/FGVTN_R44_2026-10-22/Guedala_Park_R44_Consolidado.FCStd'
sha=hashlib.sha256(src.read_bytes()).hexdigest()
assert sha=='9187c163d7d827e12387e7e9c9e953b0380c55bcc8aaed3e872f83c4665d839e'
out={'horario_UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'arquivo_CAD':f.name,'bytes':f.stat().st_size,'zip_integro':bad is None,'XML_objetos':len(names),'grupos_R45_presentes':True,'R44_preservada_sha256':sha,'R45_sha256':hashlib.sha256(f.read_bytes()).hexdigest(),'links_html_ausentes':missing,'reabertura_completa_final':'Não realizada nesta verificação; arquivo salvo pelo FreeCAD e arquivo ZIP/XML conferido independentemente. Cópia base R44 foi aberta no FreeCAD antes da consolidação.'}
(p/'Verificacao_entrega.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps(out,ensure_ascii=False,indent=2))
