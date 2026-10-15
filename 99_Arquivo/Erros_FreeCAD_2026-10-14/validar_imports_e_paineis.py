from pathlib import Path
import importlib.util,json
import FreeCAD as App
import FreeCADGui as Gui
from PySide import QtCore

root=Path(__file__).resolve().parent
addon=Path('C:/Users/Elias/AppData/Local/Packages/OpenAI.Codex_2p2nqsd0c76g0/LocalCache/Roaming/FreeCAD/v1-1/Mod/AICopilot')
rows=[]
for key,rel in [('event_observer','event_observer.py'),('ai_commands','commands/ai_commands.py')]:
    spec=importlib.util.spec_from_file_location('validacao_qt_'+key,str(addon/rel))
    m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
    rows.append({'module':key,'file':str(addon/rel),'import':'ok'})
widgets=[]
for o in Gui.getMainWindow().findChildren(QtCore.QObject):
    name=o.objectName();cl=o.metaObject().className()
    if o.inherits('QDockWidget') or 'notif' in (name+' '+cl).lower():
        widgets.append({'name':name,'class':cl,'visible':o.isVisible() if hasattr(o,'isVisible') else None})
tables=[]
for o in Gui.getMainWindow().findChildren(QtCore.QObject):
    if not o.inherits('QAbstractItemView'):continue
    p=o;chain=[]
    for _ in range(7):
        if p is None:break
        chain.append(p.objectName()+' '+p.metaObject().className());p=p.parent()
    if not any('notif' in v.lower() for v in chain):continue
    model=o.model()
    if model is None:continue
    n=model.rowCount();c=model.columnCount()
    cells=[[str(model.data(model.index(i,j),QtCore.Qt.DisplayRole)) for j in range(c)] for i in range(n)]
    tables.append({'name':o.objectName(),'class':o.metaObject().className(),'chain':chain,'rows':n,'columns':c,'cells':cells})
report={'imports':rows,'widgets':widgets,'notification_tables':tables,'saveCopy_doc':App.ActiveDocument.saveCopy.__doc__,'observer_started_by_validation':False}
(root/'Imports_paineis.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
