"""Exclusao de seis instancias externas explicitamente autorizada por Elias."""
from pathlib import Path
import json,hashlib,runpy,shutil
import FreeCAD as App
import FreeCADGui as Gui

ROOT=Path('C:/Users/Elias/Documents/PROJETOS/Guedala park')
HERE=ROOT/'guedala-park/02_Modelo_3D'
TARGET=HERE/'Guedala_Park_R52_Corrigido.FCStd'
SOURCE=ROOT/'guedala-park/01_Projeto/Revisao_sem_tubos_R51_2026-10-25/Guedala_Park_R51_Sem_estudo_tubular.FCStd'
OLD_SHA='01488a9d0b1dc048b2270cbdb37997c02d8d92ca6b59c8cc5c23c0cc021d6d6c'
SOURCE_SHA='ab5323bb12f8eca40b25bdfe4eadc8a3221c82b0646f354cd1f2832acfb27c16'
assert hashlib.sha256(TARGET.read_bytes()).hexdigest()==OLD_SHA
d=App.getDocument('Guedala_Park_R52_Corrigido');assert d
removed=['AcessoControleR21']+['AcessoControleR%03d'%i for i in range(1,6)]
targets={n:d.getObject(n).LinkedObject.Name for n in removed}
all_expressions={o.Name:list(o.ExpressionEngine) for o in d.Objects if o.Name not in removed}
dependencies={}
for n in removed:
    o=d.getObject(n);assert o.TypeId=='App::Link'
    dependencies[n]=[x.Name for x in o.InList]
    assert all(x.TypeId=='App::DocumentObjectGroup' for x in o.InList),(n,dependencies[n])
    assert not any(n in str(expr) for exprs in all_expressions.values() for expr in exprs),(n,'expression depends on alias')

def geometry(doc):
    out={}
    for o in doc.Objects:
        if o.isDerivedFrom('Part::Feature') and not o.Shape.isNull():
            s=o.Shape;b=s.BoundBox
            out[o.Name]=list(o.Placement.toMatrix().A)+list(o.getGlobalPlacement().toMatrix().A)+[s.Volume,s.Area,b.XMin,b.YMin,b.ZMin,b.XMax,b.YMax,b.ZMax,len(s.Solids),len(s.Faces),len(s.Edges),len(s.Vertexes)]
    return out

def same(a,b):
    return set(a)==set(b) and all(max(abs(x-y) for x,y in zip(a[n],b[n]))<1e-6 for n in a)

base=geometry(d)
assert not (HERE/'Verificacao_pre_exclusao_R52.json').exists()
shutil.copy2(HERE/'Verificacao_R52.json',HERE/'Verificacao_pre_exclusao_R52.json')
shutil.copy2(HERE/'Snapshot_apos.json',HERE/'Snapshot_pre_exclusao_R52.json')
for n in removed:d.removeObject(n)
added=[]
for groupname,indexname,label,partnames in [
    ('ControlesAmbienteR21','GavetasReaisQuartoR52','Gavetas roupeiro - referencias das pecas reais',['Gaveta','Gaveta001','Gaveta002','Gaveta003']),
    ('ControlesAmbienteR002','GavetasReaisCozinhaR52','Gavetas cozinha - referencias das pecas reais',['Gaveta004','Gaveta005'])]:
    o=d.addObject('App::FeaturePython',indexname);o.Label=label
    o.addProperty('App::PropertyLinkList','GavetasReais','Acessos');o.GavetasReais=[d.getObject(n) for n in partnames]
    o.addProperty('App::PropertyString','Orientacao','Acessos')
    o.Orientacao='Selecione uma referencia para abrir a peca real e editar Extensao em mm. Abra a folha de correr antes de extrair as gavetas do roupeiro. Este indice nao desenha copias.'
    d.getObject(groupname).addObject(o);added.append(o.Name)
d.recompute();assert same(base,geometry(d))
assert all(d.getObject(n) and d.getObject(n).Visibility for n in targets.values())
assert all(list(d.getObject(n).ExpressionEngine)==expr for n,expr in all_expressions.items())
save=runpy.run_path(str(ROOT/'guedala-park/01_Projeto/Otimizacao_FreeCAD_R50_2026-10-24/serializacao_binaria.py'))['salvar_documento'](d,TARGET)
App.closeDocument(d.Name);d=App.openDocument(str(TARGET))
assert same(base,geometry(d))
assert all(d.getObject(n) is None for n in removed)
assert all(d.getObject(n) and d.getObject(n).Visibility for n in targets.values())
assert all(list(d.getObject(n).ExpressionEngine)==expr for n,expr in all_expressions.items())
invalid=[o.Name for o in d.Objects if o.isDerivedFrom('Part::Feature') and not o.Shape.isNull() and not o.Shape.isValid()]
assert not invalid
assert hashlib.sha256(SOURCE.read_bytes()).hexdigest()==SOURCE_SHA
snapshot=json.loads((HERE/'Snapshot_apos.json').read_text(encoding='utf-8'))
for n in removed:snapshot.pop(n)
for n in added:
    o=d.getObject(n);v=o.ViewObject
    snapshot[n]={'type':o.TypeId,'label':o.Label,'visible':o.Visibility,'expressions':[],
        'visual':{k:str(getattr(v,k)) for k in ['ShapeColor','LineColor','PointColor','Transparency','DisplayMode','DiffuseColor'] if k in v.PropertiesList}}
(HERE/'Snapshot_apos.json').write_text(json.dumps(snapshot,ensure_ascii=False,indent=2),encoding='utf-8')
report=json.loads((HERE/'Verificacao_R52.json').read_text(encoding='utf-8'))
report.update(target=save,objects_after=len(d.Objects),added=sorted(report['added']+added),removed=removed,
    removed_alias_targets_preserved=targets,removed_alias_incoming_dependencies=dependencies,
    deletion_authorization='Elias: as gavetas fora do apartamento pode remover de vez, acho q foi teste de algum modelo',
    deletion_reopened=True,deletion_geometry_and_expressions_preserved=True,invalid_native=invalid,
    pre_deletion_sha256=OLD_SHA,hidden_render_instances=[n for n in report['hidden_render_instances'] if n not in removed])
(HERE/'Verificacao_R52.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
changes=json.loads((HERE/'Alteracoes_R52.json').read_text(encoding='utf-8'))
changes.extend({'object':n,'operation':'remove external App::Link instance','real_drawer_preserved':targets[n],'authorization':'explicit user instruction'} for n in removed)
(HERE/'Alteracoes_R52.json').write_text(json.dumps(changes,ensure_ascii=False,indent=2),encoding='utf-8')
Gui.activeDocument().activeView().viewAxonometric();Gui.activeDocument().activeView().fitAll();Gui.updateGui()
Gui.activeDocument().activeView().saveImage(str(HERE/'Vista_R52.png'),1600,1000,'Current')
