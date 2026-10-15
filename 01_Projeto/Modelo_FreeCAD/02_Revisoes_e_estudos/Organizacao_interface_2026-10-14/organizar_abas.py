"""Preserve every live project tab before closing historical revisions, one per invocation."""
from pathlib import Path
import json,hashlib,ctypes,os
from ctypes import wintypes
import FreeCAD as App
import FreeCADGui as Gui
from PySide import QtWidgets

root=(Path(__file__).resolve().parent / '.').resolve();base=(Path(__file__).resolve().parent / '../..').resolve()
canonical=(Path(__file__).resolve().parent / '../Folga_teto_R28_2026-10-14/Guedala_Park_R28_Folga_Teto_Proposta.FCStd').resolve()
report_path=(Path(__file__).resolve().parent / 'Abas_preservadas.json').resolve()
def memory():
 try:
  class Counters(ctypes.Structure):
   _fields_=[('cb',wintypes.DWORD),('PageFaultCount',wintypes.DWORD)]+[(n,ctypes.c_size_t) for n in ['PeakWorkingSetSize','WorkingSetSize','QuotaPeakPagedPoolUsage','QuotaPagedPoolUsage','QuotaPeakNonPagedPoolUsage','QuotaNonPagedPoolUsage','PagefileUsage','PeakPagefileUsage','PrivateUsage']]
  k=ctypes.WinDLL('kernel32',use_last_error=True);k.GetCurrentProcess.restype=wintypes.HANDLE
  p=ctypes.WinDLL('psapi',use_last_error=True);p.GetProcessMemoryInfo.argtypes=[wintypes.HANDLE,ctypes.c_void_p,wintypes.DWORD];p.GetProcessMemoryInfo.restype=wintypes.BOOL
  c=Counters();c.cb=ctypes.sizeof(c)
  ok=p.GetProcessMemoryInfo(k.GetCurrentProcess(),ctypes.byref(c),c.cb)
  return {'pid':os.getpid(),'working_set_bytes':int(c.WorkingSetSize),'private_bytes':int(c.PrivateUsage),'read_ok':bool(ok)}
 except Exception as e:return {'read_ok':False,'error':str(e)}
def modified_titles():
 return [{'title':w.windowTitle(),'modified':w.isWindowModified()} for a in Gui.getMainWindow().findChildren(QtWidgets.QMdiArea) for w in a.subWindowList()]
current=next(d for d in App.listDocuments().values() if d.FileName and Path(d.FileName).resolve()==(Path(__file__).resolve().parent / '../Folga_teto_R28_2026-10-14/Guedala_Park_R28_Folga_Teto_Proposta.FCStd').resolve())
assert not [(o.Name,q.Name) for o in current.Objects for q in o.OutList if q.Document!=current]
if not report_path.exists():
 report={'canonical':str(canonical),'canonical_sha256_before':hashlib.sha256(canonical.read_bytes()).hexdigest(),
         'memory_before':memory(),'tabs_before':modified_titles(),'documents_before':list(App.listDocuments()),'closed':[],
         'current_backup':None,'cross_document_references_current':[],
         'reason':'User requested a stable tidy session; preserve live state before closing old project versions. isTouched/isSaved do not alone establish absence of GUI modification.'}
 ((Path(__file__).resolve().parent / 'Recuperacao_abas').resolve()).mkdir(exist_ok=True)
 backup=(Path(__file__).resolve().parent / 'Recuperacao_abas').resolve()/('ATUAL_'+current.Name+'.FCStd')
 assert not backup.exists();original=current.FileName
 current.saveCopy(str(backup));assert current.FileName==original and backup.stat().st_size>100000
 report['current_backup']={'name':current.Name,'file':str(backup),'sha256':hashlib.sha256(backup.read_bytes()).hexdigest()}
 report_path.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
else:report=json.loads(report_path.read_text(encoding='utf-8'))
assert hashlib.sha256(canonical.read_bytes()).hexdigest()==report['canonical_sha256_before']
historical=[]
for d in App.listDocuments().values():
 if d==current or not d.FileName or not d.Name.startswith('Guedala_Park_R'):continue
 path=Path(d.FileName).resolve()
 if path.is_relative_to((Path(__file__).resolve().parent / '../..').resolve()):historical.append(d)
if historical:
 d=historical[0];source=Path(d.FileName);sourcehash=hashlib.sha256(source.read_bytes()).hexdigest()
 backup=(Path(__file__).resolve().parent / 'Recuperacao_abas').resolve()/(d.Name+'.FCStd');assert not backup.exists()
 filename=d.FileName;count=len(d.Objects);name=d.Name
 d.saveCopy(str(backup));assert d.FileName==filename and backup.stat().st_size>100000
 assert hashlib.sha256(source.read_bytes()).hexdigest()==sourcehash
 report['closed'].append({'name':name,'objects':count,'source':str(source),'source_sha256_preserved':sourcehash,'memory_backup':str(backup),'backup_sha256':hashlib.sha256(backup.read_bytes()).hexdigest()})
 # Checkpoint preservation before the reversible UI close.
 report_path.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
 App.closeDocument(name)
report['documents_after']=list(App.listDocuments());report['memory_after']=memory()
report['canonical_sha256_after']=hashlib.sha256(canonical.read_bytes()).hexdigest()
assert report['canonical_sha256_after']==report['canonical_sha256_before']
report['status']='complete_current_only' if len(App.listDocuments())==1 and current.Name in App.listDocuments() else 'in_progress'
report_path.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
App.setActiveDocument(current.Name)
result={'closed_total':len(report['closed']),'remaining_docs':len(report['documents_after']),'status':report['status'],'memory_before':report['memory_before'],'memory_after':report['memory_after'],'current_sha_preserved':True}
