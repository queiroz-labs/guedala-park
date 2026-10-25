"""Leitura do agendamento; NUNCA modifica configuracao da aplicacao."""
from pathlib import Path
from datetime import datetime,timezone
import os,json,sys,hashlib,tomllib
HERE=Path(__file__).resolve().parent
codex_root=Path(os.environ.get('CODEX_HOME',str(Path.home()/'.codex')))
path=codex_root/'automations/guedala-park-executar-plano-at-7h/automation.toml'
raw=path.read_bytes();cfg=tomllib.loads(raw.decode('utf8'))
assert cfg['id']=='guedala-park-executar-plano-at-7h' and cfg['kind']=='heartbeat'
assert cfg['target_thread_id']=='01a170d8-a0e7-7e63-b6b9-ff11a6283edd'
now=datetime.now(timezone.utc);confirmed='--confirmar-pausa'in sys.argv
if confirmed:
 assert now>=datetime(2026,10,25,10,tzinfo=timezone.utc)
 assert cfg['status']=='PAUSED','Pausa ainda nao confirmada na configuracao; usar ferramenta da aplicacao, nao editar este arquivo'
out=dict(read_UTC=now.isoformat(),configuration=cfg,configuration_file_sha256=hashlib.sha256(raw).hexdigest(),
 method='Leitura do automation.toml; mudancas so pela ferramenta oficial da aplicacao',paused_confirmed=confirmed)
name='Automacao_pausa_confirmada.json'if confirmed else 'Automacao_configuracao_lida.json'
(HERE/name).write_text(json.dumps(out,indent=2,ensure_ascii=False)+'\n',encoding='utf8')
print(json.dumps(dict(id=cfg['id'],status=cfg['status'],kind=cfg['kind'],read_UTC=out['read_UTC'],paused_confirmed=confirmed)))
