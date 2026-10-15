from pathlib import Path
import json
import FreeCAD as App
import FreeCADGui as Gui
from PySide import QtCore

root=Path(__file__).resolve().parent
editors=[]
for o in Gui.getMainWindow().findChildren(QtCore.QObject):
    if not hasattr(o,'toPlainText'):
        continue
    chain=[];p=o
    for _ in range(6):
        if p is None:break
        chain.append({'class':p.metaObject().className(),'name':p.objectName()});p=p.parent()
    is_report=any('report' in (v['class']+' '+v['name']).lower() for v in chain)
    editors.append({'chain':chain,'is_report':is_report,'text':o.toPlainText() if is_report else None})
docs=[]
for d in App.listDocuments().values():
    bad=[]
    for o in d.Objects:
        flags=[str(s) for s in o.State if str(s) not in ['Up-to-date']]
        if 'Invalid' in o.State or 'Error' in o.State:
            bad.append({'name':o.Name,'label':o.Label,'state':flags})
    docs.append({'name':d.Name,'file':d.FileName,'objects':len(d.Objects),'bad':bad})
(root/'Erros_interface.json').write_text(json.dumps({'editors':editors,'documents':docs},ensure_ascii=False,indent=2),encoding='utf-8')
