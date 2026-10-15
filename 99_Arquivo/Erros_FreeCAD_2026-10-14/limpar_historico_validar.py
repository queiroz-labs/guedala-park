from pathlib import Path
import json,re
import FreeCAD as App
import FreeCADGui as Gui
from PySide import QtCore,QtWidgets

root=Path(__file__).resolve().parent
canonical=(Path(__file__).resolve().parent / '../../01_Projeto/Modelo_FreeCAD/02_Revisoes_e_estudos/Programa_R25_2026-10-14/Guedala_Park_R25_Programa_Conferido.FCStd').resolve()
d=next(x for x in App.listDocuments().values() if x.FileName and Path(x.FileName).resolve()==canonical)
App.setActiveDocument(d.Name)
backup=root/'Recuperacao_memoria';backup.mkdir(exist_ok=True)
closed=[]
for old in list(App.listDocuments().values()):
    if old.Name not in ['TesteEspelhoR19','TesteEspelhoGrupoR19']:
        continue
    target=backup/(old.Name+'.FCStd')
    assert not target.exists()
    old.saveCopy(str(target))
    closed.append({'name':old.Name,'backup':str(target),'objects':len(old.Objects)})
    App.closeDocument(old.Name)

# Original console and notification entries were archived before this action.
assert (root/'Erros_interface.json').exists() and (root/'Notificacoes_antes.json').exists()
report_editors=[]
for o in Gui.getMainWindow().findChildren(QtCore.QObject):
    if not hasattr(o,'toPlainText'):continue
    p=o;chain=[]
    for _ in range(6):
        if p is None:break
        chain.append(p.objectName()+' '+p.metaObject().className());p=p.parent()
    if any('report' in v.lower() for v in chain):report_editors.append(o)
for o in report_editors:o.clear()
cleared_notifications=0
for w in QtWidgets.QApplication.topLevelWidgets():
    if w.isVisible() and w.inherits('QMenu'):
        for tree in w.findChildren(QtWidgets.QTreeWidget):
            cleared_notifications+=tree.topLevelItemCount();tree.clear()
        w.hide()

modules=[o for o in d.Objects if o.TypeId=='App::Part' and re.fullmatch(r'Modulo\d*',o.Name)]
assert len(modules)==20
for o in modules:o.touch()
recomputed=d.recompute()
text='\n'.join(o.toPlainText() for o in report_editors)
bad_lines=[s for s in text.splitlines() if any(t in s for t in ['allowed scope','Traceback','EXEC ERROR','Event observer error','Error reading from file','corrupted'])]
bad_objects=[o.Name for o in d.Objects if 'Invalid' in o.State or 'Error' in o.State]
result={'canonical':str(canonical),'temporary_tests_preserved_and_closed':closed,
        'notification_rows_archived_and_cleared':cleared_notifications,'modules_recomputed':len(modules),
        'recompute_result':recomputed,'new_error_lines':bad_lines,'invalid_objects':bad_objects,
        'fresh_report_text':text,'project_saved_during_validation':False,
        'future_logging_suppressed':False}
(root/'Validacao_interface_limpa.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
assert not bad_lines and not bad_objects
