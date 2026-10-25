"""Otimiza serializacao BREP sem remover objetos ou alterar geometria.

Executar por freecadcmd.exe. Como o processo nao possui GUI, os dados de
aparencia originais sao transferidos sem alteracao ao pacote salvo pelo motor.
"""
from pathlib import Path
import hashlib
import json
import os
import sys
import time
import traceback
import runpy
import zipfile
import xml.etree.ElementTree as ET
import FreeCAD as App

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
SOURCE=ROOT/'01_Projeto/Gavetas_escritorio_R49_2026-10-24/Guedala_Park_R49_Gavetas_escritorio.FCStd'
TARGET=HERE/'Guedala_Park_R50_Completo_Otimizado.FCStd'
EXPECTED='0d34ab3de1dc273e2db9d5483d7d5bb79352ebec01200540485d68c9e2b8f41e'

def write(name,data):
    (HERE/name).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

def metric(obj):
    sh=obj.Shape
    b=sh.BoundBox
    return {'volume':sh.Volume,'area':sh.Area,'bbox':[b.XMin,b.YMin,b.ZMin,b.XMax,b.YMax,b.ZMax],
            'vertices':sorted([tuple(v.Point) for v in sh.Vertexes]),
            'topology':[len(sh.Solids),len(sh.Shells),len(sh.Faces),len(sh.Wires),len(sh.Edges),len(sh.Vertexes)],
            'placement':list(obj.Placement.toMatrix().A)}

