"""Copia local das entregas manifestadas. Nao publica nem sobrescreve copias."""
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib,zipfile
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent;PROJECT=ROOT.parent
m=json.loads((HERE/'Manifesto.json').read_text(encoding='utf8'))
assert m['phase']=='encerramento' and datetime.now(timezone.utc)>=datetime(2026,10,25,10,tzinfo=timezone.utc)
v=json.loads((HERE/'Verificacao.json').read_text(encoding='utf8'));assert not v['errors']
folder=PROJECT/'05_Entregas/Execucao_ate_07h_2026-10-25';folder.mkdir(parents=True,exist_ok=True)
target=folder/'Guedala_Park_execucao_ate07h_2026-10-25.zip';assert not target.exists(),'Copia ja existe; preservar e verificar, nao sobrescrever'
files=[(ROOT/r['path']).resolve()for r in m['files']]+[HERE/'Manifesto.json',HERE/'Verificacao.json']
for p in files:assert p.is_relative_to(PROJECT.resolve()) and p.is_file()
with zipfile.ZipFile(target,'x')as z:
 for p in files:
  compression=zipfile.ZIP_STORED if p.suffix.lower()in ['.fcstd','.png','.pdf']else zipfile.ZIP_DEFLATED
  z.write(p,arcname=p.relative_to(PROJECT).as_posix(),compress_type=compression)
with zipfile.ZipFile(target)as z:assert z.testzip()is None;count=len(z.namelist())
out=dict(created_UTC=datetime.now(timezone.utc).isoformat(),file=str(target),bytes=target.stat().st_size,sha256=hashlib.sha256(target.read_bytes()).hexdigest(),
 entries=count,zip_crc=True,manifest_sha256=hashlib.sha256((HERE/'Manifesto.json').read_bytes()).hexdigest(),
 scope='Copia local das entregas/dados/estudos/fontes manifestadas, nao backup integral do repositorio. Sem upload, publicacao ou remocao de originais.')
(HERE/'Copia_seguranca.json').write_text(json.dumps(out,indent=2,ensure_ascii=False)+'\n',encoding='utf8');print(json.dumps(out,ensure_ascii=False))
