from pathlib import Path
import shutil,json
import FreeCAD as App
import Part
root=(Path(__file__).resolve().parent / '.').resolve()
doc=next(d for d in App.listDocuments().values() if d.FileName and Path(d.FileName).name=='Guedala_Park_R04_Canto_Simples.FCStd')
doc.save();archive=(Path(__file__).resolve().parent / 'Candidato_apoio_extremidade.FCStd').resolve()
if not archive.exists():shutil.copy2(doc.FileName,archive)
s=next(o for o in doc.Objects if o.Name.startswith('ControleSimplesR04'))
group=next(o for o in doc.Objects if o.Label=='Porta B - dobradicas independentes')
ref=lambda alias:s.Name+'.B'+alias
angle='-'+ref('Theta');tx=ref('T4z');ty=ref('T4x');mx,my=193.5,-666
group.setExpression('Placement.Base.x',f'({mx}+({tx})-{mx}*cos({angle})+({my})*sin({angle}))*1 mm')
group.setExpression('Placement.Base.y',f'({my}+({ty})-{mx}*sin({angle})-({my})*cos({angle}))*1 mm')
group.setExpression('Placement.Rotation.Angle',angle)
for o in group.Group:
    if o.TypeId=='Part::Cylinder':o.Placement.Base.y=-672.5
source=App.listDocuments().get('Inspecao_Simples_R04')
if source is None:source=App.openDocument(str((Path(__file__).resolve().parent / 'Fontes_STEP_Simples.FCStd').resolve()))
parts=[o for o in source.Objects if o.TypeId=='Part::Feature' and len(o.Shape.Solids)==1]
matrix=App.Matrix();matrix.A11=0;matrix.A12=0;matrix.A13=1;matrix.A21=1;matrix.A22=0;matrix.A23=0;matrix.A31=0;matrix.A32=1;matrix.A33=0
for assembly in [o for o in doc.Objects if o.TypeId=='App::Part' and o.Label.startswith('71B3550 - porta B')]:
    assembly.Placement.Base.y=-666
    for o in assembly.Group:
        index=o.IndiceCorpo if hasattr(o,'IndiceCorpo') else 5
        baked=parts[index].Shape.transformGeometry(parts[index].Shape.Placement.toMatrix());baked.Placement=App.Placement()
        o.Shape=baked.transformGeometry(matrix)
        if index in [2,3,4]:
            t='Theta' if index==4 else 'Theta'+str(index)
            o.setExpression('Placement.Base.y',ref('T'+str(index)+'x')+' *1 mm')
            o.setExpression('Placement.Rotation.Angle','-'+ref(t))
wall=next(o for o in doc.Objects if o.Label=='Lateral 18 mm de apoio da porta B - proposta');wall.Placement.Base.y=-666
s.set('B4','Abrir B antes de A; fechar A antes de B')
doc.recompute();doc.save()
result=json.dumps({'invalid':[o.Name for o in doc.Objects if 'Invalid' in o.State]})
