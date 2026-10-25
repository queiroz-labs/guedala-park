"""Teste pequeno do salvamento e da reabertura nativos, sem alterar o projeto."""
from pathlib import Path
import json
import os
import runpy
import sys
import traceback
import FreeCAD as App

HERE=Path(__file__).resolve().parent
try:
    helper=runpy.run_path(str(HERE/'serializacao_binaria.py'))
    folder=HERE.parents[2]/'outputs/freecad-performance-2026-10-24'
    folder.mkdir(parents=True,exist_ok=True)
    dest=folder/'Teste_salvamento.FCStd'
    d=App.newDocument('TesteSalvarBinario')
    box=d.addObject('Part::Box','Chapa')
    box.Length=661;box.Width=312;box.Height=18
    suppressed=d.addObject('PartDesign::Feature','FormaVazia')
    d.recompute()
    pref=App.ParamGet('User parameter:BaseApp/Preferences/Document')
    original=pref.GetBool('SaveBinaryBrep',False)
    report=helper['salvar_documento'](d,dest)
    assert pref.GetBool('SaveBinaryBrep',False)==original
    App.closeDocument(d.Name)
    d=App.openDocument(str(dest))
    assert len(d.Objects)==2
    assert abs(d.Chapa.Shape.Volume-661*312*18)<1e-6
    assert d.FormaVazia.Shape.isNull() and d.FormaVazia.SuppressedShape.isNull()
    assert not any('Invalid' in o.State for o in d.Objects)
    (HERE/'Verificacao_salvamento.json').write_text(json.dumps({'passed':True,'preferences_restored':True,
        'empty_shapes_reopen':True,'box_geometry_preserved':True,'report':report},indent=2),encoding='utf-8')
except BaseException:
    (HERE/'Erro_salvamento.txt').write_text(traceback.format_exc(),encoding='utf-8')
    traceback.print_exc();sys.stdout.flush();sys.stderr.flush();os._exit(1)
sys.stdout.flush();sys.stderr.flush();os._exit(0)
