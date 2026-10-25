"""Audita a candidata final por leitura, sem regravar o FCStd."""
from pathlib import Path
import hashlib
import json
import os
import sys
import time
import traceback
import zipfile
import xml.etree.ElementTree as ET
import FreeCAD as App

HERE=Path(__file__).resolve().parent
SOURCE=HERE.parent/'Gavetas_escritorio_R49_2026-10-24/Guedala_Park_R49_Gavetas_escritorio.FCStd'
TARGET=HERE/'Guedala_Park_R50_Completo_Otimizado.FCStd'
try:
    before=json.loads((HERE/'Geometria_antes.json').read_text(encoding='utf-8'))
    t=time.perf_counter();doc=App.openDocument(str(TARGET));open_s=time.perf_counter()-t
    differences=[]
    for name,old in before.items():
        obj=doc.getObject(name);sh=obj.Shape;b=sh.BoundBox
        topology=[len(sh.Solids),len(sh.Shells),len(sh.Faces),len(sh.Wires),len(sh.Edges),len(sh.Vertexes)]
        vertices=sorted([tuple(v.Point) for v in sh.Vertexes])
        numeric=[sh.Volume/max(1,abs(old['volume'])),sh.Area/max(1,abs(old['area']))]+[b.XMin,b.YMin,b.ZMin,b.XMax,b.YMax,b.ZMax]+list(obj.Placement.toMatrix().A)+[x for v in vertices for x in v]
        expected=[old['volume']/max(1,abs(old['volume'])),old['area']/max(1,abs(old['area']))]+old['bbox']+old['placement']+[x for v in old['vertices'] for x in v]
        if topology!=old['topology'] or len(numeric)!=len(expected) or max(abs(a-b) for a,b in zip(numeric,expected))>1e-7:differences.append(name)
    assert not differences,differences
    with zipfile.ZipFile(SOURCE) as a,zipfile.ZipFile(TARGET) as b:
        assert b.testzip() is None
        assert a.namelist().index('GuiDocument.xml')==b.namelist().index('GuiDocument.xml')
        docs=[ET.fromstring(z.read('Document.xml')) for z in [a,b]]
    def properties(xml):
        rows={}
        for obj in xml.findall('./ObjectData/Object'):
            rows[obj.get('name')]={}
            for prop in obj.findall('./Properties/Property'):
                if prop.get('type')=='Part::PropertyPartShape':
                    for child in prop:child.attrib.pop('file',None)
                rows[obj.get('name')][prop.get('name')]=ET.tostring(prop,encoding='unicode').strip()
        return rows
    original,final=map(properties,docs)
    assert set(original)==set(final)
    propdiff=[{'id':name,'property':key} for name in original for key in set(original[name])|set(final[name])
              if original[name].get(key)!=final[name].get(key)]
    expected=set(json.loads((HERE/'Banheiro_referencias_ocultas.json').read_text(encoding='utf-8'))['hidden_references'])
    assert {(x['id'],x['property']) for x in propdiff}=={(n,'Visibility') for n in expected},propdiff
    (HERE/'Diferencas_propriedades_finais.json').write_text(json.dumps(propdiff,ensure_ascii=False,indent=2),encoding='utf-8')
    report=json.loads((HERE/'Verificacao_binario.json').read_text(encoding='utf-8'))
    assert hashlib.sha256(SOURCE.read_bytes()).hexdigest()==report['source_sha256_before']
    report.update(target_sha256=hashlib.sha256(TARGET.read_bytes()).hexdigest(),target_bytes=TARGET.stat().st_size,
                  final_target_backend_open_s=open_s,final_geometry_rechecked=len(before),final_geometry_differences=differences,
                  GUI_resource_order_matches_source=True,objects=len(doc.Objects),
                  final_intentional_property_differences=propdiff,unexpected_final_property_differences=0)
    (HERE/'Verificacao_binario.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
except BaseException:
    (HERE/'Erro_verificacao_final.txt').write_text(traceback.format_exc(),encoding='utf-8');traceback.print_exc();sys.stdout.flush();sys.stderr.flush();os._exit(1)
sys.stdout.flush();sys.stderr.flush();os._exit(0)
