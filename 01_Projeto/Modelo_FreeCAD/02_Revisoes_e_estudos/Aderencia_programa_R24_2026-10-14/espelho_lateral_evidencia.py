from pathlib import Path
import zipfile,xml.etree.ElementTree as E,re,json,itertools
H=(Path(__file__).resolve().parent / '.').resolve()
f=(Path(__file__).resolve().parent / '../Implantacao_R24_2026-10-14/Guedala_Park_R24_Implantacao_Corrigida.FCStd').resolve()
with zipfile.ZipFile(f) as z:
 d=E.fromstring(z.read('Document.xml'));data={o.get('name'):o for o in d.find('ObjectData')}
 def prop(n,p):return data[n].find('Properties/Property[@name="'+p+'"]')
 rows=[]
 for n in ['ReferenciaCorrerR14','ReferenciaCorrerR001','ReferenciaCorrerR002','ReferenciaCorrerR003']:
  shape=prop(n,'Shape')[0].get('file');txt=z.read(shape).decode('utf-8')
  matches=re.findall(r'^Ve\s*\n[^\n]+\n([^\n]+)',txt,re.M)
  pts=[tuple(map(float,s.split())) for s in matches];assert len(pts)==8 and all(len(p)==3 for p in pts)
  axes=[sorted({p[i] for p in pts}) for i in range(3)]
  assert all(len(q)==2 for q in axes) and set(pts)==set(itertools.product(*axes))
  local=[q[0] for q in axes]+[q[1] for q in axes]
  glob=[local[0]+10,local[1]+3290,local[2],local[3]+10,local[4]+3290,local[5]]
  rows.append(dict(object=n,label=prop(n,'Label')[0].get('value'),xpath='/Document/ObjectData/Object[@name="'+n+'"]/Properties/Property[@name="Shape"]/Part',shape_file=shape,placement_xml=prop(n,'Placement')[0].attrib,vertices=pts,local_bbox=local,source_world_bbox=glob,mirrored_world_bbox=[7400-glob[3],glob[1],glob[2],7400-glob[0],glob[4],glob[5]],limit='Somente8 vértices de reserva retangular do BREP salvo; não resistência, ligações ou acabamento real'))
out=dict(file=str(f),parent='Modulo',parent_origin_mm=[10,3290,0],supports=rows,
 side_Peca207=dict(local_bbox_mm=[1982,82,0,2000,650,2132],source_world_bbox_mm=[1992,3372,0,2010,3940,2132],mirror_bbox_mm=[5390,3372,0,5408,3940,2132],center_y_mm=3656),
 mirror_Peca275=dict(source_world_bbox_mm=[2010,3350,200,2015,3850,2000],center_y_mm=3600),
 combined_lateral_at_mirror_height=dict(description='Peca207 + apoioReferenciaCorrerR001 estão no mesmo plano externo X2010 e encontram emY3372; na alturaZ200..2000 formam face contínuaY3290..3940',y_min_mm=3290,y_max_mm=3940,center_y_mm=3615,current_mirror_offset_y_mm=-15,
  limits='Duas peças e ligação/apoio permanecem propostas R14, não painel monolítico ou vidro/fixação homologados'),
 classification='Desvio nominal de centralização15mm no conjunto lateral proposto. Centro do painel568 isolado3656 NÃO corresponde ao conjunto que inclui o apoio82. Responsável integra somente ajuste geométrico revisado; nenhuma fabricação liberada.')
((Path(__file__).resolve().parent / 'Espelho_lateral_evidencia.json').resolve()).write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(out['combined_lateral_at_mirror_height'],ensure_ascii=True))
