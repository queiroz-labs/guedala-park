from pathlib import Path
import zipfile,xml.etree.ElementTree as E,json,math
H=(Path(__file__).resolve().parent / '.').resolve();B=(Path(__file__).resolve().parent / '../..').resolve()
file=(Path(__file__).resolve().parent / '../Implantacao_R24_2026-10-14/Guedala_Park_R24_Implantacao_Corrigida.FCStd').resolve()
with zipfile.ZipFile(file) as z:d=E.fromstring(z.read('Document.xml'))
data={o.get('name'):{p.get('name'):p for p in o.find('Properties') if p.tag=='Property'} for o in d.find('ObjectData')}
types={o.get('name'):o.get('type') for o in d.find('Objects') if o.tag=='Object'}
def v(n,p,default=None):
 e=data[n].get(p)
 if e is None or not len(e):return default
 e=e[0]
 if e.tag=='Float':return float(e.get('value'))
 if e.tag=='Bool':return e.get('value')=='true'
 if e.tag=='String':return e.get('value')
 if e.tag=='PropertyPlacement':return {k:float(x) for k,x in e.attrib.items()}
 return e.attrib
def matrix(p):
 x,y,z,w=[p.get('Q'+str(i),0 if i<3 else 1) for i in range(4)]
 return [[1-2*(y*y+z*z),2*(x*y-z*w),2*(x*z+y*w),p.get('Px',0)],
 [2*(x*y+z*w),1-2*(x*x+z*z),2*(y*z-x*w),p.get('Py',0)],
 [2*(x*z-y*w),2*(y*z+x*w),1-2*(x*x+y*y),p.get('Pz',0)],[0,0,0,1]]
def box(a,d):
 pts=[[sum(a[i][j]*q[j] for j in range(3))+a[i][3] for i in range(3)] for q in [(x,y,z) for x in [0,d[0]] for y in [0,d[1]] for z in [0,d[2]]]]
 return [min(p[i] for p in pts) for i in range(3)]+[max(p[i] for p in pts) for i in range(3)]
mapping=json.loads(((Path(__file__).resolve().parent / '../Apartamento_espelhado_R20_2026-10-14/Espelhamento_R20.json').resolve()).read_text(encoding='utf-8'))['mapping']
rows=[]
for r in mapping:
 if r['source_group'] not in ['Ambiente_sala','Ambiente_quarto','Ambiente_escritorio']:continue
 n=r['source_roots'][0]
 if n.startswith('Modulo'):continue
 dims=[v(n,k) for k in ['Length','Width','Height']]
 m=matrix(v(n,'Placement',{}));mir=[row[:] for row in m];mir[0]=[-x for x in mir[0]];mir[0][3]+=7400
 rows.append(dict(object=n,label=v(n,'Label'),type=types[n],room=r['source_group'],dimensions_mm=dims,placement=v(n,'Placement'),base_bbox_mm=box(m,dims) if all(isinstance(x,(float,int)) for x in dims) else None,mirrored_bbox_mm=box(mir,dims) if all(isinstance(x,(float,int)) for x in dims) else None,mirror_link=r['link'],mirror_visible=v(r['link'],'Visibility'),source=v(n,'Fonte'),source_note=v(n,'MedidaOriginal')))
((Path(__file__).resolve().parent / 'Standalone_R24.json').resolve()).write_text(json.dumps(dict(file=str(file),items=rows,method='Read-only ZIP/XML; bounds only Part::Box properties; no CAD execution'),ensure_ascii=False,indent=2),encoding='utf-8')
print(len(rows))
for r in rows:print(json.dumps(r,ensure_ascii=True))
