"""Run inside an isolated FreeCAD GUI. Changes only appearance, never recomputes."""
from pathlib import Path
import json,hashlib,collections,runpy
import FreeCAD as App,FreeCADGui as Gui

HERE=Path(__file__).resolve().parent
ROOT=HERE.parent.parent
SOURCE=ROOT/'01_Projeto/Consolidacao_R45_2026-10-23/Guedala_Park_R45_Consolidado.FCStd'
TARGET=HERE/'Guedala_Park_R45_Cores_R16.FCStd'
RENDERED=HERE/'.cores-renderizadas.FCStd'

def hexcolor(value):
    return '#'+''.join(f'{round(c*255):02x}' for c in value[:3])

def run():
    plan=json.loads((HERE/'Plano_de_cores.json').read_text(encoding='utf8'))
    assert hashlib.sha256(SOURCE.read_bytes()).hexdigest()==plan['sourceSHA256']
    assert not TARGET.exists(),'Preserve an existing output; generate a fresh revision explicitly.'
    doc=App.openDocument(str(SOURCE))
    original_visibility={o.Name:o.ViewObject.Visibility for o in doc.Objects}
    report={'revision':'R16','sourceSHA256':plan['sourceSHA256'],'version':App.Version(),'objects':{},'geometryRecomputed':False,'continuousCurveExceptions':[]}
    expected={}
    for name,spec in plan['objects'].items():
        obj=doc.getObject(name)
        assert obj is not None and not obj.Shape.isNull(),name
        shape=obj.Shape.copy();shape.Placement=obj.getGlobalPlacement()
        count=len(shape.Faces)
        old=obj.ViewObject.ShapeAppearance
        assert len(old) in (1,count),(name,len(old),count)
        if 'expectedFaces' in spec:assert count==spec['expectedFaces'],name
        materials=[];colors=[]
        for i,face in enumerate(shape.Faces):
            if 'faceRanges' in spec:
                key=next(key for start,end,key in spec['faceRanges'] if start<=i<end)
            else:
                key=spec['material']
                if spec.get('inner'):
                    if type(face.Surface).__name__=='Plane':
                        normal=face.normalAt(0,0)
                        scores=[(-normal.x,normal.z,normal.y)[spec['axis']]*spec['outward']]
                    else:
                        vertices,triangles=face.tessellate(1.2);scores=[]
                        for a,b,c in triangles:
                            n=(vertices[b]-vertices[a]).cross(vertices[c]-vertices[a]);n.normalize()
                            scores.append((-n.x,n.z,n.y)[spec['axis']]*spec['outward'])
                    assert scores,(name,i,'Face without normal samples')
                    if all(score<-.5 for score in scores):key=spec['inner']
                    elif any(score<-.5 for score in scores):
                        # Do not split CAD faces to reproduce a tessellation-only
                        # color boundary inside holes/curves. Keep exterior color.
                        report['continuousCurveExceptions'].append({'object':name,'face':i+1,'material':key,'reason':'One continuous curved CAD face spans both normal directions; exterior reference color retained, machining finish not specified.'})
            color=plan['palette'].get(key,key)
            assert len(color)==7 and color.startswith('#'),(name,key)
            # Each property read returns independent Material values; retain every
            # field except diffuse RGB, including transparency and surface settings.
            m=obj.ViewObject.ShapeAppearance[0 if len(old)==1 else i]
            rgb=tuple(int(color[k:k+2],16)/255 for k in (1,3,5))
            m.DiffuseColor=rgb+(m.DiffuseColor[3],)
            materials.append(m);colors.append(color.lower())
        obj.ViewObject.ShapeAppearance=tuple(materials)
        expected[name]=colors
        report['objects'][name]={'faces':count,'colors':dict(collections.Counter(colors)),'changed':colors!=[hexcolor(old[0 if len(old)==1 else i].DiffuseColor) for i in range(count)]}
    assert original_visibility=={o.Name:o.ViewObject.Visibility for o in doc.Objects}
    assert not RENDERED.exists(),'Preserve an existing intermediate output.'
    doc.saveAs(str(RENDERED))
    App.closeDocument(doc.Name)
    runpy.run_path(str(HERE/'preservar_geometria.py'))['assemble'](SOURCE,RENDERED,TARGET,list(expected))
    check=App.openDocument(str(TARGET))
    assert original_visibility=={o.Name:o.ViewObject.Visibility for o in check.Objects}
    for name,colors in expected.items():
        mats=check.getObject(name).ViewObject.ShapeAppearance
        actual=[hexcolor(mats[0 if len(mats)==1 else i].DiffuseColor) for i in range(len(colors))]
        assert actual==colors,(name,actual,colors)
    report.update(reopenedColorsMatch=True,visibilityPreserved=True,targetSHA256=hashlib.sha256(TARGET.read_bytes()).hexdigest(),objectCount=len(check.Objects),mappedObjects=len(expected),changedObjects=sum(r['changed'] for r in report['objects'].values()),mappedFaces=sum(r['faces'] for r in report['objects'].values()))
    (HERE/'Verificacao_cores.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8')
    assert hashlib.sha256(SOURCE.read_bytes()).hexdigest()==plan['sourceSHA256']
    RENDERED.unlink() # Only the temporary file created by this execution.
    return check,report

if __name__=='__main__':
    document,report=run()
    print('Appearance verified:',report['mappedObjects'],'objects;',report['mappedFaces'],'faces.')
