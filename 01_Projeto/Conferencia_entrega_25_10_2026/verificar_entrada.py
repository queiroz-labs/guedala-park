"""Conferencia leve: hashes/arquivos/links novos, sem executar criadores ou placas."""
from pathlib import Path
import json,hashlib,re,xml.etree.ElementTree as ET,zipfile
from urllib.parse import unquote
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent
m=json.loads((HERE/'Manifesto.json').read_text(encoding='utf8'))
errors=[]
for r in m['files']:
 p=ROOT/r['path']
 if not p.is_file():errors.append(dict(path=r['path'],error='arquivo ausente'));continue
 if p.stat().st_size!=r['bytes']or hashlib.sha256(p.read_bytes()).hexdigest()!=r['sha256']:errors.append(dict(path=r['path'],error='alterado desde manifesto; revisar antes de atualizar snapshot'))
source=ROOT/'Revisao_sem_tubos_R51_2026-10-25/Guedala_Park_R51_Sem_estudo_tubular.FCStd'
with zipfile.ZipFile(source)as z:
 assert z.testzip()is None;r=ET.fromstring(z.read('Document.xml'))
 count=len(r.findall('./ObjectData/Object'));expr=len(r.findall('.//Expression'))
assert count==5833 and expr==7702
assert hashlib.sha256(source.read_bytes()).hexdigest()==m['source_R51_sha256']
old=ROOT/'Otimizacao_FreeCAD_R50_2026-10-24/Guedala_Park_R50_Completo_Otimizado.FCStd'
assert hashlib.sha256(old.read_bytes()).hexdigest()==m['historical_R50_sha256']
new_docs=[ROOT/'Retomada_25_10_2026.md',HERE/'README.md']
links=0
for p in new_docs:
 for target in re.findall(r'\]\(([^)]+)\)',p.read_text(encoding='utf8')):
  target=unquote(target.split('#')[0].strip('<>'))
  if not target or target.startswith(('http','mailto:','codex:')):continue
  links+=1
  if target=='Verificacao.json'and p.parent==HERE:continue
  if not (p.parent/target).exists():errors.append(dict(path=str(p.relative_to(ROOT)),error='link local ausente',target=target))
backup=None
if (HERE/'Copia_seguranca.json').exists():
 backup=json.loads((HERE/'Copia_seguranca.json').read_text(encoding='utf8'));bp=Path(backup['file'])
 if not bp.exists()or hashlib.sha256(bp.read_bytes()).hexdigest()!=backup['sha256']:errors.append(dict(path=str(bp),error='copia local ausente ou alterada'))
out=dict(manifest_phase=m['phase'],manifest_UTC=m['created_UTC'],files_checked=len(m['files']),new_entry_links_checked=links,
 R51_objects=count,R51_expressions=expr,R51_sha_preserved=True,R50_historical_sha_preserved=True,errors=errors,
 numerical_calculations_rerun=False,CAD_documents_opened_or_saved=False,physical_tests=0,
 local_backup_sha_checked=backup is not None,status='Integridade e entrada conferidas'if not errors else 'Revisar diferencas antes de continuar')
(HERE/'Verificacao.json').write_text(json.dumps(out,indent=2,ensure_ascii=False)+'\n',encoding='utf8')
print(json.dumps(out,ensure_ascii=False))
raise SystemExit(1 if errors else 0)
