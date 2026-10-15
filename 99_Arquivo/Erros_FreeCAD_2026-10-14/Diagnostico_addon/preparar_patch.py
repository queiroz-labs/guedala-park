from pathlib import Path
import ast,difflib,hashlib,json
HERE=Path(__file__).resolve().parent
ADDON=Path('C:/Users/Elias/AppData/Local/Packages/OpenAI.Codex_2p2nqsd0c76g0/LocalCache/Roaming/FreeCAD/v1-1/Mod/AICopilot')
changes=[
 ('event_observer.py','from PySide2 import QtCore','from PySide import QtCore'),
 ('commands/ai_commands.py','from PySide2 import QtCore, QtGui, QtWidgets',
  'from PySide import QtCore, QtGui\ntry:\n    from PySide import QtWidgets\nexcept ImportError:\n    # Older FreeCAD Qt wrappers expose widgets through QtGui.\n    QtWidgets = QtGui')
]
patch=[];rows=[]
for rel,old,new in changes:
 source=ADDON/rel;raw=source.read_bytes();text=raw.decode('utf-8')
 assert text.count(old)==1,(rel,'Fonte diferente do trecho revisado')
 revised=text.replace(old,new,1)
 ast.parse(text,filename=str(source));ast.parse(revised,filename=rel+'.proposto')
 dest=HERE/(Path(rel).name+'.proposto');dest.write_text(revised,encoding='utf-8',newline='')
 patch+=list(difflib.unified_diff(text.splitlines(keepends=True),revised.splitlines(keepends=True),fromfile='a/'+rel,tofile='b/'+rel))
 rows.append(dict(path=str(source),relative=rel,source_sha256=hashlib.sha256(raw).hexdigest(),proposed_file=dest.name,old_import=old,new_import=new,ast_syntax_ok=True))
(HERE/'Compatibilidade_Qt.patch').write_text(''.join(patch),encoding='utf-8',newline='')
report=dict(changes=rows,installed_wrapper=dict(package='C:/Users/Elias/AppData/Local/Programs/FreeCAD-1.1.4/Ext/PySide',QtCore='from PySide6.QtCore import *',QtGui='from PySide6.QtGui import *; from PySide6.QtWidgets import *',QtWidgets='from PySide6.QtWidgets import *'),not_applied=True,scope='Apenas imports; não inicia observer, servidor, GUI, rede ou coleta de eventos. Comportamento e API existentes preservados.',limits='Sintaxe validada por AST, sem import no runtime FreeCAD. Responsável verifica binding/API atuais e aplicabilidade antes de gravar fora do workspace.')
(HERE/'Diagnostico_Qt.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(dict(files=len(rows),patch=str(HERE/'Compatibilidade_Qt.patch'),not_applied=True),ensure_ascii=True))
