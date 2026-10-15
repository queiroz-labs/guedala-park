from pathlib import Path
import zipfile,xml.etree.ElementTree as ET,json
root=(Path(__file__).resolve().parent / '.').resolve();base=(Path(__file__).resolve().parent / '../..').resolve();out=[]
for folder,file in [('Gavetas_R05_2026-10-13','Guedala_Park_R05_Caixas_Gavetas.FCStd'),('Padronizacao_R08_2026-10-14','Guedala_Park_R08_Gavetas_Comuns.FCStd')]:
 with zipfile.ZipFile(base/'02_Revisoes_e_estudos'/folder/file) as z:
  e=ET.fromstring(z.read('Document.xml'))
  types={o.attrib['name']:o.attrib['type'] for o in e.find('Objects') if 'name' in o.attrib}
  objs={o.attrib['name']:o for o in e.find('ObjectData') if 'name' in o.attrib}
  labels={n:o.find("Properties/Property[@name='Label']/String").attrib['value'] for n,o in objs.items()}
  def group(n):
   pp=objs[n].find("Properties/Property[@name='Group']/LinkList")
   return [x.attrib['value'] for x in pp] if pp is not None else []
  whole,cut=group('ParedesInteiras'),group('ParedesCortadas')
  selected=[n for n,t in types.items() if t=='Part::Box' and (labels[n].startswith('Parede ·') if 'R05' in folder else ('Parede' in labels[n] or labels[n].startswith('Cama') or labels[n].startswith('Mesa')))]
  out.append({'source':str(base/'02_Revisoes_e_estudos'/folder/file),'total_global_selection':len(selected),'whole_walls_count':len(set(selected)&set(whole)),'cut_walls_count':len(set(selected)&set(cut)),'selected':[{ 'name':n,'label':labels[n],'scope':'whole_wall' if n in whole else 'cut_wall' if n in cut else 'extra'} for n in selected]})
((Path(__file__).resolve().parent / 'Contagem_selecao_XML.json').resolve()).write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')
