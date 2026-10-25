"""Serie unica de reaberturas com GUI, ja com a integracao corrigida.

Alterna R49/R50 no mesmo processo e termina com a R50 aberta.
"""
from pathlib import Path
import json
import runpy
import traceback
from PySide import QtCore
import FreeCAD as App

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
R49=ROOT/'01_Projeto/Gavetas_escritorio_R49_2026-10-24/Guedala_Park_R49_Gavetas_escritorio.FCStd'
R50=HERE/'Guedala_Park_R50_Completo_Otimizado.FCStd'
JOBS=[('r49_corrigida_01',R49),('r50_corrigida_01',R50),('r50_corrigida_02',R50),('r49_corrigida_02',R49),('r50_corrigida_03',R50)]
if getattr(App,'_guedala_benchmark_final',False):
    JOBS=[(f'r50_final_0{i}',R50) for i in [1,2,3]]

def next_job(index=0):
    try:
        if index==len(JOBS):
            (HERE/'Serie_concluida.json').write_text(json.dumps({'complete':True,'tags':[x[0] for x in JOBS]}),encoding='utf-8')
            return
        tag,file=JOBS[index]
        (HERE/'job.json').write_text(json.dumps({'tag':tag,'mode':'original','profile':False,'file':str(file)}),encoding='utf-8')
        runpy.run_path(str(HERE/'medir_abertura.py'))
        result=json.loads((HERE/f'Tempo_{tag}.json').read_text(encoding='utf-8'))
        assert 'error' not in result,result.get('error')
        QtCore.QTimer.singleShot(300,lambda:next_job(index+1))
    except BaseException:
        (HERE/'Erro_serie.txt').write_text(traceback.format_exc(),encoding='utf-8')

App._guedala_benchmark_next=next_job
QtCore.QTimer.singleShot(200,next_job)
