from pathlib import Path
import json,hashlib
here=Path(__file__).resolve().parent
records=[]
for suffix in ['Mod','v1-1/Mod']:
    p=Path('C:/Users/Elias/AppData/Roaming/FreeCAD')/suffix/'AICopilot/InitGui.py'
    source=p.read_text(encoding='utf-8')
    marker='# AUTO-START: Initialize AI service when FreeCAD GUI loads'
    assert marker in source
    source=source.replace(marker,'# Keep the factory outside InitGui globals, which FreeCAD may clear.\nFreeCAD._ai_service_factory = GlobalAIService\n\n'+marker,1)
    assert 'new_service = GlobalAIService()' in source
    source=source.replace('new_service = GlobalAIService()','new_service = FreeCAD._ai_service_factory()')
    compile(source,str(p),'exec');p.write_text(source,encoding='utf-8')
    records.append({'file':str(p),'final_sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
(here/'Correcao_factory.json').write_text(json.dumps(records,indent=2),encoding='utf-8')
print('Factory persistida no módulo FreeCAD; fonte compilada.')
