from pathlib import Path
import json
import FreeCAD as App
root=(Path(__file__).resolve().parent / '.').resolve()
data=json.loads(((Path(__file__).resolve().parent / 'Montagem_R14.json').resolve()).read_text(encoding='utf-8'))
assert 'pitch_mm' not in data,'Ajuste já realizado'
d=next(d for d in App.listDocuments().values() if d.FileName and Path(d.FileName).resolve()==(Path(__file__).resolve().parent / 'Guedala_Park_R14_Correr_Simples.FCStd').resolve())
for row in data['rows']:
 driver=d.getObject(row['drivers'][1]);p=driver.Placement;p.Base.y+=4;driver.Placement=p
 # second channel four solids + the two brakes belonging to the rear lane
 for ix in [4,5,6,7,10,11]:
  o=d.getObject(row['tracks'][ix]);p=o.Placement;p.Base.y+=4;o.Placement=p
data['pitch_mm']=38
data['hypotheses'][1]='Passo38 entre vias: perfis RM-023 largura34 separados4, proposto para separar envoltórias. Não eixo certificado.'
data['hypotheses'].append('Ensaio inicial passo34 interceptou reservas guia/retenção220mm3; não sólidos de fabricante. Passo38 altera montagem proposta, sem alterar hardware/material. Folgas físicas ainda pendentes.')
data['nominal_package_mm']={'rear_carriage_y':75,'reserve_frontal':82,'margin_to_clothing_zone':7,'wood_clearance_between_planes':20,'guide_retention_gap':2}
((Path(__file__).resolve().parent / 'Montagem_R14.json').resolve()).write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8');d.recompute();d.save();result={'pitch_mm':38}
