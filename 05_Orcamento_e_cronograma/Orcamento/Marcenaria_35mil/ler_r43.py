from pathlib import Path
import zipfile, xml.etree.ElementTree as ET, json, hashlib
folder=Path(__file__).resolve().parent
model=folder.parents[1]/'Modelo_FreeCAD/01_Consolidacao/Guedala_Park_R43_Consolidado.FCStd'
with zipfile.ZipFile(model) as z:
    root=ET.fromstring(z.read('Document.xml'))
    objects=root.find('ObjectData').findall('Object')
    out=[]
    for obj in objects:
        props={p.attrib['name']:p for p in obj.find('Properties')}
        def val(k):
            p=props.get(k)
            return list(p)[0].attrib if p is not None and len(p) else None
        label=(val('Label') or {}).get('value','')
        if obj.attrib['name'].startswith('Modulo') or any(s in label.lower() for s in ['caixa grande','módulo da caixa','modulo da caixa','bancada','painel da tv','tampa r43','r43 · tampa']):
            out.append({'name':obj.attrib['name'],'label':label,'props':{k:val(k) for k in ['Comprimento','Profundidade','Altura','Material','Status','Group'] if k in props}})
    result={'model':str(model),'sha256':hashlib.sha256(model.read_bytes()).hexdigest(),'objects':len(objects),'selected':out}
    (folder/'Inventario_nominal_R43.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(out,ensure_ascii=False))
