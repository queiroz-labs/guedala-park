"""Suporte de gravacao binaria, preservando formas vazias no formato ASCII.

SaveBinaryBrep e recurso nativo do FreeCAD. Nao simplifica topologia nem
substitui objetos. O tratamento de formas vazias evita falha do leitor 1.1.4.
"""
from pathlib import Path
import hashlib
import os
import tempfile
import xml.etree.ElementTree as ET
import zipfile


def preservar_vazios(path):
    path=Path(path)
    with zipfile.ZipFile(path) as z:
        content={n:z.read(n) for n in z.namelist()}
    original_order=list(content)
    renamed={}
    xml=ET.fromstring(content['Document.xml'])
    fixes=[]
    for obj in xml.findall('./ObjectData/Object'):
        for prop in obj.findall('./Properties/Property'):
            if prop.get('type')!='Part::PropertyPartShape' or not len(prop):continue
            shape=prop[0];name=shape.get('file')
            if name and name.endswith('.bin') and content[name]==b'':
                ascii_name=name[:-4]+'.brp'
                content[ascii_name]=b''
                shape.set('file',ascii_name)
                del content[name]
                renamed[name]=ascii_name
                fixes.append((obj.get('name'),prop.get('name')))
    if fixes:
        content['Document.xml']=ET.tostring(xml,encoding='utf-8',xml_declaration=True)
        handle,tmp=tempfile.mkstemp(prefix=path.stem+'_',suffix='.FCStd',dir=path.parent)
        os.close(handle)
        try:
            with zipfile.ZipFile(tmp,'w',zipfile.ZIP_DEFLATED,compresslevel=7) as z:
                z.comment=b'FreeCAD Document'
                order=[renamed.get(n,n) for n in original_order]
                order += [n for n in content if n not in set(order)]
                for name in order:z.writestr(name,content[name])
            # ZIP integrity before replacing only the explicitly saved file.
            with zipfile.ZipFile(tmp) as z:assert z.testzip() is None
            os.replace(tmp,path)
        finally:
            if Path(tmp).exists():Path(tmp).unlink()
    return fixes


def salvar_documento(doc,path):
    import FreeCAD as App
    path=Path(path)
    pref=App.ParamGet('User parameter:BaseApp/Preferences/Document')
    previous=pref.GetBool('SaveBinaryBrep',False)
    try:
        pref.SetBool('SaveBinaryBrep',True)
        doc.saveAs(str(path))
    finally:
        pref.SetBool('SaveBinaryBrep',previous)
    fixes=preservar_vazios(path)
    if App.GuiUp:
        import FreeCADGui as Gui
        # Full native save has committed every document/view property. ZIP
        # normalization only renames empty payloads, without editing the model.
        assert not any('Touched' in obj.State for obj in doc.Objects)
        Gui.getDocument(doc.Name).Modified=False
    return {'file':str(path),'bytes':path.stat().st_size,'empty_shapes':len(fixes),
            'sha256':hashlib.sha256(path.read_bytes()).hexdigest()}
