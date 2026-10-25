"""Aplica somente a correcao de bookkeeping durante restore, com hash e backup."""
from pathlib import Path
import hashlib
import json
import shutil

here=Path(__file__).resolve().parent
meta=json.loads((here/'Patch_integracao.json').read_text(encoding='utf-8'))
target=Path(meta['target'])
assert hashlib.sha256(target.read_bytes()).hexdigest()==meta['source_sha256'], 'Integracao mudou; reconciliar antes de substituir'
backup=here/'event_observer.original_bytes.py'
if backup.exists():
    assert hashlib.sha256(backup.read_bytes()).hexdigest()==meta['source_sha256'], 'Backup inesperado'
else:
    shutil.copy2(target,backup)
candidate=(here/'event_observer.otimizado.py').read_bytes()
assert hashlib.sha256(candidate).hexdigest()==meta['candidate_sha256']
target.write_bytes(candidate)
(here/'Integracao_aplicada.json').write_text(json.dumps({'target':str(target),'backup':str(backup),
    'sha256_before':meta['source_sha256'],'sha256_after':hashlib.sha256(target.read_bytes()).hexdigest()},indent=2),encoding='utf-8')
print('Correcao aplicada com copia original preservada')
