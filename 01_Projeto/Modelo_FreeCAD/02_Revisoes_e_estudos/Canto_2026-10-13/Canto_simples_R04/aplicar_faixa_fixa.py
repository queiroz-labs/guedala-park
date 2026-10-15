from pathlib import Path
import json,shutil
import FreeCAD as App
import Part
root=(Path(__file__).resolve().parent / '.').resolve()
doc=next(d for d in App.listDocuments().values() if d.FileName and Path(d.FileName).name=='Guedala_Park_R04_Canto_Simples.FCStd')
doc.save();archive=(Path(__file__).resolve().parent / 'Candidato_apoio_quinca.FCStd').resolve()
if not archive.exists():shutil.copy2(doc.FileName,archive)
s=next(o for o in doc.Objects if o.Name.startswith('ControleSimplesR04'))
simple=next(o for o in doc.Objects if o.Label.startswith('Canto R04 - portas independentes'))
group=next(o for o in doc.Objects if o.Label=='Porta B - dobradicas independentes')
ref=lambda alias:s.Name+'.B'+alias
angle=ref('Theta');tx=ref('T4z');ty='-'+ref('T4x');mx,my=193.5,-1032
group.setExpression('Placement.Base.x',f'({mx}+({tx})-{mx}*cos({angle})+({my})*sin({angle}))*1 mm')
group.setExpression('Placement.Base.y',f'({my}+({ty})-{mx}*sin({angle})-({my})*cos({angle}))*1 mm')
group.setExpression('Placement.Rotation.Angle',angle)
for o in group.Group:
    if o.TypeId=='Part::Cylinder':o.Placement.Base.y=-1025.5
    if o.TypeId=='Part::Box':o.Width=271
Ag=next(o for o in doc.Objects if o.Label=='Porta A - dobradicas independentes')
for o in Ag.Group:
    if o.TypeId=='Part::Box':o.Length=271;o.Placement.Base.x=376
source=App.listDocuments().get('Inspecao_Simples_R04')
if source is None:source=App.openDocument(str((Path(__file__).resolve().parent / 'Fontes_STEP_Simples.FCStd').resolve()))
parts=[o for o in source.Objects if o.TypeId=='Part::Feature' and len(o.Shape.Solids)==1]
matrix=App.Matrix();matrix.A11=0;matrix.A12=0;matrix.A13=1;matrix.A21=-1;matrix.A22=0;matrix.A23=0;matrix.A31=0;matrix.A32=-1;matrix.A33=0
for assembly in [o for o in doc.Objects if o.TypeId=='App::Part' and o.Label.startswith('71B3550 - porta B')]:
    assembly.Placement.Base.y=-1032
    for o in assembly.Group:
        index=o.IndiceCorpo if hasattr(o,'IndiceCorpo') else 5
        baked=parts[index].Shape.transformGeometry(parts[index].Shape.Placement.toMatrix());baked.Placement=App.Placement();o.Shape=baked.transformGeometry(matrix)
        if index in [2,3,4]:
            t='Theta' if index==4 else 'Theta'+str(index)
            o.setExpression('Placement.Base.y','-'+ref('T'+str(index)+'x')+' *1 mm')
            o.setExpression('Placement.Rotation.Angle',ref(t))
wall=next(o for o in doc.Objects if o.Label=='Lateral 18 mm de apoio da porta B - proposta');wall.Placement.Base.y=-1050
for name,label,base,dims in [('FaixaQuinaAR04','Faixa fixa A 142 mm - proposta',(232,-650,1),(142,18,306)),('FaixaQuinaBR04','Faixa fixa B 124 mm - proposta',(232,-774,1),(18,124,306))]:
    o=doc.addObject('Part::Box',name);simple.addObject(o);o.Label=label;o.Length,o.Width,o.Height=dims;o.Placement.Base=App.Vector(*base);o.ViewObject.ShapeColor=(.75,.66,.48)
s.set('B4','Portas independentes com faixa fixa na quina');s.set('B6','A/B 271x306x18; faixa fixa 142/124; juntas 2 mm');s.set('B7','86 deg')
s.set('A8','Limitador candidato');s.set('B8','70T3553 de encaixe, 110 para86 graus; conferir montagem')
s.set('B2','0 deg');s.set('B3','0 deg');doc.recompute();doc.save()
metadata=json.loads(((Path(__file__).resolve().parent / 'Montagem_simples.json').resolve()).read_text(encoding='utf-8'));metadata.update({'new_fronts_mm':{'A':[271,306,18],'B':[271,306,18]},'fixed_corner_mm':[142,124],'status':'Proposta com faixa fixa, em conferencia. Limitador86 candidato; sem liberacao de corte.'})
((Path(__file__).resolve().parent / 'Montagem_simples.json').resolve()).write_text(json.dumps(metadata,ensure_ascii=False,indent=2),encoding='utf-8')
result=json.dumps({'invalid':[o.Name for o in doc.Objects if 'Invalid' in o.State]})
