"""FreeCADCmd, somente leitura: aceite do candidato SALVO em grade de 25 mm.

Definir GP_REPO e GP_PISOS_DIR. Lê Guedala_Park_Piso_candidato.FCStd da
saída externa; gera Aceite_pisos.json ali. Não chama a macro nem salva CAD.
"""
import ast
import hashlib
import json
import os
from pathlib import Path
import sys
import traceback


def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    import FreeCAD as App
    root=Path(os.environ['GP_REPO']).resolve()
    out=Path(os.environ['GP_PISOS_DIR']).resolve()
    candidate=out/'Guedala_Park_Piso_candidato.FCStd'
    metadata=json.loads((out/'Pisos.json').read_text(encoding='utf8'))
    assert sha(candidate)==metadata['candidate_sha256']
    macro=root/'ferramentas/estudos/modelar_pisos.FCMacro'
    tree=ast.parse(macro.read_text(encoding='utf8'))
    # Carrega as mesmas funções geométricas, sem o bloco try:main() da GUI.
    assert isinstance(tree.body[-1],ast.Try)
    tree.body.pop()
    namespace={'__file__':str(macro)}
    exec(compile(tree,str(macro),'exec'),namespace)
    doc=App.openDocument(str(candidate),True)
    floors=[doc.getObject(p['objeto']) for p in metadata['pisos']]
    assert all(o.Visibility for o in floors)
    assert all(not doc.getObject(n).Visibility for n in namespace['OLD'])
    shapes=[namespace['global_shape'](o) for o in floors]
    assert all(s.isValid() and s.isClosed() and len(s.Solids)==1 for s in shapes)
    assert all(abs(s.BoundBox.ZMin+50)<1e-6 and abs(s.BoundBox.ZMax)<1e-6 for s in shapes)
    walls=[namespace['global_shape'](o) for o in doc.getObject('ParedesInteiras').Group if o.Shape.BoundBox.ZMin<1e-6]
    acceptance=namespace['grid_acceptance'](shapes,walls)
    assert json.loads(json.dumps(acceptance))==metadata['aceite'], 'Geometria salva difere da conferida na GUI'
    assert not acceptance['celulas_sem_piso_nem_parede']
    assert not acceptance['sobreposicoes']
    assert acceptance['area_piso_sob_parede_m2']==0
    # Cada encontro deve ter face inteira em comum, sem volume compartilhado.
    contacts=[]
    for a,b in ((0,3),(1,3),(0,4),(2,4)):
        common=shapes[a].common(shapes[b])
        shared=0.
        for fa in shapes[a].Faces:
            na=fa.normalAt(0,0)
            for fb in shapes[b].Faces:
                if na.dot(fb.normalAt(0,0))>-.999:continue
                if abs((fa.CenterOfMass-fb.CenterOfMass).dot(na))>1e-6:continue
                shared+=fa.common(fb).Area
        expected=shapes[3].BoundBox.YLength*50 if b==3 else 700*50
        assert common.Volume<.01 and abs(shared-expected)<.01,(a,b,shared)
        contacts.append(dict(a=floors[a].Name,b=floors[b].Name,area_contato_mm2=round(shared,6),volume_mm3=common.Volume))
    App.closeDocument(doc.Name)
    assert sha(candidate)==metadata['candidate_sha256']
    assert all(sha(Path(p))==h for p,h in metadata['guardados'].items())
    result=dict(resultado='OK',candidate_sha256=sha(candidate),**acceptance,
                contatos_por_face=contacts,antigos_ocultos=namespace['OLD'],
                solidos_validos=5,vinilico_solido_unico=True,fonte_e_base_preservadas=True,
                controle_negativo_fresta_1mm_m2=metadata['controle_negativo_fresta_1mm'],
                controle_negativo_penetracao_1mm_mm3=metadata['controle_negativo_penetracao_1mm_mm3'])
    (out/'Aceite_pisos.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    print(json.dumps({k:result[k] for k in ('resultado','celulas_interiores','celulas_sem_piso_nem_parede','sobreposicoes','vinilico_solido_unico')},ensure_ascii=False))


if __name__=='__main__' or 'FreeCAD' in sys.modules:
    try:main()
    except Exception:
        out=Path(os.environ['GP_PISOS_DIR'])
        (out/'erro_aceite.txt').write_text(traceback.format_exc(),encoding='utf8')
        raise
