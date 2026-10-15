from pathlib import Path
import hashlib,json
here=Path(__file__).resolve().parent
targets=[Path('C:/Users/Elias/AppData/Roaming/FreeCAD')/suffix/'AICopilot/InitGui.py' for suffix in ['Mod','v1-1/Mod']]
records=[]
for i,p in enumerate(targets):
    raw=p.read_bytes();source=raw.decode('utf-8').replace('\r\n','\n')
    if '__ai_global_service' not in source:
        raise RuntimeError(f'Fonte diferente da examinada: {p}')
    backup=here/f'InitGui_antes_{i}.py'
    if backup.exists():
        assert backup.read_bytes()==raw, 'Original diferente do backup'
    else:
        backup.write_bytes(raw)
    source=source.replace('__ai_global_service','_ai_global_service').replace('__ai_socket_server','_ai_socket_server').replace('__ai_observer','_ai_observer')
    old='''        if self.event_observer:
            self.event_observer = None'''
    new='''        if self.event_observer:
            # Unregister callbacks before releasing the QObject during restart.
            FreeCADGui.Selection.removeObserver(self.event_observer)
            FreeCAD.removeDocumentObserver(self.event_observer)
            window = FreeCADGui.getMainWindow()
            if window:
                window.removeEventFilter(self.event_observer)
            self.event_observer = None'''
    assert old in source
    source=source.replace(old,new,1)
    lines=source.splitlines()
    for n,line in enumerate(lines):
        if 'Claude Desktop:' in line and 'os.path.exists' in line:
            lines[n]='                    FreeCAD.Console.PrintMessage(f"MCP local service: {\'Running\' if service.is_running else \'Stopped\'}\\n")'
    source='\n'.join(lines)+'\n'
    compile(source,str(p),'exec')
    p.write_text(source,encoding='utf-8')
    records.append({'file':str(p),'backup':str(backup),'before_sha256':hashlib.sha256(raw).hexdigest(),'after_sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
(here/'Correcao.json').write_text(json.dumps(records,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(records,ensure_ascii=False))
