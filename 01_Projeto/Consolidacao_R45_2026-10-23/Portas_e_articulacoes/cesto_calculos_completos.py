import json,math
from pathlib import Path
P=Path(__file__).parent
objects=json.loads((P.parent/'Inventario/Folhas_ativas_globais_R44.json').read_text(encoding='utf8'))
frame=[o for o in objects if o['name'] in ['PecaCestoR'+str(i).zfill(3) for i in range(4,17)]]
front=next(o for o in objects if o['name']=='PecaCestoR003')
def moment(o,rho,angle):
 b=o['bbox'];dy=((b[1]+b[4])/2-6440)/1000;dz=((b[2]+b[5])/2-120)/1000
 a=math.radians(angle)
 return o['volume']/1e9*rho*9.80665*(-dy*math.cos(a)+dz*math.sin(a))
results=[]
for rho in [650,750,900]:
 for angle in [0,15,30,45,55]:
  a=math.radians(angle); mf=moment(front,rho,angle); ma=sum(moment(o,rho,angle) for o in frame)
  laundry=[8*9.80665*(-dy*math.cos(a)+dz*math.sin(a)) for dy in [.025,.225] for dz in [.025,.425]]
  center=8*9.80665*(-.125*math.cos(a)+.225*math.sin(a))
  results.append(dict(rho=rho,angle=angle,front_Nm=mf,frame_Nm=ma,clothes_center_Nm=center,total_center_Nm=mf+ma+center,total_envelope_Nm=[mf+ma+min(laundry),mf+ma+max(laundry)]))
data={'premissas':'Frente e armação gabarito assumidas madeira homogênea650/750/900kg/m³. Não material aprovado. Armação inclui13peças004..016; exclui pivôs, saco, ferragens, pega, mãos, choques. Baseado nas AABB retangulares do export R44. Eixo idealX emY6440/Z120. Roupa8kg no centro ou qualquer ponto do envelope. Não substitui CAD comercial.','frame_volume_m3':sum(o['volume'] for o in frame)/1e9,'frame_mass_scenarios':{str(r):sum(o['volume'] for o in frame)/1e9*r for r in [650,750,900]},'pecas':[o['name'] for o in frame],'resultados':results}
(P/'Cesto_com_armacao.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps(data,ensure_ascii=False,indent=2))
