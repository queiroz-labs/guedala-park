from pathlib import Path
import argparse,json,sys
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parents[1]/'Cinematica_offline_2026-10-25'))
from cinematica import Engine
p=argparse.ArgumentParser();p.add_argument('--listar',action='store_true');p.add_argument('--folha');p.add_argument('--angulo',type=float,default=0);p.add_argument('--incluir-ocultas',action='store_true');a=p.parse_args()
e=Engine(HERE/'Snapshot_R52.json')
if a.listar:out={n:e.data['leaves'][n]['label'] for n in e.leaf_names(a.incluir_ocultas)}
elif a.folha:out={'revision':'R52','source_sha256':e.data['sha256'],'leaf':a.folha,'angle_deg':a.angulo,'centers_mm':e.centers(a.folha,a.angulo,include_hidden=a.incluir_ocultas),'matrix':e.placement(a.folha,a.angulo,include_hidden=a.incluir_ocultas).tolist()}
else:p.error('Use --listar ou --folha.')
sys.stdout.reconfigure(encoding='utf-8');print(json.dumps(out,ensure_ascii=False,indent=2))