def run():
    assert hashlib.sha256(SOURCE.read_bytes()).hexdigest()==EXPECTED
    assert not TARGET.exists(), 'Candidata ja existe: use verificar_final.py, sem sobrescrever a aparencia ou correcoes posteriores.'
    write('Progresso_binario.json',{'stage':'opening'})
    t=time.perf_counter();doc=App.openDocument(str(SOURCE));source_s=time.perf_counter()-t
    features=[o for o in doc.Objects if o.isDerivedFrom('Part::Feature') and not o.Shape.isNull()]
    write('Progresso_binario.json',{'stage':'snapshot','features':len(features),'open_s':source_s})
    before={o.Name:metric(o) for o in features}
    write('Geometria_antes.json',before)
    write('Progresso_binario.json',{'stage':'saving_binary' if not TARGET.exists() else 'verifying_existing_candidate'})
    pref=App.ParamGet('User parameter:BaseApp/Preferences/Document')
    old=pref.GetBool('SaveBinaryBrep',False)
    pref.SetBool('SaveBinaryBrep',True)
    try:
        save_s=None
        if not TARGET.exists():
            t=time.perf_counter();doc.saveAs(str(TARGET));save_s=time.perf_counter()-t
    finally:
        pref.SetBool('SaveBinaryBrep',old)
    App.closeDocument(doc.Name)
    # All GUI files are opaque bytes. Copy original visual state and all its
    # binary arrays/textures, rather than constructing a new appearance.
    with zipfile.ZipFile(SOURCE) as z:
        original_order=z.namelist()
        src_xml=ET.fromstring(z.read('Document.xml'))
        src_gui=z.read('GuiDocument.xml')
        referenced=set()
        for element in ET.fromstring(src_gui).iter():
            for key,value in element.attrib.items():
                if key.lower() in ('file','filename') and value in z.namelist():
                    referenced.add(value)
        resources={n:z.read(n) for n in referenced|{'GuiDocument.xml'} if n in z.namelist()}
        if 'thumbnails/Thumbnail.png' in z.namelist():resources['thumbnails/Thumbnail.png']=z.read('thumbnails/Thumbnail.png')
    with zipfile.ZipFile(TARGET) as z:
        content={n:z.read(n) for n in z.namelist() if n not in resources}
    content.update(resources)
    with zipfile.ZipFile(TARGET,'w',zipfile.ZIP_DEFLATED,compresslevel=7) as z:
        z.comment=b'FreeCAD Document'
        order=[]
        for n in original_order:
            mapped=n[:-4]+'.bin' if n.endswith('.brp') and n[:-4]+'.bin' in content else n
            if mapped in content:order.append(mapped)
        order += [n for n in content if n not in set(order)]
        for n in order:z.writestr(n,content[n])
    helper=runpy.run_path(str(HERE/'serializacao_binaria.py'))
    helper['preservar_vazios'](TARGET)
    with zipfile.ZipFile(TARGET) as z:
        dest_xml=ET.fromstring(z.read('Document.xml'))
        bins=[n for n in z.namelist() if n.endswith('.bin')]
        assert bins,'SaveBinaryBrep nao suportado nesta versao'
        assert z.read('GuiDocument.xml')==src_gui
    # Object properties, expressions and relationships must be identical.
    def props(xml):
        rows={}
        for obj in xml.findall('./ObjectData/Object'):
            rows[obj.get('name')]={}
            for p in obj.findall('./Properties/Property'):
                # Shape and SuppressedShape keep all maps/metadata. Only the
                # internal serialization filename changes from .brp to .bin.
                if p.get('type')=='Part::PropertyPartShape':
                    for child in p:
                        child.attrib.pop('file',None)
                rows[obj.get('name')][p.get('name')]=ET.tostring(p,encoding='unicode').strip()
        return rows
    a,b=props(src_xml),props(dest_xml)
    differences=[]
    for n in sorted(set(a)|set(b)):
        if n not in a or n not in b:
            differences.append({'id':n,'kind':'missing_object'})
        else:
            for k in sorted(set(a[n])|set(b[n])):
                if a[n].get(k)!=b[n].get(k):differences.append({'id':n,'property':k})
    write('Diferencas_propriedades.json',differences)
    assert not differences, 'Propriedades diferentes: consultar relatorio'
    write('Progresso_binario.json',{'stage':'reopening_binary'})
    t=time.perf_counter();check=App.openDocument(str(TARGET));after_s=time.perf_counter()-t
    geom=[]
    for n,expected in before.items():
        got=metric(check.getObject(n))
        if got['topology']!=expected['topology'] or len(got['vertices'])!=len(expected['vertices']):
            geom.append({'id':n,'kind':'topology'})
            continue
        error=max([abs(got['volume']-expected['volume'])/max(abs(expected['volume']),1),
                   abs(got['area']-expected['area'])/max(abs(expected['area']),1)]+
                  [abs(x-y) for x,y in zip(got['bbox']+got['placement'],expected['bbox']+expected['placement'])]+
                  [abs(x-y) for v,w in zip(got['vertices'],expected['vertices']) for x,y in zip(v,w)])
        if error>1e-7:geom.append({'id':n,'max_error':error})
    write('Diferencas_geometria.json',geom)
    assert not geom,'Geometria diferente'
    report={'source_sha256_before':EXPECTED,'source_sha256_after':hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
            'target_sha256':hashlib.sha256(TARGET.read_bytes()).hexdigest(),'source_bytes':SOURCE.stat().st_size,
            'target_bytes':TARGET.stat().st_size,'objects':len(check.Objects),'geometries_checked':len(before),
            'binary_shapes':len(bins),'properties_differences':len(differences),'geometry_differences':len(geom),
            'gui_xml_identical':True,'gui_resource_files_identical':len(resources),'source_backend_open_s':source_s,
            'target_backend_open_s':after_s,'binary_save_s':save_s,
            'method':'Same backend process; source open first, binary file opened second. Not a controlled GUI comparison.'}
    write('Verificacao_binario.json',report)
    assert report['source_sha256_after']==EXPECTED
    write('Progresso_binario.json',{'stage':'complete',**report})

try:
    run()
except BaseException:
    write('Erro_binario.json',{'error':traceback.format_exc()})
    traceback.print_exc();sys.stdout.flush();sys.stderr.flush();os._exit(1)
sys.stdout.flush();sys.stderr.flush();os._exit(0)
