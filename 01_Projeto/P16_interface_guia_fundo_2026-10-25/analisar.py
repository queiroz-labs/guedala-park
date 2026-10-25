from pathlib import Path
import json,hashlib
from PIL import Image,ImageDraw,ImageFont
HERE=Path(__file__).resolve().parent
paths=[HERE/'Intersecoes_localizadas.json',HERE/'Referencia_G2_e_furos_P16.json']
d=json.loads(paths[0].read_text(encoding='utf8'));g=json.loads(paths[1].read_text(encoding='utf8'))
classified=[]
for r in d['pairs']:
 for i,c in enumerate(r['components'],1):
  b=c['box_mm'];bottom=r['floor_box_mm'][2]
  role='under_bottom' if abs(b[2]-bottom)<1e-5 and b[5]-bottom<.3 else 'rear_bore_region'
  classified.append(dict(drawer=r['drawer'],floor=r['floor'],guide=r['guide'],component=i,role=role,**c))
assert sum(r['role']=='under_bottom'for r in classified)==16
assert sum(r['role']=='rear_bore_region'for r in classified)==2
for n in ['Gaveta008','Gaveta009']:
 subset=[r for r in classified if r['drawer']==n]
 assert len(subset)==9
 assert len([r for r in d['pairs']if r['drawer']==n and r['positive_intersection_volume_mm3']>0])==2
for a,b in zip(g['reference_regions'],[r for r in d['pairs']if r['drawer']=='Gaveta008'and r['components']]):
 assert len(a['components'])==len(b['components'])
 assert abs(a['sum_positive_solids_mm3']-b['positive_intersection_volume_mm3'])<.001
out=dict(classified=classified,summary=dict(under_bottom_components=16,rear_bore_components=2,positive_pairs=4,tested_pairs=8,
 guide400_and_configured_G2_same_component_pattern=True,nominal_bores_checked=4,
 comparison_is_physical_approval=False),inputs_sha256={p.name:hashlib.sha256(p.read_bytes()).hexdigest()for p in paths+[HERE/'analisar.py']},source_sha256=d['source_sha256'])
(HERE/'Diagnostico.json').write_text(json.dumps(out,indent=2,ensure_ascii=False)+'\n',encoding='utf8')
im=Image.new('RGB',(1300,920),'#f5f3ee');dr=ImageDraw.Draw(im)
font=lambda size:ImageFont.truetype('C:/Windows/Fonts/arial.ttf',size)
def txt(x,y,s,size=24,col='#263e3b'):dr.text((x,y),s,font=font(size),fill=col)
txt(45,30,'P16 | ONDE ESTÃO AS INTERFERÊNCIAS',34)
txt(45,83,'Gaveta inferior fechada, vista por baixo. Fonte R51 preservada.',23)
ox,oy,k=65,180,1.5
def point(x,y):return ox+(x-4334)*k,oy+(y-292)*k
dr.rectangle([point(4334,292),point(4666,682)],fill='#e3d9c6',outline='#263e3b',width=2)
txt(70,143,'TRASEIRA / FUROS',21)
for row in [r for r in classified if r['drawer']=='Gaveta008']:
 b=row['box_mm'];x0,y0=point(b[0],b[1]);x1,y1=point(b[3],b[4]);col='#b34c3d'if row['role']=='rear_bore_region'else'#307d9c'
 dr.rectangle([x0-2,y0-2,x1+2,y1+2],fill=col)
for x in (4346,4654):
 x,y=point(x,292);dr.ellipse((x-7,y-7,x+7,y+7),outline='#5e6661',width=2)
txt(90,790,'FRENTE — sentido de abertura +Y',22)
txt(650,180,'AZUL: regiões sob o fundo',27,'#307d9c')
txt(650,227,'4 por guia principal; 8 por gaveta.',23)
txt(650,267,'Espessuras geométricas até0,175 mm.',23)
txt(650,330,'VERMELHO: junto ao furo traseiro',25,'#b34c3d')
txt(650,377,'Somente na guia direita: cerca1,902 mm³.',22)
txt(650,430,'O padrão4+5 também aparece na G2',23)
txt(650,466,'oriunda da montagem configurada.',23)
txt(650,530,'Furo nominal confirmado: Ø6 ×10;',23)
txt(650,566,'eixo11 acima da face inferior do fundo.',23)
txt(650,638,'Não ampliar furos nem rebaixar o fundo',23,'#784b3f')
txt(650,674,'para apenas zerar volumes do CAD.',23,'#784b3f')
txt(45,866,'Diagnóstico geométrico; regulagem, contato funcional e montagem real ainda precisam ser confirmados.',22)
im.save(HERE/'Mapa_intersecoes.png')
print(json.dumps(out['summary']))
