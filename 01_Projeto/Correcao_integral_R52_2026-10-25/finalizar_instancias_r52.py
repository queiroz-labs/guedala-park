"""Finalizacao da candidata R52: esconder instancias graficas dos atalhos."""
import ast
from pathlib import Path

FILE=Path('C:/Users/Elias/Documents/PROJETOS/Guedala park/guedala-park/01_Projeto/Correcao_integral_R52_2026-10-25/criar_r52.py')
tree=ast.parse(FILE.read_text(encoding='utf-8'))
assert isinstance(tree.body[-1],ast.Try)
tree.body=tree.body[:-1]  # load helpers without running the guarded creator
exec(compile(tree,str(FILE),'exec'),globals())

OLD_SHA='b5493b1952265398c1ad9b82a3ee5ead8d3a6a4db7d4257f5ee780738c24e8a6'
assert hashlib.sha256(TARGET.read_bytes()).hexdigest()==OLD_SHA
d=App.getDocument('Guedala_Park_R52_Corrigido')
assert d is not None
prior=json.loads((HERE/'Verificacao_R52.json').read_text(encoding='utf-8'))
before=snapshot(d)
names=['AcessoControleR21']+['AcessoControleR%03d'%i for i in range(1,10)]+['AcessoControleR34']
target_vis={d.getObject(n).LinkedObject.Name:d.getObject(n).LinkedObject.Visibility for n in names}
changed=[]
for n in names:
    o=d.getObject(n)
    if o.Visibility:changed.append(n)
    o.Visibility=False
assert all(d.getObject(n).Visibility==v for n,v in target_vis.items()),'Alvo do link foi ocultado indevidamente'
d.recompute()
after=snapshot(d);diff=differences(before,after)
assert all(r['changed']==['visible'] for r in diff),diff
assert set(r['name'] for r in diff)==set(changed),diff
save=runpy.run_path(str(ROOT/'guedala-park/01_Projeto/Otimizacao_FreeCAD_R50_2026-10-24/serializacao_binaria.py'))['salvar_documento'](d,TARGET)
# Keep the original candidate verification/snapshot as provenance.
assert not (HERE/'Verificacao_primeira_gravacao_R52.json').exists()
shutil.copy2(HERE/'Verificacao_R52.json',HERE/'Verificacao_primeira_gravacao_R52.json')
shutil.copy2(HERE/'Snapshot_apos.json',HERE/'Snapshot_primeira_gravacao_R52.json')
App.closeDocument(d.Name);d=App.openDocument(str(TARGET))
reopened=snapshot(d);assert not differences(after,reopened)
assert all(not d.getObject(n).Visibility for n in names)
assert all(d.getObject(n).Visibility==v for n,v in target_vis.items())
original=json.loads((HERE/'Snapshot_antes.json').read_text(encoding='utf-8'))
final_diff=differences(original,reopened)
assert [r['name'] for r in final_diff if any(k in r['changed'] for k in ['local','global','geometry','valid'])]==['Peca131']
assert hashlib.sha256(SOURCE.read_bytes()).hexdigest()==EXPECTED
write('Snapshot_apos.json',reopened);write('Diferencas_R51_R52.json',final_diff)
changes=json.loads((HERE/'Alteracoes_R52.json').read_text(encoding='utf-8'))
changes.extend({'object':n,'property':'Visibility','before':True,'after':False,'reason':'Control alias rendered a duplicate drawer at local origin; real target and property access preserved.'} for n in changed)
write('Alteracoes_R52.json',changes)
prior.update(target=save,reopened=True,reopen_differences=[],hidden_render_instances=names,
             visible_aliases_corrected=changed,alias_target_visibilities_preserved=target_vis,
             intermediate_R52_sha256=OLD_SHA,active_document=d.Name)
write('Verificacao_R52.json',prior)
Gui.activeDocument().activeView().viewAxonometric();Gui.activeDocument().activeView().fitAll();Gui.updateGui()
Gui.activeDocument().activeView().saveImage(str(HERE/'Vista_R52.png'),1600,1000,'Current')
