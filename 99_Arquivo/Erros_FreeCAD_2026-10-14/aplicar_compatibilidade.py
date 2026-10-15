from pathlib import Path
import ast,hashlib,json

root=Path(__file__).resolve().parent
diag=root/'Diagnostico_addon'
addon=Path('C:/Users/Elias/AppData/Local/Packages/OpenAI.Codex_2p2nqsd0c76g0/LocalCache/Roaming/FreeCAD/v1-1/Mod/AICopilot').resolve()
spec=json.loads((diag/'Diagnostico_Qt.json').read_text(encoding='utf-8'))
backup=root/'Backup_addon';backup.mkdir(exist_ok=True)
rows=[]
prepared=[]
for item in spec['changes']:
    path=Path(item['path']).resolve()
    assert path.is_relative_to(addon)
    assert path.relative_to(addon).as_posix() in ['event_observer.py','commands/ai_commands.py']
    data=path.read_bytes()
    assert hashlib.sha256(data).hexdigest()==item['source_sha256'],path
    old=item['old_import'].encode('utf-8')
    assert data.count(old)==1
    newline=b'\r\n' if b'\r\n' in data else b'\n'
    new=item['new_import'].replace('\n',newline.decode()).encode('utf-8')
    updated=data.replace(old,new,1)
    ast.parse(updated.decode('utf-8'))
    assert updated.decode('utf-8').replace('\r\n','\n')==(diag/item['proposed_file']).read_text(encoding='utf-8')
    prepared.append((item,path,data,updated))
for item,path,data,updated in prepared:
    saved=backup/(path.name+'.antes.py')
    assert not saved.exists(),'Preserve previous backup; do not rerun blindly'
    saved.write_bytes(data)
    path.write_bytes(updated)
    rows.append({'path':str(path),'backup':str(saved),'sha256_before':hashlib.sha256(data).hexdigest(),'sha256_after':hashlib.sha256(path.read_bytes()).hexdigest(),'change':'Qt import only'})
(root/'Compatibilidade_aplicada.json').write_text(json.dumps({'status':'applied','files':rows,'scope':'Only two imports; no server/observer activation, dependencies, CAD or model settings changed'},ensure_ascii=False,indent=2),encoding='utf-8')
print('QT_COMPATIBILITY_APPLIED',len(rows))
