"""Transfer FreeCAD-generated appearance records without resaving model data.

No material binary format is interpreted here. FreeCAD writes and verifies the
material records; the original document, geometry and other GUI properties stay
byte-for-byte intact. The assembled file must then be reopened in FreeCAD.
"""
import zipfile,collections,xml.etree.ElementTree as ET
from pathlib import Path

def assemble(source,rendered,target,names):
    assert source!=target and rendered!=target
    with zipfile.ZipFile(source) as original,zipfile.ZipFile(rendered) as generated:
        source_gui=ET.fromstring(original.read('GuiDocument.xml'))
        gui=ET.fromstring(generated.read('GuiDocument.xml'))
        references=collections.Counter(m.attrib['file'] for m in source_gui.findall(".//Property[@name='ShapeAppearance']/MaterialList"))
        replacements={}
        for name in names:
            view=gui.find(f".//ViewProvider[@name='{name}']")
            prop=view.find("./Properties/Property[@name='ShapeAppearance']")
            material=prop.find('MaterialList')
            source_view=source_gui.find(f".//ViewProvider[@name='{name}']")
            source_material=source_view.find("./Properties/Property[@name='ShapeAppearance']/MaterialList")
            filename=source_material.attrib['file']
            assert references[filename]==1,(name,'Shared material requires explicit review')
            assert source_material.attrib['version']==material.attrib['version']
            replacements[filename]=generated.read(material.attrib['file'])
        # Keep original names and entry order: FreeCAD restores registered files
        # sequentially. Both XML documents and every unrelated entry stay intact.
        with zipfile.ZipFile(target,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as final:
            for entry in original.infolist():
                final.writestr(entry,replacements.get(entry.filename,original.read(entry.filename)))
    with zipfile.ZipFile(source) as original,zipfile.ZipFile(target) as final:
        assert final.testzip() is None
        for name in original.namelist():
            if name not in replacements:assert original.read(name)==final.read(name),name
    return len(replacements)
