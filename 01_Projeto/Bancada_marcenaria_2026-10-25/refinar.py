"""Confere tambem material rigido/limite de retencao sem repetir todos os casos."""
from pathlib import Path
import json,runpy,hashlib
HERE=Path(__file__).resolve().parent
module=runpy.run_path(str(HERE/'calcular.py'))
d=json.loads((HERE/'Resultados.json').read_text(encoding='utf-8'))
checks=list(d['convergence_checks'])
for r in d['results']:
 err=max(abs(v) for v in r['equilibrium_error'])
 assert err<1e-4
 checks.append(dict(case=r['case'],test='equilibrio_forca_e_momentos',max_residual=err,passed=True))
front=[module['patch'](20,1000,650,50,60)]
for tag,E,retain in [('material_mais_rigido_E8000_frente20',8000,False),('limite_retencao_distribuida_frente20',2100,True)]:
 a=next(r for r in d['results'] if r['case']==tag)
 b=module['case'](tag,front,n=20,point_count=12,top_E_initial=E,retain_bound=retain)
 err=abs(a['max_deflection_mm']/b['max_deflection_mm']-1)
 assert err<.03,(tag,err)
 checks.append(dict(case=tag,test='grau16_pontos8_versus20_pontos12',relative_change=err,
   refined_deflection_mm=b['max_deflection_mm'],passed=True))
assert hashlib.sha256(Path(d['cad']).read_bytes()).hexdigest()==d['sha256']
(HERE/'Verificacao_calculo.json').write_text(json.dumps(dict(checks=checks,count=len(checks),all_passed=all(c['passed'] for c in checks),source_unchanged=True),indent=2)+'\n',encoding='utf-8')
print(json.dumps({'checks':len(checks),'all_passed':True}))
