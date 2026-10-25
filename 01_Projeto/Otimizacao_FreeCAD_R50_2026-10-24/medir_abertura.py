"""Mede abertura real com GUI. Nao modifica ou salva o documento de origem.

Executar na GUI por runpy.run_path, depois que a chamada MCP tenha retornado.
O JSON job.json define modo (original/sem_observador), arquivo e repeticao.
"""
from pathlib import Path
import cProfile
import hashlib
import io
import json
import pstats
import time
import traceback
import ast
import FreeCAD as App
import FreeCADGui as Gui

HERE=Path(__file__).resolve().parent

def write(name,value):
    (HERE/name).write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

job=json.loads((HERE/'job.json').read_text(encoding='utf-8'))
tag=job['tag']
source=Path(job['file'])
observer=getattr(App,'_ai_observer',None)
detached=False
legacy_originals={}
result={'tag':tag,'file':str(source),'mode':job['mode'],'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest()}
try:
    write('Progresso_benchmark.json',dict(tag=tag,stage='closing_previous'))
    # Closing is outside the interval. Remove observer only while closing to
    # avoid measuring unrelated bookkeeping and restore it for original mode.
    if observer:
        App.removeDocumentObserver(observer)
        detached=True
    allowed={str((HERE.parents[1]/'01_Projeto/Gavetas_escritorio_R49_2026-10-24/Guedala_Park_R49_Gavetas_escritorio.FCStd').resolve()).casefold(),
             str((HERE/'Guedala_Park_R50_Completo_Otimizado.FCStd').resolve()).casefold()}
    for document in list(App.listDocuments().values()):
        if not document.FileName or str(Path(document.FileName).resolve()).casefold() not in allowed:
            raise RuntimeError('Documento fora dos arquivos de teste esta aberto; interromper benchmark sem fechar')
        assert not Gui.getDocument(document.Name).Modified, 'Documento com alteracoes nao salvas; nao fechar'
        assert not any('Touched' in o.State for o in document.Objects), 'Documento com alteracoes pendentes; nao fechar'
        App.closeDocument(document.Name)
    if observer and job['mode']=='original':
        if job.get('legacy_observer'):
            tree=ast.parse((HERE/'event_observer.antes.py').read_text(encoding='utf-8'))
            for method in ['slotCreatedObject','slotChangedObject']:
                legacy_originals[method]=getattr(observer.__class__,method)
                node=next(n for n in ast.walk(tree) if isinstance(n,ast.FunctionDef) and n.name==method)
                namespace={'FreeCAD':App}
                exec(compile(ast.Module(body=[node],type_ignores=[]),'<legacy_observer_benchmark>','exec'),namespace)
                setattr(observer.__class__,method,namespace[method])
        App.addDocumentObserver(observer)
        detached=False
    Gui.updateGui()
    write('Progresso_benchmark.json',dict(tag=tag,stage='opening',mode=job['mode']))
    profile=cProfile.Profile()
    if job.get('profile',True):profile.enable()
    t=time.perf_counter()
    document=App.openDocument(str(source))
    restored=time.perf_counter()
    Gui.activeDocument().activeView().viewAxonometric()
    Gui.activeDocument().activeView().fitAll()
    Gui.updateGui()
    Gui.activeDocument().activeView().redraw()
    Gui.updateGui()
    finished=time.perf_counter()
    if job.get('profile',True):profile.disable()
    stream=io.StringIO()
    if job.get('profile',True):
        pstats.Stats(profile,stream=stream).sort_stats('cumulative').print_stats(35)
        (HERE/f'Perfil_{tag}.txt').write_text(stream.getvalue(),encoding='utf-8')
        profile.dump_stats(str(HERE/f'Perfil_{tag}.prof'))
    result.update(restore_s=restored-t,scene_s=finished-restored,total_s=finished-t,
                  objects=len(document.Objects),touched=sum('Touched' in o.State for o in document.Objects),
                  source_sha256_after=hashlib.sha256(source.read_bytes()).hexdigest(),profile_enabled=job.get('profile',True),legacy_observer=job.get('legacy_observer',False),
                  method='Reopen in same FreeCAD GUI, warmed file cache; interval includes document restore, axonometric camera, fitAll, updateGui and redraw. Excludes process startup and closing previous document.')
    # Visual checks occur after the measured interval. Use exactly the same
    # saved camera for the two rendered images, irrespective of current dock size.
    if tag in ['r49_corrigida_01','r50_corrigida_01']:
        label='R49' if tag.startswith('r49') else 'R50'
        view=Gui.activeDocument().activeView()
        if label=='R49':(HERE/'Camera_R49.iv').write_text(view.getCamera(),encoding='utf-8')
        else:view.setCamera((HERE/'Camera_R49.iv').read_text(encoding='utf-8'));Gui.updateGui()
        appearance={}
        for obj in document.Objects:
            vo=obj.ViewObject
            if vo is None:continue
            appearance[obj.Name]={key:str(getattr(vo,key)) for key in
                ['ShapeColor','DiffuseColor','LineColor','PointColor','Transparency','Visibility','DisplayMode','Deviation','AngularDeflection','ShowInTree']
                if hasattr(vo,key)}
        write(f'Aparencia_{label}.json',appearance)
        view.saveImage(str(HERE/f'Vista_{label}.png'),1280,960,'Current')
    write(f'Tempo_{tag}.json',result)
    write('Progresso_benchmark.json',dict(tag=tag,stage='complete',**{k:v for k,v in result.items() if k!='tag'}))
except BaseException:
    result['error']=traceback.format_exc()
    write(f'Tempo_{tag}.json',result)
    write('Progresso_benchmark.json',dict(tag=tag,stage='error',error=result['error']))
finally:
    if observer and legacy_originals:
        if not detached:App.removeDocumentObserver(observer)
        for method,func in legacy_originals.items():setattr(observer.__class__,method,func)
        detached=True
    if observer and detached:
        App.addDocumentObserver(observer)
