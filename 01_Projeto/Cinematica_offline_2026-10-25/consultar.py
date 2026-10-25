"""Interface pequena para estudos futuros, sem carregar o FreeCAD."""
import argparse,json
from cinematica import Engine
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--listar',action='store_true')
parser.add_argument('--folha')
parser.add_argument('--angulo',type=float,default=0.)
parser.add_argument('--incluir-ocultas',action='store_true',help='Consulta historica explicita; nao reativa o projeto')
a=parser.parse_args();engine=Engine()
if a.listar:
 print(json.dumps([dict(name=n,label=engine.data['leaves'][n]['label'],visible=engine.data['leaves'][n]['visible_effective']) for n in engine.leaf_names(a.incluir_ocultas)],ensure_ascii=False,indent=2))
else:
 if not a.folha:parser.error('Informar --folha ou --listar')
 if a.folha not in engine.leaf_names(a.incluir_ocultas):parser.error('Folha ausente ou oculta nesta consulta')
 if not 0<=a.angulo<=86:parser.error('Intervalo validado:0..86graus')
 print(json.dumps(dict(leaf=a.folha,requested_angle_deg=a.angulo,
  centers_global_mm=engine.centers(a.folha,a.angulo,include_hidden=a.incluir_ocultas),
  source_sha256=engine.data['sha256'],scope='CG geometricos das frentes; sem editarCAD ou validar ferragens/colisoes.'),ensure_ascii=False,indent=2))
