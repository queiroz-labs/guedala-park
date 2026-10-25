"""Compara recomputacao de movimentos da R49 e R50, sem salvar alteracoes.

Executar com freecadcmd.exe. Mesmas entradas, todos os Placements e caixas
envolventes dos Part::Feature comparados, incluindo grupos e historico.
"""
from pathlib import Path
import hashlib
import json
import os
import sys
import traceback
import FreeCAD as App

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
FILES=[ROOT/'01_Projeto/Gavetas_escritorio_R49_2026-10-24/Guedala_Park_R49_Gavetas_escritorio.FCStd',HERE/'Guedala_Park_R50_Completo_Otimizado.FCStd']
CASES=[('ControlePortaR10','Abertura',40),('ControleCantoR35','AberturaA',35),('ControleCantoR35','AberturaB',35),
       ('ControleCestoR15','Abertura',55),('BancoR43_Controle','Abertura1',60),('BancoR43_Controle','Abertura2',60),
       ('Gaveta','Extensao',100),('Gaveta004','Extensao',100),('Gaveta008','Extensao',100),
       ('ControleCorrerR14','Deslocamento',300),('ControleCorrerR002','Deslocamento',200),
       ('ControleVaralR35','Descida',200),('ControleFornoR35','Extracao',200),
       ('ControleGrelhaInferiorR35','Extracao',50),('ControleGrelhaSuperiorR35','Extracao',50),
       ('ControleLoopManutencaoR26','Afastamento',100),
       ('BC43_Controle','CursoEsquerda',100),('BC43_Controle','CursoDireita',100)]

def save(name,value):
    (HERE/name).write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

def snapshot(doc):
    rows={}
    for obj in doc.Objects:
        row={}
        if 'Placement' in obj.PropertiesList:
            row['placement']=list(obj.Placement.toMatrix().A)
        if obj.isDerivedFrom('Part::Feature') and not obj.Shape.isNull():
            b=obj.Shape.BoundBox
            row['bbox']=[b.XMin,b.YMin,b.ZMin,b.XMax,b.YMax,b.ZMax]
        rows[obj.Name]=row
    return rows

def differences(a,b,tol=1e-6):
    result=[]
    for n in set(a)|set(b):
        if n not in a or n not in b or set(a[n])!=set(b[n]):
            result.append(n);continue
        if any(max((abs(x-y) for x,y in zip(a[n][k],b[n][k])),default=0)>tol for k in a[n]):result.append(n)
    return sorted(result)

try:
    hashes=[hashlib.sha256(f.read_bytes()).hexdigest() for f in FILES]
    reference={};results=[]
    for index,file in enumerate(FILES):
        doc=App.openDocument(str(file));base=snapshot(doc)
        for name,prop,value in CASES:
            tag=name+'.'+prop
            save('Progresso_movimentos.json',{'file':index,'case':tag})
            obj=doc.getObject(name)
            assert obj is not None and prop in obj.PropertiesList,tag
            original=getattr(obj,prop)
            original=original.Value if hasattr(original,'Value') else original
            setattr(obj,prop,value)
            doc.recompute()
            state=snapshot(doc)
            changed=differences(base,state)
            if index==0:
                reference[tag]=state
            else:
                diff=differences(reference[tag],state)
                results.append({'input':tag,'value':value,'changed_objects':len(changed),'differences_R49_R50':diff,
                                'meaning':'Same recomputed state; no collision/capacity approval implied'})
            setattr(obj,prop,original)
            doc.recompute()
            reset=differences(base,snapshot(doc))
            assert not reset,(tag,'did not return to base',reset[:10])
        App.closeDocument(doc.Name)
    assert all(not r['differences_R49_R50'] for r in results)
    assert [hashlib.sha256(f.read_bytes()).hexdigest() for f in FILES]==hashes
    save('Verificacao_movimentos.json',{'cases':results,'count':len(results),'all_equal':True,'files_unchanged':True,
                                     'method':'Sequential inputs, recompute, all object Placements and all feature bboxes, return to original state; no files saved.'})
    save('Progresso_movimentos.json',{'stage':'complete','cases':len(results)})
except BaseException:
    save('Erro_movimentos.json',{'error':traceback.format_exc()});traceback.print_exc();sys.stdout.flush();sys.stderr.flush();os._exit(1)
sys.stdout.flush();sys.stderr.flush();os._exit(0)
